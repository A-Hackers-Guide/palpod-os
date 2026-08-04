#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# scripts/pair-remote-device.sh — register a machine for Pod-driven remote
# desktop.
#
# Usage:
#   ./scripts/pair-remote-device.sh <display-name> <device-type> [rustdesk-id]
#
# Examples:
#   ./scripts/pair-remote-device.sh "Mark's Office Mac" mac 123456789
#   ./scripts/pair-remote-device.sh "Kids' iPad"        ios
#
# What it does:
#   1. Validates arguments (device-type must be one of mac/windows/linux/ios/android).
#   2. Mints a 256-bit auth token — the shared secret pal-web will require on
#      every command sent to this device.
#   3. Inserts (or upserts on rustdesk_id) a row into the `remote_devices`
#      Postgres table via the running postgres container.
#   4. Prints the manual setup steps the user needs to complete on the client
#      device.
#
# NOT covered here (pal-web's job):
#   * Flipping ai_control_allowed = true. That toggle must happen from the
#     pal-web UI where the user's household identity is known — pairing a
#     device from the CLI never implicitly grants AI control.
#   * Setting owner_user_id. Left NULL by this script; pal-web assigns the
#     current user on first UI visit.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

if [[ $# -lt 2 ]]; then
  cat >&2 <<EOF
Usage: $0 <display-name> <device-type> [rustdesk-id]
  device-type: mac | windows | linux | ios | android
  rustdesk-id: the 9-digit ID shown at the top of the RustDesk client
               (optional — omit if the device isn't online yet; you can
                run this script again once you have it).
EOF
  exit 1
fi

DISPLAY_NAME="$1"
DEVICE_TYPE="$2"
RUSTDESK_ID="${3:-}"

case "$DEVICE_TYPE" in
  mac|windows|linux|ios|android) ;;
  *) echo "[!] Invalid device-type: $DEVICE_TYPE" >&2; exit 1 ;;
esac

if [[ -n "$RUSTDESK_ID" && ! "$RUSTDESK_ID" =~ ^[0-9]{9,10}$ ]]; then
  echo "[!] RustDesk IDs are 9–10 digits. Got: $RUSTDESK_ID" >&2
  exit 1
fi

# shellcheck source=/dev/null
set -a; source .env; set +a
: "${POSTGRES_USER:?POSTGRES_USER is unset in .env}"
: "${POSTGRES_DB:?POSTGRES_DB is unset in .env}"

# --- Mint the auth token -----------------------------------------------------
AUTH_TOKEN=$(openssl rand -hex 32)

# --- Insert / upsert the row -------------------------------------------------
# We use printf | psql -v so the values are passed as psql variables and
# quoted safely — no shell interpolation into the SQL statement itself.
psql_out=$(docker exec -i postgres psql \
  -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" \
  -v ON_ERROR_STOP=1 \
  -v display_name="${DISPLAY_NAME}" \
  -v device_type="${DEVICE_TYPE}" \
  -v rustdesk_id="${RUSTDESK_ID}" \
  -v auth_token="${AUTH_TOKEN}" \
  -tA <<'SQL'
INSERT INTO remote_devices (display_name, device_type, rustdesk_id, auth_token)
VALUES (
  :'display_name',
  :'device_type',
  NULLIF(:'rustdesk_id', ''),
  :'auth_token'
)
ON CONFLICT (rustdesk_id) DO UPDATE
  SET display_name = EXCLUDED.display_name,
      device_type  = EXCLUDED.device_type,
      auth_token   = EXCLUDED.auth_token,
      last_seen_at = NOW()
RETURNING id;
SQL
)

DEVICE_UUID="${psql_out//[$'\r\n ']/}"

# --- Fetch (or hint at) the RustDesk public key ------------------------------
PUB_KEY_FILE="${REPO_DIR}/data/rustdesk-keys/id_ed25519.pub"
if [[ -f "$PUB_KEY_FILE" ]]; then
  PUB_KEY=$(cat "$PUB_KEY_FILE")
else
  PUB_KEY="(not generated yet — run ./configs/rustdesk/generate-keys.sh)"
fi

POD_HOST="${PALPOD_HOSTNAME:-palpod}.${PALPOD_DOMAIN:-local}"

# --- Report ------------------------------------------------------------------
cat <<EOF

──────────────────────────────────────────────────────────────────────────────
Registered remote device:
  UUID:        ${DEVICE_UUID}
  Name:        ${DISPLAY_NAME}
  Type:        ${DEVICE_TYPE}
  RustDesk ID: ${RUSTDESK_ID:-<not yet known>}
  Auth token:  ${AUTH_TOKEN}
  AI control:  DISABLED (toggle in pal-web → Settings → Remote Devices)

On the ${DEVICE_TYPE} device:
  1. Install the RustDesk client (see configs/rustdesk/README.md).
  2. Open Settings → Network → ID/Relay Server and set:
       ID Server    ${POD_HOST}:21116
       Relay Server ${POD_HOST}:21117
       Key          ${PUB_KEY}
  3. Restart the client. Note the 9-digit ID it displays.
  4. If you left rustdesk-id blank above, re-run:
       ./scripts/pair-remote-device.sh "${DISPLAY_NAME}" ${DEVICE_TYPE} <that-id>

In pal-web (https://pod.${PALPOD_DOMAIN:-palpod.local}):
  * Open Settings → Remote Devices — the entry will appear immediately.
  * Assign an owner (household member).
  * If you want the Pod to click/type on this device, flip Allow AI control.

──────────────────────────────────────────────────────────────────────────────
EOF

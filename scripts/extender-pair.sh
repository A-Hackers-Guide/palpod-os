#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# scripts/extender-pair.sh — manual pairing CLI.
#
# Usage:
#   ./scripts/extender-pair.sh <mac> <ip> [role]
#
# Example:
#   sudo ./scripts/extender-pair.sh aa:bb:cc:11:22:33 10.0.5.42 mic-array
#
# Normal pairing goes through mDNS → POST /api/pair (see docs/EXTENDER_PAIRING.md).
# This CLI exists for the debug case where mDNS doesn't work or you want to
# pre-provision an extender before it comes online.
#
# What it does:
#   1. Validates arguments.
#   2. Inserts the extender_registry row directly via `psql` inside the
#      postgres container.
#   3. Signs a JWT using the JWT secret from .env.
#   4. Prints the JWT + a one-liner to `scp` it onto the extender.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

if [[ $# -lt 2 ]]; then
  cat >&2 <<EOF
Usage: $0 <mac> <ip> [role]
Roles: unassigned | media-cache | game-node | mic-array | display | storage
EOF
  exit 1
fi

MAC="$1"
IP="$2"
ROLE="${3:-unassigned}"

if [[ ! "$MAC" =~ ^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$ ]]; then
  echo "[!] Invalid MAC: $MAC" >&2; exit 1
fi
case "$ROLE" in
  unassigned|media-cache|game-node|mic-array|display|storage) ;;
  *) echo "[!] Invalid role: $ROLE" >&2; exit 1 ;;
esac

# shellcheck source=/dev/null
set -a; source .env; set +a
: "${PAL_WEB_JWT_SECRET:?PAL_WEB_JWT_SECRET is unset in .env}"

# --- Sign the JWT ------------------------------------------------------------
# We deliberately don't shell out to Node here; the primary Pod signs with
# HS256 which is trivial to build from openssl + base64url.
IAT=$(date +%s)
EXP=$((IAT + 60*60*24*365))
JTI=$(openssl rand -hex 16)
HDR_JSON='{"alg":"HS256","typ":"JWT"}'
PAYLOAD_JSON=$(cat <<EOF
{"iss":"palpod-primary","sub":"${MAC}","role":"${ROLE}","iat":${IAT},"exp":${EXP},"jti":"${JTI}"}
EOF
)
b64url() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }
HDR=$(printf '%s' "$HDR_JSON" | b64url)
PAY=$(printf '%s' "$PAYLOAD_JSON" | b64url)
SIG=$(printf '%s.%s' "$HDR" "$PAY" \
  | openssl dgst -binary -sha256 -hmac "$PAL_WEB_JWT_SECRET" \
  | b64url)
JWT="${HDR}.${PAY}.${SIG}"
JWT_HASH=$(printf '%s' "$JWT" | openssl dgst -sha256 -binary | openssl base64 -A)

# --- Insert the row ----------------------------------------------------------
docker exec -i postgres psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" >/dev/null <<SQL
INSERT INTO extender_registry (mac, ip, role, jwt_hash)
VALUES ('${MAC}', '${IP}', '${ROLE}', '${JWT_HASH}')
ON CONFLICT (mac) DO UPDATE
  SET ip = EXCLUDED.ip,
      role = EXCLUDED.role,
      jwt_hash = EXCLUDED.jwt_hash,
      last_seen = NOW();
SQL

# --- Report ------------------------------------------------------------------
cat <<EOF

Paired extender:
  MAC:   ${MAC}
  IP:    ${IP}
  Role:  ${ROLE}

JWT (paste into /var/lib/palpod-extender/jwt on the device):
${JWT}

One-liner for the extender's admin:
  scp -o StrictHostKeyChecking=accept-new \\
      <(echo '${JWT}') \\
      root@${IP}:/var/lib/palpod-extender/jwt

EOF

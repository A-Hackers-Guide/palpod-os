#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# configs/rustdesk/generate-keys.sh — mint (or reveal) the RustDesk keypair.
#
# RustDesk hbbs/hbbr sign every peer handshake with an Ed25519 keypair. The
# key lives on disk at ./data/rustdesk-keys/id_ed25519{,.pub}. Clients must
# be pinned to the *public* key or hbbs will reject them.
#
# This script is idempotent:
#   * If no keypair exists, it generates a fresh Ed25519 pair.
#   * If one already exists, it leaves it alone and just prints the public
#     half so you can copy it into a client config.
#
# It does NOT need root — the keys must be readable by the rustdesk-hbbs
# container process (uid 0 inside the container), but running as your own
# user on the host is fine because the container mounts the directory rw.
#
# Usage:
#   ./configs/rustdesk/generate-keys.sh          # generate if missing, print pub
#   ./configs/rustdesk/generate-keys.sh --force  # regenerate (invalidates all clients!)
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
KEY_DIR="${REPO_DIR}/data/rustdesk-keys"
PRIV="${KEY_DIR}/id_ed25519"
PUB="${KEY_DIR}/id_ed25519.pub"

FORCE=0
if [[ "${1:-}" == "--force" ]]; then
  FORCE=1
fi

mkdir -p "${KEY_DIR}"
chmod 700 "${KEY_DIR}"

if [[ -f "${PRIV}" && -f "${PUB}" && "${FORCE}" -eq 0 ]]; then
  echo "[i] Existing keypair found at ${KEY_DIR} — leaving it in place."
else
  if [[ "${FORCE}" -eq 1 ]]; then
    echo "[!] --force: overwriting existing keypair. Every previously-paired"
    echo "    client will now report Key mismatch and must be re-pointed."
    rm -f "${PRIV}" "${PUB}"
  fi
  echo "[+] Generating a fresh Ed25519 keypair at ${KEY_DIR}..."
  # -N '' → empty passphrase (hbbs cannot enter one at boot)
  # -q    → quiet
  ssh-keygen -t ed25519 -f "${PRIV}" -N '' -q -C "palpod-rustdesk"
  chmod 600 "${PRIV}"
  chmod 644 "${PUB}"
fi

cat <<EOF

──────────────────────────────────────────────────────────────────────────────
RustDesk public key (paste this into each client's Settings → Network → Key):

$(cat "${PUB}")

Files:
  private key: ${PRIV}   (never leaves the Pod)
  public key : ${PUB}

Next steps:
  1. docker compose up -d rustdesk-hbbs rustdesk-hbbr
  2. Install the RustDesk client on the machine you want to reach.
  3. Point it at palpod.local:21116 (ID) + palpod.local:21117 (relay).
  4. Paste the public key above into the client's "Key" field.
  5. On the Pod: ./scripts/pair-remote-device.sh "<display name>" <type> <9-digit-id>
──────────────────────────────────────────────────────────────────────────────
EOF

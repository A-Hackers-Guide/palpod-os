#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# PALPod OS — uninstaller.
#
# Stops the compose stack, optionally removes named volumes (Postgres,
# Plex config, TLS certs, etc.), and optionally removes the data root
# (/var/lib/palpod by default).
#
# Two explicit prompts protect user data — no --force flag by design.
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

if [[ -f .env ]]; then
  set -a; source .env; set +a
fi
DATA_ROOT="${PALPOD_DATA_ROOT:-/var/lib/palpod}"

echo "This will stop every PAL Pod container."
read -rp "Continue? [y/N]: " ans
[[ "${ans,,}" == "y" ]] || { echo "Aborted."; exit 0; }

docker compose down --remove-orphans
echo "Stack stopped."

read -rp "Also DELETE named docker volumes (Postgres data, Plex config, certs…)? [y/N]: " ans
if [[ "${ans,,}" == "y" ]]; then
  docker compose down -v
  echo "Named volumes removed."
fi

read -rp "Also DELETE the data root at $DATA_ROOT? This is destructive. [y/N]: " ans
if [[ "${ans,,}" == "y" ]]; then
  if command -v zfs >/dev/null 2>&1 && zfs list "$DATA_ROOT" >/dev/null 2>&1; then
    read -rp "$DATA_ROOT is a ZFS dataset. Really destroy it and every snapshot? [y/N]: " ans2
    if [[ "${ans2,,}" == "y" ]]; then
      sudo zfs destroy -r "$DATA_ROOT"
      echo "ZFS dataset destroyed."
    fi
  else
    sudo rm -rf "$DATA_ROOT"
    echo "$DATA_ROOT removed."
  fi
fi

echo "Done. .env and configs/ were left in place — remove them manually if desired."

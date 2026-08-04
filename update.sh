#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# PALPod OS — updater.
#
#   1. git pull (with a stash-then-pop if the tree is dirty).
#   2. docker compose pull (fetch newer image digests).
#   3. docker compose up -d (recreate any container whose image changed).
#   4. docker image prune -f (reclaim disk).
#
# Safe to run under cron / systemd timer — exits non-zero on error.
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

echo "[+] Updating PAL Pod OS…"

DIRTY=0
if ! git diff --quiet || ! git diff --cached --quiet; then
  DIRTY=1
  echo "[!] Local changes present — stashing before pull."
  git stash push -u -m "palpod-update-$(date +%s)"
fi

git pull --ff-only

if [[ $DIRTY -eq 1 ]]; then
  echo "[+] Restoring stashed changes."
  git stash pop || echo "[!] Stash could not be applied cleanly — resolve manually."
fi

docker compose pull
docker compose up -d
docker image prune -f

echo "[+] Update complete. Current versions:"
docker compose ps

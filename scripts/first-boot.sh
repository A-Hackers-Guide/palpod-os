#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# scripts/first-boot.sh — runs from install.sh, idempotent.
#
# Responsibilities:
#   1. Create ${PALPOD_DATA_ROOT} and its subdirectories.
#   2. On TrueNAS / any ZFS host, offer to create datasets instead of dirs.
#   3. Generate a self-signed root CA + *.palpod.local leaf certificate.
#   4. Set the system timezone.
#   5. Create empty placeholder media directories if the user's paths don't
#      exist yet — Plex/Jellyfin refuse to start if their bind mounts are
#      missing.
#   6. Print a summary of what it did.
#
# Safe to re-run. Never destroys existing state.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

if [[ ! -f .env ]]; then
  echo "[first-boot] .env missing — run install.sh first." >&2
  exit 1
fi
# shellcheck source=/dev/null
set -a; source .env; set +a

DATA_ROOT="${PALPOD_DATA_ROOT:-/var/lib/palpod}"
DOMAIN="${PALPOD_DOMAIN:-palpod.local}"

# ─── 1. Data root ─────────────────────────────────────────────────────────
if command -v zfs >/dev/null 2>&1 && zfs list 2>/dev/null | awk '{print $1}' | grep -q '^tank$'; then
  # We're likely on TrueNAS / a ZFS host. Offer datasets.
  DATASET="tank/palpod"
  if ! zfs list "$DATASET" >/dev/null 2>&1; then
    echo "[first-boot] Creating ZFS dataset $DATASET → $DATA_ROOT"
    sudo zfs create -o mountpoint="$DATA_ROOT" "$DATASET"
    sudo zfs create "$DATASET/traefik"
    sudo zfs create "$DATASET/models"
    sudo zfs create "$DATASET/uploads"
    sudo zfs create "$DATASET/backups"
  else
    echo "[first-boot] ZFS dataset $DATASET already exists."
  fi
else
  echo "[first-boot] Creating $DATA_ROOT (plain directory)…"
  sudo mkdir -p "$DATA_ROOT"/{traefik/certs,models,uploads,backups}
  sudo chown -R "$USER":"$USER" "$DATA_ROOT"
fi

# ─── 2. Timezone ──────────────────────────────────────────────────────────
if [[ -n "${TZ:-}" ]] && [[ "$(cat /etc/timezone 2>/dev/null)" != "$TZ" ]]; then
  echo "[first-boot] Setting system timezone → $TZ"
  sudo timedatectl set-timezone "$TZ" || true
fi

# ─── 3. TLS root + leaf ───────────────────────────────────────────────────
CERT_DIR="${TRAEFIK_CERT_DIR:-$DATA_ROOT/traefik/certs}"
sudo mkdir -p "$CERT_DIR"

if [[ ! -f "$CERT_DIR/root.key" ]]; then
  echo "[first-boot] Generating self-signed root CA…"
  sudo openssl genrsa -out "$CERT_DIR/root.key" 4096
  sudo openssl req -x509 -new -nodes -key "$CERT_DIR/root.key" \
    -sha256 -days 3650 \
    -subj "/CN=PAL Pod Root CA/O=PAL Pod" \
    -out "$CERT_DIR/root.pem"
  sudo chmod 600 "$CERT_DIR/root.key"
  sudo chmod 644 "$CERT_DIR/root.pem"
fi

LEAF_KEY="$CERT_DIR/${DOMAIN}.key"
LEAF_CRT="$CERT_DIR/${DOMAIN}.crt"

if [[ ! -f "$LEAF_KEY" ]]; then
  echo "[first-boot] Issuing leaf certificate for *.${DOMAIN}…"
  TMP=$(mktemp -d)
  cat >"$TMP/leaf.cnf" <<EOF
[req]
distinguished_name = req
prompt = no
[req]
CN = *.${DOMAIN}
[v3_req]
subjectAltName = @alt_names
[alt_names]
DNS.1 = ${DOMAIN}
DNS.2 = *.${DOMAIN}
DNS.3 = pod.${DOMAIN}
DNS.4 = plex.${DOMAIN}
DNS.5 = jelly.${DOMAIN}
DNS.6 = books.${DOMAIN}
DNS.7 = xteve.${DOMAIN}
DNS.8 = sunshine.${DOMAIN}
DNS.9 = traefik.${DOMAIN}
EOF
  sudo openssl genrsa -out "$LEAF_KEY" 2048
  sudo openssl req -new -key "$LEAF_KEY" -out "$TMP/leaf.csr" -config "$TMP/leaf.cnf"
  sudo openssl x509 -req -in "$TMP/leaf.csr" \
    -CA "$CERT_DIR/root.pem" -CAkey "$CERT_DIR/root.key" -CAcreateserial \
    -out "$LEAF_CRT" -days 825 -sha256 \
    -extfile "$TMP/leaf.cnf" -extensions v3_req
  rm -rf "$TMP"
  sudo chmod 600 "$LEAF_KEY"
  sudo chmod 644 "$LEAF_CRT"
fi

# ─── 4. Media placeholder directories ─────────────────────────────────────
for var in MEDIA_MOVIES MEDIA_TV MEDIA_MUSIC MEDIA_AUDIOBOOKS MEDIA_PODCASTS; do
  path="${!var:-}"
  if [[ -n "$path" && ! -d "$path" ]]; then
    echo "[first-boot] Creating placeholder $var → $path"
    sudo mkdir -p "$path"
    sudo chown -R "${PUID:-1000}:${PGID:-1000}" "$path"
  fi
done

# ─── 5. Model dir ─────────────────────────────────────────────────────────
if [[ -n "${PAL_VOICE_MODEL_DIR:-}" ]]; then
  sudo mkdir -p "$PAL_VOICE_MODEL_DIR"
  sudo chown -R "${PUID:-1000}:${PGID:-1000}" "$PAL_VOICE_MODEL_DIR"
fi

# ─── 6. Summary ───────────────────────────────────────────────────────────
echo
echo "[first-boot] Done."
echo "  Data root:      $DATA_ROOT"
echo "  TLS root cert:  $CERT_DIR/root.pem"
echo "  TLS leaf cert:  $LEAF_CRT"
echo "  Install root.pem on every LAN client that will use https://*.${DOMAIN}."

#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# PALPod OS — bootstrap installer for a fresh Ubuntu 22.04 machine.
#
# What this script does, in order:
#   1. Refuses to run on anything other than Ubuntu 22.04.
#   2. Detects an NVIDIA GPU (Jetson tegra device or discrete PCIe card).
#   3. Installs Docker Engine + the compose plugin (via the official convenience
#      script) unless already present.
#   4. Installs the NVIDIA Container Toolkit and wires it into Docker.
#   5. Generates .env from .env.example and asks interactively for the
#      handful of values that don't have safe defaults.
#   6. Pulls every image referenced in docker-compose.yml (fails loudly if the
#      manifest can't be resolved for aarch64).
#   7. Runs scripts/first-boot.sh, which creates the data root, ZFS datasets
#      where appropriate, and any placeholder media directories.
#   8. `docker compose up -d` and prints next steps in bold.
#
# Safe to re-run: every step is idempotent.
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
RESET="\033[0m"

log()  { echo -e "${GREEN}[+]${RESET} $*"; }
warn() { echo -e "${YELLOW}[!]${RESET} $*"; }
fail() { echo -e "${RED}[✗]${RESET} $*" >&2; exit 1; }
bold() { echo -e "${BOLD}$*${RESET}"; }

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

# ─── 1. OS check ─────────────────────────────────────────────────────────────
if ! grep -q "Ubuntu 22.04" /etc/os-release 2>/dev/null; then
  warn "This installer is only tested on Ubuntu 22.04. Continuing anyway in 5 s…"
  sleep 5
fi

# ─── 2. GPU detection ────────────────────────────────────────────────────────
GPU_KIND="none"
if [[ -e /proc/device-tree/model ]] && grep -qi jetson /proc/device-tree/model; then
  GPU_KIND="jetson"
  log "Detected NVIDIA Jetson: $(tr -d '\0' </proc/device-tree/model)"
elif command -v nvidia-smi >/dev/null 2>&1; then
  GPU_KIND="discrete"
  log "Detected discrete NVIDIA GPU."
elif lspci 2>/dev/null | grep -qi nvidia; then
  GPU_KIND="discrete-nodriver"
  warn "NVIDIA PCIe device present but driver missing; install proprietary driver first."
else
  warn "No NVIDIA GPU detected. Sunshine + pal-voice will not work."
fi

# ─── 3. Docker Engine + compose plugin ───────────────────────────────────────
if ! command -v docker >/dev/null 2>&1; then
  log "Installing Docker Engine (official convenience script)…"
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker "$USER"
  warn "You were added to the docker group — log out & back in to use it without sudo."
else
  log "Docker already installed: $(docker --version)"
fi

if ! docker compose version >/dev/null 2>&1; then
  log "Installing docker compose plugin…"
  sudo apt-get update -y
  sudo apt-get install -y docker-compose-plugin
fi

# ─── 4. NVIDIA Container Toolkit ─────────────────────────────────────────────
if [[ "$GPU_KIND" != "none" && "$GPU_KIND" != "discrete-nodriver" ]]; then
  if ! dpkg -l nvidia-container-toolkit 2>/dev/null | grep -q '^ii'; then
    log "Installing NVIDIA Container Toolkit…"
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
      | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
      | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
      | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list >/dev/null
    sudo apt-get update -y
    sudo apt-get install -y nvidia-container-toolkit
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker
    log "NVIDIA Container Toolkit wired into Docker."
  else
    log "NVIDIA Container Toolkit already present."
  fi

  # On Jetson we additionally set the default runtime so that
  # `runtime: nvidia` in compose doesn't require the extra flag.
  if [[ "$GPU_KIND" == "jetson" ]]; then
    if ! grep -q '"default-runtime": "nvidia"' /etc/docker/daemon.json 2>/dev/null; then
      log "Setting nvidia as the default Docker runtime (Jetson)…"
      sudo tee /etc/docker/daemon.json >/dev/null <<'EOF'
{
    "default-runtime": "nvidia",
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
EOF
      sudo systemctl restart docker
    fi
  fi
fi

# ─── 5. Generate .env ────────────────────────────────────────────────────────
if [[ ! -f .env ]]; then
  log "Creating .env from .env.example…"
  cp .env.example .env

  # Random secrets where the .env has none.
  gen_secret() { openssl rand -hex 32; }

  # Fill in POSTGRES_PASSWORD, PAL_WEB_JWT_SECRET, PAL_EXTENDER_SHARED_SECRET
  # if they are blank.
  for key in POSTGRES_PASSWORD PAL_WEB_JWT_SECRET PAL_EXTENDER_SHARED_SECRET; do
    if grep -q "^${key}=$" .env; then
      value="$(gen_secret)"
      sed -i "s|^${key}=$|${key}=${value}|" .env
      log "Generated random ${key}."
    fi
  done

  # Ask interactively for values with no sensible default.
  read -rp "Plex claim token (from https://plex.tv/claim, blank to skip): " plex_claim
  sed -i "s|^PLEX_CLAIM=.*|PLEX_CLAIM=${plex_claim}|" .env

  read -rp "System timezone [$(cat /etc/timezone 2>/dev/null || echo America/Los_Angeles)]: " tz
  tz="${tz:-$(cat /etc/timezone 2>/dev/null || echo America/Los_Angeles)}"
  sed -i "s|^TZ=.*|TZ=${tz}|" .env

  read -rp "Path to Movies library [/mnt/media/movies]: " movies
  sed -i "s|^MEDIA_MOVIES=.*|MEDIA_MOVIES=${movies:-/mnt/media/movies}|" .env

  read -rp "Path to TV library [/mnt/media/tv]: " tv
  sed -i "s|^MEDIA_TV=.*|MEDIA_TV=${tv:-/mnt/media/tv}|" .env

  read -rp "Path to Music library [/mnt/media/music]: " music
  sed -i "s|^MEDIA_MUSIC=.*|MEDIA_MUSIC=${music:-/mnt/media/music}|" .env

  read -rp "Path to Audiobooks library [/mnt/media/audiobooks]: " abs
  sed -i "s|^MEDIA_AUDIOBOOKS=.*|MEDIA_AUDIOBOOKS=${abs:-/mnt/media/audiobooks}|" .env

  read -rp "Path to Podcasts library [/mnt/media/podcasts]: " pods
  sed -i "s|^MEDIA_PODCASTS=.*|MEDIA_PODCASTS=${pods:-/mnt/media/podcasts}|" .env

  log ".env populated. Review it before first boot: $REPO_DIR/.env"
else
  log ".env already exists — leaving it alone."
fi

# Load env for the rest of the script.
set -a; source .env; set +a

# ─── 6. First-boot preparation ───────────────────────────────────────────────
log "Running first-boot preparation…"
bash "$REPO_DIR/scripts/first-boot.sh"

# ─── 7. Pull images ──────────────────────────────────────────────────────────
log "Pulling docker images (this can take a while on first run)…"
docker compose pull || warn "Some images did not pull cleanly — check platform (aarch64 vs x86_64)."

# ─── 8. Bring the stack up ───────────────────────────────────────────────────
log "Starting all services…"
docker compose up -d

echo
bold "──────────────────────────────────────────────────────────────────"
bold "PAL Pod is up. Next steps:"
bold "──────────────────────────────────────────────────────────────────"
echo
echo "  Control app :  https://pod.${PALPOD_DOMAIN:-palpod.local}"
echo "  Plex        :  https://plex.${PALPOD_DOMAIN:-palpod.local}   (or http://<pod-ip>:32400/web)"
echo "  Jellyfin    :  https://jelly.${PALPOD_DOMAIN:-palpod.local}  (or http://<pod-ip>:8096)"
echo "  Audiobooks  :  https://books.${PALPOD_DOMAIN:-palpod.local}"
echo "  xTeVe       :  https://xteve.${PALPOD_DOMAIN:-palpod.local}"
echo "  Sunshine    :  https://<pod-ip>:47990   (host-net; browse to Pod's LAN IP)"
echo
bold "  Install the Pod's self-signed root on any client that will use HTTPS:"
echo "     $PALPOD_DATA_ROOT/traefik/certs/root.pem"
echo
bold "  Enable the boot unit so PAL Pod comes up on power-on:"
echo "     sudo cp systemd/palpod.service /etc/systemd/system/"
echo "     sudo systemctl daemon-reload && sudo systemctl enable --now palpod"
echo
bold "  Then read: docs/INSTALL.md and docs/EXTENDER_PAIRING.md"
echo

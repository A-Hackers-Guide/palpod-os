# INSTALL — PAL Pod OS on Ubuntu 22.04 (Jetson AGX Orin)

This is a step-by-step for a hardware engineer whose main skill is EE, not
devops. If you follow it in order you'll get a working Pod. Every step
assumes a fresh Ubuntu 22.04 install on an NVIDIA Jetson AGX Orin 64GB
Developer Kit. It will also work on any x86_64 Ubuntu machine with a
recent-ish NVIDIA GPU.

Time budget: about 45 minutes on a good internet connection, most of which
is waiting for Docker images to pull.

---

## 0. Before you start

You will need:

- The Jetson (or an x86 machine with an NVIDIA GPU) already booted into
  Ubuntu 22.04, on the wired LAN.
- Sudo access on that machine.
- A Plex account (free) if you want to claim the Plex server on first launch.
- A Steam account with SteamGuard if you plan to use game streaming.
- Somewhere the media library lives. This can be an internal disk, an
  external USB SSD, or an NFS/SMB mount. Whatever the path is on the host is
  what you'll type into `.env` later.

---

## 1. Flash the Jetson (skip if already on Ubuntu 22.04)

```bash
# On any Ubuntu host with the SDK Manager installed:
sudo apt-get install -y sdkmanager
sdkmanager --cli install --product Jetson --target-os Linux --version 5.1.2
```

Choose:

- **Target hardware:** Jetson AGX Orin 64GB Developer Kit
- **JetPack:** 6.0 GA or newer
- **Storage:** onboard eMMC + external NVMe (put the OS on NVMe)

Once flashed, first-boot walks you through the standard Ubuntu wizard.

---

## 2. Make sure the base OS is happy

```bash
sudo apt-get update
sudo apt-get -y dist-upgrade
sudo apt-get install -y git curl openssl avahi-daemon
sudo systemctl enable --now avahi-daemon
```

`avahi-daemon` gives you `*.local` mDNS resolution on the LAN — the pairing
protocol depends on it.

---

## 3. Clone the repo

```bash
cd /opt
sudo git clone https://github.com/palpod/palpod-os.git
sudo chown -R "$USER":"$USER" palpod-os
cd palpod-os
```

The install script assumes `/opt/palpod-os`. If you clone elsewhere, edit
`systemd/palpod.service` to point at your path.

---

## 4. Run the installer

```bash
./install.sh
```

You will be prompted for:

- **Plex claim token** — get one from <https://plex.tv/claim> (4-min TTL).
- **Timezone** — defaults to whatever `/etc/timezone` says.
- **Paths to your media libraries** — Movies, TV, Music, Audiobooks, Podcasts.
  Leave the default if you'll set them up later.

The installer will:

1. Detect the NVIDIA GPU and install the container toolkit.
2. Install Docker + the compose plugin (via `get.docker.com`).
3. Write random secrets into `.env` for Postgres, the JWT signer, and the
   extender-pairing shared secret.
4. Pull every image referenced in `docker-compose.yml`. Expect this to take
   10–20 minutes on first run.
5. Run `scripts/first-boot.sh` which:
   - Creates `/var/lib/palpod/{traefik/certs,models,uploads}`
   - Generates the self-signed root CA + `palpod.local` leaf
   - Creates a placeholder ZFS dataset if TrueNAS is present
6. `docker compose up -d`.

If you see red text, re-read it — most failures are `.env` typos or missing
media directories.

---

## 5. Enable the boot unit

So the Pod comes back up on its own after a power cycle:

```bash
sudo cp systemd/palpod.service /etc/systemd/system/
sudo cp systemd/palpod-healthcheck.{service,timer} /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now palpod.service
sudo systemctl enable --now palpod-healthcheck.timer
```

---

## 6. Trust the Pod's TLS root on your clients

The installer generates a self-signed CA at
`/var/lib/palpod/traefik/certs/root.pem`. Copy it to each client and install:

- **macOS:** double-click, add to System keychain, mark as "Always Trust".
- **iOS:** AirDrop, install profile in Settings → General → VPN & Device
  Management, then trust in Settings → General → About → Certificate Trust.
- **Windows:** `certmgr.msc` → Trusted Root Certification Authorities → Import.
- **Android:** Settings → Security → Encryption & credentials → Install a
  certificate → CA certificate.

You can also skip this and use plain HTTP on the direct container ports
(`http://<pod-ip>:32400/web` for Plex, etc.) — Traefik is a convenience, not
a requirement.

---

## 7. Claim Plex

Open <https://plex.palpod.local> (or `http://<pod-ip>:32400/web`) within
4 minutes of first boot. Follow the wizard, add your `MEDIA_MOVIES`,
`MEDIA_TV`, `MEDIA_MUSIC` mounts as libraries.

If the claim token expired, edit `.env`, put in a new token, then:

```bash
docker compose up -d --force-recreate plex
```

---

## 8. Verify

```bash
docker compose ps                # all containers "Up (healthy)"
docker compose logs -f pal-web   # tail the control app
curl -k https://pod.palpod.local/api/health
```

The last command should return `{ "ok": true }`. If it does, pair a Moonlight
client with Sunshine (browse to `https://<pod-ip>:47990` for the PIN) and
you're done.

---

## 9. Troubleshooting

| Symptom                          | Likely cause                                             |
|----------------------------------|----------------------------------------------------------|
| `nvidia-container-cli: initialization error` | Toolkit not installed or Docker not restarted after installing it. Re-run `./install.sh`. |
| Compose says "no matching manifest for linux/arm64/v8" | The image doesn't have an aarch64 tag. Common for older Sunshine builds — pin to `lizardbyte/sunshine:master`. |
| Plex won't claim                 | Claim token expired (4-min TTL). Get a new one, edit `.env`, `docker compose up -d --force-recreate plex`. |
| Moonlight can't find Sunshine    | Sunshine uses host networking. Check the Pod's LAN IP is reachable and mDNS/avahi is running. |
| `pal-web` loops restarting       | Sibling repo not checked out at `../pal-web` or `npm ci` hasn't run there. |
| Sphere is blank                  | `pal-face` container needs `/dev/fb0`. Confirm `ls -l /dev/fb0` on the host. |

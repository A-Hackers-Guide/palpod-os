# RustDesk on PAL Pod

The Pod runs its own **RustDesk rendezvous + relay** so remote-desktop traffic
never leaves the house. Nothing here talks to `rustdesk.com`.

Two containers cooperate:

| Container        | Role          | Ports                     |
|------------------|---------------|---------------------------|
| `rustdesk-hbbs`  | Rendezvous / ID server | 21115 tcp, 21116 tcp+udp, 21118 tcp (console) |
| `rustdesk-hbbr`  | Relay (used when peers can't P2P) | 21117 tcp, 21119 tcp (console) |

Both share an on-disk X25519 keypair at `./data/rustdesk-keys/`. Clients pin
the **public** half of that keypair; without it, `hbbs` rejects the client.

---

## First-boot key generation

Run once, from the repo root:

```bash
./configs/rustdesk/generate-keys.sh
```

The script creates `./data/rustdesk-keys/id_ed25519` (private) and
`id_ed25519.pub` (public) if they don't already exist, then prints the public
key. Copy it — you'll paste it into every client.

If you skip this step, hbbs generates its own key on first launch (that's what
the `-k _` flag on the container does). Running the script yourself just gives
you the public key up-front so you can pre-fill client configs.

---

## Install the RustDesk client

Upstream builds live at <https://github.com/rustdesk/rustdesk/releases>.

| OS           | Package                              |
|--------------|--------------------------------------|
| macOS        | `rustdesk-x.y.z-universal.dmg`       |
| Windows      | `rustdesk-x.y.z-x86_64.exe`          |
| Linux (deb)  | `rustdesk-x.y.z-x86_64.deb`          |
| Linux (rpm)  | `rustdesk-x.y.z-x86_64.rpm`          |
| Linux (Flatpak) | `flatpak install flathub com.rustdesk.RustDesk` |
| iOS          | App Store — *RustDesk Remote Desktop*      |
| Android      | Play Store or F-Droid — *RustDesk*   |

---

## Point the client at the Pod

In the RustDesk client:

1. Open **Settings → Network → ID/Relay Server**.
2. Fill in:
   - **ID Server:** `palpod.local:21116`  *(or the Pod's LAN IP)*
   - **Relay Server:** `palpod.local:21117`
   - **API Server:** *(leave blank — the Pod has no HTTP API for RustDesk)*
   - **Key:** paste the contents of `./data/rustdesk-keys/id_ed25519.pub`
3. Click **OK** and restart the client. The status bar should show a green
   dot with **Ready**. If it stays yellow, `nc -zv palpod.local 21116` from
   the client machine and check the Pod's firewall.

A pre-filled sample sits in [`example-client-config.toml`](example-client-config.toml)
that you can drop into `~/.config/rustdesk/config.toml` on Linux or the
equivalent path on macOS (`~/Library/Preferences/com.carriez.RustDesk/`) and
Windows (`%APPDATA%\RustDesk\config\`).

---

## Register the device with pal-web

Once the client shows **Ready**, note its 9-digit RustDesk ID (top of the
client window), then run on the Pod:

```bash
./scripts/pair-remote-device.sh "Mark's Office Mac" mac 123456789
```

This inserts a row into the `remote_devices` Postgres table, mints an auth
token, and prints the follow-up steps. The device then shows up in pal-web
under **Settings → Remote Devices**.

**AI control is opt-in.** By default the device is registered with
`ai_control_allowed = false` — the Pod can view it but not click/type on it.
Toggle **Allow AI control** on the device card in pal-web to grant that
permission.

---

## Troubleshooting

- **Client stuck on "Connecting..."** — hbbs is not reachable. Check
  `docker compose ps rustdesk-hbbs`, then `docker compose logs rustdesk-hbbs`.
- **Client connects but says "Key mismatch"** — the public key you pasted
  into the client doesn't match the one in `./data/rustdesk-keys/`. Re-run
  `generate-keys.sh` (it will only print the existing key, not overwrite it)
  and re-copy.
- **P2P fails, relay works but is slow** — expected across VLANs; open UDP
  21116 on the LAN firewall between the Pod's VLAN and the client's VLAN so
  peers can hole-punch.
- **`neonlabsio` / `linuxserver/anydesk` shows up in `docker ps`** — someone
  ran `docker compose --profile anydesk up -d`. That's fine; RustDesk and
  AnyDesk coexist. See the AnyDesk section of the top-level `README.md`.

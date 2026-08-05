# SECURITY — HearthOS

The single most important product invariant is:

> **Nothing leaves the house.**

Every design decision below flows from that.

---

## 1. Threat model

We defend against, in decreasing order of realism:

1. **A curious guest on the LAN** — someone with Wi-Fi access poking at open
   ports.
2. **An untrusted app on a family member's phone** trying to reach the Pod
   from the LAN side.
3. **A stolen extender** — physical loss of a paired peripheral node.
4. **Supply chain compromise of an upstream image** — a poisoned Plex
   container tag.

We do **not** defend against:

- A skilled attacker with physical console access to the primary Jetson.
  That box hosts every secret; physical possession = root.
- Nation-state actors. The product is offline; if the threat requires WAN
  ingress there is nothing to attack.

---

## 2. Boundaries

```
[ WAN ]  ─╳ no ingress  ── [ residential router ] ── [ LAN ]
                                                         │
                                                         ├── Hearth primary
                                                         │       └── Traefik :80/:443
                                                         │       └── direct ports (Plex, Jellyfin, …)
                                                         ├── extenders (mTLS + JWT)
                                                         └── clients (browsers, Moonlight, mic array)
```

- The installer NEVER opens ports on the router. If someone wants remote
  access we tell them to VPN in — Tailscale, WireGuard, or a router VPN.
- Traefik binds `:80` + `:443` on the LAN interface. The dashboard on `:8080`
  binds `127.0.0.1` only.
- The Postgres port `5432` is **not** published — it's reachable only over
  the `palpod` docker bridge.
- The healthcheck systemd unit POSTs to `http://localhost:3000` — never to a
  remote endpoint.

---

## 3. Secret storage

| Secret                          | Where it lives                                  | Rotation                                    |
|---------------------------------|-------------------------------------------------|---------------------------------------------|
| `POSTGRES_PASSWORD`             | `.env` (0600, root:root)                        | Manual; requires re-init of pal-web         |
| `PAL_WEB_JWT_SECRET`            | `.env`                                          | Rotate → all extender JWTs invalidate       |
| `PAL_EXTENDER_SHARED_SECRET`    | `.env` + baked into each extender firmware      | Rotate + re-flash extenders                 |
| `PLEX_CLAIM`                    | `.env`, one-shot (blank after claim)            | n/a                                         |
| Self-signed root CA private key | `/var/lib/palpod/traefik/certs/root.key` (0600) | Generate a new root, redistribute leaf certs |
| Steam credentials               | `.env` + inside `steam_config` volume           | Manual; Steam Guard on                      |

`.env` is `chmod 600` and owned by root. The compose stack reads it via
`docker compose`'s built-in env-file mechanism, so container processes only
see the variables their compose block explicitly names — no blanket leak.

Never commit `.env`. `.gitignore` enforces this.

---

## 4. TLS

The installer generates a **self-signed root CA** the first time it runs, then
issues a leaf cert for `*.palpod.local`. The root's private key stays on the
primary; only the public `root.pem` ever leaves. Every LAN client that wants
a browser padlock installs `root.pem` as a trusted anchor.

We deliberately do NOT use public-CA certs (Let's Encrypt / ACME). Doing so
would require the Pod to reach the ACME server (WAN), publish a TXT record
in DNS (WAN), or expose port 80 to the internet (WAN). Any of those violates
"nothing leaves the house".

If a customer wants public HTTPS they can put the Pod behind Cloudflare
Tunnel or Tailscale Funnel — that's their choice, not our default.

---

## 5. Auth

- **pal-web sessions:** cookie-based, HS256 JWT signed with
  `PAL_WEB_JWT_SECRET`, 30-day sliding expiry.
- **Extender ↔ primary:** JWT in `Authorization: Bearer …` header on every
  request. See [`EXTENDER_PAIRING.md`](EXTENDER_PAIRING.md).
- **Plex / Jellyfin / Audiobookshelf:** each has its own user store.
  Pal-web can proxy sign-in by keeping a per-user token cache in Postgres,
  but the source of truth stays in the individual service.
- **Sunshine:** PIN-based pairing over TLS. `SUNSHINE_ADMIN_PASSWORD` guards
  the web UI. Rotate it after first pair.

---

## 6. Container hardening

- All services run with `restart: unless-stopped` so a crash doesn't leave
  the Pod partially online.
- Media directories are mounted **read-only** into Jellyfin (`:ro`) — Jellyfin
  never has to write to the library, only to its own `/config`.
- xTeVe's buffer directory is scoped to `/tmp/xteve` inside its own volume,
  never onto the media library.
- pal-face is the only privileged container. It needs `/dev/fb0` and
  `--privileged` because the Jetson framebuffer isn't cleanly namespaced.
  Everything else is unprivileged.

---

## 7. Update policy

- `update.sh` pulls new image digests but does **not** blindly move image
  tags. Pin production tags in `docker-compose.yml` (e.g. `plex:1.40.0`
  instead of `plex:latest`) before shipping to a customer.
- On CI (out of scope for this repo) run `trivy image` against every image
  in `docker compose config --images` and gate ship on no CRITICAL findings.
- Postgres major-version upgrades require an explicit dump + restore. Never
  ship a compose bump from `postgres:16` to `postgres:17` without a
  migration runbook.

---

## 8. Remote Desktop Security

The remote-desktop stack (RustDesk `hbbs` + `hbbr`, optional AnyDesk) can, by
design, see and drive other machines. That makes it the highest-blast-radius
service on the Pod. Treat it accordingly.

### Threat model

An attacker who compromises the remote-desktop stack could:

- **View live screen contents** of any paired device — email, banking,
  password managers, whatever's on the display.
- **Inject input** (mouse, keyboard) into any device whose owner has toggled
  *Allow AI control* on. Without that flag, the click/type endpoints refuse
  even authenticated Pod sessions.
- **Enumerate the paired device list** and learn what machines exist on the
  home network.

They cannot:

- Reach a device that isn't paired. Pairing requires a one-time token that
  is displayed on the Pod's local console and typed into the client — an
  attacker with only remote access cannot mint a token.
- Bypass a device's own OS-level accessibility permission. RustDesk on macOS
  still needs Screen Recording + Accessibility grants; the Pod cannot grant
  those on the user's behalf.

### Mitigations

- **Per-device auth tokens.** Every paired device gets its own token,
  scoped and revocable. There is no "master" credential shared across
  devices.
- **AI control is off by default.** Voice + web can *view* immediately;
  driving input requires an explicit toggle per device. The toggle lives on
  the device card in pal-web and writes to `remote_devices.ai_control` in
  Postgres.
- **Self-hosted only.** `hbbs` and `hbbr` run on the Pod. The RustDesk
  clients are configured to point at the Pod's LAN address as their sole ID
  server — the upstream public RustDesk rendezvous is not consulted.
- **No WAN ingress.** Same rule as the rest of the stack: ports `21115-21117`
  bind to the LAN interface only. Remote access from outside the house
  requires a VPN (Tailscale / WireGuard / router VPN), same as everything
  else.

### Encryption

- An **X25519 keypair** is generated by `install.sh` the first time it runs
  and stored as `/var/lib/palpod/rustdesk/id_ed25519{,.pub}` (`0600`, owned
  by the `rustdesk` container's UID).
- The public key is what clients pin during pairing; the private key never
  leaves the Pod. No external service — including RustDesk's public
  rendezvous — sees it.
- Rotating the key invalidates every paired device. The rotation flow in
  pal-web walks the user through re-pairing.

### Audit trail

Every session is recorded in the `remote_sessions` Postgres table:

| column         | meaning                                                     |
|----------------|-------------------------------------------------------------|
| `id`           | UUID                                                        |
| `device_id`    | FK → `remote_devices.id`                                    |
| `initiator`    | `voice` / `web` / `api`                                     |
| `started_at`   | timestamptz                                                 |
| `ended_at`     | timestamptz, nullable while a session is live               |
| `input_events` | JSONB — every AI-driven click/keystroke, empty for view-only|
| `terminated_by`| `user` / `timeout` / `revocation`                           |

The pal-web *History* tab is a paginated view onto this table. Retention
defaults to 90 days; the pruner runs from the healthcheck timer.

### Revoking a device

Two supported paths — both destroy the auth token, tear down any live
session, and write a `terminated_by = 'revocation'` row to
`remote_sessions`:

- **Web UI:** *Settings → Remote Devices → [device] → Revoke*.
- **CLI:** `scripts/pair-remote-device.sh --revoke <device-id>` on the Pod.

Revocation is immediate and irreversible. Re-adding the device requires the
full pairing flow.

---

## 9. Incident response

- `docker compose logs --tail 500 -f` on the affected service is your first
  stop. Send the output to pal-web's health dashboard for triage.
- The systemd unit `palpod-healthcheck.timer` posts per-container state to
  pal-web every 60 s; if a service is unhealthy pal-web pages a household
  admin (email/push, out of scope here).
- Rollback: `git checkout` the last known-good SHA, `./update.sh`.
- Recover Postgres from a `pg_dump` backup — see [`BACKUP.md`](BACKUP.md).

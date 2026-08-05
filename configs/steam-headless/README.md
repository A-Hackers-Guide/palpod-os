# Headless Steam inside Hearth

Steam is running inside the `steam-headless` container, which is a fork of
[josh5/steam-headless](https://github.com/Steam-Headless/docker-steam-headless).
It boots an Xvfb virtual display, launches Steam Big Picture inside it, and
exposes the display via a web VNC UI on port `8083` for one-off admin.

Under normal use you never touch VNC. The intended flow is:

1. A LAN client (Moonlight on Apple TV, an iPad, a phone) pairs with **Sunshine**.
2. Sunshine's app list includes an entry called **Steam Big Picture** that
   points at the Xvfb display the headless-Steam container owns.
3. Selecting it in Moonlight streams Big Picture end-to-end, GPU-encoded, at
   whatever resolution the client requested.

---

## First-time SteamGuard login

Steam refuses to log a new device in without an interactive SteamGuard code.
Because the container has no terminal, you must attach once:

```bash
# 1. Watch the container's logs — it will print a prompt asking for
#    the SteamGuard code when it comes up:
docker compose logs -f steam-headless

# 2. Once you see "Steam Guard code required", open the web VNC UI:
#    http://<pod-ip>:8083   (password = SUNSHINE_ADMIN_PASSWORD)
# 3. Type the code Steam emailed / sent to your Steam Mobile app.
```

The container persists Steam's `sentry` file in the `steam_config` named volume,
so this only happens once per Steam account per Pod.

If you'd rather avoid the VNC UI entirely, seed
`/config/Steam/config/config.vdf` with a valid `SteamGuard` block before first
start. See `docker-steam-headless`'s docs for the exact format.

---

## Registering Steam with Sunshine

Sunshine is in its own container and needs to know how to launch Big Picture
against the headless X display. In the Sunshine web UI (`https://<pod-ip>:47990`
→ **Applications** → **Add New**) create:

- **Application Name:** `Steam Big Picture`
- **Command:**
  ```
  docker exec -e DISPLAY=:0 steam-headless steam -bigpicture
  ```
- **Working Directory:** `/home/default`
- **Image path:** upload the standard Steam Big Picture cover art.
- **Detached:** yes (so Sunshine returns immediately and just captures the
  X display where Steam is already running).

Pin the resolution to whatever the client is asking for so Steam re-launches
at the right size.

---

## What must never happen

The Sphere face is driven exclusively by **pal-face** on `/dev/fb0`. Do **not**
route Steam or Sunshine output to `/dev/fb0`, `HDMI-0`, or any physical
connector. `configs/sunshine/sunshine.conf` pins `output_name = :99` to
enforce this. If you add a second Sunshine app that streams the *desktop*
(e.g. for remote troubleshooting), make sure it targets the same virtual
display, not HDMI-0.

---

## Common breakages

| Symptom                            | Fix                                                   |
|------------------------------------|-------------------------------------------------------|
| Big Picture launches at 800×600    | Set the resolution in the Moonlight client before connecting; Sunshine forwards the request to Xvfb via `xrandr`. |
| No audio                           | Verify PulseAudio is running inside the container: `docker exec steam-headless pactl list sinks`. |
| SteamGuard prompt loops forever    | Steam invalidated the token. Rerun the interactive login via VNC. |
| Sphere flashes to Steam            | Almost certainly means `pal-face` crashed and released `/dev/fb0`. Restart `pal-face` before touching Sunshine. |

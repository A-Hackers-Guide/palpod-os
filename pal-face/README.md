# PAL Face Renderer

Procedural Pygame renderer for the animated PAL face — the round cyan display
inside the PAL Pod's levitating orb, inspired by PAL from *The Mitchells vs.
the Machines*: cyan gradient background, two tall white pill eyes, and a
cup-scoop smile.

- **Runtime:** single Jetson AGX Orin 64GB (MVP), full-screen 1080×1080 on a
  Waveshare 8" Round IPS via HDMI.
- **Framerate:** 60 fps target, verified by `scripts/benchmark.py`.
- **Control plane:** WebSocket bridge to `pal-voice` on `ws://localhost:7777`
  for face-state changes and lip-sync during TTS.
- **Runs happily solo:** no assets, no pal-voice, no crash. Just an idle face.

## Install

```bash
cd pal-face
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Deps: `pygame-ce`, `websockets`, `pyyaml`, `pydantic`, `pydantic-settings`.

## Run the demo (no pal-voice needed)

```bash
./scripts/standalone-demo.sh --windowed
```

Cycles through all 9 expressions with a 3-second hold each. This is what the
founder should run the first time the Waveshare round display is wired up —
if you see the cyan glow and pill eyes, the whole render stack is healthy.

Add `--show-mask` to see the magenta sphere outline (useful on a square
laptop monitor).

## Run the renderer

```bash
python -m palface -c config.yaml
```

or with keyboard controls (no pal-voice, no cycling — you drive the states):

```bash
python scripts/keyboard-control.py --windowed
```

| Key | State |
|-----|-------|
| 1 | NEUTRAL |
| 2 | HAPPY |
| 3 | WINK |
| 4 | SURPRISED |
| 5 | ANGRY |
| 6 | SUSPICIOUS |
| 7 | LISTENING |
| 8 | THINKING |
| 9 | TALKING |
| b | force blink |
| +/- | simulated TTS audio level |
| Esc / q | quit |

## Benchmark

```bash
python scripts/benchmark.py --seconds 60 --windowed
```

PASS if mean frame time < 16.6 ms (i.e. sustained 60 fps).

## WebSocket protocol

The renderer subscribes to `pal-voice` over WebSockets and reacts to:

```jsonc
{"type": "face_state", "state": "listening"}   // any of the 9 expressions
{"type": "tts_start"}                          // enters TALKING
{"type": "tts_frame", "audio_level": 0.7}      // drives mouth openness (0..1)
{"type": "tts_end"}                            // returns to NEUTRAL
```

Reconnect is automatic: exponential backoff 0.5s → 30s cap, forever. If
`pal-voice` restarts, `pal-face` will pick right back up.

## The 9 expressions

| State       | Eyes                                | Mouth                                     |
|-------------|-------------------------------------|-------------------------------------------|
| NEUTRAL     | default pill                        | default cup smile                         |
| HAPPY       | squinted (scale-y 0.5)              | bigger cup (1.18 × 1.45)                  |
| WINK        | left scale-y 0.08                   | slightly larger cup                       |
| SURPRISED   | 1.18 × 1.08                         | tight small opening (0.45 × 0.75)         |
| ANGRY       | rotated ±22°                        | flat line (scale-y 0.28)                  |
| SUSPICIOUS  | 0.35 vertical                       | flat + shifted right (offset +15%)        |
| LISTENING   | 1.1 uniform, breathing 0.95↔1.05    | default cup                               |
| THINKING    | 0.75 vertical, slight upward gaze   | slightly smaller cup                      |
| TALKING     | neutral (blinks pass through)       | crossfades cup ↔ oval driven by TTS level |

All transitions between states are 350 ms `easeInOutCubic`. Mid-transition
retargets don't snap — the interpolator snapshots the current interpolated
value as the new "from".

## Kiosk / framebuffer setup on Jetson

The Jetson runs headless (no X server). The renderer uses SDL2's `kmsdrm`
video driver by default:

```bash
sudo SDL_VIDEODRIVER=kmsdrm SDL_FBDEV=/dev/fb0 \
     .venv/bin/python -m palface -c config.yaml
```

Older L4T releases without KMSDRM: use `SDL_VIDEODRIVER=fbcon` instead.

The `pal` user must be in `video` and `render` groups.

Enable at boot:

```bash
sudo cp systemd/palface.service /etc/systemd/system/
sudo systemctl enable --now palface.service
journalctl -fu palface.service
```

## Docker

Build:

```bash
docker build -t palface .
```

Desktop debug (X11 passthrough):

```bash
xhost +local:docker
docker run --rm --privileged \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    palface --windowed
```

Jetson kiosk (framebuffer):

```bash
docker run --rm --privileged \
    --device /dev/fb0 --device /dev/dri \
    -e SDL_VIDEODRIVER=kmsdrm \
    -e SDL_FBDEV=/dev/fb0 \
    palface
```

## Tests

```bash
pip install -e '.[dev]'
pytest -q
```

## Layout

```
pal-face/
├── palface/          # library — importable, no side effects at import time
│   ├── renderer.py   # 60fps loop, background + eyes + mouth + sphere mask
│   ├── states.py     # FaceState dataclass, 9 canonical states
│   ├── expressions.py# builder functions per state
│   ├── interpolator.py# 350ms easeInOutCubic morphs, retargeting
│   ├── eyes.py       # pill eye layout & draw
│   ├── mouth.py      # cup-scoop smile with talking crossfade
│   ├── shapes.py     # rounded_rect_pill, cup_smile_points, radial_gradient, mask
│   ├── behaviors.py  # blinks, glances, idle expression bursts
│   ├── bridge.py     # WebSocket client — threaded, auto-reconnect
│   ├── colors.py     # palette constants
│   ├── config.py     # pydantic settings, YAML loader
│   └── __main__.py   # `python -m palface`
├── scripts/          # ops / bring-up
├── systemd/          # kiosk unit file
├── tests/            # pytest coverage of the deterministic bits
└── assets/           # README only — nothing procedural needs assets
```

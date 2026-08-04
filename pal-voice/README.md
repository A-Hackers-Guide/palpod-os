# pal-voice

The voice pipeline for **PAL Pod** — a fully-offline luxury AI + media appliance.

`pal-voice` turns *"Hey Pod"* into a running local-AI conversation. It runs on a
single **NVIDIA Jetson AGX Orin 64GB** developer kit (Ubuntu 22.04, aarch64) and
speaks only to the other pod services over an in-process WebSocket bridge.

Everything is local. Nothing leaves the box.

## The pipeline

```
                +--------+   +------+   +-------+   +-----+   +-----+
   mic  --->    |  WAKE  |-->|  VAD |-->|  STT  |-->| LLM |-->| TTS | ---> speakers
                +--------+   +------+   +-------+   +-----+   +-----+
                                 |          |         |
                                 v          v         v
                            +--------+ +---------+ +---------+
                            | FACE ID| | MEMORY  | | BRIDGE  |
                            +--------+ +---------+ +---------+
                                 |          |         |
                                 +----------+---------+
                                            |
                                            v
                                    pal-face / pal-web
```

See [`palvoice/orchestrator.py`](palvoice/orchestrator.py) for the state machine.
Its module docstring has the authoritative ASCII diagram.

## Hardware

**Target:** NVIDIA Jetson AGX Orin 64GB developer kit.

* 64 GB unified LPDDR5, 2048 CUDA cores, 64 tensor cores — enough to run
  Qwen 2.5 32B at Q5\_K\_M (~24 GB weights) at 8–12 tok/s.
* JetPack 6.x / L4T r36.x, Ubuntu 22.04 aarch64.
* USB mic array (Respeaker 4-Mic or similar) at 16 kHz mono.
* CSI camera (Arducam IMX477) for face recognition.
* HDMI or 3.5mm speakers.

Runs on x86 + NVIDIA discrete GPU for development. Falls back to CPU when no GPU
is present (slow, but the state machine still works — useful for tests).

## Models

pal-voice **does not** ship model weights. Run:

```bash
./scripts/download-models.sh
```

to fetch everything into `palvoice/models/`. See
[`palvoice/models/MODELS.md`](palvoice/models/MODELS.md) for the list, sizes,
and Hugging Face URLs.

| Stage | Model | Size |
|-------|-------|------|
| Wake  | openWakeWord custom "hey pod" ONNX | ~1 MB |
| STT   | whisper.cpp `small.en` GGML | ~250 MB |
| LLM   | Qwen 2.5 32B Instruct GGUF Q5\_K\_M | ~24 GB |
| TTS   | Piper `en_US-libritts_r-medium` ONNX + JSON | ~65 MB |
| Face  | dlib `mmod_human_face_detector` + `dlib_face_recognition_resnet_model_v1` | ~100 MB |
| Voice | Resemblyzer default weights | ~19 MB |
| Memory embed | `all-MiniLM-L6-v2` | ~90 MB |

## Run standalone

```bash
# 1. Install
python -m venv .venv && source .venv/bin/activate
pip install -e .[jetson]        # or [x86] or [cpu]

# 2. Fetch models
./scripts/download-models.sh

# 3. Copy the config
cp config.yaml.example config.yaml

# 4. Point config.yaml at your mic + camera device IDs

# 5. Run
python -m palvoice
```

You'll see structlog-JSON events on stdout as each stage fires.

## Run without a mic (smoke test)

```bash
python scripts/smoke.py fixtures/hey_pod_what_time_is_it.wav
```

Runs the full orchestrator against a canned WAV and prints the event stream.
No microphone, no camera, mocks the LLM/TTS so it also works without models.

## Run under Docker

```bash
docker build -t palpod/voice .
docker run --rm --gpus all --device /dev/snd --device /dev/video0 \
    -v $PWD/palvoice/models:/app/palvoice/models \
    -p 7777:7777 palpod/voice
```

The Dockerfile has three targets: `jetson` (nvidia/l4t-jetpack base),
`x86-gpu` (nvidia/cuda base), and `cpu` (python:3.11-slim base).

## Bridge / IPC

The orchestrator hosts a WebSocket server on `0.0.0.0:7777` (see
[`palvoice/bridge.py`](palvoice/bridge.py) for the JSON schema).

* **pal-web** subscribes for transcripts + tts events, and injects text prompts.
* **pal-face** subscribes for face-state events (`neutral | listening | thinking | talking | idle-blink`).

## Install as a service

```bash
sudo cp systemd/palvoice.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now palvoice
journalctl -u palvoice -f
```

## Layout

```
pal-voice/
├── palvoice/                 # the package
│   ├── __main__.py           # entrypoint — wires everything together
│   ├── orchestrator.py       # THE state machine
│   ├── config.py             # pydantic-settings loader
│   ├── audio.py              # mic + speaker + VAD
│   ├── wake.py               # openWakeWord runner
│   ├── stt.py                # whisper.cpp wrapper
│   ├── llm.py                # llama-cpp-python + Qwen 2.5 32B
│   ├── tts.py                # Piper wrapper
│   ├── recognize.py          # face + voice identification
│   ├── memory.py             # SQLite fact store with embeddings
│   ├── personality.py        # 3-axis slider → prompt fragments
│   └── bridge.py             # WebSocket to pal-web / pal-face
├── scripts/
│   ├── download-models.sh
│   ├── train-wakeword.py
│   └── smoke.py
├── tests/
├── systemd/palvoice.service
├── Dockerfile
├── pyproject.toml
└── config.yaml.example
```

**Start reading at `palvoice/orchestrator.py`.** Everything else is a leaf that
the orchestrator wires together.

## License

Proprietary — © PAL Pod. All rights reserved.

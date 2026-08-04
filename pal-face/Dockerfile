# PAL Face Renderer — container image.
#
# Two run modes:
#
#  1. Desktop debug (X11 passthrough):
#       xhost +local:docker
#       docker run --rm --privileged \
#           -e DISPLAY=$DISPLAY \
#           -v /tmp/.X11-unix:/tmp/.X11-unix \
#           palface --windowed
#
#  2. Jetson kiosk (framebuffer / KMSDRM, no X):
#       docker run --rm --privileged \
#           --device /dev/fb0 --device /dev/dri \
#           -e SDL_VIDEODRIVER=kmsdrm \
#           -e SDL_FBDEV=/dev/fb0 \
#           palface
#
# NB: --privileged is required for direct framebuffer / DRM access on Jetson.

FROM python:3.11-slim

# SDL2 + libs Pygame CE needs. libgl / libglu for hardware-accelerated blits.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libsdl2-2.0-0 \
        libsdl2-image-2.0-0 \
        libsdl2-mixer-2.0-0 \
        libsdl2-ttf-2.0-0 \
        libfreetype6 \
        libjpeg62-turbo \
        libpng16-16 \
        libportmidi0 \
        libgl1 \
        libglu1-mesa \
        libdrm2 \
        libgbm1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/palpod/pal-face

COPY pyproject.toml README.md ./
COPY palface ./palface
COPY scripts ./scripts
COPY config.yaml.example ./config.yaml

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

# Default: run the renderer. Override CMD to run a script instead:
#   docker run ... palface bash scripts/standalone-demo.sh
ENV PYTHONUNBUFFERED=1
ENV SDL_NOMOUSE=1

ENTRYPOINT ["python", "-m", "palface"]
CMD ["-c", "/opt/palpod/pal-face/config.yaml"]

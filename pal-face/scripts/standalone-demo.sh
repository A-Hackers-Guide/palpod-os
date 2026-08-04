#!/usr/bin/env bash
# standalone-demo.sh
# ---------------------------------------------------------------------------
# Runs the PAL face WITHOUT needing pal-voice.
# Cycles through all 9 expressions with a 3s hold each, then loops forever.
# Use during hardware bring-up (first time wiring the Waveshare round display).
#
# Usage:
#   ./scripts/standalone-demo.sh                 # fullscreen
#   ./scripts/standalone-demo.sh --windowed      # windowed for laptops
# ---------------------------------------------------------------------------
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/.." && pwd)"

cd "${ROOT}"

# Prefer a project venv if present.
if [[ -d ".venv" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

exec python "${HERE}/demo_cycle.py" "$@"

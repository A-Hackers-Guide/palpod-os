"""Benchmark the render loop for N seconds and report frame-time stats.

Target: mean frame time < 16.6ms on Jetson AGX Orin (i.e. sustained 60fps).
"""

from __future__ import annotations

import argparse
import math
import statistics
import time

from palface.config import load_config
from palface.renderer import Renderer
from palface.states import FaceStateName


def _percentile(sorted_vals, p: float) -> float:
    if not sorted_vals:
        return math.nan
    k = (len(sorted_vals) - 1) * p
    lo = int(math.floor(k))
    hi = int(math.ceil(k))
    if lo == hi:
        return sorted_vals[lo]
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", default=None)
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--windowed", action="store_true")
    ap.add_argument("--width", type=int, default=None)
    ap.add_argument("--height", type=int, default=None)
    ap.add_argument("--vsync", action="store_true",
                    help="Enable vsync (default off for benchmarking).")
    args = ap.parse_args()

    cfg = load_config(args.config)
    if args.windowed:
        cfg.screen.fullscreen = False
    if args.width:
        cfg.screen.width = args.width
    if args.height:
        cfg.screen.height = args.height
    cfg.screen.vsync = args.vsync
    cfg.bridge.offline = True

    r = Renderer(cfg, bridge=None)

    # Warmup so JIT / caches / SDL init don't skew results.
    for _ in range(10):
        r.render_frame()

    frame_ms: list[float] = []
    r.set_state(FaceStateName.TALKING)  # exercise the priciest mouth branch
    r._talking_openness = 0.5

    end = time.monotonic() + args.seconds
    last = time.perf_counter()
    while time.monotonic() < end:
        # Oscillate openness so the crossfade branch runs every frame.
        r._talking_openness = 0.5 + 0.5 * math.sin(time.monotonic() * 5.0)
        r.render_frame()
        now = time.perf_counter()
        frame_ms.append((now - last) * 1000.0)
        last = now

    # Report.
    frame_ms.sort()
    n = len(frame_ms)
    mean = statistics.fmean(frame_ms)
    p50 = _percentile(frame_ms, 0.50)
    p95 = _percentile(frame_ms, 0.95)
    p99 = _percentile(frame_ms, 0.99)
    fps = 1000.0 / mean if mean > 0 else float("nan")

    print(f"frames:         {n}")
    print(f"seconds:        {args.seconds:.1f}")
    print(f"mean frame ms:  {mean:7.3f}  ({fps:5.1f} fps)")
    print(f"p50  frame ms:  {p50:7.3f}")
    print(f"p95  frame ms:  {p95:7.3f}")
    print(f"p99  frame ms:  {p99:7.3f}")
    print(f"min  frame ms:  {frame_ms[0]:7.3f}")
    print(f"max  frame ms:  {frame_ms[-1]:7.3f}")

    ok = mean < 16.6
    print("RESULT:", "PASS (60fps sustained)" if ok else "FAIL (below 60fps)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

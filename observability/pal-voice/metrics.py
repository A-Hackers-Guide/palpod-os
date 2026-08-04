"""
palpod-os / observability / pal-voice / metrics.py
==================================================

Standalone HTTP handler that exposes pal-voice's Prometheus metrics on port
7778 (adjacent to the WebSocket bridge on 7777). Runs inside the same
process as the orchestrator — spawned as a daemon thread from
``pal_voice.main`` so it comes up with the service and dies with it.

Metrics exposed
---------------

Histograms
    palvoice_llm_latency_seconds
        End-to-end inference latency for each LLM turn. Labels: (model, phase).
        `phase` is one of {prefill, decode, total}.
    palvoice_stt_latency_seconds
        Whisper transcription latency for one utterance. Label: (model_size).
    palvoice_tts_latency_seconds
        Piper synthesis latency, measured wall-clock from the first token
        arriving at Piper to the last audio sample being pushed to the
        output ring buffer. Label: (voice).

Counters
    palvoice_llm_tokens_total
        Tokens produced by the LLM. Labels: (model, direction) where
        direction is one of {prompt, completion}. Rate divided by 1 gives
        tokens per second on the AI dashboard.
    palvoice_wake_events_total
        Wake-word events, labeled by outcome ∈
        {true_positive, false_positive, cancelled}. `cancelled` means the
        user aborted the interaction after the wake word fired but before
        an intent was produced.
    palvoice_ensemble_prompts_total
        Every prompt the ensemble ran (denominator for divergence rate).
    palvoice_ensemble_divergence_total
        Times the ensemble detected a *gross* disagreement between models.
    palvoice_ensemble_presenter_total
        Which model won the presenter role for a given prompt. Label: (model).
    palvoice_expression_state_changes_total
        Sphere face expression transitions. Labels: (from_state, to_state).

Wiring
------

In ``palvoice.main``::

    from observability.pal_voice.metrics import start_metrics_server
    start_metrics_server(port=7778)
"""

from __future__ import annotations

import logging
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from prometheus_client import (
    CollectorRegistry,
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)


log = logging.getLogger(__name__)


# ── Registry ────────────────────────────────────────────────────────────────
REGISTRY = CollectorRegistry(auto_describe=True)


# ── LLM inference ──────────────────────────────────────────────────────────
LLM_LATENCY = Histogram(
    "palvoice_llm_latency_seconds",
    "LLM inference latency. Phase = prefill|decode|total.",
    labelnames=("model", "phase"),
    # buckets tuned for local Jetson inference (0.05s..30s).
    buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0),
    registry=REGISTRY,
)

LLM_TOKENS = Counter(
    "palvoice_llm_tokens_total",
    "Tokens produced by an LLM turn. `direction` = prompt|completion.",
    labelnames=("model", "direction"),
    registry=REGISTRY,
)


# ── STT / TTS ───────────────────────────────────────────────────────────────
STT_LATENCY = Histogram(
    "palvoice_stt_latency_seconds",
    "Whisper transcription latency for one utterance.",
    labelnames=("model_size",),
    # Whisper on Jetson: small/medium/large land here.
    buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0),
    registry=REGISTRY,
)

TTS_LATENCY = Histogram(
    "palvoice_tts_latency_seconds",
    "Piper synthesis latency.",
    labelnames=("voice",),
    # Piper is fast — most utterances finish under 1s.
    buckets=(0.02, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0),
    registry=REGISTRY,
)


# ── Wake word ───────────────────────────────────────────────────────────────
WAKE_EVENTS = Counter(
    "palvoice_wake_events_total",
    "Wake-word events by outcome.",
    labelnames=("outcome",),  # true_positive | false_positive | cancelled
    registry=REGISTRY,
)


# ── Ensemble consensus ─────────────────────────────────────────────────────
ENSEMBLE_PROMPTS = Counter(
    "palvoice_ensemble_prompts_total",
    "Prompts run through the ensemble (denominator for divergence rate).",
    registry=REGISTRY,
)

ENSEMBLE_DIVERGENCE = Counter(
    "palvoice_ensemble_divergence_total",
    "Times the ensemble detected a gross disagreement between models.",
    registry=REGISTRY,
)

ENSEMBLE_PRESENTER = Counter(
    "palvoice_ensemble_presenter_total",
    "Which model won the presenter role for a prompt.",
    labelnames=("model",),
    registry=REGISTRY,
)


# ── Sphere expression ───────────────────────────────────────────────────────
EXPRESSION_STATE_CHANGES = Counter(
    "palvoice_expression_state_changes_total",
    "Sphere face expression transitions.",
    labelnames=("from_state", "to_state"),
    registry=REGISTRY,
)


# ── HTTP handler ────────────────────────────────────────────────────────────
class _Handler(BaseHTTPRequestHandler):
    # Silence the default access log — noisy, and Prometheus scrapes every 15s.
    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return

    def do_GET(self) -> None:  # noqa: N802 — BaseHTTPRequestHandler API
        if self.path == "/metrics":
            body = generate_latest(REGISTRY)
            self.send_response(200)
            self.send_header("Content-Type", CONTENT_TYPE_LATEST)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path in ("/", "/health"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"pal-voice metrics ok\n")
            return
        self.send_response(404)
        self.end_headers()


def start_metrics_server(
    port: int = 7778, host: str = "0.0.0.0"
) -> ThreadingHTTPServer:
    """Start the metrics HTTP server in a daemon thread and return the server.

    Idempotent-ish: if you call it twice you'll get two servers; call once
    from `pal_voice.main` at startup.
    """
    server = ThreadingHTTPServer((host, port), _Handler)
    thread = threading.Thread(
        target=server.serve_forever, name="palvoice-metrics", daemon=True
    )
    thread.start()
    log.info("pal-voice metrics server listening on %s:%d", host, port)
    return server

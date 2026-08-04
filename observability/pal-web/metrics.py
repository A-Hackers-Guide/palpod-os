"""
palpod-os / observability / pal-web / metrics.py
================================================

FastAPI middleware + registry that exposes a Prometheus /metrics endpoint on
pal-web's own HTTP port (8000 by default — the container-internal port; Traefik
routes external traffic to it).

Metrics exposed
---------------

Histograms
    palweb_http_request_duration_seconds
        HTTP request latency, labeled by (method, route, status_class).
        Route label is templated (e.g. "/api/devices/{device_id}") so unique
        paths do not explode cardinality.

Gauges
    palweb_active_sessions
        Currently signed-in users (WS + REST). Updated by the auth layer.
    palweb_active_grants
        Currently open remote-control grants.
    palweb_grant_seconds_remaining
        Per-grant remaining seconds. Labeled by (grant_id, initiator).
    palweb_remote_devices_registered
        Total rows in the `remote_devices` table.
    palweb_media_sessions
        Concurrent playback per service. Labeled by (service).

Counters
    palweb_input_events_total
        Every input event received on a remote-control websocket. Labels:
        (authorized: "true"|"false", initiator, reason). `reason` is empty
        for authorized events and one of {unauthorized, expired, malformed}
        for rejected ones.
    palweb_extender_heartbeats_total
        Heartbeats from PAL Web Extender clients.
    palweb_remote_grant_events_total
        Every row appended to `remote_grant_events`. Labels: (kind) where kind
        is one of {granted, denied, expired, revoked}.
    palweb_ws_anomalies_total
        Individual WebSocket anomalies (below the noise threshold). Label: (kind).
    palweb_ws_anomalies_suppressed_total
        Aggregated count of anomalies collapsed by the noise-suppression logic
        (i.e. what shows up in `remote_ws_anomaly_summary`). Label: (kind).
    palweb_consent_cooldown_blocks_total
        Consent prompts that were denied because the user is in the cooldown
        window after a previous denial.
    palweb_grant_seconds_used_total
        Cumulative grant seconds consumed. Used by the 24h rolling budget
        gauge on the remote-desktop dashboard.
    palweb_xteve_channel_tunes_total
        Increments each time a client tunes into an xTeVe channel. Label:
        (channel).

Wiring
------

In pal-web's FastAPI app factory::

    from observability.pal_web.metrics import install_metrics
    app = FastAPI()
    install_metrics(app)

Then Prometheus scrapes `http://pal-web:8000/metrics` (see
observability/prometheus/prometheus.yml → job `palpod-services`).
"""

from __future__ import annotations

import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Match


# ── Registry ────────────────────────────────────────────────────────────────
#
# We deliberately use our own CollectorRegistry rather than the process-wide
# default so that pal-web can be reloaded (dev mode) without leaking duplicate
# metric registrations, and so tests can construct an isolated Registry.
REGISTRY = CollectorRegistry(auto_describe=True)


# ── HTTP request latency ────────────────────────────────────────────────────
HTTP_LATENCY = Histogram(
    "palweb_http_request_duration_seconds",
    "Wall-clock HTTP request latency, from receipt of the request to the "
    "moment the response body finishes streaming.",
    labelnames=("method", "route", "status_class"),
    # buckets picked for typical FastAPI JSON endpoints; skew low.
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
    registry=REGISTRY,
)


# ── Session / grant gauges ─────────────────────────────────────────────────
ACTIVE_SESSIONS = Gauge(
    "palweb_active_sessions",
    "Currently signed-in users (WS + REST).",
    registry=REGISTRY,
)

ACTIVE_GRANTS = Gauge(
    "palweb_active_grants",
    "Currently open remote-control grants.",
    registry=REGISTRY,
)

GRANT_SECONDS_REMAINING = Gauge(
    "palweb_grant_seconds_remaining",
    "Seconds remaining on each open grant, labeled by grant_id + initiator.",
    labelnames=("grant_id", "initiator"),
    registry=REGISTRY,
)

REMOTE_DEVICES_REGISTERED = Gauge(
    "palweb_remote_devices_registered",
    "Total rows in the `remote_devices` table.",
    registry=REGISTRY,
)

MEDIA_SESSIONS = Gauge(
    "palweb_media_sessions",
    "Concurrent playback sessions per media service.",
    labelnames=("service",),
    registry=REGISTRY,
)


# ── Counters ────────────────────────────────────────────────────────────────
INPUT_EVENTS = Counter(
    "palweb_input_events_total",
    "Input events received on remote-control websockets. `authorized`=false "
    "means the event was rejected; `reason` explains why.",
    labelnames=("authorized", "initiator", "reason"),
    registry=REGISTRY,
)

EXTENDER_HEARTBEATS = Counter(
    "palweb_extender_heartbeats_total",
    "Heartbeats received from PAL Web Extender clients (browser add-on).",
    registry=REGISTRY,
)

REMOTE_GRANT_EVENTS = Counter(
    "palweb_remote_grant_events_total",
    "Rows appended to `remote_grant_events`. `kind` is one of "
    "granted / denied / expired / revoked.",
    labelnames=("kind",),
    registry=REGISTRY,
)

WS_ANOMALIES = Counter(
    "palweb_ws_anomalies_total",
    "Individual WebSocket protocol anomalies (below the noise threshold).",
    labelnames=("kind",),
    registry=REGISTRY,
)

WS_ANOMALIES_SUPPRESSED = Counter(
    "palweb_ws_anomalies_suppressed_total",
    "Anomalies collapsed into a single row by the noise-suppression logic; "
    "counted in remote_ws_anomaly_summary.",
    labelnames=("kind",),
    registry=REGISTRY,
)

CONSENT_COOLDOWN_BLOCKS = Counter(
    "palweb_consent_cooldown_blocks_total",
    "Consent prompts denied because the user was in the cooldown window "
    "after a previous denial.",
    registry=REGISTRY,
)

GRANT_SECONDS_USED = Counter(
    "palweb_grant_seconds_used_total",
    "Cumulative seconds consumed by grants (drives the 24h rolling budget).",
    registry=REGISTRY,
)

XTEVE_CHANNEL_TUNES = Counter(
    "palweb_xteve_channel_tunes_total",
    "Increments each time a client tunes into an xTeVe channel.",
    labelnames=("channel",),
    registry=REGISTRY,
)


# ── HTTP middleware ─────────────────────────────────────────────────────────
class PrometheusMiddleware(BaseHTTPMiddleware):
    """Time every request, then record the observation into HTTP_LATENCY.

    We resolve the *route template* (e.g. "/api/devices/{device_id}") rather
    than the raw path so a fleet with 500 devices does not create 500 label
    series. Requests that do not match a known route are labeled "<unmatched>"
    so we can see (but not enumerate) 404 traffic.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # /metrics itself must never appear in the histogram.
        if request.url.path == "/metrics":
            return await call_next(request)

        start = time.perf_counter()
        response: Response
        try:
            response = await call_next(request)
        except Exception:
            # Record a 5xx observation even if the handler raised.
            elapsed = time.perf_counter() - start
            HTTP_LATENCY.labels(
                method=request.method,
                route=_resolve_route(request),
                status_class="5xx",
            ).observe(elapsed)
            raise
        elapsed = time.perf_counter() - start
        HTTP_LATENCY.labels(
            method=request.method,
            route=_resolve_route(request),
            status_class=f"{response.status_code // 100}xx",
        ).observe(elapsed)
        return response


def _resolve_route(request: Request) -> str:
    """Return the parameterised route template for a request, or a fallback."""
    app = request.scope.get("app")
    if app is None:
        return "<unknown>"
    for route in getattr(app, "routes", []):
        match, _ = route.matches(request.scope)
        if match == Match.FULL:
            return getattr(route, "path", "<unmatched>")
    return "<unmatched>"


# ── /metrics endpoint ───────────────────────────────────────────────────────
def _metrics_endpoint() -> Response:
    payload = generate_latest(REGISTRY)
    return Response(content=payload, media_type=CONTENT_TYPE_LATEST)


def install_metrics(app: FastAPI) -> None:
    """Attach the middleware and mount /metrics on the given FastAPI app.

    Idempotent: safe to call more than once (e.g. under uvicorn --reload).
    """
    # Middleware — inserted at position 0 so we measure the full pipeline.
    app.add_middleware(PrometheusMiddleware)

    # Endpoint — only add it if it isn't already there.
    if not any(getattr(r, "path", "") == "/metrics" for r in app.routes):
        app.add_api_route(
            "/metrics",
            _metrics_endpoint,
            methods=["GET"],
            include_in_schema=False,
            name="prometheus_metrics",
        )

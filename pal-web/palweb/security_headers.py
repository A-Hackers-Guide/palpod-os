"""HTTP security-header middleware for pal-web.

The reviewer's write-up:

* CSP must be a real HTTP header (a ``<meta>`` tag is advisory only and
  browsers can't enforce ``frame-ancestors`` from meta at all).
* ``'unsafe-inline'`` is banned in ``style-src`` — the UI has no inline
  styles.
* Adjacent headers: ``X-Content-Type-Options``, ``X-Frame-Options``,
  ``Referrer-Policy``, ``Permissions-Policy``.

The header block is intentionally identical on every response so tests can
compare an exact byte-equal string. Do NOT relax ``script-src`` or
``style-src`` casually — every relaxation opens a same-origin XSS mint-grant
vector.
"""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


CSP_HEADER_VALUE = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self'; "
    "connect-src 'self' ws://pod.palpod.local wss://pod.palpod.local; "
    "object-src 'none'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'"
)

_STATIC_SECURITY_HEADERS: tuple[tuple[str, str], ...] = (
    ("Content-Security-Policy", CSP_HEADER_VALUE),
    ("X-Content-Type-Options", "nosniff"),
    ("X-Frame-Options", "DENY"),
    ("Referrer-Policy", "strict-origin-when-cross-origin"),
    ("Permissions-Policy", "interest-cohort=()"),
)


class CSPMiddleware(BaseHTTPMiddleware):
    """Emit the security-header block on every response, unconditionally.

    Placed outside of CSRF so the headers cover error responses too — a 403
    JSON body still gets a CSP header. If any header is already present the
    middleware leaves it alone; that's a safety hatch for a single handler
    that wants to override (currently unused).
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)
        for name, value in _STATIC_SECURITY_HEADERS:
            # ``setdefault`` semantics — don't stomp an intentional override.
            if name not in response.headers:
                response.headers[name] = value
        return response

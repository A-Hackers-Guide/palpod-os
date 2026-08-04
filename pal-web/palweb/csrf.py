"""CSRF middleware for pal-web.

Behavior:

* On every response to a HTML GET (either ``/remote.html`` explicitly or any
  ``text/html`` page under ``/static``), we ensure a ``palpod_csrf`` cookie is
  set. The cookie is ``HttpOnly=False`` on purpose — the browser page needs
  to read it and echo it as an ``X-CSRF-Token`` header on state-changing
  requests.
* On every ``POST/PUT/PATCH/DELETE`` to an ``/api/*`` route (except
  ``/api/auth/login``, which mints the initial cookie), we require the header
  ``X-CSRF-Token`` to match the cookie exactly.
* Requests that carry a **valid** ``X-Palpod-Agent-Token`` header (byte-equal
  to the configured secret via :func:`hmac.compare_digest`) are exempt — the
  agent uses a bearer token and is not subject to CSRF. Presence of the
  header alone is NOT enough; the previous exemption rule silently trusted
  any string. See the regression test
  ``test_regression_bogus_agent_token_does_not_bypass_csrf``.
* A request that carries BOTH the agent token AND a valid ``palpod_session``
  cookie is rejected outright with 403 ``conflicting credentials``. A browser
  cannot legitimately hold the agent secret; that combination is an XSS-
  smuggled token or a confused-deputy attack and must never be honoured.

CSRF is one layer of a stack: the CORS middleware in front rejects
cross-origin requests entirely; the Origin-header check in the grant-control
route re-validates. Every mutating router handler ALSO calls
:func:`verify_csrf_double_submit` as a defense-in-depth dependency so a bug in
one layer doesn't collapse the whole gate. If any single one of the four
layers holds, the same-origin XSS vector is neutered.
"""

from __future__ import annotations

import hmac
from typing import Iterable

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .auth import (
    AGENT_TOKEN_HEADER,
    CSRF_COOKIE_NAME,
    CSRF_HEADER_NAME,
    SESSION_COOKIE_NAME,
    _get_agent_token,
    csrf_token_is_valid_shape,
    mint_csrf_token,
)


# Endpoints where a caller is allowed to establish state without a prior CSRF
# cookie. Login mints the cookie; adding it here means the *first* login POST
# doesn't need one.
CSRF_EXEMPT_PATHS = frozenset(
    {
        "/api/auth/login",
    }
)


UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def _agent_token_is_valid(request: Request) -> bool:
    """Return True iff ``X-Palpod-Agent-Token`` is present AND byte-equal to
    the configured agent secret. Constant-time compare via
    :func:`hmac.compare_digest`.
    """
    presented = request.headers.get(AGENT_TOKEN_HEADER)
    if not presented:
        return False
    return hmac.compare_digest(presented, _get_agent_token())


class CSRFMiddleware(BaseHTTPMiddleware):
    """Double-submit CSRF: cookie value must equal header value on writes."""

    def __init__(self, app, *, protected_prefixes: Iterable[str] = ("/api/",)) -> None:
        super().__init__(app)
        self._protected_prefixes = tuple(protected_prefixes)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method.upper()

        needs_csrf_check = (
            method in UNSAFE_METHODS
            and any(path.startswith(p) for p in self._protected_prefixes)
            and path not in CSRF_EXEMPT_PATHS
        )

        if needs_csrf_check:
            # A caller cannot legitimately hold BOTH a browser session AND
            # the agent secret — a browser can't be given the agent token
            # without side-loading, and mixing the two credentials is a clear
            # confused-deputy signal. Reject regardless of what token is
            # presented.
            agent_present = bool(request.headers.get(AGENT_TOKEN_HEADER))
            session_present = bool(request.cookies.get(SESSION_COOKIE_NAME))
            if agent_present and session_present:
                return _forbidden("conflicting credentials")

            # Exempt ONLY on a byte-valid agent token. Presence-only is a
            # bypass (the previous version trusted `if header:` alone).
            if not _agent_token_is_valid(request):
                cookie_token = request.cookies.get(CSRF_COOKIE_NAME)
                header_token = request.headers.get(CSRF_HEADER_NAME)
                if not cookie_token or not header_token:
                    return _forbidden("CSRF token missing")
                if not csrf_token_is_valid_shape(cookie_token):
                    return _forbidden("CSRF cookie malformed")
                if not hmac.compare_digest(cookie_token, header_token):
                    return _forbidden("CSRF token mismatch")

        response: Response = await call_next(request)

        # Seat the CSRF cookie on any successful GET to the remote UI (or the
        # /api/auth/login response, which fires *before* the browser has had
        # a chance to see any HTML). The cookie is NOT HttpOnly by design —
        # the browser page reads it and echoes into the header.
        needs_cookie = (
            (method == "GET" and (path.endswith("remote.html") or path == "/remote.html"))
            or path == "/api/auth/login"
        )
        if needs_cookie and CSRF_COOKIE_NAME not in request.cookies:
            token = mint_csrf_token()
            # Save for the route to embed as a <meta> tag (see main.py).
            request.state.csrf_token = token
            response.set_cookie(
                CSRF_COOKIE_NAME,
                token,
                httponly=False,        # readable by page JS on purpose
                secure=_should_mark_secure(request),
                samesite="strict",
                max_age=60 * 60 * 24,  # one day
                path="/",
            )

        return response


def _should_mark_secure(request: Request) -> bool:
    # Test client uses http://testserver — don't drop the cookie there.
    return request.url.scheme == "https"


def _forbidden(detail: str) -> Response:
    from starlette.responses import JSONResponse

    return JSONResponse(status_code=403, content={"detail": detail})


# --------------------------------------------------------------------------- #
# Router-level defense-in-depth helper
# --------------------------------------------------------------------------- #


def verify_csrf_double_submit(request: Request) -> bool:
    """Return True iff the request presents matching CSRF cookie + header.

    Called from mutating route handlers as a FastAPI dependency: the
    middleware is first line, this is second line, so a same-origin XSS that
    reads ``document.cookie`` and echoes it into ``X-CSRF-Token`` still has
    to defeat BOTH layers to mint a grant. Both values are present AND
    byte-equal via :func:`hmac.compare_digest`.

    Callers exempt this check when the request is authenticated with a valid
    agent token (bearer auth doesn't need CSRF); pass that decision at the
    route level.
    """
    cookie_token = request.cookies.get(CSRF_COOKIE_NAME)
    header_token = request.headers.get(CSRF_HEADER_NAME)
    if not cookie_token or not header_token:
        return False
    if not csrf_token_is_valid_shape(cookie_token):
        return False
    return hmac.compare_digest(cookie_token, header_token)


def require_csrf_double_submit(request: Request) -> None:
    """FastAPI dependency: 403 unless CSRF double-submit is valid.

    Agent-token calls are exempt (bearer auth) — provided the token itself
    is byte-valid. This mirrors the middleware exemption rule and is the
    same-shape check applied twice for defense in depth.
    """
    # Refuse any request that mixes the two credentials (see middleware).
    agent_present = bool(request.headers.get(AGENT_TOKEN_HEADER))
    session_present = bool(request.cookies.get(SESSION_COOKIE_NAME))
    if agent_present and session_present:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="conflicting credentials",
        )
    if _agent_token_is_valid(request):
        return
    if not verify_csrf_double_submit(request):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token missing or mismatched",
        )

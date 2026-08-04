"""pal-web FastAPI application entrypoint.

Middleware order (this is load-bearing — do NOT re-shuffle):

    request → CSP → CORS → CSRF → routers

CSP (and the adjacent security-header block) is outermost so the block also
covers 4xx JSON responses that shortcut later middleware. CORS is next so it
can early-reject a hostile origin before the rest of the stack sees it. CSRF
sits just inside because it needs the request to have already been "accepted"
as coming from a permitted origin — the double-submit check adds a second
gate against same-origin XSS. Session-cookie parsing is done inline in the
FastAPI dependencies, not as middleware, because FastAPI already makes
cookies available to :func:`palweb.auth.current_user`.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import Cookie, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .auth import (
    CSRF_COOKIE_NAME,
    SESSION_COOKIE_NAME,
    SESSION_TTL_SECONDS,
    POD_OWNER_USER_ID,
    allowed_origins,
    mint_csrf_token,
    sign_session,
    verify_password,
)
from .clients.rustdesk import RustDeskClient
from .csrf import CSRFMiddleware
from .routers.remote import router as remote_router, ws_router as remote_ws_router
from .schemas import LoginRequest, LoginResponse
from .security_headers import CSPMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title="pal-web", version="0.3.0")

    # RustDesk client singleton on app.state (shared with the WS handler).
    app.state.rustdesk_client = RustDeskClient()

    # ORDER MATTERS. Starlette applies middleware bottom-up on requests, so
    # the LAST-added is the OUTERMOST. Register CSRF first, then CORS, then
    # CSP so the effective request order is CSP → CORS → CSRF → routers, and
    # every response (including 403s produced by CSRF) still carries the
    # full security-header block.
    app.add_middleware(CSRFMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(allowed_origins()),
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "X-Consent-Origin",
            "X-CSRF-Token",
            "X-Palpod-Agent-Token",
        ],
    )
    app.add_middleware(CSPMiddleware)

    # Auth: single-user login. The password comes from PALPOD_USER_PASSWORD;
    # the response sets the signed session cookie AND seats a CSRF cookie so
    # the very first POST after login has a matching pair.
    @app.post("/api/auth/login", response_model=LoginResponse)
    async def login(body: LoginRequest, response: Response) -> LoginResponse:
        if not verify_password(body.password):
            # Same-shape error for right + wrong to avoid a timing side-channel
            # on wrong-shape passwords. The hash comparison itself is
            # already constant-time via argon2/scrypt+compare_digest.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid password",
            )

        response.set_cookie(
            SESSION_COOKIE_NAME,
            sign_session(POD_OWNER_USER_ID),
            httponly=True,
            secure=False,   # dev/test — set true behind TLS in prod
            samesite="strict",
            max_age=SESSION_TTL_SECONDS,
            path="/",
        )
        # Seat CSRF cookie now so the JS layer can start emitting the header
        # without a separate GET.
        response.set_cookie(
            CSRF_COOKIE_NAME,
            mint_csrf_token(),
            httponly=False,
            secure=False,
            samesite="strict",
            max_age=SESSION_TTL_SECONDS,
            path="/",
        )
        return LoginResponse(ok=True, user_id=POD_OWNER_USER_ID)

    @app.post("/api/auth/logout")
    async def logout(response: Response) -> dict:
        response.delete_cookie(SESSION_COOKIE_NAME, path="/")
        return {"ok": True}

    # Serve remote.html from the TEMPLATE directory (NOT palweb/static/) so
    # /static/remote.html is a hard 404. The previous shape let StaticFiles
    # serve the raw file at /static/remote.html and skip the CSRF-cookie
    # seeding entirely — a fresh browser landing there would issue writes
    # with no cookie set. Now the file only lives in palweb/templates/ and
    # this handler is the canonical entry point.
    template_dir = Path(__file__).parent / "templates"

    @app.get("/remote.html", response_class=HTMLResponse)
    async def remote_page(
        request: Request,
        csrf_cookie: str | None = Cookie(default=None, alias=CSRF_COOKIE_NAME),
    ) -> HTMLResponse:
        page = (template_dir / "remote.html").read_text(encoding="utf-8")

        # Prefer an existing cookie value (so the token in the DOM matches the
        # cookie the browser will send), otherwise use the fresh one that the
        # CSRF middleware is about to set on the response.
        token = csrf_cookie or getattr(request.state, "csrf_token", None) or mint_csrf_token()
        request.state.csrf_token = token  # nudge middleware to reuse this one

        needle = "<!-- CSRF -->"
        meta_tag = f'<meta name="csrf-token" content="{token}" />'
        if needle in page:
            page = page.replace(needle, meta_tag)
        else:
            page = page.replace("</head>", f"  {meta_tag}\n</head>", 1)
        return HTMLResponse(content=page)

    # Register the remote-control router (REST + WS).
    app.include_router(remote_router)
    app.include_router(remote_ws_router)

    # Serve the static UI assets — CSS + JS only, HTML disabled. The
    # ``html=False`` disables the "serve index.html on directory paths"
    # behaviour; the important part is that remote.html has been physically
    # removed from this directory so /static/remote.html is a plain 404.
    static_dir = Path(__file__).parent / "static"
    app.mount("/static", StaticFiles(directory=str(static_dir), html=False), name="static")

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # pragma: no cover — lifecycle
        await app.state.rustdesk_client.close()

    return app


app = create_app()

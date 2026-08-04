"""Shared test fixtures for pal-web.

The pal-web test suite is designed to work without a live Postgres — models
are re-declared against SQLite for tests via SQLAlchemy's dialect
translation (JSONB -> JSON, UUID -> CHAR(36), gen_random_uuid removed). A
dedicated in-memory engine is spun up per test.

Post-security-hardening every test now runs behind:

* the CORS middleware (allow-lists ``http://testserver``)
* the CSRF middleware (requires ``X-CSRF-Token`` on writes)
* the ``current_user`` dependency (requires ``palpod_session`` cookie)

The ``client`` fixture below already logs in and stashes the CSRF token so
existing tests can keep POSTing without every one of them running through the
auth dance. Tests that specifically exercise the AUTH gates (missing cookie,
wrong CSRF, etc.) get a bare fixture below (``unauth_client``).
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import AsyncIterator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from palweb import auth as auth_module
from palweb import database as db_module
from palweb.database import Base
from palweb.main import create_app


# In-memory DB. StaticPool + check_same_thread=False keeps a single connection
# alive for the lifetime of the engine so writes from the ASGI thread are
# visible to reads on the test coroutine's thread.
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

# Deterministic secrets for reproducibility. Set BEFORE importing anything
# that reads the env.
os.environ.setdefault("PALPOD_USER_PASSWORD", "hunter2-hunter2")
os.environ.setdefault("PALPOD_SESSION_SECRET", "test-session-secret")
os.environ.setdefault("PALPOD_AGENT_TOKEN", "test-agent-token")
os.environ.setdefault(
    "PALPOD_ALLOWED_ORIGINS",
    "http://testserver,http://localhost,http://127.0.0.1",
)




@pytest_asyncio.fixture
async def engine():
    # StaticPool so the WS handler thread + the test thread share the same
    # in-memory SQLite connection. Without it, each thread opens its own
    # (empty) in-memory database and writes made in the ASGI thread are
    # invisible to the test asserting them.
    from sqlalchemy.pool import StaticPool

    eng = create_async_engine(
        TEST_DB_URL,
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    from palweb import models  # noqa: F401 — ensure model imports run

    # Register SQLite user functions so the postgres-native ``server_default``
    # calls (``now()`` and ``gen_random_uuid()``) don't blow up.
    import uuid as _uuid
    from datetime import datetime as _dt, timezone as _tz

    from sqlalchemy import event as _event

    def _register_udf(dbapi_conn, _):
        try:
            dbapi_conn.create_function("now", 0, lambda: _dt.now(_tz.utc).isoformat())
            dbapi_conn.create_function("gen_random_uuid", 0, lambda: str(_uuid.uuid4()))
        except Exception:  # noqa: BLE001
            pass

    _event.listen(eng.sync_engine, "connect", _register_udf)

    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield eng
    await eng.dispose()


@pytest_asyncio.fixture
async def session_factory(engine):
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture
async def app(session_factory, monkeypatch) -> AsyncIterator[FastAPI]:
    # Force a fresh password hash + secret load against the current env.
    auth_module.reset_auth_config_for_tests()

    # Point the app's SessionLocal at the test engine.
    monkeypatch.setattr(db_module, "SessionLocal", session_factory)
    from palweb.routers import remote as remote_router_mod
    monkeypatch.setattr(remote_router_mod, "SessionLocal", session_factory)

    application = create_app()

    async def _get_db_override() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    from palweb.database import get_db
    application.dependency_overrides[get_db] = _get_db_override
    yield application


@pytest_asyncio.fixture
async def unauth_client(app) -> AsyncIterator[AsyncClient]:
    """An httpx client with NO login performed — for auth-gate tests."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        headers={"Origin": "http://testserver"},
    ) as c:
        yield c


@pytest_asyncio.fixture
async def client(app) -> AsyncIterator[AsyncClient]:
    """Logged-in client with CSRF header pre-populated.

    The client sets ``Origin: http://testserver`` on every request so that
    the grant-control Origin allowlist check passes. After ``POST
    /api/auth/login`` the ``palpod_session`` cookie AND ``palpod_csrf``
    cookie are in the jar; the CSRF value is echoed into an
    ``X-CSRF-Token`` header default so state-changing tests work
    transparently.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        headers={"Origin": "http://testserver"},
    ) as c:
        # Log in — this seats both cookies.
        resp = await c.post(
            "/api/auth/login",
            json={"password": os.environ["PALPOD_USER_PASSWORD"]},
        )
        assert resp.status_code == 200, resp.text

        csrf = c.cookies.get("palpod_csrf")
        assert csrf, "login should have seated palpod_csrf"
        c.headers["X-CSRF-Token"] = csrf
        # Legacy header the router expects for the explicit-consent gate.
        # Tests that override it can pass headers= per request.
        yield c


@pytest_asyncio.fixture
async def agent_client(app) -> AsyncIterator[AsyncClient]:
    """Client that authenticates via the AI-agent bearer token, NOT a session."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        headers={
            "Origin": "http://testserver",
            "X-Palpod-Agent-Token": os.environ["PALPOD_AGENT_TOKEN"],
        },
    ) as c:
        yield c


@pytest.fixture
def ws_test_client(app):
    """Synchronous TestClient for WebSocket tests.

    Auto-logs-in the single-user session so that the ``palpod_session``
    cookie is in the jar when :func:`websocket_connect` performs the
    handshake. Tests that specifically want an UN-authenticated WS use
    :func:`unauth_ws_test_client` below.
    """
    c = TestClient(app)
    resp = c.post(
        "/api/auth/login",
        json={"password": os.environ["PALPOD_USER_PASSWORD"]},
    )
    assert resp.status_code == 200, resp.text
    csrf = c.cookies.get("palpod_csrf")
    assert csrf
    c.headers["X-CSRF-Token"] = csrf
    c.headers["Origin"] = "http://testserver"
    return c


@pytest.fixture
def agent_ws_test_client(app):
    """Synchronous TestClient authenticated via the agent bearer token."""
    c = TestClient(app)
    c.headers["X-Palpod-Agent-Token"] = os.environ["PALPOD_AGENT_TOKEN"]
    c.headers["Origin"] = "http://testserver"
    return c


@pytest.fixture
def unauth_ws_test_client(app):
    """Bare TestClient with no auth — for unauthenticated-WS tests."""
    return TestClient(app)


@pytest_asyncio.fixture
async def paired_device(client) -> dict:
    """Register a device and return its JSON representation."""
    resp = await client.post(
        "/api/remote/devices",
        json={
            "display_name": "Office Mac",
            "device_type": "macos",
            "rustdesk_id": "111222333",
            "auth_token": "tok-abc",
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def utcnow() -> datetime:
    return datetime.now(timezone.utc)

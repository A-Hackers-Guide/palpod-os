"""Authentication + session cookie machinery for pal-web.

The MVP single-user Pod has three distinct authenticated principals:

* ``user``     — a browser session tied to the device-local password stored in
                 ``.env`` as ``PALPOD_USER_PASSWORD``. Login is
                 ``POST /api/auth/login`` and the response sets a signed
                 ``palpod_session`` cookie.
* ``ai-agent`` — a REST caller presenting the ``X-Palpod-Agent-Token`` header
                 whose value matches ``PALPOD_AGENT_TOKEN``. This token is
                 minted for the voice orchestrator only.
* ``unauth``   — nothing valid presented. Endpoints that require a user return
                 401. Endpoints that accept either principal (a very small set)
                 reject with 401 if neither is present.

Security-critical rules — do not relax without a review:

1. The password never lands in the database. It is read from the env, hashed
   on process start with argon2 (falling back to :func:`hashlib.scrypt` when
   the ``argon2-cffi`` extra isn't installed), and compared with a constant-
   time :func:`hmac.compare_digest`.
2. Session cookies are HMAC-signed with ``PALPOD_SESSION_SECRET``. Tamper the
   cookie, get a 401. The signature is over the full payload including the
   issue timestamp.
3. Cookies are ``HttpOnly``, ``Secure``, ``SameSite=Strict``. XSS cannot exfil
   the session and cross-site requests cannot ride it (a defense complementary
   to CSRF).
4. The initiator on every audited event is derived from the *authenticated
   principal type* — never from a request body or query string.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
import uuid
from dataclasses import dataclass
from typing import Literal, Optional

from fastapi import Cookie, Depends, Header, HTTPException, Request, status


# --------------------------------------------------------------------------- #
# Environment-driven secrets
# --------------------------------------------------------------------------- #

# Single-user Pod: one owner user_id, deterministic so tests + migrations agree.
POD_OWNER_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")

# Cookie / header names — used from routes AND CSRF middleware.
SESSION_COOKIE_NAME = "palpod_session"
CSRF_COOKIE_NAME = "palpod_csrf"
CSRF_HEADER_NAME = "X-CSRF-Token"
AGENT_TOKEN_HEADER = "X-Palpod-Agent-Token"

# 24 h session TTL. Grants are the real security boundary; the session cookie
# just says "this browser was authenticated recently."
SESSION_TTL_SECONDS = 24 * 60 * 60


PrincipalKind = Literal["user", "ai-agent"]


@dataclass(frozen=True)
class Principal:
    """The authenticated caller derived server-side.

    ``kind`` is what gets written into ``RemoteInputEvent.initiator`` and
    ``RemoteSession.initiated_by``. Clients cannot influence it.
    """

    kind: PrincipalKind
    user_id: uuid.UUID


# --------------------------------------------------------------------------- #
# Password hashing — argon2 preferred, scrypt fallback
# --------------------------------------------------------------------------- #

try:  # pragma: no cover — import guard
    from argon2 import PasswordHasher  # type: ignore

    _argon2_hasher = PasswordHasher()

    def _hash_password(plaintext: str) -> str:
        return _argon2_hasher.hash(plaintext)

    def _verify_password(hashed: str, plaintext: str) -> bool:
        try:
            return _argon2_hasher.verify(hashed, plaintext)
        except Exception:  # noqa: BLE001 — argon2 raises many subclasses
            return False

except ImportError:  # pragma: no cover — fallback path
    # stdlib-only fallback: scrypt with a random salt, delimited encoding.
    def _hash_password(plaintext: str) -> str:
        salt = secrets.token_bytes(16)
        dk = hashlib.scrypt(plaintext.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)
        return "scrypt$" + base64.urlsafe_b64encode(salt).decode() + "$" + base64.urlsafe_b64encode(dk).decode()

    def _verify_password(hashed: str, plaintext: str) -> bool:
        try:
            scheme, salt_b64, dk_b64 = hashed.split("$", 2)
            if scheme != "scrypt":
                return False
            salt = base64.urlsafe_b64decode(salt_b64)
            expected = base64.urlsafe_b64decode(dk_b64)
            got = hashlib.scrypt(plaintext.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)
            return hmac.compare_digest(expected, got)
        except Exception:  # noqa: BLE001
            return False


# --------------------------------------------------------------------------- #
# In-memory hash of the env password. Rehashed only on process start.
# --------------------------------------------------------------------------- #

_password_hash: Optional[str] = None
_session_secret_bytes: Optional[bytes] = None
_agent_token: Optional[str] = None


def _load_config_from_env() -> None:
    """Read env vars and cache the password hash + session secret.

    Called lazily by :func:`get_password_hash` and :func:`_session_secret` so
    tests can override the env before the first read.
    """
    global _password_hash, _session_secret_bytes, _agent_token

    pw = os.environ.get("PALPOD_USER_PASSWORD", "palpod-dev-password")
    _password_hash = _hash_password(pw)

    secret = os.environ.get("PALPOD_SESSION_SECRET")
    if not secret:
        # Deterministic per-process default so tests are reproducible; a real
        # deployment must set the env var (documented in the README).
        secret = "palpod-dev-session-secret-CHANGEME"
    _session_secret_bytes = secret.encode("utf-8")

    _agent_token = os.environ.get("PALPOD_AGENT_TOKEN", "palpod-dev-agent-token")


def reset_auth_config_for_tests() -> None:
    """Test hook: force-reload of env-derived config."""
    global _password_hash, _session_secret_bytes, _agent_token
    _password_hash = None
    _session_secret_bytes = None
    _agent_token = None


def _password_hash_or_load() -> str:
    if _password_hash is None:
        _load_config_from_env()
    assert _password_hash is not None
    return _password_hash


def _session_secret() -> bytes:
    if _session_secret_bytes is None:
        _load_config_from_env()
    assert _session_secret_bytes is not None
    return _session_secret_bytes


def _get_agent_token() -> str:
    if _agent_token is None:
        _load_config_from_env()
    assert _agent_token is not None
    return _agent_token


def verify_password(plaintext: str) -> bool:
    """Constant-time check of a login attempt against the env password."""
    return _verify_password(_password_hash_or_load(), plaintext)


# --------------------------------------------------------------------------- #
# Cookie signing / verification
# --------------------------------------------------------------------------- #


def _b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64u_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


def sign_session(user_id: uuid.UUID) -> str:
    """Return an opaque signed session cookie value for ``user_id``."""
    payload = {"uid": str(user_id), "iat": int(time.time())}
    body = _b64u(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    sig = _b64u(hmac.new(_session_secret(), body.encode("ascii"), hashlib.sha256).digest())
    return f"{body}.{sig}"


def verify_session(cookie_value: str) -> Optional[uuid.UUID]:
    """Return the user_id if the cookie is valid and unexpired, else None."""
    try:
        body, sig = cookie_value.split(".", 1)
    except ValueError:
        return None
    expected_sig = _b64u(
        hmac.new(_session_secret(), body.encode("ascii"), hashlib.sha256).digest()
    )
    if not hmac.compare_digest(sig, expected_sig):
        return None
    try:
        payload = json.loads(_b64u_decode(body).decode("utf-8"))
        iat = int(payload["iat"])
        uid = uuid.UUID(payload["uid"])
    except (KeyError, ValueError, json.JSONDecodeError):
        return None
    if int(time.time()) - iat > SESSION_TTL_SECONDS:
        return None
    return uid


# --------------------------------------------------------------------------- #
# CSRF token helpers
# --------------------------------------------------------------------------- #


def mint_csrf_token() -> str:
    """A fresh, signed CSRF token to seat into the CSRF cookie."""
    raw = secrets.token_bytes(18)
    body = _b64u(raw)
    sig = _b64u(hmac.new(_session_secret(), body.encode("ascii"), hashlib.sha256).digest())
    return f"{body}.{sig}"


def csrf_token_is_valid_shape(token: str) -> bool:
    """Sanity-check a CSRF token's own signature (cheap defense-in-depth).

    The primary CSRF check is *cookie-vs-header equality*; this only rejects
    obvious garbage (wrong shape, wrong signer).
    """
    try:
        body, sig = token.split(".", 1)
    except ValueError:
        return False
    expected = _b64u(
        hmac.new(_session_secret(), body.encode("ascii"), hashlib.sha256).digest()
    )
    return hmac.compare_digest(sig, expected)


def hash_csrf_token(token: str) -> str:
    """Return a hex sha256 of the CSRF token — persisted alongside grants."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# Origin / Referer validation
# --------------------------------------------------------------------------- #

DEFAULT_ALLOWED_ORIGINS: tuple[str, ...] = (
    "http://pod.palpod.local",
    "https://pod.palpod.local",
    # Test client + local dev — must be in the allowed set or every test breaks.
    "http://testserver",
    "http://localhost",
    "http://127.0.0.1",
)


def allowed_origins() -> tuple[str, ...]:
    """Return the origin allowlist for CORS + Origin-header checks.

    Reads ``PALPOD_ALLOWED_ORIGINS`` (comma-separated) if set; otherwise a
    dev-friendly default that includes ``testserver`` so the httpx test client
    can hit the API.
    """
    env = os.environ.get("PALPOD_ALLOWED_ORIGINS")
    if env:
        return tuple(o.strip() for o in env.split(",") if o.strip())
    return DEFAULT_ALLOWED_ORIGINS


def origin_or_referer_allowed(origin: Optional[str], referer: Optional[str]) -> bool:
    """True iff at least one of ``Origin`` / ``Referer`` matches the allowlist."""
    allowed = allowed_origins()
    if origin and origin in allowed:
        return True
    if not origin and referer:
        # Match by scheme+host+port prefix.
        for a in allowed:
            if referer.startswith(a + "/") or referer == a:
                return True
    return False


# --------------------------------------------------------------------------- #
# FastAPI dependencies
# --------------------------------------------------------------------------- #


async def current_principal(
    request: Request,
    session_cookie: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE_NAME),
    agent_token: Optional[str] = Header(default=None, alias=AGENT_TOKEN_HEADER),
) -> Principal:
    """Return the authenticated principal, or raise 401.

    Precedence: session cookie wins. Only if no session cookie is present do
    we consider the agent token — that way a compromised browser session can
    never masquerade as the agent.
    """
    _ = request  # kept in signature for future use (e.g. rate limiting per-IP)
    if session_cookie:
        uid = verify_session(session_cookie)
        if uid is not None:
            return Principal(kind="user", user_id=uid)

    if agent_token and hmac.compare_digest(agent_token, _get_agent_token()):
        return Principal(kind="ai-agent", user_id=POD_OWNER_USER_ID)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="authentication required",
    )


async def current_user(principal: Principal = Depends(current_principal)) -> Principal:
    """Require a session-cookie-backed user principal (rejects agent tokens)."""
    if principal.kind != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user session required (agent token cannot grant control)",
        )
    return principal

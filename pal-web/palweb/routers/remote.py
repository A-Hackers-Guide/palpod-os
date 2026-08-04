"""FastAPI router for remote-device pairing, control grants, and streaming.

Security model — session-scoped consent, now with the reviewer-mandated
layered defenses. The relevant rules, in the order a request meets them:

1. **CORS** — a hostile origin can't even send a credentialed request.
2. **CSRF middleware** — same-origin XSS still trips because it lacks the
   double-submit token (:mod:`palweb.csrf`).
3. **Session cookie** — :func:`palweb.auth.current_user` refuses anything
   without a signed ``palpod_session`` cookie. The old hardcoded
   ``owner_user_id`` is gone.
4. **Origin/Referer allowlist** — :func:`grant_control` re-validates the
   request's origin. XSS from a whitelisted subresource still fails here.
5. **Owner-scoped queries** — every device lookup filters by
   ``owner_user_id == current_user.user_id``. Cross-tenant access is
   impossible even if some future bypass sneaks past the auth layer.
6. **Grant rate limits** — 30 s cool-down between mints, 240 min rolling
   24 h cap, both computed from ``remote_grant_events`` in a single txn.
7. **Server-derived initiator** — the WS handshake pins the caller's
   principal type; a client-supplied ``initiator`` field is either 422'd or
   silently overridden. The audit trail never carries a claim from the
   client about who they are.
8. **Client re-check** — :class:`RustDeskClient` still asserts the grant is
   active on every input dispatch (defense in depth).

All input events and every non-input / malformed envelope are logged.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Header,
    HTTPException,
    Query,
    Request,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from pydantic import ValidationError
from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import (
    AGENT_TOKEN_HEADER,
    CSRF_COOKIE_NAME,
    CSRF_HEADER_NAME,
    SESSION_COOKIE_NAME,
    Principal,
    _get_agent_token,
    csrf_token_is_valid_shape,
    current_user,
    current_principal,
    hash_csrf_token,
    origin_or_referer_allowed,
    verify_session,
)
from ..csrf import require_csrf_double_submit
from ..clients.rustdesk import (
    InsufficientAuthorization,
    RustDeskClient,
)
from ..database import SessionLocal, get_db
from ..models import (
    RemoteDevice,
    RemoteGrantEvent,
    RemoteInputEvent,
    RemoteSession,
    RemoteWSAnomaly,
    RemoteWSAnomalySummary,
)
from ..schemas import (
    ControlState,
    DeviceOut,
    DeviceRegisterRequest,
    GrantControlRequest,
    GrantControlResponse,
    GrantEventOut,
    InputEventEnvelope,
    RevokeControlResponse,
    SessionAnomaliesOut,
    SessionCreateRequest,
    SessionOut,
    WSAnomalyOut,
    WSAnomalySummaryOut,
)

router = APIRouter(prefix="/api/remote", tags=["remote"])

# WebSocket router lives at a different prefix so the path is /ws/remote/...
ws_router = APIRouter(prefix="/ws/remote", tags=["remote-ws"])


# --------------------------------------------------------------------------- #
# Grant-rollover policy (BYPASS #6 fix)
# --------------------------------------------------------------------------- #

GRANT_COOLDOWN_SECONDS = 30
GRANT_DAILY_BUDGET_MINUTES = 240
GRANT_ROLLING_WINDOW = timedelta(hours=24)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def _now() -> datetime:
    """UTC-aware `now()`. Isolated so tests can monkey-patch time."""
    return datetime.now(timezone.utc)


def _control_state(device: RemoteDevice) -> ControlState:
    """Map a device row's expiry timestamp to a public control state."""
    exp = device.control_grant_expires_at
    if exp is None:
        return "view_only"
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if exp <= _now():
        return "view_only"  # Expired grants read as view-only again.
    return "granted"


def _device_out(device: RemoteDevice) -> DeviceOut:
    return DeviceOut(
        id=device.id,
        display_name=device.display_name,
        device_type=device.device_type,  # type: ignore[arg-type]
        rustdesk_id=device.rustdesk_id,
        paired_at=device.paired_at,
        last_seen_at=device.last_seen_at,
        control_state=_control_state(device),
        control_grant_expires_at=device.control_grant_expires_at,
    )


def _redact_payload(event_type: str, payload: dict) -> dict:
    """Return a payload safe to persist.

    ``type_text`` and ``key_press`` payloads are redacted so raw keystrokes
    never land in the audit log.
    """
    if event_type == "type_text":
        text = str(payload.get("text", ""))
        return {
            "text_length": len(text),
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        }
    if event_type == "key_press":
        key = str(payload.get("key", ""))
        return {
            "key_sha256": hashlib.sha256(key.encode("utf-8")).hexdigest(),
            "modifiers": list(payload.get("modifiers", []) or []),
        }
    return dict(payload)


def _get_rustdesk_client(request: Request) -> RustDeskClient:
    client = getattr(request.app.state, "rustdesk_client", None)
    if client is None:
        client = RustDeskClient()
        request.app.state.rustdesk_client = client
    return client


async def _load_owned_device(
    db: AsyncSession, device_id: uuid.UUID, principal: Principal
) -> RemoteDevice:
    """Fetch a device that belongs to ``principal`` or raise 404.

    Returning 404 on cross-owner access — not 403 — hides existence.
    """
    stmt = select(RemoteDevice).where(
        RemoteDevice.id == device_id,
        RemoteDevice.owner_user_id == principal.user_id,
    )
    device = (await db.execute(stmt)).scalar_one_or_none()
    if device is None:
        raise HTTPException(status_code=404, detail="device not found")
    return device


# --------------------------------------------------------------------------- #
# REST endpoints
# --------------------------------------------------------------------------- #


@router.get("/devices", response_model=list[DeviceOut])
async def list_devices(
    principal: Principal = Depends(current_principal),
    db: AsyncSession = Depends(get_db),
) -> list[DeviceOut]:
    """List paired devices owned by the caller, with current control state."""
    result = await db.execute(
        select(RemoteDevice)
        .where(RemoteDevice.owner_user_id == principal.user_id)
        .order_by(RemoteDevice.paired_at.desc())
    )
    return [_device_out(d) for d in result.scalars().all()]


@router.post("/devices", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
async def register_device(
    body: DeviceRegisterRequest,
    principal: Principal = Depends(current_user),
    _csrf: None = Depends(require_csrf_double_submit),
    db: AsyncSession = Depends(get_db),
) -> DeviceOut:
    """Pair a new device. Only session-cookie users may pair."""
    device = RemoteDevice(
        display_name=body.display_name,
        device_type=body.device_type,
        rustdesk_id=body.rustdesk_id,
        auth_token=body.auth_token,
        control_grant_expires_at=None,  # explicit: paired == view-only
        owner_user_id=principal.user_id,
    )
    db.add(device)
    await db.commit()
    await db.refresh(device)
    return _device_out(device)


@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unpair_device(
    device_id: uuid.UUID,
    principal: Principal = Depends(current_user),
    _csrf: None = Depends(require_csrf_double_submit),
    db: AsyncSession = Depends(get_db),
) -> None:
    device = await _load_owned_device(db, device_id, principal)
    await db.delete(device)
    await db.commit()


@router.post(
    "/devices/{device_id}/grant-control",
    response_model=GrantControlResponse,
)
async def grant_control(
    device_id: uuid.UUID,
    body: GrantControlRequest,
    request: Request,
    x_consent_origin: Optional[str] = Header(default=None, alias="X-Consent-Origin"),
    origin_header: Optional[str] = Header(default=None, alias="Origin"),
    referer_header: Optional[str] = Header(default=None, alias="Referer"),
    csrf_header: Optional[str] = Header(default=None, alias=CSRF_HEADER_NAME),
    csrf_cookie: Optional[str] = Cookie(default=None, alias=CSRF_COOKIE_NAME),
    principal: Principal = Depends(current_user),
    _csrf: None = Depends(require_csrf_double_submit),
    db: AsyncSession = Depends(get_db),
) -> GrantControlResponse:
    """Mint a control-grant window.

    Layered defenses (each is INDEPENDENTLY sufficient to block the BYPASS #3
    same-origin XSS mint-a-grant vector):

    1. Session cookie (``current_user`` dep) — no XSS-injected fetch on an
       unauthenticated page mints anything.
    2. CSRF middleware — ``X-CSRF-Token`` must equal ``palpod_csrf`` cookie.
    3. Origin/Referer check (below) — a same-origin script whose Origin
       header is somehow scrubbed cannot get past this.
    4. Explicit-consent gate — the original ``X-Consent-Origin: user-tap``
       header is still required.
    5. Cool-down + rolling daily cap on grant events (BYPASS #6).
    """
    # Origin/Referer must match the allowlist. This is redundant with CORS but
    # covers the case where CORS is misconfigured or where a same-origin XSS
    # slips past CSRF.
    if not origin_or_referer_allowed(origin_header, referer_header):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "grant-control requires Origin or Referer header from an "
                "allowed origin"
            ),
        )

    # Explicit-consent gate (kept from the original design).
    if x_consent_origin != "user-tap":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "control grant requires an explicit user tap in pal-web; "
                "open the pal-web app and confirm the grant there. "
                "(Missing or invalid X-Consent-Origin header.)"
            ),
        )

    # Validate CSRF header is well-formed even though the middleware already
    # matched it against the cookie — the router still records the token hash
    # into the audit trail and wants a clean value.
    if not csrf_header or not csrf_token_is_valid_shape(csrf_header):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token missing or malformed",
        )
    _ = csrf_cookie  # middleware already compared this to csrf_header

    device = await _load_owned_device(db, device_id, principal)

    now = _now()

    # Cool-down: refuse if we minted a grant for this device < 30 s ago.
    latest_stmt = (
        select(RemoteGrantEvent)
        .where(RemoteGrantEvent.device_id == device_id)
        .order_by(RemoteGrantEvent.granted_at.desc())
        .limit(1)
    )
    latest = (await db.execute(latest_stmt)).scalar_one_or_none()
    if latest is not None:
        latest_at = latest.granted_at
        if latest_at.tzinfo is None:
            latest_at = latest_at.replace(tzinfo=timezone.utc)
        if (now - latest_at).total_seconds() < GRANT_COOLDOWN_SECONDS:
            wait = GRANT_COOLDOWN_SECONDS - int((now - latest_at).total_seconds())
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    f"grant cool-down active; wait {wait}s between grants for "
                    "this device"
                ),
            )

    # Rolling 24 h budget: sum of minutes across grants in the window.
    window_start = now - GRANT_ROLLING_WINDOW
    total_stmt = select(func.coalesce(func.sum(RemoteGrantEvent.minutes), 0)).where(
        RemoteGrantEvent.device_id == device_id,
        RemoteGrantEvent.granted_at >= window_start,
    )
    total_minutes = (await db.execute(total_stmt)).scalar_one() or 0
    if total_minutes + body.minutes > GRANT_DAILY_BUDGET_MINUTES:
        # Compute the earliest time enough budget would free up.
        rows_stmt = (
            select(RemoteGrantEvent.granted_at, RemoteGrantEvent.minutes)
            .where(
                RemoteGrantEvent.device_id == device_id,
                RemoteGrantEvent.granted_at >= window_start,
            )
            .order_by(RemoteGrantEvent.granted_at.asc())
        )
        rows = list((await db.execute(rows_stmt)).all())
        need_to_free = (total_minutes + body.minutes) - GRANT_DAILY_BUDGET_MINUTES
        freed = 0
        retry_after = now
        for granted_at, minutes in rows:
            if granted_at.tzinfo is None:
                granted_at = granted_at.replace(tzinfo=timezone.utc)
            freed += minutes
            retry_after = granted_at + GRANT_ROLLING_WINDOW
            if freed >= need_to_free:
                break
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                f"daily control budget exceeded; try again after "
                f"{retry_after.strftime('%H:%M')} UTC"
            ),
        )

    expires_at = now + timedelta(minutes=body.minutes)
    device.control_grant_expires_at = expires_at

    # Audit row — written in the same transaction as the device update so a
    # crash between the two is impossible.
    event = RemoteGrantEvent(
        device_id=device.id,
        granted_by_user_id=principal.user_id,
        granted_at=now,
        minutes=body.minutes,
        csrf_token_hash=hash_csrf_token(csrf_header),
        origin=(origin_header or referer_header or "unknown")[:255],
    )
    db.add(event)

    await db.commit()
    await db.refresh(device)

    return GrantControlResponse(
        device_id=device.id,
        control_state=_control_state(device),
        control_grant_expires_at=expires_at,
    )


@router.post(
    "/devices/{device_id}/revoke-control",
    response_model=RevokeControlResponse,
)
async def revoke_control(
    device_id: uuid.UUID,
    principal: Principal = Depends(current_user),
    _csrf: None = Depends(require_csrf_double_submit),
    db: AsyncSession = Depends(get_db),
) -> RevokeControlResponse:
    """End an active control grant immediately."""
    device = await _load_owned_device(db, device_id, principal)

    now = _now()
    device.control_grant_expires_at = now

    # Stamp the most recent still-open grant event as ended-early.
    open_stmt = (
        select(RemoteGrantEvent)
        .where(
            RemoteGrantEvent.device_id == device_id,
            RemoteGrantEvent.revoked_early_at.is_(None),
        )
        .order_by(RemoteGrantEvent.granted_at.desc())
        .limit(1)
    )
    open_event = (await db.execute(open_stmt)).scalar_one_or_none()
    if open_event is not None:
        open_event.revoked_early_at = now

    await db.commit()
    await db.refresh(device)

    return RevokeControlResponse(
        device_id=device.id,
        control_state=_control_state(device),
        revoked_at=now,
    )


@router.get(
    "/devices/{device_id}/grant-events",
    response_model=list[GrantEventOut],
)
async def list_grant_events(
    device_id: uuid.UUID,
    principal: Principal = Depends(current_principal),
    db: AsyncSession = Depends(get_db),
) -> list[GrantEventOut]:
    """Recent grant events for the UI audit-trail widget (last 10)."""
    # Ownership check first — reject with 404 on cross-owner peek.
    await _load_owned_device(db, device_id, principal)

    stmt = (
        select(RemoteGrantEvent)
        .where(RemoteGrantEvent.device_id == device_id)
        .order_by(RemoteGrantEvent.granted_at.desc())
        .limit(10)
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [GrantEventOut.model_validate(r) for r in rows]


@router.get(
    "/sessions/{session_id}/anomalies",
    response_model=SessionAnomaliesOut,
)
async def list_session_anomalies(
    session_id: uuid.UUID,
    principal: Principal = Depends(current_principal),
    db: AsyncSession = Depends(get_db),
) -> SessionAnomaliesOut:
    """Return both real anomaly rows and the per-bucket drop-summary rows.

    A security-conscious owner glancing at this endpoint should be able to
    tell "the 10 rows you see for 12:34:56 also had N others the limiter
    suppressed" — otherwise the audit trail hides floods behind its own
    ceiling.
    """
    session = await db.get(RemoteSession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")

    # Ownership scope: the session's device must belong to the caller. Same
    # 404-on-cross-owner rule as elsewhere in this router.
    device = await db.get(RemoteDevice, session.device_id)
    if device is None or device.owner_user_id != principal.user_id:
        raise HTTPException(status_code=404, detail="session not found")

    anomalies = (
        await db.execute(
            select(RemoteWSAnomaly)
            .where(RemoteWSAnomaly.session_id == session_id)
            .order_by(RemoteWSAnomaly.timestamp.asc())
        )
    ).scalars().all()

    summary_rows = (
        await db.execute(
            select(RemoteWSAnomalySummary)
            .where(RemoteWSAnomalySummary.session_id == session_id)
            .order_by(RemoteWSAnomalySummary.bucket_start.asc())
        )
    ).scalars().all()

    return SessionAnomaliesOut(
        anomalies=[WSAnomalyOut.model_validate(a) for a in anomalies],
        summary=[WSAnomalySummaryOut.model_validate(s) for s in summary_rows],
    )


@router.post("/sessions", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
async def open_session(
    body: SessionCreateRequest,
    principal: Principal = Depends(current_principal),
    _csrf: None = Depends(require_csrf_double_submit),
    db: AsyncSession = Depends(get_db),
) -> SessionOut:
    """Open a session. ``initiated_by`` is derived from the principal.

    BYPASS #9 fix: the client cannot influence ``initiated_by``. It gets
    ``"web"`` when the caller is a browser user session and ``"ai-agent"``
    when the caller is the voice orchestrator's bearer token.
    """
    device = await _load_owned_device(db, body.device_id, principal)

    initiated_by = "web" if principal.kind == "user" else "ai-agent"

    session = RemoteSession(
        device_id=device.id,
        initiated_by=initiated_by,
        transcript=body.transcript,
        was_authorized=False,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return SessionOut.model_validate(session)


# --------------------------------------------------------------------------- #
# WebSocket
# --------------------------------------------------------------------------- #


FRAME_INTERVAL_SECONDS = 1.0 / 15.0  # ~15 fps target

# BYPASS-fix rate limit for anomaly logging (per session, per second).
_ANOMALY_RATE_LIMIT = 10


async def _stream_frames(
    websocket: WebSocket,
    rustdesk_id: str,
    stop_event: asyncio.Event,
    rustdesk: RustDeskClient,
) -> None:
    """Push frame envelopes to the client at ~15 fps until stop_event is set."""
    view_ctx = {"grant_active": False, "grant_expires_at": None, "initiator": "user"}
    try:
        while not stop_event.is_set():
            try:
                frame = await rustdesk.get_screen_frame(
                    rustdesk_id, authorization_context=view_ctx
                )
                await websocket.send_json(
                    {
                        "type": "frame",
                        "rustdesk_id": rustdesk_id,
                        "captured_at": frame.captured_at.isoformat(),
                        "png_size": len(frame.png_bytes),
                    }
                )
            except Exception:  # noqa: BLE001
                pass
            await asyncio.sleep(FRAME_INTERVAL_SECONDS)
    except asyncio.CancelledError:
        return


async def _grant_watcher(
    websocket: WebSocket,
    device_id: uuid.UUID,
    initial_expiry: Optional[datetime],
    stop_event: asyncio.Event,
) -> None:
    already_notified = False
    try:
        while not stop_event.is_set():
            async with SessionLocal() as db:
                device = await db.get(RemoteDevice, device_id)
                if device is None:
                    return
                exp = device.control_grant_expires_at

            if exp is not None:
                if exp.tzinfo is None:
                    exp = exp.replace(tzinfo=timezone.utc)
                if exp <= _now() and not already_notified:
                    await websocket.send_json(
                        {
                            "type": "grant_expired",
                            "device_id": str(device_id),
                            "expired_at": exp.isoformat(),
                        }
                    )
                    already_notified = True
                elif exp > _now():
                    already_notified = False

            _ = initial_expiry
            await asyncio.sleep(1.0)
    except asyncio.CancelledError:
        return


def _authenticate_ws(websocket: WebSocket) -> Optional[Principal]:
    """Extract the principal from the WS handshake headers/cookies.

    Cookies are read straight from :attr:`WebSocket.cookies` (parsed by
    Starlette on ``accept()``'s handshake). The agent token can be passed
    either as a header (``X-Palpod-Agent-Token``) or a query string
    (``?agent_token=...``) because some WebSocket clients can't set custom
    headers.
    """
    # 1. Session cookie wins.
    cookie = websocket.cookies.get(SESSION_COOKIE_NAME)
    if cookie:
        uid = verify_session(cookie)
        if uid is not None:
            return Principal(kind="user", user_id=uid)

    # 2. Agent token — header preferred, query fallback.
    import hmac as _hmac

    token = (
        websocket.headers.get(AGENT_TOKEN_HEADER)
        or websocket.query_params.get("agent_token")
    )
    if token and _hmac.compare_digest(token, _get_agent_token()):
        from ..auth import POD_OWNER_USER_ID

        return Principal(kind="ai-agent", user_id=POD_OWNER_USER_ID)

    return None


class _AnomalyRateLimiter:
    """At-most-10-per-second-per-session limiter for anomaly writes.

    :meth:`decide` returns a tuple ``(allowed, bucket_start)`` — ``allowed``
    tells the caller whether to write a real anomaly row; ``bucket_start``
    is the whole-second UTC timestamp of the bucket, used by the caller to
    upsert a summary row on drop so the suppression itself is auditable.
    """

    def __init__(self, limit: int = _ANOMALY_RATE_LIMIT) -> None:
        self._limit = limit
        self._current_second = -1
        self._count = 0

    def decide(self) -> tuple[bool, datetime]:
        now_sec = int(time.time())
        if now_sec != self._current_second:
            self._current_second = now_sec
            self._count = 0
        bucket_start = datetime.fromtimestamp(now_sec, tz=timezone.utc)
        if self._count >= self._limit:
            return False, bucket_start
        self._count += 1
        return True, bucket_start

    def allow(self) -> bool:
        """Back-compat shim for callers that don't need the bucket."""
        allowed, _ = self.decide()
        return allowed


async def _record_anomaly_drop(
    session_id: uuid.UUID, bucket_start: datetime
) -> None:
    """Increment (or create) the dropped-count for this session's bucket.

    Uses ``ON CONFLICT`` upsert semantics so concurrent drops in the same
    bucket coalesce into a single row rather than racing. Runs on its own
    :class:`AsyncSession` so the caller's txn boundary is untouched.
    """
    from sqlalchemy.dialects.sqlite import insert as sqlite_insert
    from sqlalchemy.dialects.postgresql import insert as pg_insert

    async with SessionLocal() as db:
        dialect_name = db.bind.dialect.name if db.bind else ""
        if dialect_name == "postgresql":
            stmt = pg_insert(RemoteWSAnomalySummary).values(
                id=uuid.uuid4(),
                session_id=session_id,
                bucket_start=bucket_start,
                dropped_count=1,
            )
            stmt = stmt.on_conflict_do_update(
                constraint="uq_remote_ws_anomaly_summary_session_bucket",
                set_={"dropped_count": RemoteWSAnomalySummary.dropped_count + 1},
            )
        else:
            # SQLite (tests) supports ON CONFLICT (col_list) DO UPDATE.
            stmt = sqlite_insert(RemoteWSAnomalySummary).values(
                id=uuid.uuid4(),
                session_id=session_id,
                bucket_start=bucket_start,
                dropped_count=1,
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=["session_id", "bucket_start"],
                set_={"dropped_count": RemoteWSAnomalySummary.dropped_count + 1},
            )
        await db.execute(stmt)
        await db.commit()


async def _write_input_event(
    *,
    session_id: uuid.UUID,
    event_type: str,
    payload: dict,
    initiator: str,
    authorized: bool,
) -> None:
    """Persist one row into ``remote_input_events`` via a bare INSERT.

    Bypasses the ORM identity-map / autoflush plumbing so the row lands
    deterministically even under aggressive WS teardown.
    """
    stmt = insert(RemoteInputEvent).values(
        id=uuid.uuid4(),
        session_id=session_id,
        event_type=event_type,
        payload_json=_redact_payload(event_type, payload),
        initiator=initiator,
        authorized=authorized,
        grant_active_at_time=authorized,
        timestamp=_now(),
    )
    async with SessionLocal() as db:
        await db.execute(stmt)
        await db.commit()


async def _write_anomaly(
    db: AsyncSession,
    session_id: uuid.UUID,
    reason: str,
    raw: object,
    initiator: str,
) -> None:
    """Persist a single WS anomaly row.

    Uses a raw insert so the write path doesn't depend on the AsyncSession's
    identity-map / autoflush plumbing — pure execute + commit lets us
    guarantee the row lands even when the session is torn down promptly.
    Caller commits the transaction.
    """
    try:
        raw_str = json.dumps(raw, default=str)
    except (TypeError, ValueError):
        raw_str = str(raw)
    if len(raw_str) > 512:
        raw_str = raw_str[:512]

    stmt = insert(RemoteWSAnomaly).values(
        id=uuid.uuid4(),
        session_id=session_id,
        kind="invalid",
        reason=reason[:255],
        raw_envelope=raw_str,
        initiator=initiator,
        timestamp=_now(),
    )
    await db.execute(stmt)


@ws_router.websocket("/{session_id}")
async def remote_ws(
    websocket: WebSocket,
    session_id: uuid.UUID,
    agent_token_q: Optional[str] = Query(default=None, alias="agent_token"),
) -> None:
    """Bidirectional WebSocket for a single remote session.

    BYPASS #9 fix: the caller's principal is fixed at ``accept()`` time from
    the session cookie or agent token in the handshake headers. The client
    cannot subsequently change ``initiator`` — the field is even removed
    from :class:`InputEventEnvelope`, so a JSON body carrying it fails
    validation.
    """
    _ = agent_token_q  # documented in signature; actual extraction in helper

    principal = _authenticate_ws(websocket)
    if principal is None:
        # Accept-then-close so the client gets a 4401 code with a body.
        await websocket.accept()
        await websocket.send_json(
            {"type": "error", "error": "unauthenticated", "code": 401}
        )
        await websocket.close(code=4401)
        return

    await websocket.accept()

    async with SessionLocal() as db:
        session = await db.get(RemoteSession, session_id)
        if session is None:
            await websocket.send_json(
                {"type": "error", "error": "session not found", "code": 404}
            )
            await websocket.close(code=4404)
            return
        device = await db.get(RemoteDevice, session.device_id)
        if device is None:
            await websocket.send_json(
                {"type": "error", "error": "device not found", "code": 404}
            )
            await websocket.close(code=4404)
            return
        # Owner-scope check: refuse to hand a WS to someone who doesn't own
        # the underlying device.
        if device.owner_user_id != principal.user_id:
            await websocket.send_json(
                {"type": "error", "error": "session not found", "code": 404}
            )
            await websocket.close(code=4404)
            return

        rustdesk_id = device.rustdesk_id
        device_id = device.id
        initial_expiry = device.control_grant_expires_at

    stop_event = asyncio.Event()
    rustdesk = getattr(websocket.app.state, "rustdesk_client", None) or RustDeskClient()
    websocket.app.state.rustdesk_client = rustdesk

    frame_task = asyncio.create_task(
        _stream_frames(websocket, rustdesk_id, stop_event, rustdesk)
    )
    watcher_task = asyncio.create_task(
        _grant_watcher(websocket, device_id, initial_expiry, stop_event)
    )

    # Server-derived initiator, pinned for the life of the WS.
    initiator: str = principal.kind  # 'user' | 'ai-agent'
    anomaly_limiter = _AnomalyRateLimiter()

    try:
        while True:
            raw = await websocket.receive_json()

            # Unknown-shape envelope → anomaly row + drop.
            envelope_type = raw.get("type") if isinstance(raw, dict) else None
            if envelope_type != "input":
                allowed, bucket = anomaly_limiter.decide()
                if allowed:
                    async with SessionLocal() as db:
                        await _write_anomaly(
                            db,
                            session_id,
                            f"unknown envelope type: {envelope_type!r}",
                            raw,
                            initiator,
                        )
                        await db.commit()
                else:
                    await _record_anomaly_drop(session_id, bucket)
                continue

            # Malformed input envelope → anomaly row + WS error + drop.
            try:
                envelope = InputEventEnvelope(**raw)
            except ValidationError as ve:
                allowed, bucket = anomaly_limiter.decide()
                if allowed:
                    async with SessionLocal() as db:
                        await _write_anomaly(
                            db,
                            session_id,
                            f"invalid input event: {ve.errors()[0]['msg']}",
                            raw,
                            initiator,
                        )
                        await db.commit()
                else:
                    await _record_anomaly_drop(session_id, bucket)
                await websocket.send_json(
                    {"type": "error", "error": f"invalid input event: {ve.errors()[0]['msg']}", "code": 400}
                )
                continue

            # 1. Read the current grant state on a snapshot session.
            async with SessionLocal() as db:
                device = await db.get(RemoteDevice, device_id)
            if device is None:
                await websocket.send_json(
                    {"type": "error", "error": "device disappeared", "code": 404}
                )
                break
            exp = device.control_grant_expires_at
            if exp is not None and exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
            grant_active = exp is not None and exp > _now()

            # 2. If no grant, log rejected and drop.
            if not grant_active:
                await _write_input_event(
                    session_id=session_id,
                    event_type=envelope.event_type,
                    payload=envelope.payload,
                    initiator=initiator,
                    authorized=False,
                )
                await websocket.send_json(
                    {
                        "type": "error",
                        "error": "not authorized — no active control grant",
                        "code": 403,
                    }
                )
                continue

            # 3. Dispatch through the RustDesk client (which re-checks).
            context = {
                "grant_active": True,
                "grant_expires_at": exp,
                "initiator": initiator,
            }
            try:
                await rustdesk.send_input_event(
                    rustdesk_id,
                    envelope.event_type,
                    envelope.payload,
                    authorization_context=context,
                )
            except InsufficientAuthorization:
                await _write_input_event(
                    session_id=session_id,
                    event_type=envelope.event_type,
                    payload=envelope.payload,
                    initiator=initiator,
                    authorized=False,
                )
                await websocket.send_json(
                    {
                        "type": "error",
                        "error": "not authorized — client refused dispatch",
                        "code": 403,
                    }
                )
                continue

            # 4. Dispatch succeeded — log authorized + flip session flag.
            await _write_input_event(
                session_id=session_id,
                event_type=envelope.event_type,
                payload=envelope.payload,
                initiator=initiator,
                authorized=True,
            )
            async with SessionLocal() as db:
                sess = await db.get(RemoteSession, session_id)
                if sess is not None and not sess.was_authorized:
                    sess.was_authorized = True
                    await db.commit()

    except WebSocketDisconnect:
        pass
    finally:
        stop_event.set()
        frame_task.cancel()
        watcher_task.cancel()
        for t in (frame_task, watcher_task):
            try:
                await t
            except (asyncio.CancelledError, Exception):  # noqa: BLE001
                pass

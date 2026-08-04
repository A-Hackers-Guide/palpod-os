"""WebSocket bridge to pal-voice.

Runs in a background thread with its own asyncio loop. The renderer polls the
bridge each frame via `bridge.drain()` — cheap, thread-safe (queue.Queue).

Wire protocol (JSON messages received from pal-voice):
    {"type": "face_state", "state": "listening"}
    {"type": "tts_start"}
    {"type": "tts_end"}
    {"type": "tts_frame", "audio_level": 0.7}       # 0.0 -> 1.0

Reconnect strategy: exponential backoff, capped at reconnect_max_seconds.
Runs forever until stop() is called. Never crashes on message parse errors.
"""

from __future__ import annotations

import asyncio
import json
import logging
import queue
import threading
from dataclasses import dataclass
from typing import Any, Optional

try:
    import websockets
    from websockets.exceptions import ConnectionClosed
    _WEBSOCKETS_OK = True
except Exception:  # pragma: no cover — allow import without dep for tests
    websockets = None  # type: ignore
    ConnectionClosed = Exception  # type: ignore
    _WEBSOCKETS_OK = False


log = logging.getLogger(__name__)


@dataclass
class BridgeEvent:
    kind: str          # "face_state" | "tts_start" | "tts_end" | "tts_frame" | "connected" | "disconnected"
    payload: dict


class Bridge:
    def __init__(
        self,
        url: str,
        reconnect_initial_seconds: float = 0.5,
        reconnect_max_seconds: float = 30.0,
    ):
        self.url = url
        self.reconnect_initial = reconnect_initial_seconds
        self.reconnect_max = reconnect_max_seconds
        self._q: "queue.Queue[BridgeEvent]" = queue.Queue()
        self._stop_evt = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._connected = False

    # -------- lifecycle -----------------------------------------------------
    def start(self) -> None:
        if not _WEBSOCKETS_OK:
            log.warning("websockets not installed — bridge disabled")
            return
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._run, name="pal-bridge", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_evt.set()
        if self._loop is not None:
            try:
                self._loop.call_soon_threadsafe(lambda: None)
            except Exception:
                pass
        if self._thread is not None:
            self._thread.join(timeout=1.5)

    # -------- consumer API --------------------------------------------------
    def drain(self) -> list[BridgeEvent]:
        """Non-blocking: return all queued events since last drain."""
        out: list[BridgeEvent] = []
        while True:
            try:
                out.append(self._q.get_nowait())
            except queue.Empty:
                break
        return out

    @property
    def connected(self) -> bool:
        return self._connected

    # -------- internals -----------------------------------------------------
    def _run(self) -> None:
        try:
            asyncio.run(self._main())
        except Exception as e:  # pragma: no cover
            log.exception("bridge thread crashed: %s", e)

    async def _main(self) -> None:
        self._loop = asyncio.get_running_loop()
        backoff = self.reconnect_initial
        while not self._stop_evt.is_set():
            try:
                log.info("bridge: connecting to %s", self.url)
                async with websockets.connect(
                    self.url, open_timeout=5, ping_interval=20, ping_timeout=20
                ) as ws:
                    self._connected = True
                    self._q.put(BridgeEvent("connected", {"url": self.url}))
                    backoff = self.reconnect_initial
                    await self._reader_loop(ws)
            except (OSError, ConnectionClosed, asyncio.TimeoutError) as e:
                log.info("bridge: connection failed / closed: %s", e)
            except Exception as e:  # pragma: no cover
                log.exception("bridge: unexpected error: %s", e)
            finally:
                if self._connected:
                    self._connected = False
                    self._q.put(BridgeEvent("disconnected", {}))
            if self._stop_evt.is_set():
                break
            await asyncio.sleep(backoff)
            backoff = min(self.reconnect_max, backoff * 2.0)

    async def _reader_loop(self, ws) -> None:
        async for raw in ws:
            if self._stop_evt.is_set():
                return
            try:
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8", errors="replace")
                msg = json.loads(raw)
            except Exception as e:
                log.warning("bridge: bad message %r: %s", raw, e)
                continue
            self._dispatch(msg)

    def _dispatch(self, msg: Any) -> None:
        if not isinstance(msg, dict):
            return
        kind = msg.get("type")
        if kind == "face_state":
            state = str(msg.get("state", "")).strip()
            if state:
                self._q.put(BridgeEvent("face_state", {"state": state}))
        elif kind == "tts_start":
            self._q.put(BridgeEvent("tts_start", {}))
        elif kind == "tts_end":
            self._q.put(BridgeEvent("tts_end", {}))
        elif kind == "tts_frame":
            level = float(msg.get("audio_level", 0.0))
            self._q.put(BridgeEvent("tts_frame", {"audio_level": level}))
        else:
            log.debug("bridge: unknown type %r", kind)

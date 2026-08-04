# pal-voice

The Pod's voice orchestrator: turn ASR text into pal-web intent handler
invocations, speak the response back.

## Required environment variables

Since the security-review fix for BYPASS #9 (client-supplied initiator), the
voice orchestrator authenticates with pal-web using a dedicated bearer token
that is distinct from the browser-user session cookie. That token labels
every event the orchestrator dispatches as `initiator="ai-agent"` in the
pal-web audit log — the label is server-derived from the token and cannot be
forged by whoever fires up the WebSocket.

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `PALPOD_AGENT_TOKEN` | **yes** | `palpod-dev-agent-token` | Bearer token pal-voice sends as `X-Palpod-Agent-Token` on REST calls and as `?agent_token=` query parameter on WebSocket connects. Must match the value pal-web reads from **its** `PALPOD_AGENT_TOKEN` env var. Rotate on any orchestrator compromise. |
| `PALWEB_BASE_URL` | yes | `http://pod.palpod.local` | Base URL of the pal-web control plane the orchestrator drives. |
| `PALWEB_WS_URL` | no | derived from `PALWEB_BASE_URL` | Override if pal-web's WebSocket endpoint lives at a non-default host. |

### Deployment notes

* Store the agent token in your secrets manager, **not** in the source repo.
  Distribute it identically to pal-web (`.env`) and pal-voice (`.env`) at
  deploy time.
* The agent token is NOT a substitute for the user's session cookie in any
  code path that mints new authority. Grant-control endpoints refuse an
  agent-token caller with HTTP 403 (`current_user` dependency rejects
  non-user principals). This is by design: an AI agent must never mint its
  own control window.
* On rotation, restart pal-web and pal-voice as a pair. There is no dual-key
  overlap window.

## Local dev

```bash
cp .env.example .env
# edit .env to set PALPOD_AGENT_TOKEN, PALWEB_BASE_URL
uv sync
pytest
```

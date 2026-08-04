# PALPod OS — Observability stack

A **Prometheus + Grafana** stack that surfaces the health, security, and
performance of every PALPod service. The stack is **opt-in**: it does not
start with a plain `docker compose up -d`; you have to enable it with a
profile flag.

Enabling the stack

```bash
docker compose --profile observability up -d
```

That brings up:

| Service              | Image                                             | Purpose                                                                                    |
| -------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `prometheus`         | `prom/prometheus:latest`                          | Scrapes every exporter and every `/metrics` endpoint on the palpod bridge network.         |
| `grafana`            | `grafana/grafana:latest`                          | Renders dashboards. Datasource + dashboards are auto-provisioned from this directory.      |
| `node_exporter`      | `prom/node-exporter:latest`                       | Host CPU / memory / disk / network / ZFS metrics.                                          |
| `postgres_exporter`  | `prometheuscommunity/postgres-exporter:latest`    | Postgres 16 metrics — connections, cache hit ratio, replication lag, deadlocks.            |
| `cadvisor`           | `gcr.io/cadvisor/cadvisor:latest`                 | Per-container CPU / memory / network / block-io.                                           |
| `blackbox_exporter`  | `prom/blackbox-exporter:latest`                   | HTTP probes for Plex, Jellyfin, Audiobookshelf, xTeVe, Sunshine, Traefik.                  |

To stop just the observability stack (leave the rest of PALPod running):

```bash
docker compose --profile observability down
```

## Ports

| Service              | Host port | Notes                                                                                    |
| -------------------- | --------- | ---------------------------------------------------------------------------------------- |
| `prometheus`         | `9090`    | Query UI + admin. Bind to `127.0.0.1:9090` in production.                                 |
| `grafana`            | `3000`    | Dashboard UI. Traefik-fronted at `grafana.${PALPOD_DOMAIN}` if you enable the labels.    |
| `node_exporter`      | `9100`    | LAN-only.                                                                                |
| `postgres_exporter`  | `9187`    | LAN-only.                                                                                |
| `cadvisor`           | `8080`    | LAN-only.                                                                                |
| `blackbox_exporter`  | `9115`    | LAN-only.                                                                                |

## First Grafana login

The Grafana container boots with the default credentials:

- **Username:** `admin`
- **Password:** `admin`

Grafana forces you through a password-change flow on that first login. Set
something strong and lock the account down — the dashboards themselves are
read-only (`allowUiUpdates: false` in `dashboards.yml`), but anyone with the
admin account can still add datasources or install plugins.

Once you are in, the dashboards live under the **PALPod** folder in the
left-hand nav:

- `PALPod OS — Overview`
- `PALPod OS — AI performance`
- `PALPod OS — Media servers`
- `PALPod OS — Remote-desktop security`
- `PALPod OS — Postgres health`
- `PALPod OS — Storage health`

Every dashboard is provisioned from JSON files on disk (see
`grafana/provisioning/dashboards/`). To edit a dashboard, edit the JSON and
save — Grafana rescans the directory every 30 seconds. Do not use the
"Save" button in the UI; it will not work, because provisioned dashboards
are read-only.

## Where things live

```
observability/
├── README.md                        ← this file
├── prometheus/
│   └── prometheus.yml               ← scrape config (jobs + probes)
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml       ← auto-configures the Prometheus DS
│       └── dashboards/
│           ├── dashboards.yml       ← provider config for auto-loading
│           ├── palpod-overview.json
│           ├── palpod-ai.json
│           ├── palpod-media.json
│           ├── palpod-remote-desktop.json
│           ├── palpod-postgres.json
│           └── palpod-storage.json
├── pal-web/
│   └── metrics.py                   ← FastAPI middleware + /metrics endpoint
└── pal-voice/
    └── metrics.py                   ← HTTP handler on port 7778 for pal-voice
```

## Wiring the first-party services

Prometheus scrapes the following endpoints on the `palpod` docker network:

- `http://pal-web:8000/metrics`
- `http://pal-voice:7778/metrics`
- `http://rustdesk-hbbs:21118/metrics` (RustDesk's built-in status port)

For pal-web, import the middleware in the FastAPI app factory:

```python
from observability.pal_web.metrics import install_metrics
app = FastAPI()
install_metrics(app)
```

For pal-voice, start the metrics server from `palvoice/main.py`:

```python
from observability.pal_voice.metrics import start_metrics_server
start_metrics_server(port=7778)
```

Both modules assume `prometheus-client` is on the pip dependency list —
add it to `pal-web/pyproject.toml` and `pal-voice/pyproject.toml` before
enabling the observability profile.

## About the remote-desktop dashboard

`palpod-remote-desktop.json` is the dashboard we care most about. It reads:

- `palweb_remote_devices_registered` — from the `remote_devices` table.
- `palweb_active_grants` + `palweb_grant_seconds_remaining` — updated by the
  grant-lifecycle code path.
- `palweb_remote_grant_events_total{kind="granted|denied|expired|revoked"}`
  — incremented every time a row lands in `remote_grant_events`.
- `palweb_input_events_total{authorized,initiator,reason}` — every input
  event on the WS bridge, whether we passed it through or dropped it.
- `palweb_ws_anomalies_total{kind}` + `palweb_ws_anomalies_suppressed_total{kind}`
  — the first tracks individual anomalies, the second tracks the *aggregate
  suppressed count* recorded in `remote_ws_anomaly_summary`.
- `palweb_consent_cooldown_blocks_total` — every time we deny a consent
  prompt because the user is in the cooldown window.
- `palweb_grant_seconds_used_total` — increment as seconds elapse; drives
  the rolling 24h budget gauge.

## Safety & privacy

- The stack ships with **no external egress**. Nothing calls home; every
  metric stays on the pod.
- Grafana is admin-only. Add a reverse-proxy auth layer (Authelia,
  Traefik forward-auth, oauth2-proxy, ...) before exposing it beyond
  the LAN.
- Prometheus stores 15 days of data by default. Bump
  `--storage.tsdb.retention.time` in `docker-compose.yml` if you want more.
- The observability profile is **opt-in** because it adds ~500 MB of
  memory pressure on the Jetson. If you are running the pod at the edge of
  the AGX Orin's memory budget, leave it off.

## Note on ZFS storage panels

The `palpod-storage` dashboard queries ZFS-specific series (`node_zfs_zpool_allocated_bytes`,
`node_zfs_zpool_dataset_snapshot_count`, `node_zfs_zpool_scan_status`, etc.) that stock
`prom/node-exporter` does **not** emit — the built-in ZFS collector only exposes per-pool
I/O counters at `/proc/spl/kstat/zfs/{pool}/io`.

**Expected behavior:**

- On MVP Jetson AGX Orin (ext4/f2fs, no ZFS): the ZFS panels will read "No data". This
  is graceful and expected — no action required.
- On production TrueNAS SCALE (ZFS-native): install `pdf-technologies/zfs_exporter` or
  add `--collector.textfile.directory=/var/lib/node_exporter/textfile_collector` to
  node_exporter's command args and drop the pool-status text emitters into that dir.

The panels are drafted in advance so that when the production hardware ships, the
observability story is complete.

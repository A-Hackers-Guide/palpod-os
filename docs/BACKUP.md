# BACKUP — HearthOS

Two things must survive a total loss of the primary Jetson:

1. **Postgres** — because it owns the household identity graph: users,
   memory facts, extender registry, upload audit trail. Losing it means the
   Pod forgets the family.
2. **The media library** — hundreds of TB in the production cluster; users'
   personal rips and photos are not replaceable.

Everything else (Plex/Jellyfin config, Traefik certs, xTeVe channel map) is
regeneratable in an afternoon if lost.

---

## 1. Postgres

### Nightly logical dump

`scripts/backup-postgres.sh` (add this to cron or a systemd timer):

```bash
#!/usr/bin/env bash
set -euo pipefail
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
DEST=/var/lib/palpod/backups/postgres
mkdir -p "$DEST"
docker exec -t postgres pg_dumpall -U "${POSTGRES_USER}" \
  | gzip > "$DEST/palpod-$STAMP.sql.gz"
# Keep last 30 days.
find "$DEST" -name 'palpod-*.sql.gz' -mtime +30 -delete
```

Restore into a fresh Pod:

```bash
gunzip -c palpod-YYYYMMDDTHHMMSSZ.sql.gz \
  | docker exec -i postgres psql -U "${POSTGRES_USER}" -d postgres
```

### WAL streaming (production)

On TrueNAS SCALE, replace the compose Postgres with the Zalando Postgres
operator and enable continuous WAL archiving to a second dataset. Recovery
becomes a point-in-time restore.

---

## 2. Media library — ZFS snapshots

Assumes the library lives on a ZFS pool named `tank`. If you're on plain
Ubuntu + ext4, use `rsync --link-dest` snapshots instead; see §3.

```bash
# One-time: create datasets so snapshots are per-library, not pool-wide.
sudo zfs create tank/media
sudo zfs create tank/media/movies
sudo zfs create tank/media/tv
sudo zfs create tank/media/music
sudo zfs create tank/media/audiobooks
sudo zfs create tank/media/podcasts
```

Enable `zfs-auto-snapshot` for a rotating snapshot schedule:

```bash
sudo apt-get install -y zfsutils-linux zfs-auto-snapshot
sudo zfs set com.sun:auto-snapshot=true tank/media
```

The default policy is:

| Interval  | Retained |
|-----------|----------|
| frequent  | 4        |
| hourly    | 24       |
| daily     | 31       |
| weekly    | 8        |
| monthly   | 12       |

Off-site: `zfs send | ssh` to a second Pod or a friend's NAS. Never send
snapshots to a cloud provider — that violates the "nothing leaves the house"
guarantee unless the customer explicitly opts in.

### Restore a single file

```bash
cd /mnt/media/movies/.zfs/snapshot/zfs-auto-snap_daily-2026-08-02-0000
cp -a "Movie I Deleted (2024).mkv" /mnt/media/movies/
```

### Restore an entire library

```bash
sudo zfs rollback tank/media/movies@zfs-auto-snap_daily-2026-08-02-0000
```

---

## 3. Media library — non-ZFS fallback (rsync)

If TrueNAS/ZFS isn't in the picture, run a nightly rotating rsync:

```bash
# /etc/cron.daily/palpod-rsync
SRC=/mnt/media
DST=/mnt/backup/media
LAST=$(ls -1t "$DST" | head -1)
STAMP=$(date -u +%Y%m%d)
rsync -aH --delete \
  --link-dest="$DST/$LAST" \
  "$SRC/" "$DST/$STAMP/"
```

`--link-dest` gives you effectively-copy-on-write snapshots as hard-linked
trees. Storage cost ≈ delta size per night.

---

## 4. Configs & TLS

`/var/lib/palpod/traefik/certs/` and the docker named volumes for each
service should be included in the ZFS snapshot policy above. If you're on
ext4, tar them into the postgres backup destination:

```bash
sudo tar czf /var/lib/palpod/backups/configs-$(date -u +%Y%m%d).tar.gz \
  /var/lib/palpod/traefik \
  $(docker volume inspect plex_config      -f '{{ .Mountpoint }}') \
  $(docker volume inspect jellyfin_config  -f '{{ .Mountpoint }}') \
  $(docker volume inspect audiobookshelf_config -f '{{ .Mountpoint }}') \
  $(docker volume inspect xteve_config     -f '{{ .Mountpoint }}') \
  $(docker volume inspect sunshine_config  -f '{{ .Mountpoint }}')
```

---

## 5. Verify

A backup you never restore is a backup you don't have. Once a quarter:

1. Spin up a scratch Pod (a spare Jetson or a laptop with docker).
2. Copy the latest `palpod-*.sql.gz` and a subset of the media tree.
3. Restore Postgres, boot the compose stack, confirm every service comes up
   healthy.
4. Log the drill in the ops journal.

The pal-web control app has a **Backup drill** widget that walks you through
this and records the outcome.

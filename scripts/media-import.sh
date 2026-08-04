#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# scripts/media-import.sh — bulk import a directory of mixed media into the
# right library for each service.
#
# Usage:
#   ./scripts/media-import.sh <source-dir> [--dry-run] [--move|--copy|--link]
#
# What it does:
#   1. Walks <source-dir> recursively.
#   2. Classifies each file by extension + name pattern:
#        movies         → *.mkv/*.mp4/*.avi + no S01E01 pattern
#        tv-episodes    → *.mkv/*.mp4/*.avi + S\d+E\d+ pattern
#        music          → *.flac/*.mp3/*.m4a/*.opus/*.ogg
#        audiobooks     → *.m4b or under a folder named audiobook*/
#        podcasts       → *.mp3 under a folder named podcast*/
#   3. Copies/moves/hardlinks the file into the matching MEDIA_* directory.
#   4. Records the operation in the upload_events table via psql on the
#      postgres container so the pal-web audit page reflects it.
#   5. Kicks Plex, Jellyfin, Audiobookshelf to rescan (best-effort).
#
# Default action is --link (fast + reversible). Use --move to reclaim the
# source directory afterwards; --copy for maximum safety.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <source-dir> [--dry-run] [--move|--copy|--link]" >&2
  exit 1
fi

SRC="$1"; shift
[[ -d "$SRC" ]] || { echo "[!] Not a directory: $SRC" >&2; exit 1; }

DRY=0
MODE=link
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --move)    MODE=move ;;
    --copy)    MODE=copy ;;
    --link)    MODE=link ;;
    *) echo "[!] Unknown flag: $1" >&2; exit 1 ;;
  esac
  shift
done

set -a; source .env; set +a

# ─── Classification ────────────────────────────────────────────────────────
classify() {
  local path="$1"
  local base
  base=$(basename "$path")
  local lower_dir
  lower_dir=$(dirname "$path" | tr '[:upper:]' '[:lower:]')

  # Directory hints win.
  if [[ "$lower_dir" =~ /audiobook ]]; then echo "audiobook:$MEDIA_AUDIOBOOKS"; return; fi
  if [[ "$lower_dir" =~ /podcast ]];   then echo "podcast:$MEDIA_PODCASTS";     return; fi

  case "$base" in
    *.flac|*.mp3|*.m4a|*.opus|*.ogg|*.wav)
      # music unless podcast/audiobook by dir
      echo "music-track:$MEDIA_MUSIC"; return ;;
    *.m4b)
      echo "audiobook:$MEDIA_AUDIOBOOKS"; return ;;
    *.mkv|*.mp4|*.avi|*.mov|*.m4v|*.webm)
      if [[ "$base" =~ [Ss][0-9]+[Ee][0-9]+ ]]; then
        echo "tv-episode:$MEDIA_TV"; return
      else
        echo "movie:$MEDIA_MOVIES"; return
      fi ;;
    *) echo "unknown:"; return ;;
  esac
}

# ─── Do it ─────────────────────────────────────────────────────────────────
count_ok=0; count_skip=0
while IFS= read -r -d '' file; do
  cls="$(classify "$file")"
  kind="${cls%%:*}"
  dest_dir="${cls#*:}"

  if [[ "$kind" == "unknown" || -z "$dest_dir" ]]; then
    echo "[skip] $file  ($kind)"
    count_skip=$((count_skip+1))
    continue
  fi

  dest="$dest_dir/$(basename "$file")"
  if [[ -e "$dest" ]]; then
    echo "[skip] $file  (destination exists: $dest)"
    count_skip=$((count_skip+1))
    continue
  fi

  echo "[$kind] $file  →  $dest"

  if [[ $DRY -eq 0 ]]; then
    mkdir -p "$dest_dir"
    case "$MODE" in
      link) ln "$file" "$dest" 2>/dev/null || cp -a "$file" "$dest" ;;
      copy) cp -a "$file" "$dest" ;;
      move) mv "$file" "$dest" ;;
    esac

    # Record the event.
    size=$(stat -c%s "$dest")
    sha=$(sha256sum "$dest" | awk '{print $1}')
    target_service=$(case "$kind" in
      movie|tv-episode) echo "plex" ;;
      music-track)      echo "jellyfin" ;;
      audiobook|podcast) echo "audiobookshelf" ;;
      *) echo "" ;;
    esac)
    target_library=$(case "$kind" in
      movie) echo "Movies" ;;
      tv-episode) echo "TV" ;;
      music-track) echo "Music" ;;
      audiobook) echo "Audiobooks" ;;
      podcast) echo "Podcasts" ;;
    esac)
    docker exec -i postgres psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" >/dev/null <<SQL
INSERT INTO upload_events (filename, byte_size, classification, target_service, target_library, checksum_sha256)
VALUES ('$(printf '%s' "$dest" | sed "s/'/''/g")', $size, '${kind//-track/}'::upload_classification, '$target_service', '$target_library', '$sha');
SQL
  fi
  count_ok=$((count_ok+1))
done < <(find "$SRC" -type f -print0)

echo
echo "[done] imported: $count_ok, skipped: $count_skip"

# ─── Poke rescans ──────────────────────────────────────────────────────────
if [[ $DRY -eq 0 ]]; then
  echo "[+] Kicking library rescans (best-effort)…"
  docker exec plex           bash -c 'wget -q --spider "http://localhost:32400/library/sections/all/refresh"' 2>/dev/null || true
  docker exec jellyfin       bash -c 'curl -sS -X POST http://localhost:8096/Library/Refresh' 2>/dev/null || true
  docker exec audiobookshelf bash -c 'curl -sS -X POST http://localhost/api/libraries/scan' 2>/dev/null || true
fi

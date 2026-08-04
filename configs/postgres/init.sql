-- ─────────────────────────────────────────────────────────────────────────────
-- PALPod OS — initial database schema.
--
-- Loaded once by the postgres container on first boot from
-- /docker-entrypoint-initdb.d/00-init.sql.
--
-- Owned tables live in the public schema. The `pal-web` app expects the
-- database, user, and password from the top-level .env; they are created
-- automatically by the postgres image via POSTGRES_DB / POSTGRES_USER /
-- POSTGRES_PASSWORD, so this file only defines schema, not roles.
--
-- If you change a table shape, add a migration under pal-web/prisma/migrations
-- rather than editing this file — this file is only ever re-run on a fresh
-- Postgres volume.
-- ─────────────────────────────────────────────────────────────────────────────

BEGIN;

-- Extensions -----------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "pgcrypto";     -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "vector";       -- pgvector, best-effort. Falls
                                               -- back to BYTEA if unavailable.

-- Users ----------------------------------------------------------------------
-- A user is a household member. Each has a biometric footprint (face + voice
-- embedding) and a set of personality slider values that shape their PAL's
-- behaviour. `memory_bytes_used` is a running tally so the UI can render a
-- storage-per-person budget without a heavy join over memory_facts.
CREATE TABLE users (
    id                          UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    name                        TEXT          NOT NULL,
    face_embedding              BYTEA,        -- 512-d float32 packed
    voice_embedding             BYTEA,        -- 192-d float32 packed
    personality_slider_values   JSONB         NOT NULL DEFAULT '{}'::jsonb,
    memory_bytes_used           BIGINT        NOT NULL DEFAULT 0,
    created_at                  TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);
CREATE INDEX users_name_idx ON users (LOWER(name));

-- Profiles -------------------------------------------------------------------
-- A profile is a scoped identity a user can present to a service — think
-- "Kids mode", "Guest", "Grandma-safe TV". A user has many profiles; the
-- active profile is chosen when the user is recognised by pal-voice/pal-face.
CREATE TABLE profiles (
    id                UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID          NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    label             TEXT          NOT NULL,
    is_default        BOOLEAN       NOT NULL DEFAULT FALSE,
    -- Free-form key/value bag: plex_home_user_id, jellyfin_user_id,
    -- content_rating_ceiling, etc.
    settings          JSONB         NOT NULL DEFAULT '{}'::jsonb,
    created_at        TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);
CREATE UNIQUE INDEX profiles_one_default_per_user
    ON profiles (user_id) WHERE is_default = TRUE;

-- Extender registry ----------------------------------------------------------
-- Every peripheral node that has paired with the primary Pod. `role` is
-- assigned by pal-web after successful pairing and controls what services
-- the node runs (game-node, media-cache, mic-array, etc.).
CREATE TYPE extender_role AS ENUM (
    'unassigned',
    'media-cache',
    'game-node',
    'mic-array',
    'display',
    'storage'
);

CREATE TABLE extender_registry (
    id           UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    mac          MACADDR        NOT NULL UNIQUE,
    ip           INET,
    hostname     TEXT,
    role         extender_role  NOT NULL DEFAULT 'unassigned',
    paired_at    TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    last_seen    TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    -- The JWT the primary issued at pair time. Rotated on re-pair.
    jwt_hash     TEXT           NOT NULL,
    metadata     JSONB          NOT NULL DEFAULT '{}'::jsonb
);
CREATE INDEX extender_last_seen_idx ON extender_registry (last_seen);

-- Upload events --------------------------------------------------------------
-- Auditable record of every file the household drops into the Pod's incoming
-- watch dir. `classification` is what scripts/media-import.sh (or pal-web's
-- upload UI) decided the file was; `target_service` and `target_library`
-- point at where it landed.
CREATE TYPE upload_classification AS ENUM (
    'movie',
    'tv-episode',
    'music-album',
    'music-track',
    'audiobook',
    'podcast',
    'photo',
    'document',
    'unknown'
);

CREATE TABLE upload_events (
    id               UUID                     PRIMARY KEY DEFAULT gen_random_uuid(),
    filename         TEXT                     NOT NULL,
    byte_size        BIGINT                   NOT NULL,
    classification   upload_classification    NOT NULL DEFAULT 'unknown',
    target_service   TEXT,                    -- plex | jellyfin | audiobookshelf | null
    target_library   TEXT,                    -- e.g. "Movies", "TV", "Music"
    uploaded_at      TIMESTAMPTZ              NOT NULL DEFAULT NOW(),
    uploaded_by      UUID                     REFERENCES users(id) ON DELETE SET NULL,
    checksum_sha256  TEXT
);
CREATE INDEX upload_events_uploaded_at_idx ON upload_events (uploaded_at DESC);
CREATE INDEX upload_events_user_idx        ON upload_events (uploaded_by);

-- Memory facts ---------------------------------------------------------------
-- The Pod's long-term "what I know about this person" store. Each row is one
-- atomic fact ("mark's favourite drink is Old Fashioneds"). `importance` is
-- a heuristic score (0..1) pal-voice writes. `confirmed` flips true after the
-- user has been asked "should I remember that?" and said yes.
CREATE TABLE memory_facts (
    id                 UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID          NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    fact_text          TEXT          NOT NULL,
    importance         REAL          NOT NULL DEFAULT 0.5 CHECK (importance BETWEEN 0 AND 1),
    confirmed          BOOLEAN       NOT NULL DEFAULT FALSE,
    source             TEXT,                              -- e.g. "voice-2026-08-03T14:11Z"
    created_at         TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    last_referenced_at TIMESTAMPTZ
);
CREATE INDEX memory_facts_user_importance_idx
    ON memory_facts (user_id, importance DESC);
CREATE INDEX memory_facts_last_referenced_idx
    ON memory_facts (last_referenced_at DESC NULLS LAST);

-- Housekeeping trigger: bump users.updated_at whenever the row changes.
CREATE OR REPLACE FUNCTION touch_updated_at() RETURNS trigger AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_touch_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION touch_updated_at();

-- Remote devices ------------------------------------------------------------
-- Registry of every machine the Pod can remote into via RustDesk (or, opt-in,
-- AnyDesk). Rows are inserted by scripts/pair-remote-device.sh and by the
-- pal-web pairing flow. `ai_control_allowed` is the defense-in-depth flag
-- that gates the click/type/scroll endpoints — even an authenticated Pod
-- session gets 403 if it's false.
CREATE TABLE IF NOT EXISTS remote_devices (
    id                    UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name          TEXT          NOT NULL,
    device_type           TEXT          NOT NULL,           -- 'mac', 'windows', 'linux', 'ios', 'android'
    rustdesk_id           TEXT          UNIQUE,             -- 9-digit RustDesk ID
    auth_token            TEXT          NOT NULL,           -- shared secret for pair verification
    ai_control_allowed    BOOLEAN       DEFAULT FALSE,      -- did user explicitly grant AI control?
    paired_at             TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    last_seen_at          TIMESTAMPTZ,
    owner_user_id         UUID          REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS remote_devices_owner ON remote_devices(owner_user_id);

-- Remote sessions -----------------------------------------------------------
-- Auditable log of every remote-desktop session the Pod opens. `initiated_by`
-- distinguishes voice ("Hey Pod, show me…"), the pal-web UI, and headless
-- ai-agent calls. For voice sessions, `transcript` captures what was said
-- so the household can see later exactly what triggered the session.
CREATE TABLE IF NOT EXISTS remote_sessions (
    id             UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id      UUID          NOT NULL REFERENCES remote_devices(id) ON DELETE CASCADE,
    started_at     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    ended_at       TIMESTAMPTZ,
    initiated_by   TEXT          NOT NULL,       -- 'voice' | 'web' | 'ai-agent'
    transcript     TEXT                          -- if voice-initiated, what was said
);
CREATE INDEX IF NOT EXISTS remote_sessions_device_idx
    ON remote_sessions (device_id, started_at DESC);

COMMIT;

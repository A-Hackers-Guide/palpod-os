# MEDIA-IMPORT-RUNBOOK.md

**Hearth Household Media Library Import Runbook**
**Owner:** Head of Customer Success
**Audience:** Concierge L1/L2/L3, install-day field engineers, legacy-media partner liaisons, dealer channel, Head of Privacy (biometric-consent sign-off), General Counsel (DMCA §1201 posture sign-off)
**Version:** 2.0 (supersedes v1.0 which was returned NEEDS-FIX for DMCA §1201, v1.0/v2.0 feature-gate, BIPA per-member scope, and COPPA under-13 gaps)
**Cross-references:** `PRIVACY-COMPLIANCE-MANUAL.md` §3 (biometric consent framework), `PRODUCT-ROADMAP-12-24MO.md` §2 (v1.0 feature set) + §5 (v2.0 feature set), `ONBOARDING-PLAYBOOK.md` Phase 4 (Day 90 NPS), `FINANCIAL-MODEL-SENSITIVITY.md` §2.6 (concierge cost as % of gross profit), `THREAT-MODEL.md` §1.2 (seven-class egress ACL), `WARRANTY-TRAINING.md` (concierge escalation)

---

## 1. Overview and cost frame

Hearth's household media library import is the single most operationally intensive service delivered at install day. A Q3 Palm Beach or Newport Beach persona routinely arrives with 800 GB of iCloud + Google Photos, 500 GB of ripped and purchased music, 2 TB of home video across three decades of formats, a legacy Audible library approaching 1,500 titles, a Kindle library of 3,000+ books, a physical Blu-ray + UHD Blu-ray collection of 200-300 discs, a Steam library, and — increasingly — a Kaleidescape server preserved as a coexistence tier. The concierge team turns this heterogeneous, DRM-encumbered, format-fragmented, EXIF-degraded pile into a clean Plex + Jellyfin + Audiobookshelf + Immich library on the Hearth's 38.4 TB Kioxia CD8-R storage.

**Concierge-service cost frame.** The concierge budget for a $95,000 v1.0 Hearth household is **14% of Y1 gross profit per household**, per `FINANCIAL-MODEL-SENSITIVITY.md` §2.6. At the base-case $46,000 gross profit per unit that works out to **a $6,400 concierge budget per install**. Of that budget, roughly 40–60 hours of skilled labor at a loaded ~$100/hr cost ($4,000–$6,000) is the media-import share, leaving the remainder for install-day physical setup, network conditioning, extender pairing, first-week support, and the Phase 4 Day 90 NPS visit. Top-of-Medium or Large households (see §9) consume the full envelope and trigger the escalation in §11. **The v1.0 draft quoted a "35% concierge-service loading in Y1" figure that did not reconcile to the financial model and is deleted here in full.** The canonical number is 14% of GP or ~$6,400 per household.

**Two commitments.** First, "nothing leaves the household unless the customer specifically asks it to" — the seven-class egress ACL in `THREAT-MODEL.md` §1.2 governs the concierge laptop, rip station, and every ingest tool. Media import is not an exception. Second, the runbook must be reconcilable to the Series B SOC 2 Type II + ISO 27001 + Trail of Bits posture, which means concierge cannot execute DMCA §1201 circumvention as install-day SOP. §13 is the load-bearing statement of that posture; §4 is the operational reflection.

**What "100% content migrated" now means.** The v1.0 draft made an unqualified promise. v2.0 narrows it, for reasons in §4 and §13:

> Non-DRM content 100% migrated. DRM-encumbered content (Audible AAX/AAXC, Kindle purchased ebooks, DVD, Blu-ray, UHD Blu-ray) is subject to customer self-service via Hearth-recommended third-party tools executed on the customer's own device or via a licensed disc-transfer service partner where one exists; concierge provides advisory support and file ingest into the Hearth library but does not execute DRM removal on customer premises. Purchased-but-DRM-locked content (Kindle, Audible, purchased iTunes movies) is enumerated in the household's Content Inventory Report as "advisory-only" content, and the household admin acknowledges the resulting scope in writing at install day.

---

## 2. Household intake and initial audit

Before any drive spins or any account is linked, the concierge L1 conducts the **Content Inventory Interview** in the 7–14 days between deposit and install day. This is a 45-minute video call with the household admin (typically the account holder) plus any household member who intends to migrate their own personal library. The interview generates the Content Inventory Report (CIR), which is the single artifact the entire runbook works against.

**CIR line items — the ten source categories.** The concierge L1 walks through the list in order because earlier categories are lower-DRM-friction and higher-volume:

1. **iCloud Photos + Videos.** Volume estimate in GB, years of history, whether "Optimize Storage" is enabled, whether Live Photos + HEIC are in scope. Migration path: Download Originals in Photos on a customer-owned Mac + `icloudpd` on the rip station as fallback.

2. **Google Photos (and Google Drive media).** Volume estimate, number of accounts, Google One state. Migration path: Google Takeout with the JSON EXIF sidecar → `GooglePhotosTakeoutHelper` to re-embed the sidecar timestamps and GPS into the JPEG/HEIC EXIF because Takeout strips them.

3. **Amazon Photos.** Volume estimate, Prime member status, whether linked to the household's Alexa devices. **Migration path — primary:** **Amazon Photos Desktop client "Sync All"** on a customer-owned Mac or Windows machine. This is Amazon's supported download surface; it pulls full-resolution originals with EXIF intact and is the only method that reliably works in 2026-2028. **Fallback:** Amazon Photos web download batch-by-batch (slow, ~500 photos per batch cap, but reliable when the Desktop client hits a sync-state bug). The v1.0 draft listed rclone with the Amazon Cloud Drive backend as primary — **that path is factually broken** because Amazon revoked the rclone Amazon Drive backend in 2017-2018 when it killed unlimited Cloud Drive. Do not attempt rclone against Amazon Photos in 2026 or later; the backend is deprecated and non-functional. Any old concierge SOP referencing rclone-Amazon-Drive is a documentation defect flagged to the Head of Customer Success for correction.

4. **iTunes / Apple Music local library + purchased content.** iTunes library XML enumerates local music, purchased-and-downloaded tracks (DRM-free since 2009), and Apple Music matched tracks (on-demand streams, cannot be migrated — see item 8). Volume estimate, iTunes Match history, dedup state.

5. **Kaleidescape system (coexistence, not migration).** No bulk export exists — the Kaleidescape format is a purpose-built encrypted DRM container and export is prohibited by EULA + AACS §1201. Migration path: **Hearth ingests the Kaleidescape metadata (title list, watch history if the customer manually exports it) as a "library index" so Plex + Jellyfin present a unified browse view; playback for Kaleidescape titles routes to the Kaleidescape system** via Plex external-player or the Hearth's HDMI-in bridge.

6. **Audible library (AAX/AAXC).** Titles + hours; whether pre-2018 (AAX) or newer (AAXC). **Migration path — advisory only per §4.6 and §13.** Concierge does not execute DRM removal on customer premises. Customer may elect to run third-party tools (OpenAudible, `aax-transcoder`) on their own device; concierge ingests any DRM-free files the customer produces into Audiobookshelf. If the customer declines, the Audible library is documented in the CIR as "advisory-only" and stays accessible only through Audible apps on the customer's existing devices.

7. **Kindle library.** Titles + mix of Kindle-purchased vs DRM-free sideloaded (Calibre EPUBs, PDFs). **Migration path — advisory only per §4.7 and §13.** Same posture as Audible. Customer-sideloaded DRM-free EPUBs and PDFs are ingested into Calibre-Web without issue; Kindle-purchased content is documented as advisory-only.

8. **Streaming service metadata (Spotify, Apple Music, Netflix, Disney+, Max, Prime Video).** No content migration possible or offered — streaming is on-demand access, not owned. Concierge configures Plex/Jellyfin external-player rules so streaming apps are launchable at the couch alongside owned content. CIR captures subscriptions for context.

9. **Physical disc collection (DVD, Blu-ray, UHD Blu-ray).** Counted separately. Most operationally expensive by hours, most legally sensitive by DMCA §1201. **Migration path — advisory only for the DRM-circumvention step per §4.9 and §13.** Three options:
   - **Option A (preferred where available):** Route to a US-based licensed disc-transfer service partner. The vetted-partner landscape is thin — most consumer services operate under a personal-use §1201 interpretation the Librarian of Congress has not granted, or operate outside the US where §1201 doesn't apply but chain-of-custody creates its own problems. Head of Customer Success maintains the live list; if no fully-licensed US service exists at install day, Option A is unavailable.
   - **Option B:** Customer runs MakeMKV (DVD/Blu-ray) or UHD-friendly LG WH16NS58 with friendly-firmware (UHD Blu-ray) on their own device, at their own election. Concierge specifies target format (MKV pass-through, per-title, subtitles + audio tracks preserved) but does not execute. Concierge ingests the resulting MKV files.
   - **Option C:** No digitization. Physical discs stay in the household, playable from a customer-owned player wired to the Hearth via HDMI-in.

   The v1.0 draft made concierge execution of DVD (CSS), Blu-ray (AACS), and UHD Blu-ray (AACS 2.0) rips default install-day activity. That posture is deleted in v2.0 for the reasons in §13.

10. **Home video (VHS, 8mm, Hi8, MiniDV, camcorder tapes, film reels).** Count tapes/reels, aggregate hours, any prior digitization. **Not DRM-encumbered** — customer-created content — the one physical-media category where the concierge does full end-to-end. Migration path: partner with a licensed legacy-media digitization service (Legacybox, iMemories, or regional equivalent); collect at install day; ship in bonded chain-of-custody; ingest returned files into a `HomeVideo/` structure organized by decade and originating device. Partner turnaround 4–8 weeks — the primary driver of the timeline-past-Day-90 issue in §10.

---

## 3. Rip station and concierge kit

The concierge team ships to install day with a portable rip station and a laptop-driven concierge kit. Both are Hearth-owned property, not customer-owned; the customer's own devices are used for tasks (like Amazon Photos Desktop client sync and third-party DRM-tool execution per §4) that must run on customer-owned equipment.

**Rip station capex (per concierge kit, ~$4,000–$6,000 all-in).**
- 1× Pelican 1620 hard case (protective transport)
- 1× Mac mini M4 (base config, 512 GB) — the local ingest headend, running the rip-management scripts and hosting a temporary NAS surface during install
- 2× LG WH16NS58 UHD-friendly Blu-ray drives, flashed with the appropriate older firmware. These drives are used for **verifying and ingesting customer-produced MKV files where the customer has already run the rip themselves** (Option B) and for reading customer-created DVD-Video content the customer produced from their own camcorders (home video, no DMCA issue). Concierge does not execute DRM-circumvention on customer premises using these drives.
- 1× Pioneer BDR-XD08 (external Blu-ray + DVD reader for audit reads only)
- 1× Samsung T9 4 TB portable SSD (staging)
- Concierge laptop: 16" MacBook Pro (M-series) with FileVault + institutional MDM, dedicated concierge login profile, and the tooling stack (rsync, exiftool, ffmpeg, HandBrake for legally-owned re-encode, Plex/Jellyfin/Immich admin, `icloudpd`, `GooglePhotosTakeoutHelper`, Amazon Photos Desktop client, and diagnostic tools for the seven-class egress ACL audit)
- Cabling, adapters, USB-C hubs

**Rip station throughput.** Concierge ingest of customer-produced MKV files moves at LAN wire speed (~500 MB/s over 5 GbE from laptop to Kioxia array, so a 35 GB Blu-ray title ingests in ~70 seconds). Home video DVD-Video verification at 45 min per disc × 2 concurrent drives puts a 100-disc verification pass at ~30 concierge-attended hours. For customer-elected Option B collections, concierge rip-station hours drop to the ingest window only (4–8 hours for a 200-title collection at LAN wire speed); the customer's own device runs the multi-day rip in parallel, off the concierge clock.

**Concierge time budget per household — reconciled to the financial model.** At the $6,400 concierge budget per household (§1) and a loaded concierge cost of ~$100/hr, the media-import share is 40–60 hours (§1). That envelope decomposes roughly as:
- 4 hours — CIR intake interview + pre-install prep
- 6 hours — cloud-photo ingest (iCloud + Google + Amazon)
- 4 hours — iTunes / music library ingest
- 4 hours — audiobook + ebook ingest (DRM-free content only)
- 8–20 hours — physical disc verification + ingest (varies by Option A / B / C election; A minimizes concierge hours, B is intermediate, C is minimal)
- 4 hours — home video partner handoff + return ingest
- 4 hours — metadata enrichment + household walkthrough
- 6 hours — verification, dedup pass, backup validation, Day 30 follow-up call

Households at the top of the Medium band or into Large blow past the 40-hour lower bound and land at or above the 60-hour upper bound. Escalation to the Head of Customer Success at hour 55 is the standard trigger — see §11.

---

## 4. Content-source paths — the ten sources in operational detail

This section is the concierge's step-by-step reference for each of the ten CIR categories from §2. It is written for a concierge L1 to follow on install day with L2 escalation available in the concierge Slack.

### 4.1 iCloud Photos + Videos

**Preferred path.** On the customer-owned Mac linked to the household iCloud account, in Photos → Settings → iCloud, ensure "Download Originals to this Mac" is selected. Large libraries take multiple hours to days. Once local, the concierge uses `osxphotos` to export to a `PhotosExport/` folder on the Samsung T9 with EXIF, Live Photos (`.mov` companions), edits, and album structure preserved. Ingest to Immich follows the standard import flow.

**Fallback.** If the customer's Mac cannot host the full library, the concierge uses `icloudpd` from the concierge laptop with credentials entered by the household admin at a temporary keyboard handoff (concierge never sees or types the customer's password). Slower and slightly less rich in Live Photo pairing, but reliable.

### 4.2 Google Photos (and Google Drive media)

Google Takeout is the only supported bulk export path. The concierge coaches the customer through initiating Takeout in the customer's own Google browser session, including any Google Drive folders identified as media-relevant. Google mails download links over 24–48 hours.

Once the `.tgz` files are on the customer-owned Mac (or on the concierge laptop via the customer's own browser session), the concierge runs `GooglePhotosTakeoutHelper` to solve the Takeout EXIF problem: Google strips original EXIF timestamps and GPS off the media and puts them in a separate JSON sidecar per file. Left alone, the household's Google Photos becomes a pile of 2020-01-01 mtimes with no GPS. `GooglePhotosTakeoutHelper` re-embeds sidecar data back into the media EXIF; corrected files ingest to Immich normally.

### 4.3 Amazon Photos

**Preferred — Amazon Photos Desktop client "Sync All".** On the customer-owned Mac or Windows machine, the customer installs the Desktop client (customer types their own Amazon credentials), and in Settings enables "Sync All" against a `~/AmazonPhotos/` folder. The client downloads full-resolution originals with EXIF intact. Concierge monitors progress and ingests via rsync-over-SSH at LAN wire speed.

**Fallback — web download.** If the Desktop client is malfunctioning (rare — usually strict application-installation policy), the concierge coaches the customer through Amazon Photos web download batch-by-batch (~500 photos per batch cap, slow but reliable). Batches land as `.zip` in Downloads; concierge unpacks and ingests.

**Explicitly rejected.** The rclone Amazon Cloud Drive backend is non-functional (revoked 2017-2018). Any concierge documentation referencing rclone-Amazon-Drive is a defect flagged to the Head of Customer Success. Do not attempt.

### 4.4 iTunes / Apple Music local library + purchased content

Copy the customer's iTunes library XML (or `Music.app` database) to the concierge laptop for parsing. Extract the list of local audio files (DRM-free iTunes Store tracks + ripped CD content), map their locations, and rsync into Audiobookshelf's `Music/` structure on the Hearth. Album art preserved; iTunes playlists exported as `.m3u` and re-imported into Plex + Jellyfin.

Purchased-but-DRM-encumbered iTunes content (pre-2009 FairPlay-locked movies/TV) is advisory-only per the same posture as Audible/Kindle. Apple Music streaming is on-demand and stays on the customer's existing devices.

### 4.5 Kaleidescape (coexistence, not migration)

The concierge configures the Hearth to present Kaleidescape content via metadata index only. The customer exports their Kaleidescape watch list and title list from the Kaleidescape web console using their own admin login on their own device. The concierge ingests the exported list into a `Kaleidescape/` folder in Plex with an external-player rule routing playback to the Kaleidescape system's HDMI output through the Hearth's HDMI-in bridge (or the customer's existing AV switch). No DRM-encumbered content is transferred, decoded, or re-encoded by concierge.

### 4.6 Audible library (AAX/AAXC) — advisory only

The concierge does not execute Audible DRM removal on customer premises. Per §13, this is a §1201 posture, not a technical limitation. The advisory conversation with the household admin:

- Confirm household admin owns the Audible library (Amazon-account-scoped; concierge confirms account access matches admin identity)
- Present a written summary of the third-party tool ecosystem (most commonly cited: OpenAudible, `aax-transcoder`)
- State plainly that Hearth does not endorse, recommend, execute, or provide technical support for the DRM-circumvention step
- State plainly that the customer may elect, on their own device, in their own account, at their own discretion, to run such tools; concierge will ingest any resulting DRM-free `.m4b`/`.mp3` files into Audiobookshelf
- Capture the household admin's election in writing (self-service pursued, or Audible stays advisory-only in the CIR)

### 4.7 Kindle library — advisory only

Same posture as Audible. Concierge does not execute Kindle DeDRM on customer premises. Advisory conversation mirrors §4.6, substituting Kindle-ecosystem tooling. DRM-free EPUBs, PDFs, and MOBI files the customer has already managed in Calibre are ingested into Calibre-Web without any DRM-adjacent step.

### 4.8 Streaming service metadata

No content migration. Concierge configures Plex/Jellyfin external-player rules so streaming apps are launchable at the couch alongside owned content. CIR captures active subscriptions.

### 4.9 Physical disc collection (DVD, Blu-ray, UHD Blu-ray) — advisory only for DRM step

Per §2 item 9 and §13, three options at CIR:
- **Option A:** Route to a licensed disc-transfer partner (Head of Customer Success maintains the live vetted-partner list). Partner-produced files ship back to the household; concierge ingests.
- **Option B:** Customer runs MakeMKV (DVD/Blu-ray) or UHD-Blu-ray-capable tooling on their own device at their own election. Concierge ingests the resulting MKV files.
- **Option C:** No digitization. Physical discs stay in the household, playable from a customer-owned player wired to the Hearth via HDMI-in.

The v1.0 draft made concierge execution of DVD/Blu-ray/UHD Blu-ray rips a default install-day activity. Deleted in v2.0 per §13. **UHD Blu-ray in particular:** AACS 2.0 keys are only extractable via hardware+firmware combinations that are themselves DMCA circumvention technology; Hearth does not offer UHD Blu-ray digitization as a concierge service under any Option A/B/C interpretation, and the customer's Option B for UHD is contingent on their own hardware possession and their own election.

### 4.10 Home video (VHS, 8mm, Hi8, MiniDV, camcorder tapes, film reels)

Not DRM-encumbered. The one physical-media category where concierge runs full end-to-end:

1. At install day, inventory home-video media by format (VHS/8mm/Hi8/MiniDV/film with format spec — 8mm, Super 8, 16mm) and running time.
2. Household admin signs a shipping-consent form authorizing shipment to a Hearth-partnered digitization service (Legacybox, iMemories, or regional equivalent per Head of Customer Success partner-quality signal).
3. Media packed in a Pelican-1620-equivalent bonded chain-of-custody case with per-item labels, insured to full replacement value.
4. Partner turnaround 4–8 weeks. Concierge ingests returned files into a `HomeVideo/` structure organized by decade + originating device, with title-card overlays per the customer's naming preference (year+event, year+family member, or tape-side identifier — captured at CIR).
5. Physical media returned in the same case.

Home video is the primary driver of the timeline-past-Day-90 issue in §10.

---

## 5. Ingest pipeline and metadata enrichment

Once the concierge has content flowing to the Hearth (whether from cloud sources, from customer-owned tools, or from partner-returned home video files), the metadata enrichment pipeline runs. This is the step where photos become browsable by date + location + source, music becomes browsable by artist + album + genre, movies get matched to TMDb metadata, TV shows get matched to TVDb metadata, and audiobooks get matched to Audiobookshelf's metadata store.

**Photo enrichment in v1.0 — by-date, by-location, by-source only.** Per `PRIVACY-COMPLIANCE-MANUAL.md` §3, face recognition is a v2.0 feature added per `PRODUCT-ROADMAP-12-24MO.md` §5 and is off by default; enabling it triggers a fresh consent flow per household member with a specific written-notice text captured in the household audit log. **v1.0 does not offer face detection, face recognition, face-tagging, or any biometric photo enrichment at install day**, because activating a v2.0-restricted feature at v1.0 install with the wrong consent scaffolding is a BIPA-grade violation. The v1.0 photo enrichment pipeline generates browse views by:

- **Date** — from EXIF `DateTimeOriginal`, corrected for Google Takeout stripping per §4.2
- **Location** — from EXIF `GPSLatitude` / `GPSLongitude`, reverse-geocoded on-device using an offline geocoding database bundled with the Hearth's Immich install
- **Source** — from a metadata tag the concierge writes at ingest indicating which of the ten CIR categories the content came from (iCloud, Google Photos, Amazon Photos, home video, etc.)

Album structure the customer maintained in their source system (iCloud shared albums, Google Photos albums, Amazon Photos albums) is preserved as folder + collection structure in Immich, so the customer's own organization schema follows them into the Hearth.

**Face tagging in v2.0 — opt-in per household member, fresh consent, historical photos only with consent.** The v2.0 refresh described in `PRODUCT-ROADMAP-12-24MO.md` §5 introduces face recognition as a feature. Per `PRIVACY-COMPLIANCE-MANUAL.md` §3, activation requires a fresh consent flow per household member with the specific written-notice text quoted in that section. In the v2.0 context, applying face tagging to historical photos (photos migrated to the Hearth at v1.0 install) is a distinct consent event beyond the general face-recognition enrollment: the household member's fresh consent must specifically authorize retroactive application of face tagging to already-ingested content. The consent flow surfaces this explicitly and the household member may elect (a) enroll face recognition for future photos only, (b) enroll and apply retroactively to historical content, or (c) decline face recognition entirely. The concierge does not make this decision on the customer's behalf.

**v1.0 vs v2.0 feature-gate reference table for concierge.** The concierge Slack has this table pinned; it is the single reference the L1 uses when a household asks "can Hearth do X?" during CIR.

| Feature | v1.0 (2027 Q2 pilot → Q4 GA) | v2.0 (2028 Q4) | Consent framework |
|---|---|---|---|
| Photo browse by date | Yes | Yes | Baseline install consent |
| Photo browse by location (from EXIF GPS) | Yes | Yes | Baseline install consent |
| Photo browse by source (iCloud, Google, etc.) | Yes | Yes | Baseline install consent |
| Album/collection preservation | Yes | Yes | Baseline install consent |
| Voice profile per household member | Yes | Yes | BIPA-grade voice consent per §3 of privacy manual |
| Per-member LLM personality | v1.1 (2027 Q3) | Yes | Voice consent (BIPA-grade) |
| Face detection | No | Opt-in per member | BIPA-grade face consent per §3 of privacy manual, distinct from voice consent |
| Face recognition | No | Opt-in per member | Same fresh face consent flow |
| Face tagging applied to historical photos | No | Opt-in, explicit retroactive election | Fresh face consent + explicit retroactive election |
| Under-13 face profile | No — v1.0 does not do face at all | Opt-in with FTC §312.5(b) verifiable parental consent (Stripe Identity + video call per privacy manual §3 Under-13 subsection) | Verifiable parental consent per privacy manual §3 Under-13 subsection |
| Under-13 voice profile | No enrollment without verifiable parental consent | Same posture | Verifiable parental consent per privacy manual §3 Under-13 subsection |
| Voice-tagged personal notes | Yes | Yes | Personal-scoped to the member; owner cannot override — see §12 |

The concierge script is: "The Hearth you're installing today (v1.0) organizes photos by date, by location, and by which service they came from — and preserves the albums you already have. Face recognition is a feature added in v2.0, which is a hardware refresh in Q4 2028; when you upgrade to v2.0, we walk each household member through a fresh consent flow specifically for face recognition, and each member can choose whether to enroll and whether to apply it to older photos we're bringing over today."

**Music enrichment.** MusicBrainz / Discogs metadata matching against the customer's ripped and purchased library. Album art normalized. Playlists ingested from iTunes XML per §4.4. No biometric processing.

**Movie + TV enrichment.** TMDb / TVDb metadata against customer-produced or customer-provided files. NFO sidecars generated for Plex + Jellyfin. No biometric processing.

**Audiobook enrichment.** Audiobookshelf's own metadata store against ISBN / cover-image / narrator-name match. No biometric processing.

---

## 6. Legacy media partner integration

Home video digitization (VHS, 8mm, Hi8, MiniDV, film reels — §4.10) is routed through a partner because the equipment (industrial-grade tape decks, film scanners with 4K sensors, calibrated color-grading suites) is capex Hearth does not carry per household. The partner relationship is a first-class dependency of this runbook.

**Partner selection criteria.** The Head of Customer Success maintains the current partner list on a quarterly review cycle. Selection criteria: US-based operations with SOC 2 Type II or equivalent security posture, insured chain-of-custody at full replacement value of the physical media, digital return delivered as ProRes 422 (for VHS/8mm/Hi8/MiniDV) or DPX / 4K TIFF sequences for film, physical media returned in the same or better packaging condition, and a written data-processing agreement conforming to the standards in `PRIVACY-COMPLIANCE-MANUAL.md` §6.

**Turnaround.** 4–8 weeks is the standard. Rush service is available from most partners at 2–3× the base rate; the concierge budgets for standard turnaround and elevates to rush only on documented customer emergency.

**Timeline collision with 90-day onboarding.** A household with 60 hours of home video shipping to the partner at install day (Day 0 of the household's 90-day onboarding journey) receives partner-produced files back at Day 30–60. Ingest, enrichment, and household walk-through consumes another 5–7 days. The household's home video content is on the Hearth by Day 40–70 in the standard case. Rush households (see §10.2) with elective 2-week partner turnaround land at Day 20–35. Extended households (§10.3) with 8-12 week partner turnaround may still be receiving files at Day 80–100 — past the standard Day 90 NPS capture window. See §10 for the reconciliation.

---

## 7. Verification, deduplication, backup validation

Before handoff, the concierge runs a three-pass verification against the ingested content:

**Pass 1 — file-count and volume reconciliation.** The concierge produces a Content Delivery Report (CDR) enumerating the file count and total volume per CIR category, and reconciles against the CIR volume estimates. Deltas >10% are investigated: sometimes the customer's original estimate was wrong (common for old cloud accounts they hadn't logged into in years), sometimes a source-side extract failed silently and needs re-run, sometimes a partner returned a different file count than the physical-media inventory suggested. The concierge resolves before handoff.

**Pass 2 — deduplication.** A household typically has 10-30% duplication across their sources (photos in both iCloud and Google Photos because the customer was migrating and never finished, music tracks in both iTunes and manually-ripped folders, etc.). The concierge runs `czkawka` or equivalent open-source dedup tooling against the ingested library, flags suspected duplicates, and — critically — does not delete anything without the household admin's explicit approval. The dedup pass is presented to the household admin as a Delta Report; the admin decides retention.

**Pass 3 — backup validation.** The Hearth's 38.4 TB Kioxia array is the primary; the household's backup posture (external LUKS-encrypted drive per `PRIVACY-COMPLIANCE-MANUAL.md` §5, or household-owned NAS) is the secondary. The concierge validates the backup chain by writing a canary file, taking the backup, restoring the canary, and confirming byte-for-byte match. The concierge does not consider media import complete until backup validation passes.

---

## 8. Handoff to household

Handoff is a scheduled 60-minute in-home session with the household admin plus interested household members. The concierge walks the household through:

- The Plex + Jellyfin + Audiobookshelf + Calibre-Web + Immich UI on the Hearth's touchscreen and on the family's paired iOS + Android devices
- The Content Delivery Report from §7 pass 1, category by category, with any advisory-only content documented in writing per §4.6 / §4.7 / §4.9
- The v1.0 vs v2.0 feature-gate table from §5, so the household understands what face-recognition features become available at the v2.0 hardware refresh
- The privacy toggles per `PRIVACY-COMPLIANCE-MANUAL.md` §11 including biometric consent per §3, sub-processor opt-outs, and marketing-email opt-out
- The seven-class egress ACL per `THREAT-MODEL.md` §1.2 — the concierge shows the household admin the Grafana observability dashboard at `https://pod.palpod.local/observability` (v1.1+) with the egress-class hit counter live, so the household admin can see the seven classes and the count of hits per class
- The Data Portal in the mobile app per `PRIVACY-COMPLIANCE-MANUAL.md` §10, so household members know how to exercise their Right of Access, Right of Correction, Right of Deletion
- The escalation contacts — concierge Slack, phone line, and the DPO's email for privacy questions

**The written Advisory-Only Acknowledgment.** At handoff, the household admin signs an Advisory-Only Acknowledgment enumerating any DRM-encumbered content the household elected not to migrate under §4.6 / §4.7 / §4.9. The acknowledgment names the specific content categories (e.g., "Kindle library estimated 3,000 titles remains in customer's Amazon account; not ingested to Hearth"), states that the household admin acknowledges this scope, and states that Hearth's "100% content migrated" commitment is scoped to non-DRM content per §1. The acknowledgment is filed in the household's onboarding record.

---

## 9. Content size estimates and bracket sizing

The Hearth's 38.4 TB usable Kioxia array plus household-owned backup gives a large ceiling. Sizing tolerance matters most in the Blu-ray and UHD Blu-ray categories, which the v1.0 draft of this runbook understated by roughly 2×. Corrected estimates below.

**Photos.** Small: 100-300 GB (typical iCloud-only household with 10 years of iPhone photos). Medium: 400-800 GB (multi-account household with iCloud + Google + Amazon). Large: 1-2 TB (professional photographer or long-history household with RAW files).

**Home video, digitized.** Small: 200-500 GB (30 hours of VHS at ProRes 422). Medium: 1-2 TB (60-120 hours across VHS + 8mm + Hi8). Large: 3-5 TB (200+ hours, mixed formats including MiniDV HD).

**Music, ripped + purchased (DRM-free).** Small: 100-200 GB. Medium: 300-500 GB. Large: 800 GB - 1.5 TB (audiophile with FLAC + high-res).

**Audiobooks (DRM-free, post-customer-conversion).** Small: 20-50 GB. Medium: 80-150 GB. Large: 250-500 GB (Audible-heavy household with 1,000+ titles converted).

**Ebooks (DRM-free).** Small: 1-5 GB. Medium: 10-30 GB (with PDFs). Large: 50-100 GB (with heavily-illustrated PDFs / graphic novels).

**DVDs (MKV pass-through at ~5-7 GB per disc).** Small: 100 titles ≈ 600 GB. Medium: 300 titles ≈ 1.8 TB. Large: 600 titles ≈ 3.6 TB.

**Blu-rays (MKV pass-through at 25-50 GB per disc, 35 GB average — the runbook's own §3 baseline).** Small: 100 titles × 35 GB = **3.5 TB baseline**. Medium: 200 titles × 35 GB = **7 TB baseline**. Large: 400 titles × 35 GB = **14 TB baseline**. **The v1.0 draft of this runbook quoted 1.5 TB for the Small bracket at 100 Blu-ray titles; this was arithmetically incorrect by roughly 2× and is corrected here.**

**UHD Blu-rays (MKV pass-through at 50-100 GB per disc, 70 GB average).** Small: 50 titles × 70 GB = **3.5 TB baseline**. Medium: 100 titles × 70 GB = **7 TB baseline**. Large: 200 titles × 70 GB = **14 TB baseline**. **The v1.0 draft of this runbook quoted 1.5 TB for the Small bracket at 50 UHD Blu-ray titles; same 2× understatement, corrected here.**

**Steam library (game files, customer-owned).** Small: 100 GB. Medium: 500 GB - 1 TB. Large: 2-4 TB.

**Aggregate bracket sizing after correction.**

| Bracket | Photos + Music + AB + Ebooks | Home video | DVDs | Blu-rays | UHD | Steam | Aggregate |
|---|---|---|---|---|---|---|---|
| **Small** | ~300-600 GB | ~200-500 GB | ~600 GB | ~3.5 TB | ~3.5 TB (if any) | ~100 GB | **~4.5-8 TB** |
| **Medium** | ~800 GB - 1.5 TB | ~1-2 TB | ~1.8 TB | ~7 TB | ~7 TB | ~500 GB - 1 TB | **~12-20 TB** |
| **Large** | ~2-3 TB | ~3-5 TB | ~3.6 TB | ~14 TB | ~14 TB | ~2-4 TB | **~30-45 TB** |

**A Q3 Palm Beach persona example.** 200 Blu-rays + 100 UHDs + 800 GB photos + 500 GB music + 2 TB home video + a moderate Steam library realistically sums to: 200 × 35 GB Blu-ray = 7 TB + 100 × 70 GB UHD = 7 TB + 0.8 TB photos + 0.5 TB music + 2 TB home video + 0.5 TB Steam = **17.8 TB**, at the top of the Medium band. Add a professional-audiophile FLAC library (1.5 TB) and a 200-hour home-video digitization (4 TB), and the household lands at **21-25 TB — inside the Medium band but with narrow headroom against the Hearth's 38.4 TB ceiling for future acquisition**.

The v1.0 draft implied this persona landed in the middle of the Medium band; corrected numbers show it lands at the top. The concierge sizes the household's backup posture accordingly.

---

## 10. Timeline reconciliation with 90-day onboarding

`ONBOARDING-PLAYBOOK.md` establishes a 90-day household onboarding journey with a Phase 4 Day 90 NPS capture as a key metric. The media import runbook operates inside that 90-day window for most households and past it for a documented cohort. This section reconciles the two.

### 10.1 Standard timeline (4-6 weeks) — Small and Medium brackets without extensive legacy media

Small and Medium households without extensive VHS/8mm/film digitization complete media import in 4-6 weeks post-install. Timeline:

- **Week 0 (install day):** CIR interview complete, physical setup complete, initial cloud-sync jobs kicked off on customer-owned devices, home video (if any) shipped to partner
- **Weeks 1-3:** Cloud sync completes; concierge ingests iCloud + Google + Amazon Photos; music library ingested; DRM-free audiobook + ebook ingest complete
- **Weeks 3-4:** Physical disc collection processed via customer-elected Option A/B/C per §4.9; concierge ingests customer-produced MKV files or partner-produced files
- **Weeks 4-5:** Home video partner-produced files returned (if partner turnaround was 4 weeks); concierge ingests
- **Weeks 5-6:** Verification passes 1-3 per §7; dedup; backup validation; handoff session per §8; Advisory-Only Acknowledgment signed
- **Day 90 NPS capture (Week ~13):** Standard `ONBOARDING-PLAYBOOK.md` Phase 4 NPS runs against a household whose media import completed 7-8 weeks earlier. NPS captures the full media-import experience without qualification.

### 10.2 Rush timeline (4 weeks, escalated) — high-touch households with fast-partner-turnaround

Households with time-sensitive events (holiday, out-of-town visitors, sale of a residence with legacy media stored there) can elect the Rush timeline by paying for elective 2-week partner turnaround on home video. Timeline:

- **Week 0:** As standard
- **Weeks 1-2:** Cloud + music + audiobook + ebook ingest completes on an accelerated concierge schedule (concierge L1 dedicates a second concierge L2 for the household during the rush window)
- **Week 3:** Physical disc + rushed home video ingested
- **Week 4:** Verification + handoff + Advisory-Only Acknowledgment
- **Day 90 NPS capture:** Runs against a household whose media import completed at Week 4 — NPS captures the completed experience with the elective rush service as context.

### 10.3 Extended timeline (8-12 weeks) — Large-bracket households with extensive legacy media

Households at the top of the Medium band or in the Large band with 100+ hours of home video, 300+ Blu-rays, or historically-multi-generational film reels routinely extend past the 90-day onboarding window. Timeline:

- **Weeks 0-4:** As standard for cloud + music + audiobook + ebook + moderate-volume physical disc
- **Weeks 4-8:** Physical disc collection Option A/B/C ingest continues (Option B customer-executed rips typically take 3-6 weeks for a 300-title Blu-ray collection at customer's home pace)
- **Weeks 6-12:** Home video partner turnaround extends to 8-12 weeks; concierge ingests as files return
- **Week 13 (Day 90 NPS capture) — two-stage NPS commitment:**
  - **Stage 1 — Day 90 NPS captured against imported-content-so-far.** The concierge and the ONBOARDING team run the standard Day 90 NPS against the content that has been ingested to the Hearth as of Day 90. The NPS survey wording is calibrated to make clear that legacy home video and any elective long-tail rip content is still in progress: "Please rate your Hearth experience so far, understanding that some of your legacy media is still being processed by our partner and will land on your Hearth over the next weeks."
  - **Stage 2 — Day 180 supplemental NPS captured after legacy media completes.** A supplemental NPS survey runs at Day 180, after legacy home video has completed and been ingested. This survey wording is calibrated to the completed experience: "Now that your full library is on your Hearth, please rate your overall experience."
  - The two-stage capture gives the Head of Customer Success two data points — the "content-so-far" NPS at Day 90 (comparable across households with different content-mix profiles) and the "full library" NPS at Day 180 (the ground-truth measurement of the household's completed onboarding). Both are reported to the Board audit committee per `BOARD-GOVERNANCE.md` quarterly cadence.

The v1.0 draft of this runbook did not explicitly commit to the two-stage NPS capture for Extended-timeline households, which created an ambiguity in the Day 90 baseline. §10.3 as written here is the explicit contract.

### 10.4 Sign-off conditions

Under all three timelines, the concierge issues a **conditional sign-off** at the handoff session per §8 if any legacy media is still in transit. The conditional sign-off states: "Concierge has completed all migration tasks under its direct control; legacy media (specific inventory: [list]) remains in transit with [partner name] and will be ingested to the Hearth on return. Household admin acknowledges the conditional sign-off and consents to concierge remote-ingest of returning files without additional in-home visit unless the customer requests one." The conditional sign-off is documented in the household's onboarding record and cross-referenced in the Day 180 supplemental NPS ping.

---

## 11. Concierge SOP and escalation

**Concierge L1 role.** The concierge L1 owns the CIR interview, the day-to-day ingest work, the verification passes, and the handoff session. L1 executes the runbook as written.

**Escalation trigger — hour 55 of media-import concierge time.** At the 55-hour mark of media-import concierge time on any single household, the L1 automatically escalates to the Head of Customer Success. The escalation is not a signal that L1 did anything wrong; it is a structural check on the concierge cost envelope per §1 (14% of GP / $6,400 per household / 40-60 hours of media-import share). Escalation triggers a decision:

- **Continue and absorb.** Head of Customer Success authorizes L1 to continue past 60 hours; the excess is absorbed against the household's overall concierge budget (which may or may not have residual capacity from the physical install and first-week support). This is the default disposition for households in the top of Medium or the low Large band where the completion is 5-10 hours away.
- **Renegotiate scope with household admin.** Head of Customer Success joins the L1 in a scoping call with the household admin. Options: elective rush service (household pays for the delta), scope reduction (household elects to defer some content to a future visit), Advisory-Only expansion (household elects to move more content from the "concierge ingests" bucket to the "advisory only" bucket per §4).
- **Extended-service billable rate.** For Large-bracket households the concierge budget was never expected to cover, Hearth offers a documented Extended Service tier at $100/hr concierge time above the base 60-hour envelope. The Extended Service tier is not marketed pre-install; it is offered only after the household experiences the CIR interview and understands the true scope of their library.

**Concierge L2 role.** Concierge L2 owns advisory-tool conversations under §4.6 / §4.7 / §4.9 (Audible / Kindle / physical disc DRM step), the partner liaison for §6, the Delta Report review under §7 pass 2, and the escalation reference for L1. L2 does not execute DRM tools on customer premises; L2's role in advisory conversations is to explain the third-party ecosystem clearly enough that the household admin makes an informed election.

**Concierge L3 role.** Concierge L3 owns the DMCA §1201 posture per §13, the BIPA per-member consent framework per §12, the FTC §312.5(b) under-13 flow per §12, and the escalation-to-DPO / escalation-to-GC pipeline. L3 is the sign-off role on any household where a household member's request touches biometric consent, under-13 provisions, or DRM edge cases (customer asks concierge to run DeDRM: L3 restates the §13 posture and captures the customer's acknowledgment in writing).

**Escalation-to-DPO trigger.** Any household member privacy request that concierge cannot resolve at the mobile-app Data Portal self-service level within 24 hours escalates to the DPO per `PRIVACY-COMPLIANCE-MANUAL.md` §10. Any BIPA-scope question (member consent, member-scoped content, owner-override attempt on member-scoped biometric artifacts) escalates immediately.

**Escalation-to-GC trigger.** Any customer request that would require concierge to execute DRM circumvention on customer premises (regardless of how the customer phrases it — "just run this for me", "the tool's already installed on my Mac", "you can just do it and I won't tell anyone") escalates immediately to the General Counsel with a documented written record. GC's role is to reaffirm the §13 posture, coach the concierge on the specific language for the customer conversation, and document the incident for the audit trail.

---

## 12. Privacy, consent, and household-member scope

The runbook operates under `PRIVACY-COMPLIANCE-MANUAL.md` in full. This section documents the media-import-specific applications of the framework and closes the BIPA per-member scope gap and the COPPA under-13 gap flagged in the v1.0 draft.

### 12.1 Owner override and member-scoped biometric content — the BIPA per-member rule

The v1.0 draft of this runbook stated: "The household owner … can access any content on the Hearth regardless of scoping, via admin credentials." That statement contradicted `PRIVACY-COMPLIANCE-MANUAL.md` §3 and the BIPA per-collection framework as clarified in *Cothron v. White Castle*. **The v1.0 statement is deleted.**

The v2.0 rule is stated in two parts:

**Part 1 — Owner-created and owner-purchased content.** The household owner (account holder / household admin) can access, delete, re-organize, and manage all content the owner personally created (owner's own iCloud photos, own iTunes music library, own home video the owner is depicted in or credited with recording) or purchased (owner's Kindle purchases, owner's Audible purchases, owner's iTunes movie purchases). Owner override on the owner's own content is the default and needs no additional consent.

**Part 2 — Member-scoped biometric content.** The household owner **CANNOT** access, override, or override-and-delete content that is member-scoped by a biometric consent event. Specifically:
- **Voice-tagged personal notes** created by a household member (member A dictates a voice note that is stored under member A's per-member scope) are inaccessible to the owner without member A's fresh consent.
- **Face-tagged photos of a household member** (v2.0+; member B has enrolled face recognition and applied it to historical photos; photos in which member B is tagged are scoped to member B) are inaccessible to the owner as a *biometric-scoped* view without member B's fresh consent. The photos as unscoped media files may still be accessible under the owner's admin scope (because they were ingested at v1.0 install under the owner's admin account), but any browse view, search filter, or query that pivots on member B's face tag is not accessible to the owner without member B's consent.
- **Per-member memory graph entries** (v1.1+, per `PRODUCT-ROADMAP-12-24MO.md` §3 headline feature 2) are member-scoped and not subject to owner override.
- **Per-member voice profile embeddings** and **per-member face profile embeddings** (v2.0+) are member-scoped biometric information under BIPA and cannot be exported, viewed, or transferred by the owner. Deletion of these embeddings is initiated by the member per `PRIVACY-COMPLIANCE-MANUAL.md` §3.

**Rationale.** The BIPA per-collection framework as clarified in *Cothron v. White Castle* means each capture or use of a biometric identifier is a separate consent event. Allowing the owner to override the household member's biometric-scoped view creates exactly the risk BIPA was designed to close: an account holder consenting on behalf of another individual whose biometric information has been separately captured and separately consented. Hearth's product boundary matches BIPA's framework: **member-scoped biometric content is not subject to owner override.**

**Concierge implication at install day and at handoff.** The concierge L1 explains this to the household admin at CIR and at handoff: "Any voice profile, face profile (v2.0+), voice notes, or face-tagged content that a household member creates is scoped to that member. As the household admin, you can see the household's content overall and the content you personally created or purchased, but a specific household member's biometric-scoped content is theirs. This is how BIPA works and how our privacy framework works." The concierge script does not soften this or leave the household admin with a mistaken impression.

### 12.2 Under-13 face profile — verifiable parental consent per FTC §312.5(b)

Per `PRIVACY-COMPLIANCE-MANUAL.md` §3 Under-13 subsection, any face profile of a household member declared under 13 at profile creation requires FTC-approved verifiable parental consent under the COPPA Rule §312.5(b) methods list. Hearth's specific implementation is **credit-card verification via Stripe Identity plus a follow-up video call with the named parent or guardian confirming identity and re-reading the consent text on-camera**.

**v1.0 posture (2027 Q2 pilot → Q4 GA).** v1.0 does not face-tag under-13 members because v1.0 does not do face at all — face recognition is a v2.0 feature per `PRODUCT-ROADMAP-12-24MO.md` §5. This closes the entire COPPA-plus-BIPA gap for face-scoped under-13 content at v1.0 by construction. The concierge does not need to invoke the FTC §312.5(b) flow at v1.0 install day for face; the flow is a v2.0 concern.

**v1.0 posture on voice, under-13.** v1.0 does enroll voice profiles at install day per `PRODUCT-ROADMAP-12-24MO.md` §2.1 and per `PRIVACY-COMPLIANCE-MANUAL.md` §3 voice consent. For any household member declared under 13 at profile creation, no voice profile is enrolled without verifiable parental consent — the FTC §312.5(b) dual-step method (Stripe Identity + video call) is required per `PRIVACY-COMPLIANCE-MANUAL.md` §3 Under-13 subsection. The concierge L3 owns the video-call step; scheduling is on the L3 calendar.

**v2.0 posture on face, under-13.** When a v2.0 household enables face recognition and any household member is under 13, the fresh face consent flow per member includes the FTC §312.5(b) dual-step method as a gate before the under-13 member's face embedding is generated. Concierge L3 owns the video-call step for face just as for voice; the video-call script reads the specific face consent text on-camera and captures the parent/guardian's spoken affirmation.

**Retention on under-13 face content.** Per `PRIVACY-COMPLIANCE-MANUAL.md` §3 Under-13 subsection, retention is the stricter of the parent's stated preference or 12 months, and re-consent is required annually via the same dual-step method.

**Owner-except-parent override on under-13 face-tagged content.** Under-13 face-tagged content is member-scoped by the same BIPA per-collection rule as adult member content — with the additional COPPA-derived constraint that the parent (as verifiable-parental-consent holder for the child) is the party who can consent to viewing and re-consent the retention, not the household owner if the household owner is not the parent. In practice, most households have the account holder = parent, so this collapses to the owner-except-when-not-parent case. Where the household owner is not the child's parent (grandparent household, mixed-custody household), the concierge L3 and the DPO office adjudicate case-by-case.

### 12.3 Consent registry mirroring

Per `PRIVACY-COMPLIANCE-MANUAL.md` §3 "Consent registry mirroring" paragraph, the company-side consent registry mirrors, per household member, the full consent text version the member accepted — not merely the hash. Media-import-specific consent events (biometric enrollment at install, face consent at v2.0 activation, retroactive face-tagging election at v2.0, under-13 parental consent) are all captured under this framework and mirrored to the company-side registry indexed by member ID and consent hash (no household address, no member name). The registry is the litigation-defense primitive if a BIPA class action or COPPA state AG inquiry ever reaches the company.

### 12.4 Concierge access to household content under RustDesk

When concierge remote-support access is required (rare after install day; most media-import work happens in-home), the RustDesk tap-consent gate per `THREAT-MODEL.md` §3.7 applies. Concierge cannot view household content without the household admin's tap-consent, and the session is logged in the household audit log. For member-scoped biometric content, tap-consent from the household admin does not grant access — the specific member's fresh consent is required. This closes the possible loophole where concierge might attempt to view member-scoped content under admin-tap.

---

## 13. DMCA §1201 legal posture

**Explicit statement of position.** Hearth does not offer DMCA §1201 circumvention as a service. Hearth's concierge team is trained not to execute DeDRM tools, disc-decryption tools, or any DMCA §1201 circumvention technology on customer premises, on the customer's device, or on Hearth-owned equipment carried into the customer's home. This posture is enforced by concierge training per `WARRANTY-TRAINING.md`, by escalation-to-GC per §11, and by the Advisory-Only Acknowledgment per §8.

**What §1201 prohibits.** 17 U.S.C. §1201 prohibits circumvention of technological measures that effectively control access to a work protected under the Copyright Act, regardless of whether the underlying content is legally owned by the person performing the circumvention. The Librarian of Congress's triennial rulemaking has, in various cycles, granted narrow exemptions for accessibility use, security research, and other specific classes — **the Librarian has not granted a general personal-use exemption for Audible AAX/AAXC DeDRM, Kindle DeDRM, DVD (CSS) circumvention, Blu-ray (AACS) circumvention, or UHD Blu-ray (AACS 2.0) circumvention**. Personal-use interpretations exist in some state jurisdictions but do not override federal §1201.

**Why concierge cannot execute DRM circumvention as install-day SOP.** Even where a customer legally owns the underlying content — the customer bought the Audible book, bought the Kindle book, bought the Blu-ray disc — §1201 prohibits the circumvention technology and the trafficking-in-circumvention-technology. Hearth's Series B posture is anchored on SOC 2 Type II, ISO 27001, and a published Trail of Bits audit — three trust signals whose credibility depends on the operational reality matching the certification narrative. Concierge staff routinely committing federal DMCA §1201 violations as part of standard install-day SOP is not reconcilable with that posture. The auditor question at Type II observation-window review is: "does your operational reality match your control narrative?" and the answer must be yes.

**What concierge can do.**
- Advise the customer on the third-party ecosystem that exists for DRM-encumbered content per §4.6 / §4.7 / §4.9
- Ingest customer-produced DRM-free files (produced by the customer on the customer's own device at the customer's own election) into the Hearth library
- Route the customer to Hearth-partnered licensed disc-transfer services where they exist for physical discs (§4.9 Option A) and where the partner's licensing posture matches Hearth's audit posture
- Coexist with customer's own DRM systems (Kaleidescape per §4.5) via metadata index + external-player routing
- Document, in writing, in the Advisory-Only Acknowledgment per §8, the specific DRM-encumbered content categories that remain outside the Hearth library at the customer's household

**What concierge cannot do.**
- Execute Audible AAX/AAXC DeDRM tools on customer premises, on the customer's device, or on Hearth-owned equipment
- Execute Kindle DeDRM tools on customer premises, on the customer's device, or on Hearth-owned equipment
- Execute DVD CSS decryption tools on customer premises, on the customer's device, or on Hearth-owned equipment, in service of transferring customer-owned DVD content to the Hearth library
- Execute Blu-ray AACS decryption tools (MakeMKV-with-key-extraction or equivalent) on customer premises, on the customer's device, or on Hearth-owned equipment
- Execute UHD Blu-ray AACS 2.0 decryption tools on customer premises under any circumstances — the AACS 2.0 keys are only extractable via specific hardware + firmware combinations that are themselves circumvention technology
- Provide the customer with copies of DeDRM tools, links to DeDRM tools, or step-by-step instructions to run DeDRM tools on the customer's device (advising the customer that a third-party ecosystem exists and naming the two or three most cited tools is distinct from providing the tools themselves or step-by-step execution instructions)

**Customer-election override — the boundary.** A customer who says "I don't care about your posture, just do it" is not a valid override. The concierge L1 restates the posture, escalates to concierge L3 if the customer persists, and — if the customer continues to insist — L3 states the posture in writing and closes the conversation. Hearth's exposure to §1201 is not reduced by a customer's verbal request or written waiver, because the trafficking-in-circumvention-technology prong of §1201 applies to the trafficker's conduct regardless of the recipient's consent.

**Legal review + Board notification.** Any change to the §13 posture requires General Counsel sign-off, Head of Privacy sign-off, and Board audit committee notification per `BOARD-GOVERNANCE.md`. Any material Librarian of Congress ruling that grants a new §1201 exemption applicable to Hearth's use cases triggers a full re-review of this section and a documented decision to revise or preserve the posture.

**Written customer disclaimer at install day.** The household admin, at CIR intake or at install day (whichever comes first), signs a written disclaimer acknowledging that:
- Hearth's concierge team does not execute DRM removal on the customer's DRM-encumbered content
- The customer may elect, on their own device, in their own account, at their own discretion, to use third-party tools; if so, Hearth's concierge team will ingest the resulting DRM-free files
- The customer's DRM-encumbered content that the customer does not self-service will remain accessible only through the customer's existing devices and services, not through the Hearth
- Hearth's "100% content migrated" commitment is scoped to non-DRM content per §1

The disclaimer is filed in the household's onboarding record and referenced by future concierge sessions.

---

## 14. Cross-doc reconciliation

This runbook is consistent with, and reconciled against, the following peer documents. Any conflict resolves in favor of the peer document named as the source of truth for the specific topic, with this runbook updated to match within one revision cycle.

- **`PRIVACY-COMPLIANCE-MANUAL.md` §3 — biometric consent framework.** This runbook's §12 (owner override + member-scoped rule + under-13 face flow) is the media-import-specific application of the privacy manual §3. The privacy manual is the source of truth on consent scaffolding; any conflict resolves in favor of the privacy manual.
- **`PRODUCT-ROADMAP-12-24MO.md` §2 (v1.0 feature set) + §5 (v2.0 feature set).** The v1.0 vs v2.0 feature-gate table in §5 of this runbook is derived from the roadmap. Any change to the version-to-feature mapping in the roadmap requires simultaneous update to this runbook.
- **`ONBOARDING-PLAYBOOK.md` Phase 4 Day 90 NPS.** The Day 90 + Day 180 two-stage NPS capture in §10.3 of this runbook is the media-import-specific reconciliation of the ONBOARDING 90-day cadence. Any change to the ONBOARDING Phase 4 cadence requires simultaneous update to §10 of this runbook.
- **`FINANCIAL-MODEL-SENSITIVITY.md` §2.6 — concierge cost as % of gross profit.** The 14% GP / $6,400 per household / 40-60 hour envelope in §1 and §3 of this runbook is derived from the financial model. Any change to the concierge cost line item in the model requires simultaneous update to §1 and §3 of this runbook.
- **`THREAT-MODEL.md` §1.2 — seven-class egress ACL.** The runbook's operations (concierge laptop, rip station, temporary NAS surface, ingest tooling) all operate inside the seven-class egress ACL. Any change to the egress list requires simultaneous update to the runbook's ingest tooling section (§3) and verification section (§7).
- **`WARRANTY-TRAINING.md` — concierge training curriculum.** The §11 escalation SOP and §13 DMCA posture are implemented in the concierge training curriculum. Any change to the runbook's concierge role definitions requires simultaneous update to the training curriculum.
- **`BOARD-GOVERNANCE.md` — audit committee oversight.** Board audit committee reviews the annual media-import posture change log, the DMCA §1201 posture per §13, and any material change to the BIPA / COPPA framework per §12.

**Sign-off authority.** Changes to §12 (privacy + BIPA per-member scope + COPPA under-13) require Head of Privacy sign-off + General Counsel review. Changes to §13 (DMCA §1201 posture) require General Counsel sign-off + Head of Privacy notification + Board audit committee notification. Changes to §1 (concierge cost frame) require CFO sign-off + Head of Customer Success acknowledgment. All other changes require Head of Customer Success sign-off with the peer-document owners notified.

The compliance baseline exists so that the next audit, the next regulator inquiry, and the next enterprise buyer's due-diligence request can be answered from a single source with a straight face — and so that the concierge team can execute against a written, cross-referenced, DMCA-safe, BIPA-scoped, COPPA-compliant, financially-reconciled framework that matches the Series B posture Hearth commits to in the pitch dataroom.

*End of Media Import Runbook v2.0.*

Full file at: /private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/hearth-seriesb-media/MEDIA-IMPORT-RUNBOOK-v2.md (9,270 words, inside the 6,500-9,500 target).
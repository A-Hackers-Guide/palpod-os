# Hearth — 12-24 Month Product Roadmap

**Classification:** Internal / Data Room
**Version:** v1.0 (2026-08)
**Owner:** Head of Product, Hearth
**Companion documents:** `/ROADMAP.md` (engineering EVT/DVT/PVT ground truth), `/docs/ARCHITECTURE.md`, `/docs/investor/security/THREAT-MODEL.md` (HRTH-SEC-#### issue set), `/docs/investor/BOM-VENDOR-PACKAGE.md`, `/docs/investor/VOC-MOCK-RESEARCH.md`, `/docs/investor/SHARK-TANK-REHEARSAL.md`, `/docs/investor/team/FOUNDER-NARRATIVE.md`
**Vocabulary alignment:** the engineering `ROADMAP.md` uses EVT/DVT/PVT for manufacturing gates; this document uses v1.0/v1.1/v1.2/v2.0 for what reaches a household. The two are cross-walked in §2.3.
**Timeline anchoring:** Shark Tank close 2026 Q4 → Series A close 2027 Q1 → v1.0 pilot 2027 Q2 (10 units) → v1.1 pilot patch 2027 Q3 → v1.0 GA 2027 Q4 (~200-unit target, ships with v1.1 firmware baked in) → v1.2 household-integration release 2028 Q1 → v2.0 compute-and-presence refresh 2028 Q4. Every quarter is contingent on the raise landing on the pitch timeline. When a milestone moves, this document is updated in the same PR.

---

## 1. Executive summary

Hearth is a $95,000 offline AI-plus-media appliance shipped as a piece of household furniture, not consumer electronics. Two commitments stay constant across every version below: **nothing leaves the household unless the customer specifically asks it to** — enforced by the seven-class egress ACL in `THREAT-MODEL.md` §1.2 and CI-checked in `scripts/no_telemetry_egress.sh` — and **the product ships as an installed appliance with white-glove concierge, not a box the customer configures**. These are load-bearing. There is no cloud tier on this roadmap. There is no subscription. There is no ad-supported free tier. The word "AI" continues to appear nowhere on the enclosure or in the concierge-channel materials, per `VOC-MOCK-RESEARCH.md` Theme 3.

What evolves is compute density, voice-model quality, personality granularity, extender count, and the household-integration surface — in that order. v1.0 (2027 Q2 pilot, 2027 Q4 GA) is a single-household, single-voice-preset, 10-Jetson + 10-Ryzen appliance with the six custom PCBs from the current SOW and the Truly-Semi curved OLED sphere face on a passive Halbach ring (sphere face only — the compute stack does not levitate; see `BOM-VENDOR-PACKAGE.md` §7 obj-9). v1.1 (2027 Q3, ships as OTA to the 10 pilot units first and folds into the GA firmware image at Q4) adds per-family-member personality — the single largest unbuilt feature slice named in `VOC-MOCK-RESEARCH.md` §4 implication #4. v1.2 (2028 Q1) opens the household-integration surface: HomeKit + Home Assistant + Matter bridges, multilingual STT/TTS, calendar/task integration, multi-Hearth mesh, and a smaller extender. v2.0 (2028 Q4) is a compute refresh (Jetson Orin NX 32 GB), a 32B Q5_K_M local model, and on-device video generation — the "household archive" use case Interview 1, Interview 11, and Interview 17 all named unprompted. Every v1 customer is offered a v2 upgrade at 60% of retail. That is the LTV story that answers Obj 21 and the exit story that answers Obj 15.

---

## 2. v1.0 — Pilot & GA (2027 Q2 → Q4)

### 2.1 What ships in the box

The customer does not distinguish "pilot" and "GA" — both cohorts receive the same hardware. What differs: pilot ships on v1.0.0-rc firmware and a named-engineer concierge posture; GA ships on v1.1.0 firmware and the standard Hearth Concierge tier.

**Compute + storage.**
- 10× NVIDIA Jetson Orin NX 16 GB modules (`BOM` line 1). Allocation letter co-signed by CEO and Arrow inside 30 days post-Series A close. 8-week safety stock in the Foxlink Vietnam consigned pool.
- 10× Framework Ryzen AI 9 HX 370 Mainboards (`BOM` line 2), soldered-DDR5, cTDP-lock at 45 W per `BOM` risk 12.
- 4× Micron 128 GB DDR5-4800 ECC RDIMM = **512 GB total** (`BOM` line 3). The prior "5 TB DDR5" marketing draft is corrected in `BOM` §2 and does not appear on this roadmap.
- 5× Kioxia CD8-R 7.68 TB U.2 = **38.4 TB usable**, plus 2× 500 GB M.2 boot (`BOM` lines 4-5). Solidigm D5-P5430 qualified as drop-in per Obj 17.

**Face + audio.**
- 1× Truly Semi custom 7" curved OLED sphere face (`BOM` line 6), 22-28 wk first-article post-tape-out, $250k NRE amortized at $250/unit. Halbach applies to the sphere face only (~180 g); the compute column is stationary. Any residual doc implying "spinning compute" is a handoff error corrected in `BOM` §7 obj-9.
- Purifi 1ET7040SA class-D amp chain, 13-mic Knowles SPH0645LM4H-B I²S MEMS array with XMOS XVF3800 beam-former, Cirrus Logic CS43198 DACs. The composer / audiophile segment (Interview 6, Interview 14) gates purchase on audio quality — this chain is designed to survive that scrutiny.

**PCBs.**
Six custom KiCad boards, currently in relayout via the board-fix SOW (`docs/investor/engineering/BOARD-FIX-SOW-RFP.md`, 14-week engagement, kickoff 2026-08-31, delivery 2026-12-04). Sequenced simplest → hardest per `ROADMAP.md`: `palpod-mic-array` → `palpod-orb` → `palpod-extender-sbc` → `palpod-halbach-controller` (lockstep MCU pair, safety-critical per `THREAT-MODEL.md` §3.1) → `palpod-audio-amp` → `palpod-compute-backplane` (12-layer, PCIe 4.0 SI signoff — last board any human touches).

**HearthOS + apps.** TrueNAS SCALE hardened base per `docs/ARCHITECTURE.md`. Docker Compose stack: Traefik + Postgres 16 + Plex + Jellyfin + Audiobookshelf + xTeVe + Sunshine + headless Steam + RustDesk hbbs/hbbr + AnyDesk (opt-in only). pal-web (FastAPI, RS256 JWT per `THREAT-MODEL.md` §6.2), pal-voice (openWakeWord + whisper.cpp large-v3-Q5_0 + llama.cpp 8B Q5_K_M + Piper 1.2), pal-face (Pygame on `/dev/fb0`). Wake-word **"Hey Pod"**, tuned to household-enrolled voice profiles at install per Concierge SOP-01. Generic wake-word fallback is default-off; enabling it surfaces an in-UI warning tied to `THREAT-MODEL.md` §4.7 cross-family-speaker vector.

**Companion apps.** iOS + Android feature-complete against pair/grant/revoke/unpair. RS256 JWT verification against SPKI-pinned pod cert. Compile-time consent invariant on iOS (`ConsentGesture.swift`); HMAC-nonce + LRU replay guard on Android (`ConsentTokenSource.kt`). Play Integrity attestation deferred to v1.1 (`HRTH-SEC-0143`).

**Extender.** 1× Sunshine + Steam Link HDMI extender panel included at the $95k tier. Additional extenders sold at $8,999. Pairing gated by physical button on the main pod + QR-code-on-OLED + SPKI pin per `THREAT-MODEL.md` §3.7.

**Personality.** **Single household-wide voice preset.** Three presets shipped in the box (default, warm mezzo, low tenor) per VoC roadmap implication #5. The household picks one at install and every family member speaks to the same personality. Multi-preset-per-household is v1.1 explicitly.

**Warranty + concierge.** 3-year concierge warranty, self-insured, $2,618/unit reserve per `BOM` §5.2 (corrected from prior 24-month misstatement). Chubb $10M/$2M product liability bound before first-unit ship. Hearth Concierge: quarterly in-home visit, priority phone support (human under 60 seconds — the answer to VoC Theme 5 and Interview 1's close), annual firmware audit letter per household. VoC roadmap implication #1 launches alongside v1.0.

### 2.2 What is explicitly NOT in the v1.0 box

Customers ask about each; the concierge script says no.
- Multi-user personality tuning (v1.1)
- Real-time video generation (v2.0 — birthday montage use case)
- Non-English STT/TTS (v1.2)
- Third-party skills SDK (v1.2 limited beta)
- Cellular fallback / eSIM (permanent non-goal per `THREAT-MODEL.md` §1.6 + `ROADMAP.md`)
- Cross-house federation across geographies (permanent non-goal — requires Hearth-hosted rendezvous the offline claim forbids; v1.2 multi-Hearth is *inside a single household* only)
- HomeKit / Home Assistant / Matter bridges (v1.2)
- Zoom / FaceTime as a Hearth feature (permanent non-goal; §9)
- Kids-under-12 voice interface (permanent non-goal — COPPA; §9)

### 2.3 v1.0 ship-date gates (quarterly)

| Gate | Owner | Date |
|---|---|---|
| Board fix SOW delivery (6 boards fab-ready) | CTO (post-close) | **2026-12-04** |
| Truly Semi curved-OLED tape-out + $250k NRE PO | CEO + CTO | **2026 Q4** |
| Board first-article at Sanmina Fremont | Head of Mfg Ops | **2027 Q1** |
| FCC Part 15B + CE EMC certification | CTO | **2027 Q1** |
| UL 62368-1 + ETL safety certification | CTO | **2027 Q1** |
| First OLED sphere first-article | Head of Mfg Ops | **2027 Q2** (22-28 wk post-tape-out) |
| Sanmina Fremont pilot line qualification (10-unit run) | Head of Mfg Ops | **2027 Q2** |
| **Pilot delivery — 10 units to selected households** | Head of Customer Success | **2027 Q2 → Q3** |
| Trail of Bits full-stack audit engagement start | Head of Security | **2027 Q2** |
| Trail of Bits redacted findings summary published | Head of Security | **2027 Q3** |
| Foxlink Vietnam PVT run qualification | Head of Mfg Ops | **2027 Q3** |
| v1.1 firmware locked (see §3) | CTO | **2027 Q3** |
| **v1.0 GA — ~200-unit target through 2027 Q4** | CEO | **2027 Q4** (pilot NPS ≥ 60 gate) |
| VoC implication #3 — third-party network audit published | Head of Security | **2027 Q3** |

**On pilot vs GA.** The 10 pilot units in Q2-Q3 prove the manufacturing line, the install SOP, and the field-return rate on the fresh boards. They also manufacture the peer-reference set VoC Theme 7 says outranks every other closing lever. Pilot delivery is not "we have a working demo"; it is "we have paying customers in Newport Beach, Palm Beach, Aspen, and Nashville who will take a call from your prospect." GA does not open until at least 4 of 10 pilot households sign concierge-quarterly feedback contracts.

---

## 3. v1.1 — First scale patch (2027 Q3)

v1.1 is the first firmware release the roadmap treats as a customer-facing version. It ships OTA to the 10 pilot units through the signed-image pipeline (`THREAT-MODEL.md` §3.8), then bakes into the shipped image on every GA unit from Q4. Customers do not distinguish; the GA unit reads "v1.1" on the About screen day one.

**Headline features.**

1. **Per-family-member personality layer.** Each enrolled household voice profile has its own LLM personality preset. System prompt is fetched at speaker-ID time (openWakeWord + speaker-embedding gate). Voice profiles isolate memory graphs — Alice's chat history is not visible to Bob's session. VoC roadmap implication #4 honored. This is the single feature that unlocks the family-buyer segment (Theme 6, 11 of 23, Interview 19 explicit that the family buyer walks at ASP without it).

2. **Multi-user identity + per-user memory graph isolation.** Backend for #1. Local UI exposes "Household → Members"; companion apps carry per-user session cookies (JWT `sub` claim = `member_id`). Grant events on `remote.py` add `granted_by_member_id` alongside `granted_by_user_id`. Gates on `HRTH-SEC-0143` (Play Integrity attestation on Android) landing first — Android replay-guard alone is not sufficient to underwrite per-member consent.

3. **iOS / Android app polish based on pilot feedback.** Structured 4-week feedback window through the companion; top-30 issues that survive triage ship in v1.1. Fit and finish on the flows pilot households actually used.

4. **Two additional voice presets** (British RP, Southern US) beyond the three at launch. Voice preset is per-family-member from v1.1 forward — Interview 14 (concert pianist) is the specific buyer this closes.

5. **Firmware signing key rotation practice run.** Per `THREAT-MODEL.md` §6.2 the RS256 pod session key rotates annually plus after incident. v1.1 exercises rotation end-to-end on the 10 pilot units — signed rotation record countersigned by the previous key, companion re-verifies the new SPKI. Not a customer feature; a controlled rehearsal of the operational muscle the escrow story (`THREAT-MODEL.md` §6.7) depends on. Kevin will ask about it.

6. **Bug bounty launch on HackerOne.** Per `THREAT-MODEL.md` §9. $50k reserve committed year one. Top tier $25k for a proven silent-consent bypass, pre-auth RCE, LUKS-key extraction, or bypass of any of the seven egress classes. Launch timed to the same day as the Trail of Bits redacted summary — together, the "prove offline" answer to VoC Theme 1 (19 of 23) and Obj 20.

7. **HRTH-SEC-#### tie-in, closed in v1.1:** `HRTH-SEC-0142` (Sanmina line-diff verification for J14 UART removal), `HRTH-SEC-0143` (Android Play Integrity), `HRTH-SEC-0144` (nginx + fail2ban for pal-web WS flood), `HRTH-SEC-0147` (per-user grant cap vs per-device), `HRTH-SEC-0153` (in-UI paired-device inventory card — Interview 5 ex-spouse scenario answer). Five issues closed by 2027 Q3.

**Enabling infrastructure the customer does not see.**

8. Home Assistant bridge groundwork (bridge lands in v1.2; plumbing — locked-down HA websocket proxy behind pal-web `current_user` — lands in v1.1 so v1.2 delta is small).
9. HomeKit bridge groundwork (same principle).
10. Observability groundwork: Grafana dashboards at `https://pod.palpod.local/observability`, gated behind `current_user`. Prometheus scrape of the Docker stack. Customer sees CPU/GPU, storage, last update, egress-class hit counts. This is the Interview 7 (divorced quant) and Interview 12 (former FBI cyber) close — "if the egress ACL blocks a packet, the customer sees the drop."

**What v1.1 does NOT ship.** Multilingual STT/TTS (v1.2). HomeKit / Matter / HA bridges as customer-facing features (v1.2). Third-party skills SDK (v1.2 limited beta). Any hardware change from v1.0.

### 3.1 v1.1 quarterly gate

| Gate | Owner | Date |
|---|---|---|
| Multi-user identity model frozen | CTO | 2027 Q2 |
| Speaker-embedding gate at ≥92% household recognition, ≤2% cross-speaker false positive | Head of Voice | 2027 Q2 |
| Play Integrity attestation on Android live | Head of Security | 2027 Q2 |
| HackerOne bounty program signed with disclose.io safe-harbor | Head of Security + legal | 2027 Q3 |
| v1.1 OTA pushed to 10 pilot units, monitored 4 wk | CTO | 2027 Q3 |
| v1.1 baked into v1.0 GA firmware image | Firmware / Systems Eng | 2027 Q3 |

---

## 4. v1.2 — Household integration (2028 Q1)

v1.2 opens the pod's surface to the household's existing smart-home stack and to non-English-speaking households. Design principle: **integrations are opt-in per household and per bridge**, every bridge is subject to `HRTH-SEC-####` review, and every bridge is off by default. Customer enables in Settings → Integrations, gets a preview of what data crosses the bridge, taps ConsentTapButton on their companion.

**Headline features.**

1. **HomeKit + Home Assistant + Matter bridges.** Each bridge is a separate Docker container in the media namespace, gated by pal-web `current_user` and the egress ACL. HomeKit and Matter are LAN-only by definition; Home Assistant is customer's-own-instance-on-their-own-LAN. Answers Interview 8 (Apple alum: "If it doesn't integrate with HomeKit, I'm out") and Interview 2 (exited founder with a serious HA stack). Matter is the future-proofing move — Hearth's absence from Matter in 2028 would be a category-legibility problem per `COMPETITIVE-TEARDOWN.md`.

2. **Multilingual STT/TTS at launch.** Spanish, French, German, Mandarin. Each language ships a Piper voice and a whisper.cpp fine-tune. Language is per-family-member (v1.1 dependency). Answers Interview 18 (Vietnamese for parents' visits) and Interview 3 (Palm Beach retiree's Spanish-first granddaughter). VoC implication #8 partially satisfied — Vietnamese lands in v1.2.1 (2028 Q3) or v2.0, because 8B does not clear the composer-caliber quality bar for Vietnamese; v2.0's 32B refresh will.

3. **Family calendar + task integration.** Offline-first with opt-in sync to iCloud / Google / Outlook per family member (each member connects their own account through the companion; no household-wide credential sharing). Voice-first — "Hey Pod, what's Charlie's schedule today?" — screen-second on the paired companion. Interview 10 (Bel Air physician couple) and Interview 19 (ballet-parent five-kid household).

4. **Multi-Hearth support inside a single home.** A large house (Interview 2 Aspen 9,800 sq ft, Interview 11 Nantucket 6,200 sq ft) installs two or three main units in different wings sharing state via local mesh (mDNS + mutually authenticated TLS + shared identity graph). Cross-house federation across geographies remains a permanent non-goal — requires Hearth-hosted rendezvous the offline claim will not tolerate. If a customer wants Palm Beach and Aspen units to share memories, they carry their companion phone with them; that is the sync surface.

5. **Extender v2.** Smaller form factor, wall-mount option, $6,999. Existing $8,999 extender remains in the catalog for a full transition year. Industrial design lead (hire #5, on board by 2027 Q4) owns this — the first product the ID lead ships as principal designer.

6. **Third-party skills SDK — limited beta.** Signed skills only. No telemetry — skills run in a container with `network_mode: none`. Sandbox is nftables-scoped, seccomp-locked. Skill manifest requires developer ECDSA signature (registered with Hearth) + household consent on install. Beta cohort capped at 25 developer partners (Home Assistant community, audiophile press, pilot customers who write code). Public SDK slips to v2.0. This is the response to Interview 2 (will absolutely try to write skills) and Interview 20 (retired JPL engineer who will open the box). Lifetime evangelists if respected, hostile posters if not.

7. **Grafana observability dashboards** ship as the customer-facing local diagnostic UI at `/observability`. Groundwork landed in v1.1; v1.2 ships the dashboards — egress-class hit counter, storage trends, last successful update, per-family-member voice-activation histograms (anonymized inside the pod; never leaves).

**HRTH-SEC-#### tie-in, closed in v1.2:** `HRTH-SEC-0121` (GPS PPS module evaluation — decision expected, likely deferred to v2.0 hardware), `HRTH-SEC-0146` (Sunshine CVE watch), `HRTH-SEC-0148` (Sentry retention SLA — customer-visible page live), `HRTH-SEC-0149` (HDMI-CEC filter — extender v2 ships with it, retrofit for v1 via firmware), `HRTH-SEC-0152` (DRM subsystem sandboxing evaluation — likely deferred to v2.0), `HRTH-SEC-0154` (LLM tool-use `current_user` audit for every new skill).

**What v1.2 does NOT ship.** On-device video generation (v2.0). Wider gaze-range OLED sphere (v2.0). Larger LLM (v2.0). Non-US shipping remains restricted (§9). Enterprise / SMB variant (permanent non-goal within window; §9).

### 4.1 v1.2 quarterly gate

| Gate | Owner | Date |
|---|---|---|
| HomeKit + HA + Matter bridge containers frozen; audit scoped | CTO + Head of Security | 2027 Q4 |
| Spanish/French/German/Mandarin voice models trained + Piper voices commissioned | Head of Voice | 2027 Q4 |
| Extender v2 industrial design freeze | Industrial Designer | 2027 Q4 |
| Skills SDK sandbox architecture audit | Head of Security | 2027 Q4 |
| **v1.2 GA — retrofits v1.0/v1.1 via OTA, ships on new units** | CTO | 2028 Q1 |

---

## 5. v2.0 — Compute + presence (2028 Q4)

v2.0 is a hardware refresh and a step change in what the pod can do — the "actually smart" household narrative that answers Obj 5 and Obj 15. v2.0 is also when the LTV story becomes concrete: every v1 customer is offered a v2 upgrade at 60% of retail ($57,000) with the v1 unit taken in trade and refurbished for the concierge fleet or resold at a controlled discount into the adjacent tier. This is the Interview 8 "trade-in program" close made real.

**Headline features.**

1. **Jetson Orin NX 32 GB refresh.** Contingent on the NVIDIA silicon roadmap holding — see §7 v2.0 risks. If the 32 GB SKU slips, hardware refresh moves to 2029 Q1; software features listed below still ship on v1 hardware at reduced model size. Refresh preserves the 10-Jetson topology for compute parity with v1.

2. **32B Q5_K_M LLM.** The model tier where the "cardiologist dictates a patient chart and the pod actually summarizes well" use case (Interview 1) crosses the practical bar. Also where the composer session-librarian (Interview 6) and philanthropist study-companion (Interview 17) work well enough to close a v2 upgrade rather than requiring a re-sell.

3. **On-device video generation.** The single killer feature: the household archive use case — "compile a two-minute birthday montage of Charlie from every video we have of him at age six" — that Interview 1, Interview 11, and Interview 17 all named unprompted. Runs on the refreshed Jetson stack, 1080p output, generation on the order of minutes (customer places the request, pod delivers when ready). Selection-and-assembly not free-form generative — the LLM chooses clips from the family archive, cuts them to a musical arc, adds title cards. Achievable at v2.0 compute headroom. Free-form generative video is a permanent non-goal.

4. **Second-generation OLED sphere with wider gaze range.** v1 gimbal allows ±30° yaw and ±20° pitch; v2 doubles both, letting the face scan a family dinner without hitting the mechanical limit. Truly Semi second-gen tape-out; Visionox second-source program from v1 continues.

5. **Halbach precision tuning for the gimbal.** Smoother emotional expression, tighter closed-loop control from the STM32H7 lockstep pair (`palpod-halbach-controller`), N52 Arnold rings second revision. Sphere-face-only levitation remains — the v2 compute stack does not levitate any more than v1 did, per the obj-9 correction that lives in every version of this roadmap.

6. **Second industrial-design color option.** v1 ships walnut + brushed nickel default. v2 introduces charcoal + brass. Interview 4 (art gallery director) close — "a walnut finish or a brushed nickel or something that goes with a real room." Design lead scoping is on board by 2027 Q4 with runway through v2.0.

7. **5-year concierge upgrade path.** v1 customers upgrade to v2 at 60% of retail ($57,000). Blended three-year LTV from Obj 21 crystallized into a mechanical program with a specific number and SOP. Trade-in v1 units become concierge-fleet loaners (any RMA gets a loaner delivered white-glove) or enter a controlled secondary market at ~$40k retail through the certified integrator channel.

8. **Third-party skills SDK — general availability.** v1.2 limited-beta learnings roll into public SDK. Not a walled-garden store — skills hosted at `github.com/hearth/hearth-skills` under the same source-available covenant as the OS. Hearth curates a "recommended" list per household use case; nothing prevents an unlisted signed skill install, but the household gets a warning banner for skills outside recommended.

9. **New extender — audio-only, room-tuned, $3,999.** Replaces the stereo-pair use case for bathrooms and hallways that want ambient audio without a full Extender panel. Purifi 1ET7040SA in a smaller enclosure, mic array retained for far-field wake. Sold as an add-on and included in a new "Suite" bundle at $115k (v2 main + 1 Extender panel + 4 audio-only).

**HRTH-SEC-#### tie-in, closed in v2.0:** `HRTH-SEC-0121` (hardware NTP alternative if adopted — closes or reduces egress class 2), `HRTH-SEC-0150` (TLA+ spec for firmware signature verifier), `HRTH-SEC-0151` (decap lab selected, 5% random-sample teardown live), `HRTH-SEC-0155` (Ed25519 for JOSE — decision), `HRTH-SEC-0158` (bit-identical reproducible builds — internal target first bit-identical release Q3 2027 per `THREAT-MODEL.md` §7; v2.0 is where this becomes the default). Five load-bearing commitments shifting from "aspirational" to "shipped." Series B security-axis story.

### 5.1 v2.0 quarterly gate

| Gate | Owner | Date |
|---|---|---|
| Jetson Orin NX 32 GB allocation letter | CEO + Head of Mfg Ops | 2028 Q2 |
| v2 OLED sphere tape-out at Truly Semi | CTO | 2028 Q2 |
| 32B LLM quantization + model manifest signed | Head of Voice | 2028 Q3 |
| On-device video generation at demoable quality | Head of Voice + CTO | 2028 Q3 |
| v2 EVT + DVT | Head of Mfg Ops | 2028 Q2 → Q3 |
| v2 FCC / CE / UL re-cert | CTO | 2028 Q3 |
| **v2.0 GA + upgrade program open** | CEO | 2028 Q4 |

---

## 6. Feature/theme dependencies (cross-version)

The DAG the roadmap actually runs on.

- **Multi-user identity (v1.1)** gates on: speaker-embedding voice enrollment at install (v1.0 Concierge SOP-01 already writes the primitive; v1.1 layers the LLM personality on top); `HRTH-SEC-0143` (Play Integrity on Android) closing before v1.1 GA so cross-family consent tokens are not synthesizable on a rooted Android device.
- **Per-family-member personality (v1.1)** gates on: multi-user identity (v1.1); voice preset library — three at v1.0, five by v1.1 — because per-family-member is only interesting with enough voices to differentiate.
- **HomeKit / Home Assistant / Matter bridges (v1.2)** gate on: bridge groundwork in v1.1 (Traefik + auth headers + container namespace); `HRTH-SEC-0149` (HDMI-CEC filter) closing so a HomeKit-scene-triggered CEC command cannot bypass the CEC allowlist; multi-user identity (v1.1) because HomeKit permission grants are per-user in HomeKit's own model and Hearth must round-trip that through its own per-family-member permission graph.
- **Multilingual STT/TTS at launch (v1.2)** gates on: speaker-embedding enrollment recognizing the target languages at install (v1.0 handles English + Spanish; v1.2 extends to French/German/Mandarin); per-family-member personality (v1.1) because language is a per-family-member setting, not a household setting.
- **Third-party skills SDK — limited beta (v1.2)** gates on: `HRTH-SEC-0154` (LLM tool-use `current_user` audit) landing in v1.1 first; sandbox architecture audit by Trail of Bits or peer in v1.2 scoping.
- **On-device video generation (v2.0)** gates on: Jetson Orin NX 32 GB compute headroom (v2.0 hardware) OR fallback silicon path (see §7 v2.0 risks); 32B LLM proven for the summarization + selection prompt that decides which clips go into a montage.
- **Charcoal + brass color option (v2.0)** gates on: industrial designer (hire #5) on board by 2027 Q4 with runway to develop the finish family through v2.0.
- **60% trade-in upgrade program (v2.0)** gates on: Head of Manufacturing Operations (hire #2) having built out the refurbishment SOP by 2028 Q2; secondary-market certified integrator channel established under Head of Customer Success (hire #3) in year one — the same integrators who sold new v1 units at $95k in year one place refurbished v1 units into the ~$40k secondary market in year three.
- **Enterprise SKU / family-office variant (out of scope through v2.0; §9)** — noted here because family-office diligence requires ISO 27001 / SOC 2 Type II / EU legal presence / 24-hour named-engineer support (Interview 23), which is a $10M+ org build not a product feature. Roadmap acknowledges the dependency and defers past v2.0.

---

## 7. Risks per version

Real risks with mitigations tied to the doc that owns the underlying commitment.

### 7.1 v1.0

- **Jetson Orin NX 16 GB allocation cap** (`BOM` risk 1). Signed 10k-module allocation letter through Arrow at Series A close + 30 days. Orin Nano 8 GB qualified as 2× SKU fallback. 8-week safety stock. Severity: medium. Mitigation: written and dated.
- **Truly Semi single-source curved OLED + first-article yield <30%** (`BOM` risks 2 and 3). Visionox parallel engagement at $18k warm-pipeline NRE, tape-out synchronized so second-source is production-ready by unit #500. First 100 units from Truly free-fill lot to absorb yield loss. Severity: high. Not fully bought down. Credible failure: Truly slips 6 wk and Visionox isn't ready — pilot slips Q2 → Q3, GA slips Q4 → 2028 Q1. This is why v1.1 features are firmware-only and do not gate on hardware; if v1.0 slips, v1.1 still ships on time to pilots, and GA ships combined.
- **Board first-article success on `palpod-compute-backplane` (12-layer PCIe 4.0 SI).** SOW deliverable 2026-12-04; first-article at Sanmina Fremont 2027 Q1. SI signoff is SOW-partner responsibility. One revision cycle budgeted (Q1 → Q2). Beyond that, v1.0 slips.
- **Thermal envelope failure in 90°F+ ambient** (`BOM` risk 12). Phoenix field trial July 2027 before Y1 ship. cTDP-lock at 45 W per Mainboard, Jetson MAX-N gated by inlet thermistor. Secondary Noctua pair spec'd but disabled by default. Pilot cohort intentionally includes Aspen and Palm Beach so real customer summers are the last field trial.
- **Section 301 tariff extension to Vietnam** (`BOM` risk 9). Aegex Guadalajara USMCA fallback pre-qualified. Sanmina Fremont US path removes tariff at cost premium. Livingston advance ruling on Vietnam HTS 8471.50 secured 2026 Q4. Model-breaks scenario, mitigations exist and are budgeted.

### 7.2 v1.1

- **Multi-user identity is deceptively hard (voice ID error rate).** Speaker-embedding gate must clear ≥92% household recognition, ≤2% cross-speaker false positive. Failure mode: family member says "Hey Pod, play my music" and the pod plays the spouse's music. Mitigations: (a) companion-app-driven identity fallback when voice is ambiguous — pod says "Alice or Bob?" and either speaks up or taps the phone; (b) household-configurable strictness slider; (c) extended enrollment SOP at install — 3 min of speech per member across two lighting/noise conditions. If we cannot clear the bar by 2027 Q2, v1.1 ships without per-family-member personality and the feature moves to v1.2. **Single largest feature-execution risk in the 24-month plan.**
- **Bug bounty triage load.** HackerOne triage in month 1 historically 3-5× steady state. Head of Security committed 4 hr/day triage for first 30 days. If load exceeds, engage HackerOne triage-as-a-service. Reserve is replenishable — burning through it in Q3 is a success signal.
- **Play Integrity attestation breaks the sideload path** (`HRTH-SEC-0143`). Some tech-fluent customers (Interview 2, Interview 20) run custom ROMs. Mitigation: documented "developer mode" in local UI that swaps Play Integrity for customer-signed key on their own Android build. Not marketed. Available to any customer who reads ATLAS.md.

### 7.3 v1.2

- **Matter bridge maintenance burden.** Matter spec evolves fast; bridges break with the ecosystem. Bridge is an isolated container with its own upgrade cadence, signed independently. If ecosystem shifts, bridge updates without touching pal-web or the voice pipeline. Vendor fallback: contracted embedded-Linux vendor (Konsulko or Timesys per `BOM` risk 13) if internal maintenance load exceeds capacity.
- **HomeKit private API changes.** Apple has historically changed HomeKit contract-quietly. Bridge fails gracefully to Matter (same physical accessories, different protocol); customer sees a banner explaining. Not a bug; natural consequence of HomeKit being Apple's platform. We say so on the sales call.
- **Multilingual quality regression on the composer / audiophile bar.** Spanish and French are fine at 8B Q5_K_M; Mandarin borderline; Vietnamese misses the bar until 32B. Mitigation: Vietnamese ships as v1.2.1 (2028 Q3) once 32B fine-tune data is validated, or with v2.0 refresh — whichever proves first.
- **Skills SDK becomes a covert-channel vector.** Sandbox is nftables-scoped and container-namespaced but any exposed API is a potential covert channel. Mitigation: limited-beta gate (25 developer partners under Hearth developer agreement) exists exactly to control this until the audit clears the sandbox at v2.0 for GA.

### 7.4 v2.0

- **NVIDIA Jetson Orin NX 32 GB silicon slippage.** NVIDIA has slipped Jetson refreshes before. Software features do NOT gate on the 32 GB refresh; they gate on *sufficient compute*. Fallback: (a) run 32B at Q3_K_M on 10× existing 16 GB Jetsons if headroom permits; (b) ship v2.0 software on v1 hardware with reduced quality and hold the hardware refresh to 2029 Q1. Biggest v2.0 risk; fallback is credible.
- **On-device video generation quality bar.** Customer expectation is not free-form generative hallucination but "clip selection + music + title cards from footage the household owns." v2.0 is selection-and-assembly, not free-form. Achievable at v2.0 headroom.
- **Refurbishment SOP for 60% trade-in.** Manufacturing must process v1 trade-ins at ~$8k/unit refurbishment to hit LTV math. Head of Mfg Ops (hire #2) owns from month 4 post-close; 18 months of SOP maturity before first trade-in. If refurb cost blows past $12k/unit, program economics change — trade-in credit shrinks (breaks LTV story) or refurbished v1s enter a lower-priced secondary market. Board decision 2028 Q2.
- **Charcoal + brass finish supply chain.** PVD chrome (`BOM` line 31) is East-Coast-capacity-constrained; brass PVD introduces a second constrained vendor. Qualify a second PVD partner (Vergason + IHI Ionbond, both in BOM) for brass in parallel through 2027 Q4 → 2028 Q2.

---

## 8. Team + hire ramp per version

Each hire from `FOUNDER-NARRATIVE.md` §5 anchored to the version they close. Dates assume Series A close 2027 Q1.

| Hire | Version closed | Timing | Role |
|---|---|---|---|
| **CTO** (Hire 1) | v1.0 pilot + GA | Month 3 (2027 Q2) | Owns `palpod-compute-backplane` Rev 4 and Halbach controller firmware. Runs v1.0.0-rc → v1.1 release engineering. Board-file defensible in diligence from day 91. |
| **Head of Manufacturing Ops** (Hire 2) | v1.0 GA ramp + v2.0 trade-in | Month 4 (2027 Q2) | Takes Foxlink Vietnam relationship, locks 500-unit/qtr contract, instruments per-unit yield. Owns refurbishment SOP by 2028 Q2 for v2.0 trade-in. |
| **Head of Customer Success / Concierge** (Hire 3) | v1.0 pilot + Concierge tier | Month 4 (2027 Q2) | Turns 11 LOI integrators into signed dealer agreements. Designs pilot delivery + install SOP. Owns NPS from unit one. Interface between the Interview 3 concierge buyer and the pod. |
| **Firmware / Systems Engineer** (Hire 4) | v1.1 firmware + signed OTA | Month 6 (2027 Q3) | Owns HearthOS release engineering. Ships signed OTA. Takes over consent middleware + regression suite. Closes `HRTH-SEC-0142`, `-0144`, `-0147` in v1.1. |
| **Industrial Designer / Mech Eng** (Hire 5) | v1.2 Extender v2 + v2.0 charcoal+brass | Month 8 (2027 Q3-Q4) | Owns the enclosure through v1.0 GA polish, ships Extender v2 form factor for v1.2 (2028 Q1), lands charcoal + brass finish family for v2.0. |
| **Head of Security** (non-founder-narrative but load-bearing) | v1.0 + v1.1 | Recruited by CTO within 90 days of month 3, so 2027 Q3 land | Owns seven-class egress ACL commitment. Runs Trail of Bits audit. Owns HackerOne launch. Publishes redacted findings summary 2027 Q3. |
| **Advisor board seats 1-5** (`FOUNDER-NARRATIVE.md` §6) | v1.0 pilot credibility + Series B narrative | Filled within 180 days, all seated 2027 Q3 | Luxury hardware operator closes VoC Theme 5. Integrator channel authority closes Theme 2 + Obj 7. Family-office / RIA closes Theme 7 peer-proof. Privacy/security (retired FBI cyber leadership) closes Theme 1 + Obj 20. Audiophile press closes Interview 6 + 14 + Theme 4. |

**Team ramp by version.**
- **v1.0 pilot delivery (2027 Q2):** CEO + CTO + Head of Mfg Ops + Head of Customer Success + 3 SOW contractors held over. 7 people.
- **v1.0 GA (2027 Q4):** + Firmware/Systems Eng + Industrial Designer + Head of Security. 10 people. Advisor board seated.
- **v1.1 (2027 Q3):** same 10, running v1.1 as OTA on 10 pilot units.
- **v1.2 (2028 Q1):** ~14 (Head of Voice/Embedded, +1 mobile eng for multilingual, +1 concierge specialist per 100 units).
- **v2.0 (2028 Q4):** ~22-28 per founder-narrative "no more than thirty at scale." COO hire lands between v1.2 and v2.0 (2028 Q2) to take Mfg + Customer Success reporting from CEO.

---

## 9. What is explicitly OUT of scope through v2.0

Customers ask; concierge and sales script say no in the same words.

- **Video calls (Zoom / FaceTime) as a Hearth feature.** Customer's existing devices already do this. Adding it means persistent third-party dependency and bandwidth commitment we do not want. "Hearth is not a videoconference endpoint; that's what your phone is for." Permanent non-goal.
- **Third-party ad-supported free tier.** Ads require telemetry; telemetry breaks the offline claim. Permanent non-goal per `ROADMAP.md` and `THREAT-MODEL.md` §1.
- **Cellular fallback / eSIM.** Named in `THREAT-MODEL.md` §1.6 and §4.2. Permanent.
- **Enterprise / SMB variant.** Family-office channel (Interview 23) requires ISO 27001, SOC 2 Type II, EU legal presence, 24-hour named-engineer support — a $10M+ org build, not a product feature. Deferred past v2.0, separately budgeted at Series B. When asked: "we sell the household appliance to a family office as a household appliance; we cannot clear procurement at institutional scale until Series B closes the enterprise motion."
- **Rent-to-own / financing.** Not until Series B. Consumer financing on a $95k appliance requires a lending partner (data-sharing surface) or in-house AR (P&L change). Both are v3 conversations.
- **Non-US shipping.** None through v1.1. v1.2 adds Canada + UK + Germany + France in 2028 Q1 (aligned with multilingual STT/TTS). Middle East and Asia deferred to v2.0+ per Interview 23 walk-away analysis. "Rest of world" is not scoped in this roadmap.
- **Voice interface for kids under 12.** COPPA hazard — collecting biometric voice enrollment from a minor triggers verifiable-parental-consent requirements not compatible with the offline architecture (no consent-verification server to route through). Mitigation: households with children under 12 can enroll a "family voice" that any child speaks into with a parent-supervised session, but there is no per-child voice profile. Documented in Concierge SOP and local UI. Permanent non-goal.
- **Third-party voice assistants (Alexa / Google Assistant / Siri) as skills.** Would require phoning home. Permanent non-goal.
- **Automatic firmware push without opt-in.** Critical security hotfixes are the exception per `THREAT-MODEL.md` §8 — customer can pause with a UI setting but a persistent banner remains. Non-critical updates require opt-in.

---

## 10. Roadmap-to-pitch reconciliation

Cross-reference from `SHARK-TANK-REHEARSAL.md` objections to the roadmap version that answers each. This is the section the founder reads before every partner meeting.

- **Obj 1 (Who buys this? / $95k for a smart speaker):** v1.0 pilot delivery to Newport Beach, Palm Beach, Aspen, Nashville. The peer-proof set VoC Theme 7 says wins the sale is *manufactured* in v1.0 Q2-Q3 2027. Every Series A partner meeting after 2027 Q3 quotes a pilot customer by name (with consent).
- **Obj 2 (Valuation on zero revenue):** v1.0 pilot delivers deposit revenue $285k in 2027 Q2, GA revenue at 200 × $95k = **$19M** through 2027 Q4. Answer real Q4 2027.
- **Obj 3 (Solo founder):** Hire 1 (CTO), Hire 2 (Mfg Ops), Hire 3 (Customer Success) all land 2027 Q2. At pilot delivery, founder is CEO of a 7-person team + advisor board. Objection closed by month 4 post-close.
- **Obj 4 (Why offline is better) + Obj 20 (Trust the offline claim):** v1.1 (2027 Q3) ships Trail of Bits redacted summary + HackerOne bounty. Mechanical instruments of the offline promise — see `THREAT-MODEL.md` §10 four-legs answer. Every version after v1.1 preserves this and adds no telemetry endpoint.
- **Obj 5 (Amazon/Apple could copy this):** v2.0 (2028 Q4) 32B LLM + on-device video generation is the specific capability expensive-and-hard-for-the-clouds-to-replicate. The moat is *LLM + household archive + offline commitment* — cloud incumbents structurally cannot ship the third.
- **Obj 6 (Show me a paying customer):** v1.0 pilot. From 2027 Q3 forward, the answer is a specific customer's name and delivery date with signed case-study consent.
- **Obj 7 (CAC):** Integrator channel established in v1.0 Q2-Q3 by Head of Customer Success. VoC Theme 2 integrator dependency honored. Answer real by 2027 Q4.
- **Obj 8 (Margin at $95k):** `BOM` §5 — 48.4% hardware GM, 23.4% contribution — stable across v1.0/v1.1/v1.2. v2.0 hardware refresh with volume-driven NRE amortization targets 55%+ hardware GM.
- **Obj 9 (Halbach — gimmick or feature):** Every version of this roadmap explicitly says "OLED sphere face levitates; compute stack does not." Any founder or team-member who says otherwise is corrected in the same session. Permanent script commitment.
- **Obj 10 (PowerPoint not factory):** v1.0 first-article at Sanmina Fremont 2027 Q2 (10 units) and Foxlink Vietnam PVT 2027 Q3 (200 units through Q4). "Come see the line — I'll fly you up" is a real invitation from 2027 Q2 forward.
- **Obj 11 (Provisional patents only):** Non-provisionals convert 8 months post-Shark-Tank close, ~2027 Q2. From v1.0 pilot forward, answer is "granted patents, priority backed by provisional."
- **Obj 12 (Warranty burden):** 3-year concierge warranty per §2, $2,618/unit reserve (`BOM` §5.2), Chubb $10M/$2M bound before first-unit ship. Answer real at v1.0 delivery.
- **Obj 13 (Schoolteacher pitching hardware):** Hire 1 (CTO) at 2027 Q2 changes founder profile from "solo teacher" to "CEO + CTO from Nvidia Jetson / Meridian / Steinway Lyngdorf." Credibility real at pilot delivery.
- **Obj 14 (Kevin's hobby):** Same as Obj 2 + 6 — v1.0 GA at $19M revenue 2027 Q4 is not a hobby.
- **Obj 15 (Exit path):** **v2.0 opens the acquisition target aperture.** Natural buyers at v1.0 are Savant / Crestron / Control4 (`FOUNDER-NARRATIVE.md` §3d). At v2.0 the 32B LLM + video generation + trade-in program + refurbishment channel positions for a broader strategic set — Framework, European luxury AV group with a family-office consumer arm, or a privacy-focused strategic (Signal-affiliated, Proton, DuckDuckGo consumer hardware). Roadmap moment where the exit conversation opens.
- **Obj 16 (Thermals):** v1.0 envelope validated at Phoenix summer field trial 2027 Q3 before GA. Real data by 2027 Q3.
- **Obj 17 (38 TB storage yield):** `BOM` line 4 is Kioxia CD8-R at published enterprise capacity; Solidigm D5-P5430 drop-in. Storage stable across versions.
- **Obj 18 (Home Assistant is free):** v1.2 ships HA bridge (2028 Q1). Pivot from "we compete with HA" to "we integrate with HA." At v1.0 pilot the answer is Interview 4's — "my customers have never heard of HA." At v1.2: "our customers who *have* heard of HA install our bridge and keep it."
- **Obj 19 (Spouse says no):** VoC Theme 4 industrial design honored across versions. v1.0 walnut + brushed nickel; v2.0 adds charcoal + brass. Design lead ships by month 8 (2027 Q3-Q4). Spouse-approval story real from v1.0 delivery.
- **Obj 21 (LTV):** **v2.0 60% trade-in program (2028 Q4)** operationalizes "blended three-year LTV about a hundred twelve thousand." Before v2.0: $95k unit + Concierge + household integrations. At v2.0: $95k initial + $57k trade-in at year three + Concierge across both = ~$180k over 5 years, with concierge-fleet loaner economics offsetting.
- **Obj 22 ($10M revenue year three):** v1.0 GA 2027 Q4 (200 units) = $19M year one of shipping. Year three (2029) v2.0 volume ~800-1,000 units = ~$76-95M. Answer at Series A meetings 2027 Q1: "we're not at $10M year three, we're at $19M year one."
- **Obj 23 (3 more rounds trap):** Series A funds v1.0 through v1.2 (2027 Q1 through 2028 Q1). Series B closes 2028 Q2-Q3 to fund v2.0 hardware refresh + enterprise motion groundwork. Answer real at Series A close 2027 Q1.
- **Obj 24 (Kevin's $2M for 30%):** Roadmap-independent. See `SHARK-TANK-REHEARSAL.md` §4(h).
- **Obj 25 (Not for me):** Roadmap acknowledges walk-away segments in §9 non-goals. Founder does not chase Interview 21, 22, 23 profiles at any version. VoC §5 objection-25 rewrite ("who won't you sell this to?") is grounded in a specific set of non-goals with specific version rationales.

---

*End of Hearth 12-24 Month Product Roadmap v1.0.*

*This document supersedes ambitions previously expressed only verbally in Shark Tank rehearsal and diligence. It does not supersede the engineering `ROADMAP.md`, which owns EVT/DVT/PVT sequencing and remains the ground-truth source for manufacturing dates. This document owns customer-facing version identity (v1.0 / v1.1 / v1.2 / v2.0); the engineering document owns manufacturing gates (EVT / DVT / PVT). Where a milestone appears in both, they reconcile in the same PR that moves it.*

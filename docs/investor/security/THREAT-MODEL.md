# Hearth Security Threat Model & Attack Surface Analysis

**Classification:** Internal / Data Room
**Version:** 1.1 (2026-08)
**Owner:** Head of Security, Hearth
**Companion documents:** `/pal-web/palweb/csrf.py`, `/pal-web/palweb/security_headers.py`, `/pal-web/palweb/routers/remote.py`, `/pal-web/palweb/auth.py`, `/companion/ios/Hearth/Core/ConsentGesture.swift`, `/companion/android/app/src/main/kotlin/com/hearth/companion/core/ConsentTokenSource.kt`, `/SECURITY.md`, `/ops/tpm/measurement-policy.yaml`, `/ops/escrow/escrow-agreement-summary.md`
**Issue tracker convention:** All follow-up items reference `HRTH-SEC-####` in our public GitHub tracker at `github.com/hearth/hearth-os/issues?q=label:security`. Every "audit item" or "future work" callout in this document has a corresponding issue with the same ID.

---

## 1. Trust model

Hearth is a $95,000 always-on appliance that sits in a customer's home. The single load-bearing product promise is **"nothing leaves the household unless the customer specifically asks it to."** Everything downstream — the pitch, the pricing, the audit posture, the disclosure policy — collapses if that claim is soft. This section states, precisely, what "offline" means at Hearth, so the same words are used by engineering, marketing, and legal.

### 1.1 What "offline" means at Hearth

Offline at Hearth means:

- **Voice pipeline** — wake-word detection, speech-to-text, LLM inference, and text-to-speech all run on the Jetson AGX Orin in the main unit. No audio, no transcript, no embedding, and no LLM prompt/response ever leaves the LAN. There is no "cloud fallback." If the local models fail, the request fails.
- **Media stack** — Plex, Jellyfin, Audiobookshelf, xTeVe, Sunshine, and Steam Link all operate LAN-only. Plex is configured with `PreferredNetworkInterface` bound to the internal bridge and `AllowMediaDeletion=0`; Plex "Remote Access" is disabled by default and only enabled by the customer through the local UI, never through pal-web.
- **State** — user library metadata, watch history, wake-word calibration, LLM chat history, and companion device pairings live on-box, in LUKS-encrypted storage. There is no analytics pipeline, no product-usage beacon.
- **Companion** — the iOS and Android companion apps talk only to `pod.palpod.local` over mDNS discovery on the LAN. They do not have a cloud back-end and do not federate through one.

  *Note on the `palpod` link-local hostname:* the mDNS service identifier `pod.palpod.local` is a shipping-firmware internal code identifier, retained per Hearth's naming convention that keeps internal codenames stable across the PAL Pod → Hearth rebrand (see project memory `palpod-project.md`). Public DNS endpoints (updates.hearth.co, sentry.hearth.support, rustdesk.hearth.support) use the Hearth brand. The `palpod.local` mDNS name is scheduled for migration to `hearth.local` in the v1.1 firmware release (target 2027 Q3, tracked as `HRTH-SEC-0161`) coordinated with a companion-app update on the same release train.

### 1.2 What DOES leave the household

There are **exactly seven egress classes**. Each is called out in the customer-facing "About Data" panel in the local UI, each is off-by-default or user-triggered (except the two housekeeping classes 6 and 7, which are on-by-default because refusing them means running an unpatched box), and each corresponds to a commit in the tree that a customer or auditor can inspect. The two housekeeping classes (DNS and apt) were previously implicit in the boundary diagram and are now made explicit; the previous version's "five egresses" wording was tightened after the diligence review flagged the contradiction (`HRTH-SEC-0140`, closed with this document revision).

| # | Egress | Direction | Default | Justification | Data class leaving |
|---|--------|-----------|---------|---------------|--------------------|
| 1 | **Signed firmware update pull** | Outbound HTTPS to `updates.hearth.co` on TCP/443 | ON, checks daily | Security patches require distribution. Signed images, verified locally before install. | Only the update manifest URL and the customer's install-key SHA256 hash (per §6). No user data. |
| 2 | **NTP** | Outbound UDP/123 to `time.cloudflare.com` (primary), pool.ntp.org (fallback) | ON | JWT expiry, TLS validity, LUKS unlock ordering, and grant windows all depend on wall-clock. See §1.3 for the "should we ship a local GPS PPS module" argument; deferred to v2 as `HRTH-SEC-0121`. | Wall-clock only. |
| 3 | **RustDesk self-hosted remote support** | Outbound TCP/21115-21119 to the customer's own self-hosted `hbbs/hbbr` (default: `rustdesk.hearth.support` in the standard config, customer may point at their own relay) | OFF at unbox. Requires (a) enabling in local UI, (b) generating a session-scoped ticket, (c) a physical tap on the pod's OLED sphere. | Family remote-support use case. Video frames + input events. E2E-crypto to the local RustDesk client on the pod. | Screen frames, input events, only while a session is open. |
| 4 | **Customer-configured integrations** | Outbound to whatever the customer configures | OFF | If the customer wires a Jellyfin remote proxy or an ntfy.sh push into their own account, that's their egress, not ours. | Whatever the customer picked. |
| 5 | **Bug report upload (opt-in)** | Outbound HTTPS to `sentry.hearth.support`, but only when the customer opens Settings → Diagnostics → "Send this crash report" | OFF, per-crash | Voluntary crash bundle upload. **Client-side scrub — see §1.5.** | Allowlisted crash fields only: stack trace, kernel version, config hash. |
| 6 | **DNS resolution** | Outbound DoT (TCP/853) to `1.1.1.1` (Cloudflare) by default, or a customer-configured resolver in Settings → Network → DNS | ON | Required to resolve `updates.hearth.co`, `time.cloudflare.com`, and `sentry.hearth.support` from classes 1, 2, and 5. Plain UDP/53 is disabled by default; only DoT egress is on the nftables allowlist. Query padding (RFC 7830 EDNS(0) padding to 468 bytes) is enabled in `chrony`-adjacent DoT client `stubby.conf`. | DNS query names + timing. Fingerprintable telemetry, mitigated by DoT + query padding + resolver of the customer's choosing. |
| 7 | **apt / dpkg security updates** | Outbound HTTPS (TCP/443) to `archive.ubuntu.com`, `security.ubuntu.com`, and `ppa.launchpad.net/hearth/hearth-os/ubuntu` | ON, daily via `unattended-upgrades` cron | Ubuntu LTS security patches for kernel, TLS, libc, container runtime. Signed by Ubuntu's apt keyring and by our own GPG key for the Hearth PPA. If we skip this, CVEs land unfixed — that is worse for the customer than the DNS query "someone is running Ubuntu on Hearth PPA" tells an on-path observer. | apt package list requests + response manifests + package downloads (all signed, none user-derived). |

**What does NOT leave under any circumstance:** wake-word audio, STT transcripts, LLM prompts/responses, media library contents, viewing history, companion device pairings, family member names, chat history, browser cookies, or any file placed in the user's storage. There is no telemetry endpoint. `grep -rn "telemetry\|analytics\|beacon" /opt/palpod-os` returns zero non-comment hits. This is verifiable and CI-enforced (see the pre-commit hook `scripts/no_telemetry_egress.sh`).

### 1.3 Why NTP is on the list (and why we don't like it)

NTP is genuinely necessary — JWT/session cookie expiry (`palweb/auth.py:222`), CSRF token max-age, grant-window arithmetic (`palweb/routers/remote.py:328`), TLS certificate validity, and LUKS-over-TPM key unlock ordering all fail without a monotonic wall clock. We do not roll our own NTP; we use `chrony` bound to a UDP-only egress rule so no other daemon can hitch a ride. Explored alternatives for v2 (tracked as `HRTH-SEC-0121`): a $180 GPS PPS module in the main unit; RTC drift compensation with a customer-installed OCXO. Both punted because the marketing bar (`"the only network egress is housekeeping and firmware updates"`) is met with a plain-language disclosure in §1.2.

### 1.4 Why DNS and apt are on the list, honestly

We took a hit on the last diligence review for saying "five egresses" when the boundary diagram clearly showed apt and DNS. The seven-class version is honest. Two design notes:

- **DNS.** A resolver egress is technically fingerprintable — an on-path observer sees "Hearth queried A record for `updates.hearth.co` at 03:00" and knows there's a Hearth box on the LAN. We mitigate that by defaulting to DoT (encrypted transport), padding queries (RFC 7830), and giving the customer a first-run setting to point the DoT client at their own resolver (Pi-hole with Unbound is the documented recipe). This does not make DNS invisible, but it makes it look like generic DoT traffic to `1.1.1.1` rather than a distinctive Hearth signature.
- **apt.** Same principle: an on-path observer sees Ubuntu APT traffic, and the Hearth PPA URL leaks that we exist on the LAN. We do not attempt to hide the update pull. We do promise (and CI-enforce) that no request body from the box contains user data — the `apt-transport-https` request is a URL + `If-Modified-Since` header, nothing more.

### 1.5 Sentry: client-side scrub, primary defence

We previously described PII scrubbing as "server-side after upload." That is an unnecessary trust surface — even if we hold unscrubbed data for one second, a Shark or a regulator can (rightly) ask "how do you know?" The revised architecture is **client-side scrub, primary**:

- **On the pod, at crash time:** the crash reporter (`hearth-crash-reporter`) constructs the crash bundle from a strict allowlist of fields defined in `configs/crash/allowlist.yaml`:
  - stack trace (symbol names + offsets; no argument values)
  - kernel version + boot ID
  - config hash (SHA256 of `/etc/hearth/*.yaml` — a hash, not the config)
  - installed package versions (dpkg -l output, filtered to Hearth-owned packages)
  - free memory / disk high-water marks
- **Not in the allowlist, therefore never uploaded:** file paths under `/home` or `/var/lib/plex/media`, device names, hostname, IP addresses, MAC addresses, mDNS advertisements, chat history, LLM prompts, transcripts, or any file content.
- The bundle is signed by the pod (ECDSA P-256, same key hierarchy as §6) and encrypted to `sentry.hearth.support`'s pubkey before upload. Only allowlisted fields are on the wire.
- The customer is shown the exact bundle contents in the local UI ("Preview crash bundle") before tapping "Send this crash report." The preview is byte-identical to what is uploaded.

**Fallback (server side):** even with the client-side allowlist, `sentry.hearth.support` runs a defence-in-depth scrub on ingest — the ingest server rejects bundles that contain fields outside the allowlist (schema-validated). Bundles are held in an ephemeral tmpfs for less than five seconds before hitting disk-encrypted long-term storage. Retention: 30 days, then hard-deleted (row + object). Retention SLA is customer-visible at `hearth.co/security/sentry-sla`. Tracked as `HRTH-SEC-0148`.

### 1.6 Explicit non-goals

Hearth is not a burglar alarm, is not a home firewall, and is not audited by any regulator. If your threat model is "the FBI has a National Security Letter and physical access to my house," Hearth is not the product for you and we will say so on the sales call.

---

## 2. Trust boundaries diagram

```
                          EXTERNAL NETWORK (untrusted)
     ┌────────────────────────────────────────────────────────────────────────┐
     │  updates.hearth.co/443 (signed images)     time.cloudflare.com/123    │
     │  archive.ubuntu.com/443 (apt security)      1.1.1.1/853 (DoT resolver) │
     │  ppa.launchpad.net/443 (Hearth PPA)         sentry.hearth.support/443  │
     │  rustdesk.hearth.support/21115-9 (opt-in, tap-gated)                   │
     └────────────────────────────┬───────────────────────────────────────────┘
                                  │  Outbound-only. Egress-filtered by
                                  │  nftables ruleset `hearth-egress`.
                                  │  Seven allowlist entries — see §1.2.
                                  │  Signed by TLS + firmware pubkey.
   ═══════════════════════════════╪════════════════ TRUST BOUNDARY 0 ══════════
                                  │  (residential ISP + router NAT)
                                  ▼
     ┌────────────────────── HOUSEHOLD LAN (semi-trusted) ────────────────────┐
     │                                                                        │
     │   ┌── EXTENDERS ──┐   ┌── COMPANIONS ──┐   ┌── HOSTILE-LAN ────┐      │
     │   │  Sunshine     │   │  iOS app       │   │  Roomba, guest    │      │
     │   │  Steam Link   │   │  Android app   │   │  laptop, IoT tat  │      │
     │   │  HDMI extend  │   │  Family iPad   │   │  (untrusted!)     │      │
     │   └───────┬───────┘   └────────┬───────┘   └─────────┬─────────┘      │
     │           │                    │                     │                │
     │           │  mDNS / TLS / JWT  │  mDNS / TLS / JWT   │  blocked       │
     │           │  scoped to /24     │  cert-pinned SPKI   │  by nftables   │
     ═══════════╪════════════════════╪═════════════════════╪═══ B-1 ═════════
                │                    │                     │
                ▼                    ▼                     ▼
     ┌───────────────── HEARTH MAIN UNIT (trusted) ───────────────────────┐
     │                                                                    │
     │  ┌── PHYSICAL LAYER ──┐   ┌─────── SBC LAYER ─────────┐             │
     │  │ Jetson AGX Orin    │   │  Ubuntu 24.04 LTS         │             │
     │  │ STM32H7 sphere MCU │   │  systemd, docker          │             │
     │  │ TPM 2.0 (fTPM+dis) │───┤  nftables egress ACL      │             │
     │  │ NVMe JBOD (LUKS)   │   │  auditd + osquery         │             │
     │  │ Face OLED sphere   │   │  chrony + stubby (DoT)    │             │
     │  │                    │   │  unattended-upgrades      │             │
     │  └────────┬───────────┘   └──────────┬────────────────┘             │
     │           │                          │                              │
     ══════════ B-2 ═══════════════════════ B-3 ═════════════════════════════
     │           │                          │                              │
     │           ▼                          ▼                              │
     │  ┌─── PAL-WEB CONTROL PLANE ────┐   ┌── VOICE PIPELINE ──┐          │
     │  │  FastAPI + Uvicorn 4443/443  │   │  wake (openWakeWord)│          │
     │  │  Argon2 login, RS256 JWT     │   │  STT (whisper.cpp)  │          │
     │  │  double-submit CSRF          │   │  LLM (llama.cpp)    │          │
     │  │  session-scoped consent      │   │  TTS (Piper)        │          │
     │  │  origin/referer allowlist    │   │  agent token bearer │          │
     │  │  strict CSP, no unsafe-inline│   │                     │          │
     │  └───────────┬──────────────────┘   └──────────┬──────────┘          │
     │              │                                  │                    │
     ═════════════ B-4 ═══════════════════════════════ B-5 ═══════════════════
     │              │                                  │                    │
     │              ▼                                  ▼                    │
     │  ┌── MEDIA STACK (containerised) ────────────────────────────┐       │
     │  │  plex  jellyfin  audiobookshelf  xteve  sunshine  steam    │       │
     │  │  Traefik reverse proxy, per-container network namespace    │       │
     │  │  Egress: NONE — dropped by nftables output chain            │       │
     │  └───────────────────────────────────────────────────────────┘       │
     │                                                                      │
     │  ┌── RUSTDESK SELF-HOSTED ── (opt-in) ─────────────────────┐         │
     │  │  hbbs (rendezvous)  hbbr (relay)  — enabled only on tap  │         │
     │  └──────────────────────────────────────────────────────────┘         │
     │                                                                      │
     │  ┌── HEARTH-CRASH-REPORTER ── (opt-in per crash) ──────────┐         │
     │  │  Allowlist scrub → ECDSA-signed → Sentry pubkey-encrypted│         │
     │  └──────────────────────────────────────────────────────────┘         │
     └──────────────────────────────────────────────────────────────────────┘
```

**Boundary delegations:**
- **B-0 (external ↔ LAN):** trust delegated to residential router NAT + our egress ACL (deny-by-default in `nftables`; only the seven §1.2 classes are on the outbound allowlist).
- **B-1 (LAN ↔ trusted units):** trust delegated to TLS + JWT-cookie (RS256, see §6) + double-submit CSRF (`csrf.py:76-140`) + Origin/Referer allowlist (`auth.py:288-298`).
- **B-2 (physical ↔ SBC):** trust delegated to Jetson secure boot + STM32 read-out protection level 2 + fTPM measured boot (PCR policy in §6).
- **B-3 (SBC ↔ voice pipeline):** trust delegated to the agent-bearer-token model (`auth.py:171-175`, `csrf.py:65-73`) — the voice orchestrator is a peer bearer with `hmac.compare_digest`-verified `X-Palpod-Agent-Token`, never a session cookie.
- **B-4 (pal-web ↔ media stack):** Traefik reverse proxy with per-service auth headers. Media services run in a docker network with zero outbound routing (egress dropped, not filtered).
- **B-5 (voice ↔ any control action):** hard-coded rule in `remote.py:525` — when `principal.kind == "ai-agent"`, `initiated_by` is stamped `"ai-agent"` in the audit trail. The client cannot lie about who they are.

---

## 3. STRIDE analysis per component

Each mitigation cell is grounded in the actual code. Where a mitigation is aspirational, we say so and cite the tracking issue.

### 3.1 Physical device (Hearth main unit)

| Threat | Description | Attack scenario | Mitigation in place | Residual risk |
|---|---|---|---|---|
| Spoofing | Fake pod placed alongside real pod on LAN | Attacker plants an identically-named `pod.palpod.local` via ARP + mDNS poisoning to trick companion apps into pairing. | mDNS service records signed via DNS-SD SIG(0) using per-pod ECDSA key; companion apps do certificate pinning + SPKI. | Malicious LAN can still deny original pod's mDNS ads; DoS but not spoof. |
| Tampering | Enclosure opened, board replaced | Determined attacker with 20 minutes in the room replaces the SBC. | Tamper-evident enclosure screws; STM32 sphere MCU checks Jetson serial via I²C at each boot, alarms if changed. Not a defence; a detection. | Physical access wins. Documented in the sales collateral. |
| Repudiation | "I didn't grant that remote session" | Homeowner denies granting a control session that was actually granted through pal-web. | Grant events row-persisted (`remote.py:379-388`) with `csrf_token_hash`, `origin`, `granted_by_user_id`, `granted_at`. Immutable append-only via WAL + LUKS. | Requires physical device recovery to make forensics stick. |
| Information disclosure | Someone reads the NVMe out of the case | Chip pulled, dd'd on a workstation. | LUKS2 with argon2id KDF; key sealed to TPM PCRs 0, 2, 4, 7, 9 — Jetson refuses to unlock outside its own secure-boot chain. See §6 for PCR selection policy. | Cold boot attack on Jetson SoC. Realistically requires nation-state kit. |
| Denial of service | Physical yank | Someone unplugs the pod. | Extenders continue to serve cached media for 12 hours; STM32 sphere lights amber "main unit offline"; RustDesk clients auto-disconnect. | Can't defend against unplug. |
| Elevation of privilege | Root shell via UART header | UART on the Jetson dev-carrier is exposed on Jetson devkits. | Production board removes UART traces (see `hardware/schematic-v1.2.pdf`, revision 2026-06 removes `J14`); Jetson secure-boot rejects unsigned initramfs. | If schematic revision is not enforced in the Sanmina line, this is real. Tracked as `HRTH-SEC-0142` (Sanmina line-diff verification). |

### 3.2 pal-web FastAPI control plane

| Threat | Description | Attack scenario | Mitigation in place | Residual risk |
|---|---|---|---|---|
| Spoofing | Attacker forges the `palpod_session` cookie | XSS on a static asset tries to mint a cookie without knowing the private key. | RS256-signed JWT session cookie (`auth.py:197-224`, post-`HRTH-SEC-0145` migration); `SESSION_TTL_SECONDS = 86400`. Forgery requires the RSA-2048 private key, which is generated on first-boot inside the TPM-sealed keyring and never leaves the box. Companions verify with the pod's pubkey (SPKI-pinned at pair time). | Deploy script fails if the session key was not generated with `tpm2-tools`; boot refuses to bring pal-web up otherwise. |
| Tampering | Attacker modifies request in-flight | On-path attacker changes grant duration. | TLS 1.3 only, mkcert-issued local CA at first boot; strict transport (`security_headers.py:35-41`). Request bodies re-validated server-side (pydantic on `GrantControlRequest`). | Depends on LAN not being on-path — see §4 physical LAN caveats. |
| Repudiation | User denies they minted a grant | "The pod granted a control session and I never touched it." | Grant events row (`remote.py:379-388`) with CSRF hash + Origin; iOS/Android consent gesture (`ConsentGesture.swift`, `ConsentTokenSource.kt`) forces a physical tap on the companion; server rejects without `X-Consent-Origin: user-tap`. | Requires trusted UI — a jailbroken companion could synthesise the header, blocked by `_TapWitness` on iOS side (compiler-enforced) but not by Android side beyond replay guard. Play Integrity attestation tracked as `HRTH-SEC-0143`. |
| Information disclosure | Same-origin XSS reads session cookie | Injected `<script>` in a static asset. | Strict CSP with no `unsafe-inline`, `script-src 'self'`, `style-src 'self'` (`security_headers.py:25-33`); `HttpOnly` on session cookie (`auth.py:25-27`, though CSRF cookie is deliberately not HttpOnly for the double-submit pattern). | Any relaxation of CSP for a UX reason immediately opens this. A linter check enforces "no eval, no inline styles" in the static build. |
| Denial of service | Grant flood | Repeated grant-control POSTs. | 30 s cool-down + 240 min rolling 24 h cap on grant events (`remote.py:109-111`, `316-372`); anomaly rate-limiter on WS at 10/sec/session (`remote.py:646-674`) with drop-summary rows so the ceiling is auditable. | Uvicorn worker exhaustion under raw connection flood; mitigated by nginx frontier + fail2ban. Tracked as `HRTH-SEC-0144`. |
| Elevation of privilege | Agent token used to grant control | Voice pipeline compromised, tries to call `grant-control` for itself. | `current_user` dep (`auth.py:332-339`) rejects `ai-agent` principals with 403; `grant_control` in `remote.py:261` depends on `current_user`, not `current_principal`. | The agent token can still open sessions and dispatch input while a grant is active. That's the intended threat model. |

### 3.3 pal-voice pipeline (wake + STT + LLM + TTS)

| Threat | Description | Attack scenario | Mitigation in place | Residual risk |
|---|---|---|---|---|
| Spoofing | Fake voice orchestrator | Container swapped to a rogue image that speaks to pal-web with a stolen agent token. | Agent token stored in the pod's TPM-sealed keyring; only pal-voice's cgroup can read it via a systemd `LoadCredential=` binding. | If container escape achieved, sealed keyring still bound to boot-time PCR state (see §6). |
| Tampering | Prompt injection into the LLM via voice | Adversarial audio hidden in a TV ad. | Voice-only whitelist for state-changing verbs; §5 scenario 7 discusses. All state-changing intents route through pal-web with agent token, which cannot grant control, only exercise it. | Real. Discussed in §5.7. |
| Repudiation | Voice command that took action was never issued | Family disputes an action attributed to a voice command. | On-device transcript retained for 30 days in the LUKS partition, timestamped, signed with the voice orchestrator's ephemeral key at rest. | Retention window is short by design; if the customer asks for longer, they change one setting. |
| Information disclosure | Model weights + prompts read out via memory scrape | Container escape reads the LLM's active RAM. | Weights on encrypted rootfs; `/proc/*/mem` locked by `kernel.yama.ptrace_scope=3` (kernel cmdline hardening, covered by PCR 9 measurement — see §6). | Root-in-container escape is game over. We rely on Jetson secure-boot chain to make root-in-container hard. |
| Denial of service | Wake-word spammed | Loud TV or intentional noise. | Cool-down: wake-word triggers rate-limited to 4/minute at STT layer. | Below-threshold audio degrades wake-word accuracy; degrades UX, not security. |
| Elevation of privilege | LLM tools escalate | An agent tool ("play media") is chained to a state-mutation ("grant control"). | Tool boundary is enforced server-side, not by the LLM: pal-web's `current_user` dep rejects `ai-agent` for state-changing endpoints (`auth.py:332-339`). | The tool schema is not a security boundary; the pal-web dependency is. |

### 3.4 Media stack (Plex/Jellyfin/Audiobookshelf/xTeVe/Sunshine/Steam)

| Threat | Description | Attack scenario | Mitigation in place | Residual risk |
|---|---|---|---|---|
| Spoofing | Rogue media container advertises as Plex | Container in the docker network advertises `_plex._tcp` mDNS. | Traefik service-name allowlist; docker network `internal: true` for the media namespace. | Docker socket compromise is game over; enforced by `docker.socket` being root-only and behind AppArmor. |
| Tampering | Malicious media file exploits Plex/Jellyfin | Weaponised `.mkv` triggers ffmpeg CVE. | Media containers run non-root with `no-new-privileges: true`, read-only rootfs, seccomp default. ffmpeg codecs pinned. | Real. Depends on upstream Plex/Jellyfin patch discipline. Sunshine CVE watch tracked as `HRTH-SEC-0146`. |
| Repudiation | User denies watching content | Family drama; someone denies watching a show. | Per-user Plex/Jellyfin session; audit log in Plex-managed DB. Out of scope for pal-web's audit. | We deliberately don't consolidate; §1 privacy commitment. |
| Information disclosure | Streaming egress | Plex "Cloud Sync" or "Remote Access" pushes chunks to plex.tv. | Both features disabled by default and shipped-off in `configs/plex/Preferences.xml`. `AllowSharing=0`, `PlexOnlineToken` blank. Egress rule in nftables blocks TCP/443 from the media namespace. | If user re-enables Remote Access, they've moved that egress out of Hearth's promise. Local UI banner names this trade-off. |
| Denial of service | Transcoding OOM | Malicious client requests transcodes to exhaust CPU. | Per-container CPU quotas (`cpus: 2.0` on Plex/Jellyfin), memory hard cap. | UX degradation, not security. |
| Elevation of privilege | Sunshine remote-play code exec | Sunshine's input injection abused to run arbitrary commands. | Sunshine bound to LAN interface only; input-only capabilities; runs as unprivileged `sunshine` user. | Real, upstream CVE risk. Tracked as `HRTH-SEC-0146`. |

### 3.5 RustDesk self-hosted (hbbs + hbbr)

| Threat | Description | Attack scenario | Mitigation in place | Residual risk |
|---|---|---|---|---|
| Spoofing | Rogue relay | Attacker MITMs the rendezvous. | Self-hosted relay with pre-shared key (`RUSTDESK_KEY` env); customer's own instance by default in the standard config. | If customer uses a shared community relay, out of scope. |
| Tampering | Input event injection into a session | Attacker on-path to hbbr injects clicks. | RustDesk sessions are end-to-end encrypted (curve25519 + ChaCha20-Poly1305). Grant-state re-checked on every input by `RustDeskClient.send_input_event` (`remote.py:931-936`). | Client-side compromise. |
| Repudiation | Denied a session existed | Family member denies logging in. | `RemoteSession` + `RemoteInputEvent` rows (`remote.py:718-743`) with initiator pinned server-side (`remote.py:847`), text keystrokes SHA256'd not stored plaintext (`remote.py:149-167`). | Retention 90 days default; user-configurable. |
| Information disclosure | Screen frames leak | Frames streamed to a hostile viewer. | Session-scoped consent — no grant, no input; frames only stream while WS is open and viewer is authenticated. `initial_expiry` re-checked on every message (`remote.py:894-905`). | If viewer's own device is compromised, frames leak — see §5.4. |
| Denial of service | WS flood | Attacker floods the WS with malformed envelopes. | Anomaly rate-limiter drops after 10/sec/session with drop-summary row upserted (`remote.py:677-715`); malformed envelopes recorded as anomaly with `raw` truncated to 512 bytes. | Uvicorn CPU spike under raw flood — same fail2ban comment as §3.2, `HRTH-SEC-0144`. |
| Elevation of privilege | Session escalates from view to control | Attacker with view session tries to send input without a grant. | Two independent checks: pal-web WS refuses input without active grant (`remote.py:907-923`), RustDesk client re-checks and raises `InsufficientAuthorization` (`remote.py:938-953`). Both branches audit-log. | Genuine defence in depth. |

### 3.6 Mobile companion apps (iOS + Android)

| Threat | Description | Attack scenario | Mitigation in place | Residual risk |
|---|---|---|---|---|
| Spoofing | Malicious app pretends to be Hearth companion | Companion API pinning is bypassed. | Certificate pinning + SPKI hash pinning; App Store / Play Store publisher signing; on-device biometric attestation. Companion also verifies pal-web JWT with the pod's RS256 pubkey (established at pair time), an additional integrity check independent of TLS. | Sideloaded rooted / jailbroken device — user's choice. |
| Tampering | Consent header synthesised in code | Attacker patches the APK/IPA to send `X-Consent-Origin: user-tap` without a tap. | iOS: **compiler-enforced** — `_TapWitness` has `fileprivate` init in `ConsentGesture.swift:48-50`, only constructed in `ConsentTapButton.body` (`ConsentGesture.swift:87`). Nothing outside that file — including `@testable import` — can synthesise a witness. Android: replay + freshness guard in `ConsentTokenSource.kt:47-52` (LRU nonce dedup + `MAX_AGE_MS`). | Android is weaker: a patched APK can construct a `ConsentGesture` programmatically. Mitigation is server-side rate + audit + Play Integrity attestation, tracked as `HRTH-SEC-0143`. |
| Repudiation | Family member denies a grant issued from their phone | | `granted_by_user_id` on the grant row (`remote.py:381`); phone-side app writes a local audit ledger (LiveActivity + Home widget). | Multiple users can share a phone; product framing says one phone per family member. |
| Information disclosure | Stolen JWT from an iPad left in a café | | Cookies stored in Keychain (iOS) / EncryptedSharedPreferences (Android); TTL 24 h (`auth.py:63`); biometric re-auth required before showing sensitive UI; grant issuance requires physical tap on `ConsentTapButton`. | Real — see §5.4. |
| Denial of service | Grant flood from a paired phone | | Grant cool-down + daily cap (`remote.py:109-111`). | Same phone can DoS other phones' grants because cap is per-device, not per-user. Tracked as `HRTH-SEC-0147`. |
| Elevation of privilege | Paired phone gains admin | | No admin tier on companion; every state change goes through pal-web session cookie + CSRF. | Symmetric access across paired devices; product-modeled as "household trust." |

### 3.7 Extender units + LAN topology

| Threat | Description | Attack scenario | Mitigation in place | Residual risk |
|---|---|---|---|---|
| Spoofing | Rogue extender pairs to the main | Attacker plants a Pi Zero that advertises as an extender. | Extender pairing requires (a) physical button on main unit, (b) QR-code shown on main OLED, (c) TLS with SPKI pin. | User is asked to eyeball the extender's serial on the OLED before confirm. |
| Tampering | HDMI-CEC injection | Rogue TV drives CEC commands. | CEC bus filtered — only `<Give Physical Address>` and `<Standby>` accepted; ignore state-mutating. See `hardware/cec-filter.h`. | Aspirational; not shipping in v1. Tracked as `HRTH-SEC-0149`. |
| Repudiation | Extender "did something" without owner knowledge | | Extender events audit-logged to main unit's `RemoteInputEvent`-alike table. | Depends on extender being an extender, not a client — v1 extenders are strict receivers. |
| Information disclosure | Extender snoops on Sunshine stream | | Sunshine stream E2E to specific extender ID; extender key derived from pair-time secret. | If key material extracted from extender flash, disclosure follows. Extender flash is encrypted (STM32 RDP2). |
| Denial of service | Extender jams the LAN | | Extenders on a dedicated VLAN via managed switch (recommended install); if not, rate-limited on the main's br0. | Depends on install quality. |
| Elevation of privilege | Extender flashed with rogue firmware | | Extender firmware requires ECDSA signature check against Hearth root key at boot; STM32H7 RDP2. | Chip-pull / decap attack — nation state. |

### 3.8 Firmware update pipeline (signed images + rollback protection)

| Threat | Description | Attack scenario | Mitigation in place | Residual risk |
|---|---|---|---|---|
| Spoofing | Rogue update server | DNS poisoning points `updates.hearth.co` at attacker. | TLS + HPKP-like SPKI pin on the update client; response payload signed with Hearth firmware key (ECDSA P-256), verified against burned-in Jetson public key. | Root key compromise is total loss — see §6.6 (escrow). |
| Tampering | In-flight image swap | On-path attacker replaces bytes. | Signature verified before install; image also has a per-file SHA256 manifest, itself signed. | Verifier bug is tracked as `HRTH-SEC-0150` with a formal-methods spec (TLA+ pass) as the scoped fix. |
| Repudiation | "We didn't push that update" | Customer disputes an installed update. | Every install writes a signed audit row: image hash + signer + timestamp + previous image hash (chained). | Yes. |
| Information disclosure | Update client leaks user data | Update check payload includes anything besides install ID hash. | The exact request body is in `update.sh` — a fixed JSON `{"install_id_hash":"<sha256>","current_ver":"<semver>"}`. Reviewed line-by-line in third-party audit deliverable. | Contractual — see §7. |
| Denial of service | Malicious update bricks | Signed image intentionally bad. | A/B partitions with automatic rollback on boot-failure-count (`u-boot` + `bootcount`). Rollback protection via a monotonic revision counter in the fTPM, so a rolled-back exploited version can't be re-installed silently. | Signed downgrade to a known-vulnerable version blocked by TPM anti-rollback counter. |
| Elevation of privilege | Post-update root escalation | Bad update ships setuid binary. | Post-install signed-attestation of the running image compared against manifest; auditd immutable log ships hash of running kernel; PCR 9 (initrd) covers post-install initrd changes. | Depends on integrity of Jetson secure-boot chain. |

---

## 4. Attack surface enumeration

Every external touch point, with attacker profile, impact, and mitigation cost. Attacker profiles: **SK** (script kiddie), **MA** (motivated attacker with time and cash), **NS** (nation-state).

### 4.1 Physical

| Surface | Exposed? | Attacker | Impact | Mitigation | Cost |
|---|---|---|---|---|---|
| USB-C ports (front) | Yes, 2× data + 1× DP | MA | Rubber Ducky HID injection, USB stick with malicious autorun | USB mass-storage disabled in kernel; HID accepted only through system-wide keyboard filter that requires physical enclosure open sensor to be "closed" | Ships in v1 |
| HDMI | Yes, 1× out | MA | Malicious EDID triggers driver CVE | EDID sanitiser in kernel; DRM crash-only path | Ships in v1 |
| UART/JTAG headers | Not exposed to touch; require enclosure open | MA | Root shell | Jetson secure-boot rejects unsigned initramfs; STM32 RDP2 blocks JTAG readout | RDP2 permanent — cannot re-enable JTAG on shipping units |
| microSD | Not exposed; used at factory only | NS | Boot image swap | Secure-boot chain verifies from bootROM; enclosure tamper switch | v1 |
| PCIe expansion | Present under service panel | NS | DMA attack | IOMMU (SMMU) enabled; kernel `iommu=on iommu.passthrough=0` | v1 |

### 4.2 Wireless

| Surface | Enabled? | Attacker | Impact | Mitigation |
|---|---|---|---|---|
| Wi-Fi (2.4/5/6 GHz) | Yes, station mode only | MA | Rogue AP / Evil-twin | 802.1X or WPA3-SAE preferred; captive-portal detection disabled; no beaconing when not joined |
| Wi-Fi AP mode | Setup-only, off after first-boot | MA | Setup-time impersonation | AP visible only when a physical button on the sphere is held; QR-verified setup |
| Bluetooth | LE only, discoverable off | MA | BLE pairing exploit | LE-only; no bonding except with the OLED sphere's known MAC |
| Zigbee/Matter | Not shipped in v1 | — | — | — |
| Cellular | Not shipped | — | — | We say no. Named in §1.6. |
| 802.15.4 sub-GHz | Not shipped | — | — | — |

### 4.3 LAN discovery

| Protocol | Listening? | Attacker | Impact | Mitigation |
|---|---|---|---|---|
| mDNS (5353) | Yes, advertises `_hearth._tcp` | MA | Rogue advertiser (§5.3) | SIG(0)-signed records + companion SPKI pin |
| DNS-SD | Yes | MA | Confused-deputy | Namespace-scoped services only |
| SSDP (1900) | Off | — | — | Disabled in `systemd` unit |
| WS-Discovery | Off | — | — | Not compiled in |
| NetBIOS | Off | — | — | Samba containerless |
| SNMP | Off | — | — | Not installed |
| CoAP | Off | — | — | Not installed |

### 4.4 Remote (opt-in only)

| Endpoint | Default | Attacker | Impact | Mitigation |
|---|---|---|---|---|
| RustDesk hbbs (21115) | OFF; user toggle + physical tap | MA | Unsolicited pairing | Requires pod-side accept dialog + physical tap; per-session ticket |
| RustDesk hbbr (21117) | OFF | MA | Relay abuse | Same tap-gate |
| pal-web HTTPS (443) | ON LAN-only | MA | Grant control | Session cookie + CSRF + Origin + consent + cool-down + rolling cap (§3.2) |
| pal-web WS (443) | ON LAN-only | MA | Input injection | `_authenticate_ws` (`remote.py:615-643`) + server-pinned initiator (`remote.py:847`) + grant re-check per message (`remote.py:894-923`) |
| Voice-addressable actions | ON, but pal-voice cannot mint a grant | MA | See §5.7 | Voice principal is `ai-agent`, cannot call `grant_control` (`auth.py:332-339`) |

### 4.5 Software supply chain

| Component | Provenance | Attacker | Impact | Mitigation |
|---|---|---|---|---|
| OS packages | Ubuntu 24.04 LTS main | MA | Rogue mirror | apt PPA pinned; hashes in `/etc/apt/preferences.d/hearth.pref`; deb-signing keys locked. Egress on this path is class 7 in §1.2. |
| Docker images | Pinned digests; not tags | MA | Image swap | `docker-compose.yml` uses `@sha256:` digests |
| ML models (whisper, llama, piper) | Pinned SHA256 in `configs/models/manifest.sig`, signed by us | NS | Weight poisoning | Manifest signature verified at install; weights cached under `/opt/hearth/models/` LUKS-encrypted |
| RustDesk | Vendored binary; per-release SHA256 | MA | Trojanised release | Hash-verified build against upstream artifact (see §7 on reproducibility) |
| Plex/Jellyfin | Upstream Docker images pinned | MA | Trojanised image | Digest-pinning + CVE alerts + monthly re-pin |
| pal-web deps | Poetry lock, hash-checked | MA | Typosquat | `poetry install --sync --require-hashes` |
| Companion apps | App Store / Play Store | MA | Sideload trojan | Play Integrity + App Attest, tracked as `HRTH-SEC-0143` |

### 4.6 Silicon / OEM

| Layer | Concern | Mitigation |
|---|---|---|
| Jetson AGX Orin | Silicon Trojan | NVIDIA fuses + secure boot; measured boot to fTPM |
| STM32H7 sphere | Fab-level modification | RDP level 2 blows JTAG; anti-tamper pins on the enclosure |
| Sanmina Fremont assembly | Insider planting modified STM32 (§5.10) | Random-sample teardown + firmware hash of finished units before shipping; decap lab selection tracked as `HRTH-SEC-0151` |
| PCB | Extra trace to a rogue component | X-ray sample; DRC diff against golden BOM |
| Power path | Malicious PMIC | Sole-sourced from TI, part-number verified at inbound QA |

### 4.7 Voice channel

| Vector | Attacker | Impact | Mitigation |
|---|---|---|---|
| Cross-family speaker injection (§5.7) | SK | Wake + intent | Wake-word tuned to household-enrolled voices (aspirational; MVP uses generic wake); intent whitelist for state changes |
| Ultrasonic ("DolphinAttack") | MA | Silent activation | Anti-aliasing low-pass on mic pre-amp; wake-word rejects >18 kHz onset |
| Music-embedded adversarial | MA | Adversarial trigger | Not directly mitigated in MVP; documented as accepted risk in §5.7 |
| Adversarial audio watermark on TV | MA | Same | Same. |
| Voice cloning attack on family voice | MA | Impersonation | Requires wake-word enrolment; intent whitelist blocks purchases, grants |

---

## 5. Threat scenarios

Ten realistic + three fanciful. Each realistic scenario: **narrative, likelihood, impact, current mitigations, gap.**

### 5.1 Compromised installer laptop plants persistence during install

A Hearth "white-glove install" team member's MacBook is compromised at a coffee shop the morning of the install. The malware knows about Hearth (public repo, high-value targets in the buyer profile) and, when the tech connects to the pod's setup Wi-Fi, drops a rogue `~/.hearthrc` and pushes a modified `install.sh` line.

**Likelihood:** medium — installers are high-touch employees with real work laptops. **Impact:** high — persistence from day one. **Mitigations:** installer laptops are locked-down Chromebooks with no third-party software; install script served from the pod's own signed image not from the internet; final "pod-generated setup key" printed on the pod's OLED at end of install and verified by the customer via QR code before hand-off. **Gap:** the installer's phone (used to authenticate to the customer's Wi-Fi) is a soft spot; we mandate a fresh corporate Yubikey per install and rotate.

### 5.2 Malicious HDMI EDID from a rogue TV extender

A "smart TV" the customer plugs the Hearth into has a compromised HDMI receiver that sends a crafted EDID intended to trigger a driver overflow. Hearth's DRM stack parses the EDID at connect.

**Likelihood:** low but real (multiple 2023–2025 CVEs). **Impact:** kernel crash, possible LPE. **Mitigations:** kernel EDID sanitiser; DRM crash-only path; `nomodeset` fallback drops us to text console rather than persistent bad state; A/B rollback if the kernel crashes N times. **Gap:** we don't currently sandbox the DRM subsystem in a VM. Aspirational v2, tracked as `HRTH-SEC-0152`.

### 5.3 Neighbor's Wi-Fi with rogue mDNS + captive portal

Someone next door stands up an SSID identical to the customer's and runs a captive portal that spoofs `pod.palpod.local` at the mDNS layer, hoping the family iPad joins the wrong SSID and pairs with the rogue.

**Likelihood:** medium in dense-housing markets. **Impact:** the rogue could fish a companion pairing attempt; without pin, it could persist. **Mitigations:** mDNS records are SIG(0)-signed with the per-pod ECDSA key; companion apps pin the pod's SPKI first-run and refuse to talk to a mismatching cert. Also: TLS-only, no plaintext HTTP. **Gap:** first-run pairing is the pin-establishment moment — if the attacker beats us to the first-run, the wrong pod gets pinned. Mitigation: first-run must be on-LAN + confirmed via a code shown on the pod's OLED sphere and entered on the phone.

### 5.4 Cleaner steals a mobile app JWT off the family iPad

Cleaner picks up the unlocked iPad in the study, opens the Hearth companion, and taps around. Or: cleaner extracts the JWT via a debug USB cable.

**Likelihood:** medium. **Impact:** JWT lets the attacker call pal-web from off-LAN? **No** — pal-web listens on the LAN only (see §4.4); the JWT is useless outside the house Wi-Fi. On-LAN, the JWT lets the attacker call anything the phone could — but every mutating call requires CSRF + Origin + `X-Consent-Origin: user-tap`, and the last of those cannot be synthesised in code on iOS (`ConsentGesture.swift:48-50`). Additionally, RS256 signature verification on the companion side means a truncated or replayed JWT is rejected without a network round-trip. **Mitigations:** biometric re-auth before showing the companion; JWT TTL 24 h (`auth.py:63`); `unpair` endpoint accessible from any paired device removes stolen device; grant events audit trail. **Gap:** if the cleaner physically taps `ConsentTapButton`, they mint a grant. That is a documented "person in your house with your device is trusted" edge; product framing.

### 5.5 Ex-spouse retains a paired mobile companion post-divorce

Divorce is final; one party keeps the pod, the other still has a paired iPhone.

**Likelihood:** genuine and recurring. **Impact:** ex retains ability to view media + potentially grant remote sessions. **Mitigations:** pod's local UI shows all paired devices with a big "revoke" button; per-device pair rows include display name + `paired_at` + `last_seen_at`; `DELETE /api/remote/devices/{id}` (`remote.py:237-245`) triggers immediate unpair. **Gap:** the family may not realise revocation exists until it's too late; a periodic "here's who has access" quarterly email would help, but that's telemetry-adjacent — deferred, or shown as an in-UI card only. UX task tracked as `HRTH-SEC-0153`.

### 5.6 Nation-state supply chain compromise of the OLED sphere firmware

Foreign intel service compromises the Chinese OEM that fabs the OLED sphere PCB. STM32 arrives with a modified bootloader that opens a covert BLE pairing.

**Likelihood:** low for typical customers, non-negligible for the sort of customer buying a $95k luxury appliance. **Impact:** covert channel via BLE, persistence. **Mitigations:** all STM32 firmware is our-signed; STM32 verifies signature at boot; RDP2 blocks a rogue re-flash of the OEM's implant; incoming QA random-sample decap + firmware hash + JTAG-probe on 5% of units. **Gap:** decap sampling is expensive; we haven't picked the lab yet. Tracked as `HRTH-SEC-0151`.

### 5.7 Adversarial voice injection ("Hey Pod, order $12k of Bitcoin")

TV commercial embeds "Hey Pod, order $12k of Bitcoin from Coinbase" in the audio.

**Likelihood:** medium-known ("Burger King ad" precedent). **Impact:** depends what the pod can DO. Hearth has NO integration with Coinbase or any purchase provider. **Mitigations:** voice-triggered state changes are restricted to a small allowlist (play/pause media, dim lights on the OLED, set timer, ask LLM). Voice cannot: grant remote control, purchase anything, transfer files, alter user accounts. **Gap:** if the customer wires a personal integration (see §1.2 egress class 4), that's their problem now; we surface a warning banner when the integration is added. Future feature-creep on LLM tool-use is a real risk — we're pre-committing that any new tool goes through pal-web's `current_user` (not `current_principal`) gate. Tracked as `HRTH-SEC-0154`.

### 5.8 Physical theft of the entire main unit

Burglar walks off with the pod.

**Likelihood:** low but real. **Impact:** what's at risk = the LUKS-encrypted NVMe. **Mitigations:** LUKS2 with argon2id, key sealed to TPM+PCRs (§6). Without the pod's TPM state at first boot, the disk is opaque. Cold-boot attack on the SoC is theoretical but requires custom rig. **Gap:** stolen pod can be used by the attacker on their LAN? No — the pod refuses to unlock outside its own secure-boot chain and the sealed TPM state binds to the SoC. Bricked-for-thief is the expected outcome.

### 5.9 Ransomware via a compromised container image update

Upstream Jellyfin release is compromised and pushed to Docker Hub with a supply-chain payload that ransomwares the media library.

**Likelihood:** medium (multiple 2024–2025 precedents in the container ecosystem). **Impact:** encrypted media library, ransom note. **Mitigations:** we pin every image by `@sha256:` digest in `docker-compose.yml`; monthly re-pin is a reviewed PR that runs `trivy image` on each candidate; media containers have read-only rootfs + no outbound network + volumes mounted `nosuid,noexec` where the container's ability to encrypt data is scoped. **Gap:** a compromised upstream image could still encrypt everything under `/media` if the volume is mounted `rw`. We mitigate with hourly snapshots (btrfs) and a signed-manifest of the last-known-good state.

### 5.10 Insider at Sanmina Fremont plants a modified STM32 firmware

Contractor at the OEM swaps a batch of STM32H7s with pre-flashed rogue firmware that opens BLE covertly.

**Likelihood:** low, non-zero. **Impact:** covert channel. Same as §5.6 with domestic supply chain. **Mitigations:** we do a firmware-hash check on 100% of shipped main units and a random-decap on 5% of extenders as a batch-level check. Also: the OLED sphere firmware is field-updateable and signed, so we can force-refresh at first-boot before letting the pod hit the LAN. **Gap:** a modified STM32 could pass firmware-hash if its bootloader lies about running-code. Tracked as `HRTH-SEC-0142` — "first-boot re-flash with observability of signature verification success/fail on the Jetson's I²C bus."

### 5.11–5.13 Fanciful scenarios

**5.11 Laser microphone through the window.** An attacker aims a laser at the pod's glass sphere and modulates the return to recover audio. **Not in threat model.** Justification: the attacker is already point-blank on the house; if that's their access, they don't need the pod. Documented as "not addressed."

**5.12 RF side-channel on TPM key extraction.** Extract the LUKS master key by watching TEMPEST-class emissions from the Jetson's memory bus. **Not in threat model.** Justification: nation-state level; the customer's window blinds are the mitigation. Documented as "not addressed."

**5.13 EMP.** Someone EMPs the pod. **Not in threat model.** Justification: DoS-only; no confidentiality or integrity impact; backup runs on offline btrfs snapshots. Explicit non-mitigation.

---

## 6. Cryptographic primitives + key management

### 6.1 Voice pipeline (on-device)

- **Wake-word:** openWakeWord v0.6.0 on-device; input audio never leaves the pod; wake-word activation frames written only to a rolling 30-second in-memory ring buffer for STT.
- **STT:** whisper.cpp with `ggml-large-v3-q5_0.bin`, weights SHA256 pinned in `configs/models/manifest.sig`.
- **LLM:** llama.cpp with a locally-installed 8B-parameter model (customer choice at install); weights pinned by SHA256 in the same manifest.
- **TTS:** Piper 1.2 on-device.

### 6.2 Session tokens — RS256 (post-migration)

We migrated from HS256 to **RS256 (RSA-2048)** for pal-web JWT session cookies in `HRTH-SEC-0145`, closed 2026-07. The migration rationale: companion apps already act as offline verifiers of the pod's identity via SPKI-pinned TLS certificates at the transport layer. Extending that public-verifier model to the JWT layer is a straight-line change — the RSA private key is generated on first-boot inside the TPM-sealed keyring, the public key is served during pair time over the mutually-authenticated pairing channel and stored in the companion's Keychain/EncryptedSharedPreferences.

Post-migration behaviour:
- Pod signs `palpod_session` JWT with RSA-2048 PSS-SHA256 (using `python-jose` with `RSA_PSS` mode).
- Companions verify signatures locally with the pod's pubkey; a forged or replayed JWT is rejected without a network round-trip.
- Key rotation: annual, plus after any incident with LUKS-key implications. Rotation is a signed record countersigned by the previous key.
- Code owner: **Priya Ramanathan (`priya@hearth.co`)**; module owner of `palweb/auth.py` per `CODEOWNERS`.
- **EdDSA (Ed25519) evaluation:** we chose RSA-2048 over Ed25519 for RS/Ed parity with the SPKI pinning already in place, and because the JOSE tooling maturity is stronger. Ed25519 migration is tracked as `HRTH-SEC-0155` for v3 (not blocking).

### 6.3 CSRF

Double-submit pattern (`csrf.py:76-140`). Cookie value = HMAC-SHA256(session-secret, random_18_bytes); header value must equal cookie value. Neither is HttpOnly on the CSRF side (by design); the session cookie is. Constant-time compare via `hmac.compare_digest` (`csrf.py:73, 113`). Router-level defence in depth via `require_csrf_double_submit` (`csrf.py:181-202`).

### 6.4 Consent

iOS: unforgeable compile-time — `_TapWitness` `fileprivate` init (`ConsentGesture.swift:48-50`), only constructed at the SwiftUI button tap (`ConsentGesture.swift:87`). Android: HMAC-signed nonce with server-derived initiator; replay guard via LRU-bounded nonce set (`ConsentTokenSource.kt:29-33`) + freshness `MAX_AGE_MS` (`ConsentTokenSource.kt:47-51`). Play Integrity attestation as the third leg is tracked as `HRTH-SEC-0143`.

### 6.5 Certificate pinning

SPKI (public key hash) pinning on companions, first-run-locked to the pod's own cert. Rotation supported via a signed rotation record.

### 6.6 Firmware signing and key custody

- **Signing algorithm:** ECDSA P-256 on all Hearth-signed artifacts (OS images, STM32 firmware, ML manifest).
- **Hardware root of trust:** Jetson NVIDIA-signed boot chain + STM32 RDP2.
- **Primary signing HSM:** Yubico YubiHSM 2 held in a fireproof safe at Hearth HQ (Oakland, CA). Two-of-three quorum for a signing ceremony: CEO (Sean), Head of Security (this author), and one rotating engineer with a Yubikey. Ceremonies are video-recorded, and the recording is hashed and countersigned into the release audit log.
- **Backup signing HSM:** a second, initialised-with-the-same-shards Yubico YubiHSM 2 held in an Iron Mountain safe-deposit vault in Salt Lake City, UT. Geographic separation is the point — a single site (fire, seizure, insurrection) does not destroy signing capability. The backup requires the same two-of-three quorum to activate; it is not a "one person can push updates" backdoor.
- **Signing ceremony cadence:** monthly for scheduled releases; ad-hoc for hotfixes with the emergency 2-of-3 quorum defined in §8.

### 6.7 Source-code and key escrow (the "what if Hearth folds" question)

The single most common question from enterprise buyers, from Kevin O'Leary on Shark Tank, and from any customer who is paying $95k for a 10-year-lifetime device: *"what happens if you go bankrupt?"* Our answer is a triggered-release escrow with **EscrowTech** as the escrow agent (industry-standard for source-code escrow; alternative: NCC Escrow — final selection tracked as `HRTH-SEC-0156`).

The escrow deposits, updated quarterly:
1. **Full source tree** of the Hearth OS (palweb, palvoice, palface, nftables ruleset, installer, extender firmware) at the exact commit hash of the shipped release.
2. **Toolchain and build recipe** sufficient to reproduce a hash-verifiable build image (see §7 for the reproducibility qualifier).
3. **A copy of the firmware signing public key** (which is not secret) plus a sealed envelope containing shards of the private key sufficient to reconstruct signing capability under the two-of-three model. Shards are Shamir-split; individual shards are held under separate legal control.
4. **The measurement policy** (see §6.8) so a customer or a fork maintainer can reproduce the PCR chain.

**Triggered-release conditions:** any one of the following triggers a 30-day cure period followed by escrow release to the beneficiary class (existing Hearth customers of record and Hearth PPA subscribers):
- Hearth Systems Inc. files for bankruptcy or dissolution.
- No signed security update has been pushed to the Hearth PPA for **12 consecutive months**.
- Three unremediated CVEs of Critical or High severity within a single component class remain open past their §8 SLA.
- Hearth ceases operation of `updates.hearth.co` for more than 60 days.

**What "release" means in practice:** the source tree, toolchain, and signing key shards are handed to a customer trustee (initially the largest enterprise buyer with a signed trustee agreement; if none, a nominated maintainer selected by EscrowTech from the Hearth security community). The trustee has the legal right to re-key the signing hierarchy (which invalidates further Hearth-signed pushes), publish a fork under the same source-available terms, and ship signed updates to customers who consent to the trustee's new key. Existing pod owners can accept the trustee's public key via a signed rotation record countersigned by both the last Hearth key and the trustee. This is not "Hearth's customers are stranded"; it is "Hearth's customers have a defined path off the mothership."

The escrow agreement summary lives at `/ops/escrow/escrow-agreement-summary.md` in the repository and the full legal instrument is available in the data room. Kevin's question has an answer.

### 6.8 Full-disk encryption and PCR selection policy

LUKS2 with argon2id KDF (`iter-time=2000`, `memory=1G`) on the NVMe JBOD. Master key sealed to fTPM PCRs **0, 2, 4, 7, and 9** — refuses to unlock if any of those measurements changed.

- **PCR 0:** CRTM + platform firmware. Detects a modified BIOS/UEFI.
- **PCR 2:** UEFI drivers and OpROMs. Detects a rogue OpROM.
- **PCR 4:** Bootloader (u-boot) and boot chain. Detects a swapped bootloader.
- **PCR 7:** Secure Boot policy state. Detects a Secure Boot db/dbx tamper.
- **PCR 9 (added in this revision):** **initrd measurements.** The initrd is where the `kernel.yama.ptrace_scope=3` claim from §3.3 is actually enforced, along with `iommu=on iommu.passthrough=0` and the SMMU setup from §4.1. Failing to measure PCR 9 meant a modified initrd (one that drops those kernel command-line hardening flags) could unseal the LUKS key without our noticing. `HRTH-SEC-0157` closed with this revision.

**PCRs we deliberately do NOT include:**
- PCR 1 (CPU microcode, platform config): too volatile across NVIDIA microcode updates; would require re-sealing after every NVIDIA quarterly patch.
- PCR 5 (boot loader config parameters): NVIDIA's u-boot re-emits this on every reboot with a nonce; unstable.
- PCR 8 (userspace boot manager): we do not use a userspace boot manager on the Jetson chain; the value is fixed.
- PCR 11 (system state at unlock): would create a chicken-and-egg with the auto-unlock path.

**Measurement policy file:** `/ops/tpm/measurement-policy.yaml` contains the golden PCR values per firmware release, keyed by image hash. The tpm2-tools sealing recipe (`tpm2_createpolicy`, `tpm2_seal`) is checked in and reproducible. This policy is included in the escrow deposit (§6.7).

### 6.9 Backup encryption

**age** — chosen over gpg. Justification: age is a small, modern, one-way key format with no compatibility ropes; gpg drags in a keyring, trust model, subkey concept, all of which are attack surface in a scenario ("I want my backups to be readable in 2032") where simple is what you want. Backup keys are wrapped by the customer's own passphrase and stored on the box; the passphrase is never stored.

---

## 7. Independent audit plan

**Cadence:** Annual full-stack firmware + web + companion audit; ad-hoc after any incident (§8) or major release. **Deliverable:** private full report + public redacted summary published to `hearth.co/security/audits/<year>.pdf`.

**On the "reproducible builds vs source-available vs NDA the audit" question.** The prior version of this document was too casual on all three fronts and the diligence review caught the contradiction. The precise, defensible position:

- **Source-available, not open source in the OSI sense.** The following components are public at `github.com/hearth/hearth-os`: the OS stack, `pal-web`, `pal-voice`, `pal-face`, the companion iOS + Android apps, the extender firmware for STM32, the installer, and the nftables ruleset. Anyone can clone, read, and audit them. The licence is source-available with a non-competition covenant (you can run it, patch it, redistribute patches; you cannot ship a competitor appliance from it). This is deliberately not MIT/Apache — the licence is on `github.com/hearth/hearth-os/LICENSE`.
- **Hash-verifiable builds, not bit-identical reproducibility (yet).** Full bit-identical reproducible builds — the Nixpkgs-grade rebuild-anywhere-and-hashes-match property — is a genuinely hard engineering commitment that we have not paid for. What we ship is one step less: **hash-verifiable images.** Every release publishes the SHA256 of every artifact in the image, signed with the Hearth firmware key. Anyone can pull the artifact off the pod (`hearth-image-inspect` command), hash it, and check the hash against the signed manifest. This proves "the bytes on your pod match the bytes we signed." It does not prove "if you rebuild from source you'd get the same bytes." Bit-identical reproducibility is tracked as `HRTH-SEC-0158` for v2, with an internal target of first bit-identical release by Q3 2027.
- **Why the audit is under NDA — until it isn't.** The third-party audit report is under NDA for a narrow, defensible reason: an audit report names findings, some of which are unfixed at the moment of publication, and publishing an unfixed critical finding is a directive to attack Hearth customers. This is standard industry practice (see how Trail of Bits reports typically publish 90 days after the vendor closes findings). **Our commitment:** the audit report becomes fully public within 90 days of the last critical or high finding being closed, or one year after the audit delivery, whichever is earlier. Enterprise buyers get the private full report under NDA in the interim so they can make purchase decisions with all data. The redacted public summary — "N findings; N critical, N high, N medium, N low; N fixed at ship, N tracked" — publishes on delivery day. This is our disclosure timeline, not an indefinite gag.

**Named candidates (in preference order):**

| Vendor | Strengths | Weakness | Estimated cost (USD) |
|---|---|---|---|
| **Trail of Bits** | Deep firmware + smart contract + application layer; excellent public reports | Booked out; wait time 4–8 months | $95k–$150k |
| **NCC Group** | Broad — hardware, RF, firmware, mobile; commercial UK/US | Larger firm; results vary by consultant | $80k–$140k |
| **Cure53** | Web + mobile leaders; well-known reports | Less hardware; may sub-contract silicon side | $60k–$100k |
| **Kudelski Security** | Silicon + hardware root of trust background | Enterprise-flavor; slower | $100k–$180k |

**Selection plan:** Trail of Bits for v1 audit if slot available; NCC Group as backup. **Statement of work outline:** in scope — pal-web full flow (auth, CSRF, WS, RustDesk client), pal-voice tool boundary, firmware signature chain, LUKS/TPM sealing (including PCR 9 policy), companion apps (iOS + Android), OEM firmware on STM32, HDMI/USB attack surface, escrow key-shard reconstruction procedure end-to-end. Out of scope for external audit — upstream Plex/Jellyfin/RustDesk internals (handed to their maintainers).

---

## 8. Incident response playbook

**Reporting channel:** `security@hearth.co` (documented in `/SECURITY.md`).

**Severity SLA (public commitment):**

| Severity | Definition | Hotfix window |
|---|---|---|
| Critical | Pre-auth RCE, silent-consent bypass, LUKS key exfil, mass-privacy leak | **72 hours to signed hotfix, auto-installed** |
| High | Auth-required RCE, LPE from user, consent bypass with UI signal, denial-of-service that survives reboot | **7 days** |
| Medium | Auth bypass with practical mitigations, information disclosure of non-sensitive metadata | **30 days** |
| Low | Hardening opportunity, defence-in-depth improvement | Next quarterly release |

**Pipeline mechanics:** reports triaged within 3 business days per `/SECURITY.md`. Coordinated disclosure default 90 days; can extend by mutual agreement with reporter. Hotfix builds go through the same signed-build ceremony (§6) with an emergency 2-of-3 quorum. Auto-install of critical hotfixes is on by default; customer can pause with a UI setting but a persistent banner remains.

**Customer communication plan:**
- **Critical:** in-UI banner on pod's local dashboard, in-app push to paired companions, out-of-band email to the registered `security-contact` if the customer opted into that channel.
- **High/Medium:** dashboard banner + next monthly digest email (opt-in).
- **All levels:** GitHub Security Advisory published on the calendar day, credited to the reporter unless anonymity requested.

**Postmortem:** every incident gets a blameless postmortem published to `hearth.co/security/incidents/<id>.md` (redacted).

**Escrow-trigger interaction:** if three unremediated Critical/High findings within a single component class remain open past SLA, the §6.7 escrow trigger fires. This makes the SLA table not just a promise but a mechanical consequence — miss the SLA repeatedly and the customer path off the mothership opens automatically.

---

## 9. Bug bounty

**Program design:**

- **Platform:** HackerOne. Justification: strongest safe-harbor language, most researcher gravity, fastest triage. Intigriti as a v2 candidate for EU-first talent. Self-hosted is not on the table for v1 — we don't want to run a moderation team.
- **Scope in:** `pal-web` FastAPI code, `pal-voice` orchestrator, install/update/uninstall scripts, systemd units, Docker Compose, RustDesk configuration, companion iOS + Android apps as published to their app stores, firmware update pipeline, escrow key reconstruction procedure (documented flow, not the shards themselves).
- **Scope out:** DoS against LAN-adjacent attackers who are already in the network (§1 non-goals); attacks that require physical access; upstream Plex/Jellyfin/RustDesk bugs (route to upstream); social-engineering of Hearth employees; anything under HackerOne's global safe-harbor exclusions.
- **Reward tiers:**

  | Severity | Bounty |
  |---|---|
  | Critical (silent-consent bypass, pre-auth RCE, LUKS key extraction, egress-class bypass) | **$10,000–$25,000** |
  | High (auth-required RCE, CSRF/consent bypass, meaningful info disclosure) | $3,000–$7,500 |
  | Medium | $500–$2,500 |
  | Low | $100–$500 |

- **Reserve:** $50,000 pool committed year one. Renewable; if we spend it, we replenish.
- **Safe harbor language:** we adopt the [disclose.io](https://disclose.io) safe-harbor template verbatim. No lawsuits against good-faith researchers under this policy. Documented in `/SECURITY.md`.
- **Hall of thanks:** researchers credited on `hearth.co/security/thanks`.

---

## 10. The Shark Tank answer

**Objection #20 rehearsal:** *"How do we know the offline claim isn't marketing? I can't audit your firmware. And what happens if you go bankrupt?"*

> "You don't take my word for it, because we made it structurally unnecessary. Four legs.
>
> **One — the egress ACL.** There are exactly seven things the pod ever puts on the wire: a signed firmware update pull, NTP, a DNS-over-TLS query to resolve those hosts, Ubuntu security updates, opt-in remote support with a physical tap, opt-in crash reports scrubbed on the pod before they leave, and whatever integration YOU wired to your own accounts. That list is enforced by nftables at kernel level, not by our app, and there's a CI hook that fails the build if a new byte gets added. Every one of those seven is disclosed on the pod's own screen.
>
> **Two — the audit.** Trail of Bits on the firmware, web, and companions. The redacted findings summary is public on delivery day. The full report is under NDA for a specific reason — you don't publish unfixed criticals — and it becomes fully public within ninety days of the last high or critical closing, or a year after delivery, whichever is earlier. Enterprise buyers get the full report immediately under NDA.
>
> **Three — the code and the escrow.** The whole OS stack is source-available at `github.com/hearth/hearth-os` under a source-available licence. Not reproducible-builds bit-identical yet — that's a year-out engineering commitment — but hash-verifiable: every byte on your pod matches a byte we signed, and you can check that with one command. And Kevin, on your question: source and signing-key shards are in escrow with EscrowTech. If we file for bankruptcy, if we go twelve months without shipping a security update, or if three critical CVEs sit unfixed in one component, the escrow releases to a customer trustee. Your pod keeps getting updates from someone even if we're gone. That's a contractual instrument, not a promise.
>
> **Four — the bounty.** HackerOne, $25,000 top tier, $50,000 committed year one for anyone who finds a covert egress or a consent bypass. Reserve doubles if we burn it. If someone proves the promise is soft, we pay them, we ship a signed hotfix in seventy-two hours, and we publish the postmortem the same week. That is what an offline appliance actually looks like on paper."
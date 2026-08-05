# PRIVACY-COMPLIANCE-MANUAL.md

**Hearth Data Protection Compliance Manual**
**Owner:** Head of Privacy / Data Protection Officer
**Audience:** Board audit committee, external counsel, SOC 2 auditors, regulator submissions, Series B due diligence, international expansion legal review
**Version:** 1.0 (baseline for Y2+ international rollout)
**Cross-references:** `THREAT-MODEL.md`, `EXPANSION-Y2-PLUS.md`, `ONBOARDING-PLAYBOOK.md`, `WARRANTY-TRAINING.md`, `BOARD-GOVERNANCE.md`

---

## 1. Compliance frame

The core assertion of this manual is simple and inverts the default posture of the connected-home industry: **Hearth's offline architecture is a privacy moat, not a compliance liability.** Every household running Hearth is a self-contained data controller in a way no cloud-first competitor can claim. Voice profiles never leave the household LAN. Face embeddings never leave the household LAN. The family memory graph never leaves the household LAN. Media libraries never leave the household LAN. The seven egress classes enumerated in `THREAT-MODEL.md §1.2` — (1) signed firmware update pull (HTTPS to `updates.hearth.co`), (2) NTP (UDP/123 to `time.cloudflare.com` primary + `pool.ntp.org` fallback), (3) RustDesk self-hosted remote support (opt-in TCP/21115-21119 to `rustdesk.hearth.support`, gated by physical tap on the pod), (4) customer-configured integrations (opt-in per customer; the customer is the controller for this class), (5) bug report upload / Sentry (opt-in HTTPS to `sentry.hearth.support`, per-crash), (6) DNS resolution (DoT TCP/853 to `1.1.1.1` default, customer-configurable), (7) apt / dpkg security updates (HTTPS to `archive.ubuntu.com` + Hearth PPA at `ppa.launchpad.net`) — are the *complete* set of network activities the box performs. Nothing else leaves the household without human consent captured, logged, and revocable.

Because that set is minimal, explicit, and auditable in source code, we can demonstrate compliance across every US state privacy statute, the FTC Act, GDPR, UK GDPR, Swiss FADP, Israel PPL, Australia Privacy Act, Singapore PDPA, Hong Kong PDPO, and Japan APPI **more cheaply and with less residual risk than any cloud-first competitor**. A Ring, Alexa, or Google Nest competitor must justify petabytes of continuously ingested household audio and video sitting in a cloud region subject to third-country access requests. Hearth must justify seven narrowly scoped, individually consented, individually auditable network calls. Under any reasonable proportionality test — GDPR Article 5(1)(c) data minimization, CCPA "reasonably necessary and proportionate," BIPA "reasonably necessary to provide the service" — Hearth wins by construction.

That is not a marketing claim. It is an engineering claim we can prove with `journalctl`, iptables logs, the sub-processor list, and the source of every daemon on the box. This manual exists to translate that engineering claim into the format each regulator, auditor, and enterprise buyer expects to receive.

A word on tone. This document is written for regulators, auditors, and plaintiff-side counsel. It is not marketing copy. Where Hearth's offline posture materially reduces a risk, we say so plainly. Where the offline posture does *not* eliminate a risk — biometric collection at install, concierge access to household context under RustDesk pairing, sub-processor exposure in the seven egress classes — we say that too, and we describe the compensating controls. Overclaiming privacy is itself an FTC Section 5 violation, and the CPPA has explicitly signaled that "privacy-first" positioning creates a higher bar under CCPA. We aim to under-claim relative to what the box actually does, and back every claim with a control the auditor can inspect.

---

## 2. US federal and state privacy law

### 2.1 FTC Act Section 5

Section 5 of the FTC Act prohibits "unfair or deceptive acts or practices in or affecting commerce." For Hearth this creates three concrete obligations enforceable against the company by the Commission and, in some jurisdictions, by state AGs invoking mini-FTC Acts.

**Deception.** Every privacy claim we make in marketing, on the website, in the box, at install, and in the mobile app must be substantiated by the actual behavior of the shipped product. "Nothing leaves your household" is only defensible because the seven-class egress model in `THREAT-MODEL.md §1.2` is the complete set and each class is either infrastructure-necessary (CDN, DNS, NTP, packages) or gated on explicit consent (RustDesk pairing, Sentry, bug reports). Marketing copy, sales scripts, and Shark Tank talking points must not overclaim beyond that. The marketing review checklist in `docs/investor/marketing/` enumerates prohibited phrases: "zero telemetry," "no data ever leaves," "totally airgapped" are all prohibited because they are false with respect to the necessary infrastructure classes. Approved phrasing: "your household voice, faces, and memories never leave your Hearth" (true), "the seven things Hearth *does* send are listed on our website" (true and inspectable).

**Unfairness.** An act is unfair under Section 5 if it causes or is likely to cause substantial injury to consumers, is not reasonably avoidable, and is not outweighed by countervailing benefits. Biometric collection without meaningful consent, security controls inadequate to protect biometric data, or dark patterns steering consumers away from privacy protections would each be unfair. Compensating controls: install-time BIPA-grade written consent (§3), LUKS-plus-TPM at-rest encryption per `THREAT-MODEL.md`, privacy toggles that default to the most protective setting per §11 below.

**COPPA.** Hearth is an adults-and-teens product. The primary purchaser is 18+, the account holder is 18+, and the target market is adult households with luxury discretionary spend. Households where the primary user is under 13 are an explicit non-goal per `ROADMAP.md`. However, a Hearth in a family home may recognize a child under 13. When the install flow detects a household member profile marked under 13 (age is self-declared by the account holder at profile creation), Hearth applies COPPA-grade handling: (a) no voice profile is enrolled without verifiable parental consent captured in the mobile app; (b) the child's face embedding, if any, is stored only if the account holder actively enrolls it and re-consents at the annual privacy review; (c) no external egress is ever tied to that profile including bug reports, Sentry stack traces, or RustDesk sessions; (d) the child profile's memory graph entries are purged on the same schedule as adult profiles but with a shorter default retention (12 months rather than "household lifetime"). The Commission's 2013 COPPA amendments extended the rule to persistent identifiers and precise geolocation; Hearth's on-device-only architecture avoids most of the trigger conditions by construction, but the parental-consent gate remains as a belt-and-suspenders control.

**FTC health-data guidance (2023 policy statement and 2024 Health Breach Notification Rule amendments).** The Commission has stated that even *non-HIPAA* consumer health data receives heightened scrutiny, and that inferring health status from ambient data is itself a regulated act. Hearth's product boundary is explicit and enforced in code: no health inference is drawn from ambient voice, no wellness scoring is performed, no medical-adjacent claims appear in marketing. Concierge L1 agents are trained (`WARRANTY-TRAINING.md`) to redirect health topics rather than log them. The bright line: Hearth is a media and companion device, not a wellness product. Any future product direction into wellness would trigger the escalation path in §9 and a full re-review under this manual.

### 2.2 California CCPA / CPRA

Hearth is a "business" under Civil Code §1798.140 for CPPA purposes: annual gross revenue is projected to exceed the $25 million threshold in Y2, and even before that we voluntarily comply as our standard baseline. Each **household member with a distinct voice profile is a "consumer"** under the statute. This is important: the CPPA has treated shared-device accounts as extending rights to each identifiable individual, and Hearth's per-member voice model makes each member individually identifiable within the household.

**Right to know.** Any consumer may request, via the Data Portal in the mobile app, a full disclosure of the categories and specific pieces of personal information Hearth has collected about them, the sources, the purposes, and the categories of third parties (sub-processors) with which any of it has been shared. The Data Portal renders this from the box's own SQLite catalog. Because Hearth collects a bounded and small set of information (voice embedding, optional face embedding, memory graph entries scoped to that member, media playback history scoped to that member, mobile-app pairing metadata), the Right-to-Know response is a small JSON blob with a human-readable rendering. No cloud lookup is required. SLA: 45 days per statute, actual median target: 24 hours.

**Right to delete.** A household member removes their voice profile, memory graph, face embedding, and playback history by tapping "Delete my profile" in the mobile app. The action triggers cryptographic destruction of the LUKS-wrapped keys binding that member's data on the box, followed by best-effort overwrite of the underlying blocks and a certification event written to the audit log. The householder-scope admin console retains a tombstone (member ID, deletion date, requester identity, no PII) for two years to prove the deletion happened. The householder is emailed a certificate of deletion within 24 hours.

**Right to correct.** A household member updates their name, age, relationship metadata, and voice-profile pronunciation hints in the mobile app. Face embedding correction requires re-enrollment. Memory graph correction is a first-class flow: any household member can edit or delete individual memory nodes attributed to them.

**Right to opt out of sale or sharing.** Not applicable. Hearth sells no personal information and shares no personal information for cross-context behavioral advertising. This is enforced by the source code of the box: there is no telemetry endpoint that receives household content, and the seven egress classes carry no advertising or profiling data.

**Right to limit use of sensitive personal information.** Not applicable in the operative sense. CCPA §1798.121 permits consumers to limit use of sensitive PI to the purposes reasonably necessary to provide the requested service. Hearth uses biometrics and precise geolocation only to provide the requested service; there is no secondary use. The disclosure is made regardless.

**Right to non-discrimination.** Hearth does not offer differential pricing, differential service, or a lesser experience based on privacy choices. A household that declines Sentry crash telemetry receives the same warranty, the same concierge, the same feature roadmap as one that accepts it. Sub-processor opt-outs (§6) do not affect device functionality.

**Right to appeal.** Any denied privacy request is appealable to the Head of Privacy at `privacy@hearth.co`. If the household member is unsatisfied with the appeal outcome, they may lodge a complaint with the California Privacy Protection Agency.

**Sensitive personal information.** Hearth's sensitive-PI categories under §1798.140(ae) are: (1) biometric information — voice embeddings and, optionally, face embeddings; (2) precise geolocation — the household's installation address, captured during shipping and used by the concierge for site visits; (3) account credentials — the RustDesk pairing token and mobile-app auth tokens.

**CPPA compliance.** Hearth publishes an annual privacy assessment consistent with CCPA §1798.185(a)(15). The assessment is performed by the Head of Privacy with external counsel review and covers processing purposes, categories, retention, security, and risk-benefit balancing. It is filed with the CPPA if and when the pending final regulations require submission and published in redacted form on `hearth.co/privacy/transparency`.

### 2.3 Illinois BIPA

BIPA (740 ILCS 14/) is the strictest biometric privacy statute in the United States and, following *Cothron v. White Castle* (2023), each collection or transmission of a biometric identifier without written consent is a separate violation. Hearth's exposure model is straightforward once controls are in place, and catastrophic without them. The math is not subtle: 47,000 waitlist prospects times $1,000 statutory minimum per negligent violation is $47 million, and per-collection accrual under *Cothron* multiplies that by the number of times each face or voice was captured. This is the single largest US litigation risk facing the company and is treated as such.

**Biometric identifier collection.** Hearth collects voice embeddings and, in v2.0+ where face recognition ships, face embeddings. Both are derived on-device from raw audio and video that are discarded after enrollment. The embeddings, not the raw biometrics, are the retained "biometric information" under §14/10.

**Written informed consent.** The install flow presents each household member 13+ (younger with verifiable parental consent) with a BIPA-compliant written notice describing the specific purpose (household voice recognition), the specific term of collection and storage (until deletion by the member or three years after last household use, whichever is earlier), and a signature capture on the mobile app or the Hearth touchscreen. The consent text is stored in the household's own audit log with a timestamp, the enrolling device's public key, and the household member's electronic signature. See §3 for the operative text.

**Retention schedule.** Under §14/15(a), a written retention schedule is required and enforceable. Hearth's schedule: (1) voice embeddings retained until the household member requests deletion via the mobile app or three years after the last household interaction attributable to that member, whichever comes first; (2) face embeddings (v2.0+) on the same schedule; (3) automatic pre-expiration reminder sent 90 days before scheduled destruction inviting the member to renew consent.

**Destruction protocol.** On scheduled destruction or member-requested deletion, the LUKS-wrapped per-member key is destroyed, rendering the underlying ciphertext blocks unrecoverable regardless of subsequent physical access. A best-effort block wipe follows. A destruction certificate is emitted to the household audit log and to the member's email.

**Sale, lease, disclosure prohibition.** BIPA §14/15(c) prohibits sale, lease, trade, or profit from biometric information. Hearth explicitly does not sell, lease, trade, or otherwise profit from any biometric identifier or biometric information. This is stated in the consent notice, in the privacy policy, and in the sub-processor DPAs.

**Storage.** Encrypted at rest under LUKS with the key sealed to the TPM per `THREAT-MODEL.md §3.4`. Physical theft of the box does not compromise the biometrics because the TPM refuses to release the key without the boot-chain measurements matching the enrolled state.

### 2.4 Texas, Colorado, Connecticut, Utah, Virginia, and other comprehensive state privacy laws

Texas CUBI (Bus. & Comm. Code §503.001) parallels BIPA for biometric identifiers with a reasonable-retention standard and an AG-only enforcement mechanism. Hearth's BIPA-grade controls satisfy CUBI by construction.

Colorado (CPA), Connecticut (CTDPA), Utah (UCPA), Virginia (VCDPA), Oregon (OCPA), Texas (TDPSA), Montana (MCDPA), Delaware (DPDPA), Iowa, Indiana, Tennessee, and the rolling wave of 2024–2026 comprehensive state privacy laws share a common structural core: rights of access, deletion, correction (except UCPA), portability, opt-out of targeted advertising, opt-out of sale, opt-out of profiling with legal or similarly significant effects, and, in most states, a right to appeal. Hearth's controls satisfy the entire matrix in a single implementation because the underlying data flows are the same:

- **Rights of access / correction / deletion / portability**: single Data Portal implementation in the mobile app; jurisdiction detection selects the appropriate response template and SLA.
- **Opt-out of targeted advertising, sale, profiling**: not applicable to Hearth; the disclosure is made in each jurisdiction's required form.
- **Sensitive data processing consent**: BIPA-grade consent is stricter than any state comprehensive law and satisfies the "affirmative consent" or "opt-in" standard in CPA, CTDPA, VCDPA (as amended), OCPA, MCDPA, MODPA, and the 2025-2026 new-state wave below.
- **Data protection assessments** (CPA, CTDPA, VCDPA, MCDPA, OCPA, TDPSA, MODPA, MnCDPA): the annual privacy assessment (§2.2) is scoped to satisfy the multi-jurisdictional DPA requirement in a single document.

**2025-2026 new-state wave.** Seven new comprehensive state privacy statutes take effect across 2025 and 2026 and must be tracked as first-class deltas rather than folded into the "shared structural core" line above:

- **New Jersey Data Privacy Act (NJDPA)** — effective **January 15, 2025**. AG-only enforcement. Sensitive data (which includes biometrics) requires opt-in consent, satisfied by §3.
- **Nebraska Data Privacy Act** — effective **January 1, 2025**. Modeled on Texas TDPSA; small-business exemption threshold makes applicability turn on data-volume, not revenue.
- **New Hampshire Privacy Act (SB 255)** — effective **January 1, 2025**. Rights framework aligned with CTDPA.
- **Minnesota Consumer Data Privacy Act (MnCDPA)** — effective **July 31, 2025**. Adds a first-of-its-kind consumer right to question a profiling decision and receive an explanation; Hearth does not perform profiling, so the delta is disclosure-only.
- **Maryland Online Data Privacy Act (MODPA)** — effective **October 1, 2025**. **MODPA data-minimization is the strictest new-state delta of the entire wave and is stricter than CTDPA**: personal data collection and processing must be limited to what is "reasonably necessary and proportionate to provide or maintain a specific product or service requested by the consumer," and sensitive data processing must be "strictly necessary" — a materially higher bar than the CTDPA "reasonably necessary" standard. MODPA also bans sale of sensitive data outright (no consent cure). Hearth's on-device-only biometric architecture and the seven-class egress ceiling satisfy MODPA by construction; the compliance narrative for MODPA is the tightest in this manual and is treated as the model for other DPAs re-benchmarking to it.
- **Rhode Island Data Transparency and Privacy Protection Act** — effective **January 1, 2026**. Notable for a mandatory itemized third-party disclosure in the privacy notice.
- **Kentucky Consumer Data Protection Act (KCDPA)** — effective **January 1, 2026**. Modeled on VCDPA.

Every one of these regimes is satisfied by the same underlying implementation, but the compliance matrix (§13 cross-reference to the internal ops tracker) enumerates each state's specific delta including the MODPA "strictly necessary" language, the MnCDPA profiling-explanation right (disclosure-only), and the Rhode Island itemized-third-party disclosure requirement.

### 2.5 Washington My Health My Data Act

The Washington MHMDA (RCW 19.373) took full effect for regulated entities on March 31, 2024, and is the strictest state health-data statute with a private right of action. "Consumer health data" is defined expansively and includes inferences drawn from other data that reveal health status.

Hearth does not process consumer health data. This is a **product boundary enforced in code and in policy**: no health inference is drawn from ambient voice; no wellness or symptom scoring occurs on-device; the concierge team is trained to redirect rather than log health topics; the sub-processor list contains no health-data recipients. A voice command that mentions a medication is transcribed for the immediate response and then dropped from the memory graph unless the household member explicitly saves it as a note (in which case it is treated as household-controlled note content, not as health data processed by Hearth).

If the product ever crosses the health-inference line, MHMDA compliance requires: (a) a separate consent flow specifically for consumer-health-data processing; (b) an authorization for any sharing; (c) a geofence around sensitive locations under the geofencing prohibition; (d) enhanced deletion rights; (e) an appeals mechanism. That is a full product review — see §9 escalation path.

### 2.6 New York SHIELD Act

SHIELD (Gen. Bus. Law §899-aa/bb) imposes reasonable-security requirements on any entity holding private information of New York residents and requires breach notification. Hearth's technical controls — LUKS-plus-TPM at-rest encryption, TLS 1.3 for all outbound egress classes, principle of least privilege for the concierge role, audit logging on the box and centrally for support activity, employee training per §8 — meet the SHIELD reasonable-security standard. Breach notification procedure is documented in §9.

### 2.7 FCRA

The Fair Credit Reporting Act does not apply. Hearth is not a consumer reporting agency, does not furnish consumer reports, and does not use consumer reports for eligibility decisions. This is noted so the SOC 2 auditor can dismiss it in one line.

### 2.8 GLBA, HIPAA, FERPA

None apply. Hearth is not a financial institution, is not a HIPAA-covered entity or business associate, and is not a covered educational institution. If a household includes a HIPAA-covered clinician who uses Hearth in a home office, the customer contract is silent on their downstream obligations; Hearth is not their business associate because we do not process PHI on their behalf.

---

## 3. Biometric consent framework

Biometric consent is the single control on which the largest US litigation exposure hinges, and it is the control most easily broken by well-meaning UX iteration. The framework is codified here and changes require Head of Privacy sign-off and Board audit committee notification per `BOARD-GOVERNANCE.md`.

**Voice profile consent.** At install, and at any subsequent addition of a household member, the enrolling person taps through a screen presenting exactly this text on the Hearth touchscreen and (for remote enrollment) the mobile app:

> "By setting up your voice profile, [name] consents to Hearth learning your voice for the purpose of household voice recognition. This data is stored only on this Hearth and never leaves your household unless you specifically approve a support session or bug report. You may delete your voice profile at any time from the Hearth mobile app or by asking Hearth to 'delete my voice profile.' Hearth will keep this data until you delete it or until three years after your last interaction with this device, whichever comes first."

The consent is captured with a checkbox, a signature (electronic — pointer on the touchscreen or fingerpad on the phone), the timestamp, the household ID, the member ID, and a hash of the consent text version. The record is written to the household audit log and mirrored to a company-side consent registry (member ID and hash only, no name, no household address) for BIPA record-keeping.

**Face recognition consent (v2.0+).** Face is a separate feature added in v2.0 per `ROADMAP.md`. It is off by default. Enabling it triggers a fresh consent flow per household member with this text:

> "By setting up face recognition, [name] consents to Hearth learning your face for the purpose of recognizing you as you move through your home. Your face is analyzed on this Hearth. A mathematical fingerprint is stored on this device and never leaves your household unless you specifically approve a support session or bug report. Raw video is not stored. You may delete your face recognition data at any time from the Hearth mobile app. Hearth will keep this data until you delete it or until three years after your last interaction with this device, whichever comes first."

The same capture-and-store protocol as voice consent applies. Face consent must be given separately by each individual household member; there is no household-wide consent.

**Face embedding lifecycle.** The face model runs on-device (`pal-face/`). Raw frames are analyzed in memory and dropped. Only the embedding vector is written to disk. Embeddings never leave the LAN except in an opt-in bug report and only after the raw embedding is either scrubbed or replaced by a hash committed by the household's admin.

**Retention.** Household member controls their retention through the mobile app: delete-now, delete-on-schedule, or renew-consent-annually.

**Deletion protocol.** LUKS-wrapped key destruction (rendering ciphertext unrecoverable) followed by best-effort block wipe, followed by tombstone in the audit log and certificate to the household member's email. The 30-day certification is a formal artifact suitable for BIPA record-keeping in the event of subsequent litigation.

**Consent version control.** Every change to the consent text is a versioned event. Members enrolled under a prior version continue to hold consent under that version until they either affirm the new one or their profile is deleted. The consent hash chain proves the exact text a given member consented to.

**Consent registry mirroring (litigation-defense enhancement).** The company-side consent registry mirrors, per household member, the **full consent text version** the member accepted — not merely the hash. The hash chain remains the tamper-evidence primitive on the household side (per §3 above), and the company-side registry adds a second, litigation-defense purpose: in the event of a BIPA class action, a *Cothron*-style per-collection challenge, or a state AG discovery request, we can produce the exact text a specific member consented to on a specific date without relying on the household audit log surviving physical device loss. The mirrored copy is scoped to consent text only — no household address, no member name — indexed by member ID and consent hash. The dual system (hash chain on-box for tamper-evidence + text-version copy company-side for defense) closes the v1.0 gap where a lost or wiped pod could leave us unable to prove the exact consent text a member accepted. Tracked as HRTH-SEC-####.

**Incidental capture policy (v2.0 face recognition).** The v2.0 camera captures frames that may include guests and non-enrolled household members incidentally — a dinner-party visitor walking past the sphere, a child's friend, a cleaner. Under BIPA §14/15 and the state-comprehensive-law sensitive-data rules, capturing a face without prior written consent is a violation *per collection* under *Cothron v. White Castle*. To close this gap, the on-box `pal-face` pipeline enforces an **incidental-capture blur-and-discard policy**: every frame is scored against the household's enrolled-embedding set (voice-profile-linked); any face whose embedding does not match an enrolled member is blurred in the residual frame and its embedding is discarded before any writes to disk. No non-enrolled embedding is ever persisted, uploaded, sent to Sentry, or included in a bug report. This is enforced in the pipeline, not in policy: the write path for face embeddings takes only `EnrolledMember(id, consent_hash)` tuples as input, and the enrollment path requires a matching signed consent record. Tracked as HRTH-SEC-####.

**Under-13 parental consent — FTC-approved verifiable method (v2.0 face recognition).** For any face profile of a household member declared under 13 at profile creation, Hearth requires FTC-approved verifiable parental consent per the COPPA Rule §312.5(b) methods list. The specific method Hearth ships is **credit-card verification via Stripe Identity plus a follow-up video-call confirmation with the named parent or guardian**. The credit-card step satisfies §312.5(b)(2)(v) (payment system verification). The video-call step, staffed by the Concierge team on a scheduled slot, confirms the identity of the person authorizing consent, reads the specific consent text back to the parent/guardian on-camera, and captures their spoken affirmation as an additional audit record. This dual-step method exceeds any single §312.5(b) method's evidentiary weight and is documented as our COPPA-compliance mechanism for the v2.0 face feature in a household with under-13 members. The under-13 face profile is retained under the stricter of (a) the parent's stated retention preference or (b) 12 months, and re-consent is required annually with the same dual-step method. Tracked as HRTH-SEC-####.

---

## 4. International compliance

The baseline for international compliance is **EU GDPR as implemented in `EXPANSION-Y2-PLUS.md §8`**, which enumerates the Article 6 legal basis for each of the seven egress classes, the Article 30 records of processing, and the DPIA for the Article 35 high-risk processing (biometric identifiers). Every other international regime is documented below as a delta from that GDPR baseline.

**UK GDPR + Data Protection Act 2018.** Substantively identical to EU GDPR for Hearth's purposes. UK ICO is the supervisory authority. Transfers into the UK from the EU are covered by the UK's adequacy decision. Transfers from the UK are executed under the UK IDTA or the Addendum to the EU SCCs. UK-specific note: the UK Age-Appropriate Design Code applies if we knowingly serve under-18s, and our under-13 policy in §2.1 combined with a v2.0 age-check flow for adolescent household members satisfies the code.

**Swiss FADP (revised, in force September 2023).** GDPR-aligned with two deltas: (a) the FADP requires *individual* data-breach notification to affected data subjects "as soon as possible" without the GDPR's 72-hour "risk to rights and freedoms" threshold — Hearth defaults to notification for any confirmed breach of household data; (b) DPO designation is not mandatory but recommended, and Hearth's DPO is designated for Swiss purposes.

**Israel Privacy Protection Law (as amended by Amendment 13, in force August 2025).** Registration of certain databases with the Israeli Privacy Protection Authority is required. Hearth's household-scope biometric database, replicated per household, does not aggregate to a company-side database, so the registration analysis reduces to: (a) the company-side consent registry (member ID and hash only); (b) the concierge queue; (c) the sub-processor list. Each is registered or exempt as applicable. Adequacy for transfers between Israel and the EU is maintained.

**Australia Privacy Act 1988 and the Australian Privacy Principles.** APP 3 (collection), APP 6 (use and disclosure), APP 8 (cross-border disclosure), APP 11 (security), and APP 12 (access and correction) are the operative principles. APP 3.3 requires consent for sensitive information (which includes biometrics), satisfied by §3. APP 8 disclosure to overseas recipients requires either consent or contractual equivalence; Hearth's sub-processor DPAs (§6) impose APP-equivalent obligations. Notifiable Data Breaches scheme (Part IIIC) applies; the incident-response protocol in §9 covers it.

**Singapore PDPA.** Consent obligation and notification obligation are covered by §3. Data protection provisions parallel GDPR at a lower rigor level and are satisfied by Hearth's baseline controls. Data Protection Officer registration with the PDPC is required and complete. The Do Not Call registry does not apply because Hearth does not conduct outbound marketing calls.

**Hong Kong PDPO.** Data Protection Principles 1–6 are satisfied by the GDPR baseline. Direct marketing consent (DPP 6A) is satisfied by the explicit opt-in required for marketing per §11. Cross-border transfer restrictions under section 33 remain unactivated as of publication; Hearth's controls are ready for section 33 activation.

**Japan APPI (as amended, in force April 2022).** Consent to acquire "special care-required personal information" (biometrics fall inside this category per the 2020 amendment's clarification) is satisfied by §3. Cross-border transfer requires either recipient country adequacy (EU is adequate to Japan and vice versa), specific consent, or equivalent safeguards; Hearth's sub-processor DPAs establish equivalent safeguards.

**Canada PIPEDA and provincial equivalents (Quebec Law 25, BC PIPA, Alberta PIPA).** Meaningful consent, purpose limitation, and openness are satisfied by §3 and the public sub-processor list. Quebec Law 25 requires a Privacy Impact Assessment for any project involving personal information; the same DPIA satisfies it. Cross-border transfer disclosure is made in the privacy policy.

**Brazil LGPD.** Substantially GDPR-aligned. ANPD is the supervisory authority. DPO designation is required and complete. Cross-border transfer under LGPD Article 33 requires ANPD-approved SCCs or adequacy; Hearth uses the ANPD SCCs published in 2024.

**South Korea PIPA.** Sensitive information consent (Article 23) is satisfied by §3. Cross-border transfer notification and consent (Article 28) is satisfied by the sub-processor disclosure. PIPC is the supervisory authority.

For each of these regimes, the internal compliance matrix (maintained by the Head of Privacy) captures the specific delta from the GDPR baseline, the local counsel of record, the local DPO or representative (where required), the breach notification timelines, and the audit cadence.

---

## 5. Data lifecycle management

**Collection.** Voice profiles, memory graph entries, media library metadata, mobile-app pairing tokens, and — v2.0+, opt-in — face embeddings, all collected on-device at install and during use. Collection is scoped to the household by architecture; there is no ambient collection from adjacent networks or from streaming service accounts beyond the metadata the household member's linked account exposes.

**Storage.** LUKS-encrypted at rest with the key sealed to the TPM (`THREAT-MODEL.md §3.4`). No cloud replication. Backup, when the household enables it, is to a household-owned NAS or external drive using the same LUKS key wrapping. The company holds no copy of any household's data.

**Use.** Household-scope only. There is no cross-household correlation. There is no advertising use. There is no model training on household data (the on-device models are shipped pre-trained; on-device personalization does not exfiltrate weights). The concierge role, when engaged under RustDesk with triple consent, has ephemeral read access only to the specific artifacts required to resolve the ticket.

**Retention.** Household-member-controlled for voice and face profiles per §3. Household-admin-controlled for memory graph and media metadata. Concierge queue retention: 60 days for support ticket context, then automatic purge. Company-side consent registry: retained for the greater of six years or the statute-of-limitations period of the strictest applicable regime, holding only member ID and consent-text hash.

**Deletion.** Cryptographic wipe by LUKS key destruction, followed by best-effort block overwrite, followed by tombstone in the audit log, followed by 30-day certification to the household member. The tombstone retains member ID, deletion date, requester identity — nothing else.

**Portability.** Full JSON export via the mobile app, digitally signed by the household's admin key. A companion human-readable PDF is generated for members who prefer it. Export is scoped to the requesting member's data. Export is delivered locally (mobile app to phone) and does not transit any Hearth infrastructure.

**Breach response.** 72-hour regulator notification per GDPR Article 33 and matching state statutes; best-effort 24-hour notification to affected household members via the concierge team; SHIELD and MHMDA notification tracks run in parallel. See §9.

---

## 6. Vendor and sub-processor management

Hearth publishes a **sub-processor list** at `hearth.co/privacy/sub-processors` and mirrors it in the mobile app. The current list, corresponding to the seven egress classes:

| Sub-processor | Purpose | Egress class | Endpoint | Jurisdiction |
| --- | --- | --- | --- | --- |
| Cloudflare (CDN edge for `updates.hearth.co`) | Signed firmware update distribution | Class 1 | `updates.hearth.co` | US, global anycast |
| Cloudflare (NTP + backup) + NTP Pool volunteers | Wall-clock time sync | Class 2 | `time.cloudflare.com` (primary), `pool.ntp.org` (fallback) | US / global |
| Hetzner Online GmbH (Frankfurt) or OVH (self-hosted infrastructure sub-processors for the Hearth-operated RustDesk relay) | Self-hosted RustDesk hbbs/hbbr relay for remote support (includes concierge screen-share); tap-gated, session-scoped | Class 3 | `rustdesk.hearth.support` (regional relays per §4 international) | EU (Frankfurt) / UK (London) / regional per §4 |
| Customer-nominated | Customer is the data controller for this class; sub-processors depend entirely on what the customer configures at the local UI (e.g., ntfy.sh, personal MQTT broker, Jellyfin remote proxy) | Class 4 | Customer-determined | N/A (customer-controlled) |
| Hetzner Online GmbH (Frankfurt) or OVH (self-hosted infrastructure sub-processors for the Hearth-operated Sentry instance) | Self-hosted Sentry ingest for opt-in crash bundles; strict server-side allowlist re-validation | Class 5 | `sentry.hearth.support` | EU (Frankfurt) / UK (London) |
| Cloudflare (DNS resolver) | DoT resolution to `1.1.1.1` (customer-configurable to a nominated resolver) | Class 6 | `1.1.1.1` on TCP/853 | US, global anycast |
| Canonical Ltd (Ubuntu apt mirrors + Launchpad PPA hosting) | Ubuntu LTS security-patch distribution + Hearth PPA hosting | Class 7 | `archive.ubuntu.com`, `security.ubuntu.com`, `ppa.launchpad.net/hearth/hearth-os/ubuntu` | UK / global mirror network |

**Vendor DPAs.** Every sub-processor with any nexus to household data has a signed data processing agreement conforming to GDPR Article 28 and CCPA §1798.140(e). Where the sub-processor's own template does not meet the standard, the Hearth-issued DPA is used. The DPA library is maintained by the Head of Privacy in coordination with the General Counsel.

**Sub-processor review.** Annual, with three components: (a) desktop review of the sub-processor's SOC 2 Type II report and, where relevant, ISO 27001 certificate; (b) contractual reconfirmation of the DPA and any new sub-processor sub-flow-downs; (c) for the top three sub-processors by household-data exposure, on-site or virtual on-site visit. The 2027 cycle includes the RustDesk relay operator, Sentry, and the CDN.

**Third-country transfers.** Where the sub-processor is outside the EEA and the household is inside the EEA, transfers execute under the 2021/914 Standard Contractual Clauses, Module Two (controller-to-processor), plus a Transfer Impact Assessment addressing US Section 702 and Executive Order 12333 for US recipients. The TIA for each US recipient is refreshed annually and after any material change to US surveillance law.

**Sub-processor changes.** Households are notified 30 days in advance of any new sub-processor or material change to an existing one. The mobile app allows the household admin to review the change and, for optional egress classes (5, 6, 7), opt out. For mandatory infrastructure classes (1, 2, 3, 4), the household admin's remedy for a change they object to is to disable the corresponding update channel; documentation and support impacts are surfaced clearly.

---

## 7. Third-party audit and certifications

**SOC 2 Type II.** The Q2 2027 audit engagement targets an AICPA-registered firm. Candidate firms under evaluation: Prescient Assurance, A-LIGN, Coalfire. The scope covers the Security, Availability, Confidentiality, and Privacy Trust Service Criteria; the Processing Integrity criterion is out of scope because Hearth is not a data-processing service in the SaaS sense.

**SOC 2 Type II observation window — 12 months.** The observation period for the initial Type II runs from **July 1, 2026 through June 30, 2027** — a full 12-month window rather than the minimum-viable 6 months. A 6-month window reads as "minimum viable" to enterprise buyers and to Series B diligence teams that have seen the SaaS convention; a 12-month window is what mature security programs ship and is the honest signal that the controls have been operational, not just implemented, across a full seasonal cycle. Report delivery target: August 2027. If timeline pressure ever forces a fallback to a 6-month observation window (e.g., a Series B closing calendar), the shorter window will be published with an explicit footnote — "abbreviated Type II observation window scoped for [reason]; full-year observation window follows in the next annual cycle" — so buyers can price the signal accurately.

**ISO 27001.** Certification target Q4 2027. The Information Security Management System scope is: the corporate side (headquarters IT, the sub-processor management program, the concierge platform, the consent registry, the DPO office) and the fleet-management side (the update-signing infrastructure and the release pipeline). Each household's Hearth is out of scope because it is customer-owned and customer-operated.

**Cyber Essentials Plus.** Q1 2028 target for UK sales. UK enterprise buyers and UK household counterparties negotiating employee-benefit device programs (`EXPANSION-Y2-PLUS.md`) expect Cyber Essentials Plus as table stakes.

**FIPS 140-2 / FIPS 140-3.** Aspirational, not committed. Cryptographic modules on the Hearth (LUKS via cryptsetup, TLS via OpenSSL, TPM 2.0) support FIPS-mode compilation, and shipping a FIPS-mode SKU is on the roadmap for US federal signaling if the sales pipeline materializes. Not a Y2 commitment.

**Independent firmware audit — Trail of Bits, Q2 2027 kickoff.** Trail of Bits engagement per `THREAT-MODEL.md §7`. The engagement kickoff shifts from the v1.0 Q3 2027 slot to **Q2 2027** to accommodate Trail of Bits' documented 4–8 month lead time (called out in `THREAT-MODEL.md §7` "Booked out; wait time 4–8 months"). A Q3 2027 kickoff would miss the fall board cycle and Series B diligence window; a Q2 2027 kickoff clears the report through remediation by the same fall cycle. Scope: the seven egress-class implementations, the update chain, the LUKS-plus-TPM boot, and the RustDesk tap-consent gate. Report to be published in redacted form within 90 days of remediation.

**Bug bounty — HackerOne, Q4 2027 launch.** The v1.0 draft placed the HackerOne launch in Q3 2027 concurrent with the Trail of Bits engagement kickoff, ISO 27001 certification prep, and the SOC 2 Type II observation window mid-point. Running three major audit programs simultaneously (Trail of Bits + HackerOne + ISO 27001) with a single Head of Security in a single quarter is a scheduling error; findings from either the firmware audit or the SOC 2 gap analysis should inform bug-bounty scope, not compete with it for triage attention. **HackerOne launch shifts to Q4 2027** — after the Trail of Bits report is delivered and its critical/high findings are triaged into the tracker, and after ISO 27001 stage-1 audit completes. Scope and payout matrix per `THREAT-MODEL.md §9`, aligned with the seven egress classes and the biometric consent framework, with the biggest bounties reserved for household-data-egress bypasses.

**Audit spend — line-itemed in the financial model.** The audit and certification budget totals $95k–$150k for the Trail of Bits firmware engagement plus SOC 2 Type II (Prescient / A-LIGN / Coalfire quotes range $45k–$85k for the observation-plus-report pass) plus ISO 27001 (Stage 1 + Stage 2 range $35k–$70k with an accredited certification body) plus Cyber Essentials Plus (~$8k) plus the HackerOne Q4 2027 launch reserve ($50k committed year one per `THREAT-MODEL.md §9`). Total audit-and-certification spend is line-itemed in the operating financial model under **"Security & Compliance — Third-Party Audits" (FINANCIAL-MODEL.md line 47, cross-referenced in the Series B pitch's use-of-funds slide)**, with a two-year forward projection at $310k–$420k per annual cycle across the audit portfolio. This is not a discretionary spend; missing it defaults the enterprise-buyer signal and triggers the SLA-driven escrow trigger in `THREAT-MODEL.md §6.7`.

---

## 8. Employee training

**All employees.** Annual data privacy training: 60-minute online module plus quiz, minimum 80% pass, retakes allowed and required. The module covers the seven egress classes, the biometric consent framework, the sub-processor list, the incident-response flow, and the escalation contact tree.

**Concierge team.** Additional 40-minute module on the triple-consent gate for household access, PII handling during ticket resolution, the redirect protocol for health topics, the escalation criteria for privacy requests received via the concierge line, and the 24-hour breach-notification best-effort role the concierge team plays. Cross-referenced with `WARRANTY-TRAINING.md`.

**Engineering.** Eight-hour secure SDLC and threat-modeling training annually. Curriculum covers the STRIDE model applied to Hearth's architecture, the seven egress-class boundary conditions, the LUKS-plus-TPM boot chain, and the code-review checklist for anything touching consent flows, biometric processing, or the egress list.

**Executives.** Annual privacy briefing from external counsel, 90 minutes, covering the regulatory horizon (new state laws taking effect, GDPR enforcement trends, international expansion legal review), the litigation landscape (BIPA class-action activity, MHMDA emerging cases, GDPR representative-action developments), and material risks to the Series B narrative.

Training completion is tracked in the HR system and reported to the Board audit committee quarterly.

---

## 9. Incident response

**Response team.** DPO (lead), Head of Security, General Counsel, and CEO. The CTO is co-opted for technical breaches. External counsel is engaged for any confirmed breach. External incident-response retainer is with an AICPA-registered firm.

**Trigger criteria.** Any confirmed unauthorized access to household data, any confirmed egress outside the seven approved classes, any confirmed compromise of the consent registry, any confirmed loss of a sub-processor's containment. Suspected events trigger triage.

**72-hour regulator notification.** GDPR Article 33 sets the ceiling. State breach-notification statutes (California, New York, and thirty-plus others) have their own tracks running in parallel. The DPO owns the notification decision and the drafting; the General Counsel reviews.

**24-hour household notification (calibrated for what we actually know at hour 24).** Best-effort target via the concierge team, faster than any statute requires. The notification within 24 hours communicates the **fact of a suspected incident** — that Hearth has detected or been informed of a possible unauthorized access, egress, or containment failure affecting the household — together with containment status and interim recommended actions. Specific **data-category detail (which member profiles, which embedding categories, which time windows)** is provided as the forensic timeline confirms the scope, targeted at the **72-hour** window aligned with GDPR Article 33's regulator-notification ceiling. This two-step calibration replaces the v1.0 blanket 24-hour data-category commitment, which was operationally unrealistic — 24 hours is often before triage completes on a novel event, and issuing incorrect data-category attribution at hour 24 creates its own set of Section-5 and Article-83 problems. The household is not left waiting: the hour-24 message names the incident, the containment status, and the follow-up cadence; the hour-72 message names the confirmed data categories.

**Post-mortem.** Blameless post-mortem within 30 days per the standard incident-response template. Root-cause analysis, contributing factors, preventive measures, and residual risk are captured. A redacted post-mortem summary is published in the transparency report unless the underlying facts are subject to a law-enforcement request.

**Transparency report.** Semi-annual. Number of privacy requests received by type, response times, denial rate, breach count with category rollup, government access requests received and responded to. Published on `hearth.co/privacy/transparency`.

### 9.5 Detection stack

Notification and post-mortem workflows only work if the detection layer surfaces incidents in the first place. The detection stack, on both sides of the trust boundary in `THREAT-MODEL.md §2`, is:

- **On-box detection.** `auditd` and `osquery` run under systemd on each pod, with a hardened rule set covering the seven egress classes, the LUKS-TPM unlock chain, the RustDesk relay control channel, and the `pal-face` embedding write path. Events are batched locally and aggregated to the **company-side alert channel via the Sanmina VPN and Cloudflare Tunnel** to the security team's ingest endpoint. The tunnel is mutually-authenticated (mTLS + Cloudflare Access Zero Trust posture policy), and the endpoint is scoped to the security team by CODEOWNERS + hardware-key-required approval.
- **SIEM pipeline.** Aggregated auditd + osquery + pal-web / pal-voice application logs land in a SIEM. The MVP candidate is **Grafana Loki with Alertmanager** as the on-call routing layer, chosen for cost and self-hosting parity with the rest of the Hearth stack; the scale-out candidate is **Panther** or **Elastic Security**, evaluated Q2 2027 against fleet size. Alertmanager routes to PagerDuty for on-call rotation.
- **Sub-processor alert channels.** Each sub-processor's own alert feed is wired into the security team's queue: **Cloudflare Alerts** (CDN, DNS, NTP anomalies), **Canonical Ubuntu Security Advisories** (apt / dpkg CVE announcements pre-empt patch cycle), **Hetzner / OVH platform advisories** (regional relay infra), Cloudflare Radar for large-scale internet-health context.
- **Bug-bounty triage handoff.** HackerOne submissions triaged as valid Critical or High severity by the on-call triager are handed to the incident-response team within a **2-hour target**, matching or beating the SLA committed on the HackerOne program page. The handoff opens an incident ticket and pages the DPO if any household-data-egress bypass is credible.
- **Detection coverage report.** Semi-annual internal review of detection-rule coverage against the STRIDE matrix in `THREAT-MODEL.md §3`. Gaps become tracked issues under HRTH-SEC-####.

### 9.6 State-by-state breach-notification clock appendix

Regulator-side notification deadlines vary by state. The clock the DPO office runs against, alongside the GDPR Article 33 universal 72-hour ceiling, is summarized below. This is a working reference — the internal ops tracker keeps the full 50-state table current — but these thresholds carry the most operational weight for Hearth's household distribution:

- **California AG (Cal. Civ. Code §1798.29 / §1798.82).** Single-resident notification is required "in the most expedient time possible and without unreasonable delay." AG notification is required when a single breach affects **more than 500 California residents** (§1798.29(e) / §1798.82(f)). No fixed day-count ceiling for AG notice, but "expedient" is the operative standard.
- **New York SHIELD Act (Gen. Bus. Law §899-aa/bb).** Individual notification "in the most expedient time possible and without unreasonable delay." AG + Department of State + Division of State Police notification is required if the breach affects **more than 5,000 New York residents**, and consumer reporting agencies (Equifax, Experian, TransUnion) must be notified in that same threshold.
- **Ohio Rev. Code §1349.19.** Notification to affected residents "in the most expedient time possible but not later than **45 days** following discovery." Ohio's day-count floor is the strictest 45-day standard in the mid-tier states.
- **Texas Bus. & Comm. Code §521.053.** Notification to affected residents "as quickly as possible but no later than the **60th day** following the determination that a breach occurred," plus AG notification for breaches affecting more than 250 residents.
- **Florida F.S. §501.171.** 30-day individual notification with AG notice for breaches affecting more than 500 residents.
- **Illinois Personal Information Protection Act (815 ILCS 530).** Notification "in the most expedient time possible" with AG notice for breaches affecting more than 500 residents.
- **Colorado Rev. Stat. §6-1-716.** 30-day individual + AG notification for breaches affecting more than 500 residents.
- **GDPR Article 33 — 72-hour ceiling.** Universal EU regulator ceiling on notification of a personal-data breach to the lead supervisory authority. Individual data-subject notification (Article 34) is triggered by high risk to rights and freedoms and is separately timed.
- **Swiss FADP.** "As soon as possible" for any confirmed household-data breach; Hearth defaults to notification without waiting for a rights-and-freedoms threshold determination (per §4).

**The composite operating clock the DPO uses.** Ohio's 45-day floor and Texas's 60-day floor sit inside GDPR's 72-hour ceiling if the incident touches EU customers. The default operating standard the DPO runs against is: **72-hour GDPR ceiling if any EU customer is affected; 45-day operational ceiling as the outer target for all other incidents; 24-hour "fact of incident" household-side notification per §9 above; 72-hour "confirmed data categories" household follow-up.** Any state-specific deviation from this composite (e.g., an AG threshold triggered at the 500- or 5,000-resident count) is routed by the incident-response ticket to the specific-state notification workflow in the internal ops tracker.

---

## 10. Data subject rights fulfillment

**Right of access.** Handled via the Data Portal in the mobile app. SLA: 30 days per most state statutes, actual median target 24 hours. Delivery: JSON export digitally signed by the household admin key; PDF companion for human review; the export is generated on the household's own Hearth and does not transit company infrastructure.

**Right to rectification / correction.** Handled via the mobile app for structured fields (name, age, relationship metadata). Concierge-assisted for memory graph corrections that involve household-admin permission checks.

**Right to erasure / deletion.** Handled via the mobile app. Cryptographic key destruction is the primary control; best-effort block wipe is secondary; audit-log tombstone and 30-day email certificate close out the flow.

**Right to data portability.** JSON plus PDF export via the mobile app. Format documented publicly to enable third-party re-import for households migrating between Hearths or to a hypothetical future household-data manager.

**Right to object.** Escalation to the DPO for the narrow set of processing activities where Hearth's legal basis is legitimate interest (essentially the infrastructure egress classes 1–4). The Head of Privacy evaluates and either accommodates (usually by disabling the associated feature for the objecting household) or declines with a written explanation.

**Right to withdraw consent.** For the opt-in classes 5 (RustDesk), 6 (Sentry), and 7 (bug reports), a single toggle in the mobile app withdraws consent for all future events. Historical events already transmitted are retained by the sub-processor for their disclosed retention period.

**Right to lodge a complaint.** Contact information for the relevant DPA is included in the mobile-app privacy page and in the annual transparency report. The DPO office assists with routing.

---

## 11. Marketing and advertising compliance

**No third-party ads on Hearth.** Codified in the product spec. There is no ad server, no ad SDK, no cross-context behavioral advertising infrastructure anywhere in the product.

**No behavioral advertising anywhere in Hearth's ecosystem.** The mobile app, the website, and the concierge platform do not run behavioral ad SDKs. Marketing analytics use privacy-preserving tooling (Plausible or self-hosted equivalent) with no cross-site tracking.

**Waitlist and marketing emails.** Opt-in only, at the point of joining the waitlist, with a clear description of the message cadence and content. Every message contains a one-click unsubscribe. No dark patterns in the unsubscribe flow — no "are you sure," no multi-step confirmation, no reactivation nag.

**Referral program.** Both parties see honest disclosure of what the referrer earns and what the referee receives. Referral does not exempt either party from the standard consent flows.

**Prohibited across all marketing and product surfaces.** Dark patterns, deceptive design, buried privacy notices, forced consent, forced defaults on privacy toggles that favor the company over the household, roach-motel unsubscribe flows, and any UI that misrepresents the choice architecture. The design review checklist in `docs/investor/design/` enforces the rule at the mockup stage.

---

## 12. Contact

**Data Protection Officer:** name and email published at `hearth.co/privacy` and inside the mobile app; phone routed through the concierge team for verification. As of publication the DPO reports to the CEO and has an independent reporting line to the Board audit committee per `BOARD-GOVERNANCE.md`.

**Privacy rights requests:** `privacy@hearth.co`, 30-day SLA per statute, actual median target 24 hours for the mobile-app self-service flows.

**Regulator contacts:** California Attorney General and California Privacy Protection Agency; Illinois Attorney General; each EU Member State DPA per the lead-supervisory-authority designation in `EXPANSION-Y2-PLUS.md §8`; UK Information Commissioner's Office; Swiss Federal Data Protection and Information Commissioner; Israeli Privacy Protection Authority; Office of the Australian Information Commissioner; Singapore PDPC; Hong Kong PCPD; Japan PPC; Canadian OPC and Quebec CAI; Brazil ANPD; South Korea PIPC. Direct contact routing is maintained in the internal ops tracker.

---

## 13. Cross-doc reconciliation

This manual is the top of the compliance stack. It is consistent with, and reconciled against, the following peer documents. Any conflict resolves in favor of this manual, with the peer document updated to match within one revision cycle.

- **`THREAT-MODEL.md §1.2` — seven egress classes.** This manual's compliance frame, the sub-processor list, the DPIA scope, and the incident-response trigger criteria all sit on top of the egress-class enumeration in the threat model. Any change to the egress list requires simultaneous update to this manual, the DPIA in `EXPANSION-Y2-PLUS.md §8`, and the public sub-processor list.
- **`EXPANSION-Y2-PLUS.md §8` — GDPR Article 6 per egress class + Article 30 records + DPIA.** International compliance in §4 rests on this section as the baseline; other regimes are captured as deltas.
- **`ONBOARDING-PLAYBOOK.md §3` — install day consent capture.** The BIPA-grade consent flow in §3 of this manual and the operative consent text are the source of truth; the install-day playbook implements them.
- **`WARRANTY-TRAINING.md` — L1 concierge consent training.** The concierge module in §8 of this manual defines the curriculum; the warranty training document delivers it and tracks completion.
- **`BOARD-GOVERNANCE.md` — audit committee oversight.** The Board audit committee reviews the annual privacy assessment, the annual sub-processor review, the SOC 2 Type II report, the ISO 27001 surveillance report, the transparency report, and any material privacy incident. The DPO has a standing independent line to the committee chair.

Any change to the sub-processor list, the biometric consent text, the seven egress classes, or the retention schedules requires Head of Privacy sign-off, General Counsel review, and Board audit committee notification. The compliance baseline exists so that the next audit, the next regulator inquiry, and the next enterprise buyer's due-diligence request can be answered from a single source with a straight face.

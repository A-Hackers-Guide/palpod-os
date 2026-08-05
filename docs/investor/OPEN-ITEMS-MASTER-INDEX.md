# HEARTH — OPEN ITEMS MASTER INDEX

**Owner:** Head of Investor Relations
**Location:** `/docs/investor/OPEN-ITEMS-MASTER-INDEX.md` — sits at the top of the data room next to `INDEX.md` and `CHANGELOG.md` as the navigation trio.
**Version:** v1.1, 2026-08-05 (P0 tier recut + new category §K + reconciliation checkboxes)
**Confidentiality:** Single copy per LP under mutual NDA. Do not redistribute. Marketing use prohibited.

---

## 1. Purpose + how to read

### 1.1. Why this document exists

A diligence associate reading a 70+ document data room the size of Hearth's will find, if they are conscientious, dozens of items across the room that are either not-yet-done, not-yet-verified, dated for the future, or explicitly disclosed as pending. Some are load-bearing (SOC 2, FCC, CFO hire); some are hygiene (dual-source qualification, minor localization); some are governance ritual (annual board self-eval). All of them get flagged, and if the associate has to reconstruct the list themselves out of a room of markdown files, they will miss items — and, worse, they will infer from the misses that Hearth is either hiding pending items or does not know what its own pending items are.

**This document is the consolidated list.** Every open item, TBD, pending certification, unfilled hire, unresolved vendor selection, unverified claim, and future milestone that appears anywhere in the data room is indexed here in one navigable table, with owner, target date, priority, and cross-reference to the source doc where the item is described in full.

### 1.2. What this document is NOT

- **Not a work-tracking system.** Internal execution against these items is tracked in Jira / Linear / GitHub Issues, with per-item sub-tasks, engineering estimates, and burn-down. The `HRTH-SEC-####` ticket IDs referenced throughout the security posture live in the public GitHub tracker. This document is the LP + board + audit-side abstraction over that operational reality — a diligence artifact, not a burndown.
- **Not a risk register.** Risks that materialized (an actual incident, an actual missed date, an actual vendor default) get logged in `CHANGELOG.md` under `[Fixed]` or `[Legal]` tags. This document tracks the *planned* pipeline of items that are not yet actioned but are known and dated.
- **Not marketing-safe.** Every line item names an owner and a date; naming an owner-by-role for a role that is not yet hired (CTO, Head of Privacy, General Counsel) is honest inside the data room and misleading outside it. Do not lift any table from this document into a public press release.

### 1.3. How to navigate

Section §2 organizes open items into **eleven categories** (A through K), each with a table of item + owner + target date + priority tier + source doc reference. Section §3 defines the four **priority tiers** (P0 blocking → P3 nice-to-have) and shows the count at each tier. Section §4 is the **ownership matrix** — who owns each item, who is second in line, target-fill-by-date for any TBD second-in-line, and the escalation path. Section §5 documents the **governance policy** for how this list is maintained.

**Reading order for a diligence associate:** §1.4 (v1.1 P0 recut reconciliation) → §3 (tier definitions) → §2 by category, focusing on P0 and P1 items first → §4 for owner-side follow-ups → source docs cited in the right column for full detail. A conscientious associate will spot-check any item they consider load-bearing against the underlying source doc; the row is not a substitute for the source, only an index to it.

**Reading order for the board:** §1.4 (P0 recut), §2C (legal), §2D (vendor), §2F (financial), §2I (governance), §2K (regulatory / tax / compliance ops). These are the categories where a P0/P1 slip becomes a board conversation.

**Reading order for a prospective employee:** §2B (hires). All roles listed there are targeted hires with committed comp bands per `hr/EXEC-COMP-FRAMEWORK.md`; the row does not constitute an offer or a role commitment but is the honest planning-side view of what Hearth expects to fill and when.

### 1.4. v1.1 P0 tier recut — reconciliation table

In v1.0 the P0 tier held 27 items (26% of all open items). External diligence review flagged this as either institutional panic signal or definition drift — a well-run company does not have a quarter of its known open items in the "blocking" tier. v1.1 rewrites the P0 definition to a **strict interpretation** and re-ranks accordingly.

**New P0 definition (strict):** "Cannot close Series A / cannot ship v1.0 pilot / cannot legally operate." An item is P0 only if its slip breaks one of those three outcomes. Everything that used to sit at P0 for reasons of "very important" or "must not slip" is now P1.

**Reconciliation summary:**

| Bucket | v1.0 count | v1.1 count | Delta |
|---|---|---|---|
| P0 (blocking, strict) | 27 | 10 | −17 |
| P1 (critical, 12-mo commitment) | 46 | 70 | +24 (17 recut from P0, 7 new in §K) |
| P2 (important, 12–24 mo) | 24 | 26 | +2 (2 new in §K) |
| P3 (nice-to-have, >24 mo) | 5 | 5 | 0 |
| **Total tracked items** | **102** | **111** | **+9 (§K additions)** |

**Items recut from P0 → P1 in v1.1** (17):

| Item | Section | Rationale for downgrade |
|---|---|---|
| Trail of Bits firmware audit | §A | Load-bearing security posture, but pilot can ship without published summary in hand; P1 with 12-mo commitment |
| CE certification | §A | Required for EU market only; v1.0 pilot ships US-first, so does not block v1.0 pilot |
| CTO hire | §B | VP Engineering in seat pre-hire; Series A investors expect but do not gate close on CTO; P1 |
| Head of Manufacturing Ops | §B | Interim founder-plus-VP-Eng coverage during pilot; P1 |
| Head of Customer Success | §B | Y1 GA depends on this hire; pilot phase does not; P1 |
| Firmware Engineer (senior IC #1) | §B | Existing team ships pilot; P1 |
| Industrial Designer (senior IC) | §B | Design frozen at pilot; P1 |
| Utility patent conversion | §C | 12-month provisional deadline is P1-critical, but a missed conversion does not block Series A close or v1.0 ship — it forfeits priority date, which is a P1 material harm |
| Non-provisional patent filings | §C | Same rationale as utility conversion |
| Household-employer template MSA | §C | Governs customer-side household staff arrangement; not a legal-to-operate requirement for Hearth-the-company; P1 |
| Signed dealer distributor agreements | §C | LOIs already in hand for Series A narrative; conversion is P1-critical for revenue but does not block close |
| Trail of Bits engagement kickoff | §D | Same rationale as §A Trail of Bits audit |
| $2M term life insurance on founder | §F | Founder-personal-side risk mitigation; the strict Series A blocker is $10M key-person, not $2M term life; P1 |
| v1.0 GA (600 units cumulative Y1) | §G | Q4 2027 milestone; v1.0 pilot Q2 2027 is the P0 ship gate; GA is P1 follow-on |
| Real deposit data + weekly waitlist growth | §H | Measurement commitment, not a close/ship/operate gate; P1 |
| CES 2027 booth build final CAD + AV run-of-show | §J | Marketing execution; not a legal-to-operate gate; P1 |
| CES 2027 booth CAD sign-off | §J | Same as booth build; P1 |

**Items that remain P0 in v1.1** (10):

| Item | Section | Blocking rationale (strict) |
|---|---|---|
| Series A close ($10M primary) | §F | Definitional |
| $10M key-person policy on founder | §F | Series A protective provision — investors will not close without |
| D&O insurance — initial bind | §F | Required at Series A close |
| Product liability insurance ($10M rider) | §F | Cannot legally ship v1.0 pilot to customers without |
| **Ann Lamport Hammitte (Cooley TM) — VERIFY partner status** | §C | Blocks any external mention; Series A materials cite named counsel |
| **Nate Kelly (Kilpatrick design counsel) — VERIFY partner status** | §C | Blocks any external mention; same rationale |
| FCC certification | §A | Cannot legally sell RF device in US without |
| UL/ETL certification | §A | Dealer channel will not sell without safety mark |
| Sanmina Fremont board-fix SOW — first-article delivery | §D | Direct blocker to v1.0 pilot ship |
| v1.0 pilot (10 units to LOI dealers) | §G | The ship milestone itself |

The Ann Lamport Hammitte + Nate Kelly VERIFY-BEFORE-EXTERNAL-MENTION items **remain P0 blocking** and are called out here explicitly per external diligence review. Both stay in §C with the same P0 marker they held in v1.0.

**Additions in v1.1 (§K — regulatory ops, tax, compliance ops):** state tax + employment registration by state, OSS license compliance operational tracking, warranty reserve accounting policy, R&D tax credit filing cadence, export controls / EAR classification, 409A refresh cadence, ESPP framework, secondary transaction policy, right-to-repair public commitments. See §2K.

---

## 2. By category

### §A. Pending certifications + audits

Certifications and third-party audits with regulatory or diligence-facing consequence. All budgets are Series A committed and reflected in `operations/KPI-DASHBOARD-FRAMEWORK.md` §F1 fully-loaded cash-burn build.

**Reconciliation:** Last cross-checked against canonical source docs (`security/PRIVACY-COMPLIANCE-MANUAL.md`, `INDEX.md` §5, `BOM-VENDOR-PACKAGE.md`, `international/EXPANSION-Y2-PLUS.md`, `security/THREAT-MODEL.md`) on **2026-08-05** · Owner initials: **MK** (interim, pending Head of Security hire post-Series A) · Cadence: **monthly**

| Item | Owner | Target date | Budget | Priority | Source |
|---|---|---|---|---|---|
| SOC 2 Type I attestation | Head of Security | Q2 2027 | $85k (Vanta + audit fees) | P1 | `security/PRIVACY-COMPLIANCE-MANUAL.md`; `CHANGELOG.md` §Standing open items |
| SOC 2 Type II attestation | Head of Security | Q2 2028 (observation window opens Jul 1 2027, closes Q2 2028) | $60k Y2 audit fees | P1 | `security/PRIVACY-COMPLIANCE-MANUAL.md`; `INDEX.md` §5 |
| ISO 27001 certification | Head of Security | Q4 2027 (stage 1 audit Q3 2027, stage 2 Q4 2027) | $95k | P1 | `INDEX.md` §5; `CHANGELOG.md` §Standing open items |
| Trail of Bits firmware audit | Head of Security | Q2 2027 kickoff; published summary 90 days after critical/high remediated | $180k engagement | P1 (v1.0: P0 — recut per §1.4) | `security/PRIVACY-COMPLIANCE-MANUAL.md` §7; `INDEX.md` §5 |
| Cyber Essentials Plus (UK) | Head of Security | Q1 2028 | $18k | P2 | `international/EXPANSION-Y2-PLUS.md` |
| FCC certification (Part 15B subpart J, Part 15C) | VP Engineering | Q1 2027 (pre-CES ship) | $75k lab + filing | **P0** | `INDEX.md` §5; `BOM-VENDOR-PACKAGE.md` |
| CE certification | VP Engineering | Q1 2027 (initial); UKCA follow-on Q4 2027 | $65k | P1 (v1.0: P0 — EU market only, not v1.0 pilot blocker) | `international/EXPANSION-Y2-PLUS.md` §regulatory |
| UL/ETL certification | VP Engineering | Q1 2027 (safety mark required for LAI dealer sell-in) | $55k | **P0** | `BOM-VENDOR-PACKAGE.md`; `operations/WARRANTY-TRAINING.md` |
| UKCA certification | VP Engineering | Q4 2027 (post-Brexit UK mark) | $28k | P2 | `international/EXPANSION-Y2-PLUS.md` |
| RCM (Australia) | VP Engineering | Q1 2029 (ANZ market open) | $22k | P3 | `international/EXPANSION-Y2-PLUS.md` |
| ISED (Canada) | VP Engineering | Q1 2028 (Canada Y2 launch) | $18k | P2 | `international/EXPANSION-Y2-PLUS.md` |
| Big-4 audit engagement letter (E&Y or Deloitte) | CFO (fractional then full-time) | Signed within 30 days of Series A close (Q2 2027); FY2026 audit complete Q3 2027 | $180k FY2026 audit | P1 | `INDEX.md` §5 |
| Bit-identical reproducible builds — first release | Head of Security | Q3 2027 target (HRTH-SEC-0158) | Engineering time, no cash line | P3 | `security/THREAT-MODEL.md` §7 |
| Source-code escrow — final agent selection (EscrowTech vs NCC Escrow) | Head of Security | Q1 2027 (HRTH-SEC-0156) | $8k/yr recurring | P2 | `security/THREAT-MODEL.md` §6 |

### §B. Pending hires

Per `hr/EXEC-COMP-FRAMEWORK.md` §2. Every role has a written comp band already committed to the option-pool math in `SERIES-A-DECK.md` Slide 13. Named individuals are not disclosed here; if a candidate is in a signed offer window the CEO discloses to the lead investor bilaterally.

**Reconciliation:** Last cross-checked against `hr/EXEC-COMP-FRAMEWORK.md` §2 and `SERIES-A-DECK.md` Slide 13 option-pool math on **2026-08-05** · Owner initials: **MK** (interim, pending Head of HR hire) · Cadence: **monthly**

| Role | Target date | Comp band (source: EXEC-COMP §2) | Priority | Source |
|---|---|---|---|---|
| CTO | Q1 2027 (contingent on Series A close) | $310k base + 2.75-3.25% common | P1 (v1.0: P0 — recut, VP Eng interim coverage) | `hr/EXEC-COMP-FRAMEWORK.md` §2 |
| Head of Manufacturing Operations | Q1 2027 | $240k base + 0.75-1.0% common | P1 (v1.0: P0 — recut per §1.4) | `hr/EXEC-COMP-FRAMEWORK.md` §2 |
| Head of Customer Success | Q1 2027 | $220k base + 0.6-0.85% common | P1 (v1.0: P0 — recut per §1.4) | `hr/EXEC-COMP-FRAMEWORK.md` §2 |
| Firmware Engineer (senior IC #1) | Q1 2027 | $215k base + 0.15-0.3% | P1 (v1.0: P0 — recut per §1.4) | `hr/EXEC-COMP-FRAMEWORK.md` §2 |
| Industrial Designer (senior IC) | Q1 2027 | $210k base + 0.15-0.3% | P1 (v1.0: P0 — recut per §1.4) | `hr/EXEC-COMP-FRAMEWORK.md` §2 |
| Data Engineer (BigQuery migration) | Q1 2027 | $220k base + 0.2-0.3% | P1 | `INDEX.md` §5; `hr/EXEC-COMP-FRAMEWORK.md` §2 |
| CFO — full-time (fractional Preston Advisors until Q1 2028) | Q1 2028 promotion / hire | $290k base + 1.5-2.0% common | P1 | `INDEX.md` §5; `hr/EXEC-COMP-FRAMEWORK.md` §2 |
| General Counsel | Q1 2028 | $275k base + 0.8-1.2% common | P1 | `hr/EXEC-COMP-FRAMEWORK.md` §2; `legal/IP-ENFORCEMENT-PLAYBOOK.md` |
| VP International (Y2) | Q3 2028 | $265k base + 0.6-0.9% common | P2 | `international/EXPANSION-Y2-PLUS.md` |
| Head of Privacy / DPO | Q1 2028 (GDPR/UK-DPA requirement for EU launch) | $235k base + 0.35-0.5% common | P1 | `security/PRIVACY-COMPLIANCE-MANUAL.md` |
| Head of IP (or promoted GC scope) | Q1 2028 | $230k base + 0.35-0.5% common | P2 | `legal/IP-ENFORCEMENT-PLAYBOOK.md` |

### §C. Pending legal + documentation

Legal engagements, IP conversions, and named-professional verification items outstanding across the room.

**Reconciliation:** Last cross-checked against `legal/IP-ENFORCEMENT-PLAYBOOK.md`, `INDEX.md` §9, `customer-success/HOUSEHOLD-STAFF-KIT.md` §4, `brand/BRAND-GUIDE.md`, `sales/SALES-PLAYBOOK.md` on **2026-08-05** · Owner initials: **MK** (interim, pending GC hire Q1 2028) · Cadence: **monthly**

| Item | Owner | Target date | Priority | Source |
|---|---|---|---|---|
| Utility patent conversion (provisional → non-provisional) | Head of IP / GC | Q3 2027 (12-month provisional deadline) | P1 (v1.0: P0 — recut; missed deadline forfeits priority date, P1 material harm not a Series A / v1.0 gate) | `legal/IP-ENFORCEMENT-PLAYBOOK.md` |
| Non-provisional patent filings — Halbach controller family + consent-witness pattern | Head of IP / GC | Q3 2027 | P1 (v1.0: P0 — recut per §1.4) | `legal/IP-ENFORCEMENT-PLAYBOOK.md` |
| Design patent grants | Head of IP | Expected 12-18 months from filing | P1 | `legal/IP-ENFORCEMENT-PLAYBOOK.md` |
| Trademark registration on principal register (Hearth wordmark + sphere-silhouette design mark) | Cooley IP counsel | Pending USPTO — publication for opposition open | P1 | `legal/IP-ENFORCEMENT-PLAYBOOK.md`; `brand/BRAND-GUIDE.md` |
| Trade dress documentation (ongoing capture of sphere silhouette + face-module levitation gesture) | Head of Design + Head of IP | Ongoing through v2.0 launch | P2 | `legal/IP-ENFORCEMENT-PLAYBOOK.md` §4 |
| Cooley IP counsel — engagement letter | CEO | Q1 2027 (retainer engaged upon Series A close) | P1 | `INDEX.md` §9; `legal/IP-ENFORCEMENT-PLAYBOOK.md` |
| Wilson Sonsini corporate counsel — retainer engagement | CEO | Q1 2027 (backup to Cooley for corporate work if conflict emerges) | P2 | `INDEX.md` §9 |
| Employment counsel firm selection | Head of HR (post-hire) | Q1 2027 | P1 | `hr/EXEC-COMP-FRAMEWORK.md`; `customer-success/HOUSEHOLD-STAFF-KIT.md` §4 |
| **Ann Lamport Hammitte (Cooley TM) — VERIFY partner status** | Head of IR | Before any external doc cites the name | **P0 (blocking mention)** — remains P0 in v1.1 per §1.4 | `legal/IP-ENFORCEMENT-PLAYBOOK.md` — internal doc only until verified |
| **Nate Kelly (Kilpatrick design counsel) — VERIFY partner status** | Head of IR | Before any external doc cites the name | **P0 (blocking mention)** — remains P0 in v1.1 per §1.4 | `legal/IP-ENFORCEMENT-PLAYBOOK.md` — internal doc only until verified |
| Kaleidescape licensing coordination for customer library transfer | Head of Customer Success | Q3 2027 | P2 | `operations/MEDIA-IMPORT-RUNBOOK.md` |
| Legacy media service partner selection (Legacybox vs iMemories) | Head of Customer Success | Q2 2027 | P2 | `operations/MEDIA-IMPORT-RUNBOOK.md` |
| Household-employer template MSA + workers-comp rider | Outside counsel + Head of Ops | Q4 2026 (placeholder in `hr/` until executed) | P1 (v1.0: P0 — recut; governs customer-side arrangement, not Hearth-the-company legal-to-operate) | `CHANGELOG.md` §Standing open items; `customer-success/HOUSEHOLD-STAFF-KIT.md` §4 |
| Signed dealer distributor agreements (converting the six Founding Dealer LOIs) | VP Sales | Q1 2027 (post-CES, gated on finalized dealer margin card) | P1 (v1.0: P0 — recut; LOIs suffice for Series A narrative, signed contracts are P1-critical revenue gate) | `INDEX.md` §5; `sales/SALES-PLAYBOOK.md` |

### §D. Pending vendor / supplier / dealer

Contract manufacturer relationships, second-source qualifications, and platform-vendor selections outstanding.

**Reconciliation:** Last cross-checked against `engineering/BOARD-FIX-SOW-RFP.md`, `BOM-VENDOR-PACKAGE.md`, `operations/WARRANTY-TRAINING.md`, `security/THREAT-MODEL.md`, `INDEX.md` §4 on **2026-08-05** · Owner initials: **MK** (interim, pending Head of Manufacturing Ops hire Q1 2027) · Cadence: **monthly**

| Item | Owner | Target date | Priority | Source |
|---|---|---|---|---|
| Sanmina Fremont board-fix SOW — first-article delivery | VP Engineering | Feb 2027 first articles (14-week SOW kickoff May 4 2026) | **P0** | `engineering/BOARD-FIX-SOW-RFP.md`; `INDEX.md` §4 claim #6 |
| Trail of Bits engagement — kickoff | Head of Security | Q2 2027 | P1 (v1.0: P0 — recut, same rationale as §A Trail of Bits audit) | See §A above; `INDEX.md` §5 |
| Bug bounty platform selection (HackerOne vs Intigriti) | Head of Security | Q4 2027 | P2 | `security/PRIVACY-COMPLIANCE-MANUAL.md` |
| CRM platform decision (HubSpot Starter → Salesforce Enterprise) | VP Sales + CFO | Q1 2027 evaluation; transition Q1 2028 at dealer scale | P1 | `operations/KPI-DASHBOARD-FRAMEWORK.md` §5 |
| Board portal selection (Diligent Boards vs Boardable) | Corporate Secretary | Q1 2027 (Diligent is the working default per `BOARD-MATERIALS-TEMPLATES.md`; final selection at Series A close) | P1 | `governance/BOARD-MATERIALS-TEMPLATES.md` |
| Foxlink Vietnam dual-source with Foxlink Malaysia | Head of Manufacturing Ops | Q3 2027 | P1 | `BOM-VENDOR-PACKAGE.md` §4 |
| Sanmina dual-source with Jabil or Flex | Head of Manufacturing Ops | Q2 2028 | P2 | `BOM-VENDOR-PACKAGE.md` §4 |
| Truly Semi Nantong second-source qualification (OLED disk) | Head of Manufacturing Ops | Q4 2027 | P1 | `BOM-VENDOR-PACKAGE.md` §4 |
| Nuvation Engineering standing agreement (Halbach signoff continuity) | VP Engineering | Q1 2027 | P1 | `engineering/BOARD-FIX-SOW-RFP.md`; `operations/WARRANTY-TRAINING.md` §14 |
| Decap lab selection for random-sample IC verification (HRTH-SEC-0151) | Head of Security | Q3 2027 | P2 | `security/THREAT-MODEL.md` §5 |
| Big-Four audit firm selection (E&Y vs Deloitte) | CFO | Series A close + 30 days | P1 | `INDEX.md` §5; §6 |
| SVB inventory-backed line of credit ($3M facility) — signed | CFO | Q1 2027 | P1 | `fundraise/FINANCIAL-MODEL-SENSITIVITY.md` §7.2; `INDEX.md` §4 claim #11 |

### §E. Pending international expansion

Per `international/EXPANSION-Y2-PLUS.md`. Timelines are aspirational and subject to Series B close and per-market certification schedules.

**Reconciliation:** Last cross-checked against `international/EXPANSION-Y2-PLUS.md` §2 + §regulatory, `security/PRIVACY-COMPLIANCE-MANUAL.md` §1, `INDEX.md` §5, `product/PRODUCT-ROADMAP-12-24MO.md` on **2026-08-05** · Owner initials: **MK** (interim, pending VP International hire Q3 2028) · Cadence: **quarterly**

| Item | Owner | Target date | Priority | Source |
|---|---|---|---|---|
| Canada + UK dealer network sign-up | VP International (or CEO pre-hire) | Q1 2028 | P1 | `international/EXPANSION-Y2-PLUS.md` §2 |
| UK LAI dealer network sign-up | VP International | Q1 2028 | P1 | `international/EXPANSION-Y2-PLUS.md` |
| Germany + Austria + Switzerland dealer network | VP International | Q2 2028 | P2 | `international/EXPANSION-Y2-PLUS.md` |
| Netherlands + Italy dealer network | VP International | Q3 2028 | P2 | `international/EXPANSION-Y2-PLUS.md` |
| UAE dealer network | VP International | Q1 2029 (revised from Q4 2028) | P3 | `international/EXPANSION-Y2-PLUS.md` |
| Singapore dealer network | VP International | Q1 2029 (revised) | P3 | `international/EXPANSION-Y2-PLUS.md` |
| Language localization (7 languages by Y3+) | Head of Product | Rolling through Y3+ | P2 | `product/PRODUCT-ROADMAP-12-24MO.md`; `international/EXPANSION-Y2-PLUS.md` |
| Per-market regulatory delta close (CE, UKCA, RCM, ISED, KC, BSMI) | VP Engineering | Rolling per market open; see §A above | P1-P3 by market | `international/EXPANSION-Y2-PLUS.md` §regulatory |
| GDPR + regional data-residency compliance mapping (per-egress-class) | Head of Privacy / DPO | Q4 2027 for EU launch enablement | P1 | `security/PRIVACY-COMPLIANCE-MANUAL.md` §1 |
| CEDIA international directory outreach | VP International (or VP Sales interim) | Begins Q2 2027 | P2 | `INDEX.md` §5; `international/EXPANSION-Y2-PLUS.md` |

### §F. Pending financial + capital

Capital-formation events, insurance, and CFO-owned financial infrastructure.

**Reconciliation:** Last cross-checked against `fundraise/SERIES-A-DECK.md`, `fundraise/POST-SERIES-B-STRATEGIC-OPTIONS-MEMO.md`, `governance/BOARD-GOVERNANCE.md` §8, `customer-success/HOUSEHOLD-STAFF-KIT.md` §8.7, `team/FOUNDER-MENTAL-HEALTH-PLAYBOOK.md`, `CHANGELOG.md` on **2026-08-05** · Owner initials: **MK** (interim, fractional CFO Preston Advisors until Q1 2028) · Cadence: **quarterly**

| Item | Owner | Target date | Priority | Source |
|---|---|---|---|---|
| Series A close ($10M primary, $50M post) | CEO | Q1 2027 term sheet; Q2 2027 close (10-week diligence) | **P0** | `fundraise/SERIES-A-DECK.md`; `INDEX.md` §1 |
| Series B close (~$30M primary at ~$300M post) | CEO + CFO | Q3 2028 (revised from Q1 2029 per `POST-SERIES-B-STRATEGIC-OPTIONS-MEMO`) | P1 | `fundraise/POST-SERIES-B-STRATEGIC-OPTIONS-MEMO.md`; `fundraise/SERIES-B-PITCH-OUTLINE.md` |
| $2M term life insurance policy on founder | CEO + CFO | Q1 2027 (pre-close) | P1 (v1.0: P0 — recut; $10M key-person is the strict Series A blocker, $2M term life is founder-personal risk mitigation) | `team/FOUNDER-MENTAL-HEALTH-PLAYBOOK.md` |
| $10M key-person policy on founder | CFO | Q1 2027 (Series A protective provision) | **P0** | `governance/BOARD-GOVERNANCE.md` §8 |
| $5M key-person policies on each C-suite hire | CFO | Q2 2027 (as each C-suite closes) | P1 | `governance/BOARD-GOVERNANCE.md` §8 |
| D&O insurance — initial bind and annual renewal | CFO | Bind Q1 2027; renew annually | **P0** | `governance/BOARD-GOVERNANCE.md` §8 |
| Product liability insurance (naming Hearth + household employer) | CFO | Q1 2027 ($10M rider per HOUSEHOLD-STAFF-KIT §8.7) | **P0** | `customer-success/HOUSEHOLD-STAFF-KIT.md` §8.7; `CHANGELOG.md` v1.2 |
| Cyber insurance | CFO | Q1 2027 | P1 | `governance/BOARD-GOVERNANCE.md` §8; `security/PRIVACY-COMPLIANCE-MANUAL.md` |
| E&O insurance | CFO | Q1 2027 | P2 | `governance/BOARD-GOVERNANCE.md` §8 |
| Monthly financial variance reports (filed to `docs/investor/fundraise/variance/YYYY-MM.md`) | Head of Finance / CFO | Ongoing monthly from Q2 2027 | P1 | `CHANGELOG.md` §Standing open items |
| Quarterly investor updates (filed to `docs/investor/comms/updates/YYYY-QN.md`) | Head of IR | Ongoing quarterly from Q2 2027 | P1 | `CHANGELOG.md` §Standing open items |

### §G. Pending product roadmap

Per `product/PRODUCT-ROADMAP-12-24MO.md`. Every deliverable maps to a specific hire and a specific quarter of Series A cash.

**Reconciliation:** Last cross-checked against `product/PRODUCT-ROADMAP-12-24MO.md`, `fundraise/SERIES-A-DECK.md` Slide 14, `fundraise/SERIES-B-PITCH-OUTLINE.md`, `security/THREAT-MODEL.md` §0 on **2026-08-05** · Owner initials: **MK** (interim, pending Head of Product hire Q2 2027) · Cadence: **quarterly**

| Item | Owner | Target date | Priority | Source |
|---|---|---|---|---|
| v1.0 pilot (10 units to LOI dealers, telemetry harness live) | VP Engineering | Q2 2027 | **P0** | `product/PRODUCT-ROADMAP-12-24MO.md`; `fundraise/SERIES-A-DECK.md` Slide 14 |
| v1.0 GA (600 units cumulative Y1) | VP Engineering | Q4 2027 | P1 (v1.0: P0 — recut; pilot is P0 ship gate, GA is P1 follow-on) | `product/PRODUCT-ROADMAP-12-24MO.md`; `SERIES-A-DECK.md` Slide 14 |
| v1.1 OTA — per-family personality tuning, Llama 4 model swap, 8TB NAS default, multi-Hearth mesh foundation | Head of Product | Q3 2027 | P1 | `product/PRODUCT-ROADMAP-12-24MO.md` |
| v1.2 — international SKU (230V, CE/UKCA/PSE), Matter/HomeKit/HA bridges, multilingual, multi-Hearth mesh | Head of Product | Q1 2028 (funded from Series B) | P1 | `product/PRODUCT-ROADMAP-12-24MO.md`; `SERIES-A-DECK.md` |
| v2.0 — 32B LLM, on-device video generation, face recognition, third-party developer program | Head of Product + CTO | Q4 2028 | P2 | `product/PRODUCT-ROADMAP-12-24MO.md`; `fundraise/SERIES-B-PITCH-OUTLINE.md` |
| Concierge SDK (extender fleet + third-party integrations) | Head of Product | Q3 2027 with v1.1 | P1 | `product/PRODUCT-ROADMAP-12-24MO.md` |
| mDNS hostname migration `pod.palpod.local` → `hearth.local` (HRTH-SEC-0161) | VP Engineering | v1.1 firmware release Q3 2027 | P2 | `security/THREAT-MODEL.md` §0 |

### §H. Pending measurement + research

Data-collection commitments that will convert modeled numbers into real numbers as the installed base grows.

**Reconciliation:** Last cross-checked against `VOC-MOCK-RESEARCH.md`, `fundraise/SERIES-A-DECK.md` Slides 5-8, `customer-success/ONBOARDING-PLAYBOOK.md`, `operations/KPI-DASHBOARD-FRAMEWORK.md`, `sales/SALES-PLAYBOOK.md` on **2026-08-05** · Owner initials: **MK** (interim, pending Head of CX hire Q1 2027) · Cadence: **quarterly**

| Item | Owner | Target date | Priority | Source |
|---|---|---|---|---|
| 23-persona VoC formal cohort tracking begins | Head of Customer Success | Q3 2027 (first GA cohort) | P1 | `VOC-MOCK-RESEARCH.md` |
| Cerulli $5M+ US HNW household count verification (currently 1.5M / 2023) | Head of IR | Q1 2027 (before Series A term sheet finalization) | P1 | `fundraise/SERIES-A-DECK.md` Slide 5 |
| WealthEngine methodology footnote refresh | Head of IR | Q1 2027 (already cited in SERIES-A-DECK Slide 6 methodology footnote) | P2 | `security/PRIVACY-COMPLIANCE-MANUAL.md` §2.3 |
| Consumer trade-dress survey | Head of IP + Head of Marketing | Q2 2028 | P2 | `legal/IP-ENFORCEMENT-PLAYBOOK.md` §4 |
| Post-install NPS baseline capture (Y1 GA customers) | VP CX | Begins Q1 2028 | P1 | `customer-success/ONBOARDING-PLAYBOOK.md`; `operations/KPI-DASHBOARD-FRAMEWORK.md` |
| Extender attach measurement (0.6 / 1.2 / 2.0 / 2.4 curve validation) | VP Sales + VP CX | Begins Q1 2028 | P1 | `sales/SALES-PLAYBOOK.md`; `SERIES-A-DECK.md` Slide 8 |
| 1-year retention capture | VP CX | Q1 2029 (first Y1-anniversary cohort) | P1 | `operations/KPI-DASHBOARD-FRAMEWORK.md` CX2 |
| 3-year retention capture | VP CX | Q1 2031 (first Y3-anniversary cohort) | P2 | `operations/KPI-DASHBOARD-FRAMEWORK.md` |
| Real deposit data + weekly waitlist growth (replaces modeled deposit assumptions in `FINANCIAL-MODEL-SENSITIVITY.md` §2) | Head of Growth | Q1 2027 onward — weekly for first 12 weeks post-air, then monthly | P1 (v1.0: P0 — recut; measurement commitment, not a close/ship/operate gate) | `CHANGELOG.md` §Standing open items |
| Y1 dealer signed count vs. plan (12 by Y1 end) | VP Sales / Head of Dealer | Ongoing measurement Q1 2027+ | P1 | `operations/KPI-DASHBOARD-FRAMEWORK.md` S3 |

### §I. Pending board + governance

**Reconciliation:** Last cross-checked against `governance/BOARD-GOVERNANCE.md`, `governance/BOARD-MATERIALS-TEMPLATES.md`, `security/PRIVACY-COMPLIANCE-MANUAL.md` §7, `INDEX.md` §5 on **2026-08-05** · Owner initials: **MK** (interim, pending Board Chair transition post-independent-director seating Q3 2027) · Cadence: **quarterly**

| Item | Owner | Target date | Priority | Source |
|---|---|---|---|---|
| Independent director recruit (Series A board seat 3) | Nom-Gov chair + CEO | Q3 2027 (post Series A close) | P1 | `governance/BOARD-GOVERNANCE.md` §2; `INDEX.md` §5 |
| Independent director recruit (Series B board seat 4) | Nom-Gov chair + CEO | Q3 2028 (with Series B close) | P2 | `governance/BOARD-GOVERNANCE.md` §2 |
| Annual board self-evaluation | Nom-Gov chair (via Diligent survey tool) | Every September | P1 | `governance/BOARD-GOVERNANCE.md` §10.1; `governance/BOARD-MATERIALS-TEMPLATES.md` |
| Annual board off-site | Board Chair + CEO | Q3 annually | P1 | `governance/BOARD-GOVERNANCE.md` |
| SOC 2 evidence binder (populated forward-looking) | Head of Security | Q1 2027 forward | P1 | `security/PRIVACY-COMPLIANCE-MANUAL.md` §7 |
| Trail of Bits published summary (90 days post critical/high remediation) | Head of Security | Rolling 90-day window post-audit | P1 | `security/PRIVACY-COMPLIANCE-MANUAL.md` §7 |
| Compensation Committee formation | Board Chair | Q2 2027 (post independent director seated) | P1 | `governance/BOARD-GOVERNANCE.md` §7 |
| Audit Committee formation | Board Chair + CFO | Q2 2027 | P1 | `governance/BOARD-GOVERNANCE.md` §7 |
| Nominating Committee formation | Board Chair | Q3 2028 (deferred to Series B stage per BOARD-GOVERNANCE §7) | P2 | `governance/BOARD-GOVERNANCE.md` §7 |

### §J. Data-room-level open items

Items that concern this data room as an artifact — updates, refreshes, and version-cut cadence.

**Reconciliation:** Last cross-checked against `CHANGELOG.md`, `INDEX.md`, `comms/POST-AIR-PR-PLAYBOOK.md`, `marketing/CES-2027-LAUNCH-PLAN.md`, `fundraise/POST-SERIES-B-STRATEGIC-OPTIONS-MEMO.md` on **2026-08-05** · Owner initials: **MK** (Head of IR, interim through Series B) · Cadence: **quarterly**

| Item | Owner | Target date | Priority | Source |
|---|---|---|---|---|
| `CHANGELOG.md` v1.3 update — with real Series A close entries | Head of IR | Q1 2027 | P1 | `CHANGELOG.md` §Governance & policy |
| Series A dataroom refresh with actual delivery numbers (post Q4 2027 Y1 GA close) | Head of IR | Q1 2028 | P1 | This document §5 |
| Series B dataroom open | Head of IR + CEO | Q2 2028 | P1 | `fundraise/POST-SERIES-B-STRATEGIC-OPTIONS-MEMO.md` |
| Post-air PR retrospective (30 days after Shark Tank air date) | Head of Marketing | Air date + 30 days | P1 | `CHANGELOG.md` §Standing open items; `comms/POST-AIR-PR-PLAYBOOK.md` §12 |
| CES 2027 booth build final CAD + AV run-of-show | Head of Marketing | Q4 2026 | P1 (v1.0: P0 — recut; marketing execution, not legal-to-operate gate) | `CHANGELOG.md` §Standing open items; `marketing/CES-2027-LAUNCH-PLAN.md` §5 |
| CES 2027 booth CAD sign-off (structural + electrical) | Head of Marketing + VP Engineering | Q4 2026 | P1 (v1.0: P0 — recut per §1.4) | `marketing/CES-2027-LAUNCH-PLAN.md` §5 |
| Monthly reconciliation of this document with git log + underlying source docs | Head of IR | First business day of each month | P1 | This document §5 |
| Big-Four audit report (FY2026) added to `docs/investor/fundraise/audit/` | CFO | Q3 2027 | P1 | `INDEX.md` §5 |
| Trail of Bits summary added to `docs/investor/security/audits/` | Head of Security | Rolling post-remediation window | P1 | `security/PRIVACY-COMPLIANCE-MANUAL.md` §7 |
| Sanmina program-manager reference calls (Ravi Menon) — LP-side scheduling | Head of IR | On LP request during diligence | P2 | `INDEX.md` §4 claim #6, §9 |
| Nuvation client-services reference calls — LP-side scheduling | Head of IR | On LP request during diligence | P2 | `INDEX.md` §4 claim #9 |
| Redacted dealer LOI PDFs (produced under NDA on request) | VP Sales | On LP request | P2 | `INDEX.md` §4 claim #5 |

### §K. Regulatory operations, tax, compliance ops (new in v1.1)

New in v1.1 per external diligence review — items called out as gaps in v1.0 coverage. Groups the regulatory-ops, tax-ops, and compliance-ops obligations that had been either scattered across source docs or mentioned but not operationalized. Every item here maps to a source doc reference or a "new" tag where the item exists in operational reality (payroll, tax filing) but was not previously in the master index.

**Reconciliation:** First cross-check against source docs (`hr/EXEC-COMP-FRAMEWORK.md`, `security/THREAT-MODEL.md`, `operations/WARRANTY-TRAINING.md`, `international/EXPANSION-Y2-PLUS.md`, `governance/BOARD-GOVERNANCE.md`, `product/PRODUCT-ROADMAP-12-24MO.md`) on **2026-08-05** · Owner initials: **MK** (interim, ownership disperses to CFO / GC / Head of Security once seated) · Cadence: **quarterly** (elevates to monthly once §K item volume exceeds 15)

| Item | Owner | Target date | Priority | Source |
|---|---|---|---|---|
| State tax + employment registrations by state (nexus tracking, payroll registration, sales-tax nexus determination, foreign qualification, workers-comp coverage per state) | Head of Finance / CFO (fractional Preston Advisors) | Rolling; initial multi-state footprint complete by Q2 2027; refresh on every new-hire-in-new-state event | P1 | New in v1.1; per remote team footprint (`hr/EXEC-COMP-FRAMEWORK.md`) + Y2 international §E |
| OSS license compliance operational tracking (SBOM per firmware release, automated license scanning in CI, attribution notice generation, obligation-tracker for copyleft components) | Head of Security | Automated pipeline live by Q1 2027; per-release audit thereafter; annual full-inventory reconciliation | P1 | `security/THREAT-MODEL.md`; `security/PRIVACY-COMPLIANCE-MANUAL.md`; succession memo §8 — operationalized here per verifier note |
| Warranty reserve accounting policy (per-unit accrual model, GAAP treatment under ASC 460, quarterly reforecast against actual claims curve) | CFO (fractional then full-time) | Policy documented by Q1 2027; first reforecast Q3 2027 (post-pilot claims data); quarterly thereafter | P1 | `operations/WARRANTY-TRAINING.md`; new in v1.1 |
| R&D tax credit filing cadence (federal §41 + California R&D credit + IRC §174 capitalization treatment + qualifying-activity documentation) | CFO + tax counsel (Cooley or PwC referral) | Annual filing cycle; first FY2026 return Q3 2027 alongside Big-4 audit; annual thereafter | P1 | New in v1.1 |
| Export controls / EAR classification (ECCN determination for hardware + firmware; TAA compliance if federal channel opens; encryption self-classification + BIS notification if applicable; end-user screening process) | Head of Security + GC (Q1 2028) | Initial ECCN determination by Q1 2027 (pre-international shipment); annual review; per-market screening operational by Q1 2028 | P1 | `international/EXPANSION-Y2-PLUS.md`; new in v1.1 per verifier note |
| 409A valuation refresh cadence (post-Series-A refresh, then annual or on material event — new round, secondary, material product milestone) | CFO + independent valuation firm (Carta 409A or Aranca) | Post-Series-A close (Q2 2027); annual thereafter; ad-hoc on material event | P1 | `hr/EXEC-COMP-FRAMEWORK.md`; new in v1.1 |
| ESPP framework (plan design, board + shareholder approval, IRC §423 qualification review, first enrollment window, ongoing administration) | CFO + Comp Committee | Design Q4 2027; board approval Q1 2028; first enrollment Q2 2028 (post-first-anniversary of Series A close) | P2 | `hr/EXEC-COMP-FRAMEWORK.md`; new in v1.1 |
| Secondary transaction policy (founder + early-employee liquidity windows, ROFR mechanics, tender-offer eligibility rules, information rights for secondary buyers) | GC + Board | Policy adopted with Series B close (Q3 2028); first tender window if any Q1 2029 | P2 | `governance/BOARD-GOVERNANCE.md`; new in v1.1 |
| Right-to-repair public commitments (published repair guide, 7-year parts availability window, tools/schematics/service-manual access, iFixit partnership pathway, per-jurisdiction R2R compliance for CA / NY / MN / EU) | Head of Product + Head of Marketing | Public commitment posted Q4 2027 pre-GA; parts-availability program live Q4 2027; annual reaffirmation with each roadmap update | P1 | `product/PRODUCT-ROADMAP-12-24MO.md`; Hearth positioning docs; new in v1.1 per verifier note (Hearth right-to-repair posture is a positioning claim and must be operationalized) |

---

## 3. Priority tier

Every open item in §2 carries a tier. The tier is not a claim about importance-in-general; it is a claim about **what the item blocks if it slips**. v1.1 rewrites the P0 definition to a strict interpretation — see §1.4 for the full reconciliation.

| Tier | Definition | Timeline | Item count (v1.1) |
|---|---|---|---|
| **P0 — Blocking (strict)** | Cannot close Series A / cannot ship v1.0 pilot / cannot legally operate. Strict interpretation. An item is P0 only if its slip breaks one of those three outcomes. | 6 months (must be closed by end of Q1 2027 for Series-A-adjacent items, or by v1.0 pilot ship Q2 2027 for ship-adjacent) | 10 items |
| **P1 — Critical** | Needs commitment within 12 months. A P1 slip does not kill the round or the ship, but a slip that stacks against another P1 slip becomes a P0 by co-occurrence. Includes items that were "very important" in v1.0's loose P0 usage. | 12 months (by end of Q3 2027) | 70 items |
| **P2 — Important** | 12–24 months timeline. These are the items a competent operating team is scheduled to close during Y2 execution, not raise-side items. | 12–24 months (by end of Q3 2028) | 26 items |
| **P3 — Nice-to-have** | >24 months timeline. These are items the data room discloses as planned but do not gate any near-term milestone. Included for LP transparency, not for near-term follow-up. | >24 months (Y3+) | 5 items |

**Total tracked items:** 111 (was 102 in v1.0; +9 from §K additions). Totals may drift by ±1-2 between versions of this document as items land, get reclassified, or new items surface from the source docs. The version-cut policy in §5 defines when reclassification happens.

**Rule for reclassification.** An item is upgraded (P2 → P1, P1 → P0) when the target date is within the tier's timeline window **and** the strict P0 definition (§1.4) is met at P0. An item is downgraded only when a documented decision moves the target date out or the strict definition no longer holds; a slipped date without a decision does not lower priority, it triggers an escalation per §4.

**Guardrail on P0 count.** If the P0 count exceeds 12 in any future revision, Head of IR must include a written justification in that version's CHANGELOG entry — the strict definition is designed to keep the count low, and drift above 12 is a signal that either the definition is being loosened or the company is in genuine crisis. Either way it warrants explicit disclosure rather than silent inflation.

---

## 4. Ownership matrix

Every open item in §2 has a primary owner. The primary owner is accountable to the board for delivery and to the LPs for status. The second-in-line owner is the accountability path if the primary is unavailable (vacation, illness, transition). The escalation path is where the item lands if second-in-line cannot close it either.

**New in v1.1:** the "Target fill by (second-in-line)" column is added for every function where the second-in-line seat is currently vacant or held by "Founder + TBD." This converts vacancies into tracked items rather than silent gaps — an approach called out by verifier as required to make Section 3 of the succession memo self-consistent.

| Function | Primary owner | Second in line | Target fill by (if second-in-line vacant / TBD) | Escalation to |
|---|---|---|---|---|
| Security certifications, third-party audits, SOC 2, ISO 27001, Trail of Bits, cyber insurance | Head of Security | CTO (Q1 2027 hire) | Head of Security hire Q1 2027; CTO hire Q1 2027 (both on same hire ramp) | CEO → Board Audit Committee Chair |
| Regulatory certifications (FCC, CE, UKCA, UL, RCM, ISED) | VP Engineering | Head of Manufacturing Ops | Head of Manufacturing Ops Q1 2027 | CEO → Board Chair |
| C-suite and IC hires | CEO (for C-suite); Head of HR (for IC) | Board Comp Committee Chair | Comp Committee formation Q2 2027 (per §I) | Board Chair |
| Legal — IP, corporate counsel, employment counsel | GC (Q1 2028) / Cooley (interim) | Head of IR (until GC in seat) | GC hire Q1 2028 | CEO → Board Chair |
| Legal — IP (Head of IP scope, post-GC) | Head of IP (or promoted GC scope) | GC | Head of IP hire Q1 2028 (CFO/GC hire cycle) | CEO → Board Chair |
| Vendor selection — CRM, board portal, bug bounty platform, dual-source qualification | Function head who owns the tool (VP Sales for CRM, Corporate Secretary for board portal, Head of Security for bug bounty) | CFO (for platform-cost decisions) | CFO full-time Q1 2028 (fractional Preston Advisors covers in interim) | CEO |
| Contract manufacturer relationships — Sanmina, Foxlink, Truly Semi, Nuvation | Head of Manufacturing Ops | VP Engineering | Head of Manufacturing Ops Q1 2027 | CEO → Board Chair (if Sanmina relationship at material risk) |
| International expansion — dealer network, certifications, GDPR mapping | VP International (Q3 2028) / CEO (interim) | VP Sales (for dealer signups pre-VP International hire) | VP International Q3 2028 | CEO → Board |
| Privacy — GDPR / UK-DPA / per-egress data residency | Head of Privacy / DPO (Q1 2028) / Head of Security (interim) | GC | Head of Privacy Q1 2028; GC Q1 2028 | CEO → Board Audit Committee Chair |
| Financial — Series A / B close, insurance, monthly variance, quarterly LP updates | CEO (for capital-raise); CFO (for insurance and variance); Head of IR (for LP updates) | Fractional CFO (Preston Advisors, until Q1 2028) | CFO full-time Q1 2028 | CEO → Board Chair |
| Financial ops — state tax, R&D credit, 409A refresh, ESPP, warranty reserve | CFO (fractional Preston Advisors then full-time) | Head of Finance (post-CFO-full-time promotion or hire) | CFO full-time Q1 2028; Head of Finance TBD (post-Series-B ramp, target Q3 2028) | CEO → Audit Committee Chair |
| Export controls / EAR classification | Head of Security + GC | VP Engineering (for ECCN technical determination) | GC hire Q1 2028; Head of Security Q1 2027 | CEO → Audit Committee Chair |
| Product roadmap — v1.0, v1.1, v1.2, v2.0 | Head of Product | VP Engineering | Head of Product hire Q2 2027 | CEO |
| Measurement + research — VoC, NPS, retention, extender attach | Head of CX (post-Q1 2027 hire) | Head of Growth | Head of CX Q1 2027; Head of Growth already in seat | CEO → Board (for board-KPI slippage) |
| Board + governance — director recruit, self-eval, off-site, committees, secondary policy | Board Chair / Nom-Gov chair | Corporate Secretary | Independent director Q3 2027 → Board Chair transition; Corporate Secretary role currently held by Head of IR (interim) | Independent director (once seated) → full board |
| Right-to-repair public commitment operations | Head of Product + Head of Marketing | Head of Customer Success | Head of Product Q2 2027; Head of Marketing already in seat; Head of CX Q1 2027 | CEO → Board |
| Data room — CHANGELOG, INDEX, this document, quarterly LP updates | Head of IR | Fractional CFO | Head of IR full-time post-Series-B (Q3 2028); fractional CFO covers in interim | CEO |

**Escalation cadence.** A P0 or P1 item that slips its target date without a documented decision to move the date triggers a written notice to the escalation path within 5 business days of the slip. A written notice includes: item, original target, revised target (or "cannot yet commit"), root cause, mitigating action, and the date of the next review. The written notice is appended to `CHANGELOG.md` under a `[Fixed]` or `[Legal]` tag as appropriate.

**Board reporting.** Every quarterly board packet includes a one-page "Open Items dashboard" summarizing the P0 and P1 items with red/yellow/green status against target date. The dashboard is generated from this document plus the Jira burn-down. See `governance/BOARD-MATERIALS-TEMPLATES.md` Tab 5 for the template.

**Vacancy-as-open-item.** The "Target fill by" column above is itself a set of tracked open items — a vacancy in a second-in-line seat is a governance risk, not a neutral fact. Head of IR reconciles the "Target fill by" column against §B (Pending hires) every quarter; a slip in §B automatically slips the corresponding "Target fill by" here, and vice versa.

---

## 5. Governance

**Owner.** Head of Investor Relations owns this document. Every change is a git commit against `docs/investor/OPEN-ITEMS-MASTER-INDEX.md` and is referenced in `CHANGELOG.md` under the appropriate change-type tag.

**Update cadence.** Monthly reconciliation against (a) the git log for `docs/investor/**`, (b) the underlying source docs for any items that landed in a source-doc revision, and (c) the internal Jira / Linear burn-down. The reconciliation is a first-business-day-of-the-month ritual, published to the data room by end-of-week-one of each month. **Per-category cadence:** §A-§D reconcile monthly (they are the P0-dense sections); §E-§K reconcile quarterly. Each category header carries a reconciliation checkbox with last-checked date, owner initials, and cadence — see per-section boxes throughout §2.

**Version policy.** A minor version bump (v1.0 → v1.1) when a batch of item statuses updates, dates slip, new items are added, or a tier definition is recut. A major version bump (v1.0 → v2.0) when the room itself reaches a milestone that reshapes the entire tracked list — Series A close (Q2 2027), first GA ship (Q4 2027), Series B close (Q3 2028) each get a major bump.

**v1.1 change summary (this version):** P0 tier definition recut to strict interpretation (§1.4); 17 items moved from P0 to P1; §K added (9 new items covering state tax, OSS license compliance, warranty reserve accounting, R&D credit, export controls, 409A cadence, ESPP, secondary transaction policy, right-to-repair); reconciliation checkboxes added to every category header (§A-§K); "Target fill by" column added to §4 ownership matrix for vacant second-in-line seats. All changes are documented in `CHANGELOG.md` v1.2 → v1.3 entry.

**Add / close policy.** An item is added the moment it is knowable and dated in a source doc. An item is closed the moment it is fulfilled (SOC 2 attestation received, CFO seated, FCC certification granted, dealer contract signed) with a `[Fixed]` entry in the concurrent `CHANGELOG.md` version. Closed items move to a hidden archive at the bottom of this file (not deleted — a diligence associate asking "did you ever have a SOC 2 gap?" deserves an honest yes-with-the-date).

**Cross-references.** Every row cites the source doc where the item is described in full. If a source doc is deprecated or replaced, this document is updated within 48 hours of the source-doc change. `INDEX.md` §5 (known open items and gaps) is the LP-facing narrative summary of the same list; `CHANGELOG.md` §Standing open items is the changelog-side summary. This document is the operational source of truth — if the three drift, this one wins and the other two are reconciled to it.

**Confidentiality.** Same posture as the rest of the data room: single copy per LP under mutual NDA, marketing use prohibited, no forwarding to co-investors or deal-sharing platforms. The list of pending hires in §B in particular is competitively sensitive and must not leave a controlled diligence context.

**Rule of honest disclosure.** If a diligence associate finds an open item that is not on this list, that is a defect in this document — not a defect in Hearth. The associate is encouraged to email `dataroom@hearth.co` with the finding; Head of IR will add the item within 24 hours and issue a `[Fixed]` entry in `CHANGELOG.md`. This is not a rhetorical invitation; it has already happened twice during v1.0 authoring and once (P0 tier recut) between v1.0 and v1.1 — and is the mechanism by which the document stays honest.

---

## 6. Cross-reference index

For quick lookup: every open item in this document appears in at least one of the following source locations. If an item does not trace to a source, escalate to Head of IR.

- **`INDEX.md` §5 (Known open items and gaps)** — LP-facing narrative summary; a subset of items here, less structured.
- **`CHANGELOG.md` §Standing open items** — dated, owner-attributed table of expected changes; overlaps with §A, §D, §F, §J here.
- **`security/THREAT-MODEL.md`** — all `HRTH-SEC-####` items (0121, 0140, 0142, 0143, 0144, 0145 closed, 0146, 0147, 0148, 0149, 0150, 0151, 0152, 0153, 0154, 0155, 0156, 0157 closed, 0158, 0161); §A, §D, and §K OSS/EAR.
- **`security/PRIVACY-COMPLIANCE-MANUAL.md`** — SOC 2, ISO 27001, Trail of Bits, per-egress GDPR mapping; §A, §E, §K OSS.
- **`fundraise/SERIES-A-DECK.md`** — close timeline, milestones, Y1/Y2 revenue targets; §F and §G.
- **`fundraise/SERIES-B-PITCH-OUTLINE.md`** and **`fundraise/POST-SERIES-B-STRATEGIC-OPTIONS-MEMO.md`** — Series B timeline (revised from Q1 2029 to Q3 2028); §F, §K secondary policy.
- **`product/PRODUCT-ROADMAP-12-24MO.md`** — v1.0 → v2.0 milestones; §G, §K right-to-repair.
- **`international/EXPANSION-Y2-PLUS.md`** — per-market timelines, dealer recruitment, certification deltas, export-controls scope; §E, §K EAR.
- **`team/FOUNDER-NARRATIVE.md`** and **`team/FOUNDER-MENTAL-HEALTH-PLAYBOOK.md`** — founder-side items, hire ramp; §B and §F.
- **`legal/IP-ENFORCEMENT-PLAYBOOK.md`** — patent conversion, trademark, trade dress, named-counsel verification; §C.
- **`customer-success/HOUSEHOLD-STAFF-KIT.md`** and **`customer-success/ONBOARDING-PLAYBOOK.md`** — household-employer MSA, product-liability rider, staff-injury protocol; §C and §F.
- **`governance/BOARD-GOVERNANCE.md`** and **`governance/BOARD-MATERIALS-TEMPLATES.md`** — board composition, committees, self-eval, off-site, insurance, secondary transaction policy; §I and §K.
- **`hr/EXEC-COMP-FRAMEWORK.md`** — all hires and comp bands, 409A refresh cadence, ESPP framework, multi-state payroll; §B and §K.
- **`operations/KPI-DASHBOARD-FRAMEWORK.md`** — CRM platform decision, dashboards, measurement commitments; §D and §H.
- **`operations/WARRANTY-TRAINING.md`** — Nuvation standing agreement, Halbach signoff continuity, warranty reserve accrual model; §D and §K warranty reserve.
- **`operations/MEDIA-IMPORT-RUNBOOK.md`** — Kaleidescape licensing, Legacybox/iMemories partner selection; §C.
- **`engineering/BOARD-FIX-SOW-RFP.md`** — Sanmina Fremont SOW delivery, Nuvation standing agreement; §D.

---

## 7. Contact

- **Mark Kirk (CEO)** — mark@hearth.co
- **Head of Investor Relations** — Mark Kirk (interim; role planned to hire post-Series B) — dataroom@hearth.co
- **Data room and diligence questions** — dataroom@hearth.co (routes to Mark and Preston Advisors)
- **Board Chair** — Mark Kirk (interim); post-independent-director seating (Q3 2027), Chair role transitions per `governance/BOARD-GOVERNANCE.md` §2

---

*End of OPEN-ITEMS-MASTER-INDEX.md — v1.1 — 2026-08-05*
*Next scheduled reconciliation: 2026-09-01*

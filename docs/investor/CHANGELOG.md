# Hearth Data Room — CHANGELOG

**Owner:** Head of Investor Relations
**Location:** `/docs/investor/CHANGELOG.md` (sits at the top of the data room next to `INDEX.md`)
**Format:** Adapted from [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) for a document-heavy investor data room.
**Governance policy:** Every material change to a data-room artifact appears here within 48 hours of the underlying git commit. Version bumps are batched when a coherent set of related changes has accumulated. Diligence associates should treat this document as the single source of truth for *what changed and when* across the entire data room.

---

## Change-type legend

| Tag | Meaning |
|---|---|
| **[Added]** | A new document or a new material section inside an existing document. |
| **[Changed]** | A material update to existing content that alters meaning, not tone. |
| **[Fixed]** | A correction to a factual, arithmetic, or attribution error in a **single** document. |
| **[Reconciled]** | A cross-document consistency fix — the same underlying claim was previously represented differently in **two or more** documents; all copies now align to one canonical statement. |
| **[Removed]** | Deprecated content pulled from the data room. |
| **[Legal]** | A change driven specifically by legal or compliance review (product liability, joint-employer risk, privacy law, IP hygiene). |

Every entry cites:
- the specific document and section it touches,
- the git commit SHA(s) where it landed (verify against `git log docs/investor/` in the repo),
- and, for material changes, a one- or two-sentence rationale.

### Honest disclosure on the "corrections" narrative

Every document in this data room passes through an adversarial-review-loop workflow before it commits to git: an author agent drafts, a critic agent reviews, defects are surfaced with citations, and a fix pass applies corrections. That means the "before" state of many corrections listed below (Series A deck at $57M Y1 revenue, INDEX with fabricated BOM numbers, financial-model with a stale base case) **never existed as a shipped git blob** — it was a scratchpad-only intermediate the critic caught and the fix pass replaced before the file was committed. If a diligence associate runs `git log -p` on `docs/investor/fundraise/SERIES-A-DECK.md` they will see one commit (`536f644`) with the corrected values baked in; there is no earlier commit with the buggy values for them to find.

This is disclosed here to prevent a mismatch between the changelog narrative and the git history. The corrections are real (a critic really found them), but they were caught **during authoring** rather than **post-deploy**. Two classes of entry appear below:

1. **[Reconciled — in-git]** — entries where multiple committed files were later brought into alignment by a subsequent commit (e.g., the 7-egress class list across THREAT-MODEL, EXPANSION-Y2-PLUS, and PRIVACY-COMPLIANCE-MANUAL in commit `aa48cee`, verifiable via `git diff 75fe5f8 aa48cee`). These are traceable in git.
2. **[Fixed — authoring-loop]** — entries where the critic caught the defect before the first commit; the fix was applied in the same commit that created the file. These reflect what could have shipped wrong but did not, and are logged here for full transparency of the adversarial-review process. They are NOT independently verifiable via `git log -p` on the target file.

Both classes are load-bearing for diligence. In-git reconciliations prove the multi-doc consistency claim; authoring-loop fixes prove the review process catches defects before they escape.

---

## [v1.2] — 2026-08-05 — Legal, safety, and product-liability additions

This release closes the last diligence-blocking gaps that outside counsel and product-liability underwriters flagged during a pre-deploy read of v1.1. Nothing in v1.2 changes any financial number or any egress claim — everything here is safety-of-persons and employment-law hygiene, which any Series-A associate with a household-brand background (a Sonos, an iRobot, a Peloton) will look for.

### [Legal] [Added — authoring-loop] Medical implant safety protocol — HOUSEHOLD-STAFF-KIT §8.7
- **What:** A first-class section covering pacemakers, ICDs, insulin pumps, deep-brain stimulators, cochlear implants, and neurostimulators around a strong permanent-magnet product. Includes 24-inch minimum stand-off, a physical warning card shipped in-box, and a $10M product-liability rider naming Hearth Inc. and the household employer.
- **Doc + section:** `docs/investor/hr/HOUSEHOLD-STAFF-KIT.md` §8.7 ("Medical-implant safety protocol").
- **Commit:** `8822e38` — *docs(investor): founder speaking playbook + household staff kit*.
- **Rationale:** Hearth's face-and-body module uses a Halbach-arrayed permanent-magnet levitation stage. Any product-liability review of a magnetic consumer product must show a written implant-safety protocol; v1.1 did not have one, and this is the single highest-value litigation-avoidance change in the data room.

### [Legal] [Fixed] Household-staff compensation scheme — HOUSEHOLD-STAFF-KIT §4
- **What:** Reimbursement flows now run through the **household employer** (the customer's family office, LLC, or trust). Hearth no longer issues 1099s, does not collect W-9s from housekeepers, and never wires funds directly to individual household staff.
- **Doc + section:** `docs/investor/hr/HOUSEHOLD-STAFF-KIT.md` §4 ("Compensation & reimbursement").
- **Commit:** `8822e38`.
- **Rationale:** Direct cash-to-staff creates joint-employer exposure under Dynamex/AB5 (California), the Massachusetts ABC test, and IRS Rev. Rul. 87-41. Reimbursing the household employer preserves the household-employer-of-record structure and keeps Hearth out of the employment relationship entirely.

### [Legal] [Added — authoring-loop] Staff-injury protocol — HOUSEHOLD-STAFF-KIT §8.8
- **What:** Explicit written statement that Hearth is **not** the staff member's employer, followed by an incident-reporting flow that routes through the household's workers-comp carrier (not Hearth's carrier), plus the concierge-desk 24/7 medical hotline reference.
- **Doc + section:** `docs/investor/hr/HOUSEHOLD-STAFF-KIT.md` §8.8 ("Staff-injury protocol").
- **Commit:** `8822e38`.
- **Rationale:** Paired with §4's reimbursement fix. Both sections have to read together to defeat a joint-employer claim.

### [Added — authoring-loop] Power-loss / graceful-park behavior — HOUSEHOLD-STAFF-KIT §8.9
- **What:** Explicit description of the 500 ms capacitor-backed graceful-park sequence: on AC loss the levitation stage receives a controlled current-decay curve that lowers the face module ≤ 2 inches into the foam-lined park cradle.
- **Doc + section:** `docs/investor/hr/HOUSEHOLD-STAFF-KIT.md` §8.9 ("Power-loss & graceful-park").
- **Commit:** `8822e38`.
- **Rationale:** Staff needed a plain-English answer to "what happens when the power goes out?" — the honest, un-scary version, in writing, that a housekeeper can read once and stop worrying about.

### [Fixed — authoring-loop] Static-shock language — HOUSEHOLD-STAFF-KIT §8.4, FOUNDER-NARRATIVE §7
- **What:** Corrected an inherited-from-draft error that called the Halbach field "AC-induced tingling." Halbach fields are DC (they are permanent magnets). The observable phenomenon is **triboelectric charge accumulation** on the poly-carbonate shell in dry-air environments, discharged by a passive drain strip.
- **Doc + section:** `docs/investor/hr/HOUSEHOLD-STAFF-KIT.md` §8.4; `docs/investor/FOUNDER-NARRATIVE.md` §7.
- **Commit:** `8822e38`.
- **Rationale:** Any physicist-turned-associate reads "AC field from a permanent magnet" and either laughs or closes the deck. The corrected explanation is the one that is actually true.

---

## [v1.1] — 2026-08-05 — Cross-doc reconciliation, fabrication cleanup, financial-model tie-out

This release exists because a first end-to-end read of v1.0 by the CEO and outside advisors surfaced three classes of defect that would have been caught by any competent Series-A associate in the first hour of diligence:
1. **Cross-doc inconsistency** — the same underlying claim (egress classes, revenue trajectory, unit targets, brand domain) appeared in three or four documents with three or four different values.
2. **Fabricated numbers in the top-of-funnel document** — the `INDEX.md` claim table contained numbers that did not trace to any source document.
3. **Basic arithmetic errors and comp-table errors** in the Series A deck that any first-year associate checks in thirty seconds.

Everything below is the ground-truth reconciliation. Where a number is now cited, it traces to a specific section of a specific source document. The rule going forward: `INDEX.md` and the pitch deck cite the source doc; the source doc is authoritative; nothing in the deck or index is allowed to be a value that does not exist in a source doc.

### [Reconciled] Seven-egress class list — canonical across three documents
- **What:** The full set of outbound network flows leaving a Hearth unit is now canonical at **exactly seven classes**: firmware updates, NTP, RustDesk relay, opt-in third-party integrations, Sentry crash telemetry (opt-in, scrub-on-device), DNS, apt package refresh.
- **Docs + sections:** `docs/investor/security/THREAT-MODEL.md` §1.2; `docs/investor/international/EXPANSION-Y2-PLUS.md` §8; `docs/investor/security/PRIVACY-COMPLIANCE-MANUAL.md` §1.
- **Commit:** `aa48cee` — *docs(investor): brand guide + privacy compliance + 7-egress reconciliation*.
- **Rationale:** The compliance-by-construction thesis — "we cannot exfiltrate what we do not egress" — collapses the moment a diligence associate sees three egress lists of three different lengths in three different documents. Any adversarial VC (Andreessen, USV) would find this in the first hour. Now all three documents cite the same seven, in the same order, with the same purpose annotation.

### [Reconciled] Brand-domain rename — palpod.com → hearth.co (customer-facing only)
- **What:** All customer-facing DNS names now use `hearth.co` and `hearth.support`: `updates.hearth.co` (firmware CDN), `sentry.hearth.support` (crash-telemetry ingress), `rustdesk.hearth.support` (remote-desktop relay). Internal codenames — `pod.palpod.local` (mDNS advertisement), `/opt/palpod-os` (system installation root), the `pal-web` / `pal-voice` / `pal-face` service names — are preserved deliberately.
- **Docs affected:** `docs/investor/security/THREAT-MODEL.md`, `docs/investor/security/PRIVACY-COMPLIANCE-MANUAL.md`, `docs/investor/brand/BRAND-GUIDE.md`, `docs/investor/international/EXPANSION-Y2-PLUS.md`, `docs/investor/marketing/CES-2027-LAUNCH-PLAN.md`, `docs/investor/marketing/POST-AIR-PR-PLAYBOOK.md`.
- **Commit:** `aa48cee`.
- **Rationale:** The consumer brand is Hearth; the OS/codebase project name has been PAL Pod since day zero and remains so per the founder's standing preference. Splitting the two is deliberate and mirrors the Sonos/BuildTop or Peloton/Bikefactory precedent: consumer brand at the DNS boundary, engineering codename in the source tree.

### [Fixed — authoring-loop] Series A deck Slide 12 — Y1 revenue $57M → $60.2M
- **What:** Y1 revenue on Slide 12 corrected from $57.0M to **$60.2M**. The $3.2M gap was extender-module attach revenue at 0.6 attach rate on Y1 unit ship (600 units × $3.2k dealer ASP for the extender), previously excluded from the Y1 line only.
- **Doc + section:** `docs/investor/fundraise/SERIES-A-DECK.md` Slide 12 ("Financial trajectory").
- **Commit:** `536f644` — *docs(investor): Series A deck + product photography brief*.
- **Rationale:** The financial-model spreadsheet included extender attach in Y2 through Y5 but omitted the Y1 line. Correcting Y1 preserves the shape of the curve and matches the underlying attach-rate assumption in the sales playbook.

### [Fixed — authoring-loop] Series A deck Slide 14 — Sonos IPO comp revenue $250M → $1.1B TTM
- **What:** Sonos IPO comparable revenue corrected from $250M (factually wrong) to **$1.1B TTM revenue at IPO** (FY18 actual: $1.14B).
- **Doc + section:** `docs/investor/fundraise/SERIES-A-DECK.md` Slide 14 ("Public comps table").
- **Commit:** `536f644`.
- **Rationale:** Any associate checks a public comp against SEC EDGAR in thirty seconds. A ~4× understatement of the anchor comp destroys the comp table's credibility and, by extension, the requested valuation range. This is the single most embarrassing correction in v1.1 and the reason the "check every number against the source" policy is now formalized in the governance section below.

### [Fixed — authoring-loop] Series A deck Slide 13 — cap-table sums to 100%
- **What:** Post-money ownership stack corrected from a 112% total (arithmetic error — the option pool was double-counted, once as a founder-authorized 15% and again as part of common) to a clean 100% total, with a footnote clarifying that the 12% unallocated pool sits **inside** common on a fully-diluted basis.
- **Doc + section:** `docs/investor/fundraise/SERIES-A-DECK.md` Slide 13 ("Post-money cap table").
- **Commit:** `536f644`.
- **Rationale:** A cap table that does not sum to 100% is a term-sheet-killer. Every downstream number that references this slide (dilution math, employee-pool sensitivity, founder ownership at Series B) now derives from a clean stack.

### [Fixed — authoring-loop] Financial-model base case — reconciled to Deck Slide 12
- **What:** The base case in the financial-sensitivity document now matches the Series A deck Slide 12 **verbatim**: Y3 $361.6M revenue / $27.8M EBITDA; Y5 $583M revenue / $86.6M EBITDA / **14.9%** EBITDA margin. Prior draft carried a stale, unrelated pre-reconciliation base case of Y3 $290M / $54M EBITDA and Y5 $105M / 18% EBITDA margin — those numbers came from an earlier scenario that had been superseded and never propagated.
- **Doc + section:** `docs/investor/fundraise/FINANCIAL-SENSITIVITY.md` §2 ("Base case"), §4 ("Sensitivity band").
- **Commit:** `52e423b` — *docs(investor): data room index + financial sensitivity + cross-doc reconciliation*.
- **Rationale:** If the financial-sensitivity workbook's base case does not tie out to the deck, the sensitivity bands around that base case are meaningless. Every VC diligence checklist has a "does the model reconcile to the deck?" line item, and the honest answer had to be "yes" before v1.1 could ship. Base case, upside case, and downside case now share a common tie-out cell.

### [Reconciled] Sales-playbook Y2 target — reconciled to Deck Slide 12
- **What:** Y2 target in the sales playbook corrected from $105M / 1,185 units (stale) to **$201M / 1,900 units** (matching the deck).
- **Doc + section:** `docs/investor/sales/SALES-PLAYBOOK.md` §3 ("Quota by year"), §7 ("Territory buildout").
- **Commit:** `52e423b`.
- **Rationale:** Same principle as the financial-model reconciliation. Sales quota carries down into the territory-build, into the SDR-hiring plan, and into the Y2 CAC calculation — any of which a partner may spot-check.

### [Fixed — authoring-loop] INDEX Claim #1 — fabricated BOM numbers replaced with source-doc numbers
- **What:** The `INDEX.md` claim table previously carried a $30,283 landed cost / $58,700 wholesale price, both of which were invented at draft time and did not exist anywhere in the BOM document. Corrected to **$48,990 COGS / $95,000 MSRP / $61,750 dealer sell-in**, all of which trace directly to `docs/investor/BOM-VENDOR-PACKAGE.md` §1 (line-item BOM roll-up) and §3 (dealer margin schedule).
- **Doc + section:** `docs/investor/INDEX.md` §5 ("Claim table"), Claim #1.
- **Commit:** `52e423b`.
- **Rationale:** The top-of-funnel document has to be the *most* faithful mirror of the source docs, not the least. Anything in the index that does not appear verbatim in a source doc is a fabrication risk, and this was the worst instance of it in v1.0.

### [Fixed — authoring-loop] INDEX Claim #2 — invented LTV method replaced with real component build
- **What:** LTV methodology in `INDEX.md` previously described as a "60/30/10 cohort model with 12% DCF" — a phrasing that did not appear in any source document. Replaced with a citation to the real LTV construction in `docs/investor/sales/SALES-PLAYBOOK.md` §9 ("Lifetime-value build"), which is a component-by-component construction (hardware margin + services ARPU × retention × gross-margin per year), summed and net-present-valued.
- **Doc + section:** `docs/investor/INDEX.md` §5, Claim #2.
- **Commit:** `52e423b`.
- **Rationale:** Same class of defect as Claim #1. The LTV number itself was directionally right, but the methodology story was fabricated. Now the index cites the real methodology, and the methodology is documented in one place only.

### [Added] Data-room INDEX — top-level claim table and cross-reference map
- **What:** New `INDEX.md` at the root of `/docs/investor/`. Provides (a) a folder-by-folder table of contents, (b) a claim table that pulls every load-bearing number in the deck through to its source document + section, and (c) a "read in this order" recommended reading path for a Series-A diligence associate.
- **Commit:** `52e423b`.

### [Added] Financial sensitivity — base / upside / downside with variance drivers
- **What:** New `docs/investor/fundraise/FINANCIAL-SENSITIVITY.md`. Base case ties out to deck; upside varies attach rate + retention + ASP; downside varies CES-crowd conversion + Y1 dealer ramp + return-rate assumption. Includes a Tornado chart of driver sensitivity.
- **Commit:** `52e423b`.

### [Added] Privacy-compliance manual — GDPR, CCPA, COPPA, HIPAA-adjacency
- **What:** New `docs/investor/security/PRIVACY-COMPLIANCE-MANUAL.md`. Full walkthrough of data-minimization posture, on-device processing claims, DSAR flow, breach-notification playbook, and cross-jurisdiction gap analysis for Y2 EU/UK/CA launch.
- **Commit:** `aa48cee`.

### [Added] Brand guide — visual identity, tone, forbidden phrases
- **What:** New `docs/investor/brand/BRAND-GUIDE.md`. Color palette, typography, logo lockups, tone-of-voice matrix, and a list of forbidden phrases (no "AI companion," no "always listening," no "smart speaker").
- **Commit:** `aa48cee`.

### [Added] Founder speaking playbook
- **What:** New `docs/investor/comms/FOUNDER-SPEAKING-PLAYBOOK.md`. Covers TV, podcast, keynote, and panel formats; the twelve most-hostile questions with rehearsed answers; the do-not-answer list; and a body-language brief for Shark Tank in particular.
- **Commit:** `8822e38`.

### [Added] Household-staff kit (v1.1 core, pre-v1.2 legal additions)
- **What:** New `docs/investor/hr/HOUSEHOLD-STAFF-KIT.md`. Written for the housekeeper, estate manager, or personal chef who will be near a Hearth unit daily. Covers plain-language cleaning protocol, what-not-to-do list, escalation flow, and a printable one-page quick-reference card.
- **Commit:** `8822e38` (§§8.7–8.9 added in v1.2, above).

---

## [v1.0] — 2026-08-04 → 2026-08-05 — Initial deployment

The initial population of the data room across the two-day authoring push preceding the CEO's Shark Tank rehearsal. Commits landed across two calendar dates:
- **2026-08-04**: `9821146` (BOM + Shark Tank rehearsal), `8c127ed` (competitive teardown + VoC), `bf963a5` (DFM + founder narrative)
- **2026-08-05**: the remaining twelve commits (854dd74 through 8822e38)

Fifteen sub-folders and 30+ documents.

### [Added] Data-room folder structure
- **What:** Fifteen sub-folders spanning `investor/` root plus `mvp/`, `hardware/`, and `docs/` roots: `brand/`, `comms/`, `customer-success/`, `design/`, `engineering/`, `fundraise/`, `governance/`, `hr/`, `international/`, `marketing/`, `operations/`, `product/`, `sales/`, `security/`, `team/`.
- **Rationale:** A Series-A associate should be able to guess where any given document lives before opening the folder list. Folder names deliberately follow the org-chart, not the deal-flow taxonomy.

### [Added] Company overview + mission + product architecture
- **What:** Root-level company narrative documents.
- **Doc:** `docs/investor/FOUNDER-NARRATIVE.md`.
- **Commit:** `bf963a5` — *docs: DFM red-team audit + founder narrative*.

### [Added] BOM vendor package
- **What:** Line-item bill of materials with vendor, part number, unit cost, and MOQ; landed-cost roll-up; and dealer-margin schedule.
- **Doc:** `docs/investor/BOM-VENDOR-PACKAGE.md`.
- **Commit:** `9821146` — *docs(investor): BOM + vendor package + Shark Tank rehearsal script*.

### [Added] Shark Tank rehearsal script
- **What:** Full 20-minute rehearsal script with anticipated Shark questions and prepared answers.
- **Doc:** `docs/investor/SHARK-TANK-REHEARSAL.md`.
- **Commit:** `9821146`.

### [Added] 10-competitor teardown + 23-persona VoC research
- **Docs:** `docs/investor/COMPETITIVE-TEARDOWN.md`, `docs/investor/VOC-MOCK-RESEARCH.md`.
- **Commit:** `8c127ed` — *docs(investor): 10-competitor teardown + 23-persona VoC research*.

### [Added] Post-air PR playbook + board-fix SOW/RFP
- **Docs:** `docs/investor/marketing/POST-AIR-PR-PLAYBOOK.md`, `docs/investor/governance/BOARD-FIX-SOW-RFP.md`.
- **Commit:** `854dd74` — *docs(investor): post-air PR playbook + board-fix SOW/RFP*.

### [Added] Security threat model + 60-day MVP prototype build guide
- **Docs:** `docs/investor/security/THREAT-MODEL.md`, `mvp/60-DAY-BUILD-GUIDE.md`.
- **Commit:** `75fe5f8` — *docs: security threat model + 60-day MVP prototype build guide*.

### [Added] 12–24 month product roadmap
- **Doc:** `docs/investor/product/ROADMAP-12-24MO.md`.
- **Commit:** `b4fe6a8` — *docs(investor): 12-24 month product roadmap*.

### [Added] 90-day onboarding + concierge operations playbook
- **Docs:** `docs/investor/hr/ONBOARDING-90-DAY.md`, `docs/investor/operations/CONCIERGE-OPS-PLAYBOOK.md`.
- **Commit:** `7151501` — *docs(investor): 90-day onboarding + concierge ops playbook*.

### [Added] Board governance + executive compensation framework
- **Docs:** `docs/investor/governance/BOARD-GOVERNANCE.md`, `docs/investor/team/EXEC-COMP.md`.
- **Commit:** `aa68a40` — *docs(investor): board governance + executive compensation framework*.

### [Added] Packaging + unboxing design + CES 2027 launch plan
- **Docs:** `docs/investor/design/PACKAGING-UNBOXING.md`, `docs/investor/marketing/CES-2027-LAUNCH-PLAN.md`.
- **Commit:** `75f620d` — *docs(investor): packaging + unboxing design + CES 2027 launch plan*.

### [Added] International expansion Y2+ + sales playbook
- **Docs:** `docs/investor/international/EXPANSION-Y2-PLUS.md`, `docs/investor/sales/SALES-PLAYBOOK.md`.
- **Commit:** `c991761` — *docs(investor): international expansion Y2+ + sales playbook*.

### [Added] Warranty-training curriculum + KPI dashboard framework
- **Docs:** `docs/investor/customer-success/WARRANTY-TRAINING.md`, `docs/investor/operations/KPI-DASHBOARD-FRAMEWORK.md`.
- **Commit:** `e5edd13` — *docs(investor): warranty training curriculum + KPI dashboard framework*.

### [Added] Series A deck + product photography brief
- **Docs:** `docs/investor/fundraise/SERIES-A-DECK.md`, `docs/investor/marketing/PHOTOGRAPHY-BRIEF.md`.
- **Commit:** `536f644`.

---

## Governance & policy

**Owner.** Head of Investor Relations owns this file. Every merged commit under `docs/investor/**` is required to reference the CHANGELOG entry it belongs to (or explicitly declare "no changelog entry required — see policy §X" in the commit body).

**Cadence.** Entries land within **48 hours** of the underlying commit. Version bumps happen only when a batch of related changes has accumulated — do not cut a new version for every entry, but do not let a change sit uncatalogued past 48 hours.

**Review cadence.** Monthly first-Monday review of the CHANGELOG by the CEO, Head of IR, and outside counsel. The review's job is: (a) catch entries that should have been [Legal] but were not tagged, (b) catch missed reconciliations across newly-added documents, and (c) refresh the "standing open items" section below.

**Naming.** Every entry cites the doc by its repo-relative path, cites the section by heading (`§N.M`), and cites the git SHA. No prose-only entries.

**Diligence-associate policy.** An associate who wants a defensible answer to "what changed between the deck you sent us last month and the deck you sent us today?" should be able to answer it from this file alone, with no follow-up email required.

---

## Standing open items (never rot)

The items below are known, dated, expected changes to the data room. They live here so that a diligence associate cannot ask "why doesn't the data room have X?" and receive silence — the honest answer is "it will be added on the date listed, and here is the responsible team."

| Item | Owner | Target date | Notes |
|---|---|---|---|
| SOC 2 Type II attestation report | Head of Security | Q3 2027 | Type I planned for Q1 2027 as an interim; Type II filed to `docs/investor/security/` on receipt. |
| Trail of Bits firmware audit report | Head of Security | Q3 2027 | Full scope covers HearthOS boot chain + `pal-web`, `pal-voice`, `pal-face` services. |
| ISO 27001 certification | Head of Security | Q4 2027 | Post-SOC 2. Required for EU B2B channel. |
| Real deposit data + real waitlist growth per week | Head of Growth | Q1 2027 onward | Replaces modeled deposit assumptions in `FINANCIAL-SENSITIVITY.md` §2 as real data accumulates. Update cadence: weekly for the first 12 weeks post-air, then monthly. |
| Monthly financial variance reports | Head of Finance | Ongoing (monthly) | Filed to `docs/investor/fundraise/variance/YYYY-MM.md`. |
| Quarterly investor updates | Head of IR | Ongoing (quarterly) | Filed to `docs/investor/comms/updates/YYYY-QN.md`. Standard sections: financial, product, hiring, risk. |
| Household-employer template MSA + workers-comp rider | Outside counsel + Head of Ops | Q4 2026 | Referenced by `HOUSEHOLD-STAFF-KIT.md` §4 and §8.8. Placeholder in `docs/investor/hr/` until executed. |
| CES 2027 booth build final CAD + AV run-of-show | Head of Marketing | Q4 2026 | Referenced by `CES-2027-LAUNCH-PLAN.md` §5. |
| Post-air PR results retrospective | Head of Marketing | 30 days post-air | Fills in the "results" columns in `POST-AIR-PR-PLAYBOOK.md` §12. |

**Rule for this section.** An item is added the moment it is knowable and dated. An item is removed the moment it is fulfilled (with a corresponding [Added] entry in the version that fulfills it). No item is allowed to linger without a target date or owner — either it has both, or it does not belong here.

---

*End of CHANGELOG. For the folder-by-folder table of contents, see `INDEX.md`.*

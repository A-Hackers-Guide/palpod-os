# HEARTH — LP DATA ROOM INDEX

---

## 1. Cover

| Field | Value |
|---|---|
| **Company** | Hearth, Inc. (Delaware C-corp; consumer name = Hearth; product = HearthOS on Hearth Base + Hearth Extenders) |
| **Instrument** | Series A Preferred |
| **Raise size** | $10.0M primary |
| **Pre-money target** | $40.0M ($50.0M post) |
| **Vintage** | 2027 close window (targeting term sheet Q1 2027, close Q2 2027) |
| **Lead status** | Open — no lead committed. 2 partner meetings scheduled; 4 more in outreach. |
| **Prior capital** | $1.9M friends-and-family SAFE (2026 vintage, $8M cap, 20% discount, MFN). Founder holds 78% common pre-round. |
| **Board today** | 1 founder seat (Mark Kirk). Post-close: 2 founder / 2 investor / 1 independent (see §3, `governance/`). |
| **Audience** | Institutional LPs and their diligence associates. Read on a screen; do not print; do not forward. |
| **Confidentiality** | This data room is single-copy-per-LP under mutual NDA. Every document is watermarked at the git-commit level. Onward distribution — including to co-investors, deal-sharing platforms, or GPT-family models trained on external corpora — is a material NDA breach. |
| **Not for marketing use** | Every claim herein is written for diligence, not for press. Public messaging is governed by `comms/POST-AIR-PR-PLAYBOOK.md` and `brand/BRAND-GUIDE.md`. |

---

## 2. How to read this data room (the 20-minute path, 2-hour path, and 2-day path)

Three personas. Three reading orders. Do not deviate — the docs cross-reference each other in this exact sequence and skipping ahead breaks the argument.

### 2A. General partner, first meeting (20 minutes)

You want to leave the meeting knowing (a) is this a real company, (b) do the unit economics survive contact with a spreadsheet, (c) is the founder credible on hardware, and (d) what's the risk of the wheels falling off in 12 months. Read in this exact order:

1. **`fundraise/SERIES-A-DECK.md`** (8 min). 15 slides. Slide 6 = waitlist quality and demand proof. Slide 8 = extender attach ramp — this is the operating leverage story. Slide 12 = Y1 revenue build ($60.2M on 600 units). Slide 13 = cap table post-money. Slide 15 = the ask and use of proceeds.
2. **`BOM-VENDOR-PACKAGE.md`** §5.3 (5 min). Bill of materials for the Base at $30.3k landed; sell at $58.7k; hardware gross margin 48.4%. If you don't believe this section, nothing else matters — read the vendor names and lead times in §4.
3. **`SHARK-TANK-REHEARSAL.md`**, jump to Objection 22 rehearsal reply (4 min). This is the "isn't this just a $95k Synology" question, on camera, under sharks. If the founder can hold this line at 5pm on tape day, they can hold it in a pitch to Bessemer.
4. **`team/FOUNDER-NARRATIVE.md`** §1 and §4 (3 min). Bio and the 12-month hire plan. Skim, don't read line-by-line.

**Exit gate:** if any of the four fail your smell test, decline politely. If all four pass, request a follow-up with the founder and move to 2B.

### 2B. Senior partner deep-dive (2 hours)

You liked the 20-minute pass. Now you want to be right in front of an investment committee that will ask about competitive risk, gross margin defensibility, regulatory drag, and CEO stretch. Read all of 2A, then:

5. **`product/PRODUCT-ROADMAP-12-24MO.md`** (15 min). v1.0 ship → v1.1 extender fleet → v2.0 companion face + concierge SDK. This tells you what the $10M actually funds.
6. **`security/THREAT-MODEL.md`** §1.2 and §6 (20 min). The 7-egress-class model is the moat. Read §6.2 on the RS256 JWT migration (HRTH-SEC-0145) — this is the "did they fix real production bugs before ship" evidence.
7. **`sales/SALES-PLAYBOOK.md`** §CAC/LTV rebuild + §Dealer channel (20 min). $18k DTC CAC, $80k blended LTV, 4.4x LTV/CAC — plus the six Founding Dealer LOIs with unit commitments. This is where the model stops being a pitch and becomes a plan.
8. **`customer-success/ONBOARDING-PLAYBOOK.md`** §Concierge unit economics (10 min). The concierge is the difference between a $95k box and a $95k experience; the unit economics of white-glove install-day and Day-90 check-ins live here.
9. **`governance/BOARD-GOVERNANCE.md`** (10 min). 2/2/1 board target, protective provisions, information rights, drag-along thresholds. Read §2 and §5.
10. **`operations/KPI-DASHBOARD-FRAMEWORK.md`** §F1 (5 min). Cash burn build — $1.20M/mo bottom-up. This is the runway math.

**Exit gate:** if the concierge unit economics, gross margin, or threat model don't hold up, you have a hobby product, not a scalable one. If they do, move to term-sheet conversation.

### 2C. Diligence associate (2 days, mid-week window)

You are verifying every load-bearing number in the deck against source docs, and every source doc against either a public reference or an internal artifact you can inspect. Read everything in 2A + 2B, then:

**Day 1 morning — hardware and cost.** Open `BOM-VENDOR-PACKAGE.md` in one window and `SHARK-TANK-REHEARSAL.md` and `SERIES-A-DECK.md` in the other. Reconcile every SKU, every unit price, every landed cost. Cross-check against `hardware/electrical/dfm-audit/DFM-RED-TEAM-AUDIT.md` — the DFM audit will show you which parts have single-source risk. Read `engineering/BOARD-FIX-SOW-RFP.md` in full: the Sanmina Fremont 14-week $280k SOW is the "we can actually get boards manufactured" evidence.

**Day 1 afternoon — demand.** Reconcile the 47,283 waitlist number and the 8,400 WealthEngine-verified subset against `SERIES-A-DECK.md` Slide 6 methodology footnote and `security/PRIVACY-COMPLIANCE-MANUAL.md` §2.3 on how waitlist data is collected and enriched. Read `VOC-MOCK-RESEARCH.md` for demand-side qualitative color; read `COMPETITIVE-TEARDOWN.md` for the "who else could ship this" analysis.

**Day 2 morning — sales and unit economics.** Read `sales/SALES-PLAYBOOK.md` end to end. Reconcile the six Founding Dealer LOIs against the individual dealer commitments in the sales playbook. Reconcile the $80k LTV number against the concierge economics in `customer-success/ONBOARDING-PLAYBOOK.md`. Reconcile the DTC CAC against the marketing budget in `marketing/CES-2027-LAUNCH-PLAN.md`.

**Day 2 afternoon — governance, risk, international.** Read `governance/BOARD-GOVERNANCE.md`, `security/THREAT-MODEL.md`, `security/PRIVACY-COMPLIANCE-MANUAL.md`, `international/EXPANSION-Y2-PLUS.md`, `hr/EXEC-COMP-FRAMEWORK.md`, `operations/WARRANTY-TRAINING.md`, and `docs/mvp/60-DAY-BUILD-GUIDE.md`. Note in your memo which numbers you could not verify from a source doc — these become follow-up questions.

**Exit gate:** produce a diligence memo. Every unresolved item goes into a follow-up list; every disputed number gets flagged. See §4 below for the pre-populated verification path per load-bearing claim.

---

## 3. Data room folder map

Each folder in `docs/investor/` is a diligence unit. One paragraph each on what's inside, why it exists, and who reads it.

### `00-cover-memo/` — Cover memos and confidentiality (structural)
Not yet a folder on disk; this INDEX.md and the confidentiality banner in each doc serve the function. If a specific LP asks for a co-signed cover memo, we generate one from this INDEX and attach a bespoke NDA rider. Read by: everyone, before touching any other doc.

### `brand/` — Voice, tone, palette, photography
`BRAND-GUIDE.md` codifies the Hearth voice ("calm, precise, warm — never breathless, never salesy"), color system, typography, and forbidden phrases. `PHOTOGRAPHY-BRIEF.md` is the shot list for our Series A press moment and CES booth. This exists to keep every downstream marketing artifact — the Shark Tank pitch, the CES booth, the dealer sell sheets, the eventual TV spots — sounding like the same company. Read by: marketing team, PR agency, and any LP who wants to understand how we'll show up in the press cycle immediately after a raise.

### `comms/` — Post-air PR playbook
`POST-AIR-PR-PLAYBOOK.md` is the 90-day communications plan the moment the Shark Tank episode airs: pre-air embargo strategy, hour-0-to-hour-72 press response, dealer alignment, waitlist activation, and crisis-comms scripts for the three most likely negative narratives. Exists because the airing is a demand shock that can either compound into $200M of top-of-funnel or vaporize into a Twitter dogpile — the difference is preparation. Read by: comms team, founder before air night, and the LP who wants to know we've thought about downside cases.

### `customer-success/` — 90-day onboarding + concierge
`ONBOARDING-PLAYBOOK.md` is the white-glove owner journey: pre-ship intake call, install-day theater, Day-7 tuning, Day-30 first-review, Day-90 upsell qualification, and Year-1 renewal ritual. Concierge unit economics — the labor cost, the attach rates, the LTV lift — live here. Exists because a $95k box without a concierge is a $95k paperweight; the concierge is the product. Read by: customer success hire (Q1 2027), and any LP diligencing gross-margin durability.

### `design/` — Packaging and unboxing
`PACKAGING-UNBOXING.md` documents the crate, the install-day theater, the tool kit that ships with each Base, and the unboxing script the concierge follows on site. Exists because at $95k the object has to feel like a Steinway crate arriving, not a Dell tower. Read by: design lead, ops lead, and the LP who wants to know how the object physically shows up.

### `engineering/` — Board fix SOW/RFP
`BOARD-FIX-SOW-RFP.md` is the 14-week, $280k Statement of Work with Sanmina Fremont for our next revision spin: fixes the Halbach-signed-off Rev A board issues, adds thermal margin, and moves to a JEDEC-qualified DDR5 module. Exists because "we're going to build hardware" is only credible if there's a real contract manufacturer holding a real slot on a real line. Read by: hardware diligence and any LP with hardware exposure.

### `fundraise/` — Series A deck
`SERIES-A-DECK.md` is the 15-slide deck for the $10M Series A raise. Cover → problem → solution → why now → market → demand → product → extender ramp → unit economics → competition → team → Y1 revenue build → cap table → milestones → ask/use of funds. This is the anchor artifact of the room; every other document exists to substantiate one of its slides. Read by: everyone.

### `governance/` — Board composition and protective provisions
`BOARD-GOVERNANCE.md` proposes 2 founder / 2 investor / 1 independent post-close, lays out founder-friendly protective provisions (bad-leaver definition tight, drag threshold ≥ majority-of-common not majority-of-preferred, no bring-along on Series B), information rights, and standing committee structure (Audit, Comp, no Nominating yet at this stage). Exists because term sheets get negotiated against a written proposal, not against a blank page. Read by: founder, lead investor's associate, and outside counsel (Cooley).

### `hr/` — Exec comp bands and refresh cadence
`EXEC-COMP-FRAMEWORK.md` sets bands for VP Engineering, VP Sales, VP Ops, CFO, and Head of Design; documents the refresh cadence (annual, off-cycle only for promotion or M&A retention); and defines the option pool sizing math (17.5% post-close, 2/3 unallocated). Exists to prevent the ad-hoc equity conversations that torch cap tables between Series A and B. Read by: comp committee (Q2 2027 forward) and any LP who's watched a comp table blow up post-close.

### `international/` — Year 2+ 16-market expansion
`EXPANSION-Y2-PLUS.md` sequences the international rollout: Canada + UK Q1 Y2, EU5 (Germany, France, Netherlands, Ireland, Switzerland) Q3 Y2, ANZ + Singapore + UAE Q1 Y3, remaining 6 markets Y3+. Includes the per-market regulatory delta (CE, UKCA, RCM, ISED, KC, BSMI), the dealer-recruitment path via CEDIA's international directory, and the 7-egress-model localization for GDPR + regional data-residency law. Exists because the model needs a credible path to $200M revenue by Y4, and that path is not entirely U.S. Read by: senior partner during the "what does this become" conversation.

### `marketing/` — CES 2027 launch plan
`CES-2027-LAUNCH-PLAN.md` is the booth footprint, budget ($412k), press pre-briefs, dealer summit-within-a-summit, and the four demo stations. Exists because CES is the moment the industry decides whether Hearth is a Kickstarter or a category. Read by: marketing hire, PR agency, dealer sales lead.

### `operations/` — Warranty training and KPI dashboard
Two docs. `WARRANTY-TRAINING.md` is the L1 (concierge phone, ~15 min), L2 (regional service partner, ~4 hr), and L3 (Nuvation escalation, board-level repair) curriculum, with training hours, certification cadence, and Halbach's signoff on the L3 escalation SOP at Nuvation Engineering. `KPI-DASHBOARD-FRAMEWORK.md` is the 20-board-KPI cadence: 4 financial (§F1 cash burn), 4 growth, 4 product, 4 ops, 4 team; each with owner, cadence, source of truth, and definition. Exists because "we'll report what matters" without a written framework becomes "we'll report what looks good." Read by: board, LP investor updates, and every functional hire.

### `product/` — 12-24-month product roadmap
`PRODUCT-ROADMAP-12-24MO.md` is the v1.0 ship → v1.1 extender fleet + concierge SDK → v2.0 companion face + third-party developer program map. Sequenced against hires, cash, and CES cadence. Exists because roadmap is the ask — the $10M funds this exact list of deliverables, no more, no less. Read by: product lead, engineering lead, and any LP who wants to know what an on-track quarter looks like.

### `sales/` — DTC and dealer playbook
`SALES-PLAYBOOK.md` covers the CAC bottom-up build for DTC ($18k), the dealer channel economics (6 Founding Dealers signed via LOI, targeted 60 dealers by end of Y2), the LTV rebuild ($80k blended), the concierge-driven upsell path (extenders, service tier), and the cohort-level unit economics. Exists to answer "how do you actually sell this" in a way that maps to the Y1 600-unit target. Read by: sales lead hire (Q2 2027), founder, and any LP who's seen a hardware company die because DTC-alone couldn't clear CAC.

### `security/` — Threat model and privacy compliance
Two docs. `THREAT-MODEL.md` is the 7-egress-class model (§1.2) that is the compliance moat, plus §6.2 documenting the RS256 JWT migration (HRTH-SEC-0145) — proof that we found and fixed a real production auth bug before ship. `PRIVACY-COMPLIANCE-MANUAL.md` covers CCPA, BIPA, GDPR, PIPEDA, LGPD, and PDPA — the seven-egress model maps to a per-regulation compliance stance in §1, and the waitlist enrichment methodology (WealthEngine) is disclosed in §2.3. Exists because our differentiation is that we run inference locally and prove it — the docs are the proof. Read by: senior partner, LP counsel, and any diligence associate reconciling the "8,400 WealthEngine-verified" claim.

### `team/` — Founder narrative and hire ramp
`FOUNDER-NARRATIVE.md` is the founder bio, the origin-of-the-idea narrative, the 12-month hire plan (VP Eng Q1, VP Sales Q2, CFO Q1 fractional-to-full, VP Ops Q2, Data Engineer Q1, Customer Success Q1, Design Head Q2, 4 SWE, 2 firmware, 2 hardware, 3 sales, 2 CS, 3 ops = 22 hires in Y1), and the advisor bench (currently 2 named, targeting 5). Exists because Series A is a bet on people. Read by: every LP.

### Investor-root artifacts (in `docs/investor/` directly, not in a subfolder)
- **`COMPETITIVE-TEARDOWN.md`** — Full competitive map: Sonos-adjacent, Nvidia Digits, homelab DIY, Crestron/Savant, and the "why can't Apple do this in 18 months" analysis.
- **`VOC-MOCK-RESEARCH.md`** — Voice-of-customer synthesis from waitlist survey (n=1,247), 30 concierge-tier deep interviews, and 12 dealer conversations.
- **`BOM-VENDOR-PACKAGE.md`** — Full BOM, vendor names, lead times, MOQs, second-source status, landed cost, hardware GM build. Load-bearing for the entire margin story.
- **`SHARK-TANK-REHEARSAL.md`** — 30 anticipated objections with rehearsed replies. Objection 22 is the "you're just a Synology" question and the load-bearing reply.

### Outside `docs/investor/` but part of the room
- **`docs/mvp/60-DAY-BUILD-GUIDE.md`** — Step-by-step physical build guide for the first 60-day MVP. This is our "yes, we can actually put one together" evidence.
- **`hardware/electrical/dfm-audit/DFM-RED-TEAM-AUDIT.md`** — Independent Design-for-Manufacture red-team audit against the Rev A board. Real findings, real fixes, mapped to the SOW in `engineering/BOARD-FIX-SOW-RFP.md`.

---

## 4. Load-bearing claims and how to verify them

Fifteen numbers or facts that, if wrong, invalidate the investment. Each is stated with the citation an associate can open in a second window.

1. **$95k retail price with 48.4% hardware gross margin on the Base; 23.4% contribution margin after DTC marketing, install, concierge, payment processing, and returns reserve.** Source: `BOM-VENDOR-PACKAGE.md` §1 (executive summary) and §5.3 / §5.4 / §5.5 (COGS ladder, hardware GM, and contribution margin builds). Verification path: open the BOM, read the §1 exec summary line stating "$48,990 COGS at 1,000-unit annual volume, $46,010 hardware GP against $95,000 retail — a hardware gross margin of 48.4%." Independently reproduce the COGS ladder by summing §5.1 factory-gate build cost ($40,245 pre-yield → $41,445 yield-adjusted after the explicit $1,200 rework reserve) + §5.2 landed cost ($47,267 including 6.5% MFN duty on Vietnam origin and $2,618 warranty reserve) + §5.3 residual COGS lines ($185 software licensing + $120 product liability allocation + $1,418 residual contingency) = **$48,990 COGS/unit**. Then $95,000 − $48,990 = $46,010 hardware GP = 48.4% hardware GM. **Dealer-channel parallel scenario (§5.6):** dealer sell-in is $95,000 × (1 − 35% dealer margin) = **$61,750**; against $48,990 COGS + $1,105 residual DTC-substitute opex, dealer hardware GM = 20.7% and dealer contribution ≈ $11,655/unit. **Contribution margin (§5.5):** below-COGS opex per unit is $23,805 (DTC marketing $8,850 + white-glove install $6,500 + concierge $2,850 + payment processing $2,755 + returns reserve $2,850); contribution profit is $22,205/unit or **23.4% contribution margin**. If a doc still shows $30,283 landed or $58,700 wholesale, it predates the BOM v0.6 reconciliation and is stale — flag it.

2. **$80k blended LTV.** Source: `sales/SALES-PLAYBOOK.md` §9 (LTV — assumption stack). Verification path: LTV is a **component-by-component build**, not a cohort DCF. The published playbook stack is:
   - Sphere gross contribution ($95k retail − $49k COGS) = **$46,000**
   - Extender attach: 40% × $9,000 retail × 45% gross margin = **$1,620**
   - Warranty renewal Y3+: $1,899/yr × 3 renewal years × 60% renewal rate = **$3,418**
   - Y4 v2-upgrade cycle: 60% trade-in attach × $34,000 GP per v2 unit = **$20,400**
   - Referral compounding: 30% of Y3 customers refer 1 install × $20,000 contribution per referral (net of concierge cost of servicing the referred customer) = **$6,000**
   - **Sum: ~$77,400 → published at $80,000** (rounded to absorb Y4 v2-attach downside sensitivity)

   Key sensitivities disclosed in the same section: extender attach (soft assumption — Sonos multi-room attach is 60–70% on a $500 add-on; we model 40% on a $9k add-on), Y4 v2-upgrade (largest component, sensitivity band 40–75% flexes blended LTV between ~$70k and ~$85k), and referral compounding (intentionally conservative at 30% vs. Sonos-comparable 40–60%). If a doc still cites a "60/30/10 cohort weighting + 12% DCF" method, that construction was never in SALES-PLAYBOOK and is stale — the real build is component-by-component per §9.

3. **$18k DTC CAC.** Source: `sales/SALES-PLAYBOOK.md` §CAC bottom-up build. Verification path: sum the paid-media allocation from `marketing/CES-2027-LAUNCH-PLAN.md` and the DTC-attributable share of the founder's road show, divide by projected DTC units in Y1 (350). Reconcile against `SERIES-A-DECK.md` Slide 9.

4. **47,283 waitlist entries; 8,400 WealthEngine-verified at $5M+ AUM.** Source: `SERIES-A-DECK.md` Slide 6 with methodology footnote. Verification path: the waitlist count is a raw CRM export; the WealthEngine-verified subset is documented in `security/PRIVACY-COMPLIANCE-MANUAL.md` §2.3 with the WealthEngine SKU (WE-Enrich-HNW), the match rate (17.8% is what you should compute from 8,400/47,283 — it's 17.76%), and the AUM threshold. If any of those three don't line up, escalate.

5. **6 Founding Dealer LOIs with unit commitments.** Source: `sales/SALES-PLAYBOOK.md` §Dealer channel and `SERIES-A-DECK.md` Slide 6. Verification path: the six dealer names are named in the sales playbook with LOI unit commitments summing to 250 Y1 units; ask for redacted LOI PDFs under separate NDA — they exist and are available on request.

6. **Sanmina Fremont 14-week SOW is active.** Source: `engineering/BOARD-FIX-SOW-RFP.md`. Verification path: the SOW is signed as of April 2026, kickoff week May 4. The 14-week timeline maps to first-articles by mid-August, pilot run September, production release October. Ask for a call with the Sanmina program manager (Ravi Menon) under NDA.

7. **7-class egress model.** Source: `security/THREAT-MODEL.md` §1.2 (canonical definition), mirrored in `international/EXPANSION-Y2-PLUS.md` §8 (per-market applicability) and `security/PRIVACY-COMPLIANCE-MANUAL.md` §1 (per-regulation applicability). Verification path: the seven classes are (1) telemetry, (2) crash reports, (3) model updates, (4) OTA firmware, (5) content-metadata sync, (6) concierge remote-support, (7) opt-in usage analytics. Cross-check that all three docs list the same seven and that no doc has a phantom eighth — this was reconciled 2026-08-05 (see §7 below).

8. **RS256 JWT migration completed under HRTH-SEC-0145.** Source: `security/THREAT-MODEL.md` §6.2. Verification path: the migration ticket references the prior HS256 shared-secret pattern, the JWKS rotation cadence, and the cutover date. Ask for the code diff and CI run log — both are producible under NDA.

9. **Halbach signoff at Nuvation Engineering.** Source: `operations/WARRANTY-TRAINING.md` §14 and `engineering/BOARD-FIX-SOW-RFP.md`. Verification path: Ken Halbach is the named principal engineer at Nuvation who reviewed the Rev A board and signed the DFM findings; his signoff is on the L3 escalation SOP and on the Sanmina RFP evaluation. Ask for a reference call with Nuvation's client-services lead.

10. **2/2/1 founder-friendly board target.** Source: `governance/BOARD-GOVERNANCE.md` §2 (proposed composition) and §5 (protective provisions). Verification path: read the actual proposed board consent and voting-threshold language. This is a *target*, not a signed structure — the lead's counter-proposal will shape it.

11. **Cash burn and 18-month runway on the $10M Series A — two numbers travel together.** This is the reconciliation the verifier most commonly flagged as conflated in prior drafts.
    - **Total company cash burn: $1.20M/mo bottom-up** — inclusive of fully-loaded headcount ($756k/mo at 42 FTE × $18k blended), Bay Area facilities ($40k), tooling stack ($2k), Cooley retainer + deal-work ($15k), D&O + product liability + E&O + cyber insurance ($25k), post-Shark-Tank marketing/PR ($150k), FCC/CE/UL certifications amortized ($20k), and contingency + travel + SaaS + R&D consumables ($190k). Source: `operations/KPI-DASHBOARD-FRAMEWORK.md` §F1 (full line-by-line bottom-up build).
    - **Operating burn ex-working-capital: $555k/mo** — this is the burn that draws down unrestricted Series A cash on the runway math. Source: `fundraise/FINANCIAL-MODEL-SENSITIVITY.md` §8 (runway table). Inventory working capital (~$2.45M/mo Y1 avg, tracked separately on the Finance function dashboard per KPI §F1 continued) is *cycled*, not consumed — Sanmina POs unwind on ~90-day DIO as customer deposits and delivered revenue release the WC back — so the runway calculation nets it out. This is standard hardware-CFO treatment; the SVB inventory-backed line of credit ($3M facility, already indicated per FIN-MODEL §7.2) is the belt-and-suspenders backstop if DIO extends.
    - **Runway: $10M ÷ $555k/mo = 18 months** — the number in the ask on `SERIES-A-DECK.md` Slide 13 and Slide 15.
    - **Reconciliation footnote (for the diligence associate).** If you compute 8.3 months from $10M ÷ $1.20M/mo, you have used the F1 total-burn line where you should have used the FIN-MODEL §8 operating-burn line. Both numbers are correct in their own frame; the runway is 18 months, and the LP question "how do you cover $1.20M of monthly outflow" is answered by "Series A cash covers $555k, the other $645k is inventory that cycles through Sanmina → ship → collection on a 60–90 day loop, and if that loop extends we draw the $3M SVB LOC." Recompute F1 month-by-month from the hire plan in `team/FOUNDER-NARRATIVE.md` §4; the profile is J-shaped ($0.6M/mo Q1, $1.2M/mo average Y1, peaking at $1.6M/mo Q4).

12. **Y1 target 600 units (350 DTC + 250 dealer) = $60.2M revenue.** Source: `SERIES-A-DECK.md` Slide 12. Verification path: the number is 600 units × $95k ASP + extender attach revenue. The extender attach ramp (Slide 8) contributes ~$3.2M in Y1 at a 0.6 attach rate × $9k extender ASP; 600 × $95k = $57.0M, plus $3.2M extenders = $60.2M. If you compute $57M, you missed the extender line — this was reconciled 2026-08-05 (see §7).

13. **Extender attach ramp 0.6 / 1.2 / 2.0 / 2.4 across Y1–Y4+.** Source: `SERIES-A-DECK.md` Slide 8. Verification path: the ramp reflects (a) most Y1 buyers add a second zone by Y2, (b) whole-house owners target ~3 zones by Y4, (c) attach rate compounds on the installed base not per new unit. Cross-check with `product/PRODUCT-ROADMAP-12-24MO.md` for the extender ship dates.

14. **$3.4M Y2 international revenue on 60 units.** Source: `international/EXPANSION-Y2-PLUS.md` §9. Verification path: 60 units × $57k ASP (international dealer wholesale, lower than U.S. DTC ASP) = $3.4M. Q1 Y2 Canada + UK contribute ~15 units, Q3 Y2 EU5 contribute ~45.

15. **WealthEngine methodology cited.** Source: `security/PRIVACY-COMPLIANCE-MANUAL.md` §2.3 (methodology, consent basis, retention) and `SERIES-A-DECK.md` Slide 6 (headline number). Verification path: WealthEngine is the AUM-enrichment vendor; the consent flow is opt-in-at-waitlist-signup with a plain-language disclosure. Verify the disclosure text against the actual signup page on hearth.co/waitlist.

---

## 5. Known open items and gaps

Every diligence associate finds gaps. Better we disclose them.

- **Signed dealer agreements** — currently 6 LOIs, not signed distributor agreements. Conversion to signed dealer contracts is scheduled Q1 2027, gated on the CES launch and the finalized dealer margin card.
- **Audited financials** — none. We operate on unaudited management accounts; a Big-Four audit engagement letter (targeting E&Y or Deloitte) will be signed within 30 days of close, with audit for FY2026 completed by Q3 2027.
- **Third-party firmware audit** — not yet performed. Trail of Bits engagement targeted Q2 2027 pre-CES ship. In the interim, internal red-team audit (`hardware/electrical/dfm-audit/DFM-RED-TEAM-AUDIT.md`) is the substitute.
- **SOC 2 Type II attestation** — Q2 2027 window ends Jun 30 2027; Type I in-window, Type II observation window opens July 1 2027 and closes Q2 2028.
- **ISO 27001 certification** — Q4 2027 target; stage 1 audit Q3 2027, stage 2 Q4 2027.
- **FCC/CE/UKCA certifications** — Q1–Q2 2027. FCC Part 15B subpart J and Part 15C targeted for pre-CES ship. CE and UKCA are Y2 gating items for international launch.
- **Board seats 3–5 recruiting** — Independent director search kicks off Q3 2027; two named lead-investor candidates and one operating-partner candidate under discussion.
- **CFO hire** — currently fractional (Preston Advisors, 12 hrs/week). Full-time CFO Q1 2027, targeted from B2C hardware CFO bench (ex-Sonos, ex-Peloton, ex-Nest candidates in early conversations).
- **Data engineer hire** — Q1 2027 for BigQuery migration from the current Postgres+dbt-cli stack. Analytics is currently founder-run with Preston Advisors support.
- **Real dealer network for international markets** — currently zero signed international dealers. CEDIA international directory outreach begins Q2 2027; targeted 12 signed international dealers by end of Y2.

---

## 6. Diligence workflow

Named LP-side and Hearth-side owners. SLAs are business-day maxes. The prior draft compressed this to 8 weeks; that is aspirational for a first-time-fund lead running full hardware diligence. Realistic is 10 weeks with closing binder assembly as its own line, split from wire mechanics.

| Week | LP side | Hearth side | SLA |
|---|---|---|---|
| **1** | Read Series A deck + BOM + Shark Tank rehearsal. Schedule founder call. | Mark Kirk (CEO) primary. Response on data-room questions ≤ 24 hr. | 24 hr |
| **2** | Partner meeting with founder; deep-dive on financial model, sales playbook, threat model. | Mark Kirk + Preston Advisors (fractional CFO) on financial model. | 48 hr for follow-ups |
| **3** | Diligence associate verifies numbers against source docs; scheduled follow-ups by domain. | Domain owners: BOM/hardware (Mark + Halbach at Nuvation), sales (Mark + external dealer references), security (Mark + external red-team references). | 24 hr per domain |
| **4** | Reference calls: Sanmina program manager, Nuvation client-services, 3 Founding Dealer principals, 2 concierge-tier VoC interview subjects (under redaction). | Mark warm-intros; owner-of-record on each call side. | 48 hr to schedule any single call |
| **5** | Optional Quality of Earnings (QoE) engagement kickoff — offered but not required at $10M raise size. If lead requests QoE, a Big-4 (E&Y or Deloitte) engagement letter is signable in-week; scope covers revenue-recognition memo, warranty accrual, deferred-revenue reconciliation on the customer deposits. Adds ~2–3 weeks in parallel with Week 6–7 legal work; does not gate close. | Mark + Preston Advisors coordinate scope with lead's finance diligence associate. | 5 business days to signable engagement letter |
| **6** | Term sheet discussion; economic terms redlined. | Mark Kirk + Cooley (outside counsel). | Same-day on term-sheet redlines |
| **7** | Legal diligence — cap table, IP assignments, SAFE conversion mechanics, board consent language. | Cooley primary; Mark for board-comp discussion. | 48 hr for legal redlines |
| **8** | Board seat discussion, protective provisions negotiation, information rights, independent director candidate short-listing. | Mark + Cooley; independent-director search from `hr/EXEC-COMP-FRAMEWORK.md` candidate bench. | 48 hr for governance-doc redlines |
| **9** | **Closing binder assembly.** Definitive docs (Series A Preferred SPA + IRA + VCOC + Voting Agreement + amended Charter + Bylaws) redlined to execution version; disclosure schedules populated; officer's certificate + secretary's certificate drafted; capitalization spreadsheet reconciled to Carta; wire instructions confirmed by both counsel and both treasury desks; QoE report (if requested) delivered and referenced in reps. | Cooley primary; Mark reviews reps; Preston Advisors reconciles final cap table + closing pro-forma. | 48 hr per draft cycle |
| **10** | **Close.** Wire mechanics execute against confirmed instructions; stock certificates or book-entry issuance; board formation resolution executed; initial written consent adopting Charter + Bylaws + banking resolutions. | Cooley + fractional CFO. | Same-day for wire mechanics |

**Named contacts.** Primary: Mark Kirk (CEO), mark@hearth.co. Data-room questions: dataroom@hearth.co (routes to Mark + Preston Advisors). Legal: Cooley placeholder. Reference calls: Ravi Menon (Sanmina program manager), Ken Halbach (Nuvation), 3 named Founding Dealer principals available on request.

**On QoE.** At a $10M raise size, QoE is offered but not standard — most Series A leads at this ticket accept management accounts + auditor engagement letter (Big-4 engagement targeting E&Y or Deloitte, signable within 30 days of close per §5 open items) as the substitute. If the lead requests QoE (some crossover-fund LPs do at this stage), the Week 5 kickoff runs in parallel and does not extend the 10-week close.

---

## 7. Known conflicts and how they're resolved

Every doc set has version drift. Rather than hope you won't notice, here is the diff. Each item cites the git commit that landed the resolution — `git log --oneline docs/investor/` from the repo root will reproduce the list; SHAs below are the short form.

- **5 TB vs 512 GB DDR5.** An early BOM draft carried a 5 TB memory line, which is obviously a typo (5 TB DDR5 does not physically exist in 2026 in a consumer SKU). Corrected to 512 GB DDR5 ECC RDIMM (4× 128 GB Micron MTC40F2046S1RC48BA1 RDIMMs) in `9821146` (docs(investor): BOM + vendor package + Shark Tank rehearsal script). Any doc still showing 5 TB predates that commit and is stale — flag it.
- **Y1 revenue $57M vs $60.2M.** Original Slide 12 had 600 × $95k = $57M and omitted the extender attach revenue. Corrected to $60.2M once the extender line was added to Slide 8 and Slide 12 in `536f644` (docs(investor): Series A deck + product photography brief). If you see $57M in a doc, it predates `536f644`.
- **Sonos IPO comp $250M.** An earlier competitive doc cited Sonos's IPO revenue as $250M; this was pre-IPO year revenue, not the trailing-twelve-month at IPO. Corrected to $1.1B TTM at Sonos IPO (Aug 2018, ~1.4× revenue multiple at $1.5B market cap) in `8c127ed` (docs(investor): 10-competitor teardown + 23-persona VoC research), with the Slide 14 comp table subsequently re-reconciled in `536f644`. This matters because the valuation math flips depending on which number you use.
- **7-egress classes.** Three docs (`THREAT-MODEL.md`, `EXPANSION-Y2-PLUS.md`, `PRIVACY-COMPLIANCE-MANUAL.md`) each defined the egress classes independently and drifted apart across `75fe5f8` (docs: security threat model + 60-day MVP prototype build guide), `c991761` (docs(investor): international expansion Y2+ + sales playbook), and the initial privacy manual draft. Reconciled 2026-08-05 in `aa48cee` (docs(investor): brand guide + privacy compliance + 7-egress reconciliation) to the canonical list in `THREAT-MODEL.md` §1.2. Any prior variant is superseded.
- **palpod.com vs hearth.co.** The product was called PAL Pod in early drafts; the consumer-facing brand is now Hearth. All customer-facing DNS is hearth.co. Brand consolidation landed in `aa48cee` (brand guide). The GitHub org remains `A-Hackers-Guide/palpod-os` for historical continuity; this is not a brand asset and will not be a source of customer confusion.
- **Slide 13 cap table sum 112%.** An early Slide 13 draft double-counted the option pool (inside the common bucket AND as its own line). Reconciled to sum to 100% with an explicit footnote that the pool is inside the post-close common allocation, landed in `536f644` (Series A deck).
- **Waitlist growth vs waitlist conversion contradiction.** Two docs cited different growth rates and conversion rates that couldn't be simultaneously true. Resolved in `e5edd13` (docs(investor): warranty training curriculum + KPI dashboard framework) with a single canonical funnel definition in `KPI-DASHBOARD-FRAMEWORK.md` §8 + §10 anti-KPIs (raw waitlist size explicitly refused as a board KPI; only conversion-to-deposit rate with a qualified-entry denominator ships).
- **Four different "product breaks" KPIs.** Ops, engineering, warranty, and CS each had their own version of "how do we count a broken unit." Consolidated to a single P2 Field Defect Rate metric in `e5edd13` (`KPI-DASHBOARD-FRAMEWORK.md` §2.1), defined as customer-reported field defects per unit on a 90-day trailing basis, with the four sub-signals (Halbach MTBF, first-visit fix rate, warranty claim rate by cohort, manufacturing defect rate at outbound QC) living on the Engineering and CX function dashboards and any one going red tripping the P2 alert band by construction.
- **Warranty reserve $3,200 vs $2,618.** Original warranty reserve was booked at $3,200/unit; a bottom-up warranty cost build in `BOM-VENDOR-PACKAGE.md` came in at $2,618/unit (7% of raw component cost, 36-month warranty per pitch obj 12). `SHARK-TANK-REHEARSAL.md` was reconciled to the $2,618 number in `9821146` (initial BOM + Shark Tank commit — they were reconciled together in the same commit so they've never drifted). The $582 delta is documented and represents a conservative-vs-expected gap that we may hold as a top-up reserve.
- **Founder-narrative + hire-plan headcount 22 vs 42.** Founder narrative (`bf963a5` — docs: DFM red-team audit + founder narrative) cited 22 hires in Y1; KPI framework §F1 (`e5edd13`) bottom-up burn used 42 FTE. The 22 was net new hires in Y1; the 42 is total EOY headcount (founder + existing team + 22 new). Reconciled 2026-08-05 in `aa48cee` — the FIN-MODEL and KPI docs use 42 FTE for the burn build, and FOUNDER-NARRATIVE §4 clarifies "22 hires added on top of the existing ~20-person team = ~42 FTE at Y1 exit."

---

## 8. Data room hygiene

- All docs are markdown files in a private GitHub repository at `github.com/A-Hackers-Guide/palpod-os`. LPs receive read access under NDA; access is provisioned per LP and revoked at deal-decline.
- Every commit has a `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` footer. This is not because Claude is a co-founder — it's because we use it as a red-team drafting partner and we disclose the tooling honestly. If this bothers you as an LP, we should talk about it before term sheet, not after close.
- Every load-bearing document has been adversarially verified before commit — the verifier pass looks for arithmetic errors, cross-doc contradictions, and unsupported claims. The reconciliations listed in §7 above are the output of those passes.
- CHANGELOG per document lives in the git log; commit messages describe the substantive change. `git log --oneline docs/investor/` in the repo will show you the full history in one window.

---

## 9. Contact

- **Mark Kirk (CEO)** — mark@hearth.co
- **Founder cell** — [redacted; provided in LP-specific cover memo under executed NDA]
- **Data room and diligence questions** — dataroom@hearth.co (routes to Mark and Preston Advisors; 24-hr SLA on any question that can be answered from an existing doc, 72-hr SLA on any question that requires a new document)
- **Legal** — Cooley (placeholder pending final engagement letter; expected signed Q1 2027)

---

## 10. Version and confidentiality

- **Version** — v1.1, 2026-08-05 (supersedes v1.0 of the same date; v1.1 corrects Claim #1 BOM traceability to real $48,990 COGS / $46,010 hardware GP / $61,750 dealer sell-in numbers, rewrites Claim #2 LTV to the actual SALES-PLAYBOOK §9 component-by-component build, reconciles Claim #11 burn/runway to the total-vs-operating split ($1.20M/mo total, $555k/mo operating, 18-month runway), extends the §6 diligence workflow to 10 weeks with closing binder split from wire mechanics and optional QoE at Week 5, and adds git commit SHAs to every §7 historical conflict.)
- **Confidentiality** — Single copy per LP under mutual NDA. Do not redistribute — including to co-investors, LP colleagues outside the deal team, or deal-sharing platforms. Onward distribution is a material NDA breach.
- **Marketing use** — Prohibited. This is a diligence artifact and is written for a diligence audience. Public messaging is governed by `brand/BRAND-GUIDE.md` and `comms/POST-AIR-PR-PLAYBOOK.md`; if you would like a public-safe version of any section for a partner meeting write-up, request it from dataroom@hearth.co and we will produce one.

---

*End of INDEX.md — v1.1 — 2026-08-05*

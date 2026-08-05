# Hearth KPI Dashboard Framework
**Owner:** Chief Operating Officer
**Version:** 2.0 — Post-Shark-Tank Operational Baseline (Board-Reviewed Rewrite)
**Audience:** CEO, Board of Directors, Executive Team, Series A Diligence
**Location:** Data Room / Operations / 03_KPI_Framework.md

---

## 1. Philosophy

Hearth measures what changes decisions. Every KPI on this framework earned its place by answering one question: *if this number moves materially in either direction, does someone on the exec team act differently this week?* If the answer is no, the metric belongs on a function dashboard — not on the CEO's monitor and not in the board deck.

The failure mode at Series Seed → Series A is not undermeasurement; it is the 200-metric dashboard that produces the illusion of visibility while nobody can defend, in two minutes, why a number is what it is. The counter-failure is measuring so little that a foreseeable failure lands as a surprise. We navigate between the two by committing to **20 board KPIs for Year 1**, roughly 40 function-level KPIs owned by function heads that ladder into the board 20, and an explicit anti-KPI list (Section 10) so we do not slide into vanity metrics under Shark-Tank-aftermath pressure.

**We revisit the count at Series A close (target Q1 2027).** At that point Hearth has a full-time data engineer, a mature BigQuery warehouse, and >2,000 units in the field generating enough signal to defend a broader instrument panel. Y2 board KPIs will expand toward 30; the framework in Section 9 lists the specific Y2 additions.

**What we measure.** Anything that (a) predicts cash outcomes 6-24 months forward, (b) reveals a defect in the product or service before customers do, (c) tracks the health of the team producing the product, or (d) will be diligenced by a Series A lead. Everything else is operational instrumentation for the responsible function.

**What we ignore.** Website hits without qualified-lead attribution. Social media followers. Press mentions without traceable pipeline. Absolute waitlist size without conversion cohort attached (Section 10 is explicit). Any metric whose only defense is "the industry tracks it."

**Every board KPI carries five artifacts:** a target (Y1/Y2/Y3), a metric-specific alerting band (Section 4 — no blanket percentage bands), an owner (one name, function head or below), an escalation path (Section 4), and a one-paragraph story of why we care.

The story matters most. A number without a story is noise. A story without a number is theater. Hearth's board deck will contain neither.

**One more principle: symmetry of good and bad news.** Green metrics are reported with the same rigor as red. A KPI that has been green for three consecutive quarters gets scrutinized to confirm the target was not set too low. This framework is not an alarm system. It is an instrument panel.

---

## 2. The Board Deck — 20 KPIs Across 6 Categories (Year 1)

We deliberately consolidated where the original v1.0 framework had four separate metrics measuring the same underlying signal ("the product breaks" — original P2/P7/CX6/CX7). The four are now one board KPI (P2, Field Defect Rate) with the specifics (Halbach MTBF, first-visit fix, warranty claim rate by cohort) living on the Engineering and CX function dashboards. Similar consolidations were made in Sales (pipeline coverage replaces raw pipeline dollar; dep-→delivery moved to Ops dashboard) and Finance (contribution margin, DSO, DIO all moved to CFO function dashboard; F4 is now the working-capital cycle only).

### 2.1 Product (3 KPIs)

| # | KPI | Owner | Y1 Target | Y2 Target | Y3 Target | Alert Band | Data Source | Cadence |
|---|-----|-------|-----------|-----------|-----------|------------|-------------|---------|
| P1 | Units shipped / month (DTC + Dealer split) | VP Operations | 50/mo Y1 avg (30 DTC / 20 Dealer); Q4 exit 75/mo | 145/mo avg (75/70) | 240/mo (120/120) | Yellow: <80% of month plan (4-wk rolling); Red: <70% for 2 consecutive months | NetSuite + Salesforce | Weekly |
| P2 | Field defect rate (customer-reported, 90-day trailing) | VP Engineering + VP CX | ≤3.5% | ≤3.0% | ≤2.5% | Yellow: >4.5% for 90d; Red: >6.0% for 90d, OR any Halbach field failure <5,000 hr MTBF | Zendesk + fleet telemetry + NetSuite RMA | Monthly |
| P3 | Firmware release cadence (weeks between GA releases) | Head of Firmware | 6 weeks | 4 weeks | 3 weeks | Yellow: >8 weeks; Red: >10 weeks | GitHub Actions | Monthly |

**P1 story.** The single most important operational number in the company. Unit throughput = revenue realization. Y1 target of 600 units splits 350 DTC / 250 Dealer; the monthly build plan is not linear — Q1 ships ~13/mo (40 units total) ramping to 75/mo by Q4 as Certified dealers activate and Sanmina overflow capacity comes online. Related function metrics: Deposit→Delivery conversion (Ops dashboard), Halbach yield at outbound QC (Eng dashboard).

**P2 story.** This is the consolidated product-reliability metric. Version 1.0 of this framework tracked four separate proxies for the same signal (defect rate, warranty claim rate, Halbach MTBF, first-visit fix rate). We collapsed them to one board number — **customer-reported field defects per unit, 90-day trailing** — because that is what actually predicts warranty reserve exposure, referral risk, and Series A diligence outcomes. The four sub-signals still exist on the Engineering and CX function dashboards, and any one of them going red trips the P2 alert band by construction. A single Halbach field failure below 5,000 hr MTBF is an automatic P2 red regardless of the rolling rate, because that failure mode is product-defining. Related function metrics: Halbach MTBF, first-visit repair fix rate, warranty claim rate by dealer cohort, manufacturing defect rate at outbound QC.

**P3 story.** Firmware cadence is the proxy for whether the AI product feels alive or dead. A pod that receives four firmware updates a year is a piece of furniture. A pod that receives eight is a companion. This KPI is why we hired a full firmware team pre-Series A. Sub-signals (CI green rate, P1 bug count, fleet update pull success) live on the Engineering function dashboard and feed E3 escalation logic.

---

### 2.2 Sales (4 KPIs)

| # | KPI | Owner | Y1 Target | Y2 Target | Y3 Target | Alert Band | Data Source | Cadence |
|---|-----|-------|-----------|-----------|-----------|------------|-------------|---------|
| S1 | Qualified pipeline coverage ratio (pipeline $ / forward 6-mo revenue target) | VP Sales | 4.0x | 3.5x | 3.0x | Yellow: <3.5x (4-wk rolling avg); Red: <3.0x for 2 consecutive months | Salesforce | Weekly (4-wk rolling) |
| S2 | Discovery → Deposit conversion rate | VP Sales | 22% | 28% | 32% | Yellow: <18% for 4 consecutive weeks (rolling); Red: <15% for 4 consecutive weeks | Salesforce | Weekly (4-wk rolling) |
| S3 | Dealers signed vs. plan (cumulative) | VP Sales / Head of Dealer | 12 by Y1 end | 30 by Y2 end | 55 by Y3 end | Yellow: >2 dealers behind plan; Red: >4 dealers behind plan | Salesforce Partner | Monthly |
| S4 | Blended CAC (weighted across DTC / Dealer / Referral) | CFO + VP Sales | $5,800 blended | $4,600 | $3,500 | Yellow: >15% over target for 60d; Red: >30% over target for 60d | Marketing systems + Salesforce | Monthly |

**S1 story.** We replaced raw pipeline dollar with a coverage ratio — pipeline value divided by the forward 6-month revenue target — because a $12M pipeline is meaningful only relative to what we are trying to close. A coverage ratio expressed as a 4-week rolling average also filters out the deposit-cycle noise that made a raw weekly pipeline number a false alarm every third week. The 4.0x Y1 target is the coverage discipline that produces our 350 DTC closes. Related function metrics: discovery calls scheduled/completed per week, average deal size, weighted pipeline by stage.

**S2 story.** Discovery → Deposit is the single conversion Hearth's DTC funnel lives or dies on. A discovery call is a serious, 45-minute conversation with a qualified household earning $500k+ AGI. Anything under 18% (rolling four weeks, not any single week) tells us either the concierge team is not qualifying properly upstream or the product story is misaligned to the buyer's pain. We use 4-week rolling because week-to-week variance is dominated by deposit-cycle timing, not funnel health. Related function metrics: discovery-call completion rate, time-to-deposit, deposit refund rate.

**S3 story.** Dealer signing is on-plan the entire company depends on. The alert bands are in **absolute dealer count** (percentage-point equivalent), not percentage of plan, because "20% behind plan" is a meaningless statement when the plan is 12. Being 3 dealers behind at end of Q3 is a red condition; being 3 behind at end of Q1 is expected ramp variance. The band tightens by quarter — see the dealer playbook cadence document for the quarter-specific expected targets. Related function metrics: dealer sell-through per active dealer (S3 backbone metric on Sales dashboard), dealer NPS, dealer-attach revenue.

**S4 story.** We consolidated the old three-channel CAC metric into a **blended CAC** for the board with the by-channel breakdown living on the Sales function dashboard. The board cares whether unit economics work in aggregate; whether DTC is $7k or $9k while Dealer offsets at $3k is a Sales & Marketing exec decision, made weekly, not a governance issue. Blended CAC below $5,800 Y1 gives us a payback period under 18 months at the Y1 concierge attach rate — that is the number the board needs. Related function metrics: DTC CAC, Dealer CAC, Referral CAC (all Sales dashboard).

---

### 2.3 Customer Experience (3 KPIs)

| # | KPI | Owner | Y1 Target | Y2 Target | Y3 Target | Alert Band | Data Source | Cadence |
|---|-----|-------|-----------|-----------|-----------|------------|-------------|---------|
| CX1 | Concierge NPS (quarterly, verified promoter score) | VP CX | 70 | 72 | 75 | Yellow: <65; Red: <60, OR quarter-over-quarter drop >10 points | Delighted / Qualtrics | Quarterly |
| CX2 | 1-year retention rate (billed concierge, non-cancelled) | VP CX | 96% | 97% | 97% | Yellow: <93%; Red: <90% | Salesforce + billing | Quarterly |
| CX3 | Install-day satisfaction (post-install survey, 1-5) | VP CX | 4.8 | 4.85 | 4.9 | Yellow: <4.6 in any month; Red: <4.4 in any month, OR <4.5 for 2 consecutive months | Post-install survey | Monthly |

**CX1 story.** Concierge NPS is the product's promise instantiated. The correct comparable band for Hearth is not the tech-consumer set; it is the luxury retail concierge set. **Apple Retail runs a 76 median NPS (Statista/Comparably 2024-25 syndicated benchmarks); Bang & Olufsen private-client channel benchmarks in the low 70s; Steinway retail concierge in the low-to-mid 70s; Sonos direct-to-consumer runs 62.** Our 70+ target places us **below Apple Retail's 76 median but above Sonos direct** — squarely inside the luxury-concierge benchmark band appropriate to our stage and size, not at "barrier to entry" for the category. Alert bands are in absolute NPS points, not percentages, because NPS math makes percentage bands nonsensical. Related function metrics: verbatim theme classification, promoter-to-referrer conversion, response-rate weighting.

**CX2 story.** Retention is the lifeblood of the LTV story we will pitch at Series A. A 96% Y1 retention on the $2,400/yr concierge line, holding through Y3 at 88% (3-year retention, tracked on function dashboard until Y3 when it graduates to board deck), produces the $180k LTV number underlying the pitch. **The alert bands are in percentage-point drops** — yellow at 93% is a real warning at Y1 install-base size (~600 units, so 93% = ~42 cancellations, a signal we can act on); red at 90% is a systemic issue requiring an intervention within a quarter. A 10-25% band on 96% would put yellow at 86%, which is the house on fire, not a warning. Related function metrics: monthly churn rate, cancellation-reason coding, save-desk recovery rate.

**CX3 story.** Install day is Hearth's version of the Apple unboxing moment except that unlike unboxing, it involves two technicians in a customer's home for six hours. 4.8/5 is the floor because at $95k, anything below is a referral killer. This is CX's single most important measurement in Y1 because a Y1 install base of ~600 will generate the referral flywheel that determines Y2 CAC. Related function metrics: NPS by installer team, install-completion time, installer-side quality checklist pass rate.

*Note: original v1.0 CX SLA hit rate, warranty claim rate, first-visit repair fix rate, and 3-year retention all now live on the CX function dashboard. Warranty claim rate is rolled up into board KPI P2; first-visit fix rate is a P2 sub-signal; 3-year retention becomes board deck at Y3.*

---

### 2.4 Finance (4 KPIs)

| # | KPI | Owner | Y1 Target | Y2 Target | Y3 Target | Alert Band | Data Source | Cadence |
|---|-----|-------|-----------|-----------|-----------|------------|-------------|---------|
| F1 | Monthly operating cash burn (excl. inventory working capital) | CFO | $1.20M avg | $1.65M avg | $1.85M avg | Yellow: >115% of month plan for 2 consecutive months; Red: >130% for 2 consecutive months | QuickBooks Enterprise | Weekly (monthly close) |
| F2 | Runway remaining (months at current operating burn + WC cycle) | CFO | 18mo min at seed close | 15mo min at Series A close | 18mo min at Series B close | Yellow: <15 months; Red: <12 months | QuickBooks + treasury schedule | Weekly |
| F3 | Gross margin per unit (blended DTC + Dealer, ex-install net) | CFO | 48.4% | 51.0% | 53.5% | Yellow: <45% in any quarter; Red: <42% in any quarter | NetSuite | Monthly |
| F4 | Working capital cycle (DIO + DSO − DPO, days) | CFO | 78 days | 60 days | 45 days | Yellow: >95 days; Red: >110 days for 2 consecutive months | Aggregated NetSuite + QB | Monthly |

**F1 story — rebuilt bottom-up.** Version 1.0 stated a Y1 average operating burn of $780k/mo. That number underestimated actual cost by 40-60% and would not have survived first Series A diligence contact. The correct bottom-up build for a 42-FTE Y1 hardware-plus-services company:

| Line | Y1 avg / month | Notes |
|------|----------------|-------|
| Fully-loaded headcount (42 FTE × $18k/mo blended) | $756k | Base + benefits + payroll tax + facilities allocation per FTE at Bay Area rates |
| Bay Area facilities (5,000 sqft warehouse + office) | $40k | Fremont depot + SF office; includes utilities |
| Tooling stack (see Section 5 — right-sized Y1 stack) | $2k | HubSpot + Front + Rippling + QB + Metabase (OS) + Grafana (OS) |
| Legal (Cooley retainer + M&A/deal spikes) | $15k | $10k retainer + $5k amortized deal-work |
| Insurance (D&O + Product Liability + E&O + Cyber) | $25k | Product Liability dominates at $95k SKU |
| Marketing + PR (post-Shark-Tank plan) | $150k | Digital + brand + PR agency + Shark aftermath ad spend |
| Certifications amortized (FCC/CE/UL/Prop 65/etc.) | $20k | ~$240k Y1 total spread monthly |
| Contingency + travel + software + supplies + other | $190k | Auditor/tax, cross-country travel, SaaS, R&D consumables, ~15% of headcount line |
| **Y1 average operating burn** | **~$1.20M/mo** | |

**Inventory working capital is presented as a separate line, not rolled into operating burn**, because the two behave differently on the treasury schedule and are financed differently at Series A. Y1 unit plan of 600 units × $49k COGS = $29.4M annual COGS = $2.45M/mo average inventory working capital in the WC cycle. That is *cycled* cash, not consumed — the pods sell, deposits and delivered revenue release the working capital back — but from a treasury perspective the runway math must account for both:

- **Operating burn (F1 KPI):** $1.20M/mo Y1 avg. This is the number reported to the board and the number Series A partners will underwrite.
- **Inventory working capital cycle (tracked separately on Finance function dashboard):** $2.45M/mo Y1 avg tied up.
- **Total Y1 cash consumption from unrestricted cash:** ~$3.65M/mo blended, with the inventory piece unwinding on a ~90-day cycle as DIO improves (F4).

**Runway math (F2)** uses operating burn plus average WC cycle drag; runway of 18 months at seed close assumes a $65M inclusive seed/Shark/bridge round, per the Series A pitch narrative. At Series A close mid-Y2 with $85M+ raised, we reset to 15-month floor. At Series B close, 18-month floor.

**F1 story (continued).** Cash burn is ground truth. Every other metric is theater without it. The 40-60% understatement in v1.0 came from headcount-only math without facilities, insurance, marketing, or certification lines — precisely the error that gets caught in Series A diligence. The rebuilt bottom-up is defensible line by line. Related function metrics: burn by department, opex vs plan variance, capex schedule, WC cycle drag.

**F2 story.** Runway is the CEO's single most consequential number. Below 12 months of runway, the CEO's job becomes fundraising exclusively — that is the red band, no debate. Yellow at 15 months gives us the 90-day advance window to open a raise and close before the red trigger; running to 12-month floor is a governance failure. Related: F1.

**F3 story.** Gross margin at 48.4% is the Y1 unit-economics target from the five-year model. This assumes $49k blended COGS on the $95k base plus attach plus install services net. Any quarter under 45% is a supply chain or pricing problem — VP Ops and CFO action within 30 days. Under 42% is a red-level erosion that pages the CEO. Related function metrics: COGS by SKU, freight cost per unit, install-services net margin, attach-revenue margin.

**F4 story.** Working capital cycle at 78 days Y1 means Hearth ties up roughly $6M in working capital at Y1 exit run rate. This directly informs the Series A raise size. Contribution margin, DSO, DIO all now live on the CFO function dashboard because they are drivers into F4 rather than independent board decisions; F4 is the summary the board acts on. Related function metrics: DIO, DSO, DPO, contribution margin, cash conversion cycle by SKU.

---

### 2.5 Engineering (3 KPIs)

| # | KPI | Owner | Y1 Target | Y2 Target | Y3 Target | Alert Band | Data Source | Cadence |
|---|-----|-------|-----------|-----------|-----------|------------|-------------|---------|
| E1 | P0 bugs open (count + median age) | VP Engineering | 0 steady state | 0 | 0 | Yellow: any P0 open >24h; Red: any P0 open >72h (auto-red, pages CEO) | Linear | Daily |
| E2 | Security patch time (critical CVE to GA release) | Head of Security | 72h | 48h | 24h | Yellow: any critical CVE >72h; Red: any critical CVE >96h | GitHub + advisory feeds | Per incident |
| E3 | Fleet firmware update pull success rate (14-day post-release) | Head of Firmware | 96% within 14 days | 98% within 10 days | 99% within 7 days | Yellow: <92% at 14 days for any release; Red: <88% at 14 days for any release | Fleet telemetry | Per release |

**E1 story.** P0s are production-down or safety issues. Zero steady state is the target because any open P0 is by definition a customer-affecting bug. A P0 open more than 72 hours pages the CEO and requires an incident postmortem within a week. Sub-signals — CI green rate, P1 bug count and median age, third-party audit findings closure — live on the Engineering function dashboard and feed P3 (firmware cadence) escalation logic. Related function metrics: P1 bug count and median age, CI green rate, audit findings closure rate.

**E2 story.** Security patch time is the number that determines whether Hearth becomes the news story. An offline-first product still has an attack surface — OTA update mechanism, local network exposure, edge AI models. 72h is the industry-competitive target for critical CVE-to-GA; 24h Y3 is aspirational and requires the Head of Security to have staff-engineer bench depth by Y3. Related function metrics: SOC 2 findings status, penetration test schedule, third-party audit progress.

**E3 story.** Fleet update pull success rate is the fingerprint of firmware quality and OTA reliability combined. If we ship an update that only 88% of the install base can pull in 14 days, we have both a firmware bug and a distribution bug. This metric ladders directly to P3 (firmware cadence) and P2 (field defect rate). Related function metrics: OTA retry success, update failure by hardware revision, rollback rate.

---

### 2.6 Company (3 KPIs)

| # | KPI | Owner | Y1 Target | Y2 Target | Y3 Target | Alert Band | Data Source | Cadence |
|---|-----|-------|-----------|-----------|-----------|------------|-------------|---------|
| C1 | Employee headcount vs plan | Head of People | ±5% of plan | ±5% | ±5% | Yellow: >10% short of plan for 60d; Red: >15% short for 90d | Rippling | Monthly |
| C2 | Employee attrition (12-mo rolling regretted) | Head of People | <12% | <14% | <15% | Yellow: >15% rolling 12mo; Red: >18% rolling 12mo | Rippling | Monthly |
| C3 | Diversity in interview pipeline (slate composition) | Head of People | 40% of interview slates include ≥1 candidate from underrepresented groups | 45% | 50% | Yellow: <30% in any quarter; Red: <25% in any quarter | Rippling ATS | Quarterly |

**C1 story.** Headcount is the enabler of every other plan. Y1 EOY plan is 42 FTE. More than 15% short for 90 days and we cannot execute the Y1 unit ramp — this is a CEO-level flag. The bands moved from percentage of plan to percentage-plus-duration to filter open-req noise (any given month can be under target while an offer is out). Related function metrics: time-to-fill by role, offer acceptance rate, open reqs by function.

**C2 story.** Regretted attrition below 12% Y1 is a healthy hardware-plus-software startup. Above 18% is a culture problem or a compensation problem; either way it is CEO-level. We report regretted (voluntary + performance-managed) separately from total attrition on the function dashboard, but the board KPI is regretted only. Related function metrics: total attrition, attrition by function, exit-interview theme coding.

**C3 story.** Diversity in the recruiting pipeline is measured at the interview slate stage because that is the only leading indicator management controls. Outputs at the hire level are diagnostic; inputs are actionable. Related function metrics: hire mix outcomes, sourcing channel diversity, offer acceptance by demographic.

*Note: original v1.0 board attendance rate, founder personal hours self-report (C5 — dropped, see Section 4 for rationale and the ops-memo replacement), and advisor board activity all moved to Company function dashboard or the ops memo. Board attendance stays visible via board portal metadata and needs no separate KPI at a 5-person board.*

---

**Board KPI count: 20** (Product 3, Sales 4, CX 3, Finance 4, Engineering 3, Company 3).

**Revisit at Series A close (target Q1 2027).** At that point Hearth has hired a data engineer (per Section 5 hire ramp), has ~2,000 pods in the field generating meaningful cohort signal, and the framework will expand toward 30 board KPIs with the additions specified in Section 9. Y1 discipline is 20 because we do not have the instrumentation staff to defend more without diluting focus.

---

## 3. Reporting Cadence

### Daily Automated Dashboards
Refreshed hourly, viewable by any FTE via SSO:
- Cash balance + daily burn delta (F1)
- Unit shipments YTD + today (P1)
- P0 bugs open, by age (E1)
- Firmware CI status (Engineering function dashboard, feeds P3)

Delivered to Slack channel `#hearth-vitals` every morning at 07:00 PT. If any board KPI is in a yellow or red band, the on-call function head must acknowledge within 30 minutes.

### Weekly All-Hands Ops Review
- **Attendees:** COO (chair), CEO (as needed), VP Product, VP Sales, VP CX, VP Engineering, CFO, Head of People
- **Duration:** 60 minutes, Mondays 10:00 PT
- **Format:** Review all yellow and red KPIs from prior week (board and function-dashboard), confirm action plans, surface leading indicators trending toward yellow. Ops memo signals (Section 4) also reviewed here.
- **Deliverable:** Weekly ops memo posted to the exec channel by end of Monday

### Monthly CEO Business Review (CBR)
- **Attendees:** CEO, COO, all VPs, CFO, Head of People, Head of Firmware, Head of Security, Head of Concierge, Head of Dealer
- **Duration:** 3-4 hours, first Wednesday of each month
- **Format:** Deep dive across all 20 board KPIs plus material function-dashboard signals. Function heads present their own metrics. CEO probes anomalies. Board packet drafted after.
- **Deliverable:** CBR memo distributed to full company by end of week

### Quarterly Board Review
- **Attendees:** Full board (5), CEO, COO, CFO. Selected VPs on standby.
- **Duration:** 4 hours + private session
- **Format:** Board packet reviewed. Strategic asks and risks discussed. Voting items handled.
- **Deliverable:** Board packet (Section 11 template), signed minutes, resolutions

### Annual Review + Planning
- **Attendees:** Board + full exec team
- **Duration:** 2-day offsite
- **Format:** All 20 board KPIs reviewed. New Y+1 targets set. KPI framework itself reviewed — additions, retirements, band recalibrations. Ranked initiatives voted. Comp cycle framework approved.
- **Deliverable:** Annual operating plan, board-approved budget, ranked initiative list, KPI framework v(next)

---

## 4. Alerting + Escalation (Metric-Specific Bands)

Version 1.0 used blanket percentage bands (10% yellow / 25% red) which produced two well-known failure modes: (a) triggering on statistical noise for volatile weekly metrics and (b) hiding real emergencies for tight-range metrics like retention (10% off a 96% retention target lands yellow at 86% — that is not a warning, that is the house on fire). This version uses **metric-specific bands** matched to each KPI's scale, volatility, and lead time. Bands are stated inline in Section 2 KPI tables; general policy below.

### Alerting Band Policy

- **Volatile weekly metrics (S1 pipeline coverage, S2 conversion rate):** 4-week rolling average, band on percentage-point delta from target, not percentage of target. Weekly noise is filtered out by construction.
- **Retention (CX2, 96% target):** percentage-point bands. Yellow at 93% (3 pt below target). Red at 90% (6 pt below target). This gives us a warning that is actually a warning.
- **Cash and runway (F1, F2):** F1 by percentage of monthly plan with 2-month duration filter (single-month burn spikes are normal for hardware pre-buys). F2 by absolute months of runway: yellow at 15 months, red at 12 months. No debate.
- **NPS (CX1):** absolute NPS points. Yellow at 65, red at 60. Percentage bands make no sense for NPS math.
- **Product reliability (P2):** percentage-point band on defect rate rolling 90-day, plus a hard automatic-red trigger for any Halbach field failure below 5,000 hr MTBF regardless of aggregate rate.
- **Engineering age metrics (E1, E2):** absolute hours/days on open item age. No rolling averages — a P0 open 72 hours is 72 hours.
- **Headcount and attrition (C1, C2):** duration-conditioned bands (>10% short for 60 days, not >10% short in any single month) to filter open-req and hiring-cycle noise.

The full band definitions live inline in the Section 2 KPI tables. Any band change requires COO + CFO signoff and appears in the next board packet definition-change appendix.

### Critical Event Definitions (Automatic Red, Board-Chair Escalation Within 24h)

- Any **P0 bug in production** open >72h (customer-affecting, no workaround)
- **Field defect rate (P2)** spike >1.5 percentage points month-over-month
- **Concierge NPS (CX1)** quarter-over-quarter drop >10 points
- **Cash runway (F2)** falls below 12 months
- Any **security incident** with customer data exposure or CVE assigned
- **Loss of key executive** (any C-suite or VP-level departure)
- **Halbach levitation field failure** <5,000 hr MTBF (product-defining physical failure)
- Any **regulatory inquiry** (FCC, FTC, CPSC, state AG)
- **Loss of tier-1 dealer** post-Founding tier signing

### Dropped: C5 Founder Personal Hours (v1.0)

Version 1.0 tracked founder personal hours per week as a self-reported burnout signal (C5). We dropped it from the board framework because self-reported hours will be gamed — either by the founder minimizing to protect the KPI, or by the founder overstating to signal commitment. Neither reading is useful to the board.

The underlying concern — founder burnout as an existential risk — is real. We replace it with two things:

1. **Ops memo signal (not a board KPI):** "Founder unavailable for >5 consecutive business days" is a signal flagged in the weekly ops memo when it occurs, tracked via calendar and comms availability. This is factual, not self-reported.
2. **Chief of Staff quarterly narrative:** A one-paragraph narrative from the Chief of Staff on the CEO's calendar composition, decision-load index, and travel schedule, presented in the private board session (not the deck). This is qualitative and appropriate to how boards actually handle founder health.

### Escalation Chain
- **Yellow:** Function head → COO → weekly ops review
- **Red:** Function head → COO → CEO → Board chair (within 24 hours)
- **Critical event:** Function head → CEO simultaneously → Board chair within 4 hours → Full board within 24 hours

---

## 5. Tooling Stack + Implementation

Version 1.0 specified Salesforce Enterprise + Zendesk Enterprise + BigQuery + Fivetran + Metabase pre-Series A. That stack runs $8-12k/mo and — more importantly — implies that the COO or a founder is running BigQuery pipelines pre-Series A. Neither is right for the 42-FTE Y1 team. We move to a right-sized Y1 stack and lay out the upgrade path at Series A close.

### Y1 Tooling Stack (pre-Series A)

| Layer | Tool | Y1 Cost/mo | Purpose |
|-------|------|------------|---------|
| CRM / pipeline | HubSpot Starter | ~$200 | Pipeline, deposits, discovery calls, dealer ops |
| Concierge inbox | Front (~10 seats) | ~$250 | Concierge tickets, SLA tracking, shared inbox |
| HR + payroll + ATS | Rippling (42 FTE) | ~$840 | Headcount, attrition, comp, DEI reporting |
| Finance / GL | QuickBooks Enterprise | ~$200 | GL, AP, AR, cash |
| BI dashboards | Metabase (open source, self-hosted) | $0 | Board deck KPIs, function dashboards |
| Fleet telemetry / eng | Grafana + Prometheus (open source, self-hosted) | $0 | Fleet metrics, CI status |
| **Y1 total tooling** | | **~$1,500/mo** | |

**Data infrastructure Y1:** direct connectors from HubSpot / Front / Rippling / QB into Metabase via native integrations and CSV extracts, with weekly refresh. No BigQuery, no Fivetran, no Airflow, no data engineer pre-Series A. Fleet telemetry pipes into Grafana/Prometheus directly. This is deliberately unglamorous — it is the stack that runs itself with a fractional analyst and does not require a full-time data engineer.

### Series A Close Upgrade Path (Q1 2027)

Immediately after Series A close, we execute a planned platform migration. The Series A raise budget includes the migration line items and the data-engineer hire.

| Layer | Y2 Tool | Y2 Cost/mo | Trigger |
|-------|---------|------------|---------|
| CRM / pipeline | Salesforce Enterprise | ~$3,300 | Dealer channel scale requires Salesforce Partner Cloud |
| Concierge support | Zendesk Enterprise | ~$1,150 | Overnight tier + tooling needs Zendesk workflows |
| Data warehouse | BigQuery + Fivetran | ~$2,500 | Warehouse consolidation for board reporting + Series B diligence |
| BI dashboards | Migrate Metabase → Looker | ~$1,500 | Dashboard governance at scale |
| Fleet telemetry / eng | Grafana + Prometheus (stay) + Sentry | ~$400 | Sentry for error tracking |
| Finance / GL | QuickBooks Enterprise (Y2), NetSuite (Series B) | +$0 Y2 | NetSuite deferred to Y3 |
| **Y2 total tooling** | | **~$8-12k/mo** | |

### Data Engineer Hire: Q1 2027 (post-Series A close)

Per the Founder Narrative hiring ramp, the data engineer is a Series-A funded hire in Q1 2027. Their first 90 days: (a) migrate Metabase content to Looker, (b) stand up BigQuery + Fivetran, (c) implement dbt-based transformation logic, (d) instrument the Y2 additional board KPIs (Section 9). Second data engineer added mid-Y2.

We do not pretend a founder, COO, or fractional analyst is running BigQuery pipelines pre-Series A. The Y1 stack is deliberately sized so that they do not have to.

### Metabase Dashboard Structure (Y1)

- **CEO Vitals dashboard** — the 8 critical KPIs (Section 7)
- **Board Deck dashboard** — all 20 board KPIs, quarterly view
- **Function dashboards** — one per function (Product, Sales, CX, Finance, Engineering, Company), containing the board KPIs for that function plus function-owned operational KPIs
- **Alert view** — any KPI currently yellow or red

Every dashboard tile links to a definition page in the internal wiki. No KPI ships without a definition entry that includes: name, owner, calculation, data source, refresh cadence, alerting band, related KPIs, and the story.

---

## 6. Data Quality Principles

1. **Every metric has an owner, definition, calculation, and data source.** No exceptions. A KPI without all four does not ship to Metabase. This is a governance rule enforced by the COO on quarterly review.
2. **No metric appears on the board deck that cannot be defended in 2 minutes.** If the CEO cannot explain in two minutes to a Series A partner why a number is what it is, that metric is either wrongly instrumented or wrongly on the board deck. Both are actionable.
3. **Retroactive changes to targets require board notice.** If the Y1 target for gross margin was set at 48.4% and mid-year we want to revise to 45%, that is a governance-level change and requires notice in the next board deck.
4. **Changes to KPI definitions require board approval.** If we change the calculation of concierge NPS from a quarterly survey to a monthly rolling survey, the definitional change goes to the board for approval before the metric moves. This prevents the well-known startup pathology of quietly redefining KPIs to make them green.
5. **Historical data preserved forever.** Every KPI value is written to storage with a timestamp and definition version.
6. **Version-controlled definitions.** The internal wiki entry for each KPI is under version control in a private GitHub repo. Diffs are reviewed by the COO and CFO before merge.
7. **Anomaly review.** Any KPI moving >30% week-over-week without a scheduled event (launch, close, campaign) is auto-flagged for data quality review.
8. **Sacred numbers vs. exploratory numbers.** The 20 board KPIs are sacred. Function-level operational KPIs are exploratory and may be iterated on freely by the owning function.

---

## 7. The Critical 8 — First Quarterly Board Meeting Post-Shark-Tank

**Fiscal frame — restated explicitly.** Hearth's Shark Tank episode airs at the **start of Year 1** (target airdate: early Q1 Y1). "Q1 post-air" and "Q1 of Y1" are the same quarter. This produces the following coherent Y1 shape:

| Y1 Quarter | Units Booked (deposits) | Units Delivered | Notes |
|------------|-------------------------|-----------------|-------|
| Q1 (post-air) | 150 units / $18M booked | 40 units / $4.8M delivered | Post-Shark-Tank spike drives bookings; delivery ramp constrained by supply chain; ~13/mo delivery avg |
| Q2 | 200 | 120 | 40/mo avg delivery; deposit-to-delivery lag ~45 days catches up |
| Q3 | 200 | 180 | 60/mo avg delivery; Certified dealer tier activates |
| Q4 | 200 | 260 | 87/mo avg delivery peak; Q4 exit run rate ~75/mo steady-state (~900 annualized) |
| **Y1 total** | **~750 booked** | **~600 delivered** | ~150 units in deposit backlog at Y1 close |

The deposit backlog at Y1 close (~150 units, ~$18M deposited) becomes Q1 Y2 revenue realization. This reconciles the previously ambiguous "Q1 post-air 150 units booked / Y1 600 units delivered" numbers: bookings run ahead of deliveries because the supply chain cannot ramp in Q1 to meet the Shark-Tank demand spike, and the backlog carries forward.

These 8 KPIs get a full slide each in the first-post-air board deck. The other 12 board KPIs land in an appendix table:

1. **Total revenue booked** ($ + units) — top-line demand signal. Target Q1 post-air: $18M booked / 150 units.
2. **Total revenue delivered** ($ + units) — operational fulfillment signal. Target Q1 post-air: $4.8M / 40 units.
3. **Gross margin per unit** (F3) — unit-economics test. Target: 46-49%.
4. **Cash burn + runway** (F1, F2) — survival test. Target: $1.20M/mo operating burn, 18+ months runway.
5. **Concierge NPS** (CX1) — product-love signal. First 40 delivered pods generate first NPS reading. Target: 70+ (Apple Retail 76 median; Sonos direct 62; Hearth appropriate benchmark band).
6. **Employee headcount vs. plan** (C1) — execution capacity signal. Target: 42 FTE by Y1 end, on ramp by Q1.
7. **P0/P1 bugs open** (E1 + function dashboard) — product stability signal. Target: 0 P0, ≤12 P1 with median <14 days.
8. **Dealer signed count vs. plan** (S3) — channel expansion signal. Target: 4-6 Founding dealers signed by Q1 post-air.

Each of these 8 gets a full slide: value, trend chart (12 weeks), band (green/yellow/red), owner commentary (2-3 sentences), 2 related KPIs.

---

## 8. Series A Pitch Additions

Series A raise (target Q1 2027, i.e., mid-Y2) surfaces additional KPIs that speak specifically to investor diligence. These are pitch-deck augmentations, not additional board KPIs:

- **Waitlist conversion-to-deposit rate.** Numerator: qualified waitlist entries that convert to paid deposits within 180 days of joining. Denominator: qualified waitlist entries (qualified = passed initial concierge screening + income verification). Target for Series A pitch: 12%+ conversion within 180 days. **This replaces the v1.0 "Waitlist growth rate" metric,** which was a raw-count vanity number contradicting our own Section 10 anti-KPI stance. Raw waitlist growth is tracked internally for demand-durability sensing but is **not** presented to the board or in the Series A pitch.
- **Customer LTV.** Built from first 90-day install data plus concierge attach and extender attach. Series A LTV target: $180k over 5 years, blended.
- **Cohort retention 30d / 90d / 180d.** The confidence metric on the LTV number.
- **Revenue per dealer per quarter.** Segmented Founding / Certified / Standard. Defends the $300k+ annual revenue per active dealer target by end of Y2.
- **Referral rate.** Percentage of new closed deals traceable to an existing customer referral. Series A target: 20%+ by end of Y1. Network-effect proof.
- **Gross margin trajectory.** Not just current GM, but the slope. Series A partners will pay for margin expansion.
- **Concierge cost per household per year.** Series A target: $1,850 per household per year at 1:50 ratio, dropping to $1,400 by Y3.
- **AI inference cost per household per month.** Target: $0 (on-pod inference, no cloud spend) — distinguishing metric.

---

## 9. Y2+ Board KPI Additions (Post-Series A Close)

At Series A close (target Q1 2027), we expand the board deck toward 30 KPIs as instrumentation staff and install-base signal both mature. Confirmed additions:

- **3-year retention rate** (graduates from CX function dashboard to board at Y3).
- **Referral rate** (graduates from Series A pitch to board).
- **International revenue mix** (Y2: 15%; Y3: 25%).
- **Dealer sell-through by tier** (Founding vs. Certified vs. Standard).
- **Contribution margin** (graduates from Finance function dashboard).
- **Concierge SLA hit rate** (graduates from CX function dashboard).
- **Halbach MTBF** (graduates from Engineering function dashboard as a standalone board KPI once install base >2,000 gives statistically meaningful reads).
- **Language-specific concierge NPS** (once multilingual concierge team is operational).
- **Cross-locale repair time comparison** (once international markets active).

---

## 10. Anti-KPIs — Metrics We Explicitly Don't Chase

We commit in writing not to track as board KPIs or optimize the business against:

- **Raw waitlist size, without conversion cohort attached.** This is the most important anti-KPI to name explicitly. Post-Shark-Tank we expect a 5,000+ waitlist spike, and every advisor will suggest we headline it. We refuse. Raw waitlist size is tracked internally for demand-durability sensing but is **not presented to the board and not used in the Series A pitch.** The only waitlist metric that ships is **conversion-to-deposit rate** with a qualified-entry denominator (Section 8). This resolves the contradiction with v1.0 Section 8.
- **Shark Tank aftermath press mentions and impressions.** We expect thousands. None convert. A NYT feature that does not produce discovery calls is decoration.
- **"Concierge story of the week" without measurable business impact.** Anecdotes are for internal culture, not for the board. If a concierge story matters, it shows up in NPS verbatim theme analysis or retention.
- **GitHub commits per day, meetings held, docs written, Slack activity, demo count without qualified follow-up.** These are the actually-insidious 2024-era vanity metrics for hardware+services startups. We refuse them by name.
- **Website hits, unique visitors, sessions.** Only qualified-lead traceability from web traffic counts.
- **Social media followers, impressions, engagement rate.** Only if traceable to qualified lead.
- **Absolute units shipped per month, unweighted by defect rate.** We refuse to reward shipping speed at the expense of P2.
- **Employee happiness surveys divorced from retention and performance.** We measure C2 and pattern with exit interviews, not with pulse surveys.
- **Customer NPS in isolation.** NPS without retention (CX2) tells us how a customer felt in a survey moment, not what they did.
- **Time to first response (concierge) if optimized in isolation.** A 30-second response with a wrong answer is worse than a 5-minute response with the right one.
- **Founder time in the office / at the desk / hours self-reported.** Explicitly dropped from v1.0 as C5.
- **Number of features shipped.** A team that ships 40 features that no one uses is worse off than a team that shipped 4 that transformed the product.
- **Number of dealers signed if optimized in isolation.** S3 count is meaningless without dealer sell-through.
- **Vanity ARR extensions.** Multi-year concierge commitments are not booked as new-ARR.

**Cross-reference: raw waitlist growth is tracked internally but is NOT presented to the board and NOT included in the Series A pitch.** The Series A pitch metric is waitlist conversion-to-deposit rate with a qualified-entry denominator. The v1.0 contradiction is resolved.

---

## 11. Board Packet Template

Each quarterly board packet follows the same 20-25 page structure. Template lives at `/data-room/03_KPI_Framework/board_packet_template.docx`.

### Cover Page
Company name, quarter, date, meeting number, list of attendees, resolutions pending.

### Executive Summary (1 page)
- CEO letter (400 words): what shipped, what missed, what changed
- The 8 critical KPIs as an at-a-glance table with band coloring
- Top 3 asks of the board

### Critical KPI Deep Dive (8 pages, one per critical KPI)
Each page: current value, target, trend chart (12 weeks or 4 quarters), band, owner commentary (2-3 sentences), 2 related KPIs.

### Function-by-Function Deep Dive (6 pages)
- Product (1 page): roadmap status, all 3 Product board KPIs, top 3 function-dashboard signals, upcoming milestones
- Sales (1 page): pipeline coverage, DTC + dealer split, all 4 Sales board KPIs, top 3 function-dashboard signals
- CX (1 page): NPS, retention, install-day, all 3 CX board KPIs, top 3 function-dashboard signals
- Finance (1 page): P&L, cash, balance sheet, working capital, all 4 Finance board KPIs
- Engineering (1 page): all 3 Engineering board KPIs plus top function-dashboard signals
- Company (1 page): all 3 Company board KPIs plus Chief of Staff qualitative CEO-calendar narrative (private session)

### Financial Appendix (3 pages)
GAAP + management P&L. Cash flow statement. Balance sheet. Deferred revenue schedule. Operating burn (F1) vs inventory working capital (tracked separately).

### Strategic Asks (1-2 pages)
Formal board asks: comp band changes, executive hires, budget reallocations, term sheet approvals.

### Risks (1 page)
Top 5 risks by impact × likelihood, with current mitigation status and residual risk owner.

### Ranked Initiatives + Forward Pipeline (2 pages)
Next-quarter ranked initiatives (top 10), forward-looking sales pipeline, hiring pipeline, product roadmap next 2 quarters.

### Appendix — Full 20-KPI Table (1 page)
The remaining 12 board KPIs in a single dense table.

### Appendix — Definitions (1 page)
Any KPI definition changes since last board meeting, with rationale and approval status.

---

## Closing

This framework is meant to be operated, not admired.

In Y1 we run 20 board KPIs, deliberately scoped small because we do not yet have the data-engineering staff to defend more without diluting focus. Roughly 40 function-level KPIs sit on function dashboards, owned by function heads, reviewed at the weekly ops review — not in the board deck.

**At Series A close (target Q1 2027), we revisit.** With a data engineer hired, the BigQuery warehouse stood up, and >2,000 pods in the field generating cohort signal, the board deck expands toward 30 KPIs per Section 9. This is not a promise to add complexity for its own sake — it is a plan to add board-level visibility when we can staff it and when the signal exists to warrant it.

Any changes to this framework go through the definition-change process in Section 6. The framework is version-controlled at `/data-room/03_KPI_Framework/framework.md`.

Series A partners will diligence this document. They will pull three KPIs at random and ask us to defend the number, the calculation, the data source, and the story. This framework is written so any of the 20 can be defended in under two minutes by the owning function head — and so any function-dashboard metric can be defended in under two minutes by the function head as well.

The number we watch most closely is not on this list: it is the number of KPIs a member of the exec team can rattle off, in order, at a Series A dinner, when asked "what are you optimizing?" If the answer is 20, the framework works. If the answer is 3, we have failed at everything except attention economics. If the answer is 200, we have failed at leadership.

The framework works.

— Chief Operating Officer, Hearth
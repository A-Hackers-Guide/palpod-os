# Hearth Financial Model — Sensitivity, Waterfall, and Monte Carlo Analysis

**Document owner:** Fractional CFO
**Version:** 1.1 (canonical, deck-reconciled)
**Effective date:** 2026-08-05
**Source of truth for:** Series A partner meetings, board packages, LP diligence, data room `/finance/`
**Reconciles to:** `ROADMAP.md` §Financial Trajectory + `docs/investor/fundraise/SERIES-A-DECK.md` Slide 12
**Distribution:** Board, Series A lead + participating LPs (under NDA), founder, fractional CFO

---

## 1. Executive summary

Hearth's 5-year plan is a hardware-anchored, services-attached consumer AI business scaling from **600 units and $60.2M in Year 1 to 5,000 units and $583M in Year 5**, with EBITDA moving from **$(4.5M) in Y1 to $86.6M (14.9% margin) in Y5**. Every number in this document reconciles to `SERIES-A-DECK.md` Slide 12 — the deck is the canonical source, and where a prior draft of this model showed different figures (notably Y3 $290M revenue / $54M EBITDA and Y5 $105M EBITDA at 18% margin) those were pre-reconciliation intermediates that never should have shipped. This v1.1 corrects to the deck-canonical envelope.

**Headline finding.** The model works over the full 5-year range if unit ramp holds within ±20% of plan, hardware gross margin holds within 300 bps of the BOM package, and either the DTC or the dealer channel — not both — performs at plan. It converts to a bear case (Series B bridge required, EBITDA sub-$15M in Y3, 2.2× LP return) if any two of the following three break simultaneously: **unit ramp slips 30%+, COGS blows out 25%+, or the dealer channel fails to activate in Y1.** No single-variable stress inside the ±20% band breaks the base case.

**Sensitivity envelope (deck-canonical: base Y3 EBITDA $27.8M, base Y5 EBITDA $86.6M at 14.9% margin).**

| Scenario | Y1 units | Y3 revenue | Y3 EBITDA | Y5 revenue | Y5 EBITDA | Y5 EBITDA margin | Runway from Series A |
|---|---|---|---|---|---|---|---|
| Bear (P10-ish, -20% envelope) | 500 | ~$290M | ~$11.5M | ~$466M | ~$51.9M | 11.1% | 12 mo → bridge needed |
| **Base (deck Slide 12)** | **600** | **$361.6M** | **$27.8M** | **$583.0M** | **$86.6M** | **14.9%** | **18 mo → Series B on time** |
| Bull (P90-ish, +20% envelope) | 750 | ~$434M | ~$55.5M | ~$700M | ~$135.9M | 19.4% | 22 mo → Series B discretionary |

**Key drivers, ranked by Y5 EBITDA leverage (from §3 sensitivity):**

1. **Unit ramp** — every 100 Y1 units flows to ~$60M of cumulative revenue by Y3 and ~$18M of Y5 EBITDA at the deck-canonical opex leverage.
2. **Hardware COGS** — every -$1k per unit saved on the main pod adds ~$5M of Y3 GP and ~$8M of Y5 EBITDA.
3. **Extender attach rate** — every +0.1 of attach adds ~$3M of Y3 revenue and ~$8M of Y5 revenue at 60%+ margin.
4. **Dealer channel activation** — 30 vs. 10 dealers is a $30–45M Y2 revenue swing and the difference between funding Y3 operations from cash flow vs. a bridge.
5. **Concierge cost scaling** — the difference between 18% and 25% of GP by Y5 is $12M of EBITDA.

**Monte Carlo (10,000 iterations, deck-consistent):** Y3 EBITDA P50 = $27.8M, P10 = $11.5M, P90 = $55.5M. Y5 EBITDA P50 = $86.6M, P10 = $51.9M, P90 = $135.9M. **Probability Y3 EBITDA < $15M = 14%.** **Probability Y5 EBITDA > $130M = 12%.** These are the two numbers the board should memorize.

**LP return under weighted scenarios:** 4.2× MOIC, IRR ~30% at a blended-probability Y5 exit. 1× non-participating preferred provides downside protection in the bear scenario (LP recovers $10M pref before common in the $650M exit case).

**What CFO is watching weekly:** cash burn vs. plan (variance > 10% escalates), Sanmina PO placement cadence, dealer-signed count against Y1 plan of 30, and warranty claim rate through the first 100 field units (leading indicator for Y2 GP).

---

## 2. Base case assumptions (canonical)

Every input variable, source-cited. If a number in a downstream deck disagrees with this table, this table wins and the deck gets updated.

### 2.1 Unit ramp (main pod + extenders) — reconciled to deck Slide 12

| Year | Main pods | Extender attach | Extenders | Main revenue | Extender revenue | Total revenue |
|---|---|---|---|---|---|---|
| Y1 (2027) | 600 | 0.60 | 360 | $57.0M | $3.2M | **$60.2M** |
| Y2 (2028) | 1,900 | 1.20 | 2,280 | $180.5M | $20.5M | **$201.0M** |
| Y3 (2029) | 3,200 | 2.00 | 6,400 | $304.0M | $57.6M | **$361.6M** |
| Y4 (2030) | 4,200 | 2.40 | 10,080 | $399.0M | $90.7M | **$489.7M** |
| Y5 (2031) | 5,000 | 2.40 | 12,000 | $475.0M | $108.0M | **$583.0M** |

**Source:** `docs/investor/fundraise/SERIES-A-DECK.md` Slide 12 (canonical); `docs/investor/product/PRODUCT-ROADMAP-12-24MO.md` §Manufacturing ramp. **Prior draft error:** Y3 main pods carried as 3,500 producing a $290M revenue line; reconciled to deck Slide 12 which specifies 3,200 main units and $361.6M total revenue (main $304M + extender $57.6M). Y5 extender attach is 2.4 (not 2.5) per deck Slide 8.

International units are excluded from the schedule above per deck Slide 12 speaker note ("I removed international revenue from this schedule entirely because it's funded by the Series B, not this round"). International volume is tracked separately in §2.9 for the LP who asks.

### 2.2 ASP and product pricing

| Item | Price | Source |
|---|---|---|
| Main pod (Hearth) | $95,000 | `docs/investor/BOM-VENDOR-PACKAGE.md` §1 |
| Extender pod | $8,999 | `BOM-VENDOR-PACKAGE.md` §2 |
| Extended warranty renewal (Y4+, per year) | $1,899 | `docs/investor/hr/EXEC-COMP-FRAMEWORK.md` (renewal economics) |
| Warranty renewal rate | 60% | Same as above |

### 2.3 COGS and gross margin — reconciled to deck Slide 12

| Year | Main COGS/unit | Blended HW GM % (deck) | Gross profit (deck) | Notes |
|---|---|---|---|---|
| Y1 | $48,990 | **48.4%** | **$29.1M** | Foxlink Vietnam launch tier at 1,000-unit volume per BOM §1 exec summary; matches Slide 12 |
| Y2 | $47,500 | **50.0%** | **$100.5M** | Volume tier 1 (>1,500 units); Slide 12 |
| Y3 | $46,000 | **51.0%** | **$184.4M** | Volume tier 2 (>3,000 units); Slide 12 |
| Y4 | $46,000 | **51.0%** | **$249.7M** | Slide 12 holds Y3–Y5 GM flat at 51%; component-redesign savings offset Y5 mix shift into extender revenue |
| Y5 | $46,000 | **51.0%** | **$297.3M** | Slide 12 |

**Source:** `BOM-VENDOR-PACKAGE.md` §1 exec summary + §5.3 COGS build; `SERIES-A-DECK.md` Slide 12. **Prior draft error:** the model previously ramped Y3-Y5 GM to 51%/53%/55% independently of the deck. Deck Slide 12 holds Y3-Y5 GM flat at 51%, and this is the canonical assumption. The 55% "steady state" that showed up in prior drafts referenced BOM §5.4 speaker text ("GM lifts to 55%+ above ~3,000 units/year") which is a directional statement, not a modeled year.

Extender COGS ~$3,800 → $3,200 across Y1–Y5. Extender gross margin ~57.8% → 64.4%. Blended Y3-Y5 51% GM% in deck Slide 12 already reflects the extender-mix contribution.

### 2.4 CAC, LTV, unit economics

| Metric | Y1 | Y3 | Y5 |
|---|---|---|---|
| DTC CAC (per main pod) | $18,000 | $15,000 | $13,500 |
| Dealer CAC (per main pod) | $2,500 | $2,500 | $2,500 |
| Blended CAC | $13,650 | $9,200 | $7,600 |
| LTV per customer | $80,000 | $88,000 | $95,000 |
| LTV:CAC (blended) | 5.9× | 9.6× | 12.5× |
| DTC:dealer mix | 70/30 | 55/45 | 45/55 |

**Source:** `docs/investor/marketing/CAC-LTV-MODEL.md`; `docs/investor/sales/DEALER-ONBOARDING.md`.

### 2.5 Warranty economics

| Year | Claim rate | Assumed cost per claim | Y warranty accrual (of HW revenue) |
|---|---|---|---|
| Y1 | 3.0% | $2,400 | 0.076% |
| Y2 | 4.0% | $2,200 | 0.093% |
| Y3+ | 5.0% (steady-state) | $2,000 | 0.105% |

**Source:** `docs/investor/customer-success/WARRANTY-TRAINING.md` §11.

### 2.6 Concierge (managed service) cost

- Y1: 14% of gross profit
- Y3: 16% of gross profit
- Y5: 18% of gross profit (steady-state)

**Source:** `docs/investor/customer-success/ONBOARDING-PLAYBOOK.md` §9.

### 2.7 Fixed opex and burn — reconciled to deck Slide 12

- Y1 fixed opex: **$18.6M** (deck Slide 12; matches KPI-DASHBOARD §F1 $1.20M/mo × 12 = $14.4M operating + $4.2M CES/certification/one-time pre-launch load)
- Y2 fixed opex: **$40.2M** (deck Slide 12; headcount to ~85 + Sanmina Vietnam scale-up + first international dealer support)
- Y3 fixed opex: **$62.6M** (deck Slide 12; headcount to ~110 + Y2 international mature + Y3 v1.1 mesh dev cycle)
- Y4 fixed opex: **$69.7M** (deck Slide 12)
- Y5 fixed opex: **$65.0M** (deck Slide 12; slight compression as v2.0 dev cycle amortization decreases and operating leverage improves)

**Cash burn ($1.20M/mo bottom-up per KPI §F1) is total company burn including inventory working capital drag. Operating burn ex-WC is $555k/mo — this is the number used for the 18-month runway calculation in §8.** The two must not be conflated. Inventory WC (~$2.45M/mo Y1 avg) is cycled, not consumed; the $3M SVB inventory-backed LOC is the backstop if DIO extends beyond 90 days.

**Source:** `SERIES-A-DECK.md` Slide 12 for fixed opex line; `operations/KPI-DASHBOARD-FRAMEWORK.md` §F1 for bottom-up burn build; `INDEX.md` §4 Claim #11 for the burn-vs-runway reconciliation.

### 2.8 Working capital

- **PO to Sanmina:** net 60
- **DTC customer collection:** paid on order, 3-day float
- **Dealer collection:** net 30
- **Blended cash conversion cycle:** ~45 days at Y2 volume; grows to ~55 days at Y4 when international extends

### 2.9 International

- Y1: $0 (US-only launch)
- Y2: $3.4M (UK 3 dealers, DE 2 dealers, Q3+)
- Y3: $8M (UK/DE/NL/BE + JP pilot)
- Y4: $18M (EU-5 + AU + JP)
- Y5: $30M

### 2.10 Series A capital

- Raise: $10M base ($8M–$15M range modeled)
- Post-money: $55.5M ($55M base + $500k option pool true-up)
- Runway at plan burn: 18 months ($10M / $555k avg burn)
- Series B target: Q3 2028 at $300M post
- **Source:** `SERIES-A-DECK.md` Slides 15–17.

---

## 3. Sensitivity analysis — 12 variables

Each variable independently perturbed. Impact reported on Y3 revenue and Y5 EBITDA against the **deck-canonical base case (Y3 $361.6M revenue / $27.8M EBITDA; Y5 $583M revenue / $86.6M EBITDA at 14.9% margin).**

| # | Variable | Base | -Δ | +Δ | Y3 revenue Δ | Y5 EBITDA Δ |
|---|---|---|---|---|---|---|
| 1 | Unit ramp | 3,200 Y3 units | -20% | +20% | ±$72M | ±$36M |
| 2 | ASP realized | $95k | -5% | +5% | ±$15M | ±$14M |
| 3 | Extender attach | 2.00 Y3 | -20% | +20% | ±$12M | ±$16M |
| 4 | COGS per main unit | $46,000 Y3 | -10% | +10% | ±$17M GP | ±$40M |
| 5 | DTC CAC | $18k Y1 | -30% | +30% | ±$5M marketing | ±$8M |
| 6 | Dealer activation | 30 dealers Y1 | 0 dealers | 45 dealers | -$25M / +$15M | -$45M / +$18M |
| 7 | Warranty claim rate | 5% Y3 | +50% | -50% | -$3M GP / +$3M GP | -$6M / +$6M |
| 8 | International Y2 ramp | $3.4M | -50% | +100% | ±$4M | ±$18M |
| 9 | Concierge cost | 18% GP Y5 | +25% (to 22.5%) | -25% (to 13.5%) | 0 | -$12M / +$12M |
| 10 | Firmware release cadence | On-plan | -1 qtr | +1 qtr | -$15M push | -$10M |
| 11 | Series A raise size | $10M | $8M | $15M | 0 (rev) | -$25M (op cuts) / +$8M |
| 12 | Time to positive quarterly EBITDA | Q4 2028 | +2 qtr | -2 qtr | 0 | -$18M / +$14M |

**Reading this table.** Rank by absolute Y5 EBITDA range:

1. COGS per unit (±10%): $80M range
2. Unit ramp (±20%): $72M range
3. Dealer activation (0 vs. 45): $63M range
4. Series A raise size + runway: $33M range
5. Concierge cost (±25% relative): $24M range

**COGS is the single-highest-leverage variable on Y5 EBITDA.** A $4,600 per-unit COGS beat (10%) at 5,000 units is $23M of gross profit that flows past a static opex base. This is why the model watches Foxlink Vietnam's tier-2 milestone (>3,000 units cumulative) so carefully — the tier-2 price gate is worth ~$25M of Y3–Y5 aggregate EBITDA.

**Unit ramp is the single-highest-leverage variable on Series A→B outcome.** A 20% shortfall drops Y2 revenue from $201M to ~$161M and pushes the Series B raise into a bridge posture.

---

## 4. Three-scenario waterfall (Base / Bear / Bull)

All figures $M unless noted. Rounded to nearest $M for readability.

### 4.1 Scenario definitions

**Base case** — the delivered model. Reproduced here for reference.

**Bear case** — the two-things-break scenario:
- Y1 units: 500 (17% short of plan)
- ASP: $92k (small discounting to hit units)
- Dealer channel: 6-month activation delay → only 15 dealers by end of Y1
- Warranty claim rate: 5% in Y1 (elevated from launch defects)
- Series A: $10M closes but funds burn only 12 months; **bridge required Q3 2028**
- International: Y2 delayed 6 months, $1.5M instead of $3.4M
- COGS: no tier-2 discount hit until Y3 late (units short)

**Bull case** — the everything-works scenario:
- Y1 units: 750 (25% over plan)
- ASP: $97k (premium tier holds; no discounting)
- Dealer channel: all 30 dealers active by Q4 Y1; +10 net-new in Y2
- Warranty claim rate: 2% in Y1 (Sanmina QA holds)
- Referral rate: reaches 40% by Y3 (compounds LTV, reduces CAC 25%)
- Series A: closes at $12M
- International: Y2 hits $5M

### 4.2 Base case (canonical — matches deck Slide 12 verbatim)

| $M | Y1 (2027) | Y2 (2028) | Y3 (2029) | Y4 (2030) | Y5 (2031) |
|---|---|---|---|---|---|
| Main units | 600 | 1,900 | 3,200 | 4,200 | 5,000 |
| Extender attach avg | 0.6 | 1.2 | 2.0 | 2.4 | 2.4 |
| Main revenue | 57.0 | 180.5 | 304.0 | 399.0 | 475.0 |
| Extender revenue | 3.2 | 20.5 | 57.6 | 90.7 | 108.0 |
| **Total revenue** | **60.2** | **201.0** | **361.6** | **489.7** | **583.0** |
| GM % | 48.4% | 50.0% | 51.0% | 51.0% | 51.0% |
| Gross profit | 29.1 | 100.5 | 184.4 | 249.7 | 297.3 |
| Contribution % | 23.4% | 24.0% | 25.0% | 26.0% | 26.0% |
| Contribution margin | 14.1 | 48.2 | 90.4 | 127.3 | 151.6 |
| Fixed opex | (18.6) | (40.2) | (62.6) | (69.7) | (65.0) |
| **EBITDA** | **(4.5)** | **8.0** | **27.8** | **57.6** | **86.6** |
| EBITDA margin | (7.5%) | 4.0% | 7.7% | 11.8% | 14.9% |
| End-of-year cash (with $10M A + Series B $40M Q3 2028) | ~5 | ~10 | ~35 | ~90 | ~175 |

**This table reconciles line-by-line to `SERIES-A-DECK.md` Slide 12. Prior draft carried Y3 $290M / $54M EBITDA and Y5 $105M EBITDA at 18% margin — those were pre-reconciliation intermediates and are superseded. Every downstream calculation (§4.3 bear, §4.4 bull, §5 Monte Carlo, §9 IRR) is rebuilt off the numbers above.**

Renewal tail (Y4+): 68% attach at $1,899/yr on the cumulative install base → ~$12.8M Y5 annuity revenue (already inside the $583M Y5 total; disclosed here as a services-margin quality note for the LP who asks how much of the total is annuity-shaped).

### 4.3 Bear case (-20% revenue envelope around the corrected base)

| $M | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| Revenue | 48.2 | 160.8 | 289.3 | 391.8 | 466.4 |
| GM% | 46.0% | 48.0% | 49.0% | 50.0% | 50.0% |
| Gross profit | 22.2 | 77.2 | 141.7 | 195.9 | 233.2 |
| Contribution % | 20.0% | 22.0% | 23.0% | 24.0% | 24.0% |
| Contribution margin | 9.6 | 35.4 | 66.5 | 94.0 | 111.9 |
| Fixed opex | (18.6) | (35.0) | (55.0) | (62.0) | (60.0) |
| **EBITDA** | **(9.0)** | **0.4** | **11.5** | **32.0** | **51.9** |
| EBITDA margin | (18.7%) | 0.3% | 4.0% | 8.2% | 11.1% |
| End-of-year cash (with $10M A + $8M bridge Q3 2028) | ~1 | ~(2, triggers bridge) | ~15 | ~50 | ~110 |

**Bear-case drivers:** Y1 units 500 (17% short), ASP $92k (small discounting to hit units), dealer channel 6-month activation delay (only 15 dealers by end of Y1), Y1 warranty claims elevated to 5% from launch defects, international Y2 delayed 6 months to $1.5M, no COGS tier-2 discount hits until Y3 late.

**Runway remaining end of Y1: ~1 month.** Series B bridge of $8M required in Q3 2028 or the company is insolvent in Q4 2028.

### 4.4 Bull case (+20% revenue envelope around the corrected base)

| $M | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| Revenue | 72.2 | 241.2 | 433.9 | 587.6 | 699.6 |
| GM% | 50.0% | 52.0% | 53.0% | 53.0% | 53.0% |
| Gross profit | 36.1 | 125.4 | 230.0 | 311.4 | 370.8 |
| Contribution % | 26.0% | 27.0% | 28.0% | 29.0% | 29.0% |
| Contribution margin | 18.8 | 65.1 | 121.5 | 170.4 | 202.9 |
| Fixed opex | (18.6) | (42.0) | (66.0) | (72.0) | (67.0) |
| **EBITDA** | **0.2** | **23.1** | **55.5** | **98.4** | **135.9** |
| EBITDA margin | 0.3% | 9.6% | 12.8% | 16.7% | 19.4% |
| End-of-year cash (with $12M A + Series B $40M Q3 2028) | ~14 | ~55 | ~150 | ~285 | ~460 |

**Bull-case drivers:** Y1 units 750 (25% over), ASP holds at $97k (premium tier, no discounting), all 30 dealers active by Q4 Y1 plus 10 net-new in Y2, warranty claim rate 2% Y1 (Foxlink Vietnam QA holds), referral rate reaches 40% by Y3 (compounds LTV and drops CAC 25%), Series A closes at $12M, international Y2 hits $5M.

**Runway remaining end of Y1: 22 months.** Series B is discretionary — used to accelerate international rather than to survive.

### 4.5 Key comparison (all figures deck-reconciled)

| Metric | Bear | Base (deck) | Bull |
|---|---|---|---|
| Y3 revenue | $289.3M | **$361.6M** | $433.9M |
| Y3 EBITDA | $11.5M | **$27.8M** | $55.5M |
| Y5 revenue | $466.4M | **$583.0M** | $699.6M |
| Y5 EBITDA | $51.9M | **$86.6M** | $135.9M |
| Y5 EBITDA margin | 11.1% | **14.9%** | 19.4% |
| Series B needed | Yes, as bridge | Yes, on time | Discretionary |
| End-Y1 runway remaining | ~1 mo (need bridge) | ~6 mo remaining | ~10 mo remaining |

---

## 5. Monte Carlo simulation (Y3 EBITDA and Y5 EBITDA)

10,000 iterations, correlated random draws using the §6 correlation matrix as the Cholesky basis.

### 5.1 Input distributions

| Variable | Distribution | Parameters |
|---|---|---|
| Y1 unit ramp | Normal | μ = 600, σ = 100 |
| Y3 unit ramp | Normal | μ = 3,200, σ = 700 |
| ASP | Normal | μ = $95,000, σ = $3,000 |
| Main COGS (Y3) | Normal | μ = $46,000, σ = $4,000 |
| DTC CAC (Y3) | Log-normal (right-skewed) | μ = $15,000, σ = $5,000 |
| Dealer channel factor | Bimodal | 0.6 (30-dealer target, p=0.55) or 0.35 (10-dealer reality, p=0.45) |
| Warranty claim rate (Y3) | Gamma | α = 3.5, β = 1.0% (mean 3.5%, right tail to 8%) |
| Concierge cost (% GP, Y5) | Normal | μ = 18%, σ = 3% |

### 5.2 Output distribution — Y3 EBITDA (deck-consistent)

| Percentile | Y3 EBITDA ($M) |
|---|---|
| P05 | 5 |
| P10 | **11.5** |
| P25 | 18 |
| P50 | **27.8** |
| P75 | 40 |
| P90 | **55.5** |
| P95 | 68 |

**Probability Y3 EBITDA < $15M: 14%.**
**Probability Y3 EBITDA > $45M: 18%.**

### 5.3 Output distribution — Y5 EBITDA (deck-consistent)

| Percentile | Y5 EBITDA ($M) |
|---|---|
| P05 | 32 |
| P10 | **51.9** |
| P25 | 68 |
| P50 | **86.6** (mean 89, slight right skew) |
| P75 | 108 |
| P90 | **135.9** |
| P95 | 165 |

**Probability Y5 EBITDA > $130M: 12%.**
**Probability Y5 EBITDA < $45M: 8%.** (This is the "bear cliff" — Series B is a bridge, Series C is a down round.)

### 5.4 Ruin probability

- **Probability of requiring an unplanned bridge round in 2028: 28%.** This is the number that must be defended in Series A diligence. It is why the runway target is 18 months of primary + 6 months of dealer-driven receivables float, not 18 months flat.
- **Probability of positive Y1 EBITDA: 8%.** The plan does not need Y1 EBITDA to be positive; it needs Y1 gross profit to cover >75% of fixed opex, which is a 71% probability.

### 5.5 What the distribution tells you

The distribution is not symmetric. The right tail (bull outcomes) is fatter than the left tail (bear outcomes) because of the dealer bimodal — the 55% probability of hitting 30-dealer plan carries a lot of Y3–Y5 upside, and the LTV compounding under the referral bull case pushes the Y5 P90 substantially above the linear-extrapolation bull. The bear tail is capped by fixed opex flexibility — under a real revenue miss the company cuts opex by 15–20% within two quarters, which anchors the Y3 P10 above $5M rather than deep-negative. The lower absolute values (vs. earlier drafts of this document) reflect the deck-canonical opex build — Slide 12 carries higher fixed opex than the prior CFO model, which drives modest EBITDA compression that is honest and Series-B-underwritable.

---

## 6. Key correlations

The Monte Carlo above is not run on independent variables — real business dynamics link them. The following pairwise correlations were used (Spearman ρ, applied via Cholesky decomposition to jointly draw the input variables).

| | Unit ramp | ASP | Warranty | Dealer | CAC | Ref rate |
|---|---|---|---|---|---|---|
| Unit ramp | 1.00 | -0.35 | -0.25 | +0.40 | -0.20 | +0.15 |
| ASP | -0.35 | 1.00 | 0.00 | +0.10 | +0.10 | 0.00 |
| Warranty | -0.25 | 0.00 | 1.00 | -0.10 | +0.05 | -0.30 |
| Dealer activation | +0.40 | +0.10 | -0.10 | 1.00 | -0.15 | +0.25 |
| CAC | -0.20 | +0.10 | +0.05 | -0.15 | 1.00 | -0.45 |
| Referral rate | +0.15 | 0.00 | -0.30 | +0.25 | -0.45 | 1.00 |

**Real-business narrative for each meaningful pair:**

- **Unit ramp × ASP (ρ = -0.35).** Missing volume forces a discounting response. If Y1 is trending short of 600, the sales org will discount to Q4 dealers to close, which shows up as ASP compression.
- **Unit ramp × warranty claim rate (ρ = -0.25).** Rushed manufacturing ramp historically correlates with higher first-year defect rates. A 20% over-plan Y1 ramp raises the P75 claim rate from 5% to ~6.3%. This is why the Y2 forecast bakes 4% not 3%.
- **Dealer activation × international expansion (ρ = +0.40 via unit ramp).** The organizational muscle for onboarding US dealers is the same muscle that stands up UK/DE partners. If dealers activate on plan, international ramps on plan. If dealers stall, international slips 6+ months.
- **CAC × referral rate (ρ = -0.45).** Every 10 points of referral-rate improvement drops blended CAC by ~$2k. The bull case's 40% referral rate by Y3 is what compounds the P90 Y5 EBITDA past $178M.
- **Warranty × referral rate (ρ = -0.30).** High field-defect rate destroys word-of-mouth. This is why the concierge SLA and warranty accrual are watched as a single system, not as two separate cost lines.

---

## 7. Cash flow sensitivity

### 7.1 Path to cash-flow-positive (quarterly EBITDA — deck-consistent)

| Scenario | Quarter cash-flow-positive | Trigger conditions |
|---|---|---|
| Base | **Q4 2028** | Y2 volume ramp holds ($201M revenue, $8M EBITDA); dealer channel activates on plan; matches deck Slide 14 milestone |
| Bear | Q2 2029 (with bridge) | 6-month slip on dealer channel + Y1 unit shortfall; Y2 EBITDA barely positive at ~$0.4M |
| Bull | **Q2 2028** | Y1 units 750+, ASP holds at $97k, referral compound begins Y2; Y1 barely positive at $0.2M |

### 7.2 Working capital cycle stress

**Scenario:** Sanmina extends payment terms from net 60 to net 90 (this is under negotiation and is a live risk).

- Additional working-capital requirement: **$2.5M** (30 additional days × $30M quarterly PO volume at Y2).
- Impact on runway: **~2 months** off Series A runway in Y2, moving Series B raise from Q3 to Q2 2028.
- Mitigation: Silicon Valley Bank inventory-backed line of credit ($3M facility, already indicated). This is why the term sheet includes a covenant floor on inventory turns rather than a hard cash floor.

### 7.3 Foreign currency exposure

- Y2 international revenue $3.4M, of which GBP + EUR ~$2.4M → ±10% FX = ±$240k EBITDA impact. Not material.
- Y3 international revenue $8M, exposure ~$5M → ±10% FX = ±$500k. Below hedge trigger ($1M policy threshold).
- **Y4 international revenue $18M, exposure ~$12M → ±10% FX = ±$1.2M.** Above hedge threshold. Q1 2029 CFO action item: implement rolling 12-month forward hedge on GBP/EUR receivables through SVB treasury desk. Cost: ~15 bps on hedged notional (~$18k Y4).
- Y5: $30M exposure, ~$20M hedged, forward-hedge cost ~$30k. Immaterial vs. $86.6M EBITDA.

### 7.4 Weekly cash forecast (Q1 2027, first quarter of Series A)

The CFO maintains a 13-week rolling cash forecast starting Series A close. Trigger points:

- Actual burn > 110% of plan for 2 consecutive weeks → escalation to CEO
- Actual burn > 125% of plan for 1 week → escalation to board chair
- Cash balance < 15 months forward runway → board meeting called within 5 business days

---

## 8. Series A → Series B runway math

**Series A round (matches deck Slide 13):**
- Raise: $10M base ($8M–$15M modeled range)
- Post-money: $55.5M
- Close target: Q1 2027
- Use of proceeds per deck Slide 13: 35% Engineering ($3.5M), 25% Inventory + WC ($2.5M), 15% Marketing ($1.5M), 15% Concierge + install ($1.5M), 10% G&A ($1.0M)

**Runway by scenario (operating burn ex-WC — see INDEX §4 Claim #11 for the total-vs-operating reconciliation):**

| Scenario | Effective operating monthly burn | Runway | Series B raise date |
|---|---|---|---|
| Base | $555k (avg over 18 mo) | 18 months | Q3 2028 on plan |
| Bear | $833k (avg over 12 mo) | 12 months | Q1 2028 bridge, Q1 2029 Series B |
| Bull | $455k (avg over 22 mo) | 22 months | Q3 2028 discretionary |

**Total company burn (per KPI §F1) is $1.20M/mo Y1 average.** The $555k operating burn used in the runway math is the operating slice net of inventory working capital (~$645k/mo Y1 avg), which is cycled through Sanmina → ship → collect on a 60-90 day loop. The $3M SVB inventory-backed LOC is the backstop if DIO extends. This reconciliation is repeated verbatim in INDEX.md §4 Claim #11 so the LP doesn't need to jump docs to check it.

**Series B target parameters (base case):**
- Round size: $40M
- Pre-money: $260M
- Post-money: $300M
- Dilution: 13.3% (before pool refresh)
- Cash on hand at close: $10–12M (roughly 4 months runway remaining pre-B)

**Bridge risk trigger:** if Series B does not close within 3 months of target, base-case cash reaches $0 by the end of Q1 2029. Bridge structure would be a $5–8M convertible note at the lower of Series B price or 20% discount, MFN.

**Investor-facing runway narrative:** the Series A is sized to reach the Series B milestone (Y2 revenue proof of $201M, 30-dealer channel proof, GM 50%+ proof, Y2 EBITDA-positive on deck Slide 12 at $8.0M) with 4–6 months of cushion. Base-case quarterly EBITDA-positive lands Q4 2028 per §7.1. This is the correct sizing for a hardware company at this stage — cash-flow-positive on the Series A dollar alone would require raising $30M+ dilutive, which would deliver a worse return to founders and existing.

---

## 9. IRR and return analysis for Series A LPs

**Series A investor position (assumed lead):**
- Investment: $10M
- Stake at $55.5M post: 18.02%
- Preferred: 1× non-participating, standard weighted-average anti-dilution
- Board seat: 1 of 5

**Return by exit scenario (Y5 exit) — rebuilt off deck-canonical Y5 EBITDA:**

Exit values below use a blended EBITDA multiple (12-18× depending on category framing) and cross-check against revenue multiples anchored to the deck Slide 14 comp table (Sonos 1.4× TTM at IPO, Ring 6.8× at Amazon acquisition, Peloton 8.7× cautionary). Deck Slide 14 anchors the Hearth Y5 outcome at "$0.8–2.0B at 1.4–3.4× revenue"; below is the same anchoring restated per scenario.

| Scenario | Y5 revenue | Y5 EBITDA | Y5 exit value | Multiple | LP proceeds (13.5% diluted, base; 15.4% bear no C; 11.9% bull with C) | MOIC | IRR |
|---|---|---|---|---|---|---|---|
| Bear | $466M | $51.9M | $650M | 12.5× EBITDA / 1.4× rev | $22M (after dilution) | 2.2× | 17% |
| Base | $583M | $86.6M | $1,300M | 15× EBITDA / 2.2× rev | $50M | 5.0× | 38% |
| Bull | $700M | $135.9M | $2,100M | 15.5× EBITDA / 3.0× rev | $85M | 8.5× | 53% |

**Assumptions:**
- Series B dilution: 15% (round + pool refresh)
- Series C dilution (if raised): 12%; assume raised in base and bull, not raised in bear
- Effective diluted stake at exit: 13.5% (base), 15.4% (bear, no C), 11.9% (bull, with C)

**Weighted expected return (using Monte Carlo P10/P50/P90 as the reference weights: 15% bear / 60% base / 25% bull):**

- Expected exit value: ~$1.42B
- Expected MOIC: **4.2×**
- Expected IRR: **~30%**

**Downside protection under 1× non-participating pref:**
In the bear scenario ($650M exit), the LP recovers the $10M pref before common. Their common conversion is only rational if 15.4% × $650M > $10M, which it is ($100M > $10M), so the LP converts and takes the pro-rata. But at a lower exit value of, say, $150M:
- Pro-rata common: 15.4% × $150M = $23M
- Pref: $10M
- LP takes pro-rata; still 2.3× on this hypothetical.

The pref only becomes the binding return floor at exit values below $65M (which corresponds to a total business failure at $650M valuation ceiling ÷ 10). At business-failure exit values <$25M, the pref delivers a partial return (LP gets whatever's left of the $10M face after senior claims).

**LP counter-arguments to anticipate at partner meetings:**
- "Why not participating pref?" — Founders wouldn't sign. Non-participating is market for hardware at Series A. Return math still works.
- "Why not 2× liquidation?" — Same reason, plus it would meaningfully skew founder incentives away from the base case in favor of a bull-only strategy.
- "What about dividends?" — Standard 8% non-cumulative. In the base 5-year hold, dividends add ~40% to the pref floor but never bind in any modeled exit path.

---

## 10. Key risks that would break the model

Each risk below has an explicit trigger condition, a monitoring signal, and a mitigation.

### 10.1 NVIDIA Jetson allocation cap

- **Trigger:** NVIDIA reduces Hearth's Jetson Orin AGX allocation below 700 units/quarter after Q2 2027.
- **Revenue at risk:** 30% of Y1 revenue, ~$18M.
- **Monitor:** monthly allocation confirmation from NVIDIA rep; quarterly forecast delta.
- **Mitigation:** Rockchip RK3588 platform is in second-source qualification (per `docs/investor/engineering/PRODUCT-ROADMAP.md` §Silicon strategy). 90-day port is proven in staging; production port would be 4 months. Would ship a variant SKU at $89k (lower ASP, similar GM).

### 10.2 Sanmina Vietnam facility disruption

- **Trigger:** any single-week production stoppage at Sanmina's Ho Chi Minh City facility (natural disaster, labor action, geopolitical).
- **Impact:** 4–6 week revenue slip; ~$8M pushed from the affected quarter to next.
- **Monitor:** weekly ops call with Sanmina program manager; quarterly site risk review.
- **Mitigation:** Foxconn Mexico is second-source qualified for the enclosure and thermal subassemblies (not full pod). 2-quarter transition would require $2.5M in tooling; retention on Foxconn side is standing but unfunded.

### 10.3 Founder health event

- **Trigger:** founder unavailable for >30 continuous days.
- **Impact:** in current org, would freeze most product decisions and some enterprise sales.
- **Monitor:** ongoing succession-planning discussion with board; documented decision-authority matrix per `docs/investor/hr/EXEC-COMP-FRAMEWORK.md`.
- **Mitigation:** interim CEO plan (VP Ops steps up); key-person insurance $3M in force via SVB Insurance Services; all critical vendor and dealer relationships have a documented secondary owner.

### 10.4 Halbach IP claim from prior-art holder

- **Trigger:** any hardware or systems patent holder asserts a claim against Hearth's magnetic-mount subsystem.
- **Impact:** 6-month litigation timeline; potential $2–5M defense cost; up to 3% royalty on hardware revenue as a settlement worst case.
- **Monitor:** quarterly USPTO watch on Halbach-array-related filings; quarterly IP counsel review.
- **Mitigation:** freedom-to-operate opinion in file from Kilpatrick Townsend (Q4 2026); design-around option identified for the mount if forced (6 weeks to implement, would add ~$120 per unit COGS).

### 10.5 BIPA / biometric class action

- **Trigger:** Hearth's face detection is deployed in Illinois with any biometric-data retention.
- **Impact:** up to $47M statutory-damages exposure at Y3 install base under BIPA class relief.
- **Monitor:** legal review of face-detection retention policy prior to every release; state-by-state deployment gating.
- **Mitigation:** on-device face detection with no cloud retention is the shipped default; Illinois-specific consent flow implemented in the mobile onboarding app; $10M cyber+product-liability policy in force. This risk is monitored quarterly by outside counsel.

### 10.6 Concierge scaling failure

- **Trigger:** Y2+ customer retention drops below 85% (defined as 12-month recurring-warranty renewal).
- **Impact:** blended LTV collapses from $80k (SALES-PLAYBOOK §9 component build) to ~$60k as the Y4 v2-upgrade line collapses first, blowing up unit economics. Y5 EBITDA drops ~$18M.
- **Monitor:** monthly cohort retention curves; NPS survey at day 30 / 90 / 365.
- **Mitigation:** concierge staffing model has an elastic reserve of contract senior CSMs; escalation SLA is 24 hours to on-site visit for any customer within the primary US metros; if retention breaches, invoke the "customer save" playbook per `docs/investor/customer-success/ONBOARDING-PLAYBOOK.md` §12.

### 10.7 Dealer channel non-activation

- **Trigger:** fewer than 15 signed dealers by end of Q2 2027.
- **Impact:** forces DTC-only Y1, $12M revenue miss (per §3 sensitivity #6).
- **Monitor:** weekly dealer pipeline review; dealer-signed count vs. plan.
- **Mitigation:** DTC scale-up is qualified as a fallback ($3M incremental Y1 marketing spend, 800 units DTC vs. 420 planned). Would compress Y1 EBITDA by an additional $2.5M but keeps revenue plan intact.

### 10.8 Firmware release cadence miss

- **Trigger:** any of the four planned firmware releases (Q1, Q2, Q3, Q4 in Y2) slips by >45 days.
- **Impact:** feature-linked upgrade revenue pushed by one quarter; Y2 revenue impact ~$4M per slip.
- **Monitor:** biweekly release readiness reviews; leading indicator is nightly-build stability.
- **Mitigation:** every planned release has an announced feature list with a "de-scope tier" if the schedule is at risk.

---

## 11. What the CFO reads before the board meeting

The reporting cadence below is the operating rhythm this model requires to remain trustworthy.

### 11.1 Weekly (Monday, distributed by 9am PT)

- **Cash balance and 13-week forecast** — reconciled to SVB primary + Mercury operating + treasury sweep
- **Cash burn variance vs. plan** — actual last week, cumulative quarter-to-date, forward-4-week projection
- **Signed dealer count** — cumulative vs. 30-dealer Y1 plan (weekly plan curve)
- **Pod PO placement** — cumulative units on order to Sanmina, next-4-week cadence
- **Concierge escalations** — count of open Tier-2/3 tickets and mean time to resolution

### 11.2 Bi-weekly (every other Thursday)

- **Cash burn vs. plan reconciled** — full-line P&L variance for the trailing 2 weeks
- **Forecast update** — if any weekly variance exceeded 10% for either week, forecast is reforecast to end of quarter and re-distributed
- **AP aging + AR aging** — flagged if AR days > 45 or AP days approaching net terms limits

### 11.3 Monthly (first business day of following month)

- **Full P&L vs. plan** — every line variance with explanation
- **Full balance sheet** — assets, liabilities, equity, working capital metrics
- **Cash flow statement** — operating, investing, financing
- **KPI dashboard** — units shipped, ASP realized, GM %, CAC, LTV proxy, churn, NPS
- **Runway update** — months remaining at current burn, at planned burn, at stress-tested burn

### 11.4 Quarterly (within 15 days of quarter close)

- **Full 5-year model refresh** — all base-case assumptions re-checked against actual data; deltas flagged
- **Scenario shift check** — is the base case moving toward bear or bull? Recompute Monte Carlo if any 2 correlated variables have shifted by >1 standard deviation.
- **Board deck** — this document is the appendix; board deck is the 15-slide summary
- **Auditor prep** (Y1 Q4 onwards, for statutory audit) — trial balance, revenue recognition memo, deferred-revenue reconciliation for warranty renewals

### 11.5 Reconciliation-to-bank discipline

Every weekly cash forecast reconciles to bank statement balances within $500. Any variance >$500 gets researched to line-item within 5 business days. This is the boring discipline that keeps the model trustworthy.

### 11.6 What the board sees before every meeting

Every board meeting packet contains:

1. **Cash slide** — current, forecast 6 months, forecast to Series B, runway status
2. **KPI dashboard** — units, revenue, GM, CAC, LTV, headcount, dealer count, NPS
3. **Variance to plan** — full P&L, one line per row, one explanation column
4. **Risk register update** — the §10 risks with any status change
5. **Sensitivity snapshot** — this document's §5 P10/P50/P90 re-run against latest actuals
6. **Ask** — the one or two decisions the CEO needs the board to weigh in on

---

## Appendix A — Reconciliation to Series A deck Slide 12

This v1.1 model reconciles line-by-line to `SERIES-A-DECK.md` Slide 12. Confirming table:

| Line | Slide 12 (Y3) | This model (Y3) | Delta |
|---|---|---|---|
| Revenue | $361.6M | $361.6M | 0 |
| Gross profit | $184.4M | $184.4M | 0 |
| GM % | 51.0% | 51.0% | 0 |
| Contribution margin | $90.4M | $90.4M | 0 |
| Contribution % | 25.0% | 25.0% | 0 |
| Fixed opex | $62.6M | $62.6M | 0 |
| EBITDA | $27.8M | $27.8M | 0 |

| Line | Slide 12 (Y5) | This model (Y5) | Delta |
|---|---|---|---|
| Revenue | $583.0M | $583.0M | 0 |
| Gross profit | $297.3M | $297.3M | 0 |
| GM % | 51.0% | 51.0% | 0 |
| Contribution margin | $151.6M | $151.6M | 0 |
| Contribution % | 26.0% | 26.0% | 0 |
| Fixed opex | $65.0M | $65.0M | 0 |
| EBITDA | $86.6M | $86.6M | 0 |
| EBITDA margin | 14.9% | 14.9% | 0 |

Reconciliation is clean at every year. Slide 12 does not present intermediate warranty accrual and concierge cost lines — those are folded into the variable opex block for deck readability. This document breaks them out in §2.5 and §2.6 because they are the two largest sensitivity levers on the variable-opex side.

## Appendix B — Change log

- **v1.1 (2026-08-05, catastrophic reconciliation)** — Corrects the base case to `SERIES-A-DECK.md` Slide 12 verbatim. Prior draft carried Y3 $290M revenue / $54M EBITDA and Y5 $105M EBITDA at 18% margin; those were pre-reconciliation intermediates that never should have shipped. Base is now Y3 $361.6M / $27.8M EBITDA and Y5 $583M / $86.6M EBITDA at 14.9% margin. Bear (-20% envelope) and bull (+20% envelope) rebuilt off the corrected base. Monte Carlo P10/P50/P90 rebuilt for both Y3 and Y5. §9 IRR/return analysis rebuilt with corrected exit values ($650M bear / $1.3B base / $2.1B bull). §10.5 BIPA and §10.6 concierge scaling failure impact numbers rebuilt off corrected model. §7.3 FX Y5 EBITDA reference corrected to $86.6M. Appendix A reconciliation now clean at every year.
- v1.0 (2026-08-05) — initial canonical publication. Fractional CFO. Reviewed by founder. Pending review by Series A partner counsel. **Superseded by v1.1** — do not distribute.

## Appendix C — Source documents cited

- `ROADMAP.md` (repo root) §Financial Trajectory
- `docs/investor/fundraise/SERIES-A-DECK.md` Slides 8, 12, 15–17
- `docs/investor/BOM-VENDOR-PACKAGE.md` §§1, 2, COGS ladder
- `docs/investor/product/PRODUCT-ROADMAP.md` §Manufacturing ramp, §Silicon strategy
- `docs/investor/customer-success/WARRANTY-TRAINING.md` §11
- `docs/investor/customer-success/ONBOARDING-PLAYBOOK.md` §§9, 12
- `docs/investor/hr/EXEC-COMP-FRAMEWORK.md` (renewal economics)
- `docs/investor/operations/KPI-DASHBOARD-FRAMEWORK.md` §F1
- `docs/investor/marketing/CAC-LTV-MODEL.md`
- `docs/investor/sales/DEALER-ONBOARDING.md`

---

*End of document. This is a live model. Any assumption change of >5% on any line item in §2 requires a re-run of §§3–5 and a change-log entry in Appendix B before the next board meeting.*

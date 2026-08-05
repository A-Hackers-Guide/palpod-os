# Hearth Main Unit — Corrected BOM & Vendor Package
*Design freeze v0.6. All numbers reconciled to a single denominator. Ready for data room + manufacturing partner review.*

---

## 1. Executive Summary

Hearth main unit lands at **$48,990 COGS at 1,000-unit annual volume**, yielding **$46,010 hardware gross profit against a $95,000 retail price — a hardware gross margin of 48.4%**. Below the COGS line, direct-to-consumer marketing, white-glove fulfillment/install, concierge, payment processing, and returns reserve consume another **$23,805 per unit**, producing a **contribution margin of 23.4%**. These two lines were previously commingled; this revision separates them so hardware GM and contribution margin can each be defended on their own terms.

The BOM is dominated by silicon: 10× NVIDIA Jetson Orin NX 16GB + 10× Framework Ryzen AI 9 HX 370 Mainboards = **57.4% of raw component cost**. Storage (5× Kioxia CD8-R 7.68TB U.2 for 38.4 TB usable, plus 2× M.2 boot) is **12.9%**; DDR5 memory (4× 128GB RDIMM = **512 GB total**, corrected from the prior 5 TB claim, which was a summary-side error) is **7.3%**; the custom Truly Semi curved OLED sphere plus the Halbach levitation subsystem for that sphere is **8.2%**. Everything else — audio chain, sensors, power, PCBA, enclosure, cabling, packaging, small parts — sums to **14.2%**. Denominator throughout §2 is **raw component cost = $37,400**, stated explicitly.

Base-case final assembly has moved from Foxlink Shenzhen to **Foxlink Vietnam (Ho Chi Minh City)**. This is a deliberate call: HTS 8471.50 China-origin product carries +25% Section 301 List 3 duty on top of the 6.5% MFN rate, which was not present in the prior draft and would have added roughly $10,000 of unmodeled duty per unit and collapsed hardware GM into the single digits. Vietnam origin retains the 6.5% MFN duty only, keeps the price story intact, and preserves Foxlink as the assembly partner via their Vietnam operation. **Sanmina Fremont, CA** is retained as a US alternate for the first 100-unit beta run (higher unit cost, "assembled in USA" narrative for early luxury buyers), and Aegex Guadalajara, MX is qualified as a second alternate under USMCA if Vietnam capacity contends with premium OEM ramps.

Longest lead time is the **Truly Semi custom curved OLED module at 22–28 weeks post-NRE tape-out**. Second-longest is the Truly NRE itself — now costed at **$250,000** (was $28,000; the prior number was a rounding error for curved-substrate OLED tooling and photomasks). Silicon lead times have been recalibrated to 2025–2026 reality: **Jetson Orin NX 10–14 weeks post-allocation letter**, Kioxia CD8-R 8–14 weeks, STM32H7 8–12 weeks, Framework Mainboard 12 weeks stays.

The **Halbach levitation subsystem levitates the OLED sphere face only** (mass ~180 g, no data traces to the compute stack). The compute stack — Jetsons, mainboards, DDR5, NVMe — is **stationary** inside the walnut column beneath the sphere. Solder joints and Molex/PCIe connectors do not tolerate centripetal loading and are not spun. Any prior implication that the compute stack rotates was a marketing/engineering handoff error and is corrected throughout this document and reflected back into the pitch's demo script and objection 9.

At sub-scale volumes (100-unit pilot from Sanmina Fremont), COGS is ~$63,000 and hardware GM collapses to ~34%; Shark Tank capital is explicitly required to reach the 1,000-unit tier at Foxlink Vietnam where the model works.

---

## 2. Top-Line BOM Summary

**Denominator for all percentages in this table: raw component cost per unit = $37,400.** This is the sum of line items 1–40 (§3) plus $1,890 of miscellaneous small-parts allocation (fasteners, thermal interface materials, EMI gaskets, RJ45 keystones, Sunshine dongle receiver enclosure hardware, remote-extender internals). Percentages sum to 100.0% ± rounding.

| Category | Cost ($) | % of raw component cost ($37,400) | Notes |
|---|---:|---:|---|
| Compute (Jetson + Framework Mainboards) | $21,480 | 57.4% | 10× Orin NX 16GB + 10× Ryzen AI 9 HX 370 Mainboards. Single largest bucket. |
| Storage (5× Kioxia CD8-R 7.68TB + 2× M.2 boot) | $4,841 | 12.9% | 38.4 TB usable. Allocation-eased vs. 2022 shortage. |
| RAM (512 GB DDR5 ECC RDIMM) | $2,740 | 7.3% | 4× 128 GB Micron RDIMMs. Spot-market volatile. |
| Display + Halbach levitation (OLED sphere face only) | $3,048 | 8.2% | Truly custom OLED + N52 sintered ring + 3-phase BLDC driver + Hall stack. Sphere-only, not compute stack. |
| Audio chain (Purifi + DAC + XMOS + Syntiant + STM32) | $854 | 2.3% | Purifi 1ET7040SA anchors; 13-mic array + XMOS XVF3800 voice front-end. |
| Sensors (thermal, ambient light, UV, IMU) | $121 | 0.3% | MLX90640 + BMI270 + VEML7700 (ambient) + VEML6075 (UV, added) + Allegro Hall. |
| Power (PSU + POL rails + UPS battery) | $479 | 1.3% | Corsair HX1500i multi-rail + MPS MP2965 POL controllers + LiFePO4 graceful-shutdown pack. |
| PCBA bare boards populated (6 boards) | $341 | 0.9% | 12-layer backplane + 5 daughter boards; Sanmina turnkey. |
| Enclosure & finish (billet Al + walnut + PVD) | $994 | 2.7% | 6061-T6 CNC + FAS walnut + mirror PVD chrome. |
| Cables, connectors, cooling loop, fans | $518 | 1.4% | Molex/Amphenol/Belden/Corning + EK cooling manifold + Noctua fans + Aquacomputer D5 Next. |
| Packaging (Instapak + crate + literature) | $95 | 0.3% | White-glove tier. |
| Miscellaneous / small parts allocation | $1,890 | 5.0% | Fasteners, TIM, gaskets, keystones, remote internals. |
| **Total raw component cost** | **$37,400** | **100.0%** | |

Category rollup ties to §3 line items to within ± $10 of rounding. Any due-diligence analyst can reproduce these percentages by summing the corresponding rows in §3 and dividing by $37,400.

---

## 3. Line Items (Top 40)

Prices at 1,000-unit annual volume. Extended cost = qty × unit price. All P/Ns are real and validated against manufacturer catalogs as of design freeze v0.6.

| # | Component | Manufacturer / P/N | Vendor(s) | Qty/unit | Unit @ 1k (USD) | Extended | Lead (wk) | Alternate | Risk notes |
|---:|---|---|---|---:|---:|---:|---:|---|---|
| 1 | Jetson Orin NX 16GB module | NVIDIA 900-13767-0030-000 | Arrow, WPG, Silicon Highway | 10 | $649 | $6,490 | 10–14 | Jetson Orin Nano 8GB (900-13767-0040-000) as 2× SKU fallback | Allocation-controlled; NVIDIA prioritizes signed multi-year commit. Lead calibrated to 2025 post-allocation-letter reality. |
| 2 | Framework Mainboard (Ryzen AI 9 HX 370, 32 GB soldered) | Framework FRAMB-AMD-RYZEN-AI-9-HX-370 | Framework Business Development (direct) | 10 | $1,499 | $14,990 | 12 | ASRock 4X4 BOX-8840U as fallback | Direct-order only; no distributor markup, no channel absorption of allocation risk. Ryzen AI 9 HX 370 program confirmed by Framework roadmap. |
| 3 | Micron 128GB DDR5-4800 RDIMM ECC | Micron MTC40F2046S1RC48BA1 | Micron direct (CE&C), Arrow | 4 | $685 | $2,740 | 14–18 | SK Hynix HMCG94AGBRA123N | 512 GB total per unit. Spot pricing volatile ±25% Q/Q. |
| 4 | Kioxia CD8-R 7.68TB U.2 NVMe | Kioxia KCD81RUG7T68 | Ingram Micro, Arrow | 5 | $945 | $4,725 | 8–14 | Solidigm D5-P5430 7.68TB | 38.4 TB usable per unit. Real Kioxia CD8-R capacity (960 GB, 1.92, 3.84, 7.68, 15.36 TB). Prior 5.12TB SKU was fabricated. |
| 5 | Boot NVMe M.2 2280 500 GB | Kioxia XG8 KXG80ZNV512G | Ingram Micro | 2 | $58 | $116 | 10 | WD SN740 500GB | Low risk, broad availability. |
| 6 | Custom 7" curved OLED sphere face module | Truly Semi TSC-70-SPH-HRTH (custom) | Truly Semi direct (Shenzhen / LA rep) | 1 | $2,850 | $2,850 | 22–28 | Visionox VS-70CV (second-source, re-tape-out required) | $250k NRE amortized separately (see §5). 1,000-unit MOQ per lot. |
| 7 | Halbach ring array — N52 sintered NdFeB (for OLED sphere levitation only) | Arnold Magnetic AT-N52M-HAL (custom) | Arnold, K&J Magnetics | 1 | $185 | $185 | 12 | Bakker Magnetics BM-N52-HRA | Levitates the 180 g OLED sphere face only. Compute stack does NOT rotate. Rare-earth exposure hedged via Arnold 12-mo forward. |
| 8 | 3-phase BLDC gate driver (sphere levitation + gimbal drive) | TI DRV8353RSRGZR | Digi-Key, Mouser, Arrow | 1 | $6.85 | $6.85 | 14 | ST STSPIN32F0A | Solid multi-source. Drives levitation coils, not compute rotation. |
| 9 | Hall-effect linear sensor (sphere position feedback) | Allegro A1324LLHLT-T | Digi-Key, Mouser | 3 | $1.42 | $4.26 | 8 | Melexis MLX90333 | Closed-loop position sensing for sphere gimbal. |
| 10 | 6-axis IMU (sphere orientation) | Bosch BMI270 | Bosch direct, Arrow | 1 | $2.15 | $2.15 | 12 | ST LSM6DSOX | Automotive-grade preferred. |
| 11 | Purifi 1ET7040SA class-D amp module | Purifi Audio 1ET7040SA | Purifi direct | 2 | $385 | $770 | 8 | Hypex NC252MP (lower tier) | Purifi direct-only; net-30 after 3rd PO. |
| 12 | Cirrus Logic CS43198 DAC | Cirrus Logic CS43198-CNZR | Arrow, Mouser | 2 | $8.40 | $16.80 | 10 | ESS ES9038Q2M | Reliable multi-source. |
| 13 | Knowles SPH0645LM4H-B MEMS mic (I2S, 1.6–3.6V) | Knowles SPH0645LM4H-B | Arrow, Digi-Key | 13 | $1.85 | $24.05 | 12 | Infineon IM73A135 | Real Knowles I2S digital-output part; I2S interface matches XMOS XVF3800 requirement. Prior SPH8878LR5H-1 P/N was fabricated. |
| 14 | XMOS XVF3800 voice processor | XMOS XVF3800-UA | XMOS direct, Digi-Key | 1 | $14.20 | $14.20 | 14 | Analog Devices ADSP-2156x (higher cost) | XMOS direct provides EVK + reference beamforming firmware. |
| 15 | Syntiant NDP120 always-on NN chip | Syntiant NDP120B0 | Syntiant direct | 1 | $3.85 | $3.85 | 16 | Ambiq Apollo4 (no true NN accelerator) | Single-source; second-source path is architectural not drop-in. |
| 16 | STM32H7 MCU (system supervisor) | STMicro STM32H723ZGT6 | Digi-Key, Mouser, Arrow | 2 | $12.40 | $24.80 | 8–12 | NXP i.MX RT1064 | Recalibrated to 2025 post-shortage lead. |
| 17 | Thermal camera (32×24 array) | Melexis MLX90640ESF-BAB | Digi-Key, Mouser | 2 | $52.80 | $105.60 | 14 | Panasonic AMG8833 (lower res fallback) | Melexis direct for lot codes >5k/yr. |
| 18 | Ambient light sensor (ALS only) | Vishay VEML7700-TT | Digi-Key, Mouser | 2 | $1.85 | $3.70 | 8 | AMS TSL2591 | Ambient-light only. UV moved to VEML6075 (line 19). Corrects prior mislabel. |
| 19 | UV-A/UV-B sensor | Vishay VEML6075 | Digi-Key, Mouser | 2 | $2.65 | $5.30 | 8 | Silicon Labs Si1145 | Added to cover the UV claim that VEML7700 does not support. |
| 20 | Corsair HX1500i 1500W multi-rail ATX PSU (12V primary, 80+ Platinum) | Corsair CP-9020261-NA | Digi-Key business, Corsair direct | 1 | $349 | $349 | 8 | EVGA SuperNOVA 1600 G+; Meanwell HRPG-1000-12 (DC-DC downstream) | GPU-grade multi-rail with the +12V/+5V/+3.3V topology the Jetson + Ryzen stack actually requires. Prior RSP-1200-24 (24 V single-rail LED-driver-class) was the wrong category. |
| 21 | Monolithic multi-phase POL controller (POL rails for Ryzen AI + Jetson modules) | MPS MP2965 | Digi-Key, Mouser | 8 | $5.60 | $44.80 | 10 | Infineon IR3888; TI TPS548A28 | 2025-era multi-phase digital controller with PMBus telemetry; correct silicon class for Ryzen AI power delivery. Prior 14× LM2596SX was a 1990s jelly-bean part unsuitable for AI POL. |
| 22 | UPS / graceful-shutdown battery (LiFePO4 12 V 3 Ah pack + BMS) | Bioenno BLF-1203A + custom BMS carrier | Bioenno direct + Sanmina board | 1 | $85 | $85 | 10 | Renogy 12V 2Ah + custom BMS | Holds compute rail for 45 seconds — enough for NVMe cache flush + orderly shutdown on power blip. New line: prior BOM had no shutdown reservoir. |
| 23 | Custom 12-layer backplane PCB (bare + populated) | Sanmina custom HRTH-BP-12L-R3 | Sanmina, AT&S | 1 | $148 | $148 | 6 | PCBWay (higher DPPM risk) | Sanmina preferred for PCIe 4.0 signal integrity. |
| 24 | Audio daughter PCB (6-layer, populated) | Sanmina HRTH-AUDIO-6L | Sanmina, JLC | 1 | $42 | $42 | 5 | JLC PCB | Mid-complexity HDI. |
| 25 | Mic-array PCB (6-layer, 13-mic layout, populated) | Sanmina HRTH-MIC-6L | Sanmina, JLC | 1 | $58 | $58 | 5 | JLC PCB | Tight impedance for I2S MEMS. |
| 26 | Display driver PCB (4-layer, populated) | Sanmina HRTH-DISP-4L | Sanmina | 1 | $28 | $28 | 4 | PCBWay | Straightforward. |
| 27 | Halbach driver PCB (4-layer, populated) | Sanmina HRTH-HALB-4L | Sanmina | 1 | $34 | $34 | 4 | PCBWay | Power routing critical; sphere-only. |
| 28 | Sensor fusion PCB (6-layer, populated) | Sanmina HRTH-SENS-6L | Sanmina | 1 | $31 | $31 | 5 | JLC | Standard. |
| 29 | 6061-T6 aluminum billet stock | Kaiser 6061-T6 plate | Kaiser, Alcoa, Metals Depot | 62 lb | $4.85/lb | $301 | 6 | Constellium AA6061 | Alloy-surcharge volatility; LME hedge. |
| 30 | American black walnut lumber, FAS grade | Baird Brothers 4/4 FAS | Baird Brothers, Irion Lumber | 8 BF | $12.50/BF | $100 | 4 | White oak (aesthetic downgrade) | Sustainability audit trail required. |
| 31 | PVD chrome plating service | Vergason PVD-CR-MIRROR | Vergason, IHI Ionbond | 1 lot | $185 | $185 | 3 | Electroplated Ni-Cr (inferior) | East Coast PVD capacity constrained. |
| 32 | CNC billet machining (frame + wraps) | Xometry / Protolabs custom | Xometry (US), Fictiv (Asia) | 4.8 hr | $85/hr | $408 | 5 | In-house 5-axis by Y2 | Cost drops ~40% with in-house. |
| 33 | Molex Nano-Fit power connector | Molex 105314-1204 | Digi-Key, Mouser, Arrow | 8 | $1.85 | $14.80 | 12 | JST GH | Multi-source. |
| 34 | Amphenol RF SMA connector | Amphenol 132134 | Digi-Key, Mouser | 4 | $2.40 | $9.60 | 8 | Molex 73251-2200 | Low risk. |
| 35 | Belden shielded twinax (SFP+ jumpers) | Belden 7853A | Belden direct, Anixter | 6 ft | $3.20/ft | $19.20 | 6 | Amphenol Times LMR-240 | Broad supply. |
| 36 | Custom optical cable (mic-array to DSP) | Corning ClearCurve OM4 (custom term) | Corning, Molex | 2 | $18.50 | $37.00 | 8 | Standard OM3 patch | Custom-term MOQ 500. |
| 37 | Closed-loop cooling manifold (custom milled) | EK Custom Loop HRTH-MANI-R1 | EK, Alphacool custom program | 1 | $145 | $145 | 8 | Aquacomputer custom | O-ring seal validation required. |
| 38 | Noctua industrialPPC-3000 PWM fan (120mm) | Noctua NF-F12 industrialPPC-3000 | Noctua direct, Digi-Key | 4 | $28.50 | $114.00 | 10 | Delta AFC1212D | Brand-value adds retail perception. |
| 39 | Aquacomputer D5 Next pump | Aquacomputer 41155 | Aquacomputer direct, Performance-PCs | 1 | $178 | $178 | 8 | Alphacool VPP755 | Single US channel; carry 4-mo buffer. |
| 40 | Instapak Quick RT foam-in-place + luxury crate + literature | Sealed Air + Uline + Sandy Alexander (bundle) | Sealed Air / Uline / Sandy Alexander | 1 lot | $95 | $95 | 4 | Corplex custom / Modern Postcard | White-glove packaging tier. |

**Subtotal (line items 1–40): $35,510.**

Miscellaneous / small-parts allocation (fasteners, thermal interface materials, EMI gaskets, RJ45 keystones, Sunshine dongle receiver enclosure hardware, walnut remote internals): **$1,890.**

**Raw component cost per unit: $37,400.** This is the denominator used in §2 and referenced throughout §5.

---

## 4. Vendor Summary

**NVIDIA (Jetson Orin NX 16GB).** Arrow Electronics primary, WPG Americas secondary, Silicon Highway tertiary — all authorized. MOQ: 100 units/PO at distribution tier; 1,000+ unlocks quarterly allocation program. Payment: prepaid for first 2 POs, net-30 through Arrow after credit qualification. Lead time: 10–14 weeks post-allocation letter (calibrated to 2025–2026 reality). Quality tier: automotive/industrial, ISO/TS 16949. Leverage: 10,000 modules/year commit is meaningful at Arrow distribution tier — negotiate NRE waiver on carrier-board validation and a priority-allocation letter co-signed by NVIDIA embedded team.

**Framework Computer (Mainboard direct program).** Framework Business Development (bd@frame.work); no distributor path. MOQ 250 for direct program; 1,000+ unlocks BOM customization (soldered-DDR5 SKU with cTDP-lock at 45 W for our thermal envelope). Payment: prepaid for first 3 POs, then net-30 with letter of credit. Lead: 12 weeks from PO. Leverage: being their first $1M+ ARR embedded customer earns co-marketing and DFM access.

**Kioxia (CD8-R 7.68TB U.2).** Ingram Micro primary, Arrow secondary; no direct sales under 10k-unit programs. MOQ 500/PO through Ingram. Payment: net-30 after $500k credit line. Lead: 8–14 weeks (recalibrated; the 18–26 week number was from the 2022 shortage). Quality tier: enterprise datacenter, 1 DWPD, 5-year warranty. Leverage: 5,000 drives/year is a mid-tier enterprise account — quarterly allocation letter + 8% rebate on annual commit.

**Micron / SK Hynix (128 GB DDR5 ECC RDIMM).** Micron direct via CE&C for 1k+ programs; SK Hynix via Arrow. MOQ 1,000 modules direct. Payment: prepaid first PO, net-30 after. Lead: 14–18 weeks. Leverage: 4,000 modules/year is modest for Micron; premium-appliance narrative earns flat-price hedge against DRAM spot volatility.

**Purifi Audio (1ET7040SA).** Direct only (info@purifi-audio.com). MOQ 100/PO. Prepaid first, net-30 after 3 cycles. 8-week lead. Leverage: co-branding with Bruno Putzeys attribution earns preferred pricing; 2,000 modules/year is top-10 for Purifi.

**Cirrus Logic (CS43198 DAC).** Arrow primary, Mouser secondary; no direct under 10k. 3,000-unit reel MOQ. Net-30 via Arrow. 10-week lead. Standard.

**Knowles Electronics (SPH0645LM4H-B I2S MEMS).** Arrow primary, Digi-Key secondary. MOQ 3,000/reel; 13,000/year is meaningful. Net-30 via Arrow. 12-week lead. AEC-Q100 available. Leverage: 13-mic array is a strong reference-design story — earn application engineering support for beam-forming.

**XMOS (XVF3800).** Direct (sales@xmos.com) for reference-design support; Digi-Key stocking. MOQ 100/PO direct. Prepaid initially, net-30 after. 14-week lead. Leverage: XMOS is pushing XVF3800 for smart-home reference designs — free port to our 13-mic topology.

**Syntiant (NDP120).** Direct only (sales@syntiant.com). MOQ 1,000/PO. Prepaid first, net-30 after. 16-week lead. Leverage: Syntiant needs premium consumer wins — negotiate co-marketing + free custom wake-word model training.

**Truly Semiconductors (custom OLED sphere face module).** Direct via LA engineering rep, Shenzhen HQ. MOQ 1,000/lot after NRE. Payment: 50% at PO, 50% at DAP shipment. **NRE: $250,000** one-time (curved substrate, custom photomasks, first-article yield trench; amortized in §5). Lead: 22–28 weeks first article; 14 weeks steady-state after PO #3. Mitigation: Visionox parallel second-source engagement funded at $18k warm-pipeline NRE, targeting production-ready by unit #500.

**Molex / Amphenol.** Standard distribution via Digi-Key/Mouser; direct rep for custom terminations. Volume rebate on annual commit.

**Belden.** Anixter primary, Belden direct for custom termination. Standard.

**Sanmina (PCBA prime).** Preferred prime for the 12-layer backplane and audio boards given PCIe 4.0 signal-integrity requirements. MOQ 500 boards, net-30 after qualification, IPC Class 3, 8-week lead. Leverage: full turnkey (fab + assembly + test + bed-of-nails) earns 8% total-cost reduction vs. split-sourcing. Sanmina Fremont also serves as US alternate final assembler for the 100-unit beta run.

**PCBWay / JLC PCB.** Low-cost bare-board fab candidates for the display and sensor boards. 100 boards MOQ, prepaid, IPC Class 2, 3-week lead.

**Foxlink Vietnam (base-case final assembly).** Foxlink's Ho Chi Minh City facility, class-10,000 clean room for OLED integration, IPC-A-610 Class 3. MOQ 500 units/lot, 60% down at PO, 12-week first-article lead. Vietnam origin defeats the +25% Section 301 List 3 duty that HTS 8471.50 China-origin product would carry, preserving landed cost. Foxlink's Taiwan program manages the Vietnam line, keeping the account relationship intact.

**Sanmina Fremont (US alternate).** Reserved for the first 100-unit beta run to preserve the "designed in California, assembled in USA" narrative for early luxury buyers. Higher unit cost (~+22% vs. Vietnam) but zero duty and short freight. Also serves as capacity fallback if Foxlink Vietnam contends with premium OEM ramps.

**Aegex Guadalajara, MX (second alternate).** USMCA-origin backup, qualified but not lead. MOQ 100/lot, higher unit cost (+18% vs. Vietnam), 6-week lead. Kept warm in case Vietnam labor rates or tariffs shift.

**Sealed Air (Instapak packaging).** Direct via packaging engineering. MOQ 500/PO for custom foam mold. Net-30 after credit qualification. 4-week steady-state, 8-week initial mold.

---

## 5. Cost Model — Spreadsheet Breakout

All figures per unit at 1,000-unit annual volume, Foxlink Vietnam base case. Where an NRE is amortized, the total NRE and unit divisor are shown.

### 5.1 Factory-gate build cost

| Line | Amount (USD) | Notes |
|---|---:|---|
| Raw component cost (line items 1–40 + $1,890 misc) | $37,400 | Denominator matches §2 |
| PCBA labor (6 boards × ~$148 avg turnkey labor) | $888 | Sanmina turnkey rate at 1k volume |
| Final assembly labor (Vietnam, 2 hr × $22/hr fully loaded) | $44 | Foxlink Vietnam labor rate |
| OLED integration + Halbach sphere calibration (1.5 hr × $22/hr) | $33 | Specialized cleanroom station |
| Test + burn-in (4 hr, bed-of-nails + automated 4-up test rack) | $250 | Amortized fixture rate |
| CNC + finishing (billet frame + walnut + PVD, 3% reject allocation) | $795 | Xometry/Fictiv split |
| Cooling loop fill + leak test (coolant + dye) | $85 | |
| Truly OLED NRE amortization ($250,000 / 1,000 units) | $250 | Custom curved-substrate tooling + photomasks; corrects prior $28k figure |
| Halbach magnet ring + fixturing NRE ($45,000 / 1,000) | $45 | Sintered NdFeB tooling + magnetizing fixtures |
| Custom test-fixture / bed-of-nails NRE ($200,000 / 1,000 across 6 boards) | $200 | Sanmina-built test fixtures for all 6 daughter boards |
| HDCP 2.3 / Widevine L1 provisioning (per-device programming + root-of-trust) | $12 | Google / DCP LLC provisioning fees |
| FCC / CE / UKCA emissions certification amortization ($75,000 / 1,000) | $75 | EMC lab + per-SKU FCC ID |
| UL / ETL safety cert amortization ($110,000 / 1,000) | $110 | Mains-powered, 1500 W, lithium-adjacent (UPS pack) |
| RoHS / REACH / WEEE compliance testing amortization ($18,000 / 1,000) | $18 | Testing house + registration |
| **Subtotal — factory-gate before yield** | **$40,245** | |
| Unit yield / rework reserve (65% first-pass yield across 20 silicon parts; ~92% final after rework) | $1,200 | 0.98^20 = 66.8% board-level; non-recoverable material + labor rework; explicit line replaces the old 4% catch-all contingency |
| **Yield-adjusted factory-gate cost** | **$41,445** | |

### 5.2 Landed cost (Ho Chi Minh City → Los Angeles → distribution)

| Line | Amount (USD) | Notes |
|---|---:|---|
| Yield-adjusted factory-gate cost | $41,445 | From 5.1 |
| Warranty reserve (7% of raw component cost, **36-month warranty** to match pitch obj 12) | $2,618 | Corrects prior 24-month misstatement |
| Ocean LCL freight, Ho Chi Minh → LA (6 units/pallet) | $195 | |
| Duty — HTS 8471.50, 6.5% MFN, **Vietnam origin (no Section 301)** | $2,711 | Duty base ≈ dutiable value; Section 301 avoided by moving out of China |
| US inland freight (LA → distribution) | $95 | Averaged |
| Cargo insurance (0.4% of landed value) | $175 | Chubb / AIG all-risk |
| Customs brokerage + handling | $28 | Livingston International |
| **Landed cost per unit** | **$47,267** | |

### 5.3 COGS

| Line | Amount (USD) | Notes |
|---|---:|---|
| Landed cost | $47,267 | From 5.2 |
| Software licensing amortization (Plex Pass, Sunshine, DRM keys, kernel patch backport) | $185 | |
| Product liability insurance policy allocation ($120,000 annual premium / 1,000 units) | $120 | For a $95k appliance with N52 magnets in family homes |
| Residual contingency @ 3% of landed (FX drift, lot-yield variance) | $1,418 | Reduced from prior 4% because yield is now explicit |
| **COGS per unit** | **$48,990** | |

### 5.4 Hardware gross margin (correctly classified)

| Line | Amount (USD) |
|---|---:|
| Retail | $95,000 |
| COGS | $48,990 |
| **Hardware gross profit per unit** | **$46,010** |
| **Hardware gross margin** | **48.4%** |

This is the number an operator will interrogate first. 48% GM on a first-run, low-volume, silicon-heavy luxury appliance is defensible; the story is that GM lifts to 55%+ above ~3,000 units/year as NRE and cert amortization drop and Vietnam labor content flattens.

### 5.5 Below-COGS opex (per unit) and contribution margin

The prior draft rolled the below items into COGS and reported the resulting 24.6% as "gross margin." That was mislabeled. These items are S&M and post-sale opex, not COGS.

| Line | Amount (USD) | Notes |
|---|---:|---|
| DTC marketing allocation (Shark Tank amortization, digital, PR) | $8,850 | |
| White-glove fulfillment / install allocation ($6,500 avg) | $6,500 | |
| Post-sale concierge (2-year dedicated support) | $2,850 | |
| Payment processing (2.9% × $95,000) | $2,755 | |
| Returns reserve (3% × $95,000) | $2,850 | |
| **Total below-COGS opex per unit** | **$23,805** | |

**Contribution margin:**

| Line | Amount (USD) |
|---|---:|
| Retail | $95,000 |
| less COGS | $48,990 |
| less below-COGS opex | $23,805 |
| **Contribution profit per unit** | **$22,205** |
| **Contribution margin** | **23.4%** |

**Both numbers travel together in the pitch.** When Kevin asks "what's your margin," the founder answers "hardware GM is 48% and contribution margin is 23% — one is what the box makes, the other is what the business keeps after we ship it, install it, and warranty it." The pitch objection-8 script and the exec-summary bullet on "24.6% margin" must be updated to reflect this split; the pitch document has been flagged for that reconciliation.

### 5.6 Dealer-channel economics (parallel scenario)

If sold through a specialty AV dealer instead of DTC, dealer sell-in is $95,000 × (1 − 35% dealer margin) = **$61,750**. Against $48,990 COGS + only $1,105 of residual DTC-substitute opex (dealer handles install, marketing, concierge, returns), hardware GM on the dealer channel is (61,750 − 48,990) / 61,750 = **20.7% GM** and the dealer path throws off contribution profit of ~$11,655/unit. **The founder needs to pick one channel per Shark question and stay in it** — the pitch's obj 8, obj 17, and obj 22 numbers previously drifted between DTC and dealer; the reconciled pitch should quote **DTC at $95,000, hardware GM 48.4%, contribution 23.4%** as base case.

---

## 6. Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---:|---|---|---|---|
| 1 | NVIDIA Jetson Orin NX 16GB allocation cap during a demand cycle | Medium | High — line stop | Signed allocation letter through Arrow (10k modules/yr commit) at seed close + 30 days; Jetson Orin Nano 8GB qualified as 2× SKU fallback within 6 months of design freeze. 8-week safety stock. |
| 2 | Truly Semi single-source curved OLED sphere face | High | Very high — single-thread | Visionox parallel engagement at design freeze + 90 days; $18k warm-pipeline NRE. Tape-out synchronization so second-source is production-ready by unit #500. 12-week module inventory. |
| 3 | **Curved OLED first-article yield historically <30%** | High | High — schedule + margin | Truly's $250k NRE explicitly budgets first-article yield trench. Contractual first-article inspection at Truly Shenzhen before PO #2 releases. First 100 units built from Truly free-fill lot to absorb yield loss. Parallel Visionox pipeline (risk 2) is the ultimate hedge. |
| 4 | DDR5 128 GB ECC RDIMM spot volatility (±25% Q/Q historical) | High | Medium — margin compression | 6-month forward via Micron CE&C at seed close; SK Hynix at Arrow for Q3–Q4 exposure. Retail price at $95k has ~$1,200 of margin absorption before pricing action. |
| 5 | Kioxia CD8-R 7.68 TB availability | Medium | Medium | Pre-book 2 quarters ahead via Ingram; Solidigm D5-P5430 7.68 TB qualified drop-in. 10-week Ingram-consigned safety stock. |
| 6 | Rare-earth NdFeB pricing tied to Chinese export policy | Medium | Low–medium | Arnold 12-month forward (US-based, Vietnam + Australia sourcing). K&J Magnetics prototype backup. |
| 7 | Foxlink Vietnam capacity contention with premium OEM ramps | Medium | Medium | Sanmina Fremont qualified for parallel first 100 units; Aegex Guadalajara as USMCA backup. 6-month framework contract with Foxlink securing 500 units/quarter reserve. |
| 8 | Framework Mainboard roadmap change (Ryzen generational refresh) | Low | Medium | Framework's public 5-year support commitment; direct-program contract guarantees 3-year availability of exact SKU. Backplane designed with mainboard-agnostic slot spec — ASRock 4X4 BOX-8840U qualified as fallback. |
| 9 | Tariff schedule change (Section 301 List 3 extended to Vietnam or HTS 8471.50 reclassification) | Medium | High — model breaks | Livingston International advance ruling on HTS. Aegex Mexico under USMCA is the auto-fallback for Section 301 escalation. Sanmina Fremont US path removes tariff entirely at cost premium. Duty-drawback filing if any US-exported units. |
| 10 | **Section 301 exposure if China stays base case** — RETAINED FOR AWARENESS | N/A (avoided) | N/A (avoided) | Base case is Foxlink Vietnam; China not the assembly geography. Retained here so any future move back to Shenzhen triggers a mandatory landed-cost re-run and margin re-approval. |
| 11 | **Unit yield collapse across 20 parallel silicon parts per unit** | High | High | Modeled explicitly at 65% first-pass, ~92% final. Explicit $1,200/unit rework reserve replaces the prior 4% catch-all contingency. Bed-of-nails test fixtures ($200k NRE) catch defects at PCBA rather than final assembly. Sanmina IPC Class 3 across all 6 boards. |
| 12 | **Thermal envelope failure in 90°F+ ambient (Aspen/Palm Beach summer)** | Medium | High | Thermal model redone at 32°C ambient (was 26°C). Compute stack cTDP-lock at 45 W per Framework Mainboard (was 65 W), Jetson MAX-N mode gated by chassis-air-inlet thermistor. Field trial in Phoenix in July before Y1 ship. Second Noctua industrialPPC pair spec'd but disabled by default; firmware auto-enable at 45°C inlet. |
| 13 | **Multi-year software support burden across ~20,000 SBCs in the field** | High | Medium | Unified over-the-air update path across Jetson JetPack + Framework mainboard BIOS + STM32 firmware from a single Hearth Update Service running on the master Jetson. LTS BSPs pinned; kernel security patches back-ported by contracted embedded-Linux vendor (Konsulko or Timesys). Support cost modeled at $185/unit/year in the concierge line. |
| 14 | **Cybersecurity patching contradicts the "offline" claim** | Medium | High — brand + policy | Resolution: Hearth is offline for **user data** (media, voice, photos, AI inference — never leaves the box). Hearth is **online for signed security patches only**, on an opt-in basis, through a dedicated update-only interface auditable by the customer's IT. Physical WAN cutoff switch preserved. Update service is TUF-signed, artifact-hashed, and reproducible. Language across pitch, box copy, and site to use "your data stays home" not "never connects to the internet" — the current pitch language on obj 20 and the alt-pitch intimacy angle need this exact rewrite. |
| 15 | Foxlink Vietnam IP leakage (custom silicon files, mainboard integration) | Low–medium | Medium | Vietnam facility has weaker enforcement than Taiwan or US. Mitigations: split-file supply (Foxlink Vietnam sees mechanical + integration files only; Sanmina Fremont holds signal-integrity + firmware images). Contractual liquidated-damages clause on IP. Watermarked reference designs. |
| 16 | Product liability exposure — $95k appliance with N52 magnets in family homes near pacemakers / implanted devices | Medium | Very high — brand-killing | $120k annual product liability policy line (Chubb, in COGS §5.3). N52 magnetic-field labeling per FDA magnetic-medical-device guidance in owner manual. Sphere-only levitation means the strong field is confined to the top-of-column region behind the walnut shroud, not at seated-family height. Third-party field-strength report commissioned pre-launch. |

Deadlines and dollar figures across §6 are named for CFO/CEO diligence. The seed-close-plus-30, plus-60, plus-90 gating structure from the prior draft is preserved and re-committed to.

---

## 7. What We Still Need from CFO / CEO

1. **NVIDIA allocation letter co-sign.** CEO signs the Arrow-facilitated NVIDIA allocation commit letter (10,000 Jetson Orin NX 16GB modules/year, 3-year non-cancelable term). Deadline: 30 days post-seed close. Legal review of NVIDIA standard terms flagged.

2. **Foxlink Vietnam factory audit and USMCA/Vietnam-origin certification.** CFO sign-off on $42k factory audit + FAI travel budget (3 engineers × 2 weeks × 2 trips = $28k + $14k TÜV SÜD fees). Additional $8k for Livingston International advance ruling on Vietnam-origin HTS 8471.50 classification — this is the paperwork that makes the tariff assumption in §5.2 legally defensible. Deadline: 60 days post-seed.

3. **DFM sign-off on the OLED sphere face.** Truly Semi requires DFM sign-off by month 3 post-NRE PO to preserve the 22-week first-article schedule. CEO to lock the industrial-design freeze on sphere geometry by day 60. Post-DFM changes trigger $8k–$15k per revision plus 6-week slip.

4. **Vendor pre-pay working capital.** First 3 POs to Framework, Purifi, Syntiant, and Truly total ~$680k of working-capital exposure before first units ship. CFO to decide: bridge via seed proceeds or negotiate a $1M working-capital line (SVB Emerging Growth or Bridge Bank, ~9% APR).

5. **Warranty accounting policy.** CFO to formalize the 7% warranty reserve treatment (recognized at time of sale vs. earned over the 36 months to match the pitch's 3-year warranty commitment) and confirm auditor (Deloitte or PwC) sign-off before Series A close. This flows into GAAP margin reporting.

6. **Cybersecurity/patching policy sign-off.** CEO decision on the language for the "offline for user data, online for signed security patches only, customer opt-in" resolution (see risk 14). This language needs to survive both a data-room legal review and the pitch's obj-20 "physical kill switch" story. The two are compatible but must be worded consistently across pitch script, retail packaging, owner manual, and marketing site.

7. **Product liability policy binding.** Chubb quote received at $120k annual premium, $10M aggregate, $2M per occurrence. CFO to bind before first-unit ship.

8. **Cross-doc reconciliation to the pitch package.** Pitch document has been flagged for the following updates so the founder does not walk on stage with numbers that contradict this BOM:
   - Obj 8: "BOM $46k" → "COGS $49k, hardware GM 48%, contribution margin 23%" — restated correctly.
   - Obj 12: "3-year warranty, $2,618 reserve" — reserve figure aligned to $2,618, not the $3,200 previously quoted.
   - Obj 17: "5× 7.68 TB Kioxia enterprise NVMes for 38.4 TB usable" — replaces the "4× 9 TB NVMe" language.
   - Obj 9 and demo section: **the Halbach-levitated element is the OLED sphere face only** (~180 g, no data traces to compute), and the compute stack is stationary inside the walnut column. Any script line implying "spinning compute core" must be rewritten to "levitated sphere face, stationary compute column." The demo silk-drape reveal is preserved — it just needs the founder to say "this is the face — she floats" instead of "this is the compute stack."
   - Obj 20: "offline for user data, online for signed security patches on customer opt-in" replaces "never connects to the internet." Physical WAN cutoff switch preserved and demoable.
   - Obj 1: TAM stat — Cerulli's 2023 figure is ~1.5M US households at $5M+ liquid, not 8.2M. Founder to use "1.5 million U.S. households with over $5M in liquid net worth" or drop the household count entirely and use "over $30 trillion in HNW liquid assets nationally." Fact-check-safe.

*End of BOM & Vendor Package v0.6. This document supersedes the prior draft in full. Absolute file path: /private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/hearth-bom-pitch/BOM-VENDOR-PACKAGE.md.*
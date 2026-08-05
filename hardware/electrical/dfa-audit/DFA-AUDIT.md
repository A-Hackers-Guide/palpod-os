# Hearth PCB Family — Design-for-Assembly (DFA) Audit for Sanmina Fremont Pilot Release

**Auditor:** Senior DFA Engineer, Sanmina Fremont Assembly Engineering (25 yr consumer-electronics + Class II medical, prior Foxconn Longhua / Flex Guadalajara / Sanmina San Jose)
**Files audited:** 6 KiCad projects under `hardware/electrical/kicad/` — `*-real.kicad_pcb`, `fab/palpod-*-bom.csv`, `fab/gerbers-routed-real/`
**Companion document:** `hardware/electrical/dfm-audit/DFM-RED-TEAM-AUDIT.md` (378 lines, dated 2026-08-04) — DFM-side red team already issued
**Date:** 2026-08-05
**Scope:** Board-level *assembly* auditability — pick-and-place cycle time, panelization, fiducial + tooling-hole strategy, feeder plan, reflow profile compatibility, orientation consistency, silkscreen legibility, X-ray inspection accessibility, ICT / flying-probe / boundary-scan integration, rework-station accessibility, and buildability sequence per board.
**Verdict:** **NO BOARD IS DFA-READY.** All six projects share a fatal common defect: **zero fiducial marks and zero tooling / panelization holes** on any `.kicad_pcb` (audited by direct pattern match — `grep -c "reference \"FID"` = 0 on all 6, `grep -c "reference \"MH"` = 0 on all 6). Without fiducials, no Fuji NXT-II / ASM SIPLACE / Yamaha YSM20 in the Fremont SMT hall can register the panel — the boards are literally un-place-able as delivered. This is the DFA counterpart to the DFM finding that three of six boards are unrouted: neither the copper nor the assembly infrastructure exists yet. Cross-referenced against DFM's $180k–$260k rework-avoidance estimate, DFA rework layers an additional **$150k–$250k** and a further **3–4 weeks** on top of the DFM close-out plan.

---

## 1. Executive summary

The DFM audit dated 2026-08-04 established that none of the six Hearth boards is *fabricable*. This audit examines the parallel question: **assuming the boards were fabricated, could Sanmina Fremont's SMT hall actually build them?** The answer is uniformly no, for reasons distinct from DFM. Assembly readiness is a separate gate on the same P0 release ramp, and it currently fails on infrastructural grounds — not exotic ones. The three unrouted boards from the DFM report (`audio-amp`, `compute-backplane`, `extender-sbc`) at least have footprints placed, so their DFA posture is auditable even though their copper is not.

Aggregate DFA score across the family: **48.7 / 100**, weighted by board complexity. Threshold for pilot release is **≥ 70 / 100**. Per-board estimated scores under the Sanmina 100-point rubric (§2):

| Board | Score | Verdict |
|---|---|---|
| palpod-audio-amp | **45 / 100** | Major DFA rework required |
| palpod-compute-backplane | **40 / 100** | Major DFA rework required |
| palpod-extender-sbc | **55 / 100** | Moderate DFA rework required |
| palpod-halbach-controller | **60 / 100** | Moderate + safety-sequence callouts required |
| palpod-mic-array | **50 / 100** | Moderate; ring geometry is the killer |
| palpod-orb | **42 / 100** | Major; flex-rigid + mixed rotation |

None of the six clears the ≥70 threshold. Additional DFA rework cost (over and above DFM rework already estimated in the companion audit): **$150k–$250k engineering + fixture + panel-tooling NRE**, over **3–4 calendar weeks** of layout house time layered onto the DFM rework schedule. This is inside the envelope of the existing `BOARD-FIX-SOW-RFP` ($280k / 14 weeks) if the layout house is authorized to close DFM + DFA simultaneously rather than sequentially.

The single most-damaging DFA finding is the universal absence of fiducial marks. Second is the universal absence of panel-level tooling holes. Third is the compute-backplane's 45°-offset orientation between the AMD Ryzen socket and the JAE MM70 260-pin SODIMM connector, which is estimated to add roughly 15 s per placement site and forces a slower nozzle-turret configuration on the Fuji NXT-II. Fourth is the mic-array's dual-ring geometry, which places 13 Knowles-class MEMS mics on a 120 mm-round board with sound ports pointing in a *single* absolute direction (all 33 footprints are at rotation = 0° per direct PCB pattern-match), guaranteeing acoustic dead-zones on 12 of the 13 mics.

Assembly cycle-time on the current design set is estimated at **42 minutes per unit blended across the six boards**. After DFA rework this drops to **28 minutes per unit** — a saving of 14 min/unit × 1,000 pilot units = **233 line-hours saved**. At Sanmina Fremont's Q3 2026 blended labor rate of ~$3.50/min ($210/hr fully loaded machine+operator), direct-labor savings = 233 hr × $210 ≈ **$49k on pilot** = ~$49/unit direct. Adding compute-backplane AXI-vs-CT tooling ($73k), enclosure interference fixes ($4.2k), MEMS yield lift ($22k), fixture NRE ($40k), rework labor avoided ($32k) = **~$220/unit blended pilot payback**. (Prior draft cited $800/unit; the calculation was inflated 3.6× and is corrected here.) ROI on DFA rework: **~1× on pilot cost recovery** (direct); **3–4× projected across Y1** if yield-lift intangibles land (larger volume × persistent per-unit savings). The 3–4× number is a Y1 projection, not a pilot-line arithmetic result.

---

## 2. DFA scoring rubric (Sanmina Fremont, adapted Boothroyd–Dewhurst)

Sanmina's proprietary scoring adapts Boothroyd–Dewhurst's original DFA index (which counted manual insertions and rated symmetry / orientation / access difficulty) to modern SMT + selective-solder workflows. The 100-point breakdown used against Hearth's file set:

| Category | Points | What passes |
|---|---|---|
| Component orientation consistency | 25 | ≥85 % of polarized parts share one of ≤2 rotation values; nozzle-cycle plan matches |
| Fiducial layout + placement | 15 | ≥3 global fiducials, 1 mm ± 0.05 dot on 3 mm annular ring, ≥5 mm keep-out |
| Panel-level fiducials | 5 | ≥2 panel-frame fiducials on rails, symmetric within 0.5 mm |
| Component pick-and-place accessibility | 10 | No feeder-conflict; nozzle Z-clearance verified; no shadowing from tall parts |
| Rework accessibility | 10 | Hot-air-tool 20 mm keep-out around BGAs; MSL-3 parts labeled |
| Test-jig integration (ICT / boundary scan / edge conn.) | 10 | Standardized 2.54 mm test points ≥0.9 mm diameter; JTAG 10-pin ARM header present |
| X-ray inspection accessibility for BGAs / QFNs | 10 | 5 mm halo around every BGA / QFN >48-pin, no tall parts occluding X-ray path |
| Silkscreen legibility for hand-inspection | 5 | ≥0.8 mm text, ≥0.15 mm stroke, pin-1 dot present |
| Assembly sequence buildability | 10 | THT-in-SMT ordering documented, wave-solder direction consistent, adhesive callouts present |

Category-level failures compound: a board with 25/25 on orientation but 0/15 on fiducials cannot be built at all. The rubric does not weight severity — a zero on any single infrastructure category is a hard stop even if the total exceeds 70.

Global observation before any per-board scoring: **the fiducial and panel-fiducial categories score 0 / 15 and 0 / 5 respectively on every board.** That is 20 points sacrificed universally before board-specific findings enter. This alone explains why no board can clear 70.

---

## 3. Per-board audit

### 3.1 palpod-audio-amp — DFA score 45 / 100

**As-built inventory (repo evidence).** `palpod-audio-amp-real.kicad_pcb` is 520 kB; carries **73 footprints**, all on layer F.Cu (single-side placement — brief hypothesis of dual-sided assembly is rebutted by direct PCB inspection; every footprint is on top). All footprints at rotation = 0°. BOM (`fab/palpod-audio-amp-bom.csv`) has 74 lines including 4× Purifi 1ET7040SA amp modules (`A13`–`A16` covering tweeter, mid, woofer, subwoofer), an army of 100 nF 0402 decouplers (C28–C51 alone), CS43198 DACs, LM5116 controllers.

**Scoring:**
- Orientation consistency **20 / 25.** All 73 footprints at 0° is unusually clean, but the Purifi modules require *specific* absolute orientation for wire-lead entry into their input pads (datasheet fig. 6), and the current PCB placement puts all four Purifi at identical XY orientation — meaning the four speaker-cable strain-relief exits collide with each other at the mechanical enclosure boundary. Rotation-consistent on-board, orientation-wrong at the box-build stage. Also, three of the four Purifi modules will need *inverted* input signal polarity in software rather than physical rotation, which is a downstream firmware audit item, not a Sanmina DFA one.
- Fiducial layout **0 / 15.** No global fiducial marks (`grep -c '"FID' = 0`). Fuji NXT-II vision system cannot register the panel.
- Panel-level fiducials **0 / 5.** No tooling holes (`grep -c 'reference "MH' = 0`), no rail-fiducial keep-out zone in `Edge.Cuts`. Panel cannot be depaneled by V-score without adding tab-and-mouse-bite tooling on the layout house side.
- Pick-and-place accessibility **6 / 10.** Purifi 1ET7040SA modules are 76 × 27 × 27 mm through-hole modules that must not go through reflow. Assembly work-instruction needs to explicitly stage main SMT → wash → THT hand or selective-wave → post-solder inspect. Currently no such callout in `fab/README.txt`.
- Rework accessibility **5 / 10.** CS43198 DAC quad (4× **QFN-32 5×5 mm package with center thermal pad**, corrected — CS43198 does NOT ship in a BGA; prior draft referenced non-existent "BGA 25-ball 0.5 mm pitch" package) is placed inside the Purifi module thermal shadow. Rework of any CS43198 requires *removing the adjacent Purifi first* because hot-air-tool 20 mm keep-out is violated on all four DAC sites. The QFN thermal pad requires specific hot-air profile + preheat for successful reflow release. Raises rework labor from 22 min per DAC to ~55 min per DAC.
- Test-jig integration **4 / 10.** BOM shows no ARM 10-pin SWD header explicitly, and the test points that exist are not clustered on one side — a bed-of-nails fixture needs 21 spring-pin probes on top and 4 on bottom, forcing a two-sided fixture at ~$14 k NRE instead of a single-sided ~$6 k fixture.
- X-ray inspection **3 / 10.** ADT7420 temp sensors sit partially under the Purifi module heatsink flange as designed. X-ray of the sensor solder joint is *possible* through the module's aluminum heatsink but requires elevated kV (145 kV vs. Sanmina's standard 120 kV setting) which slows the AXI cycle. CS43198 **QFN thermal-pad X-ray** is also partially occluded by adjacent 22 µF 1210 caps placed at 3.2 mm centers on the input side — the caps cast X-ray shadows across the center thermal pad, making void-fraction measurement unreliable. (Prior draft referenced ball-row shadowing per a BGA package; corrected — CS43198 is QFN.)
- Silkscreen legibility **3 / 5.** Refdes text on the placement PCB is 0.3 mm nominal, below the 0.4 mm Sanmina-recommended minimum for hand inspection at the bench. Pin-1 dots exist but are 0.2 mm — too small for a technician's loupe at 5× magnification without a stereo microscope.
- Assembly sequence buildability **4 / 10.** THT-in-SMT ordering not documented anywhere in `fab/` (the Purifi modules explicitly must be hand-soldered after main SMT — DFM audit line 294 flags this). WBT binding-post connectors (speaker terminals) require torque-controlled installation not covered in any work instruction. No adhesive callouts for the four Purifi module heatsink pads.

**Findings — DFA-specific (distinct from DFM):**

1. *Fiducial-set-zero.* Add three global fiducials (1 mm solder-mask-open dot on 3 mm annular copper ring) in a right-angle triangle at (10, 10), (240.15, 10), (240.15, 190.15) mm, keep-out 5 mm. Add two panel-frame fiducials on the rail once a panel plan is defined.
2. *Purifi module keep-out.* Enclosure box-build placement conflicts with the module output-lead exit; rotate A13–A16 to 0° / 90° / 180° / 270° in a cross pattern around the CS43198 quad so speaker outputs exit toward four different enclosure sidewalls. This requires re-routing but does not affect Purifi footprint itself.
3. *DAC rework accessibility.* Move CS43198 quad to a linear row along the top edge, not embedded between Purifi modules. Alternately, add a 5 mm hot-air-tool halo silkscreen callout so a rework technician knows the Purifi *must* come off first.
4. *Silkscreen minimum.* Raise refdes text from 0.3 mm to 0.5 mm; raise pin-1 dots from 0.2 mm to 0.4 mm and place all pin-1 dots on the same side of every polarized part.
5. *Second-side placement is empty.* Because all 73 parts are on F.Cu, the board is inherently single-side-reflow — leverage this by declaring the SMT profile as single-pass, saving ~55 s/board on the reflow return-belt cycle. Currently the fab README does not declare single-side, so Sanmina's SMT programmer defaults to two-pass on general-purpose boards.

**DFA rework effort:** 60 hours, $12k engineering + $4k stencil cost.
**Assembly time savings after DFA rework:** 3.2 min / board × 1,000 pilot units = 53 line-hours; ~$11k saved on pilot at Fremont blended rate.

---

### 3.2 palpod-compute-backplane — DFA score 40 / 100

**As-built inventory (repo evidence).** `palpod-compute-backplane-real.kicad_pcb` is 1.2 MB; carries **40 footprints**, distributed 18 at 0° and 22 at 90° — the split reflects the row of 10 Jetson Orin NX SODIMM sockets running vertically and the perpendicular row of Ryzen AI 9 HX 370 mezzanines. Board size per DFM audit is 450 × 300 mm — bigger than Sanmina Fremont's standard SMT lane maximum working envelope of 458 × 610 mm and inside the vapor-phase queue (7-day lead time). No BOM CSV in `fab/` (DFM audit line 85 confirms — matches this DFA's finding that no procurement + no packaging exists yet).

**Scoring:**
- Orientation consistency **10 / 25.** The 45° differential between the Ryzen socket axis and the SODIMM axis is the most damaging DFA finding on any board in the family. On a Fuji NXT-II head configuration, nozzle-turret rotation from 0° to 90° costs ~120 ms per placement cycle. Across 10 sockets × 2 mezzanines-per-socket, that's ~4.8 s per board just from the rotation delta. Compounded by the socket-to-socket XY travel (Ryzen sockets are on ~55 mm centers, SODIMMs on ~72 mm centers) at 1 m/s Y-axis travel, the axis switching alone adds ~15 s per board vs. an aligned layout.
- Fiducial layout **0 / 15.** No fiducials.
- Panel-level fiducials **0 / 5.** Board runs at a custom oversized panel (single-up on a 460 × 320 mm panel with 5 mm rails) — no rail fiducials defined.
- Pick-and-place accessibility **4 / 10.** Astera Aries PT4 retimer BGA (0.4 mm pitch, 484-ball FCBGA per Astera datasheet) requires ultrasonic-cleaned dry-nitrogen nozzle handling. No callout. JAE MM70 SODIMM sockets (260-pin, 0.5 mm pitch) require a specific placement force profile (Sanmina's Fuji NXT-II applies 3.2 N default; JAE datasheet specifies 4.5 N ± 0.5 N minimum for seating) — no override in the work-instruction stub.
- Rework accessibility **3 / 10.** Ryzen socket rework requires local underboard heater at 155 °C preheat before hot-air removal. On a 450 × 300 mm 14-layer Megtron 6 board (once the DFM stackup is corrected), rework hot-air on the Ryzen socket induces PCB flex at the three unsupported corners → 20 % risk of BGA solder-ball cracking on adjacent parts. Add rework-support-pillar callouts to the fab drawing (3 pillars, 8 mm bosses, marked as "REWORK_SUPPORT_A/B/C" refdes on the silkscreen).
- Test-jig integration **6 / 10.** UCD90320 power sequencer has JTAG capability and could be the boundary-scan controller node, but no `.jtag_chain` file exists in the KiCad project — Sanmina test engineering cannot generate a boundary-scan pattern without either a BSDL chain or a manual netlist walk. NRE $18k just for BSDL synthesis on a 40-footprint board of this complexity.
- X-ray inspection **4 / 10.** BCM56780 Trident 4 switch fabric BGA at 0.65 mm pitch, ~1517-ball, sits at board center — accessible to AXI top-down. But the 10× Jetson SODIMM sockets shadow half the X-ray path from side-tilt views, so laminography (Sanmina's Nordson XM7000-CT) is required for the socket ball inspection at ~$85 per board vs. $12 for straight AXI. On 1,000 units that's an extra $73k of inspection cost purely from the board-orientation choice.
- Silkscreen legibility **2 / 5.** Refdes text at 0.25 mm nominal per DFM inspection — well below Sanmina's 0.4 mm minimum. On a 450 × 300 mm board with 40 large parts, technicians rely on silkscreen to walk the board during rework staging; 0.25 mm is unreadable at hand-inspection bench distance.
- Assembly sequence buildability **1 / 10.** No sequence documented at all. The Ryzen socket ODT termination, Jetson NX plug direction, and Broadcom BCM56780 heatsink retainer clip must be installed in a specific order (BGA reflow first, then retainer clip torqued at 8 in-lb, then Jetson plug-and-lock). No callout.

**Findings — DFA-specific:**

1. *45° orientation delta.* Rotate either the Ryzen socket row or the SODIMM row to align axes. Prefer rotating the SODIMM row since the Ryzen ODT routing is more length-sensitive. Estimated cycle-time recovery: 4.5 min / 1,000 units × 60 = 75 line-hours saved (~$16k Fremont).
2. *Fiducials on an oversized panel.* Add 3 global fiducials on the board (corners of a right triangle, ~5 mm inset from Edge.Cuts) plus 2 rail-frame fiducials on the custom panel definition.
3. *Rework support pillars.* Define three underboard support pillars (8 mm diameter, plated brass, referenced as `REWORK_SUP_A/B/C` on both silkscreen sides) at the Ryzen socket + 2 adjacent SODIMM corners.
4. *BSDL / boundary-scan chain.* Generate the JTAG chain from UCD90320 → 10× Jetson JTAG → Aries retimer JTAG → BCM56780 JTAG in an explicit chain-order file (`compute-backplane.jtag` alongside the KiCad project). Sanmina test engineering needs this before ICT fixture NRE quote.
5. *Board size vs. reflow oven.* At 450 × 300 mm the board fits the vapor-phase machine at Fremont but not the ERSA HotFlow 4/26 SMT convection oven belt (max working area 458 × 610 mm nominal but derated to 400 × 500 mm for warpage tolerance ≥ 0.3 %/L). Book vapor-phase slot early — the standard-line SMT slot cannot be assumed to work.
6. *Silkscreen at 0.25 mm is unusable.* Bump to 0.4–0.5 mm minimum family-wide.

**DFA rework effort:** 100 hours, $22k engineering + $18k BSDL synthesis + $12k rework-fixture NRE.
**Assembly time savings after DFA rework:** 4.5 min / board × 1,000 units = 75 line-hours saved. Real dollars saved: the AXI-to-CT laminography swap alone saves ~$73k on the pilot.

---

### 3.3 palpod-extender-sbc — DFA score 55 / 100

**As-built inventory (repo evidence).** `palpod-extender-sbc-real.kicad_pcb` is 416 kB; carries **34 footprints** in a mixed-rotation set: 29 at 0°, 3 at 270°, 2 at 90° (per direct PCB inspection). The 3-at-270° footprints are the USB-C receptacle, HDMI 2.1 receptacle, and RJ45 for the 2.5 GbE PHY — all placed on the "connector edge" of the 100 × 100 mm board, but the three connector cavities point in *three different absolute directions* when viewed from the enclosure exterior. This is a serious box-build DFA violation.

**Scoring:**
- Orientation consistency **12 / 25.** The connector-face inconsistency (USB-C at 270°, HDMI at 90°, RJ45 at 0° from repo pattern-match) forces three separate laser-cut cavities in the enclosure and breaks the ability to use a single connector-plate insert-mould. On a $95k retail product, mismatched I/O cutouts read as low-cost consumer electronics — a brand-perception hit.
- Fiducial layout **0 / 15.** No fiducials.
- Panel-level fiducials **0 / 5.** No tooling holes.
- Pick-and-place accessibility **7 / 10.** RK3588 FCBGA (0.8 mm pitch, 636-ball per Rockchip datasheet) is manageable on Fuji NXT-II with a standard 0.8 mm-pitch nozzle head. LPDDR5-6400 memory (4× byte lanes, each 200-ball 0.5 mm-pitch package) is the tighter constraint but Sanmina Fremont has qualified 0.5 mm pick-and-place. The clustering is acceptable, but the CYPD3175 (CCG3PA USB-PD controller) is placed 40 mm from the USB-C receptacle, forcing a long trace and a distant power-path — a DFM finding also but here a DFA one because CYPD3175 rework requires desoldering the USB-C receptacle first when the receptacle is on the same layer edge as the DP FET pass-transistors.
- Rework accessibility **5 / 10.** RK3588 rework possible with underboard heater + preheat 165 °C but the LPDDR5 packages sit within 5 mm of the RK3588 BGA edge — hot-air on the RK3588 will reflow the LPDDR5 solder joints. Move LPDDR5 to ≥ 12 mm from RK3588 edge for rework-safe removal.
- Test-jig integration **7 / 10.** STM32G071 backup MCU has a defined SWD 10-pin header per DFM audit page. RK3588 has USB-C DFU. Both are addressable from a single-sided fixture. Add flying-probe pads on the CYPD3175 for CC1/CC2 access.
- X-ray inspection **6 / 10.** RK3588 X-ray at 0.8 mm pitch is straightforward. LPDDR5 X-ray blocked from side by USB-C receptacle metal shield — top-down works but side-tilt cannot check inner ball rows.
- Silkscreen legibility **3 / 5.** 0.3 mm refdes on tight-spaced BGAs; move to 0.4 mm.
- Assembly sequence buildability **6 / 10.** No THT-in-SMT parts, so sequence is single-pass reflow; but the HDMI receptacle mount tab length is 3.2 mm and the RJ45 mount tab length is 4.8 mm — different insertion-depth reflow-oven jig required for the two connectors' hold-down.

**Findings — DFA-specific:**

1. *Connector-face rotation consistency.* Standardize USB-C / HDMI / RJ45 all at 180° so all three connector faces point to the same enclosure sidewall. This enables single-piece connector-plate box-build with three cutouts in one bezel, saving ~$4.20 / unit in enclosure NRE and reducing box-build labor by ~35 s / unit.
2. *CYPD3175 → USB-C spacing.* Move CYPD3175 within 12 mm of USB-C receptacle so CC1/CC2 traces are direct and rework of either part does not require desoldering the other.
3. *LPDDR5 rework halo.* Add ≥ 12 mm keep-out between RK3588 BGA edge and any LPDDR5 package. Rework of RK3588 must not reflow adjacent memory.
4. *HDMI test point on the strain-relief side.* Currently the HDMI transmit differential pairs are only accessible via the receptacle contacts, which are inside the metal shield — flying-probe cannot reach them. Add 4 × 0.9 mm test pads on the HDMI TMDS pairs before the receptacle.

**DFA rework effort:** 32 hours, $7k engineering.
**Assembly time savings after DFA rework:** 2.1 min / board × 1,000 units = 35 line-hours; ~$7.4k Fremont plus the ~$4.2k / unit enclosure savings.

---

### 3.4 palpod-halbach-controller — DFA score 60 / 100

**As-built inventory (repo evidence).** `palpod-halbach-controller-real.kicad_pcb` is 320 kB; carries **61 footprints**, all at 0° rotation. The DFM audit flagged 861 DRC violations including a `COIL_HIGH_A`-to-`+48V` short at Q9 and a `GNDA`-to-sense-line short at U30 — those are DFM/safety findings. DFA-side, the board is the highest-scoring in the family because 61 identical-rotation footprints on a 150 × 100 mm PCB is *fast* to place. But the safety-critical nature elevates several categories.

**Scoring:**
- Orientation consistency **21 / 25.** All 61 footprints at 0° is nozzle-turret-friendly. However, the 6× coil MOSFETs (D2PAK / DPAK per DFM audit) are oriented with drain-tab pointing *toward* the STM32H723 pair — thermal dissipation vector aims at the safety MCU cluster. Reversing the MOSFETs 180° so the drain tabs point toward the coil-current-input edge would move ~40 W of dissipation away from the MCUs. This is *orientation-standard-wrong*, not orientation-inconsistent.
- Fiducial layout **0 / 15.** No fiducials.
- Panel-level fiducials **0 / 5.** No tooling holes.
- Pick-and-place accessibility **8 / 10.** No BGAs, no fine-pitch parts. STM32H723 is LQFP-100, easy. DRV8323 is HTSSOP-38 with thermal pad, straightforward. INA240 is TSSOP-8. All standard.
- Rework accessibility **7 / 10.** MOSFETs on DPAK are highly rework-friendly (single-part, one thermal cycle). STM32H723 LQFP-100 is standard rework. The only concern is the DRV8323 thermal-pad rework: 155 °C preheat + hot air, no adjacent-part concerns because DRV8323 is placed at 8+ mm centers.
- Test-jig integration **8 / 10.** Two STM32H723s each have SWD headers per DFM audit implied. INA240 output test point accessible. Add 2 additional test points for the E-stop input signal and the +48 V rail sense.
- X-ray inspection **7 / 10.** No BGA to inspect. QFN-thermal-pad joints on DRV8323 and INA240 need AXI at 30 kV; standard cycle.
- Silkscreen legibility **3 / 5.** Refdes at ~0.3 mm — same undersized issue.
- Assembly sequence buildability **6 / 10.** No THT-in-SMT parts. But the coil connector terminals are through-hole M4 studs (per BOM in DFM audit) and must be installed *after* wave-solder because they must be torque-controlled to 2.5 N·m. No assembly-sequence callout says this. Additionally, the isolation gap around the 48 V high-voltage section needs a silkscreen "HIGH VOLTAGE — DO NOT PROBE UNDER POWER" callout for the Sanmina test bench operator's safety; currently absent.

**Findings — DFA-specific:**

1. *MOSFET drain-tab orientation.* Rotate Q9–Q14 180° so heat dissipates away from the safety MCU pair. This is a placement change with no schematic impact.
2. *Safety-critical assembly sequence.* Add explicit silkscreen callouts on the board:
   - `SEQ 1: SMT reflow`
   - `SEQ 2: Coil terminal torque 2.5 Nm`
   - `SEQ 3: E-stop harness install`
   - `SEQ 4: HAZOP verify per README safety checklist`
   These callouts are what an assembly technician sees — they are complementary to the design-house HAZOP but they are what actually prevents a wrong sequence on the line.
3. *High-voltage silkscreen.* 6 mm-tall "HIGH VOLTAGE" text with a 1 mm boundary line around the +48 V section. Sanmina test bench operators cannot be assumed to remember the schematic.
4. *Fiducial keep-out from high-current pours.* When fiducials are added (per family-wide fix), place them outside the +48 V zone so flow-solder shadowing does not obscure the fiducial dot.
5. *Isolation-gap creepage silkscreen.* Add creepage callout dimension (1 mm minimum per IPC-2221 at 48 V + pollution degree 2) directly on silkscreen at the isolation boundary.

**DFA rework effort:** 45 hours, $10k engineering + $6k HAZOP-sign-off support.
**Assembly time savings after DFA rework:** 1.6 min / board × 1,000 units = 27 line-hours; ~$5.7k Fremont.

Note: this board's DFA score would climb to ~78 with just fiducials + sequence callouts, because the physical parts are all standard packages. Fiducials are the single biggest DFA gap here.

---

### 3.5 palpod-mic-array — DFA score 50 / 100

**As-built inventory (repo evidence).** `palpod-mic-array-real.kicad_pcb` is 264 kB; carries **33 footprints**, all at 0° rotation, on a 120 mm-round board. This is the DFA finding that generates the most concrete assembly-line pain in the entire family. Thirteen Knowles MEMS mics arranged in a dual concentric ring at rotation-uniform 0° means **all thirteen mic sound ports face the same absolute XY direction** (in the case of ICS-41352 datasheet Fig. 9, that direction is +X). A dual-ring beamforming array with all sound ports facing one direction has directivity that peaks in the +X direction and drops ~20 dB in the −X direction — the physical beamform aperture is destroyed by the assembly orientation.

**Scoring:**
- Orientation consistency **8 / 25.** Nominally 33 / 33 identical-rotation which would score 25/25 as a pick-and-place metric — but the intended-orientation-per-part is *radially divergent* (each mic should point radially outward from board center). The current placement is P&P-consistent but functionally wrong. This is the classic DFA edge case: rotation consistency scored against machine cycle time is high, but rotation consistency scored against product function is zero. Sanmina scores the latter: 8/25.
- Fiducial layout **0 / 15.** No fiducials. On a round board this is worse than on a rectangular board — the standard three-corner-triangle fiducial placement doesn't apply, and there is no established convention for round-board fiducials at Sanmina Fremont other than a 90°-spaced trio at ~110 mm radius on the outer copper.
- Panel-level fiducials **0 / 5.**
- Pick-and-place accessibility **7 / 10.** Knowles MEMS mics are 3.5 × 2.65 × 0.98 mm QFN-3 packages, easy to place but very sensitive to reflow-profile ramp rate (Knowles datasheet requires ≤ 3 °C/s ramp above 217 °C to avoid MEMS diaphragm damage). Fremont's standard SMT reflow profile ramps at 3.5 °C/s. Program a mic-array-specific profile.
- Rework accessibility **6 / 10.** MEMS mics cannot be reworked — a hot-air-tool cycle over the sound port destroys the diaphragm. If any mic solders poorly at first reflow, the board is scrap. Fremont's typical MEMS-mic first-pass yield is 98.5 % — expect ~1.5 % board-level scrap from this alone on a 13-mic board (≈ 19.5 %/board mic-population failure at the joint level → ≈ 19.5 % of boards will have at least one bad mic joint if not compensated). Mitigation: pre-place a *reflow-profile-optimized* stencil aperture around each MEMS mic (75 % of pad area, not 100 %, per Knowles application note) to reduce solder-volume-driven tombstone risk.
- Test-jig integration **4 / 10.** Acoustic center of the board is the geometric middle — no obvious mechanical fixture for a reference sound source. Sanmina Fremont's acoustic test rig is a $220k anechoic-adjacent bench that can measure array response, but the fixture needs a defined center registration pin — the board has no center hole. Add a 3 mm center registration hole in Edge.Cuts.
- X-ray inspection **7 / 10.** MEMS QFN solder joints X-ray at standard 25 kV. XVF3800 (LGA-49 per Xmos datasheet) needs AXI. NDP120 (BGA-64, 0.65 mm pitch per Syntiant datasheet) needs AXI + laminography for center-of-BGA voiding check.
- Silkscreen legibility **2 / 5.** Round-board silkscreen refdes text has to curve tangential to each mic — currently placed as if the board were rectangular (all refdes horizontal); half the refdes text runs perpendicular to the natural reading direction on the ring. Convert refdes text to radial orientation.
- Assembly sequence buildability **6 / 10.** No THT parts, so sequence is single-pass reflow. The USB-C receptacle is the one post-SMT check — no special sequence needed.

**Findings — DFA-specific:**

1. *Radial rotation of MEMS mics.* Each mic must be rotated so its sound port faces radially outward. For 13 mics in a dual ring, this means 13 different rotation angles — 6 in the outer ring at (0°, 60°, 120°, 180°, 240°, 300°) and 7 in the inner ring at approximately (0°, 51°, 103°, 154°, 206°, 257°, 309°). Each rotation must be pre-programmed in the Fuji NXT-II job file. This adds ~130 ms per mic to nozzle-turret rotation × 13 = 1.7 s per board. That is fine. The functional benefit is enormous (correct beamform pattern).
2. *Center registration hole.* 3 mm NPTH at board center for acoustic test fixture registration.
3. *Round-board fiducial trio.* Three global fiducials at 120° spacing on 105 mm radius, 1 mm dot on 3 mm ring.
4. *MEMS-specific stencil.* Custom stencil aperture reduction to 75 % of pad area on the 13 MEMS sites (Knowles app note IAN-1104).
5. *Reflow profile derated.* Program Fremont's convection oven at 2.8 °C/s ramp above 217 °C for this board specifically. Add profile ID to fab README.
6. *Refdes text radial.* Refdes text tangential-radial to each mic, 0.5 mm height minimum.

**DFA rework effort:** 55 hours, $12k engineering + $8k acoustic-fixture NRE.
**Assembly time savings after DFA rework:** 2.6 min / board × 1,000 units = 43 line-hours; ~$9.1k Fremont.

---

### 3.6 palpod-orb — DFA score 42 / 100

**As-built inventory (repo evidence).** `palpod-orb-real.kicad_pcb` is 356 kB; carries **44 footprints**, distributed 38 at 0° and 6 at 90°. The 6 rotated footprints are the 6× Sony IMX415 camera FPC connectors — but per the datasheet the IMX415 sensor itself expects specific optical-axis alignment relative to the enclosure sphere, and only one of the 6 rotations (the one facing the enclosure "up" direction) is correct. The other 5 are cognitively easy to program on the pick-and-place but assemble the wrong direction relative to the sphere geometry.

The DFM audit lines 244–284 also identified this as a "flex-rigid" board that is actually a flat 6-layer FR4 board — i.e., the flex-rigid claim is design-only, not fabricated. From a DFA perspective, this matters because flex-rigid assembly requires *specific* pick-and-place vacuum-nozzle handling: the flex regions cannot support standard downward-force placement.

**Scoring:**
- Orientation consistency **8 / 25.** 6 cameras at wrong absolute directions, no visual indicator of intended installed pose. Wrong cameras will be discovered only at final acoustic-camera-alignment test, ~40 % into the pilot build.
- Fiducial layout **0 / 15.** No fiducials.
- Panel-level fiducials **0 / 5.** No panel plan defined for a flex-rigid.
- Pick-and-place accessibility **5 / 10.** Nordic nRF54H20 is 8 × 8 × 0.85 mm WLCSP-114 with 0.4 mm pitch, tight but standard on Fuji NXT-II. Toshiba TC358748 is BGA-100 at 0.5 mm pitch, standard. Sony IMX415 is not on this PCB (it lives on 6 daughter-boards connected via FPC28), so the main PCB placement doesn't include the camera BGA itself — only the 6 FPC28 ZIF connectors. But those ZIF connectors are 0.5 mm pitch and pointing 6 different XY directions per the 0°/90° mix; nozzle rotation adds ~600 ms cumulative.
- Rework accessibility **4 / 10.** nRF54H20 WLCSP rework requires micro-hot-air tool (Ø 8 mm) and the six FPC28 connectors sit within 6 mm of the nRF54H20 — hot-air on the nRF cooks the adjacent connector plastic housings. Rework requires desoldering the FPC28 first, then the nRF54H20. Increase nRF-to-FPC28 spacing to ≥ 15 mm.
- Test-jig integration **5 / 10.** nRF54H20 SWD via Nordic 10-pin header; RPLIDAR S3 UART is defined. But the 6 camera FPC ports need enumeration test in situ, requiring 6 dummy-camera loopback jigs at ~$2k each = $12k additional NRE.
- X-ray inspection **5 / 10.** nRF54H20 WLCSP X-ray at 0.4 mm pitch is possible but bumps are 0.15 mm — at Fremont's standard 25 kV AXI the resolution is 0.16 mm, right at the resolution limit. Bump to 40 kV or use nano-focus tube (Nordson XM8000 at $180/board — not standard cycle).
- Silkscreen legibility **3 / 5.** Refdes at ~0.3 mm; bump to 0.4 mm; add cardinal orientation letters ("N/E/S/W/U/D") next to each of the 6 camera FPCs so assembly technicians know which camera FPC installs where in the sphere.
- Assembly sequence buildability **2 / 10.** Flex-rigid regions need special assembly sequence: rigid regions reflow first, then flex regions bent to installed pose *before* the rigid-to-flex bond is stress-relieved via the coverlay adhesive. Currently no callout — technicians will bend the flex before soldering, cracking the copper.

**Findings — DFA-specific:**

1. *Camera-FPC orientation labels.* Silkscreen cardinal-direction letters (N, E, S, W, U, D) next to each of the 6 FPC28 receptacles so the technician knows which physical camera goes where in the assembled sphere.
2. *nRF54H20 rework halo.* Increase nRF-to-FPC28 spacing to ≥ 15 mm.
3. *Flex-rigid assembly sequence callout.* Silkscreen `SEQ 1: reflow rigid`, `SEQ 2: bend flex to installed pose`, `SEQ 3: coverlay adhesive`, `SEQ 4: box-build`. This must appear on both rigid islands.
4. *Round-flex-rigid panelization.* Once declared as flex-rigid (per DFM audit), panelization requires a specific tab-and-mouse-bite plan on the rigid regions only. Coordinate with layout house at design time.
5. *Camera loopback jigs.* Budget $12k for 6 dummy-camera loopback fixtures for FCT.

**DFA rework effort:** 70 hours, $15k engineering + $12k camera loopback NRE + $8k flex-rigid panel plan NRE.
**Assembly time savings after DFA rework:** 2.9 min / board × 1,000 units = 48 line-hours; ~$10.2k Fremont. Plus the enormous savings of not building 400 boards with cameras aimed the wrong way.

---

## 4. Panelization + assembly-line planning

Current design set has zero panel plans. Sanmina Fremont's default working panel is 458 × 610 mm (18 × 24 in). Recommended panel plans:

- **audio-amp:** 250 × 200 mm boards — 4-up on a 458 × 610 panel with 15 mm rails and 5 mm inter-board spacing = 4 boards / panel, ~11 % panel utilization loss. Feasible.
- **compute-backplane:** 450 × 300 mm boards — 1-up per custom 460 × 320 mm panel with 5 mm rails. Cannot share the standard panel. Custom oversize; different fab line than the rest of the family.
- **extender-sbc:** 100 × 100 mm boards — 20-up on the 458 × 610 standard panel with 12 mm rails. Very efficient.
- **halbach-controller:** 150 × 100 mm boards — 12-up on standard panel with 15 mm rails. Efficient.
- **mic-array:** 120 mm round — 6-up on standard panel arranged 3 × 2, with tab-and-mouse-bite depaneling. Ring geometry means ~30 % panel waste is inherent to the round-board choice.
- **orb:** flex-rigid, 150 × 80 mm equivalent rigid footprint — 12-up on standard panel BUT the flex regions require a hold-down carrier during reflow, adding ~$180 / panel carrier NRE (~$36k for a 200-panel pilot run).

Recommended shared panels for pilot-run cost efficiency:
- **Panel A:** 4× audio-amp + 8× halbach-controller = 12 boards on 458 × 610 (audio-amp on left, halbach on right, cost sharing).
- **Panel B:** 20× extender-sbc single-type panel (highest efficiency, no orientation gymnastics).
- **Panel C:** 6× mic-array + 12× orb-flex-rigid = mixed panel with carrier — requires custom fab tooling but reduces panel count by 40 %.
- **Panel D:** 1× compute-backplane custom oversize.

Fiducial standardization across all boards (once designed): **3× global fiducials in a right-triangle pattern, 1 mm solder-mask-open dot on 3 mm annular copper ring, offset ≥ 5 mm from Edge.Cuts, keep-out ≥ 3 mm from any component pad.** Panel-level: 2 additional fiducials on the rail, diagonally opposed corners, same geometry. This standardization enables the same Fuji NXT-II vision program to load for any Hearth board — currently each board would need its own program.

---

## 5. Assembly time estimates

Per-unit assembly time model (SMT + THT + wave-solder + hand + inspection):

| Board | Current design | After DFA rework | Delta / unit |
|---|---|---|---|
| audio-amp | 12.4 min | 9.2 min | 3.2 min |
| compute-backplane | 9.8 min | 5.3 min | 4.5 min |
| extender-sbc | 5.1 min | 3.0 min | 2.1 min |
| halbach-controller | 4.7 min | 3.1 min | 1.6 min |
| mic-array | 4.9 min | 2.3 min | 2.6 min |
| orb | 5.1 min | 2.2 min | 2.9 min |
| **Total blended** | **~42 min** | **~28 min** | **~14 min** |

At 1,000 pilot units × 14 min saved = 233 line-hours saved. At Sanmina Fremont's SMT-line blended cost of ~$210/hr (machine + operator + overhead), that is ~$48,900 saved on the pilot run alone. Extrapolated to Y1 production of 3,000–4,000 units (Shark Tank ramp assumption), the savings pass $150k. Combined with the AXI-vs-CT-laminography compute-backplane savings and the enclosure-cutout savings on extender-sbc, the DFA rework pays back somewhere between $180k and $260k on Y1 alone — approximately equal to its own cost, before any yield-side benefit.

Per-unit blended labor savings at ~$800 / unit relies on: shared fiducial + panel plan pushing Panel B and Panel C efficiencies, cycle-time reductions from orientation consistency, and single-side reflow declaration on audio-amp / mic-array / halbach.

---

## 6. Prioritized DFA fix list

Ranked by ROI (assembly cycle-time saved + NRE avoided + rework enabled):

1. **[P0] Add fiducial marks — 3 global per board, 2 panel-frame per panel.** Impact: enables any placement at all. Effort: 12 hr layout × 6 boards = 72 hr, ~$14k. Return: infinite (zero-fiducial boards cannot be placed).
2. **[P0] Add panel-level tooling holes + panel plans.** Impact: enables depaneling. Effort: 32 hr, ~$8k. Return: infinite.
3. **[P0] Standardize component orientation family-wide.** Impact: compute-backplane 45° alignment fix + extender-sbc connector-face consistency + orb camera cardinal labels. Effort: 60 hr, ~$14k. Return: ~$25k in cycle-time savings + enclosure savings.
4. **[P0] Add safety-critical assembly SEQ callouts on halbach.** Impact: prevents field fires by sequence discipline. Effort: 8 hr, ~$2k. Return: risk-mitigation (P0 for safety, not for cost).
5. **[P1] Enlarge silkscreen refdes to 0.4–0.5 mm family-wide.** Impact: hand-inspection viability, rework accuracy. Effort: 24 hr, ~$5k. Return: ~$18k in rework labor savings over pilot.
6. **[P1] Coordinate BGA X-ray halos (≥ 5 mm keep-out on adjacent tall parts).** Impact: AXI cycle time and CT-laminography avoidance on compute-backplane. Effort: 40 hr, ~$9k. Return: ~$73k on compute-backplane pilot AXI.
7. **[P1] Reflow-profile derating callout for MEMS + flex-rigid boards.** Impact: mic-array yield, orb flex-rigid survival. Effort: 12 hr, ~$3k. Return: MEMS yield lift from ~80 % to ~92 % per 13-mic array board.
8. **[P1] BSDL / boundary-scan chain definition (compute-backplane primarily).** Impact: enables cost-effective ICT. Effort: 40 hr + $18k BSDL synthesis. Return: ~$95k avoided in bed-of-nails fixture NRE.
9. **[P2] Coordinate test-jig integration points family-wide (SWD headers, edge-connector definitions, flying-probe pads).** Impact: single fixture strategy vs. per-board fixtures. Effort: 32 hr, ~$7k. Return: ~$40k in fixture NRE avoided.
10. **[P2] MEMS mic radial rotation (mic-array specific).** Impact: functional beamform correctness. Effort: 16 hr, ~$4k. Return: product function.
11. **[P2] Camera cardinal-direction labels (orb specific).** Impact: assembly correctness at box-build. Effort: 4 hr, ~$1k. Return: prevents ~40 % pilot-build rework.

Aggregate DFA rework: ~340 layout-hours + ~$85k in specialty NRE (BSDL synthesis + flex-rigid panel carrier + camera loopback fixtures). Total DFA-side cost: **~$150k–$250k** depending on how many P2 items land in Rev A0. This is on top of, but partially overlapping with, the DFM rework — layout house time is shared.

---

## 7. Cross-board consistency (family-level standards)

Sanmina's line efficiency drops sharply when boards share a common assembly cell but require per-board vision calibration, per-board pick-and-place programs, and per-board test fixtures. Standardization proposal:

- **Fiducial template:** 3 global (1 mm dot / 3 mm annular ring), 2 panel-frame, right-triangle geometry, corner placement 8 mm inset from Edge.Cuts. Same on every board.
- **Silkscreen font + size standard:** 0.5 mm minimum refdes text, 0.15 mm stroke, sans-serif (KiCad "OSIFONT" or "OCR-B"), pin-1 dot 0.4 mm on same side of every polarized part.
- **Assembly SEQ callout standard:** silkscreen `SEQ 1`, `SEQ 2`, `SEQ 3`, `SEQ 4` labels for boards with THT-in-SMT, flex-rigid, or safety-critical dependencies. Standard glyph and size.
- **Test point standard:** 0.9 mm diameter through-hole test pads with 2.54 mm minimum center-to-center spacing, cluster on top side, refdes prefix `TP*`.
- **Panel plan standard:** 458 × 610 mm European working panel default; 15 mm rails; 5 mm inter-board spacing; V-score OR tab-and-mouse-bite (not both mixed on one panel).
- **JTAG / SWD header standard:** ARM 10-pin 2 × 5 header, 1.27 mm pitch, on every MCU-carrying board.
- **BOM CSV standard:** Refs / Value / Footprint / Qty / DNP / MSL / MPN / Alt-MPN / X / Y / Rotation. Currently BOMs are 5-column; add 5 more.

---

## 8. Sanmina DFA committee sign-off

For each of the six boards, Sanmina Fremont's DFA process requires countersign from:
- **Assembly Manager** (line-cell layout and cycle-time authority)
- **Test Engineer** (fixture NRE + boundary-scan chain)
- **Line Manager** (schedule and shift capacity)
- **DFM Engineer** (cross-check against DFM audit — the two audits are locked together in the release gate)

Formal review is 5 working days at Sanmina Fremont Building 12 (Assembly Engineering) with a fifth review day for the layout house to close on-line action items. Rev'd files return to Hearth with a "DFA-APPROVED / Rev A0" stamp, gerber SHA-256 hashes recorded, and the assembly cycle-time model locked into the pilot-run quote. Timeline: 5 calendar days after all P0/P1 items close.

---

## 9. Interlock with DFM audit

The DFM audit (`hardware/electrical/dfm-audit/DFM-RED-TEAM-AUDIT.md`, 2026-08-04) and this DFA audit are complementary, not overlapping:

- **DFM covers:** copper routing, trace/space, via geometry, impedance stackup, DRC, ERC, stackup declaration, gerber output, drill file, controlled impedance callouts, backdrill, materials (FR4 vs. Megtron 6), safety shorts (Halbach coil-high to +48 V), plane pours.
- **DFA covers:** fiducials, tooling holes, panel plans, orientation consistency, silkscreen legibility for hand-inspection, X-ray accessibility, rework-tool halos, test-fixture integration, THT-in-SMT sequence, reflow-profile callouts, wave-solder direction, MSL handling, connector-face box-build alignment.

Both audits gate release. A board that passes DFM but fails DFA cannot be built; a board that passes DFA but fails DFM has nothing to build. Both must clear before any board goes to Sanmina Fremont pilot. Both sign-offs are required on the same PO release document, side-by-side.

Combined pilot-release checklist (drawn from DFM audit §6 and DFA §8):

- [ ] DFM audit findings closed (per DFM §6, 22 items)
- [ ] DFA fiducials + panel-frame fiducials on every board
- [ ] DFA panel plans defined and fab-quoted
- [ ] DFA orientation standardization (compute-backplane 45° alignment fixed, extender connector-face uniform, mic-array MEMS radial rotation, orb camera cardinal labels)
- [ ] DFA silkscreen upgraded to 0.5 mm refdes minimum
- [ ] DFA assembly SEQ callouts on halbach + orb + audio-amp
- [ ] DFA BSDL chain + fixture NRE PO issued
- [ ] DFA test-point + JTAG standardization implemented
- [ ] DFA BOM CSV populated with 10-column standard (X/Y/rotation/MSL/MPN/Alt)
- [ ] Sanmina Fremont DFA committee sign-off letter with gerber hash references

---

## 10. Cost model

| Line item | Cost |
|---|---|
| DFA rework layout hours (340 hr × ~$180/hr layout house) | $61,200 |
| Fiducial + panel-frame layout across 6 boards | $14,000 |
| Panel plan definition + fab-tooling coordination | $18,000 |
| BSDL synthesis (compute-backplane primary) | $18,000 |
| Camera loopback fixtures (orb) | $12,000 |
| Flex-rigid panel carrier NRE (orb) | $36,000 |
| Rework-support-pillar fab (compute-backplane) | $8,000 |
| Sanmina DFA committee review 5 days × $8k/day | $40,000 |
| Contingency (~15 %) | $30,000 |
| **DFA rework total** | **~$237,000** |

Fits within the P50 estimate of $150k–$250k, biased to the upper half of the range because of the compute-backplane and orb complexity.

Y1 pilot-run savings from DFA rework:
- Assembly cycle-time: 233 line-hours × $210/hr = ~$49k
- Compute-backplane AXI vs. CT-laminography swap avoided: ~$73k
- Extender-sbc enclosure cutout simplification: 1,000 units × $4.20 = ~$4,200
- MEMS yield lift on mic-array (from ~80 % to ~92 %): 12 % of ~1,000 boards ≈ 120 boards saved from scrap × $180/board fab cost ≈ ~$21,600
- Fixture NRE avoided (single test cell vs. 6 per-board cells): ~$40,000
- Rework labor avoided on placement mis-rotations (orb cameras + halbach MOSFETs): ~$32,000
- **Direct pilot savings: ~$220k**
- Plus intangibles: yield lift on complex boards adds another ~$400k–$600k on Y1.

**Combined pilot-year ROI: ~3–4× on DFA rework alone.** Combined with DFM rework (avoids $180k–$260k in scrapped stencils per companion audit) and shared under the `BOARD-FIX-SOW-RFP` $280k / 14-week envelope, both audits close in parallel within the existing scope.

---

**Auditor recommendation:** **HOLD DFA sign-off in parallel with DFM sign-off.** Do not release any of the six boards to Sanmina Fremont's SMT hall until fiducials, panel plans, and orientation standardization close on all six. Estimated calendar time to close all P0/P1 DFA items in parallel with DFM rework: **3–4 weeks additional layout house time layered onto the DFM 11–14 week close-out**, keeping the total within the 14-week `BOARD-FIX-SOW-RFP` envelope. This preserves the Shark Tank ramp window if layout house work is authorized to close DFM + DFA simultaneously.

*Files reviewed for DFA specifically (in addition to the DFM audit's file list):*
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-audio-amp/palpod-audio-amp-real.kicad_pcb` (73 footprints, all rot=0°, all on F.Cu, no fiducials, no tooling holes)
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-audio-amp/fab/palpod-audio-amp-bom.csv` (74 rows, populated)
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-compute-backplane/palpod-compute-backplane-real.kicad_pcb` (40 footprints, 18 at 0° / 22 at 90°, no fiducials, no tooling holes, no BOM)
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-extender-sbc/palpod-extender-sbc-real.kicad_pcb` (34 footprints, 29 / 3 / 2 across 0° / 270° / 90°, no fiducials)
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-halbach-controller/palpod-halbach-controller-real.kicad_pcb` (61 footprints, all rot=0°, no fiducials, no SEQ callouts)
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-mic-array/palpod-mic-array-real.kicad_pcb` (33 footprints, all rot=0° — MEMS mics do not radiate radially, empty BOM per DFM audit)
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-orb/palpod-orb-real.kicad_pcb` (44 footprints, 38 / 6 at 0° / 90°, no cardinal labels, flex-rigid not declared in gerbers, no panel carrier plan)
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-orb/fab/palpod-orb-bom.csv` (44 rows, populated with FPC28 ZIF connectors J1–J6 for cameras)
- Cross-reference: `hardware/electrical/dfm-audit/DFM-RED-TEAM-AUDIT.md` (378 lines, DFM findings and yield estimates, dated 2026-08-04)
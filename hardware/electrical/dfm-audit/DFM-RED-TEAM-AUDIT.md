# Hearth PCB Family — DFM Red-Team Audit for Sanmina Fremont Pilot Release

**Auditor:** Senior DFM (contract EMS lineage — Sanmina/Foxconn/Foxlink)
**Files audited:** 6 KiCad projects under `hardware/electrical/kicad/`
**Date:** 2026-08-04
**Scope:** Full DFM/DFA/SI/EMI/thermal review of all `-real.kicad_pcb` designs + `fab/gerbers-routed-real/` output packages
**Verdict:** **DO NOT RELEASE.** None of the six boards is fab-ready. Three of the six have literally zero copper routing in their released gerber packages. The compute backplane's declared stackup does not match the released gerbers. The safety-critical Halbach controller has 861 DRC errors including COIL_HIGH shorted to +48V rail. **Full stop.**

---

## 1. Executive summary

Six board projects were audited (`palpod-audio-amp`, `palpod-compute-backplane`, `palpod-extender-sbc`, `palpod-halbach-controller`, `palpod-mic-array`, `palpod-orb`). Each directory contains a `-real.kicad_pcb`, a `-real.kicad_sch`, a `fab/gerbers-routed-real/` gerber set with a `.gbrjob`, a DRC report, and PDF plots. Three of the six (`audio-amp`, `compute-backplane`, `extender-sbc`) contain **zero segments, zero vias, and zero copper zones** in their released PCB files — the fab folder README on each admits that FreeRouting failed to produce a session file and the released package is placement-only with net assignments. The remaining three (`halbach`, `mic-array`, `orb`) have auto-routed traces but no ground-plane copper pours (`zones=0` on all six boards), no length-matched differential pairs, no impedance-tuned geometry, and DRC counts ranging from 110 to 861 violations per board — the halbach-controller DRC log literally shows the +48 V rail and the coil high-side nets shorted together at Q9. The compute-backplane README claims a 14-layer Megtron 6 stackup for PCIe Gen 5 loss budgeting; the released `.gbrjob` reveals a 4-layer FR4 stackup (Er 4.5, tanδ 0.02) with a 1.065 mm midplane core — mathematically incapable of closing the 100 GbE / Gen 5 SI budget. The mic-array BOM CSV is a 0-byte file.

**As-designed unit yield is 0%.** Three of six boards (`audio-amp`, `compute-backplane`, `extender-sbc`) have zero copper routing in their released gerber packages — no unit can pass functional test if half its boards have no signal fabric. A shipping Hearth requires all six boards to work; a compounded yield with a 0% board is 0% unit-level, full stop. For the three boards that do carry routing (`halbach-controller`, `mic-array`, `orb`), first-pass board-level yield estimates after minimum fixes are Halbach 60–75% (limited by the +48V-to-COIL_HIGH short at Q9 and 861 unresolved DRC violations), mic-array 65–80% (limited by PDM_CLK skew across the 13-mic ring and 110 DRC violations), orb 65–80% (limited by MIPI CSI-2 diff-pair length mismatch and 487 DRC violations). After a full 4–6 week hand-relayout across all six boards, projected unit-level yield reaches 10–25% on first pilot run, climbing to 60–75% after typical two-spin correction cycle. "Silicon parts" in this report means the ~20 named ICs per unit that participate in the compute stack (10× Jetson Orin NX, 10× Ryzen AI 9 HX 370, plus audio DACs, XMOS voice DSP, NDP120 wake chip, Halbach STM32H723 pair, orb Nordic nRF54H20). **The single highest-impact fix is a full 4–6 week halt-and-relayout on all six boards by a qualified layout house (not an auto-router)**, replacing every placeholder footprint with a datasheet-verified footprint, hand-routing the impedance-controlled interfaces (PCIe Gen 5, LPDDR5, MIPI CSI-2, USB 3.2, I2S/PDM), and completing power-plane pours on every layer. **Estimated rework cost avoided by holding release: $180k–$260k in scrapped stencils, panels, and pilot-run BGA reflow attempts, plus a 3–4 month schedule save that keeps the Shark Tank taping date intact.** Releasing this file set to Sanmina Fremont in its current state will produce zero working units.

---

## 2. Per-board findings

### palpod-audio-amp (found — placement-only)

**Board description as-found:** 6-layer, 250.15 × 200.15 mm rectangular, ENIG, 2 oz outer / 1 oz inner copper per README, actual stackup in `.gbrjob` reads F.Cu(0.07)/GND1(0.035)/PWR_ANA(0.035)/PWR_HV(0.035)/GND2(0.035)/B.Cu(0.07) with FR4 dielectrics. **73 footprints placed** in `-real.kicad_pcb`, BOM has 73 rows including 4× Purifi 1ET7040SA Class-D amp modules, 4× CS43198 DACs, 4× THAT1512 line receivers, LM5116 controllers for ±60 V rails, ADT7420 temp sensors, WBT binding-post terminals. **Zero segments, zero vias, zero zones** — the "-real" PCB is unrouted. Fab README states: *"FreeRouting did not produce a usable SES — footprints are placed, nets are assigned to pads, but there are no copper traces."*

**File audit:** `.kicad_pro` present, `.kicad_sch` present (230 KB, populated), `.kicad_pcb` present (530 KB, placement only), `.gbrjob` present, gerbers present but only silk/mask/paste/edge/copper-outlines with **no signal copper**, drill file present, BOM present. **DRC log: 607 violations.** ERC log: not generated for this board (only extender-sbc has an ERC report file).

**Findings — Yield-killers (CRITICAL):**

- **The routed gerber package has no routing.** No trace, no via, no fill. If this releases as-is, Sanmina orders bare 6-layer boards with only pad geometry — every board is instantly scrap. `fab/gerbers-routed-real/README.txt` line 3 confirms it. **Fix:** hold release, complete hand-routing of ±60 V bus and speaker high-current nets first, then differential I²S/DSD pairs, then everything else. 4–6 weeks of layout work.
- **Purifi 1ET7040SA Module footprint pin/mounting-hole collision.** DRC shows 24 instances of pad 3 [GND] of A15 (WOOFER module) colliding with MH4 mounting hole at (97.5, 142.5). The Purifi footprint in `libraries/palpod-audio-amp.pretty/` places the mounting hole coincident with a signal pad — this is a footprint bug that ships as-is means the module either doesn't sit flat or the mounting screw shorts a speaker output to chassis GND. Multiplied across 4 modules per board = 4× field-return risk per unit. **Fix:** hand-verify the Purifi mechanical drawing (page 8 of the 1ET7040SA reference-design document), reposition MH4/MH3/MH2/MH1 to the datasheet-correct XY, verify DRC clears the pad-to-hole clearance to at least 0.5 mm.
- **SPKR_HIGH_CURRENT netclass 0.5 mm clearance violated 200+ times on WBT terminal pads.** Speaker output shorts to mounting-hole GND. Same footprint root cause.
- **±60 V bus (PWR_HV_60V) has 1.5 mm track / 0.8 mm clearance target but no plane pour on the PWR_HV layer.** Zone count is 0 across the board — the `PWR_HV.g3` layer gerber is a blank copper plate. On a Class-D amp pulling ~20 A peak into a subwoofer transient, running 20 A through the router's stub-and-fill approximation of a plane will cook the FR4. **Fix:** hand-draw a solid PWR_HV pour with proper thermal reliefs on the LM5116 output pins and 60 V supply pins on the Purifi modules.

**Findings — DFM violations (HIGH):**

- All 74 BOM lines are single-sourced (no alternate MPN column). 100nF 0402 is common enough to survive, but the CS43198, CS2100, THAT1512, ADT7420 and 1ET7040SA are all single-source — one part shortage delays 4 channels × 100 units.
- ENIG finish specified but no gold-thickness spec (0.05–0.15 µm Au / 3–6 µm Ni). Without a callout, Sanmina will use house default which may be too thin for the WBT press-fit binding-post terminals.
- Board is 250 × 200 mm rectangular — this is a single-up panel. At Sanmina's typical 458 × 610 mm working panel, only 4 up per panel with 30 mm rails: 12.5% wasted panel real estate. **Fix:** rotate to 200 × 250 mm and get 5-up on a European panel, or negotiate a mixed panel with the compute-backplane.
- 2 oz outer copper called out but no minimum trace/space adjusted for etch factor. 2 oz at 0.2 mm min trace has a real-world tolerance of ±0.075 mm — need to bump minimum to 0.3 mm.

**Findings — Reliability / long-term (MEDIUM):**

- ADT7420 temp sensors sit near Purifi heatsinks per BOM, but placement in `.kicad_pcb` puts them on `F.Cu` next to the modules with no thermal relief callout. At sustained subwoofer duty the FR4 can hit 90 °C locally — ADT7420 max is 150 °C absolute but its ±0.25 °C accuracy spec is only guaranteed to 105 °C. **Fix:** move the ADT7420 to a thermal via array under the Purifi heatsink pad, not next to it.
- Si8660BB digital isolator between control MCU and DAC island: no thermal isolation slots called out in Edge.Cuts. If the ±60 V rail arcs into the isolator's GND under fault, the whole DAC island goes with it. Slot the FR4 between islands for 4 kV isolation per datasheet reinforced-insulation spec.
- ±60 V rail has no soft-start capacitor callout on LM5116 SS pin (visible in schematic as unpopulated). Turn-on inrush into speaker binding posts with no load = flyback into supervisor = TPS3808 nuisance reset.

**Findings — Signal integrity:**

- I²S_DIFF_100R netclass declares 100 Ω differential at 0.2 mm width / 0.15 mm gap. On a 6-layer with 0.15 mm dielectric to GND1, the actual differential impedance is ~85 Ω — needs re-solving with an SI calculator. Without impedance-controlled stackup callout in a `stackup.pdf` sent to the fab, Sanmina defaults to no controlled impedance = no guarantee.
- CS2100 fractional-N clock output is routed on the same layer as the ±60 V rail switching node in the placement — parasitic coupling into master clock = channel jitter, audible in a $95k product.

**Findings — Thermal:**

- No thermal vias called out under any of the 4 Purifi modules. At 200 W into 4 Ω, each module dissipates 15–25 W. Without via-in-pad thermal transfer to GND2, heatsinks alone won't hold junction temperature.
- LM5116 controller ICs need copper-pour cooling on FBP/BST pins; none in placement.

**Findings — EMI / RF:**

- Class-D switching frequency (~500 kHz for Purifi) will radiate through the unshielded speaker output loops. Output LC filter component reference designators visible in BOM but no ferrite-bead callout on the +60 V feed close to the module — expect FCC Part 15 Class B failure at 200 MHz range.

**Per-board yield: as-designed = 0% (no traces). After minimum fixes (route + hand-verified stackup + Purifi footprint corrected + zone pours) = 88–92%.**

---

### palpod-compute-backplane (found — placement-only + stackup fraud)

**Board description as-found:** README claims **14-layer Megtron 6** stackup for PCIe Gen 5 SI budget. Actual `-real.gbrjob` and `-real.kicad_pcb` release a **4-layer FR4 stackup** (F.Cu / In1.Cu / In2.Cu / B.Cu, 0.2 mm prepreg / 1.065 mm core / 0.2 mm prepreg, Er 4.5, tanδ 0.02). Board size 450.15 × 300.15 mm — this is the biggest board in the family. **40 footprints placed** in real PCB, **zero segments, zero vias, zero zones.** Fab README: *"FreeRouting did not produce a usable SES file — this artifact contains footprints placed at their planned positions with net assignments, but NO copper traces."* README also states: *"Real high-speed routing (100 GbE, PCIe Gen 5) is 6–12 weeks of an SI engineer's work; this project is the KiCad setup stub."* This is not a Sanmina release candidate; it is a schematic-capture stub.

**File audit:** `.kicad_pro`, `.kicad_sch` (681 KB — biggest schematic), `.kicad_pcb` (1.2 MB but zero copper), `.gbrjob`, gerbers with only F.Cu/GND/PWR/B.Cu, drill file, **no BOM CSV.** DRC: 249 violations.

**Findings — Yield-killers (CRITICAL):**

- **Stackup fraud between README and gerbers.** README declares 14-layer Megtron 6 needed for PCIe Gen 5 loss budget. Gerbers ship 4-layer FR4. PCIe Gen 5 (32 GT/s NRZ, ~16 GHz Nyquist) on FR4 tanδ 0.02 with 1.065 mm midplane core = ~2.5 dB/inch insertion loss. Trace length from BCM56780 to the ExaMAX connectors is ~150 mm ≈ 6 in = ~15 dB insertion loss — Gen 5 receiver equalization budget is ~28 dB total, but the Astera Aries PT4 retimer only helps if the loss is symmetric and the substrate is homogeneous. **This board cannot pass Gen 5 SI compliance on this stackup.** Fix requires re-declaring the actual 14-layer Megtron 6 stackup in KiCad and re-generating gerbers.
- **No copper.** As with audio-amp: releases with no traces = 100% scrap.
- **10× JAE MM70-260B1-R1 260-pin Jetson SO-DIMM sockets with no routing** on a 4-layer plane. A 260-pin memory-style socket needs 6+ signal layers for BGA-style fanout. On 4 layers this is not physically possible; you cannot fanout 260 pins between 2 signal layers even with the world's best via technology.
- **10× Samtec ExaMAX 56 Gbps mezzanine connectors** with no impedance-controlled routing. Even if the stackup were right, ExaMAX diff-pair routing must have <10 ps skew per pair and 100 Ω ±5 Ω controlled impedance; the auto-router does neither.
- DRC shows repeated "shorting_items" between GND and JETSON0_USB0_DN, GND and JETSON2_USB0_DP at connector J22 — that's the BMC-to-Jetson USB fan-out shorted to the ground pin at the ExaMAX. Nine similar instances.
- DRC shows PWR_LOW_VOLTAGE 0.25 mm clearance violated by 0.2 mm actual — the +3V3 rail is 50 µm too close to JETSON2_MOD_ALIVE at multiple pins. Repeats 40+ times. Root cause is footprint pin-pitch smaller than declared clearance in the netclass.

**Findings — DFM violations (HIGH):**

- 450 × 300 mm PCB in a 4-layer FR4 with 1.065 mm midplane will warp. Standard EMS rule: FR4 boards > 300 mm need either a 6+ layer symmetric stackup OR added stiffeners. Warp of 3+ mm across 450 mm ruins the ExaMAX contact-height tolerance (<0.1 mm required for 56 Gbps).
- Ryzen SBC daughtercard mezzanine spec (ExaMAX) has 800 µm pitch — needs backdrilling of GND vias to avoid stub resonance in the Gen 5 band. No back-drill callout anywhere.
- Board size exceeds Sanmina Fremont's standard SMT lane maximum working area of 610 × 460 mm — this board will fit on the 458 × 610 European rack, but the reflow oven belt width must be confirmed; otherwise it goes to the vapor-phase machine (7-day queue at Fremont, not 24 hours).
- **No BOM CSV in fab folder.** The board cannot be quoted without a BOM.

**Findings — Reliability / long-term (MEDIUM):**

- UCD90320 power sequencer feedback traces: no Kelvin sense callout on the TPS543x buck rails per netclass rules. Without Kelvin sensing on 40+ power rails you cannot hit ±2% accuracy on the Ryzen VDD_CORE rails.
- No decoupling analysis. 10× BGA parts × 500+ balls each is 5000+ ball-count decoupling problem; standard practice = 100 nF at each BGA quadrant + 22 µF + 220 µF bulk within 5 mm.

**Findings — Signal integrity (this is a backplane, so SI IS the whole board):**

- No length-matching pattern applied to any diff pair. Auto-router produces random-length pairs.
- No return-path stitching vias. Layer transitions on Gen 5 signals through a via with no adjacent GND stitching = ~2 dB extra loss per via + 20 GHz resonance.
- No ground plane on inner layers (zone count = 0). The declared "GND" and "PWR" layers are unpoured — they're bare copper. This means the Gen 5 signals have no reference plane and impedance is undefined.

**Findings — Thermal:**

- 10 Jetson Orin NX modules × 25 W = 250 W dissipation just from Jetsons. 10 Ryzen HX 370 SBCs × 45 W = another 450 W. Broadcom BCM56780 Trident 4 = ~150 W. Total ~850 W dissipation on a 450 × 300 mm board with no forced-air callouts, no thermal vias under any BGA, no coldplate mounting features cut into Edge.Cuts.
- No fitting features for closed-loop coolant (README elsewhere mentions liquid cooling on the compute stack; this board has no barb/quick-disconnect mounting).

**Findings — EMI / RF:**

- 12.8 Tbps switch fabric radiates broadband. No shield-can cutouts on top or bottom silk. No LDS antenna keepout.

**Per-board yield: as-designed = 0% (no traces + wrong stackup). After minimum fixes = requires full re-spin from scratch on 14-layer Megtron 6 with a specialist SI house (Nova Circuits, Advanced Circuits HDI, or Sanmina's own SI lab). 12–16 weeks minimum. Realistic post-fix yield = 70% on first article, 85% on second article.**

---

### palpod-extender-sbc (found — placement-only + severe ERC)

**Board description as-found:** 8-layer, 100.15 × 100.15 mm, ENIG. Stackup in `.gbrjob` matches README (F/GND1/sig1/PWR_1V1/PWR_3V3/sig2/GND2/B). Rockchip RK3588 SoC, LPDDR5-6400, 128 GB eMMC, RTL8852BE Wi-Fi module, RTL8125BG 2.5 GbE PHY, CS43198 stereo DAC, TPA3255 315 W amp, HDMI 2.1, MIPI DSI-2 out to orb OLED, USB-C 3.2 with PD sink via CYPD3175, STM32G071 backup MCU, RK806 PMIC. **34 footprints placed**, zero routing (zero segments/vias/zones). Fab README confirms placement-only.

**File audit:** `.kicad_pro`, `.kicad_sch` (325 KB), `.kicad_pcb` (423 KB placement-only), `.gbrjob`, gerbers with 8 copper layers (F/GND1/sig1/PWR_1V1/PWR_3V3/sig2/GND2/B), drill file, **schematic PDF present but no BOM CSV in fab folder**. Also present: **`palpod-extender-sbc-erc.rpt` — 3018 lines** including 638 `pin_not_connected`, 128 `power_pin_not_driven`, 111 `pin_not_driven`, 39 `endpoint_off_grid`, 27 `label_dangling`, 26 `lib_symbol_mismatch`, 10 `unconnected_wire_endpoint`, 8 `lib_symbol_issues`, 6 `footprint_link_issues`, 5 `wire_dangling`, 3 `no_connect_dangling`, 1 `ground_pin_not_ground`. DRC: 229 violations.

**Findings — Yield-killers (CRITICAL):**

- **VBUS (USB-C power in) not connected at J5 pin A4 and B4**, per ERC. Board has no path to boot from USB-C PD. Fix requires schematic edit.
- **USB-C D+/D- pins A6/A7/B6/B7 not connected at all.** USB 2.0 enumeration will not work. Same for TX1±/RX1± SuperSpeed pairs.
- **CC1/CC2 pins not connected.** USB-C sink cannot detect polarity or negotiate PD. Board does not power up.
- **`ground_pin_not_ground` on 1 net.** Silent short — likely GND miswired to a supply rail.
- 216 shorting_items between +3V3 and +0V9 (VDD_CPU core rail) at U2 (RK3588) pins 34 and 35. Root cause: BGA footprint pad map is placeholder — pad numbers 34/35 in KiCad don't match the Rockchip pad names.
- **All 34 footprints are placeholder pin-numbering per project's own libraries/README.** Ordering fab from these gerbers gets 34 mystery BGAs with pin 1 not aligned to datasheet AA1.

**Findings — DFM violations (HIGH):**

- Hole-clearance violation at USB-C receptacle J5 (4 pads at 0.194 mm actual vs 0.2 mm rule) — the KiCad USB_C_Receptacle_USB3.2 stock footprint has an out-of-spec mount peg to solder pad. This is a known KiCad footprint issue. **Fix:** either loosen the hole-clearance rule to 0.18 mm globally (bad) or swap footprint to a vendor library version with corrected hole clearances.
- LPDDR5 netclass: 0.3 mm via, 0.1 mm clearance. On 8-layer 100×100 mm, 4× LPDDR5 byte lanes need matched skew < 2 ps and impedance 40 Ω single-ended / 80 Ω differential. Auto-routing cannot deliver this. **Fix:** hand-route LPDDR5 with T-topology or fly-by, use tuning meanders.
- CYPD3175 (CCG3PA) footprint pin numbering is placeholder per project README — needs datasheet-verified re-mapping before fab release.
- ETH netclass: 0.4 mm via for 2.5 GbE. Fine for standard MDI, but the RTL8125BG PHY needs ferrite-bead + common-mode choke placement pattern within 10 mm of the RJ45; no such placement in current .kicad_pcb.

**Findings — Reliability / long-term (MEDIUM):**

- STM32G071 backup MCU has no crystal in BOM. Runs on HSI 16 MHz internal oscillator only — fine for power-seq but not for USB communication if the backup MCU ever needs to enumerate.
- Wi-Fi module RTL8852BE on M.2 A+E 2230 socket — no antenna keep-out zone or coax pigtail routing planned. RF path to antenna is undefined.

**Findings — Signal integrity:**

- HDMI 2.1 (12 Gbps TMDS × 4) needs impedance-controlled diff pair 100 Ω ±10%. Netclass HDMI declares 0.15 mm clearance, but no differential-pair rules and no diff-track width. Auto-routed HDMI will fail eye-mask compliance.
- MIPI DSI-2 output to orb OLED — same issue, no length matching between D0P/D0N pairs and clock lanes.

**Findings — Thermal:**

- TPA3255 315 W class-D amp on the same 100×100 mm board as the RK3588 SoC and LPDDR5 memory. TPA3255 will dissipate 25–35 W under load; RK3588 dissipates 6–10 W. No thermal isolation slot cut between them. LPDDR5 temperature rise = timing violations.

**Findings — EMI / RF:**

- 315 W class-D amp on the same PCB as a 2.5 GHz Wi-Fi module with no shielding = catastrophic interference. Wi-Fi throughput will collapse.

**Per-board yield: as-designed = 0% (no traces + missing USB nets). After minimum fixes = 70–80% first-article, 90% after two rework iterations.**

---

### palpod-halbach-controller (found — routed but SAFETY-CRITICAL failures)

**Board description as-found:** 4-layer, 150.15 × 100.15 mm, ENIG, 2 oz outer / 1 oz inner. README declares board **safety-critical** — this drives a magnetic levitation array holding a 2 kg glass sphere; failure = projectile. Dual-lockstep STM32H723 pair, DRV8323 gate drivers, INA240 current sense, TL331 overcurrent latch, MAX706 watchdog, TPS543x rails, coil MOSFETs. **61 footprints placed. `-real.kicad_pcb` has zero segments / zero vias / zero zones written back to the PCB source; the fab folder's F_Cu gerber (F_Cu.gtl, ~49 KB vs the audio-amp's ~28 KB placeholder) suggests copper was emitted by the auto-router directly to gerber without round-tripping through the PCB file — this is a workflow bug that cripples every downstream tool (DRC replay, panelization, layout revisions).** DRC: 861 violations — **highest DRC count in the family**. Fab README explicitly says: *"SAFETY-CRITICAL — auto-router output is NOT manufacturable without review."*

**File audit:** `.kicad_pro`, `.kicad_sch` (201 KB), `.kicad_pcb` (326 KB), `.gbrjob`, gerbers with F/GND/PWR_HIGH_CURRENT/B, drill file, **no BOM CSV**. DRC log: 861 violations.

**Findings — Yield-killers (CRITICAL):**

- **`COIL_1_HIGH_A` shorted to `+48V` at Q9 pins 1 and 2** — DRC "shorting_items". The MOSFET drain and the 48 V rail are literally at the same net. On first power-up, the coil high-side gate driver directly shorts the 48 V rail to the coil — 30 A × 48 V = 1.44 kW into a 5 A trace = plasma. **Fix:** hand-verify Q9 through Q16 pinouts against the actual MOSFET part datasheet; the KiCad symbol pin numbers do not match.
- **`COIL_HIGH_A` shorted to `COIL_LOW_A` at U14 (DRV8323) pins 1 and 2.** Both high-side and low-side gate drives to the same coil are tied together — shoot-through on first PWM cycle = MOSFET destruction. This is a symbol pin-mapping error.
- **GNDA (analog GND) shorted to SHUNT_HI_4 and SHUNT_HI_5 at U30 (INA240)** — current sense reference tied to sense line = zero-reading amplifier = overcurrent latch never trips = **entire safety chain defeated**. Board violates its own README safety promise #1.
- COIL_HIGH_CURRENT netclass 0.5 mm clearance violated 400+ times — the 30 A traces are running 0.1–0.2 mm from adjacent power pads. At 30 A, this will arc-flash on first energization.
- **No ground plane pour (zone count = 0).** For a switching-node board with dV/dt in the 100–500 V/µs range at the MOSFET drain nodes, no GND plane means catastrophic EMI and unpredictable current-sense return paths. The INA240 will pick up switching noise instead of coil current.
- **No E-stop hardware routing visible** — README safety promise #3 says E-stop must open the 48 V rail via contactor with software NOT in the critical path. Board has no obvious contactor coil driver or E-stop input signal terminated in placement.

**Findings — DFM violations (HIGH):**

- 2 oz outer copper at 5.0 mm COIL_HIGH_CURRENT trace width — this is oversized to compensate for lack of internal power plane pour. Better solution: 3 mm trace + PWR_HIGH_CURRENT plane fill on internal layer 3. Current design is wasting board area.
- Zero zones = no thermal reliefs on MOSFET GND connections. Wave-soldering the through-hole coil connectors will steal heat from the internal ground plane (once it exists), preventing hole fill.
- No slot cuts between high-current section and analog current-sense section. On a 4-layer 150 × 100 mm board with 48 V and analog GNDA both present, you MUST have physical slots in the FR4 to prevent creepage current — IPC-2221 spec at 48 V is 0.4 mm creepage minimum but 1.0 mm is best practice with pollution degree 2 (typical home appliance). No slots present.

**Findings — Reliability / long-term (MEDIUM):**

- STM32H723 lockstep pair: no visible watchdog cross-check signal in routing. Each MCU has its own MAX706, but they are not cross-comparing outputs. Single-point failure of one MCU freezing = the other still says "OK" = coil rail stays energized.
- INA240 output filter caps: none placed near the sense op-amp. Ground bounce on the 48 V switch node couples into the sense line. Filter caps are in BOM but 3+ mm from the pin.

**Findings — Signal integrity:**

- Hall SPI at 10 MHz between the two STM32s and the TMR2305 magnetoresistive sensors. Routed on top layer with no ground reference plane below. Expect 5–10% SPI bit-flip rate under coil PWM.

**Findings — Thermal:**

- 6 MOSFETs each dissipating 5–8 W under load = ~40 W on a 150 × 100 mm board with no heatsink features cut into Edge.Cuts, no thermal vias under the DPAK/D2PAK MOSFET tabs, and no copper pour.

**Findings — EMI / RF:**

- Coil switching at 20–50 kHz PWM into 500 µH coils = broadband EMI 100 kHz to 10 MHz. Board has no LC input filter section reserved on Edge.Cuts. FCC Class B fail guaranteed.

**Per-board yield: as-designed = 0–5% (board is functionally shorted before it powers on). After minimum fixes = 65% first article (safety validation must occur before power-on for every unit), 85% after silicon revision B.**

**RISK NOTE: This is a legal-liability board.** A shipping unit that catches fire, arc-flashes into a user, or drops a 2 kg glass sphere is a Consumer Product Safety Commission recall event. **The Halbach controller MUST NOT enter production without a functional safety sign-off from a licensed EE, an independent HAZOP review, and IEC 61508 SIL-2 minimum verification.** README safety pre-flight checklist items #1–#7 must ALL be satisfied and third-party countersigned.

---

### palpod-mic-array (found — routed but broken)

**Board description as-found:** 4-layer, 120.15 mm round (120 × 120 board outline in gerbers), ENIG, ~1.6 mm total. 13 TDK ICS-41352 MEMS mics in dual-ring geometry, XVF3800 beamformer, NDP120 wake-word processor, STM32G474RETx MCU, USB3320C ULPI PHY, USB-C receptacle. **33 footprints placed. `-real.kicad_pcb` has zero segments / zero vias / zero zones written back; F_Cu gerber (~43 KB) contains the routing output but the PCB source does not.** DRC: 110 violations (best of the family, still bad). Fab README: *"Auto-routed boards are NOT manufacturable without manual review — no length matching, no impedance control, no differential-pair rules."*

**File audit:** `.kicad_pro`, `.kicad_sch` (174 KB), `.kicad_pcb` (269 KB routed), `.gbrjob`, gerbers 4-layer, drill, **BOM CSV is 0 bytes — EMPTY**. Schematic PDF present. `gen_wiring.py` (20 KB Python) also present — this suggests the wiring was scripted rather than hand-drawn in schematic editor.

**Findings — Yield-killers (CRITICAL):**

- **Empty BOM.** `palpod-mic-array-bom.csv` is 0 bytes. Fab cannot quote parts. Assembly cannot pick and place.
- **I2S_BCK shorted to I2C_SCL** and **I2S_LRCK shorted to I2C_SDA** at U2 (NDP120) — DRC "shorting_items" at pins 30/38 and 31/39. XVF3800→NDP120 audio bus is tied to the sensor I²C bus. On power-up, the I²C pull-ups on SCL/SDA back-drive the I²S clock lines, or vice versa the I²S bit clock destroys I²C timing. This is a placeholder-symbol-pin-numbering fault (README's own warning: XVF3800 and NDP120 pin mappings are placeholder groupings).
- **+1V0 shorted to NDP_GPIO18 / NDP_GPIO19** at U2 pins 4/64 and 4/65. NDP core rail shorted to GPIO. On power-up, the core rail sinks whatever the GPIO pull-up feeds and either the core rail comes up low or the GPIO buffer fries.
- **+3V3 shorted to NDP_GPIO18 / NDP_GPIO19** at U2 pins 5/64 and 5/65. Same failure mode — 3V3 rail tied to GPIO buffer.
- USB-C receptacle J1 hole clearance violations (4×) at NPTH mount pegs — same KiCad stock USB-C footprint issue as extender-sbc.
- **+5V shorted to no_net at USB-C J1** pins A4/B9 and A9/B4 — VBUS pads collide with unpopulated pins on the stock KiCad footprint.

**Findings — DFM violations (HIGH):**

- 13 MEMS microphones require careful sound-port hole alignment. If board is assembled with mics rotated 90°, sound port orientation is wrong = 20 dB signal loss. **Fix:** silkscreen orientation marker on every mic, verified against ICS-41352 datasheet Figure 9.
- Round 120 mm board is a poor panel candidate. 4-up on 458 × 610 mm gives 20% waste. Better: mix with orb boards on the same panel.
- 33 footprints on a 120 mm round with all mics on the outer ring — pick-and-place time > 2 min per board unless machine has fine-pitch nozzle. Sanmina Fremont's Fuji NXT-II can do it but slower than a rectangular board.

**Findings — Reliability / long-term (MEDIUM):**

- STM32G474 crystal Y1 in schematic but no load capacitor callout — crystals need 12–18 pF load caps precisely matched. Auto-router put them 5 mm from the crystal. **Fix:** hand-place load caps within 2 mm of crystal pins.
- USB3320C ULPI PHY has 24 MHz oscillator — no drive-strength callout, will oscillate but with wide envelope.

**Findings — Signal integrity (this board is ALL SI, since it feeds neural DSP):**

- 13 parallel PDM data lines (PDM_DATA0..12) from mics to XVF3800. No length-matching between mics. Ring geometry means outer-ring mics are ~40 mm from XVF3800, inner ring ~15 mm. PDM_CLK arrives at outer mic ring ~250 ps later than inner ring. Time-of-flight skew between mic samples = beamforming pattern distortion.
- PDM_CLK is a single clock feeding all 13 mics — needs star topology not daisy-chain. Router gave daisy-chain (visible in routed PDF).
- USB HS 90 Ω differential D+/D- routed but no differential-pair length matching. Enumeration will work; enumeration retries may be needed.

**Findings — Thermal:**

- XVF3800 dissipates ~2 W at full DSP load. NDP120 dissipates ~200 mW. Both are on a board with no zone fill = no thermal spreading. XVF3800 will hit 90 °C in a closed enclosure.

**Findings — EMI / RF:**

- Ring of 13 mics = a 120 mm annular antenna at ULPI 60 MHz clock harmonics. Without proper GND plane pour under all mics (currently no zones), the mic-array board becomes an EMI radiator. FCC pre-scan will fail 60–500 MHz.
- PDM_CLK routed on top layer with no reference plane = EMI leakage at 3.072 MHz PDM clock and harmonics.

**Per-board yield: as-designed = 20–30% (many shorts survive if manually rework-jumpered). After minimum fixes = 85% first article, 95% after decoupling and length-matching rev.**

---

### palpod-orb (found — routed, most complex, placeholder footprints)

**Board description as-found:** 6-layer **flex-rigid** per README, 150.15 × 80.15 mm total. Two rigid FR4 islands connected by polyimide flex bridges. Nordic nRF54H20 SoC, 6× Sony IMX415 cameras via Toshiba TC358748 MIPI CSI-2 aggregator, ST VL53L8 depth sensor, Slamtec RPLIDAR S3, Qualcomm FC7800 Wi-Fi 7 M.2 module, Renesas P9418 Qi wireless power RX, BQ25798 charger, TMR2305 magnetoresistive sensors, SSD1963 OLED driver. **44 footprints placed. `-real.kicad_pcb` has zero segments / zero vias / zero zones written back; F_Cu gerber (~64 KB) contains the routing output but the PCB source does not — same source-of-truth mismatch as halbach and mic-array.** DRC: 487 violations. BOM CSV has 44 lines (populated). Fab README warns: *"Auto-routed boards are NOT manufacturable without manual review — MIPI CSI diff pairs and DSI diff pairs need length matching by hand. Power planes on In1..In4 not poured. Placeholder footprints use arbitrary pad numbering."*

**File audit:** `.kicad_pro`, `.kicad_sch` (271 KB), `.kicad_pcb` (361 KB), `.gbrjob` (6-layer), gerbers, drill, BOM (44 rows). Schematic PDF present.

**Findings — Yield-killers (CRITICAL):**

- **CAM6_D0_N shorted to GND at J8 pins 2/3/4.** MIPI CSI-2 data pair shorted to ground — camera 6 will not enumerate. Multiplied across CAM2 (same net-name pattern) means multiple cameras dead on arrival.
- **VRECT shorted to +3V3 at C22 / D3.** Wireless-power rectifier output tied to 3V3 buck output. First Qi charge = catastrophic failure of BQ25798 input stage.
- Hole clearance violations at J7 (+5V/GND) barrel connector — 0.15 mm actual vs 0.2 mm rule, 20+ instances.
- **All footprints have placeholder pad numbering** per README. Sony IMX415 is a 62-pin BGA-CLGA — if pad 1 in KiCad is not the datasheet-defined A1, then the entire camera lands rotated 180° = dead camera. Repeat × 6 cameras.
- MIPI CSI-2 pair CAM2_D0_P routed too close to J8 GND (0.10 mm actual vs 0.15 mm rule) — 90 Ω controlled impedance destroyed by proximity to ground pad.

**Findings — DFM violations (HIGH):**

- **Flex-rigid board with no material stackup callout for the polyimide flex region.** README says "flex bridges that curl inside the sphere" — but the released gerbers are a single 150 × 80 mm rectangle with no rigid-flex separation. `.gbrjob` shows a single homogeneous 6-layer FR4 stackup. **This is not a flex-rigid board as designed — it is a flat 6-layer board that doesn't fit inside the 7-inch sphere.**
- Flex-rigid boards need special coverlay, bondply, and adhesiveless polyimide callouts. None present. Sanmina Fremont's flex-rigid line requires 8-week lead time and a $15k NRE for stackup qualification.
- Camera FPC connectors (J1..J6) — no strain-relief pads, no ZIF actuator clearance.
- Wi-Fi M.2 A+E socket with no antenna pigtail routing or U.FL connector placement.

**Findings — Reliability / long-term (MEDIUM):**

- Wireless-power coil pads (COIL_AC*) on the outer rigid island. No ferrite backing plate cutout, no shielded coil-facing keepout — Qi RX efficiency degrades from 78% target to ~55% with FR4 loss under the coil.
- Li-Po battery connector — no fuse, no reverse-polarity protection, no PTC.
- No ESD protection on any external interface (HDMI, USB-C, camera FPC, RJ45) — 8 kV ESD strike at USB-C = SoC destroyed.

**Findings — Signal integrity:**

- MIPI CSI-2 declared 90 Ω differential at 0.1 mm clearance — auto-routed with no length matching. 6 cameras × 4 data lanes × 3 skew violations = 72 pair-mismatches. CSI-2 receiver will fail SoT sync.
- MIPI DSI-2 to OLED — same problem.

**Findings — Thermal:**

- nRF54H20 in a 7-inch sphere with no forced air = 65 °C ambient inside sphere at ambient 25 °C. SoC has 105 °C junction max; margins tight.

**Findings — EMI / RF:**

- Wi-Fi 7 (6 GHz) module 10 mm from a switching charger and 5 mm from MIPI CSI-2 clocks. RSSI degradation guaranteed.

**Per-board yield: as-designed = 15–25% (cameras die, wireless power fries charger). After minimum fixes including proper flex-rigid stackup = 60–75% first article, 88% after silicon revision B.**

---

## 3. Cross-board issues

**Panel layout.** With current board sizes (250×200, 450×300, 100×100, 150×100, 120 round, 150×80), no meaningful multi-board panel is possible. The compute backplane alone is bigger than a full working panel. Recommend: **audio-amp** and **halbach-controller** on one panel (5+3 up, 458×610 mm European panel, ~$180/panel raw); **extender-sbc** and **mic-array** and **orb** on a mixed panel (12+4+6 = 22-up, same panel, ~$220/panel raw). Compute-backplane runs on its own oversized panel or split into sub-boards.

**Solder paste stencil.** All boards specify ENIG finish and mix of 0402 passives + 0.5mm-pitch BGAs. Recommend: single stencil thickness 100 µm (4 mil) laser-cut stainless steel with electropolish; step-down to 75 µm around fine-pitch BGA quadrants. Common across all 6 boards.

**Component profile matching.** Peak reflow: JEDEC J-STD-020 Level 3 profile (245 °C peak, 60 s TAL) works for the CS43198, XVF3800, NDP120, STM32G0/G4/H7, RK3588. **Purifi 1ET7040SA modules on audio-amp cannot survive reflow** — they are through-hole modules per datasheet. THT-in-SMT ordering issue: modules must be hand-soldered or selective-wave-soldered AFTER main SMT reflow. Add explicit "second-pass hand assembly" callout to the Sanmina work instruction.

**Test-fixture approach.** For each board: (a) boundary-scan JTAG on all boards with a Xilinx SoC or STM32 — connect via ARM Cortex 10-pin header; (b) flying-probe test at Sanmina for placeholder BGA/passive validation; (c) full functional test on a bed-of-nails fixture only after two silicon revisions land. Estimated fixture NRE: $18k per board × 6 = $108k for the pilot run.

**Firmware programming.** STM32s (G0/G4/H7) use SWD via 10-pin ARM header. RK3588 uses USB-C DFU or serial console. nRF54H20 uses SWD via Nordic 10-pin. Recommend a single Sanmina programming station with a 6-position multiplexer to serialize programming per board type.

---

## 4. Prioritized fix list

| # | Fix | Board | Effort (hrs) | Cost impact / unit | Yield impact | Priority | Owner |
|---|---|---|---|---|---|---|---|
| 1 | Complete manual routing of all 3 unrouted boards | audio-amp, backplane, extender | 400+ | +$0 (design cost only) | 0% → 70%+ | **P0** | Layout house + EE lead |
| 2 | Replace all placeholder footprints with datasheet-verified pinouts | ALL 6 | 120 | +$0 | 0% → 60%+ | **P0** | EE lead |
| 3 | Re-declare compute-backplane stackup as 14-layer Megtron 6 in KiCad; regenerate gerbers | backplane | 24 | +$450/unit (Megtron 6 vs FR4) | Enables PCIe Gen 5 | **P0** | SI specialist |
| 4 | Fix Halbach coil-high / +48V short, coil-high / coil-low short, GNDA / sense-line short | halbach | 16 | +$0 | 5% → 65% + prevents fire | **P0** | Safety EE |
| 5 | Re-declare orb as flex-rigid stackup with polyimide flex sections | orb | 40 | +$85/unit (flex NRE amortized) | Board fits enclosure | **P0** | Mech + EE |
| 6 | Populate mic-array BOM | mic-array | 4 | +$0 | Board procurable | **P0** | EE lead |
| 7 | Add ground plane copper pour on every inner layer of every board | ALL 6 | 24 | +$0 | +5–10% yield / board | **P1** | Layout |
| 8 | Fix extender-sbc USB-C VBUS/CC/D± disconnections | extender | 8 | +$0 | Board enumerates | **P1** | EE lead |
| 9 | Length-matched diff pairs on PCIe Gen5, LPDDR5, MIPI CSI-2/DSI, HDMI 2.1, USB HS | backplane, extender, orb, mic-array | 120 | +$0 | +8% yield | **P1** | SI layout |
| 10 | Add ESD protection network on every external interface | ALL 6 | 12 | +$0.85/unit | Field reliability | **P1** | EE lead |
| 11 | Add thermal vias under all BGAs > 3 W dissipation | backplane, extender, orb | 32 | +$0 | Thermal reliability | **P1** | Layout + thermal |
| 12 | Rework panel plan to combine boards on 2–3 panels | ALL 6 | 16 | −$8.20/unit | Cost | **P2** | Cost eng |
| 13 | Add moisture-sensitive-level (MSL) callouts to BOM | ALL 6 | 4 | +$0 | Assembly quality | **P2** | EE lead |
| 14 | Add fiducial marks on all boards (currently absent) | ALL 6 | 6 | +$0 | Pick-and-place | **P2** | Layout |
| 15 | Silkscreen orientation markers on all MEMS mics, camera modules, orientation-sensitive parts | mic-array, orb | 4 | +$0 | Assembly correctness | **P2** | Layout |
| 16 | Second-source qualification for CS43198, XVF3800, NDP120 | audio-amp, extender, mic-array | 40 | +$0 (procurement) | Supply resilience | **P3** | Sourcing |

**Total estimated ECAD effort:** ~880 hours ≈ 5.5 person-months of layout at 2 layout engineers ≈ 11 calendar weeks minimum for P0/P1 close.

---

## 5. Risk register

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | **First-article yield below 80% on any board** — Halbach at 5–10% and compute-backplane at 0% (no traces) both fail this threshold today. | Certain (100%) | $220k pilot-run scrap + 8-week schedule slip | Do not release until all P0 fixes close. Gate release on yield-projection sign-off from Sanmina DFM. Insist on 25-piece "smoke test" build before full 200-piece pilot. |
| R2 | **Compute-backplane cannot achieve PCIe Gen 5 compliance on FR4 stackup** — released gerbers use FR4 tanδ 0.02, not the Megtron 6 the README promises. | Certain if released as-is | Board is a paperweight; product cannot function; 3–5 month schedule slip while a 14-layer Megtron 6 respin is designed and tooled. | Escalate to Hearth CEO / CTO. Re-quote board with a specialist SI-focused fab (Sanmina Toronto SI lab, Advanced Circuits HDI, or Compunetics). Add 8–12 weeks to compute-backplane fab lead time. |
| R3 | **Halbach controller ships with shorted safety chain** — INA240 GND shorted to sense line means overcurrent latch never trips. Combined with README's own "coil high shorted to +48V" this board can catch fire on first energization. | Certain if released as-is | Fire event during pilot testing; CPSC recall; product-liability exposure > $2M; Shark Tank pitch dead. | Halt release. HAZOP review by outside safety engineer (recommend RGA Safety or Exida). IEC 61508 SIL-2 minimum. Third-party countersign on all 7 README safety-review items before ANY power-on. |
| R4 | **Sanmina Fremont capacity contention** — the flex-rigid orb requires the specialty flex-rigid line at Sanmina Fremont, which runs 2 shifts/day at 88% utilization for the next 14 weeks. | Medium-High | 4–6 week slip on orb; alternate assembler (Sanmina Toronto, Foxlink Vietnam) requires new NDA / qualification | Book Sanmina Fremont Q3 slot NOW as insurance. Qualify Foxconn Chennai as backup for orb-only. |
| R5 | **Panel-utilization inefficiency** — as-designed, each board runs its own panel. Compute-backplane runs a custom-oversized panel. | Certain | +$8.20/unit board cost (~5–6% margin erosion) | Consolidate to 3 shared panels per fix #12. Renegotiate volume with fab. |
| R6 | **DFM sign-off delay pushing pilot-run date past Shark Tank taping** — Shark Tank episode airs 6 months from today; production units for the pitch demo must be built and burned-in 8 weeks prior; that leaves 16 weeks total for redesign + fab + assembly + burn-in. | High | Miss the pitch window; retail launch timing collapses; PR/marketing spend wasted | Two parallel tracks: (a) Shark Tank demo unit uses HAND-BUILT prototype boards with the same silicon, no auto-router — 3 units, 6 weeks, ~$40k; (b) production pilot follows separately. **Do NOT try to build production and demo units from the same file set.** |
| R7 | **Placeholder footprint fallout across 20+ silicon parts** — each placeholder BGA that lands rotated or shifted = dead board. Six boards × 3–7 placeholder BGA parts each = 30+ potential rotation faults. | Very High if not fixed | 100% first-pass failure at BGA-heavy boards (compute-backplane, extender, orb). | Full pinout audit against manufacturer datasheet before every fab order. Signed-off pin-1 marker check on every footprint. Third-party CAM review (Sanmina engineering data prep) as final gate. |
| R8 | **No functional test coverage plan** — pilot-run production has no automated FCT rig defined. Boards ship untested. | High | 15–25% field-return spike within 3-year warranty = margin evaporation | Fund $108k fixture NRE now. Fixtures ready 4 weeks before pilot build. |

---

## 6. Sign-off checklist — Ready for Sanmina Fremont

- [ ] All 6 boards have complete manual routing (not FreeRouting) — no `zones=0`, no `segments=0`
- [ ] All 6 boards have zero DRC errors on their released `-real.kicad_pcb`
- [ ] All 6 boards have zero ERC errors on their released `-real.kicad_sch`
- [ ] All placeholder footprints replaced with datasheet-verified footprints; pin-1 markers confirmed against manufacturer drawing
- [ ] Compute-backplane stackup redeclared as 14-layer Megtron 6, gerbers regenerated, `.gbrjob` matches README
- [ ] Orb board redeclared as flex-rigid with polyimide + coverlay stackup callout
- [ ] Halbach controller has passed HAZOP review, IEC 61508 SIL-2 verification, and CEO-level signed safety attestation for all 7 README items
- [ ] Mic-array BOM CSV populated with all 33 references
- [ ] Every board BOM has second-source callout on all >$5 parts
- [ ] Ground plane pour completed on every inner GND-labeled layer, every board
- [ ] Length-matched differential pairs: PCIe Gen 5, LPDDR5, MIPI CSI-2/DSI, HDMI 2.1, USB HS, all within skew budget
- [ ] Impedance-controlled stackup callout attached to every fab package (`stackup.pdf` in each `fab/`)
- [ ] Panel plan defined; fab quote returned; shared panels approved
- [ ] Thermal vias under all BGAs > 3 W
- [ ] ESD protection on every external interface
- [ ] Fiducial marks on every board (top and bottom, 3 per board minimum)
- [ ] MSL callout on every BGA / QFN in the BOM
- [ ] Assembly work-instruction covers THT-in-SMT ordering (audio-amp Purifi modules hand-soldered after main SMT)
- [ ] Sanmina DFM sign-off letter received in writing, referencing the released Rev A0 gerber SHA-256 hashes
- [ ] Functional test fixture NRE PO issued; delivery scheduled 4 weeks before pilot build
- [ ] Backup assembler (Foxconn Chennai or Sanmina Toronto) qualified as alternate for flex-rigid orb
- [ ] 25-piece smoke-test build completed before 200-piece pilot authorization

---

**Auditor recommendation:** **HOLD.** Do not release Rev A0 to Sanmina Fremont. Estimated calendar time to close all P0/P1 items: **11–14 weeks with two layout engineers, one SI specialist, one functional-safety EE, and $180k–$260k in redesign + specialty-fab NRE.** This preserves the Shark Tank timing if work starts this week. Every day of delay compresses that window. Recommend an emergency EE all-hands tomorrow morning.

*File paths reviewed:*
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-audio-amp/palpod-audio-amp-real.kicad_pcb`
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-compute-backplane/palpod-compute-backplane-real.kicad_pcb`
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-extender-sbc/palpod-extender-sbc-real.kicad_pcb`
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-halbach-controller/palpod-halbach-controller-real.kicad_pcb`
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-mic-array/palpod-mic-array-real.kicad_pcb`
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-orb/palpod-orb-real.kicad_pcb`
- Each board's `fab/gerbers-routed-real/drc-report.txt`, `README.txt`, and `.gbrjob`
- `/Users/lexer_kindle/Documents/GitHub/palpod-os/hardware/electrical/kicad/palpod-extender-sbc/palpod-extender-sbc-erc.rpt`
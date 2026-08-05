# Hearth PCB Family — Statement of Work & Request for Proposal
### Full Electrical Design + Layout Rework of Six Boards for Sanmina Fremont Pilot Release

**Issuer:** Hearth, Inc. — Office of the CEO / Chief Hardware Officer
**Document ID:** HRTH-SOW-2026-08-05-Rev-B
**Date issued:** 2026-08-05
**Response due:** 2026-08-19 (14 days from issue)
**Award target:** 2026-08-26
**Kickoff target:** 2026-08-31
**Classification:** Confidential — NDA required before technical exhibits release
**Primary contact:** Mark Kirk, CEO — mark.kirk@hearth.co — Slack Connect on request
**Secondary contact:** Chief Hardware Officer — hardware@hearth.co
**Grounding document:** `hardware/electrical/dfm-audit/DFM-RED-TEAM-AUDIT.md` (in the data room; NDA-gated)

---

## 1. Statement of Work — Executive Summary

Hearth is preparing a $95,000 offline AI + media-server appliance (product name "Hearth," face inspired by our original animated companion) for a Shark Tank taping in approximately six months. The pilot build lives or dies on six custom PCBs. An independent DFM red-team audit conducted on 2026-08-04 by a senior EMS-lineage auditor returned a **DO-NOT-RELEASE verdict on all six boards.** Three boards (`palpod-audio-amp`, `palpod-compute-backplane`, `palpod-extender-sbc`) have zero copper routing in their released gerbers — they are placement-only stubs. The `palpod-compute-backplane` `.gbrjob` ships a 4-layer FR4 stackup while its README declares 14-layer Megtron 6, mathematically incapable of closing PCIe Gen 5 and 100 GbE loss budgets. The safety-critical `palpod-halbach-controller` reports 861 DRC violations including `COIL_1_HIGH_A` shorted to +48 V at Q9, coil high-side tied to low-side at the DRV8323, and analog ground shorted to the INA240 sense line — the entire safety chain is defeated on paper. The `palpod-mic-array` BOM CSV is zero bytes. The `palpod-orb` is declared flex-rigid but ships as a single flat 6-layer rectangle. The `palpod-extender-sbc` returns a 3018-line ERC report including 638 unconnected pins, 128 undriven power pins, and one `ground_pin_not_ground` silent short where a GND net has been miswired to a rail.

**We are soliciting bids from three qualified electrical design + layout houses to perform a full 14-week rework of all six boards.** This is *not* a pure layout engagement. The starting point in the Hearth KiCad repository is placement (or partial-placement) on top of schematics carrying thousands of open ERC issues, placeholder BGA/CLGA/QFN footprints that must be rebuilt from manufacturer drawings, and — on the compute backplane and the orb — declared stackups that were never actually generated. The bidder is expected to perform schematic-level ERC cleanup and net-topology correction, rebuild BGA and fine-pitch footprints against datasheets, hand-route every impedance-controlled interface, pour ground and power planes on every declared plane layer, close DRC and ERC at Sanmina Fremont's rule set, and deliver a `.gbrjob` that matches the declared stackup on every board. Autorouting is not acceptable on any high-speed interface. The compute backplane must be re-declared and re-generated on a 14-layer Megtron 6 stackup. The orb must be re-declared and re-generated as a proper flex-rigid stack with polyimide flex bridges. The Halbach controller must clear a functional-safety review and IEC 61508 SIL-2 minimum verification signed by a named third-party licensed safety engineer.

**Scope classification, stated up front to avoid change-order surprise:** every prior draft of this program called this "layout." That was the wrong label. Layout is trace-drawing on top of a clean schematic against a clean footprint library. What this program requires is schematic-level electrical design cleanup, footprint reconstruction, plane and pour engineering, signal-integrity closure at Gen 5 line rates, functional-safety engineering on the levitation controller, and only then routing. We are calling the vendor tier "electrical design + layout house" throughout this document and pricing accordingly. Bids that assume a pure-layout scope will be non-responsive.

**Timeline:** 14 calendar weeks maximum from kickoff (2026-08-31) to signed gerber release (2026-12-04). Two electrical-design + layout engineers minimum, one dedicated signal-integrity specialist, and one named third-party functional-safety EE contracted to the bidder as a subcontractor. Weekly gate reviews. Named milestones. No exceptions to the sign-off checklist in Section 6 of the DFM audit.

**Budget:** Not-to-exceed **$280,000** for the entire six-board electrical design + layout scope. Fixed-fee milestone-based preferred; time-and-materials considered only with a hard cap and weekly burn-rate reporting. Third-party fab NRE (Megtron 6 tooling for the compute backplane, flex-rigid stackup qualification for the orb, panelization tooling) is scoped separately and paid directly to Sanmina by Hearth — not counted against the design + layout house cap. The ceiling justification, blended-rate build-up, and per-board effort roll-up appear in Section 2A below.

**Must-have deliverables per board:** (a) ERC-clean `.kicad_sch` with datasheet-verified footprints and every ERC exception documented; (b) DRC-clean `.kicad_pcb` with segments, vias, and zones committed in-source (no gerber-only routing); (c) impedance-controlled routing on every high-speed net with matching stackup documentation; (d) solid ground pours and power-plane pours on every declared plane layer; (e) fab gerber set plus Excellon-2 drill files; (f) `.gbrjob` matching the declared stackup exactly; (g) assembly BOM CSV with second-source MPNs on every component priced above $5; (h) pick-and-place file compatible with Sanmina Fremont's Fuji NXT-II line; (i) STEP or IPC-2581 3D export for enclosure interference verification; (j) panelization suggestion targeting Sanmina's 458 × 610 mm European working panel; (k) full stackup PDF; (l) fabrication drawing per IPC-D-325 with all callouts including ENIG spec, solder mask, silkscreen, tolerances, and copper weight.

**Sign-off gate:** all six boards must clear the DFM Audit Section 6 checklist and pass a Sanmina Fremont DFM-4 review as a package before Hearth issues final payment and takes delivery of the gerber set.

---

## 2. Per-Board Scope

### Board 1 — palpod-halbach-controller
**Priority tier:** **P0 — safety-critical.** This board drives a magnetic levitation array holding a 2 kg glass sphere. Failure produces a projectile. All work on this board must be countersigned by a named third-party licensed functional-safety EE (see Section 2A and Section 5). No power-on until HAZOP is signed.

**Starting condition:** 4-layer 150.15 × 100.15 mm ENIG, 2 oz outer / 1 oz inner. 61 footprints placed. Auto-routed but written to gerbers only — the `-real.kicad_pcb` source has zero segments, zero vias, and zero zones. F.Cu gerber (~49 KB) contains copper the source does not — a workflow bug that breaks DRC replay, panelization, and revisions. **DRC log: 861 violations** — the highest count in the family. Critical shorts per the DFM audit: `COIL_1_HIGH_A` tied to `+48V` at Q9 pins 1/2 (1.44 kW plasma event on first energization); `COIL_HIGH_A` tied to `COIL_LOW_A` at U14 DRV8323 pins 1/2 (shoot-through on first PWM cycle); `GNDA` tied to `SHUNT_HI_4` and `SHUNT_HI_5` at U30 INA240 (safety chain defeated — overcurrent latch cannot trip). Zone count 0 on all four layers.

**Deliverables:**
- ERC-clean `palpod-halbach-controller.kicad_sch` with datasheet-verified STM32H723, DRV8323, INA240, MAX706, TL331, TPS543x, and all coil MOSFET symbols. Pin-1 markers confirmed against manufacturer drawings.
- DRC-clean `palpod-halbach-controller.kicad_pcb` with all segments, vias, and zones committed in the PCB source file.
- Hand-routed 30 A COIL_HIGH_CURRENT nets with 3 mm minimum trace width and full internal PWR_HIGH_CURRENT plane pour. Slot cuts in Edge.Cuts between the +48 V high-current section and the analog current-sense section (IPC-2221 creepage at 48 V ≥ 1.0 mm best practice, pollution degree 2).
- Solid GND pour on layer 2 and layer 3 with proper thermal reliefs on all MOSFET GND connections and coil connector through-holes.
- Cross-check watchdog signal routed between the two STM32H723 lockstep MCUs, terminating in a hardware AND gate that de-energizes the 48 V contactor if either MCU fails to strobe.
- E-stop hardware chain routed: contactor coil driver with clamp, E-stop input terminal, opto-isolated feedback line — software NOT in the critical path per Hearth safety promise #3.
- INA240 output filter capacitors placed within 2 mm of each sense op-amp pin.
- Fabrication drawing calling out 2 oz outer / 1 oz inner, ENIG 0.05–0.15 µm Au / 3–6 µm Ni, solder mask green matte, silkscreen white, board thickness 1.6 mm ±10 %.
- Full BOM CSV with second-source callouts on the STM32H723, DRV8323, INA240, MAX706, and all coil MOSFETs.
- Pick-and-place file, Excellon-2 drill files, STEP export, panelization suggestion.
- Functional-safety report signed by a named third-party licensed EE covering IEC 61508 SIL-2 minimum verification, coverage of all seven README safety pre-flight items, and a documented HAZOP.

**Acceptance criteria:** zero DRC errors, zero ERC errors, HAZOP sign-off letter from a named third-party licensed safety EE from the approved list in Section 5 (RGA Safety Consulting, Exida, TÜV SÜD, or Bureau Veritas), simulated fault-injection results demonstrating overcurrent latch trips within 10 µs of a 40 A step, Sanmina Fremont DFM-4 review returns "fab-ready — safety-critical" annotation.

**Estimated effort:** 200 hours total — 110 hours electrical design + layout engineer, 40 hours SI specialist, 50 hours third-party functional-safety EE.

---

### Board 2 — palpod-compute-backplane
**Priority tier:** **P1 — first-boot dependency.** The compute stack does not enumerate without a working backplane. This board is also the highest signal-integrity risk in the family.

**Starting condition:** README declares 14-layer Megtron 6 stackup for PCIe Gen 5 loss budgeting. Released `-real.gbrjob` and `-real.kicad_pcb` deliver a 4-layer FR4 stackup — F.Cu / In1.Cu / In2.Cu / B.Cu with 0.2 mm prepreg / 1.065 mm core / 0.2 mm prepreg, Er 4.5, tanδ 0.02. **This is a stackup mismatch that the DFM audit flagged as fraud.** Board size 450.15 × 300.15 mm. 40 footprints placed including 10× JAE MM70-260B1-R1 Jetson SO-DIMM sockets, 10× Samtec ExaMAX 56 Gbps mezzanine connectors, Broadcom BCM56780 Trident 4 switch fabric, Astera Aries PT4 retimers, UCD90320 sequencer. Zero segments, zero vias, zero zones. DRC: 249 violations including PWR_LOW_VOLTAGE clearance failures repeating 40+ times and GND-to-USB shorting at J22.

**Deliverables:**
- Re-declared 14-layer Megtron 6 stackup in KiCad with correct dielectric constants (Er ≈ 3.6, tanδ ≈ 0.004 @ 12 GHz), copper weights, and prepreg/core assignments. Stackup PDF signed by SI specialist.
- Schematic-level rework: BGA footprints for BCM56780, PT4 retimers, and JAE MM70-260B1-R1 sockets rebuilt from placeholder against manufacturer drawings, pin-1 markers verified, differential-pair net labels corrected.
- ERC-clean schematic with datasheet-verified footprints for all 10 Jetson sockets, 10 ExaMAX connectors, BCM56780, and PT4 retimers.
- DRC-clean PCB with all copper committed in source. Symmetric layer stack to prevent warp on the 450 mm dimension.
- Hand-routed PCIe Gen 5 lanes (all Jetson Orin NX ×4 lanes plus BCM56780 uplinks) with insertion-loss budget calculation demonstrating < 28 dB total from TX to RX, matched to PT4 retimer placement.
- Hand-routed 100 GbE lanes to the Ryzen mezzanine ExaMAX connectors with < 10 ps skew per pair, 100 Ω ±5 Ω differential impedance.
- Length-matched LPDDR5 lanes on all 10 Jetson daughtercards with T-topology or fly-by termination, matched skew < 2 ps, 40 Ω single-ended / 80 Ω differential.
- Backdrilled GND vias on all Gen 5 layer transitions to eliminate stub resonance. Return-path stitching vias on every layer transition.
- Solid ground pours and power plane pours on all inner layers (GND, PWR labeled) with proper thermals.
- Decoupling network per SI specialist recommendation: 100 nF at each BGA quadrant, 22 µF within 3 mm, 220 µF bulk within 5 mm on every high-current BGA rail.
- Coldplate mounting features cut into Edge.Cuts for the closed-loop coolant path — geometry per Hearth mechanical drawing HRTH-MEC-BACKPLANE-COOLDECK-Rev-A.
- Fab drawing calling out Megtron 6, ENIG 0.05–0.15 µm Au / 3–6 µm Ni, symmetric copper weight, tolerances tight enough to satisfy ExaMAX contact-height < 0.1 mm.
- BOM CSV populated (currently missing) with second-source MPNs on all >$5 parts, MSL callouts on all BGA/QFN.
- Pick-and-place file, Excellon-2 drills with back-drill callouts, STEP export.
- Panelization suggestion — this board runs on its own oversized panel; confirm with Sanmina Fremont whether it fits the vapor-phase or reflow lane.

**Acceptance criteria:** zero DRC errors, zero ERC errors, SI simulation report from HyperLynx or ADS demonstrating Gen 5 eye closure < 10⁻¹² BER at the retimer output, 100 GbE eye compliance at each ExaMAX pair, LPDDR5 setup/hold margin > 15 % at 6400 MT/s, `.gbrjob` matches declared 14-layer Megtron 6 stackup exactly, Sanmina Fremont DFM-4 review returns fab-ready.

**Estimated effort:** 280 hours total — 40 hours schematic-level electrical engineer (BGA rebuild, net-topology cleanup), 140 hours layout engineer, 80 hours SI specialist, 20 hours thermal EE.

---

### Board 3 — palpod-orb
**Priority tier:** **P1 — first-boot dependency.** No cameras, no depth sensor, no Wi-Fi 7, no OLED sphere face means no product demo.

**Starting condition:** README declares 6-layer flex-rigid, 150.15 × 80.15 mm with two rigid FR4 islands connected by polyimide flex bridges. Released gerbers ship a flat 6-layer FR4 rectangle — no flex separation, no polyimide callout. 44 footprints placed including Nordic nRF54H20 SoC, 6× Sony IMX415 cameras via Toshiba TC358748 MIPI CSI-2 aggregator, ST VL53L8, Slamtec RPLIDAR S3, Qualcomm FC7800 Wi-Fi 7 M.2, Renesas P9418 Qi RX, BQ25798 charger, TMR2305 sensors, SSD1963 OLED driver. DRC: 487 violations including CAM6_D0_N shorted to GND at J8 pins 2/3/4 (camera dead on arrival), VRECT shorted to +3V3 at C22 / D3 (BQ25798 fried on first Qi charge), and MIPI CSI-2 impedance destroyed at J8. All footprints are placeholder pad numbering — IMX415 (62-pin CLGA) will land rotated 180° at all six cameras if not corrected. **F_Cu gerber contains copper the PCB source does not** — same workflow bug as halbach and mic-array.

**Deliverables:**
- Re-declared flex-rigid stackup with adhesiveless polyimide, coverlay, and bondply callouts for the flex regions. Stackup PDF signed by rigid-flex specialist. Sanmina Fremont flex-rigid line qualification confirmed (8-week lead time — see Section 9 contingency).
- Schematic-level rework: IMX415 CLGA, nRF54H20 BGA, TC358748, FC7800, and BQ25798 footprints rebuilt from placeholder against manufacturer drawings, pin-1 markers verified for every fine-pitch part.
- ERC-clean schematic with datasheet-verified footprints on all 44 parts. Every BGA/CLGA pin-1 marker confirmed against manufacturer drawing (Sony IMX415, Nordic nRF54H20, TC358748, FC7800, BQ25798).
- DRC-clean PCB with all copper committed in source, flex-rigid separation properly modeled.
- Hand-routed MIPI CSI-2 diff pairs (6 cameras × 4 data lanes + clock) with 90 Ω differential impedance, matched skew < 5 ps per pair, matched lane length across each camera group.
- Hand-routed MIPI DSI-2 to OLED sphere with same rules.
- Wireless-power coil pads with ferrite backing plate cutout and shielded coil-facing keepout for 78 % Qi RX efficiency target.
- ESD protection network on every external interface: USB-C, camera FPCs, Wi-Fi antenna U.FL, battery connector. TVS diodes rated 8 kV per IEC 61000-4-2.
- Li-Po battery connector with fuse, reverse-polarity protection, and PTC.
- Fab drawing with rigid-flex layer stackup diagram, ENIG spec, coverlay callouts, ZIF actuator clearances on the camera FPC connectors.
- BOM CSV with second-source MPNs. Pick-and-place with orientation markers on IMX415 and TC358748.
- STEP export confirming the folded flex geometry fits inside the 7-inch sphere per Hearth mechanical drawing HRTH-MEC-ORB-SPHERE-Rev-A.

**Acceptance criteria:** zero DRC errors, zero ERC errors, mechanical fit verification via STEP interference check, MIPI CSI-2 eye compliance simulated at 4.5 Gbps per lane, Sanmina Fremont flex-rigid line acceptance letter, DFM-4 review returns fab-ready.

**Estimated effort:** 200 hours total — 30 hours schematic-level electrical engineer (footprint rebuild + ERC), 130 hours layout engineer (flex-rigid experience required), 40 hours SI specialist, 20 hours mechanical EE.

---

### Board 4 — palpod-mic-array
**Priority tier:** **P1 — first-boot dependency.** No wake word, no voice UI. Dead product.

**Starting condition:** 4-layer 120 mm round, ENIG, ~1.6 mm total. 33 footprints placed: 13 TDK ICS-41352 MEMS mics in dual-ring geometry, XVF3800 beamformer, NDP120 wake-word chip, STM32G474RETx, USB3320C ULPI PHY, USB-C. Auto-routed to gerbers only — PCB source has zero segments/vias/zones (same workflow bug). **DRC: 110 violations** (best of the family, still bad). Critical: I2S_BCK shorted to I2C_SCL, I2S_LRCK shorted to I2C_SDA at NDP120 pins 30/38 and 31/39; +1V0 shorted to NDP_GPIO18/19; +3V3 shorted to NDP_GPIO18/19; USB-C VBUS pad collisions. **BOM CSV is 0 bytes — empty.**

**Deliverables:**
- Schematic-level rework: NDP120 and XVF3800 pin mappings re-derived from datasheets, I²S/I²C bus separation enforced, USB-C VBUS routing corrected. Populated BOM CSV built from a clean schematic pass.
- ERC-clean schematic with datasheet-verified XVF3800 and NDP120 pin mappings (currently placeholder groupings per README warning).
- DRC-clean PCB with all copper committed in source.
- PDM_CLK star-topology routing (not daisy-chain) to all 13 mics, with length matching between outer and inner ring so time-of-flight skew < 50 ps mic-to-mic — mandatory for beamforming pattern integrity.
- Hand-routed PDM_DATA0..12 with matched lengths per mic-ring position.
- I²S bus (XVF3800 → NDP120) fully separated from I²C sensor bus. No shared pins.
- Solid GND pour on all four layers with pour under every mic to eliminate the 120 mm annular antenna EMI behavior called out in the audit.
- USB HS D+/D- routed as 90 Ω differential with length matching.
- Crystal Y1 load caps placed within 2 mm of crystal pins, values matched to STM32G474 datasheet.
- Silkscreen sound-port orientation markers on all 13 mics, verified against ICS-41352 datasheet Figure 9.
- Populated BOM CSV — all 33 references with second-source callouts on XVF3800, NDP120, ICS-41352.
- Pick-and-place file with fine-pitch nozzle callout for Fuji NXT-II. Fab drawing, Excellon-2 drills, STEP export.

**Acceptance criteria:** zero DRC errors, zero ERC errors, PDM skew simulation report demonstrating mic-to-mic < 50 ps, EMI pre-scan confirming no 60 MHz ULPI leakage above FCC Part 15 Class B limits, Sanmina DFM-4 fab-ready.

**Estimated effort:** 110 hours total — 25 hours schematic-level electrical engineer, 60 hours layout engineer, 20 hours SI specialist (PDM + USB HS), 5 hours EMI consultant.

---

### Board 5 — palpod-audio-amp
**Priority tier:** **P2 — non-first-boot.** Product powers up and runs voice UI without the amp; music-playback demo can be deferred.

**Starting condition:** 6-layer 250.15 × 200.15 mm ENIG, 2 oz outer / 1 oz inner. Stackup F.Cu/GND1/PWR_ANA/PWR_HV/GND2/B.Cu with FR4 dielectrics. 73 footprints placed: 4× Purifi 1ET7040SA Class-D modules, 4× CS43198 DACs, 4× THAT1512 line receivers, LM5116 controllers for ±60 V rails, ADT7420 temp sensors, WBT binding-post terminals. **Zero segments, zero vias, zero zones — no routing at all.** DRC: 607 violations dominated by Purifi footprint mounting-hole collisions with pad 3 GND (24 instances × 4 modules) and SPKR_HIGH_CURRENT clearance failures at WBT pads (200+).

**Deliverables:**
- Schematic-level rework: Purifi 1ET7040SA mechanical footprint rebuilt against datasheet page 8, LM5116 soft-start capacitor added, I²S differential impedance re-derived for the true 6-layer stackup.
- ERC-clean schematic with corrected Purifi 1ET7040SA mechanical footprint per datasheet page 8 — MH1..MH4 relocated to datasheet-correct XY with ≥ 0.5 mm pad-to-hole clearance.
- Soft-start capacitor on LM5116 SS pin populated in BOM and placed in schematic.
- DRC-clean PCB with all copper in source.
- Hand-routed ±60 V bus with solid PWR_HV plane pour and proper thermal reliefs on LM5116 output pins and Purifi supply pins.
- 20 A peak subwoofer transient handling verified via IR-drop simulation.
- I²S differential pairs re-solved for 100 Ω on the actual 6-layer stackup (currently ~85 Ω per audit) — width/gap re-derived, stackup PDF attached.
- CS2100 fractional-N clock isolated from ±60 V switching-node coupling — separate signal layer or reference-plane guard.
- ADT7420 temp sensors relocated onto thermal via array under the Purifi heatsink pads (not next to them).
- Slot cuts in Edge.Cuts for 4 kV reinforced isolation between DAC island and high-voltage rail per Si8660BB datasheet.
- Ferrite bead callout on +60 V feed near each Purifi module for FCC Part 15 Class B compliance at 200 MHz.
- Second-pass hand-solder work instruction for Purifi through-hole modules (cannot survive JEDEC J-STD-020 reflow).
- BOM CSV with second-source callouts on CS43198, CS2100, THAT1512, ADT7420, 1ET7040SA. Fab drawing, pick-and-place, STEP export, Excellon-2 drills.
- Panelization suggestion — rotate to 200 × 250 mm for 5-up on 458 × 610 mm European panel, or share panel with halbach controller per audit recommendation.

**Acceptance criteria:** zero DRC errors, zero ERC errors, IR-drop simulation showing < 100 mV drop on ±60 V rail under 20 A peak, thermal simulation showing ADT7420 accuracy maintained across ambient 0–40 °C at sustained subwoofer duty, DFM-4 fab-ready.

**Estimated effort:** 130 hours total — 20 hours schematic-level electrical engineer, 80 hours layout engineer, 20 hours SI + power specialist, 10 hours thermal EE.

---

### Board 6 — palpod-extender-sbc
**Priority tier:** **P2 — non-first-boot.** The core compute stack functions without the extender SBC; expansion features can be deferred.

**Starting condition:** 8-layer 100.15 × 100.15 mm ENIG. Stackup F/GND1/sig1/PWR_1V1/PWR_3V3/sig2/GND2/B. Rockchip RK3588, LPDDR5-6400, 128 GB eMMC, RTL8852BE Wi-Fi, RTL8125BG 2.5 GbE, CS43198, TPA3255 315 W amp, HDMI 2.1, MIPI DSI-2, USB-C 3.2 with PD via CYPD3175, STM32G071. 34 footprints placed. **Zero routing.** ERC report: 3018 lines including 638 pin_not_connected, 128 power_pin_not_driven, 1 ground_pin_not_ground (silent short — GND miswired to a rail). DRC: 229 violations. USB-C VBUS, D+/D-, CC1/CC2 all unconnected in schematic — board cannot boot from USB-C. 216 shorting_items between +3V3 and +0V9 at RK3588 pins 34/35 (placeholder BGA pinout).

**Note on effort:** this board carries the heaviest schematic-level electrical engineering load in the family. 3018 open ERC lines and a placeholder RK3588 BGA pinout are not layout work; they are electrical design work. Bidders should not price this as a routing task.

**Deliverables:**
- Schematic-level electrical rework — every one of the 3018 ERC issues resolved, USB-C VBUS/CC/D± connected per Cypress CYPD3175 reference design, RK3588 BGA pinout replaced with a datasheet-verified footprint, `ground_pin_not_ground` silent short identified and corrected, CYPD3175 CCG3PA footprint pin numbering re-mapped from placeholder.
- ERC-clean schematic with every prior 3018 issue closed or explicitly waived with justification.
- DRC-clean PCB with all copper in source.
- LPDDR5-6400 T-topology or fly-by routing with matched skew < 2 ps, 40 Ω / 80 Ω controlled impedance.
- HDMI 2.1 TMDS routed as 100 Ω ±10 % differential with length matching.
- MIPI DSI-2 to orb OLED routed with proper length matching between D0P/D0N and clock lanes.
- Wi-Fi RTL8852BE antenna keep-out zone and U.FL coax pigtail routing planned.
- RTL8125BG PHY ferrite bead + common-mode choke placement within 10 mm of RJ45.
- USB-C hole-clearance violations resolved by swapping to a vendor library footprint with corrected NPTH clearances.
- Thermal isolation slot cut between TPA3255 (25–35 W dissipation) and RK3588 + LPDDR5 island. Shield-can cutout on top silk for Wi-Fi isolation from 315 W class-D amp.
- STM32G071 crystal populated in BOM if USB backup enumeration ever required.
- Solid GND pours on GND1 and GND2 layers. Power plane pours on PWR_1V1 and PWR_3V3.
- BOM with second-source MPNs. Fab drawing, pick-and-place, STEP export, Excellon-2 drills.

**Acceptance criteria:** zero DRC errors, zero ERC errors, LPDDR5 setup/hold margin > 15 % at 6400 MT/s in simulation, USB-C PD enumeration verified in schematic against Cypress reference design, thermal simulation showing LPDDR5 timing margin held at sustained TPA3255 load, DFM-4 fab-ready.

**Estimated effort:** 140 hours total — 60 hours schematic-level electrical engineer (3018 ERC + RK3588 BGA rebuild), 60 hours layout engineer, 20 hours SI specialist.

---

**Effort roll-up:** Halbach 200 h + Backplane 280 h + Orb 200 h + Mic-Array 110 h + Audio-Amp 130 h + Extender 140 h = **1,060 hours total.** The increase from the Rev-A 880-hour estimate reflects the correct scope classification (electrical design + layout, not layout) and the schematic-level rework hours previously omitted.

---

## 2A. Budget Ceiling Justification

The Rev-A draft of this SOW set a $180,000 not-to-exceed ceiling with an 880-hour effort estimate, implying a $205/hour blended rate across layout, SI, and safety engineering labor. That number was wrong for three concrete reasons, each of which we correct here.

**First, the labor mix is not uniformly layout.** A layout engineer with high-speed digital experience prices at roughly $180–$220/hour on the current US West Coast contract market. A signal-integrity specialist competent to sign off on 14-layer Megtron 6 Gen 5 backplane stackups prices at $250–$350/hour. A licensed functional-safety EE competent to sign a HAZOP letter for a levitating-magnetic-array controller prices at $300–$400/hour and typically bills a minimum block regardless of hours consumed. A rigid-flex layout specialist prices $20–$40/hour above the general layout rate. Blending these correctly against the per-board effort roll-up in Section 2 produces a $255–$275/hour weighted average, not $205.

**Second, the scope is electrical design + layout, not layout.** The prior draft classified the engagement as "hand-relayout" and priced it against layout rates. But the extender-sbc alone carries 3018 open ERC lines, the compute-backplane and orb both require BGA and CLGA footprints rebuilt from placeholder against manufacturer drawings, and the mic-array BOM is a zero-byte file that will have to be constructed from a clean schematic pass. That is schematic-level electrical engineering. Bidders correctly scoped as electrical design + layout houses will not accept the layout-house rate for this work, and layout-only houses will change-order Hearth to the correct rate in week three. The honest answer is to price it up front.

**Third, the effort estimate needed to grow to match the corrected scope.** Adding schematic-level electrical engineering hours to each board (25 h mic-array, 20 h audio-amp, 30 h orb, 40 h backplane, 60 h extender-sbc) and increasing the Halbach safety-EE allocation from 40 h to 50 h to accommodate a full HAZOP + SIL-2 review by a third-party firm raises the total from 880 to 1,060 hours. The blended-rate math against the corrected labor mix produces a fair-market bid range of $250,000–$275,000. We set the ceiling at $280,000 to leave headroom for the cross-board DFM sweep in week 10 and any Sanmina-requested Gate-4 edits.

**Cost model, illustrative, not prescriptive:**

| Board | Sch-level EE hrs @ $260 | Layout hrs @ $200–240 | SI hrs @ $300 | Safety/Thermal/Mech hrs | Board subtotal |
|---|---|---|---|---|---|
| Halbach | — | 110 @ $210 = $23,100 | 40 @ $300 = $12,000 | 50 safety-EE @ $325 = $16,250 | ~$51,400 |
| Backplane | 40 @ $260 = $10,400 | 140 @ $210 = $29,400 | 80 @ $310 = $24,800 | 20 thermal @ $220 = $4,400 | ~$69,000 |
| Orb | 30 @ $260 = $7,800 | 130 @ $240 = $31,200 | 40 @ $300 = $12,000 | 20 mech @ $220 = $4,400 | ~$55,400 |
| Mic-Array | 25 @ $250 = $6,250 | 60 @ $200 = $12,000 | 20 @ $290 = $5,800 | 5 EMI @ $220 = $1,100 | ~$25,150 |
| Audio-Amp | 20 @ $250 = $5,000 | 80 @ $200 = $16,000 | 20 @ $290 = $5,800 | 10 thermal @ $220 = $2,200 | ~$29,000 |
| Extender | 60 @ $260 = $15,600 | 60 @ $200 = $12,000 | 20 @ $290 = $5,800 | — | ~$33,400 |
| **Subtotals** | | | | | **~$263,350** |
| Cross-board DFM sweep + panelization + Gate-4 rework reserve | | | | | ~$16,650 |
| **NTE ceiling** | | | | | **$280,000** |

Fab NRE (Megtron 6 tooling, flex-rigid stackup qualification, panelization tooling) is paid separately by Hearth to Sanmina under its own PO and is not counted against this ceiling.

---

## 3. Common Cross-Board Requirements

- **Surface finish.** ENIG on all six boards. Gold thickness 0.05–0.15 µm per IPC-4552. Nickel thickness 3–6 µm. Called out explicitly on every fab drawing — do not accept house default.
- **Solder mask.** Green matte on all boards except orb, which is matte black to reduce internal-reflection artifacts into the OLED sphere. Silkscreen white.
- **Fiducial marks.** Three global fiducials per side (top and bottom), 1.0 mm copper on 3.0 mm solder-mask keep-out, placed at Sanmina-standard XY offsets. Per-BGA local fiducials on every BGA with more than 200 balls.
- **Tooling holes.** Four 3.175 mm non-plated tooling holes per board at Sanmina Fremont's standard XY pattern. On panelized boards, tooling holes on the panel rails, not on the individual boards.
- **Length-matching group definitions.** Named groups with explicit tolerances committed in the KiCad netclass file: PCIe Gen 5 (±5 mil intra-pair, ±25 mil intra-group), LPDDR5 (±2 mil intra-pair, ±10 mil intra-byte-lane), MIPI CSI-2 and DSI-2 (±5 mil intra-pair, ±20 mil intra-group), USB 3.2 SS (±5 mil intra-pair), USB HS (±10 mil), HDMI 2.1 TMDS (±5 mil intra-pair, ±20 mil intra-group), 100 GbE (±3 mil intra-pair), I²S/PDM (±20 mil).
- **Impedance targets.** 50 Ω single-ended on general signals, 90 Ω differential for MIPI, 100 Ω differential for USB HS/SS/HDMI/PCIe, 40 Ω single-ended / 80 Ω differential for LPDDR5, 85 Ω differential for the Gen 5 lanes referenced to Megtron 6. Stackup PDF must show the calculated width/gap for each netclass with tolerance envelope.
- **Test-point strategy.** Minimum 4 test points per power rail (distributed around the rail, not clustered), 2 dedicated GND test points, 1 test point on RESET_N, 1 on BOOT_MODE, 1 on TX/RX for every UART. Test points are 40 mil pads with fiducial-style keep-out.
- **JTAG/SWD debug header.** 10-pin ARM Cortex 0.05 inch (1.27 mm) pitch on every board with an MCU or SoC. Silkscreen labels: `SWD`, pin-1 arrow, pinout on assembly drawing.
- **Board-ID silkscreen.** Standard block on the top layer of every board with part number (`HRTH-PCB-###`), revision (`Rev A0`), fab-week code area (4 mm × 8 mm blank rectangle), pin-1 marker for the whole board.
- **Panelization preference.** Single-up boards only for the compute backplane. All others panelized where economically favorable. Preference: v-score between rectangular boards, mouse-bite tabs where v-score is not feasible (mic-array round, orb flex-rigid). Panel rails 10 mm minimum with global fiducials and tooling holes.

---

## 4. Intellectual Property and Confidentiality

- **NDA required.** No design files, schematics, gerbers, BOMs, or other technical exhibits leave the Hearth repository until a bilateral NDA is countersigned. Draft NDA available on request; standard mutual form, 5-year term, California jurisdiction.
- **Confidential design elements.** The Halbach levitation controller (halbach-controller board), the OLED-sphere face driver stack (orb board), and the closed-loop compute-backplane cooldeck geometry are identified as trade-secret design elements and marked **CONFIDENTIAL — TRADE SECRET** on every file that carries them.
- **Provisional patent references.** Draft provisional application IDs HRTH-PROV-2026-004 (Halbach control loop with dual-lockstep MCU cross-check), HRTH-PROV-2026-007 (OLED-sphere flex-rigid geometry), HRTH-PROV-2026-011 (integrated media-server + AI-companion power sequencing) are cited in the relevant board directories. The design + layout house will receive redacted excerpts under NDA.
- **Ownership.** All deliverables — schematics, layouts, gerbers, BOMs, stackup documentation, simulation reports, fab drawings — become Hearth-owned work-for-hire upon delivery and payment. Design + layout house retains no rights.
- **Portfolio disclosure.** The design + layout house may reference the engagement in its portfolio only as: *"Generic PCB electrical design + layout services, luxury consumer hardware, 2027."* The product name "Hearth," any board names, any Hearth trademarks, any Shark Tank references, and any specific technical descriptions are prohibited from portfolio use for a period of three years from delivery.
- **Residuals.** Engineers may retain general skills and know-how learned during the engagement but may not reproduce any Hearth-specific design element in any other engagement.

---

## 5. Vendor Evaluation Matrix (RFP Scoring)

Weights sum to 100. Each candidate is scored on each criterion. Highest total wins the award. No implicit bonuses, no tiebreaker thumbs on the scale — a level playing field. Ties broken by earliest committed timeline, and if still tied, by lowest bid price.

**Vendor shortlist.** The Rev-A draft included Screaming Circuits Design Services on the shortlist. That was a miscasting. Screaming Circuits is a strong small-batch prototype-assembly and quick-turn 4-to-6-layer boutique, but they do not have the 14-layer Megtron 6 Gen 5 backplane track record that this program requires and would either no-bid or subcontract that scope to a partner we would rather engage directly. They are removed from this Rev-B shortlist. The replacement is **Nova Engineering** (Ohio), a long-track-record high-speed digital and safety-critical design house that has shipped Gen 5 backplane work in the last 18 months and carries in-house SI and functional-safety credentials that materially reduce subcontractor coordination risk on this program. The full Rev-B shortlist is: **Sanmina Fremont Design Team, Nuvation Engineering, Nova Engineering.**

**Third-party safety-EE requirement — standardized.** Every bid must name a specific third-party licensed functional-safety EE consultant contracted as a subcontractor to the bidder for the Halbach board HAZOP and IEC 61508 SIL-2 review. In-house safety-EE attestation from the design + layout house is **not acceptable** on this board — the levitation controller drives a magnetic array holding a 2 kg glass sphere, the safety liability is real, and Hearth requires an independent signature outside the house that did the layout. Acceptable third-party firms:

- **RGA Safety Consulting** — small-shop functional-safety practice with hardware-startup track record.
- **Exida** — well-known SIL certification body, standard reference for IEC 61508 sign-off.
- **TÜV SÜD** — SIL and functional-safety certification, highest credibility on paper.
- **Bureau Veritas** — broader safety certification with functional-safety desk.

A bidder may propose an alternative third-party firm subject to Hearth written approval. **Any bid that does not name a specific external safety-EE subcontractor for the Halbach board — or that proposes an in-house layout-house safety-EE attestation in place of a third-party signature — is auto-scored 0 on the "Safety-critical hardware track record" 15-point criterion.**

| Criterion (weight)                                              | Sanmina Fremont Design Team | Nuvation Engineering | Nova Engineering |
|---|---|---|---|
| **Hardware category experience** (25 pts) — luxury consumer, AI compute, mixed-signal audio, safety-critical motor control on the same roof | ___ / 25 | ___ / 25 | ___ / 25 |
| **SI/PI expertise for Gen 5 + DDR5** (20 pts) — demonstrated Megtron 6 stackup deliveries in the last 18 months, HyperLynx or ADS licensed in-house, at least one PCIe Gen 5 board delivered in the last 24 months | ___ / 20 | ___ / 20 | ___ / 20 |
| **Safety-critical hardware track record** (15 pts) — IEC 61508 or ISO 26262 experience, prior HAZOP-signed deliveries, **named third-party licensed functional-safety EE subcontractor for the Halbach board (auto-0 if missing)** | ___ / 15 | ___ / 15 | ___ / 15 |
| **Timeline commitment** (15 pts) — bid weeks against our 14-week envelope; earlier bids score higher, bids exceeding 14 weeks score 0 | ___ / 15 | ___ / 15 | ___ / 15 |
| **Bid price** (10 pts) — fixed-fee bids at or under $280k score 10; T&M bids score 8 minus $5k penalty per $10k above midpoint; bids above cap score 0 | ___ / 10 | ___ / 10 | ___ / 10 |
| **References** (10 pts) — three checkable references from consumer-hardware startups shipping in the last 24 months | ___ / 10 | ___ / 10 | ___ / 10 |
| **Communication cadence + project management** (5 pts) — named PM, weekly Zoom, Slack Connect commit, gate-review discipline | ___ / 5 | ___ / 5 | ___ / 5 |
| **TOTAL** | ___ / 100 | ___ / 100 | ___ / 100 |

Award threshold: 75/100 minimum. Ties broken by earliest committed timeline, then by lowest bid price. No implicit bonus for co-location with Sanmina Fremont — the RFP is run as a level playing field, and if the co-located Sanmina design team is genuinely the best-scoring bid, they win on their own merits.

---

## 6. Timeline and Milestones

Fourteen calendar weeks from kickoff (2026-08-31) to signed gerber release (2026-12-04). Two electrical-design + layout engineers minimum, one SI specialist, one named third-party functional-safety EE. Named gate reviews on the calendar below cannot slip more than 3 business days without triggering the escalation clause in Section 9.

| Week | Dates (2026)  | Named milestone | Acceptance criteria |
|---|---|---|---|
| 1 | Aug 31 – Sep 4 | Kickoff, NDA execution, file handoff, house DFM re-read, revised timeline commit | Signed NDA on file; house returns its own DFM re-read within 5 business days confirming or challenging the audit findings; joint schedule ratified; named third-party safety EE confirmed contracted |
| 2 | Sep 7 – Sep 11 | Halbach schematic ERC pass 1 + placement lock; orb schematic ERC pass 1 begins | Halbach `.kicad_sch` ERC-clean; all placeholder footprints on the halbach board replaced; orb ERC first pass reviewed with Hearth CTO |
| 3 | Sep 14 – Sep 18 | **Gate 1a — Halbach safety review (end of week 3).** **Gate 1b — Orb schematic + placement lock; flex-rigid PO gate.** | See Section 8. Orb-side gate: schematic ERC-clean, flex-rigid stackup declared and signed, Sanmina Fremont flex-rigid slot PO issued so the 8-week lead time starts against Gate 5. |
| 4 | Sep 21 – Sep 25 | Compute-backplane 14-layer Megtron 6 stackup declared; ExaMAX + JAE footprints verified; SI floor-plan review | Stackup PDF signed by SI specialist; SI floor plan reviewed with Hearth CTO |
| 5 | Sep 28 – Oct 2 | Compute-backplane PCIe Gen 5 + 100 GbE hand-routing begins; mic-array PDM star topology floor-plan | Backplane routing begins on layers 3–4 (inner Gen 5); mic-array PDF signed |
| 6 | Oct 5 – Oct 9 | Compute-backplane inner-layer routing continues; audio-amp Purifi footprint rebuild + LM5116 schematic pass | Backplane inner layers 60 %+ routed; audio-amp ERC-clean |
| 7 | Oct 12 – Oct 16 | **Gate 2 — Compute-backplane SI/PI review (end of week 7).** Extender-sbc schematic ERC cleanup begins in parallel | See Section 8. Extender-sbc ERC pass 1 reduces open-issue count 50 %+ from 3018 baseline |
| 8 | Oct 19 – Oct 23 | Audio-amp + extender-sbc placement lock, hand-routing begins on high-current and USB nets | Both boards DRC violation count reduced 50 %+ from audit baseline |
| 9 | Oct 26 – Oct 30 | Cross-board DFM sweep pass 1; panelization plan drafted with Sanmina; ESD network audit | Panelization draft returned by Sanmina; ESD audit report delivered |
| 10 | Nov 2 – Nov 6 | **Gate 3 — All P1/P2 boards DRC-clean (end of week 10)** | See Section 8 |
| 11 | Nov 9 – Nov 13 | Cross-board DFM sweep pass 2; stackup PDFs finalized on all six boards; Sanmina DFM-4 pre-review package assembled | All six stackup PDFs delivered; Sanmina DFM-4 package submitted |
| 12 | Nov 16 – Nov 20 | **Gate 4 — Sanmina Fremont DFM-4 review returns fab-ready (end of week 12)** | See Section 8 |
| 13 | Nov 23 – Nov 27 | Sanmina-requested Gate-4 edits closed; final BOM CSV pass; STEP + IPC-2581 export verified against enclosure drawings | Every Sanmina Gate-4 comment closed with named responsible engineer; STEP interference-clean |
| 14 | Nov 30 – Dec 4 | Final sign-off; gerber release with SHA-256 hashes; **Gate 5 — first-article boards ordered** | See Section 8 |

Weekly Friday 3:00 PM Pacific Zoom review with all named stakeholders. Slippage of any gate by more than 3 business days triggers the escalation clause. Note that Thanksgiving week (Nov 23 – Nov 27) is inside the envelope; bidders should factor US holiday coverage into their staffing plan and confirm coverage in the bid response.

---

## 7. Communication Protocol

- **Weekly Zoom.** Friday 3:00–4:00 PM Pacific. Attendees: Hearth CEO, Hearth CTO, design + layout house project manager, house lead engineer, SI specialist, named third-party functional-safety EE (weeks 1–4 and any week with a Halbach touchpoint), Sanmina Fremont DFM rep (weeks 7, 11, 12). Zoom link stable across engagement.
- **Slack Connect channel.** `#hearth-relayout-2026` shared between Hearth and the design + layout house. Daily standup posts required during weeks 2 through 12, 10:00 AM Pacific: yesterday, today, blockers. Sanmina rep added to the channel in week 5. Third-party safety EE added weeks 1–4 and any week with a Halbach touchpoint.
- **Gate reviews.** In-person if geographically feasible (Sanmina Fremont, Hearth HQ), Zoom otherwise. Signed written attestation captured for each gate. Third-party safety EE signature required on Gate 1a.
- **Escalation path.** Design + layout house PM → Hearth Chief Hardware Officer → Hearth CEO. Escalation clock starts at first missed daily standup on a critical gate.
- **File exchange.** All design files exchanged through NDA-gated Git remote at `git.hearth.co/relayout-2026` — Hearth-hosted. No email attachments of source. Public shares (renders, screenshots) fine on Slack Connect.
- **Change control.** Every commit to a `-real.kicad_pcb` or `-real.kicad_sch` in weeks 2–14 must reference a ticket in the shared Linear project. Untracked commits will be reverted.

---

## 8. Success Gates

Six binary gates (Gate 1 split into 1a and 1b to cover the flex-rigid PO milestone). Each requires signed attestation from the named accountable party. No gate can be waived except by the Hearth CEO in writing.

- **Gate 1a — End of week 3, Halbach board passes third-party safety-EE review.** Zero +48 V shorts to any coil net in the release candidate. All COIL_HIGH nets maintain > 2 mm to any power rail. Fuse-and-detect circuit sanity-checked by a named third-party licensed functional-safety EE from the approved list in Section 5. HAZOP letter signed and countersigned by the third-party EE (not by any design + layout house staff engineer). Overcurrent latch trip verified in simulation within 10 µs of a 40 A step. Accountable parties: named third-party functional-safety EE + Hearth Chief Hardware Officer.
- **Gate 1b — End of week 3, orb schematic + placement locked and Sanmina flex-rigid PO issued.** Orb schematic ERC-clean, flex-rigid stackup declared and signed by rigid-flex specialist, Sanmina Fremont flex-rigid line slot PO issued so the 8-week fab lead time starts against a Gate-5 target of Dec 4. If Gate 1b slips, the Section 9 flex-rigid contingency ladder engages. Accountable parties: design + layout house lead engineer + Hearth Chief Hardware Officer.
- **Gate 2 — End of week 7, compute backplane passes SI/PI review.** PCIe Gen 5 lanes close on the loss budget at the declared 14-layer Megtron 6 stackup with simulated eye margin. DDR5 lanes clean with > 15 % setup/hold margin at 6400 MT/s. 100 GbE eye compliance simulated at each ExaMAX pair. `.gbrjob` matches declared stackup exactly. Accountable parties: SI specialist + Hearth CTO.
- **Gate 3 — End of week 10, all P1/P2 boards DRC-clean.** Extender-sbc, audio-amp, orb, mic-array return zero DRC violations at Sanmina Fremont rule set. ERC-clean on all four schematics. Every placeholder footprint replaced. Accountable parties: design + layout house lead engineer + Hearth Chief Hardware Officer.
- **Gate 4 — End of week 12, Sanmina Fremont DFM-4 review returns fab-ready.** Written DFM-4 letter from Sanmina Fremont covering all six boards. Panelization approved. Stackup documentation approved. Any Sanmina-requested edits closed within weeks 12–13. Accountable parties: Sanmina Fremont DFM engineer + Hearth Chief Hardware Officer.
- **Gate 5 — End of week 14, first-article boards ordered.** Gerber SHA-256 hashes recorded and referenced in a Sanmina PO. NRE paid. Delivery date confirmed. 25-piece smoke-test build authorized. Accountable party: Hearth CEO.

---

## 9. Contingencies

- **First-article yield below 50 % on any board.** If Sanmina's first-article inspection reports yield < 50 % on a board and the root-cause investigation attributes the failure mode to a design + layout error rather than a component or fab defect, the house is responsible for one no-charge spin of that board within 3 calendar weeks. A second spin at house cost is capped at 40 % of the original board fee. A third spin escalates to Hearth CEO for renegotiation.

- **Missed gate.** Slip of any gate by more than 1 week: automatic 5 % milestone-payment penalty for that gate. Slip by more than 2 weeks: 10 % penalty and mandatory Hearth CEO / house owner-level escalation call within 3 business days. Slip by more than 3 weeks: Hearth may terminate the engagement, take current work product under existing IP-assignment terms, and re-award the balance of scope to a backup vendor. Hearth pays for work delivered up to termination minus penalties.

- **Sanmina finds new DFM issues in Gate 4.** Additional-work order capped at 10 % of the original contract value ($28,000) for closing Sanmina-identified issues. Above the cap, work continues at pre-agreed T&M rates with a hard ceiling that requires Hearth CEO signature.

- **Flex-rigid lead-time contingency.** Sanmina Fremont's flex-rigid line runs an 8-week lead time from PO to first-article delivery. Gate 1b (end of week 3) is the point at which the orb schematic + placement must be locked and the flex-rigid PO issued so that lead time closes against the Gate-5 target of 2026-12-04. Three explicit branches, applied strictly:
  - **Gate 1b hit on schedule (end of week 3):** flex-rigid PO issued to Sanmina Fremont. Fab clock starts. No contingency action.
  - **Gate 1b slips by 1 week (into week 4):** design + layout house immediately reserves an alternate slot on Sanmina's Vietnam flex line (approximately +2 weeks lead time) and notifies Hearth CTO within 24 hours. The Fremont slot is held as long as Sanmina will hold it without a deposit. If the Vietnam alternate is used, the Section 3 panelization plan is re-run against the Vietnam line's panel constraints and any incremental cost is absorbed by the design + layout house up to $10k, above which it is Hearth's cost.
  - **Gate 1b slips by 2+ weeks (into week 5 or later):** escalation to Hearth founder. Options placed on the table are: (a) place a placeholder-deposit reservation on Sanmina Fremont's flex-rigid line at Hearth's cost to buy back the slot; (b) accept the Vietnam-line +2-week schedule impact and adjust Gate 5 accordingly; (c) descope the orb from the Shark Tank taping build and ship a rigid-only demo unit with a mock sphere face. The founder makes the call. The design + layout house is expected to have all three options priced and scheduled within 5 business days of the Gate 1b miss being declared.

- **Force-majeure event affecting silicon supply.** Component substitutions requiring footprint changes are covered under the change-control process at agreed T&M rates. Design + layout house is not responsible for global-shortage-driven redesign.

- **Shark Tank taping schedule slips.** No penalty adjustment for Hearth-side calendar changes. Design + layout house continues on the ratified 14-week schedule regardless of Hearth's external deadlines.

- **Third-party safety EE unavailable.** If the named third-party safety EE becomes unavailable mid-engagement, the design + layout house has 5 business days to secure a replacement from the Section 5 approved list, subject to Hearth written approval. No in-house safety-EE attestation is accepted as a substitute at any point in the engagement.

---

## 10. Contract Terms Summary

- **Fee structure.** Fixed-fee milestone payments preferred. Milestones tied to Gates 1–5: 15 % at kickoff, 15 % at Gate 1a + 1b combined (both required), 20 % at Gate 2, 20 % at Gate 3, 20 % at Gate 4, 10 % at Gate 5. Time-and-materials bids accepted only with a hard $280k cap, weekly burn-rate reporting, and Hearth CEO right to pause work at any time.
- **Payment terms.** Net-15 from milestone acceptance. Wire transfer to design + layout house account of record. Hearth withholds no more than 10 % as retainer until Gate 5.
- **IP assignment.** All deliverables are work-for-hire owned by Hearth per Section 4. Design + layout house countersigns a broad IP-assignment clause covering all work product.
- **Warranty.** Design + layout house warrants the design + layout against latent defects for **12 months** from Gate 5. Latent defect = a design or layout error that manifests only after fabrication and assembly, was not detectable by DRC, ERC, or standard SI simulation at release, and would have been caught by industry-standard practice. Warranty remedy: no-charge respin of the affected board, capped at one spin per board per year.
- **Indemnity.** Design + layout house indemnifies Hearth against third-party IP claims arising from the house's work product (e.g., an infringing library part). Hearth indemnifies the house against claims arising from Hearth-provided schematics, silicon selections, and confidential design elements.
- **Insurance.** Design + layout house maintains $2M general liability, $2M errors-and-omissions, and $1M cyber policies for the duration of the engagement plus 12 months. The named third-party safety EE must independently carry $2M professional liability coverage attaching to the Halbach board sign-off.
- **Choice of law.** California. Venue in Alameda County or San Mateo County at Hearth's election.
- **Dispute resolution.** Good-faith negotiation for 30 days; then JAMS arbitration in San Francisco under JAMS Comprehensive Arbitration Rules. Each side bears its own fees; prevailing party recovers reasonable attorney's fees.
- **Termination for convenience.** Hearth may terminate on 10 business days' written notice. Payment due for work completed to the termination date.
- **Termination for cause.** Either party may terminate on 5 business days' written notice for material breach uncured after written notice.
- **Non-solicitation.** Neither party solicits the other's employees for 12 months post-engagement.

---

## Appendix A — Draft RFP Cover Letters

### A.1 — Sanmina Fremont Design Team

Dear Sanmina Fremont Design Services team,

Hearth is preparing to fabricate a six-board PCB family at your Fremont facility for a pilot build of our flagship product. An independent DFM red-team audit dated 2026-08-04 returned a do-not-release verdict on all six boards. We hold your Fremont fab in high regard — the co-location of a Sanmina-owned electrical design + layout team with the Sanmina line that will build the boards is a real operational advantage, and we are inviting you to bid on that basis. To be explicit up front: the Rev-A draft of this RFP carried a 5-point implicit tiebreaker bonus for Sanmina co-location. That has been removed in Rev-B. The RFP is now a level playing field. If your bid earns the top score on its own merits, you win the award without a thumb on the scale.

The scope is a full electrical design + layout rework on all six boards from a placement-only starting condition sitting on top of schematics with thousands of open ERC issues, placeholder BGA/CLGA footprints, and — on the compute backplane and the orb — declared stackups that were never actually generated. Total effort estimated at 1,060 hours across 14 calendar weeks with two electrical design + layout engineers, one signal-integrity specialist, and one named third-party functional-safety EE. The compute backplane requires a re-declared 14-layer Megtron 6 stackup and PCIe Gen 5 / 100 GbE hand-routing — we understand this pulls in your Toronto SI lab or an equivalent Sanmina resource, and we welcome that. The orb requires a flex-rigid re-declaration and qualification on your Fremont flex-rigid line — please confirm current lead time and NRE, and note the Gate 1b PO gate at the end of week 3 in Section 8 and the associated flex-rigid contingency ladder in Section 9. The Halbach controller is safety-critical; per Section 5, in-house safety-EE attestation is not acceptable, and every bid must name a specific third-party licensed functional-safety EE from the approved list (RGA Safety Consulting, Exida, TÜV SÜD, or Bureau Veritas).

Budget: not-to-exceed $280,000 for the electrical design + layout scope, exclusive of fab NRE which is paid directly to Sanmina under a separate PO. See Section 2A for the ceiling justification and per-board cost model. Timeline: kickoff 2026-08-31, gerber release 2026-12-04. Milestone-based fixed-fee preferred.

We are asking for a bid response by 2026-08-19 covering: (a) proposed team including named engineers and their PCIe Gen 5 / Megtron 6 credentials from the last 18 months; (b) named third-party functional-safety EE subcontractor for the Halbach board; (c) fixed-fee price with milestone breakdown; (d) commit to the 14-week envelope with named gate deliverables and Thanksgiving-week coverage; (e) confirmation of flex-rigid line availability and lead time from PO; (f) three consumer-hardware startup references from the last 24 months; (g) sample NDA acceptable for immediate execution so we can release the technical exhibits.

The DFM audit report and the six KiCad projects are available upon NDA execution. We can schedule a technical walkthrough with your team by end of this week.

We look forward to your proposal.

Respectfully,
Mark Kirk
CEO, Hearth, Inc.
mark.kirk@hearth.co

---

### A.2 — Nuvation Engineering

Dear Nuvation Engineering team,

Hearth is soliciting bids for a six-board PCB electrical design + layout rework on a 14-calendar-week schedule. Nuvation's specialist bench — particularly your battery-management and safety-critical hardware track record — puts you at the top of our shortlist for the Halbach controller sub-scope. We are inviting you to bid on the full six-board package alongside Sanmina Fremont's design team and Nova Engineering.

Context: our independent DFM red-team audit on 2026-08-04 returned a do-not-release verdict on all six boards. The Halbach controller alone reports 861 DRC violations including a coil high-side net shorted to the +48 V rail at Q9, high-side gate tied to low-side gate at the DRV8323, and analog ground tied to the INA240 current-sense line — the entire safety chain is defeated on paper. This board drives a magnetic levitation array holding a 2 kg glass sphere. Failure is a projectile. We need a house that will run this board through a proper HAZOP and IEC 61508 SIL-2 minimum verification signed by a named third-party licensed functional-safety EE (RGA Safety Consulting, Exida, TÜV SÜD, or Bureau Veritas — see Section 5) before we authorize any power-on. In-house safety-EE attestation from your own staff is not acceptable on this board — bids without a named external safety-EE subcontractor auto-score 0 on the safety-critical criterion.

The rest of the scope — compute backplane (14-layer Megtron 6, PCIe Gen 5, 100 GbE), extender SBC (LPDDR5-6400, HDMI 2.1, 3018 open ERC lines), orb (flex-rigid, 6-camera MIPI CSI-2), mic-array (13-mic PDM), and audio amp (±60 V rails, Purifi Class-D) — is a mix of schematic-level electrical engineering, footprint reconstruction, SI closure, and hand-routing totaling roughly 860 hours on top of the 200 hours for the Halbach board.

If Nuvation prefers to bid only the Halbach sub-scope and let another house handle the other five boards, we will consider that arrangement — please indicate your preference in the bid.

Budget: not-to-exceed $280,000 for the full six-board scope, prorated if you bid a subset. Timeline: kickoff 2026-08-31, gerber release 2026-12-04. Milestone-based fixed-fee preferred. See Section 2A for the ceiling justification and blended-rate build-up.

Please respond by 2026-08-19 with: (a) proposed team including named third-party licensed functional-safety EE for the Halbach board; (b) fixed-fee price with milestone breakdown, prorated by sub-scope if bidding a subset; (c) 14-week schedule commitment with Thanksgiving-week coverage; (d) three safety-critical or battery-management hardware references from the last 24 months; (e) NDA acceptable for immediate execution.

Nuvation's safety-critical credentials are a strong match for the highest-risk part of this program. We look forward to your response.

Sincerely,
Mark Kirk
CEO, Hearth, Inc.
mark.kirk@hearth.co

---

### A.3 — Nova Engineering

Dear Nova Engineering team,

Hearth is soliciting bids for a six-board PCB electrical design + layout rework on a 14-calendar-week schedule. Nova's long-standing high-speed digital and safety-critical hardware track record — including recent Gen 5 backplane deliveries — puts you on our Rev-B shortlist alongside Sanmina Fremont's in-house design team and Nuvation Engineering. To be direct: this is Nova's first RFP from Hearth. We are inviting you because the compute backplane in this program requires a real Gen 5 backplane house, not a boutique quick-turn shop, and you have shipped that class of board recently enough to price it honestly.

Scope: an independent DFM red-team audit on 2026-08-04 returned a do-not-release verdict on all six boards. Three ship placement-only (no copper); the safety-critical Halbach controller has 861 DRC violations including a +48 V rail shorted to a coil high-side net; the compute backplane declares a 14-layer Megtron 6 stackup in its README but ships as 4-layer FR4; the orb declares flex-rigid but ships flat 6-layer; the mic-array BOM is a zero-byte file; and the extender-sbc returns a 3018-line ERC report with one silent GND-to-rail short. Total effort estimated at 1,060 hours over 14 calendar weeks. The scope is electrical design + layout, not layout — schematic-level ERC cleanup, BGA footprint reconstruction, SI closure at Gen 5 line rates, and functional-safety engineering on the Halbach controller are all in scope.

Two structural notes on this RFP that we want to flag up front. First, the safety-critical criterion in Section 5 requires a named third-party licensed functional-safety EE contracted as a subcontractor for the Halbach board HAZOP and SIL-2 review — acceptable firms are RGA Safety Consulting, Exida, TÜV SÜD, and Bureau Veritas. In-house Nova safety-EE attestation is not acceptable on this board and any bid without a named external subcontractor auto-scores 0 on the safety-critical 15-point criterion. Second, the orb flex-rigid PO gate at end of week 3 is a hard timing constraint against Sanmina Fremont's 8-week flex-rigid lead time; Section 9 lays out the three-branch contingency ladder if that gate slips.

Budget: not-to-exceed $280,000 for the full six-board scope. Timeline: kickoff 2026-08-31, gerber release 2026-12-04. Milestone-based fixed-fee preferred. See Section 2A for the ceiling justification and blended-rate build-up.

Please respond by 2026-08-19 with: (a) proposed team including named engineers with Gen 5 backplane credentials from the last 18 months and a named third-party functional-safety EE subcontractor for the Halbach board; (b) fixed-fee price with milestone breakdown; (c) 14-week schedule commitment with Thanksgiving-week coverage; (d) three consumer-hardware or safety-critical references from the last 24 months, at least one covering a Gen 5 backplane delivery; (e) NDA acceptable for immediate execution.

We look forward to your proposal.

Best regards,
Mark Kirk
CEO, Hearth, Inc.
mark.kirk@hearth.co

---

**End of document.** Distribution: Hearth data room engineering folder (path: `hardware/electrical/dfm-audit/HRTH-SOW-2026-08-05-Rev-B.md`); PDF export emailed to the three candidate electrical design + layout houses on CEO written approval; internal copy retained in Hearth board packet for the emergency EE all-hands meeting.
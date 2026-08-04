# PAL Pod Audio Amp - KiCad Project

4-way active amplification board for the PAL Pod reference-grade audio chain:
tweeter, midrange, woofer, and subwoofer stages, each with its own
Cirrus Logic CS43198 32-bit / 384 kHz DAC feeding a THAT1512 balanced-line
receiver into a Purifi Audio 1ET7040SA Class-D amplifier module. Balanced
I2S / DSD arrives from the DAC master over a Silicon Labs Si8660BB digital
isolator; a Cirrus CS2100-CP fractional-N clock multiplier locks the DAC
master clock. HV rails are +/-60 V from a pair of TI LM5116 controller-based
SMPS stages, sequenced with a TI TPS3808 supervisor. Four Analog Devices
ADT7420 I2C temperature sensors monitor each Purifi module's heatsink.
Speaker outputs land on WBT-0705Cu binding-post terminals with muting relays.
6-layer board, 250 mm x 200 mm rectangle, ENIG, 2 oz outer copper for the
speaker / HV rails. See `../block-diagrams/audio-amp.md` for the
system-level signal chain this project implements.

## How to open

Requires **KiCad 8.0.0 or later** (KiCad 9 and 10 also open the files cleanly;
we developed and validated against KiCad 10.0.5 on macOS).

```
open -a KiCad /private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/electrical/kicad/palpod-audio-amp/palpod-audio-amp.kicad_pro
```

Or double-click `palpod-audio-amp.kicad_pro` in Finder. From KiCad's project
manager, open **Schematic Editor** and **PCB Editor**.

The project defines its own project-local symbol and footprint libraries in
`libraries/`; the `sym-lib-table` and `fp-lib-table` files at the project root
register them under the alias `palpod-audio-amp`. Standard KiCad symbols
(`Device:R`, `Device:C`, `Device:L`, `power:*`, `Connector:Conn_01x02_Pin`,
`Connector:Conn_01x04_Pin`) are embedded in the schematic's `lib_symbols`
block so the schematic opens even if a fresh KiCad install has not yet had
its stock libraries configured; on first save KiCad will link them back to
the real stdlib entries.

## What's populated

- [x] `.kicad_pro` project settings: **6-layer stackup**, ENIG, HV-friendly minimums (0.2 mm min track / 0.5 mm min copper-to-edge / 0.15 mm min via annular / 0.6 mm min via drill), and 5 net classes:
    - `Default` - 0.25 mm track, 0.6 mm via
    - `I2S_DIFF_100R` - 100 Ohm differential I2S / DSD, 0.2 mm width, 0.15 mm gap
    - `SPKR_HIGH_CURRENT` - 3 mm track, 1.8 mm via (0.5 mm clearance) for speaker outputs
    - `PWR_HV_60V` - 1.5 mm track, 1.2 mm via, 0.8 mm clearance for the +/-60 V bus
    - `ANALOG` - 0.3 mm track, 0.7 mm via for the +/-15 V analog rails
    Auto-assign patterns: `+60V / -60V / VBUS_HV*` -> `PWR_HV_60V`, `SPKR_*` -> `SPKR_HIGH_CURRENT`, `I2S_* / DSD_*` -> `I2S_DIFF_100R`, `AUDIO_* / +15V / -15V` -> `ANALOG`.
- [x] `.kicad_sch` root schematic on A3, populated title block (rev A0, 2026-08-03), embedded `lib_symbols` for every reference used (standard + power + 9 specialty parts).
- [x] Placed symbols (~70 total):
    - 4 x CS43198 DAC (one per channel: TWEETER / MID / WOOFER / SUBWOOFER)
    - 4 x THAT1512 balanced line receiver (per channel)
    - 4 x Purifi 1ET7040SA carrier connector (per channel)
    - 4 x ADT7420 heatsink temperature sensor (per module)
    - 4 x WBT-0705 speaker binding-post terminal (per channel)
    - 1 x Si8660BB digital isolator (I2S input isolation)
    - 1 x CS2100-CP master clock multiplier
    - 2 x LM5116 SMPS controller (one per rail: +60 V and -60 V)
    - 1 x TPS3808 supervisor
    - 24 x 100 nF + 8 x 10 uF decoupling caps + 4 x 1000 uF / 100 V bulk HV caps
    - 8 x 4.7 k pull-ups / gain resistors
    - 2 x 22 uH LM5116 output inductors
    - 1 x 4-pin PSU input connector, 1 x 4-pin I2S / DSD input header
- [x] Illustrative labels + wires seeding the net topology: `+60V / -60V / +15V / -15V / +12V / +5V / +3V3` power rails, `I2S_BCK / I2S_LRCK / I2S_SDIN / DSD_CLK` input bus, `SPKR_{TWEETER,MID,WOOFER,SUB}{+,-}` speaker outputs, `MUTE_* / FAULT_*_N` per-channel control, and `I2C_SCL / I2C_SDA` housekeeping bus.
- [x] `no_connect` flags on four DAC test pins (illustrative).
- [x] `libraries/palpod-audio-amp.kicad_sym` - hand-drawn symbols for the 9 specialty ICs. Each is a rectangular block with functional pin names and grouped pin types (power / input / output / bidirectional / passive). **The CS43198, Purifi, LM5116, and Si8660 pin mappings are placeholder groupings and pin numbers; the EE must verify each pin against the manufacturer datasheet before wiring.**
- [x] `libraries/palpod-audio-amp.pretty/` - 9 placeholder footprints (see `libraries/palpod-audio-amp.pretty/README.md` for the details and per-part verification checklist).
- [x] `.kicad_pcb` - **6-layer stackup declared** (F.Cu / In1.Cu = GND / In2.Cu = PWR_ANA / In3.Cu = PWR_HV / In4.Cu = GND / B.Cu), copper thickness 2 oz outer / 1 oz inner, 1.6 mm total, ENIG finish. **250 mm x 200 mm rectangular board outline drawn on Edge.Cuts.** Silkscreen title block and comment layer notes about the LV / HV isolation moat (3 mm min clearance between domains) and star ground point. No footprints placed yet - the EE places them during layout.
- [x] Pre-declared PCB nets (37) matching the schematic's power rails, I2S / DSD bus, speaker outputs, and control lines.
- [x] `sym-lib-table` / `fp-lib-table` register the project-local `palpod-audio-amp` library. Standard KiCad libraries are resolved from the user's KiCad install.
- [x] `fab/` - pre-generated schematic + PCB PDFs, 6-layer Gerbers, and BOM.csv from `kicad-cli`. All will be re-generated by the EE after real wiring / layout; these are here to prove the project exports end-to-end.

## What's stubbed / next steps for the EE

- [ ] **Verify placeholder footprints against real datasheets** before ordering fab. See `libraries/palpod-audio-amp.pretty/README.md`. In particular the Purifi 1ET7040SA module carrier is a rough 155 x 45 mm rectangle with a single-row 12-pin header; the real module has dual-row terminals on the sides and the exact positions must come from Purifi's datasheet.
- [ ] **Verify placeholder pin mappings on CS43198 / Purifi / LM5116 / Si8660 / CS2100 symbols** against the manufacturer datasheets. Update `libraries/palpod-audio-amp.kicad_sym` with the correct pin numbers, names, and electrical types.
- [ ] Complete the schematic wiring:
    - **I2S / DSD input path**: 4-pin input header -> Si8660BB isolator (VDD1 side) -> per-channel fanout to each CS43198's `SCLK / LRCK / SDIN / MCLK`. Master clock from CS2100 -> Si8660 to distribute to all DACs.
    - **DAC differential output -> line receiver**: CS43198 `AOUTA+/-` and `AOUTB+/-` -> THAT1512 `IN+/-` per channel (+15 V / -15 V rails, low-noise routing).
    - **Line receiver -> Purifi input**: THAT1512 `OUT` -> Purifi carrier connector `IN+ / IN-` (differential drive; add 100 nF DC-blocking cap in series if module requires AC-coupling).
    - **Purifi module power tree**: +60 V and -60 V bus off the two LM5116 stages, star-tied at each module carrier; +12 V aux logic from a linear reg off the +15 V rail.
    - **Speaker output**: Purifi `OUT+ / OUT-` -> mute relay -> WBT-0705 terminal. Add snubber network per Purifi datasheet.
    - **Temperature monitoring**: 4 x ADT7420 on I2C bus with unique address strap; connect to housekeeping MCU (external, not on this board).
    - **Power sequencing**: TPS3808 monitors +60 V readiness; asserts `PWR_GOOD_N` to release Purifi `MUTE` after rails stabilize (soft-start relay optional for turn-on thump control).
    - **HV bulk decoupling**: 4 x 1000 uF / 100 V radials near the Purifi input terminals; add 100 nF X7R film caps in parallel for HF path.
- [ ] Run ERC (`kicad-cli sch erc palpod-audio-amp.kicad_sch` or Tools -> Electrical Rules Checker). The current stub reports 813 violations, all consequences of the unwired stubs; drive them to zero.
- [ ] Assign every schematic symbol a valid footprint (Tools -> Assign Footprints).
- [ ] Update the PCB from the schematic (Tools -> Update PCB from Schematic in the PCB editor).
- [ ] Place footprints on the 250 x 200 mm rectangular board:
    - **LV domain (left half, x < 130 mm)**: PSU input, I2S / DSD input, Si8660 isolator, CS2100 clock, all 4 CS43198 DACs, all 4 THAT1512 receivers, TPS3808 supervisor, +/-15 V + 3.3 V + 5 V linear regs (add as needed).
    - **HV domain (right half, x > 130 mm)**: 2 LM5116 SMPS stages, HV bulk caps, 4 Purifi module carriers stacked in 2 rows, 4 ADT7420 sensors adjacent to each Purifi, 4 WBT-0705 output terminals on the right edge.
    - **Isolation moat**: 3 mm min copper-free strip on all inner and outer layers between the two domains; run only the isolated I2S and I2C traces + PWR_GOOD_N supervisor line across.
    - **Star ground**: single-point tie between GND_ANA, GND_HV, and chassis at the bottom center of the board.
- [ ] Route the +/-60 V HV rails first (they constrain the module placement). Use the `PWR_HV_60V` net class (1.5 mm track, 0.8 mm clearance).
- [ ] Route SPKR outputs on 2 oz outer copper only, using the `SPKR_HIGH_CURRENT` net class (3 mm width). Keep short, kept apart from LV signals.
- [ ] Route I2S / DSD as impedance-controlled 100 Ohm differential pairs (In2.Cu / In3.Cu are power planes -> route on F.Cu or B.Cu referenced to In1.Cu / In4.Cu ground).
- [ ] Pour GND on In1.Cu and In4.Cu (double-sided ground planes). Pour +/-60 V on In3.Cu split into two zones. Pour +/-15 V + 5 V + 3.3 V on In2.Cu split into zones.
- [ ] Run DRC to zero.
- [ ] Generate Gerbers + drill + BOM + pick-and-place (`File -> Fabrication Outputs`). Cross-check the BOM against `../block-diagrams/audio-amp.md`.
- [ ] Order 3-unit proto run from a fab that handles 6-layer, 2 oz outer, ENIG (JLCPCB, PCBWay, Advanced Circuits). Expect ~3-week turn for 6-layer.

## Command-line validation

The project has been validated with `kicad-cli` 10.0.5:

```
kicad-cli sch export netlist -o /tmp/audio-amp.net       palpod-audio-amp.kicad_sch  # succeeds; 813 ERC violations expected
kicad-cli sch erc            -o /tmp/audio-amp.erc       palpod-audio-amp.kicad_sch  # 813 violations (all from unwired stubs)
kicad-cli pcb export gerbers -o /tmp/audio-amp-gerbers/  palpod-audio-amp.kicad_pcb  # succeeds - 6 copper layers exported (F_Cu.gtl, GND1.g1, PWR_ANA.g2, PWR_HV.g3, GND2.g4, B_Cu.gbl)
kicad-cli pcb drc            -o /tmp/audio-amp.drc       palpod-audio-amp.kicad_pcb  # 0 violations (no footprints placed yet)
kicad-cli sym export svg     -o /tmp/audio-amp-symsvg/   libraries/palpod-audio-amp.kicad_sym    # renders all 9
kicad-cli fp  export svg     -o /tmp/audio-amp-fpsvg/    libraries/palpod-audio-amp.pretty       # renders all 9
```

## File format

- Schematic schema version `20231120` (KiCad 8)
- PCB schema version `20240108` (KiCad 8)
- Symbol library schema version `20231120`
- Footprint schema version `20240108`

Written in the `(hide yes)` effect-block form so the same files load
identically under KiCad 8, 9, and 10.

## Required KiCad libraries

Bundled with a stock KiCad 8+ install; no external download needed:

- `Device` (R, C, L)
- `power` (+5V, +3V3, +12V, +15V, -15V, +60V, -60V, GND) - also embedded in the schematic for offline opening
- `Connector` (Conn_01x02_Pin, Conn_01x04_Pin) - also embedded

The project-local `palpod-audio-amp` library (registered by
`sym-lib-table` / `fp-lib-table`) holds the specialty ICs and their
placeholder footprints:

| Symbol | Footprint | Purpose |
|---|---|---|
| `CS43198` | `CS43198_TQFN32` | Cirrus Logic 32-bit / 384 kHz stereo DAC |
| `CS2100-CP` | `CS2100_MSOP10` | Fractional-N master clock multiplier |
| `THAT1512` | `THAT1512_SOIC8` | Balanced line receiver |
| `Purifi_1ET7040SA` | `Purifi_1ET7040SA_Module` | Class-D amp module carrier connector |
| `LM5116` | `LM5116_HTSSOP24` | Wide-Vin sync buck controller |
| `TPS3808G01` | `TPS3808_SOT23-5` | Programmable-delay supervisor |
| `ADT7420` | `ADT7420_MSOP8` | I2C temperature sensor |
| `WBT-0705` | `WBT-0705_Terminal` | Cu speaker binding-post terminal |
| `Si8660BB` | `Si8660_SOIC16` | 6-ch digital isolator |

## Reference

- **Signal chain, BOM, test criteria:** `../../block-diagrams/audio-amp.md`
- **Board dimensions, mechanical:** TBD in the mechanical package
- **Amp module datasheet:** https://purifi-audio.com/product/1et7040sa/ (request direct from Purifi Audio - no distributor)

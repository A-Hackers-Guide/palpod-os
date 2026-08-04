# PAL Pod Mic Array — KiCad Project

Far-field microphone-array daughterboard for PAL Pod: 13 TDK InvenSense
ICS-41352 MEMS microphones in a dual-ring geometry (7 outer + 6 inner) feed
an XMOS XVF3800-INBW beamforming DSP and a Syntiant NDP120 always-on wake-word
neural processor, hosted by an STMicro STM32G474RETx MCU that uplinks over
USB 2.0 hi-speed through a Microchip USB3320 ULPI PHY. 4-layer board,
120 mm round, ENIG, ~1.6 mm total thickness. See
`../mic-array-reference-design.md` for the reference design, BOM,
stackup, impedance targets, and placement notes — this project is the KiCad
implementation of that document.

## How to open

Requires **KiCad 8.0.0 or later** (KiCad 9 and 10 also open the files cleanly;
we developed and validated against KiCad 10.0.5 on macOS).

```
open -a KiCad /private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/electrical/kicad/palpod-mic-array/palpod-mic-array.kicad_pro
```

Or double-click `palpod-mic-array.kicad_pro` in Finder. From KiCad's project
manager, open **Schematic Editor** and **PCB Editor**.

The project defines its own project-local symbol and footprint libraries in
`libraries/`; the `sym-lib-table` and `fp-lib-table` files at the project root
register them under the alias `palpod-mic-array`. Standard KiCad symbols
(`Device:R`, `Device:C`, `power:*`, `Connector:USB_C_Receptacle_USB2.0_16P`,
`MCU_ST_STM32G4:STM32G474RETx`, `Regulator_Linear:AP2114H-3.3`,
`Interface_USB:USB3320C`) are embedded in the schematic's `lib_symbols`
block so the schematic opens even if a fresh KiCad install has not yet had
its stock libraries configured; on first save KiCad will link them back to
the real stdlib entries.

## What's populated

- [x] `.kicad_pro` project settings: 4-layer stackup, ENIG, JLCPCB-friendly minimums (0.127 mm min track, 0.4 mm min via), net classes for `Default`, `Power`, `USB_HS` (90 Ω differential, 0.14 mm), `PDM` (impedance-controlled 50 Ω), auto-assign patterns for `+5V/+3V3/+1V8/+1V0`, `USB_D?`, `PDM_*`.
- [x] `.kicad_sch` root schematic on A3, populated title block (rev A0, 2026-08-03), embedded `lib_symbols` for every reference used.
- [x] Placed symbols: 13× ICS-41352 in a rough dual-ring arrangement, 1× XVF3800, 1× NDP120, 1× STM32G474RETx, 1× USB3320C, 1× USB-C receptacle (J1), 3× LDO regulators (U5/U6/U7), bulk + local decoupling caps, `+5V/+3V3/+1V8/+1V0/GND` power flags.
- [x] Illustrative wires and net labels on the +5V rail and the I2C bus, plus 17 pre-placed labels (`PDM_CLK`, `PDM_DATA0..12`, `I2S_BCK/LRCK/SDIN`, `USB_DP/DN`, `I2C_SCL/SDA`) to seed the wiring pattern.
- [x] `no_connect` flags on three NDP120 test pins.
- [x] `libraries/palpod-mic-array.kicad_sym` — hand-drawn symbols for the three specialty ICs (ICS-41352 5-pin, XVF3800 61-pin, NDP120 69-pin). Each is a rectangular block with functional pin names and grouped pin types (power/input/output/bidirectional/passive). **The XVF3800 and NDP120 pin mappings are placeholder groupings; the EE must verify each pin against the manufacturer datasheet before wiring.**
- [x] `libraries/palpod-mic-array.pretty/` — three placeholder footprints (see `libraries/palpod-mic-array.pretty/README.md` for the details and per-part verification checklist).
- [x] `.kicad_pcb` — 4-layer stackup declared (F.Cu / In1.Cu = GND / In2.Cu = PWR / B.Cu), copper thickness 1 oz outer / 0.5 oz inner, 1.6 mm total, ENIG finish. **120 mm diameter round board outline drawn on Edge.Cuts.** Silkscreen title block and a comment layer note about the analog/digital GND moat from ref-design §5.3. No footprints placed yet — the EE places them during layout.
- [x] `sym-lib-table` / `fp-lib-table` register the project-local `palpod-mic-array` library. Standard KiCad libraries are resolved from the user's KiCad install.

## What's stubbed / next steps for the EE

- [ ] **Verify placeholder footprints against real datasheets** before ordering fab. See `libraries/palpod-mic-array.pretty/README.md`.
- [ ] **Verify placeholder pin mappings on XVF3800 and NDP120 symbols** against the XMOS and Syntiant datasheets. Update `libraries/palpod-mic-array.kicad_sym` with the correct ball/pin numbers, names, and electrical types.
- [ ] Complete the schematic wiring:
    - PDM bus: 13× data lines from mics into XVF3800 PDM inputs, plus star-topology PDM_CLK from the XVF3800 fanout or a dedicated PI6C557 clock buffer (see ref-design §5.1 for skew budget).
    - I2S bus from XVF3800 → NDP120 for wake-word input; UART or SPI back from NDP120 → STM32 for wake event notification.
    - USB 2.0 differential pair: STM32 ULPI → USB3320 → USB-C connector (see ref-design §5.2 for length matching).
    - I2C bridge: STM32 ↔ XVF3800 ↔ NDP120 for host config.
    - Power tree: 5V → 3.3V analog (mics) via U5, 5V → 1.8V digital (DSP core) via U6, 5V → 1.0V (NDP internal) via U7. Decoupling per ref-design §5.6 (100 nF within 3 mm of every power pin + 10 µF bulk at each LDO output).
    - Reset/boot-strap net: STM32 GPIOs sequencing XMOS boot per ref-design §6.
    - ESD protection on USB (TPD4S014 on VBUS + D+/D-) and 5V input.
    - SWD debug header (4-pin 1.27 mm) breaking out SWDIO / SWCLK / GND / VCC per ref-design §8 TP8.
    - Test points TP1..TP10 per ref-design §8.
- [ ] Run ERC (`kicad-cli sch erc palpod-mic-array.kicad_sch` or Tools → Electrical Rules Checker). The current stub generates ~560 violations, all consequences of the unwired stubs; drive them to zero.
- [ ] Assign every schematic symbol a valid footprint (Tools → Assign Footprints).
- [ ] Update the PCB from the schematic (Tools → Update PCB from Schematic in the PCB editor).
- [ ] Place footprints on the 120 mm round board per ref-design §4:
    - 7 outer mics on R=60 mm at 45° pitch (adjust for 120 mm dia — the ref design uses 150 mm; scale radii to 45 mm/22 mm for a 120 mm board, or open a design change with the mechanical team).
    - 6 inner mics on R=30 mm.
    - IC block (XVF3800 / NDP120 / USB3320 / STM32) at the bottom center of the board.
    - USB-C at the bottom edge; 5 V power input header on the opposite edge if used.
- [ ] Route USB 2.0 D+/D- differential pair first (they constrain everything). Use the `USB_HS` net class (90 Ω differential, 0.14 mm trace).
- [ ] Route PDM bus as a star from the clock fanout. Length-tune per ref-design §5.1.
- [ ] Pour GND on In1.Cu; split In2.Cu into 3V3 and 1V8 zones with a moat between analog (mic) and digital (DSP) domains per ref-design §5.3.
- [ ] Run DRC to zero.
- [ ] Generate Gerbers + drill + BOM + pick-and-place (`File → Fabrication Outputs`). Cross-check the BOM against `mic-array-reference-design.md` §2.
- [ ] Order 5-unit proto run from JLCPCB (4-layer, ENIG, ~2-week turn).

## Command-line validation

The project has been validated with `kicad-cli` 10.0.5:

```
kicad-cli sch export netlist -o /tmp/palpod.net palpod-mic-array.kicad_sch  # succeeds; ~560 ERC violations expected
kicad-cli pcb export gerbers -o /tmp/g/         palpod-mic-array.kicad_pcb  # succeeds
kicad-cli sym export svg     -o /tmp/sym-svg/   libraries/palpod-mic-array.kicad_sym    # renders all 3
kicad-cli fp  export svg     -o /tmp/fp-svg/    libraries/palpod-mic-array.pretty       # renders all 3
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

- `Device` (R, C)
- `power` (+5V, +3V3, +1V8, +1V0, GND) — also embedded in the schematic for offline opening
- `Connector` (USB_C_Receptacle_USB2.0_16P) — also embedded
- `MCU_ST_STM32G4` (STM32G474RETx) — also embedded
- `Regulator_Linear` (AP2114H-3.3) — also embedded
- `Interface_USB` (USB3320C) — also embedded

The project-local `palpod-mic-array` library (registered by
`sym-lib-table` / `fp-lib-table`) holds the specialty ICs and their
placeholder footprints.

## Reference

- **Full BOM, stackup, impedance, placement, sequencing:** `../mic-array-reference-design.md`
- **Block-level architecture:** `../block-diagrams/mic-array.md`

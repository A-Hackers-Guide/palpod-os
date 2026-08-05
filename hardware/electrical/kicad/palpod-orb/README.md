# Hearth Orb — KiCad Project

Internal PCB for the 7-inch magnetically-levitating OLED sphere ("orb"): a
Nordic nRF54H20 dual-core Cortex-M33+M0 SoC coordinates 6× Sony IMX415 cameras
(via a Toshiba TC358748 MIPI CSI-2 aggregator), a ST VL53L8 depth sensor, a
Slamtec RPLIDAR S3, and a Qualcomm FC7800 Wi-Fi 7 module on an M.2 2230 Key
A+E socket. Wireless power comes in through a Renesas P9418 Qi RX and a
rectifier/LDO chain to 5V/3V3/1V8/1V2 rails, backed by a small Li-Po via a
TI BQ25798 buck-boost charger. Four TDK TMR2305 magnetoresistive sensors feed
the Halbach position loop back to the levitation controller in the column.
A Solomon Systech SSD1963 sits on a second rigid island as the placeholder
curved-OLED source driver and fans out over a 40-pin FPC to the panel.

The board is a **6-layer flex-rigid**: two rigid FR4 islands (one for the
main compute, one for the OLED driver) connected by polyimide flex bridges
that curl inside the sphere. See `../block-diagrams/orb.md` for the block
diagram and the mechanical/power/wireless budgets — this project is the
KiCad implementation.

## How to open

Requires **KiCad 8.0.0 or later** (KiCad 9 and 10 also open the files
cleanly; developed and validated against KiCad 10.0.5 on macOS).

```
open -a KiCad /private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/electrical/kicad/palpod-orb/palpod-orb.kicad_pro
```

Or double-click `palpod-orb.kicad_pro` in Finder. From the project manager,
open **Schematic Editor** and **PCB Editor**.

The project defines its own project-local symbol and footprint libraries in
`libraries/`; the `sym-lib-table` and `fp-lib-table` files at the project
root register them under the alias `palpod-orb`. Standard KiCad symbols
(`Device:R`, `Device:C`, `Device:L`, `Device:D_Schottky`,
`power:+5V/+3V3/+1V8/+1V2/+BATT/VRECT/GND`) are embedded in the schematic's
`lib_symbols` block so the schematic opens even on a fresh KiCad install
that has not yet been pointed at its stock libraries.

## What's populated

- [x] `.kicad_pro` project settings: 6-layer flex-rigid friendly minimums
      (0.09 mm min track / 0.3 mm min via for the CSI routing), net classes
      for `Default`, `Power`, `MIPI_CSI` (90 Ω differential, 0.1 mm),
      `MIPI_DSI`, `RF_50`, `FLEX`, `QI_RX`, auto-assign patterns for
      `+5V/+3V3/+1V8/+1V2/+BATT/VRECT`, `CAM?_D?_*`, `DSI_*`, `ANT_*/RF_*`,
      `COIL_AC*`.
- [x] `.kicad_sch` root schematic on A2, populated title block
      (rev A0, 2026-08-03), embedded `lib_symbols` for every reference
      (including all specialty ICs), 32 placed symbols.
- [x] Placed symbols: nRF54H20 (U1), TC358748 MIPI aggregator (U2),
      VL53L8 ToF (U3), BQ25798 BMS (U4), P9418 Qi RX (U5), SSD1963 OLED
      driver (U6), 4× TMR2305 Halbach sensors (U7..U10), 6× 28-pin FPC
      camera connectors (J1..J6, one per IMX415), Slamtec S3 LIDAR
      connector (J7), M.2 2230 Wi-Fi 7 socket (J8), 40-pin OLED FPC out
      (J9), 12× 100 nF decoupling caps, 4× 10 µF bulk caps, 2× 4.7 kΩ
      I²C pullups, 4× Schottky rectifier diodes (D1..D4), boost inductor
      (L1), VRECT bulk (C24), BATT bulk (C25). Power symbols for
      `+5V/+3V3/+1V8/+1V2/+BATT/VRECT/GND` (12 flags).
- [x] Illustrative wires and net labels on the power rails and the I²C
      bus, plus text labels seeding the MIPI CSI, MIPI DSI, Wi-Fi UART,
      and LIDAR UART buses.
- [x] `no_connect` flags on the two nRF54H20 antenna pins (ANT1/ANT2)
      since the RF path goes through the M.2 module in this design.
- [x] `libraries/palpod-orb.kicad_sym` — hand-drawn symbols for
      **all 11 specialty parts**: nRF54H20 (aQFN94), TC358748 (BGA80),
      SSD1963 (LFBGA121), Slamtec_S3 (10-pin conn), P9418 (QFN40),
      TMR2305 (SOT-23-5), VL53L8 (LGA16), CAM_FPC28 (28-pin ZIF for the
      IMX415), BQ25798 (QFN29), M2_2230_KeyAE (75-pin socket), OLED_FPC40
      (40-pin ZIF for curved OLED). **All pin groupings are placeholder;
      the EE must verify every ball/pad/pin number against the
      manufacturer datasheet before wiring.**
- [x] `libraries/palpod-orb.pretty/` — 11 placeholder footprints (see
      `libraries/palpod-orb.pretty/README.md` for the details and
      per-part verification checklist).
- [x] `.kicad_pcb` — **6-layer flex-rigid stackup declared** using KiCad
      8's stackup features: F.Cu / In1.Cu (GND) / In2.Cu (PWR_3V3) /
      In3.Cu (PWR_5V) / In4.Cu (GND) / B.Cu, with alternating FR4
      prepreg (rigid sections) and polyimide core (flex sections),
      1 oz outer / 0.5 oz inner effective, 1.05 mm nominal total,
      ENIG finish, dielectric constraints enabled.
- [x] **Board outline drawn as a single closed contour** covering both
      rigid islands + one flex bridge: rigid1 is 40×40 mm at the origin,
      rigid2 is 30×20 mm at x = 55..85, connected by a 35×15 mm flex
      neck at y = ±7.5. A second (return) flex bridge is called out on
      the `Dwgs.User` layer as documentation. `F.SilkS` labels on both
      islands and inside the flex neck. `Cmts.User` layer carries the
      6L stackup summary and the flex-rigid fab recommendation.
- [x] `sym-lib-table` / `fp-lib-table` register the project-local
      `palpod-orb` library. Standard KiCad libraries resolve from the
      user's install.

## What's stubbed / next steps for the EE

- [ ] **Verify placeholder footprints against real datasheets** before
      ordering fab. See `libraries/palpod-orb.pretty/README.md`. In
      particular:
    - nRF54H20 aQFN94 — replace with the Nordic vendor footprint
    - TC358748 BGA80 — regenerate from Toshiba's package outline
    - SSD1963 — **or swap in the real curved-OLED source driver footprint;
      SSD1963 is a placeholder for the proprietary vendor driver in the spec**
    - M.2 2230 Key A+E socket — replace with the actual Amphenol / Molex /
      TE socket footprint (with correct keying notch and dual-row edge pads)
    - Camera and OLED FPCs — pick the exact Molex / JST part first
- [ ] **Verify every specialty-symbol pin mapping** against the manufacturer
      datasheet. Ball/pad/pin numbers on the nRF54H20, TC358748, SSD1963,
      P9418, BQ25798, and M.2 socket symbols are placeholder groupings.
- [ ] Complete the schematic wiring:
    - MIPI CSI-2 fan-in: 6× 4-lane MIPI (24 diff pairs total) from J1..J6
      into TC358748's per-camera input banks. Length-match within each
      lane group per MIPI D-PHY skew budget (~0.05 mm).
    - MIPI CSI-2 fan-out: 4-lane CSI-2 from TC358748 to nRF54H20 (or to a
      LatticeSemi CrossLink NX FPGA if the EE chooses the FPGA aggregator
      option). This is the highest-speed bus on the board.
    - MIPI DSI: 4-lane DSI from either nRF54H20 (if it has DSI IP) or the
      SSD1963 host bus over to the OLED FPC (J9).
    - Wi-Fi 7 M.2 socket (J8) UART/SDIO/PCIe bringup to nRF54H20; drive
      `W_DISABLE`, `PERST_N`, and `WAKE_N` from MCU GPIOs.
    - LIDAR UART + motor PWM from J7 to nRF54H20 UART/PWM peripherals.
    - 4× TMR2305 Halbach sensors (U7..U10) → nRF54H20 SPI or ADC (choose
      one). If ADC, add anti-alias RC filters per the TMR2305 datasheet.
    - VL53L8 depth cam (U3) → nRF54H20 I²C + interrupt.
    - Qi RX power tree: coil pigtail → P9418 (U5) → Schottky rectifier
      (D1..D4) → C24 bulk → BQ25798 (U4) → SYS rail; SYS → LDO chain
      to +3V3 / +1V8 / +1V2. Battery on BQ25798's BAT pin with a Li-Po
      protection FET; C25 as VBAT bulk.
    - I²C bridge: nRF54H20 ↔ TC358748, VL53L8, P9418, BQ25798, camera EEPROMs,
      OLED touch. Add 4.7 kΩ pullups (R1, R2 already placed).
    - Reset/boot-strap sequencing: nRF54H20 GPIOs drive `RESET_N` on the
      cameras and the OLED driver, and hold `LPn` low on VL53L8 during
      power-up.
    - ESD protection on the USB pair inside the M.2 socket (TPD4S014) and
      on the LIDAR UART lines (TPD1E10B06).
    - SWD debug header (4-pin 1.27 mm) breaking out SWDIO / SWCLK / GND /
      VCC from nRF54H20.
- [ ] Run ERC (`kicad-cli sch erc palpod-orb.kicad_sch` or Tools →
      Electrical Rules Checker). The current stub reports ~1100
      violations, all consequences of the unwired stubs; drive them to
      zero.
- [ ] Assign every schematic symbol a valid footprint
      (Tools → Assign Footprints). Most already have footprints assigned;
      confirm the passives are on the correct 0402/0805/1210 sizes for
      the flex sections.
- [ ] Update the PCB from the schematic (Tools → Update PCB from
      Schematic in the PCB editor).
- [ ] Place footprints on the PCB:
    - **Rigid 1 (40×40 mm):** nRF54H20 in the center, TC358748 to the
      right of the MCU, VL53L8 near the top edge, BQ25798 near the
      power-input edge, P9418 next to the coil pigtail, 4× TMR2305 on
      the ring near the sphere's equatorial magnets, 6× camera FPC
      connectors around the perimeter, M.2 Wi-Fi socket along one full
      edge.
    - **Flex bridge:** route only the MIPI DSI 4 pairs + I²C + reset
      lines across the neck. 0.5 oz Cu, min bend radius = 6× flex
      thickness. Add a stiffener on B.Adhes at each rigid interface.
    - **Rigid 2 (30×20 mm):** SSD1963 (or the real OLED driver) in the
      center, OLED FPC (J9) along the right edge, decoupling caps
      immediately adjacent to VDD balls.
    - See `../block-diagrams/orb.md` for mass-budget / center-of-mass
      constraints (500 g total, CoM within 2 mm of geometric center).
- [ ] Route MIPI CSI-2 pairs first: 24 differential pairs (6 cameras ×
      4 lanes) into TC358748. Use the `MIPI_CSI` net class (90 Ω diff,
      0.1 mm trace on inner layer with GND reference). Length-match
      per-camera lane groups within 0.05 mm intra-pair and 0.5 mm
      inter-pair.
- [ ] Route MIPI DSI (4 lanes) from OLED driver to the panel FPC.
      Use `MIPI_DSI` net class.
- [ ] Pour GND on In1.Cu and In4.Cu (both GND layers). Split power on
      In2.Cu (3V3 zones) and In3.Cu (5V + VBAT + VRECT zones). Keep the
      Qi RX section GND on its own island, joined to the main GND only
      at the BQ25798 star point.
- [ ] Run DRC to zero. Current DRC reports 0 violations on the
      un-populated stub board.
- [ ] Generate Gerbers + drill + BOM + pick-and-place
      (`File → Fabrication Outputs`). Cross-check the BOM against
      `../block-diagrams/orb.md` §Block diagram.
- [ ] **Order proto run from a fab that supports flex-rigid.** This is
      **not** a JLCPCB / OSH Park capability at the standard tier —
      recommend **PCBWay Advanced (flex-rigid), MicroConnex, or Flex
      Interconnect** for the 6L polyimide-core stackup. Expect 4-6 week
      turn and a $5-15k NRE for the first article.

## Command-line validation

Validated with `kicad-cli` 10.0.5 (fontconfig warnings filtered):

```
kicad-cli sym export svg -o /tmp/orb-sym-svg libraries/palpod-orb.kicad_sym
# → renders all 11 specialty symbols to SVG

kicad-cli fp export svg -o /tmp/orb-fp-svg libraries/palpod-orb.pretty
# → renders all 11 placeholder footprints to SVG

kicad-cli sch export netlist -o /tmp/orb.net palpod-orb.kicad_sch
# → succeeds; produces 228 KB netlist covering all 32 placed symbols

kicad-cli sch erc palpod-orb.kicad_sch --output /tmp/orb-erc.rpt
# → Found 1100 violations (all unwired-stub consequences; expected)

kicad-cli pcb drc palpod-orb.kicad_pcb --output /tmp/orb-drc.rpt
# → Found 0 violations, 0 unconnected pads

kicad-cli pcb export gerbers -o fab/gerbers palpod-orb.kicad_pcb
kicad-cli pcb export drill    -o fab/gerbers/ palpod-orb.kicad_pcb
kicad-cli pcb export pdf      -o fab/palpod-orb-pcb.pdf ...
kicad-cli sch export pdf      -o fab/palpod-orb-schematic.pdf palpod-orb.kicad_sch
kicad-cli sch export bom      -o fab/palpod-orb-bom.csv       palpod-orb.kicad_sch
```

The `fab/` directory holds a full first-cut export: Gerber set, drill file,
schematic PDF, PCB PDF, BOM CSV, and a zip package. Everything is
regeneratable; do not treat these outputs as authoritative until the
placeholder symbols/footprints and wiring have been verified.

## File format

- Schematic schema version `20231120` (KiCad 8)
- PCB schema version `20240108` (KiCad 8)
- Symbol library schema version `20231120`
- Footprint schema version `20240108`

Written so the same files load identically under KiCad 8, 9, and 10.

## Required KiCad libraries

Bundled with a stock KiCad 8+ install; no external download needed:

- `Device` (R, C, L, D_Schottky) — also embedded in the schematic for
  offline opening
- `power` (+5V, +3V3, +1V8, +1V2, +BATT, VRECT, GND) — also embedded

Everything else — the 11 specialty symbols and their placeholder
footprints — lives in the project-local `palpod-orb` library registered
by `sym-lib-table` / `fp-lib-table`.

## Reference

- **Block diagram, power budget, wireless link budget, mechanical
  constraints:** `../block-diagrams/orb.md`
- **Sister project (main column mic array):**
  `../palpod-mic-array/README.md`

## Notes on flex-rigid representation

KiCad 8 has *partial* flex-rigid support — the stackup editor accepts
`(type "core")` and `(type "prepreg")` entries with different materials
(FR4 vs polyimide), so the 6L stackup here declares two polyimide-core
layers to represent the flex sections, and the flex-zone extent is
called out on the `Dwgs.User` and `F.SilkS` layers. KiCad does *not*
have a first-class "flex zone" primitive in v8, so the fab package
must be accompanied by a separate mechanical drawing showing:

1. Where the flex sections start and end (fab-house-defined "rigid
   region" polygons).
2. Which copper layers exist in the flex vs the rigid region (typically
   only F.Cu, In2.Cu, In3.Cu, B.Cu carry through the flex; the two
   GND layers stop at the rigid boundary).
3. Coverlay openings (instead of solder mask) on the flex sections.
4. Stiffener locations at each rigid/flex transition.

Attach that drawing to the Gerber package when requesting a quote.

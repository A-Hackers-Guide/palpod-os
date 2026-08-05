# Hearth Compute Backplane - KiCad Project

The compute backplane is the highest-complexity PCB in the Hearth system:
a 14-layer, 450x300 mm carrier that hosts **10x NVIDIA Jetson Orin NX**
SO-DIMM modules (JAE MM70-260B1-R1 260-pin sockets) and **10x AMD Ryzen AI 9
HX 370** mini-SBC daughtercards (Samtec ExaMAX 56 Gbps mezzanine), stitched
together by a **Broadcom BCM56780 Trident 4** 12.8 Tbps switch fabric, with
PCIe Gen 5 signal integrity closed by an **Astera Labs Aries PT4** retimer,
40+ power rails managed by a **TI UCD90320** sequencer, chassis health tied
to a **Nuvoton NCT6116** BMC, and root-of-trust in an **Infineon SLB9670**
TPM 2.0.

Real high-speed routing (100 GbE, PCIe Gen 5) is 6-12 weeks of an SI
engineer's work; this project is the KiCad **setup stub** that gets the EE
past scaffolding: file layout, library tables, symbol/footprint placeholders,
14-layer stackup, net classes, board outline, and validated tooling.

See `../block-diagrams/compute-backplane.md` for the block-level
architecture and topology.

## How to open

Requires **KiCad 8.0.0 or later** (KiCad 9 and 10 also open the files
cleanly; developed and validated against KiCad 10.0.5 on macOS).

```
open -a KiCad /private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/electrical/kicad/palpod-compute-backplane/palpod-compute-backplane.kicad_pro
```

Or double-click `palpod-compute-backplane.kicad_pro` in Finder. From the
KiCad project manager, open **Schematic Editor** and **PCB Editor**.

The project defines a project-local symbol and footprint library in
`libraries/`; `sym-lib-table` and `fp-lib-table` at the project root
register them under the alias `palpod-compute-backplane`. Standard KiCad
symbols (`Device:R`, `Device:C`, `power:+12V/+5V/+3V3/+1V8/+0V9/GND`) are
embedded in the schematic's `lib_symbols` block so the sheet loads even if a
fresh KiCad install has not yet had its stock libraries configured; on first
save KiCad will link them back to the real stdlib entries.

## What's populated

### Project (`.kicad_pro`)

- 14-layer stackup declared:
  `F.Cu / GND1 / SIG1 / GND2 / SIG2 / PWR12V / PWR3V3 / PWR1V8 / PWR_ANALOG / SIG3 / GND3 / SIG4 / GND4 / B.Cu`
- Copper: 1 oz outer / 0.5 oz inner, finish **ENIG**
- Dielectric: **Megtron 6** (Er 3.4, tan-delta 0.004) - required for PCIe
  Gen 5 loss budget
- Net classes:
  - `Default` - 0.2 mm track, 0.6 mm via
  - `HS_DIFF_100R` - 100 ohm diff pair, 0.1 mm width / 0.1 mm gap, 0.35 mm via
  - `PCIe_G5` - PCIe Gen 5 diff pair, 0.1 mm / 0.11 mm gap
  - `ETH_100G` - 100 GbE diff pair, 0.09 mm / 0.09 mm gap
  - `PWR_12V` - 1.0 mm track, 1.2 mm via (light budget - real 12V distribution needs bus bars or copper pours)
  - `PWR_LOW_VOLTAGE` - 0.4 mm track, 0.8 mm via
- Netclass auto-assignment patterns for `+12V/+5V/+3V3/+1V8/+0V9`, `ETH*`,
  `*PCIE*`, `PEX0_*`, `USB*`, `MGBE*`
- DRC minimums tuned for 4/4 mil fab (0.09 mm track, 0.1 mm clearance)

### Schematic (`.kicad_sch`)

- A0 sheet, populated title block (rev A0, 2026-08-03)
- Embedded `lib_symbols` for every reference used
- **10 x JAE MM70-260B1-R1 SODIMM** connectors (J1..J10) in a horizontal row across the top
- **10 x Samtec ExaMAX-200** mezzanine connectors (J11..J20) in a horizontal row across the bottom
- **BCM56780** (U1) - center of the sheet
- **Aries PT4** PCIe Gen5 retimer (U2) - left of switch
- **UCD90320** 32-rail power sequencer (U3) - right of switch
- **NCT6116** BMC (U4)
- **SLB9670** TPM 2.0 (U5)
- **TPS543x** buck-regulator block (U6) with input bulk cap (C1), input decouple (C2), output bulk (C3), output decouple (C4), feedback divider (R1, R2)
- **2 x ATX24** PSU input connectors (J21, J22) for the redundant 1500 W Titanium PSUs
- Power flags: `+12V`, `+5V`, `+3V3`, `+1V8`, `+0V9`, `GND`
- Illustrative wires + labels: `+12V` from ATX24 to buck input, `+5V` on
  buck output, `PMBUS_CLK/DAT` from UCD90320 to BMC, `ETH0_TX_P` from
  switch to Ryzen0 - just enough to demonstrate the wiring pattern

### Symbol library (`libraries/palpod-compute-backplane.kicad_sym`)

Hand-drawn placeholder symbols. **Pin groupings are functional
abstractions; the EE MUST verify each pin against the manufacturer
datasheet before wiring.**

| Symbol | Pins | Package | Notes |
|---|---|---|---|
| `MM70_260_SODIMM` | 260 | JAE MM70-260B1-R1 | PCIe/USB/UART/I2C/HDMI/DP/CSI groups |
| `SAMTEC_EXAMAX_200` | 200 | Samtec ExaMAX 56G | PCIe Gen5 x8 + 100GbE x4 + USB3 + JTAG + power |
| `BCM56780` | ~180 | HFCBGA-1300 | 32 SerDes quads + PCIe host + JTAG + PMBus + power (grouped; real device is 1300 balls) |
| `ARIES_PT4` | ~80 | BGA-544 | 8 upstream + 8 downstream PCIe Gen5 lanes + REFCLK + I2C mgmt |
| `UCD90320` | ~75 | BGA-173 | 32 EN outs + 32 PGOOD ins + PMBus + JTAG |
| `NCT6116` | ~50 | LQFP-128 | 6 fan tach/PWM + pump tach/PWM + 5 temp ADCs + SPI + I2C + LED outs |
| `TPS543x` | 16 | QFN-16 5x5 | Buck regulator with feedback + SS_TR + PGOOD |
| `SLB9670` | 12 | TSSOP-28 | TPM 2.0 SPI |
| `ATX24` | 24 | Molex 39-01-2240 | ATX main power input |

### Footprint library (`libraries/palpod-compute-backplane.pretty/`)

Placeholder outlines with correct package footprint (body size, pad
positions on a regular grid, pin 1 markers, silkscreen/courtyard/fab
layers).  **These are geometrically correct enough to place on the board
but the exact pad shapes and ball map MUST be verified against the
manufacturer drawing before ordering fab.**

- `MM70_260_SODIMM.kicad_mod` - 2 rows of 130 pads, 0.5 mm pitch, 68x5 mm body
- `SAMTEC_EXAMAX_200.kicad_mod` - 4 rows of 50 pads, 0.8 mm pitch
- `BCM56780_HFCBGA1300.kicad_mod` - 36x36 BGA grid, 1 mm pitch, 40x40 mm body
- `ARIES_PT4_BGA544.kicad_mod` - 24x24 BGA grid, 1 mm pitch, 24x24 mm body
- `UCD90320_BGA173.kicad_mod` - 15x12 BGA grid, 1 mm pitch, 15x12 mm body
- `NCT6116_LQFP128.kicad_mod` - 32 pads x 4 sides, 0.5 mm pitch, 20x20 mm body
- `TPS543x_QFN.kicad_mod` - QFN-16 + thermal pad, 0.65 mm pitch, 5x5 mm body
- `SLB9670_TSSOP28.kicad_mod` - TSSOP-28, 0.65 mm pitch, 4.4x9.7 mm body
- `ATX24_HEADER.kicad_mod` - 2 rows of 12 through-hole pins, 4.2 mm pitch

### PCB (`.kicad_pcb`)

- 14 copper layers matching the project stackup, ENIG finish, Megtron 6 dielectric
- **450 mm x 300 mm rectangular** board outline drawn on `Edge.Cuts`
- 6 M3 mounting holes (4 corners + 2 mid-edges)
- Nets pre-defined: `GND`, `+12V`, `+5V`, `+3V3`, `+1V8`, `+0V9`,
  `PMBUS_*`, `SYS_*`, `PCIE_REFCLK_P/N`, plus **128 ETH lane nets**
  (`ETH0_TX_P` .. `ETH31_RX_N`) and **320 PCIe lane nets**
  (`RYZEN0_PCIE0_TX_P` .. `RYZEN9_PCIE7_RX_N`)
- Silkscreen title block + rev A0 marker + fab note pointing at the block diagram
- No footprints placed yet - the EE places them during layout

## What's stubbed / next steps for the EE

- [ ] **Verify placeholder symbol pin maps against manufacturer datasheets.**
  Every symbol here is a black-box abstraction; the pin numbers/names
  chosen are best-guess groupings. Broadcom, Astera, JAE, Samtec, TI,
  Nuvoton and Infineon each ship a full pin-out. Update
  `libraries/palpod-compute-backplane.kicad_sym` before wiring.
- [ ] **Verify placeholder footprints against manufacturer land-pattern
  drawings.** Body sizes are correct; exact pad shapes/sizes/ball maps
  need to match the mechanical drawing.  Especially critical for the
  BCM56780 HFCBGA-1300 (thermal pad, dummy balls, corner keepouts).
- [ ] Wire the schematic:
  - **PCIe Gen 5 x4 from each of 10 Ryzen ExaMAX slots to the Aries PT4
    retimer** (downstream side), then Aries upstream x16 fanned to the
    BCM56780 host PCIe. That's 80 PCIe TX/RX lanes = 160 diff pairs.
  - **100 GbE from each of the 20 slots to the BCM56780** (10 Jetson +
    10 Ryzen), plus SFP28/QSFP uplink ports. Route via the switch's 32
    SerDes quads on layers SIG2/SIG3.
  - **PCIe REFCLK distribution** - 100 MHz HCSL from a central buffer
    (IDT 9DBL0651 or similar - add to schematic) to each slot and to
    the Aries and BCM56780.
  - **PMBus (I2C)** from UCD90320 to the 40+ regulator ICs and to the BMC.
  - **Power sequencing**: 40 EN outputs from UCD90320 to per-slot and
    per-rail buck regulators; 40 PGOOD returns.
  - **BMC fan/pump control** - 6 fan tach + 6 fan PWM + pump tach + pump
    PWM, plus 5 thermal ADC channels (cold-plate, radiator inlet/outlet,
    ambient, PSU) and a leak-detect input.
  - **TPM SPI** from the boot Ryzen (Ryzen 0) to the SLB9670.
  - **Reset/sequencing tree** - power-good chain from ATX24 PWR_OK to
    UCD90320 to each SoM's RESET_L via level shifters.
  - **ESD/inrush protection** on the +12V input (TVS diodes, hot-swap
    controller like LTC4225 for hot-plug support).
- [ ] **Duplicate and instantiate the TPS543x block** for every rail:
  a full realization needs ~40 buck regulators. Sketch the family tree:
  12V -> 5V (10x, per slot), 12V -> 3.3V (10x), 12V -> 1.8V (10x),
  12V -> 0.9V core (10x, PMBus-controlled adaptive VID).
- [ ] Run ERC to zero (`kicad-cli sch erc palpod-compute-backplane.kicad_sch`).
  Current stub produces ~6600 violations, essentially all "power pin not
  driven" and "pin not connected" - expected consequences of the placed-but-unwired
  connectors and giant switch chip; drive them down as wiring is added.
- [ ] Assign every schematic symbol a valid footprint (Tools -> Assign Footprints).
- [ ] Update the PCB from the schematic (Tools -> Update PCB from Schematic).
- [ ] Place footprints on the 450x300 mm board:
  - 10 Jetson SODIMMs in a horizontal row along the top edge
  - 10 Ryzen ExaMAX slots in a horizontal row along the bottom edge
  - BCM56780 centered between the two rows (thermal considerations - needs
    a heatsink; leave keepout for cold-plate)
  - Aries PT4 immediately adjacent to the switch on the Ryzen side
  - UCD90320, BMC, TPM, RTC clustered near the ATX24 input on one edge
  - Buck regulators distributed close to their load slots
  - PSU input connectors (ATX24 x2) on one edge, near a hot-swap controller
- [ ] **Impedance-controlled routing (6-12 weeks of SI engineering).**
  - 100 ohm diff pair for 100 GbE lanes with matched length within a
    quad, skew budget per Broadcom BCM56780 SI guide.
  - 85 ohm diff pair for PCIe Gen 5 (Aries retimer at ~10 in trace).
  - Run S-parameter simulations in Ansys SIwave or Cadence Sigrity.
  - Route on internal signal layers (SIG1/SIG2/SIG3/SIG4) with GND
    reference on both sides.
  - Watch via stub effects at 32 GT/s; back-drill required through-hole
    vias, or use blind/buried vias.
- [ ] Power plane splitting: PWR12V zone poured on In5.Cu with heavy
  copper (2 oz or bus bars for 200 A+); split PWR3V3/PWR1V8/PWR_ANALOG
  on their dedicated planes with return-current-aware splits per the
  fabric's requirements.
- [ ] Thermal management: cold-plate keepouts for the BCM56780 heatsink,
  Ryzen SBC coldplates, Jetson coldplates. Coordinate with mechanical.
- [ ] Chassis grounding: chassis-to-signal GND connection via a spark
  gap or 1 nF cap + 1 M ohm resistor pattern at the ATX24 input.
- [ ] Add fiducial marks (3 per side) for pick-and-place.
- [ ] Silkscreen: full reference designators, slot numbers on the
  connector row, signal names at test points.
- [ ] Run DRC to zero (current stub is 0 violations because nothing is
  routed).
- [ ] Generate Gerbers + drill + BOM + pick-and-place (File -> Fabrication
  Outputs). This is a **14-layer HDI board with Megtron 6** - not a
  hobby-fab candidate. Realistic vendors: **Advanced Circuits, Sanmina,
  TTM, or Chin-Poon**. Expect >$3000/board for a proto run and 4-6 week
  turn.

## Command-line validation

The project has been validated with `kicad-cli` 10.0.5:

```
kicad-cli sch export netlist -o /tmp/net.net       palpod-compute-backplane.kicad_sch  # succeeds
kicad-cli pcb export gerbers  -o /tmp/g/           palpod-compute-backplane.kicad_pcb  # succeeds; 14 copper layers
kicad-cli pcb drc             -o /tmp/drc.rpt      palpod-compute-backplane.kicad_pcb  # 0 violations
kicad-cli sch erc             -o /tmp/erc.rpt      palpod-compute-backplane.kicad_sch  # ~6600 violations expected (unwired stub)
kicad-cli sym export svg      -o /tmp/sym-svg/     libraries/palpod-compute-backplane.kicad_sym  # renders 9/9
kicad-cli fp  export svg      -o /tmp/fp-svg/      libraries/palpod-compute-backplane.pretty     # renders 9/9
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
- `power` (+12V, +5V, +3V3, +1V8, +0V9, GND) - also embedded in the schematic for offline opening

The project-local `palpod-compute-backplane` library (registered by
`sym-lib-table` / `fp-lib-table`) holds the specialty ICs and their
placeholder footprints.

## Reference

- **Block-level architecture:** `../../block-diagrams/compute-backplane.md`
- **System overview:** `../../block-diagrams/system-overview.md`
- **Template project:** `../palpod-mic-array/` (same layout and validation approach)
- **Regenerating the project:** `scratchpad/gen.py` writes every file
  deterministically; edit it and re-run (`python3 scratchpad/gen.py`) to
  rebuild.

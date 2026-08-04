# PAL Pod Halbach Levitation Controller — KiCad Project

**SAFETY-CRITICAL BOARD.** This is the real-time active stabilization
controller for the Halbach neodymium levitation array that holds the OLED orb
in front of the column. A control failure means a 2 kg glass sphere becomes a
projectile aimed at the user's rug (or foot). Treat every net, every symbol,
and every layout decision on this board as safety-critical until proven
otherwise via FMEA.

> ⚠️  **SAFETY REVIEW REQUIRED BEFORE POWER-ON.** Before energizing the 48 V
> coil rail for the first time — even on the bench — a licensed EE must sign
> off on the following in writing:
>
> 1. **Overcurrent latch verified.** TL331 (`U4`) trips the DRV8323 nFAULT
>    line when the summed INA240 output exceeds the hardware threshold
>    (target 30 A per phase). Bench-verify with a current-limited supply and
>    a scope; do not rely on datasheet values.
> 2. **Watchdog window verified.** MAX706 (`U3`) issues RESETn if the primary
>    STM32H723 misses a WDI pet in the 100 ms window. Firmware halts must be
>    provably caught in < 110 ms end-to-end.
> 3. **E-stop opens the coil rail in < 10 ms.** The rear-panel E-stop must
>    drive the MAX706 MR pin *and* an in-line contactor on the 48 V rail —
>    software must not be in the critical path. Latching; reset requires
>    physical button press.
> 4. **Lockstep pair agrees.** Both `U1` and `U2` (STM32H723ZGT6) compute the
>    same servo output every 100 µs; disagreement > tolerance latches
>    SAFE-SHUTDOWN (coils de-energize, catch-net engages, orb comes down
>    controlled).
> 5. **Drop-catch net installed.** The internal catch-net inside the column
>    is present and rated for the orb's terminal drop energy from full
>    levitation height.
> 6. **Magnetic-field survey.** Exterior surface field < 100 µT at maximum
>    coil current per ICNIRP 2020 general-public reference levels. Test with
>    a Narda ELT-400 or equivalent.
> 7. **Pacemaker / ISO 7010 W006 warning label** applied to the column at
>    the top plate and included in the setup manual.

See `../../block-diagrams/levitation-controller.md` for the system-level
control loop, latency budget, fault-response matrix, and regulatory notes.

## How to open

Requires **KiCad 8.0.0 or later** (KiCad 9 and 10 also open cleanly;
we developed and validated against KiCad 10.0.5 on macOS).

```
open -a KiCad /private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/electrical/kicad/palpod-halbach-controller/palpod-halbach-controller.kicad_pro
```

Or double-click `palpod-halbach-controller.kicad_pro` in Finder. From KiCad's
project manager, open **Schematic Editor** and **PCB Editor**.

Project-local symbol and footprint libraries live in `libraries/`; the
`sym-lib-table` and `fp-lib-table` at the project root register them under the
alias `palpod-halbach-controller`. Standard KiCad symbols (`Device:R`,
`Device:C`, `power:*`) are embedded in the schematic's `lib_symbols` block so
the schematic opens even on a fresh KiCad install that has not yet configured
its stock libraries.

## What's populated

- [x] `.kicad_pro`: 4-layer stackup, ENIG, JLCPCB-friendly minimums, and
      **five net classes**:
    - `Default` — 0.2 mm signal
    - `Power` — 0.5 mm rails
    - `COIL_HIGH_CURRENT` — **5.0 mm min width, 2.0 mm vias**, orange in
      the PCB editor; auto-assigned to `COIL_*`, `PHASE_*`, `PVDD`, `PGND`.
    - `CAN_FD_DIFF` — 100 Ω differential CAN-FD pair (`CANH`/`CANL`)
    - `SAFETY_CRITICAL` — pink; auto-assigned to `ESTOP*`, `OC_LATCH*`,
      `WDOG*`, `nFAULT*`, `LOCKSTEP*`
- [x] `.kicad_sch` root schematic on A2 with populated title block
      (rev A0, 2026-08-03), embedded `lib_symbols` for every reference used.
- [x] Placed symbols:
    - 2× STM32H723ZGT6 (`U1` primary, `U2` redundant) — the lockstep pair
    - 1× MAX706 window watchdog supervisor (`U3`)
    - 1× TL331 hardware overcurrent comparator (`U4`)
    - 1× MCP2542FD CAN-FD transceiver (`U5`)
    - 1× STM32G030K8T6 aux housekeeping MCU (`U6`)
    - 6× MLX90393 3D hall-effect sensors (`U7`…`U12`)
    - 6× DRV8323 gate drivers (`U13`…`U18`)
    - 12× IPI050N06N MOSFETs (`Q1`…`Q12`) — one half-bridge per driver
    - 6× INA240 current-sense amps (`U25`…`U30`)
    - 1× Recom RTK-2412 isolated DC-DC brick (`U10`) for driver rail
      isolation
    - Bulk + local decoupling capacitors, shunt resistors, pull-ups
    - Power flags: `+48V`, `+12V`, `+5V`, `+3V3`, `GND`, `GNDA`, `PGND`
- [x] Three big red-bordered safety-callout banners on the schematic
      explicitly labeling the `OC_LATCH`, `ESTOP_LATCH`, and `LOCKSTEP_A/B`
      net groups as `SAFETY-CRITICAL — DO NOT REMOVE`.
- [x] Illustrative wires and 40+ pre-placed labels seeding the wiring
      pattern: `LOCKSTEP_A_MOSI/MISO/SCK`, `LOCKSTEP_B_MOSI/MISO/SCK`,
      `WDOG_WDI`, `WDOG_RESETn`, `ESTOP_LATCH`, `ESTOP_IN`, `OC_LATCH`,
      `OC_SUM_IN`, `CAN_TXD`, `CAN_RXD`, `CANH`, `CANL`,
      `HALL0_SDA` … `HALL5_DRDY`, `COIL_1_HIGH` … `COIL_6_LOW`,
      `OC_CH1` … `OC_CH6`.
- [x] `no_connect` flags on illustrative test pins.
- [x] `libraries/palpod-halbach-controller.kicad_sym` — hand-drawn symbols
      for **10 specialty parts**: STM32H723ZGT6 (LQFP-144), DRV8323
      (HTSSOP-48 EP), INA240 (TSSOP-8), MLX90393 (QFN-16), MAX706 (SO-8),
      MCP2542FD (SO-8), TL331 (SOT-23-5), IPI050N06N (TO-262), STM32G030K8T6
      (LQFP-32), RTK-2412 (SIP-4). **Pin mappings are placeholder
      groupings — the EE must verify each pin against the manufacturer
      datasheet before wiring.**
- [x] `libraries/palpod-halbach-controller.pretty/` — twelve placeholder
      footprints. See `libraries/palpod-halbach-controller.pretty/README.md`
      for per-part verification checklist.
- [x] `.kicad_pcb`: 4-layer stackup declared
      (`F.Cu` signal 2 oz / `In1.Cu` GND 1 oz / `In2.Cu` PWR_HIGH_CURRENT
      1 oz / `B.Cu` signal 2 oz), 1.6 mm total, ENIG finish.
      **150 × 100 mm rectangular Edge.Cuts** drawn. Silkscreen and
      SAFETY.Callouts (`User.1`) layer notes populated. No footprints placed
      yet — the EE places them during layout.
- [x] `sym-lib-table` / `fp-lib-table` register the project-local
      `palpod-halbach-controller` library.

## What's stubbed / next steps for the EE

- [ ] **Verify placeholder footprints against real datasheets** before ordering
      fab. See `libraries/palpod-halbach-controller.pretty/README.md`. The
      MOSFET and DRV8323 placeholders in particular are safety-critical — a
      wrong pad on the current-sense pins would defeat the OC latch.
- [ ] **Verify placeholder pin mappings** on all specialty symbols against the
      manufacturer datasheets. Update
      `libraries/palpod-halbach-controller.kicad_sym` with correct pin numbers,
      names, and electrical types.
- [ ] **Complete the schematic wiring** — this is a placeholder; the EE draws
      the actual nets. Priorities in this order:
    1. **Lockstep interconnect** (`U1` ↔ `U2` SPI cross-strap) — this is what
       makes the board single-fault tolerant.
    2. **OC latch chain** — 6× INA240 outputs sum into TL331 (`U4`) input,
       comparator output latches through an SR flip-flop, drives all
       DRV8323 nENABLE lines low. Independent of MCU firmware.
    3. **Watchdog chain** — U1 pets MAX706 WDI; MAX706 RESETn drives an
       AND gate on the enable path.
    4. **E-stop chain** — hardwired E-stop input → MAX706 MR → coil-rail
       contactor coil. Two-channel, redundant per SIL-2 practice.
    5. **CAN-FD bus** — U1/U2 FDCAN1 → MCP2542FD → CANH/CANL termination
       (120 Ω split-terminate at each end of the bus).
    6. **Hall sensor bus** — I2C bus (with per-sensor A0/A1 straps for
       unique addresses) or SPI daisy-chain from U1. Route as star from
       the MCU quadrant; twist pairs on the flex cable side.
    7. **6× DRV8323 SPI config + PWM** — SPI shared, 6× nSCS individual;
       6× (INHA/INLA/INHB/INLB/INHC/INLC) from timer channels.
    8. **48 V rail** — 12 V input → RTK-2412 isolation → LM5155 boost →
       coil rail. Bulk 470 µF / 100 V polymer at each DRV8323 PVDD pin
       plus one 1 mF electrolytic per pair.
    9. **Power tree** — 12 V → 5 V (LMR33630) → 3.3 V (TPS7A20) for logic;
       separate 3.3 V analog rail (`+3V3A`) for INA240 REF pins.
    10. **Decoupling** — 100 nF within 3 mm of every power pin; add
        4.7 µF bulk per rail per IC.
- [ ] Add ESD protection on the E-stop input (`PESD5V0L1BA`) and the CAN
      bus (`PSD03C-LF`).
- [ ] Add optional galvanic isolation on the CAN bus if the main-compute
      board runs on a different ground reference.
- [ ] Assign every schematic symbol a valid footprint (Tools → Assign
      Footprints). Cross-check each MOSFET pad against the datasheet
      before assigning.
- [ ] Update the PCB from the schematic (Tools → Update PCB from Schematic
      in the PCB editor).
- [ ] Place footprints on the 150 × 100 mm board:
    - **Coil-driver quadrant** on the right half of the board with the
      six DRV8323 + MOSFET pairs in a row along the top edge; INA240
      shunt-amps immediately downstream; 2-pin screw terminals for the
      coil outputs on the right board edge.
    - **MCU quadrant** on the left half; lockstep pair placed
      symmetrically about the vertical midline to keep cross-strap
      trace lengths matched.
    - **MAX706 + TL331 + estop terminal + fault-latch logic** in the
      bottom-center, straddling the moat between quadrants.
    - **CAN-FD transceiver + connector** on the left edge.
    - **Hall-sensor flex connectors** across the bottom edge (6× JST-PH
      or FPC, TBD by mechanical team).
- [ ] Pour GND (`In1.Cu`) — split zone with a **moat between the
      analog/logic and coil-driver domains**, tied at a single point near
      the ADC reference.
- [ ] Pour high-current PWR (`In2.Cu`) — divide into 48 V, 12 V, and 5 V
      zones; use polygon copper for the 48 V zone in the coil-driver
      quadrant. Target 5 mm min width on all `COIL_HIGH_CURRENT` traces on
      outer layers (2 oz copper handles ~30 A at this width with modest
      temperature rise).
- [ ] Route CAN-FD as a 100 Ω differential pair. Route lockstep SPI as
      length-matched pair between the two MCUs.
- [ ] Run ERC (`kicad-cli sch erc` or Tools → Electrical Rules Checker) —
      the placeholder generates violations; drive them to zero.
- [ ] Run DRC (`kicad-cli pcb drc` or Tools → Design Rules Checker) to
      zero, including `SAFETY_CRITICAL` clearance = 0.4 mm.
- [ ] **Formal design review** with a second EE (independent of the
      designer) covering the safety chain, current paths, and layout of
      the OC / WDT / lockstep / e-stop nets.
- [ ] **FMEA / DFMEA** covering every failure mode in the fault-response
      matrix in `levitation-controller.md`.
- [ ] Generate Gerbers + drill + BOM + pick-and-place
      (`File → Fabrication Outputs`). Cross-check the BOM against the block
      diagram.
- [ ] Order 5-unit proto run from JLCPCB (4-layer, 2 oz outer, ENIG,
      ~2-week turn).

## Command-line validation

The project has been validated with `kicad-cli` 10.0.5:

```
kicad-cli sch export netlist -o /tmp/palpod-halbach.net palpod-halbach-controller.kicad_sch
kicad-cli pcb export gerbers -o /tmp/g/                 palpod-halbach-controller.kicad_pcb
kicad-cli sym export svg     -o /tmp/sym-svg/           libraries/palpod-halbach-controller.kicad_sym
kicad-cli fp  export svg     -o /tmp/fp-svg/            libraries/palpod-halbach-controller.pretty
```

## File format

- Schematic schema version `20231120` (KiCad 8)
- PCB schema version `20240108` (KiCad 8)
- Symbol library schema version `20231120`
- Footprint schema version `20240108`

Written in the `(hide yes)` effect-block form so the same files load
identically under KiCad 8, 9, and 10.

## Certifications targeted (product-level, not board-level)

- **UL 60335** (Household and similar electrical appliances — Safety) for
  the appliance as a whole.
- **FCC Part 15** subpart B (unintentional radiator) — switching noise from
  the DRV8323 stage is the primary risk. Add pre-compliance scanning as
  early as possible.
- **ICNIRP 2020** general-public magnetic-field reference levels — verify
  at the column exterior surface under worst-case coil current.
- **FDA notice for magnetic-field-near-pacemaker** — product-level, not
  board-level, but the PCB silkscreen carries the ISO 7010 W006 icon.

## Reference

- **System-level block diagram, latency budget, fault-response matrix:**
  `../../block-diagrams/levitation-controller.md`

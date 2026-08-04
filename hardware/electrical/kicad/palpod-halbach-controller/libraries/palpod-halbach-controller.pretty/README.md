# palpod-halbach-controller.pretty — PLACEHOLDER footprints

These `.kicad_mod` files are **starter outlines only**. They compile in
KiCad 8+ and give the schematic a valid footprint reference so the project
opens end-to-end, but the pad positions, sizes, and pin numbering are
best-effort approximations, not fabrication-ready.

**Before releasing to fab, the EE must verify every pad against the datasheet
of the actual package** and either re-generate these footprints from a
trusted source (SnapEDA, Ultra Librarian, IPC-7351 calculator, manufacturer
library) or hand-tune them to match the datasheet's recommended land pattern.

For a safety-critical board, an incorrect footprint on the MOSFET
source/drain, DRV8323 current-sense pins, or hall-sensor I2C address straps
would silently defeat the corresponding safety chain — treat this list as an
explicit gating checklist.

## Files

- `LQFP-144_20x20mm_P0.5mm.kicad_mod` — STMicro STM32H723ZGT6 primary and
  redundant MCU package. Verify against `RM0468` § "STM32H723ZG package
  information".
- `HTSSOP-48_6.1x12.5mm_P0.5mm_EP.kicad_mod` — TI DRV8323 (PWP package)
  gate driver. Exposed pad **must** be tied to GND with a via array;
  incorrect thermal pad handling causes intermittent shutdown under load.
- `TSSOP-8_4.4x3mm_P0.65mm.kicad_mod` — INA240 (D package) current-sense
  amp. Verify `IN+`/`IN-` pin order — reversal inverts the OC latch sense.
- `QFN-16_3x3mm_P0.5mm.kicad_mod` — Melexis MLX90393. Verify the I2C
  address straps (`A0`, `A1`) route to the correct board test-points so
  the six sensors get unique addresses.
- `SOIC-8_3.9x4.9mm_P1.27mm.kicad_mod` — MAX706 supervisor and MCP2542FD
  CAN-FD transceiver share this generic SO-8 footprint. Pin-1 marker
  correct for both.
- `SOT-23-5.kicad_mod` — TI TL331 comparator (DBV package).
- `TO-262-3_TabPin2.kicad_mod` — Infineon IPI050N06N N-channel MOSFET.
  Tab is drain, connects to pin 2. Ensure the drain copper pour connects
  to both pin 2 and the tab pad for adequate heatsinking.
- `LQFP-32_7x7mm_P0.8mm.kicad_mod` — STM32G030K8T6 aux MCU.
- `SIP-4_Recom_RTK.kicad_mod` — Recom RTK-2412 isolated DC-DC brick.
  Note the isolation gap requirement: no traces or planes may bridge the
  1500 VDC isolation barrier on the board.
- `Screw_Terminal_2Pin_5.08mm.kicad_mod` — 2-pin screw terminal used for
  each coil output. 5.08 mm pitch, rated ≥ 30 A.
- `JST-PH_4Pin.kicad_mod` — 4-pin JST-PH connector for the hall-sensor
  flex cable (VDD/SDA/SCL/GND).
- `Estop_Terminal_2Pin.kicad_mod` — 2-pin screw terminal for the hardwired
  E-stop input.

## Attributes

All footprints are marked `(attr smd)` (except the terminals) and populate:

- F.Fab / F.SilkS / F.CrtYd outlines
- A pin-1 indicator circle on F.SilkS
- SMD pads on F.Cu / F.Paste / F.Mask
- No 3D model reference (add `(model "${KIPRJMOD}/3d/<part>.step" ...)`
  when a model becomes available)

## Verification checklist (per footprint)

1. Cross-check package dimensions against the datasheet mechanical drawing.
2. Cross-check pad size and pitch against the recommended land pattern.
3. Cross-check pin-1 marker position against the datasheet pin/ball map.
4. Cross-check the courtyard against IPC-7351 (level B nominal for logic,
   level A dense not recommended for a safety-critical board).
5. Add solder-paste apertures / paste stencil reductions if manufacturer
   recommends them (HTSSOP EPs and QFN thermal pads usually do).
6. **MOSFET / DRV8323 / current-sense specific:** verify the current
   handling of the pad-to-copper connection is adequate for the peak
   30 A per-phase current with acceptable temperature rise.

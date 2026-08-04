# palpod-orb.pretty — PLACEHOLDER footprints

These `.kicad_mod` files are **starter outlines only**. They compile in KiCad 8+
and give the schematic a valid footprint reference so the project opens
end-to-end, but the pad positions, sizes, and pin numbering are best-effort
approximations, not fabrication-ready.

**Before releasing to fab, the EE must verify every pad against the datasheet
of the actual package** and either re-generate these footprints from a trusted
source (SnapEDA, Ultra Librarian, IPC-7351 calculator, manufacturer library)
or hand-tune them to match the datasheet's recommended land pattern. The
BGA/QFN packages here also need thermal-pad geometry and mask openings that
match the manufacturer's recommendations — currently only stub outlines are
provided.

## Files

- `nRF54H20_aQFN94.kicad_mod` — Nordic nRF54H20 aQFN94 (approximated as a
  76-pad perimeter QFN on 0.4 mm pitch, 7×7 mm body). Real nRF54H20 has 94
  pads on a matrix pattern and requires an epoxy-molded thermal keepout;
  regenerate from the Nordic footprint pack before layout.
- `TC358748_BGA80.kicad_mod` — Toshiba TC358748 MIPI CSI bridge (BGA80,
  ~5.6×5.6 mm on 0.5 mm pitch, 4 corner balls depopulated). Verify against
  Toshiba's package outline drawing.
- `SSD1963_LFBGA121.kicad_mod` — Solomon Systech SSD1963 OLED driver as an
  11×11 mm LFBGA121 (0.8 mm pitch). Used here as the **placeholder** for the
  proprietary curved-OLED source driver in the spec. Swap in the actual
  vendor driver's footprint before fab.
- `S3_LIDAR_UART10.kicad_mod` — 10-pin 1.0 mm pitch through-hole header for
  the Slamtec S3 LIDAR pigtail. Verify against the cable spec before drilling.
- `P9418_QFN40.kicad_mod` — Renesas P9418 wireless-power RX (QFN40,
  6×6 mm, 0.5 mm pitch). Verify pad size and thermal pad against Renesas
  package outline.
- `TMR2305_SOT23-5.kicad_mod` — TDK TMR2305 magnetoresistive sensor
  (SOT-23-5). Standard SOT-23-5 land pattern; verify against IPC-7351.
- `VL53L8_LGA16.kicad_mod` — ST VL53L8 ToF sensor (LGA16, ~6.4×3.0 mm,
  0.5 mm pitch). Verify against ST datasheet including optical window
  keepout.
- `FPC28_0.5mm_ZIF.kicad_mod` — 28-pin 0.5 mm FPC ZIF connector for
  Sony IMX415 camera flex cables. Verify against the specific Molex /
  Amphenol / JST part chosen for the pigtail; mounting-pad geometry and
  cable insertion direction differ between vendors.
- `FPC40_0.5mm_ZIF.kicad_mod` — 40-pin 0.5 mm FPC ZIF connector for the
  curved-OLED cable out to the panel. Same caveats as FPC28.
- `BQ25798_QFN29.kicad_mod` — TI BQ25798 buck-boost battery charger
  (QFN29, 4×4 mm, 0.4 mm pitch) with central thermal pad. Verify PGND
  thermal-pad geometry — a bad thermal pad here can wreck efficiency.
- `M2_2230_KeyAE.kicad_mod` — M.2 2230 Key A+E socket for the Wi-Fi 7
  module. Placeholder uses 75 continuous pads on one edge; the real socket
  is a two-row edge-connector with a keying notch (Key A at pins 8-15,
  Key E at pins 24-31). Replace with a proper M.2 socket footprint from
  Amphenol / Molex / TE before fab.

## Attributes

All footprints:

- `(attr smd)` (except the LIDAR header, which uses through-hole pads)
- F.Fab / F.SilkS / F.CrtYd outlines
- Pin-1 indicator circle on F.SilkS
- SMD pads on F.Cu / F.Paste / F.Mask; PTH pads on `*.Cu / *.Mask`
- No 3D model reference (add `(model "${KIPRJMOD}/3d/<part>.step" ...)`
  when a model becomes available)

## Verification checklist (per footprint)

1. Cross-check package dimensions against the datasheet mechanical drawing.
2. Cross-check pad size and pitch against the recommended land pattern.
3. Cross-check pin-1 marker position against the datasheet ball/pad map.
4. Cross-check the courtyard against IPC-7351 (level B nominal; use A dense
   only where the ring geometry forces it).
5. Add solder-paste apertures / paste stencil reductions if the manufacturer
   recommends them (thermal pads on QFNs almost always need windowpane
   apertures).
6. For flex-mounted parts (any part landing on the flex bridge), ensure the
   pads are on both F.Cu and B.Cu as required, and add an adhesive or
   stiffener callout on B.Adhes / F.Adhes.

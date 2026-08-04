# palpod-extender-sbc.pretty - PLACEHOLDER footprints

These `.kicad_mod` files are **starter outlines only**. They compile in KiCad 8+
and give the schematic a valid footprint reference so the project opens
end-to-end, but the pad positions, sizes, and pin numbering are best-effort
approximations, not fabrication-ready.

**Before releasing to fab, the EE must verify every pad against the datasheet
of the actual package** and either re-generate these footprints from a trusted
source (SnapEDA, Ultra Librarian, IPC-7351 calculator, manufacturer library)
or hand-tune them to match the datasheet's recommended land pattern.

## Files

- `RK3588_FCBGA948.kicad_mod` - Rockchip RK3588 FCBGA-948, 0.75 mm pitch, approx 24x24 mm. 32x32 ball grid with the four 2x2 corners depopulated. Real RK3588 has a complex non-uniform ball map with several depopulated interior regions; regenerate from the RK3588 datasheet before fab.
- `RK806_QFN68.kicad_mod` - Rockchip RK806 PMIC, QFN-68, 0.5 mm pitch, 9x9 mm with exposed thermal pad.
- `M2_A_E_2230.kicad_mod` - M.2 A+E key edge socket for 2230-length modules (Wi-Fi/BT). 75 edge-card pads, 0.5 mm pitch, plus a mounting screw hole at 30 mm from the socket.
- `CS43198_QFN32.kicad_mod` - Cirrus Logic CS43198 stereo DAC, QFN-32, 0.5 mm pitch, 5x5 mm.
- `TPA3255_HTQFP44.kicad_mod` - TI TPA3255 315 W class-D amp, HTQFP-44, 0.65 mm pitch, 10x10 mm with exposed thermal pad (heat-sink required).
- `CCG3PA_QFN40.kicad_mod` - Infineon CYPD3175 (CCG3PA) USB-PD sink controller, QFN-40, 0.4 mm pitch, 5x5 mm.
- `LPDDR5_FBGA315.kicad_mod` - Samsung K3LKBFB0EM 8 GB LPDDR5 octa-die FBGA-315, 0.5 mm pitch, ~12x11 mm with corners depopulated.

## Attributes

All footprints are marked `(attr smd)` and populate:
- F.Fab / F.SilkS / F.CrtYd outlines
- A pin-1 indicator circle on F.SilkS
- SMD pads on F.Cu / F.Paste / F.Mask
- No 3D model reference (add `(model "${KIPRJMOD}/3d/<part>.step" ...)` when a model becomes available)

## Verification checklist (per footprint)

1. Cross-check package dimensions against the datasheet mechanical drawing.
2. Cross-check pad size and pitch against the recommended land pattern.
3. Cross-check pin-1 marker position against the datasheet ball/pad map.
4. Cross-check the courtyard against IPC-7351 (level B nominal).
5. Add solder-paste apertures / paste stencil reductions if manufacturer recommends them (BGAs usually don't; large exposed pads on QFN/HTQFP typically want a partitioned paste stencil).
6. For the RK3588 FCBGA-948 specifically, verify the depopulated interior balls (thermal islands / reserved zones) against the RK3588 datasheet - the placeholder here assumes a uniform grid minus the 4 corners.

# palpod-mic-array.pretty — PLACEHOLDER footprints

These `.kicad_mod` files are **starter outlines only**. They compile in KiCad 8+
and give the schematic a valid footprint reference so the project opens
end-to-end, but the pad positions, sizes, and pin numbering are best-effort
approximations, not fabrication-ready.

**Before releasing to fab, the EE must verify every pad against the datasheet
of the actual package** and either re-generate these footprints from a trusted
source (SnapEDA, Ultra Librarian, IPC-7351 calculator, manufacturer library)
or hand-tune them to match the datasheet's recommended land pattern.

## Files

- `ICS-41352_LGA5.kicad_mod` — TDK InvenSense ICS-41352 5-pin LGA (3.5 x 2.65mm). Pad geometry is a placeholder rectangle grid; real ICS-41352 has a sound port on the *top* (or bottom, depending on package variant) and specific paste-mask requirements around the port. Consult the datasheet section "Recommended PCB Footprint" before fab.
- `XVF3800_LFBGA61.kicad_mod` — XMOS XVF3800-INBW 61-pin LFBGA at 0.65 mm pitch on an 8x8 grid (A1..H8) with A8, H1, H8 depopulated. Ball diameter and land pattern are placeholders; verify against the XMOS XVF3800 datasheet "Package information" section.
- `NDP120_LGA69.kicad_mod` — Syntiant NDP120 69-pin LGA at 0.5 mm pitch, perimeter pads plus a central thermal pad. Syntiant does not publish the pinout publicly (NDA); the pad map here is speculative and must be replaced with the datasheet's land pattern before layout.

## Attributes

All three footprints are marked `(attr smd)` and populate:
- F.Fab / F.SilkS / F.CrtYd outlines
- A pin-1 indicator circle on F.SilkS
- SMD pads on F.Cu / F.Paste / F.Mask
- No 3D model reference (add `(model "${KIPRJMOD}/3d/<part>.step" ...)` when a model becomes available)

## Verification checklist (per footprint)

1. Cross-check package dimensions against the datasheet mechanical drawing.
2. Cross-check pad size and pitch against the recommended land pattern.
3. Cross-check pin-1 marker position against the datasheet ball/pad map.
4. Cross-check the courtyard against IPC-7351 (level B nominal, or level A dense for the mics on the ring).
5. Add solder-paste apertures / paste stencil reductions if manufacturer recommends them (BGAs usually don't; LGAs often do).

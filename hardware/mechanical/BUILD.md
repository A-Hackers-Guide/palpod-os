# Mechanical BUILD — how to use these files

## Prerequisites

- OpenSCAD 2021.01 or newer (2024 nightly recommended for `angle=` on `rotate_extrude`)
  - macOS: `brew install --cask openscad`
  - Ubuntu: `sudo apt install openscad`
  - Windows: https://openscad.org/downloads.html

## Preview

1. Open `palpod-main.scad` (or `palpod-extender.scad`) in OpenSCAD.
2. Press **F5** for fast preview (OpenCSG, low-poly, ~2–5 s).
3. Press **F6** for a full render (CGAL, high-poly, ~30–60 s on modern desktop). Required before STL export.
4. Toggle subassemblies by editing the `SHOW_*` booleans at the top of the file. This is how you inspect the compute bay, amp bay, or orb in isolation.

## Export

- **STL** (mechanical handoff): File → Export → Export as STL. Use these as *starting geometry* for a SolidWorks / Fusion 360 rebuild — do not send them to a machine shop as-is.
- **AMF / 3MF** (color info preserved): File → Export → Export as 3MF. Useful when handing to a designer who wants to see the material assignments.
- **SVG** (dimensional review): rotate the view to front/side/top and File → Export → Export as SVG for 2D drawings.

## Modifying dimensions

**All dimensions live in `constants.scad`.** Never hard-code a number in `modules.scad`, `palpod-main.scad`, or `palpod-extender.scad`. If you need a new dimension:

1. Add it to `constants.scad` with a descriptive `ALL_CAPS_NAME`.
2. Document it with a comment on the same line.
3. Reference it from the module.

## What to hand a mechanical engineer

Send them, in order:

1. **`constants.scad`** — the dimensional spec (what to design to).
2. **`dimensional-drawing.md`** — human-readable envelope + tolerances.
3. **`materials-spec.md`** — 304 SS + walnut + PVD + acoustic foam grades.
4. **STL exports** of `palpod-main.scad` and `palpod-extender.scad` — starting geometry for their SolidWorks model.
5. **Statement of work**: "Reimplement in SolidWorks 2024 with GD&T per ASME Y14.5-2018, DFM callouts, and CAM-ready features (draft angles, radii, tool-access). Deliverable: STEP AP242, PDF drawings with title blocks, and a DFM review report."

## What a mechanical engineer will need from us that isn't here

- FEA vibration modes for the levitation orb cradle
- Acoustic port sizing (Helmholtz resonance) for the subwoofer enclosure volume
- Thermal FEA of the base plinth with radiator + fan curves
- Drop-test spec (IEC 60068-2-31, 100 mm face drop)
- Shipping crate design (ISPM-15 heat-treated pallet, foam-in-place)
- Cable strain-relief and grommet spec for the umbilical between column and orb

## Version pinning

These files are known to preview cleanly on:

- OpenSCAD 2021.01 (stable)
- OpenSCAD 2024.01 dev snapshot (recommended)

If you upgrade OpenSCAD and previews break, likely culprits are `rotate_extrude(angle=…)` (requires 2019.05+) and `minkowski` performance regressions.

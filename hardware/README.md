# PAL Pod Hardware Reference Package

**IMPORTANT — READ THIS FIRST.**

This is a **hardware REFERENCE package**, not a manufacturable design.

- The mechanical files are parametric **OpenSCAD source**. They preview correctly and export usable STL geometry, but they are not a substitute for a proper SolidWorks / Fusion 360 / NX model with GD&T, DFM callouts, and CAM-ready features.
- The electrical files are **block-level diagrams and reference architectures**. They are not schematics, not layouts, and definitely not Gerbers. A real hardware EE will re-implement them in KiCad 8+ (or Altium) with proper symbol libraries, ERC/DRC, and impedance-controlled stackups.
- The thermal, connectivity, and certification documents are **plans and budgets**, not simulation results.

**Everything a hired engineer needs on day one is here.** Nothing more, nothing less.

## What this package IS

- A complete, self-consistent architectural picture of the PAL Pod main column and extender.
- Real part numbers, real material grades, real block topologies.
- A junior-EE-actionable reference design for the far-field mic array (the hardest board).
- A first-day onboarding doc for the hardware EE the founder hires.

## What this package is NOT

- A BOM procurement package (top-level critical parts only — `electrical/bom-summary.md`).
- A safety certification submission.
- A tooling package for a contract manufacturer.
- An FEA / CFD / SPICE simulation record.

## File tree

```
hardware/
├── README.md                    <-- you are here
├── mechanical/
│   ├── palpod-main.scad
│   ├── palpod-extender.scad
│   ├── modules.scad
│   ├── constants.scad
│   ├── BUILD.md
│   ├── dimensional-drawing.md
│   └── materials-spec.md
├── electrical/
│   ├── block-diagrams/
│   │   ├── system-overview.md
│   │   ├── compute-backplane.md
│   │   ├── audio-amp.md
│   │   ├── mic-array.md
│   │   ├── orb.md
│   │   ├── levitation-controller.md
│   │   └── extender.md
│   ├── mic-array-reference-design.md
│   ├── power-tree.md
│   └── bom-summary.md
├── thermal/
│   ├── thermal-budget.md
│   └── airflow-diagram.md
├── connectivity/
│   ├── wireless-plan.md
│   └── uwb-orb-tracking.md
└── docs/
    ├── ARCHITECTURE.md
    ├── DFM-CHECKLIST.md
    ├── CERTIFICATION-PLAN.md
    └── FIRST-EE-DAY-ONE.md
```

## Recommended reading order

1. `docs/ARCHITECTURE.md` — system-level picture
2. `electrical/block-diagrams/system-overview.md` — top-level block diagram
3. `mechanical/dimensional-drawing.md` — physical envelope
4. `thermal/thermal-budget.md` — the number that constrains everything else
5. `electrical/power-tree.md` — the second number that constrains everything else
6. `electrical/mic-array-reference-design.md` — the first board a new EE should own
7. `docs/DFM-CHECKLIST.md` and `docs/CERTIFICATION-PLAN.md`

For a new hire: hand them `docs/FIRST-EE-DAY-ONE.md`.

## Units

Mechanical: **millimeters** unless otherwise noted (OpenSCAD default).
Electrical: **SI** (V, A, W, Ω, Hz).
Thermal: **°C** and **W**.
Cost estimates: **USD**, in 2026 dollars.

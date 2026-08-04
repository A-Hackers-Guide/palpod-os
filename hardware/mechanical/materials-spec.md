# PAL Pod — Materials Specification

Every material choice below is a trade-off decision made deliberately.
When a hardware EE or mechanical designer proposes a substitution, they
must justify it against the criteria listed here.

## 1. Structural steel frame

**Selection: AISI 304 stainless steel (2B mill finish pre-machining)**

| Criterion | 304 SS (chosen) | 1018 CRS (alt) | Notes |
|---|---|---|---|
| Corrosion resistance | Excellent | Poor (requires plating) | Luxury goods, 20-year service life |
| PVD adhesion | Excellent | Requires Ni strike | Direct PVD on 304 is standard |
| Tensile strength | 505 MPa | 440 MPa | Similar; not the driver |
| Density | 8.0 g/cm³ | 7.87 g/cm³ | Negligible weight difference |
| Cost/kg | ~$5 | ~$1.50 | 3× premium — worth it |
| Weldability | Good (TIG) | Excellent | 304 needs care re: sensitization |
| Weight (main frame, 6mm) | ~55 lb | ~54 lb | — |

**Justification**: PVD adhesion and long-term corrosion resistance dominate.
1018 would require a nickel strike layer before PVD, adding process steps
and delamination risk in service. 304 also has better polishing behavior for
the sub-Ra 0.05 µm pre-PVD finish.

**Do not substitute** 316 SS (unnecessary; molybdenum content adds cost without
benefit indoors) or 430 SS (ferritic, magnetic — interferes with Halbach array).

## 2. PVD finish

**Selection: Chromium Nitride (CrN), 3–4 µm, "gunmetal" spec**

| Criterion | CrN (chosen) | TiN | DLC |
|---|---|---|---|
| Color | Gunmetal / dark grey | Gold | Black |
| Hardness (HV) | 1800 | 2400 | 2500+ |
| Adhesion to 304 SS | Excellent | Excellent | Requires interlayer |
| Cost | Baseline | +15% | +80% |
| Aesthetic match to walnut | Excellent | Poor (gold clashes) | Too matte |

**Pre-plate surface**: Ra ≤ 0.05 µm (mirror polish). This is the driver of
cost, not the PVD itself. Budget 4× the machining time vs. a normal Ra 0.8 µm
finish. Confirm polish with a Mitutoyo SJ-410 or equivalent surface roughness
tester before submitting parts to the PVD vendor.

**PVD vendor shortlist**: Vapor Technologies (Longmont, CO), Ionbond (E. Windsor,
CT), Oerlikon Balzers (multiple US sites). Get quotes from all three; MOQ 20
parts is typical. Lead time: 3 weeks after receipt of polished parts.

## 3. Walnut panels

**Selection: FAS-grade American black walnut (*Juglans nigra*), quarter-sawn,
12 mm nominal**

| Criterion | Spec | Rationale |
|---|---|---|
| Grade | FAS (First and Second) | Highest NHLA grade; minimal defects, allows large clear cuttings |
| Cut | Quarter-sawn (not plain-sawn) | Dimensional stability across seasonal humidity swings; radial ray fleck is a bonus aesthetic |
| Grain direction | Vertical (long axis Z) | Matches column proportions; hides shrinkage as vertical lines |
| Moisture content at assembly | 8% ± 1% | Kiln-dried, acclimatized to 45% RH shop for 2 weeks pre-machining |
| Thickness after finish | 12.0 ±0.1 mm | 13 mm rough, machined to net |
| Curve | Bent-laminated, 3× 4mm plies with polyurethane adhesive | Or 5-axis milled from 20 mm blank. Bent-lam is cheaper and more stable |
| Finish | Rubio Monocoat Pure or Osmo Polyx 3062 | Hardwax oil; food-safe, low-VOC, refinishable in service |
| UV stability | Amber-tint UV inhibitor in topcoat | Walnut lightens dramatically without UV protection; the amber tint compensates |

**Reject criteria**: sapwood > 5% of any panel face; knots > 6 mm; end-checking
> 3 mm; grain runout > 1:12.

**Supplier shortlist**: Baird Brothers (OH), Rockler Hardwoods (multi-state),
Bell Forest Products (MI). Order 20% overage for grade mismatch.

## 4. Acoustic damping foam

**Selection: Melamine open-cell foam (Basotect G+), 32 kg/m³ nominal density,
25 mm thickness for cavity absorption; 10 mm layer bonded to walnut interior
face for panel damping.**

| Property | Spec | Notes |
|---|---|---|
| Density | 32 ± 2 kg/m³ | Higher densities (60 kg/m³) are worse in the 100–1000 Hz range |
| Flow resistivity | 12,000 Pa·s/m² | Sweet spot for driver-cavity absorption at woofer frequencies |
| Fire rating | Class A per ASTM E84 | Required; melamine passes natively |
| Off-gassing | Low VOC | Bake-out 48h at 60°C before install to remove residual solvent |
| Bond method | 3M 90 spray adhesive to walnut back | Avoid contact cement; degrades melamine |

**Do not substitute** polyurethane open-cell foam (fire risk, off-gassing) or
polyester "acoustic tiles" (worse Alpha_w in the woofer band).

## 5. Thermal interface

### 5a. CPU/GPU pad-side (between SoM heat spreader and cold plate)

**Selection: Honeywell PTM7950 phase-change thermal pad, 0.25 mm**

| Property | Spec |
|---|---|
| Bulk thermal conductivity | 8.5 W/m·K |
| Phase change temp | ~45°C |
| Compressible pressure | 10–15 psi (mount torque spec) |
| Shore hardness | 40A pre-phase-change |

Rationale: PTM7950 outperforms every non-liquid TIM in laptop and datacenter
benchmarks; it flows into micro-voids after the first thermal cycle and stays
put. Alternative: Kryosheet (carbon-based, longer life, harder to apply).

### 5b. Bulk gap-filling (VRMs, DDR5, storage controllers)

**Selection: Fujipoly Sarcon XR-Uh, 6 W/m·K, 1.0 – 2.0 mm as needed**

- Shore 00: 25 (soft; conforms to component height mismatch)
- Long-term stability: minimal pump-out over 5 years at 85°C

## 6. Coolant

**Selection: EK CryoFuel Clear (propylene glycol / distilled water, biocide-treated)**

- Do not use dye-based coolants (long-term staining, pump wear).
- Do not use pure distilled water (biological growth in 6 months).
- Refresh interval: 24 months (log in maintenance manual).

## 7. Cabling insulation

- **Signal cabling**: PTFE-insulated where routed near power (>60 V/m field strength). Silicone elsewhere for flex.
- **Speaker cable**: OCC (Ohno continuous casting) copper, 16 AWG for full-range, 12 AWG for subwoofer. Cable brand: DH Labs Q-10 or equivalent. Marketing beat: named copper source, terminated with locking silver-plated banana plugs.
- **Grounding**: single-point star ground at the base of the compute backplane. All chassis grounds tie there via 4 AWG bare copper braid.

## 8. Fastener spec

| Location | Fastener | Torque |
|---|---|---|
| Steel frame joints | M6 × 20 A2-70 SHCS | 8 N·m |
| Walnut-to-frame | M4 × 12 A2-70 threaded insert + SHCS | 2 N·m (do not overtighten into wood) |
| PCB standoffs | M2.5 brass, hex, 6 mm | 0.3 N·m |
| Driver flange bolts | M5 × 20 A2-70 SHCS | 4 N·m |
| Radiator to plinth | M4 × 30 A2-70 SHCS + rubber grommet | 3 N·m |

All stainless. No plated steel anywhere near the Halbach magnets.

## 9. Halbach magnet material (levitation)

- **N52 NdFeB** with **Ni-Cu-Ni** triple-plating for corrosion. Grade N52 chosen for surface field density; verify with vendor certificate.
- **Curie temperature margin**: keep magnets below 80°C in service. Coil driver stage must include thermal cutout per Section 8 of `electrical/block-diagrams/levitation-controller.md`.
- **Safety**: label all magnet assemblies "STRONG MAGNETIC FIELD — PACEMAKER WARNING" per ISO 7010 W006.

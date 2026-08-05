# Hearth — Dimensional Drawing (textual)

Units: mm. Imperial in parentheses. All references are external envelope
unless noted "interior".

Tolerance classes (apply per feature type):
- **NONMATING (cosmetic exteriors, panel edges)**: ±0.5 mm
- **MATING (bracket bosses, PCB standoffs, driver flanges)**: ±0.1 mm
- **BEARING/AIR-GAP (Halbach cradle, orb clearance)**: ±0.05 mm
- **PVD FINISH**: 3–4 µm thickness, Ra ≤ 0.05 µm pre-coat

Datums:
- **A** = bottom face of the base plinth (ground contact)
- **B** = front face of the front walnut panel (user-facing)
- **C** = vertical centerline of the column

## MAIN column — 914 × 305 × 610 mm (36" × 12" × 24")

```
                       FRONT VIEW
        <---------- 305 (12") ---------->
        +-----+-----------------------+-----+  <-- top of frame (Z = 914)
        |     |                       |     |
        | LED |    ___________        | LED |  <-- 7" orb hovers here
        | seam|   (           )       | seam|      Z = 914 + 100 (nominal)
        |     |   \_____ORB__/        |     |
        |     |    Halbach cradle     |     |
        |     +-----------------------+     |  <-- top plinth (Z = 874)
        |     |     ____   ____       |     |
        |     |    | 6.5"| 6.5"|      |     |  <-- 2× subs, 15° forward cant
        |     |    |_____|_____|      |     |
        |     |                       |     |
        |     |   =================   |     |  <-- soundbar 3 (Z ≈ 620)
        |     |                       |     |
        |     |   =================   |     |  <-- soundbar 2 (Z ≈ 560)
        |     |                       |     |
        |     |   =================   |     |  <-- soundbar 1 (Z ≈ 500)
        |     |                       |     |
        |     |       [compute        |     |  <-- compute bay (Z 200 – 480)
        |     |        backplane]     |     |      20 slots × 32mm pitch
        |     |                       |     |
        |     |    _______________    |     |  <-- amp bay lower rear
        |     |   |  Purifi × 3  |    |     |      (Z 60 – 200)
        |     |   |______________|    |     |
        |     |                       |     |
        |     |   [PSU]     [PSU]     |     |  <-- 2× 1500W, base
        |     |                       |     |
        +-----+-----------------------+-----+  <-- base plinth top (Z = 60)
        |                                   |
        |         [ RADIATOR + FANS ]       |  <-- hidden in plinth (0 – 60)
        |                                   |
        +-----------------------------------+  <-- floor / Datum A (Z = 0)
```

```
                        SIDE VIEW (right side)
                        <----- 610 (24") ----->
                    +---------------------------+  <-- Z = 914
                    |     top plinth mic ring   |
                    +---------------------------+
                    |                           |
                    |         subwoofers        |
                    |                           |
        walnut =====|                           |===== walnut
        panel       |                           |     panel
        (curved)    |    compute + audio bays   |    (curved)
        R = 1200    |                           |    R = 1200
                    |                           |
                    |                           |
                    |   [radiator, plan view]   |
                    +---------------------------+  <-- Z = 0
                     |<-- 24" deep intake ---->|
```

```
                       TOP VIEW (mic ring detail)
                              ^ Y (rear)
                              |
              o     o     o   |   o     o     o          o = outer ring mic
                     _________|_________                 (8 total, R=60)
                    /         |         \
                o  |    o     |     o    |  o           inner mics
                   |          |          |               (4 total, R=30)
                    \_________|_________/                center = broadside
              o     o     o   |   o     o     o          (1)
                              |
                              +--------> X (right)
                                (user faces +X? no — user faces -Y)
```

## EXTENDER — 457 × 152 × 305 mm (18" × 6" × 12")

Half-scale in every dimension. Simplified content:
- 1× 4" full-range driver front (Z ≈ 200)
- 1× 5" sub down-firing in base (Z ≈ 60)
- RK3588 SBC on lower shelf
- Class-D amp above SBC
- 3.5" orb hovers on top plate
- 7-hole mic ring (6 outer + 1 center) on top plate

## Key dimensioned features (for GD&T handoff)

| Feature | Nominal | Tolerance | Class | Datum |
|---|---|---|---|---|
| Overall height (main) | 914 | ±0.5 | NONMATING | A |
| Overall width (main) | 305 | ±0.5 | NONMATING | C |
| Overall depth (main) | 610 | ±0.5 | NONMATING | B |
| Walnut panel thickness | 12 | ±0.1 | MATING | — |
| Walnut curve radius | 1200 | ±5 | NONMATING | — |
| Steel frame plate | 6.0 | ±0.05 | MATING | — |
| LED seam channel width | 2.0 | ±0.05 | MATING | — |
| LED seam channel depth | 4.0 | ±0.05 | MATING | — |
| Sub driver cutout Ø | 165 | ±0.1 | MATING | — |
| Sub bolt-circle Ø | 148 | ±0.05 | MATING | — |
| Compute slot pitch | 32.00 | ±0.05 | MATING | — |
| Orb air-gap (nominal) | 12.0 | ±0.05 | BEARING | — |
| Orb Ø (main) | 178 | ±0.2 | NONMATING | — |
| Radiator envelope | 480×30×120 | ±0.5 | NONMATING | — |
| Top-plate flatness | — | 0.1 mm/300 mm | GD&T | — |
| Base plinth flatness | — | 0.05 mm/300 mm | GD&T | A |

## Structural loading (call out to mechanical EE)

- Static load bearing: **180 lb (82 kg) on 4 corner feet** → 45 lb per foot. Feet should be M8 threaded inserts, isolation-mounted (Sorbothane 50 durometer).
- Orb levitation active load: 0.5 kg suspended at 200 mm above top plate. Verify the top plinth resists 5 N vertical + 5 N·m torque from Halbach coil switching.
- Subwoofer reaction force at 30 Hz / 110 dB: expect ±20 N peak into top plinth. Verify no resonance below 80 Hz in the plinth structure (FEA).

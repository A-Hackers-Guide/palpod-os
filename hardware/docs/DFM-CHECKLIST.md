# DFM Checklist

**Audience: the hardware EE will run through this at 30% design review,
60% design review, and again pre-tape-out for each board.**

## Mechanical

### Machined parts (steel frame, top plate)

- [ ] All external corners ≥ 3 mm radius (deburring, safety)
- [ ] All internal corners ≥ 0.5 mm radius (endmill access)
- [ ] Wall thickness ≥ 3 mm anywhere the part is loaded
- [ ] Threaded holes: through-holes preferred; blind holes ≥ 1.5× diameter deep
- [ ] Countersinks specified to standard 82° or 90° fastener spec
- [ ] Chamfer edges called out per ASME Y14.5 (no "break sharp edges" ambiguity)
- [ ] Draft angles on cast/molded parts ≥ 2°
- [ ] Datum stack-up analysis complete (worst-case mate)
- [ ] Tool-access paths verified in CAM (no undercuts requiring 5-axis unless intended)
- [ ] Machining fixture design confirmed with shop

### PVD-coated parts

- [ ] Ra ≤ 0.05 µm on all Class-A cosmetic surfaces (mirror pre-polish)
- [ ] Ra ≤ 0.4 µm on non-cosmetic surfaces
- [ ] No sharp inside corners that create thin-plate PVD failure
- [ ] Racking holes / bosses added at non-visible locations for PVD hanging
- [ ] Color match against approved standard swatch (annually re-approved)
- [ ] Salt-spray test spec (ASTM B117, 240 h minimum)

### Walnut panels

- [ ] Grain direction called out on drawing (vertical on all Class-A faces)
- [ ] Quarter-sawn cut explicitly required (not "rift or quarter")
- [ ] Moisture content 8% ± 1% at assembly (verify with pin meter per lot)
- [ ] Wood-frame interface uses floating tongue-and-groove (NOT rigid bolted) to allow seasonal movement
- [ ] Finish specified (Rubio Monocoat Pure, 1 coat + wipe-off, cured 72 h)
- [ ] UV inhibitor amber tint verified against master sample
- [ ] Reject-criteria table on drawing (sapwood %, knot size, checking)

## PCB / Electrical

### Every board

- [ ] Impedance targets called out in fab notes (85 Ω diff, 50 Ω SE, etc.)
- [ ] Stackup diagram on fab drawing (with material spec: FR4-Std, Megtron 6, etc.)
- [ ] Surface finish specified (ENIG for BGA, HASL not acceptable)
- [ ] Solder mask color + silkscreen color called out
- [ ] Test points at every rail + critical net (min 8 per board)
- [ ] Boundary-scan (JTAG) chain complete on all BGAs
- [ ] Debug header (SWD or JTAG) accessible without disassembly
- [ ] Fiducials on both sides of PCB (3 minimum, non-collinear)
- [ ] Pick-and-place origin defined
- [ ] Panel routing with mouse-bites or V-scoring specified
- [ ] Assembly drawing shows component orientation (pin 1 markers)
- [ ] DFM report from fab vendor (JLCPCB / PCBWay / Sunstone) reviewed + resolved
- [ ] DFA report from assembly vendor (Advanced Assembly, MacroFab) reviewed
- [ ] ESD-safe assembly required (per JEDEC JESD625B) — call out on drawing

### Backplane specifically (highest risk)

- [ ] PCIe Gen5 loss budget simulated in Ansys SIwave or Cadence Sigrity
- [ ] Retimers placed per PCIe electrical spec (< 8 in trace to endpoint)
- [ ] Slot connector engagement/retention force verified against SoM weight
- [ ] Cold-mating vs hot-plug spec confirmed with connector vendor
- [ ] Backplane ATE / bed-of-nails design started before layout freezes

### Power boards

- [ ] Trace current density verified with IPC-2152 calculator
- [ ] Copper pour thermal analysis on high-current traces
- [ ] Bulk capacitor derating verified (voltage AND temperature)
- [ ] Short-circuit protection tested and margins documented
- [ ] Loop-stability simulation for every switching regulator

## Assembly

- [ ] Assembly sequence document exists (with photos or exploded views)
- [ ] Cycle-time estimate per station
- [ ] Torque values called out on every screw (with driver spec)
- [ ] Cable-routing diagrams show strain relief and clearance
- [ ] Anti-static wrist-strap policy + ESD-safe workstations at every station
- [ ] Kit-cart designed (parts pre-picked per unit)
- [ ] First-article inspection procedure written + signed off
- [ ] Burn-in test spec (24 h @ 40 °C ambient, full audio + compute load)
- [ ] Functional test spec (end-to-end: boot → wake word → play audio → orb levitates)

## Test / manufacturing

- [ ] ICT (in-circuit test) fixture designed for every non-trivial PCB
- [ ] Functional test rig (FTX) built for each board type
- [ ] End-of-line test procedure covers all subsystems
- [ ] Traceability system (serial number per unit + per major sub) defined
- [ ] Test data captured to MES (manufacturing execution system) for each unit
- [ ] Non-conforming material (NCM) tag + quarantine procedure documented

## Field service

- [ ] Every subsystem has a defined FRU (field-replaceable unit) boundary
- [ ] Replacement procedure documented (video preferred)
- [ ] Spare parts stocking plan (2-year MTTR promise → hold inventory)
- [ ] Firmware rollback path verified
- [ ] "Return for service" packaging designed (foam cutouts, dual-carton)

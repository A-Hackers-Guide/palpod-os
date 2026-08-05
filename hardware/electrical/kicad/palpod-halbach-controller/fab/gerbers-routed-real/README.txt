palpod-halbach-controller real place-and-route output
Generated: Tue Aug  4 17:47:42 PDT 2026

Placement: cluster-based Python auto-place
Router:    FreeRouting 1.9.0 (open-source topological)
Net class: COIL_HIGH_CURRENT nets set to 5.0mm trace width (30A rated coils)

SAFETY-CRITICAL - auto-router output is NOT manufacturable without review:
  - No length-matching, no impedance control
  - Power planes may not be optimal (2oz F.Cu/B.Cu, 1oz internal)
  - Reviewer must verify: high-current trace geometry (COIL_*), thermal
    reliefs on high-power vias, spacing at 48V rails, MOSFET dV/dt loops,
    hall SPI signal integrity

palpod-orb real place-and-route output
Generated: Tue Aug  4 17:35:52 PDT 2026

Board:     6-layer flex-rigid, two rigid islands + flex bridge
Placement: cluster-based Python auto-place (no manual review)
Router:    FreeRouting 1.9.0 (open-source topological)

This is REAL routing, not a placement-only demo. Caveats:
  - Auto-routed boards are NOT manufacturable without manual review
  - MIPI CSI diff pairs and DSI diff pairs need length matching by hand
  - Power planes on In1..In4 not poured; router used signal layers only
  - Flex-neck routing between rigid1 and rigid2 has no restricted-layer rule
  - Placeholder footprints use arbitrary pad numbering; a real fab requires
    re-mapping pad numbers to true datasheet pinouts before ordering

Files:
  Gerbers      -> palpod-orb-real-*.g??/gbr
  Drill        -> palpod-orb-real.drl
  DRC report   -> drc-report.txt
  3D top       -> board-3d-routed-top.png
  PDF top/bot  -> board-pcb-routed-{top,bot}.pdf

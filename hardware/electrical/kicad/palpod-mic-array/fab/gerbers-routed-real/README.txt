palpod-mic-array real place-and-route output
Generated: Tue Aug  4 09:00:28 PDT 2026

Placement: cluster-based Python auto-place (no manual review)
Router:    FreeRouting 2.2.4 (open-source topological)

This is REAL routing, not a placement-only demo. However:
  - Auto-routed boards are NOT manufacturable without manual review
  - No length-matching, no impedance control, no differential-pair rules
  - Power planes may not be optimal
  - Reviewer must verify: PDM_CLK stub matching, USB DP/DN differential
    trace geometry, decoupling loop area, and thermal reliefs

Files:
  Gerbers      -> palpod-mic-array-real-*.g??/gbr
  Drill        -> palpod-mic-array-real.drl
  DRC report   -> drc-report.txt
  3D top       -> board-3d-routed-top.png
  PDF top/bot  -> board-pcb-routed-{top,bot}.pdf

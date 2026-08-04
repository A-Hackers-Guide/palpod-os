#!/usr/bin/env zsh
# Post-routing finalization: import SES, generate gerbers, DRC, 3D, zip
set -u
PROJ=/private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/electrical/kicad/palpod-mic-array
PCB=$PROJ/palpod-mic-array-real.kicad_pcb
SES=$PROJ/palpod-mic-array-real.ses
CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
WORK=/private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/PLACE-AND-ROUTE-WORK/real-run
FAB=$PROJ/fab/gerbers-routed-real
mkdir -p $FAB

echo "=== Finalize pipeline started at $(date) ==="

# 1: Import SES if present
if [ -s "$SES" ]; then
  echo "--- Import SES ($(stat -f%z $SES) bytes) ---"
  $PY $WORK/post_route.py 2>&1 | grep -v Fontconfig | grep -v "Adding duplicate" | grep -v "wxApp before" | grep -v "^..:..:.. .M: Debug"
else
  echo "--- NO SES; skipping route import (board stays placement-only) ---"
fi

# 2: Gerbers
echo "--- Gerbers ---"
$CLI pcb export gerbers -o $FAB/ $PCB 2>&1 | tail -3

# 3: Drill
echo "--- Drill ---"
$CLI pcb export drill -o $FAB/ $PCB 2>&1 | tail -3

# 4: DRC
echo "--- DRC ---"
$CLI pcb drc --output $FAB/drc-report.txt $PCB 2>&1 | tail -3

# 5: 3D top render
echo "--- 3D render (top) ---"
$CLI pcb render --output $FAB/board-3d-routed-top.png --side top --quality basic $PCB 2>&1 | tail -3

# 6: PDF (F.Cu + edge + silk)
echo "--- PDF F.Cu ---"
$CLI pcb export pdf --output $FAB/board-pcb-routed-top.pdf --layers F.Cu,F.Silkscreen,Edge.Cuts $PCB 2>&1 | tail -3
$CLI pcb export pdf --output $FAB/board-pcb-routed-bot.pdf --layers B.Cu,B.Silkscreen,Edge.Cuts $PCB 2>&1 | tail -3

# 7: DEMO/REAL note
if [ -s "$SES" ]; then
cat > $FAB/README.txt <<TXT
palpod-mic-array real place-and-route output
Generated: $(date)

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
TXT
else
cat > $FAB/README.txt <<TXT
palpod-mic-array PLACEMENT-ONLY output
Generated: $(date)

FreeRouting did not produce a usable SES file — this artifact contains
footprints placed at their planned positions with net assignments, but NO
copper traces. The DRC report shows the resulting unconnected pads.

Placement: cluster-based Python auto-place
Router:    FreeRouting 2.2.4 (failed to save session)
TXT
fi

# 8: Zip
echo "--- Zip ---"
cd $PROJ/fab
rm -f palpod-mic-array-REAL-FAB-PACKAGE.zip
zip -qr palpod-mic-array-REAL-FAB-PACKAGE.zip gerbers-routed-real/
ls -l palpod-mic-array-REAL-FAB-PACKAGE.zip

echo "=== Finalize pipeline done at $(date) ==="

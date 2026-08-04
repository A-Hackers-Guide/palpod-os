#!/bin/zsh
# Full per-board pipeline. Usage: run_board.sh <basename> <timeout_seconds> <max_passes>
set -u
BASE=$1
TO=${2:-300}
MP=${3:-30}
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
JAVA=/opt/homebrew/opt/openjdk/bin/java
CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
SP=/private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware
WORK=$SP/PLACE-AND-ROUTE-WORK
LOG=$WORK/logs/${BASE}.log
PROJ=$SP/electrical/kicad/$BASE
PCB_R=$PROJ/${BASE}-routed.kicad_pcb
DSN=$PROJ/${BASE}-routed.dsn
SES=$PROJ/${BASE}-routed.ses
FAB=$PROJ/fab/gerbers-routed

mkdir -p $FAB
echo "==== $BASE at $(date) ====" | tee $LOG

# Stage 1-4: netlist parse, place, assign, DSN export
echo "--- Stage 1-4: place + DSN ---" | tee -a $LOG
$PY $WORK/place_and_route.py $PROJ $BASE 2>&1 | tee -a $LOG >/dev/null
if [ ! -s "$DSN" ]; then
  echo "STAGE_FAIL: no DSN produced" | tee -a $LOG
  exit 1
fi

# Stage 4b: FreeRouting
echo "--- Stage 4b: FreeRouting (${TO}s, ${MP} passes) ---" | tee -a $LOG
# Clear old freerouting log so we can pull per-board stats
FR_LOG=/private/var/folders/hj/n001jc5d33s_718j452r8dl40000gn/T/freerouting/freerouting.log
: > $FR_LOG
# Run freerouting in background, watch log, kill it 20s after session completes (whether SES was saved or not)
gtimeout -k 15s -s INT ${TO}s $JAVA -jar /tmp/freerouting/freerouting.jar -de "$DSN" -do "$SES" -mp $MP > $LOG.fr 2>&1 &
FR_PID=$!
# Wait for session completion in log, then give freerouting 15 more seconds to save, then kill
WATCH_START=$(date +%s)
WATCH_DEADLINE=$((WATCH_START + TO))
SESSION_DONE_AT=0
while kill -0 $FR_PID 2>/dev/null; do
  NOW=$(date +%s)
  if [ $NOW -ge $WATCH_DEADLINE ]; then break; fi
  if [ $SESSION_DONE_AT -eq 0 ] && grep -q 'Auto-router session completed' $FR_LOG 2>/dev/null; then
    SESSION_DONE_AT=$NOW
    echo "  (session completed at $(date), waiting 15s for SES save)" | tee -a $LOG
  fi
  if [ $SESSION_DONE_AT -gt 0 ] && [ $((NOW - SESSION_DONE_AT)) -ge 15 ]; then
    echo "  (killing freerouting 15s after session completed)" | tee -a $LOG
    kill -TERM $FR_PID 2>/dev/null
    sleep 3
    kill -KILL $FR_PID 2>/dev/null
    break
  fi
  sleep 2
done
wait $FR_PID 2>/dev/null
FR_STATUS=$?
cat $LOG.fr | tail -20 | tee -a $LOG
# Copy per-board freerouting log for later analysis
cp $FR_LOG $WORK/logs/${BASE}.freerouting.log 2>/dev/null || true
if [ ! -s "$SES" ]; then
  echo "FREEROUTING_FAIL (exit=$FR_STATUS)" | tee -a $LOG
  # continue anyway - we still have placed board
else
  # Stage 5: import SES
  echo "--- Stage 5: import SES ---" | tee -a $LOG
  $PY - <<PYEOF 2>&1 | tee -a $LOG
import pcbnew
b = pcbnew.LoadBoard("$PCB_R")
ok = pcbnew.ImportSpecctraSES(b, "$SES")
print("SES import:", ok)
b.Save("$PCB_R")
PYEOF
fi

# Stage 6: Gerbers, drill, DRC, 3D, PDF
echo "--- Stage 6a: Gerbers ---" | tee -a $LOG
$CLI pcb export gerbers -o $FAB/ $PCB_R 2>&1 | tail -3 | tee -a $LOG
echo "--- Stage 6b: Drill ---" | tee -a $LOG
$CLI pcb export drill -o $FAB/ $PCB_R 2>&1 | tail -3 | tee -a $LOG
echo "--- Stage 6c: DRC ---" | tee -a $LOG
$CLI pcb drc --output $FAB/drc-report.txt $PCB_R 2>&1 | tail -3 | tee -a $LOG
echo "--- Stage 6d: 3D render (top) ---" | tee -a $LOG
$CLI pcb render --output $FAB/board-3d-routed-top.png --side top --quality basic $PCB_R 2>&1 | tail -3 | tee -a $LOG
echo "--- Stage 6e: PDF (F.Cu+B.Cu) ---" | tee -a $LOG
$CLI pcb export pdf --output $FAB/board-pcb-routed-top.pdf --layers F.Cu,F.Silkscreen,Edge.Cuts $PCB_R 2>&1 | tail -3 | tee -a $LOG
$CLI pcb export pdf --output $FAB/board-pcb-routed-bot.pdf --layers B.Cu,B.Silkscreen,Edge.Cuts $PCB_R 2>&1 | tail -3 | tee -a $LOG

# Stage 6f: DEMO_ONLY note
cat > $FAB/DEMO_ONLY.txt <<TXT
DEMO ONLY - NOT MANUFACTURABLE
==============================

Board: $BASE
Generated: $(date)

This board was:
  1. Auto-placed by a naive grid-based Python script (no thermal, no signal
     integrity, no length-matching, no differential-pair awareness).
  2. Auto-routed by FreeRouting 2.2.4 (open-source topological router,
     no length-matching, no impedance control, no crosstalk analysis).

Do NOT send to fabrication. Autorouted PCBs must be reviewed by a
qualified PCB engineer. High-speed, high-current, RF, and mixed-signal
designs almost always require manual routing.

See PLACE-AND-ROUTE-REPORT.md for pipeline results.
TXT

# Stage 6g: Zip
echo "--- Stage 6g: Zip ---" | tee -a $LOG
cd $PROJ/fab
rm -f ${BASE}-routed-fab-package.zip
zip -qr ${BASE}-routed-fab-package.zip gerbers-routed/
ls -l ${BASE}-routed-fab-package.zip | tee -a $LOG

echo "==== $BASE done at $(date) ====" | tee -a $LOG

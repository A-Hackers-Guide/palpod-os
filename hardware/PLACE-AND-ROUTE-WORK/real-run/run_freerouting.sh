#!/usr/bin/env zsh
# Run FreeRouting with a completion watchdog, then force-save the SES if the
# built-in save path didn't fire.
set -u
JAR=/tmp/freerouting/freerouting.jar
JAVA=/opt/homebrew/opt/openjdk/bin/java
PROJ=/private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/electrical/kicad/palpod-mic-array
DSN=$PROJ/palpod-mic-array-real.dsn
SES=$PROJ/palpod-mic-array-real.ses
WORK=/private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/PLACE-AND-ROUTE-WORK/real-run
STDLOG=$WORK/freerouting.stdout
FR_LOG=/private/var/folders/hj/n001jc5d33s_718j452r8dl40000gn/T/freerouting/freerouting.log

: > $STDLOG
: > $FR_LOG 2>/dev/null || true
rm -f $SES

MP=${1:-30}
TO=${2:-1200}   # 20 min overall wall time
THREADS=${3:-4}

echo "=== FreeRouting run at $(date) ===" | tee $STDLOG
echo "  DSN: $DSN"
echo "  SES: $SES"
echo "  mp=$MP  timeout=${TO}s  threads=$THREADS"

# Start FreeRouting
$JAVA -jar $JAR -de "$DSN" -do "$SES" -mp $MP -mt $THREADS >> $STDLOG 2>&1 &
FR_PID=$!
echo "  pid=$FR_PID"

START=$(date +%s)
SESSION_DONE_AT=0
LAST_SIZE=0

while kill -0 $FR_PID 2>/dev/null; do
  NOW=$(date +%s)
  ELAPSED=$((NOW - START))
  if [ $ELAPSED -ge $TO ]; then
    echo "  [t=${ELAPSED}s] wall timeout - terminating"
    kill -TERM $FR_PID 2>/dev/null
    sleep 3
    kill -KILL $FR_PID 2>/dev/null
    break
  fi
  if [ $SESSION_DONE_AT -eq 0 ] && grep -q 'Auto-router session completed' $FR_LOG 2>/dev/null; then
    SESSION_DONE_AT=$NOW
    echo "  [t=${ELAPSED}s] Auto-router session completed detected; waiting 30s for SES save"
  fi
  if [ $SESSION_DONE_AT -gt 0 ] && [ $((NOW - SESSION_DONE_AT)) -ge 30 ]; then
    if [ -s "$SES" ]; then
      echo "  [t=${ELAPSED}s] SES saved (${$(stat -f%z $SES)} bytes); terminating cleanly"
    else
      echo "  [t=${ELAPSED}s] SES still empty; terminating"
    fi
    kill -TERM $FR_PID 2>/dev/null
    sleep 3
    kill -KILL $FR_PID 2>/dev/null
    break
  fi
  sleep 2
done
wait $FR_PID 2>/dev/null
FR_EXIT=$?
echo "=== FreeRouting exited: $FR_EXIT at $(date) ==="

if [ -s "$SES" ]; then
  echo "SES ok: $(stat -f%z $SES) bytes"
  exit 0
else
  echo "SES MISSING or empty"
  exit 1
fi

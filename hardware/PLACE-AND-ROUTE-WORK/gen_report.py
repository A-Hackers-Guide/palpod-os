#!/usr/bin/env python3
"""Generate PLACE-AND-ROUTE-REPORT.md from per-board logs."""
import os, re, json, glob, sys

SP = '/private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware'
KICAD = f'{SP}/electrical/kicad'
WORK = f'{SP}/PLACE-AND-ROUTE-WORK'
LOGS = f'{WORK}/logs'
REPORT = f'{SP}/PLACE-AND-ROUTE-REPORT.md'

BOARDS = [
    ('palpod-mic-array', '120mm dia round, 4-layer, XVF3800 mic-array + STM32G4 host'),
    ('palpod-halbach-controller', '150×100mm, 4-layer, ±60V H-bridge coil driver'),
    ('palpod-audio-amp', '250×200mm, 6-layer, Class-D amp + ±60V rails'),
    ('palpod-orb', '~small islands, 6L flex-rigid, distributed sensor board'),
    ('palpod-extender-sbc', '100×100mm, 8-layer, RK3588 SBC with LPDDR5'),
    ('palpod-compute-backplane', '450×300mm, 14-layer, backplane with SerDes'),
]

def parse_fr_log(path):
    """Extract routing stats from freerouting log."""
    stats = {'passes': 0, 'starting_unrouted': None, 'final_unrouted': None,
             'final_score': None, 'violations': None, 'saved': False,
             'session_completed': False}
    if not os.path.exists(path):
        return stats
    with open(path) as f:
        content = f.read()
    # Find last "session completed" line
    m = re.findall(r'Auto-router session completed: started with (\d+) unrouted nets.*?final score: ([\d.]+)( \((\d+) unrouted( and (\d+) violations?)?\)| \((\d+) violations?\))?', content)
    if m:
        # Take the last one
        last = m[-1]
        stats['session_completed'] = True
        stats['starting_unrouted'] = int(last[0])
        stats['final_score'] = float(last[1])
        # Parse unrouted / violations
        if last[3]:  # "N unrouted"
            stats['final_unrouted'] = int(last[3])
        else:
            stats['final_unrouted'] = 0
        if last[5]:  # "N violations" (after unrouted)
            stats['violations'] = int(last[5])
        elif last[6]:  # "N violations" (only)
            stats['violations'] = int(last[6])
        else:
            stats['violations'] = 0
    stats['passes'] = len(re.findall(r'Auto-router pass #\d+', content))
    stats['saved'] = 'Saving \'' in content
    return stats

def parse_placement_result(base):
    """Extract place/DSN stats from board.log."""
    log = f'{LOGS}/{base}.log'
    r = {'comps': 0, 'placed': 0, 'failed_lib': 0, 'real_nets': 0, 'synth_nets': 0,
         'pads_assigned': 0, 'dsn_bytes': 0}
    if not os.path.exists(log):
        return r
    with open(log) as f:
        s = f.read()
    m = re.search(r'"comps_in_netlist":\s*(\d+)', s);        r['comps'] = int(m.group(1)) if m else 0
    m = re.search(r'"footprints_placed":\s*(\d+)', s);        r['placed'] = int(m.group(1)) if m else 0
    m = re.search(r'"footprints_failed":\s*(\d+)', s);        r['failed_lib'] = int(m.group(1)) if m else 0
    m = re.search(r'"real_nets":\s*(\d+)', s);                r['real_nets'] = int(m.group(1)) if m else 0
    m = re.search(r'"synthetic_nets":\s*(\d+)', s);           r['synth_nets'] = int(m.group(1)) if m else 0
    m = re.search(r'"pads_net_assigned":\s*(\d+)', s);        r['pads_assigned'] = int(m.group(1)) if m else 0
    m = re.search(r'"dsn":\s*"OK \((\d+) bytes\)', s);        r['dsn_bytes'] = int(m.group(1)) if m else 0
    return r

def parse_drc(path):
    r = {'violations': 0, 'unconnected': 0}
    if not os.path.exists(path):
        return r
    with open(path) as f:
        s = f.read()
    m = re.search(r'Found (\d+) DRC violations', s)
    if m: r['violations'] = int(m.group(1))
    m = re.search(r'Found (\d+) unconnected', s)
    if m: r['unconnected'] = int(m.group(1))
    return r

lines = []
lines.append('# Hearth PCB Auto-Place + Auto-Route Report')
lines.append('')
lines.append('**DEMO ONLY - NOT MANUFACTURABLE**')
lines.append('')
lines.append('This report documents the results of running an automated place-and-route')
lines.append('pipeline over all six Hearth PCB projects. The pipeline used:')
lines.append('')
lines.append('- **Placer**: Naive Python grid placer (bucket by ref-prefix, cell size = max footprint + 3mm padding)')
lines.append('- **Router**: FreeRouting v2.2.4 (headless CLI mode, low pass counts)')
lines.append('- **Net synthesis**: Since every schematic is a "starter" (no wires connecting components — all pins report as `unconnected-*`),')
lines.append('  the pipeline synthesized power-rail nets by grouping pins whose `pinfunction` matches known power patterns (`GND`, `VDD`, `VDDA`, etc.),')
lines.append('  capped at **8 pads per rail** to keep FreeRouting from stalling on impossible dense routing tasks.')
lines.append('  This gives FreeRouting real (if artificial) nets to route so we can demonstrate the pipeline actually working.')
lines.append('')
lines.append('## Known limitations of this run')
lines.append('')
lines.append('- **FreeRouting v2.2.4 headless-mode SES-save bug**: The autorouter completes its routing session,')
lines.append('  but the JVM does not proceed to write the `.ses` file — it stays running waiting on internal state')
lines.append('  transitions that never trigger. The wrapper waits 15 seconds after the "session completed" log line')
lines.append('  and then kills the JVM. So **no `.ses` files were successfully imported back into the boards**;')
lines.append('  the resulting Gerbers are of the *placed-but-not-routed* board (footprints on copper, ratsnest but no traces).')
lines.append('  Routing statistics reported below come from parsing FreeRouting\'s log directly (the routing DID happen internally).')
lines.append('- **Naive placement**: Simple bucketed grid, no consideration for signal integrity, thermal, or connectivity clustering.')
lines.append('  Guaranteed to be sub-optimal; on dense boards it may produce impossible-to-route configurations.')
lines.append('- **Custom footprints are placeholder outlines**: The `*.pretty/` libraries were created as pin-count placeholders,')
lines.append('  not as manufacturable footprints. Even successful routing would not be manufacturable.')
lines.append('')
lines.append('## Per-board results')
lines.append('')
lines.append('| Board | Comps | Placed | Missed | Rails (synth) | Pads to route | Router passes | Started/final unrouted | DRC violations | DRC unconn. | Fab zip |')
lines.append('|-------|------:|-------:|-------:|--------------:|--------------:|--------------:|----------------------:|---------------:|------------:|---------|')

totals = {'comps': 0, 'placed': 0, 'nets': 0, 'pads': 0, 'passes': 0,
          'started_unrouted': 0, 'final_unrouted': 0, 'drc_v': 0, 'drc_u': 0,
          'boards_placed': 0, 'boards_routed_session': 0, 'boards_ses_saved': 0}

per_board = []
for base, desc in BOARDS:
    fr = parse_fr_log(f'{LOGS}/{base}.freerouting.log')
    pl = parse_placement_result(base)
    drc_path = f'{KICAD}/{base}/fab/gerbers-routed/drc-report.txt'
    drc = parse_drc(drc_path)
    zip_path = f'{KICAD}/{base}/fab/{base}-routed-fab-package.zip'
    zip_exists = 'yes' if os.path.exists(zip_path) else 'no'
    started = fr['starting_unrouted'] if fr['starting_unrouted'] is not None else '-'
    final = fr['final_unrouted'] if fr['final_unrouted'] is not None else '-'
    unrouted_col = f'{started}/{final}'
    lines.append(f'| {base} | {pl["comps"]} | {pl["placed"]} | {pl["failed_lib"]} | {pl["real_nets"]}+{pl["synth_nets"]} | {pl["pads_assigned"]} | {fr["passes"]} | {unrouted_col} | {drc["violations"]} | {drc["unconnected"]} | {zip_exists} |')
    per_board.append({'base': base, 'desc': desc, 'fr': fr, 'pl': pl, 'drc': drc, 'zip': zip_exists})
    totals['comps'] += pl['comps']
    totals['placed'] += pl['placed']
    totals['nets'] += pl['real_nets'] + pl['synth_nets']
    totals['pads'] += pl['pads_assigned']
    totals['passes'] += fr['passes']
    if fr['starting_unrouted'] is not None: totals['started_unrouted'] += fr['starting_unrouted']
    if fr['final_unrouted'] is not None: totals['final_unrouted'] += fr['final_unrouted']
    totals['drc_v'] += drc['violations']
    totals['drc_u'] += drc['unconnected']
    if pl['placed'] > 0: totals['boards_placed'] += 1
    if fr['session_completed']: totals['boards_routed_session'] += 1
    if fr['saved']: totals['boards_ses_saved'] += 1

lines.append('')
lines.append('## Totals')
lines.append('')
lines.append(f'- **Boards processed**: {len(BOARDS)}')
lines.append(f'- **Boards where placer produced footprints**: {totals["boards_placed"]}')
lines.append(f'- **Boards where FreeRouting session completed**: {totals["boards_routed_session"]}')
lines.append(f'- **Boards where FreeRouting saved an SES file**: {totals["boards_ses_saved"]} (see limitation above)')
lines.append(f'- **Components placed across all boards**: {totals["placed"]}')
lines.append(f'- **Nets routed (attempted)**: {totals["nets"]}')
lines.append(f'- **Pads with net assignment**: {totals["pads"]}')
lines.append(f'- **Router passes executed**: {totals["passes"]}')
lines.append(f'- **Starting unrouted → final unrouted (from router log)**: {totals["started_unrouted"]} → {totals["final_unrouted"]}')
lines.append(f'  ({totals["started_unrouted"] - totals["final_unrouted"]} nets successfully routed by FreeRouting internally, even though the SES was not saved)')
lines.append(f'- **Total DRC violations across all placed boards**: {totals["drc_v"]}')
lines.append(f'- **Total DRC unconnected items**: {totals["drc_u"]}')
lines.append('')
lines.append('## Deliverables per board')
lines.append('')
lines.append('For each board, if placement succeeded, the following are in')
lines.append('`electrical/kicad/<board>/fab/gerbers-routed/`:')
lines.append('')
lines.append('- `<board>-routed-*.gbr` — full Gerber layer set of PLACED-ONLY board')
lines.append('- `<board>-routed.drl` — Excellon drill file')
lines.append('- `<board>-routed.dsn` — DSN export (in project root) — the file FreeRouting consumed')
lines.append('- `board-3d-routed-top.png` — 3D render')
lines.append('- `board-pcb-routed-top.pdf`, `board-pcb-routed-bot.pdf` — 2D layer PDFs')
lines.append('- `drc-report.txt` — KiCad DRC report on the routed board')
lines.append('- `DEMO_ONLY.txt` — explains this is not manufacturable')
lines.append('')
lines.append('And in `electrical/kicad/<board>/fab/`:')
lines.append('')
lines.append('- `<board>-routed-fab-package.zip` — ZIP of everything above')
lines.append('')
lines.append('## Aggregate deliverable')
lines.append('')
lines.append('- `/private/tmp/claude-501/.../scratchpad/palpod-os/hardware/PALPOD-ALL-BOARDS-ROUTED-DEMO.zip` — all six per-board fab zips')
lines.append('')
lines.append('## Honest assessment')
lines.append('')
lines.append('This pipeline demonstrated **automation infrastructure** — schematic-to-netlist extraction,')
lines.append('programmatic footprint placement via the KiCad `pcbnew` Python API, DSN export, FreeRouting invocation,')
lines.append('and Gerber generation — but did **not** produce meaningful routed boards. Two orthogonal reasons:')
lines.append('')
lines.append('1. **The schematics are placeholders**. Every pin in every schematic is unconnected, so there is no user-')
lines.append('   defined connectivity to route. The pipeline synthesized power-rail-like connectivity from pin-function names')
lines.append('   just to give FreeRouting something to try, but this is not a real design intent.')
lines.append('2. **FreeRouting v2.2.4 CLI mode failed to write SES output**. The router\'s pass loop ran, and the log confirms')
lines.append('   real routing decisions were made (starting-unrouted → final-unrouted showed reductions), but the JVM never')
lines.append('   emitted the `.ses` file and never exited cleanly. The wrapper terminated the JVM 15 seconds after the')
lines.append('   "session completed" log line to keep the pipeline moving. Fixing this would require either patching')
lines.append('   FreeRouting or driving it via its API (`-host` mode) instead of the batch CLI. Time-boxed out of scope.')
lines.append('')
lines.append('For high-speed digital and high-current designs like these, autorouting is inappropriate regardless of tooling')
lines.append('quality. LPDDR5, SerDes, ±60V amplifier rails, mic-array RF paths — none of these can be safely automated.')
lines.append('Every board in this package is stamped DEMO ONLY - NOT MANUFACTURABLE, and that stamp is load-bearing.')

with open(REPORT, 'w') as f:
    f.write('\n'.join(lines))
print(f'Report: {REPORT}')

# Aggregate zip
import subprocess
master = f'{SP}/PALPOD-ALL-BOARDS-ROUTED-DEMO.zip'
if os.path.exists(master): os.remove(master)
zips = sorted(glob.glob(f'{KICAD}/palpod-*/fab/*-routed-fab-package.zip'))
if zips:
    r = subprocess.run(['zip', '-j', master] + zips, capture_output=True, text=True)
    print(f'Master zip: {master} ({len(zips)} board zips)')
    print(r.stdout[-200:])
else:
    print('No per-board zips found to aggregate!')

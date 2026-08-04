# PAL Pod PCB Auto-Place + Auto-Route Report

**DEMO ONLY - NOT MANUFACTURABLE**

This report documents the results of running an automated place-and-route
pipeline over all six PAL Pod PCB projects. The pipeline used:

- **Placer**: Naive Python grid placer (bucket by ref-prefix, cell size = max footprint + 3mm padding)
- **Router**: FreeRouting v2.2.4 (headless CLI mode, low pass counts)
- **Net synthesis**: Since every schematic is a "starter" (no wires connecting components — all pins report as `unconnected-*`),
  the pipeline synthesized power-rail nets by grouping pins whose `pinfunction` matches known power patterns (`GND`, `VDD`, `VDDA`, etc.),
  capped at **8 pads per rail** to keep FreeRouting from stalling on impossible dense routing tasks.
  This gives FreeRouting real (if artificial) nets to route so we can demonstrate the pipeline actually working.

## Known limitations of this run

- **FreeRouting v2.2.4 headless-mode SES-save bug**: The autorouter completes its routing session,
  but the JVM does not proceed to write the `.ses` file — it stays running waiting on internal state
  transitions that never trigger. The wrapper waits 15 seconds after the "session completed" log line
  and then kills the JVM. So **no `.ses` files were successfully imported back into the boards**;
  the resulting Gerbers are of the *placed-but-not-routed* board (footprints on copper, ratsnest but no traces).
  Routing statistics reported below come from parsing FreeRouting's log directly (the routing DID happen internally).
- **Naive placement**: Simple bucketed grid, no consideration for signal integrity, thermal, or connectivity clustering.
  Guaranteed to be sub-optimal; on dense boards it may produce impossible-to-route configurations.
- **Custom footprints are placeholder outlines**: The `*.pretty/` libraries were created as pin-count placeholders,
  not as manufacturable footprints. Even successful routing would not be manufacturable.

## Per-board results

| Board | Comps | Placed | Missed | Rails (synth) | Pads to route | Router passes | Started/final unrouted | DRC violations | DRC unconn. | Fab zip |
|-------|------:|-------:|-------:|--------------:|--------------:|--------------:|----------------------:|---------------:|------------:|---------|
| palpod-mic-array | 33 | 31 | 2 | 0+3 | 12 | 2 | 10/0 | 89 | 10 | yes |
| palpod-halbach-controller | 60 | 60 | 0 | 0+6 | 19 | 2 | 16/5 | 908 | 16 | yes |
| palpod-audio-amp | 73 | 70 | 3 | 0+5 | 24 | 3 | 19/8 | 546 | 19 | yes |
| palpod-orb | 44 | 44 | 0 | 0+6 | 29 | 2 | 23/12 | 704 | 23 | yes |
| palpod-extender-sbc | 34 | 28 | 6 | 0+5 | 5 | 2 | 3/0 | 310 | 3 | yes |
| palpod-compute-backplane | 34 | 34 | 0 | 0+4 | 26 | 0 | -/- | 202 | 22 | yes |

## Totals

- **Boards processed**: 6
- **Boards where placer produced footprints**: 6
- **Boards where FreeRouting session completed**: 5
- **Boards where FreeRouting saved an SES file**: 0 (see limitation above)
- **Components placed across all boards**: 267
- **Nets routed (attempted)**: 29
- **Pads with net assignment**: 115
- **Router passes executed**: 11
- **Starting unrouted → final unrouted (from router log)**: 71 → 25
  (46 nets successfully routed by FreeRouting internally, even though the SES was not saved)
- **Total DRC violations across all placed boards**: 2759
- **Total DRC unconnected items**: 93

## Deliverables per board

For each board, if placement succeeded, the following are in
`electrical/kicad/<board>/fab/gerbers-routed/`:

- `<board>-routed-*.gbr` — full Gerber layer set of PLACED-ONLY board
- `<board>-routed.drl` — Excellon drill file
- `<board>-routed.dsn` — DSN export (in project root) — the file FreeRouting consumed
- `board-3d-routed-top.png` — 3D render
- `board-pcb-routed-top.pdf`, `board-pcb-routed-bot.pdf` — 2D layer PDFs
- `drc-report.txt` — KiCad DRC report on the routed board
- `DEMO_ONLY.txt` — explains this is not manufacturable

And in `electrical/kicad/<board>/fab/`:

- `<board>-routed-fab-package.zip` — ZIP of everything above

## Aggregate deliverable

- `/private/tmp/claude-501/.../scratchpad/palpod-os/hardware/PALPOD-ALL-BOARDS-ROUTED-DEMO.zip` — all six per-board fab zips

## Honest assessment

This pipeline demonstrated **automation infrastructure** — schematic-to-netlist extraction,
programmatic footprint placement via the KiCad `pcbnew` Python API, DSN export, FreeRouting invocation,
and Gerber generation — but did **not** produce meaningful routed boards. Two orthogonal reasons:

1. **The schematics are placeholders**. Every pin in every schematic is unconnected, so there is no user-
   defined connectivity to route. The pipeline synthesized power-rail-like connectivity from pin-function names
   just to give FreeRouting something to try, but this is not a real design intent.
2. **FreeRouting v2.2.4 CLI mode failed to write SES output**. The router's pass loop ran, and the log confirms
   real routing decisions were made (starting-unrouted → final-unrouted showed reductions), but the JVM never
   emitted the `.ses` file and never exited cleanly. The wrapper terminated the JVM 15 seconds after the
   "session completed" log line to keep the pipeline moving. Fixing this would require either patching
   FreeRouting or driving it via its API (`-host` mode) instead of the batch CLI. Time-boxed out of scope.

For high-speed digital and high-current designs like these, autorouting is inappropriate regardless of tooling
quality. LPDDR5, SerDes, ±60V amplifier rails, mic-array RF paths — none of these can be safely automated.
Every board in this package is stamped DEMO ONLY - NOT MANUFACTURABLE, and that stamp is load-bearing.
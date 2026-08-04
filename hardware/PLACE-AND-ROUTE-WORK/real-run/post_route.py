#!/usr/bin/env python3
"""
Post-routing steps:
  1. Import SES back into PCB
  2. Save PCB
  3. Report track/via stats
"""
import os, sys, json
import pcbnew

PROJ = '/private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/electrical/kicad/palpod-mic-array'
PCB = f'{PROJ}/palpod-mic-array-real.kicad_pcb'
SES = f'{PROJ}/palpod-mic-array-real.ses'

def main():
    board = pcbnew.LoadBoard(PCB)

    # Baseline stats
    tracks_before = len([t for t in board.Tracks()])

    ses_imported = False
    if os.path.exists(SES) and os.path.getsize(SES) > 0:
        try:
            ok = pcbnew.ImportSpecctraSES(board, SES)
            ses_imported = bool(ok)
        except Exception as e:
            print(f'ImportSpecctraSES exception: {e}')

    tracks_after = len([t for t in board.Tracks()])
    # count only tracks (not vias) - vias inherit from PCB_TRACK
    n_tracks = 0; n_vias = 0
    for t in board.Tracks():
        if t.Type() == pcbnew.PCB_VIA_T:
            n_vias += 1
        else:
            n_tracks += 1

    # By layer
    by_layer = {}
    for t in board.Tracks():
        if t.Type() == pcbnew.PCB_VIA_T:
            continue
        lid = t.GetLayer()
        by_layer.setdefault(lid, 0)
        by_layer[lid] += 1

    layer_names = {}
    for lid in by_layer:
        layer_names[lid] = board.GetLayerName(lid)

    # Save board with imported tracks
    board.Save(PCB)

    # Unconnected ratsnest count
    ratsnest = board.GetConnectivity()
    ratsnest.RecalculateRatsnest()
    unconn = ratsnest.GetUnconnectedCount(True)

    result = {
        'ses_exists': os.path.exists(SES),
        'ses_bytes': os.path.getsize(SES) if os.path.exists(SES) else 0,
        'ses_imported': ses_imported,
        'tracks_before': tracks_before,
        'tracks_after': tracks_after,
        'signal_tracks': n_tracks,
        'vias': n_vias,
        'tracks_by_layer': {layer_names[lid]: n for lid, n in by_layer.items()},
        'unconnected_pads_after': unconn,
    }
    with open('/tmp/mic-array-post-route.json', 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()

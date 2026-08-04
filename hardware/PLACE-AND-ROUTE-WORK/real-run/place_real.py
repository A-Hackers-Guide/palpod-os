#!/usr/bin/env python3
"""
Cluster-based placement for the palpod-mic-array round 120mm PCB.

Reads the netlist at /tmp/mic-array-real.net, applies footprints from the
project libraries to a fresh copy of palpod-mic-array.kicad_pcb, assigns nets
to pads, and saves as palpod-mic-array-real.kicad_pcb.

Placement plan (round 120mm dia, edge at r=60mm):
    U1  XVF3800    center
    U2  NDP120     right of U1
    U4  STM32G474  lower-left cluster with U3
    U3  USB3320    next to U4
    J1  USB-C      bottom edge
    U5,U6,U7 LDOs  between USB and center IC ring
    M1..M7 outer   equally spaced at r=55mm
    M8..M13 inner  equally spaced at r=35mm
    C10..C15 100nF decoupling next to their target IC VDD pins
    C1..C6 10uF    near LDOs / bulk decoupling
"""
import os, sys, re, math, subprocess, json, time, shutil
import pcbnew

PROJ = '/private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/electrical/kicad/palpod-mic-array'
BASE = 'palpod-mic-array'
BASE_REAL = 'palpod-mic-array-real'
NETLIST = '/tmp/mic-array-real.net'
KICAD_STOCK = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints'

# ---------------- netlist parsing ----------------
def parse_netlist():
    with open(NETLIST) as f:
        s = f.read()

    # components
    parts = re.split(r'\(comp\s+\(ref\s+"', s)
    comps = []
    for part in parts[1:]:
        m = re.match(r'([^"]+)"\)\s+\(value\s+"([^"]*)"\)\s+\(footprint\s+"([^"]*)"\)', part)
        if not m:
            continue
        ref, val, fp = m.groups()
        comps.append({'ref': ref, 'value': val, 'footprint': fp})

    # nets: each net starts with "(net (code "N") (name "..") ...) "
    net_blocks = re.split(r'\(net\s+\(code\s+"', s)
    nets = []
    for part in net_blocks[1:]:
        m = re.match(r'(\d+)"\)\s+\(name\s+"([^"]*)"\)', part)
        if not m:
            continue
        code, name = m.group(1), m.group(2)
        # collect this net's nodes: everything until the next "(net" or top-level ")"
        end = part.find('(net (code "')
        blob = part if end < 0 else part[:end]
        nodes = []
        for nm in re.finditer(r'\(node\s+\(ref\s+"([^"]*)"\)\s+\(pin\s+"([^"]*)"\)', blob):
            nodes.append({'ref': nm.group(1), 'pin': nm.group(2)})
        nets.append({'code': int(code), 'name': name.lstrip('/'), 'nodes': nodes})
    return comps, nets

# ---------------- footprint loading ----------------
def resolve_lib(lib_name):
    p = os.path.join(PROJ, 'libraries', f'{lib_name}.pretty')
    if os.path.isdir(p):
        return p
    p = os.path.join(KICAD_STOCK, f'{lib_name}.pretty')
    if os.path.isdir(p):
        return p
    return None

# Fallback map for footprints not present in stock library under the exact schematic name.
FP_ALIAS = {
    'Connector_USB:USB_C_Receptacle_GCT_USB4110-xx-A':
        'Connector_USB:USB_C_Receptacle_GCT_USB4110',
    'Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.35x3.35mm':
        'Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.3x3.3mm',
}

def load_fp(fp_ref, cache):
    if fp_ref in cache: return cache[fp_ref]
    orig = fp_ref
    lib, name = fp_ref.split(':', 1)
    libpath = resolve_lib(lib)
    fp = None
    if libpath:
        try:
            fp = pcbnew.FootprintLoad(libpath, name)
        except Exception:
            fp = None
    if fp is None and orig in FP_ALIAS:
        alias = FP_ALIAS[orig]
        lib2, name2 = alias.split(':', 1)
        libpath2 = resolve_lib(lib2)
        if libpath2:
            try:
                fp = pcbnew.FootprintLoad(libpath2, name2)
            except Exception:
                fp = None
    cache[fp_ref] = fp
    return fp

# ---------------- placement plan ----------------
# Coordinates are in mm relative to board center (0,0).
# Board is a circle radius 60mm.

def mm(v): return int(v * 1_000_000)

# Central IC cluster (compact) — all coordinates in mm; +Y is DOWN (KiCad)
# Layout:
#   Y=-52  ─────── USB-C at top edge
#   Y=-14 ─┐  central IC cluster (U1, U2, U3, U4 with decap caps)
#          │
#   Y=+14 ─┘
#   Y=+26  ─────── bulk 10uF row
#   Y=+40  ─────── LDO row (U5/U6/U7)
#   Y=+50  ─────── bottom bulk caps
PLACEMENT = {
    'U1': (  0.0,   0.0, 0),   # XVF3800 BGA61 - center
    'U2': ( 14.0,   0.0, 0),   # NDP120 LGA69 - right of U1
    'U3': (-37.0,  -8.0, 0),   # USB3320 QFN-32 - upper-left, clears M11 and M5
    'U4': (-30.0,  15.0, 0),   # STM32G474 LQFP-64 - west of U1, clears M10 and LDO row
    'J1': (  0.0, -52.0, 0),   # USB-C top edge

    # LDOs (SOT-223, 10.3x10.7 bbox) - row at Y=+40
    'U5': (-14.0,  40.0, 0),   # AP2114-3.3
    'U6': (  0.0,  40.0, 0),   # TLV70218-1.8
    'U7': ( 14.0,  40.0, 0),   # TPS7A02-1.0

    # Bulk 10uF caps (0603, 3.92x4.56 bbox)
    'C1': (-13.0,  50.0, 0),   # near U5
    'C2': (  0.0,  50.0, 0),   # near U6
    'C3': ( 13.0,  50.0, 0),   # near U7
    'C4': (-13.0,  30.0, 0),   # above U5 (VIN)
    'C5': (  0.0,  30.0, 0),   # above U6
    'C6': ( 13.0,  30.0, 0),   # above U7

    # 100nF decoupling caps (0402, 4.87x4.02 bbox)
    'C10': (-12.0,  -4.0, 0),  # XVF3800 VDDIO (west of U1)
    'C11': (  5.0,  -8.0, 0),  # XVF3800 VDD_CORE (north of U1)  <-- moved to clear U2 x range
    'C12': ( 21.0,  -4.0, 0),  # NDP120 VDD_IO (east of U2)
    'C13': ( 21.0,   4.0, 0),  # NDP120 VDD_CORE (east of U2)
    'C14': (-30.0,  26.0, 0),  # STM32 VDD (below U4)
    'C15': (-43.0,  -1.0, 0),  # USB3320 VDD (below U3, x-side)
}

# Outer ring: 7 mics at r=51mm (with 5mm bbox half-extent → keeps ≥3.5mm from edge)
OUTER_R = 51.0
OUTER_OFFSET_DEG = -12.85
OUTER_MICS = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7']
# Inner ring: 6 mics at r=24mm. Skips angles where U4 (-40,+22) and U3 (-35,-8) sit.
INNER_R = 24.0
INNER_OFFSET_DEG = 15.0  # shifts inner mics off the ±X axis
INNER_MICS = ['M8', 'M9', 'M10', 'M11', 'M12', 'M13']

def compute_placement():
    plan = dict(PLACEMENT)
    # Outer ring
    for i, ref in enumerate(OUTER_MICS):
        theta_deg = OUTER_OFFSET_DEG + i * (360 / len(OUTER_MICS))
        theta = math.radians(theta_deg)
        # In +Y-down world, use standard math but flip meaning: angle 0 = right, angle 90 = down
        x = OUTER_R * math.cos(theta)
        y = OUTER_R * math.sin(theta)
        # Rotate mic body so pin 1 points inward. Simpler: leave rotation 0 for now.
        plan[ref] = (x, y, 0)
    # Inner ring
    for i, ref in enumerate(INNER_MICS):
        theta_deg = INNER_OFFSET_DEG + i * (360 / len(INNER_MICS))
        theta = math.radians(theta_deg)
        x = INNER_R * math.cos(theta)
        y = INNER_R * math.sin(theta)
        plan[ref] = (x, y, 0)
    return plan

# ---------------- main ----------------
def main():
    print('=== palpod-mic-array real place-and-route ===')

    # copy inputs -> -real suffix
    for ext in ('kicad_pcb', 'kicad_pro'):
        src = os.path.join(PROJ, f'{BASE}.{ext}')
        dst = os.path.join(PROJ, f'{BASE_REAL}.{ext}')
        if os.path.exists(src):
            shutil.copy(src, dst)
    # sch not needed for pcb operations

    comps, nets = parse_netlist()
    print(f'Parsed netlist: {len(comps)} comps, {len(nets)} nets')

    real_nets = [n for n in nets if not n['name'].startswith('unconnected-')]
    routable_nets = [n for n in real_nets if len(n['nodes']) >= 2]
    print(f'  real nets (non-unconnected): {len(real_nets)}')
    print(f'  routable multi-node nets: {len(routable_nets)}')

    # Load PCB
    pcb_path = os.path.join(PROJ, f'{BASE_REAL}.kicad_pcb')
    board = pcbnew.LoadBoard(pcb_path)

    # Remove any existing footprints (paranoid - shouldn't be any)
    for fp in list(board.Footprints()):
        board.Remove(fp)

    plan = compute_placement()

    # Load & place footprints
    fp_cache = {}
    placed = 0
    lib_miss = 0
    no_plan = 0
    fp_by_ref = {}
    # Small caps get placed AFTER larger fixtures so they can be nudged aside
    def _order_key(c):
        r = c['ref']
        if r.startswith('U') or r.startswith('J'): return (0, r)
        return (1, r)
    for c in sorted(comps, key=_order_key):
        template = load_fp(c['footprint'], fp_cache)
        if template is None:
            lib_miss += 1
            print(f'  MISS: {c["ref"]} footprint "{c["footprint"]}" not found')
            continue
        fp = pcbnew.FOOTPRINT(template)
        fp.SetReference(c['ref'])
        fp.SetValue(c['value'])
        pos = plan.get(c['ref'])
        if pos is None:
            # fallback: bottom of board
            x, y, ang = 40.0, 40.0, 0
            no_plan += 1
        else:
            x, y, ang = pos
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        if ang:
            fp.SetOrientationDegrees(ang)
        board.Add(fp)
        fp_by_ref[c['ref']] = fp
        placed += 1

    print(f'Placed: {placed}  lib_miss: {lib_miss}  no_plan: {no_plan}')

    # Overlap resolver: for each remaining overlap, nudge the smaller item away.
    # ICs and connectors (U*, J*) stay fixed; passives (C*, R*, D*, L*) are moved.
    def resolve_overlaps(board, iters=8):
        fixed = lambda ref: ref.startswith('U') or ref.startswith('J') or ref.startswith('M')
        for step in range(iters):
            fps = list(board.Footprints())
            moved = 0
            for i, f1 in enumerate(fps):
                for f2 in fps[i+1:]:
                    bb1 = f1.GetBoundingBox()
                    bb2 = f2.GetBoundingBox()
                    if not bb1.Intersects(bb2):
                        continue
                    r1 = f1.GetReference(); r2 = f2.GetReference()
                    # Skip pairs of fixed items
                    if fixed(r1) and fixed(r2):
                        continue
                    # Pick which to move
                    if fixed(r1):
                        mover = f2; other = f1
                    elif fixed(r2):
                        mover = f1; other = f2
                    else:
                        # move the second (arbitrary)
                        mover = f2; other = f1
                    # Direction from other center to mover center
                    ox = other.GetPosition().x; oy = other.GetPosition().y
                    mx = mover.GetPosition().x; my = mover.GetPosition().y
                    dx = mx - ox; dy = my - oy
                    if dx == 0 and dy == 0:
                        dx = 1_000_000  # 1mm right if coincident
                    # Compute needed push distance
                    bbm = mover.GetBoundingBox(); bbo = other.GetBoundingBox()
                    # overlap along both axes
                    ox_min, ox_max = bbo.GetX(), bbo.GetX() + bbo.GetWidth()
                    oy_min, oy_max = bbo.GetY(), bbo.GetY() + bbo.GetHeight()
                    mx_min, mx_max = bbm.GetX(), bbm.GetX() + bbm.GetWidth()
                    my_min, my_max = bbm.GetY(), bbm.GetY() + bbm.GetHeight()
                    overlap_x = min(ox_max, mx_max) - max(ox_min, mx_min)
                    overlap_y = min(oy_max, my_max) - max(oy_min, my_min)
                    if overlap_x < overlap_y:
                        # push in x
                        sign = 1 if dx > 0 else -1
                        mover.Move(pcbnew.VECTOR2I(sign * (overlap_x + 500_000), 0))
                    else:
                        sign = 1 if dy > 0 else -1
                        mover.Move(pcbnew.VECTOR2I(0, sign * (overlap_y + 500_000)))
                    moved += 1
            if moved == 0:
                break
            print(f'  overlap iter {step}: {moved} nudges')
    resolve_overlaps(board, iters=12)

    # Assign nets to pads
    net_lookup = {}
    for netname, netinfo in board.GetNetInfo().NetsByName().items():
        net_lookup[str(netname)] = netinfo
    assigned = 0; missing_pads = 0
    net_created = 0
    for net in nets:
        if net['name'].startswith('unconnected-'):
            continue
        name = net['name'].strip() or f'NET{net["code"]}'
        if name in net_lookup:
            ni = net_lookup[name]
        else:
            ni = pcbnew.NETINFO_ITEM(board, name)
            board.Add(ni)
            net_lookup[name] = ni
            net_created += 1
        for node in net['nodes']:
            fp = fp_by_ref.get(node['ref'])
            if fp is None:
                missing_pads += 1
                continue
            pad = fp.FindPadByNumber(node['pin'])
            if pad is None:
                missing_pads += 1
                continue
            pad.SetNet(ni)
            assigned += 1
    print(f'Nets: created {net_created}, assigned {assigned} pads, missing {missing_pads}')

    board.Save(pcb_path)
    print(f'Saved {pcb_path}')

    # Export DSN
    dsn_path = os.path.join(PROJ, f'{BASE_REAL}.dsn')
    try:
        # Reload fresh to prevent stale state issues
        b2 = pcbnew.LoadBoard(pcb_path)
        ok = pcbnew.ExportSpecctraDSN(b2, dsn_path)
        if ok and os.path.exists(dsn_path):
            print(f'DSN exported: {os.path.getsize(dsn_path)} bytes -> {dsn_path}')
        else:
            print(f'DSN export returned {ok}')
    except Exception as e:
        print(f'DSN export failed: {e}')

    # Summary
    result = {
        'comps_in_netlist': len(comps),
        'nets_total': len(nets),
        'real_nets': len(real_nets),
        'routable_nets': len(routable_nets),
        'total_pads_to_route': sum(len(n['nodes']) for n in routable_nets),
        'placed': placed,
        'lib_miss': lib_miss,
        'no_plan': no_plan,
        'pads_net_assigned': assigned,
        'pads_missing': missing_pads,
        'dsn_bytes': os.path.getsize(dsn_path) if os.path.exists(dsn_path) else 0,
    }
    with open('/tmp/mic-array-place-result.json', 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()

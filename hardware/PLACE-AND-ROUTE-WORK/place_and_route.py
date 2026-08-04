#!/usr/bin/env python3
"""
Full auto-place + FreeRouting pipeline for one KiCad board.
Usage: place_and_route.py <project_dir> <board_basename>

DEMO ONLY - NOT MANUFACTURABLE
"""
import os, sys, re, math, subprocess, json, time
import pcbnew

KICAD_STOCK = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints'
KICAD_CLI = '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'

# ---------- S-expression parser ------------------------------------------
def parse_sexpr(s):
    tokens = re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', s)
    def walk(i):
        assert tokens[i] == '('
        i += 1
        node = []
        while tokens[i] != ')':
            t = tokens[i]
            if t == '(':
                sub, i = walk(i)
                node.append(sub)
            else:
                if t.startswith('"') and t.endswith('"'):
                    t = t[1:-1]
                node.append(t)
                i += 1
        return node, i + 1
    root, _ = walk(0)
    return root

def find_all(node, key):
    if isinstance(node, list):
        for c in node:
            if isinstance(c, list) and c and c[0] == key:
                yield c
            yield from find_all(c, key)

def child(node, key):
    for c in node[1:] if isinstance(node, list) else []:
        if isinstance(c, list) and c and c[0] == key:
            return c
    return None

# ---------- Netlist parsing ---------------------------------------------
POWER_PATTERNS = re.compile(r'^(GND|AGND|DGND|PGND|SGND|EPAD|EP_PAD|VSS|VSSA|VSSD|VCC|VCCA|VCCD|VDD|VDDA|VDDD|DVDD|AVDD|GVDD|PVDD|VDDIO|VDDLDO|VDDSMPS|VDDUSB|VBAT|VBUS|VIN|V\+|V-|3V3|1V8|1V0|1V2|1V5|2V5|5V|12V|VREF|VREFP|VREFN)([_0-9A-Z]*)?$', re.IGNORECASE)

def infer_power_net(pinfunction):
    """Strip trailing _digits from pinfunction and return a power-rail net name, or None."""
    if not pinfunction:
        return None
    # Strip trailing _<alphanumeric> repeatedly to get root
    root = re.sub(r'_[A-Z]*\d+$', '', pinfunction, flags=re.IGNORECASE)
    root = re.sub(r'_\d+$', '', root)
    m = POWER_PATTERNS.match(root)
    if m:
        base = m.group(1).upper()
        # Normalize: all GND-like -> "GND", most VDD variants keep their name
        if base in ('AGND','DGND','PGND','SGND','VSS','VSSA','VSSD','EPAD','EP_PAD'):
            base = 'GND'
        return base
    return None

def parse_netlist(net_file):
    with open(net_file) as f:
        s = f.read()
    root = parse_sexpr(s)
    comps = []
    components = child(root, 'components')
    if components:
        for c in components[1:]:
            if not isinstance(c, list) or c[0] != 'comp': continue
            ref_n = child(c, 'ref'); val_n = child(c, 'value'); fp_n = child(c, 'footprint')
            if not fp_n: continue
            ref = ref_n[1] if ref_n else '?'
            val = val_n[1] if val_n else ''
            fp = fp_n[1] if fp_n else ''
            comps.append({'ref': ref, 'value': val, 'footprint': fp})
    # nets - collect original nets AND synthesize power nets from unconnected power_in pins
    orig_nets = []
    nets_n = child(root, 'nets')
    if nets_n:
        for n in nets_n[1:]:
            if not isinstance(n, list) or n[0] != 'net': continue
            code_n = child(n, 'code'); name_n = child(n, 'name')
            code = int(code_n[1]) if code_n else 0
            name = name_n[1] if name_n else ''
            nodes = []
            for nn in n[1:]:
                if isinstance(nn, list) and nn[0] == 'node':
                    r = child(nn, 'ref'); p = child(nn, 'pin')
                    pf = child(nn, 'pinfunction')
                    pt = child(nn, 'pintype')
                    nodes.append({'ref': r[1], 'pin': p[1],
                                  'pinfunction': pf[1] if pf else '',
                                  'pintype': pt[1] if pt else ''})
            orig_nets.append({'code': code, 'name': name, 'nodes': nodes})

    # Rebuild: keep real (non-unconnected) nets as-is; group unconnected power_in pins by inferred rail
    real_nets = [n for n in orig_nets if not n['name'].startswith('unconnected-')]
    power_bucket = {}  # rail_name -> list of {ref, pin}
    other_unconn = []
    for n in orig_nets:
        if not n['name'].startswith('unconnected-'):
            continue
        # single-node unconnected
        for node in n['nodes']:
            rail = None
            if node['pintype'] == 'power_in' or node['pintype'] == 'power_out':
                rail = infer_power_net(node['pinfunction'])
            if rail:
                power_bucket.setdefault(rail, []).append(node)
            else:
                other_unconn.append(n)
                break

    synth_nets = []
    next_code = max([n['code'] for n in orig_nets] + [0]) + 1
    # Limit synthetic net size: FreeRouting struggles with dense power nets,
    # and we're demoing the pipeline not doing real PDN. Cap each rail at 8 pads.
    MAX_PADS_PER_RAIL = 8
    for rail, nodes in power_bucket.items():
        if len(nodes) < 2:
            continue  # single-pad rails aren't useful to route
        # Take first 8 pads for demo routing
        subset = nodes[:MAX_PADS_PER_RAIL]
        synth_nets.append({'code': next_code, 'name': rail, 'nodes': subset, 'synthetic': True})
        next_code += 1
    all_nets = real_nets + synth_nets
    return comps, all_nets

# ---------- Footprint loader --------------------------------------------
def resolve_lib(project_dir, lib_name):
    # Priority: project libraries dir, then KiCad stock
    p = os.path.join(project_dir, 'libraries', f'{lib_name}.pretty')
    if os.path.isdir(p):
        return p
    p = os.path.join(KICAD_STOCK, f'{lib_name}.pretty')
    if os.path.isdir(p):
        return p
    return None

def load_footprint(project_dir, fp_ref, cache):
    if fp_ref in cache: return cache[fp_ref]
    if ':' not in fp_ref:
        cache[fp_ref] = None; return None
    lib, name = fp_ref.split(':', 1)
    libpath = resolve_lib(project_dir, lib)
    if not libpath:
        cache[fp_ref] = None; return None
    try:
        fp = pcbnew.FootprintLoad(libpath, name)
    except Exception as e:
        fp = None
    cache[fp_ref] = fp
    return fp

# ---------- Placement ----------------------------------------------------
def place_footprints(board, comps, project_dir):
    bbox = board.GetBoardEdgesBoundingBox()
    x0 = bbox.GetX(); y0 = bbox.GetY()
    w  = bbox.GetWidth(); h = bbox.GetHeight()
    cx = x0 + w/2; cy = y0 + h/2
    margin = 5 * 1_000_000  # 5mm in nm
    usable_w = max(w - 2*margin, w*0.8)
    usable_h = max(h - 2*margin, h*0.8)

    # Sort: ICs (U) first, then connectors (J), then passives
    def key(c):
        r = c['ref']
        if r.startswith('U'): return (0, r)
        if r.startswith('J'): return (1, r)
        if r.startswith('L'): return (2, r)
        if r.startswith('D'): return (3, r)
        return (4, r)
    comps_sorted = sorted(comps, key=key)

    # Load all footprints first
    fp_cache = {}
    loaded = []
    for c in comps_sorted:
        fp = load_footprint(project_dir, c['footprint'], fp_cache)
        loaded.append((c, fp))

    # Simple grid placement across the usable area
    n = len([x for x in loaded if x[1] is not None])
    if n == 0: return 0, 0
    # Compute max footprint size to size grid cells to avoid overlap
    max_fp_dim = 0
    for c, fp in loaded:
        if fp is None: continue
        try:
            bb = fp.GetBoundingBox()
            d = max(bb.GetWidth(), bb.GetHeight())
            if d > max_fp_dim: max_fp_dim = d
        except Exception:
            pass
    min_cell = max_fp_dim + 3_000_000  # 3mm padding around each footprint
    # Pick a grid that respects min_cell size
    cols = max(1, min(int(usable_w / max(min_cell, 1)), int(math.ceil(math.sqrt(n * usable_w / max(usable_h,1))))))
    rows = int(math.ceil(n / cols))
    dx = usable_w / cols
    dy = usable_h / rows
    if dx < min_cell or dy < min_cell:
        # Board too tight for this many footprints - fall back to sqrt grid, will overlap
        cols = max(1, int(math.ceil(math.sqrt(n))))
        rows = int(math.ceil(n / cols))
        dx = usable_w / cols
        dy = usable_h / rows

    placed = 0; failed = 0
    idx = 0
    for c, fp in loaded:
        if fp is None:
            failed += 1
            continue
        # New instance per placement — need to duplicate
        newfp = pcbnew.FOOTPRINT(fp)  # copy ctor
        newfp.SetReference(c['ref'])
        newfp.SetValue(c['value'])
        r = idx // cols
        col = idx % cols
        px = int(x0 + margin + dx*col + dx/2)
        py = int(y0 + margin + dy*r  + dy/2)
        newfp.SetPosition(pcbnew.VECTOR2I(px, py))
        board.Add(newfp)
        placed += 1
        idx += 1
    return placed, failed

# ---------- Net assignment ----------------------------------------------
def assign_nets(board, nets):
    net_lookup = {}
    # Existing nets in board
    for netname, netinfo in board.GetNetInfo().NetsByName().items():
        net_lookup[str(netname)] = netinfo
    # Build ref -> footprint map
    fp_map = {}
    for fp in board.Footprints():
        fp_map[fp.GetReference()] = fp

    assigned = 0; missing_pads = 0
    for net in nets:
        name = net['name']
        # Skip auto-generated unconnected nets — they don't need to be routed
        if name.startswith('unconnected-'):
            continue
        # Sanitize net name (no leading/trailing whitespace)
        name = name.strip() or f'NET{net.get("code",0)}'
        # Create or fetch net
        if name in net_lookup:
            ni = net_lookup[name]
        else:
            ni = pcbnew.NETINFO_ITEM(board, name)
            board.Add(ni)
            net_lookup[name] = ni
        for node in net['nodes']:
            fp = fp_map.get(node['ref'])
            if not fp:
                missing_pads += 1
                continue
            pad = fp.FindPadByNumber(node['pin'])
            if pad is None:
                missing_pads += 1
                continue
            pad.SetNet(ni)
            assigned += 1
    return assigned, missing_pads

# ---------- Main pipeline ------------------------------------------------
def run(project_dir, basename):
    print(f'\n{"="*70}\n== BOARD: {basename}\n{"="*70}')
    pcb_orig = os.path.join(project_dir, f'{basename}.kicad_pcb')
    pcb_routed = os.path.join(project_dir, f'{basename}-routed.kicad_pcb')
    sch = os.path.join(project_dir, f'{basename}.kicad_sch')

    result = {'board': basename, 'stages': {}, 'errors': []}

    # Copy original -> routed
    import shutil
    shutil.copy(pcb_orig, pcb_routed)
    # Also copy .kicad_pro and .kicad_sch so freerouting/kicad can open as project
    for ext in ['kicad_pro']:
        src = os.path.join(project_dir, f'{basename}.{ext}')
        dst = os.path.join(project_dir, f'{basename}-routed.{ext}')
        if os.path.exists(src): shutil.copy(src, dst)

    # Stage 1: netlist
    net_file = f'/tmp/{basename}.net'
    try:
        r = subprocess.run([KICAD_CLI, 'sch', 'export', 'netlist',
                            '-o', net_file, '--format', 'kicadsexpr', sch],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            result['stages']['netlist'] = f'FAIL: {r.stderr[:200]}'
            return result
        result['stages']['netlist'] = 'OK'
    except Exception as e:
        result['stages']['netlist'] = f'FAIL: {e}'
        return result

    comps, nets = parse_netlist(net_file)
    result['comps_in_netlist'] = len(comps)
    result['nets_in_netlist'] = len(nets)
    result['synthetic_nets'] = len([n for n in nets if n.get('synthetic')])
    result['real_nets'] = len(nets) - result['synthetic_nets']
    result['total_pads_to_route'] = sum(len(n['nodes']) for n in nets)

    # Stage 2: load + place
    board = pcbnew.LoadBoard(pcb_routed)
    try:
        placed, failed = place_footprints(board, comps, project_dir)
        result['footprints_placed'] = placed
        result['footprints_failed'] = failed
        result['stages']['place'] = f'OK ({placed} placed, {failed} lib-miss)'
    except Exception as e:
        result['stages']['place'] = f'FAIL: {e}'
        result['errors'].append(f'place: {e}')
        return result

    # Stage 3: assign nets
    try:
        assigned, miss = assign_nets(board, nets)
        result['pads_net_assigned'] = assigned
        result['pads_missing'] = miss
        result['stages']['assign_nets'] = f'OK ({assigned} pads, {miss} miss)'
    except Exception as e:
        result['stages']['assign_nets'] = f'FAIL: {e}'
        result['errors'].append(f'assign: {e}')

    board.Save(pcb_routed)

    # Stage 4: DSN export
    dsn = os.path.join(project_dir, f'{basename}-routed.dsn')
    try:
        # reload to make sure everything is fresh
        b2 = pcbnew.LoadBoard(pcb_routed)
        ok = pcbnew.ExportSpecctraDSN(b2, dsn)
        if ok and os.path.exists(dsn) and os.path.getsize(dsn) > 0:
            result['stages']['dsn'] = f'OK ({os.path.getsize(dsn)} bytes)'
            result['dsn_path'] = dsn
        else:
            result['stages']['dsn'] = 'FAIL: export returned false'
            return result
    except Exception as e:
        result['stages']['dsn'] = f'FAIL: {e}'
        result['errors'].append(f'dsn: {e}')
        return result

    return result  # freerouting invoked separately

if __name__ == '__main__':
    project_dir = sys.argv[1]
    basename = sys.argv[2]
    r = run(project_dir, basename)
    print('RESULT:', json.dumps(r, indent=2))
    # write result file
    with open(f'/tmp/{basename}.result.json', 'w') as f:
        json.dump(r, f, indent=2)

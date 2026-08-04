#!/usr/bin/env python3
"""Generate three placeholder .kicad_mod footprints."""
from pathlib import Path
import hashlib, uuid

OUTDIR = Path(__file__).resolve().parent.parent / "libraries" / "palpod-mic-array.pretty"
OUTDIR.mkdir(parents=True, exist_ok=True)

def U(seed):
    return str(uuid.UUID(bytes=hashlib.md5(seed.encode()).digest()[:16], version=4))

HEADER_FMT = '''(footprint "{name}"
	(version 20240108)
	(generator "pcbnew")
	(generator_version "8.0")
	(layer "F.Cu")
	(descr "{descr}")
	(tags "{tags}")
	(property "Reference" "{ref}"
		(at 0 {refy} 0)
		(layer "F.SilkS")
		(uuid "{u1}")
		(effects
			(font (size 1 1) (thickness 0.15))
		)
	)
	(property "Value" "{name}"
		(at 0 {valy} 0)
		(layer "F.Fab")
		(uuid "{u2}")
		(effects
			(font (size 1 1) (thickness 0.15))
		)
	)
	(property "Footprint" ""
		(at 0 0 0)
		(layer "F.Fab")
		(hide yes)
		(uuid "{u3}")
		(effects
			(font (size 1.27 1.27) (thickness 0.15))
		)
	)
	(property "Datasheet" "{datasheet}"
		(at 0 0 0)
		(layer "F.Fab")
		(hide yes)
		(uuid "{u4}")
		(effects
			(font (size 1.27 1.27) (thickness 0.15))
		)
	)
	(property "Description" "PLACEHOLDER - verify against datasheet before fab"
		(at 0 0 0)
		(layer "F.Fab")
		(hide yes)
		(uuid "{u5}")
		(effects
			(font (size 1.27 1.27) (thickness 0.15))
		)
	)
	(attr smd)
'''

def outline(w, h, seed_prefix, layer, width=0.12):
    x = w / 2
    y = h / 2
    lines = []
    for i, (x1, y1, x2, y2) in enumerate([
        (-x, -y,  x, -y),
        ( x, -y,  x,  y),
        ( x,  y, -x,  y),
        (-x,  y, -x, -y),
    ]):
        lines.append(
            f'  (fp_line (start {x1} {y1}) (end {x2} {y2}) '
            f'(stroke (width {width}) (type solid)) '
            f'(layer "{layer}") (uuid "{U(seed_prefix + str(i))}"))\n'
        )
    return "".join(lines)

def pin1_marker(x, y, seed):
    return (f'  (fp_circle (center {x} {y}) (end {x + 0.2} {y}) '
            f'(stroke (width 0.15) (type solid)) '
            f'(fill solid) (layer "F.SilkS") (uuid "{U(seed)}"))\n')

def pad_smd_rect(num, x, y, w, h, seed):
    return (f'  (pad "{num}" smd rect (at {x} {y}) (size {w} {h}) '
            f'(layers "F.Cu" "F.Paste" "F.Mask") (uuid "{U(seed)}"))\n')

def pad_smd_circle(num, x, y, d, seed):
    return (f'  (pad "{num}" smd circle (at {x} {y}) (size {d} {d}) '
            f'(layers "F.Cu" "F.Paste" "F.Mask") (uuid "{U(seed)}"))\n')

# -------------------- ICS-41352 LGA5 --------------------
def build_ics41352():
    name = "ICS-41352_LGA5"
    pkg_w, pkg_h = 3.5, 2.65
    body = HEADER_FMT.format(
        name=name, ref="M**",
        refy=-(pkg_h/2 + 1.5), valy=(pkg_h/2 + 1.5),
        descr="PLACEHOLDER TDK InvenSense ICS-41352 MEMS microphone 5-pin LGA 3.50x2.65x0.98mm - VERIFY PIN LOCATIONS AGAINST DATASHEET BEFORE FAB",
        tags="MEMS microphone PDM LGA5 PLACEHOLDER",
        datasheet="https://invensense.tdk.com/products/analog/ics-41352/",
        u1=U(name+"pref"), u2=U(name+"pval"),
        u3=U(name+"pfp"), u4=U(name+"pds"), u5=U(name+"pdesc"))
    parts = [body]
    # Fab layer outline
    parts.append(outline(pkg_w, pkg_h, name+"fab", "F.Fab", 0.1))
    # Silk outline slightly larger
    parts.append(outline(pkg_w + 0.2, pkg_h + 0.2, name+"silk", "F.SilkS", 0.12))
    # Courtyard
    parts.append(outline(pkg_w + 0.5, pkg_h + 0.5, name+"crt", "F.CrtYd", 0.05))
    # Pin 1 marker
    parts.append(pin1_marker(-pkg_w/2 - 0.5, -pkg_h/2 - 0.5, name+"pin1mk"))
    # 5 pads. Layout approximation:
    #  Pin 1 (VDD) bottom-left, pin 2 (GND) bottom-right, 3 CLK top-right,
    #  4 DATA top-middle, 5 SELECT top-left  (placeholder — verify)
    pad_w = 0.6
    pad_h = 0.6
    positions = [
        ("1", -1.2, 0.75),
        ("2",  1.2, 0.75),
        ("3",  1.2, -0.75),
        ("4",  0.0, -0.75),
        ("5", -1.2, -0.75),
    ]
    for num, x, y in positions:
        parts.append(pad_smd_rect(num, x, y, pad_w, pad_h, name+f"p{num}"))
    # 3D model reference (commented via description note; KiCad has no comment tokens)
    # Instead, include a placeholder line the EE can edit:
    # 3D model omitted; EE adds (model "${KIPRJMOD}/3d/ICS-41352.step" ...) after verifying package

    parts.append(")\n")
    return "".join(parts)


# -------------------- XVF3800 LFBGA-61 --------------------
def build_xvf3800():
    name = "XVF3800_LFBGA61"
    pkg_w, pkg_h = 7.0, 7.0
    body = HEADER_FMT.format(
        name=name, ref="U**",
        refy=-(pkg_h/2 + 1.5), valy=(pkg_h/2 + 1.5),
        descr="PLACEHOLDER XMOS XVF3800-INBW 61-pin LFBGA 0.65mm pitch approx 7x7mm - VERIFY BALL MAP AGAINST DATASHEET BEFORE FAB",
        tags="LFBGA-61 XMOS voice DSP PLACEHOLDER",
        datasheet="https://www.xmos.com/xvf3800/",
        u1=U(name+"pref"), u2=U(name+"pval"),
        u3=U(name+"pfp"), u4=U(name+"pds"), u5=U(name+"pdesc"))
    parts = [body]
    parts.append(outline(pkg_w, pkg_h, name+"fab", "F.Fab", 0.1))
    parts.append(outline(pkg_w + 0.2, pkg_h + 0.2, name+"silk", "F.SilkS", 0.12))
    parts.append(outline(pkg_w + 0.5, pkg_h + 0.5, name+"crt", "F.CrtYd", 0.05))
    parts.append(pin1_marker(-pkg_w/2 - 0.5, -pkg_h/2 - 0.5, name+"pin1mk"))
    # BGA balls: 8 rows (A..H) x 8 cols (1..8) = 64 minus 3 corners = 61
    pitch = 0.65
    ball_d = 0.35
    rows = "ABCDEFGH"
    skip = {("A", 8), ("H", 1), ("H", 8)}
    origin_x = -(len(rows) - 1) * pitch / 2  # col 1 x
    origin_y = -(len(rows) - 1) * pitch / 2  # row A y (top)
    for ri, r in enumerate(rows):
        for c in range(1, 9):
            if (r, c) in skip:
                continue
            x = origin_x + (c - 1) * pitch
            y = origin_y + ri * pitch
            num = f"{r}{c}"
            parts.append(pad_smd_circle(num, round(x, 3), round(y, 3), ball_d, name+f"p{num}"))
    # 3D model omitted

    parts.append(")\n")
    return "".join(parts)


# -------------------- NDP120 LGA-69 --------------------
def build_ndp120():
    name = "NDP120_LGA69"
    pkg_w, pkg_h = 5.0, 5.0
    body = HEADER_FMT.format(
        name=name, ref="U**",
        refy=-(pkg_h/2 + 1.5), valy=(pkg_h/2 + 1.5),
        descr="PLACEHOLDER Syntiant NDP120 69-pin LGA approx 5x5mm 0.5mm pitch - VERIFY PIN MAP AGAINST NDA DATASHEET BEFORE FAB",
        tags="LGA-69 Syntiant NDP wake PLACEHOLDER",
        datasheet="https://www.syntiant.com/ndp120",
        u1=U(name+"pref"), u2=U(name+"pval"),
        u3=U(name+"pfp"), u4=U(name+"pds"), u5=U(name+"pdesc"))
    parts = [body]
    parts.append(outline(pkg_w, pkg_h, name+"fab", "F.Fab", 0.1))
    parts.append(outline(pkg_w + 0.2, pkg_h + 0.2, name+"silk", "F.SilkS", 0.12))
    parts.append(outline(pkg_w + 0.5, pkg_h + 0.5, name+"crt", "F.CrtYd", 0.05))
    parts.append(pin1_marker(-pkg_w/2 - 0.5, -pkg_h/2 - 0.5, name+"pin1mk"))
    # 69 peripheral LGA pads around the perimeter, 0.5mm pitch, 0.3x0.5mm pads.
    # 17 pads/side * 4 = 68 + 1 center thermal pad? Use 17/17/17/17 = 68, put center TP as pin 69.
    pad_w, pad_h = 0.3, 0.5
    pitch = 0.5
    per_side = 17
    total_side_len = (per_side - 1) * pitch
    idx = 1
    # bottom side (left to right) — pin 1 starts here per LGA convention (bottom-left corner)
    y = pkg_h/2 - 0.15
    for i in range(per_side):
        x = -total_side_len/2 + i * pitch
        parts.append(pad_smd_rect(str(idx), round(x,3), round(y,3), pad_w, pad_h, name+f"p{idx}"))
        idx += 1
    # right side (bottom to top)
    x = pkg_w/2 - 0.15
    for i in range(per_side):
        y = total_side_len/2 - i * pitch
        parts.append(pad_smd_rect(str(idx), round(x,3), round(y,3), pad_h, pad_w, name+f"p{idx}"))
        idx += 1
    # top side (right to left)
    y = -pkg_h/2 + 0.15
    for i in range(per_side):
        x = total_side_len/2 - i * pitch
        parts.append(pad_smd_rect(str(idx), round(x,3), round(y,3), pad_w, pad_h, name+f"p{idx}"))
        idx += 1
    # left side (top to bottom)
    x = -pkg_w/2 + 0.15
    for i in range(per_side):
        y = -total_side_len/2 + i * pitch
        parts.append(pad_smd_rect(str(idx), round(x,3), round(y,3), pad_h, pad_w, name+f"p{idx}"))
        idx += 1
    # Center thermal pad = pin 69
    parts.append(pad_smd_rect("69", 0, 0, 3.0, 3.0, name+"p69"))
    # 3D model omitted

    parts.append(")\n")
    return "".join(parts)


for name, builder in [("ICS-41352_LGA5", build_ics41352),
                       ("XVF3800_LFBGA61", build_xvf3800),
                       ("NDP120_LGA69", build_ndp120)]:
    p = OUTDIR / f"{name}.kicad_mod"
    p.write_text(builder())
    print(f"Wrote {p} ({p.stat().st_size} bytes)")

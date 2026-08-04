#!/usr/bin/env python3
"""Generate the palpod-audio-amp KiCad project files (symbols, footprints, schematic, PCB).

Produces:
  ../libraries/palpod-audio-amp.kicad_sym
  ../libraries/palpod-audio-amp.pretty/*.kicad_mod
  ../palpod-audio-amp.kicad_sch
  ../palpod-audio-amp.kicad_pcb
"""
import os, uuid, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB_SYM = ROOT / "libraries" / "palpod-audio-amp.kicad_sym"
PRETTY = ROOT / "libraries" / "palpod-audio-amp.pretty"
SCH = ROOT / "palpod-audio-amp.kicad_sch"
PCB = ROOT / "palpod-audio-amp.kicad_pcb"

def U(seed):
    # Deterministic UUIDs per seed string
    return str(uuid.uuid5(uuid.NAMESPACE_OID, "palpod-audio-amp:" + seed))

# ---------------------------------------------------------------------------
# Custom symbol library
# ---------------------------------------------------------------------------

def sym_pin(kind, name, number, x, y, orient, length=2.54):
    return (
        f'\t\t(pin {kind} line\n'
        f'\t\t\t(at {x} {y} {orient})\n'
        f'\t\t\t(length {length})\n'
        f'\t\t\t(name "{name}"\n'
        f'\t\t\t\t(effects (font (size 1.27 1.27)))\n'
        f'\t\t\t)\n'
        f'\t\t\t(number "{number}"\n'
        f'\t\t\t\t(effects (font (size 1.27 1.27)))\n'
        f'\t\t\t)\n'
        f'\t\t)\n'
    )

def make_symbol(name, ref, value, footprint, datasheet, description, pins,
                left_count=None, box_w=25.4, pin_spacing=2.54, pad_top=2.54):
    """pins: list of tuples (kind, name, number, side) where side in ('L','R')."""
    left = [p for p in pins if p[3] == 'L']
    right = [p for p in pins if p[3] == 'R']
    left_n = len(left)
    right_n = len(right)
    h = max(left_n, right_n)
    half = (h - 1) * pin_spacing / 2 + pad_top
    box_top = half + pad_top
    box_bot = -half - pad_top
    box_l = -box_w / 2
    box_r = box_w / 2

    out = []
    out.append(f'\t(symbol "{name}"\n')
    out.append(f'\t\t(pin_names\n\t\t\t(offset 1.016)\n\t\t)\n')
    out.append(f'\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n')
    out.append(f'\t\t(property "Reference" "{ref}"\n\t\t\t(at 0 {box_top+1.5} 0)\n\t\t\t(effects (font (size 1.27 1.27)))\n\t\t)\n')
    out.append(f'\t\t(property "Value" "{value}"\n\t\t\t(at 0 {box_bot-1.5} 0)\n\t\t\t(effects (font (size 1.27 1.27)))\n\t\t)\n')
    out.append(f'\t\t(property "Footprint" "{footprint}"\n\t\t\t(at 0 0 0)\n\t\t\t(effects (font (size 1.27 1.27)) (hide yes))\n\t\t)\n')
    out.append(f'\t\t(property "Datasheet" "{datasheet}"\n\t\t\t(at 0 0 0)\n\t\t\t(effects (font (size 1.27 1.27)) (hide yes))\n\t\t)\n')
    out.append(f'\t\t(property "Description" "{description}"\n\t\t\t(at 0 0 0)\n\t\t\t(effects (font (size 1.27 1.27)) (hide yes))\n\t\t)\n')
    out.append(f'\t\t(symbol "{name}_1_1"\n')
    out.append(f'\t\t\t(rectangle\n\t\t\t\t(start {box_l} {box_top})\n\t\t\t\t(end {box_r} {box_bot})\n\t\t\t\t(stroke (width 0.254) (type default))\n\t\t\t\t(fill (type background))\n\t\t\t)\n')
    # Left pins
    for i, (kind, pname, num, _) in enumerate(left):
        y = half - i * pin_spacing
        out.append(sym_pin(kind, pname, num, box_l - 2.54, y, 0))
    # Right pins
    for i, (kind, pname, num, _) in enumerate(right):
        y = half - i * pin_spacing
        out.append(sym_pin(kind, pname, num, box_r + 2.54, y, 180))
    out.append(f'\t\t)\n\t)\n')
    return ''.join(out)


def build_sym_lib():
    # CS43198 32-pin TQFN (from Cirrus datasheet; simplified functional grouping)
    cs43198_pins = [
        ('power_in','VA','1','L'), ('power_in','AGND','2','L'),
        ('output','AOUTA+','3','L'), ('output','AOUTA-','4','L'),
        ('output','AOUTB+','5','L'), ('output','AOUTB-','6','L'),
        ('passive','FILT+','7','L'), ('power_in','VQ','8','L'),
        ('power_in','VL','9','L'), ('input','RST_N','10','L'),
        ('input','MCLK','11','L'), ('input','SCLK','12','L'),
        ('input','LRCK','13','L'), ('input','SDIN','14','L'),
        ('bidirectional','I2C_SDA','15','L'), ('bidirectional','I2C_SCL','16','L'),
        ('input','AD0','17','R'), ('input','AD1','18','R'),
        ('input','MUTE_N','19','R'), ('input','PDN_N','20','R'),
        ('output','INT_N','21','R'), ('input','DSD_EN','22','R'),
        ('input','DSD_CLK','23','R'), ('input','DSD_L','24','R'),
        ('input','DSD_R','25','R'), ('power_in','VD','26','R'),
        ('power_in','DGND','27','R'), ('passive','NC1','28','R'),
        ('passive','NC2','29','R'), ('power_in','AGND2','30','R'),
        ('power_in','VA2','31','R'), ('power_in','GND_PAD','33','R'),
    ]
    cs43198 = make_symbol(
        'CS43198', 'U', 'CS43198-CWZR',
        'palpod-audio-amp:CS43198_TQFN32',
        'https://www.cirrus.com/products/cs43198/',
        'Cirrus Logic CS43198 32-bit 384kHz stereo DAC (TQFN-32) - PLACEHOLDER pin mapping',
        cs43198_pins, box_w=30.48)

    # CS2100-CP MSOP-10 master clock
    cs2100_pins = [
        ('input','REF_CLK','1','L'), ('output','CLK_OUT','2','L'),
        ('bidirectional','I2C_SDA','3','L'), ('bidirectional','I2C_SCL','4','L'),
        ('input','AD0','5','L'),
        ('input','AUX_IN','6','R'), ('output','AUX_OUT','7','R'),
        ('power_in','VD','8','R'), ('power_in','GND','9','R'),
        ('input','RST_N','10','R'),
    ]
    cs2100 = make_symbol(
        'CS2100-CP', 'U', 'CS2100-CP',
        'palpod-audio-amp:CS2100_MSOP10',
        'https://www.cirrus.com/products/cs2100-cp/',
        'Cirrus Logic CS2100-CP fractional-N clock multiplier (MSOP-10)',
        cs2100_pins, box_w=22.86)

    # THAT1512 SOIC-8 balanced line receiver
    that1512_pins = [
        ('input','IN+','1','L'), ('input','IN-','2','L'),
        ('input','REF','3','L'), ('power_in','V-','4','L'),
        ('power_in','V+','5','R'), ('output','OUT','6','R'),
        ('input','SENSE','7','R'), ('power_in','GND','8','R'),
    ]
    that1512 = make_symbol(
        'THAT1512', 'U', 'THAT1512S08',
        'palpod-audio-amp:THAT1512_SOIC8',
        'https://thatcorp.com/1510-1512-audio-differential-line-receiver-ic/',
        'THAT Corp 1512 balanced line receiver (SOIC-8) - low-noise diff amp',
        that1512_pins, box_w=17.78)

    # Purifi 1ET7040SA - represented as a module carrier connector
    # Real module has: PWR+, PWR- (+/-60V), GND, IN+, IN-, IN_GND, MUTE, FAULT, +12V_AUX, OUT+, OUT-, GND_OUT
    purifi_pins = [
        ('power_in','PWR+ (+60V)','1','L'), ('power_in','PWR- (-60V)','2','L'),
        ('power_in','GND_PWR','3','L'), ('input','IN+','4','L'),
        ('input','IN-','5','L'), ('input','IN_GND','6','L'),
        ('input','MUTE','7','R'), ('output','FAULT_N','8','R'),
        ('power_in','+12V_AUX','9','R'), ('output','OUT+','10','R'),
        ('output','OUT-','11','R'), ('power_in','GND_OUT','12','R'),
    ]
    purifi = make_symbol(
        'Purifi_1ET7040SA', 'A', '1ET7040SA',
        'palpod-audio-amp:Purifi_1ET7040SA_Module',
        'https://purifi-audio.com/product/1et7040sa/',
        'Purifi Audio 1ET7040SA Class-D amplifier module (carrier connector) - PLACEHOLDER pinout, verify against module datasheet',
        purifi_pins, box_w=27.94)

    # LM5116 HTSSOP-24 sync buck controller
    lm5116_pins = [
        ('power_in','VIN','1','L'), ('input','UVLO','2','L'),
        ('input','EN','3','L'), ('output','VCC','4','L'),
        ('output','SS','5','L'), ('input','COMP','6','L'),
        ('input','FB','7','L'), ('input','CS','8','L'),
        ('output','CSG','9','L'), ('output','AGND','10','L'),
        ('output','RT','11','L'), ('output','SYNC','12','L'),
        ('output','HB','13','R'), ('output','HO','14','R'),
        ('output','SW','15','R'), ('output','LO','16','R'),
        ('output','VCCX','17','R'), ('output','PGND','18','R'),
        ('input','SLOPE','19','R'), ('output','RES','20','R'),
        ('output','PGOOD','21','R'), ('output','DEMB','22','R'),
        ('output','NC1','23','R'), ('output','NC2','24','R'),
    ]
    lm5116 = make_symbol(
        'LM5116', 'U', 'LM5116MHX/NOPB',
        'palpod-audio-amp:LM5116_HTSSOP24',
        'https://www.ti.com/product/LM5116',
        'TI LM5116 wide-Vin synchronous buck controller (HTSSOP-24)',
        lm5116_pins, box_w=27.94)

    # TPS3808 SOT-23-5 supervisor
    tps3808_pins = [
        ('input','VDD','1','L'), ('input','SENSE','2','L'),
        ('input','CT','3','L'),
        ('input','GND','4','R'), ('output','RESET_N','5','R'),
    ]
    tps3808 = make_symbol(
        'TPS3808G01', 'U', 'TPS3808G01DBVR',
        'palpod-audio-amp:TPS3808_SOT23-5',
        'https://www.ti.com/product/TPS3808',
        'TI TPS3808G01 programmable-delay supervisor (SOT-23-5)',
        tps3808_pins, box_w=17.78)

    # ADT7420 MSOP-8 temperature sensor
    adt7420_pins = [
        ('power_in','VDD','1','L'), ('bidirectional','SDA','2','L'),
        ('output','CT_N','3','L'), ('output','INT_N','4','L'),
        ('input','A0','5','R'), ('input','A1','6','R'),
        ('bidirectional','SCL','7','R'), ('power_in','GND','8','R'),
    ]
    adt7420 = make_symbol(
        'ADT7420', 'U', 'ADT7420UCPZ-R7',
        'palpod-audio-amp:ADT7420_MSOP8',
        'https://www.analog.com/en/products/adt7420.html',
        'Analog Devices ADT7420 +-0.25C I2C digital temp sensor (MSOP-8)',
        adt7420_pins, box_w=17.78)

    # WBT-0705 speaker binding-post terminal (2-pin high current pass-thru)
    wbt_pins = [
        ('passive','SPKR+','1','L'),
        ('passive','SPKR-','2','R'),
    ]
    wbt = make_symbol(
        'WBT-0705', 'J', 'WBT-0705Cu',
        'palpod-audio-amp:WBT-0705_Terminal',
        'https://www.wbt.de/en/product/wbt-0705cu/',
        'WBT-0705 Cu speaker binding-post terminal (2-pin high current)',
        wbt_pins, box_w=15.24)

    # SiliconLabs Si8660BB 6-ch digital isolator SOIC-16
    si8660_pins = [
        ('power_in','VDD1','1','L'), ('input','A1','2','L'),
        ('input','A2','3','L'), ('input','A3','4','L'),
        ('input','A4','5','L'), ('input','A5','6','L'),
        ('input','A6','7','L'), ('power_in','GND1','8','L'),
        ('power_in','GND2','9','R'), ('output','B6','10','R'),
        ('output','B5','11','R'), ('output','B4','12','R'),
        ('output','B3','13','R'), ('output','B2','14','R'),
        ('output','B1','15','R'), ('power_in','VDD2','16','R'),
    ]
    si8660 = make_symbol(
        'Si8660BB', 'U', 'Si8660BB-B-IS1',
        'palpod-audio-amp:Si8660_SOIC16',
        'https://www.silabs.com/isolation/digital-isolators/si866x',
        'SiLabs Si8660BB 6-ch digital isolator (SOIC-16 WB)',
        si8660_pins, box_w=25.4)

    body = (
        '(kicad_symbol_lib\n'
        '\t(version 20231120)\n'
        '\t(generator "kicad_symbol_editor")\n'
        + cs43198 + cs2100 + that1512 + purifi + lm5116 + tps3808 + adt7420 + wbt + si8660
        + ')\n'
    )
    LIB_SYM.parent.mkdir(parents=True, exist_ok=True)
    LIB_SYM.write_text(body)

# ---------------------------------------------------------------------------
# Footprints
# ---------------------------------------------------------------------------

FP_HEADER = '''(footprint "{name}"
	(version 20240108)
	(generator "pcbnew")
	(generator_version "8.0")
	(layer "F.Cu")
	(descr "{descr}")
	(tags "{tags}")
	(property "Reference" "{ref}"
		(at 0 {ref_y} 0)
		(layer "F.SilkS")
		(uuid "{u1}")
		(effects (font (size 1 1) (thickness 0.15)))
	)
	(property "Value" "{name}"
		(at 0 {val_y} 0)
		(layer "F.Fab")
		(uuid "{u2}")
		(effects (font (size 1 1) (thickness 0.15)))
	)
	(property "Footprint" "" (at 0 0 0) (layer "F.Fab") (hide yes) (uuid "{u3}")
		(effects (font (size 1.27 1.27) (thickness 0.15))))
	(property "Datasheet" "{datasheet}" (at 0 0 0) (layer "F.Fab") (hide yes) (uuid "{u4}")
		(effects (font (size 1.27 1.27) (thickness 0.15))))
	(property "Description" "PLACEHOLDER - verify against datasheet before fab" (at 0 0 0) (layer "F.Fab") (hide yes) (uuid "{u5}")
		(effects (font (size 1.27 1.27) (thickness 0.15))))
	(attr smd)
'''

def rect(layer, w, h, stroke=0.1):
    hw, hh = w/2, h/2
    return (
        f'\t(fp_line (start {-hw} {-hh}) (end {hw} {-hh}) (stroke (width {stroke}) (type solid)) (layer "{layer}") (uuid "{U(layer+str(w)+"a")}"))\n'
        f'\t(fp_line (start {hw} {-hh}) (end {hw} {hh}) (stroke (width {stroke}) (type solid)) (layer "{layer}") (uuid "{U(layer+str(w)+"b")}"))\n'
        f'\t(fp_line (start {hw} {hh}) (end {-hw} {hh}) (stroke (width {stroke}) (type solid)) (layer "{layer}") (uuid "{U(layer+str(w)+"c")}"))\n'
        f'\t(fp_line (start {-hw} {hh}) (end {-hw} {-hh}) (stroke (width {stroke}) (type solid)) (layer "{layer}") (uuid "{U(layer+str(w)+"d")}"))\n'
    )

def qfn_pads(n_per_side, pitch, pad_w, pad_h, body_w, body_h, start=1):
    """Return pads for a QFN with n_per_side per side, pin 1 at top-left, CCW."""
    pads = []
    n = start
    # Left side (top to bottom)
    x = -(body_w/2 + pad_h/2 - 0.1)
    y0 = -(n_per_side-1) * pitch / 2
    for i in range(n_per_side):
        y = y0 + i*pitch
        pads.append(f'\t(pad "{n}" smd roundrect (at {x} {y}) (size {pad_h} {pad_w}) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U("pad"+str(n))}"))\n')
        n += 1
    # Bottom side (left to right)
    y = (body_h/2 + pad_h/2 - 0.1)
    x0 = -(n_per_side-1) * pitch / 2
    for i in range(n_per_side):
        xx = x0 + i*pitch
        pads.append(f'\t(pad "{n}" smd roundrect (at {xx} {y}) (size {pad_w} {pad_h}) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U("pad"+str(n))}"))\n')
        n += 1
    # Right side (bottom to top)
    x = (body_w/2 + pad_h/2 - 0.1)
    for i in range(n_per_side):
        y = y0 + (n_per_side-1-i)*pitch
        pads.append(f'\t(pad "{n}" smd roundrect (at {x} {y}) (size {pad_h} {pad_w}) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U("pad"+str(n))}"))\n')
        n += 1
    # Top side (right to left)
    y = -(body_h/2 + pad_h/2 - 0.1)
    for i in range(n_per_side):
        xx = x0 + (n_per_side-1-i)*pitch
        pads.append(f'\t(pad "{n}" smd roundrect (at {xx} {y}) (size {pad_w} {pad_h}) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U("pad"+str(n))}"))\n')
        n += 1
    return ''.join(pads)

def soic_pads(n, pitch, pad_w, pad_h, body_w):
    """SOIC-style dual-row pads. Pin 1 at top-left, down left side, up right side."""
    pads = []
    per_side = n // 2
    y0 = -(per_side-1) * pitch / 2
    x = body_w/2 + pad_h/2 - 0.1
    # Left side (down)
    for i in range(per_side):
        y = y0 + i*pitch
        num = i + 1
        pads.append(f'\t(pad "{num}" smd roundrect (at {-x} {y}) (size {pad_h} {pad_w}) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U("soic"+str(num))}"))\n')
    # Right side (up)
    for i in range(per_side):
        y = y0 + (per_side-1-i)*pitch
        num = per_side + i + 1
        pads.append(f'\t(pad "{num}" smd roundrect (at {x} {y}) (size {pad_h} {pad_w}) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U("soic"+str(num))}"))\n')
    return ''.join(pads)

def pin1_mark(x, y):
    return f'\t(fp_circle (center {x} {y}) (end {x+0.2} {y}) (stroke (width 0.15) (type solid)) (fill solid) (layer "F.SilkS") (uuid "{U("p1"+str(x)+str(y))}"))\n'

def th_pad(num, x, y, drill, size, shape="circle"):
    return f'\t(pad "{num}" thru_hole {shape} (at {x} {y}) (size {size} {size}) (drill {drill}) (layers "*.Cu" "*.Mask") (uuid "{U("th"+num+str(x)+str(y))}"))\n'

def build_footprints():
    PRETTY.mkdir(parents=True, exist_ok=True)

    def wrap(name, descr, tags, datasheet, body_w, body_h, cyt_pad=0.5):
        u = [U(name+f":u{i}") for i in range(6)]
        hdr = FP_HEADER.format(
            name=name, descr=descr, tags=tags, datasheet=datasheet,
            ref="U**", ref_y=-body_h/2 - 1.5, val_y=body_h/2 + 1.5,
            u1=u[0], u2=u[1], u3=u[2], u4=u[3], u5=u[4],
        )
        # Fab outline (body), Silkscreen outline (slightly larger), courtyard
        hdr += rect("F.Fab", body_w, body_h, 0.1)
        hdr += rect("F.SilkS", body_w+0.2, body_h+0.2, 0.12)
        hdr += rect("F.CrtYd", body_w+cyt_pad*2, body_h+cyt_pad*2, 0.05)
        hdr += pin1_mark(-(body_w/2+0.5), -(body_h/2+0.5))
        return hdr

    # CS43198 TQFN-32, 5x5mm 0.5mm pitch
    body_w, body_h = 5.0, 5.0
    body = wrap("CS43198_TQFN32",
                "PLACEHOLDER Cirrus Logic CS43198-CWZR 32-pin TQFN 5x5mm 0.5mm pitch - VERIFY LAND PATTERN",
                "DAC TQFN32 PLACEHOLDER", "https://www.cirrus.com/products/cs43198/",
                body_w, body_h)
    body += qfn_pads(8, 0.5, 0.28, 0.7, body_w, body_h)
    # Central thermal pad "33"
    body += f'\t(pad "33" smd rect (at 0 0) (size 3.1 3.1) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{U("cs43198-thermal")}"))\n'
    body += ')\n'
    (PRETTY / "CS43198_TQFN32.kicad_mod").write_text(body)

    # CS2100 MSOP-10, 3x3mm 0.5mm pitch
    body_w, body_h = 3.0, 3.0
    body = wrap("CS2100_MSOP10",
                "PLACEHOLDER Cirrus CS2100-CP MSOP-10 3x3mm 0.5mm pitch",
                "clock MSOP10 PLACEHOLDER", "https://www.cirrus.com/products/cs2100-cp/",
                body_w, body_h)
    body += soic_pads(10, 0.5, 0.3, 1.4, body_w)
    body += ')\n'
    (PRETTY / "CS2100_MSOP10.kicad_mod").write_text(body)

    # THAT1512 SOIC-8 3.9x4.9mm
    body_w, body_h = 3.9, 4.9
    body = wrap("THAT1512_SOIC8",
                "PLACEHOLDER THAT1512 balanced line receiver SOIC-8 3.9x4.9mm 1.27mm pitch",
                "audio SOIC8 PLACEHOLDER", "https://thatcorp.com/1510-1512-audio-differential-line-receiver-ic/",
                body_w, body_h)
    body += soic_pads(8, 1.27, 0.6, 1.55, body_w)
    body += ')\n'
    (PRETTY / "THAT1512_SOIC8.kicad_mod").write_text(body)

    # Purifi 1ET7040SA module carrier - large rectangle with pin connector + 4 mount holes
    # Approx module dimensions: 155 x 45 mm (per Purifi 1ET7040SA datasheet)
    body_w, body_h = 155.0, 45.0
    body = wrap("Purifi_1ET7040SA_Module",
                "PLACEHOLDER Purifi 1ET7040SA Class-D amp module carrier footprint 155x45mm - VERIFY MOUNT PATTERN AGAINST PURIFI DATASHEET",
                "amp module PLACEHOLDER", "https://purifi-audio.com/product/1et7040sa/",
                body_w, body_h, cyt_pad=1.0)
    # 4 mounting holes at corners inset 5mm - M3
    for i,(mx,my) in enumerate([(-72.5,-17.5),(72.5,-17.5),(72.5,17.5),(-72.5,17.5)]):
        body += th_pad(f"MH{i+1}", mx, my, 3.2, 6.0)
    # 12-pin connector along the left edge, 5mm pitch (approx module interface header)
    conn_x = -70.0
    conn_y0 = -27.5
    for i in range(12):
        y = conn_y0 + i * 5.0
        body += th_pad(str(i+1), conn_x, y, 1.2, 2.2)
    body += ')\n'
    (PRETTY / "Purifi_1ET7040SA_Module.kicad_mod").write_text(body)

    # LM5116 HTSSOP-24, ~7.8x6.4mm
    body_w, body_h = 7.8, 6.4
    body = wrap("LM5116_HTSSOP24",
                "PLACEHOLDER TI LM5116 HTSSOP-24 with exposed pad",
                "buck HTSSOP24 PLACEHOLDER", "https://www.ti.com/product/LM5116",
                body_w, body_h)
    body += soic_pads(24, 0.65, 0.4, 1.5, body_w)
    body += f'\t(pad "25" smd rect (at 0 0) (size 3.4 5.0) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{U("lm5116-thermal")}"))\n'
    body += ')\n'
    (PRETTY / "LM5116_HTSSOP24.kicad_mod").write_text(body)

    # TPS3808 SOT-23-5, 2.9x1.6mm body
    body_w, body_h = 2.9, 1.6
    body = wrap("TPS3808_SOT23-5",
                "PLACEHOLDER TI TPS3808 SOT-23-5 2.9x1.6mm 0.95mm pitch",
                "supervisor SOT235 PLACEHOLDER", "https://www.ti.com/product/TPS3808",
                body_w, body_h)
    # Standard SOT23-5: pins 1,2,3 on bottom (0.95mm pitch), pins 4,5 on top
    body += f'\t(pad "1" smd roundrect (at -0.95 1.4) (size 0.6 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U("sot1")}"))\n'
    body += f'\t(pad "2" smd roundrect (at 0 1.4) (size 0.6 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U("sot2")}"))\n'
    body += f'\t(pad "3" smd roundrect (at 0.95 1.4) (size 0.6 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U("sot3")}"))\n'
    body += f'\t(pad "4" smd roundrect (at 0.95 -1.4) (size 0.6 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U("sot4")}"))\n'
    body += f'\t(pad "5" smd roundrect (at -0.95 -1.4) (size 0.6 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U("sot5")}"))\n'
    body += ')\n'
    (PRETTY / "TPS3808_SOT23-5.kicad_mod").write_text(body)

    # ADT7420 MSOP-8 3x3mm
    body_w, body_h = 3.0, 3.0
    body = wrap("ADT7420_MSOP8",
                "PLACEHOLDER Analog Devices ADT7420 MSOP-8 3x3mm 0.65mm pitch",
                "temp MSOP8 PLACEHOLDER", "https://www.analog.com/en/products/adt7420.html",
                body_w, body_h)
    body += soic_pads(8, 0.65, 0.4, 1.4, body_w)
    body += ')\n'
    (PRETTY / "ADT7420_MSOP8.kicad_mod").write_text(body)

    # WBT-0705 speaker binding-post terminal - 2 large through-holes
    body_w, body_h = 30.0, 20.0
    body = wrap("WBT-0705_Terminal",
                "PLACEHOLDER WBT-0705Cu speaker binding-post terminal, 2-pin, 19.05mm pitch, panel-mount",
                "speaker terminal PLACEHOLDER", "https://www.wbt.de/en/product/wbt-0705cu/",
                body_w, body_h, cyt_pad=1.0)
    body += th_pad("1", -9.525, 0, 5.5, 9.0)
    body += th_pad("2", 9.525, 0, 5.5, 9.0)
    body += ')\n'
    (PRETTY / "WBT-0705_Terminal.kicad_mod").write_text(body)

    # Si8660 SOIC-16 WB (10.3x7.5)
    body_w, body_h = 10.3, 7.5
    body = wrap("Si8660_SOIC16",
                "PLACEHOLDER SiLabs Si8660BB SOIC-16 WB 10.3x7.5mm 1.27mm pitch",
                "isolator SOIC16WB PLACEHOLDER", "https://www.silabs.com/isolation/digital-isolators/si866x",
                body_w, body_h)
    body += soic_pads(16, 1.27, 0.6, 2.0, body_w)
    body += ')\n'
    (PRETTY / "Si8660_SOIC16.kicad_mod").write_text(body)

    # README
    (PRETTY / "README.md").write_text("""# palpod-audio-amp.pretty - PLACEHOLDER footprints

These `.kicad_mod` files are **starter outlines only**. They compile in KiCad 8+
and give the schematic a valid footprint reference so the project opens
end-to-end, but the pad positions, sizes, and pin numbering are best-effort
approximations, not fabrication-ready.

**Before releasing to fab, the EE must verify every pad against the datasheet
of the actual package.**

## Files

- `CS43198_TQFN32.kicad_mod` - Cirrus CS43198-CWZR 32-pin TQFN 5x5mm 0.5mm pitch, central 3.1x3.1mm thermal pad (pin 33). Verify against Cirrus DS977F5.
- `CS2100_MSOP10.kicad_mod` - CS2100-CP MSOP-10.
- `THAT1512_SOIC8.kicad_mod` - THAT1512 SOIC-8.
- `Purifi_1ET7040SA_Module.kicad_mod` - **Large 155x45mm carrier footprint** for the Purifi 1ET7040SA drop-in Class-D amp module. Represents the module's mount pattern (4x M3 corner holes) and 12-pin through-hole interface header. Real module has 2 rows of high-current speaker+power terminals on the sides; this placeholder collapses them into a single-row header. **VERIFY module dimensions and pin locations against the Purifi 1ET7040SA reference/datasheet before layout.**
- `LM5116_HTSSOP24.kicad_mod` - TI LM5116 HTSSOP-24 with 3.4x5.0mm exposed pad (pin 25).
- `TPS3808_SOT23-5.kicad_mod` - TI TPS3808 supervisor SOT-23-5.
- `ADT7420_MSOP8.kicad_mod` - Analog Devices ADT7420 temperature sensor MSOP-8. Note: real ADT7420 is LFCSP-8; MSOP variant is shown here as a lower-risk placeholder.
- `WBT-0705_Terminal.kicad_mod` - WBT-0705Cu speaker binding-post terminal, 2-pin, 19.05mm pitch, 5.5mm drills. Panel-mount hardware.
- `Si8660_SOIC16.kicad_mod` - SiLabs Si8660BB 6-ch digital isolator SOIC-16 WB.

## Verification checklist (per footprint)

1. Cross-check package dimensions against the datasheet mechanical drawing.
2. Cross-check pad size and pitch against the recommended land pattern.
3. Cross-check pin-1 marker position against the datasheet ball/pad map.
4. Cross-check the courtyard against IPC-7351 (level B nominal for signal parts,
   level A dense for high-density QFNs, level C wide for high-voltage parts).
5. For the Purifi module: reconcile the placeholder single-row header against the
   actual module's dual-row terminal layout. Enlarge power terminals to 6-7mm
   drill for 6-8AWG rail wires.
6. For WBT terminals: confirm the panel cutout matches the mechanical enclosure.
""")

# ---------------------------------------------------------------------------
# Schematic - embed stdlib + specialty lib_symbols and place instances
# ---------------------------------------------------------------------------

STD_LIB_SYMS = r'''		(symbol "Device:R"
			(pin_numbers (hide yes))
			(pin_names (offset 0) (hide yes))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Value" "R" (at 0 0 90) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at -1.778 0 90) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "R_0_1"
				(rectangle (start -1.016 -2.54) (end 1.016 2.54) (stroke (width 0.254) (type default)) (fill (type none)))
			)
			(symbol "R_1_1"
				(pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:C"
			(pin_numbers (hide yes))
			(pin_names (offset 0.254) (hide yes))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "C" (at 0.635 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "C" (at 0.635 -2.54 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0.9652 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "C_0_1"
				(polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
				(polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
			)
			(symbol "C_1_1"
				(pin passive line (at 0 3.81 270) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:L"
			(pin_numbers (hide yes))
			(pin_names (offset 1.016) (hide yes))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "L" (at -1.27 0 90) (effects (font (size 1.27 1.27))))
			(property "Value" "L" (at 1.905 0 90) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "L_0_1"
				(arc (start 0 -2.54) (mid 0.6323 -1.905) (end 0 -1.27) (stroke (width 0) (type default)) (fill (type none)))
				(arc (start 0 -1.27) (mid 0.6323 -0.635) (end 0 0) (stroke (width 0) (type default)) (fill (type none)))
				(arc (start 0 0) (mid 0.6323 0.635) (end 0 1.27) (stroke (width 0) (type default)) (fill (type none)))
				(arc (start 0 1.27) (mid 0.6323 1.905) (end 0 2.54) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "L_1_1"
				(pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Connector:Conn_01x02_Pin"
			(pin_names (offset 1.016) (hide yes))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "J" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Conn_01x02_Pin" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "Conn_01x02_Pin_1_1"
				(rectangle (start -1.27 -1.27) (end 0 -3.81) (stroke (width 0.1524) (type default)) (fill (type outline)))
				(rectangle (start -1.27 1.27) (end 0 -1.27) (stroke (width 0.1524) (type default)) (fill (type outline)))
				(pin passive line (at 3.81 0 180) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 3.81 -2.54 180) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Connector:Conn_01x04_Pin"
			(pin_names (offset 1.016) (hide yes))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Conn_01x04_Pin" (at 0 -10.16 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "Conn_01x04_Pin_1_1"
				(rectangle (start -1.27 3.81) (end 0 1.27) (stroke (width 0.1524) (type default)) (fill (type outline)))
				(rectangle (start -1.27 1.27) (end 0 -1.27) (stroke (width 0.1524) (type default)) (fill (type outline)))
				(rectangle (start -1.27 -1.27) (end 0 -3.81) (stroke (width 0.1524) (type default)) (fill (type outline)))
				(rectangle (start -1.27 -3.81) (end 0 -6.35) (stroke (width 0.1524) (type default)) (fill (type outline)))
				(pin passive line (at 3.81 2.54 180) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 3.81 0 180) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 3.81 -2.54 180) (length 3.81) (name "Pin_3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 3.81 -5.08 180) (length 3.81) (name "Pin_4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
			)
		)
'''

POWER_SYMS_TMPL = r'''		(symbol "power:{net}"
			(power)
			(pin_names (offset 0))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "{net}" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "{net}_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27) (xy 0 0) (xy -0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "{net}_1_1"
				(pin power_in line (at 0 0 90) (length 0) (hide yes) (name "{net}" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
'''
GND_SYM = r'''		(symbol "power:GND"
			(power)
			(pin_names (offset 0))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "GND_0_1"
				(polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "GND_1_1"
				(pin power_in line (at 0 0 270) (length 0) (hide yes) (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
'''

# Root sheet UUID
SHEET_UUID = "11111111-2222-4333-8444-000000000001"

def _read_lib_symbol(lib_text, name):
    """Extract a full (symbol "name" ...) block by paren counting."""
    marker = f'(symbol "{name}"'
    i = lib_text.find(marker)
    if i < 0:
        raise ValueError(f"symbol {name!r} not found")
    depth = 0
    j = i
    while j < len(lib_text):
        c = lib_text[j]
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return lib_text[i:j+1]
        j += 1
    raise ValueError("unbalanced")

def sch_instance(lib_id, ref, value, footprint, x, y, uid, unit=1, angle=0):
    return (
        f'\t(symbol\n'
        f'\t\t(lib_id "{lib_id}")\n'
        f'\t\t(at {x} {y} {angle})\n'
        f'\t\t(unit {unit})\n'
        f'\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(dnp no)\n'
        f'\t\t(uuid "{uid}")\n'
        f'\t\t(property "Reference" "{ref}"\n\t\t\t(at {x+3} {y-5} 0)\n\t\t\t(effects (font (size 1.27 1.27)))\n\t\t)\n'
        f'\t\t(property "Value" "{value}"\n\t\t\t(at {x+3} {y+5} 0)\n\t\t\t(effects (font (size 1.27 1.27)))\n\t\t)\n'
        f'\t\t(property "Footprint" "{footprint}"\n\t\t\t(at {x} {y} 0)\n\t\t\t(effects (font (size 1.27 1.27)) (hide yes))\n\t\t)\n'
        f'\t\t(property "Datasheet" "~"\n\t\t\t(at {x} {y} 0)\n\t\t\t(effects (font (size 1.27 1.27)) (hide yes))\n\t\t)\n'
        f'\t\t(instances\n'
        f'\t\t\t(project "palpod-audio-amp"\n'
        f'\t\t\t\t(path "/{SHEET_UUID}"\n'
        f'\t\t\t\t\t(reference "{ref}")\n'
        f'\t\t\t\t\t(unit {unit})\n'
        f'\t\t\t\t)\n'
        f'\t\t\t)\n'
        f'\t\t)\n'
        f'\t)\n'
    )

def sch_label(text, x, y, angle=0):
    return (
        f'\t(label "{text}"\n'
        f'\t\t(at {x} {y} {angle})\n'
        f'\t\t(effects (font (size 1.27 1.27)) (justify left bottom))\n'
        f'\t\t(uuid "{U("lbl"+text+str(x)+str(y))}")\n'
        f'\t)\n'
    )

def sch_wire(x1, y1, x2, y2):
    return (
        f'\t(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{U("w"+str(x1)+str(y1)+str(x2)+str(y2))}"))\n'
    )

def sch_noconn(x, y):
    return f'\t(no_connect (at {x} {y}) (uuid "{U("nc"+str(x)+str(y))}"))\n'


def build_schematic():
    lib_text = LIB_SYM.read_text()
    # Extract the 9 custom symbol definitions from generated lib
    custom_names = ["CS43198","CS2100-CP","THAT1512","Purifi_1ET7040SA","LM5116",
                    "TPS3808G01","ADT7420","WBT-0705","Si8660BB"]
    custom_blocks = []
    for n in custom_names:
        block = _read_lib_symbol(lib_text, n)
        # Rewrite (symbol "NAME" ...) to (symbol "palpod-audio-amp:NAME" ...)
        block = block.replace(f'(symbol "{n}"', f'(symbol "palpod-audio-amp:{n}"', 1)
        # Increase indent by 1 tab
        custom_blocks.append('\n'.join('\t' + line for line in block.splitlines()) + '\n')

    # ---- Instances ----
    ref = 0
    instances = []

    def add(lib_id, ref_prefix, value, footprint, x, y, angle=0):
        nonlocal ref
        ref += 1
        rr = f"{ref_prefix}{ref}"
        uid = U(f"inst-{lib_id}-{rr}")
        instances.append(sch_instance(lib_id, rr, value, footprint, x, y, uid, angle=angle))
        return rr

    # PSU input connector
    add("Connector:Conn_01x04_Pin", "J", "PSU_INPUT",
        "TerminalBlock:TerminalBlock_bornier-4_P5.08mm", 30, 30)

    # Balanced I2S input connector
    add("Connector:Conn_01x04_Pin", "J", "I2S_DSD_IN",
        "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", 30, 60)

    # Master clock (CS2100)
    add("palpod-audio-amp:CS2100-CP", "U", "CS2100-CP",
        "palpod-audio-amp:CS2100_MSOP10", 80, 45)

    # Digital isolator between DAC domain and rest of chain
    add("palpod-audio-amp:Si8660BB", "U", "Si8660BB-B-IS1",
        "palpod-audio-amp:Si8660_SOIC16", 130, 45)

    # 4x DACs
    dac_positions = [(60, 100), (140, 100), (60, 170), (140, 170)]
    dac_labels = ["TWEETER", "MID", "WOOFER", "SUBWOOFER"]
    for (x,y), lbl in zip(dac_positions, dac_labels):
        add("palpod-audio-amp:CS43198", "U", f"CS43198_{lbl}",
            "palpod-audio-amp:CS43198_TQFN32", x, y)

    # 4x THAT1512 balanced receivers (one per channel, after DAC diff-out reconstruction)
    that_positions = [(30, 120), (110, 120), (30, 190), (110, 190)]
    for (x,y), lbl in zip(that_positions, dac_labels):
        add("palpod-audio-amp:THAT1512", "U", f"THAT1512_{lbl}",
            "palpod-audio-amp:THAT1512_SOIC8", x, y)

    # 4x Purifi 1ET7040SA carrier connectors
    purifi_positions = [(220, 105), (260, 105), (220, 175), (260, 175)]
    for (x,y), lbl in zip(purifi_positions, dac_labels):
        add("palpod-audio-amp:Purifi_1ET7040SA", "A", f"1ET7040SA_{lbl}",
            "palpod-audio-amp:Purifi_1ET7040SA_Module", x, y)

    # PSU: LM5116 SMPS controller for +/-60V rails (single instance shown - real design has 2 stages)
    add("palpod-audio-amp:LM5116", "U", "LM5116MHX_PLUS60V",
        "palpod-audio-amp:LM5116_HTSSOP24", 80, 220)
    add("palpod-audio-amp:LM5116", "U", "LM5116MHX_MINUS60V",
        "palpod-audio-amp:LM5116_HTSSOP24", 130, 220)

    # TPS3808 supervisor
    add("palpod-audio-amp:TPS3808G01", "U", "TPS3808G01DBVR",
        "palpod-audio-amp:TPS3808_SOT23-5", 180, 220)

    # 4x ADT7420 temperature sensors (one per Purifi module)
    adt_positions = [(220, 130), (260, 130), (220, 200), (260, 200)]
    for (x,y), lbl in zip(adt_positions, dac_labels):
        add("palpod-audio-amp:ADT7420", "U", f"ADT7420_{lbl}",
            "palpod-audio-amp:ADT7420_MSOP8", x, y)

    # 4x WBT speaker terminals
    wbt_positions = [(310, 105), (310, 130), (310, 175), (310, 200)]
    for (x,y), lbl in zip(wbt_positions, dac_labels):
        add("palpod-audio-amp:WBT-0705", "J", f"SPKR_{lbl}",
            "palpod-audio-amp:WBT-0705_Terminal", x, y)

    # A pile of decoupling caps and gain-set resistors (representative,
    # not exhaustive - EE fills in the rest during wiring)
    cap_x = 20
    cap_y = 250
    for i in range(24):
        add("Device:C", "C", "100nF",
            "Capacitor_SMD:C_0402_1005Metric", cap_x + (i%12)*10, cap_y + (i//12)*10)
    for i in range(8):
        add("Device:C", "C", "10uF",
            "Capacitor_SMD:C_0805_2012Metric", cap_x + i*10, cap_y + 25)
    # Bulk aluminum caps for HV rail
    for i in range(4):
        add("Device:C", "C", "1000uF/100V",
            "Capacitor_THT:CP_Radial_D18.0mm_P7.50mm", 40 + i*20, 210)
    # Resistors: I2C pull-ups + gain resistors
    for i in range(8):
        add("Device:R", "R", "4.7k",
            "Resistor_SMD:R_0402_1005Metric", cap_x + i*10, cap_y + 40)
    # Inductors for LM5116 output
    for i in range(2):
        add("Device:L", "L", "22uH",
            "Inductor_SMD:L_Coilcraft_XAL1010", 80 + i*50, 240)

    # ---- Assemble the schematic ----
    parts = []
    parts.append(
        '(kicad_sch\n'
        '\t(version 20231120)\n'
        '\t(generator "eeschema")\n'
        '\t(generator_version "8.0")\n'
        f'\t(uuid "{U("root-sch")}")\n'
        '\t(paper "A3")\n'
        '\t(title_block\n'
        '\t\t(title "PAL Pod Audio Amp")\n'
        '\t\t(date "2026-08-03")\n'
        '\t\t(rev "A0")\n'
        '\t\t(company "PAL Pod")\n'
        '\t\t(comment 1 "4-way active amplification: 4x CS43198 DAC + 4x Purifi 1ET7040SA Class-D modules")\n'
        '\t\t(comment 2 "Board: 6-layer, 250x200mm, +-60V HV rails, star-grounded analog")\n'
        '\t\t(comment 3 "Reference: hardware/electrical/block-diagrams/audio-amp.md")\n'
        '\t\t(comment 4 "PLACEHOLDER schematic - EE to complete wiring, run ERC")\n'
        '\t)\n'
        '\t(lib_symbols\n'
    )
    # Standard lib symbols
    parts.append(STD_LIB_SYMS)
    # Power symbols
    for net in ["+5V","+3V3","+12V","+15V","-15V","+60V","-60V"]:
        # sanitize KiCad power sym IDs
        parts.append(POWER_SYMS_TMPL.format(net=net))
    parts.append(GND_SYM)
    # Custom lib symbols
    for b in custom_blocks:
        parts.append(b)
    parts.append('\t)\n')  # close lib_symbols

    # Instances
    for inst in instances:
        parts.append(inst)

    # A few illustrative wires + labels to seed net topology
    parts.append(sch_wire(30, 30, 30, 25))
    parts.append(sch_label("+60V", 30, 27))
    parts.append(sch_wire(35, 30, 35, 25))
    parts.append(sch_label("-60V", 35, 27))
    parts.append(sch_wire(40, 30, 40, 25))
    parts.append(sch_label("GND", 40, 27))
    parts.append(sch_wire(45, 30, 45, 25))
    parts.append(sch_label("+12V", 45, 27))

    # I2S/DSD input labels
    for i,n in enumerate(["I2S_BCK","I2S_LRCK","I2S_SDIN","DSD_CLK"]):
        parts.append(sch_wire(30 + i*3, 60, 30+i*3, 55))
        parts.append(sch_label(n, 30+i*3, 57))

    # A few speaker output labels near WBT terminals
    for i,lbl in enumerate(["TWEETER","MID","WOOFER","SUB"]):
        parts.append(sch_label(f"SPKR_{lbl}+", 305, 95+i*30))
        parts.append(sch_label(f"SPKR_{lbl}-", 305, 98+i*30))

    # +5V / +3V3 / +15V / -15V analog rail bus at top of sheet
    for i,n in enumerate(["+5V","+3V3","+15V","-15V","+60V","-60V"]):
        parts.append(sch_label(n, 200 + i*10, 30))

    # I2C bus labels
    parts.append(sch_label("I2C_SCL", 100, 65))
    parts.append(sch_label("I2C_SDA", 100, 68))

    # Fault/mute labels
    for lbl in ["TWEETER","MID","WOOFER","SUBWOOFER"]:
        parts.append(sch_label(f"MUTE_{lbl}", 250, 155))
        parts.append(sch_label(f"FAULT_{lbl}_N", 250, 158))

    # No-connect flags on a few DAC test pins (illustrative)
    parts.append(sch_noconn(90, 100))
    parts.append(sch_noconn(90, 170))
    parts.append(sch_noconn(170, 100))
    parts.append(sch_noconn(170, 170))

    parts.append('\t(sheet_instances\n\t\t(path "/" (page "1"))\n\t)\n')
    parts.append(')\n')

    SCH.write_text(''.join(parts))


# ---------------------------------------------------------------------------
# PCB - 6 layer stackup, 250x200mm rectangle Edge.Cuts
# ---------------------------------------------------------------------------

def build_pcb():
    text = f'''(kicad_pcb
  (version 20240108)
  (generator "pcbnew")
  (generator_version "8.0")
  (general
    (thickness 1.6)
    (legacy_teardrops no)
  )
  (paper "A3")
  (title_block
    (title "PAL Pod Audio Amp - PCB")
    (date "2026-08-03")
    (rev "A0")
    (company "PAL Pod")
    (comment 1 "6-layer 250mm x 200mm rectangular board")
    (comment 2 "F.Cu / In1.Cu (GND) / In2.Cu (PWR_analog) / In3.Cu (PWR_60V) / In4.Cu (GND) / B.Cu")
    (comment 3 "2oz outer copper for HV/speaker traces, 1oz inner. ENIG finish.")
  )
  (layers
    (0 "F.Cu" signal)
    (1 "In1.Cu" power "GND1")
    (2 "In2.Cu" power "PWR_ANA")
    (3 "In3.Cu" power "PWR_HV")
    (4 "In4.Cu" power "GND2")
    (31 "B.Cu" signal)
    (32 "B.Adhes" user "B.Adhesive")
    (33 "F.Adhes" user "F.Adhesive")
    (34 "B.Paste" user)
    (35 "F.Paste" user)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (40 "Dwgs.User" user "User.Drawings")
    (41 "Cmts.User" user "User.Comments")
    (42 "Eco1.User" user "User.Eco1")
    (43 "Eco2.User" user "User.Eco2")
    (44 "Edge.Cuts" user)
    (45 "Margin" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
    (48 "B.Fab" user)
    (49 "F.Fab" user)
    (50 "User.1" user)
    (51 "User.2" user)
    (52 "User.3" user)
    (53 "User.4" user)
    (54 "User.5" user)
    (55 "User.6" user)
    (56 "User.7" user)
    (57 "User.8" user)
    (58 "User.9" user)
  )
  (setup
    (stackup
      (layer "F.SilkS" (type "Top Silk Screen"))
      (layer "F.Paste" (type "Top Solder Paste"))
      (layer "F.Mask" (type "Top Solder Mask") (color "Green") (thickness 0.01))
      (layer "F.Cu" (type "copper") (thickness 0.07))
      (layer "dielectric 1" (type "prepreg") (thickness 0.15) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In1.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 2" (type "core") (thickness 0.2) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In2.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 3" (type "prepreg") (thickness 0.36) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In3.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 4" (type "core") (thickness 0.2) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In4.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 5" (type "prepreg") (thickness 0.15) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "B.Cu" (type "copper") (thickness 0.07))
      (layer "B.Mask" (type "Bottom Solder Mask") (color "Green") (thickness 0.01))
      (layer "B.Paste" (type "Bottom Solder Paste"))
      (layer "B.SilkS" (type "Bottom Silk Screen"))
      (copper_finish "ENIG")
      (dielectric_constraints no)
      (edge_connector no)
      (castellated_pads no)
      (edge_plating no)
    )
    (pad_to_mask_clearance 0)
    (allow_soldermask_bridges_in_footprints no)
    (pcbplotparams
      (layerselection 0x00000000_00000000_55555555_5755f5ff)
      (plot_on_all_layers_selection 0x00000000_00000000_00000000_00000000)
      (disableapertmacros no)
      (usegerberextensions no)
      (usegerberattributes yes)
      (usegerberadvancedattributes yes)
      (creategerberjobfile yes)
      (dashed_line_dash_ratio 12.000000)
      (dashed_line_gap_ratio 3.000000)
      (svgprecision 4)
      (plotframeref no)
      (viasonmask no)
      (mode 1)
      (useauxorigin no)
      (hpglpennumber 1)
      (hpglpenspeed 20)
      (hpglpendiameter 15.000000)
      (pdf_front_fp_property_popups yes)
      (pdf_back_fp_property_popups yes)
      (dxfpolygonmode yes)
      (dxfimperialunits yes)
      (dxfusepcbnewfont yes)
      (psnegative no)
      (psa4output no)
      (plotreference yes)
      (plotvalue yes)
      (plotfptext yes)
      (plotinvisibletext no)
      (sketchpadsonfab no)
      (subtractmaskfromsilk no)
      (outputformat 1)
      (mirror no)
      (drillshape 1)
      (scaleselection 1)
      (outputdirectory "gerbers/")
    )
  )
  (net 0 "")
  (net 1 "+60V")
  (net 2 "-60V")
  (net 3 "+15V")
  (net 4 "-15V")
  (net 5 "+12V")
  (net 6 "+5V")
  (net 7 "+3V3")
  (net 8 "GND")
  (net 9 "GND_HV")
  (net 10 "GND_ANA")
  (net 11 "I2S_BCK")
  (net 12 "I2S_LRCK")
  (net 13 "I2S_SDIN")
  (net 14 "I2S_MCLK")
  (net 15 "DSD_CLK")
  (net 16 "DSD_L")
  (net 17 "DSD_R")
  (net 18 "I2C_SCL")
  (net 19 "I2C_SDA")
  (net 20 "SPKR_TWEETER+")
  (net 21 "SPKR_TWEETER-")
  (net 22 "SPKR_MID+")
  (net 23 "SPKR_MID-")
  (net 24 "SPKR_WOOFER+")
  (net 25 "SPKR_WOOFER-")
  (net 26 "SPKR_SUBWOOFER+")
  (net 27 "SPKR_SUBWOOFER-")
  (net 28 "MUTE_TWEETER")
  (net 29 "MUTE_MID")
  (net 30 "MUTE_WOOFER")
  (net 31 "MUTE_SUBWOOFER")
  (net 32 "FAULT_TWEETER_N")
  (net 33 "FAULT_MID_N")
  (net 34 "FAULT_WOOFER_N")
  (net 35 "FAULT_SUBWOOFER_N")
  (net 36 "PWR_GOOD_N")

  (gr_line (start 0 0)     (end 250 0)   (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{U("edge1")}"))
  (gr_line (start 250 0)   (end 250 200) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{U("edge2")}"))
  (gr_line (start 250 200) (end 0 200)   (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{U("edge3")}"))
  (gr_line (start 0 200)   (end 0 0)     (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{U("edge4")}"))

  (gr_text "PAL Pod Audio Amp - Rev A0 - PLACEHOLDER PCB"
    (at 10 10 0)
    (layer "F.SilkS")
    (uuid "{U("title-text-1")}")
    (effects (font (size 3 3) (thickness 0.4)) (justify left bottom))
  )
  (gr_text "See ../block-diagrams/audio-amp.md and README for signal chain, BOM, and layout plan"
    (at 10 15 0)
    (layer "F.SilkS")
    (uuid "{U("title-text-2")}")
    (effects (font (size 1.4 1.4) (thickness 0.2)) (justify left bottom))
  )
  (gr_text "HV domain (right half) - keep 3mm min clearance to LV domain across the 60V isolation moat"
    (at 130 190 0)
    (layer "Cmts.User")
    (uuid "{U("cmt-1")}")
    (effects (font (size 2 2) (thickness 0.3)) (justify left bottom))
  )
  (gr_text "Star ground point - single-point tie between GND_ANA / GND_HV / chassis"
    (at 10 195 0)
    (layer "Cmts.User")
    (uuid "{U("cmt-2")}")
    (effects (font (size 1.6 1.6) (thickness 0.25)) (justify left bottom))
  )
)
'''
    PCB.write_text(text)


if __name__ == "__main__":
    build_sym_lib()
    build_footprints()
    build_schematic()
    build_pcb()
    print("Generated:", LIB_SYM, PRETTY, SCH, PCB)

#!/usr/bin/env python3
"""Generate palpod-mic-array.kicad_sch — root schematic with placed symbols.

Uses KiCad 8+ schema (20231120) with the newer effect/property syntax that
also loads under KiCad 9 and 10 (`(hide yes)` inside effects, `exclude_from_sim`,
etc.). Tabs for indent to match KiCad's own writer.
"""
from pathlib import Path
import uuid, hashlib, math

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "palpod-mic-array.kicad_sch"
SYM = ROOT / "libraries" / "palpod-mic-array.kicad_sym"

def U(seed):
    return str(uuid.UUID(bytes=hashlib.md5(seed.encode()).digest()[:16], version=4))

ROOT_UUID = U("root-sheet")

# --------- extract local symbol blocks ---------
def embed_local():
    txt = SYM.read_text()
    out = []
    depth = 0
    i = 0
    start = None
    while i < len(txt):
        c = txt[i]
        if c == "(":
            depth += 1
            if depth == 2 and txt[i:i+8] == "(symbol ":
                start = i
        elif c == ")":
            depth -= 1
            if depth == 1 and start is not None:
                out.append(txt[start:i+1])
                start = None
        i += 1
    rewritten = []
    for block in out:
        head_end = block.index('"')
        after = block.index('"', head_end + 1)
        name = block[head_end+1:after]
        new = block[:head_end+1] + "palpod-mic-array:" + name + block[after:]
        # Child unit names stay bare in KiCad's own writer (e.g. "Conn_01x02_1_1")
        # but the schematic loader accepts either form. Keep bare to match convention.
        rewritten.append(new)
    return rewritten

local_sym_blocks = embed_local()


# --------- stdlib symbol stubs (new-syntax) ---------

def std_prop(name, val, x, y, rot=0, hidden=False, indent=3):
    tab = "\t" * indent
    hide = f"\n{tab}\t\t(hide yes)" if hidden else ""
    return (f'{tab}(property "{name}" "{val}"\n'
            f'{tab}\t(at {x} {y} {rot})\n'
            f'{tab}\t(effects\n'
            f'{tab}\t\t(font (size 1.27 1.27)){hide}\n'
            f'{tab}\t)\n'
            f'{tab})\n')

def sym_def_pin(etype, style, x, y, ang, length, name, number, indent=4, hidden=False):
    tab = "\t" * indent
    hide = f"\n{tab}\t(hide yes)" if hidden else ""
    return (f'{tab}(pin {etype} {style}\n'
            f'{tab}\t(at {x} {y} {ang})\n'
            f'{tab}\t(length {length}){hide}\n'
            f'{tab}\t(name "{name}"\n'
            f'{tab}\t\t(effects (font (size 1.27 1.27)))\n'
            f'{tab}\t)\n'
            f'{tab}\t(number "{number}"\n'
            f'{tab}\t\t(effects (font (size 1.27 1.27)))\n'
            f'{tab}\t)\n'
            f'{tab})\n')


def sym_R():
    return f'''\t\t(symbol "Device:R"
\t\t\t(pin_numbers
\t\t\t\t(hide yes)
\t\t\t)
\t\t\t(pin_names
\t\t\t\t(offset 0)
\t\t\t\t(hide yes)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
{std_prop("Reference","R",2.032,0,90)}{std_prop("Value","R",0,0,90)}{std_prop("Footprint","",-1.778,0,90,hidden=True)}{std_prop("Datasheet","~",0,0,0,hidden=True)}\t\t\t(symbol "R_0_1"
\t\t\t\t(rectangle
\t\t\t\t\t(start -1.016 -2.54)
\t\t\t\t\t(end 1.016 2.54)
\t\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t\t(fill (type none))
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "R_1_1"
{sym_def_pin("passive","line",0,3.81,270,1.27,"~","1")}{sym_def_pin("passive","line",0,-3.81,90,1.27,"~","2")}\t\t\t)
\t\t)
'''


def sym_C():
    return f'''\t\t(symbol "Device:C"
\t\t\t(pin_numbers
\t\t\t\t(hide yes)
\t\t\t)
\t\t\t(pin_names
\t\t\t\t(offset 0.254)
\t\t\t\t(hide yes)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
{std_prop("Reference","C",0.635,2.54,0)}{std_prop("Value","C",0.635,-2.54,0)}{std_prop("Footprint","",0.9652,-3.81,0,hidden=True)}{std_prop("Datasheet","~",0,0,0,hidden=True)}\t\t\t(symbol "C_0_1"
\t\t\t\t(polyline
\t\t\t\t\t(pts (xy -2.032 -0.762) (xy 2.032 -0.762))
\t\t\t\t\t(stroke (width 0.508) (type default))
\t\t\t\t\t(fill (type none))
\t\t\t\t)
\t\t\t\t(polyline
\t\t\t\t\t(pts (xy -2.032 0.762) (xy 2.032 0.762))
\t\t\t\t\t(stroke (width 0.508) (type default))
\t\t\t\t\t(fill (type none))
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "C_1_1"
{sym_def_pin("passive","line",0,3.81,270,2.794,"~","1")}{sym_def_pin("passive","line",0,-3.81,90,2.794,"~","2")}\t\t\t)
\t\t)
'''


def sym_power(name, netname):
    return f'''\t\t(symbol "power:{name}"
\t\t\t(power)
\t\t\t(pin_names
\t\t\t\t(offset 0)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
{std_prop("Reference","#PWR",0,-3.81,0,hidden=True)}{std_prop("Value",netname,0,3.81,0)}{std_prop("Footprint","",0,0,0,hidden=True)}{std_prop("Datasheet","",0,0,0,hidden=True)}\t\t\t(symbol "{name}_0_1"
\t\t\t\t(polyline
\t\t\t\t\t(pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27) (xy 0 0) (xy -0.762 1.27))
\t\t\t\t\t(stroke (width 0) (type default))
\t\t\t\t\t(fill (type none))
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "{name}_1_1"
{sym_def_pin("power_in","line",0,0,90,0,netname,"1",hidden=True)}\t\t\t)
\t\t)
'''


def sym_gnd():
    return f'''\t\t(symbol "power:GND"
\t\t\t(power)
\t\t\t(pin_names
\t\t\t\t(offset 0)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
{std_prop("Reference","#PWR",0,-6.35,0,hidden=True)}{std_prop("Value","GND",0,-3.81,0)}{std_prop("Footprint","",0,0,0,hidden=True)}{std_prop("Datasheet","",0,0,0,hidden=True)}\t\t\t(symbol "GND_0_1"
\t\t\t\t(polyline
\t\t\t\t\t(pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27))
\t\t\t\t\t(stroke (width 0) (type default))
\t\t\t\t\t(fill (type none))
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "GND_1_1"
{sym_def_pin("power_in","line",0,0,270,0,"GND","1",hidden=True)}\t\t\t)
\t\t)
'''


def sym_ldo():
    """AP2114H-3.3 (SOT-223-3)"""
    return f'''\t\t(symbol "Regulator_Linear:AP2114H-3.3"
\t\t\t(pin_names
\t\t\t\t(offset 0.254)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
{std_prop("Reference","U",-5.08,5.715,0)}{std_prop("Value","AP2114H-3.3",2.54,5.715,0)}{std_prop("Footprint","Package_TO_SOT_SMD:SOT-223-3_TabPin2",0,-8.89,0,hidden=True)}{std_prop("Datasheet","https://www.diodes.com/assets/Datasheets/AP2114.pdf",0,0,0,hidden=True)}\t\t\t(symbol "AP2114H-3.3_0_1"
\t\t\t\t(rectangle
\t\t\t\t\t(start -5.08 3.81)
\t\t\t\t\t(end 5.08 -3.81)
\t\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t\t(fill (type background))
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "AP2114H-3.3_1_1"
{sym_def_pin("input","line",-7.62,2.54,0,2.54,"VI","3")}{sym_def_pin("power_in","line",0,-6.35,90,2.54,"GND","1")}{sym_def_pin("output","line",7.62,2.54,180,2.54,"VO","2")}\t\t\t)
\t\t)
'''


def sym_usbc():
    pins = ""
    pins += sym_def_pin("power_in", "line", -12.7, 15.24, 0, 2.54, "VBUS", "A4")
    pins += sym_def_pin("power_in", "line", -12.7, 12.7,  0, 2.54, "VBUS", "B4")
    pins += sym_def_pin("bidirectional", "line", -12.7, 7.62, 0, 2.54, "D+", "A6")
    pins += sym_def_pin("bidirectional", "line", -12.7, 5.08, 0, 2.54, "D-", "A7")
    pins += sym_def_pin("bidirectional", "line", -12.7, 2.54, 0, 2.54, "D+", "B6")
    pins += sym_def_pin("bidirectional", "line", -12.7, 0,    0, 2.54, "D-", "B7")
    pins += sym_def_pin("input", "line", -12.7, -5.08, 0, 2.54, "CC1", "A5")
    pins += sym_def_pin("input", "line", -12.7, -7.62, 0, 2.54, "CC2", "B5")
    pins += sym_def_pin("passive", "line", -12.7, -10.16, 0, 2.54, "SBU1", "A8")
    pins += sym_def_pin("passive", "line", -12.7, -12.7,  0, 2.54, "SBU2", "B8")
    pins += sym_def_pin("power_in", "line", 12.7, 15.24, 180, 2.54, "GND", "A1")
    pins += sym_def_pin("power_in", "line", 12.7, 12.7,  180, 2.54, "GND", "A12")
    pins += sym_def_pin("power_in", "line", 12.7, 10.16, 180, 2.54, "GND", "B1")
    pins += sym_def_pin("power_in", "line", 12.7, 7.62,  180, 2.54, "GND", "B12")
    pins += sym_def_pin("passive",  "line", 12.7, 2.54, 180, 2.54, "SHIELD", "S1")
    pins += sym_def_pin("passive",  "line", 12.7, 0,    180, 2.54, "SHIELD", "S2")
    return f'''\t\t(symbol "Connector:USB_C_Receptacle_USB2.0_16P"
\t\t\t(pin_names
\t\t\t\t(offset 1.016)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
{std_prop("Reference","J",0,20.32,0)}{std_prop("Value","USB_C_Receptacle_USB2.0_16P",0,-20.32,0)}{std_prop("Footprint","",0,0,0,hidden=True)}{std_prop("Datasheet","https://www.usb.org/",0,0,0,hidden=True)}\t\t\t(symbol "USB_C_Receptacle_USB2.0_16P_0_1"
\t\t\t\t(rectangle
\t\t\t\t\t(start -10.16 17.78)
\t\t\t\t\t(end 10.16 -17.78)
\t\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t\t(fill (type background))
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "USB_C_Receptacle_USB2.0_16P_1_1"
{pins}\t\t\t)
\t\t)
'''


def sym_stm32():
    pins = ""
    pins += sym_def_pin("power_in","line",-22.86,35.56,0,2.54,"VDD","5")
    pins += sym_def_pin("power_in","line",-22.86,33.02,0,2.54,"VDDA","13")
    pins += sym_def_pin("power_in","line",-22.86,30.48,0,2.54,"VSS","8")
    pins += sym_def_pin("power_in","line",-22.86,27.94,0,2.54,"VSSA","12")
    pins += sym_def_pin("input","line",-22.86,22.86,0,2.54,"NRST","7")
    pins += sym_def_pin("input","line",-22.86,20.32,0,2.54,"BOOT0","60")
    pins += sym_def_pin("input","line",-22.86,17.78,0,2.54,"OSC_IN","3")
    pins += sym_def_pin("output","line",-22.86,15.24,0,2.54,"OSC_OUT","4")
    pins += sym_def_pin("bidirectional","line",22.86,35.56,180,2.54,"PA0","14")
    pins += sym_def_pin("bidirectional","line",22.86,33.02,180,2.54,"PA1","15")
    pins += sym_def_pin("bidirectional","line",22.86,30.48,180,2.54,"PA2/USART2_TX","16")
    pins += sym_def_pin("bidirectional","line",22.86,27.94,180,2.54,"PA3/USART2_RX","17")
    pins += sym_def_pin("bidirectional","line",22.86,25.4,180,2.54,"PA8/USB_ULPI_D0","41")
    pins += sym_def_pin("bidirectional","line",22.86,22.86,180,2.54,"PA9/USB_ULPI_D1","42")
    pins += sym_def_pin("bidirectional","line",22.86,20.32,180,2.54,"PA13/SWDIO","46")
    pins += sym_def_pin("bidirectional","line",22.86,17.78,180,2.54,"PA14/SWCLK","49")
    pins += sym_def_pin("bidirectional","line",22.86,15.24,180,2.54,"PB6/I2C1_SCL","58")
    pins += sym_def_pin("bidirectional","line",22.86,12.7,180,2.54,"PB7/I2C1_SDA","59")
    return f'''\t\t(symbol "MCU_ST_STM32G4:STM32G474RETx"
\t\t\t(pin_names
\t\t\t\t(offset 1.016)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
{std_prop("Reference","U",0,40.64,0)}{std_prop("Value","STM32G474RETx",0,-40.64,0)}{std_prop("Footprint","Package_QFP:LQFP-64_10x10mm_P0.5mm",0,0,0,hidden=True)}{std_prop("Datasheet","https://www.st.com/resource/en/datasheet/stm32g474re.pdf",0,0,0,hidden=True)}\t\t\t(symbol "STM32G474RETx_0_1"
\t\t\t\t(rectangle
\t\t\t\t\t(start -20.32 38.1)
\t\t\t\t\t(end 20.32 -38.1)
\t\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t\t(fill (type background))
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "STM32G474RETx_1_1"
{pins}\t\t\t)
\t\t)
'''


def sym_usb3320():
    pins = ""
    pins += sym_def_pin("power_in","line",-12.7,15.24,0,2.54,"VDD33","13")
    pins += sym_def_pin("power_in","line",-12.7,12.7,0,2.54,"VDD18","27")
    pins += sym_def_pin("power_in","line",-12.7,10.16,0,2.54,"GND","33")
    pins += sym_def_pin("bidirectional","line",-12.7,5.08,0,2.54,"DP","20")
    pins += sym_def_pin("bidirectional","line",-12.7,2.54,0,2.54,"DM","19")
    pins += sym_def_pin("input","line",-12.7,0,0,2.54,"ID","22")
    pins += sym_def_pin("input","line",-12.7,-2.54,0,2.54,"VBUS","23")
    pins += sym_def_pin("bidirectional","line",12.7,15.24,180,2.54,"DATA0","3")
    pins += sym_def_pin("bidirectional","line",12.7,12.7,180,2.54,"DATA1","4")
    pins += sym_def_pin("bidirectional","line",12.7,10.16,180,2.54,"DATA2","5")
    pins += sym_def_pin("bidirectional","line",12.7,7.62,180,2.54,"DATA3","6")
    pins += sym_def_pin("bidirectional","line",12.7,5.08,180,2.54,"DATA4","7")
    pins += sym_def_pin("bidirectional","line",12.7,2.54,180,2.54,"DATA5","10")
    pins += sym_def_pin("bidirectional","line",12.7,0,180,2.54,"DATA6","11")
    pins += sym_def_pin("bidirectional","line",12.7,-2.54,180,2.54,"DATA7","12")
    pins += sym_def_pin("output","line",12.7,-7.62,180,2.54,"CLK","1")
    pins += sym_def_pin("bidirectional","line",12.7,-10.16,180,2.54,"DIR","8")
    pins += sym_def_pin("bidirectional","line",12.7,-12.7,180,2.54,"NXT","9")
    pins += sym_def_pin("bidirectional","line",12.7,-15.24,180,2.54,"STP","2")
    return f'''\t\t(symbol "Interface_USB:USB3320C"
\t\t\t(pin_names
\t\t\t\t(offset 1.016)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
{std_prop("Reference","U",0,20.32,0)}{std_prop("Value","USB3320C",0,-20.32,0)}{std_prop("Footprint","Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.35x3.35mm",0,0,0,hidden=True)}{std_prop("Datasheet","https://www.microchip.com/en-us/product/USB3320",0,0,0,hidden=True)}\t\t\t(symbol "USB3320C_0_1"
\t\t\t\t(rectangle
\t\t\t\t\t(start -10.16 17.78)
\t\t\t\t\t(end 10.16 -17.78)
\t\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t\t(fill (type background))
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "USB3320C_1_1"
{pins}\t\t\t)
\t\t)
'''


# --------- schematic-instance emitter ---------
def inst_prop(name, val, x, y, rot=0, hidden=False):
    tab = "\t\t"
    hide = f"\n{tab}\t\t(hide yes)" if hidden else ""
    return (f'{tab}(property "{name}" "{val}"\n'
            f'{tab}\t(at {x} {y} {rot})\n'
            f'{tab}\t(effects\n'
            f'{tab}\t\t(font (size 1.27 1.27)){hide}\n'
            f'{tab}\t)\n'
            f'{tab})\n')

def sym_instance(lib_id, x, y, rot, ref, val, uuid_seed, footprint=""):
    u = U(uuid_seed)
    props = ""
    props += inst_prop("Reference", ref, x + 2.54, y - 5.08, rot)
    props += inst_prop("Value", val, x + 2.54, y + 5.08, rot)
    props += inst_prop("Footprint", footprint, x, y, rot, hidden=True)
    props += inst_prop("Datasheet", "~", x, y, rot, hidden=True)
    return (f'\t(symbol\n'
            f'\t\t(lib_id "{lib_id}")\n'
            f'\t\t(at {x} {y} {rot})\n'
            f'\t\t(unit 1)\n'
            f'\t\t(exclude_from_sim no)\n'
            f'\t\t(in_bom yes)\n'
            f'\t\t(on_board yes)\n'
            f'\t\t(dnp no)\n'
            f'\t\t(uuid "{u}")\n'
            f'{props}'
            f'\t\t(instances\n'
            f'\t\t\t(project "palpod-mic-array"\n'
            f'\t\t\t\t(path "/{ROOT_UUID}"\n'
            f'\t\t\t\t\t(reference "{ref}")\n'
            f'\t\t\t\t\t(unit 1)\n'
            f'\t\t\t\t)\n'
            f'\t\t\t)\n'
            f'\t\t)\n'
            f'\t)\n')


def wire(x1, y1, x2, y2, seed):
    return (f'\t(wire\n'
            f'\t\t(pts (xy {x1} {y1}) (xy {x2} {y2}))\n'
            f'\t\t(stroke (width 0) (type default))\n'
            f'\t\t(uuid "{U(seed)}")\n'
            f'\t)\n')

def label(text, x, y, rot, seed):
    return (f'\t(label "{text}"\n'
            f'\t\t(at {x} {y} {rot})\n'
            f'\t\t(effects\n'
            f'\t\t\t(font (size 1.27 1.27))\n'
            f'\t\t\t(justify left bottom)\n'
            f'\t\t)\n'
            f'\t\t(uuid "{U(seed)}")\n'
            f'\t)\n')

def noconn(x, y, seed):
    return (f'\t(no_connect\n'
            f'\t\t(at {x} {y})\n'
            f'\t\t(uuid "{U(seed)}")\n'
            f'\t)\n')


# --------- build ---------

STDLIB = [
    sym_R(), sym_C(),
    sym_power("+5V", "+5V"), sym_power("+3V3", "+3V3"),
    sym_power("+1V8", "+1V8"), sym_power("+1V0", "+1V0"),
    sym_gnd(),
    sym_ldo(),
    sym_usbc(), sym_stm32(), sym_usb3320(),
]

sch = []
sch.append('(kicad_sch\n')
sch.append('\t(version 20231120)\n')
sch.append('\t(generator "eeschema")\n')
sch.append('\t(generator_version "8.0")\n')
sch.append(f'\t(uuid "{ROOT_UUID}")\n')
sch.append('\t(paper "A3")\n')
sch.append('\t(title_block\n')
sch.append('\t\t(title "PAL Pod Mic Array")\n')
sch.append('\t\t(date "2026-08-03")\n')
sch.append('\t\t(rev "A0")\n')
sch.append('\t\t(company "PAL Pod")\n')
sch.append('\t\t(comment 1 "13-mic dual-ring far-field array with XVF3800 beamformer, NDP120 wake, STM32G474 host")\n')
sch.append('\t\t(comment 2 "Board: 4-layer, 120mm dia round, USB 2.0 hi-speed uplink")\n')
sch.append('\t\t(comment 3 "Reference: hardware/electrical/mic-array-reference-design.md")\n')
sch.append('\t\t(comment 4 "PLACEHOLDER schematic - EE to complete wiring, run ERC")\n')
sch.append('\t)\n')

sch.append('\t(lib_symbols\n')
for body in STDLIB:
    sch.append(body)
for block in local_sym_blocks:
    # indent each line of the local block by 2 tabs
    indented = "\t\t" + block.replace("\n", "\n\t\t") + "\n"
    sch.append(indented)
sch.append('\t)\n')

# --- power flags ---
sch.append(sym_instance("power:+5V",  30, 30, 0,  "#PWR01", "+5V",  "PWR-5V"))
sch.append(sym_instance("power:+3V3", 60, 30, 0,  "#PWR02", "+3V3", "PWR-3V3"))
sch.append(sym_instance("power:+1V8", 90, 30, 0,  "#PWR03", "+1V8", "PWR-1V8"))
sch.append(sym_instance("power:+1V0", 120, 30, 0, "#PWR04", "+1V0", "PWR-1V0"))
sch.append(sym_instance("power:GND",  150, 30, 0, "#PWR05", "GND",  "PWR-GND1"))
sch.append(sym_instance("power:GND",  30, 100, 0, "#PWR06", "GND",  "PWR-GND2"))
sch.append(sym_instance("power:GND",  180, 100, 0,"#PWR07", "GND",  "PWR-GND3"))

# --- LDOs ---
sch.append(sym_instance("Regulator_Linear:AP2114H-3.3", 60, 70, 0,  "U5", "AP2114H-3.3", "U5-LDO33",
                        footprint="Package_TO_SOT_SMD:SOT-223-3_TabPin2"))
sch.append(sym_instance("Regulator_Linear:AP2114H-3.3", 100, 70, 0, "U6", "TLV70218",    "U6-LDO18",
                        footprint="Package_TO_SOT_SMD:SOT-223-3_TabPin2"))
sch.append(sym_instance("Regulator_Linear:AP2114H-3.3", 140, 70, 0, "U7", "TPS7A02-1.0", "U7-LDO10",
                        footprint="Package_TO_SOT_SMD:SOT-223-3_TabPin2"))

# --- decoupling caps ---
for i, (x, cval, refn) in enumerate([(45, "10uF", "C1"), (75, "10uF", "C2"),
                                      (85, "10uF", "C3"), (115, "10uF", "C4"),
                                      (125, "10uF", "C5"), (155, "10uF", "C6")]):
    sch.append(sym_instance("Device:C", x, 90, 0, refn, cval, f"C-BULK-{refn}",
                            footprint="Capacitor_SMD:C_0603_1608Metric"))

# --- USB-C ---
sch.append(sym_instance("Connector:USB_C_Receptacle_USB2.0_16P", 40, 180, 0,
                        "J1", "USB4110-GF-A", "J1-USBC",
                        footprint="Connector_USB:USB_C_Receptacle_GCT_USB4110-xx-A"))
# --- USB PHY ---
sch.append(sym_instance("Interface_USB:USB3320C", 90, 180, 0,
                        "U3", "USB3320C-EZK-TR", "U3-USBPHY",
                        footprint="Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.35x3.35mm"))
# --- STM32 ---
sch.append(sym_instance("MCU_ST_STM32G4:STM32G474RETx", 155, 175, 0,
                        "U4", "STM32G474RETx", "U4-STM32",
                        footprint="Package_QFP:LQFP-64_10x10mm_P0.5mm"))
# --- XVF3800 ---
sch.append(sym_instance("palpod-mic-array:XVF3800", 220, 145, 0,
                        "U1", "XVF3800-INBW", "U1-XMOS",
                        footprint="palpod-mic-array:XVF3800_LFBGA61"))
# --- NDP120 ---
sch.append(sym_instance("palpod-mic-array:NDP120", 290, 145, 0,
                        "U2", "NDP120", "U2-NDP",
                        footprint="palpod-mic-array:NDP120_LGA69"))

# --- 13 mics ---
mic_center = (140, 100)
inner_radius = 25
outer_radius = 45
count = 0
for i in range(7):
    ang = 2 * math.pi * i / 7
    x = mic_center[0] + outer_radius * math.cos(ang)
    y = mic_center[1] + outer_radius * math.sin(ang)
    count += 1
    ref = f"M{count}"
    sch.append(sym_instance("palpod-mic-array:ICS-41352",
                            round(x, 2), round(y, 2), 0, ref, "ICS-41352",
                            f"MIC-{ref}",
                            footprint="palpod-mic-array:ICS-41352_LGA5"))
for i in range(6):
    ang = 2 * math.pi * i / 6 + math.pi / 6
    x = mic_center[0] + inner_radius * math.cos(ang)
    y = mic_center[1] + inner_radius * math.sin(ang)
    count += 1
    ref = f"M{count}"
    sch.append(sym_instance("palpod-mic-array:ICS-41352",
                            round(x, 2), round(y, 2), 0, ref, "ICS-41352",
                            f"MIC-{ref}",
                            footprint="palpod-mic-array:ICS-41352_LGA5"))

# --- more decap ---
for x, refn in [(210, "C10"), (220, "C11"), (230, "C12"),
                (280, "C13"), (290, "C14"), (300, "C15")]:
    sch.append(sym_instance("Device:C", x, 205, 0, refn, "100nF",
                            f"C-DECAP-{refn}",
                            footprint="Capacitor_SMD:C_0402_1005Metric"))

# --- illustrative wires ---
sch.append(wire(30, 30, 30, 65, "w1a"))
sch.append(wire(30, 65, 52.38, 65, "w1b"))
sch.append(wire(60, 30, 60, 65, "w2"))
sch.append(wire(90, 30, 90, 65, "w3"))
sch.append(wire(178, 190, 207, 190, "w4"))

# --- labels ---
sch.append(label("+5V", 30, 32, 0, "lbl-5v"))
sch.append(label("+3V3", 60, 32, 0, "lbl-33"))
sch.append(label("+1V8", 90, 32, 0, "lbl-18"))
sch.append(label("+1V0", 120, 32, 0, "lbl-10"))
sch.append(label("I2C_SCL", 190, 190, 0, "lbl-scl"))
sch.append(label("I2C_SDA", 190, 187, 0, "lbl-sda"))
sch.append(label("USB_DP", 27, 187, 0, "lbl-dp"))
sch.append(label("USB_DN", 27, 184, 0, "lbl-dn"))
for i in range(13):
    sch.append(label(f"PDM_DATA{i}", 210 + (i % 3) * 12, 60 + (i // 3) * 3, 0, f"lbl-pdm{i}"))
sch.append(label("PDM_CLK", 210, 55, 0, "lbl-pdmclk"))
sch.append(label("I2S_BCK", 260, 55, 0, "lbl-i2sbck"))
sch.append(label("I2S_LRCK", 260, 52, 0, "lbl-i2slrck"))
sch.append(label("I2S_SDIN", 260, 49, 0, "lbl-i2ssdin"))

# --- no-connects on NDP test pins ---
sch.append(noconn(303, 155, "nc-test0"))
sch.append(noconn(303, 158, "nc-test1"))
sch.append(noconn(303, 161, "nc-test2"))

sch.append('\t(sheet_instances\n')
sch.append('\t\t(path "/"\n')
sch.append('\t\t\t(page "1")\n')
sch.append('\t\t)\n')
sch.append('\t)\n')

sch.append(')\n')

OUT.write_text("".join(sch))
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")

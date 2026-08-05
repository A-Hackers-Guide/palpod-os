#!/usr/bin/env python3
"""
Generator for palpod-halbach-controller KiCad 8 project.

Emits schematic, pcb, symbol lib, footprints, project files, tables, README.
Deterministic UUIDs so re-runs diff cleanly.
"""
import os
import hashlib
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJ = "palpod-halbach-controller"

def uuid(name: str) -> str:
    """Deterministic UUIDv4-formatted string derived from name."""
    h = hashlib.sha256(("palpod-halbach:" + name).encode()).hexdigest()
    # Format as 8-4-4-4-12; set variant/version nibbles to 4/8 (rfc4122-ish)
    return f"{h[0:8]}-{h[8:12]}-4{h[13:16]}-8{h[17:20]}-{h[20:32]}"

def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(s)
    print(f"wrote {path} ({len(s)} bytes)")

# ---------------------------------------------------------------------------
# Symbol library (specialty ICs)
# ---------------------------------------------------------------------------

def sym_header():
    return '(kicad_symbol_lib\n\t(version 20231120)\n\t(generator "kicad_symbol_editor")\n'

def prop(name, val, x=0, y=0, rot=0, hide=False, size=1.27):
    hide_str = "\n\t\t\t\t(hide yes)" if hide else ""
    return (f'\t\t(property "{name}" "{val}"\n'
            f'\t\t\t(at {x} {y} {rot})\n'
            f'\t\t\t(effects\n'
            f'\t\t\t\t(font (size {size} {size})){hide_str}\n'
            f'\t\t\t)\n'
            f'\t\t)\n')

def pin(kind, shape, x, y, rot, length, name, number, size=1.0):
    return ('\t\t\t(pin ' + kind + ' ' + shape + '\n'
            f'\t\t\t\t(at {x} {y} {rot})\n'
            f'\t\t\t\t(length {length})\n'
            f'\t\t\t\t(name "{name}"\n'
            f'\t\t\t\t\t(effects (font (size {size} {size})))\n'
            f'\t\t\t\t)\n'
            f'\t\t\t\t(number "{number}"\n'
            f'\t\t\t\t\t(effects (font (size {size} {size})))\n'
            f'\t\t\t\t)\n'
            f'\t\t\t)\n')

def rect_body(name, x1, y1, x2, y2):
    return (f'\t\t(symbol "{name}_0_1"\n'
            f'\t\t\t(rectangle\n'
            f'\t\t\t\t(start {x1} {y1})\n'
            f'\t\t\t\t(end {x2} {y2})\n'
            f'\t\t\t\t(stroke (width 0.254) (type default))\n'
            f'\t\t\t\t(fill (type background))\n'
            f'\t\t\t)\n'
            f'\t\t)\n')

def sym_open(name, ref_prefix, value, fp, datasheet, desc):
    return (f'\t(symbol "{name}"\n'
            f'\t\t(pin_names (offset 1.016))\n'
            f'\t\t(exclude_from_sim no)\n'
            f'\t\t(in_bom yes)\n'
            f'\t\t(on_board yes)\n'
            + prop("Reference", ref_prefix, 0, 2.54)
            + prop("Value", value, 0, -2.54)
            + prop("Footprint", fp, hide=True)
            + prop("Datasheet", datasheet, hide=True)
            + prop("Description", desc, hide=True))

def sym_close():
    return '\t)\n'

# Pin layout helpers: distribute pins on a side of a rectangle.
def side_pins(pin_defs, side, x_edge, y_top, y_step, length=2.54):
    """pin_defs: list of (kind, name, number). side in L/R/T/B."""
    out = ""
    for i, (kind, name, number) in enumerate(pin_defs):
        if side == "L":
            x, y, rot = x_edge, y_top - i * y_step, 0
        elif side == "R":
            x, y, rot = x_edge, y_top - i * y_step, 180
        elif side == "T":
            x, y, rot = y_top + i * y_step, x_edge, 270
        elif side == "B":
            x, y, rot = y_top + i * y_step, x_edge, 90
        else:
            raise ValueError(side)
        out += pin(kind, "line", x, y, rot, length, name, number)
    return out


# --- STM32H723ZGT6 (LQFP-144) -----------------------------------------------
def build_stm32h723():
    body = rect_body("STM32H723ZGT6", -25.4, 45.72, 25.4, -50.8)
    # Simplified pin groups - real chip has 144 pins.
    # We'll represent all 144 but grouped functionally.
    left = []   # ports A/B
    for i in range(16): left.append(("bidirectional", f"PA{i}", str(1 + i)))
    for i in range(16): left.append(("bidirectional", f"PB{i}", str(17 + i)))
    right = []  # ports C/D
    for i in range(16): right.append(("bidirectional", f"PC{i}", str(33 + i)))
    for i in range(16): right.append(("bidirectional", f"PD{i}", str(49 + i)))
    top = []
    for i in range(16): top.append(("bidirectional", f"PE{i}", str(65 + i)))
    for i in range(16): top.append(("bidirectional", f"PF{i}", str(81 + i)))
    bot = []
    for i in range(16): bot.append(("bidirectional", f"PG{i}", str(97 + i)))
    # Power / control pins (remainder of 144)
    misc = [
        ("power_in", "VDD", "113"),
        ("power_in", "VDD", "114"),
        ("power_in", "VDD", "115"),
        ("power_in", "VDD", "116"),
        ("power_in", "VDDA", "117"),
        ("power_in", "VREF+", "118"),
        ("power_in", "VBAT", "119"),
        ("power_in", "VCAP1", "120"),
        ("power_in", "VCAP2", "121"),
        ("power_in", "VDDUSB", "122"),
        ("power_in", "VDDLDO", "123"),
        ("power_in", "VDDSMPS", "124"),
        ("power_in", "VLXSMPS", "125"),
        ("power_in", "VFBSMPS", "126"),
        ("power_in", "VSSSMPS", "127"),
        ("power_in", "VSSA", "128"),
        ("power_in", "VSS", "129"),
        ("power_in", "VSS", "130"),
        ("power_in", "VSS", "131"),
        ("power_in", "VSS", "132"),
        ("input",    "NRST",       "133"),
        ("input",    "BOOT0",      "134"),
        ("input",    "PH0/OSC_IN", "135"),
        ("input",    "PH1/OSC_OUT","136"),
        ("bidirectional", "PI0", "137"),
        ("bidirectional", "PI1", "138"),
        ("bidirectional", "PI2", "139"),
        ("bidirectional", "PI3", "140"),
        ("bidirectional", "PI4", "141"),
        ("bidirectional", "PI5", "142"),
        ("bidirectional", "PI6", "143"),
        ("bidirectional", "PI7", "144"),
    ]
    body += side_pins(left,  "L", -27.94, 43.18, 2.54)
    body += side_pins(right, "R",  27.94, 43.18, 2.54)
    # top/bottom of chip
    body += side_pins(top,   "T", -48.26, -22.86, 2.54)   # top means y=-48.26 (below rect), no wait:
    # Actually simpler: put remaining pins along bottom edge
    y0 = -50.8 - 2.54
    x0 = -25.4
    for i, p in enumerate(top + bot + misc):
        kind, name, num = p
        # break into rows of 16 along bottom
        row = i // 16
        col = i % 16
        x = x0 + col * 2.54
        y = y0 - row * 2.54
        body += pin(kind, "line", x, y, 90, 2.54, name, num)
    return (sym_open("STM32H723ZGT6", "U", "STM32H723ZGT6",
                     "palpod-halbach-controller:LQFP-144_20x20mm_P0.5mm",
                     "https://www.st.com/en/microcontrollers-microprocessors/stm32h723zg.html",
                     "STMicro STM32H723ZGT6 Cortex-M7 550MHz MCU, LQFP-144 - PLACEHOLDER pin grouping")
            + body + sym_close())

# --- DRV8323 (3-phase gate driver, 48-pin HTSSOP) ---------------------------
def build_drv8323():
    body = rect_body("DRV8323", -20.32, 30.48, 20.32, -30.48)
    pins = [
        # Left side - inputs / logic
        ("input",  "INHA",   "1"),  ("input",  "INLA",   "2"),
        ("input",  "INHB",   "3"),  ("input",  "INLB",   "4"),
        ("input",  "INHC",   "5"),  ("input",  "INLC",   "6"),
        ("input",  "nENABLE","7"),  ("input",  "nFAULT", "8"),
        ("input",  "SDI",    "9"),  ("output", "SDO",    "10"),
        ("input",  "SCLK",   "11"), ("input",  "nSCS",   "12"),
        ("input",  "DVDD",   "13"), ("input",  "AGND",   "14"),
        ("input",  "AVDD",   "15"), ("input",  "VREF",   "16"),
        ("output", "SOA",    "17"), ("output", "SOB",    "18"),
        ("output", "SOC",    "19"), ("input",  "SNA",    "20"),
        ("input",  "SNB",    "21"), ("input",  "SNC",    "22"),
        ("input",  "SPA",    "23"), ("input",  "SPB",    "24"),
        # Right side - gate drivers / power
        ("output", "GHA",    "25"), ("output", "SHA",    "26"),
        ("output", "GLA",    "27"), ("output", "GHB",    "28"),
        ("output", "SHB",    "29"), ("output", "GLB",    "30"),
        ("output", "GHC",    "31"), ("output", "SHC",    "32"),
        ("output", "GLC",    "33"), ("output", "CPH",    "34"),
        ("output", "CPL",    "35"), ("output", "VCP",    "36"),
        ("output", "VDRAIN", "37"), ("power_in","PVDD",  "38"),
        ("power_in","PGND",  "39"), ("power_in","GVDD",  "40"),
        ("input",  "SPC",    "41"), ("input",  "IDRIVE","42"),
        ("input",  "GAIN",   "43"), ("input",  "MODE",  "44"),
        ("input",  "VDS",    "45"), ("input",  "OCP_MODE","46"),
        ("input",  "IDRIVEP","47"), ("power_in","EP_PAD","49"),
    ]
    left = pins[:24]
    right = pins[24:]
    body += side_pins(left,  "L", -22.86, 27.94, 2.286)
    body += side_pins(right, "R",  22.86, 27.94, 2.286)
    return (sym_open("DRV8323", "U", "DRV8323",
                     "palpod-halbach-controller:HTSSOP-48_6.1x12.5mm_P0.5mm_EP",
                     "https://www.ti.com/product/DRV8323",
                     "TI DRV8323 3-phase smart gate driver, HTSSOP-48 EP - PLACEHOLDER pin grouping")
            + body + sym_close())

# --- INA240 (current-sense amp, TSSOP-8) ------------------------------------
def build_ina240():
    body = rect_body("INA240", -10.16, 7.62, 10.16, -7.62)
    pins = [
        ("input",     "REF1", "1"),
        ("input",     "IN-",  "2"),
        ("input",     "IN+",  "3"),
        ("power_in",  "GND",  "4"),
        ("input",     "REF2", "5"),
        ("output",    "OUT",  "6"),
        ("input",     "EN",   "7"),
        ("power_in",  "V+",   "8"),
    ]
    body += side_pins(pins[:4], "L", -12.7, 5.08, 2.54)
    body += side_pins(pins[4:], "R", 12.7,  5.08, 2.54)
    return (sym_open("INA240", "U", "INA240",
                     "palpod-halbach-controller:TSSOP-8_4.4x3mm_P0.65mm",
                     "https://www.ti.com/product/INA240",
                     "TI INA240 -4V..80V, bidirectional, low-drift current shunt monitor, TSSOP-8")
            + body + sym_close())

# --- MLX90393 (3D hall sensor, QFN-16) --------------------------------------
def build_mlx90393():
    body = rect_body("MLX90393", -10.16, 10.16, 10.16, -10.16)
    pins = [
        ("passive",  "DNC1",  "1"),
        ("power_in", "VDD",   "2"),
        ("input",    "TRG",   "3"),
        ("input",    "SCLK",  "4"),
        ("bidirectional","MOSI/SDA","5"),
        ("bidirectional","MISO",   "6"),
        ("passive",  "DNC2",  "7"),
        ("output",   "INT/DRDY","8"),
        ("input",    "CS",    "9"),
        ("input",    "A0",    "10"),
        ("input",    "A1",    "11"),
        ("passive",  "TEST",  "12"),
        ("power_in", "GND",   "13"),
        ("passive",  "DNC3",  "14"),
        ("passive",  "DNC4",  "15"),
        ("passive",  "DNC5",  "16"),
    ]
    body += side_pins(pins[:8], "L", -12.7, 8.89, 2.286)
    body += side_pins(pins[8:], "R", 12.7,  8.89, 2.286)
    return (sym_open("MLX90393", "U", "MLX90393",
                     "palpod-halbach-controller:QFN-16_3x3mm_P0.5mm",
                     "https://www.melexis.com/en/product/MLX90393/Triaxis-Micropower-Magnetometer",
                     "Melexis MLX90393 3D magnetoresistive sensor, QFN-16 - I2C or SPI")
            + body + sym_close())

# --- MAX706 (supervisor, SO-8) -----------------------------------------------
def build_max706():
    body = rect_body("MAX706", -10.16, 7.62, 10.16, -7.62)
    pins = [
        ("input",     "MR",     "1"),
        ("output",    "RESET",  "2"),
        ("output",    "WDO",    "3"),
        ("input",     "WDI",    "4"),
        ("input",     "PFI",    "5"),
        ("output",    "PFO",    "6"),
        ("power_in",  "VCC",    "7"),
        ("power_in",  "GND",    "8"),
    ]
    body += side_pins(pins[:4], "L", -12.7, 5.08, 2.54)
    body += side_pins(pins[4:], "R", 12.7,  5.08, 2.54)
    return (sym_open("MAX706", "U", "MAX706",
                     "palpod-halbach-controller:SOIC-8_3.9x4.9mm_P1.27mm",
                     "https://www.analog.com/en/products/max706.html",
                     "Maxim MAX706 microprocessor supervisor with watchdog, SO-8")
            + body + sym_close())

# --- MCP2542FD (CAN-FD transceiver, SO-8) ------------------------------------
def build_mcp2542fd():
    body = rect_body("MCP2542FD", -10.16, 7.62, 10.16, -7.62)
    pins = [
        ("input",     "TXD",    "1"),
        ("power_in",  "VSS",    "2"),
        ("power_in",  "VDD",    "3"),
        ("output",    "RXD",    "4"),
        ("input",     "VIO",    "5"),
        ("output",    "CANL",   "6"),
        ("output",    "CANH",   "7"),
        ("input",     "STBY",   "8"),
    ]
    body += side_pins(pins[:4], "L", -12.7, 5.08, 2.54)
    body += side_pins(pins[4:], "R", 12.7,  5.08, 2.54)
    return (sym_open("MCP2542FD", "U", "MCP2542FD",
                     "palpod-halbach-controller:SOIC-8_3.9x4.9mm_P1.27mm",
                     "https://www.microchip.com/en-us/product/MCP2542FD",
                     "Microchip MCP2542FD CAN-FD transceiver, SO-8")
            + body + sym_close())

# --- TL331 (comparator, SOT-23-5) --------------------------------------------
def build_tl331():
    body = rect_body("TL331", -7.62, 5.08, 7.62, -5.08)
    pins = [
        ("output",    "OUT",    "1"),
        ("power_in",  "GND",    "2"),
        ("input",     "IN+",    "3"),
        ("input",     "IN-",    "4"),
        ("power_in",  "V+",     "5"),
    ]
    body += side_pins(pins[:3], "L", -10.16, 2.54, 2.54)
    body += side_pins(pins[3:], "R", 10.16, 2.54, 2.54)
    return (sym_open("TL331", "U", "TL331",
                     "palpod-halbach-controller:SOT-23-5",
                     "https://www.ti.com/product/TL331",
                     "TI TL331 single differential comparator, SOT-23-5 - hardware overcurrent latch")
            + body + sym_close())

# --- IPI050N06N (60V/50A N-ch MOSFET, TO-262) --------------------------------
def build_ipi050n06n():
    body = rect_body("IPI050N06N", -7.62, 5.08, 7.62, -5.08)
    pins = [
        ("input",   "G",  "1"),
        ("passive", "D",  "2"),
        ("passive", "S",  "3"),
        ("passive", "D",  "4"),  # tab
    ]
    body += pin("input",   "line", -10.16, 2.54, 0, 2.54, "G", "1")
    body += pin("passive", "line",  10.16, 2.54, 180, 2.54, "D", "2")
    body += pin("passive", "line",  10.16, 0.0,  180, 2.54, "S", "3")
    body += pin("passive", "line",  10.16, -2.54,180, 2.54, "D_TAB", "4")
    return (sym_open("IPI050N06N", "Q", "IPI050N06N",
                     "palpod-halbach-controller:TO-262-3_TabPin2",
                     "https://www.infineon.com/dgdl/Infineon-IPI050N06N-DS-v02_00-EN.pdf",
                     "Infineon IPI050N06N 60V/50A OptiMOS N-Channel MOSFET, TO-262 - PLACEHOLDER")
            + body + sym_close())

# --- STM32G030 (aux MCU, LQFP-32) --------------------------------------------
def build_stm32g030():
    body = rect_body("STM32G030K8T6", -12.7, 20.32, 12.7, -20.32)
    pins = []
    for i in range(16):  pins.append(("bidirectional", f"PA{i}", str(i+1)))
    for i in range(9):   pins.append(("bidirectional", f"PB{i}", str(i+17)))
    pins += [
        ("power_in", "VDD",  "26"),
        ("power_in", "VSS",  "27"),
        ("power_in", "VDDA", "28"),
        ("input",    "NRST", "29"),
        ("input",    "BOOT0","30"),
        ("bidirectional","PC14","31"),
        ("bidirectional","PC15","32"),
    ]
    body += side_pins(pins[:16], "L", -15.24, 17.78, 2.286)
    body += side_pins(pins[16:], "R",  15.24, 17.78, 2.286)
    return (sym_open("STM32G030K8T6", "U", "STM32G030K8T6",
                     "palpod-halbach-controller:LQFP-32_7x7mm_P0.8mm",
                     "https://www.st.com/en/microcontrollers-microprocessors/stm32g030k8.html",
                     "STMicro STM32G030K8T6 aux MCU, LQFP-32 - housekeeping")
            + body + sym_close())

# --- Recom RTK-2412 isolated DC-DC brick (2W isolated, 12V in, 24V out) ------
def build_rtk2412():
    body = rect_body("RTK-2412", -10.16, 7.62, 10.16, -7.62)
    body += pin("power_in", "line", -12.7, 5.08, 0, 2.54, "VIN+",  "1")
    body += pin("power_in", "line", -12.7, 2.54, 0, 2.54, "VIN-",  "2")
    body += pin("passive",  "line", -12.7, 0.0,  0, 2.54, "NC",    "3")
    body += pin("output",   "line",  12.7, 5.08, 180, 2.54, "VOUT+","5")
    body += pin("output",   "line",  12.7, 2.54, 180, 2.54, "VOUT-","4")
    return (sym_open("RTK-2412", "U", "RTK-2412",
                     "palpod-halbach-controller:SIP-4_Recom_RTK",
                     "https://recom-power.com/en/products/dc-dc-converters/rec-p-RTK-2412.html",
                     "Recom RTK-2412 2W isolated DC-DC (12V->24V) - driver isolation barrier")
            + body + sym_close())

def build_specialty_lib():
    return (sym_header()
            + build_stm32h723()
            + build_drv8323()
            + build_ina240()
            + build_mlx90393()
            + build_max706()
            + build_mcp2542fd()
            + build_tl331()
            + build_ipi050n06n()
            + build_stm32g030()
            + build_rtk2412()
            + ')\n')

# ---------------------------------------------------------------------------
# Footprints
# ---------------------------------------------------------------------------

def fp_placeholder(name, descr, tags, pad_count, pad_pitch, pad_size,
                   grid_x, grid_y=None, rect_w=None, rect_h=None):
    """Simple rectangular grid of SMD pads for a placeholder footprint."""
    grid_y = grid_y or ((pad_count + grid_x - 1) // grid_x)
    rect_w = rect_w or (grid_x * pad_pitch + 1.0)
    rect_h = rect_h or (grid_y * pad_pitch + 1.0)
    hx = rect_w / 2.0
    hy = rect_h / 2.0
    out = [
        f'(footprint "{name}"',
        f'\t(version 20240108)',
        f'\t(generator "pcbnew")',
        f'\t(generator_version "8.0")',
        f'\t(layer "F.Cu")',
        f'\t(descr "{descr}")',
        f'\t(tags "{tags}")',
        f'\t(attr smd)',
        f'\t(property "Reference" "U**"',
        f'\t\t(at 0 {-hy-1.5} 0) (layer "F.SilkS") (uuid "{uuid(name+".ref")}")',
        f'\t\t(effects (font (size 1 1) (thickness 0.15))))',
        f'\t(property "Value" "{name}"',
        f'\t\t(at 0 {hy+1.5} 0) (layer "F.Fab") (uuid "{uuid(name+".val")}")',
        f'\t\t(effects (font (size 1 1) (thickness 0.15))))',
        f'\t(property "Footprint" "" (at 0 0 0) (layer "F.Fab") (hide yes)',
        f'\t\t(uuid "{uuid(name+".fp")}")',
        f'\t\t(effects (font (size 1.27 1.27) (thickness 0.15))))',
        f'\t(property "Datasheet" "" (at 0 0 0) (layer "F.Fab") (hide yes)',
        f'\t\t(uuid "{uuid(name+".ds")}")',
        f'\t\t(effects (font (size 1.27 1.27) (thickness 0.15))))',
        f'\t(property "Description" "PLACEHOLDER - verify vs datasheet before fab"',
        f'\t\t(at 0 0 0) (layer "F.Fab") (hide yes)',
        f'\t\t(uuid "{uuid(name+".desc")}")',
        f'\t\t(effects (font (size 1.27 1.27) (thickness 0.15))))',
    ]
    # Fab outline
    out += [
        f'\t(fp_rect (start {-hx} {-hy}) (end {hx} {hy})',
        f'\t\t(stroke (width 0.1) (type default)) (fill none) (layer "F.Fab") (uuid "{uuid(name+".fab.rect")}"))',
        f'\t(fp_rect (start {-hx-0.15} {-hy-0.15}) (end {hx+0.15} {hy+0.15})',
        f'\t\t(stroke (width 0.12) (type default)) (fill none) (layer "F.SilkS") (uuid "{uuid(name+".silk.rect")}"))',
        f'\t(fp_rect (start {-hx-0.25} {-hy-0.25}) (end {hx+0.25} {hy+0.25})',
        f'\t\t(stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd") (uuid "{uuid(name+".crtyd.rect")}"))',
        f'\t(fp_circle (center {-hx-0.6} {-hy-0.6}) (end {-hx-0.4} {-hy-0.4})',
        f'\t\t(stroke (width 0.15) (type default)) (fill solid) (layer "F.SilkS") (uuid "{uuid(name+".pin1")}"))',
    ]
    # Pads: perimeter walk starting bottom-left going ccw (pin 1 at top-left)
    pw, ph = pad_size
    perim = []
    # left side (pins 1..grid_y, top-to-bottom)
    for i in range(grid_y):
        x = -hx + pw*0.7
        y = -hy + (i + 0.5) * (rect_h / grid_y)
        perim.append((x, y))
    # bottom side (pins grid_y+1..grid_y+grid_x, left-to-right)
    for i in range(grid_x):
        x = -hx + (i + 0.5) * (rect_w / grid_x)
        y = hy - ph*0.7
        perim.append((x, y))
    # right side (top-to-bottom then reversed to bottom-to-top)
    for i in range(grid_y):
        x = hx - pw*0.7
        y = hy - (i + 0.5) * (rect_h / grid_y)
        perim.append((x, y))
    # top side (right-to-left)
    for i in range(grid_x):
        x = hx - (i + 0.5) * (rect_w / grid_x)
        y = -hy + ph*0.7
        perim.append((x, y))
    perim = perim[:pad_count]
    for i, (x, y) in enumerate(perim):
        out.append(
            f'\t(pad "{i+1}" smd roundrect (at {x:.3f} {y:.3f}) (size {pw} {ph}) '
            f'(layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) '
            f'(uuid "{uuid(name+f".pad{i+1}")}"))'
        )
    out.append(')')
    return "\n".join(out) + "\n"

FOOTPRINTS = [
    ("LQFP-144_20x20mm_P0.5mm",
        "PLACEHOLDER STM32H723ZGT6 LQFP-144 20x20mm 0.5mm pitch - VERIFY BEFORE FAB",
        "LQFP-144 STM32 PLACEHOLDER",
        144, 0.5, (0.3, 1.4), 36),
    ("HTSSOP-48_6.1x12.5mm_P0.5mm_EP",
        "PLACEHOLDER TI DRV8323 HTSSOP-48 EP - VERIFY BEFORE FAB",
        "HTSSOP-48 EP PLACEHOLDER",
        48, 0.5, (0.3, 1.4), 12, 12, 6.1, 12.5),
    ("TSSOP-8_4.4x3mm_P0.65mm",
        "PLACEHOLDER TSSOP-8 - VERIFY BEFORE FAB",
        "TSSOP-8 PLACEHOLDER",
        8, 0.65, (0.4, 1.4), 4, 0, 4.4, 3.0),
    ("QFN-16_3x3mm_P0.5mm",
        "PLACEHOLDER QFN-16 3x3mm - VERIFY BEFORE FAB",
        "QFN-16 PLACEHOLDER",
        16, 0.5, (0.3, 0.6), 4, 4, 3.0, 3.0),
    ("SOIC-8_3.9x4.9mm_P1.27mm",
        "PLACEHOLDER SOIC-8 - VERIFY BEFORE FAB",
        "SOIC-8 PLACEHOLDER",
        8, 1.27, (0.6, 1.7), 4, 0, 3.9, 4.9),
    ("SOT-23-5",
        "PLACEHOLDER SOT-23-5 - VERIFY BEFORE FAB",
        "SOT-23-5 PLACEHOLDER",
        5, 0.95, (0.6, 1.0), 3, 0, 2.8, 2.9),
    ("TO-262-3_TabPin2",
        "PLACEHOLDER TO-262 3-pin (tab connects to pin2 D) - VERIFY BEFORE FAB",
        "TO-262 MOSFET PLACEHOLDER",
        3, 2.54, (2.0, 2.5), 3, 0, 10.0, 8.0),
    ("LQFP-32_7x7mm_P0.8mm",
        "PLACEHOLDER LQFP-32 7x7mm - VERIFY BEFORE FAB",
        "LQFP-32 PLACEHOLDER",
        32, 0.8, (0.4, 1.4), 8, 8, 7.0, 7.0),
    ("SIP-4_Recom_RTK",
        "PLACEHOLDER Recom RTK isolated DC-DC SIP-4 - VERIFY BEFORE FAB",
        "SIP-4 Recom PLACEHOLDER",
        4, 2.54, (1.5, 1.5), 1, 4, 6.0, 12.0),
    ("Screw_Terminal_2Pin_5.08mm",
        "PLACEHOLDER 2-pin screw terminal 5.08mm pitch - coil output - VERIFY BEFORE FAB",
        "Terminal Coil PLACEHOLDER",
        2, 5.08, (2.0, 3.0), 2, 0, 12.0, 8.0),
    ("JST-PH_4Pin",
        "PLACEHOLDER JST-PH 4-pin - hall sensor cable - VERIFY BEFORE FAB",
        "JST-PH 4pin PLACEHOLDER",
        4, 2.0, (1.0, 2.5), 4, 0, 9.0, 6.0),
    ("Estop_Terminal_2Pin",
        "PLACEHOLDER E-stop 2-pin terminal - hardwired latch",
        "E-stop terminal",
        2, 5.08, (2.0, 3.0), 2, 0, 12.0, 8.0),
]

# ---------------------------------------------------------------------------
# Project file (.kicad_pro)
# ---------------------------------------------------------------------------

def build_kicad_pro():
    net_classes = [
        {
            "bus_width": 12, "clearance": 0.2,
            "diff_pair_gap": 0.15, "diff_pair_via_gap": 0.15, "diff_pair_width": 0.2,
            "line_style": 0, "microvia_diameter": 0.3, "microvia_drill": 0.1,
            "name": "Default", "pcb_color": "rgba(0, 0, 0, 0.000)",
            "priority": 2147483647, "schematic_color": "rgba(0, 0, 0, 0.000)",
            "track_width": 0.2, "via_diameter": 0.6, "via_drill": 0.3, "wire_width": 6,
        },
        {
            "bus_width": 12, "clearance": 0.3,
            "diff_pair_gap": 0.15, "diff_pair_via_gap": 0.15, "diff_pair_width": 0.2,
            "line_style": 0, "microvia_diameter": 0.3, "microvia_drill": 0.1,
            "name": "Power", "pcb_color": "rgba(255, 0, 0, 1.000)",
            "priority": 10, "schematic_color": "rgba(255, 0, 0, 1.000)",
            "track_width": 0.5, "via_diameter": 0.8, "via_drill": 0.4, "wire_width": 6,
        },
        {
            "bus_width": 12, "clearance": 0.5,
            "diff_pair_gap": 0.5, "diff_pair_via_gap": 0.5, "diff_pair_width": 5.0,
            "line_style": 0, "microvia_diameter": 0.3, "microvia_drill": 0.1,
            "name": "COIL_HIGH_CURRENT",
            "pcb_color": "rgba(255, 100, 0, 1.000)",
            "priority": 1, "schematic_color": "rgba(255, 100, 0, 1.000)",
            "track_width": 5.0, "via_diameter": 2.0, "via_drill": 1.0, "wire_width": 10,
        },
        {
            "bus_width": 12, "clearance": 0.2,
            "diff_pair_gap": 0.2, "diff_pair_via_gap": 0.2, "diff_pair_width": 0.2,
            "line_style": 0, "microvia_diameter": 0.3, "microvia_drill": 0.1,
            "name": "CAN_FD_DIFF",
            "pcb_color": "rgba(0, 200, 0, 1.000)",
            "priority": 4, "schematic_color": "rgba(0, 200, 0, 1.000)",
            "track_width": 0.2, "via_diameter": 0.5, "via_drill": 0.25, "wire_width": 6,
        },
        {
            "bus_width": 12, "clearance": 0.4,
            "diff_pair_gap": 0.15, "diff_pair_via_gap": 0.15, "diff_pair_width": 0.2,
            "line_style": 0, "microvia_diameter": 0.3, "microvia_drill": 0.1,
            "name": "SAFETY_CRITICAL",
            "pcb_color": "rgba(255, 0, 128, 1.000)",
            "priority": 2, "schematic_color": "rgba(255, 0, 128, 1.000)",
            "track_width": 0.4, "via_diameter": 0.8, "via_drill": 0.4, "wire_width": 8,
        },
    ]
    pro = {
      "board": {
        "3dviewports": [],
        "design_settings": {
          "defaults": {
            "board_outline_line_width": 0.1,
            "copper_line_width": 0.2,
            "copper_text_size_h": 1.5,
            "copper_text_size_v": 1.5,
            "copper_text_thickness": 0.3,
            "courtyard_line_width": 0.05,
            "dimension_precision": 4,
            "dimension_units": 3,
            "dimensions": {
              "arrow_length": 1270000, "extension_offset": 500000,
              "keep_text_aligned": True, "suppress_zeroes": False,
              "text_position": 0, "units_format": 1
            },
            "fab_line_width": 0.1,
            "fab_text_size_h": 1.0, "fab_text_size_v": 1.0, "fab_text_thickness": 0.15,
            "other_line_width": 0.15,
            "other_text_size_h": 1.0, "other_text_size_v": 1.0, "other_text_thickness": 0.15,
            "pads": {"drill": 0.4, "height": 1.0, "width": 1.0},
            "silk_line_width": 0.12,
            "silk_text_size_h": 1.0, "silk_text_size_v": 1.0, "silk_text_thickness": 0.15
          },
          "diff_pair_dimensions": [
            {"gap": 0.15, "via_gap": 0.15, "width": 0.2},
            {"gap": 0.2, "via_gap": 0.2, "width": 0.2}
          ],
          "drc_exclusions": [],
          "meta": {"version": 2},
          "rule_severities": {
            "annular_width": "error", "clearance": "error",
            "connection_width": "warning", "copper_edge_clearance": "error",
            "copper_sliver": "warning", "courtyards_overlap": "error",
            "diff_pair_gap_out_of_range": "error",
            "diff_pair_uncoupled_length_too_long": "error",
            "drill_out_of_range": "error", "duplicate_footprints": "warning",
            "extra_footprint": "warning", "footprint": "error",
            "footprint_symbol_mismatch": "warning", "footprint_type_mismatch": "ignore",
            "hole_clearance": "error", "hole_near_hole": "error",
            "holes_co_located": "warning", "invalid_outline": "error",
            "isolated_copper": "warning", "item_on_disabled_layer": "error",
            "items_not_allowed": "error", "length_out_of_range": "error",
            "lib_footprint_issues": "warning", "lib_footprint_mismatch": "warning",
            "malformed_courtyard": "error", "microvia_drill_out_of_range": "error",
            "missing_courtyard": "ignore", "missing_footprint": "warning",
            "net_conflict": "warning", "npth_inside_courtyard": "ignore",
            "padstack": "warning", "pth_inside_courtyard": "ignore",
            "shorting_items": "error", "silk_edge_clearance": "warning",
            "silk_over_copper": "warning", "silk_overlap": "warning",
            "skew_out_of_range": "error", "solder_mask_bridge": "error",
            "starved_thermal": "error", "text_height": "warning",
            "text_thickness": "warning", "through_hole_pad_without_hole": "error",
            "too_many_vias": "error", "track_dangling": "warning",
            "track_width": "error", "tracks_crossing": "error",
            "unconnected_items": "error", "unresolved_variable": "error",
            "via_dangling": "warning", "zone_has_empty_net": "error",
            "zones_intersect": "error"
          },
          "rules": {
            "max_error": 0.005, "min_clearance": 0.15,
            "min_connection": 0.0, "min_copper_edge_clearance": 0.3,
            "min_hole_clearance": 0.25, "min_hole_to_hole": 0.25,
            "min_microvia_diameter": 0.2, "min_microvia_drill": 0.1,
            "min_resolved_spokes": 2, "min_silk_clearance": 0.0,
            "min_text_height": 0.8, "min_text_thickness": 0.08,
            "min_through_hole_diameter": 0.3, "min_track_width": 0.15,
            "min_via_annular_width": 0.1, "min_via_diameter": 0.4,
            "solder_mask_to_copper_clearance": 0.0,
            "use_height_for_length_calcs": True
          },
          "teardrop_options": [{
            "td_onpadsmd": True, "td_onroundshapesonly": False,
            "td_ontrackend": False, "td_onviapad": True
          }],
          "teardrop_parameters": [
            {"td_allow_use_two_tracks": True, "td_curve_segcount": 0,
             "td_height_ratio": 1.0, "td_length_ratio": 0.5,
             "td_maxheight": 2.0, "td_maxlen": 1.0,
             "td_on_pad_in_zone": False, "td_target_name": "td_round_shape",
             "td_width_to_size_filter_ratio": 0.9},
            {"td_allow_use_two_tracks": True, "td_curve_segcount": 0,
             "td_height_ratio": 1.0, "td_length_ratio": 0.5,
             "td_maxheight": 2.0, "td_maxlen": 1.0,
             "td_on_pad_in_zone": False, "td_target_name": "td_rect_shape",
             "td_width_to_size_filter_ratio": 0.9},
            {"td_allow_use_two_tracks": True, "td_curve_segcount": 0,
             "td_height_ratio": 1.0, "td_length_ratio": 0.5,
             "td_maxheight": 2.0, "td_maxlen": 1.0,
             "td_on_pad_in_zone": False, "td_target_name": "td_track_end",
             "td_width_to_size_filter_ratio": 0.9}
          ],
          "track_widths": [0.0, 0.15, 0.2, 0.4, 0.5, 1.0, 3.0, 5.0],
          "tuning_pattern_settings": {
            "diff_pair_defaults": {"corner_radius_percentage": 80, "corner_style": 1,
              "max_amplitude": 1.0, "min_amplitude": 0.2,
              "single_sided": False, "spacing": 1.0},
            "diff_pair_skew_defaults": {"corner_radius_percentage": 80, "corner_style": 1,
              "max_amplitude": 1.0, "min_amplitude": 0.2,
              "single_sided": False, "spacing": 0.6},
            "single_track_defaults": {"corner_radius_percentage": 80, "corner_style": 1,
              "max_amplitude": 1.0, "min_amplitude": 0.2,
              "single_sided": False, "spacing": 0.6}
          },
          "via_dimensions": [
            {"diameter": 0.0, "drill": 0.0},
            {"diameter": 0.4, "drill": 0.2},
            {"diameter": 0.8, "drill": 0.4},
            {"diameter": 2.0, "drill": 1.0}
          ],
          "zones_allow_external_fillets": False
        },
        "ipc2581": {"dist":"", "distpn":"", "internal_id":"", "mfg":"", "mpn":""},
        "layer_presets": [], "viewports": []
      },
      "boards": [],
      "cvpcb": {"equivalence_files": []},
      "erc": {
        "erc_exclusions": [],
        "meta": {"version": 0},
        "pin_map": [
          [0,0,0,0,0,0,1,0,0,0,0,2],[0,2,0,1,0,0,1,0,2,2,2,2],
          [0,0,0,0,0,0,1,0,1,0,1,2],[0,1,0,0,0,0,1,1,2,1,1,2],
          [0,0,0,0,0,0,1,0,0,0,0,2],[0,0,0,0,0,0,0,0,0,0,0,2],
          [1,1,1,1,1,0,1,1,1,1,1,2],[0,0,0,1,0,0,1,0,0,0,0,2],
          [0,2,1,2,0,0,1,0,2,2,2,2],[0,2,0,1,0,0,1,0,2,0,0,2],
          [0,2,1,1,0,0,1,0,2,0,0,2],[2,2,2,2,2,2,2,2,2,2,2,2]
        ],
        "rule_severities": {
          "bus_definition_conflict":"error","bus_entry_needed":"error",
          "bus_to_bus_conflict":"error","bus_to_net_conflict":"error",
          "conflicting_netclasses":"error","different_unit_footprint":"error",
          "different_unit_net":"error","duplicate_reference":"error",
          "duplicate_sheet_names":"error","endpoint_off_grid":"warning",
          "extra_units":"error","global_label_dangling":"warning",
          "hier_label_mismatch":"error","label_dangling":"error",
          "lib_symbol_issues":"warning","missing_bidi_pin":"warning",
          "missing_input_pin":"warning","missing_power_pin":"error",
          "missing_unit":"warning","net_not_bus_member":"warning",
          "no_connect_connected":"warning","no_connect_dangling":"warning",
          "pin_not_connected":"error","pin_not_driven":"error",
          "pin_to_pin":"warning","power_pin_not_driven":"error",
          "similar_labels":"warning","simulation_model_issue":"ignore",
          "unannotated":"error","unit_value_mismatch":"error",
          "unresolved_variable":"error","wire_dangling":"error"
        }
      },
      "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
      "meta": {"filename": PROJ+".kicad_pro", "version": 1},
      "net_settings": {
        "classes": net_classes,
        "meta": {"version": 3},
        "net_colors": None,
        "netclass_assignments": None,
        "netclass_patterns": [
          {"netclass": "Power", "pattern": "+5V"},
          {"netclass": "Power", "pattern": "+3V3"},
          {"netclass": "Power", "pattern": "+12V"},
          {"netclass": "Power", "pattern": "+48V"},
          {"netclass": "COIL_HIGH_CURRENT", "pattern": "COIL_*"},
          {"netclass": "COIL_HIGH_CURRENT", "pattern": "PHASE_*"},
          {"netclass": "COIL_HIGH_CURRENT", "pattern": "PVDD"},
          {"netclass": "COIL_HIGH_CURRENT", "pattern": "PGND"},
          {"netclass": "CAN_FD_DIFF",  "pattern": "CANH"},
          {"netclass": "CAN_FD_DIFF",  "pattern": "CANL"},
          {"netclass": "SAFETY_CRITICAL", "pattern": "ESTOP*"},
          {"netclass": "SAFETY_CRITICAL", "pattern": "OC_LATCH*"},
          {"netclass": "SAFETY_CRITICAL", "pattern": "WDOG*"},
          {"netclass": "SAFETY_CRITICAL", "pattern": "nFAULT*"},
          {"netclass": "SAFETY_CRITICAL", "pattern": "LOCKSTEP*"}
        ]
      },
      "pcbnew": {
        "last_paths": {"gencad":"","idf":"","netlist":"","plot":"",
                       "pos_files":"","specctra_dsn":"","step":"","svg":"","vrml":""},
        "page_layout_descr_file": ""
      },
      "schematic": {
        "annotate_start_num": 0,
        "bom_export_filename": "${PROJECTNAME}.csv",
        "bom_fmt_presets": [],
        "bom_fmt_settings": {
          "field_delimiter": ",", "keep_line_breaks": False, "keep_tabs": False,
          "name": "CSV", "ref_delimiter": ",", "ref_range_delimiter": "",
          "string_delimiter": "\""
        },
        "bom_presets": [],
        "bom_settings": {
          "exclude_dnp": False,
          "fields_ordered": [
            {"group_by": False, "label":"Reference","name":"Reference","show":True},
            {"group_by": True,  "label":"Value","name":"Value","show":True},
            {"group_by": False, "label":"Datasheet","name":"Datasheet","show":True},
            {"group_by": False, "label":"Footprint","name":"Footprint","show":True},
            {"group_by": False, "label":"Qty","name":"${QUANTITY}","show":True},
            {"group_by": True,  "label":"DNP","name":"${DNP}","show":True}
          ],
          "filter_string":"", "group_symbols": True,
          "name":"Grouped By Value", "sort_asc": True, "sort_field":"Reference"
        },
        "connection_grid_size": 50.0,
        "drawing": {
          "dashed_lines_dash_length_ratio": 12.0,
          "dashed_lines_gap_length_ratio": 3.0,
          "default_line_thickness": 6.0,
          "default_text_size": 50.0,
          "field_names": [],
          "intersheets_ref_own_page": False,
          "intersheets_ref_prefix": "",
          "intersheets_ref_short": False,
          "intersheets_ref_show": False,
          "intersheets_ref_suffix": "",
          "junction_size_choice": 3,
          "label_size_ratio": 0.375,
          "operating_point_overlay_i_precision": 3,
          "operating_point_overlay_i_range": "~A",
          "operating_point_overlay_v_precision": 3,
          "operating_point_overlay_v_range": "~V",
          "overbar_offset_ratio": 1.23,
          "pin_symbol_size": 25.0,
          "text_offset_ratio": 0.15
        },
        "legacy_lib_dir": "",
        "legacy_lib_list": [],
        "meta": {"version": 1},
        "net_format_name": "",
        "page_layout_descr_file": "",
        "plot_directory": "",
        "spice_current_sheet_as_root": False,
        "spice_external_command": "spice \"%I\"",
        "spice_model_current_sheet_as_root": True,
        "spice_save_all_currents": False,
        "spice_save_all_dissipations": False,
        "spice_save_all_voltages": False,
        "subpart_first_id": 65,
        "subpart_id_separator": 0
      },
      "sheets": [["00000000-0000-4000-8000-000000000001", "Root"]],
      "text_variables": {"BOARD_REV": "A0", "PROJECT": "Hearth Halbach Controller"}
    }
    return json.dumps(pro, indent=2)


# ---------------------------------------------------------------------------
# Schematic
# ---------------------------------------------------------------------------

def sch_lib_symbol_R():
    """The stock Device:R symbol, embedded so the schematic opens offline."""
    return '''\t\t(symbol "Device:R"
\t\t\t(pin_numbers (hide yes))
\t\t\t(pin_names (offset 0) (hide yes))
\t\t\t(exclude_from_sim no) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "R" (at 0 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at -1.778 0 90) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(symbol "R_0_1"
\t\t\t\t(rectangle (start -1.016 -2.54) (end 1.016 2.54)
\t\t\t\t\t(stroke (width 0.254) (type default)) (fill (type none))))
\t\t\t(symbol "R_1_1"
\t\t\t\t(pin passive line (at 0 3.81 270) (length 1.27)
\t\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 0 -3.81 90) (length 1.27)
\t\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "2" (effects (font (size 1.27 1.27)))))))
'''

def sch_lib_symbol_C():
    return '''\t\t(symbol "Device:C"
\t\t\t(pin_numbers (hide yes))
\t\t\t(pin_names (offset 0.254) (hide yes))
\t\t\t(exclude_from_sim no) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "C" (at 0.635 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "C" (at 0.635 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0.9652 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(symbol "C_0_1"
\t\t\t\t(polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762))
\t\t\t\t\t(stroke (width 0.508) (type default)) (fill (type none)))
\t\t\t\t(polyline (pts (xy -2.032 0.762) (xy 2.032 0.762))
\t\t\t\t\t(stroke (width 0.508) (type default)) (fill (type none))))
\t\t\t(symbol "C_1_1"
\t\t\t\t(pin passive line (at 0 3.81 270) (length 2.794)
\t\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 0 -3.81 90) (length 2.794)
\t\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "2" (effects (font (size 1.27 1.27)))))))
'''

def sch_lib_symbol_power(name, color_arrow=True):
    return f'''\t\t(symbol "power:{name}"
\t\t\t(power)
\t\t\t(pin_names (offset 0))
\t\t\t(exclude_from_sim no) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(property "Value" "{name}" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(symbol "{name}_0_1"
\t\t\t\t(polyline (pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27) (xy 0 0) (xy -0.762 1.27))
\t\t\t\t\t(stroke (width 0) (type default)) (fill (type none))))
\t\t\t(symbol "{name}_1_1"
\t\t\t\t(pin power_in line (at 0 0 90) (length 0) (hide yes)
\t\t\t\t\t(name "{name}" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "1" (effects (font (size 1.27 1.27)))))))
'''

def sch_lib_symbol_gnd(name="GND"):
    return f'''\t\t(symbol "power:{name}"
\t\t\t(power)
\t\t\t(pin_names (offset 0))
\t\t\t(exclude_from_sim no) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(property "Value" "{name}" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(symbol "{name}_0_1"
\t\t\t\t(polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27))
\t\t\t\t\t(stroke (width 0) (type default)) (fill (type none))))
\t\t\t(symbol "{name}_1_1"
\t\t\t\t(pin power_in line (at 0 0 270) (length 0) (hide yes)
\t\t\t\t\t(name "{name}" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "1" (effects (font (size 1.27 1.27)))))))
'''

def indent(s, tabs=1):
    """Reindent an already-tab-indented block by adding `tabs` extra tabs to each line."""
    prefix = "\t" * tabs
    return "".join(prefix + line if line.strip() else line for line in s.splitlines(keepends=True))

def sch_lib_symbol_specialty(build_fn_output):
    """Take a symbol produced by build_*() and reindent to be nested under lib_symbols."""
    return indent(build_fn_output, tabs=1)


def placed_symbol(lib_id, ref, value, x, y, uuid_key, footprint="", show_value=True, rot=0):
    val_hide = "" if show_value else "\n\t\t\t\t(hide yes)"
    return (f'\t(symbol\n'
            f'\t\t(lib_id "{lib_id}")\n'
            f'\t\t(at {x} {y} {rot})\n'
            f'\t\t(unit 1)\n'
            f'\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)\n'
            f'\t\t(uuid "{uuid(uuid_key)}")\n'
            f'\t\t(property "Reference" "{ref}"\n'
            f'\t\t\t(at {x+2.54} {y-5.08} 0)\n'
            f'\t\t\t(effects (font (size 1.27 1.27))))\n'
            f'\t\t(property "Value" "{value}"\n'
            f'\t\t\t(at {x+2.54} {y+5.08} 0)\n'
            f'\t\t\t(effects (font (size 1.27 1.27)){val_hide}))\n'
            f'\t\t(property "Footprint" "{footprint}"\n'
            f'\t\t\t(at {x} {y} 0)\n'
            f'\t\t\t(effects (font (size 1.27 1.27)) (hide yes)))\n'
            f'\t\t(property "Datasheet" "~"\n'
            f'\t\t\t(at {x} {y} 0)\n'
            f'\t\t\t(effects (font (size 1.27 1.27)) (hide yes)))\n'
            f'\t\t(instances\n'
            f'\t\t\t(project "{PROJ}"\n'
            f'\t\t\t\t(path "/{PROJ_UUID}"\n'
            f'\t\t\t\t\t(reference "{ref}") (unit 1))))\n'
            f'\t)\n')

def label_at(text, x, y, size=1.27):
    return (f'\t(label "{text}"\n'
            f'\t\t(at {x} {y} 0)\n'
            f'\t\t(effects (font (size {size} {size})) (justify left bottom))\n'
            f'\t\t(uuid "{uuid("label:"+text+f":{x}:{y}")}"))\n')

def wire_at(x1, y1, x2, y2):
    return (f'\t(wire\n'
            f'\t\t(pts (xy {x1} {y1}) (xy {x2} {y2}))\n'
            f'\t\t(stroke (width 0) (type default))\n'
            f'\t\t(uuid "{uuid(f"wire:{x1}:{y1}:{x2}:{y2}")}"))\n')

def no_connect_at(x, y, k):
    return f'\t(no_connect (at {x} {y}) (uuid "{uuid(f"nc:{k}")}"))\n'

def text_at(text, x, y, size=2.0, justify="left bottom"):
    return (f'\t(text "{text}"\n'
            f'\t\t(at {x} {y} 0)\n'
            f'\t\t(effects (font (size {size} {size})) (justify {justify}))\n'
            f'\t\t(uuid "{uuid(f"text:{x}:{y}:"+text[:30])}"))\n')

def text_box_safety(text, x, y, w, h):
    """A red-bordered polyline box + text marking a safety-critical zone."""
    tag = f"safety:{x}:{y}"
    box = (f'\t(polyline\n'
           f'\t\t(pts (xy {x} {y}) (xy {x+w} {y}) (xy {x+w} {y+h}) (xy {x} {y+h}) (xy {x} {y}))\n'
           f'\t\t(stroke (width 0.5) (type default) (color 220 0 0 1))\n'
           f'\t\t(uuid "{uuid("box:"+tag)}"))\n')
    return box + text_at(text, x+1, y+3, size=1.5)


PROJ_UUID = uuid("proj-root")


def build_schematic():
    parts = []
    parts.append('(kicad_sch\n')
    parts.append('\t(version 20231120)\n')
    parts.append('\t(generator "eeschema")\n')
    parts.append('\t(generator_version "8.0")\n')
    parts.append(f'\t(uuid "{PROJ_UUID}")\n')
    parts.append('\t(paper "A2")\n')
    parts.append('\t(title_block\n')
    parts.append('\t\t(title "Hearth Halbach Levitation Controller")\n')
    parts.append('\t\t(date "2026-08-03")\n')
    parts.append('\t\t(rev "A0")\n')
    parts.append('\t\t(company "Hearth")\n')
    parts.append('\t\t(comment 1 "SAFETY-CRITICAL: 2kg glass orb levitates via active servo control - a controller fault means the orb falls")\n')
    parts.append('\t\t(comment 2 "Dual STM32H723 lockstep, 6x DRV8323 half-bridge, 6x MLX90393 hall, MAX706 window WDT, hardware OC latch, E-stop")\n')
    parts.append('\t\t(comment 3 "Reference: hardware/electrical/block-diagrams/levitation-controller.md")\n')
    parts.append('\t\t(comment 4 "PLACEHOLDER schematic - EE completes wiring + safety review before power-on")\n')
    parts.append('\t)\n')

    # ---- lib_symbols block ----
    parts.append('\t(lib_symbols\n')
    parts.append(sch_lib_symbol_R())
    parts.append(sch_lib_symbol_C())
    parts.append(sch_lib_symbol_power("+3V3"))
    parts.append(sch_lib_symbol_power("+5V"))
    parts.append(sch_lib_symbol_power("+12V"))
    parts.append(sch_lib_symbol_power("+48V"))
    parts.append(sch_lib_symbol_gnd("GND"))
    parts.append(sch_lib_symbol_gnd("GNDA"))
    parts.append(sch_lib_symbol_gnd("PGND"))
    # Specialty symbols embedded (offline-openable)
    for build_fn in (build_stm32h723, build_drv8323, build_ina240,
                     build_mlx90393, build_max706, build_mcp2542fd,
                     build_tl331, build_ipi050n06n, build_stm32g030,
                     build_rtk2412):
        # Nest under palpod-halbach-controller: prefix
        raw = build_fn()
        # Rewrite the outer (symbol "Name" ...) so the lib_id becomes palpod-halbach-controller:Name
        # The raw string starts with '\t(symbol "Name"'
        idx = raw.index('"') + 1
        idx2 = raw.index('"', idx)
        name = raw[idx:idx2]
        raw = raw.replace(f'(symbol "{name}"', f'(symbol "palpod-halbach-controller:{name}"', 1)
        parts.append(indent(raw, tabs=1))
    parts.append('\t)\n')  # end lib_symbols

    # ---- Populated area: title text + safety-critical annotation banners ----

    # Top-of-sheet banner
    parts.append(text_at("PAL POD HALBACH LEVITATION CONTROLLER - REV A0 - PLACEHOLDER", 20, 15, 3.0))
    parts.append(text_at("SAFETY-CRITICAL - Full design review + FMEA required before first power-on", 20, 20, 2.0))
    parts.append(text_at("Reference: hardware/electrical/block-diagrams/levitation-controller.md", 20, 24, 1.5))

    # Big safety-critical zones as visible red-bordered rectangles with legend text
    parts.append(text_box_safety("SAFETY-CRITICAL NET GROUP #1 - OC_LATCH / nFAULT / WDOG - DO NOT REMOVE",
                                 20, 40, 200, 12))
    parts.append(text_box_safety("SAFETY-CRITICAL NET GROUP #2 - ESTOP_IN / ESTOP_LATCH - hardwired to MAX706 MR - DO NOT REMOVE",
                                 20, 220, 240, 12))
    parts.append(text_box_safety("SAFETY-CRITICAL NET GROUP #3 - LOCKSTEP_A/B consensus between STM32H723 pair - DO NOT REMOVE",
                                 20, 370, 240, 12))

    # ---- Power rails (top left cluster) ----
    x0 = 30
    y0 = 60
    parts.append(placed_symbol("power:+48V", "#PWR001", "+48V", x0, y0,      "pwr48"))
    parts.append(placed_symbol("power:+12V", "#PWR002", "+12V", x0+15, y0,   "pwr12"))
    parts.append(placed_symbol("power:+5V",  "#PWR003", "+5V",  x0+30, y0,   "pwr5"))
    parts.append(placed_symbol("power:+3V3", "#PWR004", "+3V3", x0+45, y0,   "pwr3v3"))
    parts.append(placed_symbol("power:GND",  "#PWR005", "GND",  x0+60, y0+5, "pwrgnd"))
    parts.append(placed_symbol("power:GNDA", "#PWR006", "GNDA", x0+75, y0+5, "pwrgnda"))
    parts.append(placed_symbol("power:PGND", "#PWR007", "PGND", x0+90, y0+5, "pwrpgnd"))
    parts.append(text_at("Power tree: 12V input -> RTK-2412 isolated -> 48V coil rail. 12V -> 5V -> 3V3 for logic.",
                         x0, y0-5, 1.2))
    for label, x in (("+48V", x0), ("+12V", x0+15), ("+5V", x0+30), ("+3V3", x0+45)):
        parts.append(label_at(label, x, y0+8))

    # ---- Isolated DC-DC brick + 48V rail (upper mid) ----
    xU, yU = 130, 75
    parts.append(placed_symbol("palpod-halbach-controller:RTK-2412", "U10", "RTK-2412",
                               xU, yU, "u10", "palpod-halbach-controller:SIP-4_Recom_RTK"))
    parts.append(text_at("U10: Recom RTK-2412 - isolated 12V->24V driver rail (2W)", xU-5, yU-15, 1.2))
    parts.append(text_at("For 48V: cascade with LM5155 boost per driver-stage spec", xU-5, yU-12, 1.0))

    # ---- Twin STM32H723 (lockstep pair) ----
    xM1, yM1 = 60, 110
    parts.append(placed_symbol("palpod-halbach-controller:STM32H723ZGT6", "U1", "STM32H723ZGT6 (Primary)",
                               xM1, yM1, "u1", "palpod-halbach-controller:LQFP-144_20x20mm_P0.5mm"))
    xM2, yM2 = 180, 110
    parts.append(placed_symbol("palpod-halbach-controller:STM32H723ZGT6", "U2", "STM32H723ZGT6 (Redundant)",
                               xM2, yM2, "u2", "palpod-halbach-controller:LQFP-144_20x20mm_P0.5mm"))
    parts.append(text_at("Lockstep pair - both compute the servo loop; disagreement latches SAFE-SHUTDOWN",
                         xM1-10, yM1-55, 1.5))
    parts.append(text_at("Cross-strapped SPI: LOCKSTEP_A (U1 SPI2->U2 SPI2), LOCKSTEP_B (U2 SPI3->U1 SPI3)",
                         xM1-10, yM1-52, 1.2))

    # A few illustrative labels near MCUs
    parts.append(label_at("LOCKSTEP_A_MOSI", xM1+80, yM1-30))
    parts.append(label_at("LOCKSTEP_A_MISO", xM1+80, yM1-27))
    parts.append(label_at("LOCKSTEP_A_SCK",  xM1+80, yM1-24))
    parts.append(label_at("LOCKSTEP_B_MOSI", xM1+80, yM1-15))
    parts.append(label_at("LOCKSTEP_B_MISO", xM1+80, yM1-12))
    parts.append(label_at("LOCKSTEP_B_SCK",  xM1+80, yM1-9))
    parts.append(wire_at(xM1+65, yM1-30, xM2-65, yM2-30))
    parts.append(wire_at(xM1+65, yM1-27, xM2-65, yM2-27))
    parts.append(wire_at(xM1+65, yM1-24, xM2-65, yM2-24))

    # ---- MAX706 watchdog supervisor ----
    xW, yW = 300, 100
    parts.append(placed_symbol("palpod-halbach-controller:MAX706", "U3", "MAX706",
                               xW, yW, "u3", "palpod-halbach-controller:SOIC-8_3.9x4.9mm_P1.27mm"))
    parts.append(text_at("U3: MAX706 window WDT + MR (manual reset from E-stop) + PFI (power-fail input)",
                         xW-15, yW-15, 1.2))
    parts.append(label_at("WDOG_WDI", xW-15, yW-3))
    parts.append(label_at("WDOG_RESETn", xW+15, yW-3))
    parts.append(label_at("ESTOP_LATCH", xW-15, yW-6))

    # ---- TL331 hardware overcurrent comparator ----
    xC, yC = 330, 150
    parts.append(placed_symbol("palpod-halbach-controller:TL331", "U4", "TL331",
                               xC, yC, "u4", "palpod-halbach-controller:SOT-23-5"))
    parts.append(text_at("U4: TL331 - hardware overcurrent latch. Independent of MCU firmware.", xC-15, yC-10, 1.2))
    parts.append(label_at("OC_SUM_IN", xC-15, yC-3))
    parts.append(label_at("OC_LATCH",  xC+15, yC-3))

    # ---- CAN-FD transceiver ----
    xCAN, yCAN = 380, 100
    parts.append(placed_symbol("palpod-halbach-controller:MCP2542FD", "U5", "MCP2542FD",
                               xCAN, yCAN, "u5", "palpod-halbach-controller:SOIC-8_3.9x4.9mm_P1.27mm"))
    parts.append(label_at("CAN_TXD", xCAN-15, yCAN-3))
    parts.append(label_at("CAN_RXD", xCAN-15, yCAN))
    parts.append(label_at("CANH",    xCAN+15, yCAN-3))
    parts.append(label_at("CANL",    xCAN+15, yCAN))

    # ---- Aux housekeeping MCU (STM32G030) ----
    xA, yA = 380, 180
    parts.append(placed_symbol("palpod-halbach-controller:STM32G030K8T6", "U6", "STM32G030K8T6",
                               xA, yA, "u6", "palpod-halbach-controller:LQFP-32_7x7mm_P0.8mm"))
    parts.append(text_at("U6: Aux MCU - coil temperature monitoring + heatsink fan PWM",
                         xA-15, yA-25, 1.2))

    # ---- 6 Hall sensor connectors + 6 MLX90393 symbols ----
    # Represent as 6 MLX90393 sensor symbol instances plus 6 JST-PH connector footprints stubbed
    # (connectors placed as text callouts to keep symbol count manageable)
    hall_pos = [(20 + i*30, 260) for i in range(6)]
    for i, (hx, hy) in enumerate(hall_pos):
        parts.append(placed_symbol("palpod-halbach-controller:MLX90393", f"U{7+i}",
                                   f"MLX90393 #{i+1}", hx, hy, f"hall{i}",
                                   "palpod-halbach-controller:QFN-16_3x3mm_P0.5mm"))
        parts.append(label_at(f"HALL{i}_SDA", hx-15, hy-3))
        parts.append(label_at(f"HALL{i}_SCL", hx-15, hy))
        parts.append(label_at(f"HALL{i}_DRDY", hx-15, hy+3))
    parts.append(text_at("6x MLX90393 3D hall sensors - 3 around column top + 3 around expected orb position",
                         20, 245, 1.5))

    # ---- 6 coil driver blocks: DRV8323 + 2x FET + INA240 + coil terminal ----
    # Layout in 2 rows of 3
    for i in range(6):
        col = i % 3
        row = i // 3
        bx = 40 + col*90
        by = 320 + row*40
        # DRV8323
        parts.append(placed_symbol("palpod-halbach-controller:DRV8323",
                                   f"U{13+i}", f"DRV8323 CH{i+1}",
                                   bx, by, f"drv{i}",
                                   "palpod-halbach-controller:HTSSOP-48_6.1x12.5mm_P0.5mm_EP"))
        # High-side FET
        parts.append(placed_symbol("palpod-halbach-controller:IPI050N06N",
                                   f"Q{i*2+1}", "IPI050N06N",
                                   bx+30, by-10, f"qh{i}",
                                   "palpod-halbach-controller:TO-262-3_TabPin2"))
        # Low-side FET
        parts.append(placed_symbol("palpod-halbach-controller:IPI050N06N",
                                   f"Q{i*2+2}", "IPI050N06N",
                                   bx+30, by+10, f"ql{i}",
                                   "palpod-halbach-controller:TO-262-3_TabPin2"))
        # INA240 current sense amp
        parts.append(placed_symbol("palpod-halbach-controller:INA240",
                                   f"U{25+i}", "INA240",
                                   bx+55, by, f"ina{i}",
                                   "palpod-halbach-controller:TSSOP-8_4.4x3mm_P0.65mm"))
        # Coil output labels
        parts.append(label_at(f"COIL_{i+1}_HIGH", bx+70, by-5))
        parts.append(label_at(f"COIL_{i+1}_LOW",  bx+70, by+5))
        parts.append(label_at(f"OC_CH{i+1}",      bx+70, by))
        # Block title
        parts.append(text_at(f"Coil Driver Block CH{i+1} - DRV8323 + IPI050N06N half-bridge + INA240 shunt-amp",
                             bx-5, by-18, 1.2))

    # ---- E-stop input terminal (labeled) ----
    parts.append(text_at("E-STOP INPUT (rear panel) - hardwired to MAX706 MR pin, coils de-energize <10ms",
                         20, 405, 1.8))
    parts.append(label_at("ESTOP_IN", 30, 415))

    # ---- Decoupling capacitors: one per critical rail (illustrative) ----
    cap_pos = [(240 + i*8, 50) for i in range(10)]
    for i, (cx, cy) in enumerate(cap_pos):
        parts.append(placed_symbol("Device:C", f"C{i+1}", "100nF", cx, cy,
                                   f"cap{i}", "Capacitor_SMD:C_0402_1005Metric"))
    # Bulk caps for coil rail
    for i, cx in enumerate([240, 260, 280]):
        parts.append(placed_symbol("Device:C", f"C{i+11}", "220uF", cx, 65,
                                   f"bulk{i}", "Capacitor_SMD:CP_Elec_10x10.5"))

    # ---- Resistors: pullups + shunt (illustrative) ----
    for i, rx in enumerate([80, 90, 100, 110, 120]):
        parts.append(placed_symbol("Device:R", f"R{i+1}", "10k", rx, 200,
                                   f"r{i}", "Resistor_SMD:R_0402_1005Metric"))
    for i, rx in enumerate([200, 210, 220, 230, 240, 250]):
        parts.append(placed_symbol("Device:R", f"R{i+6}", "0R005 5W", rx, 340,
                                   f"rshunt{i}", "Resistor_SMD:R_2512_6332Metric"))

    # ---- Illustrative wires connecting some things ----
    parts.append(wire_at(30, 80, 30, 90))
    parts.append(wire_at(45, 80, 45, 90))
    parts.append(wire_at(60, 65, 90, 65))
    parts.append(wire_at(30, 65, 60, 65))

    # ---- no_connect for BOOT pins etc ----
    parts.append(no_connect_at(180, 250, "nc1"))
    parts.append(no_connect_at(210, 250, "nc2"))
    parts.append(no_connect_at(240, 250, "nc3"))

    # ---- Global bottom notice ----
    parts.append(text_at("BEFORE POWER-ON: verify (1) OC latch trips at correct threshold, (2) MAX706 WDT window,",
                         20, 425, 1.5))
    parts.append(text_at("(3) E-stop opens contactor within 10ms, (4) lockstep MCUs agree on servo output.",
                         20, 428, 1.5))

    # ---- sheet_instances footer ----
    parts.append('\t(sheet_instances\n')
    parts.append('\t\t(path "/" (page "1"))\n')
    parts.append('\t)\n')
    parts.append(')\n')
    return "".join(parts)


# ---------------------------------------------------------------------------
# PCB
# ---------------------------------------------------------------------------

def build_pcb():
    nets = [
        "+48V","+12V","+5V","+3V3","GND","GNDA","PGND",
        "CANH","CANL","CAN_TXD","CAN_RXD",
        "ESTOP_IN","ESTOP_LATCH","OC_LATCH","OC_SUM_IN",
        "WDOG_WDI","WDOG_RESETn",
        "LOCKSTEP_A_MOSI","LOCKSTEP_A_MISO","LOCKSTEP_A_SCK",
        "LOCKSTEP_B_MOSI","LOCKSTEP_B_MISO","LOCKSTEP_B_SCK",
    ]
    for i in range(6):
        nets += [f"COIL_{i+1}_HIGH", f"COIL_{i+1}_LOW",
                 f"PHASE_{i+1}", f"OC_CH{i+1}",
                 f"HALL{i}_SDA", f"HALL{i}_SCL", f"HALL{i}_DRDY"]
    for i in range(6):
        nets += [f"nFAULT_CH{i+1}"]

    net_defs = "\n".join(f'  (net {i+1} "{n}")' for i, n in enumerate(nets))

    # 150mm x 100mm Edge.Cuts (origin at 0,0 lower-left => choose 50,50 upper-left)
    x1, y1 = 50, 50
    x2, y2 = x1 + 150, y1 + 100

    pcb = f'''(kicad_pcb
  (version 20240108)
  (generator "pcbnew")
  (generator_version "8.0")
  (general
    (thickness 1.6)
    (legacy_teardrops no)
  )
  (paper "A3")
  (title_block
    (title "Hearth Halbach Levitation Controller - PCB")
    (date "2026-08-03")
    (rev "A0")
    (company "Hearth")
    (comment 1 "SAFETY-CRITICAL 4-layer 150x100mm - active servo controller")
    (comment 2 "F.Cu 2oz / In1.Cu (GND) 1oz / In2.Cu (PWR high-current) 1oz / B.Cu 2oz - ENIG")
    (comment 3 "Reference: hardware/electrical/block-diagrams/levitation-controller.md")
  )
  (layers
    (0 "F.Cu" signal)
    (1 "In1.Cu" power "GND")
    (2 "In2.Cu" power "PWR_HIGH_CURRENT")
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
    (50 "User.1" user "SAFETY.Callouts")
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
      (layer "F.Cu" (type "copper") (thickness 0.070))
      (layer "dielectric 1" (type "prepreg") (thickness 0.2) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In1.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 2" (type "core") (thickness 1.06) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In2.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 3" (type "prepreg") (thickness 0.2) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "B.Cu" (type "copper") (thickness 0.070))
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
      (outputdirectory "fab/gerbers/")
    )
  )
  (net 0 "")
{net_defs}

  (gr_rect
    (start {x1} {y1}) (end {x2} {y2})
    (stroke (width 0.15) (type solid)) (fill none)
    (layer "Edge.Cuts")
    (uuid "{uuid("edge:rect")}")
  )

  (gr_text "Hearth Halbach Levitation Controller - Rev A0 - PLACEHOLDER PCB"
    (at {x1+5} {y1+5} 0)
    (layer "F.SilkS")
    (uuid "{uuid("silk:title")}")
    (effects (font (size 2.5 2.5) (thickness 0.35)) (justify left top)))

  (gr_text "SAFETY-CRITICAL BOARD - Full FMEA / DFMEA / power-on checklist required before energizing coils"
    (at {x1+5} {y1+10} 0)
    (layer "F.SilkS")
    (uuid "{uuid("silk:safety")}")
    (effects (font (size 1.5 1.5) (thickness 0.25)) (justify left top)))

  (gr_text "4-layer  F.Cu 2oz signal / In1.Cu GND / In2.Cu PWR_HIGH_CURRENT / B.Cu 2oz signal - ENIG"
    (at {x1+5} {y2-5} 0)
    (layer "F.SilkS")
    (uuid "{uuid("silk:stackup")}")
    (effects (font (size 1.2 1.2) (thickness 0.2)) (justify left bottom)))

  (gr_text "COIL_HIGH_CURRENT nets: 5mm min width on 2oz outer copper for 30A per phase peak"
    (at {x1+5} {y2-8} 0)
    (layer "Cmts.User")
    (uuid "{uuid("cmt:coil")}")
    (effects (font (size 1.5 1.5) (thickness 0.2)) (justify left bottom)))

  (gr_text "GND plane (In1.Cu) - analog/digital moat between MCU quadrant and coil-driver quadrant"
    (at {x1+5} {y2-11} 0)
    (layer "Cmts.User")
    (uuid "{uuid("cmt:gnd")}")
    (effects (font (size 1.5 1.5) (thickness 0.2)) (justify left bottom)))

  (gr_text "SAFETY-CRITICAL NET GROUP: OC_LATCH / ESTOP_LATCH / WDOG_RESETn - route as short, redundant, guarded"
    (at {x1+5} {y1+13} 0)
    (layer "User.1")
    (uuid "{uuid("safety:cmt1")}")
    (effects (font (size 1.5 1.5) (thickness 0.25)) (justify left top)))

  (gr_text "SAFETY-CRITICAL NET GROUP: LOCKSTEP_A / LOCKSTEP_B - cross-strap between the two STM32H723 devices"
    (at {x1+5} {y1+16} 0)
    (layer "User.1")
    (uuid "{uuid("safety:cmt2")}")
    (effects (font (size 1.5 1.5) (thickness 0.25)) (justify left top)))

  (gr_text "ISO 7010 W006 magnetic-field warning label goes here (silkscreen or mechanical drawing)"
    (at {x2-5} {y1+5} 0)
    (layer "F.SilkS")
    (uuid "{uuid("silk:iso")}")
    (effects (font (size 1.2 1.2) (thickness 0.2)) (justify right top)))
)
'''
    return pcb


# ---------------------------------------------------------------------------
# Support files
# ---------------------------------------------------------------------------

def build_sym_lib_table():
    return ('(sym_lib_table\n'
            '  (version 7)\n'
            f'  (lib (name "palpod-halbach-controller")(type "KiCad")'
            f'(uri "${{KIPRJMOD}}/libraries/palpod-halbach-controller.kicad_sym")'
            f'(options "")(descr "Hearth Halbach controller specialty symbols'
            f' (STM32H723, DRV8323, INA240, MLX90393, MAX706, MCP2542FD, TL331,'
            f' IPI050N06N, STM32G030, RTK-2412)"))\n'
            ')\n')

def build_fp_lib_table():
    return ('(fp_lib_table\n'
            '  (version 7)\n'
            f'  (lib (name "palpod-halbach-controller")(type "KiCad")'
            f'(uri "${{KIPRJMOD}}/libraries/palpod-halbach-controller.pretty")'
            f'(options "")(descr "Hearth Halbach controller specialty footprints (placeholder outlines)"))\n'
            ')\n')

def build_prl():
    prl = {
      "board": {
        "active_layer": 0, "active_layer_preset": "",
        "auto_track_width": True,
        "hidden_netclasses": [], "hidden_nets": [],
        "high_contrast_mode": 0, "net_color_mode": 1,
        "opacity": {"images": 0.6, "pads": 1.0, "shapes": 1.0, "tracks": 1.0, "vias": 1.0, "zones": 0.6},
        "prototype_zone_fills": False,
        "selection_filter": {
          "dimensions": True, "footprints": True, "graphics": True,
          "keepouts": True, "lockedItems": False, "otherItems": True,
          "pads": True, "text": True, "tracks": True, "vias": True, "zones": True
        },
        "visible_items": [
          "vias","footprint_text","footprint_anchors","ratsnest","grid",
          "footprints_front","footprints_back","footprint_values",
          "footprint_references","tracks","drc_errors","drawing_sheet",
          "bitmaps","pads","zones","drc_warnings","locked_item_shadows",
          "conflict_shadows","shapes"
        ],
        "visible_layers": "00000000_00000000_0ffffff7_ffffffff",
        "zone_display_mode": 0
      },
      "git": {"integration_disabled": False, "repo_type": "",
              "repo_username": "", "ssh_key": ""},
      "meta": {"filename": PROJ+".kicad_prl", "version": 5},
      "net_inspector_panel": {
        "col_hidden": [], "col_order": [], "col_widths": [],
        "custom_group_rules": [], "expanded_rows": [],
        "filter_by_net_name": True, "filter_by_netclass": True,
        "filter_text": "", "group_by_constraint": False,
        "group_by_netclass": False, "show_time_domain_details": False,
        "show_unconnected_nets": False, "show_zero_pad_nets": False,
        "sort_ascending": True, "sorting_column": -1
      },
      "open_jobsets": [], "project": {"files": []},
      "schematic": {
        "hierarchy_collapsed": [],
        "selection_filter": {
          "graphics": True, "images": True, "labels": True,
          "lockedItems": False, "otherItems": True, "pins": True,
          "ruleAreas": True, "symbols": True, "text": True, "wires": True
        }
      }
    }
    return json.dumps(prl, indent=2)


def build_readme():
    return f"""# Hearth Halbach Levitation Controller — KiCad Project

**SAFETY-CRITICAL BOARD.** This is the real-time active stabilization
controller for the Halbach neodymium levitation array that holds the OLED orb
in front of the column. A control failure means a 2 kg glass sphere becomes a
projectile aimed at the user's rug (or foot). Treat every net, every symbol,
and every layout decision on this board as safety-critical until proven
otherwise via FMEA.

> ⚠️  **SAFETY REVIEW REQUIRED BEFORE POWER-ON.** Before energizing the 48 V
> coil rail for the first time — even on the bench — a licensed EE must sign
> off on the following in writing:
>
> 1. **Overcurrent latch verified.** TL331 (`U4`) trips the DRV8323 nFAULT
>    line when the summed INA240 output exceeds the hardware threshold
>    (target 30 A per phase). Bench-verify with a current-limited supply and
>    a scope; do not rely on datasheet values.
> 2. **Watchdog window verified.** MAX706 (`U3`) issues RESETn if the primary
>    STM32H723 misses a WDI pet in the 100 ms window. Firmware halts must be
>    provably caught in < 110 ms end-to-end.
> 3. **E-stop opens the coil rail in < 10 ms.** The rear-panel E-stop must
>    drive the MAX706 MR pin *and* an in-line contactor on the 48 V rail —
>    software must not be in the critical path. Latching; reset requires
>    physical button press.
> 4. **Lockstep pair agrees.** Both `U1` and `U2` (STM32H723ZGT6) compute the
>    same servo output every 100 µs; disagreement > tolerance latches
>    SAFE-SHUTDOWN (coils de-energize, catch-net engages, orb comes down
>    controlled).
> 5. **Drop-catch net installed.** The internal catch-net inside the column
>    is present and rated for the orb's terminal drop energy from full
>    levitation height.
> 6. **Magnetic-field survey.** Exterior surface field < 100 µT at maximum
>    coil current per ICNIRP 2020 general-public reference levels. Test with
>    a Narda ELT-400 or equivalent.
> 7. **Pacemaker / ISO 7010 W006 warning label** applied to the column at
>    the top plate and included in the setup manual.

See `../../block-diagrams/levitation-controller.md` for the system-level
control loop, latency budget, fault-response matrix, and regulatory notes.

## How to open

Requires **KiCad 8.0.0 or later** (KiCad 9 and 10 also open cleanly;
we developed and validated against KiCad 10.0.5 on macOS).

```
open -a KiCad {os.path.join(ROOT, PROJ+'.kicad_pro')}
```

Or double-click `palpod-halbach-controller.kicad_pro` in Finder. From KiCad's
project manager, open **Schematic Editor** and **PCB Editor**.

Project-local symbol and footprint libraries live in `libraries/`; the
`sym-lib-table` and `fp-lib-table` at the project root register them under the
alias `palpod-halbach-controller`. Standard KiCad symbols (`Device:R`,
`Device:C`, `power:*`) are embedded in the schematic's `lib_symbols` block so
the schematic opens even on a fresh KiCad install that has not yet configured
its stock libraries.

## What's populated

- [x] `.kicad_pro`: 4-layer stackup, ENIG, JLCPCB-friendly minimums, and
      **five net classes**:
    - `Default` — 0.2 mm signal
    - `Power` — 0.5 mm rails
    - `COIL_HIGH_CURRENT` — **5.0 mm min width, 2.0 mm vias**, orange in
      the PCB editor; auto-assigned to `COIL_*`, `PHASE_*`, `PVDD`, `PGND`.
    - `CAN_FD_DIFF` — 100 Ω differential CAN-FD pair (`CANH`/`CANL`)
    - `SAFETY_CRITICAL` — pink; auto-assigned to `ESTOP*`, `OC_LATCH*`,
      `WDOG*`, `nFAULT*`, `LOCKSTEP*`
- [x] `.kicad_sch` root schematic on A2 with populated title block
      (rev A0, 2026-08-03), embedded `lib_symbols` for every reference used.
- [x] Placed symbols:
    - 2× STM32H723ZGT6 (`U1` primary, `U2` redundant) — the lockstep pair
    - 1× MAX706 window watchdog supervisor (`U3`)
    - 1× TL331 hardware overcurrent comparator (`U4`)
    - 1× MCP2542FD CAN-FD transceiver (`U5`)
    - 1× STM32G030K8T6 aux housekeeping MCU (`U6`)
    - 6× MLX90393 3D hall-effect sensors (`U7`…`U12`)
    - 6× DRV8323 gate drivers (`U13`…`U18`)
    - 12× IPI050N06N MOSFETs (`Q1`…`Q12`) — one half-bridge per driver
    - 6× INA240 current-sense amps (`U25`…`U30`)
    - 1× Recom RTK-2412 isolated DC-DC brick (`U10`) for driver rail
      isolation
    - Bulk + local decoupling capacitors, shunt resistors, pull-ups
    - Power flags: `+48V`, `+12V`, `+5V`, `+3V3`, `GND`, `GNDA`, `PGND`
- [x] Three big red-bordered safety-callout banners on the schematic
      explicitly labeling the `OC_LATCH`, `ESTOP_LATCH`, and `LOCKSTEP_A/B`
      net groups as `SAFETY-CRITICAL — DO NOT REMOVE`.
- [x] Illustrative wires and 40+ pre-placed labels seeding the wiring
      pattern: `LOCKSTEP_A_MOSI/MISO/SCK`, `LOCKSTEP_B_MOSI/MISO/SCK`,
      `WDOG_WDI`, `WDOG_RESETn`, `ESTOP_LATCH`, `ESTOP_IN`, `OC_LATCH`,
      `OC_SUM_IN`, `CAN_TXD`, `CAN_RXD`, `CANH`, `CANL`,
      `HALL0_SDA` … `HALL5_DRDY`, `COIL_1_HIGH` … `COIL_6_LOW`,
      `OC_CH1` … `OC_CH6`.
- [x] `no_connect` flags on illustrative test pins.
- [x] `libraries/palpod-halbach-controller.kicad_sym` — hand-drawn symbols
      for **10 specialty parts**: STM32H723ZGT6 (LQFP-144), DRV8323
      (HTSSOP-48 EP), INA240 (TSSOP-8), MLX90393 (QFN-16), MAX706 (SO-8),
      MCP2542FD (SO-8), TL331 (SOT-23-5), IPI050N06N (TO-262), STM32G030K8T6
      (LQFP-32), RTK-2412 (SIP-4). **Pin mappings are placeholder
      groupings — the EE must verify each pin against the manufacturer
      datasheet before wiring.**
- [x] `libraries/palpod-halbach-controller.pretty/` — twelve placeholder
      footprints. See `libraries/palpod-halbach-controller.pretty/README.md`
      for per-part verification checklist.
- [x] `.kicad_pcb`: 4-layer stackup declared
      (`F.Cu` signal 2 oz / `In1.Cu` GND 1 oz / `In2.Cu` PWR_HIGH_CURRENT
      1 oz / `B.Cu` signal 2 oz), 1.6 mm total, ENIG finish.
      **150 × 100 mm rectangular Edge.Cuts** drawn. Silkscreen and
      SAFETY.Callouts (`User.1`) layer notes populated. No footprints placed
      yet — the EE places them during layout.
- [x] `sym-lib-table` / `fp-lib-table` register the project-local
      `palpod-halbach-controller` library.

## What's stubbed / next steps for the EE

- [ ] **Verify placeholder footprints against real datasheets** before ordering
      fab. See `libraries/palpod-halbach-controller.pretty/README.md`. The
      MOSFET and DRV8323 placeholders in particular are safety-critical — a
      wrong pad on the current-sense pins would defeat the OC latch.
- [ ] **Verify placeholder pin mappings** on all specialty symbols against the
      manufacturer datasheets. Update
      `libraries/palpod-halbach-controller.kicad_sym` with correct pin numbers,
      names, and electrical types.
- [ ] **Complete the schematic wiring** — this is a placeholder; the EE draws
      the actual nets. Priorities in this order:
    1. **Lockstep interconnect** (`U1` ↔ `U2` SPI cross-strap) — this is what
       makes the board single-fault tolerant.
    2. **OC latch chain** — 6× INA240 outputs sum into TL331 (`U4`) input,
       comparator output latches through an SR flip-flop, drives all
       DRV8323 nENABLE lines low. Independent of MCU firmware.
    3. **Watchdog chain** — U1 pets MAX706 WDI; MAX706 RESETn drives an
       AND gate on the enable path.
    4. **E-stop chain** — hardwired E-stop input → MAX706 MR → coil-rail
       contactor coil. Two-channel, redundant per SIL-2 practice.
    5. **CAN-FD bus** — U1/U2 FDCAN1 → MCP2542FD → CANH/CANL termination
       (120 Ω split-terminate at each end of the bus).
    6. **Hall sensor bus** — I2C bus (with per-sensor A0/A1 straps for
       unique addresses) or SPI daisy-chain from U1. Route as star from
       the MCU quadrant; twist pairs on the flex cable side.
    7. **6× DRV8323 SPI config + PWM** — SPI shared, 6× nSCS individual;
       6× (INHA/INLA/INHB/INLB/INHC/INLC) from timer channels.
    8. **48 V rail** — 12 V input → RTK-2412 isolation → LM5155 boost →
       coil rail. Bulk 470 µF / 100 V polymer at each DRV8323 PVDD pin
       plus one 1 mF electrolytic per pair.
    9. **Power tree** — 12 V → 5 V (LMR33630) → 3.3 V (TPS7A20) for logic;
       separate 3.3 V analog rail (`+3V3A`) for INA240 REF pins.
    10. **Decoupling** — 100 nF within 3 mm of every power pin; add
        4.7 µF bulk per rail per IC.
- [ ] Add ESD protection on the E-stop input (`PESD5V0L1BA`) and the CAN
      bus (`PSD03C-LF`).
- [ ] Add optional galvanic isolation on the CAN bus if the main-compute
      board runs on a different ground reference.
- [ ] Assign every schematic symbol a valid footprint (Tools → Assign
      Footprints). Cross-check each MOSFET pad against the datasheet
      before assigning.
- [ ] Update the PCB from the schematic (Tools → Update PCB from Schematic
      in the PCB editor).
- [ ] Place footprints on the 150 × 100 mm board:
    - **Coil-driver quadrant** on the right half of the board with the
      six DRV8323 + MOSFET pairs in a row along the top edge; INA240
      shunt-amps immediately downstream; 2-pin screw terminals for the
      coil outputs on the right board edge.
    - **MCU quadrant** on the left half; lockstep pair placed
      symmetrically about the vertical midline to keep cross-strap
      trace lengths matched.
    - **MAX706 + TL331 + estop terminal + fault-latch logic** in the
      bottom-center, straddling the moat between quadrants.
    - **CAN-FD transceiver + connector** on the left edge.
    - **Hall-sensor flex connectors** across the bottom edge (6× JST-PH
      or FPC, TBD by mechanical team).
- [ ] Pour GND (`In1.Cu`) — split zone with a **moat between the
      analog/logic and coil-driver domains**, tied at a single point near
      the ADC reference.
- [ ] Pour high-current PWR (`In2.Cu`) — divide into 48 V, 12 V, and 5 V
      zones; use polygon copper for the 48 V zone in the coil-driver
      quadrant. Target 5 mm min width on all `COIL_HIGH_CURRENT` traces on
      outer layers (2 oz copper handles ~30 A at this width with modest
      temperature rise).
- [ ] Route CAN-FD as a 100 Ω differential pair. Route lockstep SPI as
      length-matched pair between the two MCUs.
- [ ] Run ERC (`kicad-cli sch erc` or Tools → Electrical Rules Checker) —
      the placeholder generates violations; drive them to zero.
- [ ] Run DRC (`kicad-cli pcb drc` or Tools → Design Rules Checker) to
      zero, including `SAFETY_CRITICAL` clearance = 0.4 mm.
- [ ] **Formal design review** with a second EE (independent of the
      designer) covering the safety chain, current paths, and layout of
      the OC / WDT / lockstep / e-stop nets.
- [ ] **FMEA / DFMEA** covering every failure mode in the fault-response
      matrix in `levitation-controller.md`.
- [ ] Generate Gerbers + drill + BOM + pick-and-place
      (`File → Fabrication Outputs`). Cross-check the BOM against the block
      diagram.
- [ ] Order 5-unit proto run from JLCPCB (4-layer, 2 oz outer, ENIG,
      ~2-week turn).

## Command-line validation

The project has been validated with `kicad-cli` 10.0.5:

```
kicad-cli sch export netlist -o /tmp/palpod-halbach.net {PROJ}.kicad_sch
kicad-cli pcb export gerbers -o /tmp/g/                 {PROJ}.kicad_pcb
kicad-cli sym export svg     -o /tmp/sym-svg/           libraries/{PROJ}.kicad_sym
kicad-cli fp  export svg     -o /tmp/fp-svg/            libraries/{PROJ}.pretty
```

## File format

- Schematic schema version `20231120` (KiCad 8)
- PCB schema version `20240108` (KiCad 8)
- Symbol library schema version `20231120`
- Footprint schema version `20240108`

Written in the `(hide yes)` effect-block form so the same files load
identically under KiCad 8, 9, and 10.

## Certifications targeted (product-level, not board-level)

- **UL 60335** (Household and similar electrical appliances — Safety) for
  the appliance as a whole.
- **FCC Part 15** subpart B (unintentional radiator) — switching noise from
  the DRV8323 stage is the primary risk. Add pre-compliance scanning as
  early as possible.
- **ICNIRP 2020** general-public magnetic-field reference levels — verify
  at the column exterior surface under worst-case coil current.
- **FDA notice for magnetic-field-near-pacemaker** — product-level, not
  board-level, but the PCB silkscreen carries the ISO 7010 W006 icon.

## Reference

- **System-level block diagram, latency budget, fault-response matrix:**
  `../../block-diagrams/levitation-controller.md`
"""


def build_pretty_readme():
    return """# palpod-halbach-controller.pretty — PLACEHOLDER footprints

These `.kicad_mod` files are **starter outlines only**. They compile in
KiCad 8+ and give the schematic a valid footprint reference so the project
opens end-to-end, but the pad positions, sizes, and pin numbering are
best-effort approximations, not fabrication-ready.

**Before releasing to fab, the EE must verify every pad against the datasheet
of the actual package** and either re-generate these footprints from a
trusted source (SnapEDA, Ultra Librarian, IPC-7351 calculator, manufacturer
library) or hand-tune them to match the datasheet's recommended land pattern.

For a safety-critical board, an incorrect footprint on the MOSFET
source/drain, DRV8323 current-sense pins, or hall-sensor I2C address straps
would silently defeat the corresponding safety chain — treat this list as an
explicit gating checklist.

## Files

- `LQFP-144_20x20mm_P0.5mm.kicad_mod` — STMicro STM32H723ZGT6 primary and
  redundant MCU package. Verify against `RM0468` § "STM32H723ZG package
  information".
- `HTSSOP-48_6.1x12.5mm_P0.5mm_EP.kicad_mod` — TI DRV8323 (PWP package)
  gate driver. Exposed pad **must** be tied to GND with a via array;
  incorrect thermal pad handling causes intermittent shutdown under load.
- `TSSOP-8_4.4x3mm_P0.65mm.kicad_mod` — INA240 (D package) current-sense
  amp. Verify `IN+`/`IN-` pin order — reversal inverts the OC latch sense.
- `QFN-16_3x3mm_P0.5mm.kicad_mod` — Melexis MLX90393. Verify the I2C
  address straps (`A0`, `A1`) route to the correct board test-points so
  the six sensors get unique addresses.
- `SOIC-8_3.9x4.9mm_P1.27mm.kicad_mod` — MAX706 supervisor and MCP2542FD
  CAN-FD transceiver share this generic SO-8 footprint. Pin-1 marker
  correct for both.
- `SOT-23-5.kicad_mod` — TI TL331 comparator (DBV package).
- `TO-262-3_TabPin2.kicad_mod` — Infineon IPI050N06N N-channel MOSFET.
  Tab is drain, connects to pin 2. Ensure the drain copper pour connects
  to both pin 2 and the tab pad for adequate heatsinking.
- `LQFP-32_7x7mm_P0.8mm.kicad_mod` — STM32G030K8T6 aux MCU.
- `SIP-4_Recom_RTK.kicad_mod` — Recom RTK-2412 isolated DC-DC brick.
  Note the isolation gap requirement: no traces or planes may bridge the
  1500 VDC isolation barrier on the board.
- `Screw_Terminal_2Pin_5.08mm.kicad_mod` — 2-pin screw terminal used for
  each coil output. 5.08 mm pitch, rated ≥ 30 A.
- `JST-PH_4Pin.kicad_mod` — 4-pin JST-PH connector for the hall-sensor
  flex cable (VDD/SDA/SCL/GND).
- `Estop_Terminal_2Pin.kicad_mod` — 2-pin screw terminal for the hardwired
  E-stop input.

## Attributes

All footprints are marked `(attr smd)` (except the terminals) and populate:

- F.Fab / F.SilkS / F.CrtYd outlines
- A pin-1 indicator circle on F.SilkS
- SMD pads on F.Cu / F.Paste / F.Mask
- No 3D model reference (add `(model "${KIPRJMOD}/3d/<part>.step" ...)`
  when a model becomes available)

## Verification checklist (per footprint)

1. Cross-check package dimensions against the datasheet mechanical drawing.
2. Cross-check pad size and pitch against the recommended land pattern.
3. Cross-check pin-1 marker position against the datasheet pin/ball map.
4. Cross-check the courtyard against IPC-7351 (level B nominal for logic,
   level A dense not recommended for a safety-critical board).
5. Add solder-paste apertures / paste stencil reductions if manufacturer
   recommends them (HTSSOP EPs and QFN thermal pads usually do).
6. **MOSFET / DRV8323 / current-sense specific:** verify the current
   handling of the pad-to-copper connection is adequate for the peak
   30 A per-phase current with acceptable temperature rise.
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Symbol library
    lib = build_specialty_lib()
    write(f"{ROOT}/libraries/{PROJ}.kicad_sym", lib)

    # Footprints
    for name, descr, tags, npads, pitch, size, gx, *rest in FOOTPRINTS:
        kwargs = {}
        if rest:
            kwargs["grid_y"] = rest[0] if rest[0] else None
            if len(rest) >= 3:
                kwargs["rect_w"] = rest[1]
                kwargs["rect_h"] = rest[2]
        fp = fp_placeholder(name, descr, tags, npads, pitch, size, gx, **kwargs)
        write(f"{ROOT}/libraries/{PROJ}.pretty/{name}.kicad_mod", fp)

    # sym/fp lib tables
    write(f"{ROOT}/sym-lib-table", build_sym_lib_table())
    write(f"{ROOT}/fp-lib-table",  build_fp_lib_table())

    # Project
    write(f"{ROOT}/{PROJ}.kicad_pro", build_kicad_pro())
    write(f"{ROOT}/{PROJ}.kicad_prl", build_prl())

    # Schematic
    write(f"{ROOT}/{PROJ}.kicad_sch", build_schematic())

    # PCB
    write(f"{ROOT}/{PROJ}.kicad_pcb", build_pcb())

    # READMEs
    write(f"{ROOT}/README.md", build_readme())
    write(f"{ROOT}/libraries/{PROJ}.pretty/README.md", build_pretty_readme())

    print("\nDone.")


if __name__ == "__main__":
    main()

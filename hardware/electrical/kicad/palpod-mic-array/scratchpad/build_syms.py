#!/usr/bin/env python3
"""Generate palpod-mic-array.kicad_sym with 3 specialty symbols.

- ICS-41352: 5-pin LGA MEMS mic
- XVF3800:  61-pin LFBGA voice DSP (BGA grid A1..H8 minus 3 corners)
- NDP120:   69-pin LGA neural processor (1..69)

Uses KiCad 8/9/10 schema (20231120+) with (hide yes) form inside effects.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "libraries" / "palpod-mic-array.kicad_sym"

HEADER = '(kicad_symbol_lib\n\t(version 20231120)\n\t(generator "kicad_symbol_editor")\n'
FOOTER = ")\n"

def eff(size=1.27, hidden=False):
    h = "\n\t\t\t\t\t(hide yes)" if hidden else ""
    return f'(effects\n\t\t\t\t\t(font (size {size} {size})){h}\n\t\t\t\t)'

def sym_header(name, ref, desc, datasheet, footprint):
    return f'''\t(symbol "{name}"
\t\t(pin_names
\t\t\t(offset 1.016)
\t\t)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "{ref}"
\t\t\t(at 0 2.54 0)
\t\t\t(effects
\t\t\t\t(font (size 1.27 1.27))
\t\t\t)
\t\t)
\t\t(property "Value" "{name}"
\t\t\t(at 0 -2.54 0)
\t\t\t(effects
\t\t\t\t(font (size 1.27 1.27))
\t\t\t)
\t\t)
\t\t(property "Footprint" "{footprint}"
\t\t\t(at 0 0 0)
\t\t\t(effects
\t\t\t\t(font (size 1.27 1.27))
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "{datasheet}"
\t\t\t(at 0 0 0)
\t\t\t(effects
\t\t\t\t(font (size 1.27 1.27))
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" "{desc}"
\t\t\t(at 0 0 0)
\t\t\t(effects
\t\t\t\t(font (size 1.27 1.27))
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
'''

def sym_open_unit(name):
    return f'\t\t(symbol "{name}_1_1"\n'

def rectangle(x1, y1, x2, y2):
    return (f'\t\t\t(rectangle\n'
            f'\t\t\t\t(start {x1} {y1})\n'
            f'\t\t\t\t(end {x2} {y2})\n'
            f'\t\t\t\t(stroke (width 0.254) (type default))\n'
            f'\t\t\t\t(fill (type background))\n'
            f'\t\t\t)\n')

def pin(etype, style, x, y, angle, length, name, number):
    return (f'\t\t\t(pin {etype} {style}\n'
            f'\t\t\t\t(at {x} {y} {angle})\n'
            f'\t\t\t\t(length {length})\n'
            f'\t\t\t\t(name "{name}"\n'
            f'\t\t\t\t\t(effects (font (size 1.27 1.27)))\n'
            f'\t\t\t\t)\n'
            f'\t\t\t\t(number "{number}"\n'
            f'\t\t\t\t\t(effects (font (size 1.27 1.27)))\n'
            f'\t\t\t\t)\n'
            f'\t\t\t)\n')

def sym_close_unit():
    return '\t\t)\n'

def sym_close():
    return '\t)\n'


# ---------------- ICS-41352 ----------------
ics = []
ics.append(sym_header(
    "ICS-41352", "M",
    "TDK InvenSense ICS-41352 digital MEMS microphone (PDM, 5-pin LGA)",
    "https://invensense.tdk.com/products/analog/ics-41352/",
    "palpod-mic-array:ICS-41352_LGA5"))
ics.append(sym_open_unit("ICS-41352"))
ics.append(rectangle(-7.62, 5.08, 7.62, -5.08))
ics.append(pin("input",       "line", -10.16,  2.54, 0, 2.54, "CLK",    "3"))
ics.append(pin("output",      "line", -10.16,  0.00, 0, 2.54, "DATA",   "4"))
ics.append(pin("input",       "line", -10.16, -2.54, 0, 2.54, "SELECT", "5"))
ics.append(pin("power_in",    "line",  10.16,  2.54, 180, 2.54, "VDD",  "1"))
ics.append(pin("power_in",    "line",  10.16, -2.54, 180, 2.54, "GND",  "2"))
ics.append(sym_close_unit())
ics.append(sym_close())


# ---------------- XVF3800 (LFBGA-61) ----------------
rows = "ABCDEFGH"
skip = {("A", 8), ("H", 1), ("H", 8)}

label_pool = (
    ["VDD_CORE"] * 6 + ["VDDIO"] * 6 + ["GND"] * 10 +
    ["MCLK_IN", "MCLK_OUT", "PLL_FILT"] +
    [f"PDM_DATA{i}" for i in range(0, 8)] +
    ["PDM_CLK0", "PDM_CLK1"] +
    ["I2S_BCLK", "I2S_LRCLK", "I2S_SDOUT", "I2S_SDIN"] +
    ["I2C_SCL", "I2C_SDA"] +
    ["USB_DP", "USB_DN", "USB_VBUS", "USB_ID"] +
    ["RST_N", "BOOT_SEL", "DEBUG_SEL"] +
    ["XLINK_A0", "XLINK_A1", "XLINK_B0", "XLINK_B1"] +
    [f"GPIO{i}" for i in range(0, 12)]
)
assert len(label_pool) >= 61

pins_map = []
idx = 0
for r in rows:
    for c in range(1, 9):
        if (r, c) in skip:
            continue
        lbl = label_pool[idx]
        idx += 1
        if lbl.startswith("VDD") or lbl == "USB_VBUS":
            et = "power_in"
        elif lbl == "GND":
            et = "power_in"
        elif lbl.endswith("_N") or lbl.startswith("RST"):
            et = "input"
        elif lbl.startswith("PDM_DATA") or lbl.startswith("I2S_SDIN"):
            et = "input"
        elif lbl.startswith("PDM_CLK") or lbl.startswith("MCLK_OUT") or lbl.startswith("I2S_BCLK") or lbl.startswith("I2S_LRCLK") or lbl.startswith("I2S_SDOUT"):
            et = "output"
        elif lbl.startswith("I2C_") or lbl.startswith("USB_D") or lbl.startswith("USB_ID") or lbl.startswith("GPIO") or lbl.startswith("XLINK"):
            et = "bidirectional"
        elif lbl.startswith("MCLK_IN") or lbl.startswith("BOOT_SEL") or lbl.startswith("DEBUG_SEL"):
            et = "input"
        else:
            et = "passive"
        pins_map.append((r, c, lbl, et, f"{r}{c}"))

assert len(pins_map) == 61

xv = []
xv.append(sym_header(
    "XVF3800", "U",
    "XMOS XVF3800-INBW voice-processing DSP (61-pin LFBGA, 0.65mm pitch) - PLACEHOLDER pin mapping",
    "https://www.xmos.com/xvf3800/",
    "palpod-mic-array:XVF3800_LFBGA61"))
xv.append(sym_open_unit("XVF3800"))
body_w = 60.96
body_h = 91.44
xv.append(rectangle(-body_w/2, body_h/2, body_w/2, -body_h/2))

left = pins_map[:30]
right = pins_map[30:]
pitch = 2.54
top_y = (len(left) - 1) * pitch / 2
for i, (r, c, lbl, et, num) in enumerate(left):
    y = top_y - i * pitch
    xv.append(pin(et, "line", -body_w/2 - 2.54, y, 0, 2.54, lbl, num))
top_y = (len(right) - 1) * pitch / 2
for i, (r, c, lbl, et, num) in enumerate(right):
    y = top_y - i * pitch
    xv.append(pin(et, "line", body_w/2 + 2.54, y, 180, 2.54, lbl, num))
xv.append(sym_close_unit())
xv.append(sym_close())


# ---------------- NDP120 (LGA-69) ----------------
ndp_labels = (
    ["VDD_CORE"] * 4 + ["VDD_IO"] * 4 + ["VDD_ANA"] * 2 + ["GND"] * 12 +
    ["MCLK", "PLL_FILT"] +
    [f"PDM_DATA{i}" for i in range(0, 4)] +
    ["PDM_CLK"] +
    ["I2S_BCLK", "I2S_LRCLK", "I2S_SDIN", "I2S_SDOUT"] +
    ["SPI_MOSI", "SPI_MISO", "SPI_SCK", "SPI_CS_N"] +
    ["I2C_SCL", "I2C_SDA"] +
    ["UART_TX", "UART_RX"] +
    ["INT_N", "RST_N", "WAKE_OUT", "BOOT_SEL"] +
    [f"GPIO{i}" for i in range(0, 21)] +
    ["TEST0", "TEST1", "TEST2"]
)
assert len(ndp_labels) == 69, len(ndp_labels)

nd = []
nd.append(sym_header(
    "NDP120", "U",
    "Syntiant NDP120 neural decision processor (69-pin LGA) - PLACEHOLDER pin mapping",
    "https://www.syntiant.com/ndp120",
    "palpod-mic-array:NDP120_LGA69"))
nd.append(sym_open_unit("NDP120"))
body_w = 60.96
body_h = 96.52
nd.append(rectangle(-body_w/2, body_h/2, body_w/2, -body_h/2))
left = ndp_labels[:34]
right = ndp_labels[34:]
pitch = 2.54

def et_for(lbl):
    if lbl.startswith("VDD") or lbl == "GND":
        return "power_in"
    if lbl.endswith("_N") or lbl == "RST_N" or lbl == "INT_N":
        return "input"
    if lbl.startswith("PDM_DATA") or lbl == "I2S_SDIN" or lbl == "SPI_MOSI" or lbl == "UART_RX":
        return "input"
    if lbl.startswith("PDM_CLK") or lbl == "I2S_SDOUT" or lbl == "SPI_MISO" or lbl == "UART_TX" or lbl == "WAKE_OUT":
        return "output"
    if lbl.startswith("I2C_") or lbl.startswith("GPIO") or lbl.startswith("TEST"):
        return "bidirectional"
    if lbl == "MCLK" or lbl == "BOOT_SEL" or lbl == "SPI_SCK" or lbl == "I2S_BCLK" or lbl == "I2S_LRCLK":
        return "input"
    return "passive"

top_y = (len(left) - 1) * pitch / 2
for i, lbl in enumerate(left):
    y = top_y - i * pitch
    num = str(i + 1)
    nd.append(pin(et_for(lbl), "line", -body_w/2 - 2.54, y, 0, 2.54, lbl, num))
top_y = (len(right) - 1) * pitch / 2
for i, lbl in enumerate(right):
    y = top_y - i * pitch
    num = str(i + 35)
    nd.append(pin(et_for(lbl), "line", body_w/2 + 2.54, y, 180, 2.54, lbl, num))
nd.append(sym_close_unit())
nd.append(sym_close())

OUT.write_text(HEADER + "".join(ics) + "".join(xv) + "".join(nd) + FOOTER)
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")

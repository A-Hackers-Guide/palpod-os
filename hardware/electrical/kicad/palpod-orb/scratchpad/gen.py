#!/usr/bin/env python3
"""Generator for palpod-orb KiCad 8+ project.

Emits:
  libraries/palpod-orb.kicad_sym      — specialty symbols
  libraries/palpod-orb.pretty/*.kicad_mod — placeholder footprints
  palpod-orb.kicad_sch                 — schematic with embedded lib_symbols
  palpod-orb.kicad_pcb                 — 6-layer flex-rigid PCB with 2 rigid islands
"""
import os, uuid, hashlib, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # .../palpod-orb
LIB_DIR = ROOT / "libraries"
FP_DIR = LIB_DIR / "palpod-orb.pretty"
SCH = ROOT / "palpod-orb.kicad_sch"
PCB = ROOT / "palpod-orb.kicad_pcb"
SYM = LIB_DIR / "palpod-orb.kicad_sym"

# Deterministic UUIDs
_uuid_counter = [0]
def uid(seed=""):
    _uuid_counter[0] += 1
    h = hashlib.md5(f"palpod-orb-{seed}-{_uuid_counter[0]}".encode()).hexdigest()
    return f"{h[:8]}-{h[8:12]}-4{h[13:16]}-8{h[17:20]}-{h[20:32]}"

SHEET_UUID = "ceb7fa82-a753-46be-8eac-6e7118abde02"

# ==========================================================
# ============= Symbol library generator ===================
# ==========================================================

def sym_header():
    return '(kicad_symbol_lib\n\t(version 20231120)\n\t(generator "kicad_symbol_editor")\n'

def sym_footer():
    return ')\n'

def make_pin(kind, name, number, x, y, orient, length=2.54):
    """kind: input|output|bidirectional|passive|power_in|power_out|no_connect"""
    return (
        f'\t\t\t(pin {kind} line\n'
        f'\t\t\t\t(at {x} {y} {orient})\n'
        f'\t\t\t\t(length {length})\n'
        f'\t\t\t\t(name "{name}" (effects (font (size 1.27 1.27))))\n'
        f'\t\t\t\t(number "{number}" (effects (font (size 1.27 1.27))))\n'
        f'\t\t\t)\n'
    )

def make_symbol(sym_name, ref_prefix, value, footprint_lib, datasheet, description,
                width, height, pins_left, pins_right, pins_top=None, pins_bottom=None):
    """pins_* are lists of tuples (kind, name, number)."""
    pins_top = pins_top or []
    pins_bottom = pins_bottom or []
    hw, hh = width / 2, height / 2

    def _place(pins, axis_start, axis_end, side_x=None, side_y=None, orient=0):
        n = len(pins)
        out = []
        if n == 0:
            return out
        span = axis_end - axis_start
        step = span / (n + 1) if n > 1 else 0
        # snap-friendly integer 2.54 pitch
        pitch = 2.54
        needed = (n - 1) * pitch
        start = -needed / 2
        for i, (k, nm, num) in enumerate(pins):
            if side_x is not None:
                out.append(make_pin(k, nm, num, side_x, start + i * pitch, orient))
            else:
                out.append(make_pin(k, nm, num, start + i * pitch, side_y, orient))
        return out

    body = [
        f'\t(symbol "{sym_name}"\n',
        f'\t\t(pin_names (offset 1.016))\n',
        f'\t\t(exclude_from_sim no)(in_bom yes)(on_board yes)\n',
        f'\t\t(property "Reference" "{ref_prefix}" (at 0 {hh + 4} 0) (effects (font (size 1.27 1.27))))\n',
        f'\t\t(property "Value" "{value}" (at 0 {-(hh + 4)} 0) (effects (font (size 1.27 1.27))))\n',
        f'\t\t(property "Footprint" "palpod-orb:{footprint_lib}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n',
        f'\t\t(property "Datasheet" "{datasheet}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n',
        f'\t\t(property "Description" "{description}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n',
        f'\t\t(symbol "{sym_name}_1_1"\n',
        f'\t\t\t(rectangle (start {-hw} {hh}) (end {hw} {-hh}) (stroke (width 0.254) (type default)) (fill (type background)))\n',
    ]
    body += _place(pins_left, -hh, hh, side_x=-hw - 2.54, orient=0)
    body += _place(pins_right, -hh, hh, side_x=hw + 2.54, orient=180)
    body += _place(pins_top, -hw, hw, side_y=hh + 2.54, orient=270)
    body += _place(pins_bottom, -hw, hw, side_y=-hh - 2.54, orient=90)
    body.append('\t\t)\n\t)\n')
    return ''.join(body)


# Symbol definitions --------------------------------------------------
SPECIALTY_SYMBOLS = []

# nRF54H20 — dual Cortex-M33 + M0, 2.4 GHz radio.
# aQFN94 package. Grouped pin names; PLACEHOLDER.
nrf_left = (
    [("power_in", f"VDD_{i}", f"P{i}") for i in range(1, 7)] +
    [("power_in", f"VDDH_{i}", f"P{6+i}") for i in range(1, 4)] +
    [("power_in", f"VDDIO_{i}", f"P{9+i}") for i in range(1, 5)] +
    [("power_in", f"GND_{i}", f"P{13+i}") for i in range(1, 9)] +
    [("input", "XC1", "P22"), ("output", "XC2", "P23")] +
    [("input", "NRST", "P24"), ("input", "SWDIO", "P25"), ("input", "SWCLK", "P26")]
)
nrf_right = (
    [("bidirectional", f"P0.{i}", f"Q{i}") for i in range(0, 16)] +
    [("bidirectional", f"P1.{i}", f"Q{16+i}") for i in range(0, 16)] +
    [("bidirectional", "SDA", "Q32"), ("bidirectional", "SCL", "Q33")] +
    [("bidirectional", "SPI_MOSI", "Q34"), ("bidirectional", "SPI_MISO", "Q35"),
     ("bidirectional", "SPI_SCK", "Q36"), ("bidirectional", "SPI_CS", "Q37")]
)
nrf_top = [("no_connect", "ANT1", "R1"), ("no_connect", "ANT2", "R2")]
SPECIALTY_SYMBOLS.append(("nRF54H20",
    "U", "nRF54H20",
    "nRF54H20_aQFN94",
    "https://www.nordicsemi.com/Products/nRF54H20",
    "Nordic nRF54H20 multi-core Cortex-M33+M0 SoC with 2.4GHz radio (aQFN94) - PLACEHOLDER pin grouping, verify against datasheet",
    60, 130, nrf_left, nrf_right, nrf_top, []
))

# TC358748 — MIPI CSI-2 aggregator / parallel-to-CSI bridge (BGA80). PLACEHOLDER.
tc_left = (
    [("power_in", f"VDD_{i}", f"A{i}") for i in range(1, 5)] +
    [("power_in", f"VDDIO_{i}", f"A{4+i}") for i in range(1, 4)] +
    [("power_in", f"GND_{i}", f"A{7+i}") for i in range(1, 9)] +
    [("input", "REFCLK", "B1"), ("input", "RESET_N", "B2")] +
    [("bidirectional", "I2C_SCL", "B3"), ("bidirectional", "I2C_SDA", "B4")] +
    [("bidirectional", f"PAR_D{i}", f"C{i}") for i in range(0, 24)]
)
tc_right = (
    [("output", "CSI_D0_P", "D1"), ("output", "CSI_D0_N", "D2"),
     ("output", "CSI_D1_P", "D3"), ("output", "CSI_D1_N", "D4"),
     ("output", "CSI_D2_P", "D5"), ("output", "CSI_D2_N", "D6"),
     ("output", "CSI_D3_P", "D7"), ("output", "CSI_D3_N", "D8"),
     ("output", "CSI_CLK_P", "D9"), ("output", "CSI_CLK_N", "D10")] +
    [("input", f"CAM{c}_D0_P", f"E{c*4-3}") for c in range(1, 7)] +
    [("input", f"CAM{c}_D0_N", f"E{c*4-2}") for c in range(1, 7)] +
    [("input", f"CAM{c}_CLK_P", f"E{c*4-1}") for c in range(1, 7)] +
    [("input", f"CAM{c}_CLK_N", f"E{c*4}") for c in range(1, 7)]
)
SPECIALTY_SYMBOLS.append(("TC358748",
    "U", "TC358748",
    "TC358748_BGA80",
    "https://toshiba.semicon-storage.com/us/semiconductor/product/interface-bridge-ics-for-mobile-peripheral-devices.html",
    "Toshiba TC358748 MIPI CSI-2 bridge/aggregator (BGA80) - PLACEHOLDER pin map, verify against datasheet",
    60, 140, tc_left, tc_right, [], []
))

# SSD1963 — OLED display source-driver (LFBGA121). PLACEHOLDER.
ssd_left = (
    [("power_in", f"VDD_{i}", f"A{i}") for i in range(1, 5)] +
    [("power_in", f"VDDIO_{i}", f"A{4+i}") for i in range(1, 3)] +
    [("power_in", f"VOLED_{i}", f"A{6+i}") for i in range(1, 3)] +
    [("power_in", f"GND_{i}", f"A{8+i}") for i in range(1, 9)] +
    [("input", "XRESET", "B1"), ("input", "CS_N", "B2"),
     ("input", "RS_DC", "B3"), ("input", "WR_N", "B4"), ("input", "RD_N", "B5")] +
    [("bidirectional", f"DB{i}", f"C{i}") for i in range(0, 24)]
)
ssd_right = (
    [("output", f"SOURCE_{i}", f"S{i}") for i in range(1, 33)] +
    [("output", f"GATE_{i}", f"G{i}") for i in range(1, 9)]
)
SPECIALTY_SYMBOLS.append(("SSD1963_OLED",
    "U", "SSD1963",
    "SSD1963_LFBGA121",
    "https://www.solomon-systech.com/product/ssd1963/",
    "Solomon Systech SSD1963 curved-OLED source driver (LFBGA121) - PLACEHOLDER for proprietary custom-OLED driver; swap for real driver before fab",
    60, 160, ssd_left, ssd_right, [], []
))

# S3 LIDAR module UART connector (10-pin JST-SH pigtail on cable)
lidar_pins = [
    ("power_in", "VCC_5V", "1"),
    ("power_in", "GND", "2"),
    ("output", "UART_TX", "3"),
    ("input", "UART_RX", "4"),
    ("output", "MOTOR_PWM", "5"),
    ("output", "SYNC", "6"),
    ("bidirectional", "I2C_SCL", "7"),
    ("bidirectional", "I2C_SDA", "8"),
    ("no_connect", "NC1", "9"),
    ("no_connect", "NC2", "10"),
]
SPECIALTY_SYMBOLS.append(("Slamtec_S3",
    "J", "Slamtec_S3_LIDAR",
    "S3_LIDAR_UART10",
    "https://www.slamtec.com/en/S3",
    "Slamtec RPLIDAR S3 module cable connector (10-pin, UART+motor+sync) - PLACEHOLDER",
    30, 30, lidar_pins, [], [], []
))

# Renesas P9418 Qi RX (QFN40)
p9418_left = (
    [("power_in", f"VDD_{i}", f"P{i}") for i in range(1, 3)] +
    [("power_in", f"GND_{i}", f"P{2+i}") for i in range(1, 5)] +
    [("input", "COIL_AC1", "P7"), ("input", "COIL_AC2", "P8"),
     ("input", "CLAMP1", "P9"), ("input", "CLAMP2", "P10"),
     ("input", "BOOT1", "P11"), ("input", "BOOT2", "P12")] +
    [("power_out", "VRECT", "P13"), ("power_out", "VRECT", "P14"),
     ("power_out", "VOUT", "P15"), ("power_out", "VOUT", "P16")]
)
p9418_right = (
    [("bidirectional", "I2C_SCL", "P17"), ("bidirectional", "I2C_SDA", "P18"),
     ("input", "EN", "P19"), ("output", "PG_N", "P20"),
     ("output", "INT_N", "P21"), ("bidirectional", "COMM", "P22"),
     ("input", "MOD1", "P23"), ("input", "MOD2", "P24"),
     ("input", "AD_EN", "P25"), ("input", "FOD_CAL", "P26")] +
    [("input", f"NC_{i}", f"P{26+i}") for i in range(1, 15)]
)
SPECIALTY_SYMBOLS.append(("P9418",
    "U", "P9418",
    "P9418_QFN40",
    "https://www.renesas.com/us/en/products/power-power-management/wireless-power/p9418",
    "Renesas P9418 wireless-power RX (QFN40) - PLACEHOLDER pin map",
    60, 90, p9418_left, p9418_right, [], []
))

# TMR2305 magnetoresistive sensor (SOT-23-5)
tmr_pins = [
    ("power_in", "VCC", "1"),
    ("power_in", "GND", "2"),
    ("output", "VOUT", "3"),
    ("input", "SLEEP", "4"),
    ("output", "TEMP", "5"),
]
SPECIALTY_SYMBOLS.append(("TMR2305",
    "U", "TMR2305",
    "TMR2305_SOT23-5",
    "https://product.tdk.com/en/search/sensor/mre/",
    "TDK TMR2305 tunneling magnetoresistive sensor (SOT-23-5) - PLACEHOLDER",
    15, 15, tmr_pins, [], [], []
))

# VL53L8 ToF (LGA16)
vl_left = [
    ("power_in", "AVDD", "1"), ("power_in", "AVDDVCSEL", "2"),
    ("power_in", "GND1", "3"), ("power_in", "GND2", "4"),
    ("power_in", "VDDIO", "5"), ("input", "PWR_EN", "6"),
    ("input", "LPn", "7"), ("output", "INT", "8"),
]
vl_right = [
    ("bidirectional", "I2C_SCL", "9"), ("bidirectional", "I2C_SDA", "10"),
    ("bidirectional", "SPI_MOSI", "11"), ("bidirectional", "SPI_MISO", "12"),
    ("bidirectional", "SPI_SCK", "13"), ("bidirectional", "SPI_CS", "14"),
    ("input", "I2C_RST", "15"), ("input", "GPIO1", "16"),
]
SPECIALTY_SYMBOLS.append(("VL53L8",
    "U", "VL53L8",
    "VL53L8_LGA16",
    "https://www.st.com/en/imaging-and-photonics-solutions/vl53l8ca.html",
    "STMicro VL53L8 8x8 zone ToF sensor (LGA16) - PLACEHOLDER",
    25, 25, vl_left, vl_right, [], []
))

# IMX415 camera FPC28 connector (0.5 mm pitch, ZIF)
imx_pins = []
csi_map = {
    1: ("MIPI_D0_N", "input"), 2: ("MIPI_D0_P", "input"),
    3: ("GND", "power_in"),
    4: ("MIPI_D1_N", "input"), 5: ("MIPI_D1_P", "input"),
    6: ("GND", "power_in"),
    7: ("MIPI_D2_N", "input"), 8: ("MIPI_D2_P", "input"),
    9: ("GND", "power_in"),
    10: ("MIPI_D3_N", "input"), 11: ("MIPI_D3_P", "input"),
    12: ("GND", "power_in"),
    13: ("MIPI_CLK_N", "input"), 14: ("MIPI_CLK_P", "input"),
    15: ("GND", "power_in"),
    16: ("I2C_SCL", "bidirectional"), 17: ("I2C_SDA", "bidirectional"),
    18: ("GND", "power_in"),
    19: ("MCLK", "output"), 20: ("XVS", "input"),
    21: ("XHS", "input"), 22: ("RESET_N", "output"),
    23: ("PWR_EN", "output"),
    24: ("VDDA_2V8", "power_in"), 25: ("VDDIO_1V8", "power_in"),
    26: ("VDDD_1V2", "power_in"),
    27: ("GND", "power_in"), 28: ("SHIELD", "power_in"),
}
for i in range(1, 29):
    name, kind = csi_map[i]
    imx_pins.append((kind, f"{name}_{i}", str(i)))
SPECIALTY_SYMBOLS.append(("CAM_FPC28",
    "J", "IMX415_CAM_FPC28",
    "FPC28_0.5mm_ZIF",
    "https://www.sony-semicon.com/en/products/is/industry/imx415.html",
    "Sony IMX415 camera module 28-pin 0.5mm FPC connector (4-lane MIPI CSI-2 + I2C + power) - PLACEHOLDER",
    35, 90, imx_pins, [], [], []
))

# BQ25798 battery charger / BMS (QFN29)
bq_left = [
    ("power_in", "VBUS", "1"), ("power_in", "VBUS", "2"),
    ("power_in", "GND", "3"), ("power_in", "GND", "4"),
    ("input", "CE_N", "5"), ("input", "QON", "6"),
    ("input", "SDA", "7"), ("input", "SCL", "8"),
    ("output", "STAT", "9"), ("output", "INT", "10"),
    ("input", "ILIM", "11"), ("input", "PROG", "12"),
    ("input", "TS", "13"), ("input", "PSEL", "14"),
]
bq_right = [
    ("power_out", "SW1", "15"), ("power_out", "SW2", "16"),
    ("power_out", "SYS", "17"), ("power_out", "SYS", "18"),
    ("power_out", "BAT", "19"), ("power_out", "BAT", "20"),
    ("input", "MID", "21"), ("input", "VDRV", "22"),
    ("input", "BTST1", "23"), ("input", "BTST2", "24"),
    ("input", "REGN", "25"), ("input", "REGN", "26"),
    ("input", "PGND", "27"), ("input", "PGND", "28"),
    ("power_in", "TPAD", "29"),
]
SPECIALTY_SYMBOLS.append(("BQ25798",
    "U", "BQ25798",
    "BQ25798_QFN29",
    "https://www.ti.com/product/BQ25798",
    "TI BQ25798 buck-boost switching battery charger (QFN29) - PLACEHOLDER",
    45, 50, bq_left, bq_right, [], []
))

# M.2 2230 Wi-Fi socket, Key-A/E, 75 pins (Wi-Fi 7 FC7800)
# Placeholder: 4 key power pins + PCIe pair + USB pair + UART + GPIO
m2_left = (
    [("power_in", "GND", "2"), ("power_in", "GND", "4")] +
    [("power_in", "3V3_AUX", "6"), ("power_in", "3V3_AUX", "8")] +
    [("power_in", "3V3", "72"), ("power_in", "3V3", "74")] +
    [("bidirectional", "USB_D+", "10"), ("bidirectional", "USB_D-", "12")] +
    [("bidirectional", "SDIO_CLK", "14"), ("bidirectional", "SDIO_CMD", "16")] +
    [("bidirectional", "SDIO_D0", "18"), ("bidirectional", "SDIO_D1", "20"),
     ("bidirectional", "SDIO_D2", "22"), ("bidirectional", "SDIO_D3", "24")] +
    [("bidirectional", "UART_RX", "26"), ("bidirectional", "UART_TX", "28")] +
    [("input", "WAKE_N", "30"), ("output", "PERST_N", "32")] +
    [("output", "PCIE_TX_P", "34"), ("output", "PCIE_TX_N", "36")] +
    [("input", "PCIE_RX_P", "38"), ("input", "PCIE_RX_N", "40")] +
    [("input", "REFCLK_P", "42"), ("input", "REFCLK_N", "44")] +
    [("no_connect", f"NC_{i}", str(i)) for i in [46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70]]
)
m2_right = (
    [("power_in", "GND", "1"), ("power_in", "GND", "3")] +
    [("input", "CLKREQ_N", "5"), ("input", "W_DISABLE1_N", "7")] +
    [("input", "W_DISABLE2_N", "9"), ("input", "LED1_N", "11")] +
    [("no_connect", f"NC_R_{i}", str(i)) for i in [13, 15, 17, 19, 21, 23, 25, 27, 29, 31,
                                                     33, 35, 37, 39, 41, 43, 45, 47,
                                                     49, 51, 53, 55, 57, 59, 61, 63,
                                                     65, 67, 69, 71, 73, 75]]
)
SPECIALTY_SYMBOLS.append(("M2_2230_KeyAE",
    "J", "M.2 2230 Key A+E",
    "M2_2230_KeyAE",
    "https://en.wikipedia.org/wiki/M.2",
    "M.2 2230 Key A+E socket for Wi-Fi 7 module (e.g. QCA FC7800) - PLACEHOLDER 75-pin subset",
    50, 160, m2_left, m2_right, [], []
))

# OLED FPC40 out to curved panel
oled_pins = []
dsi_map = {
    1: ("VLED_ANODE", "power_out"), 2: ("VLED_CATHODE", "power_in"),
    3: ("GND", "power_in"),
    4: ("DSI_D0_N", "output"), 5: ("DSI_D0_P", "output"),
    6: ("GND", "power_in"),
    7: ("DSI_D1_N", "output"), 8: ("DSI_D1_P", "output"),
    9: ("GND", "power_in"),
    10: ("DSI_CLK_N", "output"), 11: ("DSI_CLK_P", "output"),
    12: ("GND", "power_in"),
    13: ("DSI_D2_N", "output"), 14: ("DSI_D2_P", "output"),
    15: ("GND", "power_in"),
    16: ("DSI_D3_N", "output"), 17: ("DSI_D3_P", "output"),
    18: ("GND", "power_in"),
    19: ("RESET_N", "output"), 20: ("TE", "input"),
    21: ("I2C_SCL", "bidirectional"), 22: ("I2C_SDA", "bidirectional"),
    23: ("INT_N", "input"),
    24: ("VDDI_1V8", "power_out"), 25: ("VDDA_3V0", "power_out"),
    26: ("VSP_5V5", "power_out"), 27: ("VSN_5V5", "power_out"),
    28: ("GND", "power_in"),
    29: ("TOUCH_INT", "input"), 30: ("TOUCH_RST", "output"),
    31: ("TOUCH_SCL", "bidirectional"), 32: ("TOUCH_SDA", "bidirectional"),
    33: ("GND", "power_in"),
    34: ("ID_DET", "input"), 35: ("BIST_EN", "output"),
    36: ("TP1", "no_connect"), 37: ("TP2", "no_connect"),
    38: ("GND", "power_in"),
    39: ("SHIELD_1", "power_in"), 40: ("SHIELD_2", "power_in"),
}
for i in range(1, 41):
    name, kind = dsi_map[i]
    oled_pins.append((kind, f"{name}_{i}", str(i)))
SPECIALTY_SYMBOLS.append(("OLED_FPC40",
    "J", "Curved_OLED_FPC40",
    "FPC40_0.5mm_ZIF",
    "https://www.lg-display.com/",
    "Curved OLED 40-pin 0.5mm FPC out to panel (MIPI DSI 4-lane + touch + power) - PLACEHOLDER",
    35, 120, oled_pins, [], [], []
))


def write_symbol_library():
    parts = [sym_header()]
    for (name, ref, val, fp, ds, desc, w, h, pl, pr, pt, pb) in SPECIALTY_SYMBOLS:
        parts.append(make_symbol(name, ref, val, fp, ds, desc, w, h, pl, pr, pt, pb))
    parts.append(sym_footer())
    SYM.write_text(''.join(parts))


# ==========================================================
# ============= Footprint generator ========================
# ==========================================================

FP_HEADER = """(footprint "{name}"
	(version 20240108)
	(generator "pcbnew")
	(generator_version "8.0")
	(layer "F.Cu")
	(descr "{descr}")
	(tags "{tags}")
	(property "Reference" "{ref}**"
		(at 0 {refy} 0)
		(layer "F.SilkS")
		(uuid "{u1}")
		(effects (font (size 1 1) (thickness 0.15))))
	(property "Value" "{name}"
		(at 0 {valy} 0)
		(layer "F.Fab")
		(uuid "{u2}")
		(effects (font (size 1 1) (thickness 0.15))))
	(property "Footprint" ""
		(at 0 0 0)
		(layer "F.Fab")
		(hide yes)
		(uuid "{u3}")
		(effects (font (size 1.27 1.27) (thickness 0.15))))
	(property "Datasheet" "{ds}"
		(at 0 0 0)
		(layer "F.Fab")
		(hide yes)
		(uuid "{u4}")
		(effects (font (size 1.27 1.27) (thickness 0.15))))
	(property "Description" "PLACEHOLDER - verify against datasheet before fab"
		(at 0 0 0)
		(layer "F.Fab")
		(hide yes)
		(uuid "{u5}")
		(effects (font (size 1.27 1.27) (thickness 0.15))))
	(attr smd)
"""

def fp_outline(hw, hh):
    silk_off = 0.1
    ct_off = 0.25
    parts = []
    for (x1, y1, x2, y2) in [
        (-hw, -hh, hw, -hh), (hw, -hh, hw, hh),
        (hw, hh, -hw, hh), (-hw, hh, -hw, -hh),
    ]:
        parts.append(f'  (fp_line (start {x1} {y1}) (end {x2} {y2}) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{uid("fabl")}"))\n')
    for (x1, y1, x2, y2) in [
        (-(hw+silk_off), -(hh+silk_off), (hw+silk_off), -(hh+silk_off)),
        ((hw+silk_off), -(hh+silk_off), (hw+silk_off), (hh+silk_off)),
        ((hw+silk_off), (hh+silk_off), -(hw+silk_off), (hh+silk_off)),
        (-(hw+silk_off), (hh+silk_off), -(hw+silk_off), -(hh+silk_off)),
    ]:
        parts.append(f'  (fp_line (start {x1} {y1}) (end {x2} {y2}) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{uid("silkl")}"))\n')
    for (x1, y1, x2, y2) in [
        (-(hw+ct_off), -(hh+ct_off), (hw+ct_off), -(hh+ct_off)),
        ((hw+ct_off), -(hh+ct_off), (hw+ct_off), (hh+ct_off)),
        ((hw+ct_off), (hh+ct_off), -(hw+ct_off), (hh+ct_off)),
        (-(hw+ct_off), (hh+ct_off), -(hw+ct_off), -(hh+ct_off)),
    ]:
        parts.append(f'  (fp_line (start {x1} {y1}) (end {x2} {y2}) (stroke (width 0.05) (type solid)) (layer "F.CrtYd") (uuid "{uid("ctl")}"))\n')
    parts.append(f'  (fp_circle (center {-(hw+0.4)} {-(hh+0.4)}) (end {-(hw+0.2)} {-(hh+0.4)}) (stroke (width 0.15) (type solid)) (fill solid) (layer "F.SilkS") (uuid "{uid("pin1")}"))\n')
    return ''.join(parts)

def fp_pad(num, x, y, w, h, shape="rect", drill=None):
    if drill:
        return f'  (pad "{num}" thru_hole {shape} (at {x} {y}) (size {w} {h}) (drill {drill}) (layers "*.Cu" "*.Mask") (uuid "{uid("pad")}"))\n'
    return f'  (pad "{num}" smd {shape} (at {x} {y}) (size {w} {h}) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{uid("pad")}"))\n'


def emit_footprint(path, name, descr, tags, ds, hw, hh, refy, valy, pads_body):
    u = [uid(f"fpprop{i}") for i in range(5)]
    body = FP_HEADER.format(
        name=name, descr=descr, tags=tags, ds=ds,
        ref="U", refy=-hh-1.5, valy=hh+1.5,
        u1=u[0], u2=u[1], u3=u[2], u4=u[3], u5=u[4]
    )
    body += fp_outline(hw, hh)
    body += pads_body
    body += ")\n"
    (FP_DIR / path).write_text(body)


def gen_bga_grid(rows, cols, pitch, pad_size, exclude=None):
    """Emit BGA pads on rows A..[rows], cols 1..cols. Origin centered."""
    exclude = exclude or set()
    letters = "ABCDEFGHJKLMNPRTUVWY"
    w = (cols - 1) * pitch
    h = (rows - 1) * pitch
    x0 = -w / 2
    y0 = -h / 2
    out = []
    pad_num = 1
    for r in range(rows):
        for c in range(cols):
            name = f"{letters[r]}{c+1}"
            if name in exclude:
                continue
            x = x0 + c * pitch
            y = y0 + r * pitch
            out.append(fp_pad(name, x, y, pad_size, pad_size, "circle"))
    return ''.join(out)


def gen_qfn(pin_count, pitch, pkg_size, pad_size=(0.3, 0.75)):
    """QFN perimeter pads, pin 1 at bottom-left."""
    per_side = pin_count // 4
    hw = pkg_size / 2
    out = []
    edge = hw - 0.1
    pw, pl = pad_size
    start = -((per_side - 1) * pitch) / 2
    n = 1
    # left side, bottom to top
    for i in range(per_side):
        y = start + i * pitch
        out.append(fp_pad(str(n), -edge, -y, pl, pw))
        n += 1
    # bottom side, left to right
    for i in range(per_side):
        x = start + i * pitch
        out.append(fp_pad(str(n), x, edge, pw, pl))
        n += 1
    # right side, top to bottom
    for i in range(per_side):
        y = start + i * pitch
        out.append(fp_pad(str(n), edge, y, pl, pw))
        n += 1
    # top side, right to left
    for i in range(per_side):
        x = start + i * pitch
        out.append(fp_pad(str(n), -x, -edge, pw, pl))
        n += 1
    return ''.join(out)


def gen_lga_perim(pin_count, pitch, pkg_size, pad_size=(0.3, 0.55)):
    """LGA perimeter pads. Assume divisible-by-4."""
    return gen_qfn(pin_count, pitch, pkg_size, pad_size)


def gen_sot23_5():
    out = []
    # SOT-23-5: pitch 0.95 on one side (3 pins), 1.9 gap on other (2 pins)
    # pins 1,2,3 on top, 4,5 on bottom
    p = 0.95
    y_top = -1.1
    y_bot = 1.1
    xs = [-p, 0.0, p]
    for i, x in enumerate(xs, 1):
        out.append(fp_pad(str(i), x, y_top, 0.6, 0.9))
    out.append(fp_pad("4", p, y_bot, 0.6, 0.9))
    out.append(fp_pad("5", -p, y_bot, 0.6, 0.9))
    return ''.join(out)


def gen_fpc_edge(pin_count, pitch, contact_len=1.0):
    """FPC ZIF connector: pins on bottom edge, single row."""
    w = (pin_count - 1) * pitch
    x0 = -w / 2
    out = []
    for i in range(pin_count):
        out.append(fp_pad(str(i+1), x0 + i * pitch, 3.5, 0.3, contact_len))
    # mounting tabs
    out.append(fp_pad("MP1", -(w/2 + 1.5), 3.0, 1.2, 1.6))
    out.append(fp_pad("MP2",  (w/2 + 1.5), 3.0, 1.2, 1.6))
    return ''.join(out)


def gen_m2_socket():
    """M.2 2230 Key A+E socket — dual row of edge pads on one end."""
    out = []
    pitch = 0.5
    # 75 pins on card edge (top row: odd numbers, bottom row: even)
    # Placeholder: 75 pads in one row along y=-6, plus 4 mounting/keying holes.
    total = 75
    w = (total - 1) * pitch
    x0 = -w / 2
    for i in range(total):
        out.append(fp_pad(str(i+1), x0 + i * pitch, -6.0, 0.3, 3.0))
    # Mounting screw hole (M.2 2230 has one at 30mm away)
    out.append(fp_pad("MTG", 0, 12.0, 2.6, 2.6, "circle", drill=1.7))
    return ''.join(out)


def write_footprints():
    # nRF54H20 aQFN94: 7x7 mm 0.4mm pitch, roughly emulate as QFN76 (approx)
    emit_footprint("nRF54H20_aQFN94.kicad_mod", "nRF54H20_aQFN94",
        "PLACEHOLDER Nordic nRF54H20 aQFN94 7x7mm 0.4mm pitch - VERIFY LAND PATTERN BEFORE FAB",
        "aQFN94 Nordic nRF54H20 PLACEHOLDER",
        "https://www.nordicsemi.com/Products/nRF54H20",
        3.5, 3.5, -4.5, 4.5,
        gen_qfn(76, 0.4, 6.8, (0.2, 0.6))
    )

    # TC358748 BGA80: ~5.6x5.6mm 0.5mm pitch, 10x10 - 20 depopulated
    excl = {"A1","A10","J1","J10"}  # corners
    emit_footprint("TC358748_BGA80.kicad_mod", "TC358748_BGA80",
        "PLACEHOLDER Toshiba TC358748 BGA80 approx 5.6x5.6mm 0.5mm pitch - VERIFY BEFORE FAB",
        "BGA80 MIPI bridge PLACEHOLDER",
        "https://toshiba.semicon-storage.com/",
        3.0, 3.0, -4.0, 4.0,
        gen_bga_grid(10, 10, 0.5, 0.28, exclude=excl)
    )

    # SSD1963 LFBGA121: 11x11mm 0.8mm pitch 12x12 - 23 depopulated (approx)
    emit_footprint("SSD1963_LFBGA121.kicad_mod", "SSD1963_LFBGA121",
        "PLACEHOLDER Solomon Systech SSD1963 LFBGA121 11x11mm 0.8mm pitch - VERIFY BEFORE FAB",
        "LFBGA121 OLED driver PLACEHOLDER",
        "https://www.solomon-systech.com/",
        5.6, 5.6, -6.5, 6.5,
        gen_bga_grid(12, 12, 0.8, 0.4)
    )

    # Slamtec S3 LIDAR: 10-pin 1.0mm JST-PH-like connector footprint
    lidar_pads = []
    for i in range(10):
        x = -4.5 + i * 1.0
        lidar_pads.append(fp_pad(str(i+1), x, 0, 0.7, 3.0, drill=1.0))
    emit_footprint("S3_LIDAR_UART10.kicad_mod", "S3_LIDAR_UART10",
        "PLACEHOLDER 10-pin 1.0mm pitch header for Slamtec S3 LIDAR cable - VERIFY",
        "connector 10-pin LIDAR PLACEHOLDER",
        "https://www.slamtec.com/en/S3",
        6, 4, -5, 5,
        ''.join(lidar_pads)
    )

    # P9418 QFN40: 6x6mm 0.5mm pitch
    emit_footprint("P9418_QFN40.kicad_mod", "P9418_QFN40",
        "PLACEHOLDER Renesas P9418 QFN40 6x6mm 0.5mm pitch - VERIFY BEFORE FAB",
        "QFN40 Qi RX PLACEHOLDER",
        "https://www.renesas.com/",
        3.0, 3.0, -4.0, 4.0,
        gen_qfn(40, 0.5, 5.8, (0.25, 0.7))
    )

    # TMR2305 SOT23-5
    emit_footprint("TMR2305_SOT23-5.kicad_mod", "TMR2305_SOT23-5",
        "PLACEHOLDER TDK TMR2305 SOT-23-5 2.9x1.6mm - VERIFY",
        "SOT-23-5 TMR sensor PLACEHOLDER",
        "https://product.tdk.com/",
        1.5, 1.5, -2.5, 2.5,
        gen_sot23_5()
    )

    # VL53L8 LGA16
    emit_footprint("VL53L8_LGA16.kicad_mod", "VL53L8_LGA16",
        "PLACEHOLDER ST VL53L8 LGA16 6.4x3.0mm - VERIFY",
        "LGA16 ToF PLACEHOLDER",
        "https://www.st.com/",
        3.2, 1.5, -2.5, 2.5,
        gen_lga_perim(16, 0.5, 5.5, (0.25, 0.5))
    )

    # FPC28 ZIF for cameras
    emit_footprint("FPC28_0.5mm_ZIF.kicad_mod", "FPC28_0.5mm_ZIF",
        "PLACEHOLDER 28-pin 0.5mm FPC ZIF connector for IMX415 camera cables - VERIFY",
        "FPC28 0.5mm connector PLACEHOLDER",
        "https://www.molex.com/",
        8.5, 3.0, -4.0, 4.0,
        gen_fpc_edge(28, 0.5)
    )

    # FPC40 for OLED
    emit_footprint("FPC40_0.5mm_ZIF.kicad_mod", "FPC40_0.5mm_ZIF",
        "PLACEHOLDER 40-pin 0.5mm FPC ZIF connector for curved OLED cable - VERIFY",
        "FPC40 0.5mm connector PLACEHOLDER",
        "https://www.molex.com/",
        11.5, 3.0, -4.0, 4.0,
        gen_fpc_edge(40, 0.5)
    )

    # BQ25798 QFN29
    emit_footprint("BQ25798_QFN29.kicad_mod", "BQ25798_QFN29",
        "PLACEHOLDER TI BQ25798 QFN29 4x4mm 0.4mm pitch - VERIFY",
        "QFN29 BMS charger PLACEHOLDER",
        "https://www.ti.com/product/BQ25798",
        2.0, 2.0, -3.0, 3.0,
        gen_qfn(28, 0.4, 3.8, (0.2, 0.55)) +
        fp_pad("29", 0, 0, 2.5, 2.5)  # thermal
    )

    # M.2 2230 Key A+E socket
    emit_footprint("M2_2230_KeyAE.kicad_mod", "M2_2230_KeyAE",
        "PLACEHOLDER M.2 2230 Key A+E socket 22x30mm - VERIFY against Amphenol/Molex M.2 socket datasheet",
        "M.2 2230 KeyAE socket PLACEHOLDER",
        "https://en.wikipedia.org/wiki/M.2",
        14, 15, -18, 18,
        gen_m2_socket()
    )


# ==========================================================
# ============= Schematic generator ========================
# ==========================================================

# Embedded lib_symbols we need: Device:R, Device:C, power:+5V,+3V3,+1V8,+1V2,+VBAT,GND
# Plus the specialty ones (referenced by lib_id palpod-orb:*).

# Standard symbol blobs (copied and simplified from the mic-array template)
STD_LIB_SYMBOLS = r'''		(symbol "Device:R"
			(pin_numbers (hide yes))
			(pin_names (offset 0) (hide yes))
			(exclude_from_sim no)(in_bom yes)(on_board yes)
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
			(exclude_from_sim no)(in_bom yes)(on_board yes)
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
			(exclude_from_sim no)(in_bom yes)(on_board yes)
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
		(symbol "Device:D_Schottky"
			(pin_names (offset 1.016) (hide yes))
			(exclude_from_sim no)(in_bom yes)(on_board yes)
			(property "Reference" "D" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "D_Schottky" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "D_Schottky_0_1"
				(polyline (pts (xy -1.27 1.27) (xy -1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
				(polyline (pts (xy 1.27 1.27) (xy 1.27 0) (xy -1.27 0) (xy 1.27 0) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
				(polyline (pts (xy -1.27 0) (xy 1.27 1.27) (xy 1.27 -1.27) (xy -1.27 0)) (stroke (width 0.254) (type default)) (fill (type outline)))
			)
			(symbol "D_Schottky_1_1"
				(pin passive line (at -3.81 0 0) (length 2.54) (name "K" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 3.81 0 180) (length 2.54) (name "A" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:+5V"
			(power)
			(pin_names (offset 0))
			(exclude_from_sim no)(in_bom yes)(on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "+5V" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "+5V_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27) (xy 0 0) (xy -0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "+5V_1_1"
				(pin power_in line (at 0 0 90) (length 0) hide (name "+5V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:+3V3"
			(power)(pin_names (offset 0))
			(exclude_from_sim no)(in_bom yes)(on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "+3V3" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "+3V3_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27) (xy 0 0) (xy -0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "+3V3_1_1"
				(pin power_in line (at 0 0 90) (length 0) hide (name "+3V3" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:+1V8"
			(power)(pin_names (offset 0))
			(exclude_from_sim no)(in_bom yes)(on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "+1V8" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "+1V8_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27) (xy 0 0) (xy -0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "+1V8_1_1"
				(pin power_in line (at 0 0 90) (length 0) hide (name "+1V8" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:+1V2"
			(power)(pin_names (offset 0))
			(exclude_from_sim no)(in_bom yes)(on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "+1V2" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "+1V2_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27) (xy 0 0) (xy -0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "+1V2_1_1"
				(pin power_in line (at 0 0 90) (length 0) hide (name "+1V2" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:+BATT"
			(power)(pin_names (offset 0))
			(exclude_from_sim no)(in_bom yes)(on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "+BATT" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "+BATT_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27) (xy 0 0) (xy -0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "+BATT_1_1"
				(pin power_in line (at 0 0 90) (length 0) hide (name "+BATT" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:VRECT"
			(power)(pin_names (offset 0))
			(exclude_from_sim no)(in_bom yes)(on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "VRECT" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "VRECT_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27) (xy 0 0) (xy -0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "VRECT_1_1"
				(pin power_in line (at 0 0 90) (length 0) hide (name "VRECT" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:GND"
			(power)(pin_names (offset 0))
			(exclude_from_sim no)(in_bom yes)(on_board yes)
			(property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "GND_0_1"
				(polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "GND_1_1"
				(pin power_in line (at 0 0 270) (length 0) hide (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
'''


def emb_specialty_lib_symbols():
    """Emit specialty symbols inside the schematic's lib_symbols block, using
       lib_id 'palpod-orb:<name>' — same content as the standalone library."""
    out = []
    for (name, ref, val, fp, ds, desc, w, h, pl, pr, pt, pb) in SPECIALTY_SYMBOLS:
        s = make_symbol(name, ref, val, fp, ds, desc, w, h, pl, pr, pt, pb)
        # Rename top-level symbol to "palpod-orb:<name>" (unit sub-symbol stays base-name_1_1)
        s = s.replace(f'(symbol "{name}"\n', f'(symbol "palpod-orb:{name}"\n', 1)
        out.append(s)
    return ''.join(out)


# Component placement
COMPONENTS = []       # list of dicts: lib_id, ref, val, footprint, x, y, uuid
POWER_SYMS = []       # power symbols
WIRES = []            # (x1,y1,x2,y2)
LABELS = []           # (text, x, y)
NO_CONNECTS = []      # (x,y)

def add_comp(lib_id, ref, val, fp, x, y, extra_props=None):
    COMPONENTS.append({
        "lib_id": lib_id, "ref": ref, "val": val, "fp": fp,
        "x": x, "y": y, "uuid": uid(f"comp-{ref}"),
        "extra": extra_props or {}
    })

def add_pwr(kind, x, y, ref_num):
    POWER_SYMS.append({"kind": kind, "x": x, "y": y, "ref": f"#PWR{ref_num:03d}", "uuid": uid(f"pwr-{ref_num}")})

# Layout — A2-size sheet region:  (KiCad uses mm, A3 = 420x297)
# We use A2 (594x420). Let's keep A3 for template consistency and spread across.

# ---- MAIN COMPUTE ISLAND ----
add_comp("palpod-orb:nRF54H20", "U1", "nRF54H20", "palpod-orb:nRF54H20_aQFN94", 100, 100)
add_comp("palpod-orb:TC358748", "U2", "TC358748", "palpod-orb:TC358748_BGA80", 220, 100)
add_comp("palpod-orb:VL53L8",   "U3", "VL53L8",   "palpod-orb:VL53L8_LGA16",    100, 200)
add_comp("palpod-orb:BQ25798",  "U4", "BQ25798",  "palpod-orb:BQ25798_QFN29",   40,  90)
add_comp("palpod-orb:P9418",    "U5", "P9418",    "palpod-orb:P9418_QFN40",     40,  180)
add_comp("palpod-orb:SSD1963_OLED", "U6", "SSD1963", "palpod-orb:SSD1963_LFBGA121", 340, 100)

# 6 cameras
for i, y in enumerate([30, 60, 90, 120, 150, 180]):
    add_comp("palpod-orb:CAM_FPC28", f"J{i+1}", f"IMX415_CAM{i+1}", "palpod-orb:FPC28_0.5mm_ZIF",
             290, y+30)

# LIDAR
add_comp("palpod-orb:Slamtec_S3", "J7", "S3_LIDAR", "palpod-orb:S3_LIDAR_UART10", 40, 250)
# M.2 Wi-Fi socket
add_comp("palpod-orb:M2_2230_KeyAE", "J8", "WiFi7_M2", "palpod-orb:M2_2230_KeyAE", 160, 250)
# OLED FPC
add_comp("palpod-orb:OLED_FPC40", "J9", "OLED_OUT", "palpod-orb:FPC40_0.5mm_ZIF", 380, 220)

# 4 TMR halbach sensors
for i, x in enumerate([210, 235, 260, 285]):
    add_comp("palpod-orb:TMR2305", f"U{7+i}", "TMR2305", "palpod-orb:TMR2305_SOT23-5",
             x, 280)

# Decoupling caps (12 illustrative)
for i in range(12):
    x = 30 + (i % 6) * 12
    y = 30 + (i // 6) * 10
    add_comp("Device:C", f"C{i+1}", "100nF", "Capacitor_SMD:C_0402_1005Metric", x, y)

# Bulk caps near LDO/BMS
for i in range(4):
    add_comp("Device:C", f"C{20+i}", "10uF", "Capacitor_SMD:C_0805_2012Metric", 30 + i*10, 130)

# Resistors (I2C pullups)
add_comp("Device:R", "R1", "4.7k", "Resistor_SMD:R_0402_1005Metric", 260, 55)
add_comp("Device:R", "R2", "4.7k", "Resistor_SMD:R_0402_1005Metric", 270, 55)

# Rectifier stage caps + Schottky bank
for i in range(4):
    add_comp("Device:D_Schottky", f"D{i+1}", "PMEG3020", "Diode_SMD:D_SOD-323", 20, 155 + i*8)

# Rectifier storage cap + boost inductor placeholder
add_comp("Device:C", "C24", "22uF", "Capacitor_SMD:C_1210_3225Metric", 20, 200)
add_comp("Device:L", "L1", "10uH", "Inductor_SMD:L_1210_3225Metric", 25, 220)

# Battery connector
add_comp("Device:C", "C25", "220uF", "Capacitor_SMD:C_1210_3225Metric", 55, 200)  # BATT bulk

# Power flags
add_pwr("+5V",   60, 20, 1)
add_pwr("+3V3",  100, 20, 2)
add_pwr("+1V8",  140, 20, 3)
add_pwr("+1V2",  180, 20, 4)
add_pwr("+BATT", 55, 190, 5)
add_pwr("VRECT", 20, 145, 6)
add_pwr("GND",   30, 40, 7)
add_pwr("GND",   90, 130, 8)
add_pwr("GND",   220, 170, 9)
add_pwr("GND",   340, 170, 10)
add_pwr("GND",   40, 285, 11)
add_pwr("GND",   160, 320, 12)

# Wires + labels
WIRES.extend([
    (60, 25, 60, 40),
    (100, 25, 100, 40),
    (140, 25, 140, 40),
    (180, 25, 180, 40),
    (55, 195, 55, 200),
    (20, 145, 20, 155),
    (260, 60, 270, 60),
])
LABELS.extend([
    ("+5V", 60, 27),
    ("+3V3", 100, 27),
    ("+1V8", 140, 27),
    ("+1V2", 180, 27),
    ("+BATT", 55, 197),
    ("VRECT", 20, 147),
    ("I2C_SCL", 260, 57),
    ("I2C_SDA", 270, 57),
    ("MIPI_CSI_TO_MCU", 220, 60),
    ("MIPI_DSI_TO_PANEL", 380, 195),
    ("WiFi7_UART_TO_MCU", 160, 245),
    ("LIDAR_UART_TO_MCU", 40, 245),
])

NO_CONNECTS.extend([(103, 40), (108, 40)])  # nRF ANT pins


def write_schematic():
    parts = []
    parts.append(f'(kicad_sch\n')
    parts.append(f'\t(version 20231120)\n\t(generator "eeschema")\n\t(generator_version "8.0")\n')
    parts.append(f'\t(uuid "{SHEET_UUID}")\n')
    parts.append(f'\t(paper "A2")\n')
    parts.append(f'\t(title_block\n')
    parts.append(f'\t\t(title "Hearth Orb")\n')
    parts.append(f'\t\t(date "2026-08-03")\n')
    parts.append(f'\t\t(rev "A0")\n')
    parts.append(f'\t\t(company "Hearth")\n')
    parts.append(f'\t\t(comment 1 "6-layer flex-rigid orb PCB: nRF54H20 + MIPI CSI-2 aggregator + 6 cameras + ToF + LIDAR + Wi-Fi 7 + Qi RX + Halbach TMR + BMS + curved OLED driver")\n')
    parts.append(f'\t\t(comment 2 "Two rigid islands connected by flex bridges. Layers: F.Cu / GND / PWR_3V3 / PWR_5V / GND / B.Cu")\n')
    parts.append(f'\t\t(comment 3 "Reference: hardware/electrical/block-diagrams/orb.md")\n')
    parts.append(f'\t\t(comment 4 "PLACEHOLDER schematic - EE to complete wiring, verify pin maps, run ERC")\n')
    parts.append(f'\t)\n')

    # lib_symbols
    parts.append('\t(lib_symbols\n')
    parts.append(STD_LIB_SYMBOLS)
    parts.append(emb_specialty_lib_symbols())
    parts.append('\t)\n')

    # Symbol instances
    for c in COMPONENTS:
        parts.append(f'\t(symbol\n')
        parts.append(f'\t\t(lib_id "{c["lib_id"]}")\n')
        parts.append(f'\t\t(at {c["x"]} {c["y"]} 0)\n')
        parts.append(f'\t\t(unit 1)\n')
        parts.append(f'\t\t(exclude_from_sim no)(in_bom yes)(on_board yes)(dnp no)\n')
        parts.append(f'\t\t(uuid "{c["uuid"]}")\n')
        parts.append(f'\t\t(property "Reference" "{c["ref"]}" (at {c["x"]+2.5} {c["y"]-5} 0) (effects (font (size 1.27 1.27))))\n')
        parts.append(f'\t\t(property "Value" "{c["val"]}" (at {c["x"]+2.5} {c["y"]+5} 0) (effects (font (size 1.27 1.27))))\n')
        parts.append(f'\t\t(property "Footprint" "{c["fp"]}" (at {c["x"]} {c["y"]} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        parts.append(f'\t\t(property "Datasheet" "~" (at {c["x"]} {c["y"]} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        parts.append(f'\t\t(instances\n')
        parts.append(f'\t\t\t(project "palpod-orb"\n')
        parts.append(f'\t\t\t\t(path "/{SHEET_UUID}" (reference "{c["ref"]}") (unit 1))\n')
        parts.append(f'\t\t\t)\n')
        parts.append(f'\t\t)\n')
        parts.append(f'\t)\n')

    # Power symbols
    for p in POWER_SYMS:
        parts.append(f'\t(symbol\n')
        parts.append(f'\t\t(lib_id "power:{p["kind"]}")\n')
        parts.append(f'\t\t(at {p["x"]} {p["y"]} 0)\n')
        parts.append(f'\t\t(unit 1)\n')
        parts.append(f'\t\t(exclude_from_sim no)(in_bom yes)(on_board yes)(dnp no)\n')
        parts.append(f'\t\t(uuid "{p["uuid"]}")\n')
        parts.append(f'\t\t(property "Reference" "{p["ref"]}" (at {p["x"]+2.54} {p["y"]-5} 0) (effects (font (size 1.27 1.27))))\n')
        parts.append(f'\t\t(property "Value" "{p["kind"]}" (at {p["x"]+2.54} {p["y"]+5} 0) (effects (font (size 1.27 1.27))))\n')
        parts.append(f'\t\t(property "Footprint" "" (at {p["x"]} {p["y"]} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        parts.append(f'\t\t(property "Datasheet" "~" (at {p["x"]} {p["y"]} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        parts.append(f'\t\t(instances\n')
        parts.append(f'\t\t\t(project "palpod-orb"\n')
        parts.append(f'\t\t\t\t(path "/{SHEET_UUID}" (reference "{p["ref"]}") (unit 1))\n')
        parts.append(f'\t\t\t)\n')
        parts.append(f'\t\t)\n')
        parts.append(f'\t)\n')

    for (x1, y1, x2, y2) in WIRES:
        parts.append(f'\t(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{uid("w")}"))\n')

    for (txt, x, y) in LABELS:
        parts.append(f'\t(label "{txt}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{uid("l")}"))\n')

    for (x, y) in NO_CONNECTS:
        parts.append(f'\t(no_connect (at {x} {y}) (uuid "{uid("nc")}"))\n')

    parts.append('\t(sheet_instances\n\t\t(path "/" (page "1"))\n\t)\n')
    parts.append(')\n')
    SCH.write_text(''.join(parts))


# ==========================================================
# ============= PCB generator =============================
# ==========================================================

def write_pcb():
    """6-layer flex-rigid PCB: two rigid island outlines on Edge.Cuts,
       silkscreen callout for flex bridge zone."""
    nets = [
        (0, ""), (1, "+5V"), (2, "+3V3"), (3, "+1V8"), (4, "+1V2"),
        (5, "+BATT"), (6, "VRECT"), (7, "GND"),
        (8, "I2C_SCL"), (9, "I2C_SDA"),
        (10, "MIPI_CSI_D0_P"), (11, "MIPI_CSI_D0_N"),
        (12, "MIPI_CSI_D1_P"), (13, "MIPI_CSI_D1_N"),
        (14, "MIPI_CSI_D2_P"), (15, "MIPI_CSI_D2_N"),
        (16, "MIPI_CSI_D3_P"), (17, "MIPI_CSI_D3_N"),
        (18, "MIPI_CSI_CLK_P"), (19, "MIPI_CSI_CLK_N"),
        (20, "DSI_D0_P"), (21, "DSI_D0_N"),
        (22, "DSI_D1_P"), (23, "DSI_D1_N"),
        (24, "DSI_D2_P"), (25, "DSI_D2_N"),
        (26, "DSI_D3_P"), (27, "DSI_D3_N"),
        (28, "DSI_CLK_P"), (29, "DSI_CLK_N"),
        (30, "COIL_AC1"), (31, "COIL_AC2"),
        (32, "ANT_WIFI"), (33, "UART_TX"), (34, "UART_RX"),
        (35, "NRST"), (36, "SWDIO"), (37, "SWCLK"),
    ]
    parts = ['(kicad_pcb\n']
    parts.append('  (version 20240108)\n  (generator "pcbnew")\n  (generator_version "8.0")\n')
    parts.append('  (general\n    (thickness 1.05)\n    (legacy_teardrops no)\n  )\n')
    parts.append('  (paper "A2")\n')
    parts.append('  (title_block\n')
    parts.append('    (title "Hearth Orb - PCB (Flex-Rigid 6-Layer)")\n')
    parts.append('    (date "2026-08-03")\n')
    parts.append('    (rev "A0")\n')
    parts.append('    (company "Hearth")\n')
    parts.append('    (comment 1 "6-layer flex-rigid: F.Cu / GND / PWR_3V3 / PWR_5V / GND / B.Cu")\n')
    parts.append('    (comment 2 "Rigid: 1oz Cu on FR4. Flex: 0.5oz Cu on polyimide. ENIG.")\n')
    parts.append('    (comment 3 "See hardware/electrical/block-diagrams/orb.md")\n')
    parts.append('  )\n')

    # Layers
    parts.append('  (layers\n')
    parts.append('    (0 "F.Cu" signal)\n')
    parts.append('    (1 "In1.Cu" power "GND1")\n')
    parts.append('    (2 "In2.Cu" power "PWR_3V3")\n')
    parts.append('    (3 "In3.Cu" power "PWR_5V")\n')
    parts.append('    (4 "In4.Cu" power "GND2")\n')
    parts.append('    (31 "B.Cu" signal)\n')
    for L, name, kind in [
        (32, "B.Adhes", "user"), (33, "F.Adhes", "user"),
        (34, "B.Paste", "user"), (35, "F.Paste", "user"),
        (36, "B.SilkS", "user"), (37, "F.SilkS", "user"),
        (38, "B.Mask", "user"), (39, "F.Mask", "user"),
        (40, "Dwgs.User", "user"), (41, "Cmts.User", "user"),
        (42, "Eco1.User", "user"), (43, "Eco2.User", "user"),
        (44, "Edge.Cuts", "user"), (45, "Margin", "user"),
        (46, "B.CrtYd", "user"), (47, "F.CrtYd", "user"),
        (48, "B.Fab", "user"), (49, "F.Fab", "user"),
        (50, "User.1", "user"), (51, "User.2", "user"),
        (52, "User.3", "user"), (53, "User.4", "user"),
        (54, "User.5", "user"), (55, "User.6", "user"),
        (56, "User.7", "user"), (57, "User.8", "user"),
        (58, "User.9", "user"),
    ]:
        parts.append(f'    ({L} "{name}" {kind})\n')
    parts.append('  )\n')

    # 6-layer flex-rigid stackup: 3x rigid dielectric + polyimide flex core call-out
    parts.append('  (setup\n')
    parts.append('    (stackup\n')
    parts.append('      (layer "F.SilkS" (type "Top Silk Screen"))\n')
    parts.append('      (layer "F.Paste" (type "Top Solder Paste"))\n')
    parts.append('      (layer "F.Mask" (type "Top Solder Mask") (color "Green") (thickness 0.01))\n')
    parts.append('      (layer "F.Cu" (type "copper") (thickness 0.035))\n')
    parts.append('      (layer "dielectric 1" (type "prepreg") (thickness 0.076) (material "FR4/Adhesive") (epsilon_r 4.2) (loss_tangent 0.02))\n')
    parts.append('      (layer "In1.Cu" (type "copper") (thickness 0.0175))\n')
    parts.append('      (layer "dielectric 2" (type "core") (thickness 0.05) (material "Polyimide (flex core)") (epsilon_r 3.4) (loss_tangent 0.003))\n')
    parts.append('      (layer "In2.Cu" (type "copper") (thickness 0.0175))\n')
    parts.append('      (layer "dielectric 3" (type "prepreg") (thickness 0.1) (material "FR4/No-flow") (epsilon_r 4.2) (loss_tangent 0.02))\n')
    parts.append('      (layer "In3.Cu" (type "copper") (thickness 0.0175))\n')
    parts.append('      (layer "dielectric 4" (type "core") (thickness 0.05) (material "Polyimide (flex core)") (epsilon_r 3.4) (loss_tangent 0.003))\n')
    parts.append('      (layer "In4.Cu" (type "copper") (thickness 0.0175))\n')
    parts.append('      (layer "dielectric 5" (type "prepreg") (thickness 0.076) (material "FR4/Adhesive") (epsilon_r 4.2) (loss_tangent 0.02))\n')
    parts.append('      (layer "B.Cu" (type "copper") (thickness 0.035))\n')
    parts.append('      (layer "B.Mask" (type "Bottom Solder Mask") (color "Green") (thickness 0.01))\n')
    parts.append('      (layer "B.Paste" (type "Bottom Solder Paste"))\n')
    parts.append('      (layer "B.SilkS" (type "Bottom Silk Screen"))\n')
    parts.append('      (copper_finish "ENIG")\n')
    parts.append('      (dielectric_constraints yes)\n')
    parts.append('      (edge_connector no)\n')
    parts.append('      (castellated_pads no)\n')
    parts.append('      (edge_plating no)\n')
    parts.append('    )\n')
    parts.append('    (pad_to_mask_clearance 0)\n')
    parts.append('    (allow_soldermask_bridges_in_footprints no)\n')
    parts.append('    (pcbplotparams\n')
    parts.append('      (layerselection 0x00000000_00000000_55555555_5755f5ff)\n')
    parts.append('      (plot_on_all_layers_selection 0x00000000_00000000_00000000_00000000)\n')
    parts.append('      (disableapertmacros no)(usegerberextensions no)(usegerberattributes yes)(usegerberadvancedattributes yes)(creategerberjobfile yes)\n')
    parts.append('      (dashed_line_dash_ratio 12.000000)(dashed_line_gap_ratio 3.000000)(svgprecision 4)\n')
    parts.append('      (plotframeref no)(viasonmask no)(mode 1)(useauxorigin no)\n')
    parts.append('      (hpglpennumber 1)(hpglpenspeed 20)(hpglpendiameter 15.000000)\n')
    parts.append('      (pdf_front_fp_property_popups yes)(pdf_back_fp_property_popups yes)\n')
    parts.append('      (dxfpolygonmode yes)(dxfimperialunits yes)(dxfusepcbnewfont yes)\n')
    parts.append('      (psnegative no)(psa4output no)(plotreference yes)(plotvalue yes)(plotfptext yes)\n')
    parts.append('      (plotinvisibletext no)(sketchpadsonfab no)(subtractmaskfromsilk no)\n')
    parts.append('      (outputformat 1)(mirror no)(drillshape 1)(scaleselection 1)(outputdirectory "gerbers/")\n')
    parts.append('    )\n')
    parts.append('  )\n')

    for (i, name) in nets:
        parts.append(f'  (net {i} "{name}")\n')

    # === Edge.Cuts: two rigid islands + flex bridges outline ===
    # Rigid 1 (main IC island): 40x40mm centered at (0,0)
    def add_line(x1, y1, x2, y2, layer, width=0.1):
        return (f'  (gr_line (start {x1} {y1}) (end {x2} {y2}) '
                f'(stroke (width {width}) (type solid)) (layer "{layer}") '
                f'(uuid "{uid("line")}"))\n')

    # Single closed contour: rigid1 (40x40 at origin) + flex bridge 1 + rigid2 (30x20)
    # Trace clockwise from (-20,-20).
    outline = [
        (-20, -20, 20, -20),      # rigid1 bottom
        (20, -20, 20, -7.5),      # rigid1 right (below flex1)
        (20, -7.5, 55, -7.5),     # flex1 bottom
        (55, -7.5, 55, -10),      # rigid2 left stub down
        (55, -10, 85, -10),       # rigid2 bottom
        (85, -10, 85, 10),        # rigid2 right
        (85, 10, 55, 10),         # rigid2 top
        (55, 10, 55, 7.5),        # rigid2 left stub up
        (55, 7.5, 20, 7.5),       # flex1 top
        (20, 7.5, 20, 20),        # rigid1 right (above flex1)
        (20, 20, -20, 20),        # rigid1 top
        (-20, 20, -20, -20),      # rigid1 left
    ]
    for (x1, y1, x2, y2) in outline:
        parts.append(add_line(x1, y1, x2, y2, "Edge.Cuts", 0.15))

    # Flex bridge 2 (return/spare) documented on Dwgs.User only — not in board outline
    parts.append(add_line(-20, -30, 85, -30, "Dwgs.User", 0.1))
    parts.append(add_line(-20, -32, 85, -32, "Dwgs.User", 0.1))
    parts.append(add_line(-20, -30, -20, -32, "Dwgs.User", 0.1))
    parts.append(add_line(85, -30, 85, -32, "Dwgs.User", 0.1))

    # Flex-zone annotation on Dwgs.User over the flex bridge (documentation layer)
    parts.append(add_line(20, -7.5, 20, 7.5, "Dwgs.User", 0.15))
    parts.append(add_line(55, -7.5, 55, 7.5, "Dwgs.User", 0.15))

    # Silkscreen callouts
    def add_text(txt, x, y, layer, size=2.0, thickness=0.3):
        return (f'  (gr_text "{txt}" (at {x} {y} 0) (layer "{layer}") '
                f'(uuid "{uid("txt")}") '
                f'(effects (font (size {size} {size}) (thickness {thickness})) (justify left bottom)))\n')

    parts.append(add_text("Hearth Orb - Rev A0", -17, -12, "F.SilkS", 1.5, 0.2))
    parts.append(add_text("Rigid1: nRF54H20 + MIPI aggregator", -17, -9, "F.SilkS", 0.9, 0.12))
    parts.append(add_text("Rigid2: SSD1963", 58, -6, "F.SilkS", 0.9, 0.12))
    parts.append(add_text("FLEX SECTION - 0.5oz Cu polyimide", 22, -4, "F.SilkS", 0.9, 0.15))
    parts.append(add_text("Return-flex bridge (documentation only)", -18, -33, "Dwgs.User", 1.0, 0.15))
    parts.append(add_text("6L flex-rigid: F.Cu / GND / PWR_3V3 / PWR_5V / GND / B.Cu. See stackup and orb.md.",
                          -18, 25, "Cmts.User", 1.2, 0.15))
    parts.append(add_text("Fab must support flex-rigid (recommend PCBWay Advanced, MicroConnex, Flex Interconnect)",
                          -18, 28, "Cmts.User", 1.0, 0.15))

    parts.append(')\n')
    PCB.write_text(''.join(parts))


# ==========================================================
# Main
# ==========================================================
if __name__ == "__main__":
    FP_DIR.mkdir(parents=True, exist_ok=True)
    write_symbol_library()
    write_footprints()
    write_schematic()
    write_pcb()
    print("Generated:")
    print(f"  {SYM}")
    print(f"  {FP_DIR}/*.kicad_mod")
    print(f"  {SCH}")
    print(f"  {PCB}")

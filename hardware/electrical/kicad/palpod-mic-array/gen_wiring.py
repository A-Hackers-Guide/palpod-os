#!/usr/bin/env python3
"""Generate wire + label records for palpod-mic-array.kicad_sch.

For each placed symbol, we know its world (px, py) and rotation (all rot=0 here).
Pin world coordinates: (px + lx, py - ly)   (Y-flip since KiCad schematic Y goes down)

Strategy: attach a `label` at each pin world coordinate. KiCad's connectivity
extractor treats a label at a pin endpoint as electrically joining the pin to
the labeled net. For safety we also add a tiny 2.54mm stub wire from the pin
outward so that the pin ↔ label junction is unambiguous.

We do NOT modify existing wires/labels or any placed symbol.
"""

import uuid
import sys
from pathlib import Path

SCH = Path("/private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/electrical/kicad/palpod-mic-array/palpod-mic-array.kicad_sch")

# -----------------------------------------------------------------------------
# Placed-symbol registry.
# Each entry: refdes -> (px, py, {pin_number: (local_x, local_y, pin_angle_deg)})
# pin_angle: 0=right, 90=up, 180=left, 270=down (KiCad symbol space)
# The pin's endpoint (connection point) is at local (lx, ly).
# -----------------------------------------------------------------------------

# ---- LDOs (AP2114H-3.3 / Regulator_Linear symbol) ---------------------------
LDO_PINS = {
    "3": (-7.62, 2.54, 0),    # VI
    "2": (7.62, 2.54, 180),   # VO
    "1": (0.0, -6.35, 90),    # GND
}

# ---- ICS-41352 mic ----------------------------------------------------------
MIC_PINS = {
    "3": (-10.16, 2.54, 0),    # CLK
    "4": (-10.16, 0.0, 0),     # DATA
    "5": (-10.16, -2.54, 0),   # SELECT
    "1": (10.16, 2.54, 180),   # VDD
    "2": (10.16, -2.54, 180),  # GND
}

# ---- 100nF and 10uF caps (Device:C) -----------------------------------------
CAP_PINS = {
    "1": (0.0, 3.81, 270),   # top pin
    "2": (0.0, -3.81, 90),   # bottom pin
}

# ---- USB-C Receptacle Connector:USB_C_Receptacle_USB2.0_16P -----------------
USBC_PINS = {
    "A4":  (-12.7, 15.24, 0),   "B4":  (-12.7, 12.7, 0),
    "A6":  (-12.7, 7.62, 0),    "A7":  (-12.7, 5.08, 0),
    "B6":  (-12.7, 2.54, 0),    "B7":  (-12.7, 0.0, 0),
    "A5":  (-12.7, -5.08, 0),   "B5":  (-12.7, -7.62, 0),
    "A8":  (-12.7, -10.16, 0),  "B8":  (-12.7, -12.7, 0),
    "A1":  (12.7, 15.24, 180),  "A12": (12.7, 12.7, 180),
    "B1":  (12.7, 10.16, 180),  "B12": (12.7, 7.62, 180),
    "S1":  (12.7, 2.54, 180),   "S2":  (12.7, 0.0, 180),
}

# ---- USB3320C ---------------------------------------------------------------
USB3320_PINS = {
    "13": (-12.7, 15.24, 0),   # VDD33
    "27": (-12.7, 12.7, 0),    # VDD18
    "33": (-12.7, 10.16, 0),   # GND
    "20": (-12.7, 5.08, 0),    # DP
    "19": (-12.7, 2.54, 0),    # DM
    "22": (-12.7, 0.0, 0),     # ID
    "23": (-12.7, -2.54, 0),   # VBUS
    "3":  (12.7, 15.24, 180),  # DATA0
    "4":  (12.7, 12.7, 180),   # DATA1
    "5":  (12.7, 10.16, 180),  # DATA2
    "6":  (12.7, 7.62, 180),   # DATA3
    "7":  (12.7, 5.08, 180),   # DATA4
    "10": (12.7, 2.54, 180),   # DATA5
    "11": (12.7, 0.0, 180),    # DATA6
    "12": (12.7, -2.54, 180),  # DATA7
    "1":  (12.7, -7.62, 180),  # CLK
    "8":  (12.7, -10.16, 180), # DIR
    "9":  (12.7, -12.7, 180),  # NXT
    "2":  (12.7, -15.24, 180), # STP
}

# ---- STM32G474RETx (placeholder symbol - subset of pins) --------------------
STM32_PINS = {
    "5":  (-22.86, 35.56, 0),   # VDD
    "13": (-22.86, 33.02, 0),   # VDDA
    "8":  (-22.86, 30.48, 0),   # VSS
    "12": (-22.86, 27.94, 0),   # VSSA
    "7":  (-22.86, 22.86, 0),   # NRST
    "60": (-22.86, 20.32, 0),   # BOOT0
    "3":  (-22.86, 17.78, 0),   # OSC_IN
    "4":  (-22.86, 15.24, 0),   # OSC_OUT
    "14": (22.86, 35.56, 180),  # PA0
    "15": (22.86, 33.02, 180),  # PA1
    "16": (22.86, 30.48, 180),  # PA2/USART2_TX
    "17": (22.86, 27.94, 180),  # PA3/USART2_RX
    "41": (22.86, 25.4, 180),   # PA8/USB_ULPI_D0
    "42": (22.86, 22.86, 180),  # PA9/USB_ULPI_D1
    "46": (22.86, 20.32, 180),  # PA13/SWDIO
    "49": (22.86, 17.78, 180),  # PA14/SWCLK
    "58": (22.86, 15.24, 180),  # PB6/I2C1_SCL
    "59": (22.86, 12.7, 180),   # PB7/I2C1_SDA
}

# ---- XVF3800 ----------------------------------------------------------------
# Left-side pins (angle 0)
XVF_PINS = {}
_left_pins = [
    ("A1", 36.83, "VDD_CORE"), ("A2", 34.29, "VDD_CORE"),
    ("A3", 31.75, "VDD_CORE"), ("A4", 29.21, "VDD_CORE"),
    ("A5", 26.67, "VDD_CORE"), ("A6", 24.13, "VDD_CORE"),
    ("A7", 21.59, "VDDIO"),
    ("B1", 19.05, "VDDIO"), ("B2", 16.51, "VDDIO"),
    ("B3", 13.97, "VDDIO"), ("B4", 11.43, "VDDIO"),
    ("B5", 8.89, "VDDIO"),
    ("B6", 6.35, "GND"), ("B7", 3.81, "GND"), ("B8", 1.27, "GND"),
    ("C1", -1.27, "GND"), ("C2", -3.81, "GND"), ("C3", -6.35, "GND"),
    ("C4", -8.89, "GND"), ("C5", -11.43, "GND"), ("C6", -13.97, "GND"),
    ("C7", -16.51, "GND"),
    ("C8", -19.05, "MCLK_IN"),
    ("D1", -21.59, "MCLK_OUT"),
    ("D2", -24.13, "PLL_FILT"),
    ("D3", -26.67, "PDM_DATA0"),
    ("D4", -29.21, "PDM_DATA1"),
    ("D5", -31.75, "PDM_DATA2"),
    ("D6", -34.29, "PDM_DATA3"),
    ("D7", -36.83, "PDM_DATA4"),
]
for num, ly, name in _left_pins:
    XVF_PINS[num] = (-33.02, ly, 0, name)

_right_pins = [
    ("D8", 38.1, "PDM_DATA5"),
    ("E1", 35.56, "PDM_DATA6"),
    ("E2", 33.02, "PDM_DATA7"),
    ("E3", 30.48, "PDM_CLK0"),
    ("E4", 27.94, "PDM_CLK1"),
    ("E5", 25.4, "I2S_BCLK"),
    ("E6", 22.86, "I2S_LRCLK"),
    ("E7", 20.32, "I2S_SDOUT"),
    ("E8", 17.78, "I2S_SDIN"),
    ("F1", 15.24, "I2C_SCL"),
    ("F2", 12.7, "I2C_SDA"),
    ("F3", 10.16, "USB_DP"),
    ("F4", 7.62, "USB_DN"),
    ("F5", 5.08, "USB_VBUS"),
    ("F6", 2.54, "USB_ID"),
    ("F7", 0.0, "RST_N"),
    ("F8", -2.54, "BOOT_SEL"),
    ("G1", -5.08, "DEBUG_SEL"),
    ("G2", -7.62, "XLINK_A0"),
    ("G3", -10.16, "XLINK_A1"),
    ("G4", -12.7, "XLINK_B0"),
    ("G5", -15.24, "XLINK_B1"),
    ("G6", -17.78, "GPIO0"),
    ("G7", -20.32, "GPIO1"),
    ("G8", -22.86, "GPIO2"),
    ("H2", -25.4, "GPIO3"),
    ("H3", -27.94, "GPIO4"),
    ("H4", -30.48, "GPIO5"),
    ("H5", -33.02, "GPIO6"),
    ("H6", -35.56, "GPIO7"),
    ("H7", -38.1, "GPIO8"),
]
for num, ly, name in _right_pins:
    XVF_PINS[num] = (33.02, ly, 180, name)

# ---- NDP120 ----------------------------------------------------------------
NDP_PINS = {}
_ndp_left = [
    ("1", 41.91, "VDD_CORE"), ("2", 39.37, "VDD_CORE"),
    ("3", 36.83, "VDD_CORE"), ("4", 34.29, "VDD_CORE"),
    ("5", 31.75, "VDD_IO"), ("6", 29.21, "VDD_IO"),
    ("7", 26.67, "VDD_IO"), ("8", 24.13, "VDD_IO"),
    ("9", 21.59, "VDD_ANA"), ("10", 19.05, "VDD_ANA"),
    ("11", 16.51, "GND"), ("12", 13.97, "GND"),
    ("13", 11.43, "GND"), ("14", 8.89, "GND"),
    ("15", 6.35, "GND"), ("16", 3.81, "GND"),
    ("17", 1.27, "GND"), ("18", -1.27, "GND"),
    ("19", -3.81, "GND"), ("20", -6.35, "GND"),
    ("21", -8.89, "GND"), ("22", -11.43, "GND"),
    ("23", -13.97, "MCLK"),
    ("24", -16.51, "PLL_FILT"),
    ("25", -19.05, "PDM_DATA0"),
    ("26", -21.59, "PDM_DATA1"),
    ("27", -24.13, "PDM_DATA2"),
    ("28", -26.67, "PDM_DATA3"),
    ("29", -29.21, "PDM_CLK"),
    ("30", -31.75, "I2S_BCLK"),
    ("31", -34.29, "I2S_LRCLK"),
    ("32", -36.83, "I2S_SDIN"),
    ("33", -39.37, "I2S_SDOUT"),
    ("34", -41.91, "SPI_MOSI"),
]
for num, ly, name in _ndp_left:
    NDP_PINS[num] = (-33.02, ly, 0, name)

_ndp_right = [
    ("35", 43.18, "SPI_MISO"),
    ("36", 40.64, "SPI_SCK"),
    ("37", 38.1, "SPI_CS_N"),
    ("38", 35.56, "I2C_SCL"),
    ("39", 33.02, "I2C_SDA"),
    ("40", 30.48, "UART_TX"),
    ("41", 27.94, "UART_RX"),
    ("42", 25.4, "INT_N"),
    ("43", 22.86, "RST_N"),
    ("44", 20.32, "WAKE_OUT"),
    ("45", 17.78, "BOOT_SEL"),
]
for num, ly, name in _ndp_right:
    NDP_PINS[num] = (33.02, ly, 180, name)

# GPIO0..GPIO20 pins 46..66
_gpio_ys = [15.24, 12.7, 10.16, 7.62, 5.08, 2.54, 0.0, -2.54, -5.08, -7.62,
            -10.16, -12.7, -15.24, -17.78, -20.32, -22.86, -25.4, -27.94,
            -30.48, -33.02, -35.56]
for i, ly in enumerate(_gpio_ys):
    NDP_PINS[str(46 + i)] = (33.02, ly, 180, f"GPIO{i}")
NDP_PINS["67"] = (33.02, -38.1, 180, "TEST0")
NDP_PINS["68"] = (33.02, -40.64, 180, "TEST1")
NDP_PINS["69"] = (33.02, -43.18, 180, "TEST2")


# -----------------------------------------------------------------------------
# Placement table: refdes -> (world_px, world_py, pin_map)
# -----------------------------------------------------------------------------
PLACEMENTS = {
    # LDOs
    "U5": (60.0, 70.0, LDO_PINS),
    "U6": (100.0, 70.0, LDO_PINS),
    "U7": (140.0, 70.0, LDO_PINS),
    # Bulk caps
    "C1": (45.0, 90.0, CAP_PINS),
    "C2": (75.0, 90.0, CAP_PINS),
    "C3": (85.0, 90.0, CAP_PINS),
    "C4": (115.0, 90.0, CAP_PINS),
    "C5": (125.0, 90.0, CAP_PINS),
    "C6": (155.0, 90.0, CAP_PINS),
    # USB-C, USB3320, STM32
    "J1": (40.0, 180.0, USBC_PINS),
    "U3": (90.0, 180.0, USB3320_PINS),
    "U4": (155.0, 175.0, STM32_PINS),
    # XVF3800, NDP120
    "U1": (220.0, 145.0, {k: (lx, ly, ang) for k, (lx, ly, ang, _n) in XVF_PINS.items()}),
    "U2": (290.0, 145.0, {k: (lx, ly, ang) for k, (lx, ly, ang, _n) in NDP_PINS.items()}),
    # Mics
    "M1":  (185.00, 100.00, MIC_PINS),
    "M2":  (168.06, 135.18, MIC_PINS),
    "M3":  (129.99, 143.87, MIC_PINS),
    "M4":  (99.46,  119.52, MIC_PINS),
    "M5":  (99.46,  80.48,  MIC_PINS),
    "M6":  (129.99, 56.13,  MIC_PINS),
    "M7":  (168.06, 64.82,  MIC_PINS),
    "M8":  (161.65, 112.5,  MIC_PINS),
    "M9":  (140.0,  125.0,  MIC_PINS),
    "M10": (118.35, 112.5,  MIC_PINS),
    "M11": (118.35, 87.5,   MIC_PINS),
    "M12": (140.0,  75.0,   MIC_PINS),
    "M13": (161.65, 87.5,   MIC_PINS),
    # 100nF decap caps
    "C10": (210.0, 205.0, CAP_PINS),
    "C11": (220.0, 205.0, CAP_PINS),
    "C12": (230.0, 205.0, CAP_PINS),
    "C13": (280.0, 205.0, CAP_PINS),
    "C14": (290.0, 205.0, CAP_PINS),
    "C15": (300.0, 205.0, CAP_PINS),
}


def pin_world(refdes, pin_number):
    """Return (world_x, world_y, pin_angle) for a pin on a placed symbol.
    All symbols in this schematic are placed at rotation 0, so:
        world_x = px + lx
        world_y = py - ly
    Pin angle in world = symbol_pin_angle (no rotation).
    """
    px, py, pin_map = PLACEMENTS[refdes]
    lx, ly, ang = pin_map[pin_number]
    return (round(px + lx, 4), round(py - ly, 4), ang)


# -----------------------------------------------------------------------------
# Connection list: (refdes, pin_number, net_name)
# -----------------------------------------------------------------------------
CONNECTIONS = []

# --- Power tree: LDO connections ---
# U5: +5V in, +3V3 out (LDO_5V_TO_3V3)
CONNECTIONS += [
    ("U5", "3", "+5V"), ("U5", "2", "+3V3"), ("U5", "1", "GND"),
    ("U6", "3", "+5V"), ("U6", "2", "+1V8"), ("U6", "1", "GND"),
    ("U7", "3", "+5V"), ("U7", "2", "+1V0"), ("U7", "1", "GND"),
]

# --- Bulk caps at LDO input/output ---
CONNECTIONS += [
    ("C1", "1", "+5V"),  ("C1", "2", "GND"),
    ("C2", "1", "+3V3"), ("C2", "2", "GND"),
    ("C3", "1", "+5V"),  ("C3", "2", "GND"),
    ("C4", "1", "+1V8"), ("C4", "2", "GND"),
    ("C5", "1", "+5V"),  ("C5", "2", "GND"),
    ("C6", "1", "+1V0"), ("C6", "2", "GND"),
]

# --- 100nF decap caps near XVF3800 (C10-C12) and NDP120 (C13-C15) ---
CONNECTIONS += [
    ("C10", "1", "+1V8"), ("C10", "2", "GND"),  # XVF3800 VDD_CORE
    ("C11", "1", "+3V3"), ("C11", "2", "GND"),  # XVF3800 VDDIO
    ("C12", "1", "+1V8"), ("C12", "2", "GND"),  # XVF3800 VDD_CORE
    ("C13", "1", "+1V0"), ("C13", "2", "GND"),  # NDP120 VDD_CORE
    ("C14", "1", "+3V3"), ("C14", "2", "GND"),  # NDP120 VDD_IO
    ("C15", "1", "+3V3"), ("C15", "2", "GND"),  # NDP120 VDD_ANA
]

# --- USB-C receptacle J1 ---
CONNECTIONS += [
    ("J1", "A4", "+5V"), ("J1", "B4", "+5V"),      # VBUS
    ("J1", "A6", "USB_DP"), ("J1", "B6", "USB_DP"),
    ("J1", "A7", "USB_DN"), ("J1", "B7", "USB_DN"),
    ("J1", "A5", "CC1"), ("J1", "B5", "CC2"),
    ("J1", "A8", "SBU1"), ("J1", "B8", "SBU2"),
    ("J1", "A1", "GND"), ("J1", "A12", "GND"),
    ("J1", "B1", "GND"), ("J1", "B12", "GND"),
    ("J1", "S1", "GND"), ("J1", "S2", "GND"),
]

# --- USB3320C U3 ---
CONNECTIONS += [
    ("U3", "13", "+3V3"),   ("U3", "27", "+1V8"),   ("U3", "33", "GND"),
    ("U3", "20", "USB_DP"), ("U3", "19", "USB_DN"),
    ("U3", "22", "USB_ID"), ("U3", "23", "+5V"),
    ("U3", "3",  "ULPI_D0"), ("U3", "4",  "ULPI_D1"),
    ("U3", "5",  "ULPI_D2"), ("U3", "6",  "ULPI_D3"),
    ("U3", "7",  "ULPI_D4"), ("U3", "10", "ULPI_D5"),
    ("U3", "11", "ULPI_D6"), ("U3", "12", "ULPI_D7"),
    ("U3", "1",  "ULPI_CLK"), ("U3", "8",  "ULPI_DIR"),
    ("U3", "9",  "ULPI_NXT"), ("U3", "2",  "ULPI_STP"),
]

# --- STM32G474 U4 ---
CONNECTIONS += [
    ("U4", "5",  "+3V3"), ("U4", "13", "+3V3"),
    ("U4", "8",  "GND"),  ("U4", "12", "GND"),
    ("U4", "7",  "NRST"), ("U4", "60", "BOOT0"),
    # PA0/PA1 tied to NDP CS + INT
    ("U4", "14", "SPI_CS_NDP"),
    ("U4", "15", "NDP_INT"),
    # PA8/PA9 = ULPI_D0/D1
    ("U4", "41", "ULPI_D0"), ("U4", "42", "ULPI_D1"),
    # PA13/PA14 = SWD
    ("U4", "46", "SWDIO"), ("U4", "49", "SWCLK"),
    # PB6/PB7 = I2C
    ("U4", "58", "I2C_SCL"), ("U4", "59", "I2C_SDA"),
    # PA2/PA3 = USART for STM32 debug console
    ("U4", "16", "STM32_UART_TX"), ("U4", "17", "STM32_UART_RX"),
]

# --- XVF3800 U1 ---
# Power pins
for pn, (_, _, _, name) in XVF_PINS.items():
    if name == "VDD_CORE":
        CONNECTIONS.append(("U1", pn, "+1V8"))
    elif name == "VDDIO":
        CONNECTIONS.append(("U1", pn, "+3V3"))
    elif name == "GND":
        CONNECTIONS.append(("U1", pn, "GND"))
# Signal pins
CONNECTIONS += [
    ("U1", "C8", "XVF_MCLK_IN"),
    ("U1", "D1", "XVF_MCLK_OUT"),
    ("U1", "D2", "XVF_PLL_FILT"),
    ("U1", "D3", "PDM_DATA_0"),
    ("U1", "D4", "PDM_DATA_1"),
    ("U1", "D5", "PDM_DATA_2"),
    ("U1", "D6", "PDM_DATA_3"),
    ("U1", "D7", "PDM_DATA_4"),
    ("U1", "D8", "PDM_DATA_5"),
    ("U1", "E1", "PDM_DATA_6"),
    ("U1", "E2", "PDM_DATA_7"),
    ("U1", "E3", "PDM_CLK"),   # PDM_CLK0 - main master clock
    ("U1", "E4", "PDM_CLK"),   # PDM_CLK1 - tied to same clock
    ("U1", "E5", "I2S_BCK"),
    ("U1", "E6", "I2S_LRCK"),
    ("U1", "E7", "I2S_SDIN"),  # XVF I2S_SDOUT -> NDP I2S_SDIN
    ("U1", "E8", "XVF_I2S_SDIN"),  # unused input
    ("U1", "F1", "I2C_SCL"),
    ("U1", "F2", "I2C_SDA"),
    ("U1", "F3", "XVF_USB_DP"),  # XVF's own USB - unused (using STM32+USB3320)
    ("U1", "F4", "XVF_USB_DN"),
    ("U1", "F5", "+5V"),
    ("U1", "F6", "XVF_USB_ID"),
    ("U1", "F7", "XVF_RST_N"),
    ("U1", "F8", "XVF_BOOT_SEL"),
    ("U1", "G1", "XVF_DEBUG_SEL"),
    ("U1", "G2", "XVF_XLINK_A0"),
    ("U1", "G3", "XVF_XLINK_A1"),
    ("U1", "G4", "XVF_XLINK_B0"),
    ("U1", "G5", "XVF_XLINK_B1"),
    ("U1", "G6", "XVF_GPIO0"),
    ("U1", "G7", "XVF_GPIO1"),
    ("U1", "G8", "XVF_GPIO2"),
    ("U1", "H2", "XVF_GPIO3"),
    ("U1", "H3", "XVF_GPIO4"),
    ("U1", "H4", "XVF_GPIO5"),
    ("U1", "H5", "XVF_GPIO6"),
    ("U1", "H6", "XVF_GPIO7"),
    ("U1", "H7", "XVF_GPIO8"),
]

# --- NDP120 U2 ---
for pn, (_, _, _, name) in NDP_PINS.items():
    if name == "VDD_CORE":
        CONNECTIONS.append(("U2", pn, "+1V0"))
    elif name == "VDD_IO":
        CONNECTIONS.append(("U2", pn, "+3V3"))
    elif name == "VDD_ANA":
        CONNECTIONS.append(("U2", pn, "+3V3"))
    elif name == "GND":
        CONNECTIONS.append(("U2", pn, "GND"))

CONNECTIONS += [
    ("U2", "23", "NDP_MCLK"),
    ("U2", "24", "NDP_PLL_FILT"),
    ("U2", "25", "NDP_PDM_DATA0"),
    ("U2", "26", "NDP_PDM_DATA1"),
    ("U2", "27", "NDP_PDM_DATA2"),
    ("U2", "28", "NDP_PDM_DATA3"),
    ("U2", "29", "NDP_PDM_CLK"),
    ("U2", "30", "I2S_BCK"),
    ("U2", "31", "I2S_LRCK"),
    ("U2", "32", "I2S_SDIN"),
    ("U2", "33", "NDP_I2S_SDOUT"),
    ("U2", "34", "SPI_MOSI"),
    ("U2", "35", "SPI_MISO"),
    ("U2", "36", "SPI_SCK"),
    ("U2", "37", "SPI_CS_NDP"),
    ("U2", "38", "I2C_SCL"),
    ("U2", "39", "I2C_SDA"),
    ("U2", "40", "NDP_UART_TX"),
    ("U2", "41", "NDP_UART_RX"),
    ("U2", "42", "NDP_INT"),
    ("U2", "43", "NDP_RST"),
    ("U2", "44", "NDP_WAKE"),
    ("U2", "45", "GND"),  # BOOT_SEL tied low
]
# NDP120 unused GPIO pins - just label them
for i in range(21):
    CONNECTIONS.append(("U2", str(46 + i), f"NDP_GPIO{i}"))
# TEST pins 67-69 already have (no_connect) records elsewhere; skip label placement.

# --- 13 mics: PDM connections ---
# Each mic gets its own PDM_DATA_n line. SELECT alternates GND/+3V3.
# Mic 0-6 -> PDM_DATA_0..6 (outer ring), Mic 7-12 -> PDM_DATA_7..12
mic_refs = ["M1", "M2", "M3", "M4", "M5", "M6", "M7",   # outer 0..6
            "M8", "M9", "M10", "M11", "M12", "M13"]      # inner + center 7..12
for i, m in enumerate(mic_refs):
    CONNECTIONS += [
        (m, "3", "PDM_CLK"),
        (m, "4", f"PDM_DATA_{i}"),
        (m, "5", "GND" if i % 2 == 0 else "+3V3"),
        (m, "1", "+3V3"),   # VDD (mic array VDD is +3V3 per prompt)
        (m, "2", "GND"),
    ]


# -----------------------------------------------------------------------------
# Generate label and stub-wire records
# -----------------------------------------------------------------------------
def gen_uuid():
    return str(uuid.uuid4())


# For each pin, place a short 2.54mm stub wire outward from the pin, then place
# a label at the far end of the stub. The stub direction depends on pin angle:
#   pin_angle 0    -> pin faces right (out of body); stub goes LEFT (-x)
#   pin_angle 180  -> pin faces left  (out of body); stub goes RIGHT (+x)
#   pin_angle 90   -> pin faces up;    stub goes UP (-y in screen)
#   pin_angle 270  -> pin faces down;  stub goes DOWN (+y in screen)
# The stub-wire endpoint is on the pin's exposed side.
# Note: KiCad snaps to a 1.27mm grid; use multiples of 1.27.

STUB = 2.54

def stub_end(px, py, ang):
    if ang == 0:      return (px - STUB, py)
    if ang == 180:    return (px + STUB, py)
    if ang == 90:     return (px, py - STUB)
    if ang == 270:    return (px, py + STUB)
    raise ValueError(f"Unknown pin angle {ang}")


records = []
seen_pin_positions = set()   # (refdes, pin) already emitted

# Track (net -> list of endpoint positions) so we skip nothing.
for refdes, pin, net in CONNECTIONS:
    key = (refdes, pin)
    if key in seen_pin_positions:
        continue
    seen_pin_positions.add(key)

    try:
        pin_x, pin_y, pin_ang = pin_world(refdes, pin)
    except KeyError as e:
        print(f"WARNING: unknown symbol/pin {refdes}/{pin}: {e}", file=sys.stderr)
        continue

    end_x, end_y = stub_end(pin_x, pin_y, pin_ang)

    # Stub wire from pin endpoint to stub end.
    records.append(
        f'\t(wire\n'
        f'\t\t(pts (xy {pin_x} {pin_y}) (xy {end_x} {end_y}))\n'
        f'\t\t(stroke (width 0) (type default))\n'
        f'\t\t(uuid "{gen_uuid()}")\n'
        f'\t)'
    )

    # Label anchored at stub-end.
    # For power/GND rails use local label. For everything else too.
    label_ang = 0 if pin_ang == 180 else 180 if pin_ang == 0 else 0
    records.append(
        f'\t(label "{net}"\n'
        f'\t\t(at {end_x} {end_y} {label_ang})\n'
        f'\t\t(effects (font (size 1.27 1.27)) (justify left bottom))\n'
        f'\t\t(uuid "{gen_uuid()}")\n'
        f'\t)'
    )


# -----------------------------------------------------------------------------
# Splice into the schematic file just before the sheet_instances / final ")"
# -----------------------------------------------------------------------------
src = SCH.read_text()
marker = "\t(sheet_instances"
idx = src.index(marker)
new_block = "\n".join(records) + "\n"
new_src = src[:idx] + new_block + src[idx:]
SCH.write_text(new_src)

# Report counts
num_wires  = sum(1 for r in records if r.lstrip().startswith("(wire"))
num_labels = sum(1 for r in records if r.lstrip().startswith("(label"))
print(f"Added {num_wires} wires, {num_labels} labels ({len(CONNECTIONS)} connections)")

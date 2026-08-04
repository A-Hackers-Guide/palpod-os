#!/usr/bin/env python3
"""Generate the palpod-compute-backplane KiCad 8 project.

Emits:
  ../palpod-compute-backplane.kicad_pro
  ../palpod-compute-backplane.kicad_sch
  ../palpod-compute-backplane.kicad_pcb
  ../sym-lib-table
  ../fp-lib-table
  ../libraries/palpod-compute-backplane.kicad_sym
  ../libraries/palpod-compute-backplane.pretty/*.kicad_mod

Runs against KiCad 8/9/10 file schemas (sch=20231120, pcb=20240108,
sym=20231120, fp=20240108).
"""
import os
import json
import uuid as _uuid
import random
from pathlib import Path

random.seed(0xBACC1AB1)  # deterministic UUIDs

ROOT = Path(__file__).resolve().parent.parent
LIB_DIR = ROOT / "libraries"
FP_DIR = LIB_DIR / "palpod-compute-backplane.pretty"
PROJECT = "palpod-compute-backplane"
ROOT_SHEET_UUID = "b90c001d-1c0a-4c0a-9c0a-1234567890ab"


def uid():
    return str(_uuid.UUID(int=random.getrandbits(128), version=4))


# ---------------------------------------------------------------------------
# Symbol library (.kicad_sym)
# ---------------------------------------------------------------------------

def sym_property(name, value, x, y, hidden=False, size=1.27):
    hide = "\n\t\t\t\t(hide yes)" if hidden else ""
    return (
        f"\t\t(property \"{name}\" \"{value}\"\n"
        f"\t\t\t(at {x} {y} 0)\n"
        f"\t\t\t(effects\n"
        f"\t\t\t\t(font (size {size} {size})){hide}\n"
        f"\t\t\t)\n"
        f"\t\t)\n"
    )


def sym_pin(ptype, x, y, angle, name, number, length=2.54):
    return (
        f"\t\t\t(pin {ptype} line\n"
        f"\t\t\t\t(at {x} {y} {angle})\n"
        f"\t\t\t\t(length {length})\n"
        f"\t\t\t\t(name \"{name}\"\n"
        f"\t\t\t\t\t(effects (font (size 1.27 1.27)))\n"
        f"\t\t\t\t)\n"
        f"\t\t\t\t(number \"{number}\"\n"
        f"\t\t\t\t\t(effects (font (size 1.27 1.27)))\n"
        f"\t\t\t\t)\n"
        f"\t\t\t)\n"
    )


def build_symbol(name, description, footprint, datasheet, width, height, pins):
    """pins: list of (side, index_in_side, count_on_side, ptype, pname, pnumber).
    We compute (x, y) automatically. side in {L, R, T, B}. Pins evenly spaced.
    """
    hw = width / 2.0
    hh = height / 2.0
    out = f"\t(symbol \"{name}\"\n"
    out += "\t\t(pin_names\n\t\t\t(offset 1.016)\n\t\t)\n"
    out += "\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n"
    out += sym_property("Reference", "U", 0, hh + 2.54)
    out += sym_property("Value", name, 0, -hh - 2.54)
    out += sym_property("Footprint", footprint, 0, 0, hidden=True)
    out += sym_property("Datasheet", datasheet, 0, 0, hidden=True)
    out += sym_property("Description", description, 0, 0, hidden=True)
    out += f"\t\t(symbol \"{name}_1_1\"\n"
    out += (
        f"\t\t\t(rectangle\n"
        f"\t\t\t\t(start {-hw} {hh})\n"
        f"\t\t\t\t(end {hw} {-hh})\n"
        f"\t\t\t\t(stroke (width 0.254) (type default))\n"
        f"\t\t\t\t(fill (type background))\n"
        f"\t\t\t)\n"
    )
    # Group pins by side and layout
    sides = {"L": [], "R": [], "T": [], "B": []}
    for p in pins:
        sides[p[0]].append(p)
    for side, plist in sides.items():
        n = len(plist)
        if n == 0:
            continue
        if side in ("L", "R"):
            # spread over height
            step = max(2.54, (height - 5.08) / max(1, n - 1) if n > 1 else 0)
            for i, (_, ptype, pname, pnum) in enumerate([(p[0], p[1], p[2], p[3]) for p in plist]):
                y = hh - 2.54 - i * step
                if side == "L":
                    x = -hw - 2.54
                    a = 0
                else:
                    x = hw + 2.54
                    a = 180
                out += sym_pin(ptype, round(x, 3), round(y, 3), a, pname, pnum)
        else:
            step = max(2.54, (width - 5.08) / max(1, n - 1) if n > 1 else 0)
            for i, (_, ptype, pname, pnum) in enumerate([(p[0], p[1], p[2], p[3]) for p in plist]):
                x = -hw + 2.54 + i * step
                if side == "T":
                    y = hh + 2.54
                    a = 270
                else:
                    y = -hh - 2.54
                    a = 90
                out += sym_pin(ptype, round(x, 3), round(y, 3), a, pname, pnum)
    out += "\t\t)\n"
    out += "\t)\n"
    return out


# ---- MM70_SODIMM_260: Jetson Orin NX carrier (JAE MM70-260B1-R1) --------
def mm70_pins():
    """260-pin SODIMM on left+right (130 per side). Names abbreviated as groups."""
    pins = []
    # 130 pins per side. Sprinkle a handful of named power/high-speed lanes.
    named = {
        1: ("power_in", "GND"),
        2: ("power_in", "GND"),
        3: ("bidirectional", "USB0_DP"),
        4: ("bidirectional", "USB0_DN"),
        5: ("bidirectional", "USB1_DP"),
        6: ("bidirectional", "USB1_DN"),
        7: ("bidirectional", "PEX0_TX0_P"),
        8: ("bidirectional", "PEX0_TX0_N"),
        9: ("bidirectional", "PEX0_RX0_P"),
        10: ("bidirectional", "PEX0_RX0_N"),
        11: ("bidirectional", "PEX0_TX1_P"),
        12: ("bidirectional", "PEX0_TX1_N"),
        13: ("bidirectional", "PEX0_RX1_P"),
        14: ("bidirectional", "PEX0_RX1_N"),
        15: ("bidirectional", "PEX0_CLK_P"),
        16: ("bidirectional", "PEX0_CLK_N"),
        17: ("output", "PEX0_RST_L"),
        18: ("input", "PEX0_WAKE_L"),
        19: ("bidirectional", "I2C_GP0_SCL"),
        20: ("bidirectional", "I2C_GP0_SDA"),
        21: ("bidirectional", "UART0_TXD"),
        22: ("bidirectional", "UART0_RXD"),
        23: ("bidirectional", "SPI0_MOSI"),
        24: ("bidirectional", "SPI0_MISO"),
        25: ("bidirectional", "SPI0_SCK"),
        26: ("output", "SPI0_CS0_L"),
        27: ("bidirectional", "MGBE0_TX_P"),
        28: ("bidirectional", "MGBE0_TX_N"),
        29: ("bidirectional", "MGBE0_RX_P"),
        30: ("bidirectional", "MGBE0_RX_N"),
        31: ("input", "MOD_SLEEP_L"),
        32: ("output", "MOD_ALIVE"),
        33: ("power_in", "VDD_IN"),
        34: ("power_in", "VDD_IN"),
        35: ("power_in", "VDD_IN"),
        36: ("power_in", "VDD_IN"),
        129: ("power_in", "GND"),
        130: ("power_in", "GND"),
        131: ("power_in", "VDD_IN"),
        132: ("power_in", "VDD_IN"),
        133: ("power_in", "VDD_IN"),
        134: ("power_in", "VDD_IN"),
        135: ("power_in", "GND"),
        136: ("power_in", "GND"),
        137: ("bidirectional", "HDMI_TX0_P"),
        138: ("bidirectional", "HDMI_TX0_N"),
        139: ("bidirectional", "HDMI_TX1_P"),
        140: ("bidirectional", "HDMI_TX1_N"),
        141: ("bidirectional", "HDMI_TX2_P"),
        142: ("bidirectional", "HDMI_TX2_N"),
        143: ("bidirectional", "HDMI_TXC_P"),
        144: ("bidirectional", "HDMI_TXC_N"),
        145: ("bidirectional", "DP0_TX0_P"),
        146: ("bidirectional", "DP0_TX0_N"),
        147: ("bidirectional", "DP0_TX1_P"),
        148: ("bidirectional", "DP0_TX1_N"),
        149: ("bidirectional", "DP0_TX2_P"),
        150: ("bidirectional", "DP0_TX2_N"),
        151: ("bidirectional", "DP0_TX3_P"),
        152: ("bidirectional", "DP0_TX3_N"),
        153: ("bidirectional", "CSI0_D0_P"),
        154: ("bidirectional", "CSI0_D0_N"),
        155: ("bidirectional", "CSI0_D1_P"),
        156: ("bidirectional", "CSI0_D1_N"),
        157: ("bidirectional", "CSI0_CLK_P"),
        158: ("bidirectional", "CSI0_CLK_N"),
        159: ("output", "SYS_RESET_L"),
        160: ("output", "POWER_EN"),
        259: ("power_in", "GND"),
        260: ("power_in", "GND"),
    }
    # side L = pins 1..130, side R = 131..260
    for n in range(1, 131):
        ptype, name = named.get(n, ("bidirectional", f"NC{n}"))
        pins.append(("L", ptype, name, str(n)))
    for n in range(131, 261):
        ptype, name = named.get(n, ("bidirectional", f"NC{n}"))
        pins.append(("R", ptype, name, str(n)))
    return pins


# ---- ExaMAX_200: Samtec ExaMAX 56Gbps mezzanine ------------------------
def examax_pins():
    """200-pin high-speed mezzanine (Samtec ExaMAX ExaMEZZ style).
    Names: PCIe Gen5 x8 + 100GbE x4 + power + control.
    """
    pins = []
    named = {}
    # PCIe Gen5 lanes 0-7 (TX/RX diff pairs) -> 32 pins
    for lane in range(8):
        base = 1 + lane * 4
        named[base] = ("bidirectional", f"PCIE_G5_TX{lane}_P")
        named[base + 1] = ("bidirectional", f"PCIE_G5_TX{lane}_N")
        named[base + 2] = ("bidirectional", f"PCIE_G5_RX{lane}_P")
        named[base + 3] = ("bidirectional", f"PCIE_G5_RX{lane}_N")
    # PCIe REFCLK
    named[33] = ("input", "PCIE_REFCLK_P")
    named[34] = ("input", "PCIE_REFCLK_N")
    named[35] = ("output", "PCIE_PERST_L")
    named[36] = ("input", "PCIE_WAKE_L")
    # 100GbE lanes (4x25G NRZ or 2x50G PAM4) -> 16 pins
    for lane in range(4):
        base = 41 + lane * 4
        named[base] = ("bidirectional", f"ETH_TX{lane}_P")
        named[base + 1] = ("bidirectional", f"ETH_TX{lane}_N")
        named[base + 2] = ("bidirectional", f"ETH_RX{lane}_P")
        named[base + 3] = ("bidirectional", f"ETH_RX{lane}_N")
    # Control
    named[57] = ("bidirectional", "SMB_CLK")
    named[58] = ("bidirectional", "SMB_DAT")
    named[59] = ("bidirectional", "UART_TXD")
    named[60] = ("bidirectional", "UART_RXD")
    named[61] = ("output", "PWR_EN")
    named[62] = ("output", "RESET_L")
    named[63] = ("input", "ALERT_L")
    named[64] = ("bidirectional", "JTAG_TCK")
    named[65] = ("bidirectional", "JTAG_TMS")
    named[66] = ("bidirectional", "JTAG_TDI")
    named[67] = ("bidirectional", "JTAG_TDO")
    # USB 3.0
    named[71] = ("bidirectional", "USB3_TX_P")
    named[72] = ("bidirectional", "USB3_TX_N")
    named[73] = ("bidirectional", "USB3_RX_P")
    named[74] = ("bidirectional", "USB3_RX_N")
    named[75] = ("bidirectional", "USB2_DP")
    named[76] = ("bidirectional", "USB2_DN")
    # Power / GND: interleaved second half
    for n in list(range(101, 141)):
        named[n] = ("power_in", "VDD_12V")
    for n in list(range(141, 201)):
        named[n] = ("power_in", "GND")
    for n in range(1, 101):
        if n not in named:
            named[n] = ("bidirectional", f"RSVD{n}")
    for n in range(1, 101):
        ptype, name = named[n]
        pins.append(("L", ptype, name, str(n)))
    for n in range(101, 201):
        ptype, name = named[n]
        pins.append(("R", ptype, name, str(n)))
    return pins


# ---- BCM56780 (Trident 4): 12.8 Tbps switch fabric ---------------------
def bcm56780_pins():
    """Big HFCBGA-1300 switch. We represent 160 grouped pins on the symbol:
    32 SerDes quads (TX+/-, RX+/-) = 128, plus mgmt/PCIe/JTAG/power/GND.
    Real device has 1300 balls; symbol is a black-box abstraction.
    """
    pins = []
    idx = 1
    # 32 SerDes lanes across L/R
    for lane in range(16):
        for name in [f"SDS{lane}_TX_P", f"SDS{lane}_TX_N", f"SDS{lane}_RX_P", f"SDS{lane}_RX_N"]:
            pins.append(("L", "bidirectional", name, str(idx)))
            idx += 1
    for lane in range(16, 32):
        for name in [f"SDS{lane}_TX_P", f"SDS{lane}_TX_N", f"SDS{lane}_RX_P", f"SDS{lane}_RX_N"]:
            pins.append(("R", "bidirectional", name, str(idx)))
            idx += 1
    # Top: mgmt + clocks + PCIe
    top_names = [
        ("input", "REFCLK_156M_P"), ("input", "REFCLK_156M_N"),
        ("bidirectional", "MDC"), ("bidirectional", "MDIO"),
        ("bidirectional", "PCIE_HOST_TX_P"), ("bidirectional", "PCIE_HOST_TX_N"),
        ("bidirectional", "PCIE_HOST_RX_P"), ("bidirectional", "PCIE_HOST_RX_N"),
        ("input", "PCIE_HOST_REFCLK_P"), ("input", "PCIE_HOST_REFCLK_N"),
        ("input", "PCIE_HOST_PERST_L"),
        ("bidirectional", "JTAG_TCK"), ("bidirectional", "JTAG_TMS"),
        ("bidirectional", "JTAG_TDI"), ("bidirectional", "JTAG_TDO"),
        ("bidirectional", "UART_TXD"), ("bidirectional", "UART_RXD"),
        ("bidirectional", "I2C_MGMT_SCL"), ("bidirectional", "I2C_MGMT_SDA"),
        ("input", "SYS_RESET_L"), ("output", "SYS_ALIVE"),
    ]
    for ptype, name in top_names:
        pins.append(("T", ptype, name, str(idx)))
        idx += 1
    # Bottom: power rails + GND
    bottom_named = [
        ("power_in", "VDD_CORE_0V9"),
        ("power_in", "VDD_CORE_0V9"),
        ("power_in", "VDD_CORE_0V9"),
        ("power_in", "VDD_CORE_0V9"),
        ("power_in", "VDD_ANA_1V8"),
        ("power_in", "VDD_ANA_1V8"),
        ("power_in", "VDD_IO_3V3"),
        ("power_in", "VDD_IO_3V3"),
        ("power_in", "VDD_SERDES_0V9"),
        ("power_in", "VDD_SERDES_0V9"),
        ("power_in", "VDD_SERDES_1V2"),
        ("power_in", "VDD_SERDES_1V2"),
    ]
    for ptype, name in bottom_named:
        pins.append(("B", ptype, name, str(idx)))
        idx += 1
    # Bulk GNDs
    for _ in range(20):
        pins.append(("B", "power_in", "GND", str(idx)))
        idx += 1
    return pins


# ---- Astera Labs ARIES PCIe Gen5 retimer ------------------------------
def aries_pins():
    """PCIe Gen5 x16 retimer. Upstream + Downstream lanes + mgmt."""
    pins = []
    idx = 1
    # Upstream x8 on left, Downstream x8 on right (subset shown)
    for lane in range(8):
        for suffix, ptype in [("UP_TX_P", "output"), ("UP_TX_N", "output"),
                              ("UP_RX_P", "input"), ("UP_RX_N", "input")]:
            pins.append(("L", ptype, f"L{lane}_{suffix}", str(idx)))
            idx += 1
    for lane in range(8):
        for suffix, ptype in [("DN_TX_P", "output"), ("DN_TX_N", "output"),
                              ("DN_RX_P", "input"), ("DN_RX_N", "input")]:
            pins.append(("R", ptype, f"L{lane}_{suffix}", str(idx)))
            idx += 1
    top_named = [
        ("input", "REFCLK_UP_P"), ("input", "REFCLK_UP_N"),
        ("output", "REFCLK_DN_P"), ("output", "REFCLK_DN_N"),
        ("input", "PERST_UP_L"), ("output", "PERST_DN_L"),
        ("bidirectional", "SMB_CLK"), ("bidirectional", "SMB_DAT"),
        ("bidirectional", "I2C_MGMT_SCL"), ("bidirectional", "I2C_MGMT_SDA"),
        ("input", "SYS_RESET_L"), ("output", "READY"),
    ]
    for ptype, name in top_named:
        pins.append(("T", ptype, name, str(idx)))
        idx += 1
    for name in ["VDD_CORE_0V9", "VDD_CORE_0V9", "VDD_1V8", "VDD_1V8",
                 "VDD_3V3", "VDD_3V3", "GND", "GND", "GND", "GND", "GND", "GND"]:
        ptype = "power_in"
        pins.append(("B", ptype, name, str(idx)))
        idx += 1
    return pins


# ---- TI UCD90320: 32-rail sequencer / power manager ----------------------
def ucd90320_pins():
    pins = []
    idx = 1
    # 32 EN outputs (L side), 32 PGOOD/margin inputs (R side)
    for i in range(32):
        pins.append(("L", "output", f"EN{i}", str(idx))); idx += 1
    for i in range(32):
        pins.append(("R", "input", f"PGOOD{i}", str(idx))); idx += 1
    for name, ptype in [("PMBUS_CLK", "bidirectional"), ("PMBUS_DAT", "bidirectional"),
                        ("PMBUS_ALERT_L", "output"), ("PMBUS_ADDR0", "input"),
                        ("PMBUS_ADDR1", "input"), ("JTAG_TCK", "bidirectional"),
                        ("JTAG_TMS", "bidirectional"), ("JTAG_TDI", "bidirectional"),
                        ("JTAG_TDO", "bidirectional"), ("RESET_L", "input"),
                        ("GPIO_FAULT", "output")]:
        pins.append(("T", ptype, name, str(idx))); idx += 1
    for name in ["VCC_3V3", "VCC_3V3", "VCC_1V8", "GND", "GND", "GND", "AGND"]:
        pins.append(("B", "power_in", name, str(idx))); idx += 1
    return pins


# ---- Nuvoton NCT6116 BMC / super-I/O -----------------------------------
def bmc_pins():
    pins = []
    idx = 1
    left = [
        ("input", "FAN0_TACH"), ("input", "FAN1_TACH"),
        ("input", "FAN2_TACH"), ("input", "FAN3_TACH"),
        ("input", "FAN4_TACH"), ("input", "FAN5_TACH"),
        ("input", "PUMP_TACH"),
        ("input", "TEMP0_ADC"), ("input", "TEMP1_ADC"),
        ("input", "TEMP2_ADC"), ("input", "TEMP3_ADC"),
        ("input", "TEMP4_ADC"),
        ("input", "PSU0_ALERT_L"), ("input", "PSU1_ALERT_L"),
        ("input", "LEAK_DETECT"),
    ]
    for ptype, name in left:
        pins.append(("L", ptype, name, str(idx))); idx += 1
    right = [
        ("output", "FAN0_PWM"), ("output", "FAN1_PWM"),
        ("output", "FAN2_PWM"), ("output", "FAN3_PWM"),
        ("output", "FAN4_PWM"), ("output", "FAN5_PWM"),
        ("output", "PUMP_PWM"),
        ("output", "CHASSIS_LED"), ("output", "STATUS_LED"),
        ("output", "FAULT_LED"),
        ("bidirectional", "I2C_MGMT_SCL"), ("bidirectional", "I2C_MGMT_SDA"),
        ("bidirectional", "SPI_MOSI"), ("bidirectional", "SPI_MISO"),
        ("bidirectional", "SPI_SCK"), ("output", "SPI_CS_L"),
    ]
    for ptype, name in right:
        pins.append(("R", ptype, name, str(idx))); idx += 1
    for ptype, name in [("bidirectional", "UART_TXD"), ("bidirectional", "UART_RXD"),
                         ("output", "PSON_L"), ("input", "PWROK"),
                         ("input", "RESET_L"), ("input", "SYS_INT")]:
        pins.append(("T", ptype, name, str(idx))); idx += 1
    for name in ["VCC_3V3", "VCC_3V3", "VCC_1V8", "VCC_STBY_3V3",
                 "GND", "GND", "GND"]:
        pins.append(("B", "power_in", name, str(idx))); idx += 1
    return pins


# ---- TPS543x buck regulator (illustrative 12V -> 5V/3V3 rail) ---------
def tps543x_pins():
    return [
        ("L", "power_in", "VIN", "1"),
        ("L", "power_in", "VIN", "2"),
        ("L", "input", "EN", "3"),
        ("L", "input", "SS_TR", "4"),
        ("L", "input", "VSENSE", "5"),
        ("L", "bidirectional", "COMP", "6"),
        ("R", "power_out", "VOUT", "7"),
        ("R", "power_out", "VOUT", "8"),
        ("R", "output", "PGOOD", "9"),
        ("R", "input", "RT", "10"),
        ("R", "bidirectional", "SYNC", "11"),
        ("R", "output", "BOOT", "12"),
        ("B", "power_in", "GND", "13"),
        ("B", "power_in", "GND", "14"),
        ("B", "power_in", "AGND", "15"),
        ("B", "power_in", "PAD", "16"),
    ]


# ---- Infineon SLB9670 TPM 2.0 -----------------------------------------
def tpm_pins():
    return [
        ("L", "bidirectional", "SPI_MOSI", "1"),
        ("L", "bidirectional", "SPI_MISO", "2"),
        ("L", "bidirectional", "SPI_CLK", "3"),
        ("L", "input", "SPI_CS_L", "4"),
        ("L", "input", "RESET_L", "5"),
        ("L", "output", "PIRQ_L", "6"),
        ("R", "input", "PP", "7"),
        ("R", "bidirectional", "GPIO", "8"),
        ("B", "power_in", "VCC_3V3", "9"),
        ("B", "power_in", "VCC_1V8", "10"),
        ("B", "power_in", "GND", "11"),
        ("B", "power_in", "GND", "12"),
    ]


# ---- ATX24 power input ------------------------------------------------
def atx24_pins():
    map_ = {
        1: "+3V3", 2: "+3V3", 3: "GND", 4: "+5V", 5: "GND", 6: "+5V",
        7: "GND", 8: "PWR_OK", 9: "+5VSB", 10: "+12V1", 11: "+12V1",
        12: "+3V3", 13: "+3V3", 14: "-12V", 15: "GND", 16: "PSON_L",
        17: "GND", 18: "GND", 19: "GND", 20: "NC", 21: "+5V",
        22: "+5V", 23: "+5V", 24: "GND",
    }
    pins = []
    for n in range(1, 13):
        ptype = "power_in" if map_[n] not in ("PWR_OK", "PSON_L", "NC") else (
            "output" if map_[n] == "PWR_OK" else ("input" if map_[n] == "PSON_L" else "passive")
        )
        pins.append(("L", ptype, map_[n], str(n)))
    for n in range(13, 25):
        ptype = "power_in" if map_[n] not in ("PWR_OK", "PSON_L", "NC") else (
            "output" if map_[n] == "PWR_OK" else ("input" if map_[n] == "PSON_L" else "passive")
        )
        pins.append(("R", ptype, map_[n], str(n)))
    return pins


def write_kicad_sym():
    parts = []
    parts.append(build_symbol(
        "MM70_260_SODIMM",
        "JAE MM70-260B1-R1 260-pin SODIMM DDR5-style connector for NVIDIA Jetson Orin NX module (PLACEHOLDER pin map - verify)",
        "palpod-compute-backplane:MM70_260_SODIMM",
        "https://www.jae.com/en/connectors/series/detail/code/MM70/",
        width=45.72, height=340.36, pins=mm70_pins(),
    ))
    parts.append(build_symbol(
        "SAMTEC_EXAMAX_200",
        "Samtec ExaMAX 56Gbps 200-pos mezzanine for AMD Ryzen AI 9 HX 370 SBC daughtercard (PLACEHOLDER - verify against Samtec drawing)",
        "palpod-compute-backplane:SAMTEC_EXAMAX_200",
        "https://www.samtec.com/products/exam",
        width=50.8, height=266.7, pins=examax_pins(),
    ))
    parts.append(build_symbol(
        "BCM56780",
        "Broadcom BCM56780 Trident 4-X9 12.8 Tbps switch ASIC (HFCBGA-1300, 40x40mm, PLACEHOLDER symbol)",
        "palpod-compute-backplane:BCM56780_HFCBGA1300",
        "https://www.broadcom.com/products/ethernet-connectivity/switching/strataxgs/bcm56780",
        width=101.6, height=203.2, pins=bcm56780_pins(),
    ))
    parts.append(build_symbol(
        "ARIES_PT4",
        "Astera Labs Aries PT4 PCIe Gen5 x16 retimer (BGA-544, PLACEHOLDER symbol)",
        "palpod-compute-backplane:ARIES_PT4_BGA544",
        "https://www.asteralabs.com/products/",
        width=76.2, height=182.88, pins=aries_pins(),
    ))
    parts.append(build_symbol(
        "UCD90320",
        "TI UCD90320 32-rail power sequencer / PMBus manager (BGA-173, PLACEHOLDER)",
        "palpod-compute-backplane:UCD90320_BGA173",
        "https://www.ti.com/product/UCD90320",
        width=68.58, height=203.2, pins=ucd90320_pins(),
    ))
    parts.append(build_symbol(
        "NCT6116",
        "Nuvoton NCT6116 super-I/O / BMC with fan tach+PWM and thermal ADC (LQFP-128, PLACEHOLDER)",
        "palpod-compute-backplane:NCT6116_LQFP128",
        "https://www.nuvoton.com/products/cloud-computing/io-hub/",
        width=68.58, height=127.0, pins=bmc_pins(),
    ))
    parts.append(build_symbol(
        "TPS543x",
        "TI TPS543x-family synchronous buck regulator (12V input, 4-20A, illustrative single-phase rail)",
        "palpod-compute-backplane:TPS543x_QFN",
        "https://www.ti.com/power-management/step-down-buck/products.html",
        width=45.72, height=76.2, pins=tps543x_pins(),
    ))
    parts.append(build_symbol(
        "SLB9670",
        "Infineon SLB9670VQ2.0 TPM 2.0 (SPI, TSSOP-28, PLACEHOLDER)",
        "palpod-compute-backplane:SLB9670_TSSOP28",
        "https://www.infineon.com/cms/en/product/security-smart-card-solutions/optiga-embedded-security-solutions/optiga-tpm/",
        width=38.1, height=76.2, pins=tpm_pins(),
    ))
    parts.append(build_symbol(
        "ATX24",
        "ATX 24-pin ATX main power input header (Molex 39-01-2240)",
        "palpod-compute-backplane:ATX24_HEADER",
        "https://www.molex.com/en-us/products/part-detail/39012240",
        width=25.4, height=76.2, pins=atx24_pins(),
    ))
    body = "".join(parts)
    (LIB_DIR / "palpod-compute-backplane.kicad_sym").write_text(
        "(kicad_symbol_lib\n"
        "\t(version 20231120)\n"
        "\t(generator \"kicad_symbol_editor\")\n"
        f"{body}"
        ")\n"
    )


# ---------------------------------------------------------------------------
# Footprints (.pretty/*.kicad_mod)
# Only need placeholder outlines with pin 1 markers and correct package size.
# ---------------------------------------------------------------------------

def fp_line(x1, y1, x2, y2, layer, width=0.15):
    return f"  (fp_line (start {x1} {y1}) (end {x2} {y2}) (stroke (width {width}) (type solid)) (layer \"{layer}\") (uuid \"{uid()}\"))\n"


def fp_rect(w, h, layer, width=0.15):
    hw, hh = w / 2, h / 2
    return (
        fp_line(-hw, -hh, hw, -hh, layer, width)
        + fp_line(hw, -hh, hw, hh, layer, width)
        + fp_line(hw, hh, -hw, hh, layer, width)
        + fp_line(-hw, hh, -hw, -hh, layer, width)
    )


def fp_courtyard(w, h, margin=0.5):
    return fp_rect(w + 2 * margin, h + 2 * margin, "F.CrtYd", 0.05)


def fp_silk(w, h, margin=0.15):
    return fp_rect(w + 2 * margin, h + 2 * margin, "F.SilkS", 0.12)


def fp_fab(w, h):
    return fp_rect(w, h, "F.Fab", 0.1)


def fp_pin1_dot(x, y):
    return f"  (fp_circle (center {x} {y}) (end {x + 0.2} {y}) (stroke (width 0.15) (type solid)) (fill solid) (layer \"F.SilkS\") (uuid \"{uid()}\"))\n"


def make_footprint(name, description, tags, body_w, body_h, pads_text, attr="smd"):
    return (
        f"(footprint \"{name}\"\n"
        f"\t(version 20240108)\n"
        f"\t(generator \"pcbnew\")\n"
        f"\t(generator_version \"8.0\")\n"
        f"\t(layer \"F.Cu\")\n"
        f"\t(descr \"{description}\")\n"
        f"\t(tags \"{tags}\")\n"
        f"\t(property \"Reference\" \"REF**\"\n"
        f"\t\t(at 0 {-body_h/2 - 2} 0)\n"
        f"\t\t(layer \"F.SilkS\")\n"
        f"\t\t(uuid \"{uid()}\")\n"
        f"\t\t(effects (font (size 1 1) (thickness 0.15)))\n"
        f"\t)\n"
        f"\t(property \"Value\" \"{name}\"\n"
        f"\t\t(at 0 {body_h/2 + 2} 0)\n"
        f"\t\t(layer \"F.Fab\")\n"
        f"\t\t(uuid \"{uid()}\")\n"
        f"\t\t(effects (font (size 1 1) (thickness 0.15)))\n"
        f"\t)\n"
        f"\t(property \"Footprint\" \"\" (at 0 0 0) (layer \"F.Fab\") (hide yes) (uuid \"{uid()}\") (effects (font (size 1 1) (thickness 0.15))))\n"
        f"\t(property \"Datasheet\" \"\" (at 0 0 0) (layer \"F.Fab\") (hide yes) (uuid \"{uid()}\") (effects (font (size 1 1) (thickness 0.15))))\n"
        f"\t(property \"Description\" \"PLACEHOLDER footprint - verify against datasheet before fab\" (at 0 0 0) (layer \"F.Fab\") (hide yes) (uuid \"{uid()}\") (effects (font (size 1 1) (thickness 0.15))))\n"
        f"\t(attr {attr})\n"
        + fp_fab(body_w, body_h)
        + fp_silk(body_w, body_h)
        + fp_courtyard(body_w, body_h)
        + pads_text
        + ")\n"
    )


def pad_smd(num, x, y, w, h):
    return f"  (pad \"{num}\" smd rect (at {x} {y}) (size {w} {h}) (layers \"F.Cu\" \"F.Paste\" \"F.Mask\") (uuid \"{uid()}\"))\n"


def pad_th(num, x, y, drill, size):
    return f"  (pad \"{num}\" thru_hole circle (at {x} {y}) (size {size} {size}) (drill {drill}) (layers \"*.Cu\" \"*.Mask\") (uuid \"{uid()}\"))\n"


def bga_pads(n_x, n_y, pitch, ball_size=0.4, start_num=1):
    """Generate a BGA-style pad grid centered at (0,0)."""
    out = ""
    x0 = -(n_x - 1) * pitch / 2
    y0 = -(n_y - 1) * pitch / 2
    num = start_num
    for iy in range(n_y):
        for ix in range(n_x):
            x = x0 + ix * pitch
            y = y0 + iy * pitch
            out += pad_smd(str(num), round(x, 3), round(y, 3), ball_size, ball_size)
            num += 1
    return out


def edge_row_pads(n, pitch, side, body_w, body_h, pad_w=0.3, pad_h=1.5, start_num=1):
    """Two rows of edge-mount pads for high-density connectors."""
    out = ""
    row_len = (n - 1) * pitch
    x0 = -row_len / 2
    num = start_num
    if side == "top":
        y = -body_h / 2 - pad_h / 2 + 0.5
        for i in range(n):
            out += pad_smd(str(num), round(x0 + i * pitch, 3), round(y, 3), pad_w, pad_h)
            num += 1
    elif side == "bottom":
        y = body_h / 2 + pad_h / 2 - 0.5
        for i in range(n):
            out += pad_smd(str(num), round(x0 + i * pitch, 3), round(y, 3), pad_w, pad_h)
            num += 1
    return out


def write_footprints():
    # MM70_260 SODIMM: 260 pins, 0.5mm pitch, body ~68mm long x ~5mm high
    n_side = 130
    pitch = 0.5
    pads = ""
    row_len = (n_side - 1) * pitch  # 64.5 mm
    x0 = -row_len / 2
    # front row (odd numbers 1..259 for top edge) - use 1..130 packed on top row
    for i in range(n_side):
        pads += pad_smd(str(i + 1), round(x0 + i * pitch, 3), -1.5, 0.3, 1.6)
    for i in range(n_side):
        pads += pad_smd(str(i + 1 + n_side), round(x0 + i * pitch, 3), 1.5, 0.3, 1.6)
    body_w, body_h = 68.0, 5.0
    (FP_DIR / "MM70_260_SODIMM.kicad_mod").write_text(
        make_footprint(
            "MM70_260_SODIMM",
            "PLACEHOLDER JAE MM70-260B1-R1 260-pos DDR5-style SODIMM socket for Jetson Orin NX SoM - VERIFY DIMENSIONS",
            "SODIMM 260 JAE MM70 Jetson PLACEHOLDER",
            body_w, body_h, pads,
        )
    )
    # ExaMAX 200 mezzanine - Samtec ExaMAX 0.8mm pitch, 4 rows
    pads = ""
    n_per_row = 50
    pitch = 0.8
    row_len = (n_per_row - 1) * pitch
    x0 = -row_len / 2
    for row, y in enumerate([-2.4, -0.8, 0.8, 2.4]):
        for i in range(n_per_row):
            pads += pad_smd(str(row * n_per_row + i + 1), round(x0 + i * pitch, 3), y, 0.4, 1.0)
    body_w, body_h = 44.0, 8.0
    (FP_DIR / "SAMTEC_EXAMAX_200.kicad_mod").write_text(
        make_footprint(
            "SAMTEC_EXAMAX_200",
            "PLACEHOLDER Samtec ExaMAX 56Gbps 200-pos mezzanine footprint - VERIFY DIMENSIONS",
            "Samtec ExaMAX 56Gbps mezzanine PLACEHOLDER",
            body_w, body_h, pads,
        )
    )
    # BCM56780 HFCBGA-1300, 40x40mm, ~1mm ball pitch, 36x36 grid
    pads = bga_pads(36, 36, 1.0, 0.5)
    body_w, body_h = 40.0, 40.0
    (FP_DIR / "BCM56780_HFCBGA1300.kicad_mod").write_text(
        make_footprint(
            "BCM56780_HFCBGA1300",
            "PLACEHOLDER Broadcom BCM56780 Trident 4 HFCBGA 40x40mm - VERIFY BALL MAP",
            "BCM56780 Trident4 HFCBGA1300 PLACEHOLDER",
            body_w, body_h, pads,
        )
    )
    # Aries PT4 BGA-544, ~1mm pitch, 24x24 grid, 24x24mm
    pads = bga_pads(24, 24, 1.0, 0.5)
    body_w, body_h = 24.0, 24.0
    (FP_DIR / "ARIES_PT4_BGA544.kicad_mod").write_text(
        make_footprint(
            "ARIES_PT4_BGA544",
            "PLACEHOLDER Astera Labs Aries PT4 PCIe Gen5 retimer BGA-544 - VERIFY BALL MAP",
            "Astera Aries PT4 BGA544 PLACEHOLDER",
            body_w, body_h, pads,
        )
    )
    # UCD90320 BGA-173, 15x15 mm, 1mm pitch
    pads = bga_pads(15, 12, 1.0, 0.45)
    body_w, body_h = 15.0, 12.0
    (FP_DIR / "UCD90320_BGA173.kicad_mod").write_text(
        make_footprint(
            "UCD90320_BGA173",
            "PLACEHOLDER TI UCD90320 32-rail power sequencer BGA-173 - VERIFY BALL MAP",
            "UCD90320 sequencer PMBus BGA173 PLACEHOLDER",
            body_w, body_h, pads,
        )
    )
    # NCT6116 LQFP-128, 20x20 mm, 0.5mm pitch
    n_per_side = 32
    pitch = 0.5
    pads = ""
    row_len = (n_per_side - 1) * pitch  # 15.5
    x0 = -row_len / 2
    num = 1
    # Left side (top->bottom)
    for i in range(n_per_side):
        pads += pad_smd(str(num), -10.5, round(-row_len / 2 + i * pitch, 3), 1.5, 0.25); num += 1
    for i in range(n_per_side):
        pads += pad_smd(str(num), round(-row_len / 2 + i * pitch, 3), 10.5, 0.25, 1.5); num += 1
    for i in range(n_per_side):
        pads += pad_smd(str(num), 10.5, round(row_len / 2 - i * pitch, 3), 1.5, 0.25); num += 1
    for i in range(n_per_side):
        pads += pad_smd(str(num), round(row_len / 2 - i * pitch, 3), -10.5, 0.25, 1.5); num += 1
    body_w, body_h = 20.0, 20.0
    (FP_DIR / "NCT6116_LQFP128.kicad_mod").write_text(
        make_footprint(
            "NCT6116_LQFP128",
            "PLACEHOLDER Nuvoton NCT6116 BMC / super-I/O LQFP-128 20x20mm 0.5mm pitch",
            "NCT6116 BMC LQFP128 PLACEHOLDER",
            body_w, body_h, pads,
        )
    )
    # TPS543x QFN-16 5x5mm, 0.65mm pitch
    n_per_side = 4
    pitch = 0.65
    pads = ""
    row_len = (n_per_side - 1) * pitch
    num = 1
    for i in range(n_per_side):
        pads += pad_smd(str(num), -2.5, round(-row_len / 2 + i * pitch, 3), 0.9, 0.3); num += 1
    for i in range(n_per_side):
        pads += pad_smd(str(num), round(-row_len / 2 + i * pitch, 3), 2.5, 0.3, 0.9); num += 1
    for i in range(n_per_side):
        pads += pad_smd(str(num), 2.5, round(row_len / 2 - i * pitch, 3), 0.9, 0.3); num += 1
    for i in range(n_per_side):
        pads += pad_smd(str(num), round(row_len / 2 - i * pitch, 3), -2.5, 0.3, 0.9); num += 1
    pads += pad_smd("17", 0, 0, 3.0, 3.0)  # thermal pad
    body_w, body_h = 5.0, 5.0
    (FP_DIR / "TPS543x_QFN.kicad_mod").write_text(
        make_footprint(
            "TPS543x_QFN",
            "PLACEHOLDER TI TPS543x-family QFN-16 5x5mm buck regulator",
            "TPS543x buck QFN16 PLACEHOLDER",
            body_w, body_h, pads,
        )
    )
    # SLB9670 TSSOP-28 4.4x9.7mm, 0.65mm pitch
    n_per_side = 14
    pitch = 0.65
    pads = ""
    row_len = (n_per_side - 1) * pitch
    x0 = -row_len / 2
    num = 1
    for i in range(n_per_side):
        pads += pad_smd(str(num), -3.0, round(-row_len / 2 + i * pitch, 3), 1.5, 0.3); num += 1
    for i in range(n_per_side):
        pads += pad_smd(str(num), 3.0, round(row_len / 2 - i * pitch, 3), 1.5, 0.3); num += 1
    body_w, body_h = 4.4, 9.7
    (FP_DIR / "SLB9670_TSSOP28.kicad_mod").write_text(
        make_footprint(
            "SLB9670_TSSOP28",
            "PLACEHOLDER Infineon SLB9670 TPM 2.0 TSSOP-28",
            "SLB9670 TPM TSSOP28 PLACEHOLDER",
            body_w, body_h, pads,
        )
    )
    # ATX24 - 24-pin thru-hole 4.2mm pitch
    pads = ""
    pitch = 4.2
    n_per_row = 12
    for i in range(n_per_row):
        pads += pad_th(str(i + 1), round(-(n_per_row - 1) * pitch / 2 + i * pitch, 3),
                        -2.1, 1.7, 3.0)
    for i in range(n_per_row):
        pads += pad_th(str(i + 13), round(-(n_per_row - 1) * pitch / 2 + i * pitch, 3),
                        2.1, 1.7, 3.0)
    body_w, body_h = 52.0, 8.0
    (FP_DIR / "ATX24_HEADER.kicad_mod").write_text(
        make_footprint(
            "ATX24_HEADER",
            "PLACEHOLDER Molex 39-01-2240 ATX24 main power header, 24-pos 4.2mm pitch",
            "ATX24 Molex 4.2mm PLACEHOLDER",
            body_w, body_h, pads,
            attr="through_hole",
        )
    )


# ---------------------------------------------------------------------------
# Schematic (.kicad_sch)
# ---------------------------------------------------------------------------

def sch_symbol_stub(lib_id, at_x, at_y, ref, value, footprint, extras=""):
    return (
        "\t(symbol\n"
        f"\t\t(lib_id \"{lib_id}\")\n"
        f"\t\t(at {at_x} {at_y} 0)\n"
        "\t\t(unit 1)\n"
        "\t\t(exclude_from_sim no)\n"
        "\t\t(in_bom yes)\n"
        "\t\t(on_board yes)\n"
        "\t\t(dnp no)\n"
        f"\t\t(uuid \"{uid()}\")\n"
        f"\t\t(property \"Reference\" \"{ref}\"\n"
        f"\t\t\t(at {at_x + 2.54} {at_y - 5.08} 0)\n"
        "\t\t\t(effects (font (size 1.27 1.27)) (justify left))\n"
        "\t\t)\n"
        f"\t\t(property \"Value\" \"{value}\"\n"
        f"\t\t\t(at {at_x + 2.54} {at_y + 5.08} 0)\n"
        "\t\t\t(effects (font (size 1.27 1.27)) (justify left))\n"
        "\t\t)\n"
        f"\t\t(property \"Footprint\" \"{footprint}\"\n"
        f"\t\t\t(at {at_x} {at_y} 0)\n"
        "\t\t\t(effects (font (size 1.27 1.27)) (hide yes))\n"
        "\t\t)\n"
        f"\t\t(property \"Datasheet\" \"~\"\n"
        f"\t\t\t(at {at_x} {at_y} 0)\n"
        "\t\t\t(effects (font (size 1.27 1.27)) (hide yes))\n"
        "\t\t)\n"
        f"{extras}"
        "\t\t(instances\n"
        f"\t\t\t(project \"{PROJECT}\"\n"
        f"\t\t\t\t(path \"/{ROOT_SHEET_UUID}\"\n"
        f"\t\t\t\t\t(reference \"{ref}\")\n"
        "\t\t\t\t\t(unit 1)\n"
        "\t\t\t\t)\n"
        "\t\t\t)\n"
        "\t\t)\n"
        "\t)\n"
    )


def sch_wire(x1, y1, x2, y2):
    return (
        "\t(wire\n"
        f"\t\t(pts (xy {x1} {y1}) (xy {x2} {y2}))\n"
        "\t\t(stroke (width 0) (type default))\n"
        f"\t\t(uuid \"{uid()}\")\n"
        "\t)\n"
    )


def sch_label(name, x, y):
    return (
        f"\t(label \"{name}\"\n"
        f"\t\t(at {x} {y} 0)\n"
        "\t\t(effects (font (size 1.27 1.27)) (justify left bottom))\n"
        f"\t\t(uuid \"{uid()}\")\n"
        "\t)\n"
    )


# --- Minimal embedded lib_symbols for stock parts used at instance level.  ---
# We embed Device:R, Device:C, and power symbols (+12V, +5V, +3V3, +1V8, +0V9,
# GND) so the sheet loads even without the KiCad stock libraries configured.
LIB_SYMBOLS_EMBEDDED = r'''(symbol "Device:R"
			(pin_numbers (hide yes))
			(pin_names (offset 0) (hide yes))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
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
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
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
'''

def power_sym(name):
    return f'''(symbol "power:{name}"
			(power)
			(pin_names (offset 0))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "{name}" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "{name}_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27) (xy 0 0) (xy -0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "{name}_1_1"
				(pin power_in line (at 0 0 90) (length 0) (name "{name}" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
'''


def gnd_sym():
    return '''(symbol "power:GND"
			(power)
			(pin_names (offset 0))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "GND_0_1"
				(polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "GND_1_1"
				(pin power_in line (at 0 0 270) (length 0) (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
'''


def embed_local_symbol(sym_text):
    """Take the raw text from libraries/palpod-compute-backplane.kicad_sym for
    a single symbol (starting with `(symbol "NAME"`), and reformat its lib_id
    header so it lives inside the schematic's lib_symbols block as
    `palpod-compute-backplane:NAME`."""
    return sym_text  # placeholder if needed


def build_schematic():
    # Collect all local symbols we placed on the schematic and embed them into
    # lib_symbols so the sheet is self-contained.
    local_sym_source = (LIB_DIR / "palpod-compute-backplane.kicad_sym").read_text()

    # Extract each symbol block from the local lib file and rename its top-line
    # to library:name (so lib_id "palpod-compute-backplane:BCM56780" resolves).
    local_syms = {}
    i = 0
    lines = local_sym_source.splitlines(keepends=True)
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.lstrip()
        if stripped.startswith("(symbol \""):
            name = stripped.split("\"")[1]
            # Find matching close-paren (top-level in this file the symbol block
            # sits under kicad_symbol_lib. Use bracket depth.
            depth = 0
            start = i
            while i < n:
                for ch in lines[i]:
                    if ch == "(":
                        depth += 1
                    elif ch == ")":
                        depth -= 1
                        if depth == 0:
                            break
                if depth == 0:
                    break
                i += 1
            end = i + 1
            block = "".join(lines[start:end])
            # Rename the top identifier from "NAME" -> "palpod-compute-backplane:NAME"
            block = block.replace(f"(symbol \"{name}\"", f"(symbol \"palpod-compute-backplane:{name}\"", 1)
            # Indent each line by one extra tab so it nests inside lib_symbols
            block = "".join("\t" + l for l in block.splitlines(keepends=True))
            local_syms[name] = block
            i = end
        else:
            i += 1

    # Compose lib_symbols block
    lib_symbols = "\t(lib_symbols\n"
    lib_symbols += "\t\t" + LIB_SYMBOLS_EMBEDDED.strip() + "\n"
    for name in ["+12V", "+5V", "+3V3", "+1V8", "+0V9"]:
        lib_symbols += "\t\t" + power_sym(name).strip() + "\n"
    lib_symbols += "\t\t" + gnd_sym().strip() + "\n"
    for block in local_syms.values():
        lib_symbols += block
    lib_symbols += "\t)\n"

    # Place symbols. Use a giant A0-ish sheet. paper "A0" is 1189 x 841mm.
    parts = []
    ref_counter = {"J": 0, "U": 0, "P": 0, "C": 0, "R": 0, "PWR": 0}
    def nref(prefix):
        ref_counter[prefix] += 1
        return f"{prefix}{ref_counter[prefix]}"

    # Row 1: 10 SODIMM connectors along the top (Jetson Orin NX carriers)
    for i in range(10):
        x = 80 + i * 100
        y = 60
        parts.append(sch_symbol_stub(
            "palpod-compute-backplane:MM70_260_SODIMM",
            x, y, f"J{i+1}", f"MM70_260_SODIMM (Jetson Orin NX #{i})",
            "palpod-compute-backplane:MM70_260_SODIMM"))
    ref_counter["J"] = 10

    # Row 2: 10 Samtec ExaMAX connectors along the bottom (Ryzen SBC carriers)
    for i in range(10):
        x = 80 + i * 100
        y = 620
        parts.append(sch_symbol_stub(
            "palpod-compute-backplane:SAMTEC_EXAMAX_200",
            x, y, f"J{i+11}", f"SAMTEC_EXAMAX_200 (Ryzen AI 9 HX 370 #{i})",
            "palpod-compute-backplane:SAMTEC_EXAMAX_200"))
    ref_counter["J"] = 20

    # Center: BCM56780 switch fabric
    parts.append(sch_symbol_stub(
        "palpod-compute-backplane:BCM56780",
        520, 340, "U1", "BCM56780 (Trident 4 12.8Tbps)",
        "palpod-compute-backplane:BCM56780_HFCBGA1300"))

    # Left of switch: Astera Aries retimer
    parts.append(sch_symbol_stub(
        "palpod-compute-backplane:ARIES_PT4",
        260, 340, "U2", "ARIES_PT4 (PCIe Gen5 retimer)",
        "palpod-compute-backplane:ARIES_PT4_BGA544"))

    # Right of switch: UCD90320 sequencer
    parts.append(sch_symbol_stub(
        "palpod-compute-backplane:UCD90320",
        800, 340, "U3", "UCD90320 (32-rail sequencer)",
        "palpod-compute-backplane:UCD90320_BGA173"))

    # BMC top-right area
    parts.append(sch_symbol_stub(
        "palpod-compute-backplane:NCT6116",
        1000, 220, "U4", "NCT6116 (BMC / super-I/O)",
        "palpod-compute-backplane:NCT6116_LQFP128"))

    # TPM 2.0
    parts.append(sch_symbol_stub(
        "palpod-compute-backplane:SLB9670",
        1000, 400, "U5", "SLB9670 (TPM 2.0)",
        "palpod-compute-backplane:SLB9670_TSSOP28"))

    # Buck reg block: TPS543x with input/output caps (+12V -> +5V rail)
    parts.append(sch_symbol_stub(
        "palpod-compute-backplane:TPS543x",
        260, 500, "U6", "TPS543x (12V -> 5V, 15A)",
        "palpod-compute-backplane:TPS543x_QFN"))
    # Input cap 470uF
    parts.append(sch_symbol_stub(
        "Device:C", 240, 500, "C1", "470uF/25V",
        "Capacitor_SMD:CP_Elec_10x10.5"))
    # Input decouple 10uF
    parts.append(sch_symbol_stub(
        "Device:C", 232, 500, "C2", "10uF/25V",
        "Capacitor_SMD:C_0805_2012Metric"))
    # Output bulk cap 220uF
    parts.append(sch_symbol_stub(
        "Device:C", 300, 500, "C3", "220uF/16V",
        "Capacitor_SMD:CP_Elec_8x10.5"))
    # Output decouple 10uF
    parts.append(sch_symbol_stub(
        "Device:C", 308, 500, "C4", "10uF/6.3V",
        "Capacitor_SMD:C_0603_1608Metric"))
    # Feedback divider
    parts.append(sch_symbol_stub(
        "Device:R", 320, 505, "R1", "10k", "Resistor_SMD:R_0402_1005Metric"))
    parts.append(sch_symbol_stub(
        "Device:R", 320, 515, "R2", "3.3k", "Resistor_SMD:R_0402_1005Metric"))

    # ATX24 input
    parts.append(sch_symbol_stub(
        "palpod-compute-backplane:ATX24",
        140, 500, "J21", "ATX24 (+12V PSU input)",
        "palpod-compute-backplane:ATX24_HEADER"))
    # Second ATX24 for redundant PSU
    parts.append(sch_symbol_stub(
        "palpod-compute-backplane:ATX24",
        180, 500, "J22", "ATX24 (+12V PSU input B)",
        "palpod-compute-backplane:ATX24_HEADER"))

    # Power flags along the top of the sheet
    for i, name in enumerate(["+12V", "+5V", "+3V3", "+1V8", "+0V9"]):
        parts.append(sch_symbol_stub(
            f"power:{name}", 30 + i * 25, 15, f"#PWR{i+1:03d}", name, ""))
    parts.append(sch_symbol_stub(
        "power:GND", 30 + 5 * 25, 15, "#PWR006", "GND", ""))

    # A few illustrative wires + labels wiring up the buck-reg output rails
    wires = ""
    labels = ""
    # +12V from ATX24 to buck input (illustrative)
    wires += sch_wire(140, 495, 260, 495)
    labels += sch_label("+12V", 145, 493)
    # buck output to +5V rail label
    wires += sch_wire(280, 500, 320, 500)
    labels += sch_label("+5V", 285, 498)
    # PMBus from UCD90320 to BMC
    wires += sch_wire(820, 320, 1000, 320)
    labels += sch_label("PMBUS_CLK", 830, 318)
    wires += sch_wire(820, 325, 1000, 325)
    labels += sch_label("PMBUS_DAT", 830, 323)
    # 100GbE from BCM56780 to Ryzen0
    wires += sch_wire(500, 340, 480, 340)
    labels += sch_label("ETH0_TX_P", 460, 338)

    # Title block
    title = (
        "\t(title_block\n"
        "\t\t(title \"PAL Pod Compute Backplane\")\n"
        "\t\t(date \"2026-08-03\")\n"
        "\t\t(rev \"A0\")\n"
        "\t\t(company \"PAL Pod\")\n"
        "\t\t(comment 1 \"10x Jetson Orin NX (SODIMM MM70) + 10x AMD Ryzen AI 9 HX 370 (ExaMAX) + BCM56780 fabric\")\n"
        "\t\t(comment 2 \"14-layer stackup, 450x300mm, ENIG, ~3kW power distribution\")\n"
        "\t\t(comment 3 \"Reference: hardware/electrical/block-diagrams/compute-backplane.md\")\n"
        "\t\t(comment 4 \"PLACEHOLDER schematic - EE to complete wiring; SI engineer to route 100GbE + PCIe Gen5\")\n"
        "\t)\n"
    )

    body = (
        "(kicad_sch\n"
        "\t(version 20231120)\n"
        "\t(generator \"eeschema\")\n"
        "\t(generator_version \"8.0\")\n"
        f"\t(uuid \"{ROOT_SHEET_UUID}\")\n"
        "\t(paper \"A0\")\n"
        + title
        + lib_symbols
        + "".join(parts)
        + wires
        + labels
        + "\t(sheet_instances\n"
          "\t\t(path \"/\"\n"
          "\t\t\t(page \"1\")\n"
          "\t\t)\n"
          "\t)\n"
        ")\n"
    )
    (ROOT / f"{PROJECT}.kicad_sch").write_text(body)


# ---------------------------------------------------------------------------
# PCB (.kicad_pcb)
# ---------------------------------------------------------------------------

def build_pcb():
    # 14-layer stackup: F.Cu, GND, sig1, GND, sig2, PWR12V, PWR3V3, PWR1V8,
    # PWR_ANALOG, sig3, GND, sig4, GND, B.Cu
    inner_layers = [
        ("In1.Cu", "power", "GND1"),
        ("In2.Cu", "signal", "SIG1"),
        ("In3.Cu", "power", "GND2"),
        ("In4.Cu", "signal", "SIG2"),
        ("In5.Cu", "power", "PWR12V"),
        ("In6.Cu", "power", "PWR3V3"),
        ("In7.Cu", "power", "PWR1V8"),
        ("In8.Cu", "power", "PWR_ANALOG"),
        ("In9.Cu", "signal", "SIG3"),
        ("In10.Cu", "power", "GND3"),
        ("In11.Cu", "signal", "SIG4"),
        ("In12.Cu", "power", "GND4"),
    ]
    layers = "    (0 \"F.Cu\" signal)\n"
    for idx, (name, kind, usage) in enumerate(inner_layers, start=1):
        layers += f"    ({idx} \"{name}\" {kind} \"{usage}\")\n"
    layers += "    (31 \"B.Cu\" signal)\n"
    layers += (
        "    (32 \"B.Adhes\" user \"B.Adhesive\")\n"
        "    (33 \"F.Adhes\" user \"F.Adhesive\")\n"
        "    (34 \"B.Paste\" user)\n"
        "    (35 \"F.Paste\" user)\n"
        "    (36 \"B.SilkS\" user \"B.Silkscreen\")\n"
        "    (37 \"F.SilkS\" user \"F.Silkscreen\")\n"
        "    (38 \"B.Mask\" user)\n"
        "    (39 \"F.Mask\" user)\n"
        "    (40 \"Dwgs.User\" user \"User.Drawings\")\n"
        "    (41 \"Cmts.User\" user \"User.Comments\")\n"
        "    (42 \"Eco1.User\" user \"User.Eco1\")\n"
        "    (43 \"Eco2.User\" user \"User.Eco2\")\n"
        "    (44 \"Edge.Cuts\" user)\n"
        "    (45 \"Margin\" user)\n"
        "    (46 \"B.CrtYd\" user \"B.Courtyard\")\n"
        "    (47 \"F.CrtYd\" user \"F.Courtyard\")\n"
        "    (48 \"B.Fab\" user)\n"
        "    (49 \"F.Fab\" user)\n"
        "    (50 \"User.1\" user)\n"
        "    (51 \"User.2\" user)\n"
    )

    # Stackup — 14 copper layers, dielectrics between each pair.
    # Use Megtron 6 (M6) for the outer PCIe-critical dielectrics.
    stackup = "    (stackup\n"
    stackup += "      (layer \"F.SilkS\" (type \"Top Silk Screen\"))\n"
    stackup += "      (layer \"F.Paste\" (type \"Top Solder Paste\"))\n"
    stackup += "      (layer \"F.Mask\" (type \"Top Solder Mask\") (color \"Green\") (thickness 0.01))\n"
    stackup += "      (layer \"F.Cu\" (type \"copper\") (thickness 0.035))\n"
    # 13 dielectrics separating 14 copper layers
    for i in range(1, 14):
        upper = "F.Cu" if i == 1 else f"In{i-1}.Cu"
        lower = "B.Cu" if i == 13 else f"In{i}.Cu"
        stackup += (
            f"      (layer \"dielectric {i}\" (type \"prepreg\") "
            f"(thickness 0.15) (material \"Megtron 6\") "
            f"(epsilon_r 3.4) (loss_tangent 0.004))\n"
        )
        if i < 13:
            stackup += f"      (layer \"In{i}.Cu\" (type \"copper\") (thickness 0.0152))\n"
    stackup += "      (layer \"B.Cu\" (type \"copper\") (thickness 0.035))\n"
    stackup += "      (layer \"B.Mask\" (type \"Bottom Solder Mask\") (color \"Green\") (thickness 0.01))\n"
    stackup += "      (layer \"B.Paste\" (type \"Bottom Solder Paste\"))\n"
    stackup += "      (layer \"B.SilkS\" (type \"Bottom Silk Screen\"))\n"
    stackup += "      (copper_finish \"ENIG\")\n"
    stackup += "      (dielectric_constraints yes)\n"
    stackup += "      (edge_connector no)\n"
    stackup += "      (castellated_pads no)\n"
    stackup += "      (edge_plating no)\n"
    stackup += "    )\n"

    # Nets
    nets_list = [
        "GND", "+12V", "+5V", "+3V3", "+1V8", "+0V9",
        "PMBUS_CLK", "PMBUS_DAT", "PMBUS_ALERT_L",
        "SYS_RESET_L", "SYS_ALIVE",
        # PCIe Gen5 refclk
        "PCIE_REFCLK_P", "PCIE_REFCLK_N",
    ]
    # ETH_G0..G31 diff pairs (P/N pairs, TX+RX)
    for lane in range(32):
        for sig in ("TX_P", "TX_N", "RX_P", "RX_N"):
            nets_list.append(f"ETH{lane}_{sig}")
    # PCIe Gen5 lanes 0-7 from each of 10 Ryzen slots
    for slot in range(10):
        for lane in range(8):
            for sig in ("TX_P", "TX_N", "RX_P", "RX_N"):
                nets_list.append(f"RYZEN{slot}_PCIE{lane}_{sig}")
    nets_text = "  (net 0 \"\")\n"
    for i, n in enumerate(nets_list, start=1):
        nets_text += f"  (net {i} \"{n}\")\n"

    # Edge.Cuts rectangle 450x300, origin at (0,0), rect from (0,0) to (450,300)
    def edge(x1, y1, x2, y2):
        return (
            f"  (gr_line (start {x1} {y1}) (end {x2} {y2}) "
            f"(stroke (width 0.15) (type solid)) (layer \"Edge.Cuts\") "
            f"(uuid \"{uid()}\"))\n"
        )

    edges = (
        edge(0, 0, 450, 0)
        + edge(450, 0, 450, 300)
        + edge(450, 300, 0, 300)
        + edge(0, 300, 0, 0)
    )
    # Mounting holes at 4 corners (M3)
    def mount_hole(x, y):
        return (
            f"  (footprint \"MountingHole_M3\"\n"
            f"    (layer \"F.Cu\") (uuid \"{uid()}\") (at {x} {y})\n"
            f"    (attr through_hole)\n"
            f"    (pad \"1\" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers \"F&B.Cu\" \"*.Mask\") (uuid \"{uid()}\"))\n"
            f"  )\n"
        )
    mounts = "".join(mount_hole(x, y) for x, y in [
        (10, 10), (440, 10), (10, 290), (440, 290),
        (225, 10), (225, 290),
    ])

    silks = (
        f"  (gr_text \"PAL Pod Compute Backplane - Rev A0 - PLACEHOLDER\" "
        f"(at 225 20 0) (layer \"F.SilkS\") (uuid \"{uid()}\") "
        f"(effects (font (size 4 4) (thickness 0.6)) (justify left bottom)))\n"
        f"  (gr_text \"14-layer / ENIG / Megtron 6 / 450x300mm\" "
        f"(at 225 30 0) (layer \"F.SilkS\") (uuid \"{uid()}\") "
        f"(effects (font (size 2 2) (thickness 0.3)) (justify left bottom)))\n"
        f"  (gr_text \"See block-diagrams/compute-backplane.md for topology\" "
        f"(at 225 280 0) (layer \"F.SilkS\") (uuid \"{uid()}\") "
        f"(effects (font (size 1.5 1.5) (thickness 0.2)) (justify left bottom)))\n"
        f"  (gr_text \"Impedance-controlled routing of ETH/PCIe lanes required - see README\" "
        f"(at 225 290 0) (layer \"Cmts.User\") (uuid \"{uid()}\") "
        f"(effects (font (size 2 2) (thickness 0.3)) (justify left bottom)))\n"
    )

    body = (
        "(kicad_pcb\n"
        "  (version 20240108)\n"
        "  (generator \"pcbnew\")\n"
        "  (generator_version \"8.0\")\n"
        "  (general\n"
        "    (thickness 2.4)\n"
        "    (legacy_teardrops no)\n"
        "  )\n"
        "  (paper \"A2\")\n"
        "  (title_block\n"
        "    (title \"PAL Pod Compute Backplane - PCB\")\n"
        "    (date \"2026-08-03\")\n"
        "    (rev \"A0\")\n"
        "    (company \"PAL Pod\")\n"
        "    (comment 1 \"14-layer 450x300mm rectangular backplane\")\n"
        "    (comment 2 \"F.Cu / GND / SIG1 / GND / SIG2 / +12V / +3V3 / +1V8 / +ANA / SIG3 / GND / SIG4 / GND / B.Cu\")\n"
        "    (comment 3 \"Reference: hardware/electrical/block-diagrams/compute-backplane.md\")\n"
        "  )\n"
        "  (layers\n"
        + layers
        + "  )\n"
        "  (setup\n"
        + stackup
        + "    (pad_to_mask_clearance 0)\n"
        "    (allow_soldermask_bridges_in_footprints no)\n"
        "    (pcbplotparams\n"
        "      (layerselection 0x00000000_00000000_ffffffff_ffffffff)\n"
        "      (plot_on_all_layers_selection 0x00000000_00000000_00000000_00000000)\n"
        "      (disableapertmacros no)\n"
        "      (usegerberextensions no)\n"
        "      (usegerberattributes yes)\n"
        "      (usegerberadvancedattributes yes)\n"
        "      (creategerberjobfile yes)\n"
        "      (dashed_line_dash_ratio 12.000000)\n"
        "      (dashed_line_gap_ratio 3.000000)\n"
        "      (svgprecision 4)\n"
        "      (plotframeref no)\n"
        "      (viasonmask no)\n"
        "      (mode 1)\n"
        "      (useauxorigin no)\n"
        "      (hpglpennumber 1)\n"
        "      (hpglpenspeed 20)\n"
        "      (hpglpendiameter 15.000000)\n"
        "      (pdf_front_fp_property_popups yes)\n"
        "      (pdf_back_fp_property_popups yes)\n"
        "      (dxfpolygonmode yes)\n"
        "      (dxfimperialunits yes)\n"
        "      (dxfusepcbnewfont yes)\n"
        "      (psnegative no)\n"
        "      (psa4output no)\n"
        "      (plotreference yes)\n"
        "      (plotvalue yes)\n"
        "      (plotfptext yes)\n"
        "      (plotinvisibletext no)\n"
        "      (sketchpadsonfab no)\n"
        "      (subtractmaskfromsilk no)\n"
        "      (outputformat 1)\n"
        "      (mirror no)\n"
        "      (drillshape 1)\n"
        "      (scaleselection 1)\n"
        "      (outputdirectory \"gerbers/\")\n"
        "    )\n"
        "  )\n"
        + nets_text
        + edges
        + mounts
        + silks
        + ")\n"
    )
    (ROOT / f"{PROJECT}.kicad_pcb").write_text(body)


# ---------------------------------------------------------------------------
# Project file (.kicad_pro)
# ---------------------------------------------------------------------------

def build_project():
    net_classes = [
        {
            "name": "Default",
            "clearance": 0.2,
            "track_width": 0.2,
            "diff_pair_width": 0.2, "diff_pair_gap": 0.15, "diff_pair_via_gap": 0.15,
            "via_diameter": 0.6, "via_drill": 0.3,
            "microvia_diameter": 0.3, "microvia_drill": 0.1,
            "priority": 2147483647,
            "pcb_color": "rgba(0, 0, 0, 0.000)",
            "schematic_color": "rgba(0, 0, 0, 0.000)",
            "line_style": 0, "wire_width": 6, "bus_width": 12,
        },
        {
            "name": "HS_DIFF_100R",
            "clearance": 0.15,
            "track_width": 0.1,
            "diff_pair_width": 0.1, "diff_pair_gap": 0.1, "diff_pair_via_gap": 0.15,
            "via_diameter": 0.35, "via_drill": 0.15,
            "microvia_diameter": 0.3, "microvia_drill": 0.1,
            "priority": 20,
            "pcb_color": "rgba(0, 200, 255, 1.000)",
            "schematic_color": "rgba(0, 200, 255, 1.000)",
            "line_style": 0, "wire_width": 6, "bus_width": 12,
        },
        {
            "name": "PCIe_G5",
            "clearance": 0.2,
            "track_width": 0.1,
            "diff_pair_width": 0.1, "diff_pair_gap": 0.11, "diff_pair_via_gap": 0.2,
            "via_diameter": 0.35, "via_drill": 0.15,
            "microvia_diameter": 0.3, "microvia_drill": 0.1,
            "priority": 30,
            "pcb_color": "rgba(255, 0, 200, 1.000)",
            "schematic_color": "rgba(255, 0, 200, 1.000)",
            "line_style": 0, "wire_width": 6, "bus_width": 12,
        },
        {
            "name": "ETH_100G",
            "clearance": 0.2,
            "track_width": 0.09,
            "diff_pair_width": 0.09, "diff_pair_gap": 0.09, "diff_pair_via_gap": 0.2,
            "via_diameter": 0.35, "via_drill": 0.15,
            "microvia_diameter": 0.3, "microvia_drill": 0.1,
            "priority": 30,
            "pcb_color": "rgba(0, 255, 100, 1.000)",
            "schematic_color": "rgba(0, 255, 100, 1.000)",
            "line_style": 0, "wire_width": 6, "bus_width": 12,
        },
        {
            "name": "PWR_12V",
            "clearance": 0.4,
            "track_width": 1.0,
            "diff_pair_width": 0.2, "diff_pair_gap": 0.15, "diff_pair_via_gap": 0.15,
            "via_diameter": 1.2, "via_drill": 0.6,
            "microvia_diameter": 0.3, "microvia_drill": 0.1,
            "priority": 10,
            "pcb_color": "rgba(255, 0, 0, 1.000)",
            "schematic_color": "rgba(255, 0, 0, 1.000)",
            "line_style": 0, "wire_width": 6, "bus_width": 12,
        },
        {
            "name": "PWR_LOW_VOLTAGE",
            "clearance": 0.25,
            "track_width": 0.4,
            "diff_pair_width": 0.2, "diff_pair_gap": 0.15, "diff_pair_via_gap": 0.15,
            "via_diameter": 0.8, "via_drill": 0.4,
            "microvia_diameter": 0.3, "microvia_drill": 0.1,
            "priority": 15,
            "pcb_color": "rgba(255, 165, 0, 1.000)",
            "schematic_color": "rgba(255, 165, 0, 1.000)",
            "line_style": 0, "wire_width": 6, "bus_width": 12,
        },
    ]
    net_patterns = [
        {"netclass": "PWR_12V", "pattern": "+12V"},
        {"netclass": "PWR_LOW_VOLTAGE", "pattern": "+5V"},
        {"netclass": "PWR_LOW_VOLTAGE", "pattern": "+3V3"},
        {"netclass": "PWR_LOW_VOLTAGE", "pattern": "+1V8"},
        {"netclass": "PWR_LOW_VOLTAGE", "pattern": "+0V9"},
        {"netclass": "ETH_100G", "pattern": "ETH*"},
        {"netclass": "PCIe_G5", "pattern": "*PCIE*"},
        {"netclass": "PCIe_G5", "pattern": "PEX0_*"},
        {"netclass": "HS_DIFF_100R", "pattern": "USB*"},
        {"netclass": "HS_DIFF_100R", "pattern": "MGBE*"},
    ]
    pro = {
        "board": {
            "3dviewports": [], "design_settings": {
                "defaults": {
                    "board_outline_line_width": 0.15,
                    "copper_line_width": 0.2,
                    "copper_text_size_h": 1.5, "copper_text_size_v": 1.5, "copper_text_thickness": 0.3,
                    "courtyard_line_width": 0.05,
                    "dimension_precision": 4, "dimension_units": 3,
                    "dimensions": {"arrow_length": 1270000, "extension_offset": 500000,
                                    "keep_text_aligned": True, "suppress_zeroes": False,
                                    "text_position": 0, "units_format": 1},
                    "fab_line_width": 0.1, "fab_text_size_h": 1.0, "fab_text_size_v": 1.0,
                    "fab_text_thickness": 0.15,
                    "other_line_width": 0.15,
                    "other_text_size_h": 1.0, "other_text_size_v": 1.0, "other_text_thickness": 0.15,
                    "pads": {"drill": 0.4, "height": 1.0, "width": 1.0},
                    "silk_line_width": 0.12,
                    "silk_text_size_h": 1.0, "silk_text_size_v": 1.0, "silk_text_thickness": 0.15,
                },
                "diff_pair_dimensions": [
                    {"gap": 0.1, "via_gap": 0.15, "width": 0.1},
                    {"gap": 0.11, "via_gap": 0.2, "width": 0.1},
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
                    "footprint_symbol_mismatch": "warning",
                    "footprint_type_mismatch": "ignore",
                    "hole_clearance": "error", "hole_near_hole": "error",
                    "holes_co_located": "warning", "invalid_outline": "error",
                    "isolated_copper": "warning", "item_on_disabled_layer": "error",
                    "items_not_allowed": "error", "length_out_of_range": "error",
                    "lib_footprint_issues": "warning",
                    "lib_footprint_mismatch": "warning",
                    "malformed_courtyard": "error",
                    "microvia_drill_out_of_range": "error",
                    "missing_courtyard": "ignore", "missing_footprint": "warning",
                    "net_conflict": "warning", "npth_inside_courtyard": "ignore",
                    "padstack": "warning", "pth_inside_courtyard": "ignore",
                    "shorting_items": "error", "silk_edge_clearance": "warning",
                    "silk_over_copper": "warning", "silk_overlap": "warning",
                    "skew_out_of_range": "error", "solder_mask_bridge": "error",
                    "starved_thermal": "error", "text_height": "warning",
                    "text_thickness": "warning",
                    "through_hole_pad_without_hole": "error",
                    "too_many_vias": "error", "track_dangling": "warning",
                    "track_width": "error", "tracks_crossing": "error",
                    "unconnected_items": "error", "unresolved_variable": "error",
                    "via_dangling": "warning", "zone_has_empty_net": "error",
                    "zones_intersect": "error",
                },
                "rules": {
                    "max_error": 0.005, "min_clearance": 0.1,
                    "min_connection": 0.0, "min_copper_edge_clearance": 0.3,
                    "min_hole_clearance": 0.2, "min_hole_to_hole": 0.2,
                    "min_microvia_diameter": 0.2, "min_microvia_drill": 0.1,
                    "min_resolved_spokes": 2, "min_silk_clearance": 0.0,
                    "min_text_height": 0.8, "min_text_thickness": 0.08,
                    "min_through_hole_diameter": 0.3, "min_track_width": 0.09,
                    "min_via_annular_width": 0.075, "min_via_diameter": 0.35,
                    "solder_mask_to_copper_clearance": 0.0,
                    "use_height_for_length_calcs": True,
                },
                "teardrop_options": [
                    {"td_onpadsmd": True, "td_onroundshapesonly": False,
                     "td_ontrackend": False, "td_onviapad": True}
                ],
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
                     "td_width_to_size_filter_ratio": 0.9},
                ],
                "track_widths": [0.0, 0.09, 0.1, 0.15, 0.2, 0.4, 1.0],
                "tuning_pattern_settings": {
                    "diff_pair_defaults": {"corner_radius_percentage": 80, "corner_style": 1,
                        "max_amplitude": 1.0, "min_amplitude": 0.2,
                        "single_sided": False, "spacing": 1.0},
                    "diff_pair_skew_defaults": {"corner_radius_percentage": 80, "corner_style": 1,
                        "max_amplitude": 1.0, "min_amplitude": 0.2,
                        "single_sided": False, "spacing": 0.6},
                    "single_track_defaults": {"corner_radius_percentage": 80, "corner_style": 1,
                        "max_amplitude": 1.0, "min_amplitude": 0.2,
                        "single_sided": False, "spacing": 0.6},
                },
                "via_dimensions": [
                    {"diameter": 0.0, "drill": 0.0},
                    {"diameter": 0.35, "drill": 0.15},
                    {"diameter": 0.6, "drill": 0.3},
                    {"diameter": 1.2, "drill": 0.6},
                ],
                "zones_allow_external_fillets": False,
            },
            "ipc2581": {"dist": "", "distpn": "", "internal_id": "", "mfg": "", "mpn": ""},
            "layer_presets": [], "viewports": [],
        },
        "boards": [],
        "cvpcb": {"equivalence_files": []},
        "erc": {
            "erc_exclusions": [],
            "meta": {"version": 0},
            "pin_map": [
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
                [0, 2, 0, 1, 0, 0, 1, 0, 2, 2, 2, 2],
                [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 2],
                [0, 1, 0, 0, 0, 0, 1, 1, 2, 1, 1, 2],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 2],
                [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 2],
                [0, 2, 1, 2, 0, 0, 1, 0, 2, 2, 2, 2],
                [0, 2, 0, 1, 0, 0, 1, 0, 2, 0, 0, 2],
                [0, 2, 1, 1, 0, 0, 1, 0, 2, 0, 0, 2],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            ],
            "rule_severities": {
                "bus_definition_conflict": "error", "bus_entry_needed": "error",
                "bus_to_bus_conflict": "error", "bus_to_net_conflict": "error",
                "conflicting_netclasses": "error", "different_unit_footprint": "error",
                "different_unit_net": "error", "duplicate_reference": "error",
                "duplicate_sheet_names": "error", "endpoint_off_grid": "warning",
                "extra_units": "error", "global_label_dangling": "warning",
                "hier_label_mismatch": "error", "label_dangling": "error",
                "lib_symbol_issues": "warning", "missing_bidi_pin": "warning",
                "missing_input_pin": "warning", "missing_power_pin": "error",
                "missing_unit": "warning", "net_not_bus_member": "warning",
                "no_connect_connected": "warning", "no_connect_dangling": "warning",
                "pin_not_connected": "error", "pin_not_driven": "error",
                "pin_to_pin": "warning", "power_pin_not_driven": "error",
                "similar_labels": "warning", "simulation_model_issue": "ignore",
                "unannotated": "error", "unit_value_mismatch": "error",
                "unresolved_variable": "error", "wire_dangling": "error",
            },
        },
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
        "meta": {"filename": f"{PROJECT}.kicad_pro", "version": 1},
        "net_settings": {
            "classes": net_classes,
            "meta": {"version": 3},
            "net_colors": None,
            "netclass_assignments": None,
            "netclass_patterns": net_patterns,
        },
        "pcbnew": {
            "last_paths": {"gencad": "", "idf": "", "netlist": "",
                            "plot": "", "pos_files": "", "specctra_dsn": "",
                            "step": "", "svg": "", "vrml": ""},
            "page_layout_descr_file": "",
        },
        "schematic": {
            "annotate_start_num": 0,
            "bom_export_filename": "${PROJECTNAME}.csv",
            "bom_fmt_presets": [],
            "bom_fmt_settings": {
                "field_delimiter": ",", "keep_line_breaks": False, "keep_tabs": False,
                "name": "CSV", "ref_delimiter": ",", "ref_range_delimiter": "",
                "string_delimiter": "\"",
            },
            "bom_presets": [],
            "bom_settings": {
                "exclude_dnp": False,
                "fields_ordered": [
                    {"group_by": False, "label": "Reference", "name": "Reference", "show": True},
                    {"group_by": True, "label": "Value", "name": "Value", "show": True},
                    {"group_by": False, "label": "Datasheet", "name": "Datasheet", "show": True},
                    {"group_by": False, "label": "Footprint", "name": "Footprint", "show": True},
                    {"group_by": False, "label": "Qty", "name": "${QUANTITY}", "show": True},
                    {"group_by": True, "label": "DNP", "name": "${DNP}", "show": True},
                ],
                "filter_string": "", "group_symbols": True,
                "name": "Grouped By Value", "sort_asc": True, "sort_field": "Reference",
            },
            "connection_grid_size": 50.0,
            "drawing": {
                "dashed_lines_dash_length_ratio": 12.0,
                "dashed_lines_gap_length_ratio": 3.0,
                "default_line_thickness": 6.0, "default_text_size": 50.0,
                "field_names": [],
                "intersheets_ref_own_page": False, "intersheets_ref_prefix": "",
                "intersheets_ref_short": False, "intersheets_ref_show": False,
                "intersheets_ref_suffix": "",
                "junction_size_choice": 3, "label_size_ratio": 0.375,
                "operating_point_overlay_i_precision": 3,
                "operating_point_overlay_i_range": "~A",
                "operating_point_overlay_v_precision": 3,
                "operating_point_overlay_v_range": "~V",
                "overbar_offset_ratio": 1.23, "pin_symbol_size": 25.0,
                "text_offset_ratio": 0.15,
            },
            "legacy_lib_dir": "", "legacy_lib_list": [],
            "meta": {"version": 1},
            "net_format_name": "", "page_layout_descr_file": "",
            "plot_directory": "", "spice_current_sheet_as_root": False,
            "spice_external_command": "spice \"%I\"",
            "spice_model_current_sheet_as_root": True,
            "spice_save_all_currents": False,
            "spice_save_all_dissipations": False,
            "spice_save_all_voltages": False,
            "subpart_first_id": 65, "subpart_id_separator": 0,
        },
        "sheets": [[ROOT_SHEET_UUID, "Root"]],
        "text_variables": {"BOARD_REV": "A0", "PROJECT": "PAL Pod Compute Backplane"},
    }
    (ROOT / f"{PROJECT}.kicad_pro").write_text(json.dumps(pro, indent=2))


def build_libtables():
    (ROOT / "sym-lib-table").write_text(
        "(sym_lib_table\n"
        "  (version 7)\n"
        f"  (lib (name \"{PROJECT}\")(type \"KiCad\")"
        f"(uri \"${{KIPRJMOD}}/libraries/{PROJECT}.kicad_sym\")(options \"\")"
        "(descr \"PAL Pod compute-backplane project-local symbols (BCM56780, MM70 SODIMM, ExaMAX, UCD90320, Aries retimer, BMC, TPM, TPS, ATX24)\"))\n"
        ")\n"
    )
    (ROOT / "fp-lib-table").write_text(
        "(fp_lib_table\n"
        "  (version 7)\n"
        f"  (lib (name \"{PROJECT}\")(type \"KiCad\")"
        f"(uri \"${{KIPRJMOD}}/libraries/{PROJECT}.pretty\")(options \"\")"
        "(descr \"PAL Pod compute-backplane project-local footprints (placeholder outlines)\"))\n"
        ")\n"
    )


def main():
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    FP_DIR.mkdir(parents=True, exist_ok=True)
    write_kicad_sym()
    write_footprints()
    build_schematic()
    build_pcb()
    build_project()
    build_libtables()
    print("OK")


if __name__ == "__main__":
    main()

# Mic Array Reference Design

**Audience: a junior EE with 2 years of experience who can drive KiCad.**
This document should be enough to open KiCad, create a new project, and start
placing footprints on Monday morning.

## 1. Scope

- 13-mic dual-ring far-field array
- Always-on wake word (140 µA idle)
- Beamformed audio output over USB 3.0 (UAC 2.0)
- Fits inside a 150 mm × 150 mm PCB (round, or square with rounded corners)
- Powered from 5 V ± 5%, 500 mA max

## 2. Bill of materials (critical parts)

| # | Ref | Part | Mfg | Digi-Key p/n | Qty | Unit $ | Datasheet |
|--:|---|---|---|---|--:|--:|---|
| 1 | M1–M13 | ICS-41352 | TDK InvenSense | 1428-1063-1-ND | 13 | 2.10 | https://invensense.tdk.com/products/analog/ics-41352/ |
| 2 | U1 | XVF3800-INBW | XMOS | 906-XVF3800-INBW-ND | 1 | 12.50 | https://www.xmos.com/xvf3800/ |
| 3 | U2 | NDP120 | Syntiant | via Syntiant sales (not on Digi-Key retail) | 1 | 8.00 | https://www.syntiant.com/ndp120 |
| 4 | U3 | USB3320C-EZK-TR | Microchip | USB3320C-EZK-TR-ND | 1 | 4.20 | https://www.microchip.com/en-us/product/USB3320 |
| 5 | U4 | STM32G474RET6 | STMicro | 497-STM32G474RET6-ND | 1 | 6.80 | https://www.st.com/en/microcontrollers/stm32g474.html |
| 6 | U5 | TPS7A4700RGWR | TI | 296-38530-1-ND | 2 | 3.90 | https://www.ti.com/product/TPS7A47 |
| 7 | U6 | PI6C557-05LE | Diodes | 2156-PI6C557-05LEX-ND | 1 | 1.80 | clock fanout |
| 8 | U7 | ASTX-H11-24.576 | Abracon | 535-ASTX-H11-24.576MHZ-T-ND | 1 | 4.50 | 24.576 MHz TCXO |
| 9 | J1 | USB Type-C 24-pin | GCT | 2073-USB4110-GF-A-060-ND | 1 | 1.40 | — |
| 10 | J2 | Molex Pico-Clasp 5-pos | Molex | WM10113-05-ND | 1 | 0.60 | 5V power in |
| 11 | Passives | 0402/0603 | Yageo | — | ~200 | ~0.02 | 100 nF, 10 µF, 4.7 kΩ, etc. |
| 12 | ESD | TPD4S014 | TI | 296-25074-1-ND | 2 | 0.75 | USB + power ESD |

**Board cost (proto, 5 units)**: ~$180 per board (parts) + $200 setup + $65/board fab (JLCPCB 4-layer, 1-2 week) = ~$300 all-in per board at qty 5. At production qty 1000: ~$95/board.

## 3. PCB stackup

**4-layer, 1.6 mm total, ENIG surface finish.**

| Layer | Thickness | Content | Copper weight |
|---|---|---|---|
| L1 (top) | — | Component + signal | 1 oz |
| Dielectric | 0.20 mm FR4 | | |
| L2 | — | GND (unbroken plane) | 0.5 oz |
| Dielectric | 1.0 mm FR4 (core) | | |
| L3 | — | 3.3V / 1.8V power planes (split) | 0.5 oz |
| Dielectric | 0.20 mm FR4 | | |
| L4 (bot) | — | Signal + GND flood | 1 oz |

**Impedance targets**:
- USB 3.0 differential pairs: 90 Ω ± 10%
- USB 2.0 differential pair: 90 Ω ± 10%
- I2S/PDM single-ended: 50 Ω (not critical; just don't neck-down)

## 4. Placement guidance

```
                          FRONT (component side)
        +-----------------------------------------+
        |                                         |
        |          [M1 - outer ring]              |
        |     [M8]                    [M2]        |
        |                                         |
        |   [M7]      [MI1 inner]    [M3]         |
        |                                         |
        |   [M6]  [MI4]  [MC]  [MI2]  [M4]        |
        |                                         |
        |   [M6]      [MI3 inner]    [M4]         |
        |                                         |
        |     [M5]                    [M4]        |
        |                                         |
        |     +------------------------------+    |
        |     | U1 XVF3800 | U2 NDP120       |    |
        |     +------------------------------+    |
        |     | U3 USB3320 | U4 STM32G4      |    |
        |     +------------------------------+    |
        |                                         |
        |  [J1 USB-C]              [J2 power]     |
        +-----------------------------------------+
```

Mic layout follows `constants.scad`:
- 8 outer mics at R=60 mm, 45° pitch
- 4 inner mics at R=30 mm, 90° pitch, offset 45° from outer
- 1 center mic

## 5. Critical routing rules

1. **PDM clock skew < 5 mm** across all 13 mic instances. Route clock as star from U6 fanout buffer; length-tune each branch.
2. **USB 3.0 SS pairs (TX+/TX-, RX+/RX-)**: keep < 100 mm total, no vias if possible; if via required, use back-drilled or blind via.
3. **Analog domain (mic supply)** separated from digital domain (XMOS core supply) by a moat in the ground plane, bridged only under U5 LDOs.
4. **Crystal (Y1) placement**: within 5 mm of XMOS OSC pins; guard ring to ground.
5. **Mic ports** need through-hole acoustic ports drilled through the top plate — coordinate with mechanical designer for 1.2 mm port diameter and gasket seat.
6. **Decoupling**: 100 nF ceramic within 3 mm of every power pin on every IC. 10 µF bulk at LDO output.

## 6. Power sequencing

```
t=0:      5V input applied
t=1ms:    U5a LDO 3.3V analog stable  -> mics powered
t=2ms:    U5b LDO 1.8V digital stable -> XMOS + NDP120 powered
t=3ms:    STM32 reset released         -> firmware boots
t=10ms:   STM32 pulls XMOS boot select, releases XMOS reset
t=25ms:   XMOS running, streams PDM into DSP pipeline
t=50ms:   USB enumeration begins
t=100ms:  Ready
```

STM32 implements this sequence with GPIOs + delays. Do NOT use RC power-on-reset; use software-controlled sequencing so recovery from brown-out is deterministic.

## 7. Firmware bring-up (informational; not this doc's scope but referenced)

- XMOS firmware: XVF3800 EVK reference application (XMOS provides), configured for 13-mic dual-ring, mods for output stream format.
- NDP120 firmware: Syntiant Model Zoo "Alexa"-scale wake word (customer swaps for their own keyword).
- STM32 firmware: bare-metal C, HAL from STM32CubeMX, tasks: power sequencing, I2C bridge for user config, USB HID for diagnostics.

## 8. Test points (mandatory)

| TP | Signal | Access | Purpose |
|---|---|---|---|
| TP1 | 5VIN | test point pad | Input voltage check |
| TP2 | 3V3_ANA | pad | LDO output |
| TP3 | 1V8_DIG | pad | LDO output |
| TP4 | GND | pad × 4 | Scope ground |
| TP5 | PDM_CLK | pad | Clock verify |
| TP6 | PDM_DATA[0] | pad | First mic bit stream |
| TP7 | XMOS_RESET# | pad | Boot debugging |
| TP8 | STM32_SWD (SWDIO, SWCLK, GND, VCC) | 4-pin 1.27mm header | Firmware flash + debug |
| TP9 | USB_D+/D- | pad | USB scope point |
| TP10 | NDP120_WAKE_OUT | pad | Wake edge scope |

## 9. What KiCad libraries to install

- **kicad-symbols** (built-in) for passives and standard MCUs
- **XMOS library**: https://github.com/xmos/lib_xmos_kicad
- **Syntiant NDP120**: schematic symbol not published; hand-draw from datasheet pinout (48-pin BGA)
- **SnapEDA** for footprints of TDK ICS-41352, Cirrus CS43198, etc.
- **Ultra-Librarian** for STM32G4 footprints (STMicro sponsors)

## 10. First-week checklist for the junior EE

- [ ] Open KiCad 8, create new project `palpod-mic-array`
- [ ] Import symbol libraries listed in §9
- [ ] Sketch schematic sheets: power, MCU, XMOS, NDP120, USB, mic-array
- [ ] Run ERC (Electrical Rules Check); resolve all errors
- [ ] Place components per §4; route USB 3.0 pairs FIRST (they constrain everything)
- [ ] Route PDM bus star topology
- [ ] Pour ground planes; verify moats per §5
- [ ] Run DRC; verify 4-layer manufacturability
- [ ] Generate BOM CSV; cross-check against §2
- [ ] Order prototypes from JLCPCB (5 units, 4-layer, ENIG, 2-week)
- [ ] While waiting: bring up XMOS EVK on desk, port firmware skeleton

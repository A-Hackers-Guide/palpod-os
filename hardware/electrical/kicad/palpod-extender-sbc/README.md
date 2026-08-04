# PAL Pod Extender SBC - KiCad Project

Thin-client single-board computer for the half-scale PAL Pod extender: a
Rockchip RK3588 octa-core SoC (quad A76 + quad A55, 6 TOPS NPU) hosts 8 GB
LPDDR5-6400 (Samsung K3LKBFB0EM-MGCP), 128 GB Kingston EMMC128G-M525 eMMC 5.1,
a Realtek RTL8852BE Wi-Fi 6E + BT 5.3 module on M.2 A+E 2230, an RTL8125BG
2.5 GbE PHY, a Cirrus CS43198 stereo DAC feeding a TI TPA3255 315 W class-D
amp for the extender's soundbar + mini-sub, HDMI 2.1 out to the TV, MIPI DSI-2
to the 3.5" levitating orb OLED, USB 3.2 hosts, USB-C 3.2 with PD sink via an
Infineon CYPD3175 (CCG3PA) controller (STM32G071 backup power-seq MCU), and a
Rockchip RK806 companion PMIC for all rails. Also carries a UART link out to
the extender's mini-Halbach controller and a wake-mic pass-through. 8-layer
board, 100 mm x 100 mm, ENIG. See
`../../block-diagrams/extender.md` for the extender-level architecture -
this project is the KiCad implementation of that document for the extender
SBC daughterboard.

## How to open

Requires **KiCad 8.0.0 or later** (KiCad 9 and 10 also open the files cleanly;
we developed and validated against KiCad 10.0.5 on macOS).

```
open -a KiCad /private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/palpod-os/hardware/electrical/kicad/palpod-extender-sbc/palpod-extender-sbc.kicad_pro
```

Or double-click `palpod-extender-sbc.kicad_pro` in Finder. From KiCad's
project manager, open **Schematic Editor** and **PCB Editor**.

The project defines its own project-local symbol and footprint libraries in
`libraries/`; the `sym-lib-table` and `fp-lib-table` files at the project root
register them under the alias `palpod-extender-sbc`. Standard KiCad symbols
(`Device:R`, `Device:C`, `power:*`, `Connector:HDMI_A_Receptacle`,
`Connector:RJ45_MagJack`, `Connector:USB3_A_Receptacle`,
`Connector:USB_C_Receptacle_USB3.2`, `Connector:Barrel_Jack_Switch`,
`Memory_NAND:EMMC128G-M525`, `MCU_ST_STM32G0:STM32G071KBTx`,
`Interface_Ethernet:RTL8125BG`) are embedded in the schematic's
`lib_symbols` block so the schematic opens even if a fresh KiCad install has
not yet had its stock libraries configured; on first save KiCad will link
them back to the real stdlib entries.

## What's populated

- [x] `.kicad_pro` project settings:
    - **8-layer stackup declared in `net_settings` and the PCB itself**:
      F.Cu / In1.Cu = GND1 / In2.Cu = sig1 / In3.Cu = PWR_1V1 /
      In4.Cu = PWR_3V3 / In5.Cu = sig2 / In6.Cu = GND2 / B.Cu.
      1 oz copper outer, 0.5 oz inner, ENIG, ~1.6 mm total thickness.
    - Net classes with impedance targets:
        - `Default`  0.15 mm track / 0.4 mm via
        - `Power`    0.5 mm track / 0.8 mm via, 0.2 mm clearance
        - `USB`      0.11 mm track, 0.13 mm diff gap - **90 R differential** for USB 3.2 SS pairs and USB 2.0 D+/D-
        - `HDMI`     0.14 mm track, 0.15 mm diff gap - **100 R differential**
        - `LPDDR5`   0.09 mm track, 0.10 mm diff gap - **100 R differential + tight length-matching** (fly-by CK, tuned per byte-lane per RK3588 hardware guide)
        - `ETH`      0.15 mm track, 0.15 mm diff gap - 100 R differential for 2.5GbE MDI pairs
    - Auto-assign netclass patterns for `+12V/+5V/+3V3/+1V8/+1V1/+0V9`,
      `USB?_DP/USB?_DN/USBC_*/USB3_*`, `HDMI_TX*/HDMI_CLK*`, `LPDDR5_*`,
      `GMAC_MDI*`.
    - DRC minimums tuned for a proper 8-layer board with fine-pitch BGA fanout
      (0.09 mm min track, 0.3 mm min via, 0.075 mm annular ring, 0.15 mm
      microvia drill available).
- [x] `.kicad_sch` root schematic on A2, populated title block (rev A0,
  2026-08-03), embedded `lib_symbols` for every reference used, including the
  seven custom symbols in the project-local library and the eleven standard
  KiCad references.
- [x] Placed symbols (16 major ICs + connectors + illustrative passives):
    - `U1` RK3588 SoC (huge functional-block symbol with LPDDR5 CH0/CH1,
      HDMI 2.1 TX, MIPI DSI-2, dual USB 3.2, USB-C with SS lanes, PCIe 2.1
      to M.2, GMAC to the GbE PHY, eMMC 5.1, dual I2S, triple UART/I2C, SPI
      to the PMIC, and general-purpose GPIO all broken out as pin groups)
    - `U2` RK806 companion PMIC (10 buck + 7 LDO rail outputs, SPI/PWRON/INT
      to the SoC)
    - `U3` Samsung K3LKBFB0EM-MGCP 8 GB LPDDR5-6400 octa-die
    - `U4` Kingston EMMC128G-M525 128 GB eMMC 5.1
    - `U5` Cirrus CS43198 stereo DAC
    - `U6` TI TPA3255 315 W class-D amp
    - `U7` Realtek RTL8125BG 2.5 GbE PHY
    - `U8` STM32G071KBTx power-sequence / PD-backup MCU
    - `U9` Infineon CYPD3175 (CCG3PA) USB-PD sink controller
    - `M1` Realtek RTL8852BE Wi-Fi 6E + BT 5.3 on an M.2 A+E 2230 socket
    - `J1` HDMI Type-A receptacle (Molex 500254-1927)
    - `J2` RJ45 magjack with integrated transformer + LEDs (Bel L829-1J1T)
    - `J3` USB 3.2 Type-A host receptacle (right edge)
    - `J4` USB 3.2 Type-A host receptacle (left edge)
    - `J5` USB Type-C receptacle (Gen 2 SS + PD sink)
    - `J6` 5.5 x 2.1 mm barrel jack (CUI PJ-063AH) for 12 V input
    - 14x decoupling caps (bulk + local, mix of 10 uF / 100 nF / 220 uF), and
      4x illustrative resistors (HDMI HPD pullups + GbE 49R9 bias).
- [x] Power rail flags (`+12V/+5V/+3V3/+1V8/+1V1/+0V9/GND`) and 20+ pre-placed
  labels (`HDMI_TX0/1_P/N`, `LPDDR5_CH0_DQ0/1`, `USB0_DP/DN`, `USBC_DP/DN`,
  `GMAC_MDIO/MDC`, `EMMC_CLK/CMD`, `I2S0_BCLK/LRCK/SDO/SDI`,
  `UART_HALBACH_TX/RX`, `PMIC_INT_N`) plus 5-6 illustrative wires seeding
  the PMIC rail fanout on the schematic.
- [x] `no_connect` flags on three RK3588 test / reserved pins.
- [x] `libraries/palpod-extender-sbc.kicad_sym` - hand-drawn functional-block
  symbols for the seven specialty ICs (RK3588, RK806, RTL8852BE_M2, CS43198,
  TPA3255, CCG3PA, K3LKBFB0EM). Each is a large rectangular block with pin
  groups and the electrical types marked (`power_in`, `input`, `output`,
  `bidirectional`, `passive`). **The RK3588 and RK806 pin mappings are
  functional-group placeholders; the EE must verify each pin number and name
  against the Rockchip datasheets before wiring.**
- [x] `libraries/palpod-extender-sbc.pretty/` - seven placeholder footprints
  (see `libraries/palpod-extender-sbc.pretty/README.md` for the details and
  per-part verification checklist).
- [x] `.kicad_pcb` - **8-layer stackup declared** (F.Cu / In1.Cu = GND1 /
  In2.Cu = sig1 / In3.Cu = PWR_1V1 / In4.Cu = PWR_3V3 / In5.Cu = sig2 /
  In6.Cu = GND2 / B.Cu), copper thickness 1 oz outer / 0.5 oz inner,
  1.6 mm total, ENIG finish, black soldermask. **100 mm x 100 mm square
  board outline on Edge.Cuts.** Silkscreen title block, layer-stackup note,
  and comment-layer notes about LPDDR5 fly-by / HDMI 100 R / USB 90 R
  differential targets and RK3588 placement plan. 100+ nets pre-declared
  (power rails, HDMI, USB, LPDDR5, ETH, EMMC, I2S, MIPI DSI, etc). No
  footprints placed yet - the EE places them during layout.
- [x] `sym-lib-table` / `fp-lib-table` register the project-local
  `palpod-extender-sbc` library. Standard KiCad libraries are resolved from
  the user's KiCad install.

## What's stubbed / next steps for the EE

- [ ] **Verify placeholder footprints against real datasheets** before
  ordering fab. See `libraries/palpod-extender-sbc.pretty/README.md`. Highest
  risk: the RK3588 FCBGA-948 ball map (real RK3588 has non-uniform depopulated
  regions the placeholder doesn't model), the LPDDR5 FBGA-315 ball map, and
  the RK806 QFN-68 pad layout.
- [ ] **Verify placeholder pin mappings on the custom symbols** against the
  Rockchip RK3588 and RK806 datasheets (both are NDA-gated in places; use the
  Rockchip RK3588 hardware design guide as the primary reference), Cirrus
  CS43198, TI TPA3255, Infineon CCG3PA, Samsung K3LKBFB0EM, and Realtek
  RTL8852BE data sheets. Update the symbol pin numbers/names in
  `libraries/palpod-extender-sbc.kicad_sym` before wiring.
- [ ] Complete the schematic wiring:
    - **LPDDR5** CH0/CH1 fly-by CK + per-byte-lane DQS/DM tuning; ZQ
      terminations; RESET# and CKE topology per RK3588 hardware design guide.
    - **HDMI 2.1** four data pairs + clock pair + CEC + DDC (SCL/SDA) +
      HPD (with 10 k pulldown and ESD/level-shift on 5 V HPD line);
      length-tune to within 5 mm intra-pair, 25 mm inter-pair.
    - **USB 3.2** for each host receptacle: SSTX/SSRX + USB 2.0 D+/D- +
      VBUS with ESD protection (TPD4E02B04 or equivalent), current-limit
      switch, and CC1/CC2 handling (Type-A ports just need Rp).
    - **USB-C 3.2 with PD sink**: CCG3PA handles CC1/CC2 negotiation and
      VBUS pass to the 12 V/5 V rail selection; STM32G071 acts as backup
      power-sequencer if PD negotiation stalls. Mux the USB SS lanes to
      the RK3588's Type-C combo phy.
    - **PCIe 2.1 x1** to the M.2 A+E slot for the RTL8852BE (Wi-Fi/BT).
      Include 100 R diff termination, PERST#/CLKREQ# with pullups, and
      the 100 MHz REFCLK from the RK3588 PCIe PHY.
    - **RGMII / SGMII** from the RK3588 GMAC to the RTL8125BG (choose
      one per datasheet), then MDI0..3 diff pairs into the RJ45 magjack.
      Terminate LED drives at the RJ45's LEDs.
    - **eMMC 5.1** 8-bit bus with DS strobe; add 22 R series termination on
      CLK and CMD; keep DS/CLK length-matched.
    - **I2S** from RK3588 -> CS43198 (data + MCLK + BCLK + LRCK) and a
      separate I2S bus for the wake-mic pass-through header.
    - **TPA3255** BTL wiring for the extender's 4" full-range and 5" sub,
      LC output filters (per TI TIDA-01527), GVDD decoupling, and PBTL vs
      BTL mode select (M1/M2/M3).
    - **PMIC**: RK806 SPI control from RK3588 SPI0, PWRON#/RESETB/SLEEP
      sequencing, per-rail feedback, and 32 kHz RTC crystal.
    - **UART_HALBACH_TX/RX** breakout header (with ESD) to the extender's
      separate mini-Halbach controller board.
    - **Orb** interface: MIPI DSI-2 (4 lanes + clk) to the 3.5" OLED, an
      I2C sidechannel for touch/GPIO, and a 5 V rail with soft-start.
    - **12 V input** protection (TVS + reverse-polarity FET + soft-start
      + eFuse), 12 V -> 5 V buck (~5 A for the amp, ~2 A for the SoC
      subsystem via the PMIC's VSYS).
    - **JTAG + UART** debug headers on the RK3588 test pins and the STM32
      SWD.
- [ ] Run ERC (`kicad-cli sch erc palpod-extender-sbc.kicad_sch` or Tools ->
  Electrical Rules Checker). The current stub generates ~700 violations, all
  consequences of the unwired stubs; drive them to zero.
- [ ] Assign every schematic symbol a valid footprint (Tools -> Assign
  Footprints).
- [ ] Update the PCB from the schematic (Tools -> Update PCB from Schematic
  in the PCB editor).
- [ ] Place footprints on the 100 mm x 100 mm board:
    - RK3588 U1 centered.
    - LPDDR5 U3 on top edge, north of the SoC, oriented for shortest
      byte-lane fanout on In2.Cu (sig1).
    - eMMC U4 south of the SoC.
    - HDMI J1 + USB J3 + RJ45 J2 on the right edge.
    - USB-A J4 + barrel jack J6 + USB-C J5 on the left edge.
    - M.2 M1 on the bottom edge (Wi-Fi antenna clearance).
    - PMIC U2 near the SoC on the left; TPA3255 U6 + CS43198 U5 grouped in
      an analog corner top-right (keep away from LPDDR5 area for EMI).
    - STM32G0 U8 + CCG3PA U9 near the USB-C receptacle.
- [ ] Route USB SS + LPDDR5 differential pairs first (they constrain
  everything). Use the `USB` (90 R diff) and `LPDDR5` (100 R diff) net
  classes.
- [ ] Route HDMI TX0..3 + CLK differential pairs on `HDMI` (100 R diff).
- [ ] Pour GND on In1.Cu and In6.Cu; split In3.Cu into 1.1 V zones (VDD_LOG,
  VDD_CENTER, VDD_DDR); split In4.Cu into 3.3 V zones (VCC3V3_SYS,
  VCC3V3_IO, VCC3V3_AUDIO). Route sig1 (In2.Cu) as the primary LPDDR5 byte-
  lane layer; sig2 (In5.Cu) for HDMI/USB/PCIe.
- [ ] Run DRC to zero.
- [ ] Generate Gerbers + drill + BOM + pick-and-place (`File -> Fabrication
  Outputs`). Cross-check the BOM against `../../block-diagrams/extender.md`.
- [ ] Order 5-unit proto run from JLCPCB (8-layer, ENIG, ~3-week turn).

## Command-line validation

The project has been validated with `kicad-cli` 10.0.5:

```
kicad-cli sch export netlist -o /tmp/psbc.net palpod-extender-sbc.kicad_sch    # succeeds; ~700 ERC violations expected (unwired stubs)
kicad-cli pcb export gerbers -o /tmp/psbc-g/    palpod-extender-sbc.kicad_pcb  # succeeds; all 8 copper layers + soldermask + silk + paste + Edge.Cuts + drill export cleanly
kicad-cli sym export svg     -o /tmp/psbc-sym/  libraries/palpod-extender-sbc.kicad_sym    # renders all 7
kicad-cli fp  export svg     -o /tmp/psbc-fp/   libraries/palpod-extender-sbc.pretty       # renders all 7
```

## File format

- Schematic schema version `20231120` (KiCad 8)
- PCB schema version `20240108` (KiCad 8)
- Symbol library schema version `20231120`
- Footprint schema version `20240108`

Written in the `(hide yes)` effect-block form so the same files load
identically under KiCad 8, 9, and 10.

## Required KiCad libraries

Bundled with a stock KiCad 8+ install; no external download needed:

- `Device` (R, C)
- `power` (+12V, +5V, +3V3, +1V8, +1V1, +0V9, GND) - also embedded in the schematic for offline opening
- `Connector` (HDMI_A_Receptacle, RJ45_MagJack, USB3_A_Receptacle, USB_C_Receptacle_USB3.2, Barrel_Jack_Switch) - also embedded
- `Memory_NAND` (EMMC128G-M525) - also embedded
- `MCU_ST_STM32G0` (STM32G071KBTx) - also embedded
- `Interface_Ethernet` (RTL8125BG) - also embedded

The project-local `palpod-extender-sbc` library (registered by
`sym-lib-table` / `fp-lib-table`) holds the specialty ICs (RK3588, RK806,
RTL8852BE M.2, CS43198, TPA3255, CCG3PA, K3LKBFB0EM) and their placeholder
footprints.

## Reference

- **Extender block-level architecture:** `../../block-diagrams/extender.md`
- **RK3588 hardware design guide:** Rockchip developer portal (NDA)
- **Main PAL Pod mic-array daughterboard (sibling project):**
  `../palpod-mic-array/`

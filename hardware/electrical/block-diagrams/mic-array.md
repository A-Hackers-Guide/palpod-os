# Far-field mic array

## Block diagram

```mermaid
graph LR
    subgraph MICS[13 MEMS mics - TDK ICS-41352 - PDM output]
      M1[Outer 1]
      M2[Outer 2]
      MN[... Outer 8]
      MI1[Inner 1]
      MI4[... Inner 4]
      MC[Center 1]
    end

    MICS -->|PDM x13| CVT[PDM-to-I2S converter<br/>TDK MEMS use hardware PDM<br/>into XMOS PDM interface]
    CVT -->|13-ch I2S| DSP[XMOS XVF3800-INBW<br/>16-core xcore.ai<br/>dual-ring beamformer<br/>AEC + noise supp + BSS]

    DSP -->|1-ch cleaned<br/>+ 3-ch context| WAKE[Syntiant NDP120<br/>always-on wake word<br/>140uA average]

    WAKE -->|GPIO wake signal| HOST_IRQ[Host wake IRQ<br/>to Ryzen 0]
    DSP -->|USB Audio Class 2.0| USB[Microchip USB3320<br/>USB 3.0 hi-speed PHY]
    USB --> HOST[Ryzen 0 audio master]

    MCU[STM32G474 mgr<br/>I2C bus master<br/>power sequencing] --> DSP
    MCU --> WAKE
    MCU --> CVT

    PWR5[5V rail] --> LDO_3V3[TI TPS7A47<br/>ultra-low-noise LDO<br/>3.3V analog]
    PWR5 --> LDO_1V8[TI TPS7A47<br/>1.8V digital]
    LDO_3V3 --> MICS
    LDO_3V3 --> DSP
    LDO_1V8 --> DSP
    LDO_1V8 --> WAKE
```

## Layout notes

- 13 mics form **two concentric rings + center**:
  - **Outer ring**: 8 mics at R = 60 mm, 45° spacing
  - **Inner ring**: 4 mics at R = 30 mm, 90° spacing, rotated 45° from outer
  - **Center**: 1 mic at origin
- Chosen because it gives XMOS's dual-ring beamformer maximum spatial diversity across the frequency band (small ring for high-freq, large ring for low-freq).

## Clocking

- Single 24.576 MHz TCXO (Abracon ASTX-H11) feeds XMOS.
- XMOS generates PDM clock for all 13 mics via a fanout buffer (Diodes Inc PI6C557-05).
- Trace-length match all 13 PDM_CLK traces to < 5 mm skew.

See `../mic-array-reference-design.md` for the full BOM and PCB stackup.

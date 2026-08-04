# Extender — half-scale thin client

## Block diagram

```mermaid
graph TD
    AC[AC 100-240V mains] --> PSU[Meanwell HRP-300<br/>300W PSU<br/>12V rail]
    PSU --> PDB[Small PDB]

    PDB -->|12V| SBC[Rockchip RK3588<br/>Radxa Rock 5B SBC<br/>8GB LPDDR5 + 128GB eMMC]
    PDB -->|12V| AMP[TI TPA3255<br/>class-D 315W stereo]
    PDB -->|5V| MIC[Mic array 7 mics<br/>same XMOS + Syntiant chain]
    PDB -->|5V| LED[LED seam driver]
    PDB -->|5V| RADIO[Wi-Fi 7 M.2 module]
    PDB -->|5V inductive| ORBTX[Qi 2.0 15W transmitter]

    SBC -->|I2S| DAC[Cirrus CS43131 headphone/line DAC]
    DAC --> AMP
    AMP --> FR[4 inch full-range driver]
    AMP --> SUB5[5 inch sub, down-firing]

    SBC -->|USB| MIC
    SBC -->|Wi-Fi 7| MAIN[Main column<br/>media stream in]
    SBC -.->|Wi-Fi 7| ORB35[3.5 inch orb]
    ORBTX -.->|inductive| ORB35

    MCU[STM32G0<br/>power seq + fans] --> PDB

    style SBC fill:#1a3a5c,color:#fff
    style MAIN fill:#3a3a3a,color:#fff
```

## Key differences vs main

| Subsystem | Main | Extender |
|---|---|---|
| Compute | 10 Jetson + 10 Ryzen | 1 RK3588 SBC |
| DAC | Cirrus CS43198 | Cirrus CS43131 |
| Amp | Purifi 1ET7040SA (4 ch) | TI TPA3255 (2 ch) |
| Drivers | 3 soundbar arrays + 2 subs | 1 full-range + 1 sub |
| Mic array | 13 mics dual ring | 7 mics single ring |
| Orb | 7" 1440p | 3.5" 720p |
| Halbach | Yes | No — orb sits in a magnetic cradle without active levitation |
| PSU | 2x 1500W redundant | 1x 300W |
| Wireless | Wi-Fi 7 + BT 5.4 + Thread + UWB | Wi-Fi 7 + BT 5.4 |
| Cooling | Liquid + fans | Passive + 1 slow fan |

## Data flow with the main column

Extender is a **stateless thin client**. All media/AI computation runs on the
main. The extender receives:
- Encoded audio + video (HEVC / VVC) over Wi-Fi 7
- Beamformed mic uplink (Opus, 32 kbps)
- Presence/config metadata (JSON over WebSocket)

If the main column is offline, the extender falls back to a local wake-word
+ radio-playback mode using the RK3588 alone.

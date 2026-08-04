# System overview — MAIN column

Every top-level subsystem inside the main column and how it connects.
Extender is described separately in `extender.md`.

```mermaid
graph TD
    AC[AC 100-240V mains<br/>NEMA 5-15 inlet] --> PSU1[PSU-A<br/>1500W 80+ Titanium<br/>+12V, +5VSB]
    AC --> PSU2[PSU-B<br/>1500W 80+ Titanium<br/>hot-standby]
    PSU1 --> PDB[Power Distribution<br/>Board<br/>12V bus + eFuses]
    PSU2 --> PDB

    PDB -->|12V| COMPUTE[Compute Backplane<br/>10 Jetson Orin NX<br/>10 Ryzen AI 9 HX 370<br/>5TB DDR5 ECC, 35TB NVMe]
    PDB -->|12V| AMP[Purifi 1ET7040SA<br/>4-way active amp]
    PDB -->|12V| COOL[Pump + Fan Controller<br/>PWM, RPM feedback]
    PDB -->|12V| LEV[Levitation Driver<br/>Halbach coil stage]
    PDB -->|5V| MIC[Mic Array Board<br/>13x MEMS + XMOS + Syntiant]
    PDB -->|5V| LED[LED Seam Driver<br/>WS2815 amber]
    PDB -->|5V/12V| RADIO[Wireless Module<br/>Wi-Fi 7 + BT 5.4 + Thread + UWB]
    PDB -->|5V inductive| ORB_TX[Orb Inductive TX<br/>Qi 2.0 30W]

    COMPUTE -->|100GbE| SWITCH[Internal Switch Fabric<br/>Marvell Prestera 32-port]
    SWITCH --> RADIO
    SWITCH --> AMP
    SWITCH --> DAC[Cirrus CS43198 DAC<br/>32-bit 384 kHz]
    DAC --> AMP
    AMP --> SPK[3x Soundbar Arrays<br/>+ 2x Top Subwoofers]

    MIC --> SWITCH
    LEV --> SWITCH
    LED --> SWITCH

    ORB_TX -.->|inductive| ORB_RX[Orb<br/>7 inch curved OLED<br/>6 cams + depth + LIDAR<br/>nRF54H20 MCU]
    RADIO <-.->|Wi-Fi 7| ORB_RX
    LEV <-.->|Hall sensor<br/>+ UWB| ORB_RX

    COOL --> RAD[Radiator + 4x 120mm fans<br/>base plinth]
    COOL --> LOOP[Liquid Loop<br/>CPU/GPU cold plates]
    LOOP --> RAD

    style COMPUTE fill:#1a3a5c,color:#fff
    style AMP fill:#5c3a1a,color:#fff
    style ORB_RX fill:#3a1a5c,color:#fff
    style LEV fill:#5c1a3a,color:#fff
```

## Power domain summary

| Domain | Voltage | Peak current | Source |
|---|---|---|---|
| Compute rail | 12 V | 200 A (2400 W) | PDB from PSU |
| Audio amp rail | 12 V | 40 A (480 W) | PDB |
| Levitation coils | 24 V (boosted) | 8 A (192 W) | PDB via boost |
| Mic array | 5 V | 0.5 A (2.5 W) | PDB LDO |
| LED seams | 5 V | 3 A (15 W) | PDB |
| Wireless | 3.3 V + 5 V | 1 A | PDB LDO |
| Orb (inductive tx) | 12 V pri, 5 V sec | 2.5 A pri (30 W) | Qi 2.0 controller |

## Data topology

- **10 Jetson + 10 Ryzen** share a **PCIe Gen5 backplane** with cross-links via Marvell Prestera 32-port switch.
- **Audio** rides a dedicated **I2S bus** from the Ryzen designated as audio master to the CS43198 DAC (electrically isolated).
- **Mic array** returns beamformed audio as **USB 3.0** (UAC 2.0 class) to the audio-master Ryzen.
- **Orb link** is **Wi-Fi 7 6GHz** for A/V, plus a low-latency **BLE 5.4 sideband** for MCU control and Halbach servo feedback.
- **Wireless module** provides the outside-world links (Wi-Fi 7, BT 5.4, Thread 1.4, UWB).

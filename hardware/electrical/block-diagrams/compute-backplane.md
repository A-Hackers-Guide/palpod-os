# Compute backplane — 10 Jetson + 10 Ryzen

## Topology

```mermaid
graph LR
    subgraph BACKPLANE[PCIe Gen5 x16 Backplane PCB - 20 slots]
      subgraph JETSON[10x NVIDIA Jetson Orin NX - 16GB]
        J0[Orin 0]
        J1[Orin 1]
        JN[... Orin 9]
      end
      subgraph RYZEN[10x AMD Ryzen AI 9 HX 370 SoM]
        R0[Ryzen 0<br/>audio master]
        R1[Ryzen 1<br/>storage master]
        RN[... Ryzen 9]
      end
    end

    J0 --> SW[Marvell Prestera<br/>DX8500 32-port switch<br/>100/400GbE + PCIe fabric]
    J1 --> SW
    JN --> SW
    R0 --> SW
    R1 --> SW
    RN --> SW

    SW -->|100GbE| NIC[Uplink NIC<br/>SFP28 to outside world<br/>optional 400G QSFP]

    R1 -->|PCIe Gen5 x4| NVME[NVMe Storage Fabric<br/>10x 3.5TB Solidigm P5810<br/>35 TB total<br/>ZFS mirror + parity]

    R0 -->|I2S out| DAC[Cirrus CS43198 DAC]
    R0 -->|I2C ctrl| AMPCTRL[Amp Control Bus]

    DDR[5 TB DDR5-4800 ECC RDIMM<br/>distributed across all 20 SoMs<br/>256 GB per module average]

    JETSON -.->|per-module DDR| DDR
    RYZEN -.->|per-module DDR| DDR

    PWR[12V rail from PDB<br/>200A capable] --> BACKPLANE
    THERM[Cold plates<br/>1 per SoM] --> LOOP[Liquid loop]
```

## Backplane PCB spec

- **Layer count**: 16 layers minimum. Recommended stackup:
  - L1 signal (top, fine pitch)
  - L2 GND
  - L3 signal (impedance-controlled, 85 Ω differential)
  - L4 GND
  - L5 signal (impedance-controlled)
  - L6 12V power plane
  - L7 3.3V power plane
  - L8 GND
  - (mirror L9–L16)
- **Material**: Megtron 6 (M6) or Isola I-Speed for PCIe Gen5 loss budget. Standard FR4 will not close timing at 32 GT/s.
- **Impedance**: 85 Ω ± 5% differential for PCIe; 50 Ω ± 5% single-ended for I2S/I2C.
- **Trace length matching**: intra-pair skew < 5 mil; inter-pair skew < 25 mil per byte lane.
- **Retimers**: expect to need PCIe Gen5 retimers (Astera Labs Aries) at ~10 inches of trace. Confirm with a sim in Ansys SIwave or Cadence Sigrity.

## Connector selection

- **Slot connector**: Amphenol ExaMEZZ or Molex NearStack 74441 for PCIe Gen5 x16. Do not use commodity DIMM slots or M.2 for high-speed lanes.
- **Power**: dedicated 12V blade contacts (30A per SoM slot) — Molex Mega-Fit or Amphenol RADSOK.
- **Latching**: mechanical latch that provides positive engagement feedback (audible click); the SoMs are field-replaceable.

## Firmware boot flow (informational)

Ryzen 0 boots first (BIOS in a dedicated SPI flash), configures the switch,
then powers on the remaining SoMs in a staggered sequence via I2C (SMBus)
control lines to the PDB. Total cold-boot time budget: 25 s (audience-facing;
UX requirement).

## Failure modes / redundancy

- Any single SoM can fail; workloads redistribute via the OS layer.
- PSU is 1+1 hot-standby; loss of one PSU derates compute to 60% but stays up.
- NVMe fabric is ZFS RAID-Z2; two-drive failure tolerated.

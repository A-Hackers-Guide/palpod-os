# Top-level BOM summary — critical / long-lead / NRE parts

This is not the full BOM. It's the parts that will *either* delay the
program or blow the budget if the founder doesn't get quotes in early.

Assume MOQ / lead times are quoted for **500 units/year** production run.

## Long-lead-time watchlist (order by month 1 of NPI)

| Part | Purpose | Lead time (2026 est.) | Notes |
|---|---|---|---|
| NVIDIA Jetson Orin NX 16GB SoM | Compute (10 per unit) | 20–26 weeks | Allocation-limited; contact NVIDIA account team |
| AMD Ryzen AI 9 HX 370 SoM | Compute (10 per unit) | 16–20 weeks | Requires COM-HPC carrier; verify SoM vendor (SECO, congatec) |
| Marvell Prestera DX8500 switch ASIC | Internal fabric | 24–30 weeks | Marvell direct; no distribution stock |
| Solidigm P5810 3.5TB NVMe | Storage (10 per unit) | 12–16 weeks | — |
| LG P-OLED curved 7" panel | Orb display | 16–24 weeks | Custom; NRE ~$1.5M for panel tooling |
| Ouster REV7 mini LIDAR | Orb depth ring | 20+ weeks | Alternative: TFmini-S array (faster, lower res) |
| Purifi 1ET7040SA amp modules | 4 per unit | 12 weeks | Purifi direct; MOQ 100 |
| Cirrus CS43198 DAC | 1 per unit | 8–12 weeks | Digi-Key stock, but reserve at qty |
| XMOS XVF3800 | Mic array | 8 weeks | — |
| Syntiant NDP120 | Wake chip | 10–14 weeks | Syntiant direct; NDA + custom model NRE ~$50k |
| N52 NdFeB Halbach magnets | Levitation | 10–14 weeks | Custom magnetization pattern; K&J Magnetics or Arnold Magnetics |
| Qorvo DW3220 UWB radio | Orb tracking | 12 weeks | — |
| Qualcomm FastConnect 7800 | Wireless module | 16 weeks | Requires Qualcomm design agreement |
| Bent-laminated walnut panels | 4 curved panels per main | 6–8 weeks | Custom millwork; Baird Bros or similar |
| PVD-coated steel frames | Structure | 8 weeks (polish) + 3 weeks (PVD) | Two-stage vendor chain |
| Curved OLED cover glass (7") | Orb outer | 20 weeks | Corning custom or Schott D263T eco custom cut |

## NRE budget (one-time, per program)

| Line item | Est. USD |
|---|---:|
| LG OLED panel tooling | 1,500,000 |
| Custom Halbach magnet magnetization jig | 40,000 |
| Curved cover glass tooling | 200,000 |
| Injection-mold tooling for orb interior frame | 120,000 |
| Steel frame CNC fixture | 25,000 |
| PVD process qualification (color match, adhesion) | 40,000 |
| Syntiant custom wake-word model | 50,000 |
| PCB fab tooling (backplane, mic array, PDB, amp mgr) | 60,000 |
| Reg / certification (FCC + CE + UL + IEC) | 250,000 |
| **Total NRE (pre-first-unit)** | **~2,285,000** |

## Per-unit BOM cost estimate (MAIN)

| Category | Est. USD (production qty 500) |
|---|---:|
| Compute (10 Jetson + 10 Ryzen + backplane) | 12,500 |
| Memory (5TB DDR5 ECC RDIMM) | 6,500 |
| Storage (35TB NVMe) | 4,500 |
| Switch fabric | 800 |
| Audio (DAC + amps + drivers) | 3,200 |
| Orb (panel + optics + electronics + Halbach) | 5,500 |
| Mic array + wake chip | 350 |
| Wireless module | 220 |
| PSUs | 900 |
| Enclosure (steel + walnut + PVD + hardware) | 4,200 |
| Cooling loop | 800 |
| Cabling + connectors + misc | 700 |
| **Direct materials** | **~40,170** |

At a $95k retail: ~42% BOM-to-retail, which is aggressive for luxury but
possible given the direct-sale, no-dealer model. Add per-unit labor
(hand assembly + burn-in test) ~$2,500 → gross margin ~55%.

## Sources / distributors used above

- **Digi-Key**, **Mouser** — jellybean semis
- **Purifi Audio** — audio modules (direct)
- **XMOS** — direct sales (US: XMOS Inc., Austin)
- **Syntiant** — direct + NDA
- **NVIDIA Embedded** — via approved AI OEM partner (SECO, Advantech)
- **AMD Embedded** — via congatec / SECO / iBASE COM-HPC vendor
- **Marvell** — direct sales
- **LG Display Automotive/Custom** — direct (long qualification)
- **Corning / Schott** — direct
- **Vapor Technologies / Ionbond / Oerlikon Balzers** — PVD process
- **Baird Brothers / Rockler / Bell Forest** — walnut stock

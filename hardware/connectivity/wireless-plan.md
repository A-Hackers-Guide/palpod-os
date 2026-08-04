# Wireless plan

## Modules

| Function | Chip | Module | Notes |
|---|---|---|---|
| Wi-Fi 7 (2.4/5/6 GHz) | Qualcomm FastConnect 7800 | Compex WPU83Q or equivalent M.2 | Requires Qualcomm design agreement |
| BT 5.4 (LE Audio, Auracast) | Same FastConnect 7800 | Same module | LE Audio codec: LC3 mandatory |
| Thread 1.4 (matter fabric) | Silicon Labs EFR32MG24 | Separate module (dedicated antenna) | Border router role |
| UWB | Qorvo DW3220 | Custom PCB integrated with mic array board | For orb tracking + phone hand-off |

## Antenna plan

Column top plate is metal (steel + PVD) — hostile to RF. Antennas mount on
the **top plinth non-metal cap** (walnut with dielectric window) and in the
**base plinth intake grille recesses**.

| Antenna | Type | Frequency | Location | Gain |
|---|---|---|---|---|
| ANT1 | 2×2 MIMO PIFA | 2.4 / 5 / 6 GHz Wi-Fi | Top plinth, ±90° azimuth | 3 dBi |
| ANT2 | 2×2 MIMO PIFA | 2.4 / 5 / 6 GHz Wi-Fi | Base plinth diagonal | 3 dBi |
| ANT3 | Whip / monopole | 2.4 GHz Thread + BT | Top plinth | 2 dBi |
| ANT4 | UWB monopole | 6.5 – 8 GHz | Top plate center | 4 dBi |

Antenna cables: 1.13 mm micro-coax, U.FL to module. Length matched < 10 mm
between MIMO pairs.

## Wi-Fi 7 configuration for orb link

- **Dedicated 320 MHz channel** in 6 GHz UNII-5 (channels 5/21/37/53/69/85/101/117/133/149/165/181/197/213)
- MLO (multi-link operation) between 5 GHz and 6 GHz for reliability failover
- Beamforming: explicit compressed feedback, orb reports CSI at 100 Hz
- Encryption: WPA3-Personal (SAE) with 32-char generated key — user never sees it

## BT 5.4 LE Audio

- LC3 codec (mandatory)
- Auracast broadcast source — allows any paired BT LE Audio device (headphones, hearing aids) to receive the same stream, latency ~30 ms
- Peripheral role for the phone companion app pairing

## Thread 1.4

- Matter 1.3 controller role
- Border router: main column only (extenders participate as router-eligible endpoints if desired)
- Certifies via CSA (Connectivity Standards Alliance) Matter cert program

## UWB

See `uwb-orb-tracking.md`.

## FCC / CE pre-scan checklist

Before submitting to Element / TÜV / Intertek for full cert:

- [ ] Radiated emissions 30 MHz – 6 GHz, 3-meter chamber, EUT rotated, both polarizations
- [ ] Conducted emissions 150 kHz – 30 MHz on AC mains
- [ ] Wi-Fi TX EIRP measured, verified within FCC Part 15.407 limits for U-NII-5/6/7
- [ ] UWB emissions per FCC Part 15.517, verified peak < -41.3 dBm/MHz outside 3.1 – 10.6 GHz
- [ ] Antenna gain vs. transmit power: verify the composite EIRP < regulatory ceiling for each band
- [ ] SAR (Specific Absorption Rate) not required for stationary appliance (> 20 cm from user); document distance-of-use in filing
- [ ] Include a "labeled with FCC ID / CE mark" location design early — bottom of base plinth, hidden but accessible

## Known risks

- **Metal PVD enclosure** will detune antennas. Plan on 2–3 iterations of antenna placement + matching network tuning with an RF engineer.
- **Wi-Fi 7 in 6 GHz** is not universally available (still restricted in some CE markets in 2026). Provide a firmware region lock; ship EU units with 6 GHz disabled if needed.
- **Halbach permanent magnets** create a strong DC magnetic field near the orb link antennas. Verify no compass/antenna interference during EMC.

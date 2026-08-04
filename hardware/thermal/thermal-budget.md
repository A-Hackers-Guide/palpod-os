# Thermal budget

## Total heat dissipation

| Source | Nominal (W) | Peak (W) | Notes |
|---|---:|---:|---|
| Jetson Orin NX (× 10) | 200 | 500 | 20W nominal, 40-50W burst |
| Ryzen AI 9 HX 370 SoM (× 10) | 300 | 800 | 30W nominal, 65-80W burst (LLM inference) |
| DDR5 ECC (5 TB, active) | 100 | 200 | ~2W per 64GB DIMM active |
| NVMe (10× 3.5TB) | 40 | 70 | Solidigm P5810 4W nominal, 7W burst |
| Marvell switch ASIC | 50 | 70 | — |
| Purifi amps (class D, ~92% eff) | 40 | 120 | Dissipation = output × (1-eff) |
| PSU heat (96% eff at 50%) | 50 | 100 | Two PSUs |
| Levitation coils (I²R) | 30 | 80 | Continuous coil hold + servo |
| Orb (radiated → captured inside column?) | 0 | 0 | Orb dissipates in free air, negligible feedback |
| Everything else (LEDs, MCUs, DAC) | 20 | 40 | — |
| **TOTAL** | **~830** | **~1980** | |

## Cooling loop design

**Target**: keep every silicon junction < 85 °C at peak, < 65 °C at nominal, room 25 °C.

- **Loop type**: single closed-loop, dielectric-safe coolant (propylene glycol), no user maintenance in normal operation.
- **Pump**: EK Quantum D5 PWM (or equivalent), 1500 L/h max, 4 m head. Redundancy: none (accept risk; failure results in staged compute throttle within 30 s).
- **Reservoir**: 400 mL, mounted at top of loop for gravity fill.
- **Cold plates**:
  - 20× SoM cold plates (custom copper, ~30 × 30 mm each) — chained in parallel via micro-manifold to minimize dP.
  - 1× amp bay cold plate (spans all 4 Purifi modules).
- **Radiator**: 480 mm × 30 mm slim (Alphacool NexXxoS ST30 480 or EK CoolStream SE 480). Dissipation capacity ~500W per unit at 30°C dT, 1500 RPM fans. **Two radiators required** for the 2000 W peak → stacked in the base plinth.
- **Fans**: 8× 120mm PWM (4 per radiator, push-pull). Noctua NF-A12x25 (or equivalent quiet spec). Controlled by pump/fan MCU (STM32G0) with liquid-temp feedback.

## Fan curve target (for UX)

- 25 °C coolant → 400 RPM (barely audible, < 12 dBA @ 1 m)
- 35 °C → 700 RPM (18 dBA)
- 45 °C → 1200 RPM (28 dBA)
- 55 °C → 1800 RPM (38 dBA — audible, only under sustained peak)
- 65 °C → THROTTLE compute + max fans

## Loop hydraulics (calculate + verify)

- Coolant flow rate target: 1.0 L/min through each SoM cold plate (parallel × 20 = 20 L/min total).
- Pressure drop budget: 3.0 m head at 20 L/min (D5 handles this comfortably).
- Verify with a physical bench of the loop before the enclosure is closed up. Use a flow meter (Koolance INS-FM17).

## Thermal simulation targets (hand to mech EE)

- CFD (Ansys Icepak or Simcenter Flotherm): steady-state at nominal + peak.
- Boundary: 25 °C ambient, forced convection at intake, radiator + fan model.
- Verify no thermal hot spots > 90 °C at any silicon junction.
- Verify enclosure walnut interior surface < 40 °C (touch temperature safety).
- Verify orb Halbach permanent magnet < 60 °C (Curie margin).

## Failure modes

| Failure | Detection | Response |
|---|---|---|
| Pump stopped | Flow sensor pulse absent > 5 s | Warn, throttle compute 50%; hard-shutdown at 10 s |
| Coolant leak | Optical leak sensor (Watercool) in base | Immediate shutdown, cut compute rail |
| Fan failure (one) | RPM tach absent | Increase remaining fans; warn user |
| Radiator blocked (dust) | dT rise across radiator | UI prompt "clean filter"; escalate to throttle |
| Coolant depletion (evaporation over years) | Reservoir level sensor | Service reminder in UI at 90% level |

## Service interval

- Coolant: 24 months.
- Fan filter: 6 months (user-serviceable magnetic mesh).
- Pump: 5-year design life (owner-financed replacement or in-warranty swap).

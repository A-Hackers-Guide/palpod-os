# Certification Plan

For a device that sells in the US, EU, UK, Canada, Australia, and Japan,
the minimum viable cert set is:

| Cert | Scope | Required for | Est. cost | Timeline |
|---|---|---|---:|---|
| FCC Part 15 Subpart B | Unintentional radiator (compute) | US market | $12k | 6–8 weeks |
| FCC Part 15 Subpart C/E | Intentional radiator (Wi-Fi / BT / UWB / Thread) | US | $30k | 8–10 weeks |
| FCC Part 15.517 | UWB specifically | US | $8k | Included in above |
| ISED (Canada) RSS | Equivalent to FCC Part 15 | Canada | $6k | Parallel to FCC |
| CE (EU RED) | Radio Equipment Directive | EU | $35k | 10–12 weeks |
| UKCA | Post-Brexit UK | UK | $8k | Reuses CE data |
| RCM (Australia) | Combined AS/NZS certs | AU/NZ | $6k | Parallel to CE |
| MIC (Japan) | Radio equipment | Japan | $15k | 10–12 weeks |
| KCC (Korea) | Radio equipment | Korea (optional launch market) | $12k | 8–10 weeks |
| **UL 62368-1** | Safety of audio/video equipment | US, Canada, EU (via EN 62368-1) | $25k | 12–16 weeks |
| RoHS 3 (Directive 2015/863) | Substance restriction | EU + de-facto global | $2k self-declared | Ongoing |
| REACH SVHC | Substance disclosure | EU | $2k | Ongoing |
| WEEE | Take-back program | EU | Registration + per-country fee | Ongoing |
| CA Prop 65 | Warning labels | California | $3k | 4 weeks |
| ICNIRP low-freq magnetic exposure | Halbach levitation | Advisory (no forced cert) | $8k voluntary | 4 weeks |
| Energy efficiency (Energy Star for AV) | US | Optional; marketing win | $5k | 4 weeks |
| **Total (baseline global)** | | | **~$175k – 250k** | 6–9 months if serial; 3–4 months if parallel |

## Lab shortlist

- **Element** (formerly Washington Labs) — full-service, strong on radio, offices US + EU
- **TÜV Rheinland** — strong on EU RED + IEC 62368-1
- **Intertek** — global; often used for consumer AV
- **UL Solutions** — the source for UL 62368-1
- **Bureau Veritas** — good on APAC MIC / KCC
- **Nemko** — northern Europe / marine
- **CETECOM** — cellular + WLAN, though we have no cellular

Recommendation: **TÜV Rheinland** for radio + safety bundle (Fremont CA lab
handles both under one PM), + **UL Solutions** for UL 62368-1 mark.

## Test facility booking timing

- Book chambers **8 weeks before EVT-2** (engineering validation test).
- Full compliance testing on DVT (design validation test) samples, ~10
  weeks before mass production.
- Retest on PVT (production validation test) sample optional but wise if
  any board revs happened since DVT.

## Pre-scan strategy (in-house)

Rent a portable EMC test kit or partner with a local pre-scan chamber
(NTS Silicon Valley, Element Fremont hourly rate) to catch issues early:

- Compex Kikusui / Tektronix pre-compliance kit ~ $2k/day rental
- Pre-scan the mic array board and wireless module separately
- Pre-scan full system in shielded room before first formal chamber visit

Every dollar spent on pre-scan saves ~$5 in formal-cert retest fees.

## Product-specific concerns

### Halbach magnetic field

- Not a mandatory cert item, but the field is strong enough (surface >100 µT possible) that we voluntarily test to ICNIRP 2020 reference levels.
- Include a **pacemaker warning** in the user manual per FDA guidance on strong-field consumer products (advisory, not mandatory).
- Ship with a magnetic-field warning label per ISO 7010 W006 near the top plate.

### High-power PSU

- 3 kW total input capability triggers UL 62368-1 attention to over-current and thermal-runaway modes.
- Ensure the PSU vendor's UL/IEC 62368 report covers the exact configuration we ship (secondary certs sometimes needed when combining two PSUs).

### Wi-Fi 6 GHz (UNII-5/6/7/8)

- Regulatory landscape still changing in EU / UK / JP through 2026.
- Firmware region lock required; verify country-code obedience during cert.

### UWB in some markets

- China: UWB regulation TBD. Ship China units with UWB disabled unless
  MIIT approval landed by launch.

## Ongoing compliance

- Substance changes: any BOM sub triggers a REACH SVHC + RoHS re-attestation.
- Firmware updates that change RF behavior may require a permissive change letter to FCC.
- Annual sustaining budget: ~$20k for label refresh, RoHS attestations, minor changes.

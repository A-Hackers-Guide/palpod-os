# PALPod Roadmap

> **This roadmap is aspirational until funded.** Every quarter below assumes
> we close the raise on the timeline we're pitching. Read it as *the shape
> of the plan* — the specific quarters will slip in exact proportion to when
> the money lands. When a milestone moves, update this file rather than
> letting the discrepancy drift.
>
> The engineering ground truth — what's built, what's stubbed, what's demo
> only — lives in [`ATLAS.md`](ATLAS.md) §4. Do not read this roadmap
> without also reading that section.

---

## Q4 2026 — Foundation

- File provisional patent covering the Halbach + active-feedback levitation
  controller, the extender pairing protocol, and the on-device consent
  architecture for AI-initiated remote input.
- Form the legal entity (**PAL Pod, Inc.**) and set up counsel of record.
- Build the **first MVP demo unit** end-to-end per
  `palpod-mvp-plan.md` (60-day, ~$13.7k BOM). The demo unit uses a round
  flat OLED with the PAL face on it — the curved sphere OLED is not
  a Q4 2026 deliverable (see `ATLAS.md` §4).
- Shark Tank appearance — pitch is $2M for 15% (see `ATLAS.md` §4).

## Q1 2027 — First hires

- Close first three hires per `palpod-hiring-brief.md`:
  1. Senior Mechanical / Industrial Designer.
  2. Senior Hardware Electrical Engineer.
  3. Senior Embedded Firmware.
- Refine the six KiCad boards from "real schematics + auto-routed demo
  only" (their current state; see
  `hardware/PLACE-AND-ROUTE-REPORT.md`) into **fab-ready** designs.
  Sequence, simplest to hardest:
  1. `palpod-mic-array`
  2. `palpod-orb`
  3. `palpod-extender-sbc`
  4. `palpod-halbach-controller` (safety-critical — lockstep MCU pair)
  5. `palpod-audio-amp`
  6. `palpod-compute-backplane` (SI signoff required; last board any
     human should route)

## Q2 2027 — EVT

- **EVT run: 20 hand-built units.** These are Engineering Validation Test
  units — they exist to confirm the mechanical, electrical, thermal, and
  software integration are correct. They are not customer-shippable.
- Open the **waitlist with refundable deposits**. Cap deposits at 3x the
  planned first-shipment number so we don't over-sell EVT confidence.
- First round of full-system thermal, acoustic, and levitation-endurance
  testing on real hardware.

## Q3 2027 — DVT + certification

- **DVT (Design Validation Test) build.** Delta from EVT: manufacturing-
  ready CAD, real BOM sources, real vendor-supplied assemblies.
- **Certification test lab work begins.** FCC (Part 15B — unintentional
  radiator), CE (EMC), safety (UL / IEC 62368-1), acoustic (product noise
  emission). Follow `hardware/docs/CERTIFICATION-PLAN.md`.

## Q4 2027 — PVT

- **PVT (Production Validation Test) with the contract manufacturer.** The
  goal is a repeatable line — the same box comes off the CM's process
  every time.
- Firmware and OS lock candidates. Cut a `v1.0-rc` branch of PALPod OS.

## Q1 2028 — First shipments

- **First customer shipments begin.** These are the deposits placed in
  Q2 2027. Cadence starts slow (a handful per month) and scales as CM
  yield stabilizes.
- **Extender production starts.** Extenders ship separately from the main
  Pod and can be added to an existing customer install without a truck roll.

---

## Beyond Q1 2028

Not committed. Candidate directions include:

- Regional distributor pilot (still no dealer margins — see `ATLAS.md` §4
  "load-bearing decisions").
- Series A close and a second CM to derisk supply.
- A serious research budget for the **actual curved OLED sphere** (currently
  a $5M NRE that has not been paid — see `ATLAS.md` §4).

None of these should be pitched to a customer as a v1.0 promise.

---

## Non-goals (permanent)

Copied from `ATLAS.md` §6. These are load-bearing product commitments and
they do not appear on any future roadmap:

- No cloud dependencies. No telemetry. No update server we host.
- No subscription tier. No "PAL Premium." One purchase, one price, forever.
- No AI-initiated remote input without explicit user-tap consent.
- The Sphere face shows only its face — never UI, never streams.

# Welcome — Your First Week on PAL Pod

You are the first hardware engineer on the PAL Pod program. Congratulations,
and I'm sorry.

The founder has spent months architecting this thing on paper. Everything
you need to hit the ground running is in this repo. Nothing is a schematic
yet; nothing is a Gerber; nothing is in SolidWorks. That's your job. But
you don't have to guess at the architecture — it's all here.

## Reading order (day 1)

Read these in this order. Should take you a full day.

1. **`../README.md`** — package overview + disclaimers.
2. **`ARCHITECTURE.md`** — system-level, one hour.
3. **`../mechanical/dimensional-drawing.md`** — the envelope.
4. **`../electrical/block-diagrams/system-overview.md`** — the top-level block diagram.
5. **`../electrical/power-tree.md`** — the numbers that constrain everything.
6. **`../thermal/thermal-budget.md`** — the other numbers that constrain everything.
7. Skim every file in **`../electrical/block-diagrams/`**.

## Day 2

Open the OpenSCAD files in `../mechanical/` and preview them. Get an
intuition for the physical envelope. Export STLs. Load one into your
mechanical viewer of choice.

Read **`../electrical/mic-array-reference-design.md`** end to end. This is
the first board you're going to design.

## Day 3

Set up your workstation:

- **KiCad 8** (nightly if 8 isn't stable yet on your OS)
- **LTspice** for analog simulation
- **Saleae Logic 2** for the Logic Pro 8 you're about to expense
- **STM32CubeIDE** for the housekeeping MCUs
- **XMOS xTIMEcomposer** (or xcore.ai tools) for the mic array DSP
- **Ansys SIwave** or Cadence Sigrity — talk to me about licensing
- **A copy of these repos**, cloned locally

Order:
- 1× JLCPCB / Digi-Key stock: enough passives + STM32G474 dev board + XMOS XVF3610 EVK (closest to XVF3800 for early bring-up)
- 1× Rigol / Siglent 1 GHz scope with USB / I2S decode
- 1× Kikusui bench PSU with programmable ramp

Total workstation spend request: ~$8k. Prepare the PO.

## Days 4–5

Start the KiCad project for the mic array board. Follow the checklist at
the bottom of `mic-array-reference-design.md` §10. Aim to have the
schematic sheet skeleton (all sheets, no routing yet) done by end of week 1.

## First-week deliverables

- Complete workstation set up
- KiCad project `palpod-mic-array` created, all schematic sheets sketched
- Reading list above complete + annotated (note anything ambiguous)
- List of open questions ready for founder 1:1 (see below)

## First-week 1:1 with founder — questions to bring

Not exhaustive; add your own:

1. **Who owns the mechanical design?** The founder or a contract firm? If contracted, who has final DFM authority?
2. **Where are the ID (industrial design) renders?** They likely exist in Figma or a Rhino file; we need to reconcile against the OpenSCAD dimensions before they diverge further.
3. **Manufacturing partner shortlist** — has Foxconn / Flex / Jabil been engaged, or are we still shopping? EMS choice drives PCB rules, connector selection, and test strategy.
4. **NRE budget authority** — see `../electrical/bom-summary.md`. $2.28M pre-first-unit. Who signs?
5. **Cert lab preference** — see `CERTIFICATION-PLAN.md`. Any prior relationships?
6. **NPI schedule** — what's the target FCS (first customer ship) date? All schedule flows backward from that.
7. **Safety posture on the Halbach orb** — are we self-certifying to ICNIRP + posting warnings, or pursuing formal review with the FDA (magnetic-field consumer devices)?
8. **Firmware team** — same person as HW? Separate? Chip-vendor SDK licenses in hand?
9. **RMA plan year-1** — target attach rate, spare parts holding, MTTR promise. Drives service-friendly design choices in the enclosure.
10. **Software team's view of the compute fabric** — do they actually need heterogeneous compute, or is this a legacy decision? A 20× homogeneous Ryzen or 20× homogeneous Jetson would simplify the backplane enormously.

## What to expect from me (the founder / spec author)

- I've written down what I believe is needed. Assume I'm wrong in the details but right in the direction.
- Push back on anything that feels engineered around a vibe rather than a requirement. The Halbach orb is emotional; if you can't make it work, tell me early — we can build a shorter product but we can't ship a broken one.
- I will not micromanage your board design. Bring me trade-off decisions with data, not options with equal weight.

## Who else you'll work with

- **Mechanical designer** (TBD contract or hire): owns SolidWorks model, GD&T, DFM.
- **Industrial designer** (TBD): owns the Figma/Rhino ID model, color/material/finish.
- **Software architect**: owns the compute fabric software layer; you'll coordinate on backplane firmware handoff.
- **QA / cert PM**: TBD; likely a contractor for month 6+.

## Reference links

- KiCad 8 install: https://www.kicad.org/download/
- STM32CubeIDE: https://www.st.com/en/development-tools/stm32cubeide.html
- XMOS tools: https://www.xmos.com/xtimecomposer/
- OpenSCAD (for previewing our mechanical files): https://openscad.org/downloads.html
- IPC-2152 current calculator: https://www.ultracad.com/calc.htm
- ICNIRP 2020 low-freq exposure guidelines: https://www.icnirp.org/

## Final note

You are the only person who will read every one of these files this week.
That is what makes you the technical owner of the hardware. From now on,
when someone changes a dimension or a rail, that change goes through you.

Welcome. Let's build something worth $95k.

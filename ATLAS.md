# Hearth Atlas

_A reading-order index for anyone new to the project. Read this file first, then follow the reading order for your role. It is the front door — every doc, every board, every service is described here in the order it makes sense to encounter it._

---

## 1. What this file is

This is the front door. When a founder hires someone new — Mech/ID, Hardware EE, Embedded, Audio DSP, full-stack, PM — the first thing the founder does is send them the path to this file. It exists because the project has crossed the threshold where a single walkthrough conversation is not enough anymore. The tree is deep, the deliverables span physical CAD, six PCB projects, three Python services, a Docker-compose environment, and two external-facing published artifacts. Without an ordered path in, a new hire will read the wrong thing first, form a wrong mental model, and spend a week un-learning. This atlas tells you what to read, in what order, why, and — critically — what to trust, what is aspirational, and what is stale. If you are not the founder, do not skip this. If you are the founder, this exists for the people you are about to onboard; check it stays honest as the project moves.

---

## 2. Where the truth lives

There are three tiers of state to know about, because they persist very differently.

**Persistent — survives everything:**
- `~/.claude/projects/-Users-lexer-kindle/memory/palpod-project.md` — the founder's per-project memory file. Survives session termination, survives machine reboot, survives the scratchpad being wiped. This is the canonical index of what has been decided.
- `~/.claude/projects/-Users-lexer-kindle/memory/MEMORY.md` — the master memory index. If Hearth is one line in that index, it links to `palpod-project.md`.
- Published artifacts:
  - Spec sheet: https://claude.ai/code/artifact/0d37522d-4ec3-4538-a645-1fee3b988962
  - Investor pitch deck: https://claude.ai/code/artifact/5d1b17f6-fd3a-47d3-8e9c-986814a6a0d1
  
  These two URLs are the marketing surface. Treat them as the customer-facing source of truth for what the product IS. If an internal doc conflicts with the spec sheet, the spec sheet is authoritative for external claims; the internal doc is authoritative for engineering reality. When those diverge, the founder needs to know before either changes.

**Session-local — dies when the shell closes:**
- Everything under `/private/tmp/claude-501/-Users-lexer-kindle/80e67baf-6192-4db2-b491-aa5b4ee00c5b/scratchpad/` including the entire `palpod-os/` tree. The scratchpad is a session-scoped temp directory. It has already outlived several sessions by luck, but the correct assumption is that it will vanish. The founder should `git init` the `palpod-os/` directory and push it to a private GitHub repo before this session ends. Every hire should be told the GitHub URL as their first line of communication.

**In-your-head — the most fragile:**
- Trade-offs the founder made in conversation but didn't write down. This atlas exists partly to force those into text. See section 4 (aspirational / honest / load-bearing decisions).

---

## 3. Reading order by role

For each role, the order is deliberate. Do not skip ahead. If a Sr EE reads the pitch deck before `hardware/docs/FIRST-EE-DAY-ONE.md`, they will form the wrong picture of what their day-one task actually is. Investor language is designed to compress the vision; engineering language is designed to be built from.

### Founder (yourself)

You already know most of this. The atlas exists because your hires won't. Skim this file end-to-end once a month to keep it honest, and update section 4 whenever you make or reverse a load-bearing decision.

Your regular re-reads:
1. `palpod-mvp-plan.md` — remember what the 60-day demo unit actually is.
2. `palpod-hiring-brief.md` — remember which role you are still missing and what advisor you still owe an intro to.
3. `palpod-os/hardware/PLACE-AND-ROUTE-REPORT.md` — remember what the auto-routed demo is not.

### Senior Mechanical / Industrial Designer (first hire)

The first hire. The product is a physical object first — steel, walnut, mirror PVD, a levitating orb. You want the ID conversation grounded before the electrical conversation.

**Day 1** — get the shape of it in your head:
- `palpod-os/hardware/mechanical/BUILD.md` — how the column comes together, what the layers are, what the tolerances look like. Start here.
- `palpod-os/hardware/mechanical/palpod-main.scad` — the OpenSCAD source for the column. Open it in OpenSCAD.app; the STL at `palpod-os/hardware/exports/palpod-main.stl` is derived from it. If you have to choose between reading the SCAD and the STL, read the SCAD — the parametric intent is in the source.
- `palpod-os/hardware/mechanical/dimensional-drawing.md` — canonical dimensions. Any datasheet you make will trace back to this.
- `palpod-os/hardware/mechanical/materials-spec.md` — steel grade, walnut species, PVD finish, magnet grade. This is where the aesthetic decisions and the manufacturing decisions collide.
- `palpod-os/hardware/mechanical/constants.scad` and `modules.scad` — the shared vocabulary of the SCAD projects.

**Day 2** — get the context that isn't strictly ID:
- `palpod-os/hardware/docs/FIRST-EE-DAY-ONE.md` — read even though you're not the EE. It carries the cultural context of "we hand you populated schematics and no routing; that's the job." Same intent applies to CAD: you get valid OpenSCAD geometry, you rebuild it into a manufacturable SolidWorks model.
- `palpod-os/hardware/exports/palpod-main.png` and `palpod-extender.png` — quick visual of what the SCAD produces so you have the shape in mind before opening any CAD tool.

**Week 1** — get the physics right:
- `palpod-os/hardware/thermal/thermal-budget.md` and `airflow-diagram.md` — the compute stack throws serious heat. The column has to survive it silently. Your enclosure geometry is downstream of this.
- `palpod-os/hardware/docs/DFM-CHECKLIST.md` — the DFM constraints for CNC, PVD, wood finishing. Every dimension you set has to survive this checklist.
- `palpod-os/hardware/mechanical/palpod-extender.scad` and its exported STL — the extender is a smaller sibling of the main pod, shipped separately. Same design language.

**Month 1** — the deliverable:
- Rebuild the main pod and extender in SolidWorks (or Fusion) as a manufacturable, parametric assembly. The OpenSCAD tree is the reference geometry; SolidWorks is the production geometry. You own that conversion. When you're done, `palpod-manufacturing-rfq.md` (in the scratchpad root, not palpod-os) is what you send to the vendors listed there.

### Senior Hardware EE (second hire)

**Day 1** — the culture doc, then one board:
- `palpod-os/hardware/docs/FIRST-EE-DAY-ONE.md` — this is written for you. It says: six KiCad projects, populated schematics, zero PCB routing, no auto-router output should be trusted. Your job is real schematic wiring and real layout by a real EE.
- `palpod-os/hardware/electrical/mic-array-reference-design.md` — the reference-design walkthrough for the simplest of the six boards.
- Open `palpod-os/hardware/electrical/kicad/palpod-mic-array/` in KiCad 8+. Read the schematic. Read the custom symbol library. Note the stackup file, the board outline, the net classes with impedance targets. Every project has all of that; only routing is missing.

**Day 2** — the other five:
- Open in this order (simplest to hardest):
  1. `palpod-mic-array/` (4-layer, 120mm round, 13 MEMS + XVF3800 + NDP120) — already read.
  2. `palpod-orb/` (6-layer flex-rigid, 40×40mm rigid islands + flex bridges) — the levitating orb PCB.
  3. `palpod-extender-sbc/` (8-layer, 100×100mm, RK3588) — the extender's brain.
  4. `palpod-halbach-controller/` (4-layer, 150×100mm, lockstep STM32H723 pair) — safety-critical, redundant, this is what keeps a 2kg orb from falling. Read the schematic carefully.
  5. `palpod-audio-amp/` (6-layer, 250×200mm, 4× Purifi + 4× CS43198 DAC) — analog and power domains kissing on the same board. Careful.
  6. `palpod-compute-backplane/` (14-layer Megtron 6, 450×300mm, 10 SODIMM + 10 ExaMAX) — the monster. Do not attempt to reason about signal integrity here without Ansys or Sigrity in hand.
- `palpod-os/hardware/electrical/block-diagrams/` — the top-down view of how the six boards talk.
- `palpod-os/hardware/electrical/power-tree.md` — where every rail comes from and how it collapses under fault.
- `palpod-os/hardware/electrical/bom-summary.md` — what you're being asked to source.

**Week 1** — what to distrust:
- `palpod-os/hardware/PLACE-AND-ROUTE-REPORT.md` — this is important. There is an auto-routed demo (`PALPOD-ALL-BOARDS-ROUTED-DEMO.zip`) that came out of a headless place-and-route experiment. The pipeline works; the output is not manufacturable. This is documented explicitly. Do not send it to a fab. Read this report so you understand what "we have a fab package" means (`PALPOD-ALL-BOARDS-FAB.zip` was auto-generated from that same experiment — also demo, also not manufacturable).
- `palpod-os/hardware/docs/ARCHITECTURE.md` — the system-level electrical architecture.
- `palpod-os/hardware/docs/CERTIFICATION-PLAN.md` — FCC/CE roadmap, EMC pre-scan plan.

**Month 1** — the deliverable:
- Real schematic capture for the simplest boards (`mic-array` and `orb`), then real routed layouts. Then the extender SBC. Halbach controller before audio amp before compute backplane. The compute backplane is the last board any human should route, and probably not until we've had a full SI review.

### Senior Embedded Firmware (third hire)

**Day 1** — the state machine and the face:
- `palpod-os/pal-voice/README.md` — the orchestrator's contract with the rest of the system. This is your center of gravity.
- `palpod-os/pal-voice/palvoice/` — open the source. The state machine and the `Deps` class are the two things to internalize before you touch anything.
- `palpod-os/pal-face/README.md` — the pygame renderer for the round OLED. Nine expressions, WebSocket-driven from pal-voice.

**Day 2** — see the face light up on your desk:
- Run `palpod-os/pal-face/scripts/standalone-demo.sh` (or the equivalent in `pal-face/scripts/`) to bring up the face independently.
- Then start pal-voice pointed at it. Wake word, STT, LLM, TTS, all local. If a service tries to talk to the cloud, that is a bug.
- `palpod-os/docs/ARCHITECTURE.md` and `palpod-os/docs/SECURITY.md` — the system-level view. Read SECURITY.md carefully; the consent model is non-negotiable (see section 6).

**Week 1** — bring up the Halbach controller on the eval board:
- `palpod-os/hardware/electrical/kicad/palpod-halbach-controller/` schematic in view.
- The firmware for the STM32H723 lockstep pair is your primary target. Get it running on an eval board before we have hardware. When there is hardware, integrate.

**Month 1** — the orb hovers. The face reacts to voice. The extender pairs. Ownership boundaries with the EE and the ID hire become clear.

### Full-stack (future hire)

- `palpod-os/pal-web/README.md` — the FastAPI backend.
- `palpod-os/pal-web/palweb/routers/` — every endpoint. When the remote-desktop endpoints land, they will be in `remote.py` here.
- `palpod-os/pal-web/palweb/static/` — the frontend that ships with the box. Vanilla web, no build step in year 1.
- `palpod-os/docs/EXTENDER_PAIRING.md` — the pairing flow between main pod and extender.
- `palpod-os/README.md` at the OS root — install, architecture, service-ports table, remote desktop section.

### Product / GTM (future hire)

- Published spec sheet: https://claude.ai/code/artifact/0d37522d-4ec3-4538-a645-1fee3b988962
- Published pitch deck: https://claude.ai/code/artifact/5d1b17f6-fd3a-47d3-8e9c-986814a6a0d1
- `palpod-mvp-plan.md` (in scratchpad root, not `palpod-os/`) — the 60-day, $13.7k BOM demo unit plan.
- `palpod-sharktank-demo-script.md` (in scratchpad root; being written by a sibling agent — expect it to be there) — the on-stage demo script.
- `palpod-hiring-brief.md` — team plan, salaries, advisor targets. Read this to know who is coming and who has said yes.

---

## 4. What's stale, what's aspirational, what's honest

This section is the most important one for a new hire. Read it slowly.

### Aspirational — do NOT ship as-is

- **Custom curved OLED sphere.** The spec sheet claims a spherical OLED face. That is a $5M NRE that has not been paid and no vendor has been engaged. The demo unit uses a round flat OLED with the Hearth face rendered on it and a curved cosmetic bezel. Do not tell customers the sphere ships in year one.
- **Halbach levitation of a 2kg orb.** Levitation of a 2kg mass with a Halbach + active feedback array is a real research problem. We have a controller PCB design (`palpod-halbach-controller`) but not a functioning levitation rig. Do not promise levitation on stage until we have a demo that runs for 30 minutes without human intervention.
- **5 TB DDR5 ECC RDIMM.** The spec sheet lists this as a headline number. It is achievable — but only on a server-class platform (Xeon Sapphire Rapids / EPYC Genoa) with real RDIMM sockets. That is not what the compute backplane KiCad project sketches. Anyone reading the KiCad and thinking "this will boot with 5 TB of RAM" is wrong.
- **HBM3e memory anywhere.** If you see HBM3e mentioned in any doc, that is fabricated context bleeding through from an earlier draft. HBM is on-die with the accelerator; it does not appear as a discrete component on a PCB. Delete on sight.
- **The compute backplane's PCIe Gen5 SI budget.** The stackup and net classes have targets. The targets have never been validated in simulation. Do not send this board to fab without an Ansys or Sigrity signoff.

### Honest but incomplete

- **All 6 KiCad projects.** Populated schematics, real symbols, real footprints, correct stackup, board outline, net classes with impedance targets, a Gerber-shaped fab package produced by an experimental auto-router. NO real PCB routing. The EE's day-one work is real routing.
- **`palpod-os/hardware/PLACE-AND-ROUTE-REPORT.md` and `PALPOD-ALL-BOARDS-ROUTED-DEMO.zip`.** The pipeline that produced these works end-to-end. The output is demo-only garbage. Explicitly documented as such. Do not send to fab. Do not show to a customer. Show to an investor only as a "we can automate a lot of this someday" story.
- **`palpod-mvp-plan.md`.** This is real. 60 days, $13.7k BOM, buildable. If we hire the three roles in `palpod-hiring-brief.md` next month, the demo unit exists by mid-October.
- **`palpod-manufacturing-rfq.md`.** Real vendor contact info. You can send this today. If we push the RFQ before the schematics are finished, we are asking for quotes on documents that will change; time the send.
- **Extender pairing flow (`palpod-os/docs/EXTENDER_PAIRING.md`).** The endpoints exist. Real cryptographic pairing has been sketched but not implemented. There is a TODO on the actual token-rotation step.

### Load-bearing decisions the founder has committed to

These are settled. Do not re-open them without cause.

- **RustDesk primary, AnyDesk optional.** Self-hosted remote desktop is the ethos; AnyDesk is opt-in only for customers who insist. `configs/rustdesk/` is the source of truth.
- **Session-scoped consent for AI-initiated remote input.** No exceptions. The AI can suggest a click; the human confirms. See section 6.
- **Direct-to-consumer, no dealer network year 1.** We ship one unit at a time. No distributor discounts, no dealer margins.
- **$2M for 15% ask.** The Shark Tank pitch is settled. Do not renegotiate with yourself between now and the shoot.
- **HearthOS built on TrueNAS SCALE.** Not Ubuntu Server, not bare Debian. TrueNAS SCALE is the production target. The docker-compose is the interim development bring-up.
- **Face aesthetic committed: an original animated companion face.** Cyan-blue OLED. Pill-shaped eyes. Cup-shaped smile. Nine expressions. Do not redesign the face. If a hire wants to change the face, they need a conversation with the founder before they touch pal-face.

---

## 5. What to do first when the scratchpad state has been lost

The scratchpad tree lives in `/private/tmp/`. macOS clears `/private/tmp/` on schedule. Future sessions may find the entire `palpod-os/` tree gone. If that happens:

1. Read `~/.claude/projects/-Users-lexer-kindle/memory/palpod-project.md`. It survives. It links to the persistent artifact URLs.
2. WebFetch each artifact URL to reconstruct the current customer-facing spec and pitch:
   - https://claude.ai/code/artifact/0d37522d-4ec3-4538-a645-1fee3b988962
   - https://claude.ai/code/artifact/5d1b17f6-fd3a-47d3-8e9c-986814a6a0d1
3. If the founder has by then pushed to GitHub — `git clone` the repo. That is the whole tree back. If they have not (a failure of process worth naming; this atlas is asking you to fix it before it happens), start over from the descriptions in `palpod-project.md`.
4. Check `/Applications/` for CAD/EDA tools that have already been installed in prior sessions: OpenSCAD, KiCad, FreeCAD, Blender. Do not reinstall from scratch; the founder has these already.

---

## 6. Non-negotiable boundaries for hires

These are not preferences. They are the product. A hire who violates one of these is having a code review that ends with a rewrite.

- **No AI-initiated remote input without explicit user-tap consent.** The remote-desktop endpoints (landing in `pal-web/palweb/routers/remote.py`) check an `X-Consent-Origin` header. Any code path that skips or fakes that check is a safety bug. The AI can propose an action; the human's actual finger on an actual screen approves it. This is the safety property that lets a $95k box sit in a customer's home and do real things without anyone getting sued.
- **No cloud dependencies added anywhere.** No AWS SDK. No third-party analytics. No "helpful" webhook to a status server. No telemetry. No update server we host. If a service can't run entirely offline on the customer's own hardware, it can't run at all. This is why we are $95k and not $9,500 with a subscription.
- **The sphere shows only its face.** Never any UI. Never any game content. Never a remote-desktop stream. Never a notification. The face is the face. Streams and UI go to TVs and extenders. This is a hard product rule. Break it and the product stops being the product.
- **No new subscription revenue models.** The buyer paid $95k. Everything they need is included, forever, on their hardware. No SaaS layer, no premium tier, no cloud storage upsell, no "Hearth Premium." If a Series A investor pushes for one, the answer is no. The whole thesis is that we sell one thing at a high price and never come back for more.

---

## 7. Links to the atlas of the atlases

- Persistent memory: `~/.claude/projects/-Users-lexer-kindle/memory/palpod-project.md`
- Memory index: `~/.claude/projects/-Users-lexer-kindle/memory/MEMORY.md`
- Published spec sheet: https://claude.ai/code/artifact/0d37522d-4ec3-4538-a645-1fee3b988962
- Published pitch deck: https://claude.ai/code/artifact/5d1b17f6-fd3a-47d3-8e9c-986814a6a0d1
- MVP plan: `../palpod-mvp-plan.md` (relative to this file) or `scratchpad/palpod-mvp-plan.md`
- Manufacturing RFQ: `../palpod-manufacturing-rfq.md`
- Hiring brief: `../palpod-hiring-brief.md`
- Shark Tank demo script: `../palpod-sharktank-demo-script.md` (sibling-agent output; expect present)
- This file: `palpod-os/ATLAS.md`

---

_A note on tone: this file is written directly, sometimes bluntly. That is deliberate. New hires get one honest map of the terrain, not a marketing tour. If the map is wrong, tell the founder and it changes. Do not paper over it._

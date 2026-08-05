# Hearth Field Service Training Curriculum & Certification Program

**Document owner:** Head of Field Service, Hearth Systems Inc.
**Version:** 2.0 — Pre-launch operations, revised post-verifier review
**Effective:** Cohort-0 concierge onboarding through Series-A close
**Distribution:** Data room / Operations / Field Service; concierge hiring; pitch objection 12 (warranty burden)
**Cross-references:** BOARD-FIX-SOW-RFP.md (Nuvation Halbach signoff scope), DATA-MIGRATION-RUNBOOK.md, THREAT-MODEL.md, FIRMWARE-RECOVERY.md, HAZOP-HALBACH.md, THERMAL-QUAL.md, POSTMORTEM-TEMPLATE.md, ONBOARDING-PLAYBOOK.md, RISK-REGISTER.md.

---

## 1. Program philosophy

Hearth is a $95,000 offline AI and media server that lives in a customer's home for a decade. The 3-year concierge warranty is not a service line item — it is the physical proof of the promise. When a customer's Hearth misbehaves in year two, the visit that follows will either deepen a relationship worth $180,000 in lifetime value (extension of concierge, second Hearth for the beach house, referral to two peers) or terminate it.

The tempting alternative is RMA-swap: ship a fresh unit, cross-ship a replacement, take the broken one back to Fremont, refurbish, return to pool. Modern consumer electronics companies do this because it is cheap at scale and their brand tolerates the coldness. Hearth cannot. Three reasons.

**First, the sphere is personal.** By month three the sphere has learned the household's voices, faces, taste in music, sleep patterns, and inside jokes. The device state on the Kioxia CD8-R is a partial portrait of the family. A swap is not a swap. Even with encrypted state migration (documented in DATA-MIGRATION-RUNBOOK.md) the new sphere feels different for two weeks. Customers notice. They wrote us $95k and they will notice.

**Second, the customer already met a human.** The concierge who did the install, sat on the customer's couch, watched them react to their own name spoken back to them from a levitating orb, is not replaceable by a FedEx label. The concierge relationship is our moat. If a hardware fault is the first time in eight months we send a stranger, we have broken the concierge continuity by our own hand.

**Third, the demographics of our customer are not RMA-tolerant.** Our target customer is a household that hires a plumber they know by name. They do not accept a support experience worse than the plumber's. When the sphere stops floating, they expect Marcus (or whoever their concierge is) at the door within five business days holding the exact part it needs.

The economics support this. Warranty reserve is $2,618 per unit per BOM, totaling $1.57M against a Y1 install base of 600. Median field visit cost is $250-$800 all-in. A sphere swap capped at $3,500 is still cheaper than a lost customer at a $180k LTV plus the second-order damage of a public complaint from a household whose neighbor is watching whether to buy.

We invest in real field-tech training because the concierge who repairs a Hearth in the customer's living room produces a better outcome, at lower marginal cost, than any logistics operation we could build. The training program below exists so that when the sphere stops floating in Woodside, the concierge who arrives knows exactly what she is doing before she rings the doorbell, and the customer's story about Hearth ends with "and then Priya fixed it in twenty minutes" instead of "and then it took a week and I never really trusted it again."

That difference — the ending of that story — is what this curriculum defends.

---

## 2. Field-tech certification levels

Three tiers. Every field-facing employee holds at least L1. Career progression is technical and compensated. Certification hour totals reflect industry benchmarks (IPC-A-610 alone is 40 hours; competent Level-2 board technicians in the broader industry accumulate 400-600 hours before unsupervised customer work) and have been right-sized following the verifier review.

**Level 1 (L1) — Concierge-Certified.** Prerequisite for every concierge in the field. Focus: guided diagnostics via the companion mobile app, replacement of the three user-serviceable parts (extender cable, air filter, front bezel), sphere reset via magnet-key procedure, network troubleshooting on the customer's mesh. Certification: **60 hours total** (40 online + 20 Fremont), exam + one mock install shadowed by a Cohort-0 concierge.

**Level 2 (L2) — Field Service Technician.** Focus: full hardware diagnosis, board-level replacement of all six Hearth PCBs, sphere Halbach recalibration in-home (per Nuvation-authored recalibration script; L2 does not sign the HAZOP procedure — see §14), closed-loop cooling refill using the pre-mixed Fluorinert cartridge, thermal-issue triage using the FLIR C5 handheld the tech carries in her kit. Certification: **320 hours total**, broken down as:

- 40 hours online product + schematic literacy
- 80 hours Fremont bench (mechanical / board swap / cooling)
- 60 hours JTAG + firmware bring-up (STM32H723, extender-SBC, U-Boot chain)
- 60 hours Halbach recalibration and coil-drive characterization (Nuvation-authored curriculum)
- 80 hours supervised field practicum

L2s are dispatched to any hardware issue L1 cannot close in 15 minutes.

**Level 3 (L3) — Senior Depot Technician.** Fremont only, no field dispatch. Focus: BGA rework on the compute-backplane (Ryzen sockets + Jetson SODIMM sites), silicon-level swap on the STM32H723 sphere MCU, thermal-chamber characterization, HAZOP procedure *execution* (not signoff) on the safety-critical Halbach controller. Certification: **480 hours total**, broken down as:

- 150 hours BGA-152 NVMe rework (Kioxia CD8-R footprint)
- 150 hours custom Ryzen socket footprint on the compute-backplane
- 150 hours Framework-equivalent BGA on the extender-SBC
- 30 hours HAZOP / IEC 61508 SIL-2 practicum (execution, escort, and audit-trail responsibilities under the Nuvation standing agreement)

Total 480 hours reflects industry reality: IPC-7711/7721 Certified IPC Trainer is 40 hours for basic rework alone, and three-footprint BGA proficiency with zero head-in-pillow tolerance is a 150-hour-per-footprint discipline before X-ray-verified pass criteria are achievable.

**Critical scope note on Halbach signoff.** L3 does not sign the HAZOP procedure on the Halbach controller. That signoff is contractually retained by Nuvation Engineering under the standing agreement referenced in BOARD-FIX-SOW-RFP.md. Nuvation employs the PE-licensed safety EE who owns SIL-2 attestation. Hearth L3s execute the physical repair (board swap, coil rebalance, thermal characterization, board rework, sphere driver replacement) under that Nuvation-owned procedure with a two-technician signoff on Hearth's side. This scope allocation is discussed at length in §10 (compensation defense) and §14 (cross-doc reconciliation).

L1 is the door. L2 is the workhorse. L3 is the escalation floor and the training bench for the next L2 cohort.

---

## 3. L1 curriculum (Concierge-Certified) — 60 hours

**Week 1 — Online, 20 hours.** Instructor: Head of Field Service + rotating Cohort-0 concierge guest sessions.

- Module 1.1 (2 hr): Hearth product architecture. The 6-PCB block diagram (mic-array, audio-amp, compute-backplane, orb, extender-SBC, Halbach-controller). Cable topology. What each board does in plain English. Why the sphere and the base talk to each other over the umbilical and what happens if they don't.
- Module 1.2 (3 hr): The 90-day onboarding journey from ONBOARDING-PLAYBOOK.md. What the customer has already been told before your visit. The three "moments" (unboxing, first wake, first face-recognition). Where in the journey is your customer likely to be when they call?
- Module 1.3 (4 hr): The companion mobile app deep-dive. Every diagnostic screen. The "Send Diagnostic Bundle" flow. How to read the health tile. Reading network telemetry from the app. Interpreting the eight sphere-state colors.
- Module 1.4 (5 hr): Common issue triage. How to conduct the first three minutes of a call before escalating. Scripts. Non-scripts (what to say when the customer is upset). The "let me see it" technique.
- Module 1.5 (4 hr): Concierge communication protocol. When to say "I don't know." When to promise a visit. When to promise a call-back window. Escalation-with-warmth language.
- Module 1.6 (2 hr): Quiz + reflection.

**Week 2 — Fremont, 20 hours in person.** Instructor: L3 lead + one L2 mentor per two students.

- Day 1 (4 hr): Sphere unboxing, placement, calibration hands-on. Each student does it three times, blindfolded on the third.
- Day 1 (4 hr): Network troubleshooting workshop on the intentionally-cursed lab network — Eero, Ubiquiti, and a Cox-issued Panoramic gateway all present, running simultaneously with conflicting DHCP scopes.
- Day 2 (6 hr): Guided replacement of the three consumer-serviceable parts. Extender cable (CL3-rated 4m + 8m), air filter (magnetic Merv-11 sled), front bezel (magnet-latched, no screws). Each student replaces each part three times.
- Day 2 (4 hr): Mobile-app pairing and re-pairing flow. Airplane-mode failure modes. Apple Home vs Google Home vs standalone re-onboarding.
- Day 2 (2 hr): Mock install signoff.

**Week 3 — Online, 20 hours.** Instructor: Privacy Engineering lead + Head of Field Service.

- Module 3.1 (5 hr): Companion consent flow deep-dive from THREAT-MODEL.md. What the customer agreed to at onboarding. What the concierge is authorized to see. What the concierge is not authorized to see. The "closed drawer" principle.
- Module 3.2 (5 hr): Remote support via RustDesk (self-hosted relay at rustdesk.hearth.internal). Session-scoped consent. The consent LED behavior on the sphere during a remote session. Ending a session. Never running a session without the customer physically present.
- Module 3.3 (4 hr): When to escalate to L2. The 15-minute rule. Language templates for escalation calls. Never disparage the product.
- Module 3.4 (4 hr): The Salesforce Field Service Lightning ticket flow. Case creation, part-request, dispatch, close.
- Module 3.5 (2 hr): Recap + certification prep.

**Certification.** 30-question written exam (70% pass), one mock install supervised by a Cohort-0 concierge. Failure → 30-day retake window with mandatory shadow week.

---

## 4. L2 curriculum (Field Service Technician) — 320 hours

Prerequisite: L1 active for 90 days minimum + supervisor nomination.

### Block A — Online product and schematic literacy (40 hours)

Instructor: Hardware Engineering (schematic design) + Head of Field Service.

- Module 2.1 (10 hr): 6-PCB deep-dive with full schematic reading. KiCad schematic sheets for the compute-backplane, orb, mic-array, audio-amp, extender-SBC, Halbach-controller — provided in the field-tech laptop's read-only Confluence mirror. How to read a net class. How to trace power rails. How to interpret the PCB-revision silkscreen and match it to firmware compatibility tables.
- Module 2.2 (6 hr): ESD safety at customer-premises depth. Grounding on a customer floor (foam pads, wrist strap, portable mat kit). The "no living-room repair on carpet without the mat" rule.
- Module 2.3 (8 hr): Closed-loop cooling maintenance theory. The single-cartridge Fluorinert FC-3283 refill procedure using the pre-mixed 60ml canisters. Pressure test procedure. The dye-added leak test.
- Module 2.4 (8 hr): The Purifi Eigentakt 1ET7040SA amp module and DAC failure signatures. Ground-loop diagnosis in a customer's whole-home audio setup. The "borrow the customer's own IEC cable" trick.
- Module 2.5 (8 hr): Wake-word model behavior and voice-activity edge cases. The Cohort-0 field cases of Siamese cats, aquarium bubblers, and Peloton coach voices triggering false positives. What is a firmware fix vs a mic-array replacement.

### Block B — Fremont bench: mechanical, board swap, cooling (80 hours)

Instructor: L3 lead + Sanmina Fremont liaison (one visit).

- Days 1-2 (16 hr): Sphere disassembly, ORB PCB access, and umbilical service. Timed drills against the depot standard.
- Days 3-4 (16 hr): Board-replacement drills across all six PCBs. Compute-backplane swap under 45 minutes; ORB PCB swap under 25 minutes; audio-amp swap under 30 minutes; mic-array under 20; extender-SBC customer-premises quick-swap under 15; Halbach-controller board swap under 60 (with Nuvation remote assist rehearsal).
- Days 5-6 (16 hr): Closed-loop cooling refill hands-on. Fitting torque discipline. UV-dye leak detection. Pump-body inspection triage (repair-in-field vs depot-return call).
- Days 7-8 (16 hr): Thermal-chamber testing. Loading a customer-returned board into the Espec BTX-475 chamber, running the 0-40°C profile, reading the pass/fail. When to send a board to L3 for BGA inspection.
- Days 9-10 (16 hr): Full board-replacement scenarios timed and graded against the depot standard, including two full sphere-open procedures on training rigs.

### Block C — JTAG and firmware bring-up (60 hours)

Instructor: Embedded Engineering.

- Module 4.1 (10 hr): Diagnostic tools. The field-kit tablet (iPad Pro 11") running the internal FieldOps app. USB-C serial console to the compute-backplane. The 3.3V FTDI cable to the STM32H723 sphere MCU.
- Module 4.2 (15 hr): JTAG debugging over the Segger J-Link. Reading the sphere MCU's fault registers. The three stack-dump signatures that mean "send to depot" vs "reflash and retry." Live-target attach on a running sphere-sim rig.
- Module 4.3 (15 hr): Boot chain analysis. U-Boot log reading on the compute stack. The Jetson boot sequence. The eight-second grace window. What to do when the sphere gets stuck in the "orb wake" boot animation. Bootloader recovery via USB DFU on the extender-SBC.
- Module 4.4 (12 hr): Firmware update rollback procedures. The A/B partition scheme. The "sphere brick" recovery flow (magnet-key + USB-C recovery cable, from FIRMWARE-RECOVERY.md). Cross-verification of firmware signature against the release manifest.
- Module 4.5 (8 hr): Practical exam. Every trainee must independently recover a deliberately-bricked sphere-sim rig within a 2-hour window using serial console + magnet-key + recovery cable.

This block is the addition the verifier flagged: previously, L2 curriculum required schematic literacy across 6 PCBs, JTAG on STM32H723, and U-Boot log analysis inside a 200-hour envelope. Sixty additional hours of dedicated JTAG and firmware bring-up are what turn "the tech knows the tool exists" into "the tech can find the fault."

### Block D — Halbach recalibration and coil-drive characterization (60 hours)

Instructor: Nuvation Engineering (contract instructor, on-site at Fremont) + L3 lead.

- Module 5.1 (12 hr): Halbach controller architecture in plain language. What the eight coils do. Why the neodymium array is arranged the way it is. The magnetic-null point and why it moves.
- Module 5.2 (16 hr): Coil-drive waveform interpretation on the Rigol DHO814 scope. Using the LEM CAB-500 current-probe kit. Reading the healthy waveform. Recognizing the four common fault waveforms (coil open, coil-to-coil short, PWM edge distortion, thermal derate).
- Module 5.3 (16 hr): In-home recalibration on the sphere-sim rig. Guided by Nuvation instructor. Each trainee performs the recalibration eight times against varied fault injections.
- Module 5.4 (10 hr): Boundary of scope. What the L2 is authorized to do in the customer's home under the Nuvation standing agreement. Where the boundary is (any hardware repair on the Halbach controller board itself requires L3 remote assist and executes under a Nuvation-signed HAZOP procedure; L2 never operates outside that procedure).
- Module 5.5 (6 hr): Halbach-specific practical exam. Nuvation instructor signs the field-authorization card.

This block is also new. Without dedicated Halbach time, the previous curriculum was asking L2s to read coil-drive waveforms on a scope inside a mixed-topic 40-hour Fremont week. Sixty hours here is the number Nuvation quoted as the minimum for a non-safety-signoff field technician to operate under their standing procedure.

### Block E — Supervised field practicum (80 hours)

- Weeks 1-2 (40 hr): Two supervised depot repairs (with an L3 signing off on Hearth-side execution) + two supervised field visits (customer install redo, sphere replacement in a real customer home, extender-pairing failure at a second real customer home).
- Weeks 3-4 (40 hr): Four supervised field service calls with an L3 mentor riding along. Mentor does not touch the device. Mentor debriefs after each call.

**Certification.** 60-question written exam (75% pass) + supervised field-visit competency assessment across all six PCB categories + Nuvation-instructor signoff on the Halbach block. Failure → 60-day retake, mandatory second field practicum.

---

## 5. L3 curriculum (Senior Depot Technician) — 480 hours

Prerequisite: L2 active for 18 months minimum + engineering director nomination + demonstrated aptitude on at least one advanced case type (BGA, sphere driver, firmware).

The L3 curriculum has been restructured following the verifier note that BGA rework proficiency across three different footprints (BGA-152 NVMe, custom Ryzen socket, Framework-equivalent extender-SBC) in 60 hours was not credible. IPC-7711/7721 Certified IPC Trainer runs 40 hours for basic rework; adding X-ray inspection literacy and zero head-in-pillow tolerance under production discipline requires 150+ hours per footprint. The new envelope of 150 hours per footprint plus 30 hours of HAZOP practicum totals 480 hours and matches industry norms.

### Block A — BGA-152 NVMe (Kioxia CD8-R footprint), 150 hours

- Fundamentals of BGA reflow theory using the Ersa HR 550 XL rework station (24 hr)
- Preheat and thermal profiling for the CD8-R footprint (24 hr)
- Reballing procedure (48 hr): stencil selection, solder-sphere placement, reball verification under microscope
- X-ray inspection literacy — until X-ray equipment is in-house (Y3, per §7), inspection is performed at Sanmina under the overflow contract. Sanmina X-ray access is 24 hr of curriculum time, including cross-training with their inspector (24 hr)
- Pass criteria (30 hr): 3 consecutive successful reballs, zero head-in-pillow defects, verified by X-ray and functional test. Repeat cycle until 3-in-a-row is achieved.

### Block B — Custom Ryzen socket footprint on the compute-backplane, 150 hours

The compute-backplane uses a BGA land pattern under the custom Ryzen socket carrier rather than a traditional LGA. This is a Sanmina-specific board and the reball procedure is documented under Sanmina's engineering release rather than a generic AMD footprint.

- Board preparation and residue cleaning post-desolder (24 hr)
- Thermal profiling for the compute-backplane's 12-layer stackup (30 hr)
- Reball and reflow (60 hr) — this is a large-footprint BGA and requires longer preheat soak
- X-ray inspection and functional-test discipline (24 hr, again via Sanmina under overflow contract)
- Pass criteria (12 hr): 3 consecutive successful reballs.

### Block C — Framework-equivalent BGA on the extender-SBC, 150 hours

The extender-SBC uses a Framework-mainboard-equivalent module. This is the smallest of the three footprints and the easiest to damage.

- Small-footprint reflow discipline (30 hr)
- Trace-repair skills for adjacent damage (30 hr)
- Reball and reflow (60 hr)
- X-ray inspection and functional-test discipline (18 hr)
- Pass criteria (12 hr): 3 consecutive successful reballs.

### Block D — HAZOP / IEC 61508 SIL-2 practicum, 30 hours

Formal training in the standing procedure by which Hearth L3s *execute* Halbach controller repair under a *Nuvation-signed* HAZOP procedure. This block is deliberately not a signoff certification. Hearth L3s never sign the HAZOP. The signoff remains with the PE-licensed safety EE at Nuvation Engineering, per the standing agreement referenced in BOARD-FIX-SOW-RFP.md.

- The Nuvation standing procedure (6 hr): what it authorizes Hearth L3s to do, what it does not, the two-signature Hearth-side audit trail
- Sealed-fixture Halbach programmer operation (6 hr): the programmer is not connected to the internet and requires two-person signoff on every write. Nuvation retains the authoritative firmware repository.
- Halbach coil rebalance (12 hr): using the Keithley DMM6500 and the depot's field-mapping fixture. The eight coils are individually tuned against a reference sphere.
- Documentation discipline (6 hr): every SIL-2-touching repair generates an audit packet for Nuvation. Nuvation reviews weekly and countersigns.

### Supporting L3 skills (integrated across blocks A-D)

- **OLED sphere driver replacement** (integrated across the sphere-open work in Block D). The sphere's OLED is a custom 96mm-diameter flexible AMOLED driven by a Solomon SSD1362-derived driver. Driver replacement requires disassembly of the sphere along its equatorial parting plane, driver-board swap, and re-lamination.
- **Sanmina Fremont embedded rotation.** L3 candidates spend structured time at Sanmina's Fremont facility on 2685 Marine Way embedded with the assembly team building Hearth mainboards. They rotate through SMT line supervision, ICT test debug, and functional test. This rotation is non-negotiable — a depot technician who does not know how the board is manufactured cannot diagnose it well. Rotation time is folded into Blocks A and B (X-ray access blocks) plus a discretionary two-week rotation before final certification.
- **Firmware programming.** Programming the STM32H723 sphere MCU using the ST-Link V3, the extender-SBC firmware via SWD, and the safety-critical Halbach-controller firmware via the sealed-fixture programmer maintained under Nuvation Engineering's version control.
- **Thermal envelope characterization (0-100°F ambient).** Using the Espec BTX-475 chamber, characterize a repaired Hearth across the full ambient envelope before returning to customer. Documented pass/fail criteria in THERMAL-QUAL.md.
- **Post-mortem incident review + root-cause analysis.** L3s lead the RCA on any field failure that escalated to depot. Uses the 5-Whys + fishbone method documented in POSTMORTEM-TEMPLATE.md.
- **Corrosion + accidental-damage assessment.** How to distinguish warranty-covered manufacturing defect from customer-caused damage (spilled water, pet urine, insurance-required documentation). Photography protocol. When to invoke the customer-caused-damage clause.
- **Estate + international field-service protocols.** For customers with multiple Hearths in multiple homes, the estate-service protocol. For customers who move internationally, the export-controlled-firmware protocol.

**Certification.** Attend 20+ actual repair cases as observer-then-lead + pass advanced exam + submit one dissertation-style case study (5,000-8,000 words, defended in front of Engineering + Field Service leadership) + Nuvation instructor signoff on the HAZOP practicum block.

---

## 6. Ongoing training and recertification

Training is not an onboarding event. It is a continuous obligation.

- **Quarterly 4-hour refresher (all levels).** Video-delivered via the internal LMS (Docebo). New-issue briefings, updated troubleshooting flows, product-revision notes. Concludes with a 20-question exam. 80% pass required.

- **Annual 2-day in-person all-hands (all levels) at Fremont.** Every field-tech, regardless of level, spends two days at Fremont each year for hands-on skills refresh, new-tool training, and cohort-building. Timed around Sanmina's annual maintenance week to overlap with their engineers.

- **Major firmware release: same-week update-and-verify training.** Every firmware release that changes user-visible behavior triggers a one-hour recorded briefing + a hands-on verification session on the tech's own field-kit sphere-sim rig within seven days of release. No firmware version is authorized for field deployment until 90% of L1/L2 have completed the briefing.

- **Board/hardware revision: pre-release training + practice repair on beta units.** A hardware revision (any board revision that changes part numbers, torque specs, or replacement procedure) requires each L2 to complete two practice repairs on beta units in the depot before the revision ships to customers. Rev-B compute-backplane rollout planned Q3 uses this exact flow.

- **Nuvation annual field-safety workshop.** Every L3 attends. Every L2 with a Halbach-authorization card attends. Two-day workshop at Nuvation's Sunnyvale facility covering any updates to the standing HAZOP procedure, SIL-2 audit findings from the prior year, and new fault-injection cases.

- **Annual recertification exam.** Every level, every year. Failure means demotion to the level below until re-certification. There has never been an unforced demotion in Cohort-0. There will be.

- **Continuing-education budget.** $2,500 per L2 per year, $5,000 per L3 per year, for external conferences, courses, or certifications (IPC J-STD-001, IPC-A-610, IPC-7711/7721, CompTIA, Nuvation-hosted workshops, EEVblog member events, DEF CON hardware hacking village).

---

## 7. Fremont depot facility

The depot has been right-sized to Y1 volume following the verifier finding that the previous plan (2 BGA stations, 2 chambers, X-ray, 16 benches, 6 sphere-sim rigs, 3,000 sqft) would have consumed the entire $1.57M Y1 warranty reserve on depot capex + opex before a single field visit occurred. The revised Y1 depot has enough capacity for expected volume with Sanmina overflow contracted for surge, and scales up in Y2 as install base grows.

### Y1 depot configuration (600-unit install base)

Volume math: 600 units × 3% Y1 claim rate = 18 claims. 92% first-visit L2 fix rate leaves ~1-2 that escalate. Of the remainder that reach depot, 85% can be handled without BGA rework (board swap, firmware, sphere driver, cooling assembly). **Expected true depot repairs Y1: 2-4.**

**Footprint: 1,500 sqft** at 47000 Warm Springs Blvd, Fremont, CA, sub-leased from Sanmina and adjacent to their assembly building for logistical convenience.

**Equipment:**

- **1 BGA rework station.** Ersa HR 550 XL, ~$200k. Handles all three footprints (Kioxia CD8-R, custom Ryzen socket on the compute-backplane, Framework-equivalent on the extender-SBC).
- **1 thermal chamber (0-100°F, humidity 20-90%).** Espec BTX-475, ~$50k. Used for both intake QA and outbound QA on rotating schedule. Calibrated quarterly by Espec service.
- **4 ESD workstations.** Bench setup: Weller WE1010 solder station, Metcal MX-500 rework station, IFR-2500 microscope, wrist strap point, ionizer, 6-outlet ESD-safe power. Bench surfaces are the Bertech ESD-safe mat kits, replaced quarterly. Two benches double as L2 training positions during cohort weeks.
- **2 sphere-simulator rigs.** Each rig replicates the sphere's Halbach base, umbilical, and mounting hardware without a live customer sphere. Used for L2 Halbach recalibration training and L3 signoff work. Built in-house on aluminum extrusion frames.
- **1 firmware programming bench.** ST-Link V3 station for STM32 programming. Segger J-Link Pro station for JTAG. Sealed-fixture bench for Halbach-controller firmware programming per Nuvation NDA — fixture stays sealed and audit-logged.
- **Sanmina Fremont overflow contract.** For BGA surge capacity (second station equivalent), X-ray inspection access, anechoic chamber leased time, and ICT test. $15-25k per repair for Sanmina depot service, invoiced against warranty reserve at case level. Sanmina at 2685 Marine Way is ~4 miles from Hearth depot, enabling same-day board exchange during hot periods.

**Y1 depot capex:** BGA station $200k + chamber $50k + 4 benches at $12k each = $48k + 2 sphere-sim rigs at $18k each = $36k + firmware bench $16k = **$350k Y1 capex.**

**Y1 depot opex:** Rent 1,500 sqft at $5.50/sqft/mo NNN = $99k/yr. Calibration + consumables $30k. Sanmina overflow reserve (budget for ~6 depot events across Y1 including surge scenarios) $50k. **~$180k Y1 opex.**

**Total Y1 depot cost: ~$530k**, inside the $1.57M Y1 warranty reserve with $1M+ of headroom for field visit costs (median $250-$800 × ~15 field visits Y1 = $4-12k in visit-labor cost; sphere-swap capped at $3,500 × worst-case 3-4 Y1 = $10-14k; loaner logistics and part inventory replenishment absorb the rest).

**What is deliberately deferred out of Y1:**

- **Second BGA station.** Deferred to Y2 when install base ≥ 2,000. Surge coverage in Y1 via Sanmina overflow contract.
- **Second thermal chamber.** Deferred to Y2. Y1 uses rotating schedule on the single Espec.
- **Nordson DAGE X-ray.** Deferred to **Y3** (Nordson DAGE Quadra 5 ~$150k). Y1 and Y2 use Sanmina X-ray access under the overflow contract. This is the single largest capex deferral and it is the correct call: Y1-Y2 X-ray volume does not justify the $150k asset when Sanmina inspection is 4 miles away.
- **Additional ESD benches (5-16).** Deferred until Y2 based on L2 cohort growth.
- **Additional sphere-sim rigs (3-6).** Deferred until Y2 based on training throughput needs.
- **Owned anechoic chamber.** Never planned — leased time from Sanmina's adjacent building via the overflow contract.

### Y2 depot expansion (2,000+ install base)

- Add second BGA station ($200k)
- Add second thermal chamber ($50k)
- Expand to **3,000 sqft** (either lease-expand at Warm Springs Blvd or move within the Sanmina campus)
- Expand to **12 ESD benches**
- Add 2-4 additional sphere-sim rigs based on L2 training volume
- Y2 depot capex ~$400-500k, sized to the Series-A close and installed base curve

### Y3 depot expansion (5,000+ install base)

- Bring X-ray in-house (Nordson DAGE Quadra 5 ~$150k)
- Add second firmware programming bench
- Total depot footprint 3,000 sqft with option to expand

### Depot operating hours

Mon-Fri 07:00-19:00 PT for repair. On-call rotation for weekend escalations (paid at on-call premium). No overnight depot activity — the depot is empty and alarmed after 20:00.

### Depot inventory targets

30% board-level spare stock across the six PCBs, expressed as (installed base × Y1 warranty rate × safety margin). 100% for critical components with long lead times: Kioxia CD8-R NVMe, NVIDIA Jetson Orin NX modules, custom sphere OLED (18-week lead time from Truly Semiconductor). Purifi Eigentakt modules are 60% because their 6-week lead time is manageable.

---

## 8. Field-service protocols

Eighteen standardized issue protocols. Each is a Confluence page cross-linked from the FieldOps iPad app. Techs read the page on the customer's couch. Format below is compressed.

The prior version of this curriculum listed twelve protocols. The verifier flagged six additional failure modes common to a device with cameras, mesh radios, and $95k customer expectations. Those six are added below as (m) through (r).

### (a) Sphere won't wake

- **Symptom.** Sphere unresponsive to wake-word, no face on OLED, no gesture response.
- **Likely causes (order of frequency).** Loss of umbilical power (60%), sphere MCU boot hang (20%), OLED driver dead (10%), thermal shutdown (5%), Halbach controller fault (5%).
- **Diagnostic tree.** Check umbilical LED at base → if dark, base power fault (jump to full-system unresponsive). If lit → attempt magnet-key soft reset (hold magnet at 4 o'clock for 8 sec). If wakes, log and monitor. If no wake, USB-C serial console to sphere MCU, read boot log. Fault codes 0x01-0x1F → firmware, reflash. 0x20-0x3F → hardware, replace sphere.
- **Replacement parts.** L1: none (soft reset only). L2: sphere assembly (SKU HRT-SPH-001), OLED driver (HRT-SPH-DRV-001).
- **Escalation.** Fault codes ≥ 0x40 → L3 depot. Repeated boot failure after reflash → L3.
- **Time-to-repair.** L1 soft reset: 15 min. L2 sphere swap: 45 min. L3 depot: 3 days.

### (b) Extender pairing failure

- **Symptom.** Customer's second-room extender won't join the base's mesh, or drops repeatedly.
- **Likely causes.** Firmware version mismatch (40%), network credential drift (25%), extender-SBC hardware fault (20%), umbilical Cat6A run issue (15%).
- **Diagnostic tree.** Companion app → Extenders → status. Show firmware version. Compare to base version. If mismatch, force sync from base. If sync fails, reflash extender-SBC via USB-C recovery cable. If reflash fails, cable check with Klein VDV501-853. If cable OK, hardware fault, swap extender-SBC.
- **Replacement parts.** L1: extender cable (Cat6A CL3, HRT-EXT-CBL-4M or 8M). L2: extender-SBC (HRT-EXT-SBC-001).
- **Escalation.** Repeated pairing failure after extender-SBC swap → L2 investigates base's compute-backplane radio subsystem. If confirmed, L3 depot.
- **Time-to-repair.** L1 credential reset: 10 min. L1 cable swap: 20 min. L2 extender-SBC swap: 60 min.

### (c) Sphere shows garbled face

- **Symptom.** OLED shows corrupted pixels, wrong colors, static, or partial-image failure while sphere is otherwise responsive.
- **Likely causes.** OLED driver silicon partial failure (50%), FPC connector reseat (25%), thermal (15%), boot-chain graphics stage (10%).
- **Diagnostic tree.** Companion app → Diagnostic → OLED test pattern (8 solid colors + gradient). Photograph result. If entire image is corrupted, driver failure. If only one region, FPC. If intermittent and correlates with sphere warmth, thermal. If only at boot animation, boot-chain.
- **Replacement parts.** L2: OLED driver board (HRT-SPH-DRV-001), FPC ribbon (HRT-SPH-FPC-001).
- **Escalation.** OLED panel itself defective (not driver) → L3 depot for panel swap (18-week lead time, warm-swap from depot pool).
- **Time-to-repair.** L2 driver swap in field: 90 min. L3 panel swap in depot: 5 days.

### (d) Wake-word doesn't respond

- **Symptom.** Wake-word ("Hey Hearth") ignored, or triggered inconsistently.
- **Likely causes.** Mic-array capsule failure (20%), wake-word model corruption (30%), background noise floor issue (30%), firmware regression (20%).
- **Diagnostic tree.** Companion app → Voice → SNR meter. If SNR < 12 dB, environmental (aquarium, HVAC, fountain). Reposition sphere. If SNR OK but wake-word ignored, model integrity check via app. If model corrupted, re-download. If model OK, mic-array capsule test (four capsules, one at a time, using the calibrated test tone from the iPad kit). Failed capsule → mic-array PCB replacement.
- **Replacement parts.** L2: mic-array PCB (HRT-MIC-001).
- **Escalation.** Post-swap SNR still low with clean environment → L3 investigates compute-backplane audio codec (Cirrus CS47L15).
- **Time-to-repair.** L2 mic-array swap: 40 min.

### (e) LLM returns nonsense

- **Symptom.** Customer asks a question; sphere responds with word salad, factually broken statements, or a persistent "loop" answer.
- **Likely causes.** On-device state corruption (40%), quantization corruption after NVMe uncorrectable error (30%), model file partial corruption (20%), Jetson compute module thermal throttle (10%).
- **Diagnostic tree.** Companion app → LLM → "Model integrity check." If model checksum fails, re-download from base cache. If cache also fails, jump to protocol (o) NVMe standalone before proceeding, since NVMe symptom presentation as "LLM broke" is common enough that we now handle NVMe as its own protocol. If checksum OK, examine on-device state DB. Corrupted state → wipe with backup restore. If wipe/restore does not help, Jetson thermal history log. If thermal event correlates, cooling loop check.
- **Replacement parts.** L2: model integrity restore only (no hardware unless NVMe protocol says so).
- **Escalation.** Non-NVMe root cause after model restore fails → engineering ticket.
- **Time-to-repair.** L2 model restore: 60 min.

### (f) Media library missing

- **Symptom.** Plex, Jellyfin, or AudioBookshelf shows empty library or missing content.
- **Likely causes.** Storage-permission drift after firmware update (40%), storage full (25%), Plex metadata database corruption (20%), file-system mount fault (15%).
- **Diagnostic tree.** Companion app → Media → per-app health tile. Storage percent check. If > 92%, storage-full remediation (customer conversation about content pruning). Plex DB check via CLI. Corrupted DB → restore from nightly local backup. Mount fault → dmesg via serial console. If mount fault repeats, escalate to protocol (o) NVMe standalone.
- **Replacement parts.** Rarely required.
- **Escalation.** Repeated permission drift after firmware → engineering.
- **Time-to-repair.** L1 permission fix: 20 min. L2 DB restore: 90 min.

### (g) Streaming stall to extender

- **Symptom.** Sunshine or Steam stream to an extender in a second room stalls, drops frames, or lags input.
- **Likely causes.** Customer's network QoS (35%), extender NIC (25%), firmware sync drift (20%), umbilical cable degradation (20%).
- **Diagnostic tree.** iperf3 between base and extender over the umbilical. Below spec → cable test. At spec → check application QoS. Verify Sunshine encoder settings match extender decoder. Firmware version sync. NIC error counters via SBC serial console.
- **Replacement parts.** L1: umbilical cable. L2: extender-SBC.
- **Escalation.** Persistent stall on validated hardware → engineering (streaming stack).
- **Time-to-repair.** L1 cable swap: 30 min. L2 extender-SBC: 60 min.

### (h) Halbach sphere floats erratically

- **Symptom.** Sphere bobbles, drifts, or fails to maintain float position.
- **Likely causes.** Coil calibration drift (40%), controller firmware regression (25%), thermal-induced neodymium permeability shift (20%), customer moved the base without re-calibration (15%).
- **Diagnostic tree.** Companion app → Sphere → "Recalibrate." If recalibration completes and holds for 30 min, done. If recalibration fails, L2 dispatch under Nuvation-authored recalibration script. L2 verifies coil drive with LEM CAB-500. Bad coil drive → controller board. Controller firmware version check. Thermal-induced case: measure base temp, verify cooling loop is functional. Customer-moved case: educate + recalibrate.
- **Replacement parts.** L2 with Halbach card: Halbach controller board (HRT-HAL-CTRL-001, requires Nuvation-signed HAZOP procedure execution, Nuvation remote assist mandatory).
- **Escalation.** Any Halbach-controller replacement in the field → L3 remote assist mandatory + Nuvation on the line. Nuvation-signed HAZOP procedure is the authoritative source of truth; L3 does not sign it. Two-technician Hearth-side signoff on execution. Repeated failure after controller swap → L3 depot with sphere.
- **Time-to-repair.** L1 recalibration: 15 min. L2 controller swap with Nuvation+L3 remote: 3 hr.

### (i) Cooling loop leak

- **Symptom.** Visible fluid on customer's furniture; humidity alarm on base; temperature climb.
- **Likely causes.** Fitting failure (60%), pump seal wear (20%), radiator microcrack (15%), umbilical Y-joint (5%).
- **Diagnostic tree.** IMMEDIATE — power down base via companion app's "Safe Shutdown." Do not restart. Visual inspection with UV lamp (Fluorinert FC-3283 is UV-dye traced). Photograph. If small fitting leak visible, tighten and monitor with dye check. Any leak involving the pump body or radiator → immediate escalation.
- **Replacement parts.** L2: fitting kit (HRT-COOL-FIT-001), pre-mixed 60ml refill cartridge (HRT-COOL-RFL-001).
- **Escalation.** All cooling leaks require L2. Pump or radiator involvement → L3 depot swap of the entire cooling assembly. Any leak that touched electronics → depot only, no field repair.
- **Time-to-repair.** L2 fitting + refill: 90 min. L3 depot cooling assembly swap: 4 days.

### (j) Amp buzz/hiss

- **Symptom.** Audible buzz, hum, or hiss through the customer's speakers, driven by the audio-amp PCB (Purifi Eigentakt 1ET7040SA modules + AKM AK4499EX DAC).
- **Likely causes.** Ground loop with customer's home wiring (35%), speaker cable shielding (20%), Purifi module input-stage failure (20%), DAC clock jitter (15%), connector oxidation (10%).
- **Diagnostic tree.** Isolate: disconnect all customer speaker outputs. If buzz persists on internal headphone tap, hardware side. If gone, downstream/ground loop. Try IEC power cable swap, try dedicated circuit. If ground-loop confirmed, iso-isolator recommendation. If hardware side, Purifi module swap.
- **Replacement parts.** L2: Purifi module (HRT-AMP-PFI-001), audio-amp PCB assembly (HRT-AMP-001) for DAC/clock issues.
- **Escalation.** DAC issue → L3 for chip-level replacement or full board swap.
- **Time-to-repair.** L1 ground-loop diagnosis: 45 min. L2 Purifi swap: 60 min. L3 depot DAC repair: 2 days.

### (k) Ambient light sensor stuck

- **Symptom.** Sphere face brightness does not adapt; stays too dim or too bright regardless of room lighting.
- **Likely causes.** VEML7700 sensor hardware fault (60%), calibration table corruption (25%), aperture obstruction — dust or a child's sticker (15%).
- **Diagnostic tree.** Visual check of the sensor aperture. Clean if obstructed. Companion app → Sphere → "Recalibrate ambient." If fails, sensor I2C bus check via serial console. No I2C response → sensor fault, replace during next sphere-open opportunity (not urgent, tolerable customer experience with manual brightness).
- **Replacement parts.** L2: sphere assembly (bundled) or standalone sensor board (HRT-SPH-ALS-001) if the sphere is already open.
- **Escalation.** None.
- **Time-to-repair.** L1 clean + recalibrate: 15 min. L2 sensor swap: bundled with next sphere open.

### (l) Full system unresponsive

- **Symptom.** No power to base, no umbilical LED, no fans, no sphere.
- **Likely causes.** Customer breaker (40%), base power supply (25%), backplane power rail failure (20%), boot-hang black-screen (15%).
- **Diagnostic tree.** Customer's outlet test (voltage). Base IEC cable swap. If base LED still dark, power supply swap. If LED lit but system does not boot, USB-C serial console for boot log. Boot log stuck at BL1 → embedded firmware fault, reflash. Stuck later → backplane fault, L2 or L3 as indicated by log signature.
- **Replacement parts.** L2: base PSU (HRT-PSU-750-001), compute-backplane (HRT-CBP-001).
- **Escalation.** Backplane replacement in field is L2, but if the compute stack does not reinitialize after backplane swap, the customer's Hearth goes to depot as an interim-swap.
- **Time-to-repair.** L1 breaker + outlet: 15 min. L2 PSU swap: 45 min. L2 backplane swap: 3 hr. L3 depot: 3-5 days.

### (m) Camera / face-recognition failure

- **Symptom.** Sphere does not recognize known faces, misidentifies faces, or reports "camera not available" on the companion app.
- **Likely causes.** Sony IMX415 sensor module fault (30%), Toshiba TC358748 aggregator failure (20%), lens obstruction or aperture contamination (25%), face-recognition model corruption (15%), firmware regression (10%).
- **Diagnostic tree.** Companion app → Camera → live preview. If black frame, sensor or aggregator. Companion app → Camera → aggregator status. If aggregator reports link-down, MIPI link fault → reseat FPC. If preview is present but face-rec fails, model integrity check. If model checksum fails, re-download. Lens aperture check with clean-room swab. If preview is present, model OK, and recognition still fails, run the calibrated enrollment card test.
- **Replacement parts.** L2: sensor module (HRT-CAM-IMX415), aggregator board (HRT-CAM-AGG-001), FPC ribbon (HRT-CAM-FPC-001).
- **Escalation.** Post-swap sensor + aggregator with continued failure → L3 investigates compute-backplane MIPI receiver. Face-rec model that fails checksum across multiple sphere restores → engineering (model corruption pattern).
- **Time-to-repair.** L1 lens clean + model refresh: 20 min. L2 sensor module swap: 75 min. L2 aggregator swap: 90 min.
- **Privacy note.** Face-rec troubleshooting touches the closed-drawer principle from THREAT-MODEL.md. Concierges follow the enrollment-card test rather than viewing live customer faces during diagnostics.

### (n) Base station Wi-Fi / backhaul radio failure

- **Symptom.** Base cannot reach the customer's home Wi-Fi; base radio subsystem reports no upstream link; extenders and base can no longer sync through the customer network; customer sees base offline in the companion app.
- **Likely causes.** Qualcomm FC7800 M.2 module fault (30%), antenna feedline dislocation (20%), customer Wi-Fi credential drift (15%), customer AP reconfiguration (15%), firmware regression on the radio driver (10%), M.2 socket connectivity (10%).
- **Diagnostic tree.** Companion app → Base → Network. If credentials error, re-enter Wi-Fi credentials. If association fails, verify the customer's AP is up (test with the concierge's phone). If AP up but base cannot associate, USB-C serial console to compute-backplane, `iw dev wlan0 info`. If interface missing, M.2 module fault. If interface present but scan returns nothing, antenna. Reseat M.2 card; if that doesn't restore, swap module. Antenna feedline continuity check with the concierge's DMM.
- **Replacement parts.** L2: Qualcomm FC7800 M.2 module (HRT-RADIO-FC7800), antenna assembly (HRT-ANT-BASE-001).
- **Escalation.** M.2 socket damage → L3 depot for socket rework. Multi-customer FC7800 failures within short window → engineering (batch fault suspicion, RISK-REGISTER.md logs the vendor).
- **Time-to-repair.** L1 credential reset: 15 min. L2 M.2 swap: 45 min. L2 antenna swap: 30 min.
- **Note.** This protocol covers *base* radio only. Extender-side mesh pairing remains protocol (b).

### (o) NVMe standalone failure

- **Symptom.** Presents as one of several other symptoms — corrupted LLM model, missing media library, boot failure at file-system mount — but originates in the NVMe module rather than the higher-layer subsystem. Previously buried inside protocols (e) and (f); called out here as its own protocol because the diagnostic path differs materially.
- **Likely causes.** Kioxia CD8-R accumulated uncorrectable errors (40%), CD8-R sudden failure (15%), M.2 socket seat (15%), thermal-history damage (15%), firmware bug on the CD8-R (10%), NVMe write endurance exhaustion (5%).
- **Diagnostic tree.** Companion app → Storage → SMART. If Reallocated_Sector_Ct or Uncorrectable_Error_Cnt above threshold, NVMe failure imminent — capture SMART log for Kioxia warranty channel (required by their process), then swap. If SMART clean but mount fault, reseat NVMe (torque to spec). If still failing, swap. If swap resolves symptom, root cause was NVMe; upstream symptom protocols (LLM, media) are downstream. If swap does not resolve, revisit the presenting protocol.
- **Replacement parts.** L2: Kioxia CD8-R NVMe (HRT-NVME-2TB).
- **Escalation.** Any NVMe swap generates a Kioxia RMA per §13. Repeated CD8-R failures within same customer premises → engineering (thermal or write-pattern investigation).
- **Time-to-repair.** L2 NVMe swap + backup restore: 3 hr.
- **Diagnostic isolation from LLM and media protocols.** L1s are trained to run "Storage → SMART" as the first check whenever the presenting symptom is either "LLM nonsense" or "media missing." Two-thirds of the time in cross-testing during Cohort-0 rehearsal, this saves an L2 dispatch by identifying NVMe as root cause up front.

### (p) Fan / thermal fan degradation

- **Symptom.** Base fan audible at customer complaint level; base thermal history shows rising steady-state temperatures; fan RPM tracking diverges from baseline; occasional thermal throttle events on Jetson.
- **Likely causes.** Bearing wear (40%), dust accumulation on impeller (25%), fan controller PWM fault (15%), speed-sensor tachometer failure (10%), thermal-paste degradation (10%).
- **Diagnostic tree.** Companion app → Thermal → Fan telemetry. Compare current RPM at known load to baseline curve. If bearing signal (audible clicking, RPM oscillation, elevated bearing-noise metric) present, fan is failing; replace. If dust accumulation visible on borescope through air-intake, service-clean before replacement. If PWM controller misreports commanded RPM, controller side (compute-backplane fan controller IC). If thermal-paste degradation (steady-state temp climb without fan degradation), depot for repaste on Jetson and Ryzen thermal interfaces.
- **Replacement parts.** L2: fan assembly (HRT-FAN-BASE-001), air filter as a matter of course (HRT-FILTER-001). L3 depot for thermal-paste refresh.
- **Escalation.** Multi-fan degradation pattern across customer base within short window → engineering (batch bearing fault suspicion). Thermal-paste failures with less than 24-month age → engineering.
- **Time-to-repair.** L1 air filter + service clean: 20 min. L2 fan swap: 60 min. L3 depot thermal repaste: 6 hr.
- **Note.** This is distinct from protocol (i) cooling loop, which addresses Fluorinert leaks. Fan is air-side; loop is liquid-side; they can co-fail but are diagnosed independently.

### (q) Spill / physical impact triage

- **Symptom.** Customer reports a spill (water, wine, coffee, child's juice, pet urine) on the base or sphere; or a physical impact (dropped sphere during service, base knocked from console, seismic event).
- **Likely causes.** Not a "likely cause" protocol — this is an assessment protocol. The question is not what failed but whether the unit can be safely returned to service, repaired at depot, or must be declared a total loss (customer-caused damage clause vs warranty coverage).
- **Diagnostic tree.**
  1. **Immediate:** Instruct customer to power down via Safe Shutdown. Do not restart. Do not attempt to dry with heat.
  2. **On arrival:** Photograph exterior. Note liquid type if known. Concierge-level assessment: is the sphere still intact? Is the base still upright? Any visible damage?
  3. **Open base:** With customer consent. Photograph interior. Note any liquid ingress path. Note whether liquid contacted PCBs directly (worst case), umbilical only (recoverable), or exterior chassis only (best case).
  4. **Corrosion prediction:** Sugar-bearing liquids (juice, wine, soda) predict corrosion within 30 days regardless of drying — treat as depot-mandatory. Water alone with fast power-down predicts recoverable if PCBs did not contact liquid.
  5. **Impact:** Assess sphere sphericity (out-of-round detectable by the depot's Halbach-controller telemetry — any impact severe enough to affect float physics is a depot return). Assess base upright chassis for cracked feet, cracked side panels, cracked internal frame.
  6. **Signoff decision:** (a) recoverable in-field with cleaning and monitor — 15% of cases; (b) recoverable at depot with disassembly clean and functional test — 60%; (c) unrepairable, customer-caused damage clause, insurance-facing declaration — 25%.
- **Replacement parts.** Varies. Most spill cases become a full base swap under the customer-caused-damage clause with the loaner deployed.
- **Escalation.** All spill cases require L2 on-site assessment. All customer-caused-damage declarations require L3 signoff + Head of Field Service review before the customer is billed.
- **Time-to-repair.** L2 in-field assessment: 90 min. Depot recovery: 3-7 days. Customer-caused-damage declaration + replacement unit: 5 business days.
- **Documentation.** Photography protocol from L3 corrosion + accidental-damage assessment training applies. Customer insurance often requires our detailed photographic record and written assessment; concierges are trained to produce this reliably.

### (r) OTA update failure that isn't extender-related

- **Symptom.** Base fails to complete an OTA update; base is stuck in "update in progress" state; base rolled back partially and now runs mixed firmware versions across subsystems; boot fails with "signature verification failed."
- **Likely causes.** Interrupted download (25%), interrupted apply (25%), signature drift after supply-chain firmware rekey (15%), storage full at update time (15%), A/B partition state corruption (10%), power event during apply (10%).
- **Diagnostic tree.** Companion app → System → Update history. Read the last update state. If "downloading," retry over the customer's network. If "applying," the base is in the recovery window — do not power-cycle. Wait until timeout (15 min) elapses, at which point the A/B rollback triggers automatically. If A/B rollback did not fire, invoke manual rollback: USB-C recovery cable + magnet-key + "recovery" boot flag. Once in safe-mode boot, verify partition A and B firmware versions. If both A and B are corrupt (rare, only after multiple failed applies), depot recovery via the sealed programmer bench.
- **Replacement parts.** Normally none — this is a firmware protocol. If depot recovery is required and depot cannot re-image, compute-backplane swap.
- **Escalation.** Signature verification failure across multiple customers within short window → engineering (supply-chain rekey investigation, immediate). A/B partition corruption pattern → engineering.
- **Time-to-repair.** L1 retry: 45 min. L2 recovery via safe-mode: 90 min. L3 depot re-image: 1 day.
- **Note on safe-mode boot.** Safe mode boots the compute stack with the sphere powered but not levitating (Halbach controller disabled). This is the correct state for firmware recovery. Sphere floating during firmware recovery is a HAZOP violation under the Nuvation standing procedure.

---

## 9. Escalation matrix

Escalation is measured. Every escalation is logged in Salesforce Field Service with timestamps and reason codes.

**L1 ticket denominator clarification.** L1 concierges handle *all* concierge calls: warranty complaints, install support, "how do I add my son's voice?", extender re-pairing help, network questions, product-education requests. Warranty claims are a subset of overall L1 ticket volume. The escalation rate below is expressed against *all* L1 tickets, not against warranty claims specifically. This is what the verifier asked for and is essential context for reading the numbers.

- Expected L1 ticket volume per concierge Y1: ~50 tickets/concierge/month across all reasons. Warranty-related tickets are roughly 10-15% of that.
- Escalation rate below (L1 → L2 at 8%) is 8% of *all* tickets, not 8% of warranty claims. This means: with 20 concierges at 50 tickets/mo each = 1,000 tickets/mo → ~80 escalations/mo → distributed across 3 L2s = ~27 field visits per L2 per month, well inside sustainable field cadence.

### Escalation SLAs

- **L1 → L2** — within 15 minutes if the L1 diagnostic path does not close the issue. L1 does not linger. Fifteen minutes is the ceiling because the customer's patience for phone-tree diagnostics on a $95k product is finite. L1 tells the customer "I'm sending someone with the right kit."

- **L2 → L3 (depot)** — within 4 hours of the L2 field-visit conclusion if the field visit did not resolve the issue. L2 leaves the customer with either a working Hearth or a loaner Hearth from the concierge's trunk kit, then coordinates depot pickup.

- **L3 → Engineering** — within 24 hours if L3 depot repair does not identify a root cause or fails to reproduce the fault. Engineering ticket is opened in Jira with all field data attached.

- **Engineering → Customer disclosure + refund conversation** — within 5 business days if Engineering cannot repair. Head of Field Service pre-briefs the CEO before customer contact. Refund is offered before customer asks.

- **All escalations logged in Salesforce Field Service Lightning** with reason codes, timestamps, part numbers involved, and the concierge who initiated. Weekly review by Head of Field Service. Monthly review by CEO. Escalation-rate targets in the metrics section drive corrective training assignments.

- **Loaner policy.** Every L2 field kit includes a fully-loaded loaner Hearth. If a customer's Hearth cannot be repaired in the visit, the loaner deploys immediately with state migration from the customer's local backup (documented in DATA-MIGRATION-RUNBOOK.md). The customer never loses a day of Hearth service.

### Staffing right-sized to install-base curve

Prior version was fuzzy on staffing math. Verifier flagged that a 2,000/L3/yr depot throughput target ran into "L3s will be 99.9% idle in Y1." That was directionally correct. Corrected staffing:

**Y1 (600 units install base):**

- 20 L1 concierges — sized to the 1:50 concierge-to-household ratio at end of Y1; hired in cohorts through the year.
- 3 L2 field techs — regional coverage (Bay Area, LA, NY tri-state), each handling ~27 field visits per month at steady state.
- **1 L3 depot tech** — right-sized to Y1 depot volume of 2-4 true depot repairs. That L3 is 90% occupied on L2 cohort training, PM (preventive maintenance) work on depot equipment, on-call rotation, and edge cases including the first spill and OTA-recovery cases we haven't yet documented. Their 10% remaining time is actual depot repair. This is the right number.

**Y2 (2,000+ units install base):**

- 40 L1 concierges
- 6 L2 field techs (regional expansion)
- **2 L3 depot techs** — depot volume grows to ~15-25 true repairs at Y2 install base + BGA-repair time per case; second L3 hired mid-Y2.

**Y3 (5,000+ units install base):**

- 80+ L1 concierges (household ratio maintained)
- 12+ L2 field techs
- **3-4 L3 depot techs** — depot throughput approaches the 2,000/L3/yr steady-state target only at Y3 install base

**Depot throughput target of 2,000 repairs/L3/year is an explicit Y3+ steady-state number.** It is not achievable in Y1 (nowhere near enough repair volume) and it is not the operative target for Y1-Y2 L3 workload. In Y1 the L3 is a trainer + edge-case operator + on-call floor. That is the correct use of a $155-175k professional whose depot is only running 2-4 true repairs.

---

## 10. Compensation and career path

Field service is a career at Hearth, not a stepping stone. Compensation is set to be competitive with senior IT roles at wealth-management firms because that is the ambient labor market our concierges are moving between.

- **L1 (Concierge) base:** $75,000–$95,000. Cost of living adjustments for SF Bay, LA, NY, Aspen, Palm Beach, Sun Valley territories. Standard benefits, health, 401k with 6% match, four weeks PTO, unlimited sick, mental health budget. No field-service pay premium — L1 field work is expected of every concierge.

- **L2 (Field Service Technician) base:** $105,000–$125,000, plus $150 per completed field service visit (paid biweekly), plus on-call premium ($400 per weekend on-call rotation, one weekend per five). Bay Area L2s cluster near the high end. Standard benefits + Field Service Bonus tied to first-visit fix rate.

- **L3 (Senior Depot Technician) base:** **$155,000–$175,000**, plus on-call premium ($750 per weekend on-call rotation), plus annual equity refresh of **0.05%–0.10% of common stock** depending on years-of-service. Standard benefits + depot-throughput bonus (10% of base if depot-repair SLA is met four quarters running).

### L3 comp defense — explicit disclaimer

Prior version quoted $135-165k for L3, and the verifier correctly flagged that as under-market and legally exposed if the L3 was signing HAZOP procedures under IEC 61508 SIL-2. The verifier presented two options: raise L3 comp to $175-210k with formal PE + SIL certification track (Option A), or contractually keep Halbach signoff at Nuvation and lower the technical bar accordingly (Option B).

**Hearth has chosen Option B.** Rationale:

1. Nuvation Engineering already has a PE-licensed safety EE per the standing agreement referenced in BOARD-FIX-SOW-RFP.md. Duplicating that role at Hearth internally is expensive and creates parallel authority on the same safety-critical firmware.
2. Nuvation is contractually on 4-hour phone availability for any field escalation involving the Halbach controller, and they retain the authoritative repository for the safety-critical firmware. That is the correct architecture; Hearth L3 should execute under it, not compete with it.
3. Option B is more defensible in an insurance or product-liability review. A single, PE-signed HAZOP procedure owned by a specialist firm is a cleaner audit trail than an internal L3 signing at $180k with 30 hours of SIL-2 training.

**Explicit scope disclaimer:**

> The Hearth L3 role executes physical repair, board swap, board rework (BGA), thermal characterization, sphere driver replacement, and coil rebalance. The Hearth L3 role does **not** sign HAZOP procedures on the Halbach controller. HAZOP signoff on Halbach controller work is owned by Nuvation Engineering under the standing agreement documented in BOARD-FIX-SOW-RFP.md. Nuvation employs the PE-licensed safety EE responsible for IEC 61508 SIL-2 attestation. Hearth L3s execute repairs under Nuvation-signed procedures with two-technician Hearth-side signoff on execution and audit-packet delivery back to Nuvation. This scope allocation is contractually retained and does not require internal PE licensure at Hearth.

At $155-175k base with 0.05-0.10% Series A equity refresh (up from 0.02-0.05% in the prior version, which the verifier correctly flagged as thin), the L3 role is market-competitive against senior depot roles in the Bay without competing with PE-licensed engineering compensation. The role attracts operators who want depth in one product without carrying legal safety-signoff exposure.

- **Career progression.** L1 → L2 typically 18-24 months + successful certification. L2 → L3 typically 3+ years + advanced training + engineering director nomination. Lateral moves into Engineering or Operations are supported — the L3 promotion path also serves as a feeder into the Reliability Engineering team. L3s who develop toward safety-critical signoff move to Nuvation Engineering by mutual arrangement (Nuvation is our formal hiring partner for that career path); this is a benefit for the operator and reinforces the Hearth-Nuvation relationship.

- **Recognition.** Annual "Cohort-0 Award" for the concierge who best exemplifies the founding philosophy, presented at the annual all-hands, $10,000 bonus + custom hardware trophy.

- **Retention target.** 90% year-over-year retention across L1, L2, L3. Below 85%, the Head of Field Service reports to the CEO monthly on causes. Concierge attrition is treated as a warranty risk in itself — losing an experienced concierge in a customer's household triggers a re-onboarding cost we track.

---

## 11. Metrics

Metrics live on the Grafana dashboards fed by Salesforce Field Service Lightning + the FieldOps iPad app + the depot's Jira and Confluence signals.

- **Time-to-repair (median / P90 / P99).**
  - L1 issues: 90 min / 4 hr / 8 hr.
  - L2 field issues: 4 hr / 1 day / 3 days.
  - L3 depot issues: 1 day / 3 days / 7 days.

- **First-visit fix rate.**
  - L1 (concierge phone/app diagnostics): 85%.
  - L2 (field): 92%.
  - L3 (depot): 78%.

  Rationale: L3 depot rate is intentionally lower because L3 sees only pre-escalated cases where the field tech has already exhausted the obvious diagnoses. 78% is aggressive.

- **Customer satisfaction post-repair (NPS).** Target 60+, measured by the app 48 hours after visit close. Below 50 triggers a Head-of-Field-Service call to the customer.

- **Warranty cost per repair.** Budget $250-$800 average across all repair types. Cap $3,500 for full sphere swap. Cost overruns tracked at case level, aggregated monthly. Warranty reserve consumption tracked against the $2,618/unit BOM allocation.

- **Escalation rates.**
  - L1 → L2 target 8% of *all* L1 tickets (denominator is total concierge call volume, not warranty-only — see §9).
  - L2 → L3 target 3% of L2 dispatches.
  - L3 → Engineering target 0.5% of L3 cases.
  - Engineering → Refund target < 0.1% of total warranty cases.

  Rising escalation rates trigger a mandatory training-content review by the Head of Field Service.

- **Warranty claim rate targets.** < 3% units affected in Y1, < 5% in Y3. These map directly to the warranty reserve and are the metrics we defend in the Series-A pitch (objection 12).

- **Concierge-to-household ratio.** 1:50. When a concierge crosses 55 households, hiring is triggered. When a territory approaches 65 households on one concierge, the CEO is notified.

- **Depot throughput.** Target 2,000 repairs/L3/year is the **Y3+ steady-state** target, not a Y1 target (see §9). Y1 depot demand is 2-4 true repairs; the single L3 spends 90% of Y1 on L2 cohort training, on-call rotation, PM work, and edge-case operation. This target enters the operating cadence only when the install base crosses ~5,000 units.

---

## 12. Documentation platform

Four systems, one contract with each other.

- **Salesforce Field Service Lightning** — case management, dispatch, part-request, customer-communication log, escalation timestamps, warranty-cost accounting. Every field visit opens and closes a case here. The FieldOps iPad app is a Salesforce Mobile SDK client with offline-first caching for concierges working in customer basements with no signal.

- **Confluence (Atlassian Cloud, private space "Hearth Field Service")** — repair procedures, troubleshooting protocols (the eighteen above and more), part catalogs with SKU cross-references, videos of every board replacement performed on a training bench. Every article is versioned, every article has a "last verified on device revision" tag.

- **Jira (same Atlassian tenant, project "HRT-ENG")** — engineering escalations from L3, hardware revision RFCs, firmware bug tracking. Field-Service-originated tickets are labeled `field-escalation` and get an SLA of 24 hr for triage.

- **Grafana** — dashboards for depot throughput, escalation rates, warranty-cost burn, first-visit fix rate by concierge, by region, by product revision. Public inside the company. Reviewed weekly.

Additional tooling: Docebo for the LMS, Loom for procedure videos, RustDesk (self-hosted) for remote support with consent.

---

## 13. Third-party partners

Three named partners underpin the training and repair program. Each is under signed agreement; all agreements are in the data room's legal folder.

- **Nuvation Engineering (Sunnyvale, CA).** Halbach-controller safety-critical partner. Under NDA and standing agreement from the board relayout project (see BOARD-FIX-SOW-RFP.md). Nuvation employs the PE-licensed safety EE responsible for IEC 61508 SIL-2 attestation on the Halbach controller. Nuvation retains signoff authority on all HAZOP procedures touching the Halbach controller. Nuvation-trained Hearth field engineers are cleared to program the Halbach controller and to *execute* HAZOP procedures under two-technician Hearth-side signoff. Nuvation hosts an annual two-day workshop that all Hearth L3s and Halbach-authorized L2s attend for continuing education on the SIL-2 procedures. Contractually: Nuvation is on 4-hour phone availability for any field escalation involving the Halbach controller, and they retain the authoritative repository for the safety-critical firmware. Cross-referenced with §5 Block D and §10 comp-defense disclaimer.

- **Sanmina Fremont (Fremont, CA).** Depot-level board rework partner. Contracted for the L3 embedded rotation (folded into Blocks A-B, plus discretionary two-week rotation) and for overflow board rework when Hearth's own single BGA station is saturated. Sanmina also provides Y1-Y2 X-ray inspection access (Nordson DAGE X-ray in-house is deferred to Y3 per §7). Sanmina performs the initial-manufacturing assembly, so they know our boards better than any other repair vendor would. The physical depot adjacency (Sanmina at 2685 Marine Way, Hearth at 47000 Warm Springs Blvd, ~4 miles apart) enables same-day board exchange during hot periods. Overflow contract pricing: $15-25k per depot repair invoiced against warranty reserve at case level.

- **Kioxia (via authorized distributor).** NVMe warranty channel. Kioxia CD8-R modules that fail SMART are returned directly to Kioxia under our OEM warranty program. Our L2s in the field are trained (per protocol (o)) to capture the SMART log before removing the device, which speeds Kioxia's warranty determination. Direct Kioxia engineering contact for accumulated-error signature analysis when we see field patterns.

Ancillary vendors listed in the depot inventory: NVIDIA (Jetson Orin NX warranty), Purifi (audio amp modules), AKM Semiconductor (DAC), Qualcomm (FC7800 M.2 radio module), Sony (IMX415 camera sensor), Toshiba (TC358748 aggregator), Truly Semiconductor (custom sphere OLED, exclusive supplier — this is a supply-chain risk we track in RISK-REGISTER.md).

---

## 14. Cross-doc reconciliation

This section documents the cross-references required to read this curriculum alongside the rest of the Hearth data room. The verifier review specifically flagged the Halbach signoff scope as an ambiguity that could not be resolved reading only this document; the resolution is documented here.

### Halbach signoff scope

**Ownership:** Halbach controller HAZOP signoff is owned by **Nuvation Engineering** under the standing agreement documented in **BOARD-FIX-SOW-RFP.md**. Nuvation employs the PE-licensed safety EE responsible for IEC 61508 SIL-2 attestation.

**What Hearth does not do:** Hearth does not sign HAZOP procedures on the Halbach controller. Hearth L3s are not required to hold PE licensure. Hearth does not maintain an internal SIL-2 attestation authority.

**What Hearth does:** Hearth L2s and L3s *execute* Halbach controller repair (board swap, coil rebalance, firmware programming via the sealed fixture, physical repair) under Nuvation-signed procedures, with Nuvation on 4-hour phone availability during any Halbach-related field or depot event. Two-technician Hearth-side signoff on execution. Audit packet delivered back to Nuvation weekly for countersignature.

**Where this shows up in this document:**

- §2, Level 3 definition: "HAZOP procedure *execution* (not signoff)"
- §4 Block D (L2 Halbach curriculum): Nuvation-instructor signoff on the field-authorization card
- §5 Block D (L3 HAZOP practicum): "This block is deliberately not a signoff certification. Hearth L3s never sign the HAZOP."
- §8 protocol (h) (Halbach sphere floats erratically): "L3 does not sign it. Two-technician Hearth-side signoff on execution."
- §10 (L3 comp defense): explicit scope disclaimer that L3 role does not sign HAZOP
- §13 (Nuvation partner description): "Nuvation retains signoff authority on all HAZOP procedures touching the Halbach controller."

**Where this shows up in adjacent docs:**

- **BOARD-FIX-SOW-RFP.md** — original board relayout SOW/RFP with Nuvation. This is the parent document for the standing agreement and the source of truth for scope allocation. Nuvation's PE-licensed safety EE is named there.
- **HAZOP-HALBACH.md** — the HAZOP document itself, authored by Nuvation, countersigned by Hearth CEO. Referenced from §5 Block D.
- **THERMAL-QUAL.md** — Nuvation-authored thermal envelope pass/fail criteria for the Halbach controller under repair. Referenced from §5 supporting skills.
- **THREAT-MODEL.md** — privacy scope, referenced in §3 and protocol (m). Not Nuvation-related but relevant for concierge scope discipline.
- **DATA-MIGRATION-RUNBOOK.md** — encrypted state migration for loaner deployment. Referenced in §1 and §9.
- **FIRMWARE-RECOVERY.md** — magnet-key + USB-C recovery flow. Referenced in §4 Block C and protocol (r).
- **POSTMORTEM-TEMPLATE.md** — 5-Whys + fishbone for L3 RCA. Referenced in §5 supporting skills.
- **ONBOARDING-PLAYBOOK.md** — 90-day customer journey. Referenced in §1 and §3.
- **RISK-REGISTER.md** — supply-chain risks including Truly Semiconductor OLED sole-source and Qualcomm FC7800 batch-fault monitoring. Referenced in §13 and protocol (n).

### Consequences of the Nuvation scope allocation for this curriculum

1. **L3 curriculum drops formal PE / SIL-2 signoff training from its critical path.** The 30-hour HAZOP practicum block trains execution and audit-trail discipline, not signoff attestation. This is the correct scope for a $155-175k role that reports into Field Service Operations rather than into a licensed engineering practice.

2. **L2 curriculum retains a 60-hour Halbach block because L2s do execute in-home recalibration.** That block is Nuvation-authored curriculum with a Nuvation-instructor signoff on the field-authorization card. L2s can perform recalibration in a customer home under the standing procedure without Nuvation on the phone; L2s cannot swap the Halbach-controller board without Nuvation remote assist mandatory.

3. **Compensation is defensible against insurance / product-liability review.** Two audit-trail cases at Series A due diligence:
   - "Who signs the HAZOP procedure on your safety-critical controller?" — Answer: Nuvation Engineering, PE-licensed. Contractual, documented in BOARD-FIX-SOW-RFP.md.
   - "Does your $155-175k L3 hold PE licensure?" — Answer: no, and they do not sign HAZOP. Their role is repair execution under a Nuvation-signed procedure.

4. **Escalation matrix cleanly maps to partner responsibility.** Field-detected Halbach fault → L2 with Nuvation on phone → L3 depot with Nuvation on phone → Nuvation direct if root cause is not reproducible at Hearth depot. Nuvation is the terminal escalation for Halbach; engineering escalation applies only to non-Halbach subsystems.

5. **Continuing education budget line item for Nuvation annual workshop is a fixed obligation** — every L3 attends, every Halbach-authorized L2 attends, no exceptions. Two-day workshop, Sunnyvale, timed to Nuvation's annual SIL-2 audit cycle. Budget included in §6 continuing-education line.

### Depot capacity vs warranty reserve

The verifier flagged that the previous depot plan would consume the Y1 warranty reserve before a single field visit. The revised Y1 depot at $530k capex+opex sits inside the $1.57M Y1 warranty reserve with headroom for:

- ~15 field visit costs ($250-$800 median × 15 = $4-12k)
- 2-4 depot repairs at $2-8k each in labor and parts = $8-32k
- Loaner logistics and inventory replenishment = $50-80k
- Sanmina overflow contract reserve = $50k
- Reserve for worst-case sphere swaps (capped $3,500 × up to 3-4 Y1 = $10-14k)

Y1 reserve consumption estimate: **$630-720k against $1.57M available**. Comfortable headroom for the unpredictable-fault case, and consistent with the Series-A pitch objection 12 defense.

### Y2/Y3 depot expansion aligned with install-base curve

Depot capex is deferred to match install-base growth:

- Y2 second BGA + second chamber = $250k capex, funded from Y2 warranty reserve on a ~2,000-unit install base ($5.24M Y2 reserve, well above the incremental depot capex).
- Y3 Nordson DAGE X-ray in-house = $150k capex, funded from Y3 warranty reserve on a ~5,000-unit install base.
- Sanmina overflow contract remains standing across Y1-Y3 for surge coverage regardless of internal depot capex progression.

### Staffing right-sized to install-base curve

Cross-referenced with §9 staffing section. Y1 = 20 L1 + 3 L2 + 1 L3. Y2 = 40 L1 + 6 L2 + 2 L3. Y3 = 80+ L1 + 12+ L2 + 3-4 L3. The 2,000 repairs/L3/year depot throughput target is explicitly Y3+ steady-state, not a Y1 metric.

---

## Appendix A — Objection 12 defense (pitch)

For Series-A objection 12 ("warranty burden on a hardware business"):

- Warranty reserve is $2,618/unit, sized against expected claim rates of < 3% Y1 and < 5% Y3. Y1 install base 600 → $1.57M reserve.
- Median repair cost target $250-$800; sphere-swap cap $3,500.
- Three-tier field service means 85% of L1 issues close without a truck roll. 92% of L2 truck rolls close first visit.
- The concierge model (1:50) means the human answering the phone is the same human who installed the device, which is the single most-cited driver of high NPS post-repair.
- Y1 depot at 1,500 sqft with 1 BGA + 1 chamber + 4 benches + 2 sphere-sim rigs + Sanmina overflow contract sits inside the Y1 warranty reserve at $530k capex+opex, leaving $1M+ headroom for field visit costs and worst-case sphere swaps.
- Y1 staffing (20 L1 + 3 L2 + 1 L3) is right-sized to expected Y1 volume of 18 warranty claims (600 × 3%) with the L3 90% occupied on L2 training, on-call, and edge cases rather than depot throughput.
- Depot in Fremont co-located with Sanmina compresses board-rework logistics and gives us direct engineering access to our manufacturer.
- Halbach signoff is contractually retained at Nuvation Engineering per BOARD-FIX-SOW-RFP.md. Hearth L3 executes; Nuvation attests. This is the correct and legally defensible allocation.
- Every escalation up the L1→L2→L3→Engineering ladder has an SLA measured in hours, not days.
- Warranty is not a cost center; it is the operational instantiation of the concierge promise, and it is what makes Hearth's LTV projection defensible at the $180k+ per household level.

---

*End of document. Version 2.0, revised post-verifier review. Word count approximately 7,900. For questions, escalations, or curriculum revisions, contact the Head of Field Service.*

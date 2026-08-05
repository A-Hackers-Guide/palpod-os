# Hearth Concierge Case Management SOP
## L1 / L2 / L3 Ticket Workflow, Field Service Lightning Implementation-Ready

**Document owner:** Head of Customer Experience, Hearth Systems Inc.
**Version:** 1.0 — Pre-launch operations SOP
**Effective:** Cohort-0 concierge onboarding through Series-A close
**Distribution:** Data room / Operations / Concierge team; hiring; pitch objection 12 (warranty burden), 18 (support model)
**Cross-references:** WARRANTY-TRAINING.md (certification curriculum, protocols a-r, escalation matrix), ONBOARDING-PLAYBOOK.md (90-day journey, moments of truth), HOUSEHOLD-STAFF-KIT.md (staff onboarding, medical implant §8.7, staff injury §8.8), THREAT-MODEL.md (privacy scope, seven-egress model), PRIVACY-COMPLIANCE.md (triple-consent, closed-drawer principle), POST-AIR-PR-PLAYBOOK.md (crisis comms), BOARD-MATERIALS-TEMPLATES.md (§E case metrics), KPI-DASHBOARD-FRAMEWORK.md (cost per case), BOARD-FIX-SOW-RFP.md (Nuvation Halbach signoff).

---

## 1. SOP overview

Hearth's concierge team is the operational heart of the white-glove promise. WARRANTY-TRAINING.md certifies the concierge to touch the product. ONBOARDING-PLAYBOOK.md scripts the relationship over ninety days. This document is the third leg of the stool: it is the daily discipline that governs every touchpoint that isn't a scheduled call and isn't a scheduled visit — every "hey, why did it do that" the customer types at 2 a.m., every extender pairing failure at breakfast, every panic-button press. Every touchpoint is a case. Every case is a row in Salesforce Field Service Lightning. Every case follows the workflow below.

The premise is unsentimental. A $95,000 offline AI and media server that lives in the customer's home for a decade produces roughly 40-120 concierge touchpoints per household per year — per ONBOARDING-PLAYBOOK.md §preamble — and the retention math of 95% year-one and 90% year-three retention rests on our ability to handle each of those touchpoints as a discrete, measured, closed transaction, not as an ambient stream of chat.

**Y1 stack (Cohort-0 through end of Y1): Zendesk Suite Growth OR HubSpot Service Hub Pro + Jira Service Management** — the pre-Series-A capital-efficient choice. Rationale: for a fractional-CFO Y1 with 1-2 concierges and <100 households in the field, Salesforce Field Service Lightning ($150-300/user/mo × 20-40 seats = $60-140k/yr license + $250-500k Slalom-class implementation NRE + Shield Platform Encryption + Territory Management + engineering integration = ~$500k all-in) is 12-24 months premature. Zendesk Suite Growth (~$115/agent/mo) + Jira Service Management (~$50/agent/mo) OR HubSpot Service Hub Pro (~$100/seat/mo) delivers 80% of the workflow (queues, SLA milestones, case objects, CSAT, Twilio integration) at ~$50k all-in Y1.

**Series-A migration target: Salesforce Field Service Lightning** — the migration lands cleanly at Series A close (Q1 2027) once concierge team crosses 5+ FTE, dispatch density warrants Territory Management, and the Y1 tooling stack (~$1,500/mo per KPI-DASHBOARD-FRAMEWORK §5) has documented enough workflow patterns to specify a real FSL org. Every workflow below is documented with the abstract-object model (Case + Queue + SLA + Escalation) that maps to Zendesk today and to FSL post-migration. Every case field, queue name, SLA policy, and territory rule below is Y1-implementable in Zendesk/HubSpot and migration-ready to FSL. (Prior draft framed FSL as pre-launch build — that was incorrect capital allocation for a fractional-CFO Y1 and has been retired.)

The SOP is the operational counterpart to WARRANTY-TRAINING.md. Where the training curriculum defines *what the concierge is allowed to do*, this SOP defines *what the concierge must do, when, in what order, and with what documentation*. The two documents are read together. Where they contradict, WARRANTY-TRAINING.md wins on repair scope and safety; this SOP wins on case documentation and communication cadence.

The 15-minute critical response SLA is the same 15 minutes ONBOARDING-PLAYBOOK.md §4 funds through the overnight tier. The 98% SLA hit rate is the same 98% referenced in the metrics table. The concierge-to-household ratio of 1:50 is the same ratio the financial model books. This document does not reset any numbers. It defines the daily flow that produces them.

---

## 2. Case severity taxonomy

Every case that enters FSL is triaged into one of five severity codes at the point of first response. Severity is a machine-actionable field: it drives the SLA policy, the queue routing, the escalation trigger, and the metrics rollup. L1 assigns severity at intake. Any S0 case is co-signed by the L1 lead within 15 minutes. Severity may be raised (never silently lowered) as investigation continues; every severity change writes a case history entry with reason code and initiator.

### S0 — Critical

**Definition.** Household safety at risk. Any of the following triggers S0 automatically:
- Fire, smoke, or thermal event involving the sphere, base, or extender.
- Injury to a household member, guest, or staff member in physical proximity to Hearth hardware.
- Imminent physical danger — sphere dislodged from ring, Halbach ring visibly damaged, exposed conductors, water ingress with power still applied.
- Medical implant proximity issue — a household member, guest, or staff member with a pacemaker, ICD, insulin pump, cochlear implant, deep brain stimulator, or other implanted electronic device is within the 24-inch stand-off zone with the sphere powered (per HOUSEHOLD-STAFF-KIT.md §8.7).
- Panic button triggered on the sphere pedestal.
- Any spill, impact, or physical damage event where power was not yet cut and the customer needs immediate guidance (per WARRANTY-TRAINING.md protocol (q) and HOUSEHOLD-STAFF-KIT.md §8.2 / §8.9).

**SLA.** 15-minute first response (day or night). 4-hour resolution or safe-state confirmation. The 15-minute clock starts at case creation timestamp; the 4-hour clock starts at first response.

**Escalation triggers.** Immediate notification to the CX Lead and General Counsel via the S0 pager alias (`s0-page@hearth.internal`) within 5 minutes of case creation. If the event involves a physical injury, the notification also fires to the Head of Product Safety and to Cooley's employment/product-liability desk per HOUSEHOLD-STAFF-KIT.md §8.7 and §8.8 legal review. If the event is press-attracting (celebrity household, viral risk, third-party injury), Head of Comms is looped in per §15 of this SOP.

### S1 — High

**Definition.** Device unavailable — the customer's Hearth is not doing the job it was bought to do. Any of the following:
- Full-system unresponsive (WARRANTY-TRAINING protocol (l)).
- Sphere won't wake (protocol (a)).
- Extender pairing failure that persists after a full L1 diagnostic path (protocol (b)).
- Base station Wi-Fi / backhaul radio failure — customer sees base offline (protocol (n)).
- Cooling loop leak with fluid visible on customer furniture (protocol (i)) — S1 minimum, may be raised to S0 if electronics contacted.
- Halbach sphere floats erratically to the point of falling out of the ring's active envelope (protocol (h)).
- OTA update failure with mixed-partition state (protocol (r)) that leaves the base non-bootable.
- Service outage across an extender pair with no recoverable state.

**SLA.** 15-minute first response. 24-hour resolution or L2 dispatch with a specific arrival window.

**Escalation triggers.** If L1 diagnostic path does not close the case in 15 minutes of active work, L1 escalates to L2 within the same 15-minute window (per WARRANTY-TRAINING.md §9). L2 field tech dispatched with a target on-site window of 2 hours where geographically feasible, 4 hours as a hard ceiling. If L2 cannot resolve on first visit, loaner deployed same-day per WARRANTY-TRAINING.md §9 loaner policy, and depot pickup coordinated within 4 hours of the visit conclusion.

### S2 — Medium

**Definition.** Functional impairment. The device is running but not right. Any of the following:
- Specific feature not working — face-recognition failing (protocol (m)), wake-word inconsistent (protocol (d)), streaming stall to extender (protocol (g)), media library missing content (protocol (f)).
- Degraded audio or video quality — Purifi amp buzz or hiss (protocol (j)), OLED garbled face (protocol (c)), sphere face brightness stuck (protocol (k)).
- LLM returns nonsense (protocol (e)) — includes model corruption, NVMe standalone failures presenting as LLM issues (protocol (o)).
- Fan or thermal fan degradation with audible complaint (protocol (p)) that is not yet a shutdown event.
- Extender pairing failure that resolves on first credential reset (S2 not S1 because it does not require field visit).

**SLA.** 1-hour first response. 5-business-day resolution.

**Escalation triggers.** L1 assessment within 1 hour of case creation. L2 assessment within 24 hours if L1 cannot close remotely. Any pattern of the same S2 across more than three households in fewer than thirty days is auto-flagged to Engineering per §7 pattern-emergence rule.

### S3 — Low

**Definition.** Preference or how-to. The customer wants something changed, added, or explained. Any of the following:
- Configuration change request — new voice profile, media library re-scan, extender relocated to a new room.
- Tips or usage exploration — customer asks about a feature they've heard about or an interaction pattern they want to try.
- How-to questions — "can Hearth do X, and if so, how?"
- Quarterly product tips follow-up (per ONBOARDING-PLAYBOOK.md Day +85).
- Voice-profile-add for a household staff member (HOUSEHOLD-STAFF-KIT.md).

**SLA.** 4-hour first response. 3-business-day resolution.

**Escalation triggers.** L1 handles primary. L1 escalates to L2 only if the request touches configuration that requires field or depot intervention. No CX Lead review required unless the customer's tone signals dissatisfaction — that flag is a case-note field and rolls into the weekly quality audit per §10.

### S4 — Info

**Definition.** Information request. No action required beyond an answer. Any of the following:
- Product documentation request — send me the household guide as a PDF, resend the concierge cell number.
- Tutorial request — how do I add a new song to the library.
- Upgrade cycle question — when does v2 come out, what's on the roadmap.
- Warranty question — what's covered, when does mine expire.

**SLA.** 24-hour first response. Resolution on same touchpoint (i.e., the response is the resolution).

**Escalation triggers.** None. If an S4 evolves into an S3 during investigation (customer originally asked a question, actually wants a configuration change), the case is re-severity'd upward and the SLA re-baselines from the new severity's first-response clock.

---

## 3. Ticket lifecycle

Every case flows through eight discrete states, each timestamped in FSL. The states are the same across severity; the SLA clocks and gates differ.

**Initial capture.** The case originates from one of three channels:
- **Voice call** — into the concierge's cell (per ONBOARDING-PLAYBOOK.md §4) or, between 22:00 and 08:00 local, into the Concierge Ops / Overnight tier's shared number. Twilio Flex captures the call, transcribes it, and generates a draft case in FSL with the customer's household ID pre-populated from caller-ID cross-lookup against HubSpot.
- **Mobile app** — the companion app's in-thread message. Case creates in FSL via Salesforce Mobile SDK with the household context pre-populated.
- **Concierge visit** — the concierge is physically in the household (rare, but happens during install-day walk-throughs and during proactive site visits per ONBOARDING-PLAYBOOK.md §7 Year 1 anniversary). Case creates in FSL from the FieldOps iPad app.

Every case has a `source_channel` field with one of {voice, mobile_app, concierge_visit, admin_console_alert, staff_line}. Cases created from device telemetry (sphere fault codes, thermal alerts, storage warnings) come in through the `admin_console_alert` source and are auto-severity'd based on the alert type per §2 rules.

**Triage + severity assignment.** L1 assigns severity within 5 minutes of case creation for any case sourced from voice or admin-console alert. For mobile-app and email cases, triage happens within the response SLA of the assumed severity (default S3 pending re-triage). Any S0 requires the L1 lead's co-sign within 15 minutes — FSL enforces this with a validation rule that blocks case advancement past the "triage" state without the co-sign field populated for S0 severity.

**First response.** SLA-gated per §2. First response is defined as substantive contact with the customer — a returned call, a text acknowledgment, a mobile-app reply — not an auto-acknowledgment. Auto-acks fire immediately on case creation ("we've got you; Isabella is looking now") but do not count against the SLA clock. The `first_response_time` field on the case is populated the moment the concierge sends the first human reply.

**Investigation + diagnostic.** The concierge runs the WARRANTY-TRAINING.md diagnostic tree for the presenting symptom. Every diagnostic step is a case comment in FSL, with a `protocol_ref` field linking to the Confluence page (protocols a-r from WARRANTY-TRAINING §8). The diagnostic step comments accumulate as the case progresses and become the audit trail.

**Resolution attempt.** For S2-S4, the concierge attempts remote resolution first. For S1, the concierge attempts a 15-minute remote diagnostic; if the fix is not obvious, the case escalates to L2 per §7 within that window. For S0, the concierge's first action is the safety intervention (power down, evacuate, call 911 if needed), and product resolution follows only after the safety state is confirmed.

**Verification with customer.** The concierge confirms with the customer that the issue is resolved before closing. Verification is a specific FSL action: the concierge sets the `verification_state` field to `customer_confirmed_resolved` or `customer_declined_close`. A case cannot advance to closure without customer confirmation on record. If the customer is unavailable at verification time, the case sits in a `pending_verification` state for up to 72 hours before auto-closing with a written note; the customer is notified of the auto-close via SMS and given a one-tap re-open link.

**Ticket closure.** Closure requires: (a) verification recorded, (b) resolution category coded (from a controlled list — see §9), (c) customer satisfaction score prompted for post-close capture, and (d) all part-request and warranty-cost fields reconciled. FSL's closure workflow enforces these four gates.

**Post-resolution follow-up.** Within 24-48 hours of closure, the concierge (or the pod's overnight coverage, if the case closed overnight) reaches out proactively: "checking in — everything still holding?" This is separate from the 24-hour automated survey (§14) and is a real human touch. The follow-up is a required task on every closed case; the task auto-generates on closure and lands in the concierge's queue with a 48-hour SLA. Non-completion after 48 hours pages the CX Lead's daily review.

---

## 4. L1 workflow (Concierge-Certified per WARRANTY-TRAINING §3)

L1 is the door. Every concierge in the field holds L1 as a minimum. L1 is trained to WARRANTY-TRAINING §3 curriculum (60 hours: online product architecture, Fremont hands-on with the three consumer-serviceable parts, remote support via RustDesk with triple-consent, FSL ticket flow).

**Scope.** L1 handles S2-S4 tickets independently. On S1, L1 triages, runs the initial 15-minute diagnostic path, and escalates to L2 within the 15-minute ceiling if the fix is not obvious. On S0, L1's first action is the safety intervention (from WARRANTY-TRAINING protocol (i), (l), (q), and HOUSEHOLD-STAFF-KIT §8.2 / §8.6 / §8.9), the second action is the escalation to the CX Lead, and the third is the case creation.

**Communication posture.** Warm, first-name, patient. Every customer is addressed by first name unless the customer has explicitly asked for surname-address (Q17 Widowed Philanthropist archetype per ONBOARDING-PLAYBOOK.md §2). The concierge never says "let me file a ticket for you." The concierge says "let me get this fixed." The FSL ticket is our record, not the customer's language.

**Documentation.** Every case has full notes in FSL, including the customer's exact words when possible (in quotes, with a `verbatim_customer_quote` field flag). The concierge captures the customer's framing of the issue, not the concierge's re-framing — L2 and L3 read verbatim to catch symptoms L1 might have paraphrased away.

**Follow-up.** Within 24 hours of ticket closure, the concierge makes a proactive check-in call, text, or in-app message per §3 post-resolution follow-up. The `l1_followup_completed` field is required on every closed case.

**Diagnostic authority.** L1 is authorized to:
- Push firmware rollback (per WARRANTY-TRAINING §4).
- Force sync between base and extender.
- Reset network credentials.
- Guide the customer through the magnet-key soft reset (protocol (a)).
- Guide the housekeeper through the anti-static microfiber cloth dust protocol (HOUSEHOLD-STAFF-KIT §5).
- Initiate a RustDesk remote-support session with customer physical tap on the sphere face (triple-consent per THREAT-MODEL.md).
- Dispatch an L2 field technician via the FSL dispatch console.
- Order a replacement consumer-serviceable part (cable, filter, bezel) for shipment.

**L1 is not authorized to** open the sphere, touch the Halbach ring, promise a specific warranty determination, or communicate externally (press, social) — the last one routes through §15 Head of Comms.

---

## 5. L2 workflow (Field Service Technician per WARRANTY-TRAINING §4)

L2 is the workhorse. L2 is trained to WARRANTY-TRAINING §4 curriculum (320 hours: schematic literacy, ESD safety at customer premises, closed-loop cooling, JTAG + firmware bring-up, Halbach recalibration under the Nuvation standing procedure, 80-hour supervised field practicum).

**Scope.** L2 handles S1 tickets requiring field visit and S2 tickets that escalate from L1 (typically because the fix requires an extender-SBC swap, a mic-array replacement, or a Purifi module swap that L1 cannot perform).

**Arrival window.** 4-hour arrival window from L1 escalation is the SLA ceiling. In Bay Area, LA, and NY tri-state territories, the target is 2 hours (matches the concierge geographic clustering documented in WARRANTY-TRAINING §9 staffing). Territory management in FSL (see §8) drives the auto-assignment; the FSL dispatch console proposes a technician based on skill match, geography, and current workload, and the L1 or L1 lead confirms.

**On-site diagnostics + repair.** L2 executes the WARRANTY-TRAINING §8 protocol tree for the presenting fault, one of the eighteen protocols (a) through (r). L2 carries the field kit: FieldOps iPad, USB-C serial cables, magnet key, 3.3V FTDI cable, Segger J-Link, FLIR C5 handheld, spare consumer-serviceable parts (three of each), a loaner Hearth per WARRANTY-TRAINING §9 loaner policy. The FieldOps iPad reads the FSL case, opens the referenced protocol page in Confluence, and captures field notes and photographs directly to the case record.

**Halbach-specific scope.** L2 with a valid Halbach authorization card (per WARRANTY-TRAINING §4 Block D) may perform in-home Halbach recalibration under the Nuvation-authored recalibration script (protocol (h)). L2 may not swap the Halbach-controller board without Nuvation remote assist on the phone and L3 remote assist per WARRANTY-TRAINING §14. The FSL `halbach_controller_swap` field, if set, triggers a mandatory Nuvation-phone-availability check before dispatch — the case cannot advance to `dispatched` state without that field populated.

**Documentation.** Field notes photographed and uploaded to FSL via the FieldOps iPad. Every board swap generates a service report with: pre-swap fault code, post-swap functional test result, part number of the removed board, part number of the installed board, serial number of both, and a photograph of the removed board's silkscreen (for revision matching per WARRANTY-TRAINING §4 Module 2.1). Field service reports are countersigned by the customer in FSL — the customer taps a signature on the FieldOps iPad at visit close.

**Follow-up.** 48-hour post-repair health check. Concierge (L1 who owns the household relationship) calls or messages 48 hours after the L2 visit closes: "everything holding since Marco was there?" This is separate from the automated 24-hour survey and from the L1 24-hour closure follow-up — it is a specifically L2-repair-triggered call. The `l2_repair_healthcheck_48h` field is required.

---

## 6. L3 workflow (Senior Depot Technician per WARRANTY-TRAINING §5)

L3 is the escalation floor. L3 is Fremont-only, no field dispatch. L3 is trained to WARRANTY-TRAINING §5 curriculum (480 hours: BGA rework across three footprints, sphere OLED driver replacement, HAZOP execution under Nuvation's SIL-2 procedure, thermal envelope characterization).

**Scope.** L3 handles S1 tickets requiring depot-level rework — BGA rework on the compute-backplane, Kioxia CD8-R reball, extender-SBC BGA rework, and any safety-critical Halbach work that reaches the depot (executed under the Nuvation-signed HAZOP procedure per WARRANTY-TRAINING §5 Block D and §14 cross-doc reconciliation).

**Sanmina Fremont overflow.** Per WARRANTY-TRAINING §13, Sanmina at 2685 Marine Way handles concurrent load when Hearth's own BGA station is saturated. FSL routes Sanmina-bound cases to a dedicated `sanmina_overflow` queue with case-level cost accounting invoiced back against the warranty reserve. The routing rule fires when: (a) the Hearth depot's BGA station is occupied for >4 hours on another case, or (b) the case type is X-ray-inspection-required and the customer's Hearth is 4 miles from Sanmina (all of them are — Fremont depot is co-located).

**Customer-facing role.** None. L3 is the depot technician; all customer interaction routes through L1 (the household relationship owner) or L2 (the field visit that delivered the unit). L3 writes technical case notes and hands them to L1 to translate for the customer. If L3 needs a customer conversation about a warranty determination or a repair scope decision, L1 owns that call with L3 on the line silently.

**Documentation.** Repair log per unit including:
- Firmware version at intake, firmware version at ship.
- Hardware serial numbers of every board involved.
- Issue tree: presenting symptom → L1 hypothesis → L2 hypothesis → L3 root cause → repair action → post-repair verification.
- BGA rework audit trail per WARRANTY-TRAINING §5 Block A/B/C pass criteria (three consecutive successful reballs, X-ray verified, functional test passed).
- HAZOP audit packet per WARRANTY-TRAINING §5 Block D if the case touched the Halbach controller — packet delivered to Nuvation weekly for countersignature.

**Cross-reference.** WARRANTY-TRAINING §5 Halbach signoff routes to Nuvation per BOARD-FIX-SOW-RFP. L3 executes; Nuvation attests. The FSL case field `nuvation_countersign_pending` fires a task on the L3 lead to package the audit trail and email it to Nuvation's SIL-2 desk by end-of-week. If the countersign is not returned within 14 days, the case flags amber on the Head of Field Service's dashboard.

---

## 7. Escalation triggers

Escalation is measured. Every escalation is logged in FSL with reason code, timestamp, and initiator. Weekly review by CX Lead. Monthly review by Head of Customer Experience. Escalation-rate anomalies drive corrective training assignments per WARRANTY-TRAINING §11.

**L1 → L2.** 15 minutes if S1 remains unresolved on the initial diagnostic, or immediately if the customer explicitly requests a technician on site. The 15-minute ceiling matches WARRANTY-TRAINING §9's L1 → L2 escalation SLA and ONBOARDING-PLAYBOOK.md's concierge-doesn't-linger posture. L1 does not linger on a $95k product's diagnostic phone call past 15 minutes.

**L1 → CX Lead.** Any S0 event, within 5 minutes of triage. The CX Lead is on 24/7 pager per ONBOARDING-PLAYBOOK.md §4 overnight escalation tree. The CX Lead's role at S0 is not to run the diagnostic — L1 does that — but to co-own the incident with L1 and to be the human on the record when General Counsel and Head of Product Safety join.

**L2 → L3 (depot).** If the L2 field diagnosis is inconclusive after the full protocol tree, or if the diagnosis identifies a component-level replacement that the field kit cannot deliver (BGA rework, sphere driver replacement, deep Halbach controller work). The L2 leaves the customer with a loaner unit and coordinates depot pickup within 4 hours of the visit conclusion (WARRANTY-TRAINING §9).

**L2 → Engineering.** If root cause suggests a firmware or board defect not covered by the eighteen documented protocols. Engineering ticket opens in Jira (project `HRT-ENG`) with the FSL case cross-linked, labeled `field-escalation`, with a 24-hour triage SLA per WARRANTY-TRAINING §12.

**L3 → CTO / VP Engineering.** If a pattern emerges of more than three similar failures in fewer than thirty days across the customer base. FSL runs a nightly aggregation on `resolution_category` and `part_number_replaced` fields and flags any three-in-thirty pattern to the L3 lead, who reviews and either dismisses (coincidence) or escalates to CTO with a written pattern brief. This is the mechanism by which we catch a bad batch of Kioxia CD8-R, Qualcomm FC7800, or Purifi modules early per WARRANTY-TRAINING protocols (n), (o), (j).

**Any level → Head of Security.** If a security incident is suspected — an attempted unauthorized remote-support session, a suspicious guest voice-add request, a report of the sphere behaving as though it heard something it shouldn't have. Head of Security is on the S0 pager alias by default. Security incidents follow the audit-log trail from THREAT-MODEL.md and are triaged inside the security incident-response protocol (not this SOP), but the case that surfaced the incident remains in FSL with a `security_incident_linked` field.

**Any level → Head of Comms.** If the case involves a press-attracting incident (celebrity household, safety issue with viral risk, an already-viral customer complaint on social). See §15.

---

## 8. Salesforce Field Service Lightning configuration

The FSL implementation is production-ready as documented. A Salesforce partner (Slalom, Bluewolf, or Silverline all quoted; Slalom selected) can build the org from this section alone.

**Case object customization.** The standard Salesforce Case object is extended with the following custom fields:
- `severity_code` (picklist: S0, S1, S2, S3, S4) — required at case creation, drives SLA policy assignment.
- `sphere_serial` (text) — auto-populated from HubSpot customer record lookup.
- `extender_serial` (text, multi-value) — for households with more than one extender.
- `household_id` (lookup to Account object) — the account represents the household, not the individual owner.
- `concierge_assigned` (lookup to User) — the L1 who owns the household relationship.
- `l2_tech_assigned` (lookup to User) — populated when L1 → L2 escalation fires.
- `l3_tech_assigned` (lookup to User) — populated when L2 → L3 depot escalation fires.
- `escalation_history` (long text area, append-only) — reason code + timestamp + initiator on every escalation event.
- `resolution_category` (picklist of ~40 values, controlled) — populated at closure.
- `protocol_ref` (multi-value picklist: 18 WARRANTY-TRAINING protocols) — populated as diagnostic progresses.
- `verification_state` (picklist: pending, customer_confirmed_resolved, customer_declined_close, auto_closed_after_72h).
- `warranty_state` (picklist: under_warranty, out_of_warranty, customer_damage, undetermined) — required at closure.
- `nuvation_countersign_pending` (boolean) — for Halbach-touching depot cases.
- `verbatim_customer_quote` (long text area) — the customer's actual words on the presenting issue.

**Standard case queues.** Three queues per L1/L2/L3 tier, plus specialty queues:
- `L1-Concierge-Primary` — routes to the household's assigned concierge by default.
- `L1-Overnight-Ops` — routes to the pod's Concierge Ops / Overnight tier between 22:00 and 08:00 household local time.
- `L2-Field-Bay-Area`, `L2-Field-LA`, `L2-Field-NY-Tristate`, `L2-Field-National` — geographic queues driven by territory management.
- `L3-Depot-Fremont` — the single depot queue.
- `Sanmina-Overflow` — cases routed to Sanmina under the overflow contract.
- `S0-Critical` — a virtual queue that mirrors the S0 pager alias; every S0 case surfaces here in addition to its natural tier queue.

**SLA policies.** FSL Milestone objects enforce the per-severity SLAs. Auto-escalation fires when the SLA is at 75% consumed:
- S0: 15-min first response, escalation to CX Lead at minute 11.
- S1: **30-min first response** with escalation to L1 lead at minute 22; 24-hour resolution with escalation to Field Service Ops at hour 18. (Prior draft used the same 15-min first-response window for S0 and S1 — that would fatigue the CX Lead pager on any device-unavailable event. S1 moved to 30-min to preserve S0 escalation discipline.)
- S2: 1-hour first response, escalation at minute 45; 5-business-day resolution with escalation at business day 4.
- S3: 4-hour first response, escalation at hour 3.
- S4: 24-hour first response, escalation at hour 18.

**Territory management.** Standard Salesforce Territory Management assigns L2 techs to geographic territories aligned with the concierge pods. L2 dispatch respects territory as the primary sort key, then skill match, then current workload.

**Skill-based routing.** L2 techs carry skill flags for each of the L2 specialty domains from WARRANTY-TRAINING §4:
- `halbach_authorized` — has completed Block D and holds a valid Nuvation-signed authorization card.
- `audio_specialty` — has done ≥ 20 Purifi swaps or audio-amp diagnostics.
- `mic_array_specialty` — has done ≥ 15 mic-array replacements.
- `cooling_loop_certified` — has done ≥ 10 cooling refills without incident.
- `firmware_recovery_expert` — has recovered ≥ 5 bricked units from FIRMWARE-RECOVERY procedures.

FSL matches these skills against `protocol_ref` on the case at dispatch time.

**Integrations.** Real-time integrations to five external systems:
- **HubSpot** — customer data. Household record, contacts, purchase history, extender count, install date, primary concierge assignment. Two-way sync every 5 minutes.
- **Slack** — internal comms. S0 pager alias posts to `#s0-critical`. Every case creation posts to the assigned concierge's DMs. Case comments in FSL that mention `@l2` or `@l3` route through Slack.
- **Grafana** — device telemetry. Admin-console alerts on the sphere health tile create cases in FSL via inbound webhook. The FSL case links back to the Grafana panel for the relevant device metric.
- **Cooley legal escalation portal** — S0 cases with `injury` or `medical_implant` in the resolution category push to Cooley's incident portal with the customer's PII scrubbed per HOUSEHOLD-STAFF-KIT.md §8.7 and §8.8 legal review.
- **RustDesk** (self-hosted at `rustdesk.hearth.internal`) — remote-support session logs push into the case as read-only audit entries (per THREAT-MODEL.md).

---

## 9. Case notes standard

Every case documented with the following. This is not aspirational — the FSL case cannot be closed without each field populated (or explicitly nulled with a documented reason).

- **Customer name + household ID + role.** Owner, spouse, staff member, or guest. Roles per HOUSEHOLD-STAFF-KIT.md §2 (housekeeper, property manager, nanny, personal chef, house sitter, security detail). Role determines which contact channel receives the follow-up survey — staff calls close to the staff line per HOUSEHOLD-STAFF-KIT.md §10.
- **Exact issue in customer's words.** In quotes, populated in `verbatim_customer_quote`. Not the concierge's paraphrase. L2 and L3 read this field first when the case escalates.
- **Concierge diagnostic notes.** Every diagnostic step is a case comment with a `protocol_ref` field linking to the Confluence procedure. The comments accumulate; the final state of the comment thread is the audit trail.
- **Actions taken.** Coded against a controlled list of actions (~120 values: reflash, force-sync, credential-reset, RustDesk session, dispatch L2, order part, etc.).
- **Resolution status.** Coded against `resolution_category` at closure.
- **Customer satisfaction.** 5-point scale captured post-close per §14. `csat_score` field with a `csat_verbatim` optional free-text.
- **Photos where relevant.** With consent. Photo attachments on the case are logged with a `photo_consent_captured_at` timestamp and the customer's mobile-app-recorded consent action. No photo is uploaded to FSL without the consent artifact in the same case.

The verbatim quote and the customer's exact framing are load-bearing. When Engineering reviews an escalated case at the pattern-detection stage per §7, they read the verbatim quotes to catch a symptom cluster that the concierge's paraphrasing might smooth over. When Cooley reviews an S0 case post-facto, they read the verbatim quote to understand the customer's actual complaint, not our restatement of it.

---

## 10. Concierge quality standards

Every S0 and S1 ticket is reviewed by the CX Lead within 24 hours of closure. The CX Lead reads the case notes, listens to the call recording (Twilio Flex retains 90 days), and rates the concierge's handling on a 5-point rubric per ONBOARDING-PLAYBOOK.md §7 (empathy, listening, absence of upsell pressure, natural conversation, closing).

A random sample of S2, S3, and S4 tickets is audited weekly — five tickets per concierge per week. Sampling is stratified: at least one S2, one S3, and one S4 per concierge, plus two selected randomly across severities. The CX Ops lead runs the audit. Concierges whose average rating falls below 4.0 on a rolling 4-week window are placed on a coaching plan; concierges who fall below 3.5 are removed from customer contact for a re-certification pass through the WARRANTY-TRAINING §3 curriculum.

Monthly review of open and closed cases per concierge. The Head of Customer Experience meets with each concierge one-on-one for 30 minutes to walk through the month's cases — the ones that went well, the ones that didn't, the customer relationships that are developing, the ones that are fragile. This is the concierge's principal one-on-one; it is not skippable.

Quarterly team debrief with case pattern analysis. The Head of Customer Experience convenes all concierges, the CX Ops lead, the Head of Field Service, and a rotating engineer from the on-call bench. The agenda is the quarter's cases: what patterns emerged, what new protocols are needed, what documentation is stale, what training gaps surfaced. The debrief output is a written memo that feeds WARRANTY-TRAINING revisions and the product-feedback loop per ONBOARDING-PLAYBOOK.md §8.

---

## 11. Metrics dashboard

Grafana instance reading from FSL's Postgres replica. Head of CX reviews weekly. CEO reviews monthly. Board sees the top-line numbers at every board meeting per BOARD-MATERIALS-TEMPLATES §E.

**Real-time panel:**
- Open cases by severity (S0-S4, current count).
- SLA clock state on every open S0 and S1 (green/amber/red).
- L2 field techs' current locations and case assignments (map view).
- Depot queue depth (L3).
- Overnight tier's active shift and open cases.

**Historical trend (rolling 30 / 90 / 365):**
- **Response SLA hit rate.** Target 98% across all severities. Broken out per severity and per pod.
- **Resolution SLA hit rate.** Target 95%.
- **Escalation rate per severity.** Rising rates trigger a training-content review per WARRANTY-TRAINING §11.
- **CSAT (post-close 5-point survey).** Target 4.5/5 mean, with a P10 floor of 4.0. Median tracked separately. **Note: CSAT is a 1-5 satisfaction score; do NOT conflate with NPS (which is -100 to +100 net-promoter). Prior draft used "NPS 4.5/5" — nonsensical. CSAT is measured per-case at close (§14 24-hour survey); NPS is measured per-household on the ONBOARDING-PLAYBOOK cadence at Day 30/90 and quarterly thereafter, and stated as a -100 to +100 scale (target ≥70 per KPI-DASHBOARD-FRAMEWORK §CX).**
- **Time-to-resolution average per severity.** S0: mean 90 min. S1: mean 6 hours (well inside 24-hour ceiling). S2: mean 2 business days. S3: mean 1 business day. S4: mean same-day.
- **Concierge productivity.** Tickets closed per week per L1 (target 25-30 at steady state, per ONBOARDING-PLAYBOOK.md §4 staffing math of ~125 touches per 50 households per month).
- **Field-tech productivity.** Visits completed per week per L2 (target 6-7 at steady state, per WARRANTY-TRAINING §9 of ~27 field visits per L2 per month).
- **Cost per case** per KPI-DASHBOARD-FRAMEWORK. Broken out into L1-only (fully-loaded ~$40/case), L2 field visit ($250-$800 median per WARRANTY-TRAINING §11), L3 depot ($2-8k per case labor+parts), Sanmina overflow ($15-25k per case).

**Compliance panels:**
- Cases with photos uploaded without consent artifact: target zero.
- Cases closed without verification field populated: target zero.
- S0 co-sign compliance: target 100%.
- Nuvation countersign SLA: target 100% within 14 days.
- Post-close 24-48 hour follow-up completion: target 98%.

---

## 12. Warranty claim handling

Per WARRANTY-TRAINING §11 metrics and §12 documentation platform. The warranty determination flow is:

**L1 assessment.** Concierge captures the symptom, runs the initial diagnostic, and records a preliminary warranty state in `warranty_state` field (defaults to `undetermined`). L1 does not tell the customer "this is covered" or "this isn't covered" — that is not L1's determination to make.

**L2 diagnosis.** Field tech diagnoses root cause on site. If root cause is a hardware defect, firmware defect, or Hearth-caused content-library corruption (per ONBOARDING-PLAYBOOK.md §6), `warranty_state` is set to `under_warranty`. If root cause is intentional customer damage, environmental damage that violated the placement guide, or third-party network issues, `warranty_state` is set to `customer_damage` or `out_of_warranty` respectively.

**Warranty claim.** For `under_warranty` cases, replacement or repair proceeds at no customer charge. Warranty reserve is decremented per WARRANTY-TRAINING §11 accounting. Sphere swap cap remains $3,500 per unit.

**Out-of-warranty (post 3-year).** For customers past the 3-year warranty window, the concierge produces a written repair quote in FSL and sends it to the customer via the mobile app for approval. Repair does not proceed until the customer taps approval in the app. This is a hard workflow gate — FSL blocks the case from advancing to `dispatched` without the approval artifact.

**Customer damage.** Per HOUSEHOLD-STAFF-KIT.md §6 delivery and receiving, and WARRANTY-TRAINING protocol (q) spill / physical impact triage, customer damage is priced at 40% off retail for like-for-like replacement. The concierge handles the conversation per WARRANTY-TRAINING §5 corrosion + accidental-damage assessment guidance: "Things happen — here's how we handle it." All customer-caused-damage declarations require L3 signoff and Head of Field Service review before the customer is billed (WARRANTY-TRAINING protocol (q) escalation).

**Staff injury.** Per HOUSEHOLD-STAFF-KIT.md §8.8, staff injuries around Hearth flow through the household employer first (workers' compensation is with the household). After employer notification, the concierge coordinates on the product-related aspect of the incident — crate handling review, PPE resupply, hazard investigation. The FSL case carries a `staff_injury_incident_linked` field that mirrors the Cooley portal record.

**Medical implant proximity.** Per HOUSEHOLD-STAFF-KIT.md §8.7, medical implant proximity events are S0 by definition. The concierge's first action is guidance to move to ≥24 inches from the sphere. The second is the case creation. The third is coordination with the customer's physician if requested, and offering the sphere-relocation option per §8.7 ongoing.

---

## 13. Vulnerability + confidentiality

Concierge access to customer household data is limited per THREAT-MODEL.md's seven-egress model and PRIVACY-COMPLIANCE.md §3 triple-consent gate.

**Data-access primitive.** Per ONBOARDING-PLAYBOOK.md §4 and THREAT-MODEL.md, the concierge cannot view customer content (photos, voice recordings, media library metadata) without triple-consent:
1. Customer physically taps the sphere face (biometric-authenticated).
2. Concierge initiates access from the FSL admin console with a stated reason.
3. Audit log entry written before access is granted, visible to customer in the mobile app.

The concierge sees only device metadata, health metrics, and support history by default. This is enforced at the FSL role hierarchy level — the concierge role does not have a permission set that includes content read.

**No case notes contain customer voice recordings or private content.** If a diagnostic requires listening to a wake-word capture or a false-positive event, the audio is reviewed in a sandboxed workflow that produces a diagnostic hash but does not persist the audio to the FSL case. The hash is the artifact; the audio is destroyed on session close.

**All case notes encrypted at rest.** FSL data is encrypted at rest with Salesforce Shield Platform Encryption. Access is logged per THREAT-MODEL.md audit-log requirements. Concierge access to any case beyond their assigned households requires a stated reason and generates an audit-log entry visible to the CX Lead's daily review.

**Staff privacy from owner.** Per HOUSEHOLD-STAFF-KIT.md §10, cases opened by staff members via the staff line are confidential from the owner unless the staff member explicitly asks otherwise. FSL enforces this at the sharing rule level — the owner's mobile app view of household activity does not include staff-line cases. This is a hard commitment and is repeated in HOUSEHOLD-STAFF-KIT.md §22 verbatim.

**Medical implant records.** Per HOUSEHOLD-STAFF-KIT.md §8.7 install-day sweep, implant status is stored in the household compliance file with restricted access. Not visible to the owner unless the individual consents. Not shared with third parties. If an implant status is referenced in an S0 medical-implant proximity case, the case's `implant_status_referenced` field is set, and the case is filed in a restricted-access sub-queue not visible to concierges outside the CX Lead and Head of Product Safety.

---

## 14. Post-case follow-up

Three touchpoints, cadence-locked.

**24-hour: automated survey.** Triggered on case closure. Sent by SMS with a Hearth-hosted link (not Typeform) per ONBOARDING-PLAYBOOK.md §8. Two questions: "On a scale of 1-5, how would you rate your experience with this Hearth service touchpoint? What could we have done better?" Response captured into the FSL `csat_score` and `csat_verbatim` fields.

**7-day: manual concierge check-in call.** L1 places a proactive call to the customer 7 days after closure. Not scripted — the goal is to confirm the resolution held, and to give the customer an opening to raise anything the survey didn't surface. Duration typically 5-10 minutes. `l1_7day_checkin_completed` field required. Non-completion after 10 days pages the CX Lead.

**30-day: NPS capture per ONBOARDING-PLAYBOOK.md cadence.** For any case that closed in the past 30 days, the customer's next scheduled NPS pulse (per ONBOARDING-PLAYBOOK.md §8 quarterly cadence for post-Day-90 customers, or the Day +29 / Day +31 pulse for customers still in onboarding) captures a specific rating on "the recent service interaction." Deltas between customers who had a case in the past 30 days and customers who didn't are the primary signal for service-quality drift; the delta is tracked on the CX dashboard weekly.

---

## 15. Escalation to Head of Comms

When a case involves a press-attracting incident — product malfunction in a celebrity home, safety issue with viral risk, viral customer complaint on social — the concierge and CX Lead notify the Head of Comms within 4 hours of case creation. The notification is via the `comms-escalation` Slack channel and a direct page.

**Do not communicate externally until Head of Comms approves.** The concierge does not respond to press inquiries. The concierge does not post on social. The concierge does not confirm to a third party that the customer is a Hearth household. If the customer themselves has posted publicly, the concierge continues to handle the case with the customer directly, but any external-facing statement — even a comment on the customer's own post — requires Head of Comms sign-off.

**Cross-reference POST-AIR-PR-PLAYBOOK crisis playbook.** For Shark Tank-adjacent cases, viral moments, and celebrity-household incidents, the POST-AIR-PR-PLAYBOOK's crisis protocol supersedes routine case flow. The FSL case remains open and continues to track the operational resolution, but the customer communication is owned by Head of Comms until the crisis is closed.

**Trigger criteria for §15 escalation:**
- Customer is a public figure with >100k followers or press access.
- Incident involves any injury or medical event.
- Incident has surfaced on social media outside of a private channel.
- Customer has explicitly threatened public complaint, legal action, or press outreach.
- Incident involves a competitor's product used adjacent to Hearth (rare, but the ecosystem stories become press).

Any single trigger fires the escalation; the CX Lead has discretion to fire preemptively on a signal not yet on the list.

---

## 16. Metrics + governance

**Weekly ops review.** Every Monday, 60 minutes. Attendees: CX Lead, all concierges via video, Head of Field Service, one rotating engineer. Agenda: open S0 and S1 cases, escalation-rate trend, prior week's audit findings, upcoming firmware push implications. Notes captured in Confluence.

**Monthly case-pattern analysis.** Head of Customer Experience runs a 90-minute session with CX Lead, Head of Field Service, and Product. The month's cases are grouped by `resolution_category` and `part_number_replaced`, and the emerging patterns are triaged as either "coincidence — monitor" or "signal — investigate." Signal cases feed the product-feedback loop and become the input to the next quarter's Engineering roadmap review per ONBOARDING-PLAYBOOK.md §8.

**Quarterly board packet §E.** Per BOARD-MATERIALS-TEMPLATES §E, the board sees:
- Case volume by severity.
- Response SLA and resolution SLA hit rates.
- CSAT post-close mean and median.
- Escalation rate trend.
- Warranty claim rate rolling 12-month.
- Cost per case by tier.
- The top three case-pattern findings from the quarter.
- The concierge team's turnover rate (target <10% per ONBOARDING-PLAYBOOK.md §4 and WARRANTY-TRAINING §10).
- Any S0 incident summary with post-mortem link.

**Annual governance review.** Head of Customer Experience produces a written annual review of the SOP against actual operating experience. Any changes to severity taxonomy, SLA policy, escalation triggers, or documentation standards are proposed here and go to CEO for sign-off before the next fiscal year. HOUSEHOLD-STAFF-KIT.md §8.7 medical implant protocol and §8.8 staff injury protocol are cleared with Cooley in the same annual pass; do not modify without a fresh legal review. WARRANTY-TRAINING.md §14 cross-doc reconciliation is refreshed alongside this SOP so the two documents remain consistent on scope allocation with Nuvation.

**Change management.** SOP changes ship via a documented pull request against this file. Reviewers: CX Lead, Head of Field Service, one CX Ops lead. Changes to §2 (severity taxonomy), §8 (FSL configuration), §13 (privacy), or §15 (comms escalation) require additional Head of Legal review. Changes to §7 (escalation triggers) require additional CTO sign-off because they affect engineering paging. Version log lives at the top of this file; version increments follow semver.

---

## Closing note

Hearth's concierge model is engineered around a single premise: the person who installed the sphere is the same person who answers the phone when it stops floating. That premise only holds if every one of the 40-120 annual touchpoints per household is a discrete, measured, closed transaction that respects the customer's time, the concierge's judgment, the technician's certification, and the household's privacy. This SOP is the discipline that produces that outcome at scale.

The 15-minute critical SLA is real because the pager is real. The 98% SLA hit rate is real because the FSL milestone objects enforce it. The triple-consent gate is real because the concierge cannot bypass it. The Nuvation countersign is real because the case is flagged amber until it arrives. The Head of Comms approval is real because the concierge does not have a Twitter account. The customer's exact words are captured verbatim because that is the sentence Engineering will read when the pattern emerges. Every field on the FSL case is load-bearing. Every escalation is timestamped. Every closure requires customer verification. The math on retention, the promise on privacy, and the LP-visible metrics on cost per case all rest on the daily discipline of this document, applied a hundred times a day, across a hundred and twenty concierges, across five thousand households, for a decade at a time.

---

*Document version 1.0. Owned by the Head of Customer Experience. Next review: post-first-100-installs debrief, co-timed with the WARRANTY-TRAINING v2.1 revision and the ONBOARDING-PLAYBOOK v1.2 revision. Word count approximately 6,400. Feeds pitch objections 12 (warranty burden — see §12), 18 (support scalability — see §11), and 21 (LTV — see §14 post-case follow-up cadence and its role in the extender-attach / v2-upgrade / referral pipeline documented in ONBOARDING-PLAYBOOK §6).*

File path (if written to disk by the parent): `/Users/lexer_kindle/Documents/GitHub/palpod-os/docs/investor/operations/CONCIERGE-CASE-MGMT-SOP.md`
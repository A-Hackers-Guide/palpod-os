# Hearth Cybersecurity Incident-Response Tabletop Exercise Playbook

**Owner:** Head of Security
**Co-owners:** Data Protection Officer, General Counsel (Cooley)
**Cadence:** Quarterly, ~90 minutes each, four scenario types on a rotating calendar
**Version:** 1.0 (Q1 2027 first-run edition)
**Cross-references:** `THREAT-MODEL.md` §7 audit / §8 incident response / §9 bug bounty; `PRIVACY-COMPLIANCE-MANUAL.md` §9 incident response / §9.5 detection stack / §9.6 state breach clock; `BOARD-GOVERNANCE.md` audit-committee oversight; `KPI-DASHBOARD-FRAMEWORK.md` incident metric tracking.

---

## 1. Exercise philosophy

Having an incident-response plan and being able to execute one are two different capabilities, and only the second one matters at 09:00 on the Monday the pager goes off. The gap between the two is closed by rehearsal — the same gap airlines close with simulator hours, hospitals close with code-blue drills, and the SEC has, since 2023, forced public companies to close on the reporting side of a cyber event. NIST Cybersecurity Framework subcategory **CSF ID.IM-02 / PR.IR-05 / RC.RP-06** ("Improve response and recovery through incident-response exercises") names this practice explicitly, and NIST SP 800-84 (Guide to Test, Training, and Exercise Programs for IT Plans and Capabilities) gives it a formal cadence: seminar-style discussion exercises, functional exercises, and full-scale exercises, each with a purpose and a place in the training arc.

The Hearth tabletop program is a **discussion-based functional exercise** in NIST 800-84's taxonomy. Ninety minutes, no live systems touched, no customer traffic disturbed, one novel scenario, and the whole response team in one room (physical or Zoom-hybrid) working the plan against a facilitator-injected timeline. It is deliberately smaller than a red-team engagement and deliberately larger than a document review.

The commercial argument is simple and mechanical. Hearth's incident response SLA (`THREAT-MODEL.md` §8) commits to a **72-hour signed hotfix for a Critical**; the composite regulatory clock (`PRIVACY-COMPLIANCE-MANUAL.md` §9.6) commits to a **72-hour GDPR ceiling and 24-hour "fact-of-incident" household notification**. Both clocks assume the response team can declare the incident within minutes, assemble within a quarter-hour, and produce a drafted regulator notification within half an hour of assembly. None of those numbers are recoverable from a cold start. The quarterly drill is what makes them defensible; the first real incident is what makes the drill pay for itself. One skipped 72-hour GDPR filing is a €20M administrative fine ceiling under Article 83. One quarter's exercise cost is $15–25k plus staff time. The math is not close.

The secondary argument is cultural. Concierges, field techs, and firmware engineers do not naturally think in "incident commander" terms. The drill teaches the vocabulary, teaches the escalation graph, and — more importantly — teaches every participant *where they sit in the escalation graph*. When the pager fires for real, nobody should be asking "am I the one who's supposed to draft the Article 33 notice." That question has a written answer, and the drill is where they memorize it.

The exercise is not theatre. Findings from the debrief are converted into version bumps of the incident-response SOP, new detection rules in Grafana Loki / Alertmanager (`PRIVACY-COMPLIANCE-MANUAL.md` §9.5), and updated notification templates. Every action item is tracked on a 30-day closeout, and the outstanding-item list is reported at the next quarterly board audit-committee meeting per `BOARD-GOVERNANCE.md`.

---

## 2. Exercise cadence and participants

Four exercises per year, each 90 minutes, rotating scenario type quarterly. The format is 30 minutes of pre-exercise briefing and role-check, 45 minutes of scenario execution against a facilitator-controlled timeline, and 15 minutes of structured debrief.

| Quarter | Scenario type | Attendee mix | Headcount | Purpose |
|---|---|---|---|---|
| Q1 | All-hands drill | Founder + Head of Security + DPO + Head of Engineering + Head of CX + Cooley partner + 3 concierges + 2 field techs + 2 firmware engineers + 1 external advisor | ~15 | Full incident-command exercise; first exposure for new hires |
| Q2 | Engineering-focused | Head of Security + Head of Engineering + DPO + firmware engineers + Cooley on-call | ~10 | Firmware / supply-chain / update-server-side drills |
| Q3 | CX-focused | Head of Security + Head of CX + DPO + concierges + field techs + Cooley on-call | ~12 | Household-facing incidents; notification-language drill |
| Q4 | Board-level | Head of Security + Head of Engineering + Head of CX + DPO + Cooley + 2 board members (audit-committee chair + one independent) | ~7 | Board oversight, disclosure judgment, and press response |

**External moderator.** Every exercise is run by an external facilitator from Coalfire, A-LIGN, or Cure53. Reports directly to the Head of Security and the DPO. Three-day engagement, $15–25k per quarter, budgeted against `KPI-DASHBOARD-FRAMEWORK.md` security-program line. Moderator scope: design the injects, run the timeline, produce the five-page written report, deliver recommendations for the SOP.

**Facilities.** Fremont conference room (physical), Zoom hybrid link for remote attendees. Cooley's on-call partner joins by Zoom. No laptops in the room except the Incident Commander's; phones face-down on the table. Whiteboard or Miro for the timeline. Printed one-pagers of the SOP, the seven-egress-class ACL, and the state-by-state clock (`PRIVACY-COMPLIANCE-MANUAL.md` §9.6) for every seat.

**Roles at every exercise (assigned at T-14 days, held constant through the drill).**

- **Incident Commander (IC):** Head of Security. Owns declaration, timeline, and closure.
- **Regulatory Liaison (RL):** DPO. Owns the Article 33 clock, the state-by-state clock, and drafted notifications.
- **Legal Lead (LL):** Cooley partner. Owns the disclosure judgment, safe-harbor language, and any law-enforcement interface.
- **Technical Lead (TL):** Head of Engineering. Owns containment, forensic capture, kill-switch deployment.
- **Customer Notification Lead (CNL):** Head of CX. Owns the household-facing message, the concierge script, and the press response.
- **Scribe:** Rotating; Q1 is the external advisor; Q2 is a firmware engineer; Q3 is a concierge; Q4 is the audit-committee chair's assistant. Owns the timestamped event log used for the debrief and the exercise report.
- **Observer(s):** Founder in Q1 and Q4; not in the response loop, watches for command-and-control gaps.

**Read-ahead materials, sent at T-14 days.** `THREAT-MODEL.md` §8 (severity SLA, communication plan), `PRIVACY-COMPLIANCE-MANUAL.md` §9 (72-hour ceiling, 24-hour household step), §9.5 (detection stack), §9.6 (state clock); the current incident-response SOP; last quarter's exercise report and outstanding action items.

**Warm-up quiz, sent at T-3 days.** Five questions on the plan. Sample: (1) Under §8 THREAT-MODEL, what defines a Critical? (2) Who owns the Article 33 draft under §9 PRIVACY? (3) Which sub-processor alert feed carries Ubuntu Security Advisories? (4) What is the operational ceiling for a non-EU incident? (5) At what California-resident count does §1798.29 AG notification trigger? Quiz answers are not scored; they surface knowledge gaps before the exercise.

---

## 3. Four scenario types (rotating quarterly)

Each scenario is designed to exercise a different slice of the plan. The rotation guarantees that within one calendar year every role, every notification track, and every containment pathway has been rehearsed at least once.

### Scenario A — Firmware supply-chain compromise

**Runs:** Q3 2027 (and every Q3 thereafter; refreshed injects each cycle).
**Which section of the plan it stresses:** `THREAT-MODEL.md` §3 (STRIDE — Tampering on the update path), §6 (signing keys + emergency 2-of-3 quorum), §8 (Critical / 72h hotfix); `PRIVACY-COMPLIANCE-MANUAL.md` §9 (72h regulator), §9.5 (Cloudflare + Canonical alert feeds).

**Setup inject (delivered at T=0):**

> **From:** dan@trailofbits.com
> **To:** security@hearth.co
> **Subject:** [URGENT] STM32H723 firmware toolchain — critical vulnerability
>
> "Team — we've identified a signature-validation weakness in the STM32H723 toolchain your Q2 firmware release was built with (CVE-2027-XXXX, disclosed under embargo). Under specific timing, an attacker with a chosen-plaintext update payload can bypass the signature check and land arbitrary firmware. We estimate ~10,000+ deployed Hearth extender boards in the affected build range. Embargo lifts in 72 hours. Standard coordinated-disclosure clock starts now."

**Scope:** 10,000+ deployed units. All Series Seed-1 investor households are in the affected range. ~2,400 EU customers within the affected fleet.
**Timeline:** notification received Monday 09:00 PT. GDPR 72-hour clock starts on discovery. Embargo lifts Thursday 09:00 PT.
**What the drill tests:**
- Does the team correctly declare Critical under §8 within five minutes?
- Does the 2-of-3 signing-key quorum assemble for the emergency hotfix?
- Does the update-server-side kill switch (release channel freeze) deploy correctly and reversibly?
- Does the RL correctly identify GDPR Article 33 applicability and draft?
- Does the CNL correctly identify Series Seed-1 investors as a separately-tracked notification cohort?
- Does the concierge team respond to household questions within SLA (Critical: 15 min for first response)?

**Success criteria:**
- 100% of Series Seed-1 investor households notified within 4 hours via out-of-band channel.
- 100% of EU customers notified within 72 hours via the two-step §9 flow (24h "fact-of-incident," 72h "confirmed data categories").
- Firmware patch signed, tested, and staged for auto-install within 5 business days.
- Press response drafted by CNL + LL within 24 hours.
- No leak of the pre-embargo CVE detail from any Hearth channel.

---

### Scenario B — State-actor targeted breach

**Runs:** Q4 2027 (board-level exercise).
**Which section of the plan it stresses:** `THREAT-MODEL.md` §1 non-goals (nation-state is explicitly not the design target — the drill tests what we do *anyway*), §8 communication plan; `PRIVACY-COMPLIANCE-MANUAL.md` §9 (external counsel engagement), governance disclosure judgment under `BOARD-GOVERNANCE.md`.

**Setup inject (delivered at T=0):**

> **Phone call, encrypted line.**
> "This is Special Agent [name], FBI San Francisco field office cyber division. We have credible intelligence that a nation-state actor is actively targeting three Hearth-installed households: a US-based diplomat, a technology-industry founder, and a defense-industry executive. We're notifying you under our victim-notification protocol. We are asking you not to disclose the specific targeting information outside your senior response team. Please have your general counsel call me at [number] within the hour."

**Scope:** Three named households. No confirmed compromise yet — the FBI is warning of active targeting, not a completed breach.
**Timeline:** notification received 14:00 PT on a Friday. Founder is at a board dinner and unreachable by normal Slack.
**What the drill tests:**
- Does the response team execute the **classified-incident protocol** without leaking to the wider org — i.e., the concierge on the phone with the diplomat's household tomorrow morning has no idea?
- Is the founder reachable in ≤4 hours via the pre-agreed out-of-band channel (Signal + backup phone number in Cooley's binder)?
- Is Cooley's on-call partner reachable within 15 minutes (the KPI target)?
- Does the RL correctly assess that this is **not yet** an Article 33 triggerable event (no confirmed breach), and correctly document that assessment so it isn't second-guessed at the post-mortem?
- Does the CNL execute the secure-channel notification to the three households within 6 hours — with language that gives the customers actionable guidance without leaking FBI operational detail?
- Does the LL negotiate the disclosure ask with the FBI (what can be shared with the households, what can be shared with the audit committee, what triggers a delayed-disclosure filing under SEC 8-K rules if we ever go public)?
- Does the Observer (Founder) resist the natural instinct to "just call the customers personally" and stay in the assigned lane?

**Success criteria:**
- FBI notification protocol executed cleanly, one phone call from LL to the named agent within one hour.
- Targeted customer notification via pre-established secure channel (Signal to a pre-registered device, not email) within 6 hours.
- No press leaks over the following 30 days (measured against the drill's simulated news cycle).
- Board audit-committee chair briefed within 24 hours under attorney-client privilege.
- Written record of the "not yet reportable under Article 33" judgment, with Cooley co-signature.

---

### Scenario C — Customer data breach via LAN

**Runs:** Q1 2028 (all-hands exercise).
**Which section of the plan it stresses:** `THREAT-MODEL.md` §3 (Spoofing / Elevation on the RustDesk relay + tap-consent path), §5 threat scenarios; `PRIVACY-COMPLIANCE-MANUAL.md` §9 full stack, §9.6 state clock (customer reports from a California resident).

**Setup inject (delivered at T=0):**

> **Concierge ticket, priority-1 escalation.**
> **Reporter:** [customer name], household in Palo Alto, California.
> **Ticket text:** "Something is very wrong. My Hearth sphere started talking to my kitchen this morning at 3 AM. My wife heard it. It said 'test test' twice then went quiet. Nobody in the house was up. This is not a false alarm. I need someone to call me back today. If this is a hack I will be going to the press."

**Scope:** Single confirmed household report. On the timeline, the forensics phase reveals a probable RustDesk relay-side vulnerability chained with a tap-consent-flow bypass — a Class 3 egress-class boundary breach in the THREAT-MODEL §3 STRIDE matrix. The affected household's voice profile and memory graph *may* have been exfiltrated during a 22-minute window.
**Timeline:** ticket received Tuesday 08:30 PT. Customer expects a callback by end of day.
**What the drill tests:**
- Does the intake concierge correctly categorize as **security incident** (per SOP §3.2) versus routing to a normal Tier-2 support ticket?
- Is the incident-response team paged and assembled within the 15-minute SLA?
- Does the TL correctly execute forensic capture (audit log preservation, on-box `auditd` + `osquery` snapshot per PRIVACY §9.5) *before* touching containment?
- Does the RL correctly identify California §1798.29 exposure (single-resident notification "in the most expedient time" — no 500-resident threshold yet, but the clock is running from the moment of confirmation)?
- Does the CNL manage the household through concierge-mediated comms, holding the household's confidence through a "we don't know yet" phase — the hardest single moment in the whole exercise?
- Does the LL evaluate the risk of a customer press disclosure and coach the CNL on the pre-emptive-narrative decision?
- Does the deletion pathway (household voice profiles + memory graph deleted from any exfiltration path within 12 hours) actually work as designed?

**Success criteria:**
- Correct triage category assigned within 15 min of intake.
- IR team assembled within 15 min of triage.
- Forensic snapshot captured within 60 min.
- Household voice profiles + memory graph cryptographic-key-destruction executed within 12 hours from any exfil egress class.
- Concierge maintains verbal contact with household every 4 hours through the first 24.
- Press statement drafted within 24 hours (whether or not it is issued).
- Notification to the household of confirmed data categories delivered within 72 hours per §9 two-step flow.

---

### Scenario D — Concierge insider threat

**Runs:** Q2 2028 (engineering + CX focused; HR is co-opted).
**Which section of the plan it stresses:** `THREAT-MODEL.md` §1 (insider trust boundary), §6 (audit-log integrity); `PRIVACY-COMPLIANCE-MANUAL.md` §8 employee training, §9 response team composition, §10 data-subject rights.

**Setup inject (delivered at T=0):**

> **Automated Alertmanager alert, routing to security on-call.**
> **Alert:** `hearth-concierge-access-anomaly`
> **Detail:** Concierge account `sarah.ellis@hearth.co` accessed 47 household audit logs in a 90-minute window on Sunday evening. All 47 households are outside her assigned "book" of 22. Twelve of the 47 accesses included memory-graph preview reads. Nine included biometric-consent-status queries. Access ended abruptly at 22:14 PT.

**Scope:** One senior concierge with 18 months of tenure and a top-quartile CX rating. 47 households whose audit logs she read without authorization. Nine of those 47 include biometric-consent-status data, which under the biometric-consent framework (`PRIVACY-COMPLIANCE-MANUAL.md` §3) is separately sensitive.
**Timeline:** alert received Monday 06:45 PT. Sarah is scheduled for a 09:00 CX standup.
**What the drill tests:**
- Does HR + Legal + Security coordination happen inside the first hour — before Sarah walks into the office and before she has an opportunity to alter or destroy evidence on her workstation?
- Which controls actually **prevented** data access versus merely **detected** the attempt — i.e., did the memory-graph preview read return real memory-graph content, or did the household-admin-key check block the actual content and leave only a metadata footprint?
- Is the departure protocol executed cleanly — badge revoked, VPN disconnected, cloud accounts frozen, laptop repossessed, personal effects logged — with a documented chain of custody so that a subsequent employment-lawsuit filing does not compromise the evidence?
- Does the CNL execute the household-notification protocol for the 47 households — with the two tiers of language, one for the 38 with metadata-only reads and one for the 9 with consent-status reads?
- Does the concierge team's **book rotation** (assigned as a control specifically for this failure mode) execute cleanly, so no household loses their point of contact?
- Does the RL correctly assess the biometric-consent-status reads under BIPA (Illinois) and CCPA (California) for the affected households, and identify which if any triggers a state-AG threshold?

**Success criteria:**
- Concierge terminated within 24 hours with documented chain of custody.
- All 47 access log entries preserved with cryptographic hashes stored in the escrow (`THREAT-MODEL.md` §6.7 mechanism, adapted).
- 47 affected households notified within 48 hours — 38 with the metadata-tier language, 9 with the consent-tier language.
- Book rotation completed within 48 hours; no household without a named concierge for more than 24 hours.
- Written HR + Legal + Security joint report to the audit committee within 30 days.

---

## 4. Q1 2027 first-exercise script (detailed)

The first exercise is the training exercise. Every subsequent quarter's script is compressed from this template; the first-run version below is the reference implementation. Scenario A (firmware supply-chain) is used as the Q1 2027 first-run inject.

### 4.1 Prep — T-14 days (Head of Security week)

| Day | Owner | Task |
|---|---|---|
| Mon T-14 | Head of Security | Send calendar invites; publish agenda + roles document to internal wiki |
| Tue T-14 | DPO | Confirm read-ahead materials packet; email to attendees |
| Wed T-14 | Cooley | Confirm on-call partner + backup partner; block calendars |
| Thu T-14 | Head of Security | Contract external moderator (Coalfire, A-LIGN, or Cure53); SoW signed |
| Fri T-14 | Head of Security | Fremont conference room booked (10 seats, whiteboard, no HDMI-connected TV — printed materials only); Zoom hybrid link generated and locked to attendee list |

### 4.2 Prep — T-3 days

- Read-ahead materials confirmed received by every attendee (email-open reply required).
- Warm-up quiz sent by DPO. Deadline T-1 day. Not graded; results used to calibrate the moderator's expected knowledge floor.
- Roles confirmed in writing. **Head of Security = IC. DPO = RL. Cooley = LL. Head of Engineering = TL. Head of CX = CNL. External advisor = Scribe.** Founder observes.
- Moderator briefed on the inject packet, timeline injects, and the scoring rubric.
- Cooley partner reviews the scenario cold and confirms no real conflicts of interest (a real Trail-of-Bits engagement is in flight — the drill uses a fictitious CVE number to avoid confusion).

### 4.3 T-0 — exercise execution (Monday, 09:00–10:35 PT)

The timeline below is the moderator's script. Every timestamp is enforced with a physical timer on the whiteboard. Overruns are logged and become debrief content — the exercise does not pause to make time for graceful play.

| Time | Event | Actor | Expected artifact |
|---|---|---|---|
| **09:00** | Moderator opens the exercise. Reads the rules. | Moderator | Ground rules acknowledged verbally by every attendee |
| **09:05** | Roles re-confirmed at the table. IC introduces herself as IC. Every other role does the same. | All | Role board visible on whiteboard |
| **09:10** | Moderator: "Here is what your on-call has just received. You have five minutes to read it silently, then the clock starts." | All | Silent read of the Trail of Bits email inject |
| **09:15** | **T=0.** Moderator: "The clock is running. Incident Commander, you have the floor." | IC | Verbal declaration |
| **09:15:30** | IC: "This is a Critical under `THREAT-MODEL.md` §8 — pre-auth firmware bypass on the update path. I am declaring an incident. Scribe, log 09:15 declaration. RL, start the Article 33 clock at 09:15 PT. TL, freeze the release channel — kill switch on. LL, get on the phone with Cooley on-call. CNL, prep the household template but do not send. Founder, you have observer status. Everyone else, phones down." | IC | Timestamped declaration in the scribe's log; verbal orders to each role |
| **09:16** | TL to moderator: "I am declaring the release-channel freeze deployed. Simulated — assume the freeze command is executed and confirmed at the update server." | TL | Moderator confirms the freeze is in place; new build cannot ship until the quorum re-signs |
| **09:17** | LL: "Cooley on-call reached, [name] is on the line. Briefed. Cooley is standing by for the disclosure judgment." | LL | Time-to-Cooley logged; KPI target ≤15 min, actual: 2 min from T=0 |
| **09:18** | RL: "Article 33 clock started at 09:15 PT. Deadline 09:15 PT Thursday. I am beginning the Article 33 draft now. State-clock check: any confirmed California residents in the affected build? TL?" | RL | Article 33 clock visible on whiteboard |
| **09:19** | TL: "Affected build range is EU-eligible units only in this exact hardware revision — but the shared toolchain means US units are potentially in scope pending forensic confirmation. Assume all 10,000 units are in scope until we can prove otherwise." | TL | Scope assumption recorded |
| **09:25** | **10-minute check.** Moderator injects: "The embargo has not lifted, but a security researcher has posted a cryptic tweet: 'STM32H723 folks, you're going to have a fun week.' The tweet has 12 retweets and one reply from a known EU journalist asking for a DM." | Moderator | New inject on the whiteboard |
| **09:26** | CNL: "That changes the press posture. LL, does this move up the press-response drafting timeline?" | CNL | Escalation logged |
| **09:27** | LL: "It doesn't force disclosure yet. But it moves the pre-emptive-narrative decision up 24 hours. CNL, draft the press statement now; hold for my sign-off." | LL | Press-drafting task assigned |
| **09:30** | RL: "First-draft Article 33 in front of me. Reading it aloud: 'On [date] at [time] PT, Hearth was informed by an external security researcher of a vulnerability in the STM32H723 firmware toolchain used to build the [build ID] extender firmware …' [Complete draft, 320 words, includes categories of personal data affected, approximate number of data subjects, likely consequences, measures taken.]" | RL | Article 33 first draft on the board; timestamp 09:30 = **15 minutes from T=0**; **KPI target ≤30 min met** |
| **09:35** | Moderator injects: "A pod owner in Berlin has just tweeted a screenshot of their pod's on-screen banner. The banner says: 'Firmware update paused. See hearth.co/status.' The tweet is at 400 retweets in 10 minutes." | Moderator | Public-signal escalation |
| **09:36** | TL: "That banner is the kill switch working as designed — it's the customer-visible signal that the release channel is frozen. The banner text is correct per SOP." | TL | Confirms kill-switch behavior |
| **09:38** | CNL: "I need to update the household template to acknowledge the banner and give a status URL. LL, sign-off on 'Hearth is aware of a firmware toolchain issue disclosed by a third-party researcher; a signed hotfix is in development; your pod is currently paused on the affected build; no household data is known to be at risk'?" | CNL | Template escalation |
| **09:39** | LL: "Sign off with one change — replace 'no household data is known to be at risk' with 'no evidence of unauthorized access to household data has been identified'. Legal-safe phrasing." | LL | Language edit logged |
| **09:40** | CNL: "Sending household template to concierge queue for staged delivery, throttled at 500 households per hour to avoid support overload. Series Seed-1 investor households flagged for direct-touch by [named concierge]." | CNL | **KPI: first customer notification staged at 09:40 = 25 minutes from T=0; target ≤60 min met** |
| **09:45** | Moderator injects: "The 2-of-3 signing-key quorum. IC, walk me through the quorum-assembly under §6." | Moderator | Signing-key drill |
| **09:46** | IC: "Founder is Key 1 shard, Head of Engineering is Key 2 shard, external HSM custodian is Key 3 shard. Emergency 2-of-3 quorum — Founder + Head of Engineering assemble physically at Fremont with hardware keys. HSM custodian is called for the third-shard-standby. Estimated wall-clock to signed hotfix, assuming no compile-time issues: 18–24 hours." | IC | Quorum plan verbalized |
| **09:50** | TL: "I am reporting firmware kill-switch deployment status. Kill switch is fully deployed — all 10,000 units on the affected build have received the pause command and displayed the banner. Zero units have attempted a new update pull since the freeze. Forensics team is beginning the post-freeze audit-log capture." | TL | Containment status logged |
| **09:55** | RL: "State-by-state clock check. California — no residential threshold to worry about until we cross 500 confirmed affected California residents. Current estimate: 1,800 California units in affected build. AG notification required. Adding to the notification queue." | RL | §1798.29(e) triggered; queued |
| **10:00** | CNL: "Investor-notification cohort delivered. All 42 Series Seed-1 investor households have received the direct-touch call; 39 confirmed acknowledgment; 3 in voicemail follow-up. Elapsed 45 minutes from T=0. Target was 4 hours. **KPI met.**" | CNL | Investor cohort closed |
| **10:05** | Moderator injects: "The German data protection authority (Baden-Württemberg) has emailed the DPO office asking for a preliminary status by end of day. RL, your call." | Moderator | Regulator direct-contact inject |
| **10:06** | RL: "Confirming receipt to Baden-Württemberg; committing to a preliminary status at 17:00 PT (02:00 CET) which will be an early Article 33 draft with the caveat that the 72-hour ceiling has not yet run. LL, sign off?" | RL + LL | LL signs off |
| **10:15** | Moderator: "Fifteen-minute warning. Head of Engineering, containment status?" | Moderator | Containment check |
| **10:16** | TL: "Containment status — freeze in place, no update attempts, forensics capture complete. Kill-switch working as designed. Signed hotfix ETA 18 hours; auto-install ETA 24 hours from signing. Expected re-open of release channel: Tuesday morning PT." | TL | Containment fully logged |
| **10:20** | IC: "Closing the exercise on the response side. RL — final Article 33 status? CNL — press status? LL — any open legal decisions?" | IC | Close-out |
| **10:21** | RL: "Article 33 draft complete, sitting for Cooley review, targeted filing at 12:00 PT tomorrow — 24 hours before the ceiling." | RL | Draft in queue |
| **10:22** | CNL: "Press statement drafted, held pending TL's confirmation of signed-hotfix ETA, expected release 18:00 PT if the researcher's tweet escalates further, otherwise hold for Wednesday morning coordinated release with the researcher." | CNL | Press held |
| **10:23** | LL: "No open legal decisions. Recommend we do not pursue the researcher for the tweet — coordinated disclosure norms hold." | LL | Legal position confirmed |
| **10:25** | IC: "Exercise concluded. Moderator, over to you." | IC | Handoff |

### 4.4 Debrief (10:25–10:35, ten minutes)

Moderator runs a structured hot-wash. Four questions, three-minute round-robins:

1. **What worked?** Fastest wins go on the board first. Q1 2027 first-run expected wins: time-to-declaration (30 seconds), time-to-Cooley (2 minutes), time-to-Article-33-draft (15 minutes), investor-cohort notification (45 minutes).
2. **What didn't work?** Expected first-run misses: kill-switch banner language ambiguity, press-statement coordination timing, state-by-state clock lookup speed. All logged.
3. **What surprised us?** New information about the plan that participants didn't previously know. Expected: how far the response depends on Cooley's on-call reachability; how much time the state-clock lookup takes without a scripted checklist.
4. **What do we change?** Action items with owners and deadlines. Every action item is written on the board with a name and a date. Nothing "we should think about"; every item has an owner or it doesn't exist.

Moderator closes with: "The exercise report will be in your inboxes within 48 hours. Every action item on the board is on a 30-day closeout. The next quarterly exercise is on [date]."

---

## 5. Post-exercise deliverables

The 48-hour packet, produced by the moderator with Head of Security review:

1. **Five-page exercise report.** Timeline, decisions, KPI table, findings, recommendations. Delivered to Head of Security, DPO, Cooley, Founder, and the audit-committee chair. Redacted summary published to the internal wiki. A further-redacted summary is included in the semi-annual transparency report per `PRIVACY-COMPLIANCE-MANUAL.md` §9.
2. **Updated incident-response SOP.** Version bump (semantic — patch for language changes, minor for new steps, major for structural). Every finding maps to either an SOP change or an explicit "no change — decision recorded" line.
3. **New detection rules.** If the drill exposed a detection gap, Grafana Loki rule + Alertmanager route are drafted, PR opened against the security-team repo, code review with two reviewers per `THREAT-MODEL.md` audit trail requirements.
4. **Notification templates.** Household template, investor template, press template, regulator preamble. All updated; version-controlled in the security-team repo.
5. **30-day action-item closeout.** Head of Security tracks every action item to closure. Items open at day 30 are escalated to the CEO. Items open at day 60 are escalated to the audit committee.
6. **Board audit-committee summary.** At the next quarterly board meeting per `BOARD-GOVERNANCE.md`, the Head of Security presents a one-slide summary: quarter's exercise scenario, KPI results, open findings, next quarter's scenario preview. Board audit-committee chair signs off in the meeting minutes.

---

## 6. Metrics per exercise

All timings measured from **T=0** (moderator's "clock is running").

| Metric | Target | Q1 2027 first-run TARGET (first-runs miss; that's why we drill) | KPI dashboard line |
|---|---|---|---|
| Time to declare incident | ≤ 5 min | ≤ 1 min | `security.exercise.time_to_declare_s` |
| Time to assemble team | ≤ 15 min | ≤ 5 min (already in the room) | `security.exercise.time_to_assemble_s` |
| Time to first regulator draft (Article 33) | ≤ 30 min | ≤ 20 min | `security.exercise.time_to_reg_draft_s` |
| Time to first customer notification (staged) | ≤ 60 min | ≤ 30 min | `security.exercise.time_to_notify_s` |
| Time to Cooley on-call reachable | ≤ 15 min | ≤ 5 min | `security.exercise.time_to_counsel_s` |
| Time to internal remediation (containment) | ≤ 4 hours | ≤ 2 hours in-drill; real-world 18–24h for signed hotfix | `security.exercise.time_to_containment_s` |
| Team confidence self-report (post-debrief, 1–10) | ≥ 7 by Q4 | 5–6 for Q1 2027 first-run | `security.exercise.team_confidence` |
| Action items closed within 30 days | 100% | 100% | `security.exercise.actions_closed_pct` |
| Cooley reachability rate (across the year) | 100% | 100% | `security.exercise.counsel_reachable_pct` |

All metrics feed the `KPI-DASHBOARD-FRAMEWORK.md` security-and-privacy panel. Trend lines quarter-over-quarter are the actual measure of program maturity — a stable-fast team beats a fast-but-jittery team.

---

## 7. Historical benchmark and framework anchoring

The Hearth program is written against three anchor references:

- **NIST SP 800-84** — Guide to Test, Training, and Exercise Programs for IT Plans and Capabilities. Hearth's quarterly drill is a "functional exercise" under the 800-84 taxonomy. Program elements — read-ahead materials, moderator role, timeline injects, structured hot-wash, five-page after-action report — all come from the 800-84 template.
- **NIST Cybersecurity Framework 2.0**, subcategories **ID.IM-02** ("Improvements are identified from evaluations") and **PR.IR-05 / RC.RP-06** ("Improve response and recovery through incident-response exercises"). The quarterly rhythm is the closure loop.
- **FedRAMP Continuous Monitoring Guide** — Hearth is not FedRAMP-authorized and does not intend to be, but the continuous-monitoring cadence (monthly attestations, quarterly assessments, annual full audit) informs how the tabletop exercise sits inside the broader control cadence: the quarterly exercise is one of the four "quarterly assessments" that feed the annual full audit produced by the SOC 2 program.
- **SOC 2 CC7.4 (Incident Response)** — primary mapping. Tabletop-exercise evidence maps most cleanly to CC7.4 (Response) and CC7.5 (Recovery). CC7.2 (Anomaly Detection & Monitoring) and CC7.3 (Anomaly Evaluation) are covered by the SIEM detection stack described in `PRIVACY-COMPLIANCE-MANUAL.md` §9.5; tabletop evidence supports those two controls but does not primarily satisfy them. Each quarter's exercise report is entered into the SOC 2 evidence binder for CC7.4 primary and CC7.2/CC7.3/CC7.5 supporting. One missed drill in a 12-month SOC 2 evidence period is a control-deficiency finding on the CC7.4 report.

The composite effect: the tabletop is not a Hearth-invented ritual. It is the operating-effectiveness evidence for two industry-standard control frameworks, and the anchor practice under one federal cybersecurity framework. Skipping it is a compliance event, not a scheduling event.

---

## 8. External moderator scope

Quarterly engagement, $15–25k per exercise, three-day scope.

**Vendor candidates (rotating quarterly to avoid moderator staleness):**

| Vendor | Strength | Typical rate |
|---|---|---|
| **Coalfire** | Broad IR-exercise practice; FedRAMP-flavored rigor; good at compliance-heavy scenarios | $18–22k / exercise |
| **A-LIGN** | SOC 2 and ISO 27001 evidence integration; auditor-familiar; good at "will this pass the auditor?" scenarios | $15–20k / exercise |
| **Cure53** | Web + mobile + technical depth; excellent at engineering-focused Q2 scenarios; may sub-contract facilitation | $20–25k / exercise |

**Statement of work outline (three-day engagement):**

- **Day 1 — Design.** Moderator reviews `THREAT-MODEL.md`, `PRIVACY-COMPLIANCE-MANUAL.md`, and the previous exercise report. Drafts injects for the current quarter's scenario. Reviews with Head of Security + DPO.
- **Day 2 — Execution.** Moderator runs the 90-minute exercise on-site in Fremont with Zoom hybrid. Delivers verbal hot-wash notes at the end.
- **Day 3 — Report.** Moderator writes the five-page after-action report, drafts SOP recommendations, delivers via encrypted file share to Head of Security and DPO. Read-back call with Head of Security to confirm nothing is misstated.

**Reporting line.** Moderator reports directly to Head of Security and DPO, in writing, with a copy to Cooley on-call. Moderator does not report to the Founder or the audit committee; the Head of Security relays the summary. This preserves the moderator's independence — the moderator's honest read of "the team missed on this" cannot be softened before it reaches the security office.

**Confidentiality.** NDA in place before the moderator sees any inject material. Reports are marked "Hearth Confidential — Security-Program-Internal" and retained on the security team's file share for seven years to align with SOC 2 evidence retention.

---

## 9. Cross-doc reconciliation

- **`THREAT-MODEL.md` §7 audit plan.** The tabletop program's quarterly cadence sits *inside* the annual full-stack audit cadence. The tabletop is not a substitute for the Trail-of-Bits engagement; the two programs are complementary — audits find defects, tabletops rehearse response.
- **`THREAT-MODEL.md` §8 incident-response playbook.** The tabletop exercise **is** the operating-effectiveness rehearsal for the §8 SLA (72-hour Critical hotfix). Every drill measures the team against §8's numbers.
- **`THREAT-MODEL.md` §9 bug bounty.** Bug-bounty submissions triaged as valid Critical or High are handed to the IR team within 2 hours (`PRIVACY-COMPLIANCE-MANUAL.md` §9.5). Q2's engineering-focused exercise cycles a bug-bounty-originated inject at least once per year.
- **`PRIVACY-COMPLIANCE-MANUAL.md` §9 incident response.** The tabletop drives the §9 numbers — 24-hour "fact of incident" household notification, 72-hour "confirmed data categories" household follow-up, Article 33 regulator ceiling. Metrics are cross-posted to the transparency report.
- **`PRIVACY-COMPLIANCE-MANUAL.md` §9.5 detection stack.** Every exercise's action items may seed new Grafana Loki rules and Alertmanager routes. The tabletop is the closed-loop verifier for the §9.5 detection layer.
- **`PRIVACY-COMPLIANCE-MANUAL.md` §9.6 state breach clock.** Every drill exercises at least one state-clock injection. Rotating over four quarters, every year covers California, New York, Texas, Ohio, Illinois, Colorado, Florida at minimum.
- **`BOARD-GOVERNANCE.md`.** Audit committee reviews the quarterly exercise report and open-action-item list at the quarterly board meeting. Board audit-committee chair signs off in the minutes.
- **`KPI-DASHBOARD-FRAMEWORK.md`.** The metrics in §6 are cross-posted to the security-and-privacy dashboard panel. Trend lines quarter-over-quarter are the actual measure of program maturity.

---

## 10. Calendar hooks

The Head of Security's calendar carries the following recurring holds. All are populated at the start of the fiscal year and adjusted as needed.

- **Q1 exercise — first business Tuesday of February, 09:00–10:35 PT.** All-hands. External moderator: Coalfire (rotating).
- **Q2 exercise — first business Tuesday of May, 09:00–10:35 PT.** Engineering-focused. External moderator: Cure53 (rotating).
- **Q3 exercise — first business Tuesday of August, 09:00–10:35 PT.** CX-focused. External moderator: A-LIGN (rotating).
- **Q4 exercise — first business Tuesday of November, 09:00–10:35 PT.** Board-level. External moderator: Coalfire (rotating).

**T-14 day and T-3 day prep windows** are auto-scheduled on the security-office calendar. External-moderator SoW is signed at T-30. Fremont conference room is held at T-45 to guarantee availability.

**Audit-committee summary slots** are held at the quarterly board meeting immediately following each exercise — first business Thursday of March, June, September, December.

---

*End of playbook. Next version: 1.1, revised after the Q1 2027 first-run debrief. Owner: Head of Security. Approver: DPO + Cooley. Distribution: security team, DPO office, Cooley on-call binder, data-room security folder, board audit-committee package.*

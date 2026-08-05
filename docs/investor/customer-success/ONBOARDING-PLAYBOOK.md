# Hearth Customer Experience Playbook
## The 90-Day Onboarding Journey & Concierge Service Operations
*Owner: Head of Customer Experience. Version 1.1. Data room: /customer-success/*

---

## Preamble — The service line is the product

Hearth is a $95,000 device that sits in a customer's home for 5-10 years. A Ferrari client sees their concierge twice a year at a service visit; a Hermès client sees theirs once a season at a personal shopping appointment. A Hearth customer will interact with their concierge somewhere between **40 and 120 times a year** — every firmware push, every memory upload, every "hey why did it do that." That means the concierge team, not the sphere hardware, is the durable moat. If we lose the concierge relationship, we lose the customer, and at $95k CAC that is fatal.

The 95% one-year and 90% three-year retention targets are not aspirational marketing — they are the LTV model in the financial doc. Every choice below is engineered backward from those two numbers, and every dollar of concierge overhead is defended in §6 and §9 against the specific extender-attach, v2-upgrade, and referral economics it protects. Concierge is intentionally a loss-leader on subscription; it is a profit-generator on lifetime.

---

# 1. The 90-Day Journey — Day by Day

## Phase 1 — Purchase & Pre-Install (Day -21 → Day 0)

### Day -21 — Deposit accepted, order confirmed
- **What happens:** Customer wires 50% deposit ($47,500) via ACH or wire. Auto-confirmation from `orders@hearth.co`. Within 90 minutes, human confirmation from the assigned concierge — a phone call, not an email. Voicemail acceptable but must include the concierge's direct cell number.
- **Who:** Concierge (primary) makes the call. Back-office ops team confirms wire receipt.
- **Feels:** Reassurance. "There is a real person who owns my order."
- **Success criterion:** 100% of deposits acknowledged by a named human within 4 hours of settlement, cell number given.

**Concierge script (Day -21 call):**
> "Mrs. Chen — this is Isabella Rodríguez, your Hearth concierge. Welcome. Your deposit landed at 11:14 this morning. Your sphere is being built in Fremont, and your target install window is the week of March 4th — I'll confirm the exact date within 72 hours once your site survey is scheduled. My direct number is 415-555-0164, saved in your caller ID as 'Isabella Hearth.' Anything you'd like me to know about your household before we start?"

### Day -20 — Welcome kit ships
- **What happens:** A hand-packed box arrives via FedEx overnight. Contents: a letter from the founder (hand-signed, not photocopied); a linen-bound *Hearth Household Guide* (48 pages, not a manual — think Herman Miller monograph); a swatch card of the four available sphere finishes (matte graphite, warm bronze, brushed titanium, ivory); a lambswool cleaning cloth; a small tin of the espresso the founder drinks in Fremont with a card that says "on install day, we'll bring you a cup." No product boxes, no packing tape branding — the box is unmarked white so household staff don't announce the delivery.
- **Who:** Concierge orders through fulfillment. Founder signs the letter (real ink, not autopen).
- **Feels:** The moment the customer realizes this is not a Sonos.
- **Success criterion:** 98% delivery within 48 hours of deposit; 100% inclusion of hand-signed letter.

### Day -18 — Site survey scheduled
- **What happens:** Concierge calls to schedule the site survey — either an in-person visit (for primary homes within 90 minutes of an installer hub) or a video walkthrough (for remote homes, seasonal residences, or international shipments). Concierge asks explicitly: "Would you like to do this yourself, or would you prefer we coordinate with your household manager?"
- **Who:** Concierge coordinates. Installer conducts.
- **Feels:** Respected, not managed.
- **Success criterion:** Survey scheduled within 5 business days of deposit.

### Day -14 — Site survey conducted
- **What happens:** 60-90 minute visit. Installer measures placement location (must be on main living floor, minimum 30cm from any wall, minimum 2.1m ceiling clearance for the Halbach halo animation, ideally within 4m of an ethernet drop). Photographs the space. Meets the household — cook, house manager, security, any children — so install day has no strangers. Confirms the sphere finish choice against the room's actual light. Runs a wifi/ethernet audit and identifies which household router the sphere will bind to.
- **Who:** Regional installer lead + concierge on video conference for the meet-and-greet portion.
- **Feels:** Bespoke. "They're not just dropping a box."
- **Success criterion:** Site survey report filed in admin console within 24 hours. Concierge signs off within 48 hours.

### Day -10 — Install date locked
- **What happens:** Concierge sends a calendar invite for a specific 4-hour window (typical: 9 AM-1 PM or 1 PM-5 PM local). Concierge confirms which household adults will be present — install requires an adult signature for the sphere ($95k asset transfer) and for the initial voice-profile capture (consent for on-device biometric processing). Reminder: pets should be crated during the 60-minute placement phase for their safety around the Halbach magnets.
- **Who:** Concierge sends invite; customer confirms.
- **Feels:** Anticipation.
- **Success criterion:** Confirmed calendar hold from the primary adult, 10+ days out.

### Day -7 — Pre-install brief
- **What happens:** 15-minute video call between concierge and household. Concierge walks through the day: what the truck looks like (unmarked white cargo van), what the installers wear (charcoal suits, not uniforms — luxury service posture), what the family should do (nothing; do not clear the room, we bring boot covers and drop cloths). Concierge confirms the family "memory upload" they'd like ready for install day — typically a photo album, a favorite recording, a home video — this becomes the first content the sphere ingests, and it is the emotional payload of the install-day close.
- **Who:** Concierge.
- **Feels:** Prepared, curious.
- **Success criterion:** 100% of families identify their memory-upload content pre-install.

### Day -3 — Manufacturing confirmation + shipping trigger
- **What happens:** Concierge sends a photo of the actual finished sphere from the Fremont floor — with the customer's initials on the QC tag. This is the "your car is on the boat" moment. Sphere ships via dedicated air freight for out-of-region, dedicated truck for in-region.
- **Who:** Fremont QC lead + concierge.
- **Feels:** Ownership. "That's mine."
- **Success criterion:** Photo sent within 24 hours of QC pass.

### Day -1 — Reminder + logistics
- **What happens:** Concierge texts the primary adult by 6 PM: "Everything on track for tomorrow, 9 AM. Marco (installer) and Priya (tuner) will arrive together in an unmarked white van. Marco's cell if there's any issue: 415-555-0198. See you tomorrow."
- **Who:** Concierge.
- **Feels:** Assured.
- **Success criterion:** 100% receive text; 0% surprise arrivals.

---

## Phase 2 — Install Day (Day 0)

Detailed minute-by-minute breakdown in §3. Summary here — **every beat below must match §3 exactly**:

- **08:30** — Tuner (Priya) arrives 30 minutes early if new residence, to run any pre-setup that doesn't require the family (network check, physical space prep). At an occupied home she waits with Marco.
- **09:00** — Both arrive at front door together. Family greeting.
- **09:05** — Boot covers, drop cloths.
- **09:10** — Sphere unloaded.
- **09:20** — Placement + power.
- **09:45** — First-boot self-tests.
- **10:00** — Network + firewall integration.
- **10:20** — Halbach calibration + household greeting.
- **10:30** — Voice profile capture. Each family member records ~2 minutes of natural speech for the on-device Piper voice model.
- **11:15** — Media library import from family NAS or photo folder.
- **11:45** — The first family memory upload — the engineered emotional beat.
- **12:00** — Concierge introduction (Isabella joins on the sphere face via video, meets the family, gives them her cell).
- **12:05** — Walkthrough: panic button, remote-support consent (triple-tap protocol), companion mobile app pairing.
- **12:30** — Priya packs up. Marco walk-around.
- **12:45** — Final Q&A + espresso ritual. The tin from the Day -20 welcome kit is opened. Marco pulls two shots on the family's machine. Family and installers sit together for 10 minutes. Not scripted. No agenda. This is the beat where the household stops feeling like a customer and starts feeling like a member.
- **13:00** — Departure. Thank-you card is dropped in a USPS mailbox on the drive home — hand-addressed, hand-signed by both installers.

**Feels:** Awe → competence → intimacy → belonging.
**Success criterion:** 4.8/5 install-day satisfaction measured 24 hours later.

---

## Phase 3 — First 30 Days

### Day +1 — First morning call
- **What happens:** Concierge calls at 9 AM local to confirm the sphere came online overnight (all firmware self-tests pass) and to ask a single question: "How does it feel this morning?" Not "any issues?" — the framing is emotional, not diagnostic.
- **Success criterion:** Call placed to 100% of households, 24 ± 4 hours post-install.

### Day +2 — Email: your first memory
- **What happens:** Automated email (composed by concierge, sent from the concierge's inbox, appears personal): a still frame from the Day 0 memory upload with the caption "Sphere replayed this at 7:42 PM last night — thought you'd want to know." The message is generated but the concierge reviews and personalizes each one.
- **Success criterion:** 100% send rate; 60%+ reply rate.

### Day +3 — The "unexpected" check-in
- **What happens:** Concierge calls again, unprompted: "We noticed your library sync completed — 4,220 photos, 316 videos, 108 songs. Everything look right? Anything missing you thought would be in there?" This is engineered proactive contact — the sphere sends a status ping to the admin console when sync completes, and the concierge is prompted to call. Customer experiences it as attentive, not automated.
- **Success criterion:** Call within 12 hours of library-sync completion; 90%+ answer rate.

### Days +4 through +7 — Passive availability
- **What happens:** Concierge does not call daily. But is on-call. Customer texts get responses within 30 minutes during 8 AM-10 PM local; overnight critical events routed to the Concierge Ops overnight tier per §4.
- **Success criterion:** Median response 12 minutes; 98% within 1 hour.

### Day +7 — Week-1 NPS + call
- **What happens:** Short survey (3 questions, sent by SMS with a Hearth-hosted link, not a Typeform): "On a 0-10 scale, how likely are you to recommend Hearth? What's the one thing you've loved most? What's the one thing that's still confusing?" Concierge reviews responses within 4 hours, calls anyone scoring below 8.
- **Success criterion:** 85%+ survey response rate; median score 9+; concierge outbound within 4 hours on any 7-or-lower.

### Days +8 through +14 — Weekly check-in
- **What happens:** Every Friday afternoon (customer-chosen time), 10-15 minute concierge call. First one: "walk me through what a typical evening with Hearth has looked like this week." Second one: "if we could change one thing before month-end, what would it be?"
- **Success criterion:** 90%+ acceptance of the weekly call for the first 4 weeks.

### Day +14 — First firmware push
- **What happens:** First scheduled firmware update. Concierge tells the customer 24 hours in advance ("we're pushing 1.03.11 tonight at 3 AM your time — it adds better wake-word tuning for the kids' voices"). Customer never sees it happen. If anything fails, sphere rolls back automatically and concierge calls at 8 AM.
- **Success criterion:** 99.5% clean pushes; 100% pre-notification; 0% surprise reboots during customer waking hours.

### Day +21 — Family use rhythm check
- **What happens:** Concierge reviews the (anonymized, aggregated) usage patterns in the admin console — how often the sphere was invoked, which family voice profiles are being used, whether the extender question has come up in any voice interaction. Uses this to guide the Day 30 call and to schedule the Day 29 baseline NPS.
- **Success criterion:** Usage baseline established for every household by Day 21.

### Day +29 — Baseline NPS (pre-montage)
- **What happens:** Two-question SMS: "On a 0-10 scale, how likely are you to recommend Hearth today? What's Hearth done best this month?" This score is the baseline for the Day-30 montage delta metric — one of the linchpin measures in §7 and §9.
- **Success criterion:** 90%+ response rate; NPS captured in cohort dashboard within 24 hours.

### Day +30 — The engineered "wow moment" + first upgrade nudge
- **What happens:** On a family member's most-active day of the week at their most-active time, the sphere plays a 90-second montage: 15 photos and 2 short video clips from the family's own library, hand-curated by the sphere's on-device model based on face recognition, timestamp clustering, and emotional-tone tagging. No AI-language framing — customer hears music (chosen from their library) and sees the montage float across the sphere face. Concierge calls the next morning: "How was last night?" This is the retention linchpin — see §7 for the full set of measurable outcomes engineered around this beat.
- **Success criterion:** 100% of households experience the engineered montage in the Day 28-32 window; concierge follow-up within 24 hours; Day-31 NPS captured within 24 hours of the follow-up call.

**Extender nudge — Day 30 call:**
> "One thing I wanted to ask — we noticed you've been using the sphere mostly from the family room. A lot of our clients add an extender in the primary bedroom around this point. If you'd like, I can arrange one shipped this week, and I'd install it remotely — you'd just plug it in. $8,999, added to your account, no separate wire. Want to think on it, or should I put it in motion?"

### Day +31 — Post-montage NPS + concierge follow-up quality capture
- **What happens:** Second NPS pulse, same two questions as Day +29. Concierge follow-up call is scored on a 5-point rubric by the CX Ops lead (spot-audited weekly). The delta between Day +29 and Day +31 is the primary retention-signal metric for the Day-30 beat.
- **Success criterion:** ΔNPS ≥ +8; concierge call quality ≥ 4.5/5; see §9 for full dashboard.

---

## Phase 4 — Days 31 to 90

### Day +45 — Extender install (if elected on Day 30)
- **What happens:** Extender arrives 3-4 business days after order. Concierge schedules a 30-minute remote install window via RustDesk (customer's consent already granted at initial install). Customer plugs it in; concierge does the pairing, the customer taps the sphere face to authorize. Follow-up call 24 hours later.
- **Success criterion:** 95% same-day paired without incident; 70% attach rate by Day 90.

### Day +60 — Monthly check-in
- **What happens:** 20-minute concierge call. Structured but conversational. Reviews any support tickets, any firmware notes, any family-added content. Ends with: "Anything Hearth *should* be doing that it isn't?"
- **Success criterion:** 85% call acceptance rate.

### Day +75 — Founder letter
- **What happens:** Physical letter from the founder (real ink, hand-addressed). Contents: "You are one of the first 100 [or however far into the customer count] Hearth households. I wanted to write personally. Here's what I'm working on for you this year. Here's my direct email. Thank you." No sales pitch.
- **Success criterion:** 100% of Day 75 buckets receive letter; 20% reply rate.

### Day +85 — Quarterly product-tip email
- **What happens:** Concierge sends 3 specific tips tailored to that household's usage. Example: "You've asked Hearth for weather 47 times this quarter — did you know you can say 'Hearth, what's the marine forecast for Catalina this weekend'? Two, you haven't set up guest voice profiles — worth 5 minutes when your family visits." Personal, not marketing.
- **Success criterion:** 60% open rate (email); 15% follow-through on at least one tip.

### Day +90 — Day 90 NPS + first upgrade path mention + escalation-path demo
- **What happens:** 5-question NPS. Includes an unprompted-recall question: "Was there a specific Hearth moment in the last 90 days that stood out for you?" 60%+ of families are expected to reference the Day 30 montage without prompting — this is a measured outcome in §9. Concierge call reviews the score and asks the "one thing you'd change" question. This is also when the concierge walks through the escalation path formally: "If something ever goes wrong that I can't fix in real time — here's how it works. I stay on the call. I loop in Priya's team on engineering. If it needs the CTO, I call him. You don't file a ticket. You call me."
- **Success criterion:** 90% NPS response rate; median 9+; ≥60% unprompted Day-30 recall; 100% of customers hear the escalation demo.

---

# 2. Persona-Specific Onboarding

Reference: VoC-MOCK-RESEARCH.md, 23 personas. Below are the 5 canonical archetypes.

## Q1 — Cardiologist, Newport Beach
**Profile:** 52, MD/PhD, intermediate technical comfort, wants a privacy briefing, family of four, likely to read the *Household Guide* cover to cover.

- **Pre-install:** Add a 30-minute video call at Day -12 with the concierge + a Hearth privacy engineer. Walk through the on-device model architecture, the triple-consent primitive, and what leaves the house (nothing, by default). Send the THREAT-MODEL.md excerpt in advance so he can pre-read.
- **Install day:** Extra 45 minutes at the walkthrough — installer opens the sphere access panel briefly to physically show the TPM chip and the ethernet-only WAN posture. Q1 is the persona who wants to see hardware.
- **Week-1 concierge tone:** Precise. Technical. No emotional gushing. "Latency on your last query was 340ms — that's within the 500ms target we hold. Anything you'd like tightened?"
- **Day-30 framing:** Send him the release notes for 1.03.11 before the montage moment. He will appreciate that the montage came from a model with a documented spec sheet.

## Q3 — Retired PE Partner, Palm Beach
**Profile:** 71, hates touchscreens, wants voice-first, wife (Marco's spouse) is the primary user. "Marco tells me it's good" is the signoff heuristic.

- **Pre-install:** Concierge does a phone call with the wife, not just Marco. She is the operational user. Add her to the primary contact list even though Marco signs the wire.
- **Install day:** Skip most of the mobile-app pairing — the family will never use the app. Give the wife the concierge's cell number written on a matte cream card, placed on the sphere charger.
- **Week-1 concierge tone:** Slower, warmer, more time. Marco expects the concierge to remember his golf handicap from the Day -7 call.
- **Day-30 framing:** No "upgrade path" language. The Day-30 call is: "How's it fitting into the house?" If the extender comes up, it comes from the wife.

## Q11 — Author + Climate Philanthropist Couple, Nantucket
**Profile:** Seasonal home, wants offline first, values Hearth's air-gapped LAN posture as a values-alignment statement.

- **Pre-install:** Two survey visits — one for the Nantucket residence, one for the Manhattan pied-à-terre if they want a second unit later. Concierge explicitly addresses seasonal-shutdown protocol: when the house closes for winter, sphere goes into a "hibernation" mode (LAN off, battery trickle, resumes on a physical wake).
- **Install day:** Add an environmental briefing — humidity, salt air, sphere finish choice (recommend brushed titanium for coastal). Priya packs a coastal-climate service kit.
- **Week-1 concierge tone:** Intellectual, curious. They will ask about the training corpus for Piper. Have that briefing ready.
- **Day-30 framing:** The wow-moment montage should draw disproportionately from their climate-work archive, not from family photos alone. They'll ask if Hearth can generate a summary of their reading list — yes, offline, on-device.

## Q17 — Widowed Philanthropist, Boston
**Profile:** 78, extreme low-touch, three adult children who live elsewhere, needs a "family assistant" framing, HATES the word "AI."

- **Pre-install:** Concierge does a longer pre-brief (60 minutes, in person if possible). Add one adult child to the concierge contact list explicitly — with the mother's consent — so a call can escalate to family without her having to make it.
- **Install day:** No mention of "voice model," "wake word," or "AI." Framing: "Hearth listens the same way a good housekeeper does — only when you call for it." The setup script never uses the word artificial.
- **Week-1 concierge tone:** Formal, warm, calls her Mrs. [Surname]. Reads out newspaper headlines gently if asked. Concierge writes down her preferred call time — 10:30 AM after breakfast — and holds it as a standing appointment.
- **Day-30 framing:** The montage draws from her late husband's photo archive — this has to be handled carefully, screened by the concierge in advance for anything the household might not want surfaced (obituary photos, etc.). This is a moment of truth; if we get this wrong we lose her forever.

## Q23 — Middle East Family-Office CIO
**Profile:** Procurement-driven, wants documentation, wants enterprise SLA framing, wants a signed statement of work, RFP-style.

- **Pre-install:** Concierge is joined by the Hearth CX Ops lead for a formal SOW walkthrough. Documentation package includes: warranty terms, data-handling attestation, incident-response commitment, uptime targets, PII posture. All countersigned.
- **Install day:** Longer window (6 hours, not 4). CIO wants to observe placement, initialization, and firewall integration in detail. Installer treats it as a corporate deployment: hand-over log, acceptance signature.
- **Week-1 concierge tone:** SLA-referenced, structured. Response times cited explicitly.
- **Day-30 framing:** Written report, not a call. Delivered as PDF. Includes usage stats, uptime, incidents (should be zero), and next-quarter commitments.

---

# 3. Install Day — The 4-Hour Script

Two-person crew: **Marco** (installer, physical setup and hardware), **Priya** (tuner, software and voice model).

- **08:00** — Marco + Priya meet at regional depot. Load sphere, extender-ready packaging (in case customer wants one on the spot), tuning tools, environmental sensors, boot covers, drop cloths, thank-you card and envelope, install-day gift (a Hearth-branded merino blanket).
- **08:30** — Arrive within 5 minutes of home. Park unmarked white van in driveway or on street, whichever the family requested at Day -7. Do not ring the bell before 09:00.
- **09:00** — Doorbell. Marco greets first, Priya second. Both extend hand, use family names, decline offered coffee ("we brought espresso for you actually — from Fremont"). Place gift, hand-signed card from concierge on the kitchen counter.
- **09:05** — Boot covers on. Drop cloths laid on the path from door to placement location.
- **09:10** — Marco unloads sphere via hand truck. Priya unloads tuning kit and networking gear.
- **09:20** — Physical placement. Marco levels the sphere pedestal to within 0.1° using a laser level. Halbach halo depends on this. Power connected via the household's dedicated 15A circuit (identified during site survey).
- **09:45** — Sphere powers on. Face illuminates with the household surname. First-boot self-tests run for 8 minutes. Marco and Priya narrate: "You'll hear a 3-second harmonic — that's the halo self-tuning."
- **10:00** — Network integration. Priya configures the sphere to the ethernet drop identified in the survey. Firewall rule added (sphere binds to LAN only, no WAN routes except firmware update endpoint at 3 AM local). If the household has an IT person, Priya calls them directly on speakerphone and walks them through the rule.
- **10:20** — Halbach halo calibration completes. Face displays the family greeting: "Good morning, [surname] household." Every family member present is greeted by first name if they were captured at the site survey.
- **10:30** — Voice profile capture. Priya sits with each family member individually, one at a time, in the living room. Each person reads a scripted paragraph (approximately 300 words, chosen from a set of literary passages — never marketing copy) into the sphere's array. Piper voice model trains on-device in ~90 seconds per profile. Children's profiles handled with a parent present.
- **11:15** — Media library import. Priya pairs the sphere to the family's Plex, Jellyfin, or Audiobookshelf server (or, if none, sets one up on the sphere's internal storage using the photo folder the concierge identified at Day -7). Scan begins — status shown on sphere face as a growing constellation.
- **11:45** — First family memory upload. This is the engineered emotional beat. The family has pre-identified a piece of content — a wedding video, a first-child photo album, a recording of a grandparent. Marco or Priya asks the sphere to play it. It plays. The family watches. **Nobody speaks over it.** This is a moment we do not narrate.
- **12:00** — Concierge introduction. Isabella (concierge) appears on the sphere face via video from her desk. Introduces herself. Confirms her cell number. Answers any questions. Tells the family: "I'm the person you call. Not a support line. Me. Or my backup, David Chen, if I'm asleep. Overnight, our Concierge Ops team covers you at the same 15-minute critical response — same admin console, same escalation to me if it matters." 5 minutes total.
- **12:05** — Walkthrough. Marco demonstrates the physical panic button on the back of the sphere pedestal (long-press, calls concierge directly, opens two-way audio). Priya demonstrates the triple-consent flow for remote support: customer taps the sphere face, concierge initiates from her end, both logged in the audit trail. Companion mobile app installed on the primary adult's phone, paired.
- **12:30** — Priya packs up. Marco does a final walk-around: pedestal level, cable management clean, no packing debris left.
- **12:45** — Final Q&A + espresso ritual. Marco opens the Fremont espresso tin from the Day -20 welcome kit and pulls two shots on the family's espresso machine (or brews via French press if none). Family and installers sit together — kitchen island or dining table, not the sphere room. No script. Marco takes any remaining questions. Priya takes notes on anything the family would like added to the concierge's Day +1 briefing. This is the beat where the household transitions from customer to member; it is not optional, it is not cut for time, and it is measured in the Day-1 satisfaction survey.
- **13:00** — Departure. Thank-you card is dropped in a USPS mailbox on the drive home — hand-addressed, hand-signed by both installers.

**If a new residence and pre-work is needed:** Priya arrives at 06:30 to run network cabling, install the ethernet drop at the placement location, and complete any electrical work identified in the survey. Marco joins her at 08:30 for the customer-facing portion.

---

# 4. Concierge Ops Playbook

## Structure

- **Named primary concierge per household.** One primary, one backup, both named. Meet the family at install. On-call **8:00 AM to 10:00 PM local household time, 7 days a week**.
- **Named overnight coverage per pod.** From 22:00 to 08:00 local, the household is covered by the pod's **Concierge Ops / Overnight tier** — a dedicated, funded rotation, not a passed hat. Overnight staff has the same admin-console access, the same 15-minute critical SLA, and an explicit escalation path to the primary concierge at home (see below).
- **1 primary concierge : 50 households.** At Year 2 (~1,000 households): **20 primary concierges + 4-6 overnight rotating = 24-26 total** across the regional pods. At Year 5 (~5,000 households): **100 primary concierges + 20 overnight = 120 total**, organized in 5 regional pods.

## Contact channels
- **Voice call** — primary. Concierge's cell phone (or the pod's overnight number, 22:00-08:00 local). Not a call center number.
- **SMS** — per household preference. Same number.
- **Companion mobile app** — in-app message thread with the concierge.
- **Email** — for records, receipts, formal documentation.

## Response SLAs
- **Critical** (device unresponsive, security event, panic-button triggered): **15 minutes, day or night.** Overnight (22:00-08:00 local) is answered by the funded Concierge Ops / Overnight tier — see staffing model below. There is no aspirational coverage in this doc.
- **High** (feature not working, privacy concern, media library corruption): **1 hour** during on-hours; 4 hours overnight.
- **Medium** (question, tip request, feature exploration): **4 hours**.
- **Low** (product suggestion, feature request): **24 hours**.

**SLA hit target: 98%.** Missed SLAs trigger auto-escalation to the L2 lead and a written apology from the concierge.

## Escalation matrix
1. **L1 — Named concierge** (primary during on-hours; Concierge Ops / Overnight during 22:00-08:00). Handles 90% of inbounds. Full access to admin console, can push firmware rollback, can dispatch installer.
2. **L2 — Engineering on-call.** Rotates weekly among senior engineers. Concierge conferences them in on live calls, never handing the customer off cold — "David from engineering is joining us now, he's been briefed."
3. **L3 — CTO.** For anything L2 can't resolve in 4 hours or anything security-material. Named handoff, direct call.

### Overnight escalation tree — funded, not aspirational
Because the 15-minute critical SLA is a funded promise, the tree below applies to any critical inbound between 22:00 and 08:00 local household time:

1. **Minute 0-15** — Concierge Ops / Overnight (on-shift, awake, at the desk) picks up. If the incident is device-diagnostic and resolvable from the admin console, it is closed here.
2. **Minute 15** — If not resolved and the household's context matters (security event, distressed caller, medical-adjacent household), overnight ops calls the household's **primary concierge on their home cell**. Primary concierge is compensated for this callback (see comp section — an "on-call retainer" line separate from base). If the primary does not pick up within 3 minutes, overnight ops calls the **backup concierge**.
3. **Minute 20** — If still unresolved, overnight ops pages **L2 engineering on-call**.
4. **Minute 30** — If the incident is security-material or involves a physical safety concern, overnight ops pages the **CTO** and the **Head of CX** directly. Both hold on-call pagers 24/7 with a defined comp adder.

Every step in the tree is logged in the audit trail. Every escalation past minute 15 is reviewed weekly by the Head of CX. The tree is the reason 24-26 heads (Year 2) or 120 heads (Year 5) is the honest floor for the staffing model, not 20 or 100.

## Concierge tooling

**Admin console.** Internal web app. Shows:
- Household profile (names, addresses, install date, extender count).
- Device state (firmware version, last online, storage %, model version).
- Support history (every call, message, ticket).
- Audit trail — every concierge action, timestamped, immutable.

**Data-access primitive.** Per THREAT-MODEL.md, the concierge cannot view customer content (photos, voice recordings, media library metadata) without triple-consent:
1. Customer physically taps the sphere face (biometric-authenticated).
2. Concierge initiates access from admin console with a stated reason.
3. Audit log entry written before access is granted, visible to customer in the mobile app.

The concierge sees only device metadata, health metrics, and support history by default. **This is not a compliance checkbox — it is the moat.** Concierges are trained to explain this on Day 0 and to reference it whenever the customer asks a data question.

## Staffing model

**Primary tier — 1 concierge : 50 households.** Justification: median 2.5 touches per household per month, mean call length 12 minutes. 50 households = ~125 touches/month, ~25 hours of live time, plus ~40 hours of proactive admin and check-ins. 65 hours/month = ~15 hours/week of active work, balance is on-call.

**Overnight tier — Concierge Ops / Overnight.** A dedicated role, hired as its own track, staffed at ~$85k base plus 15% shift differential plus 20% target bonus tied to overnight SLA hit rate. Rotates **8-hour shifts covering 22:00 to 08:00 across the pod's timezones**. Each regional pod carries **4 heads** at ramp (Year 2, ~1,000 households, 4-5 pods = 4-6 overnight total across all pods) and **4 heads per pod at maturity** (Year 5, 5 pods × 4 heads = 20 overnight). Each overnight head covers ~250 households at Year 5 — a much higher ratio than primary, appropriate because overnight incidents are diagnostic-heavy and resolved from the console rather than emotional-relationship work.

**Comp adder for primary concierge overnight callbacks.** When the escalation tree reaches a primary concierge at home (minute 15+), the primary is compensated at a $200 per-callback flat plus $50/15-min of live-call time, capped at a 4-hour session. Budgeted at ~2 callbacks per primary per month at maturity — a $6,000/year comp adder per primary — folded into the Year 5 $14M concierge opex figure in §9.

**Year 2 total concierge headcount: 24-26.** 20 primary + 4-6 overnight rotating.
**Year 5 total concierge headcount: 120.** 100 primary + 20 overnight, plus 25 senior/advisor/regional-head roles above the line (see §10).

## Recruiting sources

- **Ex-Apple Retail Genius Bar** — technical polish, customer polish.
- **Ex-Hermès private client / Chanel VIP** — luxury service posture.
- **Ex-Four Seasons / Peninsula / Auberge concierge staff** — 24/7 mindset, discretion.
- **Ex-family office estate managers** — HNW household understanding.
- **Ex-Genesys / Twilio NOC + ex-hospital overnight nursing coordinators** — specifically for the Concierge Ops / Overnight role. Different profile from the primary tier: calm under 3 AM pressure, comfortable with dashboards, comfortable escalating without ego.

Named recruiter partnerships: Marcum, Boyden's private client practice, an informal network out of Four Seasons Palm Beach, Bellevue, and Wailea, plus a dedicated night-shift recruiter partnership with Aya Healthcare for the overnight tier.

## Compensation

- **Concierge I** (0-12 months): $75,000 base + 15% target bonus tied to NPS + **0.02-0.03% Hearth equity**, 4-year vest.
- **Concierge II** (12-24 months): $85,000 base + 20% bonus + **0.05% equity**.
- **Senior Concierge** (24-48 months): $110,000 base + 30% bonus + **0.10% equity**.
- **Household Advisor** (48+ months, portfolio of 20 top-tier households + mentor role): $150,000 base + 35% bonus + **0.15% equity**.
- **Head of Concierge** (regional, ~5 concierges reporting): **$240,000-280,000 base** + 40% bonus + **0.20% equity**.
- **Concierge Ops / Overnight** (dedicated track): $85,000 base + 15% shift differential + 20% bonus + **0.02-0.03% equity**, matched to Concierge I band.

Senior and regional roles are intentionally **cash-heavy**: base and performance bonus are the primary compensation, equity is upside. See §10 for the aggregate cap-table math (target ≤5% of pool at Year 5, well below the 8-9% envelope prior drafts implied).

**Turnover target: <10%/year.** Above 10%, the customer relationship model breaks. See §10 for the career track.

---

# 5. Extender Pairing — The Second-Room Moment

The extender is a second, smaller sphere ($8,999) that lives in a bedroom, study, or garden room and shares the household voice profiles, media library, and concierge relationship.

**Trigger:** Day 30 concierge call typically. Some families order at install, some at Day 90.

**Flow:**
1. **Order.** Concierge places order during the check-in call; ACH or wire; ships in 3-4 business days.
2. **Delivery.** FedEx overnight in the same unmarked box as the main sphere; contents are the extender itself + a plug-in guide.
3. **Remote install.** Customer plugs in the extender at the intended location. Concierge schedules a 30-minute remote install window and initiates via the mobile app.
4. **Pairing.** Extender broadcasts a one-time code visible on its face. Customer says the code aloud; the main sphere hears and pairs. Concierge confirms the pairing in the admin console.
5. **Physical authorization.** A family member taps the main sphere face to authorize the extender's access to the household's voice profiles and media library.
6. **Follow-up.** Concierge calls 24 hours later to confirm streaming quality and playback experience.

**Success criterion:** 95% same-day paired without incident. 70% extender attach by Day 90 across the customer base — this is the anchor for the loss-leader reconciliation in §6.

---

# 6. First 12-Month Renewal + Upgrade + RMA Pipeline

## Warranty coverage — 3 years included

- **Covered:** any hardware defect (sphere, halo, pedestal, extender); any firmware defect; any error by the concierge or installer team; any content-library corruption caused by Hearth.
- **Not covered:** intentional customer damage (drops, spills, pet damage); environmental damage that violated the placement guide (installed within 30cm of an active fireplace, in an unheated seasonal room without the winterization kit); third-party network issues.

## Renewal

- **Year 3, month 10:** Concierge call to offer 2-year renewal at $2,999 ($1,499.50/yr — a 20% discount to the standard renewal rate).
- **Year 3, month 12:** Standard renewal at $1,899/yr, month-to-month or annual.
- **Retention lever:** the renewal call is framed as continuity, not a sales moment. "We're coming up on year 3, and I wanted to make sure you're set for year 4. Nothing changes — same concierge, same coverage. Want me to put the 2-year renewal on the account?"

## Upgrade path

- **v1.x → v1.y (firmware):** free, over-the-air, opt-in for beta / auto for stable.
- **v1 → v2 (hardware):** offered at Year 4 at 60% of new retail ($57,000). Framed by concierge as "a natural refresh." Target conversion: 60% of active Year-4 households — the same 60% the financial model books at LTV.
- **v1 → v2 sphere trade-in:** old sphere returned to Fremont, refurbished, resold as certified pre-owned at 55% of new retail, or donated to a school of the customer's choice with a plaque. This is a real LTV lever per the ROADMAP.

## RMA

- **Detection:** admin console alerts on any hardware fault. Concierge is auto-paged.
- **Response:** concierge calls within 15 minutes. If replacement is warranted, replacement unit ships within 48 hours.
- **Install:** installer visits within 5 business days to swap. Old unit returned to Fremont for teardown analysis.
- **Interim:** customer keeps the interim unit as a backup unless returned within 30 days of the swap.
- **Customer damage:** covered at 40% off retail for like-for-like replacement. Concierge handles the conversation with grace: "Things happen — here's how we handle it."

## Why concierge is intentionally a loss-leader on subscription

The Year-4-and-beyond concierge economics do not close on subscription renewal alone. This is deliberate, and the LP-facing reconciliation is below.

**Per-household annuals at Year 4+:**
- Subscription renewal: **$1,899/yr**
- Loaded concierge cost (blended $85-95k comp × 1.3 load / 50 HH): **$2,200-2,500/yr**
- Concierge is **~120-130% of subscription revenue in isolation** — a loss on that line item.

**But concierge is the sales team for four higher-margin lines.** The 90-day journey, the moments-of-truth calendar, and the named-relationship posture are what actually drive:

1. **Extender attach at 70% by Day 90.** Each attach is $8,999 with a gross margin of ~70% = **$6,300 gross profit per attaching household**, booked in Year 1.
2. **v2 upgrade at 60% by Year 4.** Each upgrade is a $57,000 net sale (60% of new retail) with a gross margin of ~60% net of refurb and trade-in credit = **$34,200 gross profit per upgrading household**, booked in Year 4.
3. **90% Year-3 retention (vs. an untended baseline of ~65% typical of luxury CE).** Every retained household is another $1,899 × 5-7 years of renewal plus the extender/upgrade cycles above. The concierge relationship is the retention protection.
4. **30% of Year-3+ new sales come from existing-customer referrals** per the financial model. At a $95k ticket with $22k gross profit, each referral is worth ~$22k of gross profit **and** ~$18k of CAC savings vs. paid acquisition. If a concierge portfolio of 50 households produces 3-4 referrals a year, that is $120-160k of gross profit that is directly attributable to the relationship.

**Per-household gross-profit contribution attributable to concierge activity, blended across the cohort:**
- Year 1 extender attach (70% × $6,300): **$4,410**
- Year 4 v2 upgrade (60% × $34,200): **$20,520**, or ~$3,420 amortized per year over 6 years
- Referral value amortized per household: **~$3,000-4,000/yr** on a 3-4-per-portfolio production basis
- Retention-protected renewal margin: **~$1,200/yr**

Blended, a household under concierge care produces **~$12,000-13,000 of gross profit per year attributable to concierge activity** across the full lifecycle. Against a **$2,200-2,500/yr concierge cost**, concierge sits at **~18-20% of gross profit per household — in line with luxury retail benchmarks** (Hermès private client ≈ 15%, Bentley concierge ≈ 18%). See §9 for the full unit-economics reconciliation and the year-by-year target for concierge cost as a share of subscription vs. gross profit.

**Framing for LP conversations:** concierge is a distribution channel priced as a cost line. It should be measured on gross-profit contribution and CAC-payback compression, not on subscription-line profitability. Any Year 5 target that has concierge covered by subscription alone would require raising the ratio to 1:75 or higher — which would break the retention economics on which the entire LTV rests. The trade is deliberate and the math is written down.

---

# 7. The Engineered "Moments of Truth"

## Day 1 first-boot
Sphere animates — halo spins up, face glows to a soft warm white — and greets the household by surname. "Good evening, Chen household." First voice interaction is a family member asking a simple question ("what's the weather tomorrow"), and the sphere responds in the family's chosen voice tone, at the volume it learned from Day 0 room acoustics. The customer's memory: *it knew us already.*

**Measurable outcomes:** Day-1 satisfaction ≥ 4.8/5; first-boot self-test pass rate 100%; concierge outbound within 24 ± 4 hours at 100% cadence.

## Day 3 unexpected check-in
Concierge calls unprompted. "We noticed your library sync completed — anything you want to talk about?" The engineered element: sync completion is a system event that pages the concierge. Customer experiences it as attentiveness, not automation. Concierge is trained never to say "I got a notification" — they say "I saw the sync finished."

**Measurable outcomes:** call placed within 12 hours of sync completion at 95%+; 90%+ answer rate; sentiment of the call scored by the CX Ops lead's weekly spot-audit at 4.5/5+.

## Day 30 memory montage
On the family's most-used evening at their most-used time, the sphere plays a 90-second montage: 15 photos, 2 short video clips, curated on-device from the family's own library. Music from the family's own library, chosen by mood. No AI-language framing. The family sees moments they had forgotten. Concierge calls the next morning: "How was last night?"

**Measurable outcomes — all quantitative, all tested in the cohort dashboard (§9):**
- **Δ NPS from Day 29 to Day 31: target ≥ +8 points.** Day-29 baseline captured by SMS; Day-31 pulse captured within 24 hours of the follow-up concierge call. This is the single most-watched metric on the Day-30 beat.
- **Day-31 concierge follow-up call quality score: ≥ 4.5/5**, rated by the CX Ops lead on a 5-point rubric (empathy, listening, absence of upsell pressure, natural conversation, closing). 10% of calls audited weekly.
- **Day-90 unprompted-recall rate: ≥ 60%** of households, when asked "was there a specific Hearth moment in the last 90 days that stood out for you?", mention the Day 30 montage without prompting.
- **Montage execution window compliance: 100%** of montages fire in the Day 28-32 window on the family's highest-activity evening at their highest-activity time. Zero fires outside window without documented household reason.
- **Concierge Day-31 follow-up completion: 100%** within 24 hours of the montage event.

These metrics replace prior draft language that referenced qualitative reactions. The engineered beat is real, and it is now measured on evidence, not on sentiment.

## Day 90 quarterly product tip + upgrade path mention
Concierge sends 3 personalized tips based on that family's usage. Mentions the upgrade path (v1 → v2, hardware trade-in, extender expansion) as a footnote, not a pitch. The customer registers that Hearth thinks about them as an evolving relationship, not a closed sale.

**Measurable outcomes:** 60% open rate; 15% follow-through on at least one tip; Day 90 NPS median ≥ 9.

## Day 180 personal founder note
A hand-signed physical letter from the founder. Real ink, actual signature (spot-audit: 10% of the founder's staff verify random letters weekly, no autopen). The customer's memory: *the person who made this knows my name.*

**Measurable outcomes:** 100% mailing cadence; 10% spot-audit pass rate on autopen fraud check at 100%; 20% customer reply rate.

## Year 1 anniversary photo book
Hearth generates a hardcover photo book — 40 pages, printed by Artifact Uprising, delivered in a linen sleeve — summarizing the year's family memories. On-device curation, off-device print via a signed BAA with Artifact Uprising (photos leave the household only in an encrypted print job for the specific book, deleted from AU's systems within 72 hours of print). Cost: $80 per book. Retention weapon.

**Measurable outcomes:** 100% of 12-month anniversaries receive book; 72-hour AU deletion audit at 100%; Δ 12-month-anniversary NPS +5 in the two weeks following book delivery.

## Year 3 warranty renewal call
Framed as "we've been with you 3 years — here's what's ahead." Concierge references specific moments from the household's history ("your daughter's graduation photos, your husband's 60th"). Renewal happens as an afterthought at the end of the call. Target close rate: 92%.

---

# 8. Customer Feedback Loop

- **Post-install NPS** — 3 questions max, sent by SMS at Day 1, Day 7, Day 29 (baseline), Day 31 (post-montage), Day 90. Concierge reviews within 4 hours, calls anyone scoring 7 or lower.
- **Quarterly notes to product team** — every concierge writes 500-1000 words summarizing conversations with their 50 households, tagged by theme. Product team reads all notes, publishes response memo.
- **Feature requests via concierge only.** No public voting board. Luxury signal: feedback is via a person, not a form. Concierge relays requests to product, product responds within 30 days, concierge closes the loop with the customer.
- **Annual "State of the Household" email** — every anniversary, each customer gets a personal summary: what they used most, what features they missed, what's on the roadmap for them. Written by the concierge, reviewed by the CX Ops lead.
- **Founder escalation** — any customer considering leaving is escalated to the founder for a personal call BEFORE they leave. Not after. Named "save protocol."

---

# 9. Metrics & Dashboards

## Retention, satisfaction, and operations

| Metric | Target | Cadence |
|---|---|---|
| Install-day satisfaction | ≥ 4.8/5 | Day 1 + Day 7 |
| Day 29 → Day 31 Δ NPS (montage beat) | **≥ +8 points** | Cohort |
| Day 31 concierge follow-up call quality | **≥ 4.5/5** | Weekly spot-audit |
| Day 90 unprompted Day-30 recall | **≥ 60% of families** | Cohort |
| Concierge NPS | ≥ 70 | Quarterly |
| 1-year retention | ≥ 95% | Rolling |
| 3-year retention | ≥ 90% | Rolling |
| Warranty claim rate (Yr 1) | < 3% | Rolling |
| Warranty claim rate (Yr 3) | < 5% | Rolling |
| Concierge SLA hit rate (all tiers, incl. overnight) | ≥ 98% | Weekly |
| Overnight critical SLA hit rate (22:00-08:00 only) | ≥ 98% | Weekly |
| Extender attach rate by Day 90 | ≥ 70% | Cohort |
| Renewal rate (Yr 3 → Yr 4) | ≥ 60% | Cohort |
| v2 upgrade conversion (Yr 4) | ≥ 60% | Cohort |
| Referral share of new-customer sales (Yr 3+) | ≥ 30% | Rolling |
| Concierge turnover | < 10% / yr | Rolling |
| Founder-save success rate | ≥ 60% | Rolling |

## Concierge unit economics — the reconciliation an LP will ask for

| Metric | Year 1 | Year 3 | Year 5 |
|---|---|---|---|
| Loaded concierge cost per household / yr | ~$2,400 | ~$2,400 | ~$2,300 |
| Subscription revenue per household / yr | ~$1,050 (pro-rata) | ~$1,899 | ~$1,899 |
| **Concierge cost as % of subscription revenue** | **~230%** | **~130%** | **~120%** |
| Extender-attach gross profit per HH / yr (amortized) | $4,410 | $735 (residual) | $735 |
| v2 upgrade gross profit per HH / yr (amortized) | — | $3,420 | $3,420 |
| Referral gross profit per HH / yr | $500 (light) | $3,500 | $4,000 |
| **Total gross profit per household / yr attributable to concierge activity** | ~$5,000 | ~$12,000 | ~$13,000 |
| **Concierge cost as % of gross profit per household** | ~48% | ~20% | **~18%** |
| Luxury benchmark (Hermès private client / Bentley concierge) | 15% / 18% | 15% / 18% | 15% / 18% |

**Interpretation:** concierge runs ~230% of subscription in Year 1 (deliberate — the loss is bought back by the extender attach that concierge activity produces in the same year), converges to 120% by Year 5 (with subscription still not covering concierge on its own), and lands at ~18% of gross-profit-per-household by Year 5 — inside the luxury benchmark band. The target is not "concierge pays for itself on subscription." The target is "concierge cost as a share of gross profit stays within luxury benchmark by Year 5," and it does.

## Why concierge is intentionally a loss-leader — one page for the LP deck

The prior draft implied concierge should close on subscription. It cannot, and it should not be asked to. Concierge is the sales, retention, and referral channel — priced as a cost line only because comp is comp. Specifically:

- **(a) Concierge drives 70%+ extender attach at 30 days.** $6,300 gross profit per attach, booked in Year 1.
- **(b) Concierge drives 60% v2 upgrade at Year 4.** $34,200 gross profit per upgrade.
- **(c) Concierge protects 90% Year-3 retention.** The renewal margin defended is $1,200+/yr per household, uncounted in most SaaS retention models because the counterfactual (no concierge, ~65% retention) is not modeled.
- **(d) Concierge drives 30% of Year-3+ new sales via referrals.** ~$22k gross profit per referral, plus ~$18k of avoided CAC.

If any of (a)-(d) misses target by more than 20% for two consecutive quarters, the Head of CX brings a re-plan to the CEO and the board. If all four hit, concierge is the highest-ROI channel in the company measured on blended gross-profit contribution per dollar of comp — and the LP conversation moves from "why so much concierge" to "why not more."

**Dashboards:** internal Grafana instance reading from the concierge admin console's Postgres. Head of CX reviews weekly. CEO reviews monthly. Board sees the retention chart and the unit-economics table above at every board meeting.

---

# 10. Concierge Career Track — 5-Year Path

The comp ladder below is engineered around three constraints, in order: (1) turnover under 10%/yr so portfolios stay intact, (2) cash-heavy senior/regional comp so top performers don't need equity to feel rewarded, and (3) an **aggregate cap-table envelope of ≤5% at Year 5** — well below the 8-9% a prior draft implied and inside the 3-5% band VC-standard for a services function.

## Concierge I — Months 0-12
- Handles 30 households (ramped from 15 in the first 90 days).
- Reports to a Senior Concierge.
- Comp: $75,000 base + 15% target bonus + **0.02-0.03% equity**, 4-year vest.
- Development: shadows 20+ install days, completes internal certification on the admin console, product architecture, and privacy primitives.

## Concierge II — Months 12-24
- Handles 50 households at full load.
- May specialize in a persona pod (medical, PE/finance, arts/philanthropy).
- Comp: $85,000 + 20% + **0.05%**.
- Development: mentors a Concierge I; leads at least one product-feedback synthesis to the product team.

## Senior Concierge — Months 24-48
- Handles 50 households + mentors 2 Concierge Is.
- Regional lead for a specific geography (e.g., Southern California, Northeast Coast).
- Comp: **$110,000 + 30% + 0.10%** — cash weighted, equity is upside.
- Development: participates in install-team hiring; contributes to the Household Guide revisions.

## Household Advisor — Months 48+
- Handles a curated portfolio of 20 top-tier households (multi-property, procurement-heavy, or founder-relationship households).
- Mentor and quality-audit role for the pod.
- Comp: **$150,000 + 35% + 0.15%** — cash weighted.
- Development: prep track for Head of Concierge role.

## Head of Concierge (Regional) — 48+ months
- 5 concierges reporting; owns a regional pod (e.g., "Northeast," 250 households) plus the pod's overnight tier.
- Owns regional NPS, retention numbers, and overnight SLA.
- Comp: **$240,000-280,000 base + 40% target bonus + 0.20% equity.** Cash-heavy by design: performance bonus at 40% of base is comparable to a VP of Sales in a Series B SaaS company. Equity is upside, not primary comp.
- Reports to Head of Customer Experience.

## Concierge Ops / Overnight — dedicated track
- Rotating 8-hour shifts covering 22:00-08:00 across the pod's timezones. 4 heads per pod at maturity.
- Comp: $85,000 base + 15% shift differential + 20% bonus + **0.02-0.03% equity** — matched to Concierge I band on equity, above it on cash to reflect the overnight shift.
- Ladder into primary concierge or into a Senior Ops role that owns a pod's overnight rota.

## Year-5 aggregate cap-table math

At Year 5 the concierge organization looks like:
- 100 primary concierges × 0.02-0.05% (weighted average ~0.035%) = **~3.5%**
- 20 overnight rotating × 0.025% = **~0.5%**
- 20 Senior Concierges × 0.10% (a subset of the 100 primary count above, promoted) — captured within the primary band, not additive
- 15 Household Advisors × 0.15% = **~2.25%** — small population, curated
- 5 Regional Heads × 0.20% = **~1.0%**

Depending on promotion cadence, the aggregate is between **4.5% and 5.0% of the fully-diluted cap table at Year 5.** This sits inside the 3-5% band Series B investors underwrite for a services-heavy function and is far more defensible than the 8.75% a prior draft implied. Rationale for the target:

- **≤5% keeps CX inside the "services function" envelope Sequoia, Benchmark, and Bond typically underwrite.** Above 5%, we get a diligence question we cannot easily answer.
- **Cash-heavy senior comp preserves the primary retention lever** — top performers are paid at market on cash, and equity becomes upside on the outcome they helped create.
- **The equity envelope is the same order of magnitude as an ops/founding-engineering function at Series B**, which is the correct benchmark because concierge is a distribution-and-retention channel, not an ancillary support cost.
- **Portfolio continuity through promotion** — concierges keep their households as they promote — remains the primary non-monetary retention lever. Combined with founder access, an annual off-site (Nantucket, Sonoma), and a real ladder that doesn't force people into general management to grow, this is a cap-table story LPs will underwrite.

**Turnover target: < 10% per year.** Retention levers: cash-forward comp at senior levels, portfolio continuity, founder access, off-site, and a real career ladder. Equity is a supporting lever, not the primary one.

---

## Closing note

The 90-day journey ends at Day 90 only on the calendar. The concierge relationship, the founder relationship, and the household's felt sense that "Hearth is people, not a device" continue for 5-10 years. Every hour spent on Days -21 through +90 is an hour compounded across the customer's lifetime. If we hold 95%/90% retention, we hold a business worth building. If we don't, no amount of hardware brilliance saves us. This is where luxury lives — and every dollar of concierge comp on the P&L is a dollar that returns as extender attach, v2 upgrade, referral, and retention. The math is written down. The overnight tier is funded. The install-day script closes on time. The Day-30 beat is measured on Δ NPS, not on tears. The cap table stays inside the envelope an LP can underwrite.

---
*Document version 1.1. Owned by the Head of Customer Experience. Next review: post-first-100-installs debrief. Feeds pitch objections 12 (warranty burden — see §6) and 21 (LTV — see §6 upgrade path, §7 anniversary book, and §9 unit-economics reconciliation).*
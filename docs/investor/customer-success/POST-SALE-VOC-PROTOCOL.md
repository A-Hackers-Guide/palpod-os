# Hearth Post-Sale Voice-of-Customer Research Protocol
## The Ongoing VoC Framework for the Delivered Install Base

**Owner:** Head of Customer Experience (accountable) + Head of Research (execution)
**Version:** 1.0 — Baseline for Y1 GA (Q4 2027) through Series B (Q1 2029)
**Audience:** CEO, Board of Directors, Series B diligence, Head of Product, Head of CX, all Hearth employees (redacted internal edition)
**Location:** Data Room / customer-success / POST-SALE-VOC-PROTOCOL.md
**Cross-references:** `VOC-MOCK-RESEARCH.md`, `ONBOARDING-PLAYBOOK.md`, `CONCIERGE-CASE-MGMT-SOP.md`, `KPI-DASHBOARD-FRAMEWORK.md`, `PRIVACY-COMPLIANCE-MANUAL.md §3`, `THREAT-MODEL.md §1.2 egress class 5`, `WARRANTY-TRAINING.md`, `HOUSEHOLD-STAFF-KIT.md`, `SERIES-B-PITCH-OUTLINE.md §4`

---

## 1. Research philosophy

Pre-launch voice-of-customer research at Hearth was, by construction, an act of imagination. The `VOC-MOCK-RESEARCH.md` twenty-three-persona corpus is a rigorous but stylized composite — a fusion of adjacent qualitative work, screening-panel signal, and founder-network conversations, blended into archetypal buyers who match the demographic descriptor of the pre-launch waitlist. It was the right instrument for the moment: it forced the founding team to reason about a customer we could not yet observe, and it produced the buyer-segmentation and objection-handling scaffolding that carried us to first delivery. It is a good ancestor. It is not a source of truth about the actual customer.

Post-launch VoC is a different discipline entirely, and the switchover point is Q4 2027 — the moment the first paying household unboxes a sphere. From that day forward, imagined customers are a liability and real customers are the only voice we listen to. This document establishes the ongoing protocol for hearing that voice, at cadence, with rigor, in a form the board can defend to a Series B lead and the product team can act on inside a sprint.

Three underlying beliefs shape everything below.

**First: the company that stops listening after delivery loses the product-market fit it just found.** Product-market fit is not a discovery event; it is a state that erodes if unattended. A luxury connected device sold into a five-to-ten-year household relationship has a longer half-life of fit than a $12 SaaS seat, but a shorter one than a Steinway grand — because the software changes, the household changes, and the competitive context changes. A Hearth in Y1 is a fundamentally different product from a Hearth in Y3: eight firmware releases will have shipped by Y1 end (target: six-week cadence), extender attach will have changed household usage patterns, and the concierge team will have grown from 6 to 40. If we assume the buyer we shipped in month one is the buyer we're serving in month thirty, we will get quiet drift wrong until it is churn.

**Second: real households + real usage patterns + real friction points > stylized composite thinking.** The `VOC-MOCK-RESEARCH.md` corpus described what the Cardiologist in Newport Beach *would* do in the first six months. The post-sale VoC protocol describes what he actually did. Those two datasets are related and not identical. A composite persona cannot surface the specific extender placement problem that emerges in 4,000+ sq ft floorplans with structural steel, because no composite persona has structural steel. A composite cannot tell you that the espresso ritual at 12:45 install-day landed as intended for 78% of households but read as cloying for the tech-fluent founder segment (composite Interview 2). Those are the findings that change product decisions, and they only come from actual delivered households.

**Third: qualitative signal from ~1% of the install base per quarter, systematically captured, outperforms quantitative signal from 100% of the install base captured passively.** A Day 90 NPS score of 72 tells you the direction. A 45-minute video interview with 30 households a quarter, transcribed, thematically coded, and cross-referenced against telemetry and concierge cases, tells you why. The board will want both numbers. The product team can only act on the second one. This protocol is designed to produce both, in parallel, without either polluting the other.

We invert the usual startup posture on this. Most startups treat VoC research as a marketing exercise — a source of testimonials for the website and quotes for the pitch deck. Hearth treats VoC as a **product engineering input** that also happens to produce testimonials as a byproduct. The research is done to change decisions, not to validate them. If a quarter of interviews surfaces no new insight, the interviewers are being trained wrong. If the interviews reliably produce feel-good quotes and no friction, we are talking to the wrong households. The protocol is calibrated for the second failure mode: we oversample households with mixed satisfaction, we probe hard on frustration, and we mandate a full 5-minute "have you considered stopping?" segment in every interview regardless of how green the concierge scorecard reads on that household.

The alternative — the failure mode we're engineering away from — is the startup that ships to product-market fit, celebrates, and then discovers eighteen months later that half the customers were quietly disappointed but too polite to complain. At $95,000 a household, at 5–10 year expected relationships, at a Y3 install base of 5,700 units generating an LTV story on which the Series B valuation is built, the cost of that failure is measured in tens of millions of dollars of eroded enterprise value. This protocol is the insurance policy against it.

---

## 2. Research cadence and methods

The protocol runs seven concurrent streams. Each stream has a distinct purpose, cadence, sample structure, and governance owner. Together they produce the full picture; individually, no stream is sufficient.

### 2.1 Quarterly in-depth interview program (the primary instrument)

Thirty households per quarter in Y1, forty-five in Y2, sixty in Y3+. Forty-five-minute semi-structured video interviews conducted by trained third-party researchers (§5, §9). Aligned to specific household milestones: Day 90 (freshest, still-forming impressions), Day 180 (early routine formation), Day 365 (first renewal window signal), and annually thereafter at renewal anniversary. Each household is interviewed at most twice per year to avoid response fatigue; households can opt out at any time with no service impact per PRIVACY-COMPLIANCE-MANUAL §2.2 non-discrimination.

Sampling is stratified across **three primary dimensions**: cohort quarter, household-composed archetype (single principal, couple, multi-generational, family with children), and international vs. domestic. Prior draft claimed 7-dimension stratification at N=30 — that math didn't survive ("systematic surfacing per segment" at ≤1 interview per stratum cell is not systematic; it's anecdotal). At 3 dimensions with N=30 we get 5-10 interviews per meaningful cell, which supports qualitative saturation per segment. **Secondary dimensions** (sphere finish choice, concierge case density, extender attach state, presence of household staff) are captured as descriptor metadata on each interview for post-hoc analysis, NOT as sampling strata. Sampling is not random; it is deliberately structured to ensure each primary segment produces signal each quarter. Statistical generalizability is not the goal; systematic surfacing of segment-specific findings is. Saturation criterion per stratum: 5 interviews minimum per archetype × cohort × geography cell before we claim a finding is segment-signal rather than individual-observation.

### 2.2 Continuous NPS capture

Per ONBOARDING-PLAYBOOK cadence: Day 30, Day 90, Day 180, Day 365, and quarterly thereafter for the life of the relationship. All captures are single-question NPS ("How likely are you to recommend Hearth to a friend or colleague?") plus one open-text follow-up ("What is the primary reason for your score?"). Delivery: in-app for households who have installed the mobile app, email fallback, concierge-verbal capture on the quarterly wellness call for households who prefer phone contact.

The NPS instrument is intentionally short. Long survey instruments correlate with lower response rates in luxury segments (industry benchmark: Bang & Olufsen private-client NPS surveys average 6 questions; Hearth stays at 2). The rich signal comes from the interview program (§2.1) and the concierge cases (§2.3), not from the NPS instrument. NPS is the quantitative baseline that lets us track trend and stratify the interview sample. It is not the primary insight source.

Response rate target: 65% for Day 30, 55% for Day 90, 45% for Day 180 and beyond. Non-response is itself signal and is tracked separately; households who go non-responsive for two consecutive NPS windows trigger a concierge outreach independent of any complaint or ticket.

### 2.3 Concierge case pattern analysis

Monthly review of L1/L2/L3 case tickets per CONCIERGE-CASE-MGMT-SOP.md. Every concierge case is coded at closure against a controlled taxonomy: category (hardware / software / concierge experience / physical design / voice interaction / face recognition / media library / extender / integration / other), severity (P0 through P4), household segment, resolution path, and time-to-resolution.

The monthly analysis produces two artifacts. First, a **top-10 case-pattern list** — the ten most common issue categories in the trailing month, ranked by frequency and severity, with representative case examples. This goes into the product team's Monday standup and the CX weekly review. Second, a **rising-pattern alert** — any category whose 90-day trailing frequency has increased more than 40% over the prior 90-day baseline, or any P0/P1 that has occurred more than twice in a household segment, triggers an immediate cross-functional review with product, engineering, and CX leadership.

Concierge case data is inherently biased toward the complaining half of the customer base — the silent half never files a ticket. The interview program (§2.1) is the corrective; it samples across the full complaint distribution, not just complainers.

### 2.4 Anonymized usage telemetry (opt-in)

Per THREAT-MODEL egress class 5 (bug reports, opt-in HTTPS to `sentry.hearth.support`) and a distinct class we're adding for aggregated usage counts: opt-in transmission of scalar usage counters — sphere wake events per day, extender activation counts per day, voice interaction counts per day, feature-usage counters (music, media playback, memory recall, notes) — with no content, no transcripts, no timing sequences, no cross-household correlation.

Opt-in is presented at install day within the BIPA consent flow described in PRIVACY-COMPLIANCE-MANUAL §3, with entirely independent revocation. Target opt-in rate: 60%+ at Y1, given the Hearth brand posture around household sovereignty and the fact that offering this at all requires care not to undermine our "your household voice, faces, and memories never leave your Hearth" marketing promise. The distinction we make explicit in the consent copy: transmitting a counter that says "your sphere woke 42 times today" is categorically different from transmitting "here is what you said," and the source code of the counting daemon is inspectable by the household.

Analysis is at the cohort level, never at the household level in cross-team briefings. A telemetry finding may say "Y1-Q4 cohort shows median 38% higher extender activation than Y2-Q2 cohort" and cannot say "Household 4127 activated their extender 12 times more than average." Household-level dashboards exist for the concierge team's own use in support of that specific household, gated to the concierge assigned to that household, and are not visible to product or research.

### 2.5 Household staff research

Housekeepers, nannies, house managers, chefs, and property managers who interact with Hearth are a distinct research population per HOUSEHOLD-STAFF-KIT relationship. They see the product from a different angle than the principal purchaser: they use it more often (in some households), they use it differently (voice-first, less patient with dialog trees), and they observe failure modes the principal never sees because the household staff resolves them silently before the principal notices.

Cadence: quarterly interviews with 10 household staff members in Y1 (scaling to 20 in Y3), separately recruited from participating households, separately consented, separately compensated ($200 honorarium to the staff member individually), interviewed by a researcher with hospitality-industry experience (not by the same researcher who interviews principals). Interview length: 30 minutes. Structure detailed in §4.

Consent is nuanced. The household principal must permit the recruitment invitation to go to their staff, but the staff member's participation is voluntary and confidential — the principal is not told which staff members participated, is not shown the transcripts, and is not given any household-attributable summary. Findings are reported to Hearth only at the aggregate level across staff, or at the household-anonymized level within a segment. Violation of this confidentiality boundary is a fireable offense within Hearth Research.

### 2.6 Annual retention interview

Every household approaching a renewal decision (Year 3 → Year 4 concierge subscription renewal is the primary trigger; ownership of the sphere itself is not subscription-gated) is offered a 45-minute annual retention interview. This runs regardless of whether the household is showing churn signals — offering it only to at-risk households would poison the instrument. Compensation: $300 honorarium routed through the research firm.

Interview structure: 15 minutes on the year in review ("What did Hearth do for you this year that mattered?"), 15 minutes on the near-term ("What would make next year better?"), 10 minutes on the counterfactual ("If you moved to a smaller home / your household changed / a competitor released something similar, would Hearth come with you?"), 5 minutes on referrals ("Who in your life have you told about this? Who else should have one?"). Response rate target: 70%+ at Y3 onward; the Y1 renewal cohort is small (~100 households, since Y1 GA is Q4 2027 and Y3-to-Y4 renewals begin Q4 2030) and warrants a target of 85%.

### 2.7 Post-cancellation interviews

Any household that cancels the concierge subscription or returns the sphere is offered a mandatory-invitation, entirely optional 30-minute interview. Explicit protocol: the interview is offered by name in the cancellation flow, the cancellation is processed regardless of whether they accept, the honorarium ($400) is delivered regardless of what they say in the interview, and there is no attempt to save the account within the interview itself (save attempts happen in a separate flow, before the interview offer, run by the concierge team, and they are decoupled from the research entirely).

Interview target: 90% of cancellations complete the interview within 60 days of cancellation. This is the single highest-signal research population Hearth has: they have converted, lived with the product, and left. Their reasons are the roadmap.

Cancellation interviews are conducted by a senior researcher (not by junior interviewers, not by the concierge who lost the account, and not by anyone with a commercial incentive to reframe). The transcript goes to a small standing committee — Head of CX, Head of Product, CEO — and to no one else without further consent. Aggregate findings enter the quarterly board packet.

---

## 3. Sample size and cohort tracking

Sample size scales with install base and stabilizes at the point where an additional interview per quarter is no longer changing the thematic-saturation curve. That point, in analogous consumer-luxury research programs, sits around 45–60 interviews per quarter across a stratified sample of an installed base under 10,000.

### 3.1 Y1 targets (200 units GA + 400 late-year ramp = 600 total installed by Y1 end)

- Quarterly interviews: N=30 rolling (~5% of installed base per quarter, which is intentionally high for the small Y1 base to compensate for lower base-rate diversity)
- Annual retention interviews: N=0 in Y1 (first cohorts still under 12 months)
- Post-cancellation: expected N≤10 in Y1 at 96%+ retention target from KPI-DASHBOARD-FRAMEWORK CX2, all interviewed
- Household staff: N=10 per quarter
- Concierge case pattern analysis: 100% of cases coded, monthly aggregate report
- Telemetry opt-in target: 60% of Y1 base by Y1 end

### 3.2 Y2 targets (2,500 install base)

- Quarterly interviews: N=45 rolling (~1.8% of installed base per quarter)
- Annual retention interviews: N=~50 (the Y1 Q4-2027 cohort begins hitting Y3→Y4 renewal in late Y3, not Y2 — so Y2 sees only the very small Q1-2028 pre-GA cohort at renewal; we plan for 20 minimum)
- Post-cancellation: expected N≤80 at 97% retention, all interviewed
- Household staff: N=15 per quarter
- Cohort tracking: Y1 GA cohort followed forward at every milestone
- Telemetry opt-in target: 70%+ Y2

### 3.3 Y3 targets (5,700 install base)

- Quarterly interviews: N=60 rolling (~1.1% of installed base per quarter)
- Annual retention interviews: N=~140 across the Y1 cohorts hitting Y3→Y4 window
- Post-cancellation: expected N≤170 at 97% retention, all interviewed
- Household staff: N=20 per quarter
- Cohort tracking: Y1 GA cohort now in Year 3 of longitudinal follow, Y2 cohorts in Year 2
- Telemetry opt-in target: 75%+ Y3

### 3.4 Cohort discipline

Cohort tracking is the discipline that most distinguishes a durable VoC program from a rolling-snapshot one. Every household is tagged at delivery with a cohort quarter (e.g., "27Q4," "28Q1"). All findings are always analyzed with cohort as a first-class variable. A Y3-cohort-27Q4 interview is compared against the same household's Y1-cohort-27Q4 interview and against the Y3-cohort-27Q4 aggregate — not against a same-quarter snapshot of newer cohorts.

Cohort tracking horizon: **Y1 GA cohort (27Q4) is followed for a minimum of five years.** This produces the first defensible dataset for a Series B pitch's LTV story: five years of longitudinal signal on the households that bought the first-generation product, including through the v2 hardware transition, extender introductions, and the full concierge team scaling. The 27Q4 cohort is the crown-jewel dataset of the entire research program and its members are handled with corresponding care — no over-interviewing, no experimental research designs, and preferential treatment in participation invitations.

**International cohorts are tracked separately** — UK, DACH (Germany/Austria/Switzerland), and Singapore each get their own cohort track from first international shipment onward. International household interviews are conducted by researchers based in-region, in the household's preferred language, with cultural translation review before any finding enters the domestic aggregate. Combining international and domestic data prematurely is one of the failure modes we're most disciplined against — a UK household's "very satisfied" answer sits in a different cultural register than a US household's and combining them into a mean is a lie by construction.

---

## 4. Interview protocol — the 45-minute template

Every quarterly in-depth interview follows the same skeleton, personalized only where §2.1 sampling stratification indicates a segment-specific probe. The skeleton exists because comparability across cohorts and time is more valuable than the marginal insight from freewheeling per-interview design; interviewer discretion applies within segments, not to the segment structure.

### 4.1 Opening (5 minutes) — warm-up and context refresh

The interviewer opens with a brief, non-transactional greeting; confirms the household's preferred name form; and does a two-minute context refresh: "Since we last spoke [or since your install date], here's what we know from the concierge notes — you took delivery on [date], you're in [region], you have [household composition on file]. Anything that has changed we should know?" This surfaces material household events (moves, staff changes, family additions or losses) that will shape everything downstream.

Then the informed-consent restatement: "This conversation will be recorded and transcribed. Findings are used to improve Hearth's product and are shared inside Hearth in aggregate form. Your name and household will never be in a marketing artifact without your written consent. You can skip any question or stop the interview at any time." This is captured verbally on the recording and logged.

### 4.2 The 90-day open (10 minutes) — "How has Hearth changed your household?"

Semi-structured open question with minimal prompting. Interviewer discipline: listen for the answer that isn't the product. When a household member says "we started having dinner together again" or "the kids ask me to put on music and it's the first time in three years we've had music in the house" — that is the finding, and the interviewer's job is to draw out the specificity, not to redirect toward the feature.

This block is where the biggest surprises live. It is the block most frequently mistaken by inexperienced interviewers as "warm-up" — it is not. It is the primary research finding of the interview, and the remainder of the session is calibration around what emerges here.

### 4.3 Feature-specific probes (10 minutes) — personalized per household

The interviewer has a pre-populated feature-usage sheet drawn from concierge notes, telemetry (if opted in), and prior interviews. From this sheet, three or four features get specific probes. The probes are constructed the day before each interview, not from a fixed script, because the whole point is to ask this household about their features, not this quarter's average household's features.

Standard probe forms: "You've used [feature X] roughly [Y] times per week — walk me through the last time you used it. Where were you standing? Who else was in the room? What did you ask for?" This produces episodic recall rather than opinion, and episodic recall is roughly twice as reliable at surfacing product friction as opinion is.

### 4.4 Frustration surface (5 minutes) — critical for product feedback

Structured, deliberately hard. The interviewer opens: "I want to spend the next five minutes on what has frustrated you. Everything I've heard so far has been very positive, and one of the failure modes of this kind of research is that people are polite. So I'm going to push here."

Three prompts, in order:
1. "What has not worked the way you expected?"
2. "What have you stopped trying to do because it didn't go well the first time?" — this is the highest-yield question of the whole interview, because it surfaces silent-abandonment features
3. "If you could change one thing about your Hearth today, what would it be?"

The interviewer holds the pause after each of these prompts for uncomfortably long. Discomfort is the point. Frustration that emerges in the first three seconds is usually the polite frustration. Frustration that emerges after ten seconds of silence is the real one.

### 4.5 Referral proxy (5 minutes) — "What would you tell a friend about it?"

Two probes. First, an open form: "Someone at dinner asks you about Hearth — what do you actually say?" This produces the household's own product pitch, in their own words, which is the highest-quality raw material for marketing copy the company can obtain (and is treated as such under §10 publication rules).

Second, a bounded form: "Who in your life have you already told? What did they say back?" This is the honest referral signal, in contrast to the NPS "would you recommend" hypothetical. A household that has already told two friends is the referral-flywheel input the LTV model depends on. A household that gave an NPS 9 but has told nobody is a different signal — a satisfied but not evangelical customer.

### 4.6 Churn early warning (5 minutes) — "Have you considered stopping?"

This is the block that most surprises non-research stakeholders when they first review the protocol. Every interview asks it, regardless of household signal. The framing matters: "Every household we talk to, we ask this. Have you considered stopping — either canceling the concierge, unplugging the sphere, or moving to something else? Even in a small way?"

The reason we ask every interview is that if we only asked at-risk households, the presence of the question itself would signal to the household that they're at risk, which changes the answer. Universal asking normalizes the question. The information yield across an install-base cohort is what we're after: 82% of households in Y1-27Q4 said "never" at Day 90 tells us something. 74% at Day 180 tells us something different. The comparison is the finding.

Follow-up probes when a household indicates any consideration of stopping: what triggered the thought, what would have to change to remove the thought, what would be the tipping point.

### 4.7 Household staff involvement and concierge experience (5 minutes)

Two intersecting probes. First, household staff: "Who in the household — including any staff — uses Hearth other than you? What's their relationship with it?" This surfaces the shadow-usage patterns that principal-only research misses. It also identifies household staff candidates for the separate §2.5 research stream.

Second, concierge experience: "Tell me about your concierge relationship. When did you last talk to them? What was the interaction? How do you feel about them?" The concierge is the durable moat per ONBOARDING-PLAYBOOK preamble; this block validates whether the moat is holding.

### 4.8 Close

Interviewer thanks the household, restates confidentiality, confirms the honorarium delivery mechanism, and offers the household member the opportunity to add anything unprompted. Roughly 15% of interviews have their highest-signal moment in this "anything else?" close, which is why it is a mandated element and not a courtesy.

---

## 5. Interviewer training

The single largest determinant of interview data quality is interviewer craft. Bad interviewers produce data that looks like research and is worse than no data, because it enters the record and drives decisions. This is the single most under-appreciated failure mode of in-house VoC programs, and it is why we do not conduct interviews with internal Hearth staff for the primary program.

### 5.1 External training partner

All quarterly-program interviewers are trained by an external research firm — Ipsos, Kantar, or a comparable qualitative-research operator — under a Y1 training contract of $30–50k. Training scope: qualitative interview craft, active listening, probe construction, pause discipline, unconscious-bias screening, and household-specific cultural fluency for the luxury segment.

Renewal: every interviewer completes an annual recertification module ($5k per interviewer per year at Y2+), and any interviewer whose transcripts fail two consecutive quarterly quality reviews (§6.3) is retrained before returning to the roster.

### 5.2 Consent and privacy training

Every interviewer is separately trained on the Hearth-specific consent framework in PRIVACY-COMPLIANCE-MANUAL §3, on BIPA, and on the household-scoped confidentiality model. Interviewers sign a Hearth-specific NDA that survives their contract by three years.

### 5.3 Non-leading question discipline

Interviewers are drilled on non-leading question construction. "Do you like the new feature?" is a leading question. "How has the new feature affected your household routine, if at all?" is not. Every interviewer transcript is spot-audited for leading questions in the first six months of tenure, then quarterly.

### 5.4 Household member consent at interview start

The interview opens with an explicit consent restatement (§4.1) and confirms the household member's understanding. Any member can skip any question with no explanation required and no follow-up. This is captured verbally in the recording and in the researcher's structured notes.

### 5.5 Household staff separate interviews with separate consent

The consent for the principal to be interviewed does not extend to household staff. When staff are interviewed under §2.5, they consent independently, are compensated independently, and their transcripts are held on separate confidentiality terms. The principal is told that staff research happens but is not told which staff participated. See §5.2 for the confidentiality enforcement.

### 5.6 Cultural fluency for international cohorts

UK interviews are conducted by UK-based researchers. DACH interviews are conducted in German by German-speaking researchers with in-region cultural fluency. Singapore interviews are conducted by researchers with Singapore hospitality-industry background. Translation of transcripts into English for the domestic team happens after the interview, not during, and includes a cultural-translation note (e.g., "The household's phrasing here would read more strongly in US English than the direct translation suggests").

---

## 6. Data infrastructure

Every data-handling decision in this program is downstream of PRIVACY-COMPLIANCE-MANUAL. The research infrastructure inherits the same offline-first, household-controlled, minimum-egress posture as the product itself, and any variance from that posture is documented as a delta rather than a default.

### 6.1 Storage

Interview transcripts are stored on Hearth-controlled infrastructure — the research subsystem within `research.hearth.co`, hosted in a US-region GCP tenancy with EU-region redundancy for GDPR-scope data. Transcripts are encrypted at rest with per-household envelope keys, are pseudonymized before entering the analysis corpus (a stable household ID, no name or address), and are retained per PRIVACY-COMPLIANCE-MANUAL §3 retention schedules.

Video recordings are held for a maximum of 90 days from interview date and then destroyed; only the transcript, the researcher's structured notes, and the coded findings persist beyond 90 days. This is a discipline against the temptation to re-mine video for expressions or hesitations after the interview — the transcript is the record, and the video's short retention forces the researcher to capture what matters during the initial pass.

### 6.2 Household-scoped data — never cross-household correlation without explicit consent

The default is that a finding attributable to Household 4127 is not correlated with a finding attributable to Household 4128 without both households' explicit written consent. This restriction is stricter than most research programs and is inherited from the household-sovereignty posture of the product itself. The workaround for aggregate analysis is pseudonymization: analyses at the segment or cohort level operate on pseudonymized IDs, and re-identification requires the same consent gate that any household right-to-know request would receive.

### 6.3 Quantitative outputs

Anonymized quantitative results — NPS by cohort, thematic-coding frequencies, feature-usage counters from the opt-in telemetry stream — feed the CX dashboards and Board packet §E per KPI-DASHBOARD-FRAMEWORK cadence. These outputs are structured so that a Series B diligence lead can inspect the underlying methodology without inspecting the underlying individual households, per the same firewall the auditor sees.

### 6.4 Marketing use

Interview content is never used for external marketing without explicit household consent captured after the fact, in a separate flow, with a specific quote or theme in view. This is the single most-frequently-violated principle in most research programs and the one we are most disciplined against. The temptation to use a beautiful quote from the Day 180 interview in a Series B deck is very strong. The rule is: the quote does not appear anywhere outside the internal report without a separately captured, quote-specific, written consent from that household. Violations are documented as compliance incidents and reported to the audit committee.

### 6.5 Deletion on household request

A household member's transcripts, structured notes, and coded findings are destroyed on request, within 45 days per CCPA SLA (targeting 24 hours per PRIVACY-COMPLIANCE-MANUAL §2.2). The deletion is cryptographic (per-household envelope key destruction) and produces a certificate of deletion to the household. Aggregate findings that included the household's data are retained; the household's specific contribution is unlinked and cannot be reassembled.

---

## 7. Feedback loops

The research program produces a finding-to-action pipeline at four cadences. The pipeline is the point; a program that captures voice and never transmits it to the decisions is theater.

### 7.1 Weekly — concierge case patterns to product standup

Every Monday, the concierge case pattern analysis (§2.3) top-10 goes to the product team's Monday standup as a fifteen-minute standing agenda item. The concierge case-review lead delivers the report. Rising-pattern alerts (§2.3) preempt the standing agenda if any are open.

### 7.2 Monthly — interview themes to CX and product monthly review

The trailing month's completed interviews are thematically coded by a lead researcher and produce a monthly thematic report. Format: five to seven themes, each with representative quotes (pseudonymized), frequency across the interview sample, cohort stratification, and an explicit "so what?" that names the specific product or CX action the theme suggests. This report goes to Head of CX and Head of Product monthly, in advance of the CX/product monthly review meeting where it is discussed against the concierge-case top-10 for cross-signal validation.

### 7.3 Quarterly — full VoC report to CEO, Head of Product, Head of CX

The full quarterly VoC report is a ~40-page internal document produced by the research lead. It includes: interview thematic analysis, NPS trend by cohort, concierge case aggregation, telemetry aggregation (for opted-in households), household staff research findings, cancellation interview findings, and cross-signal integrations. It concludes with a prioritized list of five to ten specific recommendations for product, CX, and marketing action, each with an owner and a target quarter.

The CEO reads it in full. The Head of Product and Head of CX read it in full. The board sees a summary version in the quarterly board packet (§7.4). Every recommendation is tracked in the following quarter's report against action taken.

### 7.4 Semi-annually — board packet §E VoC summary

Every board packet includes a "voice of customer" summary in §E, running six to eight pages, drawn from the two most recent quarterly reports. Structure: cohort-level metrics, thematic trends, recommendation follow-through from the prior six months, and a single narrative section titled "what we heard we didn't want to hear," which is deliberately calibrated for the failure mode of an all-green board summary (§10.2).

### 7.5 Annually — full VoC report to entire company

Once per year, in Q1, the prior full year's VoC synthesis is published to every Hearth employee. Format: a redacted long-form document (~80 pages) plus a two-hour all-hands session where the research lead walks through the findings and takes questions. Every household-attributable quote is either separately consented (§6.4) or fully pseudonymized. This annual publication is the single largest cultural intervention we make on behalf of customer-centricity: everyone in the company, from engineering to finance to Marco the installer, reads what the customer said. Marco reads what happened after he left.

---

## 8. Board-level metrics

The research program produces the following metrics into KPI-DASHBOARD-FRAMEWORK §CX and board packet §E. These are the quantitative outputs; the qualitative outputs are the narrative context that gives them meaning.

- **1-year retention curve by cohort.** Percentage of households in each cohort still in active concierge subscription at 1-year anniversary. Y1 target: 96% per KPI-DASHBOARD-FRAMEWORK CX2. Reported by cohort quarter so drift is visible.
- **3-year retention curve.** Percentage of households in each cohort still active at 3-year anniversary. First measurable in Q4 2030 for the 27Q4 GA cohort. Y3 target: 88% per FIN-MODEL LTV assumption.
- **Household NPS by cohort.** Cohort-stratified NPS, tracked at each capture point (Day 30 / 90 / 180 / 365 / quarterly). Reported both as latest snapshot and as trajectory. Y1 target: 70+.
- **Household staff NPS.** Distinct instrument, distinct target. Y1 target: 60+ (household staff population is less demographically homogeneous than principals and less inclined to score in the 9–10 range regardless of satisfaction; the target reflects that structural difference, not a lower expected quality bar).
- **Concierge NPS.** Per CX1 in KPI-DASHBOARD-FRAMEWORK. Y1 target 70, Y3 target 75.
- **Referral-proxy score.** Percentage of interviewed households who report having actually recommended Hearth to at least one specific person in the trailing 90 days (not the hypothetical NPS "would you recommend" — the concrete "have you"). Y1 target: 45%. Y3 target: 65%.
- **Churn early-warning score.** Percentage of interviewed households who report having considered stopping in the trailing quarter. Y1 target: <20%. Rising trend triggers §7.1 rising-pattern review even if retention numbers remain green.
- **Product feedback signal strength.** Number of distinct product-actionable findings surfaced per quarter that produce a product-team ticket. Not a target metric — a health metric. Below 15/quarter suggests the interviews are converging on satisfaction validation rather than product signal, which triggers an interviewer-training review.

These metrics feed the Series B pitch materials directly. The board narrative on customer health is built from them, and the underlying qualitative context — the quotes, the themes, the specific household stories that make the metrics legible — is provided to serious diligence leads under a data-room NDA.

---

## 9. Third-party research firm engagement

Y1 primary research firm engagement is with a **boutique qualitative-research firm capable of quarterly luxury-segment depth interviews** — candidates: reMarkable (unrelated to the tablet company), C Space, Ripple Effect, or a comparable operator — at **$250–350k per year** for the quarterly interview program including 170 depth interviews (~120 principal + 40 staff + 10 cancellation) at a fully-loaded ~$2,000-2,500 per interview, plus $30-50k training investment, plus transcription infrastructure and thematic coding. **Prior draft cited Ipsos/Kantar at $75-120k/yr — that was a mispricing: Ipsos and Kantar are $4B+ firms with $200-500k engagement minimums and $2-5k per depth interview all-in; at 170 interviews × $3k midpoint the Ipsos/Kantar spend alone is ~$510k before training or PM overhead. The $75-120k number is boutique-firm pricing, so the firm assignment is corrected here to match.** Y2+ scales to $400-500k as N increases to 45 then 60. Ipsos/Kantar remain candidates only if the RFP surfaces pricing below their published minimums, which is unlikely absent an unusual strategic account fit.

Y2 the firm engagement scales to $150–200k with the expanded sample size and adds a boutique specialist firm — Boyer & Associates, a former Corporate Executive Board (now Gartner) practice lead, or comparable — at $50–75k for the household-staff research stream, which requires a different research craft than the principal interview program.

Y3 the strategic decision on bringing the primary program in-house versus continuing outsourced is made. Both paths have defensible cases:

- **In-house** (VP Research + 3-person team, $600–800k annualized): higher control, deeper integration with product decisions, better retention of institutional research knowledge across years, but at the risk of the same interviewer-craft failure mode we've engineered against
- **Continuing outsource** ($250–400k annualized at Y3 scale): craft discipline maintained, external perspective preserved, insulation against internal politicking of findings, but at the cost of some integration latency and firm-side researcher turnover

The recommendation as of this document is: bring one senior research lead in-house at Y2 (VP-level, $300–400k loaded) as the internal owner of the program, and continue outsourcing interview execution through Y3 minimum. Revisit at Series B close. The senior lead's job is not to conduct interviews; it is to translate findings into decisions and to hold Hearth accountable to acting on them.

**Alternative firm considerations:** the boutique qualitative-research firms most often referenced in luxury CPG and premium-service categories — reMarkable (unrelated to the tablet company), C Space, Corporate Executive Board's successor practice at Gartner Peer Community — should each be evaluated on the Y2 boutique engagement. Ipsos and Kantar are the default because they have the operational scale for the primary program; the boutique firms are stronger on specific segment work.

---

## 10. Publication of VoC insights

The default publication posture is internal and rare. Nothing about this program is optimized for external content generation, and every external publication decision is treated as a compliance-and-brand event, not a marketing event.

### 10.1 Internal (default: everything)

Quarterly readouts to CEO, Head of Product, Head of CX. Semi-annual board packet §E. Annual full-company report and all-hands. These publications are internal by construction and are the primary channels for the research program's own outputs.

### 10.2 External (default: never; exceptions: rare and curated)

Occasional external publication may take one of three forms, in ascending order of external exposure:

1. **A Substack post or founder essay on a single VoC theme** — with explicit household consent on any quoted material, with legal review, and only when the theme has genuine informational value beyond product marketing. The bar is: would this be worth reading if it were not written by Hearth? Frequency: at most twice a year.
2. **A podcast interview with the founder or Head of CX referencing aggregate findings** — no specific household attribution ever, no quotes without written consent, aggregate percentages only. Frequency: opportunistic, not scheduled.
3. **A rare permission-granted individual customer story** — deep, respectful, done with legal and PR review, with the household's ongoing content-approval right, treated as a favor from the household to Hearth rather than the reverse. Frequency: at most once a year, ideally zero.

None of the above is done to drive marketing pipeline. Marketing pipeline uses the sales team's own testimonial program, which is a separate legal and consent framework.

### 10.3 Investor-facing

Quarterly VoC summary in board packet §E per §7.4. Fuller VoC synthesis in Series B and Series C pitch materials, with the underlying methodology reviewable by diligence leads under NDA. Investor-facing content is aggregate-only in written materials; specific household stories, if shared at all, are shared verbally by the CEO in a diligence conversation, with the household's prior written consent and with the diligence lead's understanding that it is not for circulation.

### 10.4 Employee-facing

Every employee reads every internal report. This is a first-principles cultural commitment. It is what keeps engineering, finance, and operations connected to the actual customer. A company where the customer research lives in the CX and product functions only is a company where the rest of the organization drifts from the customer. Hearth's cultural bet is that having Marco the installer read the same VoC report that the CEO reads makes Marco a better installer and the CEO a better CEO. It also makes the research program itself accountable to more people than a private feedback loop would.

---

## 11. Cross-referenced VoC categories

Every finding is coded against a controlled taxonomy of eight categories, and findings are reported both by category and cross-category where relevant. The categories are:

- **Product (functionality)** — what the sphere and its software actually do, feature-by-feature. Highest-frequency category by ticket volume, second-highest by interview signal.
- **Concierge (relationship)** — the human relationship with the assigned concierge. Highest-signal category by strategic weight, per the ONBOARDING-PLAYBOOK preamble that the concierge is the durable moat.
- **Physical design (aesthetics and fit)** — where the sphere physically lives, how it looks in the room, whether it visually fits the household. Understated category that produces surprisingly high satisfaction signal — the households that love this category love it deeply.
- **Voice and face (interaction quality)** — quality of voice interaction, face-recognition experience, dialog-tree fluency, hallucination rate, latency. Product-team's densest signal source.
- **Media library import (onboarding)** — the MEDIA-IMPORT-RUNBOOK experience, from initial NAS ingestion to ongoing media additions. Highest-friction category in Y1 by concierge-ticket volume; the top-of-mind driver of early-cohort frustration.
- **Extender experience** — placement, coverage, dual-sphere synchronization, extender-specific concierge interactions. Newer category that requires more sampling as extender attach rate grows.
- **International-specific concerns** — customs, warranty logistics, regional integrations, cultural fit of concierge scripts, language localization. Tracked separately per §3.4 cohort discipline.
- **Household staff dynamics** — how staff interact with the sphere, how the principal-staff-Hearth triad functions, whether the sphere creates or resolves household-workflow friction. Distinct research stream per §2.5.

Cross-category findings are common and are called out explicitly. Example: a household frustration with media library import (category 5) may present as a product complaint but resolves as a concierge onboarding-experience issue (category 2) — the media import worked technically but the household member was never shown that a specific playlist was in the library. That kind of cross-cutting finding is the highest-leverage output of the program.

---

## 12. Ownership and governance

**Owner:** Head of Customer Experience is accountable for the program. Head of Research (Y2+ hire) is responsible for execution. Until the Head of Research is hired (target Q2 2028), the Head of CX runs the program directly with contracted research-firm support.

**Reporting:** monthly to CEO in a 30-minute standing meeting with the Head of CX. Quarterly to the board in board packet §E. Semi-annually to the audit committee for compliance-and-consent review per PRIVACY-COMPLIANCE-MANUAL §3.

**Budget:** Y1 total program budget **$500–700k** (was $200-400k in prior draft — corrected after research-firm mispricing + honoraria arithmetic error), with the breakdown:
- Research firm engagement (boutique tier — reMarkable / C Space / Ripple Effect): **$250–350k** (was $75-120k Ipsos/Kantar — mispriced; see §9 correction)
- Interviewer training: $30–50k (§5)
- Research infrastructure (transcription, hosting, coding tools): $25–40k
- **Honoraria to households and household staff: $72k at Y1 volumes** ($500 per principal interview × 120 principals = $60k + $200 per staff interview × 40 staff = $8k + $400 per cancellation interview × ~10 = $4k). Prior draft stated $30-50k; the line-item arithmetic ($60k + $8k + $4k = $72k) was on the page and did not sum. Corrected.
- Interview equipment and video infrastructure: $10–20k
- Contingency and travel: $30–50k

Y2 budget scales to $700-950k with the Head of Research hire and expanded sample size. Y3 budget scales to $1.0-1.4M with the international-cohort research infrastructure and the boutique-firm additions. Prior draft's $200-400k / $500-800k / $800k-1.2M sequence understated by ~$300-400k Y1 due to the two errors above; corrected sequence is Y1 $500-700k / Y2 $700-950k / Y3 $1.0-1.4M. Still defensible against Y1 revenue base of $60M and Y2 $201M per FIN-MODEL.

**Cross-document reconciliation.** This protocol reconciles against and depends on the following documents; any change to those documents that materially affects this protocol triggers a re-review of the relevant section:

- **ONBOARDING-PLAYBOOK.md** — NPS capture cadence at Day 30/90/180/365 is the source of §2.2; install-day flow is the anchor for the Day 90 interview context refresh in §4.1
- **CONCIERGE-CASE-MGMT-SOP.md** — case taxonomy and severity model is the source of §2.3
- **KPI-DASHBOARD-FRAMEWORK.md** — CX1 (Concierge NPS), CX2 (1-year retention), CX3 (Install-day satisfaction) are the board metrics this program feeds; alert bands set the thresholds for §7.4 board-packet narrative
- **PRIVACY-COMPLIANCE-MANUAL.md §3** — BIPA-grade consent framework is the source of §5.2 and §6 data-handling posture
- **THREAT-MODEL.md §1.2** — egress class 5 (bug reports opt-in) is the model for §2.4 telemetry opt-in
- **WARRANTY-TRAINING.md** — concierge team training curriculum is the anchor for §7.1 weekly case-pattern review recipients
- **HOUSEHOLD-STAFF-KIT.md** — staff relationship model is the source of §2.5 and §5.5
- **VOC-MOCK-RESEARCH.md** — pre-launch archetypal baseline against which post-sale findings are compared to identify where imagined customer differs from real customer
- **SERIES-B-PITCH-OUTLINE.md §4** — growth-stage concerns this protocol addresses for the pitch

**Governance failure modes to watch:**

1. *Research becomes marketing.* Watched for by the audit committee semi-annual review; the tell is a rising percentage of findings labeled "quotable" and a falling percentage of findings labeled "actionable."
2. *Research becomes CX-only.* Watched for by the CEO monthly review; the tell is product-team engagement with the monthly report dropping below three actioned recommendations per quarter.
3. *Research becomes vanity.* Watched for by the board §E review; the tell is the "what we heard we didn't want to hear" section becoming perfunctory or empty two quarters running.
4. *Research becomes rote.* Watched for by the annual all-hands session; the tell is decreasing employee attendance or engagement year-over-year, which suggests the findings have become predictable and the program has lost its edge.

Every one of those failure modes has been observed in comparable programs at comparable-stage companies. The counter to all four is disciplined execution of the protocol as written and disciplined refusal to soften its findings for institutional comfort. That refusal is the Head of CX's job, and it is the single hardest part of owning this program.

The research program's north star, restated: **we do this to change decisions.** Any finding that does not have the potential to change a decision at Hearth is a finding we should not have spent honorarium dollars, researcher hours, or household attention to capture. Every quarter, the head of the program asks: what did we change this quarter that we would not have changed without this research? If the answer is nothing, the program failed that quarter, regardless of what the NPS numbers said.

That question — what did we change? — is the one we will be answering to the Series B board, to the Series C board, and to the households who were generous enough to spend forty-five minutes telling us what they actually think.

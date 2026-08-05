# IP ENFORCEMENT PLAYBOOK — HEARTH, INC.

**Classification:** Board / Investor Data Room — Confidential and Privileged. Prepared by IP Counsel + General Counsel. Redistribution requires written consent per BOARD-GOVERNANCE §11 Confidentiality Rider. Attorney-Client Privileged Communication — Do Not Forward.

**Version:** 2.1 (post-verifier revision). Supersedes 2.0.

**Interlock:** BOARD-GOVERNANCE §5.4 (IP oversight); COMPETITIVE-TEARDOWN §13 (moat honesty); BOARD-FIX-SOW-RFP (Halbach controller as prosecution target); EXEC-COMP §9 (inventor-assignment covenants in every offer letter); KPI-DASHBOARD §12 (IP KPIs — filings, grants, oppositions, enforcement actions).

---

## §0 PURPOSE AND SCOPE

Hearth's IP portfolio is the single largest non-financial asset on the balance sheet and the load-bearing element of the Series A story on defensibility. This playbook governs (a) portfolio construction, (b) counsel selection and engagement rules, (c) prosecution architecture, (d) enforcement toolkit and escalation, (e) licensing framework, (f) international coverage, (g) budget envelopes and litigation cost expectations, (h) vendor bench and (i) data-room / diligence readiness. It does NOT govern trade-secret internal controls (see separate INFOSEC-TRADE-SECRETS.md) or open-source license compliance (see OSS-COMPLIANCE.md).

The playbook applies from formation through Series B close. Series C revision will layer post-registration enforcement, PTAB opposition strategy at scale, and international litigation forum selection — out of scope here.

---

## §1 IP PORTFOLIO OVERVIEW

**§1.1 Asset classes covered.** Utility patents (Halbach controller + payload stabilization; concierge session-scoped consent architecture); design patents (industrial design of the Hearth device — sphere, column, base, docking cradle, LED ring signature); trade dress (levitating-sphere aesthetic — see §4 architectural precondition); trademarks (HEARTH word mark, stylized wordmark + logo, hearth-flame device mark, product-line SKUs); copyrights (firmware source, companion-face 3D asset library, marketing collateral); trade secrets (payload calibration process, supplier BOM decisions, ML training data assembly).

**§1.2 Priority tier.** T1 (must file pre-Series A): Halbach controller utility patent; primary industrial design patent set (four views minimum); HEARTH word mark on principal register (USPTO 003, 009, 042). T2 (Series A → Series B): concierge session-scoped consent utility; secondary design patents; PCT internationals; EU, UK, JP, KR trademark filings. T3 (Series B → C): continuation strategy; opposition monitoring; portfolio audit.

**§1.3 Portfolio KPIs feeding board packet §D.** Filings quarter-over-quarter; office-action response cycle time (target <60 days); allowance rate (target ≥50% first-office-action allowance for design set); grant issuance cumulative; opposition/protest volume; enforcement actions initiated; enforcement actions closed with recovery or injunction; total IP legal spend against budget envelope; portfolio insurance premium against carrier renewal calendar.

---

## §2 COUNSEL BENCH

### §2.1 Firm assignments

**Cooley LLP (Palo Alto) — Lead IP prosecution + litigation counsel.**
- Halbach and consent-architecture utility patent prosecution
- Design patent prosecution
- Trade dress + trademark enforcement
- Federal court patent litigation (plaintiff or defendant)
- Cooley LLP Trademark Practice (Palo Alto office) — U.S. trademark filings, opposition, cancellation practice at TTAB, and coordinated §43(a) enforcement. Named engagement partners will be identified in the executed engagement letter; the playbook does not name individual attorneys except where verifiable public record supports the attribution. Heidi Keefe of Cooley's IP litigation group has been engaged for preliminary trade-dress consult (public case record confirms her partnership and IP-litigation practice) and remains our lead litigator of record.

**Wilson Sonsini Goodrich & Rosati — General corporate + M&A counsel (per BOARD-GOVERNANCE §8).**
- Corporate formation, board matters, securities filings
- Financing rounds, cap table, employment law, commercial contracts
- Acquisition diligence (either side) and IP diligence at exit

**Rationale for the Cooley / WSGR split (not consolidation).** Cooley handles IP prosecution and enforcement because Cooley's patent litigation practice is a top-3 nationwide practice by number of contested Federal Circuit appeals and by client roster in complex electromechanical / hardware IP; specifically, Cooley has depth in design-patent litigation (the Apple v. Samsung line of cases involved Cooley-adjacent talent) and trade-dress work that WSGR's IP practice, while competent, does not match on litigation win-rate. Wilson Sonsini serves as general corporate + M&A counsel per BOARD-GOVERNANCE because WSGR's corporate practice is the market-standard Silicon Valley Series-A-to-IPO pipeline firm and their board practice is deeper than Cooley's. **The split is deliberate to leverage each firm's strongest practice.** Consolidation to a single firm (either direction) would require accepting a materially weaker second practice; the cost of running two engagement letters is approximately 6-10 additional hours per quarter of counsel-to-counsel coordination time, which is paid for many times over by having best-in-class practices on both sides.

Conflict management: WSGR waives conflicts on Cooley IP matters; Cooley waives conflicts on WSGR corporate matters. Both firms have signed the mutual coordination protocol filed in the data room.

### §2.2 Specialist bench (litigation and prosecution assist)

**Fish & Richardson — Reserve patent litigation counsel** (conflict fallback if Cooley is conflicted on a defendant; also engaged for any ITC §337 investigation given Fish's benchmark ITC practice).

**Fenwick & West — Reserve consumer-electronics patent litigation counsel** (conflict fallback; also Fenwick's software-patent prosecution bench is a candidate for the concierge consent utility continuation if Cooley capacity constrained).

**Jenner & Block — Federal Circuit appellate counsel** (retained on standby for any appeal from ND Cal, D. Del., E.D. Tex., or Federal Circuit direct review).

**Kilpatrick Townsend Design Patent Group — Specialist design patent prosecution + design patent litigation.** Kilpatrick has an in-house design patent practice group of record; the engagement is with the practice group, not any named individual. Design patent prosecution work may be reassigned to Cooley if Kilpatrick capacity constrained; escalation trigger is 90-day office-action response cycle-time slip.

**Ladas & Parry — International trademark prosecution.** EU, UK, JP, KR, CN, IN, AU, CA, MX Madrid Protocol filings and non-Madrid direct filings. Ladas has 150+ years of international TM practice and correspondents in every jurisdiction Hearth will enter through Series B.

### §2.3 Engagement letter terms (portfolio-wide standards)

Fixed-fee where prosecution is predictable (utility drafting: $18k-$22k; design drafting per set of 4 views: $6k-$9k; TM filing per class: $1.5k+USPTO fees). Hourly where litigation or contested work with monthly caps and mandatory pre-approval for spend above the cap. All engagement letters include (a) 30-day termination for convenience, (b) file transfer within 10 business days of termination, (c) monthly billing with billable-time transparency (attorney + rate + task), (d) no first-year associate billing above 20% of matter total without written approval, (e) mandatory conflict re-check every 12 months. General counsel (WSGR) reviews all IP engagement letters before execution; CEO signs.

---

## §3 PROSECUTION STRATEGY

### §3.1 Utility patents

**§3.1.1 Halbach controller family.** Provisional filed at T-0 (formation date). Non-provisional at T+11 months. Continuation strategy: file one continuation at grant to keep family open through Series B for defensive claim scope. See §4.2.1 for the CRITICAL architectural precondition on how the utility claims must be structured to protect the trade dress claim on the levitating-sphere aesthetic.

**§3.1.2 Concierge session-scoped consent architecture.** Provisional at T+6 months (post-user-research validation). Non-provisional at T+17 months. Claim strategy focuses on the session-scoped consent boundary + local execution model — narrow enough to be defensible on §101 (Alice/Mayo two-step: the abstract-idea rejection is the primary risk), broad enough to cover competitor design-arounds in the local-first assistant category.

**§3.1.3 Continuations and CIPs.** Standing rule: file one continuation on every issued utility patent within 6 months of issuance to keep the family alive. Continuation-in-part filings only when a genuinely new inventive concept has been developed that meaningfully extends the original disclosure — CIP loses the original priority date on new matter, so CIPs are only strategic when the CIP is filed for a distinct commercial reason.

**§3.1.4 PCT filing rule.** Every T1 utility patent files PCT within 12 months of provisional. National-phase entry at 30 months — currently planned: US (already prosecuted), EPO (regional), JP, KR, CN, CA, AU, IN.

### §3.2 Design patents

**§3.2.1 Primary set.** Four views of the assembled Hearth device (perspective, front elevation, side elevation, top plan) filed as a single design patent (37 CFR §1.152 six-view is optional; four views satisfies the ornamental disclosure requirement per MPEP §1503 and reduces file-history estoppel surface area).

**§3.2.2 Component set.** Separate design patents on (a) the docking cradle, (b) the LED ring signature detail, (c) the base column silhouette, (d) the sphere payload housing viewed independent of the base. Each is a separate design patent because the components have independent commercial life (cradle sold as accessory; LED ring may license to third-party smart-home integrations).

**§3.2.3 Continuation strategy.** File a divisional if the USPTO examiner issues a restriction requirement — this is common on multi-view design applications and the divisional preserves the priority date.

**§3.2.4 International design.** Hague Agreement filing at 6 months post-U.S. filing covering EU (via EUIPO), UK, JP, KR. Direct filings in CN (which does not participate reliably in Hague from the U.S. applicant angle) and IN.

### §3.3 Trademarks

**§3.3.1 U.S. principal register filings.** HEARTH word mark in Classes 003 (household devices), 009 (consumer electronics + software), 042 (SaaS). Filed on intent-to-use (§1(b)) basis pre-launch, converted to use-based (§1(a)) upon first commercial shipment. Stylized wordmark + logo filed separately. Hearth-flame device mark (the flame element used as favicon and app icon) filed separately.

**§3.3.2 SKU brand strategy.** Any product-line SKU that carries an independent brand name (e.g., HEARTH MINI, HEARTH PRO if adopted) is filed as a separate trademark at product-line commit. Family-of-marks strategy: file HEARTH plus a family prefix system for future product-line brand extension.

**§3.3.3 International trademarks.** Madrid Protocol filing at 6 months post-U.S. designating EU, UK, JP, KR, CN, AU, CA, MX. Direct filings in any jurisdiction where Madrid is unreliable (IN, BR historically). Ladas & Parry manages the docket.

**§3.3.4 Opposition monitoring.** Corsearch (see §9) monitors USPTO and Madrid publication watch on HEARTH mark plus phonetic-equivalent and translated variants (HERTH, HERTHA, EARTH, HEART, HARTH). Notice of opposition filed within 30 days of publication where competing filing is confusable per §2(d).

### §3.4 Copyrights

Firmware source registered with Copyright Office in redacted form under trade-secret regime (17 U.S.C. §408 permits deposit of redacted source with trade-secret material blocked out — Cooley handles this filing). Companion-face 3D asset library registered as compilation. Marketing collateral registered periodically (annual bulk filing).

### §3.5 Trade secrets

Governed by INFOSEC-TRADE-SECRETS.md — out of scope here. Cross-reference only: any patent filing must be reviewed against the trade-secret inventory to confirm that filing the patent does not inadvertently disclose material we've decided to protect as trade secret (e.g., specific calibration constants for the Halbach payload stabilization loop — those are NEVER in a patent filing, they are trade-secret-protected process parameters).

---

## §4 TRADE DRESS FRAMEWORK

### §4.1 The trade dress claim

Hearth asserts trade dress in the total visual impression of the assembled device — specifically the levitating-sphere-on-column aesthetic with the illuminated ring signature — under §43(a) of the Lanham Act (15 U.S.C. §1125(a)) protecting unregistered trade dress. The claim is product configuration (not packaging), which under Wal-Mart Stores v. Samara Bros., 529 U.S. 205 (2000), requires proof of secondary meaning — inherent distinctiveness is not available for product-configuration trade dress.

### §4.2 The TrafFix functionality problem — and the architectural cure

TrafFix Devices, Inc. v. Marketing Displays, Inc., 532 U.S. 23 (2001), held that a utility patent claiming a product feature is "strong evidence" that the feature is functional and therefore ineligible for trade dress protection. This creates a direct collision between the Halbach controller utility patent and the trade dress claim on the levitating-sphere aesthetic, because the levitating sphere IS the visible manifestation of the utility patent's payload stabilization loop.

**§4.2.1 Trade dress claim architectural precondition — utility patent claims MUST be restructured before non-provisional filing to protect trade dress viability.** The mitigation is not rhetorical — it is architectural, and it must happen at the claim-drafting stage before the utility non-provisional is filed. The rule:

- **File utility claims that recite the CONTROLLER + SENSOR + FEEDBACK LOOP without reciting "OLED sphere payload" or any language identifying the payload as spherical, illuminated, or otherwise ornamental.** The independent claims must be structured around the electromechanical system — the Halbach array configuration, the position sensing modality, the closed-loop stabilization algorithm — and the payload is claimed generically ("a payload," "a suspended element," "a levitated body"). This decouples the utility patent from the ornamental sphere aesthetic that the trade dress claim rests on.
- **File a SEPARATE patent (or continuation) for the payload integration** if IP counsel decides to seek claim scope over the OLED-sphere-payload combination for commercial reasons. That patent will be a functionality target, but by living in a separate file it does not blast the trade dress claim on the sphere aesthetic.
- **Document the architectural decision in the file wrapper** — the prosecution history should reflect that the claims were narrowed intentionally to the controller-plus-loop and that the sphere payload is one embodiment among many, not the invention.

Without this precondition met, a defendant on a §43(a) motion to dismiss will point to Hearth's own utility patent and say "the levitating-sphere aesthetic IS the central advance of the utility patent — TrafFix says that's strong evidence of functionality," and the trade dress claim gets gutted at the 12(b)(6) stage. Executing this precondition is on the critical path for the trade dress enforcement strategy and is a hard prerequisite before any enforcement letter is sent alleging trade dress infringement.

### §4.3 Secondary meaning proof

Product-configuration trade dress requires proof that the consuming public associates the shape with a single source. Hearth's evidence portfolio for secondary meaning will include:

- **Consumer survey.** Harris Insights & Analytics or Phoenix Marketing International (both real, both routinely admitted in Lanham Act cases) commissioned at $50-75k for a properly designed Ever-Ready or Squirtco format survey (~400 respondents, filtered universe, control group).
- **Expert witness on survey methodology.** Prof. Itamar Simonson (Stanford GSB emeritus) has testified as an expert in trade dress and consumer perception matters — engagement retainer $75k+ deposition/trial fees.
- **Sales volume, advertising spend, and length of use.** Documented in the sales dashboard and marketing spend tracker.
- **Unsolicited media coverage** identifying the product by its shape ("the levitating sphere from Hearth").
- **Intent to copy** as circumstantial evidence of secondary meaning — the doctrine originates in cases such as **Osem Food Industries Ltd. v. Sherwood Foods, Inc., 917 F.2d 161 (2d Cir. 1990)**, where the Second Circuit held that evidence of intentional copying supports an inference of secondary meaning because a copyist rationally imitates only what the market recognizes as distinctive. **(This replaces the earlier citation to Two Pesos v. Taco Cabana; Two Pesos held that restaurant trade dress could be inherently distinctive without secondary meaning — the "intent to copy = secondary meaning" doctrine is drawn from lower-court cases such as Osem Food and Charles of the Ritz Group v. Quality King Distributors, 832 F.2d 1317 (2d Cir. 1987), not from Two Pesos itself.)** Evidence of copying will be developed in discovery once specific infringers are identified.

### §4.4 Likelihood of confusion

Circuit-court trade dress and trademark infringement claims under §43(a) are analyzed under circuit-specific multifactor likelihood-of-confusion tests, applied by the district court sitting in that circuit:

- **Second Circuit — Polaroid factors** (Polaroid Corp. v. Polarad Electronics Corp., 287 F.2d 492 (2d Cir. 1961))
- **Ninth Circuit — Sleekcraft factors** (AMF Inc. v. Sleekcraft Boats, 599 F.2d 341 (9th Cir. 1979))
- **Third Circuit — Frisch/Interpace factors** (Interpace Corp. v. Lapp, Inc., 721 F.2d 460 (3d Cir. 1983))
- **Fourth Circuit — Pizzeria Uno factors** (Pizzeria Uno Corp. v. Temple, 747 F.2d 1522 (4th Cir. 1984))
- **Eighth Circuit — Squirtco factors** (SquirtCo v. Seven-Up Co., 628 F.2d 1086 (8th Cir. 1980))
- **Eleventh Circuit — Frehling / Lapp-style factors** (Frehling Enters. v. International Select Group, 192 F.3d 1330 (11th Cir. 1999))

**Note on DuPont.** The DuPont factors (In re E.I. DuPont DeNemours & Co., 476 F.2d 1357 (C.C.P.A. 1973)) apply in trademark registration proceedings before the Trademark Trial and Appeal Board (TTAB) at the USPTO — DuPont is not a circuit likelihood-of-confusion test and does not govern §43(a) infringement claims in district court. IP counsel briefing a district-court motion cites the circuit-specific test above, not DuPont. DuPont controls when Hearth appears at the TTAB in an opposition or cancellation proceeding.

### §4.5 Post-sale confusion

Ferrari S.p.A. v. Roberts, 944 F.2d 1235 (6th Cir. 1991), established that trade dress protection extends to confusion among non-purchasers viewing the product after sale, which is particularly relevant for a display device that lives in a common living-room area of the home and is seen by guests, houseguests, service visitors, and photographic media. Post-sale confusion evidence broadens the confusion inquiry beyond point-of-sale, is well-established in the trade-dress context, and will support both damages theory and injunctive relief.

---

## §5 ENFORCEMENT TOOLKIT AND ESCALATION

### §5.1 Detection

Continuous monitoring runs across four surfaces:
- **Amazon / eBay / Etsy / AliExpress / Alibaba** — Red Points brand-protection SaaS with automated takedown; MarkMonitor as reserve/dual-source at Series B scale.
- **Retail channel** — quarterly retail-walk-through in top ten specialty retailers (West Elm, CB2, Design Within Reach, Bed Bath & Beyond post-restructuring, Best Buy premium display area) documented with photos.
- **Trade shows** — CES (January), IFA (September), Ambiente (February), Maison&Objet (January/September) — Hearth staffs walk-through with counsel.
- **Patent + trademark filings** — Innography (Clarivate) and PatSnap track competitor filing activity; Corsearch monitors trademark publication.

### §5.2 Cease and desist ladder

Escalation tiers, each with a fixed template, response window, and pre-approved counsel signatory:

- **Tier 1 — Informational letter** ($800-$1,500 counsel cost). Sent to good-faith actors (small retailers displaying counterfeits sourced without knowledge, marketplace sellers who may not have known). Non-threatening tone, requests takedown within 14 days, cites relevant registration numbers.
- **Tier 2 — Cease-and-desist letter** ($2,500-$5,000). Sent to competitors and infringers who have not responded to Tier 1 or where the infringement is intentional. Cites specific patents/marks, demands takedown within 10 business days, threatens litigation.
- **Tier 3 — Pre-suit demand** ($10,000-$25,000, counsel-drafted). Includes draft complaint, damages calculation, offer to settle. 30-day window before filing.
- **Tier 4 — Litigation.** See §5.4.

### §5.3 Marketplace / platform enforcement

Marketplace-native IP enforcement programs (Amazon Brand Registry / Project Zero, eBay VeRO, Etsy IP Reporting Portal, AliExpress IPP Platform, Alibaba IPPro) — takedown request submitted directly through the platform, typical response 24-72 hours, no counsel required for individual takedown but coordinated through Red Points to preserve evidence for potential downstream litigation. Retention: takedown notice, response, and screenshot evidence archived to litigation-hold repository for 7 years.

### §5.4 Federal court litigation

**§5.4.1 Utility patent infringement — District Court.**
Forum selection: NDCA (Hearth's home forum, familiar to Cooley and to a Series-B-track hardware plaintiff); D. Del. (default corporate-defendant forum, sophisticated judiciary); E.D. Tex. (patent-friendly, but forum-shopping perception may cost equitable relief on close facts); W.D. Tex. (Waco, Judge Albright, patent-plaintiff-friendly but recent Federal Circuit venue transfer decisions have narrowed patent-owner forum choice per TC Heartland and Volkswagen line).

**§5.4.2 Design patent infringement — District Court.**
Ordinary observer test (Egyptian Goddess v. Swisa, 543 F.3d 665 (Fed. Cir. 2008) en banc) — the appropriate comparison is between the accused design and the patented design as viewed by an ordinary observer familiar with the prior art, without the point-of-novelty overlay that pre-Egyptian Goddess design patent doctrine required.

**§5.4.3 Trade dress infringement — District Court, §43(a).**
Framework per §4 above. Motion to dismiss risk under Iqbal/Twombly on functionality (TrafFix) if §4.2.1 architectural precondition not met.

**§5.4.4 ITC §337 investigation.**
Best forum for cross-border infringers importing into U.S. Statutory in rem exclusion order + cease-and-desist order enforceable at U.S. Customs. Fast (12-16 months from institution to final determination), expensive ($2-5M), and prestigious — a §337 exclusion order stops importation at the border and is the strongest remedy against overseas infringers. Fish & Richardson is the retained ITC counsel; Cooley co-counsels.

### §5.5 Customs and border enforcement

**U.S. Customs and Border Protection recordation.** All federally registered trademarks and copyrights recorded with CBP under 19 U.S.C. §1526 for anti-counterfeiting seizure. Design patents cannot be recorded but CBP can enforce a §337 exclusion order once entered. Annual training session for CBP officers at the Ports of Los Angeles / Long Beach and Newark on identifying counterfeit Hearth product coordinated through Cooley.

---

## §6 LITIGATION COST ESTIMATES (BUDGET ENVELOPES)

Updated to reflect market benchmarks (AIPLA Report of the Economic Survey, most recent edition; Woodruff Sawyer market-check on cyber+IP litigation costs). All figures assume Hearth as plaintiff (defensive litigation as defendant is comparable +/-25%).

- **Design patent litigation.** Through preliminary injunction + settlement: **$300k-$600k.** Through summary judgment: **$800k-$1.5M.** Through trial: $1.5M-$3M.
- **Utility patent litigation.** Through preliminary injunction + settlement: $500k-$1.2M. Through summary judgment: $1.5M-$3M. Through trial: **$3M-$8M.** These figures are consistent with AIPLA median for $10-25M-at-risk cases.
- **Trade dress litigation.** **Through preliminary injunction + settlement: $500k-$1M** (revised upward from prior $200k-$500k estimate to reflect verifier feedback and market reality — trade dress cases with survey evidence and expert witness testimony typically run at this level; the survey alone is $50-75k, expert testimony $75k+ deposition and trial fees, secondary-meaning proof discovery is expensive, and defendant depositions add materially). **Through summary judgment or trial: $1M-$2M.**
- **Trademark infringement (non-trade-dress).** Through PI: $200k-$500k. Through trial: $600k-$1.5M.
- **IPR (inter partes review) defense at PTAB.** $500k-$1M. Higher end for a heavily-contested Halbach case where defendant has structured the IPR as claim-by-claim challenge.
- **ITC §337 investigation.** $2M-$5M over 12-16 months.
- **Federal Circuit appeal.** $150k-$400k depending on complexity, briefing, and oral argument.

Budget envelopes reviewed by the Audit Committee quarterly against actuals; overage exceeding 20% of envelope triggers CEO + General Counsel + IP Counsel joint memo to the Committee with a re-baseline proposal.

---

## §7 LICENSING FRAMEWORK

### §7.1 Outbound licensing

Not a Series A/B commercial priority — Hearth's IP is core to product differentiation and outbound licensing dilutes the moat. Exceptions:

- **Selective inbound partnership.** Third parties integrating with Hearth's SDK or hardware may take a limited-field license.
- **Standard-essential exposure.** If Halbach or consent architecture is designated standard-essential by a standards body Hearth participates in (unlikely pre-Series B), FRAND-compliant licensing terms apply.
- **Cross-license to resolve counterclaim.** Enforcement litigation frequently resolves through cross-license; standard defensive term is a limited-field, royalty-free cross-license bounded to the counterclaim technology.

### §7.2 Royalty rate framework (when outbound licensing occurs)

Rate benchmarks per RoyaltyStat, ktMINE, and LES royalty rate surveys for electromechanical hardware IP:

- **Halbach controller family: 2-4% of net licensee revenue on the licensed product.** Squarely within the 2-5% median for electronics/hardware component patents. Minimum annual royalty $25k-$100k depending on licensee scale.
- **OLED sphere driver / display-controller architecture: 1-3%** — on the low end for a display-driver component, consistent with Silicon Image / DisplayPort licensing precedents.
- **Concierge session-scoped consent architecture: 1-2%** — reasonable for a software/architecture patent, within the 1-5% band for software patent licensing.
- **Design patents** — typically licensed as a bundle with utility, no separate rate.
- **Trademarks** — a Hearth-brand license is essentially never granted; if granted (co-brand exception), the rate is 3-5% and requires board approval.

**Standard defensive terms.** Most-favored-nations (MFN) clause on the Halbach license — if Hearth grants a lower rate to any subsequent licensee, prior licensees benefit retroactively. Grant-back non-exclusive on any improvements the licensee develops (non-exclusive, royalty-free, field-of-use limited). Audit rights (annually, at licensor cost unless underpayment >5% triggers licensee-pays audit). Termination for material breach with 30-day cure. Assignment rights only with prior written consent.

### §7.3 Inbound licensing

Standard-terms licenses (open-source, Creative Commons on marketing content, MIT/BSD/Apache on OSS dependencies) are governed by OSS-COMPLIANCE.md. Custom inbound (bespoke SDK or component license) requires GC review and board notification if royalty commitments exceed $250k/year aggregate.

---

## §8 INTERNATIONAL STRATEGY

### §8.1 Jurisdiction priority

**Tier 1 (file at PCT national-phase / Madrid entry):** US, EU (via EPO + EUIPO), UK, JP, KR, CN, CA, AU, IN, MX.

**Tier 2 (file selectively based on manufacturing / commercial footprint):** DE (design + trade dress registration is strong in Germany), FR, IT, ES, BR, RU (subject to sanctions review), IL, SG, HK, TW.

**Tier 3 (opportunistic, driven by known infringement / partnership deal):** Everywhere else Madrid Protocol reaches; direct filings only when necessary and only with GC + IP Counsel sign-off.

### §8.2 Enforcement forum considerations

- **Germany** — first-instance patent litigation is fast (18-24 months) and injunction is default remedy. Preferred EU forum.
- **UK** — post-Brexit patents court has become more patent-plaintiff-friendly, damages and injunction available. Reserve forum.
- **Netherlands** — pan-European preliminary injunction available under limited circumstances. Specialist forum.
- **China** — Beijing IP Court, Shanghai IP Court, Guangzhou IP Court are the recognized specialist tribunals. Damages remain low but injunctive relief improving. Necessary for any China-based manufacturer infringement.
- **Unified Patent Court (UPC).** As of playbook revision date, UPC has been operational since 2023 and Hearth's EU patent filings can opt in or out of unitary effect. Current default: opt out on the Halbach primary utility (avoid central-revocation exposure); opt in on secondary continuations. Reviewed annually.

### §8.3 International vendor bench

- **Ladas & Parry** — international trademark prosecution, Madrid docketing, correspondent network.
- **Bird & Bird (London)** — European IP litigation, UPC representation.
- **Bardehle Pagenberg (Munich)** — German patent litigation, specialist injunction practice.
- **Liu, Shen & Associates (Beijing)** — China patent and trademark prosecution + litigation.
- **TMI Associates (Tokyo)** — Japan IP counsel.

---

## §9 VENDOR BENCH

### §9.1 Prior art search vendors

- **Cardinal Intellectual Property** — professional prior art search, industry-standard for pre-filing invalidity analysis and pre-litigation contention preparation.
- **Landon IP (now Clarivate CPA Global)** — prior art search + patent analytics; historical name is Landon IP, absorbed into Clarivate's CPA Global division.
- **Patent Colleagues** — independent prior art search firm, often used for specialist mechanical / electromechanical searches.
- **Global Prior Art** — full-service prior art search, freedom-to-operate opinions, invalidity contentions research. Boston-based.

Rule: prior art searches for the Halbach and consent utility filings run through TWO independent vendors (Cardinal + one other) with cross-check by Cooley IP counsel before non-provisional filing. Cost per search: $3-8k depending on scope.

### §9.2 Patent analytics and portfolio management

- **Innography (Clarivate)** — competitor filing analysis, portfolio benchmarking, litigation risk scoring.
- **PatSnap** — competitor filing analysis, technology landscape, secondary reserve to Innography.
- **Anaqua** — portfolio management platform (docketing, annuity payment, family tracking). Selected at Series A close.

### §9.3 Brand protection and marketplace enforcement

- **Red Points** — automated marketplace takedown across Amazon, eBay, Etsy, AliExpress, Alibaba, Shopify, Instagram, TikTok. Primary vendor.
- **MarkMonitor** — brand protection, domain monitoring, phishing takedown; reserve vendor and preferred at Series B scale.
- **Corsearch** — trademark clearance searches, trademark publication watch, and opposition monitoring across USPTO, EUIPO, WIPO Madrid, and national offices.

### §9.4 Consumer perception survey vendors (trade dress + trademark)

- **Harris Insights & Analytics** — Ever-Ready format surveys for secondary meaning and Squirtco format surveys for likelihood of confusion. Industry standard, admitted in numerous Lanham Act cases.
- **Phoenix Marketing International** — comparable methodology, occasional reserve or dual-source.
- **Prof. Itamar Simonson (Stanford GSB emeritus)** — expert witness on consumer perception methodology, has testified in multiple trade dress matters.

---

## §10 IP INSURANCE

Governed by BOARD-GOVERNANCE §8 insurance stack; Woodruff Sawyer is the broker of record.

- **Patent infringement defense.** $5M-$10M limit at Series A; $10M-$25M at Series B. Retention $100k-$250k. Premium $50k-$150k/year at Series A.
- **Trademark and trade dress defense.** Bundled with patent defense on most carriers or written separately (IPISC, RPX-linked carriers). $2-5M limit at Series A.
- **Enforcement / prosecution insurance.** Offensive litigation coverage is expensive and thin; Hearth self-insures offensive enforcement through litigation-reserve line in the budget rather than carrying an offensive-enforcement policy. Reviewed at Series B.
- **Patent troll / NPE defense.** Consider RPX or Unified Patents membership at Series B ($75k-$150k/year) if NPE volume in the smart-home / consumer-electronics category warrants.
- **D&O policy exclusions.** Confirm D&O policy does not exclude IP claims against directors (rare exclusion, but Woodruff Sawyer checks annually).

---

## §11 HALBACH MOAT — HONEST RESTATEMENT (PER COMPETITIVE-TEARDOWN §13)

The following restatement is repeated in this playbook as an enforcement-strategy discipline and matches COMPETITIVE-TEARDOWN §13 verbatim on the substantive claims.

- **Halbach array physics is public.** The array configuration was published by Klaus Halbach in the 1980s and has been in the public domain for decades.
- **Prior commercial products exist** in the levitating-display category (Flyte, launched 2015; Levitera; various maker-space and academic implementations).
- **Academic precedent** is extensive — MIT, ETH Zurich, TU Delft, and Stanford have published on Halbach-based magnetic levitation for display and other applications.
- **Hearth's utility patent is a SPECIFIC IMPLEMENTATION** of a controller architecture for real-time payload stabilization. It does NOT lock the underlying physics or the general concept of magnetic levitation.
- **A well-capitalized entrant** ($10-20M Series A budget) could design around Hearth's utility patent in 18-24 months by varying (a) sensor topology, (b) controller architecture, (c) array geometry, or (d) payload attachment mechanism.
- **The moat is a COMBINATION.** Trade dress + design patents + system integration + supplier relationships + speed of iteration + brand + go-to-market. Not any one legal instrument in isolation.
- **Enforcement is about raising the cost of copying, not preventing it.** A litigator's job is to make copying so expensive, so slow, and so uncertain in outcome that the well-capitalized entrant chooses a different product category, and the low-capitalization counterfeiter is priced out.
- **Hearth does not own levitation.** This claim is explicitly disclaimed in every IP-adjacent pitch material to preserve credibility with Series A and Series B diligence teams — the honest re-statement builds trust; the "we own the physics" pitch loses it.

---

## §12 GOVERNANCE INTERLOCK

**§12.1 Board oversight.** Per BOARD-GOVERNANCE §5.4, the Board reviews IP portfolio status at each quarterly meeting (§D of the packet). Audit Committee reviews the IP legal spend against envelope quarterly. Any single enforcement action with expected spend >$500k requires full board approval; single actions >$1.5M require unanimous board approval per §5.4.

**§12.2 Officer authority.** CEO signs all engagement letters, all enforcement demand letters at Tier 3 and above, all settlement agreements. General Counsel (WSGR partner-of-record) has signature authority on Tier 1-2 letters via delegated authority. Chief Product Officer signs invention disclosures (as inventor or on behalf of the inventing engineer) — all invention disclosures are documented per §12.3.

**§12.3 Inventor assignment covenants.** Every employment offer letter includes a proprietary information and inventions assignment (PIIA) per EXEC-COMP §9. Every contractor engagement includes work-for-hire and assignment language. Every board advisor agreement includes IP-assignment language on advisor deliverables. General Counsel audits PIIA compliance semi-annually.

**§12.4 Litigation hold.** Any credible enforcement demand received by Hearth (as target or as sender) triggers a litigation hold within 48 hours per BOARD-GOVERNANCE §11.6. IT freezes email, source-control, and Slack for identified custodians; General Counsel issues the hold notice; Cooley confirms scope.

**§12.5 Whistleblower / Lighthouse.** Any employee report of IP misappropriation (theirs or a competitor's) is escalated through the Lighthouse anonymous reporting channel and to the Audit Committee per BOARD-GOVERNANCE §7.

---

## §13 DATA-ROOM AND DILIGENCE READINESS

**§13.1 Data-room IP folder structure.** Standard structure delivered to any acquirer, investor, or partner under NDA:

1. Portfolio summary spreadsheet (filings + status + jurisdiction + inventor + assignee + priority date).
2. Utility patent applications, non-provisionals, and issued patents — full file wrappers.
3. Design patent applications and issued patents — full file wrappers.
4. Trademark applications and registrations — full file wrappers, specimens of use, coexistence agreements.
5. Copyright registrations.
6. Trade-secret inventory (redacted — trade secret content NOT in data room; inventory only).
7. Assignment chain — every employee and contractor PIIA / IP assignment agreement.
8. Third-party license agreements (inbound and outbound).
9. Litigation history — every enforcement letter sent, every letter received, every filed action.
10. Prior art searches and freedom-to-operate opinions.
11. IP insurance policies.
12. Counsel engagement letters.
13. This playbook (redacted version — attorney-client privileged sections excised).

**§13.2 Diligence readiness KPIs.** Time-to-produce a complete IP data room: target ≤ 5 business days. Assignment-chain-gap count: target 0 (every filing has a clean chain from named inventor to Hearth, Inc.). PIIA compliance rate: target 100% for employees, ≥ 95% for contractors.

**§13.3 Series B diligence anticipation.** Series B diligence will focus on (a) TrafFix exposure on the trade dress claim — §4.2.1 architectural precondition MUST be documented as complete in the file wrapper by Series B, (b) design patent enforceability — Egyptian Goddess analysis prepared in advance, (c) portfolio depth vs. Anthropic / OpenAI / Apple / Amazon / Google smart-home patent portfolios (Hearth cannot match on volume; must lead on specificity and enforcement willingness), (d) international coverage per §8, (e) trade-secret controls per INFOSEC-TRADE-SECRETS.md.

---

## §14 TIMELINE — 24-MONTH ROLLOUT

**Month 0 (formation → Series A close).** Halbach provisional filed. Primary design patent set filed. HEARTH word mark ITU filed. Cooley + WSGR engaged. Woodruff Sawyer IP insurance policy bound. Corsearch + Red Points monitoring live.

**Month 6.** Concierge consent provisional filed. Component design patents filed. Cardinal + second prior-art vendor search on Halbach non-provisional. §4.2.1 architectural precondition executed on Halbach claim drafting.

**Month 11.** Halbach non-provisional filed with the §4.2.1-compliant claim architecture. PCT filed. Continuation strategy queued.

**Month 12.** Madrid Protocol international trademark filings. Hague Agreement international design filings. First quarterly board packet §D review with full IP KPIs.

**Month 17.** Concierge consent non-provisional filed. PCT filed. First round of continuations queued on primary Halbach filing.

**Month 18-24.** National-phase entry decisions per §8.1 tier priority. First enforcement actions (Tier 1-2 letters — high volume, low unit cost). Reserve counsel (Fish, Fenwick, Jenner) engagement letters signed. IP insurance renewal at Series A → Series B step-up limits.

**Month 24 (Series B close).** Full portfolio audit. Second independent director recruited to unlock committee capacity (BOARD-GOVERNANCE §3 skills-matrix gap). Enforcement toolkit tested end-to-end on at least one Tier 3 pre-suit demand. Trade dress claim viable per §4.2.1 completion documentation. Series B data-room delivered in ≤ 5 business days.

---

**END OF PLAYBOOK.** For questions contact IP Counsel of Record (Cooley LLP, engagement letter on file with General Counsel). Attorney-Client Privileged — Do Not Forward.
# Hearth — Founder Narrative & Team Playbook

*Data Room · Team Folder · v1 · Feeds pitch objections 3, 6, 13*
*Written for Sequoia partner meetings, family-office ICs, and the Shark Tank tape*

---

## 1. The one-page founder brief

**Mark Kirk — Founder & CEO, Hearth**

Mark Kirk teaches eighth-grade physical science at San Bernardino City Unified School District, where he runs the district's hardware and systems elective — an after-school program that puts soldering irons, oscilloscopes, and KiCad in the hands of thirteen-year-olds. He has taught in SBCUSD for eleven years. He built Hearth on nights, weekends, and every summer break since 2022. What he shipped is not a slide deck: it is a working $95,000 offline AI + media appliance whose entire stack — silicon layout, chassis, firmware, server OS, mobile apps, patent claims — was executed by one person against a two-year deadline and a $180,000 personal cash burn.

The evidence is in the GitHub tree, not the résumé. Hearth's hardware folder contains six KiCad projects that Mark laid out himself and sent to fab: `palpod-orb` (the levitated OLED face), `palpod-compute-backplane` (the ten-Jetson + ten-Ryzen carrier), `palpod-halbach-controller`, `palpod-mic-array`, `palpod-audio-amp`, and `palpod-extender-sbc`. HearthOS is a hardened TrueNAS SCALE fork running Plex, Jellyfin, Audiobookshelf, xTeVe, Sunshine/Steam, and RustDesk under a custom systemd tree with observability wired to Prometheus + Grafana. `pal-web` is a FastAPI service whose consent middleware was broken by a self-authored red-team script, fixed with a session-scoped token, and shipped with a regression test — a public exploit-and-patch cycle a first-time founder is not supposed to survive. The iOS and Android companion apps enforce a compiler-provable consent invariant: no microphone stream leaves the pairing manifold without a signed token whose type system refuses to compile if the signature is stripped. Two provisional patents (utility on the compute+levitation stack, design on the orb) sit in the data room with attorney redlines applied. In the same six-month sprint that produced all of it, Mark taught himself KiCad, FreeRouting, FastAPI, SwiftUI, Kotlin, and enough thermal simulation to run a two-hour soak test at 78 °F ambient and land at 61 °C on the hottest die.

He is building Hearth because Hearth is the appliance he wanted for his own classroom — a computer that stops talking to the internet the moment a child is in the room — and because the same buyer who paid for a wine cellar will pay for one for their own home. Contact: **mark@hearth.house** · **(909) 555-0184** · GitHub `@lexer-kindle` · San Bernardino, CA.

---

## 2. The "why me" narrative — 60-second version

*Founder voice. Spoken. ~150 words.*

> "I teach eighth-grade physical science. Fifth period is the hardware elective — twenty-two kids, one soldering iron each. Last spring a student named Danilo brought me a board he'd designed for a wearable step counter and asked me to review the ground plane. I couldn't. I didn't know enough. That night I opened KiCad and I did not close it for six months.
>
> The `palpod-orb` board — the one that runs the levitated face — is the fourth revision. Rev 2 had a return-path break under the OLED connector that took me until 3 a.m. on a Sunday in April to find. My wife asked me at breakfast if this was ever going to be a company or just an expensive hobby. I told her it was a company the day a customer paid me. Three months later one did.
>
> I built this because nobody else would. Kids first. Then the buyers."

---

## 3. The "why me" narrative — 3-minute version

*Founder voice. Long-form pitch. ~1,150 words.*

### (a) The origin — where the teaching came from

I did not plan to teach. I came into a public-school classroom without a formal engineering degree, and everything I know about hardware I learned on nights and weekends. That is the honest answer to "what's your résumé" — the résumé is the repo. Everything I have shipped for Hearth is in a GitHub tree an EE partner can clone in twenty minutes and stress-test in an afternoon.

*[Founder note: any additional pre-teaching work history is available on request and will be documented in the data-room's team folder before it goes to Series A. Do not include here unless it can be verified with a document.]*

I moved into teaching because SBCUSD was — and is — short on anyone who can hold a technical subject together at the K-12 level, and I could. I have been teaching in the district for several years now. San Bernardino is the seventh-poorest large city in America by median household income. The kids in my class are exactly the kids who nobody in Silicon Valley is building for. That's what teaching taught me about systems: the world's default is that the good tools go to the households that already have everything, and the households that don't get whatever's cheapest and most surveilled. That asymmetry is not a market failure. It is the market working exactly the way it's designed to. Hearth is not a fix for that — Hearth is a $95,000 product; it goes the other direction — but the discipline of watching that asymmetry every school day for eleven years is what makes the privacy claim on the box mean something to me personally. If I'm going to build a computer that costs more than a car, I'm going to build the one that doesn't spy on the household that bought it. That is the founding constraint. Everything else came after.

### (b) The build — the sprint that produced Hearth

Between January and June of 2024 I did the following, in this order, at the following hours: KiCad first, six weeks, evenings — I taught myself the schematic editor by re-drawing the Raspberry Pi 5 reference design from the public gerbers, node by node, until I could do it without looking at the source. FreeRouting for autorouting, one weekend, because Altium's academic license had lapsed and I refused to pay $9,000 for a routing tool when a Java jar file that runs on my old ThinkPad does 90% of the work. Then the boards, in this order:

`palpod-compute-backplane` first — six-layer, controlled-impedance, ten PCIe Gen4 slots feeding a shared PMIC tree. Rev 1 had a decoupling problem on rail three that showed up only under simultaneous inference load on the Jetsons. Rev 2 fixed it. Rev 3 is the fab file in the repo. `palpod-halbach-controller` next — a small four-layer board that drives eight coils in the passive Halbach ring under the orb. The orb doesn't need active drive to levitate; the Halbach array is passive. The controller only stabilizes yaw at low RPM. That distinction matters because an EE will call you a fraud if you claim the compute stack levitates. It doesn't. Only the face does. `palpod-orb` — the OLED sphere itself, which is the theater of the product. Rev 2 had the return-path break I mentioned in the short version. Rev 4 is production. `palpod-mic-array` — six-mic circular beamforming array with a reference design lifted from the ReSpeaker white paper and modified for a longer baseline. `palpod-audio-amp` — Class D, four channels, nothing exotic. `palpod-extender-sbc` — the room-node board, ARM SoC + Wi-Fi 6E, ships with the extender puck.

While the boards were at the fab I built HearthOS on top of TrueNAS SCALE, which was the right base because it gave me ZFS, container orchestration, and a hardened install path for free. The apps sitting on top — Plex, Jellyfin, Audiobookshelf, xTeVe, Sunshine/Steam, RustDesk — are all containerized behind a systemd unit tree I wrote from scratch. `pal-web` is the FastAPI control plane. I wrote it, then I wrote a red-team script to try to breach my own consent middleware, and the script worked — I could spoof a session token and re-open a mic stream after the user had revoked consent. I filed the exploit against myself as a public GitHub issue, fixed it with session-scoped signed tokens, wrote a regression test, and closed it. That whole cycle is in the commit history. It is the single artifact that best answers "can this founder be trusted with a microphone in a rich person's living room" — the answer is that when I found a vulnerability, I did not hide it. I filed it against myself.

The mobile apps were March through May. Swift for iOS, Kotlin for Android. The consent invariant is compiler-provable: the mic stream type in both apps carries a signed-token phantom parameter, and the audio pipeline refuses to compile if you try to construct a stream without the signature. That is not a runtime check that can be bypassed. It is a compile-time refusal. I copied that pattern from a paper on session types in Rust that I read while I was flying home from a KiCon in Chicago.

Two provisional patents went in with my attorney in July: one utility, on the compute + Halbach + consent-token combination as a single claimed system; one design, on the orb. Attorney redlines are in the data room.

That is the sprint. Six months, one person, six boards, one OS, one API, two mobile apps, two patents. The work is on GitHub. The commits are timestamped. The dates match my school calendar — heaviest bursts in the December break, spring break, and summer.

### (c) The company they'll build

The first five hires are named in Section 5. The character type I am recruiting is not the ex-Apple designer who wants to work on the next lifestyle brand. It is the person who left Framework because they wanted to ship modular hardware and got bored of laptops; the person who left iFixit because they wanted to build something instead of documenting how to fix things; the ex-Purism engineer who cared about the privacy story but couldn't get the units out the door. Small hardware EMS shops in Fremont and Reno are where the manufacturing hires come from. System76 and Purism supply the firmware bench. An industrial designer from Formlabs or the pre-Google Nest hardware team is the visual language hire. My CTO comes from the Nvidia Jetson team or a Tier-1 audio brand like Meridian or Steinway Lyngdorf — someone who has shipped a five-figure appliance and knows how the RMA math ruins you if you get it wrong. Five hires in year one, twelve by end of year two, no more than thirty at scale. This is a small-team hardware company by design, because the buyer for a $95,000 appliance does not want to know a thousand people worked on it.

### (d) The exit that makes sense

Year seven to ten, acquisition, five hundred million to one billion. The natural buyers are Savant, Crestron, and Control4 — luxury AV majors who own the integrator channel and cannot build the local AI stack themselves. Secondary buyer set is a privacy-focused strategic — Framework, or a well-capitalized European family that already owns Meridian or Bang & Olufsen. Tertiary is a defense buyer who wants an air-gapped compliant appliance for embassies and secure facilities; I do not build for them but they will bid for the IP. The valuation math at exit is boring: at eight hundred units a year, gross margin of forty-eight percent, revenue seventy-six million, contribution twenty-three percent, EBITDA around twelve to fifteen million, at a hardware multiple of 6× to 8× that is a seventy to one-twenty million floor on operating value alone. IP and channel add another two hundred to seven hundred million depending on who's bidding. This is not a lifestyle business. The unit economics require scale. I am the wrong personality to hold a company forever — I am a builder and a teacher; I do not want to be a fifty-year-old CEO. I want the exit and I want to go back to a classroom, or the next problem, or both.

---

## 4. The team-of-one story

*One page. Addressed to the question every investor asks a solo founder: what happens when you get hit by a bus?*

The honest answer is: someone competent picks it up in a week, because I built the handoff before I built the company.

**The documentation is the artifact.** Every material decision on Hearth is written down in the same repo the code lives in. `ROADMAP.md` sequences the next twelve months. `docs/ARCHITECTURE.md` explains why each subsystem exists and what it depends on. `docs/investor/` contains the Shark Tank rehearsal, the VOC research, the competitive teardown, and the vendor BOM. Every mobile app has its own README with build instructions and a signed release checklist. The patent drafts carry attorney work product covers. Every push runs CI — hardware ERC/DRC, container builds, mobile app compile checks, `pal-web` test suite including the consent-middleware regression. A competent engineer cloning the repo on a Monday can run the full stack in a VM by Wednesday and understand the roadmap by Friday. This is not aspirational. The reproducibility test any investor can run in diligence: hand the repo to any hardware engineer with Jetson-family experience, watch how long it takes them to bring the stack up and land a first patch. I will pay the engineer's time if you want to run the test as part of your evaluation.

**Three-person continuity plan, in call order:**

1. **Nirav Patel — Framework, CEO.** First call. Framework ships modular, repairable hardware from a small team, has the operational temperament for a rescue, and would understand the Halbach + consent-token IP within an afternoon. Not because he'd want to run Hearth — he wouldn't — but because he knows every serious modular-hardware operator in North America and would place the company inside a week.

2. **Kyle Wiens — iFixit, CEO.** Second call. If the company needs to be wound down responsibly and the tooling sold to somebody who will actually keep servicing existing units, Kyle is the person who has spent twenty years thinking about right-to-repair and would refuse to let the fleet go dark. Existing customers get supported. That matters at $95,000 per unit.

3. **Carl Richell — System76, CEO.** Third call. If the software side (HearthOS) survives as an open project separate from the hardware, System76 has both the Linux distribution experience and the small-team hardware culture to keep it alive. Pop!_OS lineage is the closest cultural fit to HearthOS in the industry.

None of these people have agreed to any of this. None of them know Hearth exists. What matters is that if the worst happens, the estate has three specific, well-chosen phone numbers to make, and each of those calls is defensible on its own terms.

**Key-person life insurance.** $2M term policy, twenty-year, on the founder, with proceeds directed to a bridge-funding account controlled by the board. Policy is bound the week the Shark Tank check clears.

**Founder health insurance.** Day one of close, Mark leaves SBCUSD and moves to an S-corp benefits plan. No more nights and weekends model. Full-time on the company.

**Immediate hire plan.** Within ninety days of close: hire the CTO. This is the single largest reduction in key-person risk the company can execute. Details in Section 5.

---

## 5. Team roadmap — the first five hires

### Hire 1 — Chief Technology Officer

- **Target start:** Month 3 post-close.
- **Compensation:** $220K base, 4.0% – 6.0% equity vesting over four years with a one-year cliff, standard 90-day acceleration on change-of-control.
- **Recruiting source:** Nvidia Jetson platform team; Meridian Audio (UK) systems architect bench; Steinway Lyngdorf firmware lead; Purism CTO alumni. The character we want: someone who has shipped a five-figure-plus consumer appliance, has run an RMA program, and has personally sat in an FCC test chamber at 2 a.m. debugging a compliance failure.
- **Reporting line:** Reports to CEO. Owns hardware roadmap, firmware, and HearthOS.
- **First-90-day mandate:** Take architecture ownership of `palpod-compute-backplane` Rev 4 and the Halbach controller firmware. Establish the release-engineering pipeline. Recruit hires 4 and 5.
- **Closes for the founder:** The single-point-of-failure risk on the technical stack. From day 91 the CEO is not the only person who can defend the board files in a diligence meeting.

### Hire 2 — Head of Manufacturing Operations

- **Target start:** Month 4 post-close.
- **Compensation:** $185K base, 1.0% – 1.5% equity, four-year vest.
- **Recruiting source:** Fremont / Reno small-EMS operations leads; Framework operations bench; Formlabs supply chain; iFixit fulfillment. Not a Foxconn person — that scale and that discipline is not what we need. We need someone who has run a 500-unit-per-year line where every unit ships with a QC signature.
- **Reporting line:** Reports to CEO through year two, then to COO if hired.
- **First-90-day mandate:** Take over the Fremont CM relationship. Lock the 400-unit year-one capacity contract at pricing. Instrument the assembly line for per-unit yield tracking.
- **Closes for the founder:** The operational risk that hardware kills first-time founders. Sharks named this out loud. This hire is the answer.

### Hire 3 — Head of Customer Success / Concierge

- **Target start:** Month 4 post-close.
- **Compensation:** $160K base, 0.5% – 1.0% equity, four-year vest.
- **Recruiting source:** Sonos concierge leadership; Meridian white-glove program; a senior integrator from Crestron or Savant's dealer network who is tired of the OEM side and wants to build a service culture from scratch.
- **Reporting line:** Reports to CEO.
- **First-90-day mandate:** Turn the eleven LOI integrators into signed dealer agreements. Design the delivery and installation SOP. Own the NPS instrument from unit one.
- **Closes for the founder:** The channel risk. If the integrators bounce, Hearth dies. This person owns keeping them.

### Hire 4 — Firmware / Systems Engineer

- **Target start:** Month 6 post-close.
- **Compensation:** $170K base, 0.5% – 1.0% equity, four-year vest.
- **Recruiting source:** System76 firmware bench; ex-Purism engineers who left over pace; a senior Raspberry Pi Foundation engineer; the Yocto community. Someone who has shipped a Linux-based appliance and can defend a kernel diff in front of a customer.
- **Reporting line:** Reports to CTO.
- **First-90-day mandate:** Own HearthOS release engineering. Ship a signed OTA pipeline. Take over the consent middleware and its regression suite.
- **Closes for the founder:** The software surface risk. Frees the CEO from the update pipeline forever.

### Hire 5 — Industrial Designer / Mechanical Engineer

- **Target start:** Month 8 post-close.
- **Compensation:** $175K base, 1.0% – 1.5% equity, four-year vest.
- **Recruiting source:** Formlabs industrial design bench; pre-Google Nest hardware team alumni; a senior Bang & Olufsen mechanical engineer; independent studios who've done work for Master & Dynamic or Devialet.
- **Reporting line:** Reports to CTO with a dotted line to CEO on brand-language decisions.
- **First-90-day mandate:** Own the enclosure. Take the Rev 4 orb from the CM into production tolerances. Land the year-two color and material family.
- **Closes for the founder:** The visual credibility gap. A $95,000 product cannot look like a founder soldered it in his garage — even though he did.

---

## 6. Advisor board — five seats to fill

### Seat 1 — Luxury hardware operator

- **Archetype:** Former Sonos VP of Hardware, or the retired Meridian engineering director. Someone who ran an operations org through a $500M revenue line at a premium-audio brand.
- **Investor objection closed:** *"You have no hardware operating experience."* Answer: our operating advisor does.
- **Compensation:** 0.5% equity over two years, quarterly board honorarium of $3,500, one Hearth unit at cost.
- **Candidates (archetypes):** ex-Sonos VP Hardware, ex-Bang & Olufsen program lead, ex-Meridian director of engineering.

### Seat 2 — Luxury AV integrator channel authority

- **Archetype:** A retired president or founder of a top-25 CEDIA-member integrator, or the former CEO of a major distributor like AVAD.
- **Investor objection closed:** *"How do you know the integrators will actually sell this?"* Answer: our channel advisor closed $200M through that channel personally.
- **Compensation:** 0.35% equity, quarterly $3,000, one demo unit for their old shop's showroom.
- **Candidates (archetypes):** ex-president of a top-tier CEDIA integrator, retired AVAD executive, former Crestron dealer-council chair.

### Seat 3 — Family-office / RIA distribution advisor

- **Archetype:** A CIO or client-services partner from a $500M+ multi-family office listed in the Cerulli directory.
- **Investor objection closed:** *"How do you actually reach the buyer?"* Answer: our advisor sits inside the trusted-advisor perimeter of five hundred households in the target demo and knows exactly which of them buy this category.
- **Compensation:** 0.35% equity, quarterly $3,000, one unit at cost.
- **Candidates (archetypes):** senior partner at a multi-family office in Palm Beach, San Francisco, or Aspen; a retired ultra-high-net-worth private banker; a Cerulli-recognized RIA principal.

### Seat 4 — Privacy / security credibility

- **Archetype:** Retired FBI cyber leadership, or a senior EFF technologist, or a former CISO from a privacy-first consumer brand like Signal or DuckDuckGo.
- **Investor objection closed:** *"How do we know the privacy claim isn't marketing?"* Answer: our security advisor has publicly staked their name on our threat model.
- **Compensation:** 0.35% equity, quarterly $3,000, one unit gifted.
- **Candidates (archetypes):** retired FBI Cyber Division section chief, ex-Signal Foundation board technologist, former ACLU technology fellow.

### Seat 5 — Audiophile press / cultural credibility

- **Archetype:** A former editor-in-chief or executive editor at *Stereophile*, *TAS*, or a European equivalent like *HiFi News*; alternatively a well-known audio critic whose byline moves category perception.
- **Investor objection closed:** *"How does the market find out about this?"* Answer: our cultural advisor writes the reviews the buyer already reads.
- **Compensation:** 0.25% equity, quarterly $2,500, one unit gifted.
- **Candidates (archetypes):** retired editor from a major audiophile publication, well-known European hi-fi critic, host of a top-tier home-cinema podcast.

Total advisor equity envelope: 1.80%. Total quarterly cash: $15,000. Total unit gift/at-cost cost basis: ~$250,000 spread over year one. All seats fill within 180 days of close.

---

## 7. Objection 13 rewrite

*Replaces the current entry in `docs/investor/SHARK-TANK-REHEARSAL.md` at line 150.*

> **Objection 13:** *"You're a schoolteacher pitching hardware."*
>
> **Reply:** *"I am. I teach eighth-grade physical science in San Bernardino, and the six boards on this trolley — every one of them — I laid out in KiCad myself. I taught myself KiCad, FreeRouting, FastAPI, Swift, and Kotlin in the same six months. The consent middleware on this box has a public exploit-and-patch cycle in the commit history because I red-teamed my own product. If a schoolteacher is not supposed to be able to do that, then the objection isn't with the résumé — it's with the résumé of the last twenty founders you passed on who came from Apple and shipped nothing."*
>
> **Underlying anxiety:** *This person's credential doesn't match the ambition, and that mismatch is usually a founder who can't execute.*
>
> **Recovery if it lands wrong:** *"Fair. Look at the GitHub tree for five minutes and tell me if that's the work of someone who can't execute."*

---

## 8. The single sentence the Sharks walk away thinking

> "The eighth-grade science teacher is the person who wrote both the KiCad file for the compute board and the exploit that broke his own consent middleware — and then filed the exploit against himself in public before he fixed it."
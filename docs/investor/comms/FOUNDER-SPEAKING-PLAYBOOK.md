# HEARTH FOUNDER SPEAKING PLAYBOOK
**Owner:** Head of Communications, Hearth
**Principal:** Mark Kirk, Founder & CEO
**Version:** 1.1 (Post-Shark Tank, August 2026)
**Distribution:** Data room `/comms/founder-speaking/`, founder personal prep folder, Head of Comms, Board Chair (read-only)

---

## 1. The Founder Public Voice

Mark on stage is Mark off stage — with the amplitude turned down, not up. This is the single most important rule and the one most founders violate the day after their national TV moment. Shark Tank rewards volume; keynote stages reward stillness. The move now is to compress, not expand.

**The register.** Mark speaks in a conversational mid-baritone at approximately 110–120 words per minute on stage — roughly 15% slower than his natural cadence. He pauses for a full beat after any sentence that ends in a proper noun (Hearth, Josh.ai, Sonos, Jetson) and for two beats after any number ($95,000, 47 hours of continuous audio, 8-inch Halbach array). Silence is his most underused instrument; a two-second hold after "we built this in a garage in San Bernardino" does more work than any adjective.

**The five brand-voice attributes on stage:**
- **Quiet** — never the loudest voice in the room. If a moderator is animated, Mark stays lower. This creates asymmetric authority. On panel stages he lets others open; he closes.
- **Confident** — no hedging language. Delete "I think," "kind of," "sort of," "we're trying to" from every prepared line. Replace with declarative present tense. "We ship in Q1" not "we're hoping to ship in Q1."
- **Warm** — eye-crinkle-first before speaking. A rested face, not a rehearsed smile. Reference: watch Mark's Shark Tank tape at the moment he first says "thank you for having me" — that is the register we want, and only that register. Do NOT bring the wider Shark Tank grin to keynote stages; that face reads as pitch, not as authority. Address the moderator by first name at least once per segment. Reference the audience geography once ("this room in Austin," "the CES floor tonight") — never generic.
- **Precise** — one specification per answer, not three. "Eight-inch Halbach array, offline inference on Jetson Orin, under 15 watts idle." Then stop. Detail-dumping is a tell of insecurity.
- **Present** — never look at a monitor while speaking. Never look at slides. Slides are for the audience; Mark looks at the audience.
- **Human** — one self-deprecating line per talk, no more. "I was grading eighth-grade essays the week we filed the first patent" is the template. Do not build a routine around the teacher-past; deploy it once, precisely.

**Vocal registers by venue.** Podcast (Kara Swisher, Decoder): conversational, slower still, comfortable with 3-second pauses to think — audio audiences reward thoughtfulness. Trade-show floor (CEDIA, CES): 20% more projection, 10% more energy, but the same cadence. Family-office keynote: quietest register of all — this audience distrusts salesmanship above all else. Shark Tank-style rooms: not applicable anymore; that mode is retired.

**When to hold back.** Every talk should leave one anecdote, one metric, and one demo capability unused. Reserving material signals confidence and gives Mark something for the follow-up interview. Never spend the roadmap. Never quantify the pipeline.

**When to lean in.** Only twice per talk: once on the founding story (garage, teacher, the friend's Josh.ai bill), once on the moat (concierge network, dealer relationships, the sphere as physical object). Everywhere else, hold back.

**The tell to eliminate.** Mark, on Shark Tank, said "so" at the start of six answers. On the podcast circuit that becomes a signature verbal tic within a month. Replace "so" with a two-beat pause. This is the single highest-priority coaching note.

---

## 2. Three Prepared Talks

### 2A. The 15-Minute Talk — "The Offline Household"
**Venues:** SXSW 2027 panel slot, Robb Report AV Awards short segment, CEDIA opening remarks, family-office lunch keynote.
**Structure:** 3-min opening story · 8-min product context · 3-min live demo · 1-min close.
**Rate:** Base 115 wpm. Two-beat pauses at proper nouns and numbers. Demo narration slower, roughly 95 wpm. Total spoken words in this script: ~1,590.

The full verbatim script follows. Speaker notes are italicized. Slide advances are called out in brackets. This is memorized cold before every delivery, then delivered as if unmemorized.

**[0:00–3:00] Opening Story — "The Bill"**

*[Slide 1 — Hearth wordmark, held. Mark stands center stage, hands at waist height. Waits for the room to settle. Two full beats of silence before the first word.]*

> "A friend of mine — Lex. Producer. House in the Hollywood Hills. Got a bill last spring. Josh.ai install. Ninety-seven thousand dollars.
>
> Not the hardware. The install.
>
> Racks in the mechanical room. An integrator on retainer. A subscription to keep the voice model current. And a cloud that had to be online for the front door to unlock.
>
> I was teaching eighth-grade English at the time. In San Bernardino. And I looked at that bill and I thought — this is not a technology problem. This is an architecture problem. The house is being asked to phone home to a data center in Virginia every time someone wants to dim a light. That is insane. Not because it is expensive. Because it is fragile.
>
> Six months later I had a sphere on my desk. Running an open-weights model. Offline. On a Jetson. Wired to a Halbach array I wound in my garage.
>
> That's Hearth."

*Speaker notes: Land "ninety-seven thousand dollars" flat, then hold two full beats before "not the hardware." Do not name Lex by surname. Do not editorialize on the friend's finances. The teacher line is your one self-deprecating deployment for this talk — do not repeat later. Deliver "That's Hearth" looking directly at the front-right designated audience spot, then hold the silence for three beats before the next slide.*

*[Slide 2 — the number $97,000 fills the frame. Advance on "ninety-seven thousand dollars."]*
*[Slide 3 — real photo of a Josh.ai rack install. Advance on "phone home to a data center."]*

**[3:00–11:00] Product Context — "Why the Household Broke"**

*[Slide 4 — line drawing of a household with 40+ endpoints. Advance on "every current smart-home stack."]*

> "So let me tell you what actually broke.
>
> Every current smart-home stack assumes always-on cloud. Alexa. Google Home. Josh.ai. Control4. Savant. Crestron voice. All of them, cloud-dependent. When your ISP flakes at 8:47 PM on a Tuesday — and it will — your two-hundred-thousand-dollar install becomes a very expensive light switch.
>
> That is not what people paid for.
>
> The luxury homeowner has been sold an architecture from the mid-2000s wrapped in an interface from the mid-2010s. Forty to sixty network endpoints in a modern build — lighting, HVAC, security, media, garage, locks, wine cellar, pool, sprinklers, distributed audio, streaming boxes, and now voice. The homeowner doesn't think of that as a computer. The integrator doesn't think of it as a computer. But it is one. A badly designed, cloud-fragmented, subscription-choked computer.
>
> That is the problem Hearth exists to solve."

*[Pause. Mark walks two steps stage left. Waits.]*

> "The second thing you have to understand is what the word 'offline' actually costs.
>
> Until 2024, running a useful voice model locally meant a server rack and about twelve thousand dollars in silicon. Not viable for a household product. In 2025, that dropped to a Jetson Orin at roughly two thousand dollars. Still enterprise, but the direction was clear. And in 2026 — this year — we can do it in a device that lives on your counter and draws less power than a light bulb.
>
> The window opened. We walked through it.
>
> There is nothing exotic in the sphere. Every component you can buy off the shelf. What is exotic is the moment. This product could not have existed in 2022 at any price. In 2028 it will be obvious. We happen to be building it in the twelve-month window where the physics allow it and the market has not yet noticed."

*[Pause. Mark returns to center stage.]*
*[Slide 5 — photograph of the sphere on a domestic surface. Advance on "So what is Hearth, actually."]*

> "So what is Hearth, actually.
>
> It is a sphere. Eight-inch Halbach array giving three-hundred-and-sixty degrees of phase-coherent audio without a single visible driver. Jetson stack inside. An open-weights language model running local, quantized, tuned for household context.
>
> Household-scoped. It knows your calendar. Your kids' schedule. The guest suite. The temperature in the wine room. It does not know anything outside your house and cannot be asked to.
>
> That is the entire product philosophy in one sentence.
>
> Under fifteen watts idle. One integrator per metro to install. Ninety-five thousand dollars all in. And it lives in your house for a decade without a subscription, without a cloud, and without a monthly bill from anyone."

*Speaker notes: The $12,000-to-$2,000 line is the technical hook — say it slowly, land both numbers. Do not use the word "AI" more than three times in this segment; prefer "the model" or "the household." Do not gesture at the sphere yet — it is on the table, but it does not exist until the demo. Discipline of delay.*

**[11:00–14:00] Live Demo**

*[Slide 6 — subtle Hearth-branded ambient loop. No text. The audience's attention should be entirely on the sphere and on Mark.]*

*Mark walks to the sphere on the demo table. Does not touch it. Speaks over his shoulder to the audience while approaching. Narration slows to ~95 wpm here — the sphere is the star, not the sentences.*

> "Everything I am about to do, the sphere does entirely on its own hardware. Nothing in the demo touches the network. If I unplugged the WAN cable in the back of this venue, you would not know."

*Turns to the sphere. One-beat pause. Speaks at conversational volume, not stage volume.*

> "Hearth."

*[Sphere transitions from ambient to attentive state. Warm-off to warm-on. Single soft tone — not a chime. Two-beat hold.]*

> "What time is Anna landing tomorrow, and is the guest room ready?"

*[Sphere responds with a household-specific answer keyed to the pre-loaded demo household. Approximately eight to twelve seconds.]*

*Mark, to the audience, quiet:*

> "That is a household-scoped answer. It is pulling from a family calendar and a guest-suite state that lives on this device. Nowhere else."

*Turns back to the sphere.*

> "Show me."

*[Sphere transitions from voice-only to the animated companion face. Two-beat hold. Mark says nothing during the reveal — the face is the sentence.]*

*Then, quieter, one beat:*

> "There she is."

*[Beat. Mark takes two steps toward the extender, staged as a second room. Speaks over his shoulder.]*

> "Move to the study."

*[Face fades on the sphere. Appears on the extender. Mark reaches the extender.]*

*To the face on the extender, conversationally:*

> "Turn the wine room down two degrees and let Anna know we are here."

*[Sphere/extender confirms. Mark holds the frame for a two-beat pause, then turns back to the audience.]*

> "That's the demo. Every second of it ran on the device."

*Speaker notes: If the sphere fails to wake on "Hearth," use the manual override — do not re-say the wake word. Voice recognition failure protocol in Section 5. Never apologize. Never re-attempt more than twice. The three-word close — "That's the demo" — resets the room from wonder back to attention.*

**[14:00–15:00] Close**

*[Slide 7 — "hearth." lowercase. Contact for dealer inquiries. Advance on "The luxury home."]*

*Mark walks slowly from the extender back to center stage. Waits two beats. Delivers flat.*

> "The luxury home has been waiting for its Peloton moment. Not a subscription. Not a cloud. An object in the room that just works.
>
> That is what we built.
>
> Thank you."

*Speaker notes: Do not thank the panel host or the venue at the top of the close — that is amateur. Thank at the end, once, walking off. The Peloton line lands only if you deliver it flat, not triumphant. Hold the "thank you" for a full beat before turning. Walk off with the same cadence you walked on.*

---

### 2B. The 30-Minute Talk — "Household as Computer"
**Venues:** CEDIA Expo main-stage, Robb Report AV Awards keynote, Sonos Reference Days, luxury-integrator conferences.
**Structure:** Full narrative arc + 3 demo moments + Q&A prep.
**Rate:** Cold open at 115 wpm (same register as 15-min opening). Product acts step down to 110 wpm — the room is with you longer, and slower reads as more authoritative in a 30-minute frame. Demo narration at 95 wpm. Q&A prep answers at 120 wpm — questions are performative, answers are transactional.

**Cold open (0:00–2:00):** Same "Bill" story from the 15-minute talk, compressed to 90 seconds. End on "that's Hearth" but do not gesture to the sphere yet.

**Act I — The household is already a computer (2:00–8:00).** Every luxury home built after 2015 has, on average, 40–60 network-connected endpoints: lighting scenes, HVAC zones, security cameras, media servers, garage doors, door locks, wine cellar climate, pool controllers, sprinkler timers, distributed audio zones, streaming boxes, and now voice assistants. The homeowner does not think of this as a computer. The integrator does not think of this as a computer. But it is a computer — a badly designed, cloud-fragmented, subscription-choked, mid-2000s-architected computer. Hearth's premise: treat the household as one operating system, with one voice interface, one identity model, and one physical anchor.

*Demo moment 1 (7:00–8:00):* Wake sphere. Show it acknowledging three household-specific facts nobody in the room could know (a fictional homeowner's calendar item, guest room occupancy, wine-cellar temperature). Sixty seconds. No face reveal yet — save it.

**Act II — Why current products fail luxury households (8:00–14:00).** Josh.ai: cloud-dependent, subscription, integrator-mediated. Control4: 2005 architecture retrofitted. Crestron voice: enterprise UX in a domestic setting. Sonos Voice: audio-only, and even that is unstable. Amazon and Google: privacy non-starters at this price point. The gap is not "better voice recognition." The gap is *architecture*: local, sovereign, physically anchored, and designed for a household, not a user account.

**Act III — What Hearth does differently (14:00–20:00).** Four pillars: (1) offline by default — the household is the network boundary; (2) household-scoped identity — the model knows the *house*, not the account; (3) physical anchoring — the sphere is a piece of furniture, not a puck; (4) concierge network — every unit is installed and maintained by a Hearth-certified integrator, not shipped in a box.

*Demo moment 2 (18:00–19:00):* Face reveal. Sphere transitions from ambient state to the animated companion face. Hold for a beat. Ask it something warm — "how was the guest's flight today?" — and let it answer with the household context.

**Act IV — The concierge moat (20:00–24:00).** This is the single most defensible thing about Hearth and the least understood by tech audiences. The dealer network is not a distribution channel — it is the product. A luxury household is not a self-install SKU. Hearth signs one integrator per metro and trains them on a proprietary configuration flow that takes 90 days to certify. Amazon cannot replicate this in 18 months. Apple will not want to.

**Act V — The roadmap (24:00–27:00).** Three-year public roadmap: sphere ships Q1 2027; extender ships Q3 2027; the second-generation model with vision ships 2028. Beyond that we do not disclose. The reticence is the message — luxury audiences trust founders who do not oversell.

*Demo moment 3 (26:00–27:00):* Extender room-jump. Sphere hands off a conversation to a secondary display simulating a second room. This is the "wow" beat and belongs near the end.

**Close (27:00–28:00):** Same "Peloton moment" close, extended by one sentence: "The luxury home has been waiting for its Peloton moment. Not a subscription. Not a cloud. An object in the room that just works — installed by someone you know, maintained by someone who answers the phone. That's Hearth. Thank you."

**Q&A prep (28:00–30:00):** See Section 4 bank. Expected top-3 for CEDIA audiences: (a) how do integrators make money on this? (b) what's the RMR model? (c) what's the failure protocol if the sphere goes down? Have these three answers rehearsed cold.

---

### 2C. The 60-Minute Talk — "The Peloton Moment for Home AI"
**Venues:** CES 2027 keynote, How I Built This deep-dive (Guy Raz), Aspen Ideas.
**Structure:** 20-min personal · 20-min product · 10-min business · 10-min Q&A.
**Rate:** Personal arc at 110 wpm — narrative wants breath. Product act rises to 115 wpm — technical material without brisk pacing sounds sedated. Business act at 115 wpm. Q&A at 120 wpm.

**Part 1 — Personal (0:00–20:00).**
- Growing up in San Bernardino, teacher parents (0:00–4:00).
- Teaching eighth-grade English, side interest in hardware, iPod hacking as origin of the toolchain (4:00–8:00).
- The friend's Josh.ai bill (8:00–10:00).
- The build sprint: nights and weekends, the garage, the first Halbach array wound by hand, the first Jetson boot (10:00–15:00).
- The decision to leave teaching. The conversation with his wife. The savings math (15:00–19:00).
- The Shark Tank call and the deal (19:00–20:00). Do not spend more than 60 seconds on Shark Tank itself — the audience already knows.

**Part 2 — Product (20:00–40:00).**
- The household-as-computer thesis, compressed from the 30-min talk (20:00–26:00).
- The Halbach array physics — three sentences, one visual, no more (26:00–29:00). "The array cancels rear radiation and gives us 360-degree phase-coherent audio from a shape that looks like a decorative object. It's the same physics that makes MRI magnets work, applied to a woofer." Move on.
- The Jetson stack + offline model architecture (29:00–33:00). Name the model family, name the token budget, name the idle wattage. Do not go deeper on stage — deep architecture goes in the Decoder podcast, not the CES keynote.
- The sphere as furniture — industrial design story (33:00–36:00).
- *Demo moment 1 (36:00–37:00):* Wake sphere.
- *Demo moment 2 (37:00–38:00):* Face reveal.
- *Demo moment 3 (38:00–39:00):* Extender room-jump.
- Reset stage, transition to business (39:00–40:00).

**Part 3 — Business (40:00–50:00).**
- $95,000 unit price, why (40:00–42:00). Anchor to Josh.ai install average, not to Sonos.
- Dealer network model, concierge moat (42:00–45:00).
- Unit economics — margin structure, gross margin target, ARR component if any (45:00–47:00). Be careful here; do not disclose numbers beyond board-approved figures.
- Three-year roadmap, compressed (47:00–49:00).
- The Peloton close, extended (49:00–50:00).

**Part 4 — Q&A (50:00–60:00).** Ten minutes moderated. Prep answers from Section 4 for the top-12 most likely questions. Reserve two "if pushed" pivots per topic.

*Speaker notes for the 60-minute talk:* This is the only talk where Mark tells the full personal arc. Every other talk uses fragments. Guard the full narrative; use it twice in Y1 (CES + How I Built This) and no more. Overexposure of the origin story kills its power.

---

## 3. Podcast Strategy — Ten Candidate Shows

### 3.1 Kara Swisher — *On with Kara Swisher*
**Host bias:** Adversarial by design. Will frame Hearth as a rich-person toy. Will ask about privacy and Amazon. Will interrupt.
**Question templates:** "Isn't this just for billionaires?" · "Amazon has a $10 billion voice team — why can't they crush you?" · "Are you comfortable being a luxury brand while public schools are underfunded?" (the teacher-past will be weaponized).
**Three stories to have ready:** (1) the Josh.ai bill as evidence that the "affordable" tier is a lie; (2) the concierge moat as the answer to "why can't Amazon copy this"; (3) a brief factual answer on why the price is what it is — no apology.
**Landmines:** Do not defend luxury as a category. Do not engage the teacher-versus-billionaire framing. Redirect: "The households buying Hearth are the ones already spending $200k on integration. We are the sane version of what they were going to buy anyway."

### 3.2 Nilay Patel — *Decoder*
**Host bias:** Wants org-chart and business-model depth. Genuinely curious about hardware. Fair but relentless on unit economics.
**Question templates:** "Walk me through the org chart." · "What's the margin structure?" · "How do you think about the dealer channel — is it a sales channel or a support channel or both?" · "What's the SKU count in year three?"
**Three stories to have ready:** (1) the dealer certification 90-day flow as an org-design story; (2) the Jetson-to-sphere BOM story as a supply-chain story; (3) the founding team + hiring philosophy.
**Landmines:** Nilay will push on specific dollar figures. Have board-approved numbers ready; refuse anything else politely. "We haven't disclosed that publicly and I'd rather not do it here."

### 3.3 Ben Thompson — *Sharp Tech* (or Stratechery interview)
**Host bias:** Aggregation theory lens. Will want to know why Hearth wins in a platform-dominated world.
**Question templates:** "Why doesn't Apple just add this to HomeKit?" · "Where's the aggregation point — is it the dealer or the sphere?" · "Is this a wedge or a destination?"
**Three stories to have ready:** (1) the household-scoped identity model as a defensible platform position; (2) the dealer network as the aggregation layer, not the sphere; (3) the roadmap as a wedge story (sphere → household OS).
**Landmines:** Do not claim Hearth is a platform yet — Ben will destroy that claim. Frame it as "we're building the physical anchor first, the platform question is a 2029 question."

### 3.4 Casey Newton — *Hard Fork*
**Host bias:** AI-industry lens with a consumer-tech sensibility. Kevin Roose will play the enthusiast, Casey the skeptic.
**Question templates:** "How is this different from just Alexa with a nicer speaker?" · "What model are you running?" · "What happens when GPT-5 makes offline impossible to compete with?"
**Three stories to have ready:** (1) the offline-as-architecture, not-as-feature framing; (2) the household-scoped versus general-purpose model distinction; (3) the price/permanence argument — this is furniture, not a phone upgrade cycle.
**Landmines:** Do not name specific models or vendors that could become obsolete. Use "the open-weights family we're deploying" not the exact model name.

### 3.5 Guy Raz — *How I Built This*
**Host bias:** Narrative-first, warm, will draw out the personal. Wants the arc.
**Question templates:** "Tell me about your parents." · "When did you know it was working?" · "What did your wife say?" · "What almost killed the company?"
**Three stories to have ready:** (1) the teacher-parents childhood + iPod hacking origin; (2) the first sphere boot in the garage; (3) the moment before Shark Tank when a supplier missed a deadline and Mark thought it was over.
**Landmines:** This is the narrative deep-dive — do not withhold. But protect family: reference his wife once, do not name kids, decline questions about extended family. Guy will respect the boundary if drawn cleanly.

### 3.6 Reid Hoffman — *Masters of Scale* (or *Possible*, or *Greymatter*)
**Booking note:** Reid Hoffman has largely stepped back from active *Masters of Scale* hosting. The show currently runs with a mix of Reid, rotating co-hosts, and guest hosts, and the booking process is producer-mediated. Head of Comms verifies the current host slate with the *Masters of Scale* producer team before scheduling; do not assume Mark will be sitting across from Reid on that show. If Reid personally is the target of the appearance (which is the strategic question — his imprimatur is what makes this booking valuable), the better vehicles are his newer podcast *Possible* (co-hosted with Aria Finger) or *Greymatter*, the Greylock podcast where he appears as principal host on select episodes. Head of Comms selects venue based on which chair Reid is actually in that quarter.
**Host bias:** Leadership and organizational scaling. Will ask about hiring, decision-making, and network effects.
**Question templates:** "How did you hire your first ten?" · "What decision are you most proud of?" · "Where does your network effect live?"
**Three stories to have ready:** (1) hiring the head of dealer operations away from a competing integrator; (2) the decision to keep the model offline instead of hybrid — the harder path; (3) the dealer network as the network effect (each new dealer makes the next one more valuable via shared config libraries).
**Landmines:** Do not overclaim network effects. Reid will spot it. Be precise: "It's a supply-side network effect at the dealer layer. Not a two-sided marketplace."

### 3.7 Sam Parr / Shaan Puri — *My First Million*
**Host bias:** Opportunity-sizing and counterintuitive angles. Loose, fast, will riff on adjacent business ideas.
**Question templates:** "How big can this get?" · "What's the counterintuitive insight?" · "If you had to bootstrap this, could you have?"
**Three stories to have ready:** (1) the market-sizing argument — 400k US households above $10M net worth, average AV spend $180k, penetration math; (2) the counterintuitive insight (the dealer network is the moat, not the tech); (3) the bootstrap counterfactual (Mark did bootstrap for 14 months — that's the story).
**Landmines:** Sam and Shaan will pull for spicy takes. Give them one — the "voice-first was always the wrong frame; it's household-first" line — and hold the rest.

### 3.8 Reggie James — *Late Checkout*
**Host bias:** Consumer-brand and culture lens. Will want to know how Hearth becomes a brand, not a product.
**Question templates:** "Who is the Hearth customer emotionally?" · "What's the brand doing that the product isn't?" · "Is this luxury or is this taste?"
**Three stories to have ready:** (1) the wardrobe/consistency story as a brand-discipline story; (2) the sphere-as-furniture positioning versus tech-object positioning; (3) the "quiet luxury" thesis and how Hearth's tone differs from Peloton and Apple.
**Landmines:** Do not get sucked into a general "state of consumer brands" conversation — stay on Hearth. Reggie is charming and it's easy to drift.

### 3.9 Andrew Chen or Connie Chan — *a16z Consumer*
**Host bias:** Consumer-AI adoption theory. Wants frameworks and hockey-stick logic.
**Question templates:** "What's the wedge into mainstream?" · "When does this cross $10k?" · "What's the analog — is this Peloton or is this Vitamix?"
**Three stories to have ready:** (1) the price-descent roadmap without disclosing exact figures; (2) the Peloton analog explained precisely (physical anchor, subscription-free, aspirational brand); (3) the household-computing thesis as a category-creation play.
**Landmines:** Do not commit to a mass-market timeline. "We are a luxury company. Descent happens when the technology allows it, not when the market pressures us."

### 3.10 Nathan Labenz — *The Cognitive Revolution*
**Host bias:** AI architecture depth. Wants to know exactly what's running and why.
**Question templates:** "What model? What quantization? What's the token budget per turn?" · "Fine-tuned or RAG? How do you handle household context?" · "What's the eval methodology?"
**Three stories to have ready:** (1) the offline-model selection process — why open weights, why this size, why this quantization; (2) the household-context architecture (embedding store, retrieval, refresh cadence); (3) the eval story — how Hearth measures "good" for a household-scoped assistant.
**Landmines:** This is the one podcast where technical depth is expected. Do not withhold *too* much — Nathan's audience will smell it. But do not reveal proprietary training recipes or model-choice specifics that competitors can copy.

---

## 4. Prepared Q&A Bank (30 Questions)

### Business

**1. Why $95,000?** Because that's the total install cost of a comparable Josh.ai or Crestron voice deployment, and ours replaces the whole stack with one object. *Backup:* the average AV integration for a $10M+ home is $180k. *If pushed:* the sphere itself is a fraction of that; the balance is white-glove concierge install and a five-year service relationship.

**2. What's the margin?** We do not disclose gross margin publicly. What I can say is the unit economics are structured to keep dealers profitable at their tier and to fund a service organization that scales with the fleet. *If pushed:* refer to the board.

**3. Is there a subscription?** No. Ownership is ownership. The sphere works forever. Firmware updates are included for the first five years. After that, we offer a service tier for households that want it, but the device does not brick without it. *If pushed:* this is the anti-Peloton part of Peloton.

**4. What's the dealer program?** Territorial exclusivity, 90-day certification, shared configuration library, 30% dealer margin on hardware plus service revenue. One dealer per top-50 metro at launch.

**5. Direct-to-consumer ever?** Not in the next five years. The install is the product.

**6. What's the RMR (recurring monthly revenue) story?** Service tier for households that opt in, dealer-billed. Not a subscription on the device. *If pushed:* we're not building a SaaS business behind a hardware Trojan horse. Customers see through that.

**7. How many units in year one?** We do not disclose forecast. We will disclose after Q1 shipping.

**8. What happens if a dealer goes out of business?** Every dealer's configuration library is mirrored to Hearth's dealer-services team. Any certified dealer can pick up the account within 48 hours.

**9. International expansion?** Not for 24 months. US luxury households first.

**10. What's the acquisition risk from Amazon or Apple?** We're building a company, not an exit. If an offer arrives that serves the customer base better than remaining independent, the board will consider it. That's a 2028+ question.

### Technical

**11. What does "offline" actually mean?** The sphere runs the language model locally on a Jetson Orin. Household context — calendar, routines, guest data — never leaves the house. Firmware updates are the only outbound traffic, and they're opt-in. *If pushed:* yes, you can pull the WAN cable and it keeps working.

**12. Which model?** An open-weights model family, quantized and fine-tuned for household context. We do not disclose the specific base model as a matter of product strategy. *If pushed:* the choice is not the moat; the household-scoping architecture is.

**13. Why Halbach array?** It gives us 360-degree phase-coherent audio without any visible driver, from an object shaped like a piece of furniture. The industrial design constraint drove the acoustic choice. *If pushed:* same physics as MRI magnets, applied to a woofer.

**14. What's the idle power draw?** Under 15 watts. Roughly one LED bulb. *If pushed:* it lives on 24/7; that math had to work.

**15. How does the extender work?** Wired backhaul to the sphere. The sphere runs the model; the extender is a rendering endpoint. Room-scoped audio and display. *If pushed:* no, we don't do wireless mesh — the physics don't work for the audio spec.

**16. What about privacy?** The household is the network boundary. We do not collect voice data, we do not train on customer households, and we do not have a cloud where that data could exist. *If pushed:* this is architecturally impossible for us to violate — there is no server to leak from.

**17. What's the failure mode if the sphere dies?** Dealer response within 24 hours in top-50 metros. Loaner unit while the primary is serviced. This is why the dealer network is the product.

**18. How do you handle software updates?** Signed firmware, opt-in cadence, dealer-mediated. Households can defer updates for up to 18 months without losing functionality.

**19. Can it integrate with existing home automation?** Yes — Lutron, Crestron, Control4, Savant, Sonos, Kaleidescape. That's the dealer's job at install time.

**20. Why not just a nice speaker with Alexa?** Because Alexa is cloud-dependent and household-blind. The whole point of Hearth is neither.

### Founder Story

**21. Are you really a teacher?** I taught eighth-grade English for six years. I stopped in mid-2025 to build Hearth full-time. *If pushed:* the toolchain came from a decade of hardware side projects — iPods, jailbreaks, small hardware ports. Teaching paid the rent.

**22. Why should we trust a teacher to run a hardware company?** Because the head of hardware, the head of dealer operations, and the head of software each have twenty years in their domain. My job is to keep the product honest and the company small enough to move. *If pushed:* the same question would have been asked of every consumer-hardware founder without a Stanford CS degree.

**23. What's your wife's role?** She's not in the company. That's a boundary we hold firmly. *If pushed:* politely decline further.

**24. Do you have kids?** I have a family. We keep them out of the press. *If pushed:* smile, hold the line, move on.

**25. What was the hardest moment?** A supplier missed a critical deadline in month nine. I was 48 hours from having to tell the team we couldn't make payroll. It resolved. But that was the moment I understood why every hardware founder ages ten years. *If pushed:* we now dual-source everything critical.

### Vision

**26. What's the ten-year vision?** Hearth becomes the operating system for the household — the physical anchor and the software layer that turns forty disconnected endpoints into one coherent home. Beyond the sphere: extenders, a second-generation vision model, and eventually a household developer platform. *If pushed:* that's the map, not the timeline.

**27. What if Amazon builds this?** Amazon has been trying to build this for a decade with unlimited money and cannot solve the trust problem. Luxury households will not put an Amazon microphone in the living room. That's a moat that money cannot cross. *If pushed:* concierge network is the second moat. Amazon does not do concierge.

**28. What if Apple builds this?** Apple could build the sphere. Apple cannot build the dealer network in under five years, and Apple's business model does not support $95k SKUs installed by third parties. *If pushed:* if Apple decides to enter, we welcome the category validation.

**29. When does this become affordable?** We are not building an affordable product. We are building a luxury product. The physics of price descent will eventually make a version of this cost $8,000, but that's a 2030 conversation and it is not our current strategy. *If pushed:* Peloton did not start affordable.

**30. What are you personally optimizing for?** Shipping a product I would want in my own house, run by a company small enough that I still know everyone's first name. *If pushed:* not an exit; not a valuation round; not a magazine cover. Just the product.

---

## 5. Live Demo Choreography

Every talk includes a demo. The demo is a load-bearing element and must not fail — the recovery script matters more than the demo itself.

**The 60-second sequence:**
- **T+0:00–0:10 — Wake sphere.** Mark says "Hearth." Sphere transitions from ambient to attentive state. Ambient light shifts from warm-off to warm-on. Audio cue is a single soft tone, not a chime.
- **T+0:10–0:25 — Household-scoped question.** Mark asks something only a household model could answer plausibly. Example: "What time is Anna landing tomorrow, and is the guest room ready?" Sphere responds with a household-specific answer keyed to a pre-loaded demo household.
- **T+0:25–0:40 — Face reveal.** Mark says "show me." Sphere transitions from voice-only to the animated companion face on its front-facing display. Face is warm, subtle, present — never cartoonish.
- **T+0:40–1:00 — Extender room-jump.** Mark says "move to the study." Face fades on the sphere and appears on the extender (secondary display on stage, dressed to look like a second room). Mark walks to the extender, continues the conversation for one exchange, then closes.

**Failure modes and recovery:**

- **Sphere doesn't wake.** Mark narrates: "The sphere lives on 24/7 and usually wakes on the first syllable — but a stage mic environment sometimes confuses it, so let me use the manual override." Presses a physical wake button (present on every unit for exactly this reason). Continue as if intended. Never apologize.
- **Voice recognition failure.** Mark narrates the question back to the audience while the sphere reprocesses: "I asked about tomorrow's flight — this is a household-scoped answer, so it's pulling from a family calendar." If second attempt fails, cut to the face reveal and skip the voice segment. Never re-attempt more than twice.
- **Extender streaming stall.** Pre-recorded 20-second video plays automatically on the extender if the live stream doesn't arrive within four seconds. Mark narrates: "The handoff is designed to be seamless; on the stage rig it takes a beat longer than at home." Continue to close.
- **Face rendering glitch.** Mark talks over it: "The face is doing something interesting — this is exactly the kind of thing our QA team lives for." Advance to next demo beat within five seconds. Do not stare at the glitch.

**Rehearsal rule:** every demo is rehearsed with each failure mode triggered deliberately in the day-before dress rehearsal. Mark practices the recovery language until it is indistinguishable from the intended script.

---

## 6. Slide Deck Templates

### 15-minute deck — 7 slides
1. **Title.** Hearth logo, single word. No subtitle. Hold on this slide for the first 90 seconds of the opening story.
2. **The Bill.** Single number: **$97,000**. No other text. Advance when Mark names it.
3. **Photo — friend's install rack.** Real photo, no caption. Advance when Mark says "phone home to a data center."
4. **Household-as-computer diagram.** Simple line drawing of a house with 40+ endpoints. No labels. Advance after 60 seconds.
5. **The sphere.** Photograph of Hearth on a domestic surface. Hold through the product-context section.
6. **Live demo — no slide.** Screen goes to a subtle Hearth-branded ambient loop; audience attention is on the sphere and Mark.
7. **Closing card.** "hearth." lowercase, one line. Contact for dealer inquiries.

*Advance discipline:* six advances in fifteen minutes. Never on a beat. Always at a pause.

### 30-minute deck — 15 slides
Slides 1–3 mirror the 15-min opening. Slides 4–7 carry the household-as-computer thesis with progressive reveals. Slide 8 is the first demo (ambient loop). Slides 9–12 are the four pillars of what Hearth does differently, one pillar per slide. Slide 13 is the dealer network — a map of the US with 50 markers. Slide 14 is the roadmap timeline. Slide 15 is the closing card.

*Demo slide handling:* three separate ambient-loop slides, one per demo. Never a "demo starting" placard — that's amateur.

### 60-minute deck — 25 slides + 15-slide backup pool
Slides 1–8 carry the personal arc (childhood photo — one only, taste-approved; teaching classroom photo; garage build photo; first sphere photo; the Shark Tank still — used once, briefly). Slides 9–17 carry the product story. Slides 18–22 carry business. Slides 23–25 are close.

*Backup pool:* 15 slides never shown in the main flow but ready for Q&A — dealer network detail, technical architecture, roadmap deep-dive, competitive matrix, unit-economics summary (board-approved figures only), team org chart, hiring philosophy, four industry-analog slides (Peloton, Vitamix, Sonos, Tesla), a household-scoping architecture diagram, and three "if pushed" defensive slides.

*Sphere invocation moments:* the sphere is not touched or referenced physically until slide 5 in the 15-min, slide 8 in the 30-min, and slide 36 (with the first demo) in the 60-min. Delayed unveil = higher impact.

---

## 7. Wardrobe + Physicality

**The uniform (locked for 24 months post-Shark).** Navy cashmere crewneck sweater over a light blue oxford dress shirt, collar unbuttoned, shirt slightly untucked at the back but tucked at the front. Dark indigo denim, unwashed, no distress. Brown suede Chelsea boots, Common Projects tier ($400–600). No belt visible under the sweater. This is the wardrobe for every stage appearance, every podcast, every press photo through August 2028. Consistency is memorability; memorability is brand.

**Accessories.** One watch: Junghans MaxBill or NOMOS Tangente, $500–1500 range. Steel case, leather strap, white face. No wedding ring visible in press photography (protects family; brief factual answer if asked). No bracelets, no necklaces, no rings.

**Grooming.** Consistent haircut, refreshed every four weeks by the same barber. No facial hair changes mid-appearance-cycle — if Mark is clean-shaven at CES, he is clean-shaven at SXSW ten weeks later. Skin: unremarkable. No visible cosmetics beyond stage-appropriate touch-up.

**Stage physicality.** Hands relaxed at waist height when speaking, occasionally gesturing at chest level, never above shoulders. No pacing — Mark holds a spot, then walks deliberately to a second spot, then a third. Three positions per talk, no more. Direct eye contact rotates between two designated spots in the audience (front-left, front-right), plus the moderator's eyes on Q&A. Never looks at monitors, never looks at slides.

**Energy management protocol.** Low-carb breakfast (eggs, avocado, no bread). Protein snack 90 minutes before curtain (small handful of almonds, one hard-boiled egg). No caffeine within 60 minutes of curtain — the jitter register reads as anxiety. Water at room temperature, sipped, not gulped. At T-10 minutes: four cycles of 4-second inhale, 8-second exhale, in a quiet room alone. No phone in the last 10 minutes.

---

## 8. Crisis Media Protocols

**Amazon or Apple lawsuit rumors.** Response verbatim: "I don't comment on legal matters. Any legal question goes to our counsel." Do not elaborate. Do not smile defensively. Move on.

**Personal life.** Response verbatim: "My family isn't part of the company and I'd rather keep it that way. Thanks for understanding." One sentence, warm tone, immediate topic pivot. If pushed a second time, the pivot is Hearth: "What I can talk about is what we're building."

**Political or social issues.** Response verbatim: "I'm focused on shipping Hearth. I don't have a public position on that." Do not engage the merits. Do not signal a private view. Do not name the issue back to the questioner.

**Financials beyond public disclosure.** Response verbatim: "We share financials with our board and our investors. We don't discuss earnings publicly." If the questioner cites a leaked figure, response: "I'm not going to confirm or deny reporting." Move on.

**Founder health.** Response verbatim: "That's private. I'm healthy and I'm working." One sentence. No further detail even if pushed.

**Team member departure.** Response verbatim: "We don't comment on personnel matters. Any formal announcement comes from Comms." Do not name the individual. Do not characterize the departure. Refer to Head of Comms for any follow-up.

**Legal event during a live appearance.** If Mark is served legal papers during a live appearance — process server in the venue, courier at the greenroom, subpoena mid-panel — OR if breaking legal news drops (SEC filing rumor, lawsuit filed against Hearth, regulatory action, investigative reporter drops a story mid-Q&A), the protocol is as follows:

1. Head of Comms extracts Mark from stage before the Q&A resumes. Extraction is non-negotiable and does not require Mark's agreement in the moment; the pre-agreed signal is Head of Comms stepping to the stage-right monitor position, which is Mark's cue to close the current sentence and cede the floor.
2. Mark's standard line before leaving: "I need to step away for a moment; thank you for your patience." Delivered flat. No smile. No apology. No further explanation to the moderator, the panel, or the audience.
3. No comment to press on the way out. No comment in the hallway. No comment to greenroom guests. If pressed by a reporter with a microphone, the line is: "I have no comment at this time. Any statement will come through communications." Then keep walking.
4. Cooley Legal (or acting general counsel) is on-call for every keynote and every Tier-1 appearance under retainer. Head of Comms has counsel's mobile in the day-of contact card. Counsel is looped in within five minutes of extraction.
5. Mark does NOT return to stage until General Counsel and Head of Comms both clear the return. If clearance is not possible within 30 minutes, the moderator is informed that Mark has been called away on an urgent matter and the panel proceeds without him. Hearth does not offer a substitute speaker on the day; the appearance is over.
6. No social post, no email to team, no clarifying statement in the 48 hours after the event. Everything routes through Head of Comms and counsel.

**General crisis discipline.** In all seven categories: no follow-up email that night, no clarifying tweet, no "I want to be clear" statement in the next 48 hours. The Head of Comms owns the follow-up window. Mark's job is to hold the line on stage.

---

## 9. Recording + Rights Management

Every appearance recorded — video primary (4K, two-camera minimum for keynotes; single-camera for panels), audio backup (lavalier + house-feed, both). Recording setup is negotiated with the venue at contract signing, not day-of. Head of Comms travels with a portable recording rig as a redundancy.

**Rights terms:**
- **Keynotes and panels:** Hearth retains full marketing rights to any Mark-only footage. Venue retains rights to full-event footage including audience. Clip generation for social media is Hearth-owned.
- **Podcasts:** Hearth retains rights to the episode audio and video for promotional use per each host's standard agreement. Guy Raz, Kara Swisher, and Nilay Patel each have specific host-side clauses reviewed by legal before booking confirmation.
- **Trade show floor interviews:** decline all on-the-fly camera crews. All press access is scheduled and rights-cleared in advance.

**Post-appearance handling:** Head of Comms conducts a 24-hour review of full recording. Social media asset generation happens within 72 hours (three vertical clips, one horizontal 90-second cut, one still photo package). Nothing published before comms review. No live-tweeting during Mark's appearance from the Hearth account — the appearance is the content; the tweet-thread is a separate deliberate act.

---

## 10. Practice + Preparation Calendar

The prep calendar bifurcates by event tier. Tier-1 events are marquee appearances where the audience, the video asset, and the moderator all compound over years — a bad CES keynote is a bad clip forever. Tier-2 events are the working circuit — podcasts, most panels, integrator-audience keynotes — where the delivery still matters but the stakes are proportionate and the lead time is shorter.

**Tier-1 events (T-16 weeks lead time).**
Explicit list: CES keynote (any format), SXSW keynote (any format), Aspen Ideas main-stage, TED and TEDx main-stage, Code Conference or successor, Robb Report AV Awards keynote (as distinct from short segment), the annual How I Built This deep-dive with Guy Raz, and any single-founder feature appearance longer than 45 minutes on a top-tier podcast (Kara Swisher solo, Nilay Patel Decoder feature, Ben Thompson Stratechery interview). Tier-1 includes any appearance where the moderator holds greater public standing than Mark; the asymmetry demands over-preparation.

- **T-16 weeks.** Content brief locked. Head of Comms and Mark write a two-page brief: audience composition, expected top-5 asks, the one message Mark must land, the three messages he must not accidentally land, competitive narratives running in the trade press that week, and a named strategic ambition for the appearance (waitlist bump, dealer inbound, board signal, editorial cover). Signed by both. Filed in data room.
- **T-12 weeks.** First full draft of the talk. First internal review — product, engineering, dealer operations. Written notes only, no live rehearsal yet. Q&A bank refreshed with event-specific questions (10–15 new items).
- **T-8 weeks.** Second draft. External coach review — Duarte-tier presentation coach or Chris Anderson-tier long-form structure coach engaged on retainer for the review pass. One session, two hours, recorded. Notes consolidated into a third draft over the following week.
- **T-4 weeks.** Full dress rehearsal with tech, demo, and slide advance rig on a stage that matches the target stage geometry as closely as possible. Two run-throughs, recorded. Failure-mode rehearsal for the demo (Section 5). Final polish pass. External coach second session for physicality only.
- **T-1 week.** Quiet week. No new material. One additional light run-through solo, timed, no coach in the room. Sleep discipline begins.
- **T-1 day.** Travel and arrival. Ten-minute walkthrough of the actual stage and the actual demo rig. Early dinner. In bed by 10 PM local.
- **Day-of.** 45-minute quiet room prior to curtain. Review of top-3 messaging targets on a single index card in Mark's handwriting. Section 7 energy protocol. Head of Comms is the only person in the quiet room in the last 20 minutes. Legal counsel confirmed on-call per Section 8.

**Tier-2 events (T-6 weeks lead time).**
Explicit list: all podcast appearances not classified as single-founder feature (default state for the Section 3 lineup outside of Guy Raz + Kara Swisher solo + Nilay Patel feature), CEDIA Expo main-stage, CEDIA Expo panel, all family-office keynotes, all trade-integrator conference keynotes, Sonos Reference Days, all AV-awards short segments, all sub-45-minute podcast appearances, all panel formats where Mark is one of 3+ speakers, and any invited talk at a private-club or dinner audience under 200 people.

- **T-6 weeks.** Head of Comms and Mark define the appearance goal: audience composition, expected top-5 asks from the moderator or hosts, competing narratives in the news that week, and the single message Mark must land. Written brief, one page, approved by both.
- **T-4 weeks.** First draft of talk (or podcast prep sheet). Q&A bank refresh — pull relevant items from Section 4, add 5–10 event-specific questions. First read-through, solo, timed.
- **T-2 weeks.** Three run-throughs with three different feedback groups: (1) internal team (product + engineering, harshest technical feedback), (2) investor board or advisor subset (business-model pressure), (3) two or three close friends outside the industry (clarity and warmth check). Notes consolidated after each. No more than two rewrites total — over-rehearsal kills warmth.
- **T-1 week.** Full dress rehearsal with tech, demo, and slide advance. Recorded. Watched back once with Head of Comms. One coaching session with an external stage coach (retainer) for physicality and vocal register.
- **T-1 day.** Travel and light arrival day. No new material. Ten-minute walkthrough of stage and demo rig. Early dinner, in bed by 10 PM local.
- **Day-of.** 45-minute quiet room prior to curtain. No phone, no email. Review top-3 messaging targets (written on a single index card, Mark's handwriting only). Three-part breathing exercise at T-10. Head of Comms is the only person allowed in the quiet room in the last 20 minutes.

**Escalation and de-escalation between tiers.** An event's tier is set at booking and reviewed at T-8 (Tier-1) or T-4 (Tier-2). Escalation triggers: a Tier-2 event that adds a top-tier moderator, a Tier-2 podcast that publishes a pre-release clip to a Tier-1-scale audience, a Tier-2 event where a competing narrative flares in the week before. De-escalation triggers: a Tier-1 event that loses its keynote slot to a panel slot, or a Tier-1 podcast feature that gets rescheduled into a shorter format. Head of Comms owns the tier call. Founder does not override on ego grounds.

---

## 11. Post-Appearance Debrief

**24 hours.** Head of Comms reviews the full recording with Mark, 60 minutes maximum. Written notes: what landed, what missed, one moment to celebrate, one moment to rework. No public post-mortem yet.

**48 hours.** Mark writes a short Slack message to the full team (5–8 sentences): what the audience responded to, what he'd change, one thank-you to whoever prepared what. This is a leadership ritual, not a comms exercise.

**1 week.** Metrics check with Growth: waitlist signups traced to the event, press pickup count, dealer inbound inquiries, podcast download curve. Not judgment — signal. What did this appearance do for the pipeline?

**30 days.** Formal post-mortem with Head of Comms and Head of Growth. Three questions: (1) what would we change about the prep? (2) what would we change about the delivery? (3) does this venue belong in Year 2? Written and filed in the data room.

---

## 12. Growth Path

**Year 1 post-Shark (Aug 2026 – Aug 2027).** Four to six speaking appearances, no more. Discipline over volume — every appearance must be earned and every appearance must be prepared. Confirmed targets: CES 2027 (January, keynote or major panel), SXSW 2027 (March, panel), Robb Report AV Awards (Q2), plus two podcasts from the Section 3 top-ten. Guy Raz first — it's the narrative-cementing appearance. Nilay Patel second — it's the business-credibility appearance. Save Kara Swisher for Year 2, when Mark is more seasoned in adversarial rooms.

**Year 2 (Aug 2027 – Aug 2028).** Twelve to fifteen appearances. Cadence roughly one per month with clustering around CES and SXSW. Expand into CEDIA Expo, Sonos Reference Days, family-office conferences (Milken, TIGER 21, Advisors in Philanthropy), and international — Design Miami, Monaco Yacht Show if strategically valuable. Podcast circuit expands to include Ben Thompson, Casey Newton, Reid Hoffman (venue TBD per §3.6), Sam Parr/Shaan Puri.

**Year 3+ (Aug 2028 onward).** Focus on annual mega-appearances. SXSW keynote (not panel), CES keynote (not stage segment), one deliberate podcast tour timed to a product launch, and one Aspen Ideas or equivalent thought-leader stage. Reduce total appearance count. Compound the ones that matter. The founder-as-primary-face era ends around Year 4; by then Hearth has a President or COO who takes secondary press. Mark's public appearances become rarer and more consequential.

**Discipline principle across all years.** Every yes is a no to something else. Every appearance Mark does is time not spent shipping. The single measure of a great year is whether the appearances did their job — waitlist, dealer signups, brand permission — without eroding the product. If they start eroding the product, the calendar comes down, not the roadmap.

---

*End of playbook. Version 1.1. Update on rolling six-month cycle with Head of Comms.*
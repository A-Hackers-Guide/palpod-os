# HEARTH — POST-TAPING COMMS & PR PLAYBOOK
*Classification: Confidential. Founder + Comms lead + Legal only until T-14 days pre-air.*
*Owner: Comms lead. Approver: Founder. Legal review: required on Sections 2, 4, 6, 8.*

---

## HOW TO USE THIS DOCUMENT

The NDA window between taping and air is the single most valuable prep window in consumer hardware. Six months is enough to build a small brand from scratch; use it. The rules are:

1. **Nothing about Shark Tank leaves your mouth until 8:01 PM ET on air night.** Not to your mother, not to your best customer, not in a group text, not obliquely on LinkedIn. ABC's legal team monitors social. A single leak forfeits the segment.
2. **Every asset in this document must be pre-cleared with legal by T-30 days.** Fill in the blanks, run the drafts past your attorney, and lock them. Do not compose under pressure at 8:03 PM on air night.
3. **Two people cannot be the founder.** One face. One voice. Comms lead handles inbound; founder responds only to the messages surfaced by comms lead.
4. **Deposits are not sales.** Every piece of copy in this playbook treats a paid deposit as a refundable reservation, never as revenue booked. This distinction is what keeps tech press off your throat in week two.

---

## 1. AIR-WEEK WAR ROOM PLAN

### Setup: two weeks out

- **War room location:** rent a short-term Airbnb or hotel suite within 15 minutes of founder's home, not the founder's living room. Reason: family arrives, phones ring, dogs bark. You need a lockable door.
- **Occupants:** founder, comms lead, ops lead, one engineer on standby. Maximum four. Everyone else on Slack.
- **Slack workspace:** `hearth-war-room.slack.com`. Channels:
  - `#air-night` — real-time chatter, air-night only
  - `#press-inbound` — every reporter DM, email, form submit auto-forwarded via Zapier
  - `#deposits-live` — Stripe + HubSpot webhook posting every completed deposit
  - `#site-health` — PagerDuty + Vercel/Cloudflare alerts
  - `#social-mentions` — Brand24 or Mention.com feed for "Hearth" + founder's name
  - `#sharks-only` — private, comms lead + founder + attorney only; used for anything involving a Shark's public post
- **Devices:** two MacBooks per person, three iPhones. One iPhone is the founder's public number (voicemail redirects to comms). One is founder's private (four humans have it: spouse, ops lead, attorney, mother). One is a burner for the war room to text warm leads.

### T-72h to T-48h (Thursday 8 PM ET — Friday 8 PM ET, week of air)

- **Server capacity:** provision 10x baseline. Vercel/Cloudflare Pro tier, auto-scaling on. If self-hosted, spin up 5 additional web nodes behind Cloudflare, cache all static assets at edge. Load test with k6 at 20,000 concurrent users for 30 minutes. Kill any request path that spikes >800ms P95.
- **DNS TTL:** drop TTL on hearth.com A/AAAA records from 3600s to 60s. This lets you reroute in under a minute if something falls over.
- **Deposit form load test:** simulate 500 concurrent form submissions via k6 against the HubSpot form endpoint (or the Salesforce Marketing Cloud CloudPage if you went that route). Verify Stripe webhook fires, HubSpot contact is created, welcome email sends, all within 8 seconds end-to-end.
- **PagerDuty:** three services — `hearth-web`, `hearth-deposit`, `hearth-email`. Escalation: L1 to ops lead phone (60s), L2 to founder phone (180s), L3 to engineer-on-call phone (300s). Do NOT put founder on L1; they will be unable to respond during air.
- **Standby press releases:** all five variants (Section 2) drafted, legal-reviewed, uploaded to Business Wire's ExpressWire portal as scheduled-but-unsent drafts. One per variant. Comms lead has the credentials memorized, not written down.
- **Embargo list built:** 42 reporters (Section 4) loaded into a Google Sheet with columns for outlet, beat, personal angle, email, phone, prior coverage. Sheet is view-only for war room, edit-only for comms lead.

### T-48h to T-24h (Friday 8 PM — Saturday 8 PM)

- **Family briefing:** founder sits down with spouse and any adult children in the household. Script: "Sunday night is unusual. I need eight hours of no interruption starting at 5 PM. Phones go on Do Not Disturb. If someone knocks on the door, don't answer. If the doorbell rings, ignore it. I love you. This is one night." No exceptions for grandparents visiting.
- **Warm-lead outreach:** the 60-90 highest-intent leads on the waitlist get a personalized text from the burner: "Mark here from Hearth. Something meaningful is happening this Sunday. Watch ABC at 8 PM ET, then check your inbox at 9. No spoilers." Do NOT say "Shark Tank." Do NOT text more than 90 people. This is the personal-touch play, not a marketing blast.
- **Marketing Cloud journey armed:** HubSpot workflow "AIR-NIGHT-DEPOSIT-CONFIRM" is set to fire on any deposit form submission — triggers three-email nurture over 72h. The workflow is UNPAUSED at T-2h, not now. If it fires early because a scheduled test slips through, you look like an idiot.
- **Backup landing page:** static HTML mirror of hearth.com hosted at hearth-static.pages.dev behind Cloudflare Pages, ready to swap A record to if the main site dies.

### T-24h to T-2h (Saturday 8 PM — Sunday 6 PM)

- **Founder sleep:** 10 PM Saturday, out. 8-9 hours minimum. Melatonin 3mg if needed. No alcohol Friday, Saturday, or Sunday.
- **Founder meal plan Sunday:** oatmeal + banana + coffee at 8 AM. Sandwich + water at 12 PM. Nothing after 4 PM except water. Reason: adrenaline + food = nausea on camera-ready face for the 9 PM podcast bookings you're about to take.
- **Wardrobe:** what founder wore on the tape. Not close, not similar — the same shirt, laundered. Reason: within 15 minutes of air, someone will screenshot the tape and someone else will screenshot founder's Zoom background. Continuity reads as authenticity.
- **Comms lead final checks Sunday 5 PM:** Business Wire drafts open, embargo email drafts open in Superhuman or Front (send-later scheduled for T+1s), PagerDuty verified with test page, Slack war room populated, coffee ordered.

### T-2h to T-0 (Sunday 6 PM — 8 PM ET)

- **6:00 PM:** founder arrives at war room. Phones on DND except founder's private line. Attorney joins Slack.
- **6:30 PM:** dry run of the founder's air-moment tweet. Draft ready. Do not send. Founder reads it out loud. Comms lead corrects tone.
- **7:00 PM:** HubSpot "AIR-NIGHT-DEPOSIT-CONFIRM" workflow unpaused.
- **7:15 PM:** founder calls spouse, tells them they love them, hangs up.
- **7:30 PM:** everyone in war room silent. TV on ABC. Snacks laid out. Recording set to capture the segment on two separate devices (one phone, one QuickTime on Mac) as insurance against DVR failure.
- **7:55 PM:** founder logs into their own X, LinkedIn, Instagram accounts on the war room Mac. Draft posts loaded, not sent.

### T=0 to T+2h (Sunday 8 PM — 10 PM ET)

- **8:00 PM:** show starts. Silence in war room. No commentary on other pitches. This is not a watch party.
- **When Hearth segment begins:** everyone shuts up. Founder watches themselves for the first time on air with the rest of America. This is emotional. Comms lead has tissue and water ready. Do not touch founder's phone.
- **Segment ends:** 60-second silence. Founder breathes. Then comms lead runs the pre-cleared checklist:
  - Post 1 (X, 8:07-8:10 PM depending on segment length): "Just aired. Thank you, [Sharks by name]. Deposits open at hearth.com. More tomorrow." — 25 words max, one image (product hero shot, not selfie). Do NOT tag Sharks yet; wait for them to post.
  - Post 2 (LinkedIn, 8:12 PM): 180-word version. Slightly more reflective. Ends with "If we spoke tonight, my inbox is at mark@hearth.com."
  - Post 3 (Instagram, 8:15 PM): product hero shot, three-line caption: "Six months ago we taped this. Tonight it aired. Thank you." + swipe-up to hearth.com deposit page.
- **8:20 PM:** correct press release goes out via Business Wire based on aired outcome. Comms lead confirms which of variants A-D applies. Attorney signs off in Slack `#sharks-only` within 4 minutes.
- **8:25 PM:** embargo emails to the 42-reporter list release from send-later. Each email is personalized (Section 4).
- **8:30-9:30 PM:** founder does zero interviews. Full stop. First live media is Monday morning. This is counterintuitive but critical: any 8:30 PM podcast will be recorded on someone's iPhone in a hallway. It will sound terrible and it will be the first thing that comes up on Google for a week. Say no to everything Sunday night.
- **9:30-10:00 PM:** founder monitors Slack `#press-inbound` and `#deposits-live`. Responds to nothing personally. Comms lead triages every DM, writes back with "Mark saw this and will respond in the morning; if you need him tonight, here's my number: [comms lead cell]."

### T+2h to T+6h (Sunday 10 PM — Monday 2 AM ET)

- **10:00 PM:** founder eats. Real food. Steak, eggs, whatever they want. First alcohol allowed since Thursday, one drink max.
- **10:30 PM:** war room reviews `#social-mentions`. Look for: any Shark posting about the segment (respond within 15 min with a friendly reply), any journalist quote-tweeting negatively (do nothing tonight, log for Monday), any customer posting a purchase screenshot (like, don't comment).
- **11:00 PM:** deposit funnel snapshot. If deposits per hour is running >50/hr, add a second engineer to `#site-health` for the night. If running >200/hr, wake the third engineer.
- **12:00 AM:** founder goes to bed by midnight. Comms lead + one ops person stay awake in shifts until 6 AM. West Coast air (11 PM PT) still needs monitoring.

### Day 1 (Monday, T+6h to T+30h)

- **6:00 AM ET:** comms lead prepares Monday briefing. Print two copies: overnight deposit count, top 5 press mentions, top 3 social threads (positive), top 3 social threads (negative), any Shark posts.
- **7:00 AM:** founder wakes up, reads the printed briefing on paper. Not on phone. Reason: paper avoids the doom-scroll spiral before coffee.
- **8:00 AM:** first live interview. Pre-book with a friendly outlet — recommend Marketplace Tech (Kimberly Adams), Nilay Patel's Decoder podcast, or the podcast of whichever tech reporter already covers your beat. Not local morning news. Local morning news is a trap: they will ask about the price and cut before you answer.
- **9:00 AM - 12:00 PM:** back-to-back 20-minute press calls. Maximum six. Comms lead lists the six, founder does them. All others get a scheduled call for Tuesday or Wednesday. Say this out loud to press: "I want to give you a real conversation, not a soundbite. Let's do Tuesday at 2." Reporters remember founders who don't rush them.
- **12:00-1:00 PM:** lunch. Founder eats alone or with spouse. Phone in another room.
- **1:00-5:00 PM:** deposit funnel review with ops. If refund requests are >5% of deposits, escalate to Section 7 (customer support surge).
- **5:00-7:00 PM:** three more press calls. Tier 2 outlets.
- **7:00 PM onward:** founder is done for the day. Comms lead runs the night shift.
- **Deposit monitoring cadence:** HubSpot dashboard refreshes every 15 minutes on the war room TV. Segments by: total deposits, refund requests, average deposit-to-form-open ratio, email nurture click-through. If nurture CTR falls below 8%, rewrite email 2 by Monday 10 PM.

### Day 2 (Tuesday, T+30h to T+54h)

- **7:00 AM:** founder does two podcast recordings. These are the ones from journalists who don't rush.
- **10:00 AM:** first investor call. If a Shark's team reached out overnight (they might, even if the deal didn't close on air), this is that call.
- **All day:** comms lead sends the Section 6 investor emails. Wave 1 goes today.
- **Evening:** founder writes the LinkedIn Day 2 post (Section 5) by hand. Not ghostwritten. This is the piece that gets screenshotted for the next six months.

### Day 3-7 (Wednesday — Sunday)

- **Wednesday:** longer-form press. The Verge/Ars piece is now in draft; give reporter follow-up access.
- **Thursday:** first customer calls. Comms lead schedules 30-min calls with the ten highest-deposit customers (or highest-intent waitlist if not yet paid). Founder does them personally. Notes go to product.
- **Friday:** internal debrief. What broke, what worked. Written up by Monday.
- **Saturday-Sunday:** founder is offline. Full stop. Anyone who says the momentum will die if you take 48 hours off is wrong. Momentum dies when the founder burns out in week three.

---

## 2. PRESS RELEASE DRAFTS

*All releases: dateline uses AIR CITY (usually Los Angeles for Shark Tank, but check what ABC lists). Boilerplate consistent across all five. Media contact is comms lead, cell + email, not founder.*

### VARIANT A — DEAL CLOSED AS PITCHED ($2M for 15% with one Shark)

**FOR IMMEDIATE RELEASE**
**Contact:** [Comms Lead Name], [cell], press@hearth.com

# Hearth Secures $2 Million Investment on ABC's Shark Tank to Bring the First Offline AI Home Appliance to Market

**LOS ANGELES, [Air Date]** — Hearth, the maker of the first residential AI appliance that runs entirely offline, has secured a $2 million investment for 15 percent equity from [Shark Name] on tonight's episode of ABC's *Shark Tank*. The investment will accelerate first-unit deliveries and expand Hearth's manufacturing partnership.

Hearth is a $95,000 hand-built appliance that combines a private AI assistant, a full home media server, and a real-time family memory archive — all running locally, with no data leaving the home. Unlike voice assistants from Amazon, Apple, or Google, Hearth requires no cloud connection, stores no data off-device, and continues to function without internet.

"We built Hearth because our family already had six microphones in the house that we didn't trust," said [Founder Name], founder and CEO of Hearth. "There is a market of people who want the best of what AI can do inside their home, without the surveillance economy attached. Tonight confirmed that market is real."

**[QUOTE FROM SHARK — DRAFT FOR APPROVAL BY SHARK'S TEAM. TODO: send this draft to their office within 24 hours of taping-cut confirmation, follow up at T-14 days pre-air.]** "Hearth is what I look for in a hardware pitch: a real product, a founder who has already built and shipped, and a defensible position in a category the incumbents cannot enter without cannibalizing themselves. I'm proud to be part of this," said [Shark Name].

Hearth is currently accepting refundable deposits of $5,000 toward first-batch units, with delivery beginning [quarter, year]. Deposits are fully refundable through the delivery date. The company has manufactured and delivered [X] units to founding customers to date.

**About Hearth**
Hearth designs and builds the world's first offline residential AI appliance. Based in [City, State] and founded in [Year] by [Founder Name], a [prior credential — teacher, engineer, whatever is honest], Hearth serves families and individuals who want private, capable, high-craft technology in the home. Learn more at hearth.com.

**Media assets:** high-resolution product photography, founder headshot, and B-roll available at hearth.com/press.

###

*(~470 words)*

---

### VARIANT B — DEAL CLOSED WITH AMENDED TERMS ($2.5M for 20% with two Sharks)

**FOR IMMEDIATE RELEASE**
**Contact:** [Comms Lead Name], [cell], press@hearth.com

# Hearth Closes $2.5 Million Round with Two Shark Tank Investors to Scale the First Offline AI Home Appliance

**LOS ANGELES, [Air Date]** — Hearth has closed a $2.5 million investment for 20 percent equity, jointly led by [Shark A] and [Shark B], on tonight's episode of ABC's *Shark Tank*. Two Sharks committing together to a hardware product on the show is uncommon; both cited the untapped market for premium offline AI as the reason.

Hearth is a $95,000 hand-built residential appliance that combines a private AI assistant, a full home media server, and a real-time family memory archive, all running locally without any cloud dependency.

"[Shark A] and [Shark B] each brought different strengths and we structured the round to reflect that," said [Founder Name], founder and CEO. "The additional capital lets us commit to manufacturing capacity twelve months earlier than our original plan. The revised terms are the right ones for the company we intend to build."

**[QUOTE FROM SHARK A — DRAFT FOR APPROVAL, TODO.]**

**[QUOTE FROM SHARK B — DRAFT FOR APPROVAL, TODO.]**

Hearth is accepting refundable $5,000 deposits toward first-batch delivery in [quarter, year]. Deposits are fully refundable through delivery.

**About Hearth** [same boilerplate as Variant A]

###

*(~380 words)*

---

### VARIANT C — DEAL CLOSED WITH ROYALTY ATTACHED

**FOR IMMEDIATE RELEASE**
**Contact:** [Comms Lead Name], [cell], press@hearth.com

# Hearth Partners with [Shark Name] on $2 Million Investment to Deliver the First Offline AI Home Appliance

**LOS ANGELES, [Air Date]** — Hearth has closed a $2 million investment for 15 percent equity and a per-unit partnership royalty with [Shark Name] on tonight's episode of ABC's *Shark Tank*. The royalty structure aligns the investor's return with unit-level delivery success, a fit for a hand-built luxury appliance category.

Hearth is a $95,000 residential appliance that combines a private AI assistant, home media server, and a family memory archive, running entirely offline.

"The royalty component was something [Shark] and I discussed on the floor and it fits how Hearth is built," said [Founder Name], founder and CEO. "Each Hearth is hand-assembled. Each customer is a real relationship. Structuring the partnership so [Shark] participates in every unit sold reflects the actual shape of the business, not a projection."

**[QUOTE FROM SHARK — DRAFT FOR APPROVAL, TODO.]** The quote should frame the royalty as an alignment mechanism, not a cost of capital.

Hearth is accepting refundable $5,000 deposits toward first-batch delivery in [quarter, year].

**About Hearth** [same boilerplate]

###

*(~350 words)*

*Note to comms lead: do not apologize for the royalty. Do not describe it as "Kevin's usual move." Framing is: this is a category where per-unit economics matter, and the investor structured for that. If pressed by tech press, use: "A royalty on a $95,000 unit is a partnership signal, not a burden. The unit economics support it comfortably."*

---

### VARIANT D — ALL SHARKS PASSED (THE OPPORTUNITY RELEASE)

**FOR IMMEDIATE RELEASE**
**Contact:** [Comms Lead Name], [cell], press@hearth.com

# Hearth Presents First Offline AI Home Appliance on ABC's Shark Tank; Delivery to First Customers Continues on Schedule

**LOS ANGELES, [Air Date]** — Hearth, the maker of the first residential AI appliance that runs entirely offline, presented to the Sharks on tonight's episode of ABC's *Shark Tank*. No investment was concluded on the show. Hearth's first-batch deliveries continue on schedule for [quarter, year].

"Twelve years ago I was teaching fifth grade," said [Founder Name], founder and CEO of Hearth. "Tonight our product was in front of ten million people. That is the accomplishment. A Shark Tank deal was one of several ways this could have gone; the appearance itself is the outcome we planned for. The response tonight — from customers, from investors we were already in conversation with, from families I have never met — has been the strongest signal we've had since the product first shipped."

Hearth is a $95,000 hand-built residential appliance that combines a private AI assistant, a full home media server, and a family memory archive, running entirely offline. First units have already been delivered to founding customers. Refundable $5,000 deposits are open at hearth.com.

The company is in active conversations with institutional investors focused on premium hardware, private AI, and family technology. A Series A raise is expected to close in the coming quarters, with commitments already in place. Hearth will announce the round when closed, not before.

"The Sharks asked hard questions and I welcomed them," said [Founder Name]. "Some of the concerns I fully agree with. Others reflect the reality that this is a new category and the incumbents are not the ones who will build it. Every founder who has built a first-of-category product has had a version of tonight. We build tomorrow."

**About Hearth** [same boilerplate]

###

*(~360 words)*

*Note to comms lead: this release NEVER apologizes, NEVER attacks the Sharks, NEVER uses the phrase "they didn't get it" or "they weren't the target market." Every one of those framings has been used by past Shark Tank losers and it reads exactly like it sounds. The release above assumes strength and delivers it. Read it to the founder at T-30 days and rewrite if any sentence sounds defensive.*

---

### VARIANT E — SEGMENT DID NOT AIR

**FOR IMMEDIATE RELEASE**
**Contact:** [Comms Lead Name], [cell], press@hearth.com

# Hearth Opens Founder Round Ahead of First Consumer Deliveries

**[CITY, State], [Date]** — Hearth, the first offline AI residential appliance, today opened its Founder Round: 100 refundable $5,000 deposits toward the first consumer batch, delivering [quarter, year].

Hearth is a $95,000 hand-built appliance combining private AI, a home media server, and a family memory archive — running fully offline. First units have shipped to founding customers.

Interested customers can reserve at hearth.com. Press inquiries: press@hearth.com.

**About Hearth** [same boilerplate]

###

*(~110 words)*

*Note: this release is only sent if the segment is confirmed cut by ABC. Do not send speculatively — if the network hasn't confirmed the cut and the founder cannot verify, wait. Sending an "our episode is not airing" release when the episode is actually airing next week is a career-ender.*

---

## 3. INTERVIEW CRIB SHEET — 15 QUESTIONS

Founder voice: measured, warm, dry humor, never defensive, teacher-first. Every answer under 45 seconds if spoken aloud. Comms lead: rehearse these with the founder at T-14 days and again at T-3 days. Not memorized — internalized.

*This is the founder-facing crib. Read on the plane, hand to the agent, keep by the phone during press week. The comms-lead prep annotations (why each question is a trap, what pivot to steer toward) live in Appendix B and stay in the war room binder — do not carry them into the interview itself.*

### 1. "Why did you go on Shark Tank?"
"Because ten million families would see a category that didn't exist before tonight. That's not something an ad budget buys. I built Hearth for people who want capable technology in their home without the surveillance economy attached. Shark Tank puts that idea in front of the audience it was made for."

### 2. "Did you rehearse?"
"I rehearsed the numbers. I did not rehearse the story — the story is the last twelve years. If you rehearse the story you sound like you're selling something you don't actually believe. I believe this one."

### 3. "What surprised you about the Sharks?"
"How present they are. On television they are characters. In the room they are business operators asking exactly the questions you'd expect an operator to ask. That was more useful to me than the outcome of the deal."

### 4. "What did the Sharks get wrong?"
"I don't think they got anything wrong given what they saw in ten minutes. They asked about scale. I answered honestly that scale is not the shape of this business in year one. If I had ten more minutes with any of them I would have made the same argument in more detail. Ten minutes is what the format is."

### 5. "Would you accept a deal from Kevin O'Leary?"
"Kevin has done more consumer hardware deals than anyone else on that panel. If Kevin O'Leary calls me on Monday, I take the call. I take every call. That's the job right now."

### 6. "You're a schoolteacher — is that a gimmick?"
"I taught for eleven years. I built the first prototype on evenings and weekends because I couldn't find what I wanted to buy for my own family. The teaching part isn't a gimmick — it's why the product exists. Every design decision in Hearth is what I would have wanted in a home appliance when I was raising kids on a teacher's salary and worrying about what Alexa was hearing."

### 7. "$95,000? Really?"
"Yes. It's hand-built, warranted for ten years, and it does the work of five separate devices that families already own. The audience for a first-batch $95,000 appliance is small and specific. That's who we built for. A second product at a different price point is on the roadmap. Not this year."

### 8. "How is this not just a fancy Alexa?"
"Alexa listens on Amazon's servers. Hearth listens on your own hardware, in your house, with no internet connection required. Alexa is a microphone with a shortcut to a shopping cart. Hearth is a home computer that answers to no one but you. That's not a spec difference, it's a category difference."

### 9. "Are you going to compete with Apple or Amazon?"
"We're not competing with them. They can't build this product without cannibalizing their advertising and data businesses. That's not a weakness of theirs, it's a strategic constraint. Our category is the category they aren't allowed to enter. That's the thesis."

### 10. "What happens if a customer gets hacked?"
"The security model of Hearth starts with 'the device is not on the internet by default.' A device that doesn't reach the network can't be reached from the network. That's not marketing, it's how the hardware ships. If a customer opts in to remote access we walk them through the trade-offs in writing before we enable it. I'd rather have a slower support experience and a customer who understands their attack surface than a fast experience and a headline in six months."

### 11. "Why is this made overseas?"
"The chassis is machined in [Country], the boards are assembled in [Country], the final integration and QC happens in [State, US]. The choice is craft, not cost — the machinist who makes our chassis has been doing this kind of work for thirty years and there aren't fifteen shops in North America that can do it to spec. When there are, we'll move that step."

### 12. "When can I actually buy one?"
"First batch is delivering [quarter, year] to founding-customer deposits. Second batch opens for reservation on hearth.com after the first batch delivers. If the reader wants one now, hearth.com/reserve — refundable through delivery, ten-year warranty."

### 13. "Do you have investors already lined up beyond Shark Tank?"
"We're in active conversation with several institutional investors and family offices. I'm not going to name them tonight. When a round closes, we announce it. Not before."

### 14. "What's next after Hearth?"
"Hearth is what's next. This is the first offline AI residential appliance and there is a five-year roadmap of software and second-product decisions to make. I'll answer 'what's next after Hearth' when Hearth is in ten thousand homes."

### 15. "What would you tell yourself before your Shark Tank taping?"
"That the answer to every question you're worried about is 'the truth, said calmly.' The Sharks aren't there to trick you. The audience isn't there to catch you. You spent twelve years building something you understand better than anyone in that room. Say it plainly and then stop talking."

---

## 4. PRINT & TECH PRESS OUTREACH PLAN

### Embargo mechanics
- **Embargo lifts:** 8:01 PM ET on air night. That is the moment ABC's segment concludes on the East Coast broadcast.
- **Email sent:** 8:25 PM ET, from press@hearth.com via Front, personalized send-later. Subject: "Hearth — Shark Tank aired, embargo lifted, here's the story."
- **Attachments:** press release PDF, product hero image (300 DPI, 5000px wide), founder headshot, one-page fact sheet, phone number of comms lead.
- **Pre-embargo briefings:** two reporters get pre-briefed at T-72h under embargo — pick the two most likely to write a Day-1 feature (recommend one from The Verge, one from Ars Technica). They get NDA + embargo agreement in writing, signed via DocuSign.

### The list — 42 reporters, named with beats and specific asks

Names and outlet assignments are current as of the last comms-lead scrub at T-60 days. Comms lead re-scrubs at T-14 days: reporters move; if a name has left their masthead, replace with the current beat holder and note the swap in the sheet. Do not send an embargo email to a reporter who left three months ago.

**The Verge**
1. **Nilay Patel (Editor-in-Chief, Decoder host):** "The offline AI story you've been waiting for someone to actually build — a shipped $95k appliance with ten-year warranty, founded by a fifth-grade teacher. Decoder recording within 10 days of air?" Ask: 45-minute Decoder.
2. **Sean Hollister (Senior Editor, hardware):** "You cover hardware as hardware, not as a startup story. Hearth is machined chassis, real thermal design, a real BOM. Loaner unit available week of air." Ask: hands-on review.
3. **David Pierce (Editor-at-Large, consumer tech):** "The 'what's the point of a smart speaker' beat you've been on for five years — Hearth is the first product that treats that question as the design brief." Ask: features piece.

**Ars Technica**
4. **Ron Amadeo (Reviews Editor):** "You've written the definitive teardowns on every Google Home device. Hearth is designed to be teardown-friendly, ten-year serviceable. Send loaner + spec sheet?" Ask: teardown review.
5. **Andrew Cunningham (Senior Reviews Editor):** "Your Mac mini home-server piece made me build Hearth's local media stack differently. Want to send you the appliance version and get your unfiltered read." Ask: hands-on with the local media stack.
6. **Lee Hutchinson (Senior Technology Editor, infrastructure):** "You care about the boring parts — power, thermal, IPMI-equivalent management on a home appliance. Hearth ships with real out-of-band management. Would love a systems-thinking piece." Ask: infrastructure feature.

**Wired**
7. **Boone Ashworth (Staff Writer, consumer tech):** "The privacy-tech beat is full of vaporware. Hearth ships. Day-1 unit review plus founder interview access." Ask: Day-1 review, exclusive.
8. **Julian Chokkattu (Reviews Director):** "For the reviews team: a $95k appliance is a category, not a product. A reviews-desk conversation about how to cover it fairly." Ask: reviews-desk meeting.
9. **Lauren Goode (Senior Writer, consumer tech and platforms):** "You cover the intersection where consumer tech becomes a household object. Hearth is that intersection with a ten-year warranty attached." Ask: platforms angle feature.

**Bloomberg (current tech bench, checked at T-60 days)**
10. **Ian King (Senior Reporter, chips + hardware supply chain):** "The offline-AI category runs on inference silicon that used to only live in a data center. Hearth is what happens when you productize that silicon for a house. Interested in the supply-chain story that sits underneath?" Ask: supply-chain feature.
11. **Mark Gurman (Managing Editor, consumer tech / Power On):** "Not asking you to write about a rival to Apple. Asking you to write about the category Apple can't enter without cannibalizing its own services revenue. Power On newsletter mention." Ask: newsletter beat.
12. **Vlad Savov (Reporter, consumer devices):** "You review products others don't take seriously and take seriously products others don't review. Hearth is both." Ask: reviews desk hands-on.

**Core Memory (Ashlee Vance's Substack — the Bloomberg-Businessweek-in-your-inbox rehome)**
13. **Ashlee Vance:** "You wrote the Musk book by spending months in the room with a founder others were writing about from a distance. Hearth is a six-month story if you want it — full founder access, factory access, and the customers who have already taken delivery. This is the arc you built Core Memory to run." Ask: long-form profile, exclusivity on the factory tour.

**New York Times**
14. **Brian X. Chen (Consumer Tech Columnist):** "You test consumer tech as a consumer, not a spec-sheet reader. A $95k appliance breaks your usual frame — the story is what happens when a household object is priced like a car." Ask: column consideration.
15. **Tim McKeough (Home + Design contributor):** "Hearth lives on furniture, not on a shelf. The design story is a Home section story, not a Tech section story. Photography ready." Ask: Home section feature.
16. **Erin Griffith (Reporter, startups):** "Founder profile with the Shark Tank hook — teacher-turned-hardware-founder in a category the incumbents can't enter. Financial discipline angle: refundable deposits, no revenue-booking games." Ask: startup profile.

**Wall Street Journal**
17. **Joanna Stern (Senior Personal Technology Columnist):** "Your column is the one where a product either survives contact with real use or doesn't. Loaner unit for real-use review, and full access if you want to hear the story behind the price." Ask: personal-tech column review.
18. **Nicole Nguyen (Personal Tech Reporter):** "The consumer angle: what does it mean for a family to spend $95k on a household object that promises to work for a decade? That's your beat." Ask: consumer feature.
19. **Katherine Bindley (Personal Journal, tech and family):** "The Family & Tech intersection. Hearth is the first product that treats family privacy as the design brief, not a compliance checkbox." Ask: Personal Journal feature.

**The Information**
20. **Aaron Tilley (Senior Reporter, consumer devices):** "The subscribers-only crowd wants the VC angle: what does the Series A pipeline look like after this segment, and which funds already circled." Ask: subscriber-only piece with fund names.
21. **Kate Clark (Deputy Bureau Chief, venture):** "The venture angle on a hardware company that isn't asking for growth capital yet — that's a rare story your readers actually want." Ask: venture piece.

**Bloomberg Businessweek (separate from Bloomberg news bench above)**
22. **Max Chafkin (Features Editor, tech and business):** "The long-form Businessweek arc: teacher-to-founder, category creation, the six months of silence between taping and air. You've run this kind of piece before; this is that piece with a product you can hold in your hand at the end." Ask: features piece.

**TechCrunch**
23. **Brian Heater (Hardware Editor):** "Your beat is hardware that ships. Hearth ships. Would like a hands-on plus a founder call for the Hardware column." Ask: Hardware column feature.

**Fast Company**
24. **Mark Wilson (Global Design Editor):** "The industrial-design story of the year in home tech. Machined chassis, ten-year warranty, priced like a piece of furniture. Photography by [name] ready." Ask: design feature.
25. **Elissaveta Brandon (Design contributor):** "The 'design as a moral position' angle — what does it mean to design a household object that refuses to phone home? That's a Fast Company piece." Ask: design essay.

**Inc.**
26. **Cameron Albert-Deitch (Senior Reporter, founder features):** "Founder profile: schoolteacher-turned-hardware-founder, twelve-year build, Shark Tank moment. Inc. reader is the small-business owner asking 'could I do that?'" Ask: founder profile.

**Forbes**
27. **Alex Konrad (Senior Editor, venture and 30 Under 30):** "Not 30 Under 30 — 40-plus, teacher, built a category. That's the counter-profile Forbes doesn't run enough of." Ask: founder feature.
28. **Kerry A. Dolan (Wealth Editor):** "Your beat is where wealth actually spends. Hearth is a $95k residential appliance the ultra-high-net-worth demographic is quietly buying. Data on the first cohort available under embargo." Ask: wealth-lens feature.

**Business Insider**
29. **Ben Bergman (Senior Reporter, VC and startups):** "The Shark Tank deal follow-through angle: who called on Monday morning, and what a founder does with a $2M offer when they didn't need capital in the first place." Ask: deal-mechanics piece.
30. **Melia Russell (Correspondent, startups):** "The category-creation angle from the operator's seat. What Hearth built and why. Founder access." Ask: startups piece.

**Fortune**
31. **Emma Hinchliffe (Senior Writer, Fortune 500 and MPW):** "The premium-hardware category built by a founder outside the usual pattern. That's a Fortune feature." Ask: profile.

**CNBC**
32. **Andrew Ross Sorkin (Squawk Box co-anchor, DealBook founder) via producer Steve Kopack:** "Post-Shark-Tank founder segment for Squawk or DealBook. The offline-AI category story with the six-month NDA context." Ask: broadcast segment.

**Axios**
33. **Dan Primack (Business Editor, Axios Pro Deals):** "The deal-mechanics angle for the Pro subscribers: royalty vs equity vs no-deal, and what a founder does with the traffic from a Shark Tank segment either way." Ask: Pro deals writeup.

**Marketplace / NPR**
34. **Kimberly Adams (Marketplace Tech host):** "The friendliest Day-1 booking. Marketplace audience is the exact intersection of business-literate and consumer-curious that Hearth needs." Ask: Marketplace Tech interview.

**Rest of World**
35. **Andrew Deck (Reporter, AI and platforms):** "The offline-first thesis is a global story, not just a US one. Families in markets with weaker broadband and stronger privacy law are the second cohort. Would like a piece on the international angle." Ask: global-angle feature.

**Robb Report**
36. **Rachel Cormack (Senior Editor, luxury tech and gadgets):** "The luxury home tech category has been dead since Kaleidescape. Hearth is what the next generation looks like at $95k. Photography and factory access ready." Ask: luxury tech feature.

**Dwell**
37. **Duncan Nielsen (Editorial, home design and technology):** "Hearth is designed to live on furniture. The Dwell reader is the exact buyer — someone who spends on architecture, cares about material, doesn't want a plastic puck on the counter." Ask: home-design feature with photography.

**6sqft / Curbed (New York Magazine)**
38. **Michelle Sinclair Colman (Contributor, interior design and home tech):** "The interior-designer-and-tech intersection. Hearth is a design object first, an AI appliance second. Feature the object, then the story." Ask: interior-design piece.

**The Ringer**
39. **Bryan Curtis (Editor-at-Large, culture and media):** "The Shark Tank cultural angle: what it means when a hand-built $95k residential appliance is on a show whose brand is $19.99 water-bottle openers. That's a Ringer piece." Ask: culture essay.

**Wallpaper\***
40. **Bill Prince (Editor-in-Chief) or Tilly Macalister-Smith (Contributing Editor, design):** "Hearth belongs in the Wallpaper* audience's home before it belongs in a tech magazine. Would like a design-first feature — object photography, no product-marketing copy." Ask: design feature.

**Monocle**
41. **Josh Fehnert (Executive Editor):** "The Monocle reader owns the exact type of home Hearth was designed for. A category-defining hand-built object at the intersection of design and craft. Would value a piece in Monocle's design or business section." Ask: design or business feature.

**Departures / Elite Traveler (luxury lifestyle)**
42. **Jesse Ashlock (Editor-in-Chief, Departures):** "The Departures reader is the exact cohort taking delivery in the first year. Hearth as a household object at the intersection of design, technology, and privacy." Ask: lifestyle feature.

**Podcast bench — parallel outreach, comms lead runs alongside the reporter list**

- **Kara Swisher (On with Kara Swisher):** "The Swisher take on offline AI is the take that moves the conversation. Ask: full-episode booking."
- **Kevin Roose + Casey Newton (Hard Fork, NYT):** "You've covered every AI story of the last three years except this one — the one where the AI stays in the house. Ask: segment or full episode."
- **Scott Galloway (Prof G Markets):** "The category-economics angle: what makes a $95k residential appliance a defensible market versus a novelty. Prof G reader is the exact wealth demographic Hearth is priced for. Ask: full-episode booking."
- **Guy Raz (How I Built This, NPR):** "The twelve-year build story — the teacher, the garage prototype, the eleven-year gap between idea and shippable product. This is the exact HIBT arc. Ask: full episode with a lead time of 90+ days."
- **Nilay Patel (Decoder, The Verge):** already booked via Verge outreach above; parallel podcast confirmation.
- **Reid Hoffman (Masters of Scale):** "The category-creation frame. How a hardware founder scales a business that is deliberately not designed for infinite scale in year one. Ask: full episode."
- **Reggie James (Late Checkout):** "The consumer-culture read on Hearth as an object. The Late Checkout audience is early-adopter design-literate. Ask: full episode."
- **Ben Thompson (Sharp Tech + Stratechery daily update):** "The strategic-position argument: why Apple, Amazon, Google cannot enter this category without cannibalizing themselves. That is a Stratechery piece and a Sharp Tech segment. Ask: paid-subscriber feature + Sharp Tech booking."
- **Nathan Labenz (The Cognitive Revolution):** "The offline-inference technical stack: what runs on-device, what the model roadmap looks like, why on-device inference is the future the cloud-AI companies won't sell you. Ask: full episode with the engineering lead alongside the founder."
- **Sam Parr + Shaan Puri (My First Million):** "The MFM audience is the exact demographic between 'could-buy-this' and 'wants-to-know-how-you-built-this.' The twelve-year arc plus the $95k unit economics is an MFM episode. Ask: full episode."

### Outreach rules
- Every email is personalized in the first sentence with something the reporter has actually written.
- No blast emails. Ever.
- Reporters who don't reply within 48 hours get one follow-up on Wednesday. Not a second.
- Any reporter who quotes founder without asking for a follow-up gets thanked publicly and moved to a lower tier for the next cycle.
- If Verge and Ars both want exclusive, offer Verge the founder interview and Ars the teardown. Two exclusives, one product, both happy.
- Verify each named reporter is still on the beat at T-14 days. Bench moves; the sheet has to move with it. A dead-address embargo email is worse than no email.

---

## 5. SOCIAL MEDIA 30-DAY PLAN

### Account architecture

- **Founder personal — LinkedIn:** primary. This is where investors, enterprise buyers, and press live. Post cadence: 3x/week during days 1-30, 1x/week thereafter.
- **Founder personal — X:** secondary. Do NOT use Threads or Bluesky as primary. Reason: tech press lives on X. Journalists check founder's X within 5 minutes of a story angle emerging. Threads and Bluesky are pleasant places that produce zero press pickups.
- **Hearth brand — Instagram:** primary. This is the industrial-design story. Product photography, machining process, delivery moments. Post cadence: 4x/week during days 1-30, 2x/week thereafter.
- **Hearth brand — X:** secondary. Amplifies founder personal, handles support-adjacent replies.
- **Hearth brand — TikTok:** conditional, see the ABC-clip decision below.
- **Do NOT open on the founder personal account:** TikTok (wrong tone for founder voice), Threads (no press), Bluesky (no press), YouTube Shorts (until a real video pipeline exists).

### The ABC clip-rights question (revised call on TikTok)

The prior version of this playbook said "no TikTok, full stop." That's the right call for the founder's personal presence. It is not necessarily the right call for the brand account, because a Shark Tank clip has a native 72-hour life on TikTok whether Hearth is on the platform or not — random creators re-cut and re-post those segments constantly, sometimes with commentary the brand does not want to be the only voice missing from.

The clip-rights question:

- **ABC owns the segment.** The founder does not own it. Standard Shark Tank contestant contracts grant ABC and Sony Pictures Television broad rights to the taped segment; the contestant retains no distribution rights and can re-post only under fair-use limits (short clips, commentary, transformative use). Founder cannot upload the full segment to any platform, brand-owned or otherwise. This is not a Hearth-specific rule; every past contestant is bound by it.
- **ABC does typically release short official clips.** Historically, ABC's Shark Tank social team posts a 60-90 second cut of most segments to the show's own TikTok, Instagram, and YouTube within 24-72 hours of air. That clip is embeddable and shareable. Comms lead can request, ahead of air, that the show's social team tag the brand account when it posts — most producers say yes to that ask.
- **The distribute-or-don't-distribute call for the brand account:**
  - **Distribute (open a brand-only TikTok):** if Hearth wants a share of the 72-hour attention window on the platform where the segment will circulate regardless of participation. Post the ABC-owned clip only by resharing/duetting ABC's official post (never re-uploading ABC's video file). Add short brand-voice commentary in-frame. Cross-post the same content pattern to Instagram Reels, where it has a longer tail and lower brand risk.
  - **Don't distribute (no brand TikTok, ever):** if the founder's judgment is that the audience on TikTok is not the $95k appliance buyer and the platform tone is a permanent brand-risk. This is a defensible call. The cost is losing the 72-hour window to third-party creators whose commentary the brand does not control.
- **Recommendation:** open a brand-only TikTok on T-14 days, populate with three product-photography posts (no founder face, no dancing, no trend audio), verify the handle. On air night, reshare ABC's official clip once (with one line of brand commentary) and do nothing else on the platform for the first 72 hours. Reassess at T+30. If the analytics show engagement from a demographic that maps to the deposit funnel, keep it. If not, archive the account. Do not delete — archived is recoverable, deleted invites a squatter.
- **Legal:** any TikTok activity gets the same three-eye rule as the rest of this playbook (comms lead drafts, attorney reviews, founder approves). Do not freelance TikTok posts on air night.

### Day-by-day: Days 1-7 (drafts ready for founder edit)

**Day 1 (Monday) — LinkedIn (founder):**
> Last night, ten million people saw Hearth for the first time.
>
> Twelve years ago, I was teaching fifth grade in [City]. I built the first Hearth prototype in my garage on weekends because I couldn't find what I wanted to buy for my own family — a computer that answered to me, in my house, with the internet unplugged.
>
> Since taping in [Month], I've been under NDA. I couldn't tell anyone. Not my mother, not my best customer, not the reporters who reached out. That was the hardest part.
>
> What I can tell you now: [one sentence outcome — closed / continued conversations / built the category]. And that we are open for reservations. First batch delivers [quarter].
>
> To everyone who reached out overnight — I read every message. I'm answering as fast as I can. Thank you.
>
> hearth.com

**Day 1 — X (founder):**
> Reservations at hearth.com. First batch [quarter]. Ten-year warranty. Refundable through delivery.
>
> Every DM will get a response. Give me 48 hours. — Mark

**Day 1 — Instagram (brand):**
> Post 1: Product hero, three-line caption: "Twelve years. One appliance. Now yours."
> Post 2 (evening): Behind-the-scenes photograph — the chassis being machined. Caption: "This is where every Hearth begins."

**Day 2 (Tuesday) — LinkedIn (founder):**
> The single question I've been asked most in the last 18 hours: "Why $95,000?"
>
> Because every part of Hearth is a decision you can look at and touch. The chassis is machined from a single billet of [material] by a shop that has been doing this work for thirty years. The boards are custom, not off-the-shelf. The chassis alone represents [X] hours of machinist time.
>
> $95,000 is what it costs to build this appliance and stand behind it for ten years without a subscription. It's not what everyone can afford. It's the honest number for what this is.
>
> A second product at a different price point is on the roadmap. It's not this year's job.

**Day 2 — X (founder):**
> The $95k question, answered: machined chassis, custom boards, ten-year warranty, no subscription. Hand-built. The honest number for what this is.

**Day 2 — Instagram (brand):**
> Video (15s): the chassis being wrapped for shipping. Caption: "One appliance, hand-inspected, delivered."

**Day 3 (Wednesday) — LinkedIn (founder):**
> On going on Shark Tank as a former schoolteacher:
>
> Someone asked me yesterday if the teacher story was a gimmick. It's not. It's the reason Hearth exists.
>
> In a classroom you learn very quickly that technology either serves the room or takes it over. A device that keeps every kid's attention on the wrong thing is a device that makes the teacher's job harder. I bought a lot of technology for my classroom over eleven years and I got fooled a lot.
>
> Hearth is the appliance version of the lesson I learned in that classroom. Every design decision — offline-first, no subscription, no advertising surface — is what I would want in my own home from the perspective of someone who has watched technology take rooms over.
>
> Being a schoolteacher isn't a marketing story. It's the design brief.

**Day 3 — X (founder):** teaser image + link to LinkedIn.

**Day 3 — Instagram (brand):** carousel — three shots of the founder in the workshop, black-and-white, with the appliance in the background. Caption: "The design brief was written in a classroom."

**Day 4 (Thursday) — LinkedIn (founder):**
> A note on the deposits.
>
> Yesterday and today we processed more Hearth deposits than in the previous twelve months combined. Every deposit is fully refundable through delivery. I want that on the record because I've seen too many hardware companies book pre-orders like revenue.
>
> If your Hearth doesn't ship or you change your mind, you get your money back. Every dollar.
>
> That's the deal. We stand behind the product, but the customer holds the leverage. That's how it should work when you're spending $95,000 on an appliance you haven't physically touched.

**Day 4 — X (founder):** short version of same message.

**Day 4 — Instagram (brand):** product photograph, morning light, in a home setting. Caption: "This is where a Hearth lives."

**Day 5 (Friday) — LinkedIn (founder):**
> To the investors who reached out this week:
>
> I've received [X] introductions since Sunday from institutional funds, family offices, and strategics. I've replied to every one. I'll take every serious meeting.
>
> A note on how I think about the raise: we don't need capital to keep shipping. First-batch deliveries are funded. What additional capital does is compress the timeline for the second batch and the software roadmap. That means we'll be selective. The right partner for Hearth is a partner who understands that this is a category, not a series of quarterly sales cycles.
>
> If that's you, my inbox is open: mark@hearth.com

**Day 5 — X (founder):** "Investor inbox is mark@hearth.com. Selective. Serious partners only."

**Day 5 — Instagram (brand):** short reel — assembly floor, ambient sound only, no music. Caption: "The build."

**Day 6 (Saturday) — quiet day.** One Instagram post (product in a home setting, no caption beyond location). Founder off social.

**Day 7 (Sunday) — LinkedIn (founder):**
> One week ago tonight, Hearth aired on Shark Tank. I've slept about four hours a night since.
>
> What I've learned in seven days:
>
> The category is real. Real in the sense that families with the resources to buy this are searching for it, not being sold it. Every conversation this week began with the customer explaining Hearth back to me. That's when you know.
>
> The story that sells the product is the design story. Not the AI story. Not the media-server story. The design story. The chassis, the wood, the sound of the fans (there is no sound), the way the appliance sits on furniture like a piece of furniture. That's the entry point. AI is the reason to keep it for ten years.
>
> I owe my family a Sunday. I'll be back Monday. Thank you for the week.

### Days 8-30 — three drafted posts per theme week, cross-posted per platform

Each post below is drafted for a specific day and adapted for LinkedIn, X, and Instagram. Founder edits the LinkedIn copy by hand before publishing; the X and Instagram adaptations are comms-lead drafts the founder approves in one sitting. Post one per day on the founder's LinkedIn, cross-post the X adaptation same day, and hand the Instagram post to the brand-account operator with the caption pre-written.

#### Week 2 — the build (Days 8-14)

**Day 8 (Monday) — Post 8A: The Supply Chain, Boring and Honest**

- **LinkedIn (founder, ~250 words):**
  > I owe you the boring version of the Hearth supply chain.
  >
  > The chassis is machined in [Country] by [Shop], a family-owned CNC shop that has been running the same [machine model] for eleven years. Lead time on a batch of thirty chassis is nine weeks. The boards are fabricated in [Country] by [Fab] on a fourteen-layer Megtron 6 stackup. Fab lead time is six weeks; assembly at [EMS] adds another three. Final integration and QC happens in [State].
  >
  > None of that is glamorous. All of it is the reason a Hearth ships on time or doesn't.
  >
  > The reason I'm telling you the boring version is because the last time a consumer hardware company avoided this question, the answer turned out to be "we don't know where the chassis is made and we've never been to the fab." That is the failure mode. The way you avoid it is to publish the honest version before anyone asks.
  >
  > If you have a question about a specific supplier, ask it in the comments. I'll answer what I can without breaching a supplier NDA. What I can't answer, I'll tell you why.

- **X (founder, one post):**
  > The boring Hearth supply chain, published on purpose: chassis machined in [Country], boards fabbed in [Country] on 14-layer Megtron 6, final integration in [State]. Ask a supply-chain question in replies. I'll answer what I can.

- **Instagram (brand, single image or short reel):** photo of the raw billet the chassis is machined from, before the first cut. Caption: "One billet. Nine weeks of machining. Every Hearth starts here." No hashtags. No emoji.

**Day 10 (Wednesday) — Post 8B: The Thing That Almost Killed Us in Board Bring-up**

- **LinkedIn (founder, ~280 words):**
  > A story from six months ago that I couldn't tell you until this week.
>
  > During board bring-up on Rev-A of the main SBC we discovered a shoot-through path on the power stage that would have destroyed the board on first plug-in if we'd shipped it. The mistake was mine — I signed off on a schematic that a second pair of eyes should have caught. It cost us a re-spin, three weeks, and about $18,000 in scrap.
>
  > I'm telling you this for two reasons. The first is that the audit that caught it is the same audit that gets run on every board before every batch now, and that audit is a Hearth cost line that will never go away. The second is that when a hardware founder tells you the first prototype worked, they are either lying or they got lucky. The honest version is that the first one didn't work and the second one caught fire and the third one is the one that shipped.
>
  > If you are buying a Hearth, you are buying the third one. That is the correct number of iterations to buy from a founder.

- **X (founder, one post):**
  > During Rev-A board bring-up we caught a shoot-through path on the power stage that would have bricked every board on first plug-in. Re-spin, three weeks, $18k in scrap. The version you buy is Rev-D. That's the right number of iterations to buy from a hardware founder.

- **Instagram (brand):** photo of a stack of failed Rev-A boards next to a shipping Rev-D board, taken with workshop lighting. Caption: "Left: the boards that failed. Right: the board that ships. Between them: eight months."

**Day 12 (Friday) — Post 8C: Why Every Hearth Gets a QC Signature**

- **LinkedIn (founder, ~220 words):**
  > Every Hearth ships with a hand-signed QC sheet.
>
  > On the sheet: the serial number, the machinist's initials on the chassis, the assembler's initials on the boards, the integrator's initials on the final unit, the QC lead's signature at the end. Four humans. Four names. The customer knows who built their appliance.
>
  > That practice is not scalable. It is deliberately not scalable. At the volumes Hearth is priced for, the QC sheet is a promise the customer can hold. If we ever scale past the point where a human name can go on a signature line, we will have moved to a different product at a different price. This one, at this price, ships with signatures.
>
  > If you have taken delivery of a Hearth in the last quarter, the four names on your QC sheet are still on the team.

- **X (founder, one post):**
  > Every Hearth ships with a hand-signed QC sheet — machinist, assembler, integrator, QC lead. Four humans, four names. Not scalable. Deliberately not scalable. At this price the signature is part of the product.

- **Instagram (brand):** overhead photo of a QC sheet on a Hearth's shipping crate, signatures visible but names blurred for privacy. Caption: "The last page in every shipping crate."

#### Week 3 — the customer (Days 15-21)

**Day 15 (Monday) — Post 9A: The First Customer**

- **LinkedIn (founder, ~300 words):**
  > This week the first customer who took delivery of a Hearth agreed to let me write about them.
>
  > They are a family of five in [State], not in tech, not on the internet in the way most of you reading this are on the internet. They bought a Hearth because their oldest child has a specific medical condition that makes the household's data-privacy math different from the average family's, and because they were tired of finding out — years later — what a smart-home device had been listening to.
>
  > They did not buy Hearth because it was on Shark Tank. They bought Hearth eight months before we taped. They are the customer I was building for the entire time and did not know by name until March.
>
  > I visited them last month. The appliance is in their living room. It sits on a walnut console next to a stack of their kid's picture books. It has been on continuously for four months. It has needed one software update, which I pushed manually because they have opted out of automatic remote access. The update took eleven minutes.
>
  > This is the exact use case. Not a keynote. Not a demo. A family with a specific reason and a device that does the thing it said it would do.
>
  > If you are considering a deposit, this is the customer you would be joining. I would rather have thirty families like this one in year one than three hundred customers acquired by a Super Bowl ad.

- **X (founder, one post):**
  > First delivered Hearth is a family of five in [State]. Bought eight months before we taped. Appliance has been on continuously for four months, needed one manual software update, and sits on a walnut console next to a stack of picture books. This is the customer.

- **Instagram (brand):** photograph of a Hearth in a real living room, morning light, no people visible. Consented to by the customer. Caption: "Month four in a real home. This is a Hearth in the wild."

**Day 17 (Wednesday) — Post 9B: The Unboxing Ritual (customer-consented reel)**

- **LinkedIn (founder, ~180 words):**
  > The delivery of a Hearth is a two-person job that takes about forty minutes. The customer opens the crate with our field integrator, who walks through the setup and answers every question in person. We do not leave until the customer says they are done asking.
>
  > This is not a scalable delivery model. It is a deliberately not-scalable delivery model. At the volumes we ship, the delivery is part of the product. The customer's first hour with the appliance is the hour that decides whether they will keep it, refer it, or return it.
>
  > A video of a recent delivery — with the customer's consent and their address blurred — is on our Instagram this morning. The customer asked to be the one who plugged it in for the first time. That is the answer to every question about the price.

- **X (founder, one post):**
  > A Hearth delivery is a 40-minute two-person job. The customer's first hour with the appliance is the hour that decides everything. Video from a recent (consented) delivery on IG this morning. Customer wanted to plug it in themselves. That is the whole answer.

- **Instagram (brand, reel, 45-60 seconds):** field integrator opening the crate with the customer in-frame from the shoulders down (face blurred or off-camera by customer preference). Ambient sound only, no music. Ends with the customer plugging in the appliance and turning it on for the first time. Caption: "A Hearth delivery. Filmed with the customer's permission. The last five seconds are their favorite part."

**Day 19 (Friday) — Post 9C: Why the First Customer Bought**

- **LinkedIn (founder, ~320 words):**
  > A longer piece than usual. The question I've been asked most this week: who buys a $95,000 residential appliance?
>
  > I've now interviewed the first fifteen customers who took delivery. There is a pattern.
>
  > None of them bought Hearth for the AI. Not one. When I asked "why Hearth," fifteen out of fifteen answered with a version of "I want a device in my house that isn't watching me." The AI is why they will keep it. Privacy is why they bought it.
>
  > None of them are wealthy in the way you might imagine a $95k-appliance customer is wealthy. Two are physicians. Four are business owners. Three work in law. Two are in finance. Four are in other categories I promised not to name. What they share is a specific relationship to their household's data — either professional exposure (a lawyer with client privilege, a physician with HIPAA), or a personal reason (a child with a medical condition, a spouse who was doxxed, a survivor of a specific kind of harm).
>
  > None of them bought Hearth on impulse. The average research-to-deposit window in the founding cohort was 71 days. The average time from deposit to delivery configuration confirmation was 14 days after the T-90 window opened.
>
  > This is not the profile of the Shark Tank buyer we were told to expect. This is a specific customer with a specific reason. The category is real because this customer is real.
>
  > If you are that customer, my inbox is mark@hearth.com. I answer every one.

- **X (founder, one post):**
  > 15 interviews with the first 15 delivered Hearth customers. None bought it for the AI. All bought it for privacy. Average research-to-deposit window: 71 days. This is not the impulse buyer. This is a specific customer with a specific reason. The category is real because they are.

- **Instagram (brand):** infographic-style single image, brand typography, no photograph. Text: "First 15 customers. 71-day average research-to-deposit. 0 bought for the AI. 15 bought for the privacy." Caption: "Data from the first cohort."

#### Week 4 — the future (Days 22-30)

**Day 22 (Monday) — Post 10A: The Software Roadmap, Without Dates**

- **LinkedIn (founder, ~260 words):**
  > A software roadmap for Hearth, without dates.
>
  > Every current Hearth ships with the appliance's core software stack. Every current Hearth will receive, over the next twenty-four months, four software capability additions. In rough order:
>
  > 1. A local-model upgrade path — the ability to swap in newer open-weight models as they are released, on the customer's schedule, with the customer's consent, on the customer's hardware.
  > 2. A family-account model — multiple household members with distinct profiles, all data staying on-device, no cloud sync.
  > 3. An expanded media-server capability — deeper library management, better transcoding, richer metadata on the family archive.
  > 4. An offline knowledge-store capability — the family's own documents, notes, and photographs, indexed and queryable on-device.
>
  > No dates. Not because I don't have them. Because I have watched too many hardware companies commit to a date they had to walk back. Every feature above will ship when it is ready. If you have taken delivery of a Hearth, every feature above is a free software update to the appliance you already own. That is the promise.
>
  > The second product is on a separate track. Different price point, different form factor. Not this year.

- **X (founder, one post):**
  > Hearth software roadmap, no dates: model swap path, family accounts, deeper media server, offline knowledge store. All free updates to shipped units. Second product is a separate track and it is not this year.

- **Instagram (brand):** four-tile carousel, one tile per roadmap item, brand typography. Caption: "Four software capabilities on the roadmap. Every one of them a free update to the appliance you already own."

**Day 25 (Thursday) — Post 10B: What I Learned From Sharks Who Said No**

- **LinkedIn (founder, ~340 words):**
  > It's been three weeks since Hearth aired. I have re-watched my segment four times.
>
  > A note for founders who are about to tape.
>
  > The Sharks who did not fund me on air have been more useful to me in the three weeks since than the deal I did or didn't close. Two of them followed up personally. One connected me to a family office. One walked me through, honestly, why they passed — and every reason they gave was a reason I have to answer for the next investor whether or not it comes from a Shark's mouth.
>
  > If you are about to tape: the Sharks who pass are not your enemy. They are the free critics who watched your product for ten minutes in a room where you could not defend it in writing, and who told you, in front of ten million people, what your Series A pitch will need to answer.
>
  > Take the note. Do not defend. Do not tweet a rebuttal three days later. Answer the note in the deck.
>
  > The company you build in the twelve months after your segment is the company that either validates the Sharks who said yes or vindicates the founder who received a no. Both are outcomes you control. Neither is decided on the show.

- **X (founder, one post):**
  > Three weeks after Hearth aired: the Sharks who passed have been more useful than the ones who didn't. Free critics with ten minutes and ten million witnesses. Take the note. Don't tweet the rebuttal. Answer the note in the deck.

- **Instagram (brand):** black-and-white photo of the founder in the workshop, back to camera, looking at a whiteboard with (illegible) notes. Caption: "Three weeks after air. Back to work."

**Day 29 (Monday) — Post 10C: The Founder's Vision Piece**

- **LinkedIn (founder, ~380 words):**
  > A month after air. I want to write down what Hearth is for.
>
  > Hearth is for the household that has decided its data is a possession, not a product.
>
  > For most of the last fifteen years the trade has been implicit: give a device your voice, your search history, your family's schedule, your children's questions, your medical anxieties, and in exchange the device will get slightly better every year at answering. The device gets smarter. So does the company that owns the device. The household gets a lower bill and a longer trail.
>
  > The trade was worth it when the alternative was no capability at all. It is not worth it now, because the capability exists on hardware that a household can own. What was true in 2011 is not true in 2026. The category we built Hearth for is the category where that fact is legible to the customer.
>
  > This is not an anti-Amazon post. This is not an anti-Apple post. Those companies made specific trades that are honest at their scale. Hearth is a different trade at a different scale. The household that wants both — the capability and the possession of their data — is the household Hearth was built for.
>
  > The five-year picture: a small number of very well-built appliances that a household owns for a decade, upgraded by software, serviced by humans whose names are on the QC sheet, in a category the incumbents cannot enter without cannibalizing themselves.
>
  > The one-year picture: ship the current batch. Open reservations on the next. Answer every question that comes in from the customers who have already committed. Hire two more machinists. Stop tweeting long threads.
>
  > This post is the last one for a while. Back to work. hearth.com

- **X (founder, one post):**
  > A month after air. Hearth is for the household that has decided its data is a possession, not a product. Full note on LinkedIn. Back to work.

- **Instagram (brand):** photograph of a delivered Hearth in a customer's home (previously used photo or a new one, with consent), late afternoon light. Caption: "A household object that belongs to the household. That is the whole idea."

### Rules
- Every post drafted by founder or comms lead. No ghostwriters.
- No thirst-trap founder photography. No "day in the life" content. No inspirational quotes.
- Reply to every substantive DM in 48 hours or don't reply at all. Half-response is worse than no response.
- Screenshot every negative comment before responding; screenshot the response after. Legal record.
- Brand-account TikTok, if opened, follows the ABC-clip-rights rules above. No freelancing.

---

## 6. INVESTOR FOLLOWUP WAVE

### Tier 1 — Sharks who passed but stayed engaged

Timing: Tuesday morning, T+40h. Any Shark whose team sent a message post-air, or who followed founder on social, or who quoted the segment publicly.

**Email template:**

> Subject: Following up from Sunday
>
> [Shark first name],
>
> Thank you for the questions on Sunday. You were right to press on [specific concern raised in the segment]. I've thought about it every day since we taped and my answer is sharper now than it was in the room.
>
> If you have 30 minutes in the next two weeks, I'd like to walk you through the numbers with the six months of context I couldn't share on the show. No deck. Just the numbers and the decisions behind them.
>
> Anywhere convenient for you. I'll come to you.
>
> Mark

Rules: no CC, no attachment, no PDF. Human email, one paragraph, one ask.

### Tier 2 — Series A funds with hardware track record

Target list (comms lead builds): a16z (hardware team — Andrew Chen for consumer, Anish Acharya), Founders Fund (Delian, Lauren Gross), Costanoa Ventures, Root Ventures, Bolt (Ben Einstein), Lux Capital, True Ventures. Also relevant: Playground Global, Eclipse Ventures.

**Email template:**

> Subject: Hearth — post-Shark Tank, opening conversations
>
> [First name],
>
> Sunday night Hearth aired on Shark Tank. Refundable deposits since air are [$X, honest number]. The category — offline AI residential — is now visible to the audience it was built for.
>
> I'm not raising this week. I'm meeting the funds who could be the right partner for the Series A we'll open [timeframe — quarter, be specific but not aggressive]. Yours is on that list because [one honest sentence — a portfolio company they built that maps to this, or a public post that maps to the thesis].
>
> 30 minutes on Zoom in the next three weeks?
>
> Mark
> Founder, Hearth
> hearth.com

Rules: never say "raising a Series A right now" if the round isn't formally open. Every claim is falsifiable if pressed. If they ask for the deck, send a 12-slide deck with real financials, not a highlight reel.

### Tier 3 — Family offices + strategics

Target list: Amazon Devices Ventures (they will not fund a competitor but the meeting shapes the narrative), Samsung NEXT, LG Nova, Sony Innovation Fund, Google Nest (long shot), family offices that already own the customer (concierge property firms, luxury lifestyle groups).

**Email template — family office variant:**

> Subject: Hearth — a category the incumbents can't build
>
> [First name],
>
> Hearth aired on Shark Tank on Sunday. The response, in short: the customer for a $95,000 offline appliance exists, is easy to reach, and does not want the incumbents to build this product.
>
> That's a rare structural position. It's why I'm writing.
>
> I'd like to introduce you to the company before we open the Series A. No formal ask. Fifteen minutes on Zoom whenever your calendar allows. I'll bring the numbers and a candid view of what the next 24 months look like.
>
> Mark
> Founder, Hearth

**Email template — strategic variant (Amazon Devices Ventures example):**

> Subject: Hearth — the offline-first category, from a founder who respects what you've built
>
> [First name],
>
> A quick note. Hearth aired on Shark Tank on Sunday. It's an offline residential AI appliance at a $95k price point — not a competitor to Alexa or Echo, but a product in a category the incumbents cannot enter without cannibalizing their advertising and data businesses.
>
> I'm not writing with a fundraising ask. I'm writing because the founders who build in adjacent categories tend to talk to the strategics who define the neighboring ones. I'd value 20 minutes on Zoom to introduce Hearth and hear how your team is thinking about the residential AI category over the next 24-36 months.
>
> If that's a conversation worth having, my calendar is open. If it isn't, I understand.
>
> Mark
> Founder, Hearth

Rules for Tier 3: never sound like you're pitching. Sound like you're introducing the company. Strategics take meetings with founders who don't need them and skip meetings with founders who do.

### Tracking
- Every email logged in HubSpot with a custom "Investor Outreach" pipeline.
- Response rate expected: Tier 1 ~40%, Tier 2 ~25%, Tier 3 ~15%.
- Comms lead reports weekly to founder: sent, opened, replied, meeting scheduled, meeting held, next step.

---

## 7. CUSTOMER SUPPORT SURGE PLAN

### The 72-hour math
Expect: deposit inflows spike 20-100x normal for 72h. Refund requests spike 10-30x normal starting T+24h. Two distinct customer archetypes emerge:

1. **The considered buyer** — did research over 48-72h, deposited on Tuesday, will not request a refund.
2. **The 11:47 PM buyer** — deposited between 10 PM and midnight on air night after two glasses of wine, will request a refund between T+18h and T+72h.

Plan for both.

### Refund policy — written explicitly, published at hearth.com/reservations

- Full refund of $5,000 deposit, no questions asked, at any time up to product delivery.
- Refund processed within 5 business days.
- No cancellation fee, no partial retention, no restocking fee.
- Deposit does not lock a delivery slot until the customer confirms configuration at T-90 days pre-delivery.

**Post this policy explicitly on the deposit form and the confirmation email. Reason: any customer who reads it and still deposits is a serious customer. Any customer who complains it was hidden has a case in the state's consumer-protection court.**

### Escalation matrix

| Level | Handler | Response SLA | Scope |
|-------|---------|-------------|-------|
| L1 | Support agent (contract, on-call for 30 days post-air) | 4 business hours | Deposit questions, timeline, spec clarifications |
| L2 | Ops lead | 24 business hours | Refund requests, configuration changes, unusual delivery locations |
| L3 | Comms lead | Same-day | Any customer who mentions social media, press, or "I'm going to post about this" |
| L4 | Founder | Same-day | Customers who have deposited $10k+ (edge case), or any escalation from L3 |

### Decision framework for edge cases

**"I want to change the color."**
- Before T-90 days: yes, no cost.
- After T-90 days: yes with $500 reconfiguration fee OR wait to next batch.

**"I want a 5-year extended warranty on top of the 10-year."**
- Say yes. Price it at 15% of unit cost. Fulfill it. Never allow warranty to become a differentiator — the 10-year is the differentiator. A 15-year answer is a courtesy.

**"I want to gift it. Can it be delivered to a different address?"**
- Yes. Confirm both addresses in writing. Comms lead reviews any gift over $50k for tax-disclosure requirements.

**"I've changed my mind — refund me and add me to the next batch's waitlist."**
- Yes on both counts. Do not editorialize.

**"I want to visit the factory before I take delivery."**
- Yes. Ops lead schedules quarterly factory tours for confirmed customers. This is a retention feature, not a burden.

**"My deposit went through but I don't remember making it."**
- Immediate full refund, no questions, personal call from ops lead. Screenshot the transaction, save to file. This is the 11:47 PM buyer. Treat with grace. They may come back in six months.

### Timeline reset promises

If manufacturing slips: notify all deposit customers by email at the moment the slip is confirmed internally. Do not wait for the original delivery month. The email says exactly this:

> Your Hearth was scheduled to deliver in [original month]. We now expect delivery in [new month]. The reason is [one honest sentence]. Your deposit remains fully refundable through the new delivery date. If you want a refund now, reply to this email and it will be processed within 5 business days. If you want to hold the reservation, no action needed.

Every slip announcement goes out on Tuesday morning. Never Friday afternoon.

### Support tools
- HubSpot Service Hub for ticket routing.
- Front for shared inbox on support@hearth.com.
- Aircall or Dialpad for phone support during business hours + 72h air-week extended hours.
- Slack `#customer-escalations` channel for L3+.

---

## 8. CRISIS MANAGEMENT PLAYBOOK

### General principles

1. **Speed is second to accuracy.** A response 90 minutes late but factually airtight beats a response in 15 minutes with a claim you can't back up.
2. **The founder does not respond to critics on X.** Ever. Comms lead responds through the brand account only. Founder responds only when the response is a documented statement, not a reply.
3. **Every response is drafted by comms lead, reviewed by attorney, and approved by founder before it posts.** Three-eye rule, no exceptions, even under time pressure.
4. **Screenshot everything.** The original post, the timeline, our response, their reply. Full-page screenshots to legal file within 1 hour of any incident.

### Scenario A: A Shark posts a snarky follow-up on X after air

**Example:** "@[Shark] tweets: 'Cute product but $95k for a fancy Alexa? Pass.'"

The response depends on whether this is a one-off snark or a coordinated audience pile-on. The old playbook treated both the same way — 60-minute wait, friendly brand-account reply, offline resolution. That is right for the first case and wrong for the second. The branches:

**Branch A1 — one-off snark (default assumption for the first 45 minutes):**
- Do NOT respond within the first 60 minutes. The impulse to respond quickly is wrong. Wait.
- Comms lead drafts three response options within 30 minutes and puts them in Slack `#sharks-only`. Attorney reviews. Founder picks one.
- **Preferred response (from brand account, not founder):** friendly, warm, does not engage the substance of the criticism, invites the Shark to a demo. Example: "Appreciate the airtime, [Shark]. Anytime you want to see one in person, we'll bring it to you. — The Hearth team"
- **Founder personal accounts stay silent.** The founder never quote-tweets a Shark's criticism. The founder never subtweets. The founder does not "like" any reply to the Shark's post, positive or negative.
- If the Shark escalates: comms lead reaches out to Shark's team privately via LinkedIn or the Shark Tank producer contact list. Never publicly. Resolve it offline.
- If the Shark's post crosses the 50k-like threshold within 24 hours: pre-drafted longer statement is issued 24-36 hours later, only if the pressure continues. Format: LinkedIn post from founder, 250 words max, gracious, substantive.

**Branch A2 — coordinated audience pile-on (escalate the moment amplification signals trip):**

The trigger for shifting from A1 to A2 is amplification velocity, not sentiment. Amplification tiers, measured on the Shark's post using Brand24 / native X metrics / a manual reload every 5 minutes:

| Tier | Amplification signal | Time-to-signal | Escalation |
|------|---------------------|----------------|------------|
| P0 | <10k likes at T+45min | first 45 min | Stay on Branch A1. Wait the 60 minutes. |
| P1 | 10k-50k likes at T+45min OR >5k retweets at T+30min | first 45 min | Move to 30-minute response window. Comms lead drafts a warmer, more substantive brand-account reply. Founder personal still silent. Attorney on Slack. |
| P2 | 50k-200k likes at T+45min OR >20k retweets at T+45min OR the post is being amplified by three or more accounts >500k followers | first 45-90 min | Move to 20-minute response window. Comms lead drafts a **longer statement** (150-200 words), not just a reply. Attorney reviews same call. Founder approves in `#sharks-only`. Post from brand account, not founder. Notify Shark Tank producer contact simultaneously with a private DM asking them to raise the temperature check internally. |
| P3 | 200k+ likes within 45 minutes OR the pile-on has produced press pickup from any Tier-1 outlet OR the founder or a family member has been named-and-shamed by a >1M-follower account | first 45-120 min | **Move to 15-minute cadence.** Longer statement goes out under 4 hours from the original tweet, not 24-36. Founder issues the statement personally on LinkedIn (not X), 300-450 words, gracious, substantive, cites the specific criticism, does not name the Shark. Comms lead simultaneously issues a shorter version from the brand account on X. Attorney is on the phone, not Slack. |
| P4 | 500k+ likes within 24 hours OR the pile-on has produced a threat to the founder's family / staff / customers / or produced a coordinated-review-bombing pattern on public review surfaces | within 4 hours of any P4 signal | **Attorney letter is on the table.** Not a takedown request — a preservation-of-evidence letter to X and any platform where the pile-on is amplified, requesting retention of account and post data pending review of any defamatory statements. Attorney determines whether a formal cease-and-desist is warranted based on the content of the pile-on, not the velocity. Comms lead activates the crisis-communications retainer with the outside PR firm (if one is on retainer; if not, this is the moment to spend the retainer fee). Founder does no public commentary for 12 hours while attorney and comms lead assess. |

**Rules that apply across all A2 tiers:**
- **Comms lead escalates to founder personally by phone (not Slack) the moment a P2 signal is confirmed.** Founder makes the P2-to-P3 decision. Founder + attorney make the P3-to-P4 decision jointly.
- **The founder personal accounts still do not quote-tweet, subtweet, or like anything.** The founder statement, if any, is a long-form LinkedIn post, not a series of replies.
- **Do not delete the brand account's first response** even if the situation escalates. Deletion looks like guilt. Follow-up statements supersede.
- **Screenshot cadence:** every 15 minutes during P2, every 5 minutes during P3, continuous during P4. Save with UTC timestamp to the legal file.
- **What NEVER happens, at any tier:** no threats, no name-calling, no personal attack on the Shark, no attempt to organize a counter-campaign, no engagement with the pile-on accounts individually. Statements only. Documented. Signed.

### Scenario B: A customer publishes a security concern about the offline claim

**Example:** A customer posts a thread on X or Hacker News: "I bought a Hearth and my traffic logs show it phoning home to a Cloudflare IP. So much for 'offline.'"

**Response protocol:**
- This is a five-alarm fire. Response within 4 hours, no longer.
- Engineering triage FIRST, response SECOND. Verify the claim internally before you comment. Do not deny before you know. Do not confirm before you know.
- Likely explanations (in order of probability): time sync (NTP), a legitimate check-for-updates ping that the customer opted into, an actual bug, a genuine security failure. Each has a different response.
- If the claim is legitimate (traffic is going somewhere the customer didn't opt into):
  - Public acknowledgment on the brand account within 4 hours.
  - Full written statement on hearth.com/statement within 24 hours.
  - Firmware patch within 5 business days.
  - Personal call from founder to the customer who reported it.
  - No NDA on the customer as a condition of the fix.
- **Never call the customer wrong on X.** Even if they are wrong. Take the conversation to email within one exchange.
- Comms lead drafts a "what we found" statement no matter the outcome. The statement is proactively published within 72 hours whether the finding is "we had a bug" or "here's the traffic and here's what it is." Transparency ends the story faster than defense.

**Pre-drafted acknowledgment (fill in the blanks):**

> A Hearth customer raised a question this morning about network traffic from their unit. We take that question seriously. Every Hearth ships offline-first, and any exception to that — such as a customer-enabled software update check — is one we should be able to describe precisely.
>
> Our engineering team is reviewing the reported traffic today. We'll publish what we find at hearth.com/statement by [date + time], regardless of what the finding is.

### Scenario C: A tech publication runs a hit piece

**Example:** The Verge or Ars publishes a 3000-word piece titled "The $95,000 AI Appliance for Rich People Who Are Scared of Amazon."

**Response protocol:**
- First hour: do nothing publicly. Read the piece three times. Highlight every factual claim and mark it accurate / inaccurate / debatable.
- Second hour: attorney reviews for defamatory statements. If nothing rises to that level (and it usually doesn't), the response is editorial, not legal.
- Same day: comms lead emails the reporter with a courteous factual correction request for any inaccurate claim. Attach documentation. Do not threaten. Do not CC the editor. First communication is one-to-one with the reporter.
- Within 48 hours: founder writes a LinkedIn response. NOT a rebuttal. A reframe.

**Founder LinkedIn response template:**

> [Reporter] at [Outlet] wrote a piece today about Hearth. It's not a piece I would have written — I disagree with the framing on [one specific point] and I think [one specific claim] is factually incomplete — but it's a piece that raises the honest questions any reader would raise about a $95,000 residential appliance.
>
> Here's what I want to say plainly:
>
> [Three-paragraph substantive response to the strongest critique in the piece. Concede what is fair. Push back on what is wrong. Ignore what is petty.]
>
> If you're a reader of [Outlet] and you're skeptical after that piece, my inbox is mark@hearth.com. I'll answer every question. That's the deal I make with anyone spending $95,000 on something we made.

**Rules on the LinkedIn response:**
- Do not attack the reporter personally. Ever.
- Do not tell the reader the piece is wrong overall. Concede where fair, push back where the facts are on your side, move on.
- Publish the LinkedIn response as an article, not a status update. Reason: articles get archived, indexed, and cited. Status updates disappear.
- Do NOT respond on X, only LinkedIn. X escalates; LinkedIn documents.

---

## 9. POST-CYCLE DEBRIEF — 90 DAYS AFTER AIR

### The founder's long-form retro
Publication target: 90-day mark, on the founder's LinkedIn or Medium, cross-posted to hearth.com/blog. Format: 3,500-4,500 words, one long piece. This is the piece that gets read in year two and year three by every future customer and investor doing due diligence.

### Outline

**1. Cold open — the moment the segment aired.**
Sensory. Not analytical. Two paragraphs on what the war room actually looked and felt like at 8:07 PM ET on air night. No numbers, no analysis, no self-congratulation. Just the room.

**2. Section 1: What Shark Tank actually is.**
What most first-time founders misunderstand about the format. The taping-to-air gap. The edit. The size of the audience relative to what founders expect (bigger). The staying power of the segment relative to what founders expect (shorter than they hope, longer than they fear).

**3. Section 2: What the segment did for the company.**
Concrete numbers, disclosed honestly. Deposit volume in the 72h window, in the 30d window. Refund rate. Press mentions. Investor conversations initiated. What percentage of those investor conversations turned into meetings, and what percentage of the meetings turned into anything meaningful. Real numbers.

**4. Section 3: What the segment did NOT do.**
- It did not sell out the first batch. (Or it did, and that's what we're saying honestly.)
- It did not turn the founder into a household name. Fame is not the outcome; category legibility is.
- It did not solve any product problem. Every product problem the founder had before taping is still a product problem after air.
- It did not shorten the timeline to profitability by a single day.

**5. Section 4: The three decisions the founder would make differently.**
Genuine. Not humble-brag. Real decisions with real trade-offs. Examples:
- "I would have said no to two of the six podcasts I did in the air week."
- "I would have hired a second support agent 30 days earlier."
- "I would have spent less energy on the Shark's team follow-up and more on the family-office pipeline I'd been ignoring."

**6. Section 5: What the six months between taping and air actually cost.**
The NDA is not free. The founder spent six months not saying the one true fact about their business. Cost: emotional, strategic, competitive. Value: the six months of build time. Was it worth it? Founder's honest answer.

**7. Section 6: What Hearth looks like 90 days after air.**
Ship rate, customer count, next batch reservation status, team size, cash position (approximate — you don't have to disclose exact numbers, but you can disclose direction). What the second product looks like. What the software roadmap looks like.

**8. Section 7: Advice to the founder who is about to tape.**
Ten specific things, written to that founder as if they were reading the piece on the plane to Los Angeles. Not "believe in yourself." Actual advice.

Examples:
- "The Sharks are not going to bring up the thing you're most worried they'll bring up. They will bring up the thing you have not thought about since prototype three."
- "Do not use the phrase 'this is a game-changer.' In the room, on air, in any interview, ever."
- "The single most useful hour of preparation is the hour where you rehearse being interrupted. Every substantive answer will be interrupted mid-sentence."

**9. Section 8: What comes next.**
Sober. Not a pitch. What the next 12 months look like. Where the company is going. What the founder is committing to.

**10. Closing — return to the sensory.**
Come back to the war room. Come back to what the room felt like at 8:07 PM. Land on the family. Land on the first customer taking delivery. Land on the fact that a company is still, at heart, one person deciding to spend twelve more months building the thing they were building.

### Publication protocol
- Draft by founder, edited by comms lead, legally reviewed for any financial disclosures.
- Published Tuesday morning, 8 AM ET. (Reason: Tuesday and Wednesday mornings get the highest LinkedIn engagement for long-form.)
- Simultaneously posted as a hearth.com/blog entry with canonical link back to LinkedIn.
- One-time notification to the 42-reporter list: "90-day retro from the founder — no ask, just a read if you're interested." Not a press release. Not a pitch. A courtesy.
- Founder does no interviews about the piece for the first 72 hours. Let the piece speak.

---

## APPENDIX A: THE CHECKLIST

Print this. Tape it to the war room wall.

**T-30 days:**
- [ ] All five press release variants drafted, legal-reviewed, uploaded to Business Wire drafts
- [ ] Interview crib sheet rehearsed with founder twice
- [ ] Reporter list built to 42 names with personal angles
- [ ] Server capacity provisioned to 10x baseline, load tested
- [ ] War room location booked
- [ ] HubSpot workflow AIR-NIGHT-DEPOSIT-CONFIRM built and tested
- [ ] Investor outreach lists finalized in HubSpot pipeline
- [ ] Refund policy published on hearth.com/reservations
- [ ] Customer support agent contract signed for 30 days coverage
- [ ] Brand-account TikTok handle claimed (whether or not activated)
- [ ] ABC social team contacted re: brand-account tag on official clip

**T-7 days:**
- [ ] Family briefed on air-night protocol
- [ ] Founder wardrobe laundered, laid out
- [ ] Warm-lead 90-person text list finalized on burner
- [ ] Two exclusive-embargo reporter briefings scheduled
- [ ] All social drafts loaded, not sent
- [ ] Attorney on-call schedule confirmed for T-0 through T+48h
- [ ] Reporter sheet re-scrubbed: every name is still on the beat

**T-24h:**
- [ ] Founder sleep 10 PM Saturday
- [ ] DNS TTL dropped to 60s
- [ ] PagerDuty verified with test page
- [ ] Business Wire scheduled drafts confirmed
- [ ] Backup static landing page ready to swap
- [ ] Deposit form final load test at 500 concurrent

**T-2h:**
- [ ] Founder in war room, phones on DND
- [ ] HubSpot workflow unpaused
- [ ] TV recording set up on two devices
- [ ] Water, snacks, tissues laid out

**T=0:**
- [ ] Silence. Watch.

**T+7 min:**
- [ ] Post 1 (X) sent
- [ ] Post 2 (LinkedIn) sent within 12 min
- [ ] Post 3 (Instagram) sent within 15 min
- [ ] Correct press release variant confirmed
- [ ] Business Wire release sent by T+20 min
- [ ] Reporter embargo emails released by T+25 min

**T+24h:**
- [ ] Overnight briefing printed on paper for founder
- [ ] First Tier 1 friendly interview complete
- [ ] Six back-to-back press calls scheduled and executed
- [ ] Deposit funnel snapshot reviewed with ops
- [ ] LinkedIn Day 2 post drafted by founder

**T+7 days:**
- [ ] Day 7 LinkedIn published
- [ ] All Tier 1 investor follow-up emails sent
- [ ] All Tier 2 investor emails sent
- [ ] Internal debrief scheduled for Friday

**T+90 days:**
- [ ] Founder long-form retro published Tuesday 8 AM ET
- [ ] 42-reporter courtesy note sent
- [ ] Full playbook post-mortem archived to `/docs/playbooks/shark-tank-2026-retro.md`

---

## APPENDIX B: INTERVIEW CRIB — COMMS-LEAD PREP ANNOTATIONS

This appendix is the comms-lead prep annotation on Section 3. It does **not** travel with the founder into an interview. It lives in the war-room binder and is used at T-14 days and T-3 days to rehearse the tone, then closed. The founder does not read the "Trap" line before answering a question — they read the answer, internalize it, and answer plainly.

### Q1. "Why did you go on Shark Tank?"
- **Trap:** frames the appearance as opportunistic self-promotion.
- **Pivot:** category creation, not personal brand.

### Q2. "Did you rehearse?"
- **Trap:** rehearsed = inauthentic. Not rehearsed = unprofessional. Both are losing answers.
- **Pivot:** to origin story, briefly.

### Q3. "What surprised you about the Sharks?"
- **Trap:** invites gossip. Any specific answer becomes tomorrow's headline.
- **Pivot:** what you learned, not who you liked.

### Q4. "What did the Sharks get wrong?"
- **Trap:** any answer here reads as bitter-loser.
- **Pivot:** the format, not the people.

### Q5. "Would you accept a deal from Kevin O'Leary?"
- **Trap:** on-record disparagement of a Shark, or embarrassment.
- **Pivot:** to seriousness of running the business, not personality.

### Q6. "You're a schoolteacher — is that a gimmick?"
- **Trap:** identity-loaded. Any defensive answer confirms the framing.
- **Pivot:** product decisions traceable to origin.

### Q7. "$95,000? Really?"
- **Trap:** invites defensive price justification. You will lose that fight.
- **Pivot:** roadmap without overpromising.

### Q8. "How is this not just a fancy Alexa?"
- **Trap:** category confusion. Reporters use this framing to bait a technical rant.
- **Pivot:** one clean contrast, no engineering deep-dive.

### Q9. "Are you going to compete with Apple or Amazon?"
- **Trap:** makes founder sound naive if answered "yes." Makes founder sound small if answered "no."
- **Pivot:** structural argument, not bravado. **Field note:** the current answer will get push-back from any reporter who follows platform strategy closely. Rehearse a second-follow-up: "So you're saying they *couldn't* build it? They obviously could." Founder answer: "They could build the hardware. They can't sell it without cannibalizing the business they've spent twenty years building. That's a strategy constraint, not an engineering one."

### Q10. "What happens if a customer gets hacked?"
- **Trap:** implies liability, sets up "sources say Hearth acknowledged security concerns."
- **Pivot:** the answer IS the security posture. Do not elaborate. Do not use words like "military-grade" or "unhackable."

### Q11. "Why is this made overseas?"
- **Trap:** nationalism. Invites either a dishonest answer or a defensive one.
- **Pivot:** craft, honesty about supply chain.

### Q12. "When can I actually buy one?"
- **Trap:** overpromise. Any specific date you can't hit is a lawsuit or a story in six months.
- **Pivot:** the URL, once.

### Q13. "Do you have investors already lined up beyond Shark Tank?"
- **Trap:** implies desperation if you say no; overpromises if you say yes.
- **Pivot:** discipline.

### Q14. "What's next after Hearth?"
- **Trap:** reveals unfocused founder.
- **Pivot:** focus.

### Q15. "What would you tell yourself before your Shark Tank taping?"
- **Trap:** emotional exposure. This is the question that becomes a viral clip if answered wrong.
- **Pivot:** none. This is the mic-drop. Let the pause happen.

---

*End of playbook. Every section is a document a director could execute against. Every variant is legally reviewable. Every question is rehearsable. No section requires the founder to invent something at 8:03 PM on air night.*

*Comms lead sign-off: __________________ Date: __________*
*Founder sign-off: __________________ Date: __________*
*Attorney sign-off: __________________ Date: __________*

# Hearth Competitive Intelligence Teardown
**Prepared for:** Data room / pitch-objection prep
**Version:** 1.1 — 2026-08-04

---

## 1. Categorical Map

Hearth occupies an empty quadrant. The luxury home market splits cleanly along two axes: **data locality** (offline vs. cloud) and **product breadth** (general-purpose AI companion vs. single-purpose media/control). Cloud + general-purpose is the crowded consumer quadrant (Alexa, Google, Apple). Cloud + single-purpose is the luxury dealer channel (Crestron, Control4, Josh.ai — all fundamentally cloud-augmented for anything non-trivial). Offline + single-purpose is the audiophile/videophile server world (Roon, Kaleidescape). **Offline + general-purpose AI at a luxury price point does not exist as a productized offering.** Home Assistant + Ollama exists as a DIY parts bin but is not a product: no industrial design, no warranty, no install, no personality layer, no single vendor to call in year four. Hearth is the first productized entry — and, to be precise, it is a pre-production entry: ~10 refundable deposits, zero delivered units at the time this document was written.

```
                        GENERAL-PURPOSE AI COMPANION
                                    ▲
                                    │
              Echo Show 15          │          ***HEARTH***
              Apple HomePod stack   │          (empty until now)
              Google Nest Hub Max   │          HA Yellow + Ollama DIY
                                    │          exists here as parts
      CLOUD-DEPENDENT ◄──────────────┼──────────────► FULLY OFFLINE
                                    │
              Josh.ai               │          Roon Nucleus Titan
              Crestron Home         │          Kaleidescape Strato
              Control4              │          Sonos (local playback only)
              Sonos Era 300         │
                                    │
                                    ▼
                        SINGLE-PURPOSE MEDIA / CONTROL
```

---

## 2. Head-to-Head Teardowns

### **Amazon Echo Show 15 (top-of-line) — Mass-market smart display**
- **Vendor + status:** Amazon Devices, shipped Dec 2021, refreshed Gen 2 (2023) with Fire TV integration. Amazon Devices HW org ~10,000 headcount, unprofitable division per repeated internal leaks.
- **Price at Hearth-adjacent config:** $279.99 base + $34.99 tilt mount + Alexa Voice Remote Pro at $34.99 = **~$350**. Multi-room requires 3–6 additional Echos (~$800–1,800 total).
- **What it actually does:**
  - 15.6" 1080p display, wall-mount kiosk form factor
  - Alexa voice + visual widgets (calendar, notes, photos)
  - Fire TV integration (Prime, Netflix, Disney+)
  - Video call via Alexa Communications
  - Ring/Blink camera dashboard
- **Cloud dependency:** Total. Every voice query round-trips to AWS. Alexa is effectively inert without internet. Photos come from Amazon Photos. Calendar sync via Google/Microsoft OAuth. Zero on-device intelligence beyond wake-word.
- **AI capabilities:** Alexa LLM ("Alexa+"), rolled out 2024, $19.99/mo for non-Prime and included with Prime. STT/TTS cloud. Wake-word on-device. Latency 800–1,500 ms typical.
- **Media stack:** Prime Video, Netflix, Hulu, Disney+. No Plex/Jellyfin/Roon native support. Sideload possible but unsupported. No local library concept.
- **Install / integration:** DIY, 20–40 minutes. Requires Amazon account, Wi-Fi, phone app.
- **Warranty + support:** 1-year limited, 30-day return. Chat/phone support, no SLA. Refurb replacement, not repair.
- **User base + brand cachet:** Estimated 3–5M Echo Show 15 units sold. Buyer archetype: middle-class kitchen wall, Prime household. Zero luxury signal.
- **Where it beats Hearth:** Price ratio ~270:1. Alexa skills ecosystem (100,000+). Ring/Blink integration is best-in-class for the $400 tier. Amazon logistics — next-day replacement.
- **Where Hearth beats it:** Everything a $5M+ liquid buyer cares about. Privacy (Amazon has multiple documented incidents of Alexa recordings reviewed by contractors, culminating in the 2023 FTC $25M COPPA settlement). Industrial design (plastic slab vs. sculpted metal enclosure with an OLED sphere on the roadmap). Family personality. Local media library. No subscription. White-glove install.
- **The exact Shark objection:** *"For four hundred dollars I can put an Echo Show in every room of my house. Explain to me why anyone pays two hundred seventy times that."*
- **Founder's reply:** *"The buyer we're selling to already has six Echoes and doesn't use them, because they don't want Amazon in the bedroom. Hearth is the answer to what happens when you're wealthy enough to reject the surveillance bargain. Echo is the product you tolerate; Hearth is the one you display."*

---

### **Apple HomePod + Apple TV 4K + Apple Vision Pro — Ecosystem stack**
- **Vendor + status:** Apple Inc., all shipping. Vision Pro launched Feb 2024; HomePod 2nd gen Feb 2023; Apple TV 4K (2022) still current at time of writing. Apple hardware revenue ~$300B.
- **Price at Hearth-adjacent config:** 2× HomePod ($299 ea) + Apple TV 4K 128GB ($149) + Vision Pro 512GB ($3,499) + AppleCare+ 2-yr (~$499) = **~$4,745**. Add HomePod minis for extenders ($99 ea).
- **What it actually does:**
  - Siri voice across HomePod + Apple TV + Vision Pro + iPhone
  - Apple Music, Apple TV+, iTunes library streaming
  - HomeKit hub (locks, cameras, thermostats)
  - Spatial video capture + playback on Vision Pro
  - AirPlay 2 multi-room
- **Cloud dependency:** Siri is cloud-primary (Apple Intelligence 2024+ runs some inference on-device with Private Cloud Compute for larger models). Apple Music streams from cloud. HomeKit runs locally but requires Apple ID cloud login. iCloud Photo Library is cloud.
- **AI capabilities:** Apple Intelligence (A17/M2+ only, released Oct 2024). On-device 3B-class model for simple tasks, Private Cloud Compute for larger. Siri STT partial on-device 2024+, TTS on-device. Latency 400–900 ms.
- **Media stack:** Apple TV+ / Apple Music / iTunes. No Plex/Jellyfin/Roon. Infuse/VLC sideload for third-party libraries. AirPlay 2 to Sonos, others.
- **Install / integration:** DIY, 1–2 hours across all devices. Vision Pro requires face/eye setup at an Apple Store recommended.
- **Warranty + support:** AppleCare+ optional, 2–3 years. Genius Bar / phone. No home visit.
- **User base + brand cachet:** HomePod ~15M units. Vision Pro 300–500k units through 2025 per triangulated JPMorgan and IDC estimates. Luxury signal moderate — Vision Pro yes, HomePod no.
- **Where it beats Hearth:** Ecosystem lock-in is the moat that matters. If the household is already 8-iPhone / 4-Mac / all Apple Music, the integration is unbeatable. Vision Pro spatial video is unique. Best-in-class privacy story for a cloud product.
- **Where Hearth beats it:** Apple has no equivalent to (a) a family-server media library that isn't iTunes-locked, (b) a per-family-member personality layer, (c) fully offline operation, (d) any physical presence beyond a smart speaker, (e) any Plex/Jellyfin support, (f) any concierge install. The relevant asymmetry is structural: Apple's ~$26B/yr Services line is built on iCloud storage, Apple Music, TV+, and AppleCare subscriptions — a fully-offline family appliance that replaces those revenue streams is not a product Apple is culturally incentivized to build.
- **The exact Shark objection:** *"My family lives in Apple's ecosystem. Why would I add a third-party box when Tim Cook is spending fifty billion a year on Apple Intelligence?"*
- **Founder's reply:** *"Because Apple Intelligence still requires an Apple ID, still sends your calendar to iCloud, and still has no answer for the family that wants their nineteen thousand home videos in one place without iCloud fees. Hearth complements the Apple household — AirPlay works, HomeKit bridges — and gives them the offline layer Apple structurally can't ship without cannibalizing its own services revenue."*

---

### **Josh.ai — Luxury voice control, dealer channel**
- **Vendor + status:** Josh.ai (Denver), founded 2015 by Alex Capecelatro. **~$28M total raised through Series B (2021)** per public reporting. Estimated 60–80 headcount. Dealer-only channel via CEDIA-certified integrators.
- **Price at Hearth-adjacent config:** Josh Core ($4,000–6,000 installed) + 6× Josh Nano microphones (**$1,800–2,200 each installed = $10,800–13,200**) + Josh Micro portable ($1,000–1,500 installed) + integration with Lutron/Sonos/etc. **Typical whole-house: $20,000–40,000 installed.**
- **What it actually does:**
  - Natural-language voice control for lighting, shades, HVAC, AV, security
  - Deep integrations: Lutron, Crestron, Control4, Savant, Sonos, Kaleidescape, Sony, SunBrite
  - Family voice profiles + privacy modes
  - Josh Nano ceiling-mount microphones tuned for luxury rooms
  - Josh Micro (portable speaker/mic)
  - Josh Core hardware appliance for the rack
- **Cloud dependency:** Voice processing is cloud (Josh's own cloud, not Amazon/Google). Josh has published a "privacy-first" positioning but STT and NLU generally require internet. Local fallback for basic commands only.
- **AI capabilities:** Proprietary NLU on top of Whisper-class STT (cloud). Announced GPT-class integration in 2024 ("Josh GPT") — cloud relay. Latency 500–1,200 ms.
- **Media stack:** No native media library. Controls third-party media (Kaleidescape, Sonos, Roon). Zero storage, zero playback engine.
- **Install / integration:** Dealer-only, CEDIA-certified integrators. 40–120 hours typical whole-house. Custom programming required.
- **Warranty + support:** 2-year hardware, dealer-mediated support. Josh does not directly support end users.
- **User base + brand cachet:** ~15,000–25,000 homes est. Buyer archetype: $3–15M home, existing Crestron/Lutron, wants a voice layer. Real luxury signal in CEDIA circles.
- **Where it beats Hearth:** Deep integration with existing luxury AV/lighting stacks Hearth doesn't touch at v1. CEDIA dealer network — 3,000+ certified installers vs. Hearth's zero at launch. Josh Nano ceiling mics look better in a coffered ceiling than any Hearth extender will. Josh ships Nano + Micro + Core hardware — this is a real hardware company with its own supply chain, not a pure software vendor.
- **Where Hearth beats it:** Josh does not run offline. Josh has no LLM companion with persistent memory, no per-user personality, no media server, no photo archive, no unified physical presence, no display, no local generative intelligence. Josh is voice-and-control on top of other people's boxes. Hearth is a whole product for a different job.
- **The exact Shark objection:** *"Josh already owns the luxury voice-control category and works with every dealer in America. You're a startup with no dealer network. How do you win?"*
- **Founder's reply:** *"Josh is a beautifully-designed voice layer that still routes to the cloud for anything non-trivial. When the internet drops, Josh degrades to lights-on/lights-off. We ship the whole product — voice, LLM, media, memory, presence — and none of it needs internet. We're not competing for the dealer's programming hours; we're the box the dealer installs alongside Josh, because the client asked why their five-million-dollar house stops responding when Comcast has an outage."*

---

### **Crestron Home — Whole-house control system**
- **Vendor + status:** Crestron Electronics (private, NJ), founded 1971. Estimated $1.5–2B revenue, ~4,500 employees. Dealer-only, CEDIA-certified.
- **Price at Hearth-adjacent config:** CP4 processor ($3,500) + 10× TSW-1070 touchpanels at **realistic $2,500–3,500 dealer-installed each ≈ $30,000** + DM-NVX AV routing (~$25,000) + programming ($15,000–30,000) + install (~$20,000). **Typical whole-house: $75,000–200,000.**
- **What it actually does:**
  - Whole-house control — lighting, shades, HVAC, AV, security, pool, gate
  - AV distribution over DM-NVX (4K60 4:4:4 HDR)
  - Touch panels in every room, physical keypads
  - Custom programming per house — every button hand-coded
  - Enterprise-grade reliability
- **Cloud dependency:** Local processor, but Crestron Home OS phones home for updates. Voice integration (via Alexa/Google/Josh) is cloud. Remote support via Crestron XiO cloud.
- **AI capabilities:** None native. Voice is bolt-on. No LLM, no personality.
- **Media stack:** Distributes AV, does not source it. Requires Kaleidescape/Roon/Apple TV/Plex/etc. behind it. Crestron is the switchboard, not the library.
- **Install / integration:** Dealer-only, mandatory. 80–400 hours programming. Every project is bespoke.
- **Warranty + support:** 3-year standard on processor, 2-year on panels. Dealer-mediated. TrueBlue support tier ($ premium).
- **User base + brand cachet:** ~100,000+ Crestron Home installs. Buyer archetype: $5M–$50M homes, yachts, jets. Deep dealer moat. This is the reference luxury standard.
- **Where it beats Hearth:** Category-defining. If a wealthy buyer wants one box that runs lighting + shades + HVAC + security + pool + AV routing, Crestron does that and Hearth does not. Dealer network is 40 years deep.
- **Where Hearth beats it:** Crestron has no AI, no personality, no media library, no photo archive, no offline LLM. Crestron programming is a $30K+ bill of labor per house; Hearth is a $95K appliance delivered configured. Crestron feels like 2005; Hearth feels like 2035.
- **The exact Shark objection:** *"For the same money the buyer gets Crestron Home which does forty times more — lighting, shades, security, AV routing. You do voice and media. Why isn't this Crestron's tenth SKU?"*
- **Founder's reply:** *"Crestron will never build this because their business model is dealer programming hours — an appliance that works out of the box destroys their channel. That's why the category is empty. Hearth is not a Crestron replacement; it's the box the Crestron dealer sells alongside Crestron because the client wanted a companion, not a control system."*

---

### **Control4 (Snap One → Resideo) — Mid-luxury control system**
- **Vendor + status:** Snap One (formerly public, NASDAQ:SNPO). Resideo announced the acquisition **April 2024** and **closed the deal June 2024** for ~$1.4B, taking Snap One (and thus Control4) private. Control4 originally acquired by Snap One in 2019. ~1,500 employees.
- **Price at Hearth-adjacent config:** CA-10 controller ($1,800) + 6× T4 touchpanels ($1,200 ea = $7,200) + Halo remote ($500) + programming + install. **Typical whole-house: $25,000–70,000.**
- **What it actually does:**
  - Same category as Crestron but 30–50% lower price point
  - Lighting, AV, security, HVAC control
  - Dealer-installed via CEDIA channel
  - Composer Pro programming (proprietary)
  - OS3.4 with wellness/scenes/voice
- **Cloud dependency:** Local controller, cloud for remote access + firmware. Alexa/Google integration cloud.
- **AI capabilities:** None native. Bolt-on voice.
- **Media stack:** Distributes, doesn't source. Integrates with Roon, Sonos, Kaleidescape, Plex.
- **Install / integration:** Dealer-only. 40–120 hours.
- **Warranty + support:** 2-year standard, extended plans dealer-mediated.
- **User base + brand cachet:** ~500,000+ homes globally. Buyer archetype: $1–5M homes, upper-middle luxury. Less prestige than Crestron.
- **Where it beats Hearth:** Same as Crestron — actual whole-house control. Bigger dealer base than Crestron. Better price/feature ratio.
- **Where Hearth beats it:** Same as Crestron. Plus: Control4 now sits under Resideo, a mass-market brand — the luxury cachet is eroding under the new parent.
- **The exact Shark objection:** *"Control4 already sells to the same dealers you'd need. Why don't they add an LLM and eat you?"*
- **Founder's reply:** *"Resideo just closed on them for one-point-four billion in June — they are optimizing for Home Depot channels, not for the five-million-dollar buyer. And even if they added an LLM tomorrow, it would be cloud, because their entire OS is built on remote access. Hearth's whole thesis is that offline is the product."*

---

### **Sonos Era 300 + Sonos multi-room — Audiophile-adjacent multi-room**
- **Vendor + status:** Sonos Inc. (NASDAQ:SONO), founded 2002. ~$1.5B revenue trailing four quarters, ~1,500 employees. Public and turbulent — 2024 app rewrite fiasco wiped hundreds of millions from market cap and forced a CEO transition.
- **Price at Hearth-adjacent config:** 6× Era 300 ($449 ea = $2,694) + Arc Ultra soundbar ($999) + Sub 4 ($799) + Sonos Amp for wired zones ($699) = **~$5,200**. No install fees, DIY.
- **What it actually does:**
  - Multi-room wireless audio (Wi-Fi + Sonos mesh)
  - 30+ streaming service integration (Spotify, Apple Music, Tidal, Amazon)
  - Dolby Atmos Music via Era 300
  - Voice via Sonos Voice Control (limited), Alexa, or Google
  - Sonos app (post-rewrite, still stabilizing)
- **Cloud dependency:** Streaming is cloud (music services). Sonos accounts are cloud. Local library playback via Plex/Roon/DLNA works offline. Voice cloud.
- **AI capabilities:** Sonos Voice Control is on-device for basic music commands only. No LLM. No general-purpose AI.
- **Media stack:** Audio-only. No video. Roon Ready, Plex-friendly, Tidal Connect, Spotify Connect, AirPlay 2.
- **Install / integration:** DIY, 30–90 min. No dealer required (though some do install).
- **Warranty + support:** 1-year limited, 45-day return. Phone/chat, no SLA.
- **User base + brand cachet:** ~15M households. Buyer archetype: audiophile-adjacent middle-upper class. Brand cachet damaged by the 2024 app rollout and legacy-device sunset controversies.
- **Where it beats Hearth:** Sonos audio quality per dollar is best-in-class in the mass market. Every streaming service integrates. The mesh works. If the buyer only wants music, Sonos wins.
- **Where Hearth beats it:** Sonos is audio-only. No video, no library, no AI, no display, no companion, no photos. Sonos is a subset — it should sit *inside* Hearth's stack (and does, via AirPlay/DLNA).
- **The exact Shark objection:** *"Sonos does multi-room for five grand. Why would anyone pay ninety more for the same speakers with a chatbot?"*
- **Founder's reply:** *"Because Sonos is speakers. Hearth is speakers plus the family's memory, the family's LLM, the family's video library, and a physical presence in the room that says 'this house is intelligent.' We AirPlay to the buyer's existing Sonos on day one — we're additive, not replacing."*

---

### **Roon Nucleus Titan + audiophile stack — Audiophile-first media server**
- **Vendor + status:** Roon Labs (acquired by Harman/Samsung 2023). Nucleus Titan launched Oct 2024. ~40 headcount at Roon.
- **Price at Hearth-adjacent config:** Nucleus Titan server ($13,995) + Roon Ready DAC (dCS Bartók APEX $25,000 or Wadax Reference $150,000) + Roon subscription ($14.99/mo or $829 lifetime) + streamer/endpoints (Aurender, Grimm) $10,000–40,000. **Practical audiophile stack: $50,000–200,000.**
- **What it actually does:**
  - Roon library management + streaming service overlay (Tidal, Qobuz)
  - Best-in-class metadata + album art + credits
  - DSP room correction, headphone crossfeed
  - Multi-zone bit-perfect distribution to Roon Ready endpoints
  - RAAT protocol (proprietary uncompressed streaming)
- **Cloud dependency:** Library is local on Titan. Roon core requires occasional cloud auth. Metadata is cloud-fetched. Tidal/Qobuz streaming is cloud.
- **AI capabilities:** Roon Radio recommendation engine (not LLM). No voice, no companion, no chat.
- **Media stack:** Audio only. Best-in-class for audio. No video whatsoever.
- **Install / integration:** DIY-capable but Sonic Frontiers / Music Direct / dealer install typical. 4–20 hours + room correction tuning.
- **Warranty + support:** 2-year Roon hardware. Roon Labs support forum + email.
- **User base + brand cachet:** ~200,000+ Roon subscribers. Buyer archetype: serious audiophile, $5K–$500K audio system. Real prestige in the audiophile world; unknown outside.
- **Where it beats Hearth:** Nothing in the world touches Roon for audiophile audio management. If the buyer has a Wadax DAC, Hearth cannot compete on audio quality. Metadata layer is 15 years deep.
- **Where Hearth beats it:** Roon is audio only. No video, no LLM, no companion, no photos, no display, no smart-home. Roon requires a subscription forever. Hearth's roadmap includes Roon-Ready output so the audiophile household runs both.
- **The exact Shark objection:** *"A serious audiophile already spent fifty grand on a Roon + Wadax stack. Your $95K is a tenth compute cluster and a floating ball — where's the audio credibility?"*
- **Founder's reply:** *"We don't compete with Wadax and we don't want to. Hearth ships Roon-Ready on the output — it feeds their DAC bit-perfect. We're selling the room the audiophile's spouse also uses. She doesn't want a Wadax; she wants a companion that remembers her mother's birthday and shows her the grandkids' videos when she asks."*

---

### **Home Assistant Yellow + local LLM stack — DIY / free alternative**
- **Vendor + status:** Nabu Casa (parent of the Home Assistant OSS project). Yellow launched 2022, HA Green (cheaper) launched 2023. ~50 headcount. Home Assistant is the reference for DIY smart home.
- **Price at Hearth-adjacent config:** HA Yellow ($199 + CM4 module ~$150 = $349) + Ollama-capable box (Framework Desktop with Ryzen AI Max+ 395, 128GB unified memory, ~$2,500) + Home Assistant Voice Preview Edition ($59 × 6 = $354) + Whisper/Piper local + Wyoming protocol. **Total parts: $3,200–4,500. Plus 40–200 hours of your own labor.**
- **What it actually does:**
  - Full local smart-home hub (Zigbee, Z-Wave, Matter, Thread)
  - Local voice via Home Assistant Voice PE + Whisper + Piper + Ollama
  - LLM integration (any Ollama model — Llama 3.3 70B, Qwen 3, etc.)
  - Full automation engine, dashboards (Lovelace)
  - No cloud dependency if configured that way
- **Cloud dependency:** Zero required. Optional Nabu Casa Cloud ($6.50/mo) for remote access.
- **AI capabilities:** Whatever Ollama model you install. Llama 3.3 70B runs on Framework Desktop at ~15 tok/s. Whisper large-v3 STT, Piper TTS, all local. Latency 800–3,000 ms depending on hardware.
- **Media stack:** None native. Add Plex/Jellyfin/Emby yourself on the same or separate box.
- **Install / integration:** Pure DIY. 40–200 hours real. Every device integration is a config file.
- **Warranty + support:** None (community forum). Nabu Casa Cloud subscription includes email support.
- **User base + brand cachet:** ~500,000+ HA installs. Buyer archetype: technical, DIY, values control over convenience. Zero luxury signal.
- **Where it beats Hearth:** Cost ratio ~25:1. Extensibility infinite. Community of 100,000+ contributors. Privacy is genuine — code is open source. If the buyer has a technical family member, HA does 80% of Hearth for 4% of the price.
- **Where Hearth beats it:** HA has no industrial design, no physical presence, no warranty, no install, no personality layer as a product, no white-glove, no unified experience. A $5M+ liquid buyer does not spend 200 hours configuring YAML. HA is a hobby; Hearth is a possession.
- **The exact Shark objection:** *"A twelve-year-old on YouTube has a video showing how to do all of this with Home Assistant and a Framework Desktop for four thousand dollars. Your entire product is a design tax."*
- **Founder's reply:** *"The buyer who would spend two hundred hours on YAML doesn't have five million liquid, because they're spending their time on YAML. The buyer we sell to values their time at a thousand dollars an hour and their family's privacy at any price. Ninety-five thousand dollars is twelve days of their billed time to get a beautiful, warrantied, installed answer instead of a hobby."*

---

### **Kaleidescape Strato V + Terra — Luxury media-first server**
- **Vendor + status:** Kaleidescape (Mountain View), founded 2001. Relaunched from bankruptcy in 2016 under new ownership. ~80 headcount. Dealer-only via CEDIA.
- **Price at Hearth-adjacent config:** Strato V player ($4,995) + Terra 48TB server ($20,995) or Terra 88TB ($30,995) + movie downloads ($15–40 each, avg $25 × 200 = $5,000). **Typical config: $30,000–55,000 hardware + $5–15K library.**
- **What it actually does:**
  - Reference-quality 4K UHD movie playback (higher bitrate than any streaming service)
  - Kaleidescape Movie Store — 15,000+ titles, own-not-rent model
  - Bit-perfect Dolby Atmos + Vision + HDR10+
  - Multi-zone playback (up to 8 Stratos from one Terra)
  - Bookmark sync, curated collections, custom scenes with control systems
  - **Personal content:** import tooling for the buyer's own video files, plus an authorized-dealer disc-to-vault ripping program for physical Blu-ray/DVD they already own
- **Cloud dependency:** Movie Store is cloud (download once). Playback is fully local after download. Account auth is cloud but playback offline.
- **AI capabilities:** None. Zero. Not a voice product, not an AI product.
- **Media stack:** Video-first, with imported personal video supported. No audio-only tier, no photo archive.
- **Install / integration:** Dealer-only. 8–24 hours. Integrates with Crestron, Control4, Josh.ai.
- **Warranty + support:** 1-year standard, 3-year extended via dealer. Kaleidescape Concierge included.
- **User base + brand cachet:** ~50,000–70,000 systems. Buyer archetype: dedicated home theater owners, $10M+ homes, $50K+ theater rooms. Highest cachet in videophile luxury.
- **Where it beats Hearth:** Reference video quality Hearth cannot match on day one. Movie Store licensing gives access to titles Plex doesn't have legally. Theater integration is best-in-class. This is the videophile luxury standard.
- **Where Hearth beats it:** Kaleidescape does not do audio streaming, family photos, AI, voice, or companion. Its personal-content import path exists but is far more constrained than a general Plex/Jellyfin/Immich stack — and it explicitly does not do LLMs, per-user personality, or any of Hearth's non-video jobs.
- **The exact Shark objection:** *"For fifty grand less than Hearth, Kaleidescape gives me true reference cinema in every room. Media is what my buyer actually wants."*
- **Founder's reply:** *"Kaleidescape is the gold standard for cinema, and we don't try to be that — we ship Kaleidescape-compatible integrations and let their box do what it's best at. Our buyer also has thirty thousand family photos, fifteen years of home video, and a nine-thousand-track FLAC collection they ripped in 2008 — plus they want an AI companion Kaleidescape has publicly said they'll never build. We're additive to a Kaleidescape household, not a replacement for it."*

---

### **Custom Ryzen server + Home Assistant + Ollama build ($12k parts + $5k integrator)**
- **Vendor + status:** Not a vendor — a stack. Typical build: Framework Desktop 128GB or custom Threadripper 7960X + 128GB DDR5 + 4× 20TB Enterprise HDD + 2× RTX 5090 (32GB VRAM ea) + TrueNAS Scale + HA Yellow + Ollama. Integrator: local A/V dealer or freelance Linux consultant.
- **Price at Hearth-adjacent config:** Server parts ~$12,000. Integrator labor 30–60 hrs @ $150–200/hr = $4,500–12,000. **Realistic total: $16,000–24,000.**
- **What it actually does:**
  - Local LLM inference (Llama 3.3 70B or Qwen 3 235B quantized at 20–40 tok/s on dual 5090)
  - Plex + Jellyfin + Immich + Audiobookshelf + Home Assistant
  - Whisper + Piper voice, custom wake-word
  - 60–80TB usable media storage
  - Full offline operation
- **Cloud dependency:** None if configured that way.
- **AI capabilities:** Whatever the buyer picks. Genuinely comparable raw capability to Hearth's compute cluster on paper.
- **Media stack:** Full DIY — every service the buyer wants.
- **Install / integration:** Integrator programs it once. Ongoing maintenance falls to the buyer or a $200/hr consultant on retainer.
- **Warranty + support:** Component-level warranties (AMD 3yr, Samsung 5yr, Seagate 5yr). No system warranty. When a drive fails at 2am, the buyer calls the integrator or replaces it themselves.
- **User base + brand cachet:** Unknown — thousands of self-built setups exist, no product identity. Zero luxury signal.
- **Where it beats Hearth:** Cost ratio 4–6:1. Fully upgradable — swap GPUs in three years. Open-source stack — no vendor risk. Ryzen AI Max+ 395 or dual 5090 rivals Hearth's 20-SBC cluster on raw tok/s.
- **Where Hearth beats it:** No industrial design, no companion presence, no personality layer, no unified UX, no warranty, no white-glove, no 5-year commitment. When a drive fails, the buyer's family loses the media library until the integrator responds. When the integrator retires, the buyer is stranded. Hearth is a product; this is a project.
- **The exact Shark objection:** *"This is the killer. I can buy the exact same technical capability from a local integrator for twenty grand. You're marking up eighty percent for industrial design."*
- **Founder's reply:** *"We're marking up for three things the integrator can't sell: an original animated companion face that makes it a piece of furniture instead of a rack in the basement, a three-year concierge warranty where we ship a replacement in 48 hours, and a company that will still exist in 2035 to support the firmware. The integrator will retire. The Ryzen won't get updates. Hearth is the answer to 'who do I call in year four?' — and that answer is worth seventy-five thousand dollars to a person with five million liquid."*

---

## 3. Feature Comparison Matrix

**Split into two tables to distinguish shipping capability from roadmap capability. This distinction is load-bearing: Hearth is pre-production, and several of its differentiators are engineered but not yet in customer hands.**

**Legend:** ✅ PASS · ◐ PARTIAL · ✗ FAIL · ⊘ N/A · ? UNKNOWN

### 3a. Shipping today (Hearth v1.0 pilot target 2027 Q2)

| Product | Price (Hearth-config) | Offline AI | Multi-room stream | Media library | Family photo+video archive | No cloud required | White-glove install | Warranty | Extenders | 5-yr firmware commit |
|---|---:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **Hearth v1.0** | $95,000 | ✅ | ✅ | ✅ (Plex/Jellyfin/ABS) | ✅ (Immich) | ✅ | ✅ | 3yr | ✅ $8,999 | ✅ |
| Echo Show 15 | $350 | ✗ | ◐ | ✗ | ◐ Amazon Photos | ✗ | ✗ | 1yr | ⊘ | ✗ |
| Apple HomePod+ATV+Vision | $4,745 | ◐ on-device AI | ✅ AirPlay 2 | ◐ iTunes only | ◐ iCloud | ✗ | ✗ | 1yr (2yr AC+) | ⊘ | ? |
| Josh.ai | $20–40k | ✗ | ⊘ (controls Sonos) | ✗ | ✗ | ✗ | ✅ dealer | 2yr | ⊘ (Nano/Micro) | ? |
| Crestron Home | $75–200k | ✗ | ✅ DM-NVX | ✗ (routes it) | ✗ | ◐ mostly local | ✅ dealer | 3yr | ✅ touchpanels | ✅ |
| Control4 | $25–70k | ✗ | ✅ | ✗ | ✗ | ◐ | ✅ dealer | 2yr | ✅ | ? |
| Sonos Era 300 stack | $5,200 | ✗ | ✅ | ◐ local NAS ok | ✗ | ◐ playback yes | ✗ | 1yr | ⊘ | ✗ |
| Roon Nucleus Titan stack | $50–200k | ✗ | ✅ RAAT | ✅ audio only | ✗ | ◐ | ◐ dealer optional | 2yr | ⊘ | ? |
| HA Yellow + Ollama DIY | $3.2–4.5k | ✅ | ◐ DIY | ◐ DIY Plex | ◐ DIY Immich | ✅ | ✗ | none | ⊘ | ✗ |
| Kaleidescape Strato V | $30–55k | ✗ | ✅ video | ◐ K-store + import | ✗ | ◐ playback yes | ✅ dealer | 1–3yr | ✅ Stratos | ✅ |
| Custom Ryzen + Ollama | $16–24k | ✅ | ◐ DIY | ✅ DIY | ✅ DIY | ✅ | ◐ integrator | component | ⊘ | ✗ |

### 3b. Hearth roadmap (post-v1.0; explicitly not shipping at pilot delivery)

| Roadmap capability | Hearth target | Nearest analog today |
|---|---|---|
| Per-user personality layer (family-member-tuned LLM) | v1.1 (2027 Q3) | None shipping — Alexa Voice ID + Siri Voice ID exist for identification, not for a tuned generative personality |
| Levitating OLED sphere physical presence | v1.5 (~2028 Q2), engineering prototype only at pilot ship | Flyte and Levitera ship consumer levitation objects; no shipping product combines OLED + wireless-power + Halbach in the way Hearth targets |
| Household-wide voice ID with per-user memory graph | v1.1 | Alexa Voice ID (shallow), Siri Voice ID (shallow), Josh voice profiles (permissions, not memory) |
| Roon-Ready audiophile output | v1.2 | Native to Roon Nucleus, licensable |
| Native Crestron/Control4/Josh integration modules | v1.3 | The incumbents own these ecosystems |

**Reading:** Hearth v1.0 wins on offline AI + media library + family archive + no-cloud + white-glove + warranty + extenders + 5-year firmware commit simultaneously — a combination none of the incumbents ship. But the two most emotionally-differentiating features (per-user personality, levitating sphere) are aspirational at v1.0 pilot and must not be sold as shipping features in a data-room diligence conversation. Positioning them as shipping is the single fastest way to fail associate-level diligence.

---

## 4. The Competitor Hearth Actually Loses To

**Hearth loses to Crestron Home + Josh.ai + Kaleidescape stacked together in the $50M+ ultra-luxury home segment.**

**The buyer:** A $50M+ liquid net worth household building or renovating a $15M+ estate with an active CEDIA integrator on the project. They've already committed to Crestron for lighting/shades/HVAC/AV routing and Kaleidescape for the theater. Josh.ai sits on top as the voice layer.

**Why Hearth loses here:** These buyers don't buy appliances — they buy dealer relationships. The integrator has been programming Crestron for 15 years, has a service contract, and will not recommend an unknown startup as the AI companion because it introduces a support risk they can't underwrite. In this segment the dealer, not the buyer, chooses the SKU list.

**The boundary — where we don't compete and that's fine:**
- Homes over $15M new construction with a general contractor + CEDIA integrator on retainer
- Buyers who define "luxury" as "the dealer handles everything"
- Households where the AV rack already fills a 12U enclosure and adding another box is architecturally hostile

**Where we do win in that same wealth tier:**
- The buyer's second home, mountain cabin, or beach house where they didn't hire an integrator
- The buyer's adult children's houses ($3–8M, no dealer relationship)
- Existing Crestron households where the buyer became annoyed that "Alexa, play the Beatles" still requires Amazon
- The next-generation buyer (35–50) who grew up on iPhone and finds Crestron's UI insulting

**Rough TAM implication:** The $50M+ ultra-luxury addressable is ~15,000 US households. We concede half — 7,500. The $5–50M liquid tier is ~700,000 households (per Cerulli / Spectrem 2024). We only need 1–2% of that tier for a $650M–$1.3B revenue business. We're not fighting Crestron for the estate; we're fighting the Sharks' assumption that the estate is the only luxury market.

---

## 5. Moat Table

Now with a fifth column: the well-capitalized Series-A hardware startup that is the actual 18-month risk. Amazon and Apple are structurally slow. Josh is capacity-constrained. The real threat is a Framework-caliber hardware team with $30–50M, an open-weights model, and a white-glove partner — imagine a Nothing-style industrial-design house teaming with a boutique AV integrator. Every claim below is evaluated against that entrant, honestly.

| Hearth claim | Amazon 12mo? | Apple 12mo? | Josh.ai 12mo? | Series-A entrant ($30–50M, 18mo)? | Legal moat | Time-to-parity (well-capitalized) |
|---|---|---|---|---|---|---|
| **Offline-only architecture** | **N** — Alexa's business model is ad-attributable voice queries; going offline destroys the LTV curve. Amazon has repeatedly killed offline Echo internally per leaked docs. | **N in 12mo** — Apple Intelligence has an on-device path but Private Cloud Compute is the strategy. Fully-offline would cannibalize iCloud/Music/TV+ services revenue (~$26B/yr). Culturally hard in 12–24mo. | **N** — Josh's entire NLU stack is cloud. Rewriting to local would take 18mo and dismantle their current model-licensing economics. | **Y** — Open-weights (Llama 3.3, Qwen 3, DeepSeek) run acceptably on Framework Desktop-class hardware today. A Series-A team ships this in 12–18mo. | None (approach, not IP) | 12–18 months for a dedicated startup; 24–36+ months for Amazon/Apple due to business-model conflict |
| **Luxury industrial design (sculpted enclosure + companion presence)** | **N** — Amazon Devices has never shipped a $1,000+ home product. Design DNA is Bezos-era "cheap and cheerful," though Astro (2021) shows they'll ship weird premium hardware if the strategy demands it. | **Y in principle** — Apple could obviously do this. But wouldn't at $95K — HomePod strategy is $299 mass-market. | **Y** — Josh has decent ID (Nano, Micro). Could contract an Ammunition-caliber ID firm and ship a premium enclosure in 12mo. | **Y** — This is the entrant's easiest win. Nothing/Teenage Engineering/Fuseproject-style ID + a boutique CM ships luxury industrial design in 9–12 months. | Trade dress once shipped; design patents on enclosure + mount pending. Meaningful but not category-defining. | 9–12 months for a competitor with a top-tier ID partner |
| **20-SBC compute cluster** | **Y** — Amazon runs the largest silicon fleet on earth. Could clone the topology in 6mo if they cared. Astro proves they'll ship it when there's a reason. | **Y** — Apple Silicon M-series clusters trivially. Mac Studio Ultra already exceeds our tok/s on inference. Culturally won't ship at a home-appliance form factor. | **N** — Josh has no hardware manufacturing at Hearth's cluster scale, no supply chain for 20-SBC boards. Would need to acquire capability. | **Y** — Framework Desktop Ryzen AI Max+ 395 at 128GB is a single-box answer with comparable practical throughput. The entrant doesn't need to match the cluster topology; they only need to match the delivered tokens/sec. | None (commodity approach); custom PCB IP defensible but not category-defining | 6–9 months technically for any well-funded entrant willing to accept the BOM |
| **Original animated companion face / (roadmap) OLED sphere with Halbach levitation** | **N in 12mo for the sphere** — Amazon has no magnetic-levitation engineering team; would need to acquire or license. | **N in 12mo for the sphere** — Apple could, culturally won't at Hearth's price. Also patent-encumbered by existing Halbach + wireless-power IP holders. | **N** — Josh has no HW engineering for mechanical products. | **Y for the sphere in 12–18mo** — Flyte, Levitera, and academic groups (MIT, ETH Zürich publications on Halbach + wireless power) have prior art going back over a decade. A competent hardware team with a competent patent attorney can design around Hearth's pending applications. | Trade dress + design patents once shipped; utility applications pending. Real IP is on system integration and supplier relationships, not on the physics of Halbach levitation itself. **This is a trade-dress + integration + supplier-relationship moat, not a fundamental-physics moat.** | 12–18 months for a Series-A entrant with a competent IP attorney; the physics is public and the parts are commodities |
| **Personality-per-family-member** | **Y technically** — Alexa Voice ID exists. Shallow — no persistent per-user memory graph. Full parity in 12mo requires rebuilding the memory layer, which Amazon announced with Alexa+ (2024) but under-shipped. | **Y technically** — Siri Voice ID exists. Cultural resistance to per-user tuned generative personalities (privacy / child-safety board fights). Realistic in 18mo. | **N** — Josh has voice profiles for permissions, not per-user LLM personalities. Would need to license an LLM stack. | **Y in 12–18mo** — Open-weights + LoRA per user is the entrant's easiest software moat to replicate. There is no defensive IP here. | Software approach — weak legal moat. Data moat (family memory graphs accumulated over years of customer ownership) is the real moat, and Hearth doesn't have it yet — it accrues with time-in-service, and at v1.0 pilot Hearth has zero years of it. | 12–18 months for the software; 5+ years for the data moat, and only after Hearth actually retains customers that long |
| **3-year concierge warranty + white-glove install** | **N** — Amazon does not do concierge at any price. Cultural mismatch with Devices ops. | **Y** — Apple could via Apple Store Business. Cultural mismatch — HomePod is not white-gloved today. | **Y** — Josh already dealer-installs. Could extend warranty terms in 12mo. This is where Josh is closest. | **Y** — A white-glove partner (boutique AV integrator on retainer, or a Sonos-of-Everest-style service partner) delivers this. Not defensible against a well-capitalized entrant. | None (operational moat, not legal) | 6–12 months operationally for anyone willing to spend on the ops build |

**Summary read for the Sharks (honest version):** Amazon won't (business model). Apple could but won't (services cannibalization). Josh could partially but lacks the hardware capability at scale. **The real 18-month risk is a well-capitalized Series-A entrant that pairs open-weights software, Framework-class hardware, luxury industrial design, and a boutique integrator partner. That entrant could match Hearth's shipping-day v1.0 feature list in 12–18 months.** Hearth's durable advantages are (1) first-mover with the productized answer, (2) a defensible trade-dress + supplier-relationship + integration moat, (3) an accumulating data moat that only compounds if we keep customers past year three, and (4) speed of execution. The moat is not physics — it is category ownership plus operational depth, and category ownership is only durable if we ship well and fast.

---

## 6. Positioning Statement

Hearth is the first productized offline family-AI + media appliance — a fully local companion, media library, and memory archive, white-glove installed at a luxury price point.

*(25 words. Pre-production; ~10 refundable deposits at time of writing; pilot delivery target 2027 Q2. Not sold as "shipping" until units are in customer homes.)*
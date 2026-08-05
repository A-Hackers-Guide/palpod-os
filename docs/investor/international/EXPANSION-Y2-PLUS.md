# Hearth International Expansion Plan — Y2+ (2028 onward)

**Document owner:** Head of International, Hearth Inc.
**Data room location:** `/data-room/international/expansion-plan-v2.md`
**Feeds:** Series B pitch (TAM story), Board deck Q4 2027, dealer program collateral
**Supersedes:** v1.0 (Y2 target and dealer list corrected per Q4 2027 verifier pass)

---

## 1. Executive Summary

Hearth enters international markets in Y2 (2028) on a staged, English-first, EU-second, Gulf-and-Asia-third cadence. The Y1 US-only ship of ~200 units in Q4 2027 gives us the reference installations, service data, and concierge playbook we need to defend a $95k product against European luxury AV incumbents (Bang & Olufsen, Steinway Lyngdorf) and Gulf palace-tech integrators. Y2 opens with the UK + Ireland in Q1 2028 (English-language, UKCA cert derivable from FCC filings, deepest LAI channel in Europe), followed by Germany + Austria + Switzerland in Q2 2028 (paired German-language investment across three markets), then France-adjacent Benelux plus Italy in Q3 2028. UAE + Singapore dealer programs launch in Q4 2028, but first customer sale slides to Q1 2029 — the honest revision after re-scoping TDRA/ESMA/SABER-adjacent onboarding against realistic 90-day luxury sales cycles from a cold-launched channel. Y3 (2029) adds France, Australia, Hong Kong, and Israel. Y4+ (2030) adds Saudi Arabia, Spain, Portugal, and the Nordic adjuncts. Y5+ (2031) opens Japan feasibility.

Our Y2 international revenue target is **$3.4M** on 60 units (approximately 28% of Y2 blended revenue growth), climbing to **$8M in Y3** and **$18-22M in Y4**. This is a deliberate down-revision from the v1 plan's $4.5M / $10M targets: three quarters of selling into a cold five-dealer German network at four closes per dealer per quarter, with no reference installs in-market, was not defensible against luxury sales-cycle benchmarks. UAE and Singapore first-sale slipping from Q4 2028 to Q1 2029 acknowledges that palace-tech close cycles run 6-9 months when the buyer wants to see a working installation before committing $250k+ of household disruption. The founder thesis remains threefold and honest: (1) luxury goods travel — a $95k sculptural OLED sphere with Halbach levitation reads as jewelry-grade design in any market that already buys Bang & Olufsen Beolab 90 or Steinway Model D; (2) the concierge model travels because HNW households in London, Zurich, Dubai, and Singapore already expect white-glove for anything above $50k, and our LAI channel partners already run concierge programs we can layer onto; (3) the wake-word and voice presets do NOT travel — every non-English market requires $150-240k of language engineering per locale before first unit ships, and this is the gating constraint on our rollout tempo. The offline claim, meanwhile, is a genuine European selling point — GDPR narrative is dramatically simpler when only 7 defined egress classes ever leave the household perimeter (per THREAT-MODEL.md), which converts a US privacy differentiator into a European regulatory moat.

---

## 2. Market Opportunity Ranking (16 Markets)

### 2.1 Composite Ranking Formula (Published)

Every market's composite rank is a weighted score across four dimensions. Weights are published here so the ranking is auditable rather than argued from cases:

- **HNW density (weight 40%)** — count of households at $5M+ liquid, sourced from Knight Frank Wealth Report 2025 and Capgemini World Wealth Report 2025, cross-checked against Cerulli-adjacent 2025 regional wealth reports. Higher score for higher household count, log-scaled so Germany's 130k doesn't drown out Switzerland's 65k in headline rank.
- **Regulatory friction (weight 25%)** — inverse score: higher score for easier certification. UK/IE at top, Saudi/Israel at bottom, reflecting SABER/SASO overhead and Israeli MoC bench-testing timeline.
- **Channel maturity (weight 20%)** — CEDIA member density, verified LAI firms per HNW household, existence of luxury AV showroom infrastructure at the required price point.
- **Language burden (weight 15%)** — inverse score: higher score for lower burden. English-first markets (UK, IE, SG-primary) score highest; markets requiring RTL engineering or unshared voice models (Arabic, Hebrew, French — French shares no components with other locales in our stack) score lowest.

France's Y3 deferral is the clearest test of the formula: France ranks #7 on HNW density alone (approximately 120,000 households at $5M+), which is more than any Tier I market except Germany and the UK. However, French adds a full 15% penalty on language burden — French requires complete localization (Île-de-France voice preset, Toubon-compliant docs, CNIL-compliant DPA, Whisper fine-tune on France Télévisions + INA archive, Piper voice actor with perpetual synthesis rights) that shares no components with any other market in our Y2 rollout. Italian shares no components either, but Italian docs, voice model, and Whisper corpus were already scoped for Q3 2028 shipping, so the Italian burden is committed capex; French would be a fresh $170-210k line item plus a dedicated Paris concierge FTE. The formula puts France just below the composite threshold that separates Y2 from Y3 entry.

### Tier I — Y2 Entry (Q1-Q3 2028) + Y2 Dealer Launch (Q4 2028)

**1. United Kingdom** — Rank #1
- HNW at $5M+ liquid: ~155,000 households (London + Home Counties concentrate 62%)
- Regulatory: UKCA + BS EN 62368-1 (audio/AV safety) + WEEE + UK-GDPR. Radio Equipment Regulations 2017 (post-RED). No wireless subclass beyond FCC-derivable.
- Distribution: Deepest LAI channel in Europe. CEDIA UK membership >800 firms.
- Concierge: English-primary. No language investment. Founder can Zoom-close from US in first year.
- **Tier I. Q1 2028 first customer sale.**

**2. Germany** — Rank #2
- HNW at $5M+: ~130,000 households (Munich, Frankfurt, Düsseldorf, Hamburg, Stuttgart) — downshifted from prior v1 estimate of 180k after re-cross-checking Knight Frank 2025 against DIW-Berlin household wealth study
- Regulatory: CE (EMC 2014/30/EU, LVD 2014/35/EU, RED 2014/53/EU) + EU-GDPR + WEEE + ElektroG registration + BattG (battery reg)
- Distribution: Strong LAI channel, culturally exacting on build quality, favors German dealers
- Concierge: German-required. Regional accents matter (Bavarian vs Hochdeutsch matters at $95k)
- **Tier I. Q2 2028 first customer sale.**

**3. Switzerland** — Rank #3
- HNW at $5M+: ~65,000 households (Zurich, Geneva, Zug, Basel, Lugano)
- Regulatory: Swiss-specific EMC & radio via BAKOM (Bundesamt für Kommunikation), CH-DSG (Data Protection Act, GDPR-aligned since Sept 2023). VAT 8.1%. Non-EU customs.
- Distribution: Bang & Olufsen boutiques dominate luxury AV; Steinway Lyngdorf Zürich showroom active
- Concierge: German + French + Italian. Practically: German + French covers 92% of HNW
- **Tier I. Q2 2028** (paired with Germany)

**4. Austria** — Rank #4 (upgraded from Y3 Tier II to Y2 Tier I)
- HNW at $5M+: ~22,000 households (Vienna concentrated, Salzburg secondary)
- Regulatory: CE-aligned (EU member). German-language reuse of DE materials at ~90% coverage; ~10% Austrian High German register tune required
- Distribution: Piggyback on German dealer network with a Vienna-specific dealer relationship
- Concierge: Shares German concierge team with Austrian accent switching
- **Tier I. Q2 2028** as paired low-cost adjunct to Germany — total incremental cost for Austrian activation ~$45k against a market that closes 3-5 units annually at concierge tier

**5. Netherlands / Belgium / Luxembourg (Benelux)** — Rank #5
- HNW at $5M+: ~64,000 combined (35k NL + 22k BE + 7k LU)
- Regulatory: CE + GDPR shared with EU. NL has aggressive AP (Autoriteit Persoonsgegevens) enforcement
- Distribution: NL has a real smart-home integrator base; BE served through Focus21 in Brussels; LU is family-office-driven
- Concierge: Dutch + French (BE Wallonia + LU) + German (LU east). Dutch HNW comfortable in English; Wallonia + LU require French — so BE/LU are the first pull on French language investment even though France itself defers
- **Tier I. Q3 2028** first customer sale

**6. Italy** — Rank #6 (corrected to Tier I / Y2 from prior Tier II tag)
- HNW at $5M+: ~95,000 households (Milan finance + Rome family wealth + Venice/Como resort second homes)
- Regulatory: CE + GDPR + Garante Privacy + Italian-language docs required per DL 206/2005 consumer code
- Distribution: Milan integrator base is well-developed at the sub-$200k residential-AV price point; Como second-home market pulls Swiss demand through
- Concierge: Italian-required. Milanese vs Roman accent distinctions matter less than dialect authenticity; Piper baseline covers both
- **Tier I. Q3 2028** first customer sale

### Tier II — Y3 Entry (2029)

**7. France** — Rank #7 (retained Y3 with explicit language-burden justification)
- HNW at $5M+: ~120,000 households (Paris + Riviera + Bordeaux)
- Regulatory: CE + GDPR + CNIL enforcement (most aggressive DPA in EU) + French-language product labeling law (Toubon Law) + AGEC extended producer responsibility for electronics
- Distribution: LAI mature but insular. French dealers negotiate hard on both margin and exclusivity terms
- Concierge: French-required, no exceptions. Île-de-France accent for baseline; Québécois separate for Y4+
- **Language burden justification for Y3 deferral:** French language investment shares zero components with any Y2-shipping locale. Italian ships Q3 2028 but shares no morphology or phonology with French; German ships Q2 2028 with no cross-benefit. A full French locale (Whisper fine-tune on France Télévisions + INA + BnF audio archives, Piper Île-de-France voice preset with perpetual rights, LLM prompt localization tuned to tu/vous register, Toubon-compliant docs, DPA reviewed by French counsel) totals $170-210k standalone plus a dedicated Paris concierge FTE at ~$220k/year fully loaded. Deferring one quarter to Q1 2029 lets us amortize French investment against a full year of European operating experience and defer $400k+ against the Y2 cash burden
- **Tier II. Q1 2029** first customer sale

**8. Hong Kong** — Rank #8
- HNW at $5M+: ~55,000 households (downshifted from prior v1 estimate of 85k after cross-checking Knight Frank 2025 against HKMA family-office census)
- Regulatory: OFCA (radio type approval), PCPD (Privacy Commissioner), no VAT
- Distribution: Small but sophisticated integrator base; overlaps SG concierge staffing
- Concierge: Cantonese-preferred, Mandarin-acceptable, English-secondary
- Political/geopolitical risk premium; National Security Law enforcement trajectory monitored quarterly
- **Tier II. Q2 2029** first customer sale

**9. Australia** — Rank #9
- HNW at $5M+: ~72,000 households (Sydney harbourside + Melbourne wine-country secondary + Perth mining wealth)
- Regulatory: RCM mark, ACMA radio compliance, C-Tick legacy, Australian Consumer Law, Privacy Act 1988. AU electrical safety (AS/NZS 62368-1) derivable from IEC
- Distribution: Boutique CI market; CEDIA APAC active with a growing Sydney/Melbourne bench
- Concierge: English-primary. Time zone challenge (UTC+10) — needs local hire in Y3
- **Tier II. Q2 2029** first customer sale

**10. Ireland** — Rank #10
- HNW at $5M+: ~8,000 households (Dublin + Cork tech wealth)
- Regulatory: CE + GDPR (EU member) but easily adapted from UK materials
- Distribution: Shares UK dealer channel; Cyberhomes extends into Dublin through prior client relationships
- Concierge: English-primary; shared with UK
- **Tier I adjunct to UK. Q1 2028** first customer sale (rides UK launch at ~5% incremental cost)

**11. UAE (Dubai + Abu Dhabi)** — Rank #11
- HNW at $5M+: ~28,000 households (heavily expat + local royal-adjacent)
- Regulatory: TDRA type approval (radio), ESMA ECAS (Emirates Conformity Assessment Scheme), 5% VAT, Sharia-compliant financing options preferred, Arabic-language product requirement for consumer goods
- Distribution: Palace-tech integrators run $500k+ residential jobs; buying decisions run through majlis / advisor channels
- Concierge: English-primary for expat, Arabic-required for local/royal accounts
- **Tier I dealer launch Q4 2028. Q1 2029 first customer sale.**

**12. Singapore** — Rank #12
- HNW at $5M+: ~42,000 households (regional wealth hub; family office growth)
- Regulatory: IMDA equipment registration, PDPA (Personal Data Protection Act, GDPR-adjacent), Consumer Protection Fair Trading Act
- Distribution: Boutique but sophisticated
- Concierge: English-primary. Mandarin secondary. Founder can operate direct with dealer support
- **Tier I dealer launch Q4 2028. Q1 2029 first customer sale.**

### Tier III — Y3-Y4 Entry (2029-2030)

**13. Spain** — Rank #13
- HNW at $5M+: ~45,000 households (Madrid + Barcelona + Marbella + Balearics)
- Regulatory: CE + GDPR + AEPD + Spanish-language labeling
- Concierge: Castilian Spanish baseline; Mexican + Argentine variants shipped as separate LatAm package Y4+
- **Tier III. Q3 2029.**

**14. Portugal** — Rank #14
- HNW at $5M+: ~10,000 households (Lisbon + Cascais + Comporta + Algarve/Alentejo golf coast)
- Regulatory: CE + GDPR + CNPD + Portuguese-language
- Concierge: Portuguese-required for local; English works for expat retirees
- **Tier III. Q4 2029.**

**15. Israel** — Rank #15
- HNW at $5M+: ~35,000 households (Tel Aviv luxury + Herzliya Pituach)
- Regulatory: Ministry of Communications type approval, Standards Institution of Israel (SII), Privacy Protection Law 1981 (GDPR-adequacy pending)
- Concierge: Hebrew + English (both required)
- Regional political sensitivity — market timing must be sensitive to security posture
- **Tier III. Q1 2030.**

**16. Saudi Arabia** — Rank #16
- HNW at $5M+: ~24,000 households (Riyadh concentrated, Jeddah secondary)
- Regulatory: CITC (Communications & Information Technology Commission), SASO (Saudi Standards), SABER platform mandatory for import, 15% VAT
- Concierge: Arabic-required, gender-of-installer considerations (male installer for male majlis, female installer for family quarters), Sharia-compliant financing (Murabaha) needed as option
- **Tier III. Q2 2030** — deliberate deferral pending Vision 2030 palace-tech RFP dynamics

---

## 3. Regulatory Landscape — 3 Tiers

### Tier A — Easy Adaptation
**Markets:** UK, Ireland, Australia
**Certification bodies:** BSI Group (UK — UKCA marks), NSAI (Ireland — reuses CE), SAI Global / TÜV Rheinland Australia (RCM)
**Standards:** BS EN 62368-1 (safety), Radio Equipment Regulations 2017 (UK), AS/NZS 62368-1 (AU), IEC 62311 (EMF)
**Cost per market:** $75-125k (dossier reuse from FCC filing, no new test lab required beyond compliance verification)
**Time to first sale:** 10-14 weeks from dossier submission
**Language investment:** Zero incremental (en-GB accent tuning already scoped for Y1 GA; en-AU deferred to Y3)

### Tier B — Moderate Adaptation
**Markets:** Germany, Switzerland, Austria, France, Netherlands/Belgium/Luxembourg, Italy, Spain, Portugal, Singapore, Hong Kong
**Certification bodies:** TÜV Rheinland, TÜV SÜD, Dekra, Intertek, SGS (EU); BAKOM (Switzerland); IMDA (Singapore); OFCA (Hong Kong)
**Standards:** CE marking via EMC Directive 2014/30/EU, LVD 2014/35/EU, RED 2014/53/EU (wireless), Ecodesign 2019/1782, RoHS 3 (2015/863/EU), WEEE 2012/19/EU + national registrations (ElektroG in Germany, ADEME in France, RAEE in Italy), GDPR (Regulation 2016/679)
**Cost per market:** $150-250k (test lab time + notified body + country-specific WEEE registration + local authorized representative if required)
**Time to first sale:** 16-24 weeks from test lab intake
**Language investment:** $150-240k per language (see §11)

### Tier C — Hard Adaptation
**Markets:** UAE, Saudi Arabia, Israel
**Certification bodies:** TDRA + ESMA (UAE), CITC + SASO + SABER (Saudi Arabia), Ministry of Communications + SII (Israel)
**Standards:** UAE Standard for Radio Communications (TDRA); GSO (Gulf Standards Organization) technical regulations; ECAS (Emirates Conformity Assessment Scheme); SASO 2902 (energy efficiency); Saudi-specific data-localization rules under the Personal Data Protection Law (PDPL, September 2023); Israeli Privacy Protection Regulations 2017
**Cost per market:** $250-400k (SABER + palace-tech distributor onboarding + local Arabic content sub-contractor + Israel MoC bench testing)
**Time to first sale:** 24-36 weeks
**Language investment:** $200-280k per language (Arabic RTL UI engineering + Hebrew + non-Latin voice models)

---

## 4. Product Adaptations Per Market

### Wake-Word (Base: "Hey Pod")
| Locale | Wake-word | Rationale |
|---|---|---|
| en-US, en-GB, en-AU, en-IE, en-SG, en-HK, en-IL | Hey Pod / Hey Hearth | English default; "Hey Hearth" markets that reject US branding |
| de-DE, de-AT, de-CH | Hey Feuerstelle | Literal for "hearth" with romantic register |
| fr-FR, fr-CH, fr-BE | Hey Foyer | "Foyer" carries both home + hearth semantics |
| it-IT | Ciao Focolare | Italian register warmer than English |
| es-ES, es-MX (Y4) | Hola Hogar | "Hogar" is the household-hearth term |
| nl-NL, nl-BE (Vlaams) | Hallo Haard | Direct cognate |
| pt-PT | Olá Lareira | Portuguese |
| ar-AE, ar-SA | قل يا موقد (Qul ya Mawqid) | "Mawqid" (moqid) is the classical Arabic hearth |
| he-IL | היי אח (Hey Ach) | "Ach" = fireplace/hearth |
| zh-HK | 你好爐子 (Nei5 hou2 lou4zi) | Cantonese |
| zh-CN (Y4+) | 你好爐子 (Nǐ hǎo lúzi) | Mandarin |

Voice engineering per §11.

### STT (Whisper.cpp)
- Base: `whisper-large-v3` fine-tuned per locale on 200h+ dialectal corpus
- Fine-tunes commissioned from Common Voice + licensed broadcast archives (BBC for en-GB, RAI for it-IT, France Télévisions + INA for fr-FR)
- On-device inference on Jetson Orin NX (INT8, ~180ms first-token latency target)

### TTS (Piper)
- **en-GB:** Received Pronunciation baseline + optional Home Counties, Edinburgh, Newcastle regional presets
- **de-DE:** Hochdeutsch baseline + Bavarian + Austrian variants
- **fr-FR:** Île-de-France baseline; Québécois model as separate en-CA/fr-CA package (Y4)
- **es-ES:** Castilian; Mexican + Argentine variants ship as separate LatAm package Y4+
- **it-IT:** Standard Italian; Neapolitan + Sicilian on request only (custom concierge SKU)
- **ar:** MSA baseline; Khaleeji (Gulf) variant for UAE/Saudi
- Piper models fine-tuned from open licensed voice actors ~4-6h data; QA via 12-native-speaker MOS panel

### LLM
- Llama 3.1 8B multilingual (or Llama 4 successor at deploy time) as baseline
- Prompt engineering pack per locale: cultural register (formal Sie vs informal du in Germany; tu vs vous in France; Cantonese pronoun politeness), regional entity awareness (BBC iPlayer default in UK, Sky Sport in DE, Canal+ in FR)
- No cloud fallback — matches offline claim

### Content Integration (Plex / Jellyfin / Audiobookshelf)
- UK: BBC iPlayer via jellyfin-plugin, Sky Q ingest, Amazon Prime UK catalog, Disney+ UK
- Germany: ARD Mediathek, ZDF, RTL+, Sky Deutschland, Netflix DE
- France (Y3): France.tv, TF1+, Canal+ à la carte
- UAE: OSN, Shahid VIP, StarzPlay, Netflix ME
- Singapore/HK: mewatch, TVB Anywhere, Now TV, Netflix regional
- Sports: Sky Sports (UK), BeIN (ME), Fox Sports AU — via existing xTeVe/threadfin

### Mobile Companion App Currency + Locale
- Currency display per market (GBP, EUR, CHF, AED, SAR, SGD, HKD, AUD, ILS)
- Date format per locale (dd/mm/yyyy for most non-US)
- Metric-first everywhere except imperial toggle on Companion app
- Concierge chat available in local language
- Right-to-left mirroring for Arabic + Hebrew (see §11 engineering line)

---

## 5. Distribution Channel Per Market

Named LAI dealer targets, terms, and initial commitments. Every dealer named below is a verifiable operating AV integrator or luxury audio retailer with a public storefront; unverified prospects are stated as "vendor selection through CEDIA member directory outreach" rather than named to preserve credibility with the diligence audience.

### UK — Q3 2027 program launch
- **Cyberhomes** (Buckinghamshire) — high-end CI with concurrent >£1M projects; propose exclusive London postcodes SW1/SW3/SW7/W1/W8/NW3/NW8 for 12 months
- **Grahams Hi-Fi** (Islington, London) — flagship-store presence useful for brand exposure at the London retail street level
- **Ultimate Home** (Surrey) — Weybridge/Cobham/Esher (footballer belt)
- **Custom Controls** (Manchester) — Northern England territory; Manchester/Cheshire/Leeds
- **New Wave AV** (Cheshire) — Cheshire golden triangle
- **Terms:** 30% dealer margin off VAT-inclusive MSRP, £150k first-year Founding Dealer stocking floor (2 demo units + 1 sold), 12-month exclusivity in designated postcodes, quarterly CEDIA-accredited training, 3-year service contract inclusion

### Ireland — Q1 2028
- Extend Cyberhomes into Dublin territory (existing prior client relationships); Cork covered via Buckinghamshire remote-plus-Dublin travel model. No separate Irish dealer program initially.

### Germany — Q1 2028 dealer program / Q2 2028 first customer sale
- **Cinegate** (Frankfurt) — Hessen/Rhineland; luxury home cinema specialist with existing >€500k residential portfolio
- **PS-Wohnen** (München) — Bavaria; high-end residential AV integrator
- **Hifi im Hinterhof** (Berlin) — Berlin + Brandenburg; luxury audio retailer with installation practice
- **Sinuslive** (Hamburg) — Northern Germany
- **HiFi-Studio Wittmann** (Nürnberg) — Franconia + Stuttgart adjacency
- **Terms:** 28% dealer margin (Germany is competitive), €200k Founding Dealer stocking floor, 18-month exclusivity in stated Länder, TÜV-witnessed installation training, WEEE registration passed to dealer

### Austria — Q2 2028 (paired with Germany launch)
- Vienna dealer selection through CEDIA member directory outreach; target Q1 2028 signing. Austrian pilot rides German dealer support relationships until Vienna dealer is trained.

### Switzerland — Q2 2028
- **Bang & Olufsen Zürich boutique** — Zurich, Zug primary catchment
- **Bang & Olufsen Genève boutique** — Geneva, Lausanne, Vaud
- **Bang & Olufsen Basel boutique** — Basel, Aargau
- **Steinway Lyngdorf Zürich showroom** — brand-parity partnership; co-listed in Steinway concierge network for high-end audio buyers
- **Home Systems Zug** — Zug + Ticino; family-office-adjacent
- **Terms:** 35% dealer margin (Swiss market bears it), CHF 150k Founding Dealer stocking floor, non-exclusive city allocation (Zurich has 3 potential dealers; keep competition), BAKOM co-registration

### Netherlands — Q3 2028
- **van der Meer Custom Installations** (Rotterdam) — Randstad + Wassenaar/Scheveningen
- **Musique en Diagonale** (Utrecht) — Central NL luxury AV
- **Poehl Audio** (Amsterdam) — Amsterdam-Zuid concentration
- **Terms:** 30% margin, €150k Founding Dealer stocking floor, AP-privacy-officer co-signed DPA

### Belgium + Luxembourg — Q3 2028 (paired)
- **Focus21** (Brussels) — Brussels + Wallonia; French-language installation practice
- **Bang & Olufsen Brussels boutique** — brand-tier presence
- Luxembourg served by Focus21 travel model initially; Q3 2029 review for dedicated LU dealer

### France — Q1 2029 (Tier II)
- **FANEtec** (Paris) — Paris + Île-de-France
- **CDS Home Automation** (Paris + Côte d'Azur) — Paris HQ with Riviera + Monaco second office
- **Focus AV France** — Paris + Bordeaux
- **Terms:** 32% dealer margin, €200k Founding Dealer stocking floor (French dealers require deeper inventory to defend margin), Toubon-compliant French docs, CNIL-compliant DPA co-signature

### Italy — Q3 2028
- **Custom Team** (Milano) — Milan + Como + Bergamo
- **Casacontrol Milano** — Milan + Amalfi coast (Amalfi covered by owner's Naples travel)
- **Villa Systems** (Como) — Como lake luxury residential specialization
- **Terms:** 30% margin, €150k Founding Dealer stocking floor, Garante-compliant DPA, Como-specific concierge shared with Swiss team

### UAE — Q4 2028 dealer program / Q1 2029 first customer sale
- **Custom House** (Dubai) — Palm Jumeirah + Emirates Hills; palace-tech integrator with royal-adjacent portfolio
- **Bel-Air Cinema** (Al Wasl, Dubai) — home cinema and residential AV
- **Onbite Systems Middle East** (Abu Dhabi) — Abu Dhabi + Al Ain palace-tech
- **Terms:** 35% dealer margin (Gulf luxury benchmark), AED 750k Founding Dealer stocking floor, TDRA/ESMA co-registration, Arabic-language sales collateral, Sharia-compliant financing option required via Emirates NBD or Mashreq Al Islami

### Saudi Arabia — Q2 2030
- **Al-Naeem Trading** (Riyadh) — palace-tech firm with active Vision 2030 project portfolio
- **Saudi Comfort Systems** — Riyadh + Jeddah residential
- Additional Riyadh dealer selection through CEDIA MENA + SASO importer directory outreach, Q4 2029 target
- Terms: TBD, SABER filing pre-condition

### Singapore — Q4 2028 dealer program / Q1 2029 first customer sale
- **Sound Affairs** — Singapore luxury audio retailer with installation practice
- **TC Acoustic Distribution** — high-end audio distribution with dealer network
- **Kris Sound (Singapore Home Automation)** — residential AV integrator
- **Terms:** 30% margin, SGD 200k Founding Dealer stocking floor, IMDA registration co-signed

### Hong Kong — Q2 2029
- **Alma Acoustics** (HK) — luxury audio + custom install
- **Radar Audio** (HK) — high-end audio retailer with installation
- **Speaker Cellar HK** — boutique high-end audio + AV
- **Terms:** 32% margin, HKD 1.2M Founding Dealer stocking floor, OFCA registration

### Australia — Q4 2028 dealer program / Q2 2029 first customer sale
- **SmartHouse Sydney** — Sydney harbourside + Palm Beach + Point Piper
- **Cinema Direct Melbourne** — Toorak + Portsea + Mornington Peninsula
- **Digital Cinema Perth** — Cottesloe + Mosman Park + Peppermint Grove
- **Boutique Home Cinema Brisbane** — Brisbane + Sunshine Coast + Gold Coast
- **Terms:** 30% margin, AUD 200k Founding Dealer stocking floor, RCM co-registration, Australian Privacy Principles DPA

---

## 6. Concierge Model Per Market

Baseline: **1 concierge per 50 concierge-tier households**. Smaller markets share regional concierge until threshold triggers dedicated hire.

### Y2 Staffing (2028)
- **US East Coast concierge:** 3 FTE (Boston HQ) covering US + Canada + covering-shift for UK morning
- **London concierge:** 2 FTE (based Marylebone or Fitzrovia) — covers UK + Ireland + Netherlands + early German morning
- **Frankfurt concierge:** 1 FTE (Q2 2028 hire) — covers Germany + Switzerland + Austria
- **Milan concierge:** 1 FTE (Q3 2028) — Italy + Southern France advance work
- **Dubai concierge:** 1 FTE (Q4 2028 hire, in-market Q4) — UAE dealer program support + advance work for Q1 2029 first sales
- **Singapore concierge:** 1 FTE (Q4 2028 hire) — SG dealer program + HK relief + AU advance work

**Total Y2 international headcount:** 6 FTE at fully-loaded cost ~$180k/year each (Frankfurt/London/Milan) to $350k/year (Dubai + Singapore combined package + expat premium) = ~$1.5M/year concierge burden.

### Y3 Additions
- Paris concierge: 1 FTE (France dedicated)
- Sydney concierge: 1 FTE (Australia + NZ time zone)
- HK concierge: 1 FTE (splits from Singapore)
- Frankfurt team grows to 2 FTE
- London team grows to 3 FTE
- **24h coverage established** by end Y3 (US East + London + Frankfurt + Dubai + Singapore + Sydney = full clock)

### Y4 Additions
- Riyadh concierge (Saudi dedicated, gender-diverse team)
- Tel Aviv concierge (Israel)
- Madrid concierge (Spain + Portugal)

### Cultural Adaptation Training
Every concierge completes:
- 40h product-technical training (Fremont, quarterly cohort)
- 20h cultural register training (per-market: e.g., German Sie/du transitions; French vous norms; Gulf majlis protocol; Japanese keigo if Y5+)
- 8h GDPR / PDPA / local-privacy law
- Ongoing quarterly recertification

### Local RustDesk Relays
Self-hosted RustDesk relay per jurisdiction to keep remote-desktop traffic on local infrastructure and defensible under local data residency:
- **EU relay:** Frankfurt (Hetzner AX102 dedicated), serves DE/AT/CH/NL/BE/LU/FR/IT/ES/PT/IE
- **UK relay:** London (OVH or M247 UK), UK-only for post-Brexit clarity
- **UAE relay:** Etisalat Cloud Dubai (Category-B compliant)
- **Saudi relay:** STC Cloud Riyadh (PDPL-aligned)
- **Singapore relay:** SG-based Vultr HF instance, serves SG/HK/AU pre-Sydney
- **Australia relay:** AWS Sydney ap-southeast-2 (Q3 2029)

Each relay adds ~$2-4k/year infra + $8k initial setup. Configuration ships in the concierge tier only.

---

## 7. Pricing Per Market — The Math

Base US retail: **$95,000 main sphere / $6,999 companion extender**.

All non-US prices set to protect ~25% gross margin post-duty/VAT and normalize on-the-shelf price with local luxury benchmarks (Steinway grand ~$180k, Beolab 90 ~$95k, Bulthaup B3 kitchen ~$150k — Hearth sits below).

### UK — £75,000 / £6,999 (VAT-inclusive)
- USD 95,000 × 0.79 GBP/USD = £75,050
- Ex-VAT (÷1.20): £62,542
- Landed cost target: £45,000
- Dealer margin @30%: £18,762
- Net-to-Hearth per unit: £43,780 ≈ **$55,417**
- Duty: 0% under UK Global Tariff (HTS 8471.30 laptops / 8517.62 network — final HS classification TBD)
- Extender pass-through: £6,999 VAT-inclusive = ex-VAT £5,833, dealer margin £1,750, net-to-Hearth £4,083

### EU baseline (Germany used) — €89,000 / €8,199 (VAT-inclusive)
- USD 95,000 × 0.92 EUR/USD = €87,400 → round to €89,000
- Ex-VAT @19% (Germany): €74,790
- Dealer margin @28%: €20,941
- Net-to-Hearth: €53,849 ≈ **$58,532**
- VAT variance by market: DE 19%, AT 20%, NL 21%, BE 21%, LU 17%, FR 20%, IT 22%, ES 21%, PT 23%, IE 23%. Hearth absorbs the delta; pricing consistent across EU to prevent cross-border arbitrage.

### Switzerland — CHF 92,000 / CHF 8,500 (VAT-inclusive)
- Ex-VAT @8.1%: CHF 85,105 ≈ $97,822 (matches US retail — premium market bears it)
- Dealer margin @35% for B&O boutique: CHF 29,787
- Net-to-Hearth: CHF 55,318 ≈ **$63,584**
- Higher net-per-unit reflects Swiss channel cost + brand-parity with B&O

### UAE — AED 349,000 / AED 25,700 (VAT-inclusive)
- Ex-VAT @5%: AED 332,381 ≈ $90,568
- Dealer margin @35%: AED 116,333
- Net-to-Hearth: AED 216,048 ≈ **$58,867**
- Sharia-financing option adds ~2.5% cost absorbed by Hearth

### Saudi Arabia — SAR 356,000 / SAR 26,240 (VAT-inclusive)
- Ex-VAT @15%: SAR 309,565 ≈ $82,551
- Dealer margin @35%: SAR 108,348
- Net-to-Hearth: SAR 201,217 ≈ **$53,658**
- SABER + local content premium tolerated; Saudi HNW willing but market slower to close

### Singapore — SGD 128,000 / SGD 9,499 (GST-inclusive)
- Ex-GST @9%: SGD 117,431 ≈ $86,986
- Dealer margin @30%: SGD 35,229
- Net-to-Hearth: SGD 82,202 ≈ **$60,890**

### Hong Kong — HKD 745,000 / HKD 55,000 (no VAT)
- No GST/VAT applies
- USD 95,000 × 7.85 HKD/USD = HKD 745,750
- Dealer margin @32%: HKD 238,400
- Net-to-Hearth: HKD 506,600 ≈ **$64,535**

### Australia — AUD 145,000 / AUD 10,700 (GST-inclusive)
- Ex-GST @10%: AUD 131,818 ≈ $86,723
- Dealer margin @30%: AUD 39,545
- Net-to-Hearth: AUD 92,273 ≈ **$60,706**

**Weighted-average net-to-Hearth across international ~$58,500 vs US $66,500** (US direct sale, no dealer margin). International gross margin ~7-10% lower but volume + brand halo justify.

---

## 8. Data Residency + GDPR

The offline architecture is the case. Per THREAT-MODEL.md's 7-class egress model, only these classes ever leave the household perimeter — and Hearth is the **data controller** for every one of them under GDPR Article 4(7) because we determine the purposes and means of processing:

1. **Firmware update pull** (signed, initiated by device, HTTPS to Hearth update CDN)
2. **NTP** (time sync, RFC 5905, `time.cloudflare.com` primary + household pool)
3. **DNS** (encrypted, DoH to Cloudflare `1.1.1.1` + user override)
4. **Concierge screen-share on user request only** (via local RustDesk relay per §6)
5. **Support ticket creation** (metadata only: firmware version, error class, no user content, user-initiated)
6. **License activation** (one-time at commissioning: serial + license key exchange)
7. **Optional weather/news content pull** (user-toggled, IP-anonymized via user's own network)

**Everything else — every voice utterance, every media file, every LLM prompt, every calendar entry, every wake-word training sample — stays on-device.** No cloud STT, no cloud TTS, no cloud LLM, no cloud media library. Every processing step runs on the Jetson cluster + Framework nodes inside the sphere.

### GDPR Article 6 Lawfulness Per Egress Class

The v1 draft asserted Article 6 lawfulness was "not required" — that was wrong. Hearth is a controller for each of the 7 egress classes (firmware CDN captures client IPs, license activation captures serial↔identity mapping, support tickets are personal data by definition, DNS resolution is metadata about household activity). Article 6(1) lawfulness must be asserted per processing class:

| Egress class | Article 6 legal basis | Rationale |
|---|---|---|
| 1. Firmware update pull | 6(1)(b) contract performance + 6(1)(f) legitimate interest | Update delivery is a necessary part of ongoing product service; security patching is a documented legitimate interest with balancing test filed in DPIA |
| 2. NTP | 6(1)(f) legitimate interest | Household time sync is necessary for scheduled operations, event correlation, and security; no personal data revealed beyond the IP of the LAN egress |
| 3. DNS (DoH) | 6(1)(f) legitimate interest | Name resolution is necessary for network operation; DoH minimizes exposure vs plaintext DNS; user override is documented |
| 4. Concierge screen-share (RustDesk) | 6(1)(a) explicit consent + physical-tap gesture at device | Concierge cannot initiate; user must physically tap "Allow Concierge" gesture on the device, which creates a session-scoped ephemeral tunnel with local audit log |
| 5. Support ticket creation | 6(1)(a) explicit consent, per-ticket | User authors and confirms each ticket submission; no automated telemetry |
| 6. License activation | 6(1)(b) contract performance | Serial↔license exchange is necessary to establish the paid contract |
| 7. Optional weather/news content pull | 6(1)(a) explicit consent, per-widget | User toggles each content widget individually; consent is granular and revocable in device settings |

Two additional egress paths deserve their own line even though they aren't in the "7 classes" from THREAT-MODEL:

- **`apt update` (Debian package repository refresh for Framework nodes)** — 6(1)(f) legitimate interest (system security). Traffic is to Debian mirrors + Framework OEM repo, not to Hearth. Documented and disclosed.
- **Bug-report upload with user attachments** — 6(1)(a) explicit consent per-report, with a preview screen showing exactly what will be transmitted before the user confirms.

### DPIA (Article 35) Requirements

DPIAs are filed for firmware update pull and — separately and more thoroughly — for concierge screen-share, which is the highest-risk processing class in the Hearth architecture because it involves live audio/video of the household. The concierge DPIA includes:

- Session-scoped ephemeral tunnel design (RustDesk relay per jurisdiction)
- Physical-tap consent gesture required to open the tunnel
- Local audit log with user copy stored on-device
- Documented sub-processor list (see below)
- Balancing test against Article 6(1)(f) not-relied-upon (we rely on 6(1)(a) instead precisely because the intrusion is high)

DPIA filed at data room `/compliance/eu/gdpr-dpia-v2.pdf`.

### Sub-Processor List (Published)

Per Article 28, we maintain and publish the sub-processor list. Customers must be notified of new sub-processors 30 days in advance of engagement.

| Sub-processor | Location | Purpose | Data touched |
|---|---|---|---|
| Cloudflare | Global anycast | NTP + DoH resolution | Household egress IPs, DNS query metadata |
| Amazon CloudFront (firmware CDN) | Global anycast, EU nodes for EU customers | Firmware binary distribution | Household egress IPs, firmware version fetch logs |
| Sanmina (Fremont) | US (California) | Manufacturing-stage QA data + support-ticket triage L3 | Serial numbers, calibration data, support ticket content |
| Hetzner Online GmbH | Germany (Frankfurt) | EU RustDesk relay + EU CDN edge | Session metadata for concierge screen-share (payload E2E-encrypted; relay sees IP + session start/end only) |
| OVH / M247 | UK (London) | UK RustDesk relay | Same as EU relay, UK jurisdiction |
| Etisalat Cloud | UAE (Dubai) | UAE RustDesk relay | Same, UAE jurisdiction |
| STC Cloud | Saudi Arabia (Riyadh) | Saudi RustDesk relay | Same, Saudi jurisdiction, PDPL-aligned |
| Vultr | Singapore | SG/HK RustDesk relay | Same, SG jurisdiction |
| AWS ap-southeast-2 | Australia (Sydney) | AU RustDesk relay (Q3 2029) | Same, AU jurisdiction |
| ProDPO Ltd | Ireland (Dublin) | Fractional DPO — EU | Compliance advisory; no operational data access |
| The DPO Centre | UK (Colchester) | Fractional DPO — UK | Compliance advisory; no operational data access |

### Third-Country Transfer — Fremont Support Flow

The v1 draft treated Fremont support routing as a routine internal flow. It is not. Any EU customer support ticket that reaches Fremont for L3 diagnosis constitutes a **third-country transfer** under Chapter V of GDPR. This requires:

- **Standard Contractual Clauses 2021/914 (Module Two: controller-to-processor)** signed between Hearth EU controller entity (Hearth GmbH, Frankfurt) and Sanmina Fremont for support-ticket flows
- **Transfer Impact Assessment (TIA)** documenting the Schrems II analysis of US surveillance law exposure and the supplementary technical measures (payload minimization — no user content in tickets, only firmware version + error class; end-to-end encryption of ticket payload at rest at Sanmina)
- **Same SCC coverage for the concierge Fremont escalation path** used when a concierge in London/Frankfurt/Milan/Dubai needs product engineering support during a live household session
- SCCs also cover the **prior "non-EU dealer flows"** identified in v1 (UAE, SG, HK, AU dealers with EU customers)

TIA and SCC package filed at `/compliance/eu/scc-fremont-2021-914.pdf`.

### Article 30 Records

Records of processing (Article 30) are maintained for the 7 egress classes plus the two additional egress paths (`apt update`, bug-report upload). Public data-flow diagram in the Data Handling Disclosure document ships with every unit. Full Article 30 register is available on request to any Supervisory Authority within 24 hours of request per our documented procedure. Register maintained at `/compliance/eu/article-30-register-v2.xlsx`.

### Article 13/14 (Transparency)
- Documentation package "Hearth Data Handling Disclosure" ships with every unit, per-language, with Article 13 disclosures at commissioning and Article 14 disclosures for any third-party data source (e.g., dealer-provided delivery data).

### Article 17 (Right to be Forgotten)
- Local `hearth-erase` command wipes user data hard from all sphere nodes. Concierge assists remotely on request. No remote copy to erase because no remote copy exists — except the license activation record (which is retained for contract-of-sale defense per Article 17(3)(e)) and support ticket history (retained six years per accounting requirements, then hard-purged).

### Article 20 (Data Portability)
- Local export to standard formats (JSON for structured data, media in original codecs). Concierge can walk user through the export UI.

### Article 37 (DPO)
- Hearth appoints a fractional DPO via **ProDPO** (Dublin-based) starting Q1 2028 for EU-wide coverage. UK DPO via **The DPO Centre** (Colchester). Both are named sub-processors with contact detail published at `hearth.com/dpo/eu` and `hearth.com/dpo/uk`.

### SAR (Subject Access Request) Mechanism
- Local concierge triggers on-device SAR export via secure tunnel
- 30-day response window (Article 12) tracked in concierge CRM
- Zero-egress design means most SARs answered "we hold nothing about you beyond order + serial + support tickets" — but that phrasing must NOT be interpreted as "no processing occurred." The 7 egress classes are processing; the SAR response discloses what data was captured (client IPs at CDN, license activation records, ticket text) and how it was used.

### Country-Specific Overlays
- **UK-GDPR** (Data Protection Act 2018): identical technical posture; separate ICO registration for Hearth UK Ltd
- **CH-DSG** (revised 2023): identical
- **UAE PDPL** (Federal Decree-Law 45/2021): identical + local-language disclosure
- **Saudi PDPL** (September 2023): identical + data-localization at Saudi RustDesk relay
- **Singapore PDPA:** identical + Do-Not-Call registry for outbound concierge calls
- **Australia Privacy Act 1988 + APPs:** identical + APP 8 cross-border disclosure statement

---

## 9. Financial Model

### Revenue Targets (Revised)
| Year | Total Intl Revenue | Unit Count | Avg Net-per-unit | Comment |
|---|---|---|---|---|
| Y2 (2028) | **$3.4M** | 60 units | $56,700 | Down-revised from v1 $4.5M; 5 Y2 markets ship, UAE + SG defer to Q1 2029 |
| Y3 (2029) | **$8.0M** | 135 units | $59,300 | Down-revised from v1 $10M; UAE + SG + FR + HK + AU + IE mature |
| Y4 (2030) | **$18-22M** | 305-370 units | $59,700 | Saudi + Israel + Spain activate |
| Y5 (2031) | **$30M** | 500 units | $60,000 | Steady-state pre-Series C |

### Y2 Per-Market Contribution (Revised)
| Market | Units | Revenue (USD net) | Timing |
|---|---|---|---|
| UK + Ireland | 22 | $1,220,000 | Q1-Q4 |
| Germany | 13 | $760,000 | Q2-Q4 |
| Austria | 2 | $115,000 | Q3-Q4 |
| Switzerland | 7 | $445,000 | Q2-Q4 |
| Netherlands + BE + LU | 8 | $470,000 | Q3-Q4 |
| Italy | 5 | $295,000 | Q3-Q4 |
| UAE (dealer launch only, no revenue Y2) | 0 | $0 | Q4 dealer program |
| Singapore (dealer launch only, no revenue Y2) | 0 | $0 | Q4 dealer program |
| **Total Y2** | **57** | **$3,305,000** | |

Rounding to **60 units / $3.4M** to accommodate 2-3 direct concierge-tier sales through the Founder + London concierge channel.

### Y2 International Cost Stack (Revised — dealer stocking removed to CapEx)
| Category | Cost |
|---|---|
| Certifications (UK + EU + CH + AE + SG) | $950,000 |
| Language engineering (en-GB, de-DE, it-IT, nl-NL, ar-AE partial) | $780,000 |
| Concierge FTE (6 heads × ~$250k avg loaded) | $1,500,000 |
| Sales & marketing local (5 core markets × ~$300k) | $1,500,000 |
| RustDesk relays + infra | $60,000 |
| Legal + DPO + local counsel (ProDPO + DPO Centre + SCC drafting + DPIA counsel) | $420,000 |
| Trade shows (ISE Barcelona, CEDIA Expo, MEBA Dubai) | $220,000 |
| **Total Y2 Intl Opex** | **$5,430,000** |

**Dealer stocking capital ($700k) is NOT in the opex table.** Stocking commitment is dealer CapEx — dealers finance their own inventory position. Hearth's obligation is production and delivery, not dealer working capital. The v1 draft's inclusion of stocking under Hearth opex was a categorization error; it is corrected here. To the extent Hearth extends payment terms on stocking inventory (net-60 or net-90 to Founding Dealers in the launch markets), those extended terms show up in working-capital financing, not opex — modeled in the CFO cash flow at approximately $700-900k of trade receivables float at Y2 peak, not P&L.

Y2 international is **planned negative** by ~$2.0M gross to net — market-building investment. **Y3 approaches break-even.** Y3 opex grows to ~$7.5M against $8M net revenue → net contribution ~$0.5M. Y4 opex ~$12M against $20M revenue → $8M contribution to corporate.

### Per-Market Cert Cost Detail
- UK UKCA + WEEE + UK-GDPR reg: $95,000
- Ireland (piggyback CE + NSAI notification): $18,000
- Germany CE + ElektroG + BattG + notified body: $195,000
- Switzerland BAKOM + import cert: $110,000
- Austria (piggyback CE + national reg): $22,000
- Netherlands (piggyback CE + RAI): $28,000
- Italy (piggyback CE + Garante docs): $45,000
- UAE TDRA + ESMA + ECAS + Arabic docs: $285,000
- Singapore IMDA + local rep: $135,000
- France (piggyback CE + ADEME + Toubon docs) — Y3: $75,000

---

## 10. Timeline + Operational Sequencing

### 2027
- **Q1:** Head of International hired (fractional through Q2, FTE Q3)
- **Q2:** UK entity incorporation (Hearth UK Ltd, London); Ireland entity (Hearth Ireland Ltd, Dublin) — enables VAT registration
- **Q3:** UK + Ireland dealer program launch at CEDIA UK Awards (October). Cyberhomes signs LOI. UKCA test dossier submitted to BSI.
- **Q4:** UK certification complete; en-GB voice model ships as part of Y1 GA firmware; first UK unit ships to Cyberhomes demo showroom December 2027

### 2028 (Y2)
- **Q1:** UK first customer sales; Ireland shipping. German + Austrian dealer program launched at ISE Barcelona (February). Swiss B&O + Steinway Lyngdorf partnership announced. Frankfurt entity incorporated (Hearth GmbH). CE test dossier at TÜV Rheinland Köln.
- **Q2:** German + Swiss + Austrian certifications complete. de-DE voice model ships (Hochdeutsch + Bavarian + Austrian variants). First German sale. First Swiss sale. First Austrian sale. Frankfurt concierge FTE onboarded. Netherlands dealer program launched at Amsterdam AV trade show.
- **Q3:** Italy + Benelux dealer sales open. it-IT and nl-NL voice models ship. Milan concierge FTE. First Italian sale. First Netherlands sale. Belgian/Luxembourg first sales through Focus21 Brussels.
- **Q4:** UAE + Singapore dealer programs launch at Dubai Design Week + Singapore Design Week (November). ar-AE Khaleeji voice model ships. Dubai + Singapore concierge FTEs onboarded and begin dealer certification work. First customer sales in UAE and SG target Q1 2029 to align with realistic 60-90 day palace-tech / family-office sales cycles from a cold-launched channel.

### 2029 (Y3)
- **Q1:** UAE first customer sale. Singapore first customer sale. France dealer program launches at ISE Barcelona. fr-FR voice model ships. Paris concierge FTE. Ireland: dedicated Dublin dealer relationship signed as UK volume validates.
- **Q2:** France first customer sale. Australia certification complete + first sale. Sydney concierge FTE onboarded. Hong Kong dealer program launches. First HK sale. zh-HK Cantonese voice model ships.
- **Q3:** Spain dealer program launched. es-ES voice model. First Spain sale by end Q3.
- **Q4:** Portugal + Israel dealer programs. he-IL voice model in development. pt-PT voice ships end Q4.

### 2030 (Y4)
- **Q1:** Israel first sale. Israel dealer program consolidates.
- **Q2:** Saudi Arabia dealer program (Al-Naeem Trading + Saudi Comfort Systems). ar-SA Najdi accent voice model ships as delta over ar-AE.
- **Q3:** Second-wave Tier B (Norway, Denmark, Sweden — Nordic expansion) evaluated
- **Q4:** Japan feasibility study (Y5+)

---

## 11. Language Adaptation Cost Estimate (Revised)

### Per-Language Investment Budget
| Component | Cost | Notes |
|---|---|---|
| STT model qualification (Whisper.cpp fine-tune) | $50-80k | Includes $30-60k for 200h transcribed dialectal speech corpus at $100-300/hr sourced-and-verified rate + $15-20k compute + $5k MOS eval |
| TTS voice preset development (Piper) | $45-75k per voice | Voice actor session + fine-tune + eval |
| Voice actor perpetual synthesis rights | $15-30k per voice preset | Buy-out for indefinite synthesized use across future firmware; negotiated per talent |
| LLM prompt localization | $15-25k | Cultural register + regional entity map |
| Documentation + UI translation | $20-40k | Professional translators + legal review |
| Wake-word retraining | $8-15k | 10k sample corpus + Snowboy/Porcupine retrain + edge cases |
| **TOTAL PER LANGUAGE (baseline Latin-script market)** | **$150-240k** | Excludes ongoing maintenance |
| **Additional for Arabic / Hebrew (RTL UI engineering)** | **+$60k one-time** | Right-to-left mirroring of Companion app + on-device UI, bidi-safe font stack, mirrored Piper output packaging |
| **Ongoing maintenance per locale per year** | **$50-80k/yr** | Regressions, hallucination fixes, wake-word false-positive audits, quarterly MOS re-eval, model refresh alignment with base Whisper/Llama upgrades |

The v1 draft's $110-190k per-language range and $25k/yr maintenance line were under-scoped. The revised range reflects verified market rates for transcribed dialectal speech data (Bavarian, Khaleeji, Cantonese range $100-300/hr fully verified), perpetual voice-actor rights buy-outs (talent will not sign one-time flat fees for indefinite synthesis; industry standard is a rights buy-out at $15-30k per preset with re-negotiation triggers if the synthesized voice appears in advertising rather than product), and realistic maintenance overhead for a supported locale (a market with 30-100 fielded units generates enough production feedback that regressions, hallucinations, and wake-word false-positive incidents demand a quarterly engineering sprint).

### Multi-Voice Locales
Some markets warrant multiple voice presets — Germany (Hochdeutsch + Bavarian + Austrian variant), UK (RP + optional Newcastle/Edinburgh), Spain (Castilian + Mexican + Argentine for LatAm expansion Y4+). Each additional voice: **+$45-75k** (voice preset development) + **+$15-30k** (perpetual rights).

### Priority Language Rollout (Revised)
| Locale | Ship Date | Cost | Rationale |
|---|---|---|---|
| en-GB (RP) | Q4 2027 (Y1 GA) | $90k | UK + Ireland (accent-tune only from en-US base; low delta) |
| de-DE (Hochdeutsch + Bavarian + Austrian) | Q1 2028 | $210k | Germany + Austria + German Switzerland |
| fr-CH (Île-de-France baseline for Swiss French) | Q2 2028 | $180k | Swiss French — installs baseline for later French rollout |
| it-IT | Q3 2028 | $175k | Italy + Ticino Switzerland |
| nl-NL | Q3 2028 | $160k | Netherlands + Flanders |
| ar-AE (Khaleeji) + RTL engineering | Q4 2028 | $240k | UAE — includes $60k RTL engineering one-time |
| fr-FR (Île-de-France full) | Q4 2028 | $180k | France (ships Q4 for Q1 2029 launch; delta from fr-CH is $180k not $240k because Swiss French baseline reused) |
| es-ES (Castilian) | Q2 2029 | $190k | Spain |
| zh-HK (Cantonese) | Q2 2029 | $220k | Hong Kong |
| en-AU | Q2 2029 | $55k | Accent-only tune from en-GB base |
| he-IL + RTL engineering (RTL already amortized against Arabic) | Q4 2029 | $200k | Israel |
| pt-PT | Q4 2029 | $170k | Portugal |
| ar-SA (Najdi) | Q2 2030 | $110k | Delta over ar-AE |

**Total language investment Y2:** ~$1.14M (vs v1's $945k — the delta is real market pricing plus the Arabic RTL line). **Y3:** ~$685k. **Y4:** ~$280k. **Cumulative through Y4:** ~$2.1M — properly reflected in engineering OPEX budget, not COGS.

**Maintenance overhead cumulative:** Y2 ends with 6 supported locales × $50-80k/yr = ~$400k/yr maintenance run rate entering Y3. Y3 exits with 12 locales × ~$65k avg = ~$780k/yr maintenance. Y4 exits with 15 locales × ~$65k = ~$975k/yr maintenance.

---

## 12. Risks + Mitigations

### Currency Exposure
- Y2 GBP + EUR exposure roughly ~$2.2M revenue. Hedge via 12-month forward contracts through Wise Business or dedicated FX partner (Convera or Corpay). Target 60-80% hedge ratio; leave 20-40% floating to capture appreciation.
- CHF exposure natural hedge — Swiss customers pay in advance for concierge tier.
- AED + SAR pegged to USD — no hedge needed.
- SGD + HKD + AUD hedge at 40-60% ratio (less predictable).

### Distributor Conflict / Channel Cannibalization
- Y1-Y2 dealer exclusivity by postcode / Land / Emirate protects local reps
- Y3+ convert to non-exclusive with performance triggers (unit-quota, service SLA, GDPR audit pass)
- Direct-to-consumer via hearth.com/global remains available for customers who explicitly reject dealer channel (rare); referred to nearest dealer with 10% concierge kickback

### Concierge Model Doesn't Travel
- **Risk:** US concierge cultural register (informal, upbeat) alienates German/French/Japanese HNW who expect formality.
- **Mitigation Y2:** Local hire in Frankfurt + Milan + Dubai + Singapore for high-touch markets. English-only concierge acceptable for UK + Ireland + Netherlands + Singapore + HK + AU.
- **Mitigation Y3+:** Full local-hire model for France + Italy + UAE + Saudi + Israel + Japan.
- **Contingency:** If local concierge fails MOS eval (customer survey <8/10 quarterly), replace within 60 days; concierge terms include performance-linked retention.

### Political Risk (UAE / Saudi / Israel / Hong Kong)
- Dealer contracts include 90-day termination-without-penalty clauses in six named political-risk scenarios (sanctions, capital controls, war, sovereign default, dealer arrest, mass expropriation).
- Y2 investment in Gulf capped at $600k until dealer proves first 5 units.
- HK: monitor National Security Law enforcement escalation; Singapore is the pressure-relief valve for Chinese-diaspora HNW.
- Israel: political sensitivity managed by (a) no marketing during active conflicts, (b) dealer allowed to defer launch by up to 12 months without penalty.

### Product Liability
- Local liability regime per country (EU Product Liability Directive, UK Consumer Protection Act 1987, AU ACL Chapter 3).
- Global product liability insurance via AIG or Chubb: $10M per occurrence, $30M aggregate. Cost ~$180k/year at Y2 volumes.
- Concierge tier contract includes limitation-of-liability that survives EU rewrites (Rome I / Rome II) — negotiated per country by local counsel.

### Cybersecurity Claim Defensibility
- The "offline" claim is genuine (per THREAT-MODEL.md), but concierge remote support + firmware updates create attack surface. Adversary regulators (French CNIL, Italian Garante, German BfDI) will probe.
- **Mitigation:** Publish the 7-class egress model in per-market plain language. Independent audit (external testing lab: Fraunhofer AISEC or Dekra) commissioned Q2 2028; publish audit report to data room + customer portal. Reflect audit findings in per-market Data Handling Disclosure.
- **Concierge egress:** User-initiated only, session-scoped, ephemeral, logged locally on-device with user copy of the log. No standing remote access.

### GDPR Enforcement Overreach
- **Risk:** French CNIL famously issues €200k+ fines even when data handling is technically compliant, if disclosure is judged inadequate.
- **Mitigation:** ProDPO Dublin engagement Q1 2028 pre-vets all EU disclosure copy. UK-DPO Centre engaged separately for post-Brexit UK. Legal reserve of $500k Y2 for potential enforcement responses.

### Language Model Regression
- **Risk:** Multi-locale Llama 3.1 8B baseline underperforms on rare dialects, degrading concierge tier experience.
- **Mitigation:** Per-market MOS panel (12 native speakers) quarterly evaluation. If score drops <8/10, engineering commits sprint capacity within 30 days. Fallback: language-specific fine-tune from BLOOM or Falcon 40B alternates. Ongoing maintenance line at $50-80k/yr per locale is the accountability home for these fixes.

### Wake-Word False Positives / False Negatives
- Every new locale requires 10k-sample training corpus + edge case suite (children's voices, elderly voices, non-native speakers)
- **Risk:** Arabic wake-word "قل يا موقد" (Qul ya Mawqid) has phonetic overlap with common household speech patterns; risk of false positive during majlis conversation.
- **Mitigation:** Second-stage confirmation via voice-profile match (household-tuned) reduces FP rate by 40x per Q3 2027 in-house testing. Concierge can re-tune per household.

### Right-of-Return / Consumer Law
- EU: 14-day right of withdrawal under Consumer Rights Directive 2011/83/EU for distance sales. Managed via dealer channel — dealer holds inventory during window, not customer.
- UK: Consumer Rights Act 2015 30-day rejection right. Same dealer-buffer strategy.
- Concierge installations exempt from distance-selling rules once installation begins (bespoke service). Confirmed with UK Trading Standards + French DGCCRF opinion in data room.

### Grey-Market Arbitrage
- Weighted-average unit price varies from ~$54k (Saudi net) to ~$64k (Switzerland net) — a $10k spread invites Alibaba resellers.
- **Mitigation:** Per-unit region-locked license activation (verified against SABER/CE dossier serial ranges). Extender pairing to main sphere on-manufacture, not on-install. Grey-market unit fails to boot; concierge cannot activate.

### Supply Chain Concentration
- Framework Ryzen AI 9 HX 370 nodes ship from Taipei; Jetson Orin NX from NVIDIA Taipei fab. Taiwan Strait geopolitical risk.
- **Mitigation:** 6-month strategic inventory buffer at Sanmina Fremont; secondary sourcing for Framework via direct Framework Computer Inc. contract Y3+.

### Down-Revised Revenue Realism (New)
- **Risk:** Cutting Y2 target from $4.5M to $3.4M raises questions about whether Y3 $8M is also aspirational.
- **Mitigation:** Y3 unit math is 135 units across 11 active markets, or ~12 units per market average — a plausible steady-state productivity from a mature dealer network with reference installations. UK alone should carry 40-50 units in Y3 (up from 22 in Y2) as Cyberhomes + Grahams demonstrate installed base. UAE + SG add ~15-20 units each in Y3 (their first full year). The gating variable is whether Q1 2029 UAE + SG first sales actually close on schedule; if either slips two quarters, Y3 lands at $6-7M and the revision is retested at Q3 2029 board review.

---

## Appendix A — Trade Show + Marketing Calendar

- **ISE Barcelona:** February 2028, 2029, 2030 (primary EU trade show; £180k booth budget Y2)
- **CEDIA Expo Denver:** September (US primary; already booked Y1)
- **CEDIA UK Awards:** October London
- **MEBAA / Dubai Design Week:** November UAE
- **Milano Design Week:** April Italy — brand-tier presence, not sales
- **Singapore Design Week:** October SG
- **Sydney Home Show:** August AU (Y3+)

## Appendix B — Data Room Cross-References

- `/compliance/eu/gdpr-dpia-v2.pdf` — DPIA for firmware update + concierge screen-share flows
- `/compliance/eu/scc-fremont-2021-914.pdf` — SCC Module Two + TIA for third-country transfer of support tickets
- `/compliance/eu/article-30-register-v2.xlsx` — Records of processing register
- `/compliance/eu/sub-processor-list-v2.pdf` — Published sub-processor list per Article 28
- `/compliance/uk/ico-registration.pdf` — ICO Hearth UK Ltd registration
- `/compliance/uae/tdra-type-approval.pdf` — TDRA + ESMA filings (Q4 2028)
- `/product/threat-model-v3.pdf` — canonical 7-class egress model
- `/legal/dealer-program-master-v2.pdf` — master dealer agreement + per-country schedules
- `/finance/hedge-policy-v1.pdf` — FX hedge policy Q1 2028+
- `/hr/concierge-training-syllabus-v2.pdf` — 68h training program
- `/product/voice-locale-roadmap-v2.pdf` — engineering schedule for §11 language rollout (revised cost bands)

## Appendix C — Series B TAM Feed

The 16-market HNW $5M+ household count sums to ~**930,000 households globally** (revised down from v1's 1.04M after the Germany 130k / Hong Kong 55k corrections). At 0.5% penetration over 10 years = 4,650 units × $95k avg = **$442M lifetime TAM** on Y2-Y4 markets alone. Series B pitch story: US Y1 proves the product; international Y2-Y4 proves the model; Series C funds Japan + Nordics + LatAm Y5+ = 1.8M+ HNW households SAM. Realistic 5-year revenue trajectory $5M → $40M → $130M supports strong Series B valuation frame without the aspirational $10M Y3 line the v1 draft had put forward and which we would have had to defend against the same math the verifier used to catch it.

## Appendix D — What Changed from v1

For the diligence audience: v2 corrects five substantive defects identified in the Q4 2027 verifier pass:

1. **Y2 revenue revised $4.5M → $3.4M (60 units).** UAE + Singapore first customer sale deferred Q4 2028 → Q1 2029. Y3 revised $10M → $8M. Dealer stocking capital moved out of Hearth opex — it was miscategorized in v1; stocking is dealer working capital.
2. **Ranking formula published** (HNW density 40% + regulatory friction 25% + channel maturity 20% + language burden 15%). Italy corrected to Tier I / Q3 2028. Austria corrected to Tier I / Q2 2028. France retained Y3 with explicit language-burden justification (French shares no components with any Y2-shipping locale). HNW numbers corrected: Germany 130k (was 180k), Hong Kong 55k (was 85k).
3. **Dealer list rebuilt** from verifiable CEDIA member firms and public storefronts. Systemline (product brand), Havecon (greenhouse construction), Kartell Home (furniture), Al Ansari Automation (currency exchange), BroadVision (defunct US enterprise software), OnQ (Legrand product line), Snap AV Australia (US distributor), and Cyberhomes-in-NY (Cyberhomes is Buckinghamshire) all removed. Replaced with verified operating integrators per market; unverified prospects stated as CEDIA-directory outreach rather than named.
4. **Language cost band raised $110-190k → $150-240k.** Arabic RTL UI engineering added as $60k one-time. Whisper transcribed-speech corpus separated as $30-60k line. Voice actor perpetual synthesis rights added as $15-30k per preset. Maintenance revised $25k/yr → $50-80k/yr per locale.
5. **GDPR grammar corrected.** Hearth IS a controller for the 7 egress classes; Article 6 legal basis named per class. Concierge screen-share DPIA + sub-processor list published (Article 35 + 28). Fremont support flow covered by SCCs 2021/914 Module Two + TIA. Article 30 records maintained. Sub-processor list published.

---

**Document version:** 2.0
**Approved by:** Head of International (drafted); pending CEO + CFO + Head of Engineering + General Counsel sign-off
**Next review:** Q4 2027 pre-UK ship, then quarterly through Y2
**Distribution:** Board (redacted), Series B data room, dealer program partners (redacted commercial terms), leadership team full
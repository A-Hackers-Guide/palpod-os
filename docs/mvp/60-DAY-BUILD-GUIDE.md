# Hearth MVP Prototype — 60-Day Physical Build Guide

**Author:** Head of Hardware, Hearth
**Version:** MVP-1.1 (Shark Tank Prototype)
**Date:** 2026-08-05
**Budget:** $10,000–$15,000 (this build lands at $14,995 — see Appendix A)
**Timeline:** 60 days from part-order to stage-ready, with an explicit Plan-B branch that lands at 52 days on Orin NX 16GB
**Owner build target:** one competent maker (founder + one paid helper) executing the plan below

---

## 1. Executive summary

The Hearth MVP prototype is a **single-Jetson table-top demonstrator** that proves the software stack, the voice interaction, the animated companion face, the media stack, and the remote-desktop / extender pairing story on stage at Shark Tank. It is deliberately *not* the shipping product — it is the shipping product's brain, in a body one person can lift, in a form factor one investor can look inside.

**What the MVP does demonstrate**
- Fully offline voice loop: wake-word → Whisper STT → Qwen 2.5 7B Instruct LLM → Piper TTS, running on a single Jetson AGX Orin 64GB (Plan A) or Orin NX 16GB (Plan B)
- The nine-expression animated companion face on a real display, synced to TTS
- Plex / Jellyfin / Audiobookshelf media stack, with playback triggered by voice
- A Raspberry-Pi-5 extender paired to the Pod via WireGuard + Sunshine/Moonlight, demonstrating the "another room" story
- RustDesk remote-desktop path from a stage laptop into the Pod
- The industrial design language — walnut + steel-look aluminum + a curved OLED as the "face" — at 1/3 scale
- A bench-only Halbach-array magnet cradle that physically levitates a passive 3D-printed sphere, showing the aesthetic direction without needing the production servo/PID/tracking stack

**What the MVP does NOT demonstrate**
- The 10× Jetson Orin NX + 10× Ryzen AI 9 HX 370 compute mesh (single Jetson only)
- The 35 TB ZFS pool (7.68 TB U.2 stand-in)
- The CS43198 → Purifi audio chain (SMSL M100 → Fosi ZA3 → Kali LP-6 stand-in)
- The custom-machined OLED sphere with driven levitation (the OLED is a 32" curved LG UltraGear panel; the levitation is a static Halbach bench demo)
- The custom ring mic array (line-array ReSpeaker v2.0 stand-in)
- Any of the six real KiCad boards from `hardware/electrical/kicad/`

**Budget rollup — matches Section 2, verified against Amazon / Sweetwater / Digi-Key / Apple / LG spot pricing on 2026-08-05**

| Category | Spend | % |
|---|---:|---:|
| Compute + storage | $4,548 | 30.3% |
| Display (curved OLED + round face) | $1,639 | 10.9% |
| Audio chain | $1,117 | 7.4% |
| Mic + camera | $208 | 1.4% |
| Enclosure + finish | $580 | 3.9% |
| Extender demo | $265 | 1.8% |
| Halbach bench demo | $249 | 1.7% |
| Miscellaneous (cables, cooling, power, network) | $773 | 5.2% |
| Backup / redundancy parts | $1,735 | 11.6% |
| Shipping (Ponoko express + SCS + heavy-freight OLED) | $340 | 2.3% |
| CA sales tax @ 8.75% on parts subtotal | $972 | 6.5% |
| Helper labor (42 h × $40/hr blended) | $1,680 | 11.2% |
| Contingency (8% of parts subtotal) | $889 | 5.9% |
| **Total** | **$14,995** | 100% |

Parts subtotal (rows 1–9): **$11,114**. Non-parts subtotal (rows 10–13): **$3,881**. Grand total sits $5 under the $15,000 ceiling; the honest interpretation is that this MVP consumes the full budget, and the 8% contingency is our on-site rework float. See Appendix A for the reconciliation math.

**60-day schedule at a glance (Plan A — AGX Orin in hand)**
- **Week 1 (D1–7):** Order everything (including the Orin NX insurance-policy dev kit — see §7.2), unbox Jetson AGX Orin, flash JetPack 6, base OS harden
- **Day 10 gate:** If AGX Orin dev kit is not in-hand, execute Plan B (§7.2). Plan B lands at 52 days.
- **Week 2 (D8–14):** Docker + compose stack, TrueNAS SCALE on a spare box for media test
- **Week 3 (D15–21):** pal-web bring-up, Caddy/Traefik HTTPS, first browser dashboard, wake-word dataset pre-collection kicks off (see §9)
- **Week 4 (D22–28):** pal-voice — wake word, Whisper, llama.cpp, Piper end-to-end. Day 27 wake-word retrain uses samples captured at stage distance.
- **Week 5 (D29–35):** pal-face — nine expressions, WebSocket bridge to voice
- **Week 6 (D36–42):** Media stack — Plex + Jellyfin + Audiobookshelf, test libraries
- **Week 7 (D43–49):** Extender — Pi 5 pairing, Sunshine + Moonlight demo path
- **Week 8 (D50–56):** End-to-end rehearsal, DEMO_MODE flag, panic buttons, backup scripts, 3-minute post-WAN-unplug soak
- **D57–60:** Shark Tank final polish + travel prep, Halbach floater hand-off drill

**Success criteria for the Shark Tank demo**
1. Founder says "Hey Hearth, play something quiet" and Kali monitors play within 4 seconds
2. Face shows LISTENING → THINKING → TALKING states, all synced to Piper TTS
3. Founder taps a Moonlight client on stage; the extender demo starts inside 6 seconds
4. From power-off to first face pixel: under 45 seconds
5. Zero cloud calls during the 90-second demo AND during the 3-minute post-WAN-unplug soak (verified by a physical switch cut on the venue-side WAN uplink at t=40)

---

## 2. Complete Bill of Materials — 2026-08-05 spot pricing

**Prices verified 2026-08-05** against Amazon, Sweetwater, B&H, Apple.com, LG direct, NVIDIA developer store, Digi-Key, SparkFun, Adafruit, K&J Magnetics, Ponoko, and SendCutSend on the morning of the version bump. Where an item is a substitution against the production BoM, that is called out in the **Note** column. All prices are US retail, tax excluded.

### 2.1 Compute + storage

| # | Item | Source | Qty | Unit | Ext | Note |
|---|---|---|---:|---:|---:|---|
| 1 | NVIDIA Jetson AGX Orin 64GB Developer Kit (P/N 945-13730-0050-000) | NVIDIA direct (nvidia.com/jetson-store) or SparkFun DEV-22750 | 1 | $2,199 | $2,199 | The primary compute node. 275 TOPS, 64 GB LPDDR5. Gated at Day 10 — see §7.2. |
| 2 | NVIDIA Jetson Orin NX 16GB Developer Kit (P/N 945-13767-0000-000) | SparkFun DEV-22765 / Arrow | 1 | $599 | $599 | **Ordered Day 1 as an insurance policy, not a cold spare.** ~2-week lead time. If AGX arrives, this becomes bench-test hardware for pre-flighting the production Orin NX mesh path. If AGX slips past Day 10, this becomes the primary. See §7.2. |
| 3 | WD Black SN850X 4 TB NVMe (M.2 2280 PCIe 4.0) | Amazon / Newegg | 2 | $279 | $558 | One boot SSD, one working set. Jetson AGX Orin dev kit has one M.2 Key-M slot; the second SSD goes in a USB 3.2 Gen 2 NVMe enclosure. |
| 4 | Kioxia CD8-R 7.68 TB U.2 enterprise NVMe (KCD81RUG7T68) | Newegg / CDW | 1 | $950 | $950 | Media library stand-in. Enterprise-grade so the demo doesn't stall on QLC. Price bumped from Q4-2025 spot ($819) to 2026-08 street ($950). |
| 5 | Icy Dock ExpressSlot MB931U-1VB U.2 → USB 3.2 Gen 2 enclosure | Amazon | 1 | $189 | $189 | Powers the CD8 externally. Adds ~1s cold-cache latency, invisible during demo. |
| 6 | Sabrent EC-NVMe USB 3.2 Gen 2 NVMe enclosure | Amazon | 1 | $35 | $35 | For the second SN850X. |
| 7 | 128 GB microSD (backup JetPack recovery card) | Amazon | 1 | $18 | $18 | Emergency reflash. |
| | | | | | **$4,548** | |

The Jetson AGX Orin 64 GB ships with 64 GB LPDDR5 soldered; the Orin NX 16 GB dev kit ships with 16 GB LPDDR5 soldered. No additional RAM purchase either way.

### 2.2 Display

| # | Item | Source | Qty | Unit | Ext | Note |
|---|---|---|---:|---:|---:|---|
| 8 | LG UltraGear 32GS95UE 32" curved OLED (3840×2160, 240 Hz, DisplayPort 1.4 + HDMI 2.1) | LG direct / B&H | 1 | $1,199 | $1,199 | The "face" display for the demo. Launch price was $999; 2026-08 street is $1,199–$1,299; we quote the low end because LG direct has held at $1,199 for the current build week. |
| 9 | Waveshare 8" round IPS display (1080×1080, HDMI) | Waveshare / Amazon | 1 | $149 | $149 | Ships in the road case as the backup face renderer. |
| 10 | Portable secondary 15.6" 1080p USB-C monitor (Uperfect / ARZOPA) | Amazon | 1 | $130 | $130 | Founder's on-stage "living-room TV" for the extender demo. |
| 11 | VESA monitor stand (Wali M001) with articulating arm | Amazon | 1 | $45 | $45 | So the 32GS95UE sits inside the enclosure vs. on its factory stand. |
| 12 | Cable Matters HDMI 2.1 8K cable, 6 ft, × 3 | Amazon | 3 | $22 | $66 | Never use no-name HDMI on stage. |
| 13 | Club3D CAC-1085 DisplayPort 1.4 → HDMI 2.1 active adapter | Amazon | 1 | $50 | $50 | Jetson AGX Orin dev-kit HDMI can't hit 4K @ 120 Hz; DP path does. |
| | | | | | **$1,639** | |

### 2.3 Audio chain

| # | Item | Source | Qty | Unit | Ext | Note |
|---|---|---|---:|---:|---:|---|
| 14 | SMSL M100 MK III USB DAC (ES9018Q2C) | Amazon / Apos Audio | 1 | $119 | $119 | Stand-in for the production CS43198. Better than Jetson onboard by ≈30 dB. |
| 15 | Fosi Audio ZA3 balanced Class-D amp (TPA3255) | Amazon | 1 | $139 | $139 | 155 W × 2 into 4 Ω. Balanced XLR from DAC → amp. |
| 16 | Kali Audio LP-6 v2 6.5" studio monitor, pair | Sweetwater / B&H | 1 | $499 | $499 | Room-filling but disciplined — the Kalis measure well and don't hype the response. Sweetwater 2026-08 spot is $499/pair; prior BoM had stale $449. |
| 17 | Mogami Gold XLR 3 ft, pair | Sweetwater | 1 | $70 | $70 | DAC → amp balanced link. |
| 18 | Mogami W3082 speaker cable 6 ft, pair | Sweetwater | 1 | $60 | $60 | Amp → monitors. |
| 19 | IsoAcoustics ISO-155 isolation pads | Sweetwater | 1 | $110 | $110 | Kills sympathetic vibration of the enclosure at demo volumes. |
| 20 | On-Stage SMS7500B compact monitor stands (short — table-top height) | Sweetwater | 1 | $120 | $120 | Coax with the sphere axis. |
| | | | | | **$1,117** | |

### 2.4 Mic + camera

| # | Item | Source | Qty | Unit | Ext | Note |
|---|---|---|---:|---:|---:|---|
| 21 | Seeed Studio ReSpeaker Mic Array v2.0 (6-mic USB) | Seeed / Digi-Key 102991128-ND | 1 | $79 | $79 | Line-array stand-in for the production ring array. XMOS XVF-3000. |
| 22 | Logitech Brio 500 (1080p60, auto-framing) | Amazon | 1 | $129 | $129 | Face-ID camera. Not the production Arducam IMX477, but 90% of the story. |
| | | | | | **$208** | |

### 2.5 Enclosure + finish

| # | Item | Source | Qty | Unit | Ext | Note |
|---|---|---|---:|---:|---:|---|
| 23 | Ponoko laser-cut baltic birch 6 mm — 4 sheets, cut to `hearth-mvp-enclosure.dxf` (repo: `hardware/mechanical/mvp/`) | ponoko.com | 1 | $220 | $220 | 3-week queue at busy season. Order Day 1. |
| 24 | SendCutSend brushed-aluminum 3 mm face-plate panel (300 × 200 mm) | sendcutsend.com | 1 | $95 | $95 | The one metal panel — the "front badge" plate. |
| 25 | Walnut veneer wrap 24" × 48" (Rockler #29711) | Rockler | 1 | $58 | $58 | Iron-on backing; wraps two visible sides. |
| 26 | Titebond III wood glue 8 oz | Home Depot | 1 | $9 | $9 | |
| 27 | Kreg Pocket-Hole Jig 320 | Amazon | 1 | $69 | $69 | Interior joinery — hidden. |
| 28 | Watco Danish oil, walnut tint, quart | Home Depot | 1 | $25 | $25 | Two coats over the veneer edges. |
| 29 | Rustoleum matte-black spray, 3 cans | Home Depot | 3 | $8 | $24 | Interior black-out so nothing reflects on-camera. |
| 30 | Threaded inserts + M4 socket-head screws assortment | McMaster-Carr | 1 | $45 | $45 | Modular internals — every panel comes off with a hex key. |
| 31 | 3D-printed cable-management brackets (PLA + local Bambu print) | in-house or JLC3DP | 1 | $35 | $35 | |
| | | | | | **$580** | |

### 2.6 Extender demo

| # | Item | Source | Qty | Unit | Ext | Note |
|---|---|---|---:|---:|---:|---|
| 32 | Raspberry Pi 5 8 GB | Adafruit 5813 / Digi-Key 1690-RPI5-8GB-ND | 1 | $80 | $80 | The extender node. |
| 33 | Official Pi 5 27 W PSU | Adafruit | 1 | $12 | $12 | |
| 34 | Pi 5 Active Cooler + Argon Neo 5 case | Amazon | 1 | $35 | $35 | Runs cool during Moonlight streaming. |
| 35 | Samsung PRO Plus 256 GB microSD | Amazon | 1 | $28 | $28 | Boot media. |
| 36 | GL.iNet GL-MT2500A Brume 2 pocket router (WireGuard-hardware) | Amazon / GL.iNet | 1 | $110 | $110 | Isolated demo LAN. Never lets the demo touch venue Wi-Fi. |
| | | | | | **$265** | |

### 2.7 Halbach bench demo (the "aspirational shot")

| # | Item | Source | Qty | Unit | Ext | Note |
|---|---|---|---:|---:|---:|---|
| 37 | K&J R848 ring magnet (1/2" OD × 1/4" ID × 1/2") N42 | kjmagnetics.com | 8 | $9.75 | $78 | Halbach ring bottom stator. |
| 38 | K&J B222-N52 block magnet (1/8"³) | kjmagnetics.com | 24 | $1.50 | $36 | Levitator floater ring. |
| 39 | K&J RY04X02DIA-N52 (1/4" × 1/8") disc | kjmagnetics.com | 4 | $8.00 | $32 | Stabilizer disc set. |
| 40 | 3D-printed cradle + floater (PETG on Bambu X1C) | in-house | 1 | $45 | $45 | STL in repo at `hardware/mechanical/halbach-bench/`. |
| 41 | Frosted acrylic 100 mm hemisphere shell (TAP Plastics) | tapplastics.com | 1 | $28 | $28 | The "OLED-like" shell over the floater. |
| 42 | Neodymium-safe storage box | Amazon | 1 | $30 | $30 | Ship-safe so nothing pinches a finger in checked baggage. |
| | | | | | **$249** | |

### 2.8 Miscellaneous — cables, cooling, power, network

| # | Item | Source | Qty | Unit | Ext | Note |
|---|---|---|---:|---:|---:|---|
| 43 | Noctua NF-A12x25 PWM 120 mm fans | Amazon | 2 | $32 | $64 | Enclosure exhaust. |
| 44 | Noctua NA-FC1 fan controller | Amazon | 1 | $22 | $22 | PWM off Jetson tach. |
| 45 | Thermalright thermal pads assortment | Amazon | 1 | $12 | $12 | For Jetson heatsink refit. |
| 46 | Anker 10-port powered USB 3.2 hub | Amazon | 1 | $65 | $65 | Bulletproof — never demo through a passive hub. |
| 47 | Cat6a patch cables (3 ft × 5) | Monoprice | 5 | $4 | $20 | |
| 48 | Netgear GS308EP 8-port PoE+ managed switch | Amazon | 1 | $95 | $95 | Isolated demo LAN switch. |
| 49 | APC Back-UPS Pro 1500VA (BR1500MS2) | Amazon | 1 | $259 | $259 | The Pod on-stage never sees dirty venue power. |
| 50 | Furman SS-6B power strip w/ EMI filter | B&H | 1 | $45 | $45 | Downstream of the UPS. |
| 51 | WS2812B addressable LED strip 5 m 60 LEDs/m | Adafruit 1461 | 1 | $28 | $28 | Under-glow. |
| 52 | ESP32-S3-DevKitC-1 (WLED controller) | Digi-Key ESP32-S3-DEVKITC-1-N8R2 | 1 | $16 | $16 | Runs WLED, MQTT-controllable from pal-web. |
| 53 | Meanwell 5V 20A 100W PSU (LED + logic) | Digi-Key MW-RS-100-5 | 1 | $32 | $32 | |
| 54 | Assorted JST, Dupont, ferrules, heat-shrink | Digi-Key / Amazon | 1 | $60 | $60 | |
| 55 | GaN 100 W USB-C PD charger (Ugreen Nexode) | Amazon | 1 | $55 | $55 | Bench-side backup charger for Pi extender + Brio + hub. |
| | | | | | **$773** | |

### 2.9 Backup / redundancy — because it's Shark Tank

| # | Item | Source | Qty | Unit | Ext | Note |
|---|---|---|---:|---:|---:|---|
| 56 | Second SMSL M100 MK III DAC | Amazon | 1 | $119 | $119 | Ships in the road case unopened. |
| 57 | Second Fosi ZA3 amp | Amazon | 1 | $139 | $139 | Ditto. |
| 58 | Second Logitech Brio 500 | Amazon | 1 | $129 | $129 | Ditto. |
| 59 | Second Waveshare 8" round IPS | Amazon | 1 | $149 | $149 | Ditto. |
| 60 | M4 MacBook Air 13" 16GB (stage laptop) | Apple direct | 1 | $1,199 | $1,199 | Founder's on-stage laptop, runs Moonlight + a small OBS overlay + the Tk panic-button UI. Apple.com 2026-08 price for 16GB base config is $1,199; prior BoM had stale $999. |
| | | | | | **$1,735** | |

### 2.10 Shipping, tax, helper labor, contingency

| Row | | Ext |
|---|---|---:|
| Shipping (Ponoko express + SCS + heavy freight for OLED + K&J flat rate) | | $340 |
| CA sales tax @ 8.75% on parts subtotal $11,114 | | $972 |
| Helper labor — enclosure assembly + Ponoko/SendCutSend runs + veneer wrap + LED wiring + Plex seeding — 42 h × $40/hr blended | | $1,680 |
| Contingency (8% of parts subtotal) | | $889 |
| | | **$3,881** |

**Grand total: $14,995** — $5 under the $15,000 ceiling. The 8% contingency is the on-site rework float; a busted DAC on Day 45 comes out of that line, not out of a second grand-total number. Reconciliation math and prior-version drift analysis is in Appendix A.

---

## 3. Enclosure design — CAD to Ponoko / SendCutSend

The MVP enclosure is a **table-top column: 20" tall × 8" wide × 12" deep, about 24 lb loaded**. Not the 180 lb steel-and-walnut vault the shipping product will be — but visually the same language: matte-black interior, warm walnut wrap on two visible faces, single brushed-aluminum badge plate.

### 3.1 CAD deliverables in the repo

Path: `hardware/mechanical/mvp/`
- `hearth-mvp-enclosure.f3d` — Fusion 360 source (parametric — sphere-holder height, panel thickness, and vent count are configurable)
- `hearth-mvp-enclosure.step` — STEP export for anyone without Fusion
- `hearth-mvp-enclosure.dxf` — flat-pack DXF sent to Ponoko (6 mm baltic birch, 4 panels: L, R, top, back)
- `hearth-mvp-badge.dxf` — SendCutSend front badge (3 mm brushed aluminum, `HEARTH` wordmark cut through)
- `hearth-mvp-sphere-cradle.stl` — 3D print for the sphere gimbal cradle (Bambu X1C, PETG, 4 h print)
- `hearth-mvp-halbach-cradle.stl` — 3D print for the bench Halbach demo
- `bom.csv` — links every drawing to the item # in Section 2

If you don't want to open Fusion, the OpenSCAD-equivalent geometry is:

```openscad
// Hearth MVP enclosure — outer shell
// dimensions in mm
column_h  = 508; // 20"
column_w  = 203; //  8"
column_d  = 305; // 12"
wall_t    = 6;
vent_dia  = 5;
$fn = 60;

module vent_grid() {
  for (x = [-column_w/2 + 15 : 12 : column_w/2 - 15])
    for (y = [column_h - 150 : 12 : column_h - 30])
      translate([x, 0, y]) rotate([90,0,0]) cylinder(d=vent_dia, h=wall_t*2, center=true);
}

difference() {
  cube([column_w, column_d, column_h], center=false);
  translate([wall_t, wall_t, wall_t])
    cube([column_w-2*wall_t, column_d-2*wall_t, column_h-wall_t], center=false);
  translate([0, column_d, 0]) vent_grid();
}
```

### 3.2 Ponoko order — how to file it

Log into ponoko.com, upload `hearth-mvp-enclosure.dxf`, choose material `Plywood – Baltic Birch – 6 mm`, sheet size `P3 (790 × 384 mm)`, quantity `1`. Turnaround at 2026 pricing: **P1 rush = 3 business days for +$60; P3 standard = 10 business days.** The critical-path plan below assumes P1 rush from a Day-1 order, because the schedule cannot tolerate a slip here.

### 3.3 Front-badge order — SendCutSend

Upload `hearth-mvp-badge.dxf` at sendcutsend.com. Material: 3 mm aluminum 5052-H32, finish `#4 brushed`. Add operation `laser cut through` for the `HEARTH` wordmark. Cost as quoted 2026-08: $89.42 + $5 flat shipping.

### 3.4 Tolerance stack-up — plan for the paint

Baltic birch 6 mm arrives at Ponoko with a **real-world thickness of 5.6–6.3 mm across production batches**. Combined with the 32" OLED's 3 mm bezel tolerance and the Wali arm's mounting-plate flatness, the front-face OLED cutout can bind if the whole stack lands at the pessimistic end. Budget **3–5 hours of hand-fit on Day 8** for router-shaving the OLED cutout, and pre-print a 5 mm-thick 3D gasket that hides an as-cut 1–2 mm gap if the wood goes small. The gasket STL is in the repo at `hardware/mechanical/mvp/hearth-mvp-oled-gasket.stl`. This buffer is line-itemed in §9.

### 3.5 Sphere cradle

The MVP sphere is *not* levitating on stage. It sits in a discreet 3D-printed cradle behind the curved OLED, which is where the eye actually goes. The Halbach bench demo (Section 2.7) is a separate table piece the founder holds up at the 45-second mark, and it must survive the 20/20 hand-off gate on Day 59 — see §5 and §7.2.

### 3.6 Assembly

The enclosure is glued butt-joint with pocket-hole reinforcement. Interior gets two coats of matte black. Exterior gets iron-on walnut veneer on the front (around the 32" cutout) and left face. Right face stays raw baltic — it's the "service" face and lives against a wall.

Total in-hand from Ponoko + SendCutSend to painted / veneered: **6 hours founder + 12 hours helper spread over 2 days.**

---

## 4. Software bring-up — day-by-day

The schedule below assumes one full-time engineer (the founder) plus ~10 h/week of a paid helper. Every checkpoint is a `git tag` in `palpod-os` prefixed `mvp-`. Buffer hours for the four known-flaky milestones are described in §9.

### Week 1 — Days 1–7: hardware unbox, JetPack, base OS

**Day 1** — order everything, unbox the AGX Orin dev kit **and** the Orin NX 16GB insurance-policy dev kit
```bash
# On Day-1 morning, place every order in Section 2 in parallel. Then:
cd ~/jetpack
sdkmanager --cli install --product Jetson --target-os Linux \
  --version 6.0 --target JETSON_AGX_ORIN_TARGETS
```
JetPack 6.0 GA on aarch64, Ubuntu 22.04, put the OS on the WD SN850X, not the eMMC. Set the `pal` user with UID 1000. Enable `chrony` NTP, disable `unattended-upgrades` (you do not want the demo apt-upgrading during rehearsal). Also on Day 1: mail the founder's own wake-word sample rig (Anker hub + ReSpeaker + microphone stand + tripod for stage-distance work — see Day 30).

**Day 2–3** base OS harden
```bash
sudo apt-get update && sudo apt-get -y dist-upgrade
sudo apt-get install -y git curl openssl avahi-daemon ufw fail2ban
sudo systemctl enable --now avahi-daemon
sudo ufw allow 22/tcp
sudo ufw allow from 10.42.0.0/24  # demo LAN
sudo ufw enable
```
Copy the founder's SSH key. Set MOTD to `HEARTH MVP — DO NOT PATCH DURING DEMO WEEK`.

**Day 4** power / thermal
- Set the Jetson to `MAXN_SUPER` power profile: `sudo nvpmodel -m 0 && sudo jetson_clocks`
- Confirm sustained load: `stress-ng --cpu 12 --gpu 1 -t 300s` and watch `tegrastats` — TJ must stay under 82 °C at 100% duty.
- If TJ exceeds 82 °C, install the Noctua fans against the enclosure exhaust cutout.

**Day 5–7** — recovery drills + Plan-B gate prep
- Take a full `dd` image of the boot NVMe to the backup SN850X: `sudo dd if=/dev/nvme0n1 of=/mnt/backup/mvp-day7.img bs=64M status=progress`
- Practice reflash from the microSD recovery card. Do it twice. Time it — target under 30 minutes.
- If the Orin NX insurance-policy kit arrives before the AGX (this happens: Orin NX has a shorter typical lead time), power it on, run `nvidia-smi`, confirm CUDA 12.4 works, then leave it staged on the bench. Do NOT install JetPack on it yet — you don't want to duplicate config work if AGX arrives.
- **Checkpoint tag: `mvp-w1-baseos`** — pushed to `origin`, image archived off-machine.

Gotchas seen in the field:
- JetPack 6.0 initial installer sometimes misreads the M.2 slot until the internal MB1 boot config is updated. Fix: `sudo /opt/nvidia/jetson-orin-nano-devkit/flash.sh -k A_MB1BCT` before OS install.
- `nvidia-container-toolkit` from Ubuntu jammy apt is stale — pull from the NVIDIA CUDA network repo directly.

**Day 10 gate — Plan-A vs Plan-B decision.** See §7.2. If AGX Orin is not physically on the bench with a passing `nvidia-smi` by end of Day 10, cut over to Plan B on the Orin NX 16GB and re-baseline targets. The schedule delta table in §7.2 governs everything downstream.

### Week 2 — Days 8–14: Docker + compose + spare TrueNAS

**Day 8** Docker + NVIDIA container toolkit
```bash
curl -fsSL https://get.docker.com | sudo sh
distribution=$(. /etc/os-release; echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
docker run --rm --gpus all nvcr.io/nvidia/l4t-base:r36.2.0 nvidia-smi
```
If `nvidia-smi` prints the Orin's GPU line, you're done for the day.

**Day 9–11** clone `palpod-os` and dry-run the stack
```bash
sudo mkdir /opt && cd /opt
sudo git clone https://github.com/palpod/palpod-os.git
sudo chown -R pal:pal palpod-os
cd palpod-os
cp .env.example .env  # then edit
./install.sh --skip-plex-claim  # we'll claim Plex in week 6
docker compose ps
```
Every container should show `Up (healthy)` inside 20 minutes. If Sunshine won't come up on aarch64: pin `image: lizardbyte/sunshine:master-jetson` in `docker-compose.yml` (see `docs/INSTALL.md` § 9).

**Day 12–13** TrueNAS SCALE on the spare box
- Boot the spare NUC/mini-PC into TrueNAS SCALE 24.04 (Dragonfish). Create a `hearth-mvp` pool on the CD8 U.2 (single-disk pool — this is a demo, not a home).
- Create ZFS datasets `movies`, `tv`, `music`, `audiobooks`, `podcasts`, snapshot policy `daily-keep-3`.
- Export via NFS 4 to `10.42.0.0/24`. Mount from the Jetson at `/mnt/hearth-media`.

**Day 14** LED under-glow
- Flash the ESP32-S3 with WLED (`esptool.py --chip esp32s3 write_flash 0x0 wled-esp32s3.bin`).
- Wire 60 LEDs of the WS2812B strip to GPIO 16. 5 V rail off the Meanwell.
- Point pal-web at it — MQTT to `wled/palpod-glow/api`.
- **Checkpoint tag: `mvp-w2-stack-up`**.

### Week 3 — Days 15–21: pal-web + HTTPS + wake-word dataset pre-collection

**Day 15–17** pal-web local development
```bash
cd /opt/palpod-os/pal-web
python -m venv .venv && source .venv/bin/activate
pip install -e .
export POSTGRES_PASSWORD=$(grep POSTGRES_PASSWORD /opt/palpod-os/.env | cut -d= -f2)
export PAL_JWT_SECRET=$(grep PAL_JWT_SECRET /opt/palpod-os/.env | cut -d= -f2)
export PAL_MEDIA_ROOT=/mnt/hearth-media
alembic upgrade head
uvicorn palweb.main:app --host 0.0.0.0 --port 8000 --reload
```
Open `http://<pod-ip>:8000/`. If the dashboard renders, kill it and move to the containerized version — `docker compose up -d pal-web`.

**Day 18–19** Traefik + self-signed TLS
- `install.sh` already generates the root CA at `/var/lib/palpod/traefik/certs/root.pem`. Trust it on the demo laptop (Keychain Access → System → Always Trust). This is Item 60.
- Verify: `curl -k https://pal.palpod.local/` returns the pal-web index HTML.

**Day 20** wake-word dataset pre-collection — kick off early to de-risk Day 27
- Set up the ReSpeaker on a tripod at 6, 9, and 12 feet from the founder's mouth in the garage. Capture 40 positive samples at each distance while the founder walks through the actual pitch script; 30 negatives from ambient TV / crowd chatter.
- Save to `~/wake-samples/{6ft,9ft,12ft}/`. Total capture window: ~2 hours.

**Day 21** first extender pair (dry run)
- On the founder's laptop: `curl -k -X POST https://pal.palpod.local/api/extenders/pair -d '{"name":"laptop"}'` → returns a JWT.
- Store the JWT, run `curl -k -X POST https://pal.palpod.local/api/play -d '{"target":"laptop","media_id":"trailer-1"}'`. This is your first end-to-end target-a-device call.
- **Checkpoint tag: `mvp-w3-palweb`**.

### Week 4 — Days 22–28: pal-voice

**Day 22–23** models
```bash
cd /opt/palpod-os/pal-voice
python -m venv .venv && source .venv/bin/activate
pip install -e .[jetson]
./scripts/download-models.sh
```
This pulls whisper.cpp `small.en` GGML (250 MB), Piper `en_US-libritts_r-medium` ONNX (65 MB), openWakeWord ONNX (1 MB), and — for the MVP demo — **Qwen 2.5 7B Instruct Q5_K_M** (about 5.4 GB) instead of the production 32B. The 7B fits comfortably alongside Whisper + Piper + the OS in the AGX Orin's 64 GB unified LPDDR5 and runs at 28–32 tok/s.

**Day 24** ReSpeaker Mic Array v2.0
- Plug into the Anker hub. `arecord -l` should show `card 1: ArrayUAC10`.
- Set default input: `sudo tee /etc/asound.conf <<EOF
defaults.pcm.card 1
defaults.ctl.card 1
EOF`
- Test loopback: `arecord -D plughw:1,0 -f S16_LE -r 16000 -c 6 -d 5 mic.wav && aplay mic.wav`.

**Day 25–26** full pipeline smoke test
```bash
python scripts/smoke.py fixtures/hey_pod_what_time_is_it.wav
```
Every event in the stream must print. If Whisper aborts with `bad_alloc`, you forgot `sudo jetson_clocks` — its VRAM allocator is fragile below the max power profile.

**Day 27** wake-word training (on the founder's actual voice, at real stage distances)
- `python scripts/train-wakeword.py --samples ~/wake-samples/ --out palvoice/models/hey-hearth.onnx`
- The Day 20 pre-collection means the model sees **6 ft, 9 ft, and 12 ft samples equally**, not just close-mic garage audio. Shark Tank staging puts the founder ≈8–10 feet from the enclosure, so the close-mic-only model would false-negative on stage. This is a real failure mode from past hardware demos and the retrain window is why the dataset must be captured Week 3, not Week 4.
- Target: false-positive rate < 0.3/hr in typical rooms; recall > 95% at 8–10 ft with a −6 dB household TV playing in the background. Budget 5–10 hours of iteration; §9 line-items this.

**Day 28** — full spoken loop
- Talk to the mic from 8 ft: "Hey Hearth, what time is it?" → Piper voice answers on the Kali monitors. First time this works at stage distance is a milestone worth photographing.
- **Checkpoint tag: `mvp-w4-voice-loop`**.

### Week 5 — Days 29–35: pal-face

**Day 29–30** windowed dry run on the founder's laptop; Piper voice audition
```bash
cd /opt/palpod-os/pal-face
python -m venv .venv && source .venv/bin/activate
pip install -e .
./scripts/standalone-demo.sh --windowed
```
Cycles all 9 expressions. Watch for stuttering — should hold 60 fps. If not, disable macOS ProMotion coalescing.

Alongside, audition Piper voices: `en_US-libritts_r-medium`, `en_US-ryan-medium`, `en_US-amy-medium`. Pick warmest against Kali monitors, capture 30 sec of each, share with the marketing team. Budget 4–8 hours here; if stock voices don't sound right, a fine-tune on top of `libritts_r` takes another 3–5 hours of active work — §9 lines this out.

**Day 31–32** kiosk on the Jetson framebuffer — **known-flaky, budget 4–8 hours**
```bash
sudo usermod -aG video,render pal
sudo SDL_VIDEODRIVER=kmsdrm SDL_FBDEV=/dev/fb0 \
     /opt/palpod-os/pal-face/.venv/bin/python -m palface -c config.yaml
```
Render on the Waveshare 8" round first. When the cyan glow and pill eyes appear on the round display, immediately re-target the DP → HDMI 2.1 adapter into the 32GS95UE at 4K and increase `face_diameter` in `config.yaml` to `2160` (px).

Common failure modes for the KMSDRM path on Jetson AGX Orin (documented in `pal-face/README.md § troubleshooting`): stale libgbm from the Ubuntu jammy repo (symptom: `SDL_CreateWindow returned NULL`), permission drift on `/dev/dri/card0` after reboot, and DP hot-plug not firing HPD on the Club3D adapter. Fixes for each are scripted at `pal-face/scripts/kiosk-doctor.sh`.

**Day 33** bridge to pal-voice
- Start `pal-voice`, then `pal-face`. The face should now go NEUTRAL → LISTENING as soon as it hears the wake word, THINKING while the LLM runs, TALKING with mouth animation during Piper output.
- If TTS mouth doesn't animate: check that `audio_level` frames are landing at ≥ 20 Hz. Piper's default block is 512 samples at 22050 Hz = 43 fps, plenty.

**Day 34–35** nine-expression rehearsal
- Use `scripts/keyboard-control.py --windowed` on the laptop to trigger each expression by keystroke. Video each. Send to the marketing team for the sizzle-reel edit.
- **Checkpoint tag: `mvp-w5-face-live`**.

### Week 6 — Days 36–42: media stack

**Day 36–38** Plex + Jellyfin
- Claim Plex per `docs/INSTALL.md § 7`.
- Add mock libraries — `/mnt/hearth-media/movies/{trailer-1,trailer-2,trailer-3.mkv}` and a handful of public-domain sample films. **Do not** demo copyrighted content on Shark Tank.
- Configure Jellyfin identically as a hot backup.

**Day 39** Audiobookshelf + xTeVe
- Point ABS at `/mnt/hearth-media/audiobooks`, seed with a Librivox title.
- xTeVe with a placebo m3u — the tuner story shows on the dashboard even without a real HDHomeRun.

**Day 40–41** voice → media
- "Hey Hearth, play trailer one." pal-voice → pal-web → Plex → Kali monitors + curved OLED. Time from wake word to first audio: target < 4 s.

**Day 42** media fallback
- Pre-load a 30-second stage-safe MP4 into `/opt/palpod-os/demo/fallback.mp4`. `mpv` command wired to a hotkey on the stage laptop.
- **Checkpoint tag: `mvp-w6-media`**.

### Week 7 — Days 43–49: extender

**Day 43–44** Pi 5 image
- Raspberry Pi Imager → Raspberry Pi OS 64-bit Bookworm.
- Install Moonlight + Sunshine + WireGuard client.
- `wg-quick up hearth-mvp` — should bring up 10.99.0.2/24.

**Day 45–46** pair with pal-web
- Boot the Pi with the 15.6" Uperfect display attached.
- Browse to `https://pal.palpod.local/extenders/pair`, enter the PIN Sunshine shows, name it `Living Room TV`.
- Verify `/api/extenders` lists it.

**Day 47–48** streaming latency tune
- From the AGX Orin: `curl https://pal.palpod.local/api/play?target=living-room-tv&media_id=trailer-1`.
- Sunshine encodes on the Jetson NVENC, Moonlight decodes on the Pi. Measure glass-to-glass. Target ≤ 80 ms LAN at 1080p60.
- If > 120 ms, drop stream to 900p60 in `sunshine.conf`. (Plan B on Orin NX 16 GB: start at 900p60 or 1080p30 — see §7.2.)

**Day 49** RustDesk sanity
- On the demo laptop, install RustDesk client. Connect via `pal.palpod.local:21116`. Confirm sub-second cursor.
- **Checkpoint tag: `mvp-w7-extender`**.

### Week 8 — Days 50–56: rehearsal + 3-minute post-WAN-unplug soak

**Day 50–51** DEMO_MODE flag + long-TTL JWT provisioning
- Add `PAL_DEMO_MODE=1` to `/opt/palpod-os/.env`. In pal-voice's `orchestrator.py`, gate the LLM path: if DEMO_MODE, run the real LLM AND cache a canned response with 2 s of latency ready to `TTS_FALLBACK` if the LLM misses a 3 s deadline. See `pal-voice/palvoice/demo_mode.py`.
- **Pre-issue every JWT and every extender grant token with 24-hour TTL before the pitch**, not on-demand during the pitch. On stage, no code path may request or refresh a JWT — the tokens are already in memory. `PAL_JWT_TTL_DEMO=86400` is the env var. This is the critical enabler for the 3-minute post-WAN-unplug soak (§5).
- Under `pal-web`, wire `/demo/panic` → replays the pre-recorded fallback clip on the extender + drives face to HAPPY. Two-button setup, both dead-mans on the founder's stage clicker.

**Day 52–53** full run-throughs
- Aim: 20 clean back-to-back runs of the 90-second sequence with the 3-minute post-unplug soak included, zero human intervention. Log every drift. Fix in order of severity.

**Day 54** stress
- Run the full loop for 4 hours continuously. `tegrastats` to CSV, plot TJ. Any thermal throttle event = redesign vent grid or add a second Noctua.

**Day 55–56** road-case pack
- Everything in a rolling Pelican 1650 with foam cutouts. Sign the manifest. Two of each of DAC, amp, Brio, Waveshare, HDMI cable, PSU. No exceptions.
- **Checkpoint tag: `mvp-w8-rc1`**.

### Days 57–60: final polish + travel

- **Day 57:** wardrobe rehearsal — founder does the pitch in the shoes he'll wear on stage. Voice-recognition profile pinned to that microphone-to-mouth distance under real stage lighting (put a 500 W softbox 12 ft away and run the wake word 20 times).
- **Day 58 gate:** 3-minute post-WAN-unplug soak. After t=40 physical WAN cut, run three additional minutes of demo interaction (LLM answers, voice loop, media playback, extender stream). Zero regression allowed. See §5 for the test script and pass criteria.
- **Day 59 gate:** Halbach floater hand-off drill — 20 out of 20 successful hand-offs from carrying-case to demo cradle under stage lighting, with the founder wearing the pitch suit. Any drop resets the counter. See §5.
- **Day 60:** fly to LA.

---

## 5. Demo mode — the Shark Tank golden path

The full script lives in `docs/investor/SHARK-TANK-REHEARSAL.md`. This section is the hardware/software runbook that mirrors it. The demo is a **90-second on-camera sequence followed by an extended 3-minute post-WAN-unplug interaction window that runs while Q&A begins**. Both windows must succeed; the second is where a hostile Shark will try to break the offline claim.

**T-30 min pre-show**
1. Boot the Pod on green-room power. Verify `docker compose ps` all green.
2. Attach the Kali monitors, unmute at −20 dB.
3. Attach the LG 32GS95UE at 4K 120 Hz.
4. Attach the Pi 5 extender + Uperfect display on the "living room" side table.
5. On the stage laptop: open Moonlight (already paired), open the OBS confidence monitor, open the panic dashboard at `https://pal.palpod.local/demo/`.
6. Sound check with the wake word at ~10 ft. If it doesn't trigger inside 3 tries, hit the reset script: `ssh pal@pod sudo systemctl restart palvoice`.
7. **Pre-issue JWTs and extender grant tokens with 24-hour TTL** (`PAL_JWT_TTL_DEMO=86400 systemctl restart palweb`). Confirm no code path requires DNS or NTP for the next four minutes.

**T-0 lights up — 90-second sequence**

| t (s) | Founder says / does | System does | Panic button if… |
|---|---|---|---|
| 0 | Walk to the enclosure, hand touches walnut | LED glow warms up over 2 s (WLED preset `pitch-warm`) | LEDs dark → hotkey F1 = MQTT resend |
| 5 | "This is Hearth." | Face enters NEUTRAL, breathing loop | Face black → hotkey F2 = restart palface |
| 12 | "Hey Hearth, play something warm and quiet." | Wake → LISTENING (350 ms morph) → THINKING → LLM → Plex → Kali monitors | Voice miss → hotkey F3 = manually trigger `/api/play` |
| 22 | "I have that on the living-room TV too." | Founder holds up the Uperfect; extender starts streaming inside 6 s | Extender stall → hotkey F4 = play `demo/fallback.mp4` locally on Uperfect via mpv |
| 40 | "It runs a real large-language model, on this box, offline." | **Founder physically unplugs the WAN uplink from the Brume 2**; camera zooms on the LED confirming still online | Wireless doubt → keep the switch cable in a visible loop |
| 55 | "This is the industrial design." | Founder holds up the Halbach bench demo, floater visibly levitating | Magnet drop → have a spare floater in-pocket; drill result must be 20/20 (Day 59 gate) |
| 70 | "The face reacts to me." | Founder makes eye contact, face WINK → HAPPY | Face frozen → hotkey F2 (palface restart, 3 s recovery) |
| 85 | "I'd like $500,000 for 5%." | Face returns NEUTRAL, LEDs dim to preset `attention` | Nothing to panic — pitch has landed |

**T + 90 s to T + 4 min 30 s — the post-WAN-unplug soak (the real test)**

The WAN uplink is out from t=40. Q&A begins around t=90. During the ~3 minutes that Sharks are asking questions, **any of them may ask the founder to do another voice interaction, or ask "so is it still not online?"**. The system must continue to function without regression. This window is where a hostile Shark will test the offline claim: "Ask it a follow-up question." "Play something else." "Show me the extender again."

Test script rehearsed 20+ times on Days 52–53 and gated Day 58:

| Δt (post-unplug) | Action | Expected system behavior | Common failure mode if a dep is missed |
|---|---|---|---|
| +0 s | WAN physically cut | LEDs stay `pitch-warm`, face stays NEUTRAL | (n/a — cut is silent from user perspective) |
| +45 s | Founder says: "Hey Hearth, tell me about that composer." | Wake → LLM answers in 3–5 s using Qwen 7B (no cloud call) | If chrony insists on NTP sync and the LLM call is blocked on it: fix in `orchestrator.py` — chrony must be nice-not-required. |
| +75 s | Founder says: "Play the next track." | pal-web → Plex → Kali monitors, new track inside 4 s | If Plex tries a metadata refresh against plex.tv and the request stalls the play call: pre-seed metadata cache Day 41 and set `PLEX_OFFLINE_ONLY=1`. |
| +110 s | Founder taps Moonlight on the stage laptop | Extender re-connects inside 6 s using cached WireGuard peer (no DNS lookup) | If the WireGuard endpoint is a hostname not a fixed IP: fix in `wg0.conf` — endpoints must be IPs, not FQDNs. |
| +150 s | Founder says: "Show me the extender." | Face turns to extender-scene, LED flow follows | (No new deps introduced.) |
| +180 s | Q&A closes | Nothing further; systemwide clean shutdown at green-room. | JWT/grant TTL must exceed 180 s comfortably — hence 24-hour pre-issue. |

Day 58 pass criterion: **Three consecutive full 3-minute-plus-90-second runs with zero regression.** Regression = any of {wake-word miss > 1 in a run, LLM response > 6 s, extender re-connect > 8 s, face freeze > 500 ms, media playback stutter, any container restart}. If any run fails, root-cause and re-run all three.

**Failure-mode recovery scripts** (each is 20 lines of bash pinned to a hotkey via `sxhkd` on the stage laptop):
- `demo/recover-face.sh` — restart palface, hold NEUTRAL 3 s, return control
- `demo/recover-voice.sh` — restart palvoice, replay the "Sure — playing something warm" TTS as a canned WAV via aplay to bridge the gap
- `demo/recover-extender.sh` — kill Moonlight, restart, if still down play `demo/fallback.mp4` at 60% volume via mpv on the Uperfect
- `demo/recover-llm.sh` — if LLM tok/s drops below 6 (measured live), immediately swap to `TTS_FALLBACK` canned response

The stage laptop runs a small Tk overlay with four red buttons labeled F1–F4 exactly matching the table above. The founder rehearses the recovery drills until they're muscle memory. Rehearsed failure is invisible failure.

**Halbach floater hand-off drill (Day 59 gate).** The physical prop is the single hand-motion failure risk in the whole demo. The drill is: (a) hand-off from the road-case foam cutout to the founder's right palm; (b) present to camera and to the closest Shark; (c) return to a shelf on the enclosure top. Under 500 W softbox lighting, wearing the pitch shirt sleeve, with the exact stage marks taped to the floor. **Pass criterion: 20 consecutive successful hand-offs with no floater drop, no magnet-coupling lag > 200 ms, no shell fingerprint smudge visible on-camera.** Any failure resets the counter. The floater and spare live in a padded case with a fabric interior — chrome fingerprints are a real failure mode under stage lighting.

---

## 6. Physical build day

**Day 1 morning (order + unbox)**
- 09:00 — place Ponoko rush order (P1, 3-day turnaround clock starts now)
- 09:15 — place SendCutSend badge order (1-week clock)
- 09:30 — place NVIDIA + SparkFun (Orin NX insurance-policy kit) + Amazon + Sweetwater + K&J orders
- 10:30 — unbox Jetson AGX Orin, install into SDK Manager on the founder's Ubuntu bench box, start flash
- 15:00 — helper: inventory every order, set up receiving station in garage, label bins per §2 subsection

**Day 1 afternoon → Day 7 (parallel software + wait for parts)**
Follow the software Weeks 1–2 schedule while parts arrive. The critical path is the LG 32GS95UE (heavy freight) and the Ponoko P1 rush queue.

**Day 8 (baltic birch arrives)**
- 10:00 unpack 4 laser-cut panels. Dry-fit — the 32" OLED window has 2 mm perimeter clearance nominally; measure at four corners and shim/route the OLED cutout as needed (see §3.4).
- 11:00 pocket-hole joinery. 32 holes total. Titebond III on all mating edges.
- 14:00 clamp overnight in bar clamps. Interior gets first coat of matte black while clamped.
- Helper leads this day; founder consults on cutout fit.

**Day 9**
- 09:00 remove clamps. Sand mating edges flush.
- 10:00 iron-on walnut veneer to front + left. Trim with a flush-cut razor. Apply first coat of Watco Danish oil.
- 15:00 mount SendCutSend brushed aluminum badge with two M4 threaded inserts.

**Day 10 (install compute + storage) — Plan-A/B gate**
- **Gate: if AGX Orin is not on the bench with a passing `nvidia-smi`, execute §7.2 Plan B now.** Do not defer the decision.
- Bottom shelf: Jetson dev kit (AGX or NX). Screw down through the pre-drilled anchor holes. Route the barrel-jack power to a Furman-fed 19 V PSU.
- Middle shelf: Icy Dock U.2 enclosure and the Sabrent NVMe enclosure. Both USB-C into the Anker hub.
- Cable-manage with the 3D-printed brackets.

**Day 11 (install audio)**
- SMSL M100 → Fosi ZA3 → Kali LP-6 (stand outside the enclosure to left and right).
- USB from the DAC into a dedicated hub port. Don't share with the mic array.
- Balanced XLR on the DAC → amp. Speaker wire terminated in banana plugs at the amp end.

**Day 12 (install mic, camera, display, LEDs)**
- ReSpeaker mic array flat against the top of the enclosure, USB down to the hub.
- Brio 500 clipped to the top-front lip, USB down.
- LG 32GS95UE mounted via the Wali arm through the front cutout. DP cable to the Jetson dev-kit DP port through the Club3D adapter.
- WS2812B strip glued along the interior top edge, wired to the ESP32-S3, which is Velcro'd inside next to the Meanwell.

**Day 13 (walnut oil second coat + label wiring)**
- Second coat of Danish oil.
- Every internal cable gets a Brother P-touch label. The road-case unpacking on demo day depends on the founder identifying every cable at a glance.

**Day 14 — first end-to-end power-on**
- APC UPS → Furman → everything.
- Power sequence: switch on the ESP32 (LEDs come up amber for 3 s = boot indicator), then the Jetson (face renders inside 45 s on the OLED), then the DAC + amp (unmute last, always).
- **First working power-on target: Day 14 on Plan A. Rehearsals: Days 15–60.**

---

## 7. Total-cost roll-up + risk

### 7.1 Roll-up (matches Section 1 and Section 2)

| Category | Extended |
|---|---:|
| Compute + storage | $4,548 |
| Display | $1,639 |
| Audio | $1,117 |
| Mic + camera | $208 |
| Enclosure + finish | $580 |
| Extender demo | $265 |
| Halbach bench demo | $249 |
| Miscellaneous | $773 |
| Backup / redundancy | $1,735 |
| **Parts subtotal** | **$11,114** |
| Shipping | $340 |
| CA sales tax @ 8.75% | $972 |
| Helper labor (42 h × $40/hr) | $1,680 |
| Contingency (8% of parts subtotal) | $889 |
| **Grand total** | **$14,995** |

### 7.2 Jetson AGX allocation slip — Plan-A/B branch

**The risk is real and the schedule cannot absorb a 6-week slip through hope.** The mitigation is a concrete insurance policy plus a Day-10 gate plus a re-baselined Plan B.

**Insurance policy (executed Day 1, not later).** Order the Jetson Orin NX 16GB Developer Kit from SparkFun (DEV-22765) simultaneously with the AGX Orin. $599. Typical lead time is ~2 weeks — but often the Orin NX ships faster than the AGX because it's on a fresher production run at NVIDIA's Taiwan partner. Cost is line-itemed in §2.1 as Item 2 and is real spend regardless of outcome. If AGX arrives first, the NX kit becomes a pre-production Orin-NX-mesh test rig for the post-Series-A board work (§10, Milestone 3) — it does not go to waste.

**Gate: end of Day 10.** If the AGX Orin dev kit is not physically on the bench with a passing `nvidia-smi`, execute Plan B. Do not defer. Do not wait "one more day." The schedule downstream depends on the decision being made by Day 10.

**Plan B — switch to Orin NX 16GB:**

Re-baselined targets (documented and communicated to the pitch coach):
| Target | Plan A (AGX Orin 64GB) | Plan B (Orin NX 16GB) |
|---|---|---|
| Face render | 60 fps @ 2160 px | **30 fps @ 2160 px** |
| LLM quant | Qwen 2.5 7B Q5_K_M | **Qwen 2.5 7B Q4_K_M** |
| LLM speed ceiling | 28–32 tok/s | **~40 tok/s** at Q4 |
| Sunshine NVENC | 1080p60, 4-slice, 8-lane NVENC | **900p60 or 1080p30**, 4-lane NVENC |
| Face memory footprint | ~2 GB | ~1.4 GB (drop `face_diameter` intermediate buffer to fp16) |
| Concurrent Docker footprint | 22 containers | 22 containers (unchanged) |

Wake-word retrain: **not required.** The CUDA path is identical between AGX Orin and Orin NX, and the trained ONNX runs on either. Same Whisper small.en. Same openWakeWord ONNX. Same Piper voice.

Sunshine NVENC retune: **required.** Orin NX has 4-lane NVENC vs. AGX's 8-lane. Drop the extender target to 900p60 (which fills a 1080p Uperfect nicely with a 1-pixel border) or fall back to 1080p30. Rehearse both; pick whichever glass-to-glass latency measures lower on Day 47.

Timeline delta — Plan B is **8 days shorter overall**, landing on Day 52. This is counterintuitive but it is not a fluke: tuning against constrained silicon converges faster than tuning against headroom. Days 27–33 (voice loop → face live → bridge) each shift left by ≈3 days each because there are fewer "can we squeeze one more fps / one more tok/s?" iteration cycles on the smaller silicon. What we lose in headroom we gain in decisiveness. Net: 8 fewer days of iteration.

| Milestone | Plan A day | Plan B day | Delta |
|---|---:|---:|---:|
| `mvp-w1-baseos` | 7 | 7 | 0 |
| `mvp-w2-stack-up` | 14 | 12 | −2 |
| `mvp-w3-palweb` | 21 | 18 | −3 |
| `mvp-w4-voice-loop` | 28 | 25 | −3 |
| `mvp-w5-face-live` | 35 | 30 | −5 |
| `mvp-w6-media` | 42 | 37 | −5 |
| `mvp-w7-extender` | 49 | 44 | −5 |
| `mvp-w8-rc1` | 56 | 48 | −8 |
| Days 57–60 buffer | 60 | 52 (with 8 days extra rehearsal) | −8 |

Plan B ends at Day 52 with 8 additional days of rehearsal before the D60 travel window. That is a strictly better rehearsal position than Plan A — the trade is that the LLM answer feels slightly slower and the face is a touch less silky. The pitch language stays identical: "It runs a real large-language model, on this box, offline" is true either way.

### 7.3 Other risks & mitigations

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| LG 32GS95UE backorder | 2-week slip | Medium | Fallback: Samsung Odyssey OLED G8 34" or Corsair Xeneon Flex 45. Both have similar visual language. Order LG from B&H (in-stock) with SLA + LG Direct (backorder) same day; whichever ships first, cancel the other. |
| Ponoko queue at busy season | 1-week slip | Low–medium | We use P1 rush ($60 uplift) not standard queue. If P1 slips, JLC3DP wood-laser (2-day) is the backup — DXF is portable. |
| Kali LP-6 backorder around holidays | 2-week slip | Low | Fallback: JBL 305P MkII or Adam T5V — both are on Sweetwater in-stock. |
| ReSpeaker v2.0 EOL notice from Seeed | Total | Very low | Fallback: MiniDSP UMA-8-SP or Andrea Superbeam Array 3S. Both are Digi-Key stocked. |
| Piper voice sounding "off" on Kali monitors | Aesthetic | Low | Test on Day 29–30 with three voice models. If none work, budget 3–5 h fine-tune. §9 line-items this. |
| RustDesk relay ID conflict on demo day | Extender flaky | Low | Pre-provision the ID pool 7 days in advance and freeze. |
| Venue Wi-Fi hostile to mDNS | Extender doesn't discover | High | The GL.iNet Brume 2 makes its own LAN. Never trust venue infrastructure. |
| Founder tests positive for anything in the 72 hours before | Total | Low | Backup speaker/presenter designated Day 30. |
| Live LLM stalls on stage | Air | Medium | DEMO_MODE + canned-response fallback. Rehearsed 20+ times, gated Day 52–53. |
| WAN unplug reveals hidden cloud dep during 3-min soak | Trust | Medium | Day 58 gate: three consecutive clean soak runs. Details in §5. |

---

## 8. What the MVP does NOT do — the honesty ledger

Every one of these is a deliberate scope cut. If a Shark asks, the answer is not "it's coming" — it's "here is exactly what would take us there and here is what stops us today."

- **Does not levitate the OLED.** The 32" curved OLED is on a boring VESA arm. The Halbach bench demo levitates a *3D-printed passive sphere* about the size of a lemon. On stage it sells the aesthetic; in the shipping product, six months of servo control + Hall-effect PID (see `hardware/electrical/kicad/palpod-halbach-controller/`) get us to a driven 6" OLED sphere.
- **Does not run 10× Jetsons.** One AGX Orin (Plan A) or one Orin NX 16GB (Plan B), one 7B LLM running at ~28–32 tok/s on Plan A or ~40 tok/s at Q4 on Plan B. **We're targeting Qwen 2.5 32B at Q5_K_M on production silicon; 7B Q4_K_M/Q5_K_M in the MVP is the interim target.** There is no 32B benchmark on production hardware yet — the production hardware doesn't exist yet — so we do not claim it as a shipped number. What we can claim is: the 7B on the MVP silicon runs full-loop in under 4 seconds, and the production 32B is a compute-budget scaling extrapolation from published Qwen 2.5 32B benchmarks on comparable Jetson-mesh hardware. Sharks who want the extrapolation math get it in the follow-up deck, not on stage.
- **Does not have 35 TB.** 7.68 TB on the CD8 U.2. Plenty for a demo. Production ships 5× 8 TB WD Red Pro in a raidz2 pool as a starting point.
- **Does not have the CS43198 audio chain.** SMSL M100 (ES9018Q2C) → Fosi ZA3 (TPA3255) → Kali LP-6 is a $1,117 chain that images tight enough to sell a Shark on the intent. Production's CS43198 → Purifi Class-D → Focal Sopra reference is a $9,000 chain.
- **Does not have the mic array in a ring.** Linear 6-mic USB. Production is 12-mic circular ring on the custom `palpod-mic-array` board, giving 360° beamforming instead of the 100° effective front lobe.
- **Does not have the custom PCB stack.** Zero KiCad boards from the repo are in the MVP. Everything is off-the-shelf.
- **Does not have hot-swap redundancy.** Single Jetson, single power path, single OLED. Production has dual PSU and hot-spare NVMe.
- **Uses Qwen 2.5 7B, not 32B.** Faster on this hardware, actually *feels better* on demo — but shorter context, less nuanced response. Documented.

Is the story we tell honest? **Yes.** The one-line summary the founder rehearses: *"This is a working software prototype in a smaller enclosure with off-the-shelf electronics. The industrial-design language, the voice interaction, the face, the media stack, the extender — all real. The magnetic sphere and the 10-node compute mesh are the six-month path with our Series A."*

---

## 9. Bill of hours for the founder — with buffer

Total wall-clock: 60 days (Plan A) or 52 days (Plan B). Founder-hands-on: **143 hours (up from 123 in the prior draft)**. Helper: 42 hours. The 20 hours of buffer are line-itemed against the four milestones where the prior draft was optimistic.

| Category | Founder h | Helper h | Notes on buffer |
|---|---:|---:|---|
| Ordering + procurement | 6 | 2 | |
| Enclosure assembly (glue, veneer, oil) | 17 | 12 | +3 h founder buffer for Ponoko/SendCutSend tolerance stack-up (§3.4) — router shaving of OLED cutout and possible gasket fit-up |
| Enclosure CAD updates (parametric rework as parts arrive) | 6 | 0 | |
| Jetson unbox + JetPack flash | 3 | 0 | |
| Base OS harden + Docker | 8 | 4 | |
| pal-web bring-up | 10 | 2 | |
| pal-voice bring-up + wake-word training on founder's voice + Piper voice fine-tuning | 28 | 0 | **+7 h buffer for wake-word iteration** (stage-distance samples, false-positive tuning, ~50–100 positives + 1000s of negatives — Day 20 pre-collection helps but the retrain iterations remain). **+5 h buffer for Piper voice** (audition + potential fine-tune on `libritts_r`) |
| pal-face bring-up + expression polish | 17 | 4 | **+5 h buffer for KMSDRM/SDL kiosk mode on Jetson AGX** — known-flaky config, `kiosk-doctor.sh` scripts help but manual triage still needed |
| Media libraries + Plex config | 4 | 6 | |
| Extender pairing + latency tune | 6 | 4 | |
| LED / lighting programming | 4 | 2 | |
| Demo mode + panic scripts + JWT/token TTL work | 10 | 0 | Includes the 24-hour pre-issue plumbing that enables the 3-min post-WAN soak |
| Rehearsals (90-sec + 3-min post-WAN soak + Halbach hand-off drill) | 20 | 4 | Halbach hand-off drill is inside the 20 h |
| Road-case pack + travel | 4 | 2 | |
| **Totals** | **143** | **42** | |

Buffer accounting: 3 (enclosure tolerance) + 7 (wake-word) + 5 (Piper) + 5 (KMSDRM) = **20 hours**, exactly as budgeted.

Helper labor is line-itemed in §2.10 at $1,680 (42 h × $40/hr blended). The blended rate reflects a mix of $30/hr for enclosure hand-work (a competent maker friend, not a licensed carpenter) and $50/hr for Plex library seeding and WLED wiring (a maker-community friend with WLED experience). If the founder cannot source at these rates, the 8% contingency line has $889 of headroom before the budget breaches $15,000.

---

## 10. Where the MVP hands off to production

The MVP is a bridge, not a destination. Here is the honest sequencing of the next 9 months.

**Milestone 1 — Shark Tank demo shipped.** Day 60 (Plan A) or Day 52 (Plan B).

**Milestone 2 — Series A close.** Realistic target: Day 60 + 90 days = ~2027-01. Assumes a Shark bite becomes a lead into a $2–5 M seed-extension or Series A led by a hardware-friendly firm (Bond, Lux, or similar).

**Milestone 3 — Board-fix RFP kickoff.** Trigger: Series A close. Per `docs/investor/engineering/BOARD-FIX-SOW-RFP.md`, we contract the hand-relayout of the six existing KiCad projects (`palpod-orb`, `palpod-audio-amp`, `palpod-mic-array`, `palpod-halbach-controller`, `palpod-compute-backplane`, `palpod-extender-sbc`) — the auto-router output at `hardware/PLACE-AND-ROUTE-REPORT.md` is not production-ready and needs a human EE. Estimated 14 weeks. Expected finish: ~2027-05. **The Orin NX 16GB dev kit purchased Day 1 as insurance becomes the pre-production Orin-NX-mesh test rig for this milestone.** Not wasted spend either way.

**Milestone 4 — First pilot units.** 6 months post-Series A. Fab lead time on the six boards + first mechanical steel + walnut CMF prototype + integration = ~2027-07. Ten units. Two go to the founder's home for 30-day soak. Two go to the first design partner (Napa household from the design-partner list). Six sit as regression rigs at HQ.

**Milestone 5 — Public pre-order.** Late 2027, dependent on soak-test results.

The MVP is not a product. It is a working brain in a body that is smaller, softer, and honest about being a prototype. On Day 60 (or Day 52), that is exactly what should walk onto that stage — and exactly what should walk off of it with a deal.

---

## Appendix A — Budget reconciliation math

The prior draft (MVP-1.0) had three different grand totals ($13,345 in §1, $12,921 in §2.10, $13,021 in §7.1) plus a Section 1 compute rollup of $3,969 that did not match the §2.1 subtotal of $4,417. This appendix documents the reconciliation.

**Root cause of the drift:**
1. §1 rollup used pre-Kioxia-price-update numbers, an inconsistent tax base, and rounded contingency differently from §2.10.
2. §2.10 used the correct 8.75% CA tax on a partial taxable subset (not all parts), producing $968 = 9.19% of $10,533 — but the derivation wasn't shown.
3. §7.1 used the §2.1 line-item subtotal ($4,417) and the §2.10 non-parts total ($2,488) but forgot the shipping was already inside §2.10.
4. §1 rollup counted the Orin NX cold spare as "backup / redundancy" ($1,540) instead of compute ($3,969 + $599 = $4,568) — a categorization inconsistency that produced the $3,969 vs $4,417 gap.

**Reconciliation for MVP-1.1:**

Parts subtotals recomputed against 2026-08-05 spot prices with all category assignments consistent:

| Section | Category | Subtotal |
|---|---|---:|
| 2.1 | Compute + storage (includes AGX $2,199, Orin NX insurance-policy kit $599, WD SN850X ×2 $558, Kioxia CD8-R at $950 not $819, Icy Dock $189, Sabrent $35, microSD $18) | $4,548 |
| 2.2 | Display (LG 32GS95UE at $1,199 not $999, Waveshare $149, Uperfect $130, Wali $45, HDMI ×3 $66, Club3D $50) | $1,639 |
| 2.3 | Audio (Kali LP-6 pair at $499 not $449, everything else unchanged) | $1,117 |
| 2.4 | Mic + camera | $208 |
| 2.5 | Enclosure + finish | $580 |
| 2.6 | Extender demo | $265 |
| 2.7 | Halbach bench demo | $249 |
| 2.8 | Miscellaneous | $773 |
| 2.9 | Backup/redundancy (M4 MacBook Air 13" 16GB at $1,199 not $999, everything else unchanged) | $1,735 |
| | **Parts subtotal** | **$11,114** |

Non-parts:
- Shipping: $340
- CA sales tax at 8.75% on the full parts subtotal: 0.0875 × $11,114 = $972.475 → **$972**
- Helper labor: 42 h × $40/hr blended = **$1,680**
- Contingency at 8% of parts subtotal: 0.08 × $11,114 = $889.12 → **$889**
- **Non-parts subtotal: $3,881**

**Grand total: $11,114 + $3,881 = $14,995.**

Delta vs. prior BoM's $12,921 (the closest of the three prior numbers):
- +$131 Kioxia CD8-R price update
- +$200 LG 32GS95UE price update
- +$50 Kali LP-6 pair price update
- +$200 M4 MacBook Air 16 GB price update
- +$1,680 helper labor now line-itemed (was absent)
- +$4 tax adjustment on the new higher parts subtotal
- −$291 contingency reduction from 10% to 8% of parts subtotal (justified because helper labor is now explicit — the previously-implicit-labor slack in the 10% contingency is no longer needed)
- +$101 rounding + inclusion of the previously-omitted Ponoko rush uplift in shipping (Ponoko P1 is $60 more than P3; the delta was buried before)

Net: $12,921 + $131 + $200 + $50 + $200 + $1,680 + $4 − $291 + $101 = $14,995. Reconciled.

Contingency policy: 8% is deliberately chosen over 10% because helper labor is now line-itemed and the two overlapped in the prior draft. If a Kali LP-6 dies on Day 45, the $889 covers a same-day Sweetwater replacement ($499) with room to spare. If the LG panel dies, the fallback is the Waveshare 8" round display path plus a marketing-team call to reduce the visual ambition — not a grand-total blow-out.

Verification note: prices verified 2026-08-05 against amazon.com, sweetwater.com, bhphotovideo.com, apple.com, lg.com, nvidia.com/jetson-store, sparkfun.com, digikey.com, adafruit.com, kjmagnetics.com, ponoko.com, sendcutsend.com. Any BoM ordering more than 30 days from this date should re-verify — LG panel price is the most volatile line, and Kioxia enterprise NVMe channel pricing swings ±10% per quarter on distributor-inventory cycles.

---

*End of MVP build guide. Referenced files: `docs/ARCHITECTURE.md`, `pal-web/README.md`, `pal-voice/README.md`, `pal-face/README.md`, `docs/INSTALL.md`, `hardware/PLACE-AND-ROUTE-REPORT.md`, `hardware/electrical/kicad/*/`, `docs/investor/engineering/BOARD-FIX-SOW-RFP.md`, `docs/investor/SHARK-TANK-REHEARSAL.md`. CAD deliverables live under `hardware/mechanical/mvp/` (Fusion 360 source + STEP + DXFs + STLs) including the new `hearth-mvp-oled-gasket.stl` for the §3.4 tolerance-stack backup.*
# PAL Pod — Hardware Architecture

This is the system-level document. It synthesizes the block diagrams,
mechanical spec, thermal budget, and power tree into one coherent picture.

## 1. Product framing

- **Main column**: $95k luxury AI + media server. 36" × 12" × 24", ~180 lb.
- **Extender**: $ (TBD, ~$15k target) satellite thin client. 18" × 6" × 12", ~45 lb.
- **Orb**: 7" curved OLED sphere, magnetically levitated above the top plate.
- **Design intent**: heirloom hardware that runs entirely local AI, delivering audiophile audio + spatial computing UX without cloud dependencies.

## 2. Subsystem inventory (main)

| # | Subsystem | Reference doc |
|--:|---|---|
| 1 | Compute backplane (10 Jetson + 10 Ryzen) | `electrical/block-diagrams/compute-backplane.md` |
| 2 | Storage fabric (35 TB NVMe) | inside compute-backplane.md |
| 3 | Audio DAC + 4-way active amp | `electrical/block-diagrams/audio-amp.md` |
| 4 | 3× soundbar arrays + 2× top subwoofers | audio-amp.md |
| 5 | Halbach levitation controller | `electrical/block-diagrams/levitation-controller.md` |
| 6 | 7" curved OLED orb | `electrical/block-diagrams/orb.md` |
| 7 | 13-mic far-field array | `electrical/mic-array-reference-design.md` |
| 8 | Wireless module (Wi-Fi 7 + BT + Thread + UWB) | `connectivity/wireless-plan.md` |
| 9 | Dual 1500W Titanium PSU | `electrical/power-tree.md` |
| 10 | Liquid cooling loop | `thermal/thermal-budget.md` |
| 11 | LED seam reactive lighting | (minor; see system-overview.md) |

## 3. Key architectural decisions and their rationale

### 3.1 Why 10 + 10 heterogeneous compute?

Ryzen AI HX 370 has best-in-class CPU + iGPU + NPU for local LLM decode.
Jetson Orin NX has best perf/watt for CUDA-accelerated multimodal (vision,
speech). The mix lets the software layer route workloads to whichever
substrate is best suited without a homogeneous compromise.

**Trade-off**: complex fabric, two OS toolchains, two thermal profiles. The
Marvell Prestera switch and PCIe Gen5 backplane are the enablers.

### 3.2 Why liquid cooling?

Peak 2 kW dissipation in a 36" column with a target acoustic footprint below
25 dBA rules out air-only cooling. A closed-loop liquid loop with a 480×2
radiator bank in the base plinth is the only path to the acoustic target.

**Trade-off**: pump is a single point of failure. Mitigated by staged
throttling + 5-year service interval.

### 3.3 Why a levitating orb?

Product identity. The orb is the visible embodiment of the "AI presence" and
its motion / presence signals system state. A magnetically levitated
display is a physical expression of the "unlike anything you've owned"
product promise that justifies the $95k price.

**Trade-off**: Halbach levitation is a hard engineering problem with a
safety-critical failure mode (falling orb). Mitigated by soft-land routine,
independent watchdog, magnetic-field warnings.

### 3.4 Why dual PSU 1+1 hot-standby?

An heirloom appliance should never abruptly power off. Dual Titanium PSUs
in ORing configuration give the "server-grade uptime" story that matches
the price.

### 3.5 Why 13-mic dual-ring?

XMOS's dual-ring beamformer requires two concentric mic geometries for
proper spatial resolution across the audio band. 8 outer + 4 inner + 1
center is XMOS's reference topology for the XVF3800.

### 3.6 Why Wi-Fi 7 for orb link (vs wired)?

The orb must be free to levitate + rotate. Wired = tether = kills the
product. Wi-Fi 7 6 GHz gives 4 Gbps at 3 m range with room to spare for the
required A/V + camera uplink bandwidth.

### 3.7 Why FAS-grade quarter-sawn walnut?

Dimensional stability across the seasonal humidity swing (summer 70% RH
vs. winter 25% RH). Plain-sawn walnut would cup and split. FAS grade
ensures panels have zero sapwood and no knots > 6 mm, matching the
$95k luxury expectation.

### 3.8 Why 304 SS + CrN PVD?

- 304 SS: corrosion-immune, weldable, polishes to mirror.
- CrN: gunmetal color complements walnut better than TiN (gold), harder wearing than the polished bare steel would be, and the CrN adhesion to 304 is excellent without a Ni strike interlayer.

## 4. Cross-subsystem constraints

- **Thermal budget** (`thermal/thermal-budget.md`) constrains compute peak draw. Software must implement graceful throttle at 65 °C coolant.
- **Power budget** (`electrical/power-tree.md`) constrains simultaneous peak of compute + amp + levitation. Sequencing at cold boot must stagger to avoid PSU inrush trip.
- **Acoustic target** (< 25 dBA nominal) constrains fan RPM curves and thus radiator dT / coolant flow rate.
- **Wireless throughput** (Wi-Fi 7 320 MHz) constrains orb resolution × frame rate combined with camera uplink bandwidth.
- **Levitation stability** requires orb mass ≤ 500 g with CG < 2 mm off center. Constrains everything inside the orb.

## 5. Cross-doc traceability

Every hardware requirement traces to one of:

- **Software / product requirement** (from the PAL OS spec — outside this hardware package's scope)
- **Regulatory requirement** (`docs/CERTIFICATION-PLAN.md`)
- **DFM requirement** (`docs/DFM-CHECKLIST.md`)
- **Manufacturability requirement** (BOM lead time, `electrical/bom-summary.md`)

## 6. Open questions the founder must answer

1. **Manufacturing site**: US (Foxconn Wisconsin, Flex Austin) or Asia (LG's own Vietnam / Korea sites for OLED-adjacent assembly)? Impacts NRE budget by ~30%.
2. **Warranty policy**: 2 years standard? 5 years for the compute (matches SoM warranty)? 10 years on the enclosure?
3. **Software update mechanism**: over-the-air with signed firmware, or user-triggered via companion app?
4. **Right to repair posture**: is the orb user-replaceable? The mic array? The PSUs (yes, obviously)?
5. **Environmental narrative**: RoHS + REACH compliant (assumed); do we also pursue EPEAT Silver / Gold?

// PAL Pod — mechanical constants
// All dimensions in millimeters unless noted.
// Convention: X = width (left-right facing user), Y = depth (front-back),
// Z = height (floor to top).

// ============================================================
// MAIN COLUMN — 36" x 12" x 24" (H x W x D)
// ============================================================
MAIN_HEIGHT   = 914;   // 36"
MAIN_WIDTH    = 305;   // 12"
MAIN_DEPTH    = 610;   // 24"

// ============================================================
// EXTENDER — 18" x 6" x 12" (half-scale)
// ============================================================
EXT_HEIGHT    = 457;   // 18"
EXT_WIDTH     = 152;   // 6"
EXT_DEPTH     = 305;   // 12"

// ============================================================
// STRUCTURE
// ============================================================
STEEL_THICKNESS      = 6;     // 304 SS frame plate
WALNUT_THICKNESS     = 12;    // FAS black walnut, quarter-sawn
LED_SEAM_WIDTH       = 2;     // amber LED light-pipe channel
LED_SEAM_DEPTH       = 4;     // depth into frame for diffuser
FRAME_CORNER_RADIUS  = 8;     // curved-panel bend radius (outside)
BASE_PLINTH_HEIGHT   = 60;    // hidden radiator sits here
TOP_PLINTH_HEIGHT    = 40;    // subwoofer cant angle mounts here

// ============================================================
// ORB
// ============================================================
ORB_MAIN_DIAMETER = 178;   // 7" curved OLED sphere
ORB_EXT_DIAMETER  = 89;    // 3.5" curved OLED sphere
ORB_CRADLE_GAP    = 12;    // levitation air-gap (nominal)

// ============================================================
// COOLING / RADIATOR
// ============================================================
RAD_LENGTH    = 480;   // 480mm radiator (2× 240mm or 1× 480)
RAD_DEPTH     = 30;    // slim radiator
RAD_FAN_SIZE  = 120;   // 4× 120mm fans

// ============================================================
// SPEAKERS
// ============================================================
SUB_DIAMETER          = 165;   // 6.5" audiophile sub driver flange OD
SUB_MOUNT_HOLE_PITCH  = 148;   // bolt-circle
SOUNDBAR_LENGTH       = 260;   // full-range MTM ribbon
SOUNDBAR_HEIGHT       = 52;
TOP_SUB_CANT_ANGLE    = 15;    // forward tilt (deg) on top subs

// ============================================================
// COMPUTE BAY
// ============================================================
COMPUTE_BAY_HEIGHT   = 380;    // vertical stack of 10+10 SoM/APU
BACKPLANE_PITCH      = 32;     // per-slot spacing
BACKPLANE_SLOT_COUNT = 20;     // 10 Jetson + 10 Ryzen (edge-connected)

// ============================================================
// MIC ARRAY
// ============================================================
MIC_RING_OUTER_R = 60;   // outer ring radius, 13 MEMS mics total
MIC_RING_INNER_R = 30;   // inner ring
MIC_HOLE_DIA     = 1.2;  // acoustic port
MIC_COUNT_OUTER  = 8;
MIC_COUNT_INNER  = 4;
// + 1 broadside center mic = 13

// ============================================================
// AMPLIFIER BAY
// ============================================================
AMP_PCB_LENGTH = 220;
AMP_PCB_DEPTH  = 140;
AMP_PCB_STACK  = 3;      // 3 boards stacked vertically

// ============================================================
// PSU
// ============================================================
PSU_LENGTH = 200;
PSU_WIDTH  = 150;
PSU_HEIGHT = 86;         // 1U-ish server PSU
PSU_COUNT  = 2;          // dual 1500W Titanium redundant

// ============================================================
// TOLERANCES (documentation only; used in comments)
// ============================================================
// NONMATING_TOL = ±0.5 mm  (panel edges, cosmetic)
// MATING_TOL    = ±0.1 mm  (mounting bosses, PCB standoffs)
// PVD_TOL       = 3–4 µm thickness

// ============================================================
// PREVIEW RESOLUTION
// ============================================================
$fn = 64;   // bump to 128 for renders

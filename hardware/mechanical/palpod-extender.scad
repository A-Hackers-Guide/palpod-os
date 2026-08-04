// PAL Pod — EXTENDER enclosure (half-scale)
// Preview: F5. Render: F6.

include <constants.scad>;
use <modules.scad>;

SHOW_FRAME     = true;
SHOW_PANELS    = true;
SHOW_LED_SEAMS = true;
SHOW_INTERNALS = true;
SHOW_ORB       = true;

module palpod_extender() {
    // ---- steel frame (half-scale) ----
    if (SHOW_FRAME)
        color([0.35,0.35,0.40])
            steel_frame(EXT_WIDTH, EXT_DEPTH, EXT_HEIGHT, STEEL_THICKNESS);

    // ---- curved walnut panels ----
    if (SHOW_PANELS) {
        color([0.35, 0.22, 0.12]) {
            translate([0, -EXT_DEPTH/2 + WALNUT_THICKNESS, 0])
                walnut_panel(EXT_WIDTH-16, EXT_HEIGHT-60,
                             WALNUT_THICKNESS, 600);
            translate([0, EXT_DEPTH/2 - WALNUT_THICKNESS, 0])
                rotate([0, 0, 180])
                    walnut_panel(EXT_WIDTH-16, EXT_HEIGHT-60,
                                 WALNUT_THICKNESS, 600);
        }
    }

    // ---- LED seams ----
    if (SHOW_LED_SEAMS) {
        for (x = [-1, 1], y = [-1, 1])
            translate([x*(EXT_WIDTH/2 - LED_SEAM_WIDTH),
                       y*(EXT_DEPTH/2 - LED_SEAM_WIDTH),
                       0])
                cube([LED_SEAM_WIDTH, LED_SEAM_WIDTH, EXT_HEIGHT-50], center=true);
    }

    // ---- internals: RK3588 SBC + tiny amp + single sub + full-range ----
    if (SHOW_INTERNALS) {
        // RK3588 SBC (~100x70mm)
        translate([0, 0, -EXT_HEIGHT/4])
            color([0.1,0.4,0.1]) cube([100, 70, 2], center=true);

        // Small class-D amp (single board)
        translate([0, EXT_DEPTH/4, -EXT_HEIGHT/4 + 40])
            color("darkgreen") cube([120, 80, 2], center=true);

        // 4" full-range driver, front-facing
        translate([0, -EXT_DEPTH/2 + WALNUT_THICKNESS + 20, 0])
            color([0.1,0.1,0.1]) cylinder(h=50, d=102, center=true, $fn=48);

        // 5" downward sub in the base
        translate([0, 0, -EXT_HEIGHT/2 + 40])
            color([0.05,0.05,0.05]) cylinder(h=60, d=127, center=true, $fn=48);
    }

    // ---- 3.5" orb ----
    if (SHOW_ORB) {
        translate([0, 0, EXT_HEIGHT/2 + ORB_EXT_DIAMETER/2 + ORB_CRADLE_GAP + 12])
            color([0.9, 0.9, 0.95, 0.85])
                sphere(d=ORB_EXT_DIAMETER, $fn=48);
        translate([0, 0, EXT_HEIGHT/2 + 4])
            color([0.2,0.2,0.25])
                orb_cradle(dia=ORB_EXT_DIAMETER);
    }

    // ---- top plate with 7-hole reduced mic array ----
    difference() {
        translate([0, 0, EXT_HEIGHT/2 - 3])
            color([0.30,0.30,0.35])
                cylinder(h=6, d=90, center=true, $fn=64);
        // 6 ring mics + 1 center
        translate([0, 0, EXT_HEIGHT/2 - 3]) {
            for (i = [0:5])
                rotate([0, 0, 60*i])
                    translate([28, 0, 0])
                        cylinder(h=10, d=MIC_HOLE_DIA, center=true, $fn=16);
            cylinder(h=10, d=MIC_HOLE_DIA, center=true, $fn=16);
        }
    }
}

palpod_extender();

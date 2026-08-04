// PAL Pod — MAIN column enclosure
// Preview in OpenSCAD: F5. Render: F6. Export: File > Export > STL.
//
// This is a REFERENCE geometry. It is dimensionally accurate at the
// envelope and bay level, but is not a manufacturable model. Hand the
// exported STL to a mechanical engineer as starting geometry.

include <constants.scad>;
use <modules.scad>;

// ------------------------------------------------------------
// Toggles — comment/uncomment to inspect sub-assemblies
// ------------------------------------------------------------
SHOW_FRAME       = true;
SHOW_PANELS      = true;
SHOW_LED_SEAMS   = true;
SHOW_INTERNALS   = true;
SHOW_ORB         = true;
SHOW_RADIATOR    = true;

// ------------------------------------------------------------
// Assembly
// ------------------------------------------------------------
module palpod_main() {
    // ---- structural steel frame ----
    if (SHOW_FRAME)
        color([0.35, 0.35, 0.40])   // gunmetal PVD
            steel_frame(MAIN_WIDTH, MAIN_DEPTH, MAIN_HEIGHT);

    // ---- curved walnut panels (front + back) ----
    if (SHOW_PANELS) {
        color([0.35, 0.22, 0.12]) {  // walnut
            translate([0, -MAIN_DEPTH/2 + WALNUT_THICKNESS, 0])
                walnut_panel(MAIN_WIDTH-24, MAIN_HEIGHT-BASE_PLINTH_HEIGHT-TOP_PLINTH_HEIGHT-40,
                             WALNUT_THICKNESS, 1200);
            translate([0, MAIN_DEPTH/2 - WALNUT_THICKNESS, 0])
                rotate([0, 0, 180])
                    walnut_panel(MAIN_WIDTH-24, MAIN_HEIGHT-BASE_PLINTH_HEIGHT-TOP_PLINTH_HEIGHT-40,
                                 WALNUT_THICKNESS, 1200);
        }
    }

    // ---- amber LED seams (4 vertical edges) ----
    if (SHOW_LED_SEAMS) {
        for (x = [-1, 1], y = [-1, 1])
            translate([x*(MAIN_WIDTH/2 - LED_SEAM_WIDTH),
                       y*(MAIN_DEPTH/2 - LED_SEAM_WIDTH),
                       0])
                rotate([0, 0, 0])
                    cube([LED_SEAM_WIDTH, LED_SEAM_WIDTH,
                          MAIN_HEIGHT-BASE_PLINTH_HEIGHT-TOP_PLINTH_HEIGHT],
                         center=true);
    }

    // ---- internal bays ----
    if (SHOW_INTERNALS) {
        // Compute stack — mid column
        translate([0, 0, 0])
            compute_bay();

        // Amp bay — lower rear
        translate([0, MAIN_DEPTH/2 - AMP_PCB_DEPTH/2 - 30,
                   -MAIN_HEIGHT/2 + BASE_PLINTH_HEIGHT + 100])
            amp_bay();

        // PSU bay — lower front
        for (i = [0:PSU_COUNT-1])
            translate([0, -MAIN_DEPTH/2 + PSU_WIDTH/2 + 20,
                       -MAIN_HEIGHT/2 + BASE_PLINTH_HEIGHT + PSU_HEIGHT/2 + i*(PSU_HEIGHT+10)])
                psu_block();

        // Front-facing MTM soundbars (3 stacked)
        for (i = [0:2])
            translate([0, -MAIN_DEPTH/2 + WALNUT_THICKNESS + 20,
                       -MAIN_HEIGHT/2 + 260 + i*SOUNDBAR_HEIGHT*1.2])
                color([0.1,0.1,0.1])
                    cube([SOUNDBAR_LENGTH, 40, SOUNDBAR_HEIGHT], center=true);

        // Top canted subwoofers (2× 6.5", tilted forward)
        for (i = [-1, 1])
            translate([i*70, 0, MAIN_HEIGHT/2 - TOP_PLINTH_HEIGHT - 40])
                rotate([TOP_SUB_CANT_ANGLE, 0, 0])
                    color([0.05,0.05,0.05])
                        cylinder(h=90, d=SUB_DIAMETER, center=true, $fn=64);
    }

    // ---- 7" curved OLED orb, hovering above top plinth ----
    if (SHOW_ORB) {
        translate([0, 0, MAIN_HEIGHT/2 + ORB_MAIN_DIAMETER/2 + ORB_CRADLE_GAP + 20])
            color([0.9, 0.9, 0.95, 0.85])
                sphere(d=ORB_MAIN_DIAMETER, $fn=64);
        // Halbach cradle beneath
        translate([0, 0, MAIN_HEIGHT/2 + 8])
            color([0.2,0.2,0.25])
                orb_cradle();
    }

    // ---- radiator hidden in base plinth ----
    if (SHOW_RADIATOR) {
        translate([0, 0, -MAIN_HEIGHT/2 + BASE_PLINTH_HEIGHT/2])
            radiator_block();
    }

    // ---- top-plate mic ring ----
    // Represented as a shallow disc with 13 holes cut into it.
    difference() {
        translate([0, 0, MAIN_HEIGHT/2 - 3])
            color([0.30,0.30,0.35])
                cylinder(h=6, d=MIC_RING_OUTER_R*2 + 30, center=true, $fn=96);
        translate([0, 0, MAIN_HEIGHT/2 - 3]) mic_ring();
    }
}

palpod_main();

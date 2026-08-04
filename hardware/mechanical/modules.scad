// PAL Pod — shared OpenSCAD modules
// All modules parametric. Default arguments match the MAIN column;
// pass explicit args for the extender.

include <constants.scad>;

// ------------------------------------------------------------
// steel_frame(w, d, h, t)
// A closed rectangular tube frame with rounded corners and
// cutouts for panels. Cosmetic 6mm plate steel.
// ------------------------------------------------------------
module steel_frame(w=MAIN_WIDTH, d=MAIN_DEPTH, h=MAIN_HEIGHT, t=STEEL_THICKNESS) {
    difference() {
        // outer shell
        minkowski() {
            cube([w - 2*FRAME_CORNER_RADIUS,
                  d - 2*FRAME_CORNER_RADIUS,
                  h - 2*FRAME_CORNER_RADIUS], center=true);
            sphere(r=FRAME_CORNER_RADIUS, $fn=32);
        }
        // hollow interior
        translate([0, 0, 0])
            cube([w - 2*t, d - 2*t, h - 2*t], center=true);
        // large front/back cutouts for walnut panels
        translate([0, d/2 - t/2, 0])
            cube([w - 4*t, t*2, h - 4*t - BASE_PLINTH_HEIGHT], center=true);
        translate([0, -(d/2 - t/2), 0])
            cube([w - 4*t, t*2, h - 4*t - BASE_PLINTH_HEIGHT], center=true);
    }
}

// ------------------------------------------------------------
// walnut_panel(w, h, thickness, curve_r)
// Curved walnut panel. Uses rotate_extrude for a section of a
// cylinder, then trimmed by a rectangular bounding box.
// ------------------------------------------------------------
module walnut_panel(w=MAIN_WIDTH-24, h=MAIN_HEIGHT-120,
                    thickness=WALNUT_THICKNESS, curve_r=1200) {
    // Curve radius 1200mm gives a very gentle convex bow
    // over a 280mm-wide panel (~8mm crown).
    intersection() {
        translate([0, -curve_r, 0])
            rotate_extrude(angle=180, convexity=4, $fn=128)
                translate([curve_r, 0])
                    square([thickness, h], center=false);
        translate([-w/2, -thickness*2, 0])
            cube([w, thickness*3, h]);
    }
}

// ------------------------------------------------------------
// led_seam(length, w, d)
// Reactive amber LED seam — a slim channel machined into the
// steel frame edge, filled with a frosted acrylic diffuser.
// Represented here as a thin bar.
// ------------------------------------------------------------
module led_seam(length=100, w=LED_SEAM_WIDTH, d=LED_SEAM_DEPTH) {
    color([1.0, 0.6, 0.15, 0.85])
        cube([length, w, d], center=true);
}

// ------------------------------------------------------------
// mount_bracket(w, d, hole_pitch, hole_dia)
// L-bracket with two through-holes for M4 machine screws.
// ------------------------------------------------------------
module mount_bracket(w=40, d=25, t=3, hole_pitch=20, hole_dia=4.2) {
    difference() {
        union() {
            cube([w, d, t]);
            cube([w, t, d]);
        }
        for (x = [w/2 - hole_pitch/2, w/2 + hole_pitch/2]) {
            translate([x, d/2, -0.1]) cylinder(h=t+0.2, d=hole_dia, $fn=24);
            translate([x, -0.1, d/2]) rotate([-90,0,0])
                cylinder(h=t+0.2, d=hole_dia, $fn=24);
        }
    }
}

// ------------------------------------------------------------
// panel_curve(radius, arc_deg, height, thickness)
// Generic curved panel primitive used by walnut_panel and by
// the orb cradle.
// ------------------------------------------------------------
module panel_curve(radius=600, arc_deg=30, height=200, thickness=6) {
    rotate_extrude(angle=arc_deg, convexity=4, $fn=128)
        translate([radius, 0])
            square([thickness, height]);
}

// ------------------------------------------------------------
// subwoofer_cutout(dia, bolt_circle, bolt_dia)
// Through-cut for a driver + 4 or 6 mounting holes.
// ------------------------------------------------------------
module subwoofer_cutout(dia=SUB_DIAMETER, bolt_circle=SUB_MOUNT_HOLE_PITCH,
                        bolt_dia=5, bolts=6) {
    cylinder(h=100, d=dia, center=true, $fn=96);
    for (i = [0:bolts-1])
        rotate([0, 0, 360/bolts * i])
            translate([bolt_circle/2, 0, 0])
                cylinder(h=100, d=bolt_dia, center=true, $fn=24);
}

// ------------------------------------------------------------
// amp_bay(pcb_l, pcb_d, stack, pitch)
// A rectangular volume representing the 3-board Purifi amp
// stack with airflow gaps.
// ------------------------------------------------------------
module amp_bay(pcb_l=AMP_PCB_LENGTH, pcb_d=AMP_PCB_DEPTH,
               stack=AMP_PCB_STACK, pitch=35) {
    for (i = [0:stack-1])
        translate([0, 0, i*pitch])
            color("darkgreen") cube([pcb_l, pcb_d, 2], center=true);
    // stack bounding volume
    %cube([pcb_l+10, pcb_d+10, stack*pitch+10], center=true);
}

// ------------------------------------------------------------
// compute_bay(slots, pitch, slot_l, slot_d)
// Vertical backplane with 20 edge-connected SoM/APU cards.
// ------------------------------------------------------------
module compute_bay(slots=BACKPLANE_SLOT_COUNT, pitch=BACKPLANE_PITCH,
                   slot_l=140, slot_d=95) {
    for (i = [0:slots-1])
        translate([0, 0, i*pitch])
            color([0.1,0.4,0.1]) cube([slot_l, slot_d, 1.6], center=true);
    // backplane
    color([0.05,0.2,0.05])
        translate([-slot_l/2, 0, slots*pitch/2 - pitch/2])
            cube([2, slot_d, slots*pitch], center=true);
}

// ------------------------------------------------------------
// orb_cradle(dia, gap)
// A hemispherical recess with clearance for the levitating orb.
// ------------------------------------------------------------
module orb_cradle(dia=ORB_MAIN_DIAMETER, gap=ORB_CRADLE_GAP) {
    difference() {
        // outer support shell
        sphere(d = dia + gap*2 + 20, $fn=96);
        // inner air-gap for orb
        sphere(d = dia + gap*2, $fn=96);
        // top opening for the orb itself
        translate([0, 0, dia])
            cube([dia*2, dia*2, dia*2], center=true);
    }
}

// ------------------------------------------------------------
// radiator_block(l, d, h)
// Represents a slim 480mm liquid-cooling radiator + fan bank.
// ------------------------------------------------------------
module radiator_block(l=RAD_LENGTH, d=RAD_DEPTH, h=120) {
    color([0.6,0.6,0.65]) cube([l, d, h], center=true);
}

// ------------------------------------------------------------
// psu_block(l, w, h)
// Server-style PSU (1500W Titanium).
// ------------------------------------------------------------
module psu_block(l=PSU_LENGTH, w=PSU_WIDTH, h=PSU_HEIGHT) {
    color([0.2,0.2,0.2]) cube([l, w, h], center=true);
}

// ------------------------------------------------------------
// mic_ring(outer_r, inner_r, hole_dia)
// 13-hole MEMS mic port pattern (8 outer + 4 inner + 1 center).
// Cut through the top plate.
// ------------------------------------------------------------
module mic_ring(outer_r=MIC_RING_OUTER_R, inner_r=MIC_RING_INNER_R,
                hole_dia=MIC_HOLE_DIA, depth=6) {
    // 8 outer
    for (i = [0:MIC_COUNT_OUTER-1])
        rotate([0, 0, 360/MIC_COUNT_OUTER * i])
            translate([outer_r, 0, 0])
                cylinder(h=depth, d=hole_dia, center=true, $fn=24);
    // 4 inner
    for (i = [0:MIC_COUNT_INNER-1])
        rotate([0, 0, 360/MIC_COUNT_INNER * i + 45])
            translate([inner_r, 0, 0])
                cylinder(h=depth, d=hole_dia, center=true, $fn=24);
    // 1 center
    cylinder(h=depth, d=hole_dia, center=true, $fn=24);
}

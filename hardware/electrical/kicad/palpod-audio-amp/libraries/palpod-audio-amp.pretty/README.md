# palpod-audio-amp.pretty - PLACEHOLDER footprints

These `.kicad_mod` files are **starter outlines only**. They compile in KiCad 8+
and give the schematic a valid footprint reference so the project opens
end-to-end, but the pad positions, sizes, and pin numbering are best-effort
approximations, not fabrication-ready.

**Before releasing to fab, the EE must verify every pad against the datasheet
of the actual package.**

## Files

- `CS43198_TQFN32.kicad_mod` - Cirrus CS43198-CWZR 32-pin TQFN 5x5mm 0.5mm pitch, central 3.1x3.1mm thermal pad (pin 33). Verify against Cirrus DS977F5.
- `CS2100_MSOP10.kicad_mod` - CS2100-CP MSOP-10.
- `THAT1512_SOIC8.kicad_mod` - THAT1512 SOIC-8.
- `Purifi_1ET7040SA_Module.kicad_mod` - **Large 155x45mm carrier footprint** for the Purifi 1ET7040SA drop-in Class-D amp module. Represents the module's mount pattern (4x M3 corner holes) and 12-pin through-hole interface header. Real module has 2 rows of high-current speaker+power terminals on the sides; this placeholder collapses them into a single-row header. **VERIFY module dimensions and pin locations against the Purifi 1ET7040SA reference/datasheet before layout.**
- `LM5116_HTSSOP24.kicad_mod` - TI LM5116 HTSSOP-24 with 3.4x5.0mm exposed pad (pin 25).
- `TPS3808_SOT23-5.kicad_mod` - TI TPS3808 supervisor SOT-23-5.
- `ADT7420_MSOP8.kicad_mod` - Analog Devices ADT7420 temperature sensor MSOP-8. Note: real ADT7420 is LFCSP-8; MSOP variant is shown here as a lower-risk placeholder.
- `WBT-0705_Terminal.kicad_mod` - WBT-0705Cu speaker binding-post terminal, 2-pin, 19.05mm pitch, 5.5mm drills. Panel-mount hardware.
- `Si8660_SOIC16.kicad_mod` - SiLabs Si8660BB 6-ch digital isolator SOIC-16 WB.

## Verification checklist (per footprint)

1. Cross-check package dimensions against the datasheet mechanical drawing.
2. Cross-check pad size and pitch against the recommended land pattern.
3. Cross-check pin-1 marker position against the datasheet ball/pad map.
4. Cross-check the courtyard against IPC-7351 (level B nominal for signal parts,
   level A dense for high-density QFNs, level C wide for high-voltage parts).
5. For the Purifi module: reconcile the placeholder single-row header against the
   actual module's dual-row terminal layout. Enlarge power terminals to 6-7mm
   drill for 6-8AWG rail wires.
6. For WBT terminals: confirm the panel cutout matches the mechanical enclosure.

# assets/

No image or font assets ship with the PAL Face Renderer.

Every pixel drawn on the round OLED is procedural:

- Background: radial gradient (`palface.shapes.radial_gradient`)
- Eyes: rounded-rect "pills" via `pygame.draw.rect(border_radius=...)`
- Mouth: cup-scoop polygon from the spec-sheet SVG path
  `M 30 60 L 70 60 C 78 82, 22 82, 30 60 Z`,
  flattened to a polyline and filled with `pygame.draw.polygon`
- Glow: soft alpha-blended pill/oval rendered underneath each feature
- Sphere mask: a full-screen scratch surface with a transparent circle punched
  out, blit on top to blacken pixels outside the round display

This keeps the wheel/tarball tiny, scales perfectly to any resolution
(1080×1080, 1440p, arbitrary round panels), and means no font/asset licensing
questions.

If you ever add fonts (e.g. for a startup splash), drop `.ttf` files here and
load them via `pygame.font.Font("assets/whatever.ttf", size)`. Keep it
lightweight — this is a face renderer, not a UI kit.

# PowerPoint edition — how it is built

1. `PASS=spec node build2.js x.pptx` records every glass panel into `spec.json`.
2. `python glass.py spec.json img` bakes one background per slide: a blurred 3D stadium render with frosted glass panels.
3. `node build2.js ../King_Salman_Stadium_Group8.pptx` builds the deck on those backgrounds; all text, numbers and bars stay editable.

Fonts: Segoe UI, Segoe UI Semibold, Segoe UI Black and Segoe UI Light (standard on Windows).

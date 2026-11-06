# PowerPoint edition — how it is built

1. `PASS=spec node build2.js x.pptx` records every glass panel into `spec.json`.
2. `python glass.py spec.json img` bakes one background per slide: a blurred 3D stadium render with frosted glass panels.
3. `node build2.js ../King_Salman_Stadium_Group8.pptx` builds the deck on those backgrounds; all text, numbers and bars stay editable.

Font: Arial throughout (identical on Mac and Windows, so text fits the same everywhere). Proofing is turned off on all text.

**Final version (Nov 2026):** the team edited the deck by hand in PowerPoint (`King_Salman_Stadium_Group8_Final_v2`):
- the part dividers are gone;
- "Our case" and "Who buys, who supplies" are merged into one slide;
- the scenario and materials slides are merged into one;
- the risks and controls slide moved to the end, after the sources.

The two review notes were then applied to that file directly, and the PDF was exported from it. `build2.js` produces the earlier 24-slide layout, so don't rebuild the final deck with it.

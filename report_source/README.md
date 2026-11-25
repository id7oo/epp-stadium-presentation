# Report edition (A4 PDF) — how it is built

`../Group8_Stadium_EPP_Report.pdf` is the designed A4 version of the group report
(`Group8_Stadium_EPP_Report_highlighted.docx`, 15 November 2026), in the same Night Glass look as the deck:
dark night-green pages, frosted glass panels, gold labels, green for Saudi supply, orange for imports.

1. `npm install` — fetches the Plus Jakarta Sans font used by the web deck.
2. `python3 bake.py` — bakes the blurred page backgrounds, section banners and cover crops into `img/` from `../pptx_source/img/`.
3. `python3 build.py` — writes `report.html` (all text, charts as inline SVG).
4. `node render.js report.pdf --png png` — prints the A4 PDF with Chromium, reports any page whose content overflows, and writes PNG previews.

Every sentence of the Word report is in the PDF. Tables became visuals (procurement situations as cards, the draft import bands
as a tier chart, the EP categories as a factor-range chart, the funding table as an activity-versus-credit chart). The imports
breakdown by product group uses the same group calculation as slide 6 of the deck [1, 2].

**Student numbers** are read from `team_ids.json` (git-ignored, because this repository is public). Without that file, or with
`NO_IDS=1`, the last page lists the names only. The PDF committed here is built without student numbers.

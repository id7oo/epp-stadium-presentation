"""SVG charts for the A4 report. All geometry in millimetres (viewBox units = mm)."""
FG, FG2, FG3, FG4 = '#F2F7F6', '#B4C5C2', '#7F928F', '#56696A'
GREEN, GOLD, IMP, BLUE, OTHER, CREDIT = '#22D38B', '#E2B357', '#EE6A33', '#4A95F0', '#7C918C', '#D79A1E'
TRACK = 'rgba(255,255,255,.07)'
GRID = 'rgba(255,255,255,.09)'


def pt(x): return x * 0.3528


def T(x, y, s, size=7, w=500, fill=FG2, anchor='start', extra=''):
    size = max(size, 6.1)
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-size="{pt(size):.3f}" font-weight="{w}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{s}</text>')


def R(x, y, w, h, fill, r=None, extra=''):
    r = h / 2 if r is None else r
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{max(w, 0):.2f}" height="{h:.2f}" rx="{min(r, w / 2):.2f}" fill="{fill}" {extra}/>'


def L(x1, y1, x2, y2, stroke=GRID, w=.25, extra=''):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{stroke}" stroke-width="{w}" {extra}/>'


def svg(w, h, body, defs=''):
    return (f'<svg width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'<defs>{GLOW}{HATCH}{defs}</defs>{body}</svg>')


GLOW = ('<filter id="glow" x="-20%" y="-80%" width="140%" height="260%"><feGaussianBlur stdDeviation="1.1" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
HATCH = ('<pattern id="hatch" width="1.6" height="1.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<rect width="1.6" height="1.6" fill="rgba(226,179,87,.16)"/><line x1="0" y1="0" x2="0" y2="1.6" stroke="rgba(226,179,87,.75)" stroke-width=".55"/></pattern>'
         '<pattern id="hatchg" width="1.6" height="1.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<rect width="1.6" height="1.6" fill="rgba(255,255,255,.03)"/><line x1="0" y1="0" x2="0" y2="1.6" stroke="rgba(255,255,255,.22)" stroke-width=".45"/></pattern>')


# ── 1. GASTAT ratios: national construction vs the SAR 4.5bn scenario ──────────
def gastat(W=168):
    x0, bw = 40, 74           # bar area
    cA, cB = W - 30, W        # right edges of the two value columns
    out = []
    out.append(T(0, 3, 'SAME RATIOS, TWO SCALES', 5.8, 700, GOLD, extra='letter-spacing=".5"'))
    out.append(T(cA, 3, 'SAUDI 2023', 5.6, 700, FG3, 'end', extra='letter-spacing=".35"'))
    out.append(T(cB, 3, 'OUR SCENARIO', 5.6, 700, FG3, 'end', extra='letter-spacing=".35"'))
    out.append(L(cA - 27.5, 0, cA - 27.5, 47, GRID))
    f = 307.541 / 645.816; imp = 60.507 / 307.541; pw = bw * f
    rows = [('Output', 'value of construction work', 'SAR 645.8bn', 'SAR 4,500m', 9),
            ('Intermediate purchases', 'materials and services bought in', 'SAR 307.5bn', 'SAR 2,142.9m', 23),
            ('of which imported', '19.67% of purchases', 'SAR 60.5bn', 'SAR 421.6m', 37)]
    for i, (a, b, v1, v2, y) in enumerate(rows):
        col = '#FF9B6E' if i == 2 else FG
        out.append(T(0, y + 3.3, a, 8.2, 700, col))
        out.append(T(0, y + 7.0, b, 6.2, 500, FG3))
        out.append(T(cA, y + 4.4, v1, 9.2, 800, col, 'end'))
        out.append(T(cB, y + 4.4, v2, 9.2, 800, col, 'end'))
    y1, y2, y3 = 9, 23, 37
    out.append(R(x0, y1, bw, 6, 'rgba(180,197,194,.28)', 1.6))
    out.append(f'<path d="M{x0},{y1 + 6} L{x0},{y2} M{x0 + pw:.2f},{y1 + 6} L{x0 + pw:.2f},{y2}" stroke="rgba(255,255,255,.2)" stroke-width=".3" stroke-dasharray="0.8 0.8"/>')
    out.append(T(x0 + pw + 2.5, y2 + 4.3, '47.6% of output', 6.6, 700, FG2))
    out.append(R(x0, y2, pw * (1 - imp) - .5, 6, GREEN, 1.6, 'filter="url(#glow)"'))
    out.append(R(x0 + pw * (1 - imp) + .5, y2, pw * imp - .5, 6, IMP, 1.6, 'filter="url(#glow)"'))
    out.append(T(x0 + pw * (1 - imp) / 2, y2 + 4.1, 'Saudi-made 80.3%', 6.2, 800, '#062014', 'middle'))
    xi = x0 + pw * (1 - imp) + .5
    out.append(f'<path d="M{xi:.2f},{y2 + 6} L{x0},{y3} M{x0 + pw:.2f},{y2 + 6} L{x0 + pw * imp:.2f},{y3}" stroke="rgba(238,106,51,.45)" stroke-width=".3" stroke-dasharray="0.8 0.8"/>')
    out.append(R(x0, y3, pw * imp, 6, IMP, 1.6, 'filter="url(#glow)"'))
    out.append(T(x0 + pw * imp + 2.5, y3 + 4.3, '19.67% of purchases · about one riyal in five', 6.6, 700, '#FF9B6E'))
    return svg(W, 46, ''.join(out))


# ── 2. Modelled stadium imports by product group ───────────────────────────────
IMPORTS = [('Other chemical products', 'paints, coatings, sealants, adhesives', 94, True),
           ('Basic metals', 'steel, aluminium, copper', 83, True),
           ('Wood products', 'timber, plywood, wooden doors', 39, False),
           ('Glass and non-metallic', 'cement, glass, ceramic tiles', 34, False),
           ('Basic chemicals', 'industrial gases, resins, solvents', 30, False),
           ('Refined petroleum', 'diesel, asphalt, lubricants', 29, False),
           ('Rubber and plastics', 'PVC pipes, insulation, seals', 15, False),
           ('Electrical machinery', 'cables, switchgear, transformers', 14, False),
           ('All other inputs', '', 83, False)]


def imports_chart(W=106):
    lab = 44; bx = lab + 2; bw = W - bx - 22; rh = 7.2; top = 2
    out = []
    for i, (n, ex, v, hl) in enumerate(IMPORTS):
        y = top + i * rh
        if i == 8:
            out.append(L(0, y - .9, W, y - .9, GRID))
        out.append(T(lab, y + 2.5, n, 7, 700 if hl else 600, FG if hl else FG2, 'end'))
        if ex:
            out.append(T(lab, y + 5.0, ex, 5.4, 500, FG3, 'end'))
        out.append(R(bx, y + .9, bw, 2.8, TRACK))
        col = IMP if hl else 'rgba(150,172,167,.55)'
        out.append(R(bx, y + .9, bw * v / 94, 2.8, col, None, 'filter="url(#glow)"' if hl else ''))
        out.append(T(bx + bw * v / 94 + 1.6, y + 3.35, str(v), 7, 800 if hl else 700, FG if hl else FG2))
    # bracket for the top two
    bxr = W - 8.5
    out.append(f'<path d="M{bxr - 2},{top + .9} h2 v{rh * 2 - 1.4} h-2" fill="none" stroke="{IMP}" stroke-width=".35"/>')
    out.append(T(bxr + 1.4, top + 5.0, '42%', 8, 800, '#FF9B6E'))
    out.append(T(bxr + 1.4, top + 8.2, 'of imports', 5, 600, FG3))
    h = top + 9 * rh + 1
    return svg(W, h, ''.join(out))


# ── 3. Draft obligation tiers with the scenario marker ─────────────────────────
def tiers(W=106):
    H = 58; x0, x1 = 6, W - 2; vmax = 650
    X = lambda v: x0 + (x1 - x0) * v / vmax
    base = 46; hpp = 1.35  # mm per percentage point
    out = []
    out.append(L(x0, base, x1, base, 'rgba(255,255,255,.25)', .3))
    # below threshold
    out.append(R(X(0), base - 3, X(75) - X(0) - .4, 3, 'url(#hatchg)', .6))
    out.append(T(X(37.5), base - 7.6, 'below the', 5.2, 600, FG3, 'middle'))
    out.append(T(X(37.5), base - 5.0, 'threshold', 5.2, 600, FG3, 'middle'))
    bands = [(75, 300, 25, False), (300, 500, 20, True), (500, 650, 15, False)]
    for a, b, r, on in bands:
        h = r * hpp
        fill = 'rgba(226,179,87,.85)' if on else 'rgba(150,172,167,.35)'
        out.append(R(X(a) + .4, base - h, X(b) - X(a) - .8, h, fill, .9, 'filter="url(#glow)"' if on else ''))
        out.append(T((X(a) + X(b)) / 2, base - h + 5.2, f'{r}%', 10 if on else 9, 800, '#1A1304' if on else FG, 'middle'))
    # scenario marker
    xm = X(421.61)
    out.append(L(xm, 4.5, xm, base + .2, FG, .35, 'stroke-dasharray="1 .8"'))
    out.append(f'<circle cx="{xm:.2f}" cy="{base:.2f}" r="1.2" fill="{IMP}" stroke="#0b1513" stroke-width=".5"/>')
    out.append(T(xm, 2.6, 'Our scenario · SAR 421.6m', 6.4, 700, FG, 'middle'))
    # axis
    for v in (0, 75, 300, 500, 650):
        out.append(L(X(v), base, X(v), base + 1.2, 'rgba(255,255,255,.3)', .3))
        lab = f'{v}' if v < 650 else '650+'
        out.append(T(X(v), base + 4.2, lab, 6, 600, FG3, 'middle'))
    out.append(T(x1, base + 8.6, 'imports from one foreign company, SAR m (excl. VAT)', 5.6, 500, FG3, 'end'))
    return svg(W, H, ''.join(out))


# ── 4. Obligation under the draft vs the preceding framework ───────────────────
def obligation_compare(W=62):
    out = []; bw = W - 2; vmax = 147.56
    rows = [('April 2026 draft · 20%', 84.32, GOLD, True), ('Preceding policy · 35%', 147.56, 'rgba(150,172,167,.55)', False)]
    for i, (n, v, c, on) in enumerate(rows):
        y = i * 12
        out.append(T(0, y + 3, n, 6.3, 700, FG if on else FG2))
        out.append(R(0, y + 4.6, bw * v / vmax, 3.2, c, None, 'filter="url(#glow)"' if on else ''))
        out.append(T(bw * v / vmax - 1, y + 10.9, f'SAR {v:.2f}m', 7.4, 800, FG if on else FG2, 'end'))
    return svg(W, 24, ''.join(out))


# ── 5. EP category factor ranges with our proposed factors ─────────────────────
FACTORS = [('Knowledge transfer', 1, 3, 2, 'New assessed skills and Saudi trainers'),
           ('Technology transfer', 2, 4, 3, 'Usable diagnostic tools and technical rights'),
           ('Localisation', 1, 3, 2, 'New qualified Saudi materials or services'),
           ('Subcontracting', 1, 2, None, 'Approved additional purchases from local firms'),
           ('Research and development', 2, 4, None, 'Local research into material performance'),
           ('Export development', 2, 4, 'later', 'Durable export channels for Saudi output'),
           ('Investment', 1, 3, None, 'Viable expansion of a local facility')]


def factor_chart(W=178):
    lab = 37; sx0 = lab + 6; sx1 = sx0 + 56; act = sx1 + 8
    X = lambda v: sx0 + (sx1 - sx0) * (v - .5) / 4
    rh = 8.0; top = 8
    out = []
    out.append(T(0, 3.6, 'EP CATEGORY', 5.6, 700, GOLD, extra='letter-spacing=".4"'))
    out.append(T(X(.5), 3.6, 'DRAFT FACTOR (MULTIPLIER)', 5.6, 700, GOLD, extra='letter-spacing=".4"'))
    out.append(T(act, 3.6, 'POTENTIAL STADIUM ACTIVITY', 5.6, 700, GOLD, extra='letter-spacing=".4"'))
    n = len(FACTORS)
    for v in (1, 2, 3, 4):
        out.append(L(X(v), top - 1, X(v), top + n * rh - 1, GRID))
    for i, (name, a, b, ours, actv) in enumerate(FACTORS):
        y = top + i * rh; cy = y + 2.6
        if i % 2 == 0:
            out.append(R(-2, y - 1.2, W + 4, rh, 'rgba(255,255,255,.025)', 1.2))
        out.append(T(0, cy + 1.1, name, 7.2, 700 if ours else 600, FG if ours else FG2))
        out.append(R(X(a) - 1.4, cy - 1.4, X(b) - X(a) + 2.8, 2.8, 'rgba(34,211,139,.22)', None, 'stroke="rgba(34,211,139,.6)" stroke-width=".25"'))
        out.append(T(X(a) - 2.6, cy + 1.05, str(a), 6.2, 700, FG3, 'end'))
        out.append(T(X(b) + 2.6, cy + 1.05, str(b), 6.2, 700, FG3))
        if isinstance(ours, int):
            out.append(f'<circle cx="{X(ours):.2f}" cy="{cy:.2f}" r="1.9" fill="{GOLD}" stroke="#0b1513" stroke-width=".5" filter="url(#glow)"/>')
            out.append(T(X(ours), cy + .95, str(ours), 5.4, 800, '#1A1304', 'middle'))
        elif ours == 'later':
            out.append(f'<circle cx="{X(3):.2f}" cy="{cy:.2f}" r="1.7" fill="none" stroke="{GOLD}" stroke-width=".35" stroke-dasharray=".7 .5"/>')
        out.append(T(act, cy + 1.1, actv, 7, 500, FG2))
    yb = top + n * rh + 1.5
    for v in (1, 2, 3, 4):
        out.append(T(X(v), yb + 1.5, f'×{v}', 6, 700, FG3, 'middle'))
    # legend
    ly = yb + 6.4
    out.append(R(0, ly - 2.2, 7, 2.8, 'rgba(34,211,139,.22)', None, 'stroke="rgba(34,211,139,.6)" stroke-width=".25"'))
    out.append(T(9, ly, 'Draft range (Article 9)', 6.2, 600, FG2))
    out.append(f'<circle cx="{46:.2f}" cy="{ly - .8:.2f}" r="1.6" fill="{GOLD}"/>')
    out.append(T(49, ly, 'Factor we propose (Section 5)', 6.2, 600, FG2))
    out.append(f'<circle cx="{93:.2f}" cy="{ly - .8:.2f}" r="1.5" fill="none" stroke="{GOLD}" stroke-width=".35" stroke-dasharray=".7 .5"/>')
    out.append(T(96, ly, 'Later phase, outside the initial funding', 6.2, 600, FG2))
    return svg(W, ly + 1.5, ''.join(out))


# ── 6. Stadium contract benchmarks ─────────────────────────────────────────────
def stadiums(W=168):
    lab = 48; x0 = lab + 4; x1 = W - 44; vmax = 5.0
    X = lambda v: x0 + (x1 - x0) * v / vmax
    out = []
    out.append(T(0, 3, 'STADIUM', 5.6, 700, GOLD, extra='letter-spacing=".4"'))
    out.append(T(x0, 3, 'MAIN WORKS VALUE, SAR BILLION', 5.6, 700, GOLD, extra='letter-spacing=".4"'))
    out.append(T(W, 3, 'SEATS', 5.6, 700, GOLD, 'end', extra='letter-spacing=".4"'))
    top = 7
    for v in range(0, 6):
        out.append(L(X(v), top, X(v), top + 41, GRID))
        out.append(T(X(v), top + 44.5, str(v), 6, 600, FG3, 'middle'))
    rows = [
        ('King Salman Stadium, Riyadh', 'Ministry of Sport · budget unpublished', 4.5, 'scen', '92,760', 'SAR 4.5bn group scenario'),
        ('Qiddiya stadium', 'FCC–Nesma joint venture', 4.0, 'aw', '45,000', 'about SAR 4.0bn'),
        ('', 'mechanical package, awarded separately', 0.829, 'pk', '', 'SAR 829m'),
        ('', 'façade package, awarded separately', 0.997, 'pk', '', 'SAR 997m excl. VAT'),
        ('Aramco stadium, Al Khobar', 'BESIX–Albawani', 3.7, 'aw', '46,096', 'about SAR 3.7bn'),
    ]
    y = top + 1.5
    for n, sub, v, kind, seats, vl in rows:
        if kind == 'pk':
            out.append(T(lab, y + 2.4, sub, 5.9, 500, FG3, 'end'))
            out.append(R(x0, y + .6, X(v) - x0, 2.2, 'rgba(74,149,240,.55)', 1.1))
            out.append(T(X(v) + 1.6, y + 2.5, vl, 6.2, 700, FG2))
            y += 5
            continue
        if n.startswith('Aramco'): y += 1.5
        out.append(T(lab, y + 2.9, n, 7.3, 700, FG, 'end'))
        out.append(T(lab, y + 5.9, sub, 5.9, 500, FG3, 'end'))
        if kind == 'scen':
            out.append(R(x0, y + .7, X(v) - x0, 5, 'url(#hatch)', 1.4, f'stroke="{GOLD}" stroke-width=".35"'))
            out.append(T(X(v) + 2, y + 4.5, vl, 7.2, 800, GOLD))
        else:
            out.append(R(x0, y + .7, X(v) - x0, 5, BLUE, 1.4, 'filter="url(#glow)"'))
            out.append(T(X(v) + 2, y + 4.5, vl, 7.2, 800, FG))
        out.append(T(W, y + 4.5, seats, 8.2, 800, FG if kind == 'scen' else FG2, 'end'))
        y += 9 if kind == 'scen' else 7.4
        if kind == 'scen':
            out.append(L(0, y - 1.6, W, y - 1.6, GRID))
    return svg(W, top + 46, ''.join(out))


# ── 7. Proportion bar (e.g. 696 of 2,026) ──────────────────────────────────────
def proportion(part, whole, W=80, col=GREEN, label_part='', label_rest=''):
    f = part / whole
    out = [R(0, 0, W * f - .4, 4, col, 1.2, 'filter="url(#glow)"'), R(W * f + .4, 0, W * (1 - f) - .4, 4, 'rgba(150,172,167,.3)', 1.2)]
    out.append(T(0, 8.4, label_part, 6.4, 700, FG))
    out.append(T(W, 8.4, label_rest, 6.4, 600, FG3, 'end'))
    return svg(W, 10, ''.join(out))


# ── 8. Dot grid (e.g. 12 of 22) ────────────────────────────────────────────────
def dots(n_on, n, cols=11, r=1.75, gap=4.6, col=GREEN):
    rows = (n + cols - 1) // cols; out = []
    for i in range(n):
        cx = r + .3 + (i % cols) * gap; cy = r + .3 + (i // cols) * gap
        if i < n_on:
            out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r}" fill="{col}" filter="url(#glow)"/>')
        else:
            out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r - .2}" fill="none" stroke="rgba(180,197,194,.45)" stroke-width=".35"/>')
    return svg(round(cols * gap, 1), round(rows * gap, 1), ''.join(out))


# ── 9. Actual vs target (apprenticeships) ──────────────────────────────────────
def vs_target(actual, target, W=70, vmax=None, lab_a='', lab_t='', col=GREEN):
    vmax = vmax or actual * 1.1
    X = lambda v: W * v / vmax
    out = [R(0, 3, W, 3.4, TRACK), R(0, 3, X(actual), 3.4, col, None, 'filter="url(#glow)"')]
    out.append(L(X(target), .8, X(target), 8.6, GOLD, .45))
    out.append(T(X(target), 11.6, lab_t, 6, 700, GOLD, 'middle'))
    out.append(T(min(X(actual), W) , 11.6, lab_a, 6, 700, FG, 'end'))
    return svg(W, 12.5, ''.join(out))


# ── 10. Gauge: scenario imports vs the outcomes-track criterion ────────────────
def gauge(W=80):
    vmax = 600; X = lambda v: W * v / vmax
    out = [R(0, 4, W, 3.4, TRACK), R(0, 4, X(421.6), 3.4, IMP, None, 'filter="url(#glow)"')]
    out.append(L(X(500), 1.4, X(500), 10, GOLD, .45))
    out.append(T(X(500), 13.2, 'SAR 500m criterion', 6, 700, GOLD, 'middle'))
    out.append(T(X(421.6) - .6, 2.6, 'our SAR 421.6m', 6, 700, FG, 'end'))
    return svg(W, 14, ''.join(out))


# ── 11. Materials basket and a 25% shift ───────────────────────────────────────
def basket(W=106):
    vmax = 176.97; X = lambda v: W * v / vmax
    out = []
    out.append(T(0, 3, 'Modelled chemicals and metals import basket', 6.6, 700, FG))
    out.append(T(W, 3, 'SAR 176.97m', 7.4, 800, FG, 'end'))
    s = 44.24
    out.append(R(0, 5, X(s) - .4, 6, GREEN, 1.4, 'filter="url(#glow)"'))
    out.append(R(X(s) + .4, 5, W - X(s) - .4, 6, 'rgba(238,106,51,.75)', 1.4))
    # inner split of the basket: chemicals 94, metals 83 (rounded)
    out.append(T(X(s) / 2, 9.2, '25% shift', 6.2, 800, '#062014', 'middle'))
    out.append(T(X(s) + 2.5, 9.2, 'remaining 75% · SAR 132.73m', 6.2, 700, '#2A0E03'))
    out.append(T(0, 16, 'SAR 44.24m', 10, 800, GREEN))
    out.append(T(25, 16, 'additional domestic purchases, subject to actual items, capacity and cost', 6.3, 500, FG2))
    return svg(W, 17.5, ''.join(out))


# ── 12. Funding: activity vs EP credit under two factor sets ───────────────────
def funding(W=178):
    cats = [('Technology transfer', BLUE), ('Knowledge transfer', GREEN), ('Localisation', GOLD)]
    lab = 30; x0 = lab + 4; x1 = W - 24; vmax = 90
    X = lambda v: x0 + (x1 - x0) * v / vmax
    obl = 421.6096 * .2
    sets = [('Illustrative factors 3, 2, 2', (3, 2, 2)), ('Same mix at category minima 2, 1, 1', (2, 1, 1))]
    out = []; y = 6
    for v in range(0, 91, 10):
        out.append(L(X(v), 3, X(v), 64, GRID))
        out.append(T(X(v), 67.5, str(v), 6, 600, FG3, 'middle'))
    out.append(T(x1 + 2, 67.5, 'SAR m', 6, 600, FG3))
    for title, fs in sets:
        act_total = obl * 3 / sum(fs); each = act_total / 3
        out.append(T(0, y + 1.5, title.upper(), 5.6, 700, GOLD, extra='letter-spacing=".35"'))
        y += 4
        for kind in ('Activity value', 'EP credit'):
            out.append(T(lab, y + 3.6, kind, 7.2, 700, FG if kind == 'EP credit' else FG2, 'end'))
            cx = x0
            for (cn, cc), f in zip(cats, fs):
                v = each * (f if kind == 'EP credit' else 1)
                w = X(v) - x0
                op = '1' if kind == 'EP credit' else '.55'
                out.append(R(cx + .25, y, w - .5, 5.2, cc, 1.1, f'fill-opacity="{op}"'))
                lbl = f'{v:.2f}' if kind == 'EP credit' else f'{v:.2f}'
                if w > 9:
                    out.append(T(cx + w / 2, y + 3.55, lbl, 5.8, 800, '#06110E', 'middle'))
                cx += w
            tot = obl if kind == 'EP credit' else act_total
            out.append(T(cx + 2, y + 3.7, f'SAR {tot:.2f}m', 7.6, 800, FG if kind == 'EP credit' else FG2))
            y += 7.4
        y += 3.6
    # legend
    lx = x0
    for cn, cc in cats:
        out.append(R(lx, 71, 2.8, 2.8, cc, .6))
        out.append(T(lx + 4, 73.4, cn, 6.4, 600, FG2))
        lx += 31
    out.append(T(W, 73.4, 'faded: activity value · solid: credit earned', 6.2, 500, FG3, 'end'))
    return svg(W, 75, ''.join(out))

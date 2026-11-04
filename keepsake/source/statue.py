"""King Salman Stadium keepsake — a four-colour, print-ready landscape model.

Builds the stadium scene from the 3D presentation (stepped bowl, diagrid
facade, gold roof ring, pitch, approach road with palms, the MBSC billboard,
the container yard and floodlight masts) on an engraved plinth, as one
watertight solid per filament colour. Units are millimetres; +Z is up and the
viewer stands on the -Y side.

Usage: python statue.py OUT_DIR
Writes, for each size (large, small): one STL per colour and a Bambu Studio
3MF that loads as a single object with the four parts already assigned to
AMS slots 1-4 (white, green, gold, red).
"""
import math, os, sys, zipfile
import numpy as np
from manifold3d import Manifold, CrossSection, FillRule
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from skimage import measure, morphology

HERE = os.path.dirname(os.path.abspath(__file__))
COLOURS = ['white', 'green', 'gold', 'red']
FONT = FontProperties(fname='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
_IFD = '/usr/share/fonts/opentype/inter/InterDisplay-%s.otf'
FONTS = {w: _IFD % w for w in ('Black', 'ExtraBold', 'Bold', 'SemiBold', 'Medium')}

# ── primitives ──────────────────────────────────────────────────────────────
def ellipse(a, b, n=160):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return CrossSection([np.c_[a * np.cos(t), b * np.sin(t)]])

def rrect(w, d, r, n=10):
    r = min(r, w / 2 - .01, d / 2 - .01)
    pts = []
    for cx, cy, a0 in [(w/2-r, d/2-r, 0), (-w/2+r, d/2-r, 90), (-w/2+r, -d/2+r, 180), (w/2-r, -d/2+r, 270)]:
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return CrossSection([np.array(pts)])

def rect(x0, y0, x1, y1):
    return CrossSection([np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])])

def slab(cs, z0, h):
    return cs.extrude(h).translate([0, 0, z0])

def box(x0, y0, z0, x1, y1, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])

def union(parts):
    parts = [p for p in parts if p is not None and not p.is_empty()]
    if not parts: return Manifold()
    return Manifold.batch_boolean(parts, manifold3d_op_add())

def manifold3d_op_add():
    import manifold3d
    return manifold3d.OpType.Add

def text_cs(s, height, cx, cy):
    """Text as a CrossSection, cap height `height`, centred on (cx, cy)."""
    tp = TextPath((0, 0), s, size=1, prop=FONT)
    polys = [p for p in tp.to_polygons(closed_only=True) if len(p) > 2]
    cap = TextPath((0, 0), 'H', size=1, prop=FONT).get_extents().height
    k = height / cap
    ext = tp.get_extents()
    ox, oy = (ext.x0 + ext.x1) / 2, cap / 2
    return CrossSection([(p - [ox, oy]) * k + [cx, cy] for p in polys], FillRule.EvenOdd)

def tracked_cs(s, cap_h, cx, cy, weight='Bold', track=0.0):
    """Letter-spaced text in Inter Display: cap height `cap_h`, extra spacing `track` x cap height."""
    from matplotlib.ft2font import FT2Font
    path = FONTS[weight]; prop = FontProperties(fname=path)
    ft = FT2Font(path); ft.set_size(1, 72)
    capp = TextPath((0, 0), 'H', size=1, prop=prop).get_extents().height
    k = cap_h / capp
    x, rings = 0.0, []
    for ch in s:
        adv = ft.load_char(ord(ch)).linearHoriAdvance / 65536.0
        if ch.strip():
            tp = TextPath((x, 0), ch, size=1, prop=prop)
            rings += [p for p in tp.to_polygons(closed_only=True) if len(p) > 2]
        x += adv + track
    x -= track
    return CrossSection([(r - [x / 2, capp / 2]) * k + [cx, cy] for r in rings], FillRule.EvenOdd)

def mask_cs(mask, width_mm, cx, cy, px_per_mm=12):
    """Binary image (row 0 = top) -> CrossSection `width_mm` wide, centred."""
    h, w = mask.shape
    scale = width_mm / w
    step = max(1, int(round(1 / (scale * px_per_mm))))
    m = mask[::step, ::step]
    m = np.pad(m, 2).astype(float)
    rings = []
    for c in measure.find_contours(m, .5):
        if len(c) < 6: continue
        xy = np.c_[(c[:, 1] - 2) * step * scale, -(c[:, 0] - 2) * step * scale]
        rings.append(xy)
    cs = CrossSection(rings, FillRule.EvenOdd).simplify(0.02)
    b = cs.bounds()
    return cs.translate([cx - (b[0] + b[2]) / 2, cy - (b[1] + b[3]) / 2])

# ── the scene ───────────────────────────────────────────────────────────────
def build(S, small):
    """S = linear scale (1 = large). `small` drops detail finer than a 0.4 mm nozzle."""
    def L(v, lo=None):                       # scaled length with a printable floor
        v = v * S
        return max(v, lo) if lo else v
    P = {c: [] for c in COLOURS}

    W, D = L(210), L(170)
    H = L(8, 5)                              # plinth height
    CH = L(1.4, 1)                           # top chamfer
    P['white'].append(rrect(W, D, L(10)).extrude(H - CH))
    P['white'].append(rrect(W, D, L(10)).extrude(CH, scale_top=((W - 2*CH) / W, (D - 2*CH) / D)).translate([0, 0, H - CH]))
    z0 = H

    # front text strip
    # a three-level hierarchy: the name, the place and year, then the group credit
    t1, t2, t3 = L(7.6, 4.2), L(4.0, 2.7), L(3.1, 2.4)
    y3 = -D / 2 + L(4.2, 2.4) + t3 / 2
    y2 = y3 + t3 / 2 + L(3.0, 1.7) + t2 / 2
    y1 = y2 + t2 / 2 + L(3.2, 1.9) + t1 / 2
    strip = (y1 + t1 / 2 + L(3.2, 1.9)) + D / 2
    tz1, tz2 = L(1.0, .7), L(.7, .5)
    title = tracked_cs('KING SALMAN STADIUM', t1, 0, y1, 'Black', .04)
    sub = tracked_cs('RIYADH  ·  2034', t2, 0, y2, 'SemiBold', .28)
    cred = tracked_cs('GROUP 8  ·  MBSC EMBA  ·  ECN 511  ·  2026', t3, 0, y3, 'SemiBold' if small else 'Medium', .18)
    P['gold'].append(slab(title, z0, tz1))
    P['gold'].append(slab(sub, z0, tz2))
    P['gold'].append(slab(cred, z0, tz2))
    # hairline rules either side of RIYADH · 2034, plaque style
    sb = sub.bounds(); tb = title.bounds(); rw = L(.8, .7)
    for x0, x1 in [(tb[0], sb[0] - L(4, 2.4)), (sb[2] + L(4, 2.4), tb[2])]:
        if x1 - x0 > L(4): P['gold'].append(box(x0, y2 - rw / 2, z0, x1, y2 + rw / 2, z0 + tz2))
    yStrip = -D / 2 + strip

    # stadium footprint (centre pushed back so the road has room)
    cy = L(14)
    A, B = L(58), L(51)                      # outer facade
    Ai, Bi = A - L(3.5, 2.2), B - L(3.5, 2.2) # inner face of the outer wall
    WALL = L(26)
    st = lambda cs: cs.translate([0, cy])

    # plaza (white, left bare) and the lawn (green, raised)
    plaza = st(ellipse(A + L(8), B + L(8)))
    road_w = L(22, 13)
    road = rect(-road_w / 2, yStrip, road_w / 2, cy - B + L(4))
    yard = rect(L(44), yStrip + L(4), W / 2 - L(8), L(-22))
    bb_x0, bb_x1, bb_y = -W / 2 + L(10), -W / 2 + L(60), yStrip + L(13)
    billboard_pad = rect(bb_x0 - L(2), bb_y - L(5), bb_x1 + L(2), bb_y + L(5))
    lawn = rrect(W - L(7), D - L(7), L(7)).translate([0, 0]) - rect(-W, -D, W, yStrip + L(1.5))
    lawn = lawn - plaza - road - yard - billboard_pad
    LZ = L(1.2, .8)
    P['green'].append(slab(lawn, z0, LZ))

    # road lane dashes (gold)
    dash_w, dash_l, gap = L(1.2, 1), L(4.5, 3), L(3.2, 2.4)
    y = yStrip + L(2)
    while y + dash_l < cy - B - L(1):
        P['gold'].append(box(-dash_w / 2, y, z0, dash_w / 2, y + dash_l, z0 + L(.4, .4)))
        y += dash_l + gap

    # stadium podium, stepped bowl and outer wall (white)
    a0, b0 = L(28), L(19)                    # innermost seating edge, around the pitch
    PODIUM = L(1.5, 1)
    P['white'].append(slab(st(ellipse(A + L(2), B + L(2)) - ellipse(a0, b0)), z0, PODIUM))
    N = 16 if not small else 10
    for i in range(N):
        f = i / (N - 1)
        ai, bi = a0 + (Ai - a0) * f, b0 + (Bi - b0) * f
        h = L(2.2) + (L(24) - L(2.2)) * f ** 1.2
        P['white'].append(slab(st(ellipse(A, B) - ellipse(ai, bi)), z0, h))
    P['white'].append(slab(st(ellipse(A, B) - ellipse(Ai, Bi)), z0, WALL))
    # vomitory tunnels into the middle tier
    for k in range(10):
        th = 2 * math.pi * k / 10 + .31
        fx, fy = math.cos(th), math.sin(th)
        mid_a, mid_b = a0 + (Ai - a0) * .5, b0 + (Bi - b0) * .5
        vw = L(3.2, 2)
        v = box(-vw / 2, -L(4), 0, vw / 2, L(4), L(3.2, 2)).rotate([0, 0, math.degrees(th) + 90])
        v = v.translate([mid_a * fx, cy + mid_b * fy, z0 + L(2.2) + (L(24) - L(2.2)) * .5 ** 1.2 - L(3.2, 2) + .01])
        P['white'][-1] = P['white'][-1]  # keep wall
        P.setdefault('_cut', []).append(v)

    # pitch (green) with white field markings
    pitch_floor = st(ellipse(a0 + .01, b0 + .01))
    pz = PODIUM - L(.6, .4)                  # markings sit flush with the pitch top
    green_pitch = slab(pitch_floor, z0, PODIUM)
    P['green'].append(green_pitch)
    if not small:
        lw = L(.8)
        fw, fd = L(40), L(26)
        lines = []
        def frame(x0, y0, x1, y1):
            return rect(x0 - lw/2, y0 - lw/2, x1 + lw/2, y1 + lw/2) - rect(x0 + lw/2, y0 + lw/2, x1 - lw/2, y1 - lw/2)
        lines.append(frame(-fw/2, -fd/2, fw/2, fd/2))
        lines.append(rect(-lw/2, -fd/2, lw/2, fd/2))
        lines.append(ellipse(L(4.2) + lw/2, L(4.2) + lw/2, 64) - ellipse(L(4.2) - lw/2, L(4.2) - lw/2, 64))
        for sgn in (-1, 1):
            x_edge = sgn * fw / 2
            lines.append(frame(min(x_edge, x_edge - sgn * L(6.5)), -L(7.5), max(x_edge, x_edge - sgn * L(6.5)), L(7.5)))
        mk = None
        for c in lines: mk = c if mk is None else mk + c
        P['_lines'] = [slab(mk.translate([0, cy]), z0 + pz, L(.6, .4))]

    # diagrid facade: raised diagonal ribs around the outer wall (white)
    rib_w, rib_out = L(1.5, 1.0), L(.8, .6)
    NR = 36 if not small else 24
    span = 2 * math.pi / NR * 3
    zb, zt = z0 + L(2), z0 + WALL - L(1.2)
    SEG = 7
    def surf(th, z, out):
        x, y = A * math.cos(th), B * math.sin(th)
        nx, ny = B * math.cos(th), A * math.sin(th); n = math.hypot(nx, ny); nx, ny = nx / n, ny / n
        tx, ty = -A * math.sin(th), B * math.cos(th); t = math.hypot(tx, ty); tx, ty = tx / t, ty / t
        return x, y + cy, nx, ny, tx, ty
    ribs = []
    for k in range(NR):
        for sgn in (-1, 1):
            th0 = 2 * math.pi * k / NR
            for s in range(SEG):
                pts = []
                for u in (s / SEG, (s + 1) / SEG):
                    th, z = th0 + sgn * span * u, zb + (zt - zb) * u
                    x, y, nx, ny, tx, ty = surf(th, z, rib_out)
                    for dn in (-L(.6, .5), rib_out):
                        for dt in (-rib_w / 2, rib_w / 2):
                            for dz in (-rib_w / 2, rib_w / 2):
                                pts.append([x + nx * dn + tx * dt, y + ny * dn + ty * dt, z + dz])
                ribs.append(Manifold.hull_points(np.array(pts)))
    P['white'].append(union(ribs))

    # gold roof ring: 45-degree undersides inside and out, so it prints without supports
    rz = z0 + WALL
    lip = L(.9, .7)
    ring_out = A + L(1.2, .8)
    outer = st(ellipse(A, B)).extrude(ring_out - A, scale_top=(ring_out / A, (B + ring_out - A) / B)).translate([0, 0, rz])
    outer = outer + slab(st(ellipse(ring_out, B + ring_out - A)), rz + ring_out - A, L(3.2) - (ring_out - A))
    inset = L(2.6, 1.6)
    cone = ellipse(Ai, Bi).extrude(inset, scale_top=((Ai - inset) / Ai, (Bi - inset) / Bi)).translate([0, cy, rz - .01])
    hole = slab(st(ellipse(Ai - inset, Bi - inset)), rz + inset - .02, L(10))
    ring = outer - cone - hole
    P['gold'].append(ring)

    # the centre-hung scoreboard from the presentation, on cables to the wall top
    sbw, sbh = L(19, 10), L(9, 5)
    sb_top = z0 + WALL - L(1.2, .8)
    sb_bot = sb_top - sbh
    body = box(-sbw / 2, cy - sbw / 2, sb_bot, sbw / 2, cy + sbw / 2, sb_top)
    # 45-degree underside to a point, then a thin snap-off pin down to the centre spot
    apex = sb_bot - sbw / 2
    pyr = Manifold.hull_points(np.array([[dx * sbw / 2, cy + dy * sbw / 2, sb_bot] for dx in (-1, 1) for dy in (-1, 1)] + [[0, cy, apex]]))
    pin_r = L(.9, .7)
    pin = Manifold.cylinder(apex - (z0 + PODIUM) + L(.6), pin_r, pin_r * .55, 16).translate([0, cy, z0 + PODIUM - .01])
    P['white'] += [body, pyr, pin]
    # four red screens, with MBSC and 2034 in white on the large model
    scr_w, scr_h, scr_d = sbw - L(2.4, 1.4), sbh - L(2.2, 1.4), L(.6, .5)
    for k, label in enumerate(['MBSC', '2034', 'MBSC', '2034']):
        cs = rect(-scr_w / 2, sb_bot + (sbh - scr_h) / 2, scr_w / 2, sb_bot + (sbh + scr_h) / 2)
        face = cs.extrude(scr_d).rotate([90, 0, 0]).translate([0, -sbw / 2 + .01, 0])
        parts_r = [face]
        if not small:
            txt = tracked_cs(label, scr_h * .5, 0, sb_bot + sbh / 2, 'Black', .06)
            parts_r.append(('w', txt.extrude(scr_d + L(.5)).rotate([90, 0, 0]).translate([0, -sbw / 2 + .01, 0])))
        for pr in parts_r:
            col, m = ('red', pr) if not isinstance(pr, tuple) else ('white', pr[1])
            m = m.rotate([0, 0, 90 * k]).translate([0, cy, 0])
            if col == 'red': P['red'].append(m)
            else: P.setdefault('_over', []).append(m)
    # cables: straight gold rods from the board's top corners to the wall top
    cr = L(.75, .6)
    for dx in (-1, 1):
        for dy in (-1, 1):
            th = math.atan2(dy * B, dx * A)
            ex, ey = (Ai + L(1)) * math.cos(th), cy + (Bi + L(1)) * math.sin(th)
            sx0, sy0 = dx * (sbw / 2 - cr), cy + dy * (sbw / 2 - cr)
            pts = [[px + ox, py + oy, sb_top - cr * 2 + oz] for (px, py) in ((sx0, sy0), (ex, ey))
                   for ox in (-cr, cr) for oy in (-cr, cr) for oz in (0, cr * 2)]
            P['gold'].append(Manifold.hull_points(np.array(pts)))

    # palms along the approach (green)
    rng = np.random.default_rng(2034)
    def bez(p0, p1, p2, t):
        return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2
    def palm(x, y, hgt, lean=0.0, lean_dir=0.0):
        """Date palm: ringed, slightly leaning trunk and a crown of arched fronds.
        Frond tips stay at least ~15 degrees above horizontal so they print without supports."""
        parts = []
        tr = L(1.05, .9)
        nseg = max(5, int(hgt / L(1.1, .9)))
        lx, ly = math.cos(lean_dir) * lean, math.sin(lean_dir) * lean
        pts_axis = []
        for i in range(nseg + 1):
            f = i / nseg
            pts_axis.append(np.array([x + lx * f * f * hgt, y + ly * f * f * hgt, z0 + LZ * .5 + f * hgt]))
        for i in range(nseg):
            c0, c1 = pts_axis[i], pts_axis[i + 1]
            r0 = tr * (1 - .25 * i / nseg); r1 = tr * (1 - .25 * (i + 1) / nseg)
            ring = r0 * 1.16                                   # the leaf-scar rings of a date palm
            seg = []
            for k in range(10):
                a = 2 * math.pi * k / 10
                for (c, r) in ((c0, r0), (c0 * .7 + c1 * .3, ring), (c1, r1)):
                    seg.append([c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]])
            parts.append(Manifold.hull_points(np.array(seg)))
        top = pts_axis[-1]
        parts.append(Manifold.sphere(tr * 1.25, 18).translate(top.tolist()))
        nf = 9 if not small else 7
        for j in range(nf):
            a = 2 * math.pi * j / nf + rng.uniform(-.25, .25)
            reach = L(6.4, 3.6) * rng.uniform(.85, 1.1)
            lift = L(3.4, 2.0) * rng.uniform(.9, 1.15)
            end = lift * .55 + reach * .27                     # >= ~15 deg at the tip
            d = np.array([math.cos(a), math.sin(a), 0.0])
            p0 = top + [0, 0, L(.2)]; p1 = top + d * reach * .35 + [0, 0, lift]; p2 = top + d * reach + [0, 0, end]
            side = np.array([-d[1], d[0], 0.0])
            SEG = 7
            prev = None
            for i in range(SEG + 1):
                t = i / SEG
                c = bez(p0, p1, p2, t)
                w = (L(1.5, 1.0) * (1 - t) + L(.45, .45) * t)
                th = (L(.8, .7) * (1 - t) + L(.45, .45) * t)
                sec = [c + side * w / 2, c - side * w / 2, c + [0, 0, th / 2], c - [0, 0, th / 2]]
                if prev is not None:
                    parts.append(Manifold.hull_points(np.array(prev + sec)))
                prev = sec
        # two young spear fronds standing up in the middle
        for j in range(2):
            a = rng.uniform(0, 2 * math.pi); d = np.array([math.cos(a), math.sin(a), 0.0]) * L(1.2)
            tip = top + d + [0, 0, L(3.2, 2)]
            parts.append(Manifold.hull_points(np.array([top + [L(.5), 0, 0], top - [L(.5), 0, 0], top + [0, L(.5), 0], top - [0, L(.5), 0], tip])))
        return union(parts)
    pal = []
    # an avenue of palms lining the approach road
    nrow = 4 if not small else 3
    for i, yy in enumerate(np.linspace(yStrip + L(6), cy - B - L(3), nrow)):
        for sx in (-1, 1):
            pal.append(palm(sx * (road_w / 2 + L(4.5, 3)), yy, L(12.5, 7) * rng.uniform(.9, 1.08), L(.06), math.pi / 2 + sx * .4))
    # groves around the plaza and at the back corners
    grove = [(-W/2 + L(18), D/2 - L(18)), (-W/2 + L(28), D/2 - L(12)), (W/2 - L(18), D/2 - L(18)), (W/2 - L(30), D/2 - L(11)),
             (-W/2 + L(14), L(18)), (-W/2 + L(22), L(4)), (W/2 - L(16), L(22)), (W/2 - L(26), L(30))]
    if small: grove = grove[::2]
    for (gx, gy) in grove:
        pal.append(palm(gx, gy, L(14, 8) * rng.uniform(.85, 1.1), L(.08), rng.uniform(0, 2 * math.pi)))
    # rounded shrubs ringing the plaza (half spheres print without supports)
    nsh = 30 if not small else 18
    for k in range(nsh):
        th = 2 * math.pi * k / nsh + .05
        px, py = (A + L(11)) * math.cos(th), cy + (B + L(11)) * math.sin(th)
        if abs(px) < road_w / 2 + L(3) and py < cy: continue                       # keep the road clear
        if px > L(40) and py < L(-20): continue                                      # and the yard
        if -W / 2 + L(8) < px < -W / 2 + L(62) and py < yStrip + L(22): continue    # and the billboard
        if abs(px) > W / 2 - L(5) or abs(py) > D / 2 - L(5) or py < yStrip + L(3): continue
        r = L(2.1, 1.4) * rng.uniform(.8, 1.15)
        pal.append(Manifold.sphere(r, 20).translate([px, py, z0 + LZ * .5]).trim_by_plane([0, 0, 1], z0 + LZ * .5))
    P['green'].append(union(pal))

    # container yard — the import "leak" (red, gold, white)
    cw, cd, chh = L(11, 7), L(4.4, 3), L(3.6, 2.4)
    cols = ['red', 'gold', 'white', 'red', 'white', 'gold']
    gx0, gy0 = L(48), yStrip + L(8)
    k = 0
    for r in range(4 if not small else 3):
        for c in range(3):
            x = gx0 + c * (cw + L(1.6, 1.2)); yy = gy0 + r * (cd + L(1.4, 1))
            if x + cw > W / 2 - L(8): continue
            hgt = 1 if (r + c) % 3 else 2
            for lvl in range(hgt):
                col = cols[(k + lvl) % len(cols)]
                P[col].append(box(x, yy, z0 + lvl * chh, x + cw, yy + cd, z0 + (lvl + 1) * chh - .02 * (lvl == 0)))
            k += 1

    # floodlight masts by the yard (white post, gold 45-degree head)
    if not small:
        for (x, y) in [(L(42), yStrip + L(6)), (W / 2 - L(6), L(-26)), (W / 2 - L(6), yStrip + L(6))]:
            post, mh = L(2.2), L(30)
            P['white'].append(box(x - post/2, y - post/2, z0, x + post/2, y + post/2, z0 + mh))
            hw = L(3.4)
            pts = [[x + dx * post/2, y + dy * post/2, z0 + mh - L(.2)] for dx in (-1, 1) for dy in (-1, 1)] + \
                  [[x + dx * hw, y + dy * L(1.4), z0 + mh + L(1.6)] for dx in (-1, 1) for dy in (-1, 1)] + \
                  [[x + dx * hw, y + dy * L(1.4), z0 + mh + L(3.2)] for dx in (-1, 1) for dy in (-1, 1)]
            P['gold'].append(Manifold.hull_points(np.array(pts)))

    # the billboard from the opening scene, carrying the MBSC shield
    bw, bh, bt = bb_x1 - bb_x0, L(36, 20), L(3.4, 2.6)
    base_h = L(3, 2)
    P['white'].append(box(bb_x0 - L(1), bb_y - L(3), z0, bb_x1 + L(1), bb_y + L(3), z0 + base_h))
    P['white'].append(box(bb_x0, bb_y - bt / 2, z0 + base_h, bb_x1, bb_y + bt / 2, z0 + base_h + bh))
    from PIL import Image
    red = np.array(Image.open(os.path.join(HERE, 'shield_red.png')).convert('L')) > 127
    white = np.array(Image.open(os.path.join(HERE, 'shield_white.png')).convert('L')) > 127
    shield = red | white
    shield = morphology.remove_small_holes(shield, max_size=5000)
    if small:
        # keep only the bold parts a 0.4 mm nozzle can draw at this size: MBSC and the swoosh
        lab = measure.label(white)
        keep = np.zeros_like(white)
        for reg in measure.regionprops(lab):
            if reg.area > 9000: keep[lab == reg.label] = True
        white_use = keep
    else:
        white_use = morphology.dilation(white, morphology.disk(3))
    sh_h = bh - L(4, 2.4)
    sh_w = sh_h * shield.shape[1] / shield.shape[0]
    scx, scz = (bb_x0 + bb_x1) / 2, z0 + base_h + bh / 2
    front = bb_y - bt / 2
    red_d, wht_d = L(.9, .7), L(.6, .5)
    def on_face(cs, depth, y_face):
        # CrossSection in (x, z) -> solid on the billboard face, standing out towards -Y
        m = cs.extrude(depth)                       # along +Z
        m = m.rotate([90, 0, 0])                    # (x, y, z) -> (x, -z, y): depth now along -Y
        return m.translate([0, y_face + .01, 0])
    sh_cs = mask_cs(shield, sh_w, scx, scz)
    wh_cs = mask_cs(white_use, sh_w * white_use.shape[1] / shield.shape[1], scx, scz) if False else None
    # align white to the shield frame exactly: build both from one bounding box
    def mask_in_frame(mask):
        hgt, wid = shield.shape
        sc = sh_w / wid
        step = max(1, int(round(1 / (sc * 12))))
        mm = np.pad(mask[::step, ::step], 2).astype(float)
        rings = []
        for c in measure.find_contours(mm, .5):
            if len(c) < 6: continue
            rings.append(np.c_[scx - sh_w / 2 + (c[:, 1] - 2) * step * sc, scz + sh_h / 2 - (c[:, 0] - 2) * step * sc])
        return CrossSection(rings, FillRule.EvenOdd).simplify(.02)
    sh_cs = mask_in_frame(shield)
    if small:
        ys, xs = np.where(white)
        band = white.copy(); band[int(shield.shape[0] * .19):] = False      # the MBSC heading band
        by = np.where(band.any(1))[0]
        band_mid = scz + sh_h / 2 - (by.min() + by.max()) / 2 / shield.shape[0] * sh_h
        wh_cs = text_cs('MBSC', max(sh_h * .13, 2.6), scx, band_mid)
        # the white swoosh under the heading, kept bold
        lab = measure.label(white & ~band)
        big = max(measure.regionprops(lab), key=lambda r: r.area if r.bbox[1] < 40 else 0)
        sw = morphology.dilation(lab == big.label, morphology.disk(6))
        wh_cs = wh_cs + mask_in_frame(sw & shield)
    else:
        wh_cs = mask_in_frame(white_use & shield)
    P['red'].append(on_face(sh_cs - wh_cs, red_d, front))
    P['white'].append(on_face(wh_cs, red_d + wht_d, front))
    # a gold frame around the panel face
    fr = L(1.2, 1)
    frame = (rect(bb_x0, z0 + base_h, bb_x1, z0 + base_h + bh) - rect(bb_x0 + fr, z0 + base_h + fr, bb_x1 - fr, z0 + base_h + bh - fr))
    P['gold'].append(on_face(frame, L(.6, .5), front))

    # ── resolve colours so no two parts overlap ──
    cut = union(P.pop('_cut', []))
    over = union(P.pop('_over', []))                      # white lettering on red screens
    lines = union(P.pop('_lines', [])) + over
    solids = {c: union(P[c]) for c in COLOURS}
    solids['white'] = solids['white'] - cut
    solids['red'] = solids['red'] - over
    solids['gold'] = solids['gold'] - solids['red']
    solids['green'] = solids['green'] - solids['red'] - solids['gold'] - lines
    solids['white'] = solids['white'] + lines - solids['red']
    solids['white'] = solids['white'] - solids['red'] - solids['gold'] - solids['green']
    return solids

# ── export ──────────────────────────────────────────────────────────────────
def mesh_arrays(m):
    mesh = m.to_mesh()
    return np.asarray(mesh.vert_properties)[:, :3].astype(np.float64), np.asarray(mesh.tri_verts).astype(np.int64)

def write_stl(path, v, f):
    tri = v[f]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    data = np.zeros(len(f), dtype=[('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
    data['n'] = n; data['v'] = tri
    with open(path, 'wb') as fh:
        fh.write(b'King Salman Stadium keepsake'.ljust(80, b' '))
        fh.write(np.uint32(len(f)).tobytes()); fh.write(data.tobytes())

def write_3mf(path, parts, name):
    """Bambu Studio / PrusaSlicer 3MF: one object, four parts, parts mapped to AMS slots 1-4."""
    objs, comps, cfg_parts = [], [], []
    for i, (col, (v, f)) in enumerate(parts, start=1):
        vs = '\n'.join('<vertex x="%.4f" y="%.4f" z="%.4f"/>' % tuple(p) for p in v)
        ts = '\n'.join('<triangle v1="%d" v2="%d" v3="%d"/>' % tuple(t) for t in f)
        objs.append('<object id="%d" type="model"><mesh><vertices>\n%s\n</vertices><triangles>\n%s\n</triangles></mesh></object>' % (i, vs, ts))
        comps.append('<component objectid="%d"/>' % i)
        cfg_parts.append('<part id="%d" subtype="normal_part"><metadata key="name" value="%s"/><metadata key="extruder" value="%d"/></part>' % (i, col.capitalize(), i))
    oid = len(parts) + 1
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
             'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021">\n'
             '<metadata name="Title">%s</metadata>\n<resources>\n%s\n<object id="%d" type="model"><components>%s</components></object>\n'
             '</resources>\n<build><item objectid="%d" transform="1 0 0 0 1 0 0 0 1 128 128 0" printable="1"/></build>\n</model>\n'
             % (name, '\n'.join(objs), oid, ''.join(comps), oid))
    cfg = ('<?xml version="1.0" encoding="UTF-8"?>\n<config>\n<object id="%d"><metadata key="name" value="%s"/>'
           '<metadata key="extruder" value="1"/>%s</object>\n</config>\n' % (oid, name, ''.join(cfg_parts)))
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
          '<Default Extension="config" ContentType="text/xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct); z.writestr('_rels/.rels', rels)
        z.writestr('3D/3dmodel.model', model); z.writestr('Metadata/model_settings.config', cfg)

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for label, S, small in [('large', 1.0, False), ('small', 0.52, True)]:
        solids = build(S, small)
        parts = []
        for col in COLOURS:
            m = solids[col]
            v, f = mesh_arrays(m)
            # sit on the build plate
            parts.append((col, (v, f)))
        zmin = min(p[1][0][:, 2].min() for p in parts)
        parts = [(c, (v - [0, 0, zmin], f)) for c, (v, f) in parts]
        for col, (v, f) in parts:
            write_stl(os.path.join(out, 'stadium_%s_%d_%s.stl' % (label, COLOURS.index(col) + 1, col)), v, f)
        write_3mf(os.path.join(out, 'stadium_%s_4colour.3mf' % label), parts, 'King Salman Stadium (%s)' % label)
        allv = np.vstack([p[1][0] for p in parts])
        ext = allv.max(0) - allv.min(0)
        print(label, 'size mm: %.1f x %.1f x %.1f' % tuple(ext),
              ' | '.join('%s %d tris vol %.1f cm3 genus-ok %s' % (c, len(f), solids[c].volume() / 1000, solids[c].status().name)
                         for c, (v, f) in parts))

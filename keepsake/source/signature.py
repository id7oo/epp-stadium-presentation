"""Signature edition: King Salman Stadium as Populous designed it, a faceted dome of
folded petals (gold ridges with green planted panels, slots of light between
them, a canyon entrance with a media screen) in its park of green-roofed
pavilions, on a two-tier award plinth with the lettering on the front face and
the full MBSC logo on the back.

Built print-first for a Bambu X1C with AMS: no surface steeper than 45 degrees
from vertical, no floating parts, four colours (white, green, gold, red).

Usage: python signature.py OUT_DIR
"""
import math, os, sys
import numpy as np
from manifold3d import Manifold, CrossSection
import statue as ST
import editions as E
from statue import ellipse, rrect, rect, slab, box, union, tracked_cs, COLOURS

SIZE, T1, T2, INSET = 170, 20, 6, 8          # plinth: lower tier, upper tier, upper-tier inset

def plinth(P):
    CH = 1.2
    # lower tier, with the lettering on its front face
    P['white'].append(rrect(SIZE, SIZE, 10).extrude(T1 - CH))
    P['white'].append(rrect(SIZE, SIZE, 10).extrude(CH, scale_top=((SIZE - 2 * CH) / SIZE,) * 2).translate([0, 0, T1 - CH]))
    yf = -SIZE / 2
    for txt, cap, wt, tr, zc in [('KING SALMAN STADIUM', 6.4, 'Black', .05, T1 - 5.4),
                                 ('RIYADH  ·  2034', 2.9, 'SemiBold', .3, T1 - 11.0),
                                 ('GROUP 8  ·  MBSC EMBA  ·  ECN 511  ·  2026', 2.5, 'SemiBold', .2, T1 - 15.4)]:
        P['gold'].append(E.face_solid(tracked_cs(txt, cap, 0, zc, wt, tr), .8, yf))
    P['gold'].append(E.face_solid(rect(-SIZE / 2 + 16, 1.4, SIZE / 2 - 16, 2.2), .6, yf))
    # the full college logo on the back face (built facing -Y, turned to face +Y)
    full = np.array(E.Image.open(os.path.join(ST.HERE, 'logo_full.png')).convert('L')) > 127
    redm = np.array(E.Image.open(os.path.join(ST.HERE, 'logo_red.png')).convert('L')) > 127
    lh = 14.5; k = lh / full.shape[0]; lw = full.shape[1] * k
    x_left, z_top = -lw / 2, T1 / 2 + lh / 2
    sc = 1010
    sh = np.zeros_like(full); sh[:, :sc] = full[:, :sc]
    tx = np.zeros_like(full); tx[:, sc:] = full[:, sc:]
    shield = E.morphology.remove_small_holes(sh, max_size=5000)
    sh_w = E.morphology.dilation(sh & ~redm, E.morphology.disk(3)) & shield
    sh_cs, wh_cs = ST._mask_rings(shield, x_left, z_top, k), ST._mask_rings(sh_w, x_left, z_top, k)
    back = []
    back.append(('red', E.face_solid(sh_cs - wh_cs, .9, yf)))
    back.append(('white', E.face_solid(wh_cs, 1.5, yf)))
    back.append(('gold', E.face_solid(ST._mask_rings(E.morphology.dilation(tx & ~redm, E.morphology.disk(2)), x_left, z_top, k), .9, yf)))
    if (tx & redm).any():
        back.append(('red', E.face_solid(ST._mask_rings(E.morphology.dilation(tx & redm, E.morphology.disk(2)), x_left, z_top, k), .9, yf)))
    for c, m in back:
        P[c].append(m.rotate([0, 0, 180]))
    # gold band where the tiers meet, then the upper tier
    up = SIZE - 2 * INSET
    P['gold'].append(slab(rrect(up + 2.4, up + 2.4, 7) - rrect(up - .01, up - .01, 6), T1, 1.0))
    P['white'].append(slab(rrect(up, up, 6), T1, T2 - CH))
    P['white'].append(rrect(up, up, 6).extrude(CH, scale_top=((up - 2 * CH) / up,) * 2).translate([0, 0, T1 + T2 - CH]))
    return T1 + T2, up

# ── the faceted dome ────────────────────────────────────────────────────────
def dome(P, cx, cy, z0, A=58, B=50, H=30, N=14):
    ell = lambda t, f: (cx + A * f * math.cos(t), cy + B * f * math.sin(t))
    # profile rings: (radius factor, height factor); the base wall is near-vertical,
    # everything above leans inward, so nothing overhangs more than a few degrees
    RINGS = [(1.00, 0.0), (1.015, .16), (0.90, .55), (0.68, .84), (0.42, .965), (0.17, 1.0)]
    # white core: the light seen through the slots between petals
    core = []
    for (f, h) in RINGS:
        for t in np.linspace(0, 2 * math.pi, 96, endpoint=False):
            x, y = ell(t, f * .95); core.append([x, y, z0 + h * H * .985])
    P['white'].append(Manifold.hull_points(np.array(core)))
    gap = 1.7
    front = -math.pi / 2
    for i in range(N):
        t0 = front + 2 * math.pi * i / N; t1 = front + 2 * math.pi * (i + 1) / N
        rmid = (A + B) / 2
        g0 = gap / rmid / 2 * (3.2 if i == 0 else 1)            # the canyon entrance opens on the front seam
        g1 = gap / rmid / 2 * (3.2 if i == N - 1 else 1)
        a, b = t0 + g0, t1 - g1
        tm = (a + b) / 2
        pts = []
        for j, (f, h) in enumerate(RINGS):
            ridge = 1.045 if 1 <= j <= 4 else 1.0               # a folded ridge down the middle of each petal
            for t, ff in ((a, f), (tm, f * ridge), (b, f)):
                x, y = ell(t, ff); pts.append([x, y, z0 + h * H])
        petal = Manifold.hull_points(np.array(pts))
        # the planted green panel: inset from the petal's edges, standing a little proud
        d = .14 * (b - a)
        gp = []
        for (f, h) in RINGS[1:4]:
            for t, ff in ((a + d, f * 1.012), (tm, f * 1.047), (b - d, f * 1.012)):
                x, y = ell(t, ff); gp.append([x, y, z0 + h * H])
        # keep the panel off the top and bottom bands so the gold reads as a frame
        green = Manifold.hull_points(np.array(gp)) ^ box(cx - 2 * A, cy - 2 * B, z0 + .24 * H, cx + 2 * A, cy + 2 * B, z0 + .8 * H)
        P['gold'].append(petal - green)
        P['green'].append(green)
    # top cap
    P['gold'].append(slab(ellipse(A * .19, B * .19, 96).translate([cx, cy]), z0 + H - .4, 1.2))
    P['white'].append(slab(ellipse(A * .12, B * .12, 96).translate([cx, cy]), z0 + H + .8, .7))
    # the media screen above the canyon entrance
    sx, sy = ell(front, 1.0)
    # a 45-degree bracket under the screen runs back into the dome, so it prints unsupported
    zb, yfr = z0 + .34 * H, sy - 1.4
    scr = Manifold.hull_points(np.array([[sx + dx, yfr, zb + dz] for dx in (-7, 7) for dz in (0, 6)] +
                                        [[sx + dx, yfr + 9, zb + 6] for dx in (-7, 7)] +
                                        [[sx + dx, yfr + 9, zb - 9] for dx in (-7, 7)]))
    P['red'].append(scr)
    P['white'].append(E.face_solid(tracked_cs('MBSC', 2.6, sx, zb + 3, 'Black', .05), .5, yfr))
    # entrance canyon: a lit slot down to a white entrance plaza step
    P['white'].append(box(sx - 4, sy - 6, z0, sx + 4, sy + 6, z0 + 1.2))
    # podium the dome stands on
    P['white'].append(slab(ellipse(A + 3, B + 3, 160).translate([cx, cy]), z0 - 1.2, 1.25))

# ── the park around it ──────────────────────────────────────────────────────
def pavilion(P, x, y, z0, ang, L=26, W=11, Hh=6.5):
    """Green-roofed pavilion rising out of the ground (a ramp), gold shopfront on the high side."""
    c, s = math.cos(ang), math.sin(ang)
    def w(px, py, pz): return [x + px * c - py * s, y + px * s + py * c, pz]
    pts = [w(-L / 2, -W / 2, z0), w(L / 2, -W / 2, z0), w(-L / 2, W / 2, z0), w(L / 2, W / 2, z0),
           w(-L / 2, W / 2, z0 + Hh), w(L / 2, W / 2, z0 + Hh)]
    P['green'].append(Manifold.hull_points(np.array(pts)))
    front = [w(-L / 2 + 1.2, W / 2 - .4, z0), w(L / 2 - 1.2, W / 2 - .4, z0), w(-L / 2 + 1.2, W / 2 + .5, z0), w(L / 2 - 1.2, W / 2 + .5, z0),
             w(-L / 2 + 1.2, W / 2 - .4, z0 + Hh - 1.2), w(L / 2 - 1.2, W / 2 - .4, z0 + Hh - 1.2),
             w(-L / 2 + 1.2, W / 2 + .5, z0 + Hh - 1.2), w(L / 2 - 1.2, W / 2 + .5, z0 + Hh - 1.2)]
    P['gold'].append(Manifold.hull_points(np.array(front)))

def build():
    P = E.new_parts(); rng = np.random.default_rng(2034)
    z0, up = plinth(P)
    cx, cy = 0, 10
    half = up / 2 - 2.5
    # park lawn with paths cut through it
    plaza = ellipse(68, 60, 160).translate([cx, cy])
    paths = None
    for ang in [-90, -30, 30, 90, 150, 210]:
        a = math.radians(ang)
        p = CrossSection([np.array([[0, -2.6], [140, -2.6], [140, 2.6], [0, 2.6]])]).rotate(ang).translate([cx, cy])
        paths = p if paths is None else paths + p
    # the approach road sweeping in from the front-left corner
    road_pts = []
    for t in np.linspace(0, 1, 40):
        x = -half + 4 + (cx - (-half + 4)) * t + 18 * math.sin(math.pi * t)
        y = -half + 4 + (cy - 60 - (-half + 4)) * t
        road_pts.append((x, y))
    road = None
    for (a, b) in zip(road_pts, road_pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy); nx, ny = -dy / n * 5.5, dx / n * 5.5
        seg = CrossSection([np.array([[a[0] + nx, a[1] + ny], [a[0] - nx, a[1] - ny], [b[0] - nx, b[1] - ny], [b[0] + nx, b[1] + ny]])])
        road = seg if road is None else road + seg
    lawn = rrect(up - 5, up - 5, 5) - plaza - paths - road
    P['green'].append(slab(lawn, z0, 1.2))
    # gold dashes along the road
    for (a, b) in list(zip(road_pts, road_pts[1:]))[1::3]:
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        P['gold'].append(box(-1.6, -.5, 0, 1.6, .5, .4).rotate([0, 0, ang]).translate([mx, my, z0]))
    # the stadium
    dome(P, cx, cy, z0 + 1.2)
    # green-roofed pavilions in the park, each rising toward the stadium
    for (x, y) in [(-62, 52), (-40, 66), (62, 52), (40, 66), (66, -20), (70, 6), (52, -48), (-70, 2)]:
        ang = math.atan2(cy - y, cx - x)
        pavilion(P, x, y, z0, ang - math.pi / 2, L=20, W=10, Hh=6)
    # shrubs and trees (half domes print without supports), palms along the road
    for _ in range(46):
        x, y = rng.uniform(-half + 3, half - 3), rng.uniform(-half + 3, half - 3)
        if ((x - cx) / 70) ** 2 + ((y - cy) / 62) ** 2 < 1: continue
        p = np.array([x, y])
        if min(np.hypot(*(p - np.array(q))) for q in road_pts) < 8: continue
        r = rng.uniform(1.3, 2.3)
        P['green'].append(E.shrub(x, y, z0 + .6, r))
    for (a, b) in list(zip(road_pts, road_pts[1:]))[3:30:7]:
        dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy)
        for sd in (-1, 1):
            px, py = a[0] - dy / n * 8.5 * sd, a[1] + dx / n * 8.5 * sd
            if max(abs(px), abs(py)) > half - 6: continue          # keep clear of the tier's edge chamfer
            P['green'].append(E.palm(px, py, z0, 11, rng, .8))
    # trucks on the approach
    for idx, col in [(12, 'red'), (24, 'white')]:
        a, b = road_pts[idx], road_pts[idx + 1]
        ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) - 90
        E.truck(P, a[0], a[1], z0, ang + 180, col, .7)
    return P

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    S = E.resolve(build())
    parts = [(c, ST.mesh_arrays(S[c])) for c in COLOURS]
    zmin = min(v[:, 2].min() for _, (v, f) in parts)
    parts = [(c, (v - [0, 0, zmin], f)) for c, (v, f) in parts]
    for c, (v, f) in parts:
        ST.write_stl(os.path.join(out, 'stadium_signature_%d_%s.stl' % (COLOURS.index(c) + 1, c)), v, f)
    ST.write_3mf(os.path.join(out, 'stadium_signature_4colour.3mf'), parts, 'King Salman Stadium (signature)')
    allv = np.vstack([v for _, (v, f) in parts])
    print('signature %.0f x %.0f x %.0f mm' % tuple(allv.max(0) - allv.min(0)), ' | '.join('%s %s' % (c, S[c].status().name) for c in COLOURS))

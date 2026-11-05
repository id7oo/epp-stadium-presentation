"""Two square editions of the keepsake, built from the same parts as statue.py
(stadium with scoreboard, trucks, containers, palms, the MBSC logo panel, the
lettering) arranged as new compositions:

  ringroad  - the stadium raised on a round dais, a terraced spiral road
              winding up to its gate with trucks climbing it, the logo as a
              corner monolith, the container port in the opposite corner.
  imports   - "Built on imports": the stadium crowns a stepped pyramid of
              shipping containers, ~80% white (made in Saudi, 80.3%) and ~20%
              red (imported, 19.7%); a grand stair rises to it through a
              logo gateway; trucks circle the pyramid.

Usage: python editions.py OUT_DIR
"""
import math, os, sys
import numpy as np
from manifold3d import Manifold, CrossSection
from skimage import morphology
from PIL import Image
import statue as ST
from statue import ellipse, rrect, rect, slab, box, union, tracked_cs, COLOURS, HERE

def face_solid(cs, depth, y_face, embed=.3):
    """Relief drawn in (x, z), standing `depth` out from a face at y_face towards -Y and
    sunk `embed` into the wall, so a slicer always sees it joined to the wall."""
    return cs.extrude(depth + embed).rotate([90, 0, 0]).translate([0, y_face + embed, 0])

def new_parts():
    return {c: [] for c in COLOURS}

# ── plinth with the lettering on its front face ─────────────────────────────
def plinth(P, size, H):
    CH = 1.4
    P['white'].append(rrect(size, size, 12).extrude(H - CH))
    P['white'].append(rrect(size, size, 12).extrude(CH, scale_top=((size - 2 * CH) / size,) * 2).translate([0, 0, H - CH]))
    yf = -size / 2
    lines = [('KING SALMAN STADIUM', 6.6, 'Black', .05, H - 5.2),
             ('RIYADH  ·  2034', 3.0, 'SemiBold', .3, H - 11.0),
             ('GROUP 8  ·  MBSC EMBA  ·  ECN 511  ·  2026', 2.6, 'SemiBold', .2, H - 15.2)]
    for txt, cap, wt, tr, zc in lines:
        cs = tracked_cs(txt, cap, 0, zc, wt, tr)
        P['gold'].append(face_solid(cs, .8, yf))
    # thin gold rule framing the face
    P['gold'].append(face_solid(rect(-size / 2 + 14, 1.0, size / 2 - 14, 1.8), .6, yf))
    return H

# ── stadium, parametric copy of the statue.py stadium ───────────────────────
def stadium(P, s, cx, cy, z0, rng):
    L = lambda v, lo=None: max(v * s, lo) if lo else v * s
    A, B = L(58), L(51)
    Ai, Bi = A - L(3.5, 2), B - L(3.5, 2)
    WALL = L(26)
    st = lambda cs: cs.translate([cx, cy])
    a0, b0 = L(28), L(19)
    PODIUM = L(1.5, 1)
    P['white'].append(slab(st(ellipse(A + L(2), B + L(2)) - ellipse(a0, b0)), z0, PODIUM))
    N = 16 if s > .7 else 11
    for i in range(N):
        f = i / (N - 1)
        ai, bi = a0 + (Ai - a0) * f, b0 + (Bi - b0) * f
        h = L(2.2) + (L(24) - L(2.2)) * f ** 1.2
        P['white'].append(slab(st(ellipse(A, B) - ellipse(ai, bi)), z0, h))
    P['white'].append(slab(st(ellipse(A, B) - ellipse(Ai, Bi)), z0, WALL))
    # pitch and markings
    P['green'].append(slab(st(ellipse(a0 + .01, b0 + .01)), z0, PODIUM))
    if s > .7:
        lw, fw, fd = L(.8, .7), L(40), L(26)
        def frame(x0, y0, x1, y1):
            return rect(x0 - lw/2, y0 - lw/2, x1 + lw/2, y1 + lw/2) - rect(x0 + lw/2, y0 + lw/2, x1 - lw/2, y1 - lw/2)
        mk = frame(-fw/2, -fd/2, fw/2, fd/2) + rect(-lw/2, -fd/2, lw/2, fd/2)
        mk = mk + (ellipse(L(4.2) + lw/2, L(4.2) + lw/2, 64) - ellipse(L(4.2) - lw/2, L(4.2) - lw/2, 64))
        for sg in (-1, 1):
            xe = sg * fw / 2
            mk = mk + frame(min(xe, xe - sg * L(6.5)), -L(7.5), max(xe, xe - sg * L(6.5)), L(7.5))
        P.setdefault('_lines', []).append(slab(st(mk), z0 + PODIUM - L(.6, .45), L(.6, .45)))
    # diagrid ribs
    rib_w, rib_out = L(1.5, 1.0), L(.8, .6)
    NR = 36 if s > .7 else 26
    span = 2 * math.pi / NR * 3
    zb, zt = z0 + L(2), z0 + WALL - L(1.2)
    ribs = []
    for k in range(NR):
        for sg in (-1, 1):
            for sgi in range(7):
                pts = []
                for u in (sgi / 7, (sgi + 1) / 7):
                    th, z = 2 * math.pi * k / NR + sg * span * u, zb + (zt - zb) * u
                    x, y = A * math.cos(th), B * math.sin(th)
                    nx, ny = B * math.cos(th), A * math.sin(th); n = math.hypot(nx, ny); nx, ny = nx / n, ny / n
                    tx, ty = -A * math.sin(th), B * math.cos(th); t = math.hypot(tx, ty); tx, ty = tx / t, ty / t
                    for dn in (-L(.6, .5), rib_out):
                        for dt in (-rib_w / 2, rib_w / 2):
                            for dz in (-rib_w / 2, rib_w / 2):
                                pts.append([cx + x + nx * dn + tx * dt, cy + y + ny * dn + ty * dt, z + dz])
                ribs.append(Manifold.hull_points(np.array(pts)))
    P['white'].append(union(ribs))
    # gold roof ring with 45-degree undersides
    rz = z0 + WALL
    ro = A + L(1.2, .8)
    outer = ellipse(A, B).extrude(ro - A, scale_top=(ro / A, (B + ro - A) / B)).translate([cx, cy, rz])
    outer = outer + slab(st(ellipse(ro, B + ro - A)), rz + ro - A, L(3.2) - (ro - A))
    ins = L(2.6, 1.6)
    cone = ellipse(Ai, Bi).extrude(ins, scale_top=((Ai - ins) / Ai, (Bi - ins) / Bi)).translate([cx, cy, rz - .01])
    hole = slab(st(ellipse(Ai - ins, Bi - ins)), rz + ins - .02, L(10))
    P['gold'].append(outer - cone - hole)
    # centre-hung scoreboard: 45-degree underside, snap-off pin, red screens, gold cables
    sbw, sbh = L(19, 9), L(9, 4.5)
    sb_top = z0 + WALL - L(1.2, .8); sb_bot = sb_top - sbh
    P['white'].append(box(cx - sbw/2, cy - sbw/2, sb_bot, cx + sbw/2, cy + sbw/2, sb_top))
    apex = sb_bot - sbw / 2
    P['white'].append(Manifold.hull_points(np.array([[cx + dx * sbw/2, cy + dy * sbw/2, sb_bot] for dx in (-1, 1) for dy in (-1, 1)] + [[cx, cy, apex]])))
    pr = L(.9, .7)
    P['white'].append(Manifold.cylinder(apex - (z0 + PODIUM) + L(.6), pr, pr * .55, 16).translate([cx, cy, z0 + PODIUM - .01]))
    sw_, sh_, sd_ = sbw - L(2.4, 1.2), sbh - L(2.2, 1.2), L(.6, .5)
    for k, lab in enumerate(['MBSC', '2034', 'MBSC', '2034']):
        face = rect(-sw_/2, sb_bot + (sbh - sh_)/2, sw_/2, sb_bot + (sbh + sh_)/2).extrude(sd_).rotate([90, 0, 0]).translate([0, -sbw/2 + .01, 0])
        P['red'].append(face.rotate([0, 0, 90 * k]).translate([cx, cy, 0]))
        if s > .7:
            t = tracked_cs(lab, sh_ * .5, 0, sb_bot + sbh / 2, 'Black', .06).extrude(sd_ + L(.5)).rotate([90, 0, 0]).translate([0, -sbw/2 + .01, 0])
            P.setdefault('_over', []).append(t.rotate([0, 0, 90 * k]).translate([cx, cy, 0]))
    cr = L(.75, .6)
    for dx in (-1, 1):
        for dy in (-1, 1):
            th = math.atan2(dy * B, dx * A)
            ex, ey = cx + (Ai + L(1)) * math.cos(th), cy + (Bi + L(1)) * math.sin(th)
            sx0, sy0 = cx + dx * (sbw/2 - cr), cy + dy * (sbw/2 - cr)
            pts = [[px + ox, py + oy, sb_top - cr * 2 + oz] for (px, py) in ((sx0, sy0), (ex, ey))
                   for ox in (-cr, cr) for oy in (-cr, cr) for oz in (0, cr * 2)]
            P['gold'].append(Manifold.hull_points(np.array(pts)))
    return dict(A=A, B=B, top=rz + L(3.2))

# ── palms ───────────────────────────────────────────────────────────────────
def bez(p0, p1, p2, t):
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2

def palm(x, y, z0, hgt, rng, s=1.0, lean=.06):
    L = lambda v, lo=None: max(v * s, lo) if lo else v * s
    parts = []
    tr = L(1.05, .85)
    nseg = max(5, int(hgt / L(1.1, .9)))
    ld = rng.uniform(0, 2 * math.pi)
    axis = [np.array([x + math.cos(ld) * lean * f * f * hgt, y + math.sin(ld) * lean * f * f * hgt, z0 + f * hgt]) for f in np.linspace(0, 1, nseg + 1)]
    for i in range(nseg):
        c0, c1 = axis[i], axis[i + 1]
        r0, r1 = tr * (1 - .25 * i / nseg), tr * (1 - .25 * (i + 1) / nseg)
        seg = []
        for k in range(10):
            a = 2 * math.pi * k / 10
            for (c, r) in ((c0, r0), (c0 * .7 + c1 * .3, r0 * 1.16), (c1, r1)):
                seg.append([c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]])
        parts.append(Manifold.hull_points(np.array(seg)))
    top = axis[-1]
    parts += ST.printable_crown(top, tr, L(5.0, 3.2), rng, 8)
    return union(parts)

def shrub(x, y, z0, r):
    return Manifold.sphere(r, 20).translate([x, y, z0]).trim_by_plane([0, 0, 1], z0)

# ── trucks and containers ───────────────────────────────────────────────────
def truck(P, x, y, z0, angle_deg, col, s=1.0):
    L = lambda v: v * s
    tw, cab_l, tr_l = L(6.6), L(5.6), L(15)
    wh_r, ch_h = L(1.5), L(1.2)
    parts = {'white': [], 'gold': [], col: []}
    for wy in (L(1.8), cab_l + L(3), cab_l + tr_l - L(2.5)):
        parts['white'].append(Manifold.cylinder(tw + L(.4), wh_r, wh_r, 20).rotate([0, 90, 0]).translate([-(tw + L(.4)) / 2, wy, z0 + wh_r * .7]))
    parts['white'].append(box(-tw/2, 0, z0 + wh_r * .9, tw/2, cab_l + tr_l, z0 + wh_r * .9 + ch_h))
    cz = z0 + wh_r * .9 + ch_h
    parts['white'].append(box(-tw/2, 0, cz, tw/2, cab_l - L(.6), cz + L(5.2)))
    parts['gold'].append(box(-tw/2 + L(.6), -L(.4), cz + L(2.6), tw/2 - L(.6), L(.2), cz + L(4.4)))
    parts[col].append(box(-tw/2 + L(.2), cab_l, cz, tw/2 - L(.2), cab_l + tr_l, cz + L(5.6)))
    total = cab_l + tr_l
    for c, ms in parts.items():
        m = union(ms).translate([0, -total / 2, 0]).rotate([0, 0, angle_deg]).translate([x, y, 0])
        P[c].append(m)

# ── the MBSC logo panel (shield, Arabic and English name, red rule) ─────────
def logo_panel(P, cx, cy, z0, angle_deg, pw, ph, logo_h, pt=4.0, legs=False, opening=None, caption=None):
    """Panel facing -Y before rotation. `opening` = (width, height) cut out at the
    bottom centre, turning the panel into a gateway."""
    full = np.array(Image.open(os.path.join(HERE, 'logo_full.png')).convert('L')) > 127
    redm = np.array(Image.open(os.path.join(HERE, 'logo_red.png')).convert('L')) > 127
    Q = new_parts()
    yb = pt / 2; yf = -pt / 2
    panel = box(-pw/2, yf, z0, pw/2, yb, z0 + ph)
    if opening:
        ow, oh = opening
        panel = panel - box(-ow/2, yf - 1, z0 - 1, ow/2, yb + 1, z0 + oh)
    Q['white'].append(panel)
    # buttresses behind so a thin panel prints rigid
    for bx in np.linspace(-pw/2 + 6, pw/2 - 6, 4 if pw > 60 else 2):
        if opening and abs(bx) < opening[0] / 2 + 2: continue
        Q['white'].append(Manifold.hull_points(np.array([[bx + d, yb - .01, z0] for d in (-1, 1)] + [[bx + d, yb + 4, z0] for d in (-1, 1)] +
                                                        [[bx + d, yb - .01, z0 + ph * .6] for d in (-1, 1)])))
    fr = 1.3
    frame = rect(-pw/2, z0, pw/2, z0 + ph) - rect(-pw/2 + fr, z0 + fr, pw/2 - fr, z0 + ph - fr)
    if opening:
        ow, oh = opening
        frame = (frame - rect(-ow/2 - fr, z0 - 1, ow/2 + fr, z0 + oh + fr)) + (rect(-ow/2 - fr, z0, ow/2 + fr, z0 + oh + fr) - rect(-ow/2, z0 - 1, ow/2, z0 + oh))
    Q['gold'].append(face_solid(frame, .7, yf))
    k = logo_h / full.shape[0]; lw = full.shape[1] * k
    x_left, z_top = -lw / 2, z0 + ph - (ph - (opening[1] if opening else 0)) / 2 + logo_h / 2 if opening else z0 + ph / 2 + logo_h / 2
    sc = 1010
    sh = np.zeros_like(full); sh[:, :sc] = full[:, :sc]
    tx = np.zeros_like(full); tx[:, sc:] = full[:, sc:]
    shield = morphology.remove_small_holes(sh, max_size=5000)
    sh_w = morphology.dilation(sh & ~redm, morphology.disk(3)) & shield
    sh_cs, wh_cs = ST._mask_rings(shield, x_left, z_top, k), ST._mask_rings(sh_w, x_left, z_top, k)
    Q['red'].append(face_solid(sh_cs - wh_cs, .9, yf))
    Q['white'].append(face_solid(wh_cs, 1.5, yf))
    Q['gold'].append(face_solid(ST._mask_rings(morphology.dilation(tx & ~redm, morphology.disk(2)), x_left, z_top, k), .9, yf))
    if (tx & redm).any():
        Q['red'].append(face_solid(ST._mask_rings(morphology.dilation(tx & redm, morphology.disk(2)), x_left, z_top, k), .9, yf))
    if caption:
        cap = 3.0
        while True:
            cs = tracked_cs(caption, cap, 0, z_top - logo_h - 2.2 - cap / 2, 'Bold', .1)
            b = cs.bounds()
            if b[2] - b[0] <= pw - 8 or cap <= 2.2: break
            cap -= .1
        Q['gold'].append(face_solid(cs, .8, yf))
    for c in COLOURS:
        for m in Q[c]:
            P[c].append(m.rotate([0, 0, angle_deg]).translate([cx, cy, 0]))

def fat(m, e=.02):
    """m grown a hair up and down: subtracting it never leaves a zero-thickness skin
    where two colours share a face exactly (that skin renders black and is not watertight)."""
    return union([m, m.translate([0, 0, e])])            # upward only: parts resting on a colour stay in contact

def resolve(P):
    over = union(P.pop('_over', []))
    lines = union(P.pop('_lines', [])) + over
    cut = union(P.pop('_cut', []))
    S = {c: union(P[c]) for c in COLOURS}
    S['white'] = S['white'] - cut
    S['red'] = S['red'] - fat(over)
    red_f = fat(S['red'])
    S['gold'] = S['gold'] - red_f
    gold_f = fat(S['gold'])
    S['green'] = S['green'] - red_f - gold_f - fat(lines)
    S['white'] = (S['white'] - fat(lines) + lines) - red_f - gold_f - fat(S['green'])
    return S

# ══ EDITION 1: THE RING ROAD ═══════════════════════════════════════════════
def ringroad():
    P = new_parts(); rng = np.random.default_rng(8)
    SZ, H = 190, 18
    plinth(P, SZ, H); z0 = H
    Rd, Rr, DH = 52, 74, 24            # dais radius, outer road radius, dais height
    # lawn across the top, minus the round dais and road
    lawn = rrect(SZ - 6, SZ - 6, 9) - ellipse(Rr + 1.5, Rr + 1.5, 220)
    lawn = lawn - rect(SZ / 2 - 66, -SZ / 2, SZ / 2, -SZ / 2 + 66)            # container port corner, white
    P['green'].append(slab(lawn, z0, 1.2))
    # the dais, with a gold band at its lip
    P['white'].append(slab(ellipse(Rd, Rd, 220), z0, DH))
    P['gold'].append(slab(ellipse(Rd + .01, Rd + .01, 220) - ellipse(Rd - 2.2, Rd - 2.2, 220), z0 + DH, .8))
    # terraced spiral road: flat steps rising from the port corner to the stadium gate
    a_start, a_end = math.radians(-40), math.radians(-40 + 320)
    NS = 80
    road = []
    for i in range(NS):
        a0 = a_start + (a_end - a_start) * i / NS; a1 = a_start + (a_end - a_start) * (i + 1) / NS + .002
        h = .6 + (DH - .6) * (i + 1) / NS
        ts = np.linspace(a0, a1, 6)
        wedge = CrossSection([np.array([[0, 0]] + [[(Rr + 5) * math.cos(t), (Rr + 5) * math.sin(t)] for t in ts])])
        sector = (ellipse(Rr, Rr, 360) - ellipse(Rd - .5, Rd - .5, 360)) ^ wedge
        road.append(slab(sector, z0, h))
        # gold centre dashes on every other step
        if i % 2 == 0:
            am = (a0 + a1) / 2; rm = (Rd + Rr) / 2
            dash = Manifold.cube([1.1, 2.6, .4]).translate([-.55, -1.3, 0]).rotate([0, 0, math.degrees(am)]).translate([rm * math.cos(am), rm * math.sin(am), z0 + h])
            P['gold'].append(dash)
        # a continuous gold kerb on the outer edge, so the climb reads as one rising gold line
        kerb = (ellipse(Rr, Rr, 360) - ellipse(Rr - 1.3, Rr - 1.3, 360)) ^ wedge
        P['gold'].append(slab(kerb, z0 + h - .01, 1.4))
    P['white'].append(union(road))
    # stadium on the dais
    info = stadium(P, .7, 0, 0, z0 + DH, rng)
    # trucks climbing the road
    for frac, col in [(.1, 'red'), (.36, 'white'), (.62, 'red'), (.86, 'gold')]:
        i = int(frac * NS); am = a_start + (a_end - a_start) * (i + .5) / NS
        h = .6 + (DH - .6) * (max(i - 2, 0) + 1) / NS
        rm = (Rd + Rr) / 2 + 1.5
        truck(P, rm * math.cos(am), rm * math.sin(am), z0 + h, math.degrees(am) + 180, col, .9)
    # palms ringing the outside of the road
    for k in range(14):
        a = 2 * math.pi * k / 14 + .1
        x, y = (Rr + 8) * math.cos(a), (Rr + 8) * math.sin(a)
        if x > 20 and y < -20: continue                         # leave the port corner clear
        if x < -40 and y < -40: continue                        # and the logo corner
        P['green'].append(palm(x, y, z0, 13 * rng.uniform(.85, 1.1), rng))
    for (x, y) in [(-80, 80), (-68, 84), (80, 80), (84, 66), (-84, 40)]:
        P['green'].append(palm(x, y, z0, 15 * rng.uniform(.9, 1.1), rng))
    # the container port (front-right corner) with floodlight masts
    cols = ['red', 'white', 'white', 'gold', 'white', 'red', 'white', 'white']
    k = 0
    for r in range(4):
        for c in range(3):
            x0 = SZ / 2 - 62 + c * 18; y0 = -SZ / 2 + 8 + r * 7
            n = 2 if (r + c) % 2 == 0 else 1
            for lv in range(n):
                P[cols[k % len(cols)]].append(box(x0, y0, z0 + lv * 4.4, x0 + 16, y0 + 5.6, z0 + (lv + 1) * 4.4)); k += 1
    for (x, y) in [(SZ / 2 - 66, -SZ / 2 + 38), (SZ / 2 - 8, -SZ / 2 + 38)]:
        P['white'].append(box(x - 1.1, y - 1.1, z0, x + 1.1, y + 1.1, z0 + 34))
        P['gold'].append(Manifold.hull_points(np.array([[x + dx * 1.1, y + dy * 1.1, z0 + 33.8] for dx in (-1, 1) for dy in (-1, 1)] +
                                                        [[x + dx * 3.4, y + dy * 1.4, z0 + 35.6] for dx in (-1, 1) for dy in (-1, 1)] +
                                                        [[x + dx * 3.4, y + dy * 1.4, z0 + 37.2] for dx in (-1, 1) for dy in (-1, 1)])))
    # the logo monolith in the front-left corner, turned to face the corner
    logo_panel(P, -70, -70, z0 + 1.2, -45, 50, 34, 16)
    return P

# ══ EDITION 2: BUILT ON IMPORTS ════════════════════════════════════════════
def imports():
    P = new_parts(); rng = np.random.default_rng(2034)
    SZ, H = 190, 18
    plinth(P, SZ, H); z0 = H
    cyp = 4                                      # pyramid centre, nudged back
    levels = [128, 108, 90, 74, 60]
    cw, cd, chh, gap = 12.4, 5.2, 5.4, .8
    stair_w = 20
    # ring road around the pyramid (bare white plinth), lawn strip outside it
    road_o = 162
    P['green'].append(slab(rrect(SZ - 6, SZ - 6, 9) - rrect(road_o, road_o, 10).translate([0, cyp]), z0, 1.2))
    # the containers: four interlocking levels, orientation alternating
    allc, ext = [], []
    for li, F in enumerate(levels):
        zb = z0 + li * chh
        lx, ly = (cw, cd) if li % 2 == 0 else (cd, cw)
        nx, ny = int((F + gap) // (lx + gap)), int((F + gap) // (ly + gap))
        wx, wy = nx * (lx + gap) - gap, ny * (ly + gap) - gap
        ext.append((wx, wy))
        ox, oy = -wx / 2, cyp - wy / 2
        for i in range(nx):
            for j in range(ny):
                x0, y0 = ox + i * (lx + gap), oy + j * (ly + gap)
                if abs(x0 + lx / 2) < stair_w / 2 + lx / 2 and y0 < cyp: continue      # the stair slot
                allc.append((x0, y0, zb, x0 + lx, y0 + ly, zb + chh))
    # 19.7% imported (red), the rest made in Saudi (white), scattered
    order = rng.permutation(len(allc))
    red_set = set(order[:int(round(len(allc) * .197))].tolist())
    for idx, c in enumerate(allc):
        P['red' if idx in red_set else 'white'].append(box(*c))
    # a hidden solid core in every level, so upper containers never bridge a gap
    for li, (wx, wy) in enumerate(ext):
        P['white'].append(box(-wx / 2 + 3, cyp - wy / 2 + 3, z0 + li * chh, wx / 2 - 3, cyp + wy / 2 - 3, z0 + (li + 1) * chh))
    top = z0 + len(levels) * chh
    dw, dd = ext[-1]
    # top deck: green lawn with a gold edge, the stadium on it
    P['green'].append(box(-dw / 2, cyp - dd / 2, top, dw / 2, cyp + dd / 2, top + 1.0))
    P['gold'].append(slab(rrect(dw, dd, 2).translate([0, cyp]) - rrect(dw - 2.4, dd - 2.4, 1.5).translate([0, cyp]), top + 1.0, .8))
    stadium(P, .47, 0, cyp + 1, top + 1.0, rng)
    # the grand stair up the front, between gold cheek walls
    run_start, run_end = cyp - ext[0][1] / 2 - 4, cyp - dd / 2 + 1
    nsteps = 22
    for i in range(nsteps):
        y0 = run_start + (run_end - run_start) * i / nsteps
        P['white'].append(box(-stair_w / 2, y0, z0, stair_w / 2, run_end, z0 + (top + 1.0 - z0) * (i + 1) / nsteps))
    for sx in (-1, 1):
        P['gold'].append(Manifold.hull_points(np.array(
            [[sx * (stair_w / 2 + dx), run_start, z0] for dx in (0, 1.4)] + [[sx * (stair_w / 2 + dx), run_end, z0] for dx in (0, 1.4)] +
            [[sx * (stair_w / 2 + dx), run_start, z0 + 2.4] for dx in (0, 1.4)] + [[sx * (stair_w / 2 + dx), run_end, top + 2.4] for dx in (0, 1.4)])))
    # the logo gateway on the lawn in front of the ring road, with the presentation's ratio under the logo
    gy = cyp - road_o / 2 - 5.5
    logo_panel(P, 0, gy, z0 + 1.2, 0, 64, 36, 14.5, pt=3.4, opening=(stair_w + 6, 12),
               caption='80.3% SAUDI  \u00b7  19.7% IMPORTED')
    # trucks circling the road
    rr = (road_o / 2 + ext[0][0] / 2 + 3) / 2
    for (x, y, ang, col) in [(rr, cyp - 22, 0, 'red'), (rr, cyp + 38, 180, 'white'), (-rr, cyp + 20, 180, 'white'),
                             (34, cyp + rr, 90, 'gold'), (-30, cyp + rr, 270, 'red'), (-46, cyp - rr, 90, 'gold')]:
        truck(P, x, y, z0, ang, col, .86)
    # palms along the lawn strip
    q = SZ / 2 - 7
    for (x, y) in [(-q, -q), (q, -q), (-q, q), (q, q), (-q, -30), (q, -30), (-q, 40), (q, 40), (-40, q), (40, q), (-62, -q), (62, -q)]:
        P['green'].append(palm(x, y, z0, 15 * rng.uniform(.88, 1.1), rng, s=.9))
    return P

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for label, fn in [('ringroad', ringroad), ('imports', imports)]:
        solids = resolve(fn())
        parts = []
        for col in COLOURS:
            v, f = ST.mesh_arrays(solids[col]); parts.append((col, (v, f)))
        zmin = min(p[1][0][:, 2].min() for p in parts)
        parts = [(c, (v - [0, 0, zmin], f)) for c, (v, f) in parts]
        for col, (v, f) in parts:
            ST.write_stl(os.path.join(out, 'stadium_%s_%d_%s.stl' % (label, COLOURS.index(col) + 1, col)), v, f)
        ST.write_3mf(os.path.join(out, 'stadium_%s_4colour.3mf' % label), parts, 'King Salman Stadium (%s)' % label)
        allv = np.vstack([p[1][0] for p in parts]); ext = allv.max(0) - allv.min(0)
        print(label, 'size mm: %.1f x %.1f x %.1f' % tuple(ext), ' | '.join('%s %d tris %s' % (c, len(f), solids[c].status().name) for c, (v, f) in parts))

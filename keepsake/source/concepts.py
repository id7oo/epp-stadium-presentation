"""Ten concept models of the keepsake, for choosing a direction. Each turns one
idea from the presentation into an object, built from the same parts as the
printable editions (stadium with scoreboard, trucks, containers, palms, the
MBSC logo panel, the lettering). Concepts are for looking at, not yet tuned
for printing.

Usage: python concepts.py OUT_DIR [name ...]
"""
import math, os, sys
import numpy as np
from manifold3d import Manifold, CrossSection
import statue as ST
import editions as E
from statue import ellipse, rrect, rect, slab, box, union, tracked_cs, COLOURS

def cyl(x, y, z, h, r, r2=None, n=64):
    return Manifold.cylinder(h, r, r if r2 is None else r2, n).translate([x, y, z])

def label(P, txt, x, y, z, cap=3.2, w='Bold', col='gold', track=.1):
    P[col].append(slab(tracked_cs(txt, cap, x, y, w, track), z, .7))

def containers_pile(P, x, y, z, nx, ny, levels, rng, red_frac=.4, cw=8, cd=3.4, ch=3.2):
    for lv in range(levels):
        for i in range(nx - lv):
            for j in range(ny):
                x0 = x + i * (cw + .5) + lv * (cw + .5) / 2; y0 = y + j * (cd + .5)
                P['red' if rng.random() < red_frac else 'white'].append(box(x0, y0, z + lv * ch, x0 + cw, y0 + cd, z + (lv + 1) * ch))

def base(P, size=180, H=16):
    return E.plinth(P, size, H)

# 1 ── THE COIN SLICE ─────────────────────────────────────────────────────────
def coin_slice():
    P = E.new_parts(); rng = np.random.default_rng(1); z0 = base(P)
    R, T = 78, 9
    lost = 2 * math.pi * .197
    a0 = math.radians(-60); a1 = a0 + lost
    def wedge(r, aa, bb, cx=0, cy=0):
        ts = np.linspace(aa, bb, 40)
        return CrossSection([np.array([[cx, cy]] + [[cx + r * math.cos(t), cy + r * math.sin(t)] for t in ts])])
    keep = wedge(R, a1, a0 + 2 * math.pi)
    coin = slab(keep, z0, T)
    rim = slab(keep - ellipse(R - 4, R - 4, 160), z0 + T, 1.6)
    P['gold'] += [coin, rim]
    P['green'].append(slab(keep ^ ellipse(R - 4, R - 4, 160), z0 + T, 1.0))
    # the slice, pulled out and lifted, red, carrying containers and a truck
    am = (a0 + a1) / 2; dx, dy = 22 * math.cos(am), 22 * math.sin(am)
    sl = wedge(R, a0, a1).translate([dx, dy])
    P['red'].append(slab(sl, z0, T + 5))
    for k in range(5):
        rr = 30 + k * 9
        x, y = dx + rr * math.cos(am), dy + rr * math.sin(am)
        P['white' if k % 2 else 'gold'].append(box(x - 4, y - 1.7, z0 + T + 5, x + 4, y + 1.7, z0 + T + 8.2).rotate([0, 0, 0]))
    E.truck(P, dx + 58 * math.cos(am) - 6, dy + 58 * math.sin(am) + 4, z0 + T + 5, math.degrees(am), 'red', .7)
    label(P, '19.7%  IMPORTED', dx + 50 * math.cos(am) + 14, dy + 50 * math.sin(am) - 22, z0, 3.4)
    label(P, '80.3%  STAYS IN SAUDI ARABIA', -10, 70, z0 + T + 1, 3.0)
    E.stadium(P, .66, -6, 4, z0 + T + 1, rng)
    for a in np.linspace(a1 + .3, a0 + 2 * math.pi - .3, 9):
        P['green'].append(E.palm((R - 9) * math.cos(a), (R - 9) * math.sin(a), z0 + T + 1, 11, rng, .8))
    E.logo_panel(P, -62, 68, z0, 0, 44, 30, 13)
    return P

# 2 ── DEADLINE HOURGLASS ─────────────────────────────────────────────────────
def hourglass():
    P = E.new_parts(); rng = np.random.default_rng(2); z0 = base(P)
    R, Hh = 62, 112
    P['gold'].append(cyl(0, 0, z0, 4, R + 6))
    P['gold'].append(cyl(0, 0, z0 + Hh, 4, R + 6) - cyl(0, 0, z0 + Hh - 1, 6, R - 4))   # open ring lid
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        P['gold'].append(cyl((R + 2) * math.cos(a), (R + 2) * math.sin(a), z0 + 4, Hh - 4, 2.4))
    # glass outline as two faint white rings at the neck
    P['white'].append(cyl(0, 0, z0 + Hh / 2 - 1, 2, 7) - cyl(0, 0, z0 + Hh / 2 - 2, 4, 5.5))
    # upper chamber: an inverted cone of containers draining down
    for lv in range(9):
        zz = z0 + Hh - 4 - (lv + 1) * 4
        rr = 52 - lv * 5.2
        n = max(4, int(2 * math.pi * rr / 9))
        for i in range(n):
            a = 2 * math.pi * i / n + lv * .3
            x, y = rr * .8 * math.cos(a), rr * .8 * math.sin(a)
            m = box(-3.6, -1.5, 0, 3.6, 1.5, 3.4).rotate([0, 0, math.degrees(a) + 90]).translate([x, y, zz])
            P['red' if rng.random() < .3 else 'white'].append(m)
        P['white'].append(cyl(0, 0, zz, 4, rr * .8 - 3))
    # the stream through the neck
    for k in range(10):
        P['red' if k % 3 == 0 else 'white'].append(box(-1.2, -.8, z0 + Hh / 2 - 10 + k * 2.2, 1.2, .8, z0 + Hh / 2 - 8.6 + k * 2.2).rotate([0, 0, k * 37]))
    # lower chamber: the stadium the containers became
    E.stadium(P, .74, 0, 0, z0 + 4, rng)
    label(P, '2034', 0, -R - 1, z0 + Hh + 4, 7, 'Black')
    E.logo_panel(P, 0, -82, z0, 0, 50, 24, 11)
    for (x, y) in [(-78, -78), (78, -78), (-78, 78), (78, 78)]:
        P['green'].append(E.palm(x, y, z0, 14, rng, .9))
    return P

# 3 ── IMPORT SKYLINE ─────────────────────────────────────────────────────────
def skyline():
    P = E.new_parts(); rng = np.random.default_rng(3); z0 = base(P)
    data = [('METALS', 54.5), ('ELECTRICAL', 50.3), ('WOOD', 44.7), ('CHEMICALS', 43.2), ('PLASTICS', 32.6), ('GLASS', 11.8), ('FUELS', 8.0), ('FEEDSTOCK', 7.3)]
    Ht, w, gap = 80, 17, 3.5
    x0 = -(len(data) * (w + gap) - gap) / 2
    for i, (name, share) in enumerate(data):
        x = x0 + i * (w + gap); y = 40
        hr = Ht * share / 100
        P['white'].append(box(x, y, z0, x + w, y + w, z0 + Ht - hr))
        P['red'].append(box(x, y, z0 + Ht - hr, x + w, y + w, z0 + Ht))
        # window bands
        for zz in np.arange(z0 + 4, z0 + Ht - hr - 2, 5):
            P['gold'].append(box(x + 2, y - .4, zz, x + w - 2, y + .2, zz + 1.2))
        P['gold'].append(E.face_solid(tracked_cs('%.1f%%' % share, 3.2, x + w / 2, z0 + Ht - hr / 2, 'Black', .02), .7, y))
        label(P, name, x + w / 2, y - 6, z0, 2.4, 'Bold', 'gold', .05)
    E.stadium(P, .62, 0, -22, z0, rng)
    for k, (x, col) in enumerate([(-66, 'red'), (62, 'red'), (-50, 'white')]):
        E.truck(P, x, -4 - k * 8, z0, 0, col, .8)
    E.logo_panel(P, 64, -64, z0, -20, 40, 26, 11)
    for (x, y) in [(-78, -78), (-60, -80)]:
        P['green'].append(E.palm(x, y, z0, 13, rng, .9))
    return P

# 4 ── THE BALANCE ────────────────────────────────────────────────────────────
def balance():
    P = E.new_parts(); rng = np.random.default_rng(4); z0 = base(P)
    Hp, L_ = 70, 68
    tilt = math.radians(12)
    P['gold'].append(cyl(0, 0, z0, 4, 16))
    P['gold'].append(cyl(0, 0, z0 + 4, Hp, 3.4, 2.6))
    pz = z0 + 4 + Hp
    P['gold'].append(Manifold.sphere(4.5, 32).translate([0, 0, pz]))
    # the beam, tipped toward the heavier side (the stadium)
    beam = box(-L_, -2, -1.6, L_, 2, 1.6).rotate([0, math.degrees(tilt), 0]).translate([0, 0, pz])
    P['gold'].append(beam)
    ends = [(-L_ * math.cos(tilt), pz + L_ * math.sin(tilt)), (L_ * math.cos(tilt), pz - L_ * math.sin(tilt))]
    # heavy side (right, lower): the stadium on its pan
    (xl, zl), (xr, zr) = ends
    pr_z = zr - 34
    P['gold'].append(cyl(xr, 0, pr_z - 3, 3, 40))
    for k in range(3):
        a = 2 * math.pi * k / 3
        P['gold'].append(Manifold.hull_points(np.array([[xr, 0, zr], [xr + .8, 0, zr], [xr, .8, zr]] +
                                                        [[xr + 36 * math.cos(a) + dx, 36 * math.sin(a) + dy, pr_z] for dx in (0, .8) for dy in (0, .8)])))
    E.stadium(P, .52, xr, 0, pr_z, rng)
    # light side (left, higher): the red imports
    pl_z = zl - 26
    P['gold'].append(cyl(xl, 0, pl_z - 3, 3, 26))
    for k in range(3):
        a = 2 * math.pi * k / 3
        P['gold'].append(Manifold.hull_points(np.array([[xl, 0, zl], [xl + .8, 0, zl], [xl, .8, zl]] +
                                                        [[xl + 23 * math.cos(a) + dx, 23 * math.sin(a) + dy, pl_z] for dx in (0, .8) for dy in (0, .8)])))
    for lv in range(3):
        for i in range(3 - lv):
            for j in range(4):
                P['red'].append(box(xl - 13 + i * 9 + lv * 4.5, -9 + j * 4.6, pl_z + lv * 3.4, xl - 5 + i * 9 + lv * 4.5, -5.4 + j * 4.6, pl_z + (lv + 1) * 3.4))
    label(P, '80.3% STAYS', xr, -58, z0, 4, 'Black')
    label(P, '19.7% LEAKS', xl, -58, z0, 4, 'Black', 'red')
    E.truck(P, -20, -76, z0, 90, 'red', .8)
    E.logo_panel(P, 0, 74, z0, 180, 70, 30, 14)
    return P

# 5 ── MULTIPLIER RIPPLES ─────────────────────────────────────────────────────
def ripples():
    P = E.new_parts(); rng = np.random.default_rng(5); z0 = base(P, 190)
    rounds = [600, 283.5, 134, 63.3, 29.9]
    for k, v in enumerate(rounds):
        r = 54 + k * 9
        h = 2 + 22 * v / 600
        ring = ellipse(r + 2.6, r + 2.6, 200) - ellipse(r, r, 200)
        # each round loses ~52.75% to leakage: a red arc proportional to it
        lost = 2 * math.pi * .25
        a0 = math.radians(200 + k * 14)
        ts = np.linspace(a0, a0 + lost, 30)
        wedge = CrossSection([np.array([[0, 0]] + [[(r + 10) * math.cos(t), (r + 10) * math.sin(t)] for t in ts])])
        P['white'].append(slab(ring - wedge, z0, h))
        P['red'].append(slab(ring ^ wedge, z0, h * .6))
        label(P, 'R%d' % (k + 1), (r + 1.3) * math.cos(math.radians(-90)), (r + 1.3) * math.sin(math.radians(-90)) - 0, z0 + h, 2.4, 'Black')
    P['green'].append(slab(rrect(184, 184, 9) - ellipse(54 + 4 * 9 + 4, 54 + 4 * 9 + 4, 200), z0, 1.2))
    E.stadium(P, .82, 0, 0, z0, rng)
    P['gold'].append(slab(ellipse(53, 53, 200) - ellipse(51, 51, 200), z0, 1.2))
    label(P, 'EACH ROUND SMALLER  ·  r = 0.4725', 0, -88, z0, 2.6, 'Bold')
    for (x, y) in [(-84, -84), (84, -84), (-84, 84), (84, 84)]:
        P['green'].append(E.palm(x, y, z0, 14, rng, .9))
    E.logo_panel(P, 72, 72, z0 + 1.2, -135, 30, 22, 9)
    return P

# 6 ── THE LEAK FUNNEL ────────────────────────────────────────────────────────
def funnel():
    P = E.new_parts(); rng = np.random.default_rng(6); z0 = base(P)
    E.stadium(P, .7, -10, 6, z0, rng)
    zt = z0 + 92
    outer = cyl(-10, 6, zt - 40, 40, 6, 46); inner = cyl(-10, 6, zt - 38, 40.2, 4, 44)
    P['gold'].append(outer - inner)
    P['gold'].append(cyl(-10, 6, zt - 56, 17, 5.5) - cyl(-10, 6, zt - 57, 19, 3.6))
    # three gold legs from the plinth up to the funnel lip
    for k in range(3):
        a = math.radians(60 + k * 120)
        P['gold'].append(Manifold.hull_points(np.array([[-10 + 60 * math.cos(a) + d, 6 + 60 * math.sin(a), z0] for d in (0, 2.4)] +
                                                        [[-10 + 60 * math.cos(a), 6 + 60 * math.sin(a) + d, z0] for d in (0, 2.4)] +
                                                        [[-10 + 45 * math.cos(a) + d, 6 + 45 * math.sin(a), zt - 2] for d in (0, 2.4)] +
                                                        [[-10 + 45 * math.cos(a), 6 + 45 * math.sin(a) + d, zt - 2] for d in (0, 2.4)])))
    # red leak pipe out of the side, down to the port
    pts = [(-10 + 30, 6 - 10, zt - 22), (40, -30, zt - 30), (58, -48, z0 + 30), (62, -56, z0 + 12)]
    for (a, b) in zip(pts, pts[1:]):
        P['red'].append(Manifold.hull_points(np.array([[p[0] + dx, p[1] + dy, p[2] + dz] for p in (a, b) for dx in (-3, 3) for dy in (-3, 3) for dz in (-3, 3)])))
    containers_pile(P, 46, -80, z0, 4, 4, 2, rng, .7)
    E.truck(P, 30, -60, z0, 90, 'red', .8); E.truck(P, 78, -20, z0, 0, 'red', .8)
    label(P, 'SAR 421m LEAKS', 60, -86, z0, 2.8, 'Black', 'red')
    E.logo_panel(P, -62, -70, z0, 30, 44, 28, 12)
    for (x, y) in [(-80, 80), (80, 80), (-80, 40)]:
        P['green'].append(E.palm(x, y, z0, 14, rng, .9))
    return P

# 7 ── EXPLODED STADIUM ───────────────────────────────────────────────────────
def exploded():
    P = E.new_parts(); rng = np.random.default_rng(7); z0 = base(P)
    s = .9
    A, B = 58 * s, 51 * s
    gap = 14
    P['gold'].append(cyl(0, 0, z0, 118, 2.2))
    layers = []
    # pitch
    P['green'].append(slab(ellipse(28 * s, 19 * s), z0 + 6, 2))
    P['white'].append(slab(ellipse(28 * s + 2, 19 * s + 2) - ellipse(28 * s, 19 * s), z0 + 6, 2))
    # lower tier, upper tier as stepped rings
    for t, (ai, ao, hh) in enumerate([(28, 42, 8), (42, 54.5, 10)]):
        zb = z0 + 6 + gap * (t + 1)
        for i in range(6):
            f = i / 5
            a = (ai + (ao - ai) * f) * s; b = a * (51 / 58)
            P['white'].append(slab(ellipse(ao * s, ao * s * 51 / 58) - ellipse(a, b), zb, 1.2 + hh * f))
    # facade with ribs
    zf = z0 + 6 + gap * 3 + 6
    P['white'].append(slab(ellipse(A, B) - ellipse(A - 2.2, B - 2.2), zf, 22))
    for k in range(32):
        a = 2 * math.pi * k / 32
        for sg in (-1, 1):
            p0 = [A * math.cos(a), B * math.sin(a), zf + 1]; a2 = a + sg * .3
            p1 = [A * math.cos(a2), B * math.sin(a2), zf + 21]
            P['white'].append(Manifold.hull_points(np.array([[p[0] * f, p[1] * f, p[2] + dz] for p in (p0, p1) for f in (.99, 1.02) for dz in (0, 1.2)])))
    # roof ring and scoreboard
    zr = zf + 22 + gap
    P['gold'].append(slab(ellipse(A + 1.5, B + 1.5) - ellipse(A - 6, B - 6), zr, 3))
    zs = zr + gap
    P['white'].append(box(-9, -9, zs, 9, 9, zs + 9))
    for k in range(4):
        P['red'].append(box(-7, -9.6, zs + 1.5, 7, -8.9, zs + 7.5).rotate([0, 0, 90 * k]))
    # leader labels on the plinth
    for txt, y in [('SCOREBOARD', 54), ('ROOF RING', 40), ('DIAGRID FACADE', 26), ('UPPER TIER', 12), ('LOWER TIER', -2), ('PITCH', -16)]:
        label(P, txt, 70, y, z0, 2.6, 'Bold')
    E.logo_panel(P, -62, 64, z0, 0, 46, 30, 13)
    E.truck(P, -66, -40, z0, 0, 'red', .8)
    return P

# 8 ── TWO BANKS ──────────────────────────────────────────────────────────────
def two_banks():
    P = E.new_parts(); rng = np.random.default_rng(8)
    size, H = 180, 16
    E.plinth(P, size, H); z0 = H
    # diagonal channel cut through the plinth top
    ch = CrossSection([np.array([[-size, size - 26], [-size, size + 26], [size, -size + 26], [size, -size - 26]]) * .5]).translate([0, 0])
    chan = slab(CrossSection([np.array([[-95, -70], [-70, -95], [95, 70], [70, 95]])]), z0 - 7, 20)
    P.setdefault('_cut', []).append(chan)
    # port bank (front-right) and stadium bank (back-left)
    containers_pile(P, 20, -82, z0, 6, 5, 2, rng, .55)
    E.truck(P, 64, -30, z0, 0, 'red', .8)
    E.stadium(P, .64, -32, 32, z0, rng)
    P['green'].append(slab(CrossSection([np.array([[-88, -60], [60, 88], [-88, 88]])]) - ellipse(42, 37).translate([-32, 32]), z0, 1.2))
    for (x, y) in [(-80, -40), (-82, 0), (-40, 80), (0, 82), (-80, 80)]:
        P['green'].append(E.palm(x, y, z0, 13, rng, .85))
    # the gold EPP bridge with the academy pavilion at its crown
    # a bold arch: deck plus two gold arch ribs, spanning the channel corner to corner
    for t in np.linspace(0, 1, 40):
        x = -30 + 66 * t; y = -30 + 66 * t
        hz = 22 * math.sin(math.pi * t)
        P['gold'].append(box(-11, -2.2, 0, 11, 2.2, 2.6).rotate([0, 0, -45]).translate([x, y, z0 + hz]))
        for sd in (-1, 1):
            ox, oy = sd * 9.2 * math.cos(math.radians(-45)), sd * 9.2 * math.sin(math.radians(-45))
            P['gold'].append(box(-1.2, -1.6, 0, 1.2, 1.6, 2.4).rotate([0, 0, -45]).translate([x + ox, y + oy, z0 + hz + 6 + 6 * math.sin(math.pi * t)]))
    # the academy pavilion at the crown
    P['white'].append(box(-8, -8, 0, 8, 8, 10).rotate([0, 0, 45]).translate([3, 3, z0 + 24]))
    P['gold'].append(Manifold.hull_points(np.array([[3 + 12 * math.cos(a), 3 + 12 * math.sin(a), z0 + 34] for a in np.linspace(0, 2 * math.pi, 4, endpoint=False) + math.pi / 4] + [[3, 3, z0 + 42]])))
    E.truck(P, -14, -14, z0 + 15, -45, 'white', .7); E.truck(P, 22, 22, z0 + 15, 135, 'red', .7)
    label(P, 'EPP  ·  SAR 84m', 38, 6, z0, 3.0, 'Black')
    label(P, 'ACADEMY', 7, -10, z0 + 0, 2.4, 'Bold')
    E.logo_panel(P, -64, 70, z0 + 1.2, 0, 40, 26, 11)
    return P

# 9 ── FLOATING ISLAND ────────────────────────────────────────────────────────
def floating():
    P = E.new_parts(); rng = np.random.default_rng(9); z0 = base(P)
    Hc = 46
    for k in range(23):
        P['gold'].append(box(-7, -7, 0, 7, 7, 2.1).rotate([0, 0, k * 8]).translate([0, 0, z0 + k * 2]))
    zi = z0 + Hc
    # the island: a rock cone underneath, lawn on top
    P['white'].append(cyl(0, 0, zi - 34, 34, 6, 62, 18))
    P['green'].append(cyl(0, 0, zi, 1.6, 62, 62, 18))
    E.stadium(P, .78, 0, 0, zi + 1.6, rng)
    for a in np.linspace(0, 2 * math.pi, 10, endpoint=False):
        P['green'].append(E.palm(56 * math.cos(a), 56 * math.sin(a), zi + 1.6, 9, rng, .7))
    # the port on the ground below
    containers_pile(P, -80, -82, z0, 5, 3, 2, rng, .5)
    containers_pile(P, 34, -82, z0, 5, 3, 2, rng, .5)
    E.truck(P, -10, -70, z0, 90, 'red', .8); E.truck(P, 62, 62, z0, 0, 'white', .8)
    E.logo_panel(P, -60, 66, z0, 20, 46, 30, 13)
    return P

# 10 ── COIN STACKS ───────────────────────────────────────────────────────────
def coin_stacks():
    P = E.new_parts(); rng = np.random.default_rng(10); z0 = base(P)
    chain = [('SAR 4.5bn', 'scenario', 4500, 'gold'), ('SAR 2,143m', 'purchases', 2143, 'white'),
             ('SAR 1,721m', 'stays', 1721, 'green'), ('SAR 421m', 'leaks', 421, 'red'), ('SAR 84m', 'EP credit', 84, 'gold')]
    Hmax = 86
    for k, (v, sub, amt, col) in enumerate(chain):
        a = math.radians(160 - k * 35)
        x, y = 66 * math.cos(a), 66 * math.sin(a) - 8
        hgt = max(3, Hmax * (amt / 4500) ** .6)
        n = int(hgt / 2.4)
        for i in range(n):
            c = cyl(x, y, z0 + i * 2.4, 2.2, 13, 13, 48)
            P[col].append(c)
            P[col].append(cyl(x, y, z0 + i * 2.4 + 2.0, .4, 12.4, 12.4, 48))
        label(P, v, x, y - 22, z0, 2.8, 'Black', 'gold' if col != 'gold' else 'red')
        label(P, sub.upper(), x, y - 27, z0, 2.0, 'Bold')
    E.stadium(P, .62, 0, -14, z0, rng)
    E.truck(P, 40, -60, z0, 60, 'red', .8)
    E.logo_panel(P, -60, -70, z0, 25, 40, 26, 11)
    for (x, y) in [(-80, 82), (80, 82)]:
        P['green'].append(E.palm(x, y, z0, 14, rng, .9))
    return P

CONCEPTS = [('01_coin_slice', coin_slice), ('02_hourglass', hourglass), ('03_skyline', skyline), ('04_balance', balance),
            ('05_ripples', ripples), ('06_funnel', funnel), ('07_exploded', exploded), ('08_two_banks', two_banks),
            ('09_floating', floating), ('10_coin_stacks', coin_stacks)]

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    only = set(sys.argv[2:])
    for name, fn in CONCEPTS:
        if only and name not in only: continue
        try:
            S = E.resolve(fn())
        except Exception as e:
            print(name, 'FAILED', repr(e)); continue
        parts = [(c, ST.mesh_arrays(S[c])) for c in COLOURS]
        zmin = min(v[:, 2].min() for _, (v, f) in parts if len(v))
        for c, (v, f) in parts:
            ST.write_stl(os.path.join(out, 'stadium_%s_%d_%s.stl' % (name, COLOURS.index(c) + 1, c)), v - [0, 0, zmin], f)
        allv = np.vstack([v for _, (v, f) in parts if len(v)])
        print(name, 'ok %.0f x %.0f x %.0f mm' % tuple(allv.max(0) - allv.min(0)))

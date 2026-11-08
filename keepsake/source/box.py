"""Gift box for the light edition, sized for the model printed at 1.469x
(base 173.4 x 101.4 mm, 101.5 mm tall with the logo plaque in its slot).

Two parts on one plate, both in the box colour (green by default):
  * a tray: a 5 mm base with a low lip; the model sits in a fitted recess;
  * a lid that lifts straight off. It prints upside down, so the official
    MBSC logo, the gold frame and the lettering are inlaid in the first
    three layers of its top face; the walls carry debossed lettering in the
    box colour (no colour changes).

Usage: python box.py OUT_DIR
"""
import math, os, sys
import numpy as np
from manifold3d import Manifold
from PIL import Image
from scipy import ndimage
from skimage import morphology
import statue as ST
import editions as ED
import light as LT
from statue import rrect, rect, slab, box, union, tracked_cs, COLOURS, HERE

BODY = 'green'                          # box colour: AMS slot 2. Use 'white' for a white box.
DR = 'DR. R. E. GEORGE'                 # the instructor named in the course assessment guidelines
SCALE = 1.46903513                      # the scale the light edition was printed at

# the printed model
M_W, M_D = 118.0 * SCALE, 69.0 * SCALE                          # base footprint
M_H = (LT.H0 - LT.SLOT_DEPTH + LT.PH) * SCALE                   # top of the standing plaque
M_R = 7.0 * SCALE                                               # base corner radius

# the box (mm)
CL = 1.0                                 # clearance around the model in the recess
REC_W, REC_D, REC_R = M_W + 2 * CL, M_D + 2 * CL, M_R + CL
LIP_T, LIP_H = 3.0, 5.0                  # lip wall and height (holds the model, guides the lid)
FLOOR = 5.0                              # tray base thickness
FIT = 0.3                                # lid-to-lip clearance per side
WALL, TOP = 2.4, 2.6                     # lid wall and top thickness
HEAD = 2.4                               # air above the plaque
LIP_W, LIP_D, LIP_R = REC_W + 2 * LIP_T, REC_D + 2 * LIP_T, REC_R + LIP_T
LI_W, LI_D, LI_R = LIP_W + 2 * FIT, LIP_D + 2 * FIT, LIP_R + FIT          # lid inside
LO_W, LO_D, LO_R = LI_W + 2 * WALL, LI_D + 2 * WALL, LI_R + WALL          # lid outside
T_W, T_D, T_R = LO_W + 4, LO_D + 4, LO_R + 2                               # tray flange: a 2 mm reveal
LID_H = M_H + HEAD + TOP                 # the lid stands on the flange
INLAY = 0.6

def chamfered(w, d, r, h, c):
    """Rounded-rectangle block with a 45-degree chamfer of size c on its top edge."""
    body = rrect(w, d, r).extrude(h - c)
    cap = rrect(w, d, r).extrude(c, scale_top=((w - 2 * c) / w, (d - 2 * c) / d)).translate([0, 0, h - c])
    return body + cap

def tray():
    P = ED.new_parts()
    P[BODY].append(chamfered(T_W, T_D, T_R, FLOOR, 1.0))
    ring = rrect(LIP_W, LIP_D, LIP_R) - rrect(REC_W, REC_D, REC_R)
    P[BODY].append(slab(ring, FLOOR - .01, LIP_H + .01))
    # two finger scoops in the lip, left and right, to lift the model out
    for sx in (-1, 1):
        cut = Manifold.cylinder(30, 9, 9, 48).rotate([0, 90, 0]).translate([sx * (REC_W / 2 + LIP_T / 2) - 15, 0, FLOOR + LIP_H + 5])
        P['_cut'] = P.get('_cut', []) + [cut]
    # debossed line on the flange front
    cs = tracked_cs('GROUP 8  ·  MBSC EMBA  ·  ECN 511  ·  2026', 2.4, 0, FLOOR / 2, 'SemiBold', .2)
    P['_cut'].append(ED.face_solid(cs, 0, -T_D / 2, embed=.5))
    S_ = {c: union(P[c]) for c in COLOURS}
    S_[BODY] = S_[BODY] - union(P['_cut'])
    return S_

def _logo_layers(width, x_left, y_top):
    """The official logo as top-face inlays: red shield, white details and outline, gold name."""
    red = np.array(Image.open(os.path.join(HERE, 'mbsc_official_red.png')).convert('L')) > 127
    txt = np.array(Image.open(os.path.join(HERE, 'mbsc_official_text.png')).convert('L')) > 127
    wht = np.array(Image.open(os.path.join(HERE, 'mbsc_official_shieldwhite.png')).convert('L')) > 127
    cols = np.arange(red.shape[1])[None, :]
    rule = red & (cols >= 2100)
    top_of_rule = np.where(rule.any(1))[0].min()
    shield_red = red & (cols < 2100)
    name = txt.copy(); name[top_of_rule - 20:] = False
    rows = np.where((shield_red | wht | name).any(1))[0]
    r0, r1 = rows.min(), rows.max() + 1
    shield_red, wht, name = shield_red[r0:r1], wht[r0:r1], name[r0:r1]
    k = width / red.shape[1]
    px = lambda mm: max(1, int(round(mm / k)))
    white = morphology.dilation(wht, morphology.disk(px(.08)))
    redm = shield_red & ~white
    gold = morphology.dilation(name, morphology.disk(px(.1)))
    height = (r1 - r0) * k
    return {c: ST._mask_rings(m, x_left, y_top, k) for c, m in (('red', redm), ('white', white), ('gold', gold))}, height

def lid():
    """Built upright (top face up), then turned over for printing."""
    P = ED.new_parts()
    shell = chamfered(LO_W, LO_D, LO_R, LID_H, 1.2) - rrect(LI_W, LI_D, LI_R).extrude(LID_H - TOP).translate([0, 0, -.01])
    P[BODY].append(shell)
    zi = LID_H - INLAY
    inl = lambda cs: slab(cs, zi, INLAY + .01)
    fw = LO_W - 2 * 1.2                 # the flat top inside the chamfer
    fd = LO_D - 2 * 1.2
    # gold frame
    m = 6.0
    P['gold'].append(inl(rrect(fw - 2 * m, fd - 2 * m, 8) - rrect(fw - 2 * m - 2.4, fd - 2 * m - 2.4, 6.8)))
    # the logo with the college name, centred on the lid, and nothing else
    LW = 150.0
    _, lh = _logo_layers(LW, 0, 0)
    rings, lh = _logo_layers(LW, -LW / 2, lh / 2)
    for c, cs in rings.items():
        P[c].append(inl(cs))
    # debossed walls, in the box colour: the course on the front, the group on the back, the city on the sides
    cuts = []
    for txt, cap, wt, tr, zc in [('KING SALMAN STADIUM', 8.0, 'Black', .06, 60.0),
                                  ('ECN 511  \u00b7  ECONOMICS FOR MANAGERS  \u00b7  MBSC EMBA', 2.9, 'SemiBold', .2, 48.0)]:
        cuts.append(ED.face_solid(tracked_cs(txt, cap, 0, zc, wt, tr), 0, -LO_D / 2, embed=.6))
    team = [('GROUP 8', 9.0, 'Black', .3, 60.0),
            ('MBSC EMBA  \u00b7  2026', 4.0, 'SemiBold', .3, 47.0)]
    for txt, cap, wt, tr, zc in team:
        cuts.append(ED.face_solid(tracked_cs(txt, cap, 0, zc, wt, tr), 0, -LO_D / 2, embed=.6).rotate([0, 0, 180]))
    city = tracked_cs('RIYADH  \u00b7  2034', 6.0, 0, 55.0, 'Black', .3)
    for sx in (-1, 1):
        cuts.append(ED.face_solid(city, 0, -LO_W / 2, embed=.6).rotate([0, 0, -90 * sx]))
    S_ = {c: union(P[c]) for c in COLOURS}
    over = union([S_[c] for c in COLOURS if c != BODY])
    S_[BODY] = S_[BODY] - union(cuts) - over
    return S_

def flipped(sol):
    out = {c: m.rotate([180, 0, 0]) for c, m in sol.items()}
    zmin = union(list(out.values())).bounding_box()[2]
    return {c: m.translate([0, 0, -zmin]) for c, m in out.items()}

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    Tr, Ld = tray(), lid()
    Lp = flipped(Ld)
    # assembled previews: closed, and open with the model in the tray
    for tag, sol in (('box_tray', Tr), ('box_lid', Ld)):
        for c in COLOURS:
            v, f = ST.mesh_arrays(sol[c]); ST.write_stl(os.path.join(out, 'stadium_%s_%d_%s.stl' % (tag, COLOURS.index(c) + 1, c)), v, f)
        bb = union(list(sol.values())).bounding_box()
        print(tag, 'size %.1f x %.1f x %.1f mm' % (bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2]), ' '.join('%s %.1fcm3' % (c, sol[c].volume() / 1000) for c in COLOURS))
    LT.write_3mf_plate(os.path.join(out, 'stadium_light_giftbox.3mf'),
                       [('Box tray', LT.parts_of(Tr), (128, 64)), ('Box lid', LT.parts_of(Lp), (128, 190))],
                       'King Salman Stadium gift box')
    print('model %.1f x %.1f x %.1f | recess %.1f x %.1f | lid outer %.1f x %.1f x %.1f | tray %.1f x %.1f' % (M_W, M_D, M_H, REC_W, REC_D, LO_W, LO_D, LID_H, T_W, T_D))

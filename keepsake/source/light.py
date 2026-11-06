"""Light edition of the keepsake: a faster, smaller print (target well under 20 h on
an X1C with the AMS) that keeps what matters most: the stadium, the trucks and
container yard, and a large full-colour MBSC logo.

Why it is fast: on a multi-colour print the time goes into filament swaps
(about 1.5-2 min each), and a swap is needed on every layer that holds more
than one colour. So every colour here lives in a short band of layers:

  * the MBSC logo is a separate flat plaque, printed face up, with the shield,
    calligraphy, name and frame inlaid in its top 0.6 mm (3 layers). It slots
    upright into a rail behind the stadium (glue optional);
  * the stadium is cut in half (the back half stands, the pitch is whole), all
    white, with the gold roof ring on top where nothing else is printed;
  * lawn, pitch, lettering and road dashes share the first 0.6 mm above the base;
  * containers and the truck's container share one red band, the upper tier of
    containers one gold band;
  * the scoreboard's red screens are flush inlays, so they add no overhangs.

Two objects on one plate: the base (118 x 66 mm) and the logo plaque (100 x 62 mm).

Usage: python light.py OUT_DIR
"""
import math, os, sys, json, uuid, zipfile
import numpy as np
from manifold3d import Manifold
from skimage import morphology
from PIL import Image
import statue as ST
import editions as ED
from statue import ellipse, rrect, rect, slab, box, union, tracked_cs, COLOURS, HERE

S = 0.62                                   # stadium scale relative to the large model
W, D = 118.0, 66.0                         # base footprint: compact, the half stadium fills it
H0 = 6.0                                   # base thickness; the scene starts at z = H0
CY = -11.0                                 # the cut line: the stadium's long axis
SX = -W / 2 + 3 + 58 * S + 2 * S           # stadium centre (x), left part of the base
PT, PH, PW = 3.2, 62.0, 100.0              # plaque thickness, height, width
SLOT_DEPTH = 3.5                           # how far the slot goes into the base
RAIL_H, RAIL_Y0, RAIL_Y1 = 8.0, 23.0, 30.0
SLOT_Y = (RAIL_Y0 + RAIL_Y1) / 2
SLOT_W, SLOT_CLEAR = PT + 0.3, 0.4         # slot width, and extra length along x
INSERT = SLOT_DEPTH + RAIL_H               # plaque length hidden in the rail
INLAY = 0.6                                # colour depth on the plaque face

L = lambda v: v * S

# ══ the base ═════════════════════════════════════════════════════════════════
def base():
    P = ED.new_parts()
    z0 = H0
    CH = 1.0
    P['white'].append(rrect(W, D, 7).extrude(H0 - CH))
    P['white'].append(rrect(W, D, 7).extrude(CH, scale_top=((W - 2 * CH) / W, (D - 2 * CH) / D)).translate([0, 0, H0 - CH]))

    # front strip: KING SALMAN STADIUM, then RIYADH · 2034 between gold rules
    y_strip = -D / 2 + 12.0
    t1 = tracked_cs('KING SALMAN STADIUM', 5.0, 0, -D / 2 + 8.6, 'Black', .05)
    t2 = tracked_cs('RIYADH  \u00b7  2034', 2.6, 0, -D / 2 + 3.6, 'SemiBold', .3)
    P['gold'] += [slab(t1, z0, .6), slab(t2, z0, .6)]
    b1, b2 = t1.bounds(), t2.bounds()
    for x0, x1 in [(b1[0], b2[0] - 3), (b2[2] + 3, b1[2])]:
        P['gold'].append(box(x0, -D / 2 + 3.6 - .4, z0, x1, -D / 2 + 3.6 + .4, z0 + .6))

    # stadium dimensions
    A, B = L(58), L(51)
    Ai, Bi = A - L(3.5), B - L(3.5)
    WALL = L(26)
    a0, b0 = L(28), L(19)
    PODIUM = 1.0
    st = lambda cs: cs.translate([SX, CY])
    back = lambda m: m ^ box(-W, CY, -1, W, D, 200)          # keep only the back half

    # road along the front (right behind the title strip), container quay on the right
    yr0, yr1 = y_strip + .5, CY - .3
    road = rect(-W / 2 + 3, yr0, W / 2 - 3, yr1)
    qx0 = SX + A + L(2) + 2.5
    quay = rect(qx0, CY, W / 2 - 3, RAIL_Y0 - 1.5)
    plaza = st(ellipse(A + L(2) + 1.2, B + L(2) + 1.2))
    lawn = rrect(W - 4, D - 4, 5) - rect(-W, -D, W, yr1 + .01) - quay - plaza - rect(-PW / 2 - 5.5, RAIL_Y0 - 1.0, PW / 2 + 5.5, RAIL_Y1 + 1.5)
    P['green'].append(slab(lawn, z0, .6))
    x = -W / 2 + 5
    ym = (yr0 + yr1) / 2
    while x + 4 < W / 2 - 4:
        P['gold'].append(box(x, ym - .4, z0, x + 4, ym + .4, z0 + .4)); x += 7

    # podium and pitch, back half, with flush white markings
    P['white'].append(back(slab(st(ellipse(A + L(2), B + L(2)) - ellipse(a0, b0)), z0, PODIUM)))
    P['green'].append(back(slab(st(ellipse(a0 + .01, b0 + .01)), z0, PODIUM)))
    lw, fw, fd = .7, L(40), L(26)
    def frame(x0, y0, x1, y1):
        return rect(x0 - lw / 2, y0 - lw / 2, x1 + lw / 2, y1 + lw / 2) - rect(x0 + lw / 2, y0 + lw / 2, x1 - lw / 2, y1 - lw / 2)
    mk = frame(-fw / 2, -fd / 2, fw / 2, fd / 2) + rect(-lw / 2, -fd / 2, lw / 2, fd / 2)
    mk = mk + (ellipse(L(4.2) + lw / 2, L(4.2) + lw / 2, 64) - ellipse(L(4.2) - lw / 2, L(4.2) - lw / 2, 64))
    for sg in (-1, 1):
        xe = sg * fw / 2
        mk = mk + frame(min(xe, xe - sg * L(6.5)), -L(7.5), max(xe, xe - sg * L(6.5)), L(7.5))
    P['_lines'] = [back(slab(st(mk), z0 + PODIUM - .4, .4))]

    # the back half of the stands: stepped bowl, outer wall and diagrid ribs (all white)
    stand = []
    N = 12
    for i in range(N):
        f = i / (N - 1)
        ai, bi = a0 + (Ai - a0) * f, b0 + (Bi - b0) * f
        h = L(2.2) + (WALL - L(2.2)) * f ** 1.2
        stand.append(slab(st(ellipse(A, B) - ellipse(ai, bi)), z0, h))
    stand.append(slab(st(ellipse(A, B) - ellipse(Ai, Bi)), z0, WALL))
    rib_w, rib_out = 1.0, .6
    NR = 28
    span = 2 * math.pi / NR * 3
    zb, zt = z0 + L(2), z0 + WALL - .8
    for k in range(NR):
        for sg in (-1, 1):
            for sgi in range(7):
                pts = []
                for u in (sgi / 7, (sgi + 1) / 7):
                    th, z = 2 * math.pi * k / NR + sg * span * u, zb + (zt - zb) * u
                    x_, y_ = A * math.cos(th), B * math.sin(th)
                    nx, ny = B * math.cos(th), A * math.sin(th); n = math.hypot(nx, ny); nx, ny = nx / n, ny / n
                    tx, ty = -A * math.sin(th), B * math.cos(th); t = math.hypot(tx, ty); tx, ty = tx / t, ty / t
                    for dn in (-.5, rib_out):
                        for dt in (-rib_w / 2, rib_w / 2):
                            for dz in (-rib_w / 2, rib_w / 2):
                                pts.append([SX + x_ + nx * dn + tx * dt, CY + y_ + ny * dn + ty * dt, z + dz])
                stand.append(Manifold.hull_points(np.array(pts)))
    P['white'].append(back(union(stand)))

    # gold roof ring, back half, 45-degree undersides
    rz = z0 + WALL
    ro = A + .8
    outer = ellipse(A, B).extrude(ro - A, scale_top=(ro / A, (B + ro - A) / B)).translate([SX, CY, rz])
    outer = outer + slab(st(ellipse(ro, B + ro - A)), rz + ro - A, 2.0 - (ro - A))
    ins = 1.6
    cone = ellipse(Ai, Bi).extrude(ins, scale_top=((Ai - ins) / Ai, (Bi - ins) / Bi)).translate([SX, CY, rz - .01])
    hole = slab(st(ellipse(Ai - ins, Bi - ins)), rz + ins - .02, 10)
    P['gold'].append(back(outer - cone - hole))

    # scoreboard on a pin over the half pitch: white body, flush red screens with white lettering
    sbw, sbh = L(19), L(9)
    bx, by = SX, CY + sbw / 2 + .8
    sb_top = rz - .8; sb_bot = sb_top - sbh
    P['white'].append(box(bx - sbw / 2, by - sbw / 2, sb_bot, bx + sbw / 2, by + sbw / 2, sb_top))
    apex = sb_bot - sbw / 2
    P['white'].append(Manifold.hull_points(np.array([[bx + dx * sbw / 2, by + dy * sbw / 2, sb_bot] for dx in (-1, 1) for dy in (-1, 1)] + [[bx, by, apex]])))
    pr = 1.1
    P['white'].append(Manifold.cylinder(apex - (z0 + PODIUM) + .6, pr, pr * .7, 20).translate([bx, by, z0 + PODIUM - .01]))
    sw_ = sbw - 1.4
    for k, lab in enumerate(['MBSC', '2034', 'MBSC', '2034']):
        scr = rect(-sw_ / 2, sb_bot + .7, sw_ / 2, sb_top - .7)
        txt = tracked_cs(lab, (sbh - 1.4) * .55, 0, sb_bot + sbh / 2, 'Black', .08)
        m = ED.face_solid(scr - txt, 0, -sbw / 2, embed=.6)        # flush: 0.6 mm into the face
        P['red'].append(m.rotate([0, 0, 90 * k]).translate([bx, by, 0]))

    # container quay: a low white quay, a red-and-white lower tier, a gold-and-white upper tier
    QH = 1.8
    P['white'].append(box(qx0, CY, z0, W / 2 - 3, RAIL_Y0 - 1.5, z0 + QH))
    cw, cd, chh = 7.0, 3.0, 2.5
    zc = z0 + QH
    ncol = int((W / 2 - 3 - qx0 - 2) // (cw + 1))
    cols_x = [qx0 + 1.2 + i * (cw + 1.0) for i in range(ncol)]
    rows_y = [CY + 1.2 + j * (cd + 1.0) for j in range(12)]
    for j, yy in enumerate(rows_y):
        for i, xx in enumerate(cols_x):
            if yy + cd > RAIL_Y0 - 2.5: continue
            low = 'red' if (i + j) % 3 != 1 else 'white'
            P[low].append(box(xx, yy, zc, xx + cw, yy + cd, zc + chh))
            if (i * 3 + j) % 4 != 3:
                P['gold' if (i + 2 * j) % 3 else 'white'].append(box(xx, yy, zc + chh, xx + cw, yy + cd, zc + 2 * chh))

    # trucks on the road: an imported red container heading for the quay, a white (made in Saudi) one leaving
    def truck(x, y, heading, load):
        s = .7
        tw, cab_l, tr_l = 6.6 * s, 5.6 * s, 15 * s
        wh_r = 1.5 * s
        parts = {'white': [], 'red': []}
        for wy in (1.8 * s, cab_l + 3 * s, cab_l + tr_l - 2.5 * s):
            parts['white'].append(Manifold.cylinder(tw + .3, wh_r, wh_r, 20).rotate([0, 90, 0]).translate([-(tw + .3) / 2, wy, z0 + wh_r * .7]))
        ch_z = z0 + wh_r * .9
        cz = z0 + QH                                     # deck at quay height: one red band for every container
        parts['white'].append(box(-tw / 2, 0, ch_z, tw / 2, cab_l + tr_l, cz))
        parts['white'].append(box(-tw / 2, 0, cz, tw / 2, cab_l - .4, cz + 5.2 * s))
        parts[load].append(box(-tw / 2 + .15, cab_l + .2, cz, tw / 2 - .15, cab_l + tr_l, cz + chh))
        total = cab_l + tr_l
        for c, ms in parts.items():
            if not ms: continue
            P[c].append(union(ms).translate([0, -total / 2, 0]).rotate([0, 0, heading]).translate([x, y, 0]))
    lane = (yr1 - yr0) / 4
    truck(18, yr1 - lane, 90, 'red')
    truck(-30, yr0 + lane, -90, 'white')

    # low shrubs along the plaza edge (palms left out: they would add a colour swap on ~80 layers)
    for th in np.linspace(.12, math.pi - .12, 15):
        px, py = SX + (A + L(2) + 3.2) * math.cos(th), CY + (B + L(2) + 3.2) * math.sin(th)
        if px > qx0 - 2 or py > RAIL_Y0 - 3 or abs(px) > W / 2 - 4: continue
        P['green'].append(Manifold.sphere(1.4, 18).translate([px, py, z0 + .3]).trim_by_plane([0, 0, 1], z0 + .3))

    # the rail with the slot for the logo plaque
    rail = rect(-PW / 2 - 4, RAIL_Y0, PW / 2 + 4, RAIL_Y1)
    P['white'].append(slab(rail, z0, RAIL_H))
    slot = box(-PW / 2 - SLOT_CLEAR / 2, SLOT_Y - SLOT_W / 2, z0 - SLOT_DEPTH, PW / 2 + SLOT_CLEAR / 2, SLOT_Y + SLOT_W / 2, z0 + RAIL_H + 1)
    P['_cut'] = [slot]
    return ED.resolve(P)

# ══ the logo plaque, printed flat and face up ═══════════════════════════════
def plaque():
    """Plaque in its print pose: lying flat, face up, bottom edge at y = 0."""
    P = ED.new_parts()
    T = PT
    P['white'].append(rrect(PW, PH, 2.5).translate([0, PH / 2]).extrude(T))
    zi = T - INLAY
    inl = lambda cs: slab(cs, zi, INLAY + .001)
    # gold frame on the visible part
    fr = 1.2
    v0 = INSERT + 1.5
    P['gold'].append(inl(rect(-PW / 2 + 1.8, v0, PW / 2 - 1.8, PH - 1.8) - rect(-PW / 2 + 1.8 + fr, v0 + fr, PW / 2 - 1.8 - fr, PH - 1.8 - fr)))
    # the full college logo: red shield with white calligraphy, gold name, red rule
    full = np.array(Image.open(os.path.join(HERE, 'logo_full.png')).convert('L')) > 127
    redm = np.array(Image.open(os.path.join(HERE, 'logo_red.png')).convert('L')) > 127
    lh = 25.0
    k = lh / full.shape[0]; lw_ = full.shape[1] * k
    x_left, v_top = -lw_ / 2, PH - 5.0
    sc = 1010
    sh = np.zeros_like(full); sh[:, :sc] = full[:, :sc]
    tx = np.zeros_like(full); tx[:, sc:] = full[:, sc:]
    shield = morphology.remove_small_holes(sh, max_size=5000)
    sh_w = morphology.dilation(sh & ~redm, morphology.disk(5)) & shield
    sh_cs, wh_cs = ST._mask_rings(shield, x_left, v_top, k), ST._mask_rings(sh_w, x_left, v_top, k)
    P['red'].append(inl(sh_cs - wh_cs))
    P['gold'].append(inl(ST._mask_rings(morphology.dilation(tx & ~redm, morphology.disk(4)), x_left, v_top, k)))
    if (tx & redm).any():
        P['red'].append(inl(ST._mask_rings(morphology.dilation(tx & redm, morphology.disk(3)), x_left, v_top, k)))
    # caption under the logo
    cap = tracked_cs('GROUP 8  ·  MBSC EMBA  ·  ECN 511  ·  2026', 2.6, 0, v_top - lh - 4.0, 'Bold', .12)
    P['gold'].append(inl(cap))
    S_ = ED.resolve(P)
    return S_

def plaque_upright(Pq):
    """The plaque turned upright and dropped into the slot (for the assembled preview)."""
    out = {}
    for c, m in Pq.items():
        mm = m.rotate([90, 0, 0])                     # face (+z) now faces -y; v becomes height
        out[c] = mm.translate([0, SLOT_Y + PT / 2, H0 - SLOT_DEPTH])
    return out

# ══ export: one Bambu project with two objects on one plate ═════════════════
def write_3mf_plate(path, objects, title):
    """objects = [(name, [(colour, (v, f)), ...], (x, y)), ...] placed on the 256 mm plate."""
    U = lambda: str(uuid.uuid4())
    NS = ('xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
          'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
          'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p"')
    head = '<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" %s>\n' % NS
    meta = ('<metadata name="Application">BambuStudio-01.10.01.50</metadata>\n'
            '<metadata name="BambuStudio:3mfVersion">1</metadata>\n')
    files = {}
    top_objs, build_items, cfg_objs, plate_inst, assemble = [], [], [], [], []
    sub_id = 0
    top_id = 1000
    for oi, (name, parts, (px, py)) in enumerate(objects, start=1):
        allv = np.vstack([v for _, (v, f) in parts])
        off = np.array([(allv[:, 0].min() + allv[:, 0].max()) / 2, (allv[:, 1].min() + allv[:, 1].max()) / 2, allv[:, 2].min()])
        subs, comps, cfgp = [], [], []
        fname = '3D/Objects/object_%d.model' % oi
        for col, (v, f) in parts:
            sub_id += 1
            vv = v - off
            vs = ''.join('<vertex x="%.4f" y="%.4f" z="%.4f"/>' % tuple(p) for p in vv)
            ts = ''.join('<triangle v1="%d" v2="%d" v3="%d"/>' % tuple(t) for t in f)
            subs.append('<object id="%d" p:UUID="%s" type="model"><mesh><vertices>%s</vertices><triangles>%s</triangles></mesh></object>' % (sub_id, U(), vs, ts))
            comps.append('<component p:path="/%s" objectid="%d" p:UUID="%s" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>' % (fname, sub_id, U()))
            slot_no = COLOURS.index(col) + 1
            cfgp.append('<part id="%d" subtype="normal_part"><metadata key="name" value="%s %s"/>'
                        '<metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>'
                        '<metadata key="extruder" value="%d"/></part>' % (sub_id, name, col.capitalize(), slot_no))
        files[fname] = head + meta + '<resources>\n' + '\n'.join(subs) + '\n</resources>\n<build/>\n</model>\n'
        top_id += 1
        tr = '1 0 0 0 1 0 0 0 1 %.2f %.2f 0' % (px, py)
        top_objs.append('<object id="%d" p:UUID="%s" type="model"><components>%s</components></object>' % (top_id, U(), ''.join(comps)))
        build_items.append('<item objectid="%d" p:UUID="%s" transform="%s" printable="1"/>' % (top_id, U(), tr))
        cfg_objs.append('<object id="%d"><metadata key="name" value="%s"/><metadata key="extruder" value="1"/>%s</object>' % (top_id, name, ''.join(cfgp)))
        plate_inst.append('<model_instance><metadata key="object_id" value="%d"/><metadata key="instance_id" value="0"/>'
                          '<metadata key="identify_id" value="%d"/></model_instance>' % (top_id, 100 + oi))
        assemble.append('<assemble_item object_id="%d" instance_id="0" transform="%s" offset="0 0 0"/>' % (top_id, tr))
    main = (head + meta + '<metadata name="Title">%s</metadata>\n<resources>\n%s\n</resources>\n<build p:UUID="%s">%s</build>\n</model>\n'
            % (title, '\n'.join(top_objs), U(), ''.join(build_items)))
    cfg = ('<?xml version="1.0" encoding="UTF-8"?>\n<config>\n%s\n'
           '<plate><metadata key="plater_id" value="1"/><metadata key="plater_name" value=""/><metadata key="locked" value="false"/>%s</plate>\n'
           '<assemble>%s</assemble>\n</config>\n' % ('\n'.join(cfg_objs), ''.join(plate_inst), ''.join(assemble)))
    project = {
        'version': '01.10.01.50', 'name': 'project_settings', 'from': 'project',
        'filament_colour': [ST.FILAMENT_HEX[c] for c in COLOURS], 'filament_type': ['PLA'] * 4,
        'filament_settings_id': ['Bambu PLA Basic @BBL X1C'] * 4,
        'printer_settings_id': 'Bambu Lab X1 Carbon 0.4 nozzle', 'printer_model': 'Bambu Lab X1 Carbon',
        'print_settings_id': '0.16mm Optimal @BBL X1C',
        'enable_support': '0', 'layer_height': '0.16', 'sparse_infill_density': '10%', 'sparse_infill_pattern': 'grid',
        'wall_loops': '2', 'enable_prime_tower': '1', 'flush_into_infill': '1',
    }
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
          '<Default Extension="png" ContentType="image/png"/>'
          '<Default Extension="config" ContentType="text/xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    mrels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             + ''.join('<Relationship Target="/%s" Id="rel-%d" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>' % (fn, i + 1)
                       for i, fn in enumerate(files)) + '</Relationships>')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct)
        z.writestr('_rels/.rels', rels)
        z.writestr('3D/3dmodel.model', main)
        z.writestr('3D/_rels/3dmodel.model.rels', mrels)
        for fn, txt in files.items(): z.writestr(fn, txt)
        z.writestr('Metadata/model_settings.config', cfg)
        z.writestr('Metadata/project_settings.config', json.dumps(project, indent=4))

def parts_of(solids):
    return [(c, ST.mesh_arrays(solids[c])) for c in COLOURS if not solids[c].is_empty()]

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    B_ = base(); Q_ = plaque()
    for tag, sol in (('light_base', B_), ('light_plaque', Q_), ('light_assembled', None)):
        if sol is None:
            up = plaque_upright(Q_)
            sol = {c: B_[c] + up[c] for c in COLOURS}
        for c in COLOURS:
            v, f = ST.mesh_arrays(sol[c])
            ST.write_stl(os.path.join(out, 'stadium_%s_%d_%s.stl' % (tag, COLOURS.index(c) + 1, c)), v, f)
        allm = union(list(sol.values())); bb = allm.bounding_box()
        print(tag, 'size %.1f x %.1f x %.1f mm' % (bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2]),
              ' '.join('%s %.1fcm3' % (c, sol[c].volume() / 1000) for c in COLOURS))
    write_3mf_plate(os.path.join(out, 'stadium_light_4colour.3mf'),
                    [('Base', parts_of(B_), (128, 172)), ('Logo plaque', parts_of(Q_), (128, 52))],
                    'King Salman Stadium (light edition)')
    print('wrote', out)

"""Photo-style Blender (Cycles) renders of the four-colour keepsake.

Usage: python render_blender.py PRINT_DIR SIZE OUT.png [view]
  SIZE  large | small        view  hero | front | top | billboard | bowl
Materials imitate the filaments: matte white PLA, green, silk gold and red.
"""
import sys, math, os
import bpy, bmesh
from mathutils import Vector

src, size, out = sys.argv[1], sys.argv[2], sys.argv[3]
view = sys.argv[4] if len(sys.argv) > 4 else 'hero'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

MATS = {
    'white': dict(c=(0.86, 0.85, 0.82), r=0.46, m=0.0, coat=0.15),
    'green': dict(c=(0.02, 0.22, 0.08), r=0.42, m=0.0, coat=0.2),
    'gold':  dict(c=(0.80, 0.52, 0.16), r=0.28, m=0.85, coat=0.0),
    'red':   dict(c=(0.50, 0.015, 0.025), r=0.40, m=0.0, coat=0.2),
}
def material(name, d):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*d['c'], 1)
    b.inputs['Roughness'].default_value = d['r']
    b.inputs['Metallic'].default_value = d['m']
    if 'Coat Weight' in b.inputs: b.inputs['Coat Weight'].default_value = d['coat']
    return m

objs = []
for i, col in enumerate(['white', 'green', 'gold', 'red'], 1):
    path = os.path.join(src, 'stadium_%s_%d_%s.stl' % (size, i, col))
    bpy.ops.wm.stl_import(filepath=path)
    ob = bpy.context.selected_objects[0]; ob.name = col
    # weld + smooth only when asked: welding touching boxes (container stacks) makes
    # non-manifold edges that render as black patches; the STL normals are already right
    if os.environ.get('SMOOTH', '0') == '1':
        bm = bmesh.new(); bm.from_mesh(ob.data)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
        bm.to_mesh(ob.data); bm.free()
    ob.data.materials.append(material(col, MATS[col]))
    bpy.context.view_layer.objects.active = ob
    if os.environ.get('SMOOTH', '0') == '1':
        try: bpy.ops.object.shade_auto_smooth(angle=math.radians(40))
        except Exception: pass
    objs.append(ob)

# model extents
lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
for ob in objs:
    for v in ob.data.vertices:
        p = ob.matrix_world @ v.co; lo = Vector(map(min, lo, p)); hi = Vector(map(max, hi, p))
ctr = (lo + hi) / 2; span = (hi - lo).length

# studio: a seamless sweep, a big soft key light, a rim light and a fill
bpy.ops.mesh.primitive_plane_add(size=span * 12, location=(ctr.x, ctr.y, lo.z - .05))
floor = bpy.context.object
fm = material('floor', dict(c=(0.035, 0.07, 0.06), r=0.55, m=0, coat=0)); floor.data.materials.append(fm)
def area(name, loc, energy, size_, color=(1, 1, 1)):
    bpy.ops.object.light_add(type='AREA', location=loc); L = bpy.context.object; L.name = name
    L.data.energy = energy; L.data.size = size_; L.data.color = color
    d = ctr - Vector(loc); L.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return L
k = span / 270
area('key', (ctr.x - 260 * k, ctr.y - 300 * k, ctr.z + 380 * k), 4.2e6 * k * k, 260 * k, (1, .96, .9))
area('rim', (ctr.x + 260 * k, ctr.y + 330 * k, ctr.z + 220 * k), 2.2e6 * k * k, 160 * k, (.85, .92, 1))
area('fill', (ctr.x + 330 * k, ctr.y - 240 * k, ctr.z + 90 * k), .7e6 * k * k, 200 * k)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.02, 0.035, 0.032, 1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.6

# camera
VIEWS = {  # azimuth from -Y (deg), elevation (deg), distance x span, aim offset, focal mm
    'hero': (-22, 36, 1.95, (0, -6 * k, -4 * k), 70),
    'square': (-30, 32, 2.25, (0, -4 * k, -2 * k), 70),
    'square_front': (0, 20, 2.1, (0, 0, -2 * k), 70),
    'square_back': (180, 18, 2.1, (0, 0, -6 * k), 70),
    'dome': (-16, 26, 1.05, (0, 4 * k, 10 * k), 70),
    'front': (0, 16, 1.7, (0, 0, -6 * k), 80),
    'top': (10, 68, 1.45, (0, 6 * k, 0), 60),
    'billboard': (12, 14, .55, (-62 * k, -46 * k, 8 * k), 85),
    'bowl': (8, 44, .62, (0, 14 * k, 6 * k), 70),
    'back': (205, 30, 1.85, (0, 4 * k, -4 * k), 70),
    'side': (68, 24, 1.75, (0, 0, -4 * k), 70),
    'scoreboard': (14, 40, .58, (0, 14 * k, 6 * k), 85),
    'yard': (-28, 32, .66, (66 * k, -44 * k, 6 * k), 80),
    'avenue': (4, 10, .64, (0, -30 * k, 10 * k), 50),
    'palms': (40, 14, .46, (-14 * k, -44 * k, 10 * k), 70),
}
az, el, dk, aim, focal = VIEWS[view]
tgt = ctr + Vector(aim)
d = span * dk
cam_loc = tgt + Vector((math.sin(math.radians(az)) * math.cos(math.radians(el)) * d,
                        -math.cos(math.radians(az)) * math.cos(math.radians(el)) * d,
                        math.sin(math.radians(el)) * d))
bpy.ops.object.camera_add(location=cam_loc); cam = bpy.context.object
cam.rotation_euler = (tgt - cam_loc).to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = focal; cam.data.clip_end = span * 50
cam.data.dof.use_dof = True; cam.data.dof.focus_distance = (tgt - cam_loc).length; cam.data.dof.aperture_fstop = 11
sc.camera = cam

sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = int(os.environ.get('SAMPLES', 96))
sc.cycles.use_denoising = True
rx, ry = (int(v) for v in os.environ.get('RES', '1600x1000').split('x'))
sc.render.resolution_x, sc.render.resolution_y = rx, ry
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.015
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_depth = '16'
sc.render.film_transparent = False
try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'; sc.view_settings.exposure = -0.35
except Exception: pass
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print('rendered', out)

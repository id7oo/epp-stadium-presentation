import sys
import os
src = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src)
import statue
from manifold3d import JoinType
from collections import defaultdict
cfg = {'large': (1.0, False, False, 'top'), 'small': (0.52, True, False, 'top'), 'monument': (1.0, False, False, 'face'), 'nameplate': (1.0, False, False, 'bevel')}
S, small, cut, txt = cfg[sys.argv[1]]
allm = statue.union(list(statue.build(S, small, cut, txt).values()))
bb = allm.bounding_box(); lh = .2
def printable(cs):  # what a 0.4 mm nozzle can actually lay down in this layer
    return cs.offset(-.2, JoinType.Round).offset(.2, JoinType.Round)
z = bb[2] + lh * .5; prev = None; bad = []
while z < bb[5]:
    pr = printable(allm.slice(z))
    if prev is not None:
        for comp in pr.decompose():
            a = comp.area()
            if a < .05: continue
            if (comp ^ prev).area() < .15 * a:      # nothing printed under it
                b = comp.bounds(); bad.append((round(z, 2), round(a, 2), round((b[0] + b[2]) / 2), round((b[1] + b[3]) / 2)))
    prev = pr; z += lh
g = defaultdict(list)
for t in bad: g[(t[2] // 5, t[3] // 5)].append(t)
print(sys.argv[1], 'floating regions (slicer view):', len(bad), 'at', len(g), 'places')
for k, v in sorted(g.items(), key=lambda kv: kv[1][0][0])[:20]:
    print('  x=%d y=%d z=%.1f area=%.2f' % (v[0][2], v[0][3], v[0][0], v[0][1]))

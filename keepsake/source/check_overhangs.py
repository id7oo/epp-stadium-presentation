import sys, numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import statue
from collections import defaultdict
cfg = {'large': (1.0, False, False, 'top'), 'monument': (1.0, False, False, 'face'), 'nameplate': (1.0, False, False, 'bevel')}
S, small, cut, txt = cfg[sys.argv[1]]
allm = statue.union(list(statue.build(S, small, cut, txt).values()))
v, f = statue.mesh_arrays(allm)
tri = v[f]
n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); area = np.linalg.norm(n, axis=1) / 2
n = n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
cz = tri[:, :, 2].mean(1)
# facing down more than 60 degrees from vertical (under 30 degrees from horizontal), not on the bed
mask = (n[:, 2] < -0.866) & (cz > 0.3) & (area > 1e-4)
c = tri[mask].mean(1); a = area[mask]
g = defaultdict(float); where = {}
for p, aa in zip(c, a):
    k = (int(p[0] // 6), int(p[1] // 6), int(p[2] // 3)); g[k] += aa; where[k] = p
print(sys.argv[1], 'downward faces <30 deg from horizontal: total %.1f mm2 in %d clusters' % (a.sum(), len(g)))
for k, aa in sorted(g.items(), key=lambda kv: -kv[1])[:25]:
    p = where[k]; print('  %.1f mm2 near x=%.0f y=%.0f z=%.1f' % (aa, p[0], p[1], p[2]))

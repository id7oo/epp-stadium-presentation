"""Bake each slide's background: a blurred, darkened 3D stadium render with frosted
glass panels composited on it (blur, tint, sheen, hairline edge, soft shadow).
Text and data stay native in PowerPoint on top of these images.

Usage: python glass.py spec.json IMG_DIR
"""
import json, sys, os
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageChops

spec = json.load(open(sys.argv[1])); D = sys.argv[2]
PX = 144                                   # pixels per inch: 13.333 x 7.5 in -> 1920 x 1080
W, H = 1920, 1080
TINT = {'glass': (40, 70, 62), 'green': (20, 120, 80), 'gold': (150, 110, 30), 'red': (160, 60, 25), 'dark': (6, 14, 16)}

def rounded(w, h, r):
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255); return m

cache = {}
def backdrop(name, mode):
    key = (name, mode)
    if key in cache: return cache[key]
    im = Image.open(os.path.join(D, name)).convert('RGB').resize((W, H), Image.LANCZOS)
    if mode == 'content':
        im = im.filter(ImageFilter.GaussianBlur(26))
        a = np.asarray(im).astype(float)
        a = a * .30 + np.array([4, 12, 12]) * .7                       # deep, night-green
        # vignette and a soft glow up-right, like the web deck
        y, x = np.mgrid[0:H, 0:W]
        v = 1 - .55 * np.clip(((x - W * .5) / W) ** 2 * 2.2 + ((y - H * .5) / H) ** 2 * 2.2, 0, 1)
        g = np.clip(1 - np.sqrt(((x - W * .78) / W) ** 2 + ((y - H * .12) / H) ** 2) * 1.6, 0, 1) ** 2
        a = a * v[..., None] + np.array([10, 60, 42]) * g[..., None] * .55
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    cache[key] = im
    return im

def panel(base, sharp, p):
    x, y, w, h = [int(round(v * PX)) for v in (p['x'], p['y'], p['w'], p['h'])]
    r = int(p.get('r', .16) * PX)
    if w < 4 or h < 4: return base
    tint = TINT[p.get('tint', 'glass')]
    strength = p.get('alpha', 1.0)
    # 1. soft drop shadow
    if p.get('shadow', True):
        sh = Image.new('L', (W, H), 0)
        ImageDraw.Draw(sh).rounded_rectangle([x, y + 14, x + w, y + h + 14], r, fill=int(150 * strength))
        sh = sh.filter(ImageFilter.GaussianBlur(26))
        base = Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), base, sh)
    # 2. frosted body: heavy blur of what is behind, lifted and tinted
    pad = 40
    box = (max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad))
    behind = sharp.crop(box).filter(ImageFilter.GaussianBlur(30))
    behind = behind.crop((x - box[0], y - box[1], x - box[0] + w, y - box[1] + h))
    a = np.asarray(behind).astype(float)
    a = a * .55 + np.array(tint) * .38 + 255 * .035
    # 3. sheen: a diagonal highlight from the top-left corner
    yy, xx = np.mgrid[0:h, 0:w]
    d = (xx / max(w, 1) * .55 + yy / max(h, 1) * .9)
    sheen = np.clip(1 - d * 1.9, 0, 1) ** 1.8 * 38
    a = a + sheen[..., None]
    # 4. fine noise so it reads as material, not flat fill
    a = a + np.random.default_rng(x * 7 + y).normal(0, 1.6, a.shape)
    body = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    m = rounded(w, h, r)
    if strength < 1: m = m.point(lambda v: int(v * strength))
    base.paste(body, (x, y), m)
    # 5. hairline edge: brighter at the top, fading down
    edge = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ed = ImageDraw.Draw(edge)
    ed.rounded_rectangle([0, 0, w - 1, h - 1], r, outline=(255, 255, 255, int(70 * strength)), width=2)
    fade = Image.fromarray((np.clip(1.15 - yy / max(h, 1) * .85, .3, 1) * 255).astype(np.uint8))
    edge.putalpha(ImageChops.multiply(edge.getchannel('A'), fade))
    accent = p.get('edge')
    if accent:
        ed2 = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(ed2).rounded_rectangle([0, 0, w - 1, h - 1], r, outline=tuple(int(accent[i:i + 2], 16) for i in (0, 2, 4)) + (150,), width=2)
        edge = Image.alpha_composite(edge, ed2)
    base = base.convert('RGBA'); base.alpha_composite(edge, (x, y)); return base.convert('RGB')

for s in spec:
    sharp = backdrop(s['base'], 'photo' if s['mode'] == 'photo' else 'content')
    out = sharp.copy()
    if s['mode'] == 'photo' and s.get('shade'):
        a = np.asarray(out).astype(float)
        xs = np.linspace(0, 1, W)[None, :, None]; ys = np.linspace(0, 1, H)[:, None, None]
        k = np.clip(1 - (1.25 - xs * 1.3) * s['shade'], .08, 1) if s.get('shadeDir', 'left') == 'left' else np.clip(1 - (ys ** 1.4) * s['shade'], .1, 1)
        out = Image.fromarray(np.clip(a * k + np.array([3, 9, 9]) * (1 - k), 0, 255).astype(np.uint8))
        sharp = out
    for p in s['panels']:
        out = panel(out, sharp, p)
    out.save(os.path.join(D, 's_%02d.jpg' % s['i']), quality=88)
print('baked', len(spec))

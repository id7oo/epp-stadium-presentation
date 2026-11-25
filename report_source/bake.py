"""Bake page backgrounds, section banners and the cover image for the A4 report."""
import os, sys
import numpy as np
from PIL import Image, ImageFilter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = REPO + '/pptx_source/img/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUT, exist_ok=True)

def night(im, W, H, blur=28, keep=.30, glow=(.80, .10)):
    """Blurred, darkened night-green treatment, same recipe as the deck's glass.py."""
    im = im.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im).astype(float)
    a = a * keep + np.array([4, 12, 12]) * (1 - keep)
    y, x = np.mgrid[0:H, 0:W]
    v = 1 - .55 * np.clip(((x - W * .5) / W) ** 2 * 2.2 + ((y - H * .5) / H) ** 2 * 1.6, 0, 1)
    g = np.clip(1 - np.sqrt(((x - W * glow[0]) / W) ** 2 + ((y - H * glow[1]) / H) ** 2) * 1.5, 0, 1) ** 2
    a = a * v[..., None] + np.array([10, 60, 42]) * g[..., None] * .55
    a = a + np.random.default_rng(1).normal(0, 1.2, a.shape)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def portrait(name, cx=.5):
    im = Image.open(SRC + name).convert('RGB')
    w, h = im.size; cw = int(h * 210 / 297)
    x0 = int(np.clip(w * cx - cw / 2, 0, w - cw))
    return im.crop((x0, 0, x0 + cw, h))

# 1. content backgrounds (portrait A4, 1000 x 1414)
W, H = 1000, 1414
for key, name, cx, glow in [('bg_a', 'r_hero.jpg', .55, (.82, .08)), ('bg_b', 'cover.jpg', .46, (.18, .06)),
                            ('bg_c', 'r_top.jpg', .5, (.85, .9)), ('bg_d', 'r_side.jpg', .55, (.15, .92))]:
    im = portrait(name, cx).resize((W, H), Image.LANCZOS)
    night(im, W, H, glow=glow).save(f'{OUT}/{key}.jpg', quality=78, optimize=True, progressive=True)

# 2. section banners (210 x 74 mm -> 1920 x 677)
for key, name, y in [('ban_1', 'aerial.jpg', .45), ('ban_2', 'r_yard.jpg', .55), ('ban_3', 'r_bowl.jpg', .5),
                     ('ban_4', 'r_scoreboard.jpg', .45), ('ban_5', 'r_top.jpg', .42), ('ban_6', 'r_monument.jpg', .62),
                     ('ban_r', 'r_palms.jpg', .5)]:
    im = Image.open(SRC + name).convert('RGB')
    if im.size[0] != 1920: im = im.resize((1920, int(im.size[1] * 1920 / im.size[0])), Image.LANCZOS)
    w, h = im.size; bh = int(w * 74 / 210)
    y0 = int(np.clip(h * y - bh / 2, 0, h - bh))
    b = im.crop((0, y0, w, y0 + bh))
    a = np.asarray(b).astype(float)
    a = a * .78 + np.array([4, 18, 16]) * .22            # a touch of the night-green grade
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(f'{OUT}/{key}.jpg', quality=84, optimize=True, progressive=True)

# 3. cover photo (210 x 190 mm crop of the Populous concept rendering)
im = Image.open(SRC + 'cover.jpg').convert('RGB')
w, h = im.size; cw = int(h * 210 / 190); cx = int(w * .47)
x0 = int(np.clip(cx - cw / 2, 0, w - cw))
im.crop((x0, 0, x0 + cw, h)).save(f'{OUT}/cover.jpg', quality=86, optimize=True, progressive=True)

# 4. back cover render
im = Image.open(SRC + 'r_hero.jpg').convert('RGB')
w, h = im.size; cw = int(h * 210 / 170); x0 = int(w * .5 - cw / 2)
im.crop((x0, 0, x0 + cw, h)).save(f'{OUT}/back.jpg', quality=84, optimize=True, progressive=True)

# 5. official logo, recoloured for the dark page (grey college name -> near-white)
svg = open(REPO + '/keepsake/source/mbsc_logo_official.svg').read().replace('#6e6f72', '#EEF4F3')
open(f'{OUT}/mbsc_logo_dark.svg', 'w').write(svg)
import shutil; shutil.copy(SRC + 'qr.png', f'{OUT}/qr.png'); shutil.copy(SRC + 'r_signature.jpg', f'{OUT}/closing.jpg')
for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(f'{OUT}/{f}') // 1024, 'KB')

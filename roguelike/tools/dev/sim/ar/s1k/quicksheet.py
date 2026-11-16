import sys, json
from pathlib import Path
from PIL import Image, ImageDraw
rp = Path(sys.argv[1]); out = sys.argv[2]
tex = rp / 'assets/rlk/textures/mboss/kn_kit'
items = sorted(tex.glob('*.png'))
W = 900; x = y = rowh = 0; pos = []
ims = []
for p in items:
    im = Image.open(p).convert('RGBA')
    sc = 3 if max(im.size) <= 32 else 2 if max(im.size) <= 64 else 1
    im = im.resize((im.width * sc, im.height * sc), Image.NEAREST)
    w, h = max(im.width, 6 * len(p.stem)) + 10, im.height + 16
    if x + w > W: x, y, rowh = 0, y + rowh, 0
    pos.append((x, y)); ims.append((p.stem, im)); x += w; rowh = max(rowh, h)
H = y + rowh
sheet = Image.new('RGBA', (W, H), (60, 70, 66, 255))
d = ImageDraw.Draw(sheet)
for (n, im), (x, y) in zip(ims, pos):
    sheet.alpha_composite(im, (x + 4, y + 12)); d.text((x + 4, y), n, fill=(255, 255, 255, 255))
sheet.convert('RGB').save(out, quality=85)
print(sheet.size)

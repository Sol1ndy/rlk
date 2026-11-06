# usage: python3 -I skinview.py out.jpg skin.png[:slim|classic] ...  -> front/back figures, 8x (arm width 3 slim / 4 classic)
import sys
from PIL import Image
def fig(sk, back=False, aw=3):
    sk = sk.convert('RGBA'); S = 8; W, H = 16, 32
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    def paste(box, dst):
        img.alpha_composite(sk.crop(box), dst)
    parts = [  # base front, base back, overlay front, overlay back, dst (front view)
        ((8, 8, 16, 16), (24, 8, 32, 16), (40, 8, 48, 16), (56, 8, 64, 16), (4, 0)),
        ((20, 20, 28, 32), (32, 20, 40, 32), (20, 36, 28, 48), (32, 36, 40, 48), (4, 8)),
        ((44, 20, 44 + aw, 32), (44 + 2 * aw - aw + 4 - aw + aw, 20, 0, 0), (44, 36, 44 + aw, 48), None, (4 - aw, 8)),
        ((36, 52, 36 + aw, 64), None, (52, 52, 52 + aw, 64), None, (12, 8)),
        ((4, 20, 8, 32), (12, 20, 16, 32), (4, 36, 8, 48), (12, 36, 16, 48), (4, 20)),
        ((20, 52, 24, 64), (28, 52, 32, 64), (4, 52, 8, 64), (12, 52, 16, 64), (8, 20)),
    ]
    # arm backs: right arm back starts at 44 + aw + 4 (after front aw and side 4); left arm back at 36 + aw + 4
    parts[2] = (parts[2][0], (48 + aw, 20, 48 + 2 * aw, 32), parts[2][2], (48 + aw, 36, 48 + 2 * aw, 48), parts[2][4])
    parts[3] = (parts[3][0], (40 + aw, 52, 40 + 2 * aw, 64), parts[3][2], (56 + aw, 52, 56 + 2 * aw, 64), parts[3][4])
    for bf, bb, of, ob, d in parts:
        w = bf[2] - bf[0]
        if back:
            dx = W - d[0] - w
            paste(bb, (dx, d[1])); paste(ob, (dx, d[1]))
        else:
            paste(bf, d); paste(of, d)
    return img.resize((W * S, H * S), Image.NEAREST)
out = sys.argv[1]; figs = []
for spec in sys.argv[2:]:
    p, _, kind = spec.partition(':'); aw = 4 if kind == 'classic' else 3
    s = Image.open(p); figs += [fig(s, False, aw), fig(s, True, aw)]
o = Image.new('RGBA', (sum(f.width + 16 for f in figs), figs[0].height + 16), (110, 120, 130, 255)); x = 8
for f in figs: o.alpha_composite(f, (x, 8)); x += f.width + 16
o.convert('RGB').save(out, quality=90)

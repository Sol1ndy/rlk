#!/usr/bin/env python3
"""picks.py OUT.jpg cols thumbw  vid:t[:x,y,w,h] ...  -> labelled contact sheet of individually chosen frames."""
import sys, subprocess, os, tempfile
from PIL import Image, ImageDraw
out, cols, tw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
here = os.path.dirname(os.path.abspath(__file__)); d = tempfile.mkdtemp(dir=os.path.join(here, '..', 'tmp'))
src = os.path.join(here, '..', 'src')
ims = []
for i, spec in enumerate(sys.argv[4:]):
    parts = spec.split(':'); v, t = parts[0], float(parts[1]); crop = parts[2] if len(parts) > 2 else None
    f = os.path.join(d, f'{i}.jpg')
    vf = ('crop={2}:{3}:{0}:{1},'.format(*crop.split(',')) if crop else '') + f'scale={tw}:-2'
    subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', os.path.join(src, v + '.mp4'), '-frames:v', '1', '-vf', vf, '-q:v', '3', '-y', f], check=True)
    ims.append((f'{v} {t:.2f}', Image.open(f).convert('RGB'))); os.remove(f)
os.rmdir(d)
h = max(im.height for _, im in ims); w = tw
rows = (len(ims) + cols - 1) // cols
s = Image.new('RGB', (cols * w, rows * h)); dr = ImageDraw.Draw(s)
for j, (lab, im) in enumerate(ims):
    x, y = (j % cols) * w, (j // cols) * h
    s.paste(im, (x, y)); dr.rectangle([x, y, x + 6 * len(lab) + 3, y + 11], fill=(0, 0, 0)); dr.text((x + 2, y), lab, fill=(255, 255, 0))
s.save(out, quality=84); print(out, s.size)

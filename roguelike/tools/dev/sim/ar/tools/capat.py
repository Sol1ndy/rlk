#!/usr/bin/env python3
"""capat.py VIDEO OUT.jpg t1 t2 ... : caption region (1080p x0..1500 y700..990) at the given times, stacked, 640 wide."""
import sys, subprocess, os, tempfile
from PIL import Image, ImageDraw
v, out, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
here = os.path.dirname(os.path.abspath(__file__)); d = tempfile.mkdtemp(dir=os.path.join(here, '..', 'tmp'))
ims = []
for i, t in enumerate(ts):
    f = os.path.join(d, f'{i}.jpg')
    subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', v, '-frames:v', '1', '-vf', 'crop=1500:290:0:700,scale=640:-2', '-q:v', '2', '-y', f], check=True)
    ims.append((t, Image.open(f).convert('RGB'))); os.remove(f)
os.rmdir(d)
w, h = ims[0][1].size
s = Image.new('RGB', (w, h * len(ims))); dr = ImageDraw.Draw(s)
for j, (t, im) in enumerate(ims):
    s.paste(im, (0, j * h)); dr.rectangle([0, j*h, 70, j*h+12], fill=(0,0,0)); dr.text((2, j * h), f'{os.path.basename(v)[:-4]} {t:.1f}', fill=(255, 255, 0))
s.save(out, quality=88); print(out, s.size)

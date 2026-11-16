#!/usr/bin/env python3
"""captions.py VIDEO OUT.jpg [step=0.5] : caption strip crops (1080p x0..1400, y740..905) whenever the caption changes."""
import sys, subprocess, os, tempfile, glob
from PIL import Image, ImageDraw, ImageChops, ImageStat
v, out = sys.argv[1], sys.argv[2]
st = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
here = os.path.dirname(os.path.abspath(__file__))
d = tempfile.mkdtemp(dir=os.path.join(here, '..', 'tmp'))
subprocess.run(['ffmpeg', '-v', 'error', '-i', v, '-vf', f'fps=1/{st}:round=down,crop=1400:165:0:740,scale=560:-2',
                '-q:v', '3', '-y', os.path.join(d, '%03d.jpg')], check=True)
fs = sorted(glob.glob(os.path.join(d, '*.jpg')))
keep = []; prev = None
for i, f in enumerate(fs):
    im = Image.open(f).convert('L')
    # text = bright pixels; compare binarized
    b = im.point(lambda p: 255 if p > 200 else 0)
    if prev is None or ImageStat.Stat(ImageChops.difference(b, prev)).mean[0] > 6:
        keep.append((i * st, Image.open(f).convert('RGB')))
    prev = b
w, h = keep[0][1].size
sheet = Image.new('RGB', (w + 60, h * len(keep)), (0, 0, 0))
dr = ImageDraw.Draw(sheet)
for j, (t, im) in enumerate(keep):
    sheet.paste(im, (60, j * h)); dr.text((2, j * h + 4), f'{os.path.basename(v)[:-4]} {t:.1f}', fill=(255, 255, 0))
sheet.save(out, quality=85)
for f in fs: os.remove(f)
os.rmdir(d)
print(out, sheet.size, len(keep))

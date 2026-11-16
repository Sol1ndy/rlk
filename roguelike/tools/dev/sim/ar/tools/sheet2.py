#!/usr/bin/env python3
"""sheet2.py VIDEO START END STEP OUT.jpg [cols=4] [thumbw=160] [crop=x,y,w,h]
One ffmpeg pass: frames every STEP s in [START,END), tiled with 'vN t.tts' labels (t = START + i*STEP)."""
import sys, subprocess, os, tempfile, glob
from PIL import Image, ImageDraw
v, s, e, st, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 4
tw = int(sys.argv[7]) if len(sys.argv) > 7 else 160
crop = sys.argv[8] if len(sys.argv) > 8 else None
here = os.path.dirname(os.path.abspath(__file__))
d = tempfile.mkdtemp(dir=os.path.join(here, '..', 'tmp'))
vf = ('crop={2}:{3}:{0}:{1},'.format(*crop.split(',')) if crop else '') + f'fps=1/{st}:round=down,scale={tw}:-2'
n = int(round((e - s) / st))
subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(s), '-t', str(e - s), '-i', v, '-vf', vf, '-frames:v', str(n),
                '-q:v', '4', '-y', os.path.join(d, '%03d.jpg')], check=True)
fs = sorted(glob.glob(os.path.join(d, '*.jpg')))
ims = [Image.open(f).convert('RGB') for f in fs]
w, h = ims[0].size
rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, rows * h), (0, 0, 0))
dr = ImageDraw.Draw(sheet)
name = os.path.basename(v)[:-4]
for i, im in enumerate(ims):
    x, y = (i % cols) * w, (i // cols) * h
    sheet.paste(im, (x, y))
    lab = f'{name} {s + i * st:.2f}'
    dr.rectangle([x, y, x + 6 * len(lab) + 3, y + 11], fill=(0, 0, 0))
    dr.text((x + 2, y), lab, fill=(255, 255, 0))
sheet.save(out, quality=82)
for f in fs: os.remove(f)
os.rmdir(d)
print(out, sheet.size, len(ims))

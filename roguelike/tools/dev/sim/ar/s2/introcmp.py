#!/usr/bin/env python3
"""intro vs footage: left v1 crops (the boss), right the rig's intro at the mapped beat tick (renders/s2_intro_vs_ref.jpg)."""
import subprocess, os
from PIL import Image, ImageDraw
S = '/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/ar'
CROP = {'a': '880,230,180,180', 'b': '800,190,320,320', 'c': '760,160,360,360'}
PAIRS = [(0.3, 'a', 4, 'E0 tea: cup and saucer at her chest'), (0.6, 'a', 16, 'E0 sip'), (1.05, 'a', 38, 'E1 hands drop, cup gone'),
         (1.38, 'b', 50, 'E2 arm out to the side'), (1.52, 'b', 61, 'E4 the haft through the palm'), (1.70, 'b', 68, 'E4 crescent ignites'),
         (2.10, 'b', 80, 'E5 hold, title'), (2.52, 'c', 94, 'E6 twirl: rising'), (2.58, 'c', 96, 'E6 overhead'),
         (2.65, 'c', 98, 'E6 at her right'), (2.80, 'c', 101, 'E6 low in front'), (2.95, 'c', 104, 'E6 back, hold'),
         (3.40, 'c', 112, 'E8 flip over the top'), (3.70, 'c', 117, 'E8 head at her right'), (4.20, 'c', 124, 'E9 lowering'),
         (4.80, 'c', 140, 'E9 stance')]
W = 300
rows = []
os.makedirs(f'{S}/s2/ic', exist_ok=True)
for i, (ts, cr, t, lab) in enumerate(PAIRS):
    fa = f'{S}/s2/ic/a{i}.jpg'
    x, y, w, h = CROP[cr].split(',')
    subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ts), '-i', f'{S}/src/v1.mp4', '-frames:v', '1', '-vf', f'crop={w}:{h}:{x}:{y},scale={W}:-2', '-q:v', '3', '-y', fa], check=True)
    fb = f'{S}/s2/ic/b{i}.jpg'
    subprocess.run([f'{S}/s2/r.sh', fb, f'rlk:kn_dbg/intro/{t}', '--', '--views', 'az:12,6', '--extent', '2.5', '--center', '0', '1.6', '0',
                    '--width', str(W), '--title', f'rig intro t{t}'], check=True)
    a, b = Image.open(fa).convert('RGB'), Image.open(fb).convert('RGB')
    b = b.resize((W, int(b.size[1] * W / b.size[0])))
    hh = max(a.size[1], b.size[1])
    row = Image.new('RGB', (2 * W, hh + 14), (0, 0, 0))
    row.paste(a, (0, 14)); row.paste(b, (W, 14))
    ImageDraw.Draw(row).text((4, 1), f'v1 {ts:.2f}s  ->  intro t{t}  {lab}', fill=(255, 230, 90))
    rows.append(row)
    os.remove(fa); os.remove(fb)
# two columns of pairs
half = (len(rows) + 1) // 2
colh = lambda rs: sum(r.size[1] for r in rs)
out = Image.new('RGB', (4 * W, max(colh(rows[:half]), colh(rows[half:]))))
y = 0
for r in rows[:half]:
    out.paste(r, (0, y)); y += r.size[1]
y = 0
for r in rows[half:]:
    out.paste(r, (2 * W, y)); y += r.size[1]
out = out.resize((640, int(out.size[1] * 640 / out.size[0])))
out.save(f'{S}/renders/s2_intro_vs_ref.jpg', quality=84)
print(out.size)

#!/usr/bin/env python3
"""renders/s2_pairs/<clip>.jpg: the footage sheet (ref/<sheet>, left, 320 px) next to the clip strip (right, 320 px, every 6 t)."""
import json, subprocess, os, sys
from PIL import Image, ImageDraw
S = '/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/ar'
M = json.load(open(f'{S}/wt_s2/roguelike/tools/arlecchino_rig_manifest.json'))
PAIRS = {'a2': 'p1_A_normal_2hit', 'a4': 'p1_A_normal_5hit', 'a5': 'p1_A_normal_5hit', 'b1': 'p1_B_throw', 'b2': 'p1_B_throw2_grab',
         'c1': 'p1_C_leap', 'c2': 'p1_C_wing', 'd1': 'p1_D_dash', 'd2': 'p1_D_follow', 'e1': 'p1_E_zigzag_a', 'f1': 'p1_F_banquet',
         'g1': 'p1_G_blades', 'h1': 'p1_H_clones', 'e70': 'p1_E70_event', 't_p2': 'p2_T_transition', 'q0_dive': 'p2_Q0_fall',
         'q1': 'p2_Q1_twin', 'q2': 'p2_Q2_throw_a', 'q3': 'p2_Q3_rear', 'q4_shot': 'p2_Q4_beam', 'q5a': 'p2_Q5_banquet_b',
         'q5b': 'p2_Q5_banquet_a', 'q6': 'p2_Q6_feast'}
os.makedirs(f'{S}/renders/s2_pairs', exist_ok=True)
W = 320
for clip, ref in (PAIRS.items() if len(sys.argv) < 2 else [(c, PAIRS[c]) for c in sys.argv[1:]]):
    c = M['clips'][clip]
    ext, cen = ('3.4', ['0', '2.2', '0']) if c['form'] == 'p2' or clip in ('f1', 'e70') else ('2.7', ['0', '1.7', '0'])
    if clip == 't_p2':
        ext, cen = '4.6', ['0', '4.0', '0']
    out = f'{S}/s2/pair_{clip}.jpg'
    subprocess.run([f'{S}/s2/r.sh', out, f'rlk:kn_dbg/{clip}/{{t}}', '--', '--strip', f'0..{c["len"]}:6', '--views', 'az:20,8', '--extent', ext, '--center', *cen,
                    '--cols', '4', '--width', str(W), '--title', f'{clip} ({c["len"]} t, {c["form"]}) every 6 t'], check=True)
    a = Image.open(f'{S}/ref/{ref}.jpg').convert('RGB'); a = a.resize((W, int(a.size[1] * W / a.size[0])))
    b = Image.open(out).convert('RGB'); b = b.resize((W, int(b.size[1] * W / b.size[0])))
    o = Image.new('RGB', (2 * W, max(a.size[1], b.size[1]) + 14))
    o.paste(a, (0, 14)); o.paste(b, (W, 14))
    ImageDraw.Draw(o).text((4, 1), f'footage ref/{ref}.jpg  |  rig {clip}: {c["source"][:60]}', fill=(255, 230, 90))
    o.save(f'{S}/renders/s2_pairs/{clip}.jpg', quality=80)
    os.remove(out)
    print(clip, o.size)

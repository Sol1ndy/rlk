#!/usr/bin/env python3
"""batch.py <label> <dmgMul|-> <mode:policy:dodge:char,...> [jobs]: seeds 11 22 33, 3600 t, Lv15 vs L18 (knfair.py)."""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
H = Path(__file__).resolve().parent
DP = '/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/ar/review/bal/snap/roguelike'
label, mul, specs = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
out = H / 'out' / label
out.mkdir(parents=True, exist_ok=True)
env = dict(os.environ)
if mul != '-':
    env['KN_DMGMUL'] = mul
todo = []
for sp in specs:
    mode, pol, dod, ch = sp.split(':')
    for sd in (11, 22, 33):
        todo.append([sys.executable, str(H / 'knfair5.py'), DP, mode, pol, dod, ch, str(sd), os.environ.get('KN_N', '3600'), '18', '15',
                     str(out / f'{mode}_{pol}_{dod}_{ch}_{sd}.json')])
def go(c):
    r = subprocess.run(c, capture_output=True, text=True, timeout=3600, env=env)
    return (r.stdout.strip().splitlines() or [''])[-1] + (' ERR ' + r.stderr[-300:] if r.returncode else '')
with ThreadPoolExecutor(jobs) as ex:
    for line in ex.map(go, todo):
        print(line, flush=True)

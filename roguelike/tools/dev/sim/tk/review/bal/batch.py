#!/usr/bin/env python3
"""batch.py <dp> <label> <spec,...> [jobs]: spec = mode:policy:dodge:char:n ; seeds 11 22 33; env TK_LEAD passes through."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
H = Path(__file__).resolve().parent
dp, label, specs = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
seeds = [int(x) for x in os.environ.get('TK_SEEDS', '11,22,33').split(',')]
out = H / 'out' / label
out.mkdir(parents=True, exist_ok=True)
todo = []
for sp in specs:
    mode, pol, dod, ch, n = sp.split(':')
    for sd in seeds:
        f = out / f'{mode}_{pol}_{dod}_{ch}_{sd}.json'
        todo.append([sys.executable, str(H / 'tkfair.py'), dp, mode, pol, dod, ch, str(sd), n, os.environ.get('TK_LV', '6'), str(f)])
def go(c):
    r = subprocess.run(c, capture_output=True, text=True, timeout=7200)
    return (r.stdout.strip().splitlines() or [''])[-1] + (' ERR ' + r.stderr[-300:] if r.returncode else '')
with ThreadPoolExecutor(jobs) as ex:
    for line in ex.map(go, todo):
        print(line, flush=True)

#!/usr/bin/env python3
"""analyze.py <label>...: %max HP lost per minute per (mode, policy, dodge, char) and per phase; whole-fight kill time."""
import json, sys
from collections import defaultdict
from pathlib import Path
H = Path(__file__).resolve().parent
for label in sys.argv[1:]:
    g = defaultdict(list)
    for f in sorted((H / 'out' / label).glob('*.json')):
        r = json.loads(f.read_text())
        g[(r['mode'], r['policy'], r['dodge'], r['char'])].append(r)
    print(f'== {label}')
    for k, rs in sorted(g.items()):
        lost = sum(sum(d[3] or 0 for d in r['dmg']) for r in rs)
        tick = sum(r['ticks'] for r in rs)
        hp = rs[0]['hp']
        hits = sum(len([d for d in r['dmg'] if d[3]]) for r in rs)
        deaths = sum(len(r['deaths']) for r in rs)
        per = defaultdict(lambda: [0, 0])
        for r in rs:
            for ph, t in r['phases'].items():
                per[ph][1] += t
            for d in r['dmg']:
                per[d[5]][0] += d[3] or 0
        phs = ' '.join(f'{ph} {100.0 * v[0] / hp / max(1e-9, v[1] / 1200):.0f}' for ph, v in per.items() if v[1] >= 200)
        ttk = [r['ticks'] / 20 for r in rs if r['end'] == 'dead']
        bypat = defaultdict(int)
        for r in rs:
            for d in r['dmg']:
                bypat[d[4]] += d[3] or 0
        w40 = 0.0
        for r in rs:
            ev = sorted((d[0], d[3] or 0) for d in r['dmg'])
            j, acc = 0, 0
            for i in range(len(ev)):
                acc += ev[i][1]
                while ev[i][0] - ev[j][0] >= 40:
                    acc -= ev[j][1]; j += 1
                w40 = max(w40, 100.0 * acc / hp)
        print(f'{" ".join(k):32s} w40 {w40:5.1f}% %max/min {100.0 * lost / hp / (tick / 1200):6.1f}  hits/min {hits / (tick / 1200):5.1f}  '
              f'HP/hit {lost / max(1, hits):5.1f}  deaths/min {deaths / (tick / 1200):4.2f}  ttk {ttk}  | {phs} | pat ' +
              ' '.join(f'{p}:{100 * v // max(1, lost)}%' for p, v in sorted(bypat.items(), key=lambda x: -x[1])[:6]))

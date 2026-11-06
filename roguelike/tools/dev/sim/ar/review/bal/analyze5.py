#!/usr/bin/env python3
"""analyze5.py <label>...: %max HP lost / min per (mode, policy, dodge, char) vs Apep (P1 for p1a / p1b, P3 for p2), the
worst 40 t window (with / without the Q5B final), orbs taken, breaks, deaths per 3 min."""
import json, sys
from collections import defaultdict
from pathlib import Path
H = Path(__file__).resolve().parent
APEP = {'p1': {'melee walk': 127.7, 'melee none': 132.2, 'ranged walk': 78.7},
        'p2': {'melee walk': 94.4, 'melee none': 186.5, 'ranged walk': 92.8}}
rows = {}
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
        w40 = w40x = 0.0
        for r in rs:
            for excl in (False, True):
                ev = sorted((d[0], d[3] or 0) for d in r['dmg']
                            if not (excl and d[4] == 47 and len(d) > 7 and d[7] == 'brand' and 100.0 * (d[3] or 0) / hp >= 20))
                j, acc, w = 0, 0, 0.0
                for i in range(len(ev)):
                    acc += ev[i][1]
                    while ev[i][0] - ev[j][0] >= 40:
                        acc -= ev[j][1]
                        j += 1
                    w = max(w, 100.0 * acc / hp)
                if excl:
                    w40x = max(w40x, w)
                else:
                    w40 = max(w40, w)
        rate = 100.0 * lost / hp / (tick / 1200)
        ap = APEP['p2' if k[0] == 'p2' else 'p1'].get(f'{k[1]} {k[2]}')
        orbs = sum(r.get('orbs', 0) for r in rs) / len(rs)
        brk = sum(r.get('brk', 0) for r in rs) / len(rs)
        deaths = sum(len(r['deaths']) for r in rs) / len(rs)
        rows[(label, k)] = rate
        print(f'{" ".join(k):28s} %max/min {rate:6.1f}' + (f' = {rate / ap:4.2f}x Apep {"P3" if k[0] == "p2" else "P1"}' if ap else '')
              + f'  worst 40 t {w40:5.1f} % (w/o Q5B final {w40x:5.1f})  orbs {orbs:4.1f} breaks {brk:3.1f} deaths {deaths:3.1f} (n {len(rs)})')
    for pol in ('melee walk sword', 'melee none sword', 'ranged walk bow'):
        a, b = rows.get((label, ('p1a',) + tuple(pol.split()))), rows.get((label, ('p1b',) + tuple(pol.split())))
        if a and b:
            p1 = 0.3 * a + 0.7 * b
            ap = APEP['p1'].get(' '.join(pol.split()[:2]))
            print(f'  P1 (0.3 P1a + 0.7 P1b) {pol:18s} {p1:6.1f} = {p1 / ap:4.2f}x Apep P1')

#!/usr/bin/env python3
"""breakdown.py <label>: HP lost per pattern (and hits, pattern-minutes) per (mode, policy, dodge, char) group."""
import collections, glob, json, sys
from pathlib import Path
D = Path(__file__).resolve().parent / 'out' / sys.argv[1]
G = collections.defaultdict(list)
for f in sorted(glob.glob(str(D / '*.json'))):
    r = json.load(open(f))
    if r['mode'] in ('p1', 'p3'):
        G[(r['mode'], r['policy'], r['dodge'], r['char'])].append(r)
for k, rs in sorted(G.items()):
    by, hits, pt, T = collections.Counter(), collections.Counter(), collections.Counter(), 0
    for r in rs:
        T += r['ticks']
        pt.update(r['pat_ticks'])
        for d in r['dmg']:
            by[d[4]] += d[3] or 0
            hits[d[4]] += 1
    tot = sum(by.values())
    print(k, 'n', len(rs), 'min', round(T / 1200, 1), '%/min', round(100 * tot / 268 / (T / 1200), 1),
          'deaths', sum(len(r['deaths']) for r in rs))
    print('    ', '  '.join(f'{p}:{100 * by[p] / 268 / (T / 1200):.1f}%/m({hits[p]}h,{pt.get(str(p), 0) / 1200:.1f}pm)'
                           for p in sorted(by)))

#!/usr/bin/env python3
"""Balance batch (plan.md "Review-fix decisions", fairness F1): the reviewer's fairness sim (copied here from
mb2/review/fairness/sim: fsim.py, unchanged except the blade reach) on a datapack, butterfly (force 2) vs Guardian
(force 1), the three player behaviours stand / melee walk / ranged walk (react 5), seeds 11 22 33, 3600 t each.

    python3 bal.py <datapack root> <label> [seeds] [jobs]

Writes out_<label>/*.json and prints HP/min (mean over seeds) per policy with the butterfly / Guardian ratio, plus the
butterfly's damage by pattern (HP/min, Burning DoT and the 달빛 고치 cost separate)."""
import json
import os
import sys
import time
from collections import defaultdict
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
POLICIES = (('stand', 'none'), ('melee', 'walk'), ('ranged', 'walk'))
NAMES = {1: 'H1', 2: 'H2', 3: 'H3', 4: 'H4', 11: 'B1', 12: 'B2', 13: 'B3', 14: 'B4', 15: 'B5', 20: 'TF', 0: '-'}


def one(args):
    dp, out, force, policy, dodge, seed, n = args
    os.environ['FDP'] = dp
    sys.path.insert(0, HERE)
    import fsim as F
    t = time.time()
    s, ag, t0 = F.fight(force=force, policy=policy, dodge=dodge, react=5, n=n, seed=seed)
    res = dict(force=force, policy=policy, dodge=dodge, seed=seed, n=n, t0=t0, dmg=s.dmg, stats=ag.stats,
               secs=time.time() - t)
    json.dump(res, open(os.path.join(out, f'{force}_{policy}_{dodge}_s{seed}.json'), 'w'), default=str)
    return f'{force} {policy} {dodge} s{seed}', round(time.time() - t, 1)


def table(out):
    runs = defaultdict(list)
    for f in sorted(os.listdir(out)):
        if f.endswith('.json'):
            r = json.load(open(os.path.join(out, f)))
            runs[(r['force'], r['policy'], r['dodge'])].append(r)
    rows = {}
    for (force, pol, dodge), rs in runs.items():
        mins = sum(r['n'] for r in rs) / 1200
        dm = [d for r in rs for d in r['dmg']]
        tot = sum(d[3] for d in dm)
        hits = len([d for d in dm if d[2] not in ('dot', 'coc')])
        dot = sum(d[3] for d in dm if d[2] == 'dot')
        deaths = sum(len(r['stats'].get('deaths', [])) for r in rs)
        by = defaultdict(float)
        for d in dm:
            k = (NAMES.get(d[4], str(d[4])) if force == 2 else f'G{d[4]}') + ('dot' if d[2] == 'dot' else 'coc' if d[2] == 'coc' else '')
            by[k] += d[3] / mins
        rows[(force, pol, dodge)] = dict(hpm=tot / mins, hits=hits / mins, dot=dot / mins, deaths=deaths / mins, by=by, n=len(rs))
    return rows


def show(out):
    rows = table(out)
    print(f'{"policy":12s} | {"BF HP/min":>9s} {"GD HP/min":>9s} {"BF/GD":>6s} | BF hits/min, DoT/min, deaths/min | GD hits/min')
    for pol, dodge in POLICIES:
        b, g = rows.get((2, pol, dodge)), rows.get((1, pol, dodge))
        if not b or not g:
            continue
        print(f'{pol + " " + dodge:12s} | {b["hpm"]:9.1f} {g["hpm"]:9.1f} {b["hpm"] / g["hpm"]:6.2f} | '
              f'{b["hits"]:5.2f} {b["dot"]:6.1f} {b["deaths"]:5.2f} | {g["hits"]:5.2f}   (seeds {b["n"]}/{g["n"]})')
    for pol, dodge in POLICIES:
        b = rows.get((2, pol, dodge))
        if b:
            print(f'  BF {pol:6s}: ' + '  '.join(f'{k} {v:.1f}' for k, v in sorted(b['by'].items(), key=lambda x: -x[1])))
    return rows


if __name__ == '__main__':
    dp, label = os.path.realpath(sys.argv[1]), sys.argv[2]
    seeds = [int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else '11,22,33').split(',')]
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    out = os.path.join(HERE, f'out_{label}')
    os.makedirs(out, exist_ok=True)
    todo = [(dp, out, f, p, d, s, 3600) for f in (2, 1) for p, d in POLICIES for s in seeds]
    with Pool(jobs) as pool:
        for r in pool.imap_unordered(one, todo):
            print(*r, flush=True)
    show(out)

#!/usr/bin/env python3
"""Tables from out/<label>/*.json: python3 analyze.py <label> [label2 ...]"""
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
FG_NAMES = {1: 'C1', 2: 'C2', 3: 'C3', 4: 'C4', 5: 'C5', 6: 'C6', 11: 'F1', 12: 'F2', 21: 'W', 20: 'warp', 22: 'pack', 0: '-'}


def load(labels):
    runs = []
    for lb in labels:
        d = os.path.join(HERE, 'out', lb)
        for f in sorted(os.listdir(d)):
            if f.endswith('.json'):
                r = json.load(open(os.path.join(d, f)))
                r['_file'] = f
                runs.append(r)
    return runs


def key(r):
    return (r['force'], r['policy'], r['dodge'], r['char'], r['react'], r.get('real_hp', False), r.get('tri', True))


def table(runs):
    grp = defaultdict(list)
    for r in runs:
        grp[key(r)].append(r)
    rows = {}
    for k, rs in sorted(grp.items()):
        ticks = sum((r['t_end'] - r['t0']) for r in rs)
        mins = ticks / 1200
        dm = [d for r in rs for d in r['dmg']]
        tot = sum(d[3] for d in dm)
        hits = [d for d in dm if d[2] != 'dot']
        deaths = sum(len(r['stats'].get('deaths', [])) for r in rs)
        by = defaultdict(float)
        cnt = defaultdict(int)
        for d in dm:
            nm = FG_NAMES.get(d[4], str(d[4])) if k[0] == 3 else f'G{d[4]}'
            by[nm] += d[3] / mins
            cnt[nm] += 1
        st = defaultdict(int)
        sth = defaultdict(int)
        std = defaultdict(int)
        for r in rs:
            for a, v in r['stats']['st_ticks'].items():
                st[a] += v
            for a, v in r['stats']['st_hits'].items():
                sth[a] += v
            for a, v in r['stats']['st_dealt'].items():
                std[a] += v
        dealt = sum(std.values())
        swings = sum(r['stats']['swings'] for r in rs)
        dashes = sum(r['stats']['dashes'] for r in rs)
        jumps = sum(r['stats']['jumps'] for r in rs)
        inreach = sum(r['stats']['inreach'] for r in rs)
        fields = [f for r in rs for f in r['fields']]
        rows[k] = dict(n=len(rs), mins=mins, hpm=tot / mins, hitsm=len(hits) / mins, deathsm=deaths / mins, by=by, cnt=cnt,
                       st=st, sth=sth, std=std, dealtm=dealt / mins, swingsm=swings / mins, dashm=dashes / mins,
                       jumpm=jumps / mins, inreach=inreach / ticks, fields=fields, runs=rs)
    return rows


def show(rows):
    print(f'{"force policy dodge char react":38s} | {"HP/min":>7s} {"hits/m":>6s} {"deaths/m":>8s} {"dealt/m":>8s} {"dash/m":>6s} {"jump/m":>6s} {"inreach":>7s} n')
    for k, r in rows.items():
        print(f'{str(k[:5]):38s} | {r["hpm"]:7.1f} {r["hitsm"]:6.2f} {r["deathsm"]:8.2f} {r["dealtm"]:8.1f} {r["dashm"]:6.2f} {r["jumpm"]:6.2f} {r["inreach"]:7.1%} {r["n"]}')
    print()
    for k, r in rows.items():
        print(f'{str(k[:5]):38s} by pattern HP/min: ' + '  '.join(f'{a} {v:.1f}({r["cnt"][a]})' for a, v in sorted(r['by'].items(), key=lambda x: -x[1])))
    print()
    for k, r in rows.items():
        tot = sum(r['st'].values())
        print(f'{str(k[:5]):38s} time share: ' + '  '.join(f'{a} {v / tot:.1%}' for a, v in sorted(r['st'].items()))
              + ' | dealt/min by state: ' + '  '.join(f'{a} {v / r["mins"]:.0f}' for a, v in sorted(r['std'].items())))
    print()
    for k, r in rows.items():
        if k[0] != 3:
            continue
        fs = r['fields']
        if not fs:
            continue
        br = [f for f in fs if f['broke']]
        tbreak = [f['close'] - f['open'] for f in br]
        full = [f for f in fs if f['close'] is not None]
        print(f'{str(k[:5]):38s} fields {len(fs)} closed {len(full)} broken {len(br)}; open->break ticks {sorted(tbreak)}; '
              f'counts in unbroken: {[len(f["counts"]) for f in full if not f["broke"]]}')


if __name__ == '__main__':
    show(table(load(sys.argv[1:])))

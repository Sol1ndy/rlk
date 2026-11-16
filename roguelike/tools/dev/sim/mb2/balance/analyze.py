import json, glob, os, sys, math
from collections import defaultdict
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
HPMAX = 136
WALK, SWING = 0.2159, 0.10795
NAMES_BF = {1: 'H1', 2: 'H2', 3: 'H3', 4: 'H4', 11: 'B1', 12: 'B2', 13: 'B3', 14: 'B4', 15: 'B5', 20: 'TF', 0: '-'}

runs = defaultdict(list)
for f in sorted(glob.glob(os.path.join(OUT, '*.json'))):
    r = json.load(open(f))
    runs[(r['force'], r['policy'], r['dodge'], r['react'], r.get('sprint', False))].append(r)

def pname(force, p):
    return NAMES_BF.get(p, str(p)) if force == 2 else f'G{p}'

print('== per policy (means over seeds; 3600 t = 3 min per run; player Lv4 item-less, HP 136, def 16; boss Lv4)')
print('boss policy dodge react | dmg/min (%HP) hits/min dot%  coc | deaths/min | dashes/min | uptime all / human / bf / groggy | eff-uptime')
for key in sorted(runs):
    rs = runs[key]
    force, pol, dodge, react, spr = key
    mins = sum(r['n'] for r in rs) / 1200
    dm = [d for r in rs for d in r['dmg']]
    tot = sum(d[3] for d in dm)
    dot = sum(d[3] for d in dm if d[2] == 'dot')
    coc = sum(d[3] for d in dm if d[2] == 'coc')
    hits = len([d for d in dm if d[2] not in ('dot', 'coc')])
    deaths = sum(len(r['stats'].get('deaths', [])) for r in rs)
    dashes = sum(r['stats']['dashes'] for r in rs)
    S = lambda k: sum(r['stats'].get(k, 0) for r in rs)  # noqa
    up = S('attack') / max(1, S('ticks'))
    uh = S('h_attack') / max(1, S('h_ticks'))
    ub = S('bf_attack') / max(1, S('bf_ticks'))
    ug = S('gr_attack') / max(1, S('gr_ticks'))
    eff = S('eff') / max(1, S('ticks'))
    print(f'{"BF" if force == 2 else "GD"} {pol:6s} {dodge:4s} r{react} | {tot / mins:6.1f} ({100 * tot / mins / HPMAX:5.1f}%) {hits / mins:5.2f} {100 * dot / max(1, tot):4.1f}% {coc / mins:4.1f} | '
          f'{deaths / mins:4.2f} | {dashes / mins:5.1f} | {up:5.1%} / {uh:5.1%} / {ub:5.1%} / {ug:5.1%} | {eff:5.1%}')

print()
print('== damage by pattern (BF, all runs of a policy; HP per minute)')
for key in sorted(runs):
    force, pol, dodge, react, spr = key
    rs = runs[key]
    mins = sum(r['n'] for r in rs) / 1200
    by = defaultdict(float)
    for r in rs:
        for d in r['dmg']:
            k = pname(force, d[4]) + ('dot' if d[2] == 'dot' else ('coc' if d[2] == 'coc' else ''))
            by[k] += d[3]
    print(f'{"BF" if force == 2 else "GD"} {pol:6s} {dodge:4s} r{react}: ' + '  '.join(f'{k} {v / mins:.1f}' for k, v in sorted(by.items(), key=lambda x: -x[1])))

print()
print('== hazards at creation (dmg > 0): player inside -> escape distance vs tell (walk 0.216 / swing 0.108 / reaction 5 t)')
for force in (2, 1):
    for pol in ('melee', 'ranged'):
        tab = defaultdict(list)
        for key, rs in runs.items():
            if key[0] != force or key[1] != pol or key[2] == 'none':
                continue
            for r in rs:
                for h in r['hz']:
                    if (h.get('D') or 0) <= 0 or h.get('t', 0) < r['t0']:
                        continue
                    tab[(pname(force, h['pat']), h['D'], h['K'], h['W'], h['A'])].append(h)
        print(f'-- {"BF" if force == 2 else "GD"} {pol}')
        print('pattern dmg shape tell act | n  inside% | esc mean / max | walk-ok% swing-ok% react5-ok% (of inside)')
        for k in sorted(tab, key=lambda x: (str(x[0]), x[1])):
            hs = tab[k]
            ins = [h for h in hs if h.get('inside')]
            if not hs:
                continue
            W = k[3]
            e = [h['esc'] for h in ins]
            wok = sum(1 for x in e if x <= W * WALK) / max(1, len(e))
            sok = sum(1 for x in e if x <= W * SWING) / max(1, len(e))
            rok = sum(1 for x in e if x <= max(0, W - 5) * WALK) / max(1, len(e))
            print(f'{k[0]:4s} {k[1]:4d} K{k[2]} {W:3d} {k[4]:2d} | {len(hs):3d} {100 * len(ins) / len(hs):5.1f}% | '
                  f'{(sum(e) / len(e)) if e else 0:5.2f} / {max(e) if e else 0:5.2f} | {100 * wok:5.1f}% {100 * sok:5.1f}% {100 * rok:5.1f}%')

print()
print('== no-walk events (the escape was longer than the walk could cover before the hit), per pattern, melee/ranged dash r5')
for key in sorted(runs):
    force, pol, dodge, react, spr = key
    if dodge == 'none':
        continue
    rs = runs[key]
    c = defaultdict(int)
    for r in rs:
        for x in r['stats'].get('nowalk', []):
            c[(pname(force, x[7]), x[1], x[2])] += 1
    un = defaultdict(int)
    for r in rs:
        for x in r['stats'].get('unavoid', []):
            un[pname(force, x[4])] += 1
    print(f'{"BF" if force == 2 else "GD"} {pol:6s} {dodge:4s} r{react}: nowalk ' + ', '.join(f'{a}:{b}{"" if cc == 1 else ""}({d}) x{cc}' for (a, b, d), cc in sorted(c.items())) +
          ' | unavoid ' + ', '.join(f'{a} x{b}' for a, b in sorted(un.items())))

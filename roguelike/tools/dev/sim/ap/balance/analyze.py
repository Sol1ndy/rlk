#!/usr/bin/env python3
"""analyze.py: the plan 9.7 table from apfair runs (batch.py outputs).

    python3 analyze.py <label> [label ...] [--gd <gd label>] [--out <file>]

Every row says its measure, the value, the target / band / gate and ok / FAIL / n/a. The static rows cite the suites that
check them. The Guardian reference is the gd label (the Lv4 player vs L4 on this harness; it reproduces S:az/harness's
gdref seed by seed).
"""
import glob
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
args = sys.argv[1:]
gd_label = 'gd'
out = None
labels = []
i = 0
while i < len(args):
    if args[i] == '--gd':
        gd_label = args[i + 1]
        i += 2
    elif args[i] == '--out':
        out = args[i + 1]
        i += 2
    else:
        labels.append(args[i])
        i += 1

RUNS = []
for lb in labels:
    for f in sorted(glob.glob(str(HERE / 'out' / lb / '*.json'))):
        r = json.loads(Path(f).read_text(encoding='utf-8'))
        r['_label'] = lb
        RUNS.append(r)
GD = [json.loads(Path(f).read_text(encoding='utf-8')) for f in sorted(glob.glob(str(HERE / 'out' / gd_label / '*.json')))]
LINES = []


def say(s=''):
    LINES.append(s)
    print(s)


def sel(runs, **kw):
    return [r for r in runs if all(r.get(k) == v for k, v in kw.items())]


def lost(r, ph=None):
    return sum((d[3] or 0) for d in r['dmg'] if ph is None or d[5] == ph)


def rate(runs, ph):
    """mean % max HP per minute in phase ph over the runs."""
    v = []
    for r in runs:
        t = r['phases'].get(ph, 0)
        if t > 0:
            v.append(100.0 * lost(r, ph) / r['hp'] / (t / 1200.0))
    return sum(v) / len(v) if v else None


def worst_window(r, w=40, phs=None):
    ds = [d for d in r['dmg'] if (d[3] or 0) > 0 and (phs is None or d[5] in phs)]
    best = 0
    for d in ds:
        best = max(best, sum(e[3] for e in ds if d[0] <= e[0] < d[0] + w))
    return 100.0 * best / r['hp']


LONG = {3: 160, 2: 140, 4: 130, 32: 224, 35: 72, 31: 92, 33: 113, 34: 87}   # pattern lengths > 120 t use 60-t windows


def worst_cast(r):
    """the largest same-pattern damage inside one cast window (<= 120-t casts: 120 t; longer casts: the worst 60 t);
    the Q2 blast excluded: any pattern-32 hit above 10 % max HP (the field ticks are 2-3 %; fix 10-22f: the old test,
    a single hit of >= 50 % max HP, let a lethal blast through whose loss was capped by an agent already below half HP)."""
    ds = [d for d in r['dmg'] if (d[3] or 0) > 0 and not (d[4] == 32 and d[3] > 0.1 * r['hp'])]
    best, at = 0, None
    for d in ds:
        w = 60 if LONG.get(d[4], 0) > 120 else 120
        v = sum(e[3] for e in ds if e[4] == d[4] and d[0] <= e[0] < d[0] + w)
        if v > best:
            best, at = v, d[4]
    return 100.0 * best / r['hp'], at


def mean(v):
    v = [x for x in v if x is not None]
    return sum(v) / len(v) if v else None


def fmt(v, nd=1):
    return 'n/a' if v is None else (f'{v:.{nd}f}' if isinstance(v, float) else str(v))


ROWS = []


def row(name, value, target, ok):
    ROWS.append((name, value, target, ok))
    say(f'{"ok  " if ok is True else ("FAIL" if ok is False else "n/a ")} | {name:62} | {value:28} | {target}')


# ------------------------------------------------------------------ the Guardian reference
gref = {}
for pol, dodge in (('stand', 'none'), ('melee', 'walk'), ('ranged', 'walk')):
    rs = sel(GD, policy=pol, dodge=dodge)
    gref[pol] = rate(rs, 'gd')
say('Guardian reference (gd, Lv4 vs L4, 3 seeds x 3 min): stand %s / melee walk %s / ranged walk %s %% max HP per min'
    % tuple(fmt(gref[k]) for k in ('stand', 'melee', 'ranged')))
say()

# ------------------------------------------------------------------ P1 / P3 rates
for ph in ('p1', 'p3'):
    for pol, dodge, ch in (('stand', 'none', 'sword'), ('melee', 'walk', 'sword'), ('ranged', 'walk', 'bow')):
        rs = sel(RUNS, mode=ph, policy=pol, dodge=dodge, char=ch)
        v = rate(rs, ph)
        g = gref.get(pol)
        ratio = v / g if (v is not None and g) else None
        row(f'{ph.upper()} {pol} {dodge} %max/min vs 0.9x Guardian', f'{fmt(v)} = {fmt(ratio, 2)}x (n {len(rs)})',
            '0.72-1.08x (target 0.90x)', None if ratio is None else 0.72 <= ratio <= 1.08)

# whole fight HP lost per agent (Guardian kill runs on this harness: melee walk sword 84.5 %/min x 95 s, ranged walk bow
# 65.7 %/min x 92 s: S:az/harness/guardian_m0.txt section 3, reproduced here by the gd calibration)
GWHOLE = {'melee': 84.5 * 95 / 60, 'ranged': 65.7 * 92 / 60}
for pol, ch in (('melee', 'sword'), ('ranged', 'bow')):
    rs = sel(RUNS, mode='whole', policy=pol, dodge='walk', char=ch, mult=1.0)
    v = mean([100.0 * lost(r) / r['hp'] for r in rs])
    row(f'whole fight HP lost, {pol} walk {ch} (% max HP)', f'{fmt(v)} (n {len(rs)})',
        f'<= 2.5x Guardian whole fight = {2.5 * GWHOLE[pol]:.0f}', None if v is None else v <= 2.5 * GWHOLE[pol])

# worst 40 t window, walkers
for pol, ch in (('melee', 'sword'), ('ranged', 'bow')):
    rs = [r for r in RUNS if r['policy'] == pol and r['dodge'] == 'walk' and r['char'] == ch and r['mode'] in ('p1', 'p3', 'whole')]
    v = max([worst_window(r) for r in rs], default=None)
    row(f'worst 40 t window, {pol} walk (% max HP)', f'{fmt(v)} (n {len(rs)})', '<= 45', None if v is None else v <= 45)

# one cast, stand agent
rs = [r for r in RUNS if r['policy'] == 'stand' and r['mode'] in ('p1', 'p3')]
wc = [worst_cast(r) for r in rs]
v = max(wc, default=(None, None))
row('all hits of one cast, stand agent (% max HP; Q2 blast excluded)', f'{fmt(v[0])} (pattern {v[1]})', '<= 60',
    None if v[0] is None else v[0] <= 60)
row('dash-only hits per 40 t (static)', 'pat_p1 / pat_p3 TABLE checks', '<= 2, >= 6 t apart', True)

# undodgeable share, walkers
rs = [r for r in RUNS if r['dodge'] == 'walk' and r['policy'] in ('melee', 'ranged') and r['mode'] in ('p1', 'p3')]
nd = sum(d[3] or 0 for r in rs for d in r['dmg'] if d[6] == 1)
tot = sum(d[3] or 0 for r in rs for d in r['dmg'])
v = 100.0 * nd / tot if tot else None
row('undodgeable share of damage, walkers (P1 + P3)', f'{fmt(v)} %', '<= 25 %', None if v is None else v <= 25)

# perfect dasher
for ph in ('p1', 'p3'):
    for pol, ch in (('melee', 'sword'), ('ranged', 'bow')):
        rs = sel(RUNS, mode=ph, policy=pol, dodge='dash', char=ch)
        v = rate(rs, ph)
        lim = 0.3 * gref['melee'] if gref.get('melee') else None
        row(f'perfect dasher {ph.upper()} {pol} dash %max/min', f'{fmt(v)} (n {len(rs)})', f'<= 0.3x Guardian walker = {fmt(lim)}',
            None if (v is None or lim is None) else v <= lim)

# positional
f_ = rate(sel(RUNS, mode='p1', policy='melee_front'), 'p1')
b_ = rate(sel(RUNS, mode='p1', policy='melee_back'), 'p1')
v = (1 - f_ / b_) * 100 if (f_ is not None and b_) else None
row('positional (P1): FRONT melee walker vs BACK melee walker', f'front {fmt(f_)} back {fmt(b_)}: {fmt(v)} % less',
    '>= 25 % less', None if v is None else v >= 25)

# Q2 (fix 10-22f: the field ticks 2 % every 10 t from 20 t after the banner, before any dome stands; the domes at
# random layouts, the player's dome forming first 34 t after the banner)
def cast_lost(r, c):
    """% max HP lost during one cast (every player damage event between its start and its end)."""
    hpmax = 268.0
    return 100.0 * sum(d[3] for d in r['dmg'] if c['t0'] <= d[0] <= c.get('end', 10 ** 9)) / hpmax


for q in ('dome', 'late', 'early'):
    rs = sel(RUNS, mode='q2', q2mode=q)
    cs = [c for r in rs for c in r['casts']]
    bl = sum(c['blast'] for c in cs)
    tk = max([c['ticks'] for c in cs], default=None)
    tkm = mean([c['ticks'] for c in cs]) if cs else None
    de = sum(c['deaths'] for c in cs)
    lost_c = [cast_lost(r, c) for r in rs for c in r['casts']]
    lv = f'HP lost per cast mean {fmt(mean(lost_c))} / max {fmt(max(lost_c))} % max HP' if lost_c else ''
    if q == 'dome':
        row('Q2 walk-to-nearest-dome agent: blast hits / max ticks per cast / deaths', f'{bl} / {fmt(tk)} (mean {fmt(tkm)}) / {de} '
            f'({len(cs)} casts, {len(rs)} seeds); {lv}', '0 / <= 3 (the 2 pre-dome ticks + 1) / 0 over 9 seeds',
            None if not cs else (bl == 0 and tk <= 3 and de == 0))
    elif q == 'late':
        row('Q2 late agent (moves at dome 1 + 40 t): deaths', f'{de} ({len(cs)} casts; ticks max {fmt(tk)}, blast hits {bl}); {lv}', '0',
            None if not cs else de == 0)
    else:
        row('Q2 early leaver (leaves at the blast, from full HP): deaths', f'{de} ({len(cs)} casts, blast hits {bl}); {lv}', '0 (survives)',
            None if not cs else de == 0)
row('human jump model (static)', 'pat_p1 / pat_p3: jumpable => mbHzY1 <= 7', 'every documented jump dodge succeeds', True)

# P2
def p2len(rs):
    v = [r['phases'].get('p2', 0) / 20.0 for r in rs if r['end'] == 'stage_end']
    return (mean(v), len(v), len(rs))


for label, kw, band in (('plan agent, item-less sword', dict(char='sword', mult=1.0, agent='plan'), (85, 120)),
                        ('plan agent, sword x1.75 (items)', dict(char='sword', mult=1.75, agent='plan'), (50, 75)),
                        ('plan agent, bow x2.5 (strongest)', dict(char='bow', mult=2.5, agent='plan'), (30, 9999))):
    rs = sel(RUNS, mode='p2', **kw)
    m, n, nn = p2len(rs)
    row(f'P2 stage length (s), {label}', f'{fmt(m)} ({n}/{nn} won)', f'{band[0]}-{band[1] if band[1] < 9999 else ""}'.rstrip('-') if band[1] < 9999 else f'>= {band[0]}',
        None if m is None else (band[0] <= m <= band[1] and n == nn))
sw = sel(RUNS, mode='p2', char='sword', mult=1.0, agent='plan')
sw_dps = mean([sum(d[1] for d in r['dealt']) / max(1, r['ticks']) for r in sw])
for ch in ('sword', 'bow', 'catalyst'):
    rs = sel(RUNS, mode='p2', char=ch, mult=1.0, agent='plan')
    dps = mean([sum(d[1] for d in r['dealt']) / max(1, r['ticks']) for r in rs])
    rel = dps / sw_dps if (dps and sw_dps) else None
    fails = sum(1 for r in rs if r['fails'] > 0)
    row(f'P2 failures, plan agent, {ch} ({fmt(rel, 2)}x sword DPS)', f'{fails} / {len(rs)}', '0 / 9 (chars >= 0.6x)',
        None if not rs else (fails == 0 if (rel or 0) >= 0.6 else True))
rs = sel(RUNS, mode='p2', agent='nearest')
fails = sum(1 for r in rs if r['fails'] > 0)
m, n, nn = p2len(rs)
row('P2 failures, "nearest target" agent, item-less sword', f'{fails} / {len(rs)} (len {fmt(m)} s)', '<= 1 / 9',
    None if not rs else fails <= 1)
rs = sel(RUNS, mode='p2', agent='idle')
ft = mean([r['fail_t'][0] / 20.0 for r in rs if r.get('fail_t')])
row('P2 idle agent: the Heart at 0', f'{fmt(ft)} s (n {len(rs)})', '30-45 s', None if ft is None else 30 <= ft <= 45)
p2r = rate(sel(RUNS, mode='p2', char='sword', mult=1.0, agent='plan'), 'p2')
p1r = rate(sel(RUNS, mode='p1', policy='melee', dodge='walk', char='sword'), 'p1')
row('P2 HP loss per minute vs the P1 rate (melee walk sword)', f'{fmt(p2r)} vs {fmt(p1r)}', '<= 0.8x P1',
    None if (p2r is None or p1r is None) else p2r <= 0.8 * p1r)
# one 포식성 bite chain on a standing player (static: the chain coefficients through the 9.2 hit grid, HP = 2.83 x raw)
chain = [0.67, 0.34, 0.20, 0.13]
hpc = sum(2.83 * math.floor(0.18 * c * 100) for c in chain)
row('one 포식성 bite chain on a standing player (static, 9.2 grid)', f'{100 * hpc / 268:.1f} % max HP', '<= 30 %', 100 * hpc / 268 <= 30)
rs = sel(RUNS, mode='whole', policy='melee', dodge='walk', char='sword', mult=1.0)
tk = mean([r['ticks'] / 1200.0 for r in rs if r['end'] == 'dead'])
row('full fight, item-less sword agent (min)', f'{fmt(tk, 2)} ({sum(1 for r in rs if r["end"] == "dead")}/{len(rs)} kills)', '<= 6.5',
    None if tk is None else tk <= 6.5)
m, n, nn = p2len(sel(RUNS, mode='p2', char='sword', mult=1.0, agent='plan'))
row('apfair P2 vs p2sim_rev W7 (item-less sword 105 s)', f'{fmt(m)} s = {fmt((m / 105.0 - 1) * 100 if m else None)} %',
    'within 15 %', None if m is None else abs(m / 105.0 - 1) <= 0.15)
say()
nok = sum(1 for r in ROWS if r[3] is True)
nf = sum(1 for r in ROWS if r[3] is False)
say(f'rows: {len(ROWS)}, ok {nok}, FAIL {nf}, n/a {len(ROWS) - nok - nf}')
# per-pattern P1 / P3 contribution (melee walk sword): HP lost per pattern
for ph in ('p1', 'p3'):
    rs = sel(RUNS, mode=ph, policy='melee', dodge='walk', char='sword')
    by = {}
    for r in rs:
        for d in r['dmg']:
            if d[5] == ph:
                by[d[4]] = by.get(d[4], 0) + (d[3] or 0)
    tot = sum(by.values()) or 1
    say(f'{ph} melee walk, HP lost by pattern id (share): ' + ', '.join(f'{k}: {v} ({100 * v / tot:.0f} %)' for k, v in sorted(by.items())))
    rs = sel(RUNS, mode=ph, policy='stand')
    by = {}
    for r in rs:
        for d in r['dmg']:
            if d[5] == ph:
                by[d[4]] = by.get(d[4], 0) + (d[3] or 0)
    tot = sum(by.values()) or 1
    say(f'{ph} stand, HP lost by pattern id (share): ' + ', '.join(f'{k}: {v} ({100 * v / tot:.0f} %)' for k, v in sorted(by.items())))
if out:
    Path(out).write_text('\n'.join(LINES) + '\n', encoding='utf-8')

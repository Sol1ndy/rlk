#!/usr/bin/env python3
"""Batch of fgfair fights: python3 batch.py <label> <spec> [jobs]
spec: comma list of force:policy:dodge:char:seed[:n[:real_hp[:react[:tri]]]] or a preset name."""
import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))


def one(args):
    label, force, policy, dodge, char, seed, n, real_hp, react, tri, extra = args
    sys.path.insert(0, HERE)
    if extra.get('FDP'):
        os.environ['FDP'] = extra['FDP']
    import fgfair as F
    t = time.time()
    s, ag, tr, t0 = F.fight(force=force, policy=policy, dodge=dodge, react=react, n=n, seed=seed, char=char,
                            real_hp=real_hp, until_dead=real_hp, tri_aware=tri)
    st = {k: v for k, v in ag.stats.items()}
    hz = [dict(v, id=k) for k, v in s.hzrec.items()]
    b = F.body_of(s)
    res = dict(force=force, policy=policy, dodge=dodge, char=char, seed=seed, n=n, real_hp=real_hp, react=react, tri=tri,
               t0=t0, t_end=s.t, dmg=s.dmg, dodges=s.dodges, stats=st, fields=tr.fields, tri_t=tr.tri, dead_t=tr.dead_t,
               dealt=s.dealt, hz=hz, secs=time.time() - t,
               hp_end=(s.sc(('e', b.id), 'mhpC') if b else None), hp_max=(s.sc(('e', b.id), 'mhpM') if b else None))
    out = os.path.join(HERE, 'out', label)
    os.makedirs(out, exist_ok=True)
    name = f'{force}_{policy}_{dodge}_{char}_r{react}_s{seed}{"_hp" if real_hp else ""}{"" if tri else "_naive"}.json'
    json.dump(res, open(os.path.join(out, name), 'w'), default=str)
    return name, round(time.time() - t, 1)


PRESETS = {
    # the butterfly balance's three behaviours (react 5, 3 seeds x 3 min), FG and GD
    'base': [(f, p, d, c, s, 3600, False, 5, True) for f in (3, 1) for (p, d, c) in
             (('stand', 'none', 'sword'), ('melee', 'walk', 'sword'), ('ranged', 'walk', 'bow')) for s in (11, 22, 33)],
    'dash': [(f, p, 'dash', c, s, 3600, False, 5, True) for f in (3, 1) for (p, c) in
             (('melee', 'sword'), ('ranged', 'bow')) for s in (11, 22, 33)],
    'fgbase': [(3, p, d, c, s, 3600, False, 5, True) for (p, d, c) in
               (('stand', 'none', 'sword'), ('melee', 'walk', 'sword'), ('ranged', 'walk', 'bow')) for s in (11, 22, 33)],
    'fgttk': [(3, p, d, c, s, 14000, True, 5, True) for (p, d, c) in
              (('melee', 'walk', 'sword'), ('melee', 'walk', 'navia'), ('ranged', 'walk', 'bow'), ('ranged', 'walk', 'catalyst'))
              for s in (11, 22, 33)],
    'gdttk': [(1, p, d, c, s, 14000, True, 5, True) for (p, d, c) in
              (('melee', 'walk', 'sword'), ('melee', 'walk', 'navia'), ('ranged', 'walk', 'bow'), ('ranged', 'walk', 'catalyst'))
              for s in (11, 22, 33)],
    'ttk': [(f, p, d, c, s, 14000, True, 5, True) for f in (3, 1) for (p, d, c) in
            (('melee', 'walk', 'sword'), ('melee', 'walk', 'navia'), ('ranged', 'walk', 'bow'), ('ranged', 'walk', 'catalyst'),
             ('melee', 'dash', 'sword'))
            for s in (11, 22, 33)],
}


if __name__ == '__main__':
    label = sys.argv[1]
    spec = sys.argv[2]
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    extra = {'FDP': os.environ.get('FDP', '')}
    if spec in PRESETS:
        todo = [(label,) + t + (extra,) for t in PRESETS[spec]]
    else:
        todo = []
        for item in spec.split(','):
            p = item.split(':')
            f, pol, dod, ch, sd = int(p[0]), p[1], p[2], p[3], int(p[4])
            n = int(p[5]) if len(p) > 5 else 3600
            hp = bool(int(p[6])) if len(p) > 6 else False
            rc = int(p[7]) if len(p) > 7 else 5
            tri = bool(int(p[8])) if len(p) > 8 else True
            todo.append((label, f, pol, dod, ch, sd, n, hp, rc, tri, extra))
    with Pool(jobs) as pool:
        for r in pool.imap_unordered(one, todo):
            print(*r, flush=True)

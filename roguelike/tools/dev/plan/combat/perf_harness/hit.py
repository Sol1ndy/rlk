"""Per-hit cost: one basic melee hit through the real combat/apply, small vs late inventory (no kill / kill)."""
import sys, collections, copy, random
sys.path.insert(0, '.')
from scen import *
random.seed(3)

def mob(s, hp):
    e = Ent('husk', (1.5, 64.0, 2.5), (0.0, 0.0), ['rlk_mob', 'rlk_zmob'])
    s.ents.append(e)
    for o, v in (('mhpM', hp), ('mhpC', hp), ('mlv', 30), ('mres', 0), ('elAct', 0), ('hbT', 0)):
        s.setsc(('e', e.id), o, v)
    return e

def strike(s, tgt, dmg, elem=0):
    pl = s.player
    pc = pctx(s)
    s.call('rlk:combat/melee_begin', pc)
    s.call('rlk:combat/clear_atkflags', pc)
    for k, v in (('#dmg', dmg), ('#elem', elem), ('#elU', 1000 if elem else 0), ('#icd', 1), ('#crit', 0),
                 ('#stunHit', 1), ('#hitLanded', 0), ('#bowHit', 0), ('#lunar', 0), ('#tfm', 0), ('#trueDmg', 0)):
        s.setsc(k, 'tmp', v)
    s.setsc('#basic', 'itv', 1)
    s.setsc('#dmgBase', 'tmp', dmg)
    a = s.n
    snap = dict(s.incl)
    m0 = sum(s.macro_lines.values())
    s.call('rlk:combat/apply', Ctx(tgt, tuple(tgt.pos), tuple(tgt.rot)))
    s.call('rlk:combat/on_hit', pc) if (s.sc('#hitLanded', 'tmp') or 0) else None
    s.setsc('#basic', 'itv', 0)
    parts = {f: s.incl[f] - snap.get(f, 0) for f in s.incl if s.incl[f] - snap.get(f, 0)}
    return s.n - a, parts, sum(s.macro_lines.values()) - m0

for tag, items, stars in (('small(3)', SMALL, 0), ('late(18,★★★)', LATE, 3)):
    s, pl = world(items, stars)
    for k in range(3):
        m = mob(s, 10**7)
        n, parts, ml = strike(s, m, 500, elem=4 if k else 0)
        print(f'{tag} hit {k} (elem {4 if k else 0}): {n} commands, macro lines {ml}')
    top = sorted(parts.items(), key=lambda x: -x[1])[:14]
    for f, v in top:
        print(f'     {f:40s} {v}')
    m = mob(s, 100)
    n, parts, ml = strike(s, m, 500)
    print(f'{tag} killing hit: {n} commands, macro lines {ml}; on_kill {parts.get("rlk:items/hook/on_kill", 0)} gold_drop {parts.get("rlk:combat/gold_drop", 0)}')
    print('   errors', s.errors.most_common(4))

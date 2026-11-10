#!/usr/bin/env python3
"""scen.py: commands per tick by function, small vs late-game inventory, out of combat vs combat churn.

    python3 scen.py [dp]

Tick model (rlk:tick order, the parts that touch the player / items): F5 ride_tick's consumable lines (view/ride_tick
23-25, view/tick runs before player/tick) -> player/tick (real, everything inside) -> after player/tick: the combat
inputs (skill cast / energy gain land here, as combat/atkblock_manage and char/particle_tick do in rlk:tick).
"""
import collections
import copy
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from psim import PSim, Ent, Ctx, pctx  # noqa: E402

DP = Path(sys.argv[1] if len(sys.argv) > 1 else '/home/user/rlk/roguelike')
FN = DP / 'data/rlk/function'
RIDE = (FN / 'view/ride_tick.mcfunction').read_text(encoding='utf-8').split('\n')
CONS = [l for l in RIDE if 'minecraft:consumable' in l and l.startswith('execute if items')]
assert len(CONS) == 3, CONS

SMALL = ['whetstone', 'hood', 'pebble']
LATE = ['sword_hwamu', 'demonomicon', 'sword_kirion', 'crimson_moon', 'mech_heart', 'pain_despair', 'source_samples',
        'stormy_eye', 'moon_chalice', 'ember_oath', 'night_stars', 'ice_quill', 'salon_invite', 'sealed_sword',
        'star_wisp', 'maple_leaf', 'old_slate', 'lucky_coin']           # 18 = invCap max: 2 mythic weapons ... trinkets
KEY = ['rlk:items/equip_scan', 'rlk:player/inv/manage', 'rlk:items/stat_light', 'rlk:items/hook/tick_player',
       'rlk:items/hook/stat_buffs', 'rlk:engravings/tick', 'rlk:engravings/scan', 'rlk:engravings/info_build',
       'rlk:items/scan_loop', 'rlk:items/scan_add', 'rlk:player/inv/sync', 'rlk:player/inv/place_items',
       'rlk:player/inv/collect_loop', 'rlk:char/tick', 'rlk:player/hotbar/tick', 'rlk:player/update_item',
       'rlk:player/hud/tick', 'rlk:lvup/tick', 'rlk:invd/tick', 'rlk:char/motion/tick', 'rlk:player/apply_attributes',
       'rlk:player/health_tick', 'rlk:player/elem_tick', 'rlk:player/bol/tick', 'rlk:view/shield_fx']


def world(items, stars=0, cap=18):
    s = PSim(FN)
    pl = Ent('player', (0.5, 64.0, 0.5), (0.0, 0.0), ['player', 'rlk_body'])
    s.ents.append(pl)
    s.player = pl
    s.call('rlk:load', Ctx(None, (0, 0, 0), (0, 0)))
    s.cache['rlk:perf/ride_cons'] = CONS
    P = ('e', pl.id)
    s.setsc(P, 'invCap', cap)
    s.setsc(P, 'level', 30)
    for _ in range(5):
        tick(s)
    for i in items:
        s.call('rlk:items/give', pctx(s), {'id': i})
        tick(s)
        tick(s)
        if stars:
            s.setsc(i, 'enhL', stars)
            s.storage.setdefault('rlk:pinv', {}).setdefault('enh', {})[i] = stars
    # settle: hotbar / skill items / consumable / scans
    for _ in range(30):
        tick(s)
    return s, pl


def tick(s, after=None):
    s.t += 1
    c = pctx(s)
    s.call('rlk:perf/ride_cons', c)
    s.call('rlk:player/tick', c)
    if after:
        after(s)


def measure(s, n, after=None):
    P = ('e', s.player.id)
    per, by = [], collections.Counter()
    scans = 0
    inv0 = s.inv_changes
    where0 = copy.copy(s.inv_change_where)
    for k in range(n):
        a = s.n
        b = dict(s.incl)
        sc0 = s.ncall['rlk:items/equip_scan']
        tick(s, (lambda s, k=k: after(s, k)) if after else None)
        per.append(s.n - a)
        for f in KEY:
            by[f] += s.incl[f] - b.get(f, 0)
        scans += s.ncall['rlk:items/equip_scan'] - sc0
    where = {k: v - where0.get(k, 0) for k, v in s.inv_change_where.items() if v - where0.get(k, 0)}
    return per, by, scans, s.inv_changes - inv0, where


def combat_after(s, k):
    """Combat churn on the player: the skill goes on cooldown (18 s) when ready, energy +3pt every 15 ticks until the
    burst is cast at full (then 0), as combat/atkblock_manage and the particle absorb do after player/tick."""
    P = ('e', s.player.id)
    if (s.sc(P, 'skillCd') or 0) <= 0 and k % 40 == 5:
        s.setsc(P, 'skillCd', 360)
    if k % 15 == 0:
        e = (s.sc(P, 'energy') or 0) + 300
        if e >= 6000:
            e = 0
            s.setsc(P, 'burstCd', 300)
        s.setsc(P, 'energy', e)


def report(tag, res, n):
    per, by, scans, invch, where = res
    per_s = sorted(per)
    avg = sum(per) / len(per)
    print(f'{tag}: ticks {n} avg {avg:.0f} cmds/tick, p50 {per_s[len(per)//2]}, max {per_s[-1]}; equip_scan runs {scans} '
          f'({scans / n * 20:.2f}/s), player inventory changes {invch} {dict(sorted(where.items(), key=lambda x: -x[1])[:6])}')
    for f in KEY:
        if by[f]:
            print(f'    {f:34s} {by[f] / n:8.1f}/tick  ({by[f]})')
    return avg, per_s[-1]


def one_scan(s):
    """Cost of one dirty pass (inv/manage + equip_scan) and its parts, macro instantiations."""
    P = ('e', s.player.id)
    c = pctx(s)
    snap = dict(s.incl)
    m0 = copy.copy(s.macro_n)
    mb0 = copy.copy(s.macro_bytes)
    a = s.n
    s.call('rlk:player/inv/manage', c)
    man = s.n - a
    b = s.n
    s.call('rlk:items/equip_scan', c)
    eq = s.n - b
    parts = {f: s.incl[f] - snap.get(f, 0) for f in s.incl if s.incl[f] - snap.get(f, 0)}
    mac = {f: s.macro_n[f] - m0.get(f, 0) for f in s.macro_n if s.macro_n[f] - m0.get(f, 0)}
    mby = {f: s.macro_bytes[f] - mb0.get(f, 0) for f in s.macro_bytes if s.macro_bytes[f] - mb0.get(f, 0)}
    return man, eq, parts, mac, mby


if __name__ == '__main__':
    t0 = time.time()
    out = {}
    for tag, items, stars in (('small(3)', SMALL, 0), ('late(18,★★★)', LATE, 3)):
        s, pl = world(items, stars)
        P = ('e', pl.id)
        print(f'== {tag}: order {s.storage["rlk:pinv"].get("order")} it_ held: '
              f'{sum(1 for (h, o), v in s.scores.items() if h == P and o.startswith("it_") and v)}')
        man, eq, parts, mac, mby = one_scan(s)
        print(f'  one dirty pass: inv/manage {man} + equip_scan {eq} = {man + eq} commands (x2: invDirty 2)')
        top = sorted(parts.items(), key=lambda x: -x[1])
        for f, v in top[:22]:
            print(f'    {f:40s} {v:6d}  macro inst {mac.get(f, 0):4d}  macro chars {mby.get(f, 0):7d}')
        print(f'  macro instantiations in the pass: {sum(mac.values())}, substituted chars {sum(mby.values())}, '
              f'distinct arg sets: scan_add {len(s.macro_args["rlk:items/scan_add"])}, scan_count {len(s.macro_args["rlk:items/scan_count"])}')
        for f, v in sorted(mac.items(), key=lambda x: -x[1])[:10]:
            print(f'      macro {f:40s} {v}')
        # idle (out of combat): skill ready, energy full
        s.setsc(P, 'skillCd', 0)
        s.setsc(P, 'energy', 9999999)
        for _ in range(5):
            tick(s)
        out[(tag, 'idle')] = report(f'  {tag} out of combat', measure(s, 400), 400)
        out[(tag, 'combat')] = report(f'  {tag} combat churn', measure(s, 400, combat_after), 400)
        if s.errors:
            print('  sim errors:', s.errors.most_common(8))
    print('wall', round(time.time() - t0, 1), 's')

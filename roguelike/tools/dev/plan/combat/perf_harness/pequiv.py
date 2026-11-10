#!/usr/bin/env python3
"""pequiv.py <dpA> <dpB> [--mode raw|settled] [--only name,...]: run the same scenario scripts on two trees and diff
the full state (all scores, all storage, the player inventory with components, entities) at every checkpoint.

raw:     dumps as they are (for trees whose dirty-pass timing is the same, e.g. A vs A+B).
settled: before each dump run rlk:items/stat_light once on both (stat_light restarts the 2-tick scanTick cadence, so trees
         with different pass timing are compared after the same recompute) and ignore scanTick / hudKey (the pass's
         HUD redraw request).
Scratch the passes leave behind (named in SCRATCH) is reported separately, not as a difference.
"""
import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pworld import SMALL, LATE, world, tick, combat_after, f_press, dump, diff, pctx  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('a')
ap.add_argument('b')
ap.add_argument('--mode', default='raw')
ap.add_argument('--only', default='')
ap.add_argument('-v', action='store_true')
args = ap.parse_args()

# scratch storage the dirty pass leaves behind (work lists / last-loop values): never read before being rewritten
SCRATCH = ('rlk:pinv.pcnt', 'rlk:pinv.cscan', 'rlk:pinv.ccur', 'rlk:pinv.ccnt', 'rlk:pinv.cbase',
           'rlk:scan.', 'rlk:eng.q', 'rlk:eng.b.', 'rlk:eng.bt', 'rlk:eng.e')
SCRATCH_SC = {('#syO', 'tmp'), ('#syN', 'tmp'), ('#syP', 'tmp'), ('#syH', 'tmp'), ('#scT', 'tmp'), ('#scO', 'tmp'),
              ('#scF', 'tmp'), ('#scM', 'tmp'), ('#scN', 'tmp'), ('#want', 'eng'), ('#scEp', 'eqEp'),
              ('PLAYER', 'eqEp'),
              # last-loop values the item scan leaves (the full scan ends on the last registry id, the fast scan on the last
              # held id); every reader sets them first: #cnt (ditem/retrieve_p), #enh (all enh_get callers, tune/apply),
              # #cntF (scan_add_prep), #fA/#fD/#fC (tune/fac before every use)
              ('#cnt', 'tmp'), ('#cntF', 'tmp'), ('#enh', 'tmp'), ('#fA', 'tmp'), ('#fD', 'tmp'), ('#fC', 'tmp')}

MIX = ['sword_hwamu', 'whetstone', 'whetstone', 'old_slate', 'hood', 'demonomicon', 'old_slate', 'pebble', 'mech_heart',
       'sealed_sword', 'lucky_coin', 'crimson_moon']
MIX_ENH = {'sword_hwamu': 3, 'whetstone': 1, 'old_slate': 2, 'demonomicon': 3, 'mech_heart': 1}


def P(s):
    return ('e', s.player.id)


def run(dp, script, mode):
    out = []
    st = {'s': None}

    def cp(name):
        s = st['s']
        if mode == 'settled':
            s.call('rlk:items/stat_light', pctx(s))
        out.append((name, dump(s)))

    for step in script:
        kind = step[0]
        if kind == 'world':
            _, items, stars, enh, cap, char = step
            s, pl = world(dp, [], 0, cap=cap)
            st['s'] = s
            if char:
                s.call('rlk:char/select', pctx(s), {'id': char})
                for _ in range(5):
                    tick(s)
            for i in items:
                s.call('rlk:items/give', pctx(s), {'id': i})
                tick(s)
                tick(s)
                stv = (enh or {}).get(i, stars)
                for _k in range(max(0, (stv or 0) - ((s.storage.get('rlk:pinv', {}).get('enh', {}).get(i)) or 0))):
                    s.call('rlk:items/enh_add', pctx(s), {'id': i})        # the game's path (ench/pick), which also marks dirty
                    s.setsc(('e', s.player.id), 'invDirty', 2)
            for _ in range(30):
                tick(s)
            cp('setup')
            continue
        s = st['s']
        if kind == 'idle':
            for _ in range(step[1]):
                tick(s)
        elif kind == 'combat':
            n, fd = step[1], step[2]
            for k in range(n):
                tick(s, lambda s, k=k: combat_after(s, k))
                if fd and k % fd == fd - 1:
                    f_press(s)
        elif kind == 'set':
            s.setsc(P(s), step[1], step[2])
        elif kind == 'setfake':
            s.setsc(step[1], step[2], step[3])
        elif kind == 'call':
            s.call(step[1], pctx(s), step[2] if len(step) > 2 else None)
        elif kind == 'discard':                         # click an item in inventory.<n> onto the cursor (= discard)
            inv = s.player.data['inv']
            sl = f'inventory.{step[1]}'
            if sl in inv:
                inv['player.cursor'] = inv.pop(sl)
                s.call('rlk:player/inv/dirty', pctx(s))
        elif kind == 'swap':                           # move inventory.<a> <-> inventory.<b> (same count)
            inv = s.player.data['inv']
            a, b = f'inventory.{step[1]}', f'inventory.{step[2]}'
            inv[a], inv[b] = inv.get(b), inv.get(a)
            for k in (a, b):
                if inv[k] is None:
                    del inv[k]
            s.call('rlk:player/inv/dirty', pctx(s))
        elif kind == 'give':
            s.call('rlk:items/give', pctx(s), {'id': step[1]})
        elif kind == 'cp':
            cp(step[1])
        else:
            raise ValueError(kind)
    return out, st['s']


def base(items, stars=0, enh=None, cap=18, char=None):
    return [('world', items, stars, enh, cap, char)]


COMBAT = [('set', 'skillCd', 0), ('set', 'energy', 9999999), ('idle', 20), ('cp', 'idle'),
          ('combat', 120, 37), ('cp', 'combat120'), ('combat', 121, 0), ('cp', 'combat241'),
          ('set', 'skillCd', 0), ('set', 'burstCd', 0), ('idle', 45), ('cp', 'rest')]
EDIT = [('discard', 10), ('idle', 3), ('cp', 'discard'), ('swap', 9, 11), ('idle', 3), ('cp', 'swap'),
        ('give', 'pebble'), ('idle', 3), ('cp', 'give'), ('call', 'rlk:items/enh_add', {'id': 'pebble'}),
        ('set', 'invDirty', 2), ('idle', 3), ('cp', 'enh'),
        ('call', 'rlk:engravings/dev', {'id': 'guard', 'n': 3}), ('idle', 3), ('cp', 'engdev'),
        ('call', 'rlk:engravings/dev', {'id': 'guard', 'n': 0}), ('idle', 3), ('cp', 'engdev0'),
        ('idle', 205), ('cp', 'fallback')]
DEV = [('set', 'devMode', 1), ('idle', 3), ('give', 'hood'), ('idle', 3), ('cp', 'dev_give'),
       ('set', 'devMode', 0), ('idle', 3), ('cp', 'dev_off')]

SCEN = {
    'late18': base(LATE, 3) + COMBAT + EDIT + DEV,
    'small3': base(SMALL) + COMBAT + EDIT,
    'mix_dup_slate': base(MIX, 0, MIX_ENH, cap=14) + COMBAT + EDIT + DEV,
    'full_cap': base(LATE[:9], 2, cap=9) + [('give', 'pebble'), ('idle', 3), ('cp', 'over_cap')] + COMBAT,
    'navia': base(LATE[:6], 1, char='navia') + [('set', 'nvC', 3)] + COMBAT + [('set', 'nvC', 0), ('idle', 30), ('cp', 'nv0')],
    'nefer': base(LATE[6:12], 2, char='nefer') + [('set', 'nfC', 2)] + COMBAT,
    'clorinde': base(SMALL, 1, char='clorinde') + [('set', 'clNV', 40)] + COMBAT,
    'ronova': base(LATE[12:], 3, char='ronova') + [('set', 'rnEn', 2)] + COMBAT,
    'skirk': base(LATE[:4], 0, char='skirk') + [('set', 'skM', 1)] + COMBAT,
    'empty': base([]) + COMBAT + [('give', 'hood'), ('idle', 3), ('cp', 'first')],
}

only = [x for x in args.only.split(',') if x]
bad = 0
for name, script in SCEN.items():
    if only and name not in only:
        continue
    ra, sa = run(args.a, script, args.mode)
    rb, sb = run(args.b, script, args.mode)
    ig_sc = [lambda k: k in SCRATCH_SC]
    if args.mode == 'settled':
        ig_sc.append(lambda k: k[1] in ('scanTick', 'hudKey'))
    nd = 0
    scratch = set()
    for (na, da), (nb, db) in zip(ra, rb):
        d = diff(da, db, ignore_scores=ig_sc)
        real = [x for x in d if not any(x.startswith(f'storage {p}') for p in SCRATCH)]
        scratch |= {x.split(':')[0] for x in d if x not in real}
        if real:
            nd += 1
            print(f'  DIFF {name}/{na}: {len(real)}')
            for x in real[:12 if not args.v else 200]:
                print('     ', x)
    ea = {str(k): v for k, v in sa.errors.items() if 'health_tick' not in str(k) and 'hunger' not in str(k)}
    eb = {str(k): v for k, v in sb.errors.items() if 'health_tick' not in str(k) and 'hunger' not in str(k)}
    nerr = {k: v for k, v in eb.items() if ea.get(k) != v}
    held = sum(1 for (h, o), v in sb.scores.items() if h == ('e', sb.player.id) and o.startswith('it_') and v)
    nb_scan, nb_fast = sb.ncall['rlk:items/equip_scan'], sb.ncall['rlk:items/scan_held']
    paths = (f'scans fast {nb_fast}/{nb_scan}; collect runs '
             f'{sb.ncall["rlk:player/inv/collect_loop"] - sb.ncall["rlk:player/inv/collect_one"]}/{sb.ncall["rlk:player/inv/sync"]} syncs')
    print(f'{"ok  " if not nd else "FAIL"} {name}: {len(ra)} checkpoints, {nd} differ; held ids {held}, '
          f'order {len(sb.storage.get("rlk:pinv", {}).get("order", []))}; {paths}; scratch-only diffs {sorted(scratch)[:6]}'
          + (f'; new sim errors {list(nerr.items())[:3]}' if nerr else ''))
    bad += bool(nd)
print('EQUIV', 'PASS' if not bad else f'FAIL ({bad} scenarios)')
sys.exit(1 if bad else 0)

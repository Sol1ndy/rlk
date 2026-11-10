#!/usr/bin/env python3
"""pworld.py (lane P): the scen.py world with the F5 seat present and the whole F5 item step of view/ride_tick
(hand_wrap, then the three consumable lines), so that player/hotbar/wrap's seat gate is live; plus a full state dump.

tick(s) = view/ride_tick's item lines (view/tick runs before player/tick) -> the real rlk:player/tick -> `after`.
"""
import collections
import copy
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from psim import PSim, Ent, Ctx, pctx, snbt_dump  # noqa: E402

SMALL = ['whetstone', 'hood', 'pebble']
LATE = ['sword_hwamu', 'demonomicon', 'sword_kirion', 'crimson_moon', 'mech_heart', 'pain_despair', 'source_samples',
        'stormy_eye', 'moon_chalice', 'ember_oath', 'night_stars', 'ice_quill', 'salon_invite', 'sealed_sword',
        'star_wisp', 'maple_leaf', 'old_slate', 'lucky_coin']


def ride_lines(fn):
    ride = (fn / 'view/ride_tick.mcfunction').read_text(encoding='utf-8').split('\n')
    cons = [l for l in ride if 'minecraft:consumable' in l and l.startswith('execute if items')]
    assert len(cons) == 3, cons
    assert 'function rlk:view/hand_wrap' in ride
    return ['function rlk:view/hand_wrap'] + cons          # ride_tick order: hand_wrap (:20) then :23-25


def new_sim(dp, seat=True, char=None):
    fn = Path(dp) / 'data/rlk/function'
    s = PSim(fn)
    pl = Ent('player', (0.5, 64.0, 0.5), (0.0, 0.0), ['player', 'rlk_body'])
    s.ents.append(pl)
    s.player = pl
    s.call('rlk:load', Ctx(None, (0, 0, 0), (0, 0)))
    if seat:                                               # after load (load clears rlk_view entities)
        s.ents.append(Ent('armor_stand', (0.5, 66.0, 0.5), (0.0, 0.0), ['rlk_view', 'rlk_vseat', 'rlk_pet']))
    s.cache['rlk:perf/ride_items'] = ride_lines(fn)
    s.fn = fn
    return s, pl


def tick(s, after=None, ride=True):
    s.t += 1
    c = pctx(s)
    if ride:
        s.call('rlk:perf/ride_items', c)
    s.call('rlk:player/tick', c)
    if after:
        after(s)


def world(dp, items, stars=0, cap=18, seat=True, settle=30, enh=None):
    s, pl = new_sim(dp, seat)
    P = ('e', pl.id)
    s.setsc(P, 'invCap', cap)
    s.setsc(P, 'level', 30)
    for _ in range(5):
        tick(s)
    for i in items:
        s.call('rlk:items/give', pctx(s), {'id': i})
        tick(s)
        tick(s)
        st = (enh or {}).get(i, stars)
        for _k in range(max(0, (st or 0) - ((s.storage.get('rlk:pinv', {}).get('enh', {}).get(i)) or 0))):
            s.call('rlk:items/enh_add', pctx(s), {'id': i})        # the game's path (ench/pick), which also marks dirty
            s.setsc(('e', s.player.id), 'invDirty', 2)
    for _ in range(settle):
        tick(s)
    return s, pl


def combat_after(s, k):
    """scen.py's combat churn: skill on cooldown (18 s) when ready, energy +3 pt every 15 ticks, burst at full."""
    P = ('e', s.player.id)
    if (s.sc(P, 'skillCd') or 0) <= 0 and k % 40 == 5:
        s.setsc(P, 'skillCd', 360)
    if k % 15 == 0:
        e = (s.sc(P, 'energy') or 0) + 300
        if e >= 6000:
            e = 0
            s.setsc(P, 'burstCd', 300)
        s.setsc(P, 'energy', e)


def measure(s, n, after=None):
    per = []
    scans = 0
    manages = 0
    for k in range(n):
        a = s.n
        sc0 = s.ncall['rlk:items/equip_scan']
        m0 = s.ncall['rlk:player/inv/manage']
        tick(s, (lambda s, k=k: after(s, k)) if after else None)
        per.append(s.n - a)
        scans += s.ncall['rlk:items/equip_scan'] - sc0
        manages += s.ncall['rlk:player/inv/manage'] - m0
    ps = sorted(per)
    return {'avg': sum(per) / n, 'p50': ps[n // 2], 'max': ps[-1], 'scans': scans, 'manages': manages, 'n': n}


def f_press(s):
    """The swap-hands packet between ticks: main hand (hotbar.0) <-> off hand, inventory_changed fires."""
    inv = s.player.data['inv']
    inv['hotbar.0'], inv['weapon.offhand'] = inv.get('weapon.offhand'), inv['hotbar.0']
    if inv['hotbar.0'] is None:
        del inv['hotbar.0']
    if inv.get('weapon.offhand') is None:
        inv.pop('weapon.offhand', None)
    s.call('rlk:player/inv/dirty', pctx(s))


def one_pass(s):
    """One dirty pass (inv/manage + equip_scan) as player/tick runs it; commands, macro instantiations / lines."""
    c = pctx(s)
    a = s.n
    mi = sum(s.macro_n.values())
    ml = sum(s.macro_lines.values())
    s.call('rlk:player/inv/manage', c)
    man = s.n - a
    s.call('rlk:items/equip_scan', c)
    return {'manage': man, 'equip_scan': s.n - a - man, 'total': s.n - a,
            'macro_inst': sum(s.macro_n.values()) - mi, 'macro_lines': sum(s.macro_lines.values()) - ml}


# ------------------------------------------------------------------ state dump
def dump(s):
    """Everything observable: all scores (player + fake players), all storage, every entity's tags / data,
    the player inventory (components included)."""
    P = ('e', s.player.id)
    scores = {}
    for (h, o), v in s.scores.items():
        hk = 'PLAYER' if h == P else (f'ent+{h[1] - P[1]}' if isinstance(h, tuple) else h)   # ids relative to the player
        scores[(hk, o)] = v
    st = copy.deepcopy(s.storage)
    inv = copy.deepcopy(s.player.data.get('inv', {}))
    ents = sorted((e.etype, tuple(sorted(e.tags))) for e in s.ents if e is not s.player)
    return {'scores': scores, 'storage': st, 'inv': inv, 'ents': ents}


def _flat(prefix, v, out):
    if isinstance(v, dict):
        if not v:
            out[prefix] = '{}'
        for k, x in v.items():
            _flat(f'{prefix}.{k}' if prefix else k, x, out)
    elif isinstance(v, list):
        out[prefix] = snbt_dump(v)
    else:
        out[prefix] = repr(v)


def diff(a, b, ignore_scores=(), ignore_storage=()):
    """-> list of differences (strings). ignore_* are predicates on (holder, objective) / storage key path."""
    d = []
    ka = set(a['scores']) | set(b['scores'])
    for k in sorted(ka, key=str):
        if any(f(k) for f in ignore_scores):
            continue
        va, vb = a['scores'].get(k), b['scores'].get(k)
        if va != vb:
            d.append(f'score {k}: {va} != {vb}')
    fa, fb = {}, {}
    _flat('', a['storage'], fa)
    _flat('', b['storage'], fb)
    for k in sorted(set(fa) | set(fb)):
        if any(f(k) for f in ignore_storage):
            continue
        if fa.get(k) != fb.get(k):
            d.append(f'storage {k}: {str(fa.get(k))[:160]} != {str(fb.get(k))[:160]}')
    for sl in sorted(set(a['inv']) | set(b['inv'])):
        if a['inv'].get(sl) != b['inv'].get(sl):
            d.append(f'inv {sl}: {snbt_dump(a["inv"].get(sl)) if a["inv"].get(sl) else None} != '
                     f'{snbt_dump(b["inv"].get(sl)) if b["inv"].get(sl) else None}'[:400])
    if a['ents'] != b['ents']:
        d.append(f'entities: {collections.Counter(a["ents"]) - collections.Counter(b["ents"])} vs '
                 f'{collections.Counter(b["ents"]) - collections.Counter(a["ents"])}')
    return d

#!/usr/bin/env python3
"""test_px.py: the hit proxies of the chapter mode (AZ-CM, scratchpad az/contract/cm.md 9, 13.5, 15.2) on cproto's stub
manifest (tools/mboss_cproto_rig_manifest.json, read here for every expected offset / width / state).

    python3 test_px.py <worktree>/roguelike [boss id, default cproto]

 1. spawn: fixed UUIDs (block + pxBase + k), tags (never rlk_zmob / rlk_mshield), width, mbPart, the body husk (scale 0.1,
    rlk_mb_big, rlk_mb_noshield: no shield entity), the inv set at spawn and the inv rule during the intro
 2. tracks: rest offsets, a clip's keys (positions within the 0.15-b write threshold, heights), parked = 8 b under
 3. state sets: normal / tail_only / inv (rlk_mb_pxinv) / dead (death_start), unknown set warns and changes nothing
 4. one attack event -> exactly one hit on the body, for the apply_reset / melee_apply loops and every engine
    combat/apply call site (the lines are read from the real files); the number at the proxy; #mbPart / #mbPartGT
 5. a reaction in the same tick -> its own hit; element/dot and element/lunar/hit -> one hit each
 6. RES per element on the body, on_hit / incoming / the floor on the body
 7. Navia pellets counted on the body (char/navia/pellet_go, once per pellet); the minimap ignores proxies
 8. clicks polled every live tick, dropped every paused tick
 9. the push capsule (moves the player out <= 0.6 b/t, gates: dash, dead, selection, map view; px-bound capsule)
10. target-side audit (cm.md 9.6, README "챕터 보스"): Arlecchino's blood-debt goes to the body once (px/to_body),
    proxy-held superconduct / echo window / mirror / aura move to the body (px/db), Ronova's aim id stays on the proxy
11. /reload: the proxies come back with the same UUIDs, set and offsets
12. px + shield:true (Apep O2, cm.md 2.2 / 9.5; a registry variant of this boss): the body keeps a click shield of the
    registry hit size beside its proxies, and one attack event over a proxy and the body is still one hit (recheck APEP-10)
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import cmsim as M  # noqa: E402
from mcsim import Ctx, Ent  # noqa: E402

DP = Path(sys.argv[1]).resolve()
BOSS = sys.argv[2] if len(sys.argv) > 2 else 'cproto'
C0 = M.C0
check = M.check
REG = json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
B = M.entry(REG, BOSS)
MAN = json.loads((DP / f'tools/mboss_{BOSS}_rig_manifest.json').read_text(encoding='utf-8'))
LAY = MAN['proxies']['layout']
NAMES = [p['name'] for p in LAY]
REST = MAN['proxies']['rest']
CLIPS = {c['name']: c for c in MAN['clips']}
FN = DP / 'data/rlk/function'


def uuid_of(k):
    return MAN['uuids']['block'] + '%02x' % (B['pxBase'] + k)


def st(s):
    return s.storage.setdefault('rlk:mboss', {})


def px(s, name):
    r = [e for e in M.proxies(s) if f'rlk_mb_px_{name}' in e.tags]
    return r[0] if r else None


def world_of(body, local):
    """anchor + local (x left, z forward) rotated by the anchor yaw (MC: yaw 0 faces +z)."""
    x, z = local
    th = math.radians(body.rot[0])
    f = (-math.sin(th), math.cos(th))
    l_ = (math.cos(th), math.sin(th))
    return body.pos[0] + x * l_[0] + z * f[0], body.pos[2] + x * l_[1] + z * f[1]


def near(a, b, tol=0.16):
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol


def logged(s):
    log = []
    orig = s.call

    def call(fid, ctx, macro=None):
        log.append((s.t, fid, ctx.ex, tuple(ctx.pos), dict(macro) if macro else None))
        return orig(fid, ctx, macro)
    s.call = call
    return log


def body_hits(log, b, i0):
    return [r for r in log[i0:] if r[1] == 'rlk:mboss/d/on_hit' and r[2] is b]


def setup(chapter=2):
    s, pl = M.setup(DP)
    s.setsc('#chapter', 'room', chapter)
    log = logged(s)
    M.fight(s, BOSS, chapter)
    return s, pl, log


def hit_ctx(s, pl, dmg=100, elem=0):
    for k, v in (('#dmg', dmg), ('#dmgBase', dmg), ('#elem', elem), ('#elU', 1000 if elem else 0), ('#icd', 1 if elem else 0),
                 ('#crit', 0), ('#stunHit', 0), ('#hitLanded', 0), ('#bowHit', 0), ('#lunar', 0), ('#tfm', 0), ('#trueDmg', 0),
                 ('#skillDmg', 0)):
        s.setsc(k, 'tmp', v)
    s.setsc('#basic', 'itv', 0)


def run_line(s, line, ctx):
    s.cache['rlk:cmtest/line'] = [line]
    return s.call('rlk:cmtest/line', ctx)


# ------------------------------------------------------------------------------------------------- 1 spawn
print('== 1. spawn')
s, pl, log = setup()
b = M.body_of(s)
pxs = M.proxies(s)
check(f'1a {len(LAY)} proxies (manifest layout), one per name', len(pxs) == len(LAY) and all(px(s, n) for n in NAMES),
      [sorted(e.tags) for e in pxs])
for k, p in enumerate(LAY):
    e = px(s, p['name'])
    if e is None:
        continue
    check(f'1b {p["name"]}: UUID block + pxBase + {k} ({uuid_of(k)}), mbPart {k + 1}, width {p["w"]}',
          getattr(e, 'uuid', None) == uuid_of(k) and M.esc(s, e, 'mbPart') == k + 1 and abs(e.data.get('width', 0) - p['w']) < 1e-6,
          (getattr(e, 'uuid', None), M.esc(s, e, 'mbPart'), e.data.get('width')))
    check(f'1c {p["name"]}: tags rlk_room rlk_mb_aux boss rlk_mb_px rlk_mb_px_{p["name"]}; never rlk_zmob / rlk_mshield; response false',
          {'rlk_room', 'rlk_mb_aux', 'boss', 'rlk_mb_px', 'rlk_mb_px_' + p['name']} <= e.tags and not ({'rlk_zmob', 'rlk_mshield', 'miniboss'} & e.tags),
          sorted(e.tags))
check('1d the body: husk, rlk_mb_big + rlk_mb_noshield (cur.shield 0b: hit {0,1}... no click box), no miniboss',
      b.etype == 'husk' and {'rlk_mb_big', 'rlk_mb_noshield', 'boss'} <= b.tags and 'miniboss' not in b.tags, sorted(b.tags))
sc = [r[4] for r in log if r[1] == 'rlk:mboss/body_scale']
check('1e the body husk is scaled to the registry scale (0.1)', sc and abs(float(sc[-1]['s']) - B['scale']) < 1e-6, sc)
n0 = len([e for e in s.ents if 'rlk_mshield' in e.tags])
s.call('rlk:mob/shield_ensure', Ctx(b, tuple(b.pos), (0, 0)))
check('1f mob/shield_ensure on the body spawns no shield (rlk_mb_noshield line)', len([e for e in s.ents if e.alive and 'rlk_mshield' in e.tags]) == n0)
sp = [r for r in log if r[1] == 'rlk:mboss/px/state' and r[4]]
check('1g at spawn the set is inv (cm.md 9.4); the intro ended with normal', sp and sp[0][4].get('set') == 'inv'
      and st(s)['px']['set'] == 'normal', [r[4] for r in sp[:3]])
check('1h the intro body inv (rlk_mb_inv from the spawn) was never marked rlk_mb_pxinv, and is gone after the intro',
      'rlk_mb_inv' not in b.tags and 'rlk_mb_pxinv' not in b.tags, sorted(b.tags))

# ------------------------------------------------------------------------------------------------- 2 tracks
print('== 2. tracks, parking')
s.call('rlk:mboss/cproto/rig/play', Ctx(b, tuple(b.pos), b.rot), {'c': CLIPS['idle']['id']})
M.run(s, 2)


def pos_ok(s, name, local, live=True):
    e, b = px(s, name), M.body_of(s)
    want = world_of(b, local)
    y = b.pos[1] + (0 if live else -8)
    return e is not None and near((e.pos[0], e.pos[2]), want) and abs(e.pos[1] - y) < 0.01, (e and e.pos, want, y)


for n in NAMES:
    r = REST[n]
    ok, info = pos_ok(s, n, (r[0], r[1]))
    check(f'2a {n} at its rest column on the anchor floor', ok, info)
clip = CLIPS['sweep']
s.call('rlk:mboss/cproto/rig/play', Ctx(b, tuple(b.pos), b.rot), {'c': clip['id']})
keys = sorted((int(t), v) for t, v in clip['px']['keys'].items())
mid = keys[1]
M.run(s, 1 + mid[0])
check(f'2b sweep: rig tick {mid[0]} shown (mbT)', M.esc(s, b, 'mbT') == mid[0], M.esc(s, b, 'mbT'))
for n in NAMES:
    v = mid[1][n]
    ok, info = pos_ok(s, n, (v[0], v[1]))
    e = px(s, n)
    check(f'2c sweep tick {mid[0]}: {n} at the key column (within 0.15 b) and height {v[2]}', ok and abs(e.data.get('height', 0) - v[2]) < 0.16,
          (info, e.data.get('height')))
writes = [r for r in log if r[1].startswith(f'rlk:mboss/px/{BOSS}/k/{clip["id"]}/')]
check('2d key functions run only on ticks with a > 0.15 b change (not every tick)', 0 < len(writes) < clip['len'], len(writes))
clip = CLIPS['sink']
s.call('rlk:mboss/cproto/rig/play', Ctx(b, tuple(b.pos), b.rot), {'c': clip['id']})
M.run(s, clip['len'] + 2)
core = px(s, 'core')
ok, info = pos_ok(s, 'core', (0, 0), live=False)
check('2e sink: the core column top <= 0.3 -> parked 8 b under the floor, no rlk_mob', ok and 'rlk_mob' not in core.tags, info)
check('2f the tail stays live', 'rlk_mob' in px(s, 'tail').tags)
s.call('rlk:mboss/cproto/rig/play', Ctx(b, tuple(b.pos), b.rot), {'c': CLIPS['rise']['id']})
M.run(s, CLIPS['rise']['len'] + 2)
check('2g rise: the core comes back live', 'rlk_mob' in px(s, 'core').tags and pos_ok(s, 'core', tuple(REST['core'][:2]))[0])

# ------------------------------------------------------------------------------------------------- 3 state sets
print('== 3. state sets')
for name, sd in MAN['states'].items():
    if name == 'dead':
        continue
    s.call('rlk:mboss/px/state', C0, {'set': name})
    live = {n for n in NAMES if 'rlk_mob' in px(s, n).tags}
    check(f'3a set {name}: live = {sorted(sd["px"])}', live == set(sd['px']) and st(s)['px']['set'] == name, sorted(live))
    if sd.get('inv'):
        check(f'3b set {name} (inv:true): the body gets rlk_mb_inv + rlk_mb_pxinv', {'rlk_mb_inv', 'rlk_mb_pxinv'} <= b.tags, sorted(b.tags))
    caps = st(s).get('push', [])
    check(f'3c set {name}: push[] = its capsules ({len(sd["capsules"])})', len(caps) == len(sd['capsules']), caps)
s.call('rlk:mboss/px/state', C0, {'set': 'normal'})
check('3d leaving inv removes exactly what px added', 'rlk_mb_inv' not in b.tags and 'rlk_mb_pxinv' not in b.tags)
b.tags.add('rlk_mb_inv')
s.call('rlk:mboss/px/state', C0, {'set': 'inv'})
check('3e an inv the body already has is never marked (no rlk_mb_pxinv)', 'rlk_mb_pxinv' not in b.tags)
s.call('rlk:mboss/px/state', C0, {'set': 'normal'})
check('3f ... and leaving inv leaves it (px never removes an inv it did not add)', 'rlk_mb_inv' in b.tags)
b.tags.discard('rlk_mb_inv')
s.call('rlk:mboss/px/state', C0, {'set': 'normal'})
m0 = len(s.tells)
s.call('rlk:mboss/px/state', C0, {'set': 'nosuch'})
check('3g an unknown set warns (tellraw) and changes nothing', st(s)['px']['set'] == 'normal'
      and any('알 수 없는 판정 상태' in x for _, x in s.tells[m0:]), [x for _, x in s.tells[m0:]][-1:])

# ------------------------------------------------------------------------------------------------- 4 one event, one hit
print('== 4. one attack event -> one hit on the body')
core, tail = px(s, 'core'), px(s, 'tail')
# all live proxies and the body inside every site's radius: the player and the event origin at the core
pl.pos = [core.pos[0], core.pos[1], core.pos[2] + 0.5]
pc = Ctx(pl, tuple(pl.pos), (180.0, 0.0))
hp = lambda: M.esc(s, b, 'mhpC')  # noqa: E731
s.setsc('#mbFloor', 'mb', 0)
i0 = len(log)
s.call('rlk:combat/melee_begin', pc)
hit_ctx(s, pl)
for t in (core, tail, b):
    s.call('rlk:combat/apply_reset', Ctx(t, tuple(t.pos), (0, 0)))
check('4a apply_reset over core, tail and the body in one event: one hit', len(body_hits(log, b, i0)) == 1, len(body_hits(log, b, i0)))
r = [x for x in log[i0:] if x[1] == 'rlk:combat/apply' and x[2] is b]
check('4b the hit runs at the proxy that took it (the number shows there), #mbPart = its mbPart, #mbPartGT now',
      r and near((r[0][3][0], r[0][3][2]), (core.pos[0], core.pos[2]), 0.01) and M.mb(s, '#mbPart') == 1, r[:1])
i0 = len(log)
s.cache['rlk:combat/melee_front'] = ['scoreboard players set #meleeFront tmp 1']   # the front-cone test (tp facing) is engine geometry
s.call('rlk:combat/melee_begin', pc)
hit_ctx(s, pl)
for t in (b, core):
    s.call('rlk:combat/melee_apply', Ctx(t, tuple(t.pos), (0, 0)))
check('4c melee_apply loop, the body first: one hit, #mbPart 0 (a direct body hit)', len(body_hits(log, b, i0)) == 1 and M.mb(s, '#mbPart') == 0,
      (len(body_hits(log, b, i0)), M.mb(s, '#mbPart')))
i0 = len(log)
for t in (core, tail):
    s.call('rlk:combat/melee_begin', pc)
    hit_ctx(s, pl)
    s.call('rlk:combat/apply_reset', Ctx(t, tuple(t.pos), (0, 0)))
check('4d two attack events (two melee_begin) in the same tick: two hits', len(body_hits(log, b, i0)) == 2)

SITES = ['element/give', 'items/proc/raven_hit', 'items/proc/kirion_slash', 'items/proc/quill_fx', 'items/proc/demono_pillar_fx',
         'items/proc/rain_hit', 'items/proc/demono_tentacle_fx', 'items/proc/kslash_burst', 'items/proc/demono_fireball_hit',
         'engravings/abyss/fire', 'char/navia/rose_hit', 'char/lumine/crystal', 'element/aoe_hit']
OWN_SEQ = ['element/dot', 'element/lunar/hit']        # bump #atkSeq themselves: each call is its own event
calls = sorted(p.relative_to(FN).as_posix()[:-len('.mcfunction')] for p in FN.rglob('*.mcfunction')
               if any(l.rstrip().endswith('function rlk:combat/apply') for l in p.read_text(encoding='utf-8').split('\n')))
calls = [c for c in calls if not c.startswith('mboss/')]
LOOPS = ['combat/apply_reset']                         # the loop helper of 4a / 4c (52 + 10 callers)
check(f'4e every engine combat/apply call site is covered here ({len(calls)})', sorted(SITES + OWN_SEQ + LOOPS) == calls,
      sorted(set(calls) ^ set(SITES + OWN_SEQ + LOOPS)))
for site in SITES:
    lines = [l for l in (FN / f'{site}.mcfunction').read_text(encoding='utf-8').split('\n') if l.rstrip().endswith('function rlk:combat/apply')]
    i0 = len(log)
    s.call('rlk:combat/clear_atkflags', pc)
    hit_ctx(s, pl)
    for e in (core, tail, b):
        e.tags.discard('rlk_abt')
    for line in lines:
        if 'as @e[' in line:          # the site's own target selection
            if 'rlk_abt' in line:
                for e in (core, tail, b):
                    e.tags.add('rlk_abt')
            run_line(s, line, pc)
        else:                       # the caller's @s: the site is run once per target of the caller's loop
            for e in (core, tail, b):
                run_line(s, line, Ctx(e, tuple(e.pos), (0, 0)))
    for e in (core, tail, b):
        e.tags.discard('rlk_abt')
    n = len(body_hits(log, b, i0))
    check(f'4f {site}: one attack event over both proxies and the body -> exactly one body hit', n == 1, n)

# ------------------------------------------------------------------------------------------------- 5 reactions, DoT, lunar
print('== 5. reactions, DoT, lunar')
for site in OWN_SEQ:
    i0 = len(log)
    hit_ctx(s, pl)
    s.setsc('#dmg', 'tmp', 50)
    s.call(f'rlk:{site}', Ctx(core, tuple(core.pos), (0, 0)))
    check(f'5a {site} as a proxy: its own event, one body hit', len(body_hits(log, b, i0)) == 1, len(body_hits(log, b, i0)))
    i0 = len(log)
    hit_ctx(s, pl)
    s.setsc('#dmg', 'tmp', 50)
    s.call(f'rlk:{site}', Ctx(b, tuple(b.pos), (0, 0)))
    check(f'5b {site} as the body: one hit (px/dup lets a new event through)', len(body_hits(log, b, i0)) == 1)
i0 = len(log)
s.call('rlk:combat/melee_begin', pc)
hit_ctx(s, pl)
s.call('rlk:combat/apply_reset', Ctx(core, tuple(core.pos), (0, 0)))
seq0 = s.sc('#atkSeq', 'tmp')
# a queued superconduct on the body (rxQ 4) runs in the same game tick: element/rx_run -> run/supercond -> aoe_hit over
# every rlk_mob within 4 b (both proxies and the body stand there)
for o, v in (('rxQ', 4), ('rxDmg', 300), ('rxDmg3', 300), ('rxEl', 4), ('elAct', 1)):
    s.setsc(('e', b.id), o, v)
s.call('rlk:element/rx_run', Ctx(b, tuple(b.pos), (0, 0)))
aoe = [r for r in log[i0:] if r[1] == 'rlk:element/aoe_hit']
check('5c a reaction in the same tick as the attack: its own #atkSeq and exactly one more hit, although its AoE touched '
      f'{len(aoe)} targets', len(body_hits(log, b, i0)) == 2 and s.sc('#atkSeq', 'tmp') == seq0 + 1 and len(aoe) >= 3,
      (len(body_hits(log, b, i0)), len(aoe)))
check('5d the superconduct debuff written on the proxies moves to the body next tick (px/db)',
      M.run(s, 1) or ((M.esc(s, b, 'scT') or 0) >= 230 and all((M.esc(s, e, 'scT') or 0) == 0 for e in (core, tail))),
      (M.esc(s, b, 'scT'), [M.esc(s, e, 'scT') for e in (core, tail)]))

# ------------------------------------------------------------------------------------------------- 6 RES, hooks, floor
print('== 6. RES, on_hit, incoming, floor')


def dealt(s, target, elem, dmg=1000):
    s.call('rlk:combat/melee_begin', pc)
    hit_ctx(s, pl, dmg, elem)
    s.setsc(('e', b.id), 'mhpC', 10 ** 7)
    s.setsc(('e', b.id), 'mhpM', 10 ** 7)
    for o in ('elAct', 'aFire', 'aWater', 'aThunder', 'aIce', 'aGrass', 'aVoid', 'scT', 'mirEnd', 'aurEnd'):
        s.setsc(('e', b.id), o, 0)
    h0 = M.esc(s, b, 'mhpC')
    s.call('rlk:combat/apply', Ctx(target, tuple(target.pos), (0, 0)))
    return h0 - M.esc(s, b, 'mhpC')


res = B['res']
d0, d1, d5 = dealt(s, core, 0), dealt(s, core, 1), dealt(s, tail, 5)
r0, r1 = res.get('0', res['*']), res.get('1', res['*'])
check(f'6a per-element RES on the body through a proxy: physical {r0} % vs pyro {r1} % (dealt {d0} / {d1})',
      d0 > 0 and d1 > 0 and abs(d0 / d1 - (100 - r0) / (100 - r1)) < 0.03, (d0, d1))
check('6b geo uses its own RES (30 %), like physical', abs(d5 - d0) <= max(2, d0 * 0.02), (d5, d0))
check('6c RES of the body: mbRes0..8 from the registry', [M.esc(s, b, f'mbRes{k}') for k in range(9)]
      == [res.get(str(k), res['*']) for k in range(9)])
dealt(s, tail, 0)
check('6d on_hit runs on the body with #mbPart = the proxy hit (tail 2)', M.mb(s, '#cpLastPart') == 2, M.mb(s, '#cpLastPart'))
i0 = len(log)
dealt(s, core, 0)
check('6e incoming: cb/inc/<id> -> the module hook + mboss/floor, as the body', any(r[1] == f'rlk:mboss/cb/inc/{BOSS}' and r[2] is b for r in log[i0:])
      and any(r[1] == 'rlk:mboss/floor' and r[2] is b for r in log[i0:]))
s.setsc('#mbFloor', 'mb', 5000)
s.setsc('#mbFloorHit', 'mb', 0)
s.call('rlk:combat/melee_begin', pc)
hit_ctx(s, pl, 10 ** 6)
s.setsc(('e', b.id), 'mhpC', 9000)
s.call('rlk:combat/apply', Ctx(core, tuple(core.pos), (0, 0)))
check('6f the floor holds on the body (mhpC >= #mbFloor, #mbFloorHit 1)', M.esc(s, b, 'mhpC') >= 5000 and M.mb(s, '#mbFloorHit') == 1,
      (M.esc(s, b, 'mhpC'), M.mb(s, '#mbFloorHit')))
s.setsc('#mbFloor', 'mb', 0)
s.setsc('#mbFloorHit', 'mb', 0)
s.setsc(('e', b.id), 'mhpC', 10 ** 7)

# ------------------------------------------------------------------------------------------------- 7 Navia, minimap
print('== 7. Navia pellets, minimap')
for e in s.ents:
    e.tags.discard('rlk_np')
# one pellet step inside the proxy (char/navia/pellet, M0's text: every rlk_mob in the box gets rlk_np), then the end of
# that pellet (char/navia/pellet_go after the loop: a proxy hit becomes one body hit, the proxies are not counted)
lines = (FN / 'char/navia/pellet.mcfunction').read_text(encoding='utf-8').split('\n')
for line in [l for l in lines if 'rlk_np' in l and l.startswith('execute positioned ~-0.75')]:
    run_line(s, line, Ctx(pl, (core.pos[0], core.pos[1] + 0.75, core.pos[2]), (0, 0)))
tagged = [e for e in M.proxies(s) if 'rlk_np' in e.tags]
go = (FN / 'char/navia/pellet_go.mcfunction').read_text(encoding='utf-8').split('\n')
redirect = [l for l in go if 'rlk_mb_px' in l and not l.startswith('#')]
for line in redirect:
    run_line(s, line, Ctx(pl, tuple(pl.pos), (0, 0)))
check('7a a pellet inside a live proxy counts on the body (pellet_go: rlk_np on the body, never on a proxy; 2 lines per pellet, '
      'none per step)', tagged and 'rlk_np' in b.tags and not any('rlk_np' in e.tags for e in M.proxies(s)) and len(redirect) == 2
      and not any('rlk_mb_px' in l for l in lines), (len(tagged), len(redirect)))
i0 = len(log)
s.cache['rlk:room/map_mob'] = ['scoreboard players add #MAPMOB mb 1']     # the marker drawing itself is the minimap's
for line in [l for l in (FN / 'room/map_mobs.mcfunction').read_text(encoding='utf-8').split('\n') if 'room/map_mob ' in l + ' ']:
    run_line(s, line, Ctx(pl, tuple(pl.pos), (0, 0)))
drawn = [r[2] for r in log[i0:] if r[1] == 'rlk:room/map_mob']
check('7b room/map_mobs draws the body but never a proxy', b in drawn and not any('rlk_mb_px' in e.tags for e in drawn), [sorted(e.tags)[:3] for e in drawn])

# ------------------------------------------------------------------------------------------------- 8 polls
print('== 8. click polls')
a0 = s.sc('#POLLA', 'mb') or 0
core.data['attack'] = {'player': [1, 2, 3, 4], 'timestamp': s.t}
tail.data['interaction'] = {'player': [1, 2, 3, 4], 'timestamp': s.t}
r0_ = s.sc('#POLLR', 'mb') or 0
M.run(s, 1)
check('8a a live tick polls the proxies: attack -> poll_attack, interaction -> poll_right',
      (s.sc('#POLLA', 'mb') or 0) == a0 + 1 and (s.sc('#POLLR', 'mb') or 0) >= r0_ + 1, (s.sc('#POLLA', 'mb'), s.sc('#POLLR', 'mb')))
tail.data.pop('interaction', None)
s.setsc(('e', pl.id), 'pkMode', 1)
core.data['attack'] = {'player': [1, 2, 3, 4], 'timestamp': s.t}
a1 = s.sc('#POLLA', 'mb') or 0
M.run(s, 2)
check('8b paused: the stored click is dropped (px/clear_input), not polled', 'attack' not in core.data and (s.sc('#POLLA', 'mb') or 0) == a1)
s.setsc(('e', pl.id), 'pkMode', 0)
M.run(s, 2)

# ------------------------------------------------------------------------------------------------- 9 push capsule
print('== 9. push capsule')
s.setsc('#cpCool', 'mb', 99999)          # no boss pattern during the push checks
s.setsc('#cpPat', 'mb', 0)
s.call('rlk:mboss/lib_clear', C0)
s.call('rlk:mboss/px/state', C0, {'set': 'normal'})
s.call('rlk:mboss/cproto/test', Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 30})
check('9a cproto test 30 asks for the push every tick (#cpPush 1)', M.mb(s, '#cpPush') == 1)
for e in [e for e in s.ents if e.etype in ('marker',) and 'rlk_mb_hz' in e.tags]:
    e.alive = False


def dist_body(pl):
    return math.hypot(pl.pos[0] - b.pos[0], pl.pos[2] - b.pos[2])


def inside_core():
    pl.pos = [b.pos[0] + 0.3, b.pos[1], b.pos[2] + 0.2]


for gate, obj, val in (('dashing', 'dashMoveT', 1), ('dead', 'dead', 1), ('selecting', 'pkMode', 1), ('map view', 'vMap', 1)):
    inside_core()
    s.setsc(('e', pl.id), obj, val)
    p0 = list(pl.pos)
    M.run(s, 1)
    check(f'9b gate: {gate} -> the player is not moved', pl.pos == p0 or obj in ('pkMode',) and pl.pos == p0, (p0, pl.pos))
    s.setsc(('e', pl.id), obj, 0)
inside_core()
d0 = dist_body(pl)
steps = []
for _ in range(12):
    p0 = list(pl.pos)
    M.run(s, 1)
    steps.append(math.hypot(pl.pos[0] - p0[0], pl.pos[2] - p0[2]))
    if dist_body(pl) > 1.2 * 1.0 + 0.05 and steps[-1] == 0:
        break
check('9c inside the body capsule: moved out, <= 0.6 b per tick', max(steps) <= 0.6 + 1e-6 and max(steps) > 0 and dist_body(pl) >= 1.1,
      ([round(x, 2) for x in steps], round(dist_body(pl), 2)))
s.setsc('#cpPush', 'mb', 0)          # (test 30 toggles it with `store success ... unless`, which mcsim does not store on a fail)
M.run(s, 1)
inside_core()
p0 = list(pl.pos)
M.run(s, 2)
check('9d no request (#mbPushOn cleared every chapter-fight tick by mboss/world_cm_pre) -> no push', pl.pos == p0 and (M.mb(s, '#mbPushOn') or 0) == 0,
      (p0, pl.pos, M.mb(s, '#mbPushOn'), M.mb(s, '#cpPush')))

# ------------------------------------------------------------------------------------------------- 10 audit
print('== 10. target-side audit')
s.call('rlk:mboss/px/state', C0, {'set': 'normal'})
M.run(s, 1)
core, tail = px(s, 'core'), px(s, 'tail')
for o in ('arDir',):
    for e in (core, tail, b):
        s.setsc(('e', e.id), o, 0)
for e in (core, tail):
    e.tags.add('rlk_hit')
run_line(s, 'execute as @e[tag=rlk_hit,tag=rlk_mb_px] run function rlk:mboss/px/to_body', C0)
check('10a px/to_body: the proxies lose rlk_hit, the body gains it (once)', 'rlk_hit' in b.tags and not any('rlk_hit' in e.tags for e in (core, tail)))
b.tags.discard('rlk_hit')
txt = (FN / 'char/arlecchino/skill_hit.mcfunction').read_text(encoding='utf-8').split('\n')
i_kb = next(i for i, l in enumerate(txt) if 'skill_kb' in l)
i_sw = next(i for i, l in enumerate(txt) if 'px/to_body' in l)
i_ar = next(i for i, l in enumerate(txt) if ' arDir = ' in l)
i_ap = next(i for i, l in enumerate(txt) if 'apply_reset' in l)
check('10b skill_hit: the swap line after the damage (apply_reset) and before the arDir / mark lines', i_ap < i_sw < i_ar and i_kb < i_sw, (i_ap, i_sw, i_ar))
s.setsc('#ynow', 'tmp', s.t + 600)
for e in (core, tail):
    e.tags.add('rlk_hit')
for line in txt[i_sw:i_ar + 1]:
    if line.startswith(('execute', 'scoreboard')) and 'time query' not in line and '#ynow tmp +=' not in line:
        run_line(s, line, C0)
check('10c ... so arDir lands on the body only', (M.esc(s, b, 'arDir') or 0) > s.t and not any((M.esc(s, e, 'arDir') or 0) > 0 for e in (core, tail)),
      (M.esc(s, b, 'arDir'), [M.esc(s, e, 'arDir') for e in (core, tail)]))
for e in s.ents:
    e.tags.discard('rlk_hit')
for o, v in (('scT', 240), ('rnNoE', 200), ('mirEnd', s.t + 400), ('aurEnd', s.t + 300)):
    s.setsc(('e', b.id), o, 0)
    s.setsc(('e', core.id), o, v)
s.setsc(('e', b.id), 'elAct', 0)
M.run(s, 1)
check('10d px/db: superconduct / echo window / mirror / aura on a proxy move to the body (the proxy drops them), elAct 1',
      all((M.esc(s, b, o) or 0) >= v - 2 for o, v in (('scT', 240), ('rnNoE', 200), ('mirEnd', 1), ('aurEnd', 1)))
      and all((M.esc(s, core, o) or 0) == 0 for o in ('scT', 'rnNoE', 'mirEnd', 'aurEnd')) and M.esc(s, b, 'elAct') == 1,
      [(o, M.esc(s, b, o), M.esc(s, core, o)) for o in ('scT', 'rnNoE', 'mirEnd', 'aurEnd')])
lines = (FN / 'char/ronova/na_aim_hit.mcfunction').read_text(encoding='utf-8').split('\n')
s.setsc('#rnAimTg', 'tmp', 0)
for line in lines[1:3]:
    run_line(s, line, Ctx(pl, (tail.pos[0] - 0.5, tail.pos[1] + 0.5, tail.pos[2] - 0.5), (0, 0)))
check('10e Ronova\'s aim id (rnId) stays on the aimed proxy (accepted: the homing shot then hits the proxy -> the body)',
      (M.esc(s, tail, 'rnId') or 0) >= 1 and s.sc('#rnAimTg', 'tmp') == M.esc(s, tail, 'rnId'), (M.esc(s, tail, 'rnId'), s.sc('#rnAimTg', 'tmp')))

# ------------------------------------------------------------------------------------------------- 11 reload
print('== 11. /reload')
uu0 = sorted(getattr(e, 'uuid', None) for e in M.proxies(s))
o0 = json.dumps(st(s)['px']['o'], sort_keys=True)
s.call('rlk:mboss/init', C0)
check('11a mboss/init kills the proxies (rlk_mb_aux) and reload summons them again: same UUIDs, set and offsets',
      sorted(getattr(e, 'uuid', None) for e in M.proxies(s)) == uu0 and json.dumps(st(s)['px']['o'], sort_keys=True) == o0
      and st(s)['px']['set'] == 'normal', (uu0, sorted(getattr(e, 'uuid', None) for e in M.proxies(s))))
M.run(s, 2)
check('11b after /reload the proxies are live and follow the anchor', all('rlk_mob' in px(s, n).tags for n in NAMES))

# ------------------------------------------------------------------------------------------------- 12 px + shield
print('== 12. px + shield:true (Apep O2)')


def v_shield(reg):
    e = M.entry(reg, BOSS)
    e['shield'] = True
    e['hit'] = {'w': 2.0, 'h': 3.0}


VS = M.variant(DP, v_shield, 'shield')
try:
    s, pl = M.setup(VS)
    s.setsc('#chapter', 'room', 2)
    log = logged(s)
    M.fight(s, BOSS, 2)
    b = M.body_of(s)
    check('12a shield:true: the px body is rlk_mb_big without rlk_mb_noshield; every proxy spawned',
          b is not None and 'rlk_mb_big' in b.tags and 'rlk_mb_noshield' not in b.tags and len(M.proxies(s)) == len(LAY),
          (sorted(b.tags) if b else None, len(M.proxies(s))))
    b.tags.discard('rlk_mb_inv')
    s.call('rlk:mob/shield_ensure', Ctx(b, tuple(b.pos), (0, 0)))
    sh = [e for e in s.ents if e.alive and 'rlk_mshield' in e.tags]
    check('12b mob/shield_ensure gives the body one click shield of the registry hit size (2.0 x 3.0)',
          len(sh) == 1 and abs(float(sh[0].data.get('width', 0)) - 2.0) < 1e-6 and abs(float(sh[0].data.get('height', 0)) - 3.0) < 1e-6,
          [(e.data.get('width'), e.data.get('height')) for e in sh])
    s.call('rlk:mboss/px/state', C0, {'set': 'normal'})
    core = px(s, NAMES[0])
    pl.pos = [core.pos[0], core.pos[1], core.pos[2] + 0.5]
    pc = Ctx(pl, tuple(pl.pos), (180.0, 0.0))
    s.setsc('#mbFloor', 'mb', 0)
    i0 = len(log)
    s.call('rlk:combat/melee_begin', pc)
    hit_ctx(s, pl)
    for t in (core, b):
        s.call('rlk:combat/apply_reset', Ctx(t, tuple(t.pos), (0, 0)))
    check('12c one attack event over a proxy and the shielded body: one hit on the body', len(body_hits(log, b, i0)) == 1,
          len(body_hits(log, b, i0)))
finally:
    M.drop_variant(VS)

M.summary('PX')

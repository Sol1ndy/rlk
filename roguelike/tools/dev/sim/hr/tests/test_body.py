#!/usr/bin/env python3
"""test_body.py: round X (lane XB; tools/dev/plan/combat/x_brief.md, xb_progress.md): the body rule of the 홍련 fight.

    python3 test_body.py <roguelike> [section ...] [--keys=a9,mx] [--pols=walk,hold] [--dists=6,10] [--eye=2.36] [--json=out.json]
    (run from a copy of tools/dev/sim outside the datapack, as every hr suite)

The user (11-16): 「홍련 보스전에서 여전히 몸이 서로 부딪히는 문제가 있어」. Her body and the player's avatar must never come closer than
api.BODY['rule'] (1.4) b centre to centre on the floor plane while she is fought (no fight contact is declared). Round W's
dodgecam found nothing because its player never walked and stood at the eye height of a player (1.62), while in the game the
camera rider sits ~2.36 b over the avatar's feet (core/cam_ok measured from there). This suite is the investigation's
collide_run.py / g1fail_run.py made a gate (<S>/cb/collide/, 11-16):

  fight   every pattern of api.P1 (phase 1) and api.P2 (phase 2) and both gauntlets (their fail branch: nobody parries) in the
          H1 world (the real core, judge, hazards and the REAL dodge set), the player's camera rider at seat height (the
          player entity's eyes `eye` b over its feet = the avatar's feet; 2.11 / 2.36 / 2.85 for the three camera settings,
          --eye), the game's tick order: the walk is the avatar's Motion set before the functions (view/move's own clamp line,
          view/body_rule) and applied after them (vanilla physics, then the ground friction 0.546), the knockback marker's
          steps in rlk:tick's place. Players: walk (toward her at 0.216 b/t, stopping 1.5 b from her as a player would; the
          dodge one tick before every hit: a lunge-step while walking, else the twist toward her), hold (W held through her,
          no dodge), sprint (W + sprint, 0.28 b/t), lunge (W held + the dodge before every hit: the lunge-step into her),
          stand (no walk; the dodge and the double dodge's cartwheel 3 t later); start 3 / 6 / 10 b in front of her (the
          gauntlets: 6 b, from the south, north, east and west). Gate: at the end of no tick is her body (any height) nearer
          than the rule to the avatar on the floor plane, and no knockback of hers pushes the player toward her.
  sep     the soft separation (core/sep) alone: an avatar put 1.0 b off her is moved straight away from her (<= 0.25 b a
          tick, at the rule after two ticks); with a wall behind it, not into the wall; at the arena's edge, not out of it;
          not on a beat's held tick (mboss/main does not run) nor while a camera holds the player; a W-holding avatar at the
          rule keeps it through the tick's physics (its Motion clamped: core/sep_motion and view/body_rule).
  moves   the player's own moves toward her: the twist, the lunge-step, the back-step and the cartwheel (player/dodge/body),
          아를레키노's E (char/arlecchino/skill_dash on her), 클로린드's lunge (player/nudge -> player/step_move_tick) end at the
          rule (her body) / 1.6 b (a boss body), and a move away from her is never stopped.
  cam     core/cam_ok at the three seat heights: a floor point 1.0 / 1.5 b off the avatar fails (its body clause); 2.0 b with
          no camera line passes.
Prints one line per check; exit 1 on any failure. --json writes the per-run table (closest distance, ticks below the rule).
"""
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / 'lib'))
import test_wi as T  # noqa: E402
from test_wi import H, api, S3, DP, C0, fn_lines, beat_reset  # noqa: E402
from mcsim import Ctx, split  # noqa: E402

FLAGS = [a for a in sys.argv[1:] if a.startswith('--')]
SECT = [a for a in sys.argv[2:] if not a.startswith('-')]
FAILS, NCK = [], [0]
BODY = getattr(api, 'BODY', {'rule': 1.4, 'stop': 1.6, 'push': 0.25, 'near': 1.75})
RULE = BODY['rule']
EYES = (2.11, 2.36, 2.85)          # the seat rider's eyes over the avatar's feet (camera settings near / default / far)
WALK = 0.2159                      # #viewWalk 2159 x moveSpeed 100 % (b/t)
SPRINT = WALK * 1.3                # #viewSprint 130 in a fight
FRICTION = 0.546                   # the ground: 0.91 x block friction 0.6 (horizontal, after the move)
STOP_AT = 1.5                      # the walking player's own stop (the investigation's walk15)
RIDER_EYE = 1.62 * 0.0625         # the rider's own eye height (view/ride_mount: scale 0.0625)
HER_EYE = 1.74                     # her husk's eye height (scale 1.0)


def flag(name, default=None):
    for a in FLAGS:
        if a.startswith(f'--{name}='):
            return a.split('=', 1)[1]
    return default


def ck(name, ok, info=''):
    NCK[0] += 1
    print(('ok   ' if ok else 'FAIL ') + name + ('' if ok or info == '' else f'  -- {str(info)[:900]}'), flush=True)
    if not ok:
        FAILS.append(name)
    return ok


def want(name):
    return not SECT or name in SECT


VIEW_MOVE = fn_lines('view/move')
CLAMP = next((l for l in VIEW_MOVE if 'view/body_rule' in l), None)      # view/move's walk clamp (None on a tree without it)
KB_TICK = next(l for l in fn_lines('tick') if 'player/knockback/tick' in l)


class BodySim(T.DcSim):
    """test_wi's dodgecam world (the avatar's Motion: hrsim.ScSim.data_get / _motion_set, round X); the real knockback
    (player/knockback/start is a leaf stub in the vendored sims: world() takes the stub out)."""


def hsep(a, b):
    return math.hypot(a.pos[0] - b.pos[0], a.pos[2] - b.pos[2])


def world(key, ph, dist, eye, bearing=0.0):
    """dc_world (the H1 world, her at C facing the player `dist` b away) with the seat-height eyes, the avatar's Motion and the
    real knockback; bearing: the player's side of her (0 = south, the default; 180 north, 90 west, 270 east)."""
    s, pl = H.setup_sc(DP, seed=9, lv=15, hp=5834, player_level=15, cls=BodySim)
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
    s.call('rlk:bal/load', C0)
    beat_reset(s, 0, T.DC_STUB)
    for f in ('rlk:player/knockback/start', 'rlk:player/knockback/tick', 'rlk:player/knockback/step', 'rlk:view/stop_h'):
        s.cache.pop(f, None)
    assert H.fight_sc(s)
    if ph == 2 and key not in api.GAUNTLETS:
        H.test_id(s, 33)
        H.run_h1(s, 2)
    H.heal(s)
    a = math.radians(bearing)
    H.place_player(s, H.CX + 0.5 - math.sin(a) * dist, H.CZ + 0.5 + math.cos(a) * dist)
    H.place_body(s, H.CX + 0.5, H.CZ + 0.5)
    pl.tags.update(('rlk_body', 'rlk_av'))      # the player entity stands for the avatar (positions, Motion)
    # ... and for the camera rider at the seat: `anchored eyes` adds the EXECUTOR's eye height to the `at` position (vanilla
    # EntityAnchorArgument.Anchor.apply reads the source entity): run as the player (round X's core/cam_ok) its eyes are the
    # rider's, `eye` b over the avatar's feet; run as her (round W's core/cam_ok: `execute at @a[tag=player] anchored eyes`), her
    # husk's 1.74 b went on top of the rider's feet (`eye` - the rider's own 0.10 b at scale 0.0625)
    pl.data['eye'] = eye
    H.body_of(s).data['eye'] = eye - RIDER_EYE + HER_EYE
    pid = ('e', pl.id)
    for o in ('rdCam', 'pmMoveLock', 'pmActive', 'skDash', 'dashMoveT', 'dashCool', 'dashUpN', 'stepT'):
        s.setsc(pid, o, 0)
    s.setsc(pid, 'dashPX', round(pl.pos[0] * 100))
    s.setsc(pid, 'dashPZ', round(pl.pos[2] * 100))
    s.setsc('#charN', 'tmp', 5)
    s.setsc('#inAct', 'view', 0)
    s.motion[pl.id] = [0.0, 0.0, 0.0]
    return s, pl


def walk_motion(s, pl, b, speed, stop):
    """view/move for a player holding W toward her (the camera on her): the walk's Motion, the round X clamp line of view/move
    (view/body_rule) on it, stored on the avatar. Not while a dodge moves the body (view/move returns) or a knockback marker
    pushes it (view/stop_h)."""
    pid = ('e', pl.id)
    if (s.sc(pid, 'dashMoveT') or 0) >= 1 or (s.sc(pid, 'stepT') or 0) >= 1:
        return False
    if s.select('@e[tag=rlk_plkb,limit=1]', C0):
        s.motion[pl.id][0] = s.motion[pl.id][2] = 0.0
        return False
    d = hsep(pl, b)
    if stop is not None and d <= stop + 1e-6:
        return False
    ux, uz = (b.pos[0] - pl.pos[0]) / d, (b.pos[2] - pl.pos[2]) / d
    v = speed if stop is None else min(speed, d - stop)
    s.setsc('#mx', 'view', int(ux * v * 10000))
    s.setsc('#mz', 'view', int(uz * v * 10000))
    if CLAMP:
        s.cmd(split(CLAMP), Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    s.motion[pl.id][0] = (s.sc('#mx', 'view') or 0) / 10000
    s.motion[pl.id][2] = (s.sc('#mz', 'view') or 0) / 10000
    return True


def tick(s, pl, press):
    """One game tick: rlk:tick's knockback line, test_wi.dc_tick (the dodge press, player/tick's cooldown and move lines, her
    balance clock, the world, the position record), then vanilla physics on the avatar's Motion."""
    s.cmd(split(KB_TICK), C0)
    T.dc_tick(s, pl, press)
    m = s.motion[pl.id]
    pl.pos = [pl.pos[0] + m[0], pl.pos[1], pl.pos[2] + m[2]]
    m[0] *= FRICTION
    m[2] *= FRICTION


POLICIES = {'walk': (WALK, STOP_AT, True), 'hold': (WALK, None, False), 'sprint': (SPRINT, None, False),
            'lunge': (WALK, None, True), 'stand': (0.0, None, True)}


def run(key, ph, pol, dist, eye, bearing=0.0):
    s, pl = world(key, ph, dist, eye, bearing)
    pid = ('e', pl.id)
    speed, stop, dodge = POLICIES[pol]
    b0 = H.body_of(s)
    pl.rot = T.aim_at(pl, b0)
    tid = S3.TID[key]
    if key in api.GAUNTLETS:
        H.test_id(s, tid)
    else:
        H.start_pattern(s, tid)
    t0 = s.t
    limit = (api.JUDGE_T[key] + 40) if key in api.GAUNTLETS else 300
    st = dict(min=99.0, at=None, below=[], ticks=0, kb_in=[], presses=0, moved=0.0)
    presses, seen, prev = set(), False, tuple(pl.pos)
    while s.t - t0 < limit:
        pat = H.hr(s, '#pat') or 0
        if key not in api.GAUNTLETS:
            want_tid = S3.TID['ult'] if key == 'ult' else tid
            if pat == want_tid or (key == 'ult' and pat == S3.TID['rings']):
                seen = True
            elif seen and pat == 0:
                break
        for h in s.select('@e[type=minecraft:marker,tag=rlk_mb_hz]', C0):
            g = lambda o, h=h: s.sc(('e', h.id), o) or 0  # noqa: E731
            if dodge and g('mbHzD') >= 1 and g('mbHzHit') == 0 and g('mbHzW') - g('mbHzT') == 1:
                presses.add(s.t + 1)
                if pol == 'stand':
                    presses.add(s.t + 4)
        b = H.body_of(s)
        if b is not None:
            pl.rot = T.aim_at(pl, b)
            if speed:
                walk_motion(s, pl, b, speed, stop)
        H.heal(s)
        t = s.t + 1
        kb0 = {e.id for e in s.select('@e[tag=rlk_plkb]', C0)}
        tick(s, pl, t in presses)
        st['presses'] += t in presses
        b = H.body_of(s)
        if b is None:
            continue
        for e in s.select('@e[tag=rlk_plkb]', C0):
            if e.id not in kb0:            # a new knockback: its push direction against the line from her to the player
                y = math.radians(e.rot[0])
                dx, dz = -math.sin(y), math.cos(y)
                vx, vz = pl.pos[0] - b.pos[0], pl.pos[2] - b.pos[2]
                if dx * vx + dz * vz < 0:
                    st['kb_in'].append(s.t - t0)
        d = hsep(pl, b)
        st['ticks'] += 1
        if d < st['min']:
            st['min'], st['at'] = d, s.t - t0
        if d < RULE - 1e-6:
            st['below'].append((s.t - t0, round(d, 2)))
        st['moved'] += math.dist(prev, pl.pos)
        prev = tuple(pl.pos)
    st['min'] = round(st['min'], 3)
    st['moved'] = round(st['moved'], 1)
    return st


def fight():
    eye = float(flag('eye', '2.36'))
    keys = [(k, 1) for k in api.P1] + [(k, 2) for k in api.P2]
    only = flag('keys')
    if only:
        keys = [k for k in keys if k[0] in only.split(',')]
    pols = (flag('pols') or 'walk,hold,sprint,lunge,stand').split(',')
    dists = [float(x) for x in (flag('dists') or '3,6,10').split(',')]
    table, tot = {}, dict(runs=0, below=0, kb_in=0, ticks=0)
    for key, ph in keys:
        g = key in api.GAUNTLETS
        for pol in pols:
            for dist, bearing in ([(6.0, b) for b in (0.0, 180.0, 90.0, 270.0)] if g else [(d, 0.0) for d in dists]):
                r = run(key, ph, pol, dist, eye, bearing)
                tot['runs'] += 1
                tot['below'] += len(r['below'])
                tot['kb_in'] += len(r['kb_in'])
                tot['ticks'] += r['ticks']
                lab = f'{key} P{ph} {pol} {dist:g} b' + (f' from {int(bearing)} deg' if g else '') + f' eye {eye:g}'
                table[lab] = dict(min=r['min'], at=r['at'], below=len(r['below']), kb_in=len(r['kb_in']), ticks=r['ticks'],
                                  presses=r['presses'], moved=r['moved'])
                ck(f'fight {lab}: closest {r["min"]:.2f} b (t{r["at"]}), {len(r["below"])} of {r["ticks"]} ticks nearer than {RULE} b; '
                   f'knocked toward her {len(r["kb_in"])}; {r["presses"]} dodges, the avatar travelled {r["moved"]} b',
                   not r['below'] and not r['kb_in'], dict(below=r['below'][:8], kb_in=r['kb_in'][:4]))
    ck(f'fight (eye {eye:g}): {tot["runs"]} runs, {tot["ticks"]} ticks: nearer than {RULE} b on {tot["below"]}, knocked toward her '
       f'{tot["kb_in"]}', tot['below'] == 0 and tot['kb_in'] == 0, tot)
    out = flag('json')
    if out:
        Path(out).write_text(json.dumps(table, indent=1), encoding='utf-8')


# ============================================================================================================ sep
def idle_world(dist, eye=2.36, bearing=0.0):
    """Her in P1 standing (the test hold: no decision), the avatar `dist` b off her."""
    s, pl = world('a1', 1, dist, eye, bearing)
    H.hold(s, True)
    s.setsc('#rec', 'hr', 9999)
    return s, pl


def sep():
    s, pl = idle_world(1.0)
    b = H.body_of(s)
    ds = []
    for _ in range(4):
        tick(s, pl, False)
        ds.append(round(hsep(pl, b), 3))
    ck(f'sep: an avatar put 1.0 b off her goes straight away from her: {ds} (<= {BODY["push"]} b a tick, the rule after two ticks)',
       ds[0] >= 1.0 + BODY['push'] - 0.051 and ds[0] <= 1.0 + BODY['push'] + 0.051 and ds[1] >= RULE - 1e-6
       and all(d <= RULE + 0.051 for d in ds), ds)
    # straight away: the bearing kept
    s, pl = idle_world(1.0, bearing=50.0)
    b = H.body_of(s)
    a0 = math.atan2(pl.pos[0] - b.pos[0], pl.pos[2] - b.pos[2])
    tick(s, pl, False)
    tick(s, pl, False)
    a1 = math.atan2(pl.pos[0] - b.pos[0], pl.pos[2] - b.pos[2])
    ck(f'sep: radial (the bearing from her kept within 1 deg: {math.degrees(a1 - a0):+.2f})', abs(math.degrees(a1 - a0)) < 1.0)
    # a wall behind the avatar: not into it
    s, pl = idle_world(1.0)
    b = H.body_of(s)
    z_wall = math.ceil(pl.pos[2] + 0.3 + 1e-6)         # the block face 0.2 b behind the avatar's back
    for y in (201, 202):
        for x in range(int(H.CX) - 2, int(H.CX) + 3):
            s.blocks[(x, y, z_wall)] = 'stone'
    for _ in range(3):
        tick(s, pl, False)
    ck(f'sep: a wall 0.2 b behind the avatar (z {z_wall}): not pushed into it (its back {pl.pos[2] + 0.3:.3f} < {z_wall})',
       pl.pos[2] + 0.3 <= z_wall + 1e-6, pl.pos)
    # the beat's held tick: mboss/main does not run (no push); a camera hold: no push
    s, pl = idle_world(1.0)
    s.setsc('#btHold', 'cb', 1)
    tick(s, pl, False)
    held = hsep(pl, H.body_of(s))
    s.setsc('#btHold', 'cb', 0)
    ck(f'sep: not on a beat\'s held tick ({held:.3f} b after it)', abs(held - 1.0) < 1e-6, held)
    s, pl = idle_world(1.0)
    pl.tags.add('rlk_mb_camh')
    tick(s, pl, False)
    ck(f'sep: not while a camera holds the player ({hsep(pl, H.body_of(s)):.3f} b)', abs(hsep(pl, H.body_of(s)) - 1.0) < 1e-6)
    # a W-holding avatar from 3 b: the rule kept at the end of every tick (her clamp + view/body_rule)
    s, pl = idle_world(3.0)
    b = H.body_of(s)
    mins = []
    for _ in range(30):
        walk_motion(s, pl, b, WALK, None)
        tick(s, pl, False)
        mins.append(hsep(pl, b))
    ck(f'sep: W held into her from 3 b for 30 ticks: closest {min(mins):.3f} b, last {mins[-1]:.3f} b (>= {RULE})',
       min(mins) >= RULE - 1e-6, [round(x, 3) for x in mins[-6:]])
    # ... and on held ticks only the player's own clamp acts (view/body_rule): still never inside
    if CLAMP:
        s, pl = idle_world(1.6)
        b = H.body_of(s)
        s.setsc('#btHold', 'cb', 1)
        mins = []
        for _ in range(6):
            walk_motion(s, pl, b, SPRINT, None)
            tick(s, pl, False)
            mins.append(hsep(pl, b))
        s.setsc('#btHold', 'cb', 0)
        ck(f'sep: sprinting into her through 6 held beat ticks (only view/body_rule acts): closest {min(mins):.3f} b',
           min(mins) >= RULE - 1e-6, [round(x, 3) for x in mins])
    else:
        ck('sep: view/move has the round X clamp line (view/body_rule)', False)


# ============================================================================================================ moves
def move_run(dodge_mv, dist=1.9, toward=True):
    """A dodge move of the given kind (#dgMv) started at `dist` b from her, toward her (or straight away): the closest distance."""
    s, pl = idle_world(dist)
    b = H.body_of(s)
    pid = ('e', pl.id)
    d0 = hsep(pl, b)
    sgn = 1 if toward else -1
    ux, uz = sgn * (b.pos[0] - pl.pos[0]) / d0, sgn * (b.pos[2] - pl.pos[2]) / d0
    s.setsc(pid, 'dashUX', round(ux * 100))
    s.setsc(pid, 'dashUZ', round(uz * 100))
    s.setsc(pid, 'dashDX', round(ux * 1000))
    s.setsc(pid, 'dashDZ', round(uz * 1000))
    s.setsc('#dgMv', 'cb', dodge_mv)
    s.setsc('#dgCr', 'cb', 0)
    s.call('rlk:player/dodge/len', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    mins = []
    for _ in range(8):
        tick(s, pl, False)
        mins.append(hsep(pl, b))
    return min(mins), mins[-1]


def moves():
    for mv, name in ((1, 'twist'), (3, 'lunge-step'), (4, 'back-step'), (2, 'cartwheel')):
        lo, last = move_run(mv, 1.9)
        ck(f'moves: the {name} straight at her from 1.9 b stops in front of her (closest {lo:.3f} b >= {RULE})', lo >= RULE - 1e-6)
        lo2, last2 = move_run(mv, 1.45, toward=False)
        ck(f'moves: the {name} straight away from her from 1.45 b is not stopped (ends {last2:.2f} b)', last2 > 1.45 + 0.3)
    # 아를레키노's E: she is the target
    s, pl = idle_world(5.0)
    b = H.body_of(s)
    b.tags.add('rlk_artg')
    s.call('rlk:char/arlecchino/skill_dash', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    b.tags.discard('rlk_artg')
    tick(s, pl, False)
    ck(f'moves: 아를레키노\'s E on her arrives {hsep(pl, b):.3f} b off her (>= 1.6 before her own separation)', hsep(pl, b) >= 1.6 - 0.02)
    # 클로린드's lunge (player/nudge: 0.5 b a tick for 4 t along the view) from 2.5 b
    s, pl = idle_world(2.5)
    b = H.body_of(s)
    pl.rot = T.aim_at(pl, b)
    s.setsc('#nSpd', 'tmp', s.sc('#clStepSpd', 'tmp') or 5)
    s.setsc('#nT', 'tmp', s.sc('#clStepT', 'tmp') or 4)
    s.call('rlk:player/nudge', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    stepl = next(l for l in fn_lines('player/tick') if 'step_move_tick' in l)
    mins = []
    for _ in range(6):
        s.cmd(split(stepl), Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
        mins.append(hsep(pl, b))
    ck(f'moves: 클로린드\'s lunge at her from 2.5 b stops {min(mins):.3f} b off her (>= 1.6)', min(mins) >= 1.6 - 0.02, [round(x, 2) for x in mins])


# ============================================================================================================ cam
def cam():
    for eye in EYES:
        s, pl = idle_world(6.0, eye)
        pl.rot = T.aim_at(pl, H.body_of(s))
        res = {}
        for d, side in ((1.0, 90), (1.5, 90), (2.0, 90)):
            y = math.radians(pl.rot[0] + side)
            pos = (pl.pos[0] - math.sin(y) * d, 201.0, pl.pos[2] + math.cos(y) * d)
            res[d] = bool(s.call('rlk:boss/scarlet/core/cam_ok', Ctx(H.body_of(s), pos, (0.0, 0.0))))
        ck(f'cam: core/cam_ok with the camera rider\'s eyes {eye} b over the avatar\'s feet: beside the avatar at 1.0 / 1.5 b fails, '
           f'2.0 b passes ({res})', not res[1.0] and not res[1.5] and res[2.0], res)


def main():
    if want('cam'):
        cam()
    if want('moves'):
        moves()
    if want('sep'):
        sep()
    if want('fight'):
        fight()
    print(f'test_body: {NCK[0] - len(FAILS)} / {NCK[0]} ok' + (f', {len(FAILS)} FAILED' if FAILS else ''))
    sys.exit(1 if FAILS else 0)


if __name__ == '__main__':
    main()

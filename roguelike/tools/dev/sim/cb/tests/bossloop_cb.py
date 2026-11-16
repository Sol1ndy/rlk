#!/usr/bin/env python3
"""bossloop_cb.py: review A-11 — a real mid-boss fight whose world loop runs rlk:tick's pre-pass and near pass.

    python3 bossloop_cb.py <datapack root> [boss n]         (default n 1: 파수꾼・타락; run by test_cb.py's `bossloop` section)

The boss world loops of the fight suites (azsim.world, fgsim.world, hrsim.world_sc) call mboss/main only, so no fight
suite ran player/def/input, the dodge-start box or mboss/near_all. Here the vendored azsim world of
tools/dev/sim/hr/tests/lib (read only; its own process because its mcsim is not this folder's) gets, per tick:

    rlk:tick's pre-pass lines (#now, player/def/input, #dgOpen, the box line), taken from tick.mcfunction itself
    azsim.world (low gravity, element ticks, mboss/main, the room tick, boxes, schedules)
    rlk:tick's mboss/near_all line, run right after mboss/main returns (as in rlk:tick)

and a scripted player with the real inputs: the F5 use-item right-click (rcU -> player/def/rc -> combat/rc_hold ->
rclick_do -> player/dash) one tick before a dodgeable hazard strikes, then the body leaves (a long dash) so that only the
dodge start is inside; F one tick before a parryable hazard strikes. Not modelled: the inventory (the two `items`
tests answer from `hands`), the guard / dash clips and the item hooks (stubbed), effects (stubbed; test_cb `fx`).
Prints `ok` / `FAIL` lines; exit 1 on a failure.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'hr/tests/lib'))
import azsim  # noqa: E402
from mcsim import Ctx, split  # noqa: E402

DP = Path(sys.argv[1]).resolve()
BOSS = int(sys.argv[2]) if len(sys.argv) > 2 else 1
FN = DP / 'data/rlk/function'
C0 = Ctx(None, (0.0, 0.0, 0.0), (0.0, 0.0))
FAILS = []


def ck(name, ok, info=''):
    print(('ok   ' if ok else 'FAIL ') + name + ('' if ok or info == '' else f'  -- {info}'), flush=True)
    if not ok:
        FAILS.append(name)


def code(rel):
    return [l for l in (FN / f'{rel}.mcfunction').read_text(encoding='utf-8').split('\n') if l.strip() and not l.startswith('#')]


TICK = code('tick')
I0 = next(i for i, l in enumerate(TICK) if l.startswith('execute store result score #now cb run time query gametime'))
I1 = next(i for i, l in enumerate(TICK) if 'player/def/box_end' in l)
PRE = TICK[I0:I1 + 1]
NEAR = next(l for l in TICK if 'mboss/near_all' in l)
MAIN = next(i for i, l in enumerate(TICK) if 'function rlk:mboss/main' in l)
COOL = next(l for l in code('player/tick') if 'remove @s dashCool 1' in l)
STUB = ('rlk:player/def/guard', 'rlk:items/hook/on_parry_press', 'rlk:items/hook/on_parry', 'rlk:items/hook/on_pdodge',
        'rlk:items/hook/on_dash', 'rlk:char/motion/dash', 'rlk:char/motion/finish', 'rlk:player/dash_dir',
        'rlk:player/def/fx/pd', 'rlk:player/def/fx/p1', 'rlk:player/def/fx/p2', 'rlk:player/def/fx/p3')


class CbAz(azsim.AzSim):
    """azsim + the game time, the two inventory tests of the input path, real click data, `store success` without run"""
    hands = {'mainhand': 'attack', 'offhand': None}
    pre = 0
    log = None

    def cmd(self, t, ctx):
        if t[0] == 'time' and t[1:3] == ['query', 'gametime']:
            return 100000 + self.t + self.pre
        return super().cmd(t, ctx)

    def execute(self, t, ctx):
        if len(t) > 5 and t[0] in ('if', 'unless') and t[1:3] == ['items', 'entity']:
            role = self.hands.get(t[4].split('.')[-1])
            ok = role is not None and ('role:' not in t[5] or f'role:"{role}"' in t[5])
            if ok == (t[0] == 'unless'):
                return 0
            return self.execute(t[6:], ctx) if len(t) > 6 else 1
        if len(t) > 5 and t[0] == 'store' and t[2] == 'score' and 'run' not in t:
            v = 1 if super().execute(t[5:], ctx) else 0     # (mcsim leaves the score alone when the condition fails)
            self.store(t[1:5], v, ctx)
            return v
        return super().execute(t, ctx)

    def data_entity_test(self, kind, sel, path, ctx):
        if kind == 'entity' and path in ('interaction', 'attack'):
            es = self.select(sel, ctx) if sel != '@s' else ([ctx.ex] if ctx.ex else [])
            return bool(es) and path in es[0].data
        return super().data_entity_test(kind, sel, path, ctx)

    def call(self, fid, ctx, macro=None):
        if self.log is not None and fid in WATCH:
            self.log.append((self.t + self.pre, fid, sorted(ctx.ex.tags) if ctx.ex is not None else None, tuple(ctx.pos),
                             tuple(ctx.ex.pos) if ctx.ex is not None else None))
        r = super().call(fid, ctx, macro)
        if fid == 'rlk:mboss/main' and self.log is not None:
            self.cmd(split(NEAR), C0)                       # rlk:tick: the near pass right after mboss/main
        return r


WATCH = {'rlk:player/def/input', 'rlk:mboss/near_all', 'rlk:mboss/hz/near', 'rlk:mboss/pj/near', 'rlk:player/def/pd_go',
         'rlk:player/def/par3_go', 'rlk:bal/hit', 'rlk:player/def/box_end', 'rlk:combat/rclick_do', 'rlk:player/dash_go'}


def main():
    s, zone, pl = azsim.setup(force=BOSS, dp=DP, cls=CbAz)
    for f in STUB:
        s.cache[f] = []
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']      # (as test_bal_boss: the real gauge)
    s.call('rlk:bal/load', C0)
    P = ('e', pl.id)
    for o, v in (('curHealth', 10 ** 6), ('maxHealth', 10 ** 6), ('energy', 0), ('dashCool', 0), ('rcT', 0), ('rcU', 0),
                 ('sneakT', 0), ('buT', 0), ('rdCam', 0), ('pmMoveLock', 0), ('pmActive', 0), ('skillCd', 0)):
        s.setsc(P, o, v)
    s.setsc('#burstCost100', 'tmp', 10 ** 8)
    s.call('rlk:player/def/reset', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    # (HI, 11-11: lane H2's FN-cam hold / release lines may stand between mboss/main and the near pass)
    ck('bossloop: rlk:tick has the pre-pass before and the near pass right after mboss/main', I1 < MAIN and TICK.index(NEAR) > MAIN
       and all('rlk:mboss/cam/' in l for l in TICK[MAIN + 1:TICK.index(NEAR)])
       and len(PRE) == 6 and 'player/def/beat/clock' in PRE[1] and PRE[2] == 'scoreboard players operation #now cb -= #btAdj cb',
       (I0, I1, MAIN, TICK.index(NEAR), len(PRE)))
    ck(f'bossloop: the fight of boss n {BOSS} starts (azsim: the real gate, intro, #mbSt 1)', azsim.to_fight(s, zone))
    s.log = []
    home = list(pl.pos)
    away, out = 0, {'ticks': 0, 'pre': 0, 'near': [], 'pd': 0, 'par3': 0, 'body': 0, 'box': 0, 'hp': 0, 'near_closed': 0, 'tried': 0, 'bal': []}
    mode = 0
    N = 1500
    for _ in range(N):
        if (s.sc('#mbSt', 'mb') or 0) != 1 or not azsim.body_of(s):
            break
        # the player's decision for this tick: a hazard that strikes in this tick's mboss/main (mbHzT + 1 = mbHzW)
        f = rc = False
        if away == 0:
            for h in s.select('@e[type=minecraft:marker,tag=rlk_mb_hz]', C0):
                g = lambda o, h=h: s.sc(('e', h.id), o) or 0  # noqa: E731
                if g('mbHzD') >= 1 and g('mbHzHit') == 0 and g('mbHzW') - g('mbHzT') == 1:
                    if g('mbHzND') == 0 and (s.sc(P, 'dashCool') or 0) == 0 and mode % 2 == 0:
                        rc = True
                    elif g('mbHzNP') == 0:
                        f = True
                    if rc or f:
                        mode += 1
                        break
        s.hands = {'mainhand': None, 'offhand': 'attack'} if f else {'mainhand': 'attack', 'offhand': None}
        if rc:
            s.setsc(P, 'rcU', 1)                            # the using_item advancement of the tick before
            out['tried'] += 1
        hp0, en0 = s.sc(P, 'curHealth'), s.sc(P, 'energy')
        n0 = len(s.log)
        s.pre = 1
        for l in PRE:                                       # rlk:tick lines 15-18
            s.cmd(split(l), C0)
        s.pre = 0
        s.hands = {'mainhand': 'attack', 'offhand': None}
        if rc and s.sc(P, 'dgAt') == 100000 + s.t + 1:
            pl.pos = [home[0] + 40.0, home[1], home[2]]     # the body is gone (a long dash): only the dodge start can be hit
            away = 3
        azsim.world(s)                                      # ... mboss/main + the near pass (CbAz.call) ...
        s.cmd(split(COOL), Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
        ev = s.log[n0:]
        out['ticks'] += 1
        out['pre'] += len([e for e in ev if e[1] == 'rlk:player/def/input'])
        nr = [e for e in ev if e[1] == 'rlk:mboss/near_all']
        opened = (s.sc('#dgOpen', 'cb') or 0) == 1
        if nr:
            out['near'].append(s.t)
            out['near_closed'] += not opened
        elif opened and (s.sc('#mbLive', 'mb') or 0) == 1 and (s.sc('#mbPause', 'mb') or 0) != 1:
            out['near_closed'] += 1                         # the window is open but the pass did not run
        if away:
            if [e for e in ev if e[1] == 'rlk:player/def/pd_go']:
                out['pd'] += 1
                out['hp'] += hp0 - s.sc(P, 'curHealth')
                out['en'] = out.get('en', 0) + s.sc(P, 'energy') - en0
            away -= 1
            if away == 0:
                pl.pos = list(home)
        if [e for e in ev if e[1] == 'rlk:player/def/par3_go']:
            out['par3'] += 1
            out['bal'] += [e for e in ev if e[1] == 'rlk:bal/hit']
        tags_ok = 'rlk_body' in pl.tags and not s.select('@e[tag=rlk_body_real]', C0) and (s.sc('#gh', 'cb') or 0) == 0 \
            and not [e for e in s.select('@e[tag=rlk_body]', C0) if e is not pl]
        out['body'] += not tags_ok
        if not opened and s.select('@e[tag=rlk_dgo]', C0) and (s.sc('#dgKill', 'cb') or 0) <= 100000 + s.t:
            out['box'] += 1
    ck(f'bossloop: {out["ticks"]} fight ticks ran, the pre-pass (player/def/input) once in each', out['ticks'] >= 400 and out['pre'] == out['ticks'],
       (out['ticks'], out['pre']))
    ck(f'bossloop: mboss/near_all ran on {len(out["near"])} ticks: exactly the ticks with the window open (live, not paused)',
       len(out['near']) >= 3 and out['near_closed'] == 0, (len(out['near']), out['near_closed']))
    ck(f'bossloop: {out["tried"]} dodges one tick before a strike, the body 40 b away: {out["pd"]} perfect dodges found at the dodge '
       f'start through the near pass (>= 3), no HP lost, +10 pt each', out['pd'] >= 3 and out['hp'] == 0 and out.get('en', 0) == 1000 * out['pd'],
       (out['tried'], out['pd'], out['hp'], out.get('en')))
    ck('bossloop: after every tick the body mark is on the player alone (ghost_on / ghost_off paired) and no dodge-start box '
       'outlives its window', out['body'] == 0 and out['box'] == 0, (out['body'], out['box']))
    ok_bal = all(b[2] is not None and 'rlk_mb_body' in b[2] and b[3] == b[4] for b in out['bal'])
    ck(f'bossloop: F one tick before a parryable strike: {out["par3"]} perfect parries (>= 1), rlk:bal/hit as the boss body at its '
       f'position (review B-05)', out['par3'] >= 1 and len(out['bal']) >= 1 and ok_bal, (out['par3'], out['bal'][-1:]))
    print(f'bossloop_cb: {"FAILED " + str(len(FAILS)) if FAILS else "all passed"}')
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())

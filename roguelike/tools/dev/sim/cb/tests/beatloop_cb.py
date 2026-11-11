#!/usr/bin/env python3
"""beatloop_cb.py: the perfect parry / dodge beat in a REAL mid-boss fight (round V, lane VP; proof (b) for the boss framework).

    python3 beatloop_cb.py <datapack root> [boss n = 1]

The world of bossloop_cb.py (the vendored azsim of tools/dev/sim/hr/tests/lib + rlk:tick's own pre-pass lines, which now
hold the beat's clock) runs the same fight twice, with the beat's world hold off (#btOn tmp 0) and on (1). The scripted
player decides once per COMBAT tick (the tick number the pre-pass carries), exactly as the fight looked on that world tick,
so both runs get the same inputs on the beat's clock. On a held tick the loop does what rlk:tick does: its mboss/main line
(run here as written) calls mboss/main, which returns on its first line (the hook), scheduled functions still run (the effect kits, on their lag-corrected clock), the dodge
cooldown line is gated. Compared per world tick: every `#... mb` score of the framework and the module (the two raw game-time
caches #plG / #pxG aside), the body's position, every hazard's clock, the player's health.

  policy f     F one tick before every parryable strike (perfect parries): the two runs must be IDENTICAL world tick by world
               tick, the beat-on run exactly 5 real ticks longer per perfect parry
  policy mix   F and dodges alternate: the beat-on run may differ only where a dodge beat made the player untouchable; it
               reports the perfect dodges, checks N = 7 per dodge and that nothing was lost inside a beat
Prints one line per check; exit 1 on any failure.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bossloop_cb as B  # noqa: E402
from bossloop_cb import azsim, Ctx, split, C0, ck, FAILS, DP, BOSS, PRE, COOL, TICK  # noqa: E402

POST = next(l for l in TICK if 'player/def/beat/post' in l)
MAINL = next(l for l in TICK if 'function rlk:mboss/main' in l)
# presentation the simulator has no use for (avatar clips, particles, glyph cards, the title); the beat's engine stays real
STUB = ('rlk:player/def/guard', 'rlk:items/hook/on_parry_press', 'rlk:items/hook/on_parry', 'rlk:items/hook/on_pdodge',
        'rlk:items/hook/on_dash', 'rlk:char/motion/dash', 'rlk:char/motion/finish', 'rlk:player/dash_dir',
        'rlk:player/def/fx/p1', 'rlk:player/def/fx/p2', 'rlk:player/def/fx/p3_at', 'rlk:player/def/fx/p3_star',
        'rlk:player/def/fx/p3_shatter', 'rlk:player/def/fx/p3_bolt', 'rlk:player/def/fx/pd_at', 'rlk:player/def/fx/pd_body',
        'rlk:player/def/fx/pd_ember', 'rlk:player/def/fx/pd_chime', 'rlk:player/def/fx/ovl', 'rlk:char/motion/beat/parry',
        'rlk:char/motion/beat/dodge0', 'rlk:char/motion/beat/dodge', 'rlk:char/motion/beat/off', 'rlk:char/motion/beat/wglow_off',
        'rlk:char/motion/beat/tint_off', 'rlk:player/def/beat/act', 'rlk:player/def/beat/st/pass', 'rlk:player/def/beat/st/off',
        'rlk:player/def/beat/st/tp_on', 'rlk:player/def/beat/st/tp_off')
SKIP = {'#plG', '#pxG', '#mbPlG'}        # raw game-time caches (same-tick tests only)


def fight(on, policy, n_real=1700):
    s, zone, pl = azsim.setup(force=BOSS, dp=DP, cls=B.CbAz)
    for f in STUB:
        s.cache[f] = []
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
    s.call('rlk:bal/load', C0)
    P = ('e', pl.id)
    for o, v in (('curHealth', 10 ** 6), ('maxHealth', 10 ** 6), ('energy', 0), ('dashCool', 0), ('rcT', 0), ('rcU', 0),
                 ('sneakT', 0), ('buT', 0), ('rdCam', 0), ('pmMoveLock', 0), ('pmActive', 0), ('skillCd', 0), ('devMode', 0),
                 ('dead', 0), ('rnDie', 0), ('pkMode', 0), ('vMap', 0), ('plActive', 0)):
        s.setsc(P, o, v)
    s.setsc('#burstCost100', 'tmp', 10 ** 8)
    s.setsc('#3', 'tmp', 3)
    s.call('rlk:player/def/reset', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    s.call('rlk:player/def/beat/reset', C0)
    s.setsc('#btOn', 'tmp', on)
    assert azsim.to_fight(s, zone)
    s.log = []
    home = list(pl.pos)
    away = mode = 0
    last_c = None
    rows, st = {}, {'real': 0, 'par3': 0, 'pd': 0, 'held': 0, 'lost_in_beat': 0, 'rock': 0}
    lag0 = s.sc('#btLag', 'cb') or 0
    c0 = None
    for _ in range(n_real):
        if (s.sc('#mbSt', 'mb') or 0) != 1 or not azsim.body_of(s):
            break
        c = 100000 + s.t + 1 - (s.sc('#btLag', 'cb') or 0)
        if c0 is None:
            c0 = c
        f = rc = False
        if c != last_c and away == 0:
            for h in s.select('@e[type=minecraft:marker,tag=rlk_mb_hz]', C0):
                g = lambda o, h=h: s.sc(('e', h.id), o) or 0  # noqa: E731
                if g('mbHzD') >= 1 and g('mbHzHit') == 0 and g('mbHzW') - g('mbHzT') == 1:
                    if policy == 'mix' and g('mbHzND') == 0 and (s.sc(P, 'dashCool') or 0) == 0 and mode % 2 == 0:
                        rc = True
                    elif g('mbHzNP') == 0:
                        f = True
                    if rc or f:
                        mode += 1
                        break
        last_c = c
        s.hands = {'mainhand': None, 'offhand': 'attack'} if f else {'mainhand': 'attack', 'offhand': None}
        if rc:
            s.setsc(P, 'rcU', 1)
        hp0 = s.sc(P, 'curHealth')
        n0 = len(s.log)
        dg0 = s.sc(P, 'dgAt')
        s.pre = 1
        for l in PRE:
            s.cmd(split(l), C0)
        s.pre = 0
        s.hands = {'mainhand': 'attack', 'offhand': None}
        if rc and s.sc(P, 'dgAt') != dg0:
            pl.pos = [home[0] + 40.0, home[1], home[2]]     # the body is gone: only the dodge start can be hit
            away = 3
        hold = (s.sc('#btHold', 'cb') or 0) == 1
        inv = (s.sc('#btInv', 'cb') or 0) == 1
        st['real'] += 1
        if hold:
            st['held'] += 1
            s.t += 1                                        # real time passes; rlk:tick's world lines are gated ...
            s.cmd(split(MAINL), C0)                         # ... rlk:tick's own mboss/main line: main returns on its first line
            s.run_sched()
        else:
            azsim.world(s)
            s.cmd(split(COOL), Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
        s.cmd(split(POST), C0)
        ev = s.log[n0:]
        st['par3'] += len([e for e in ev if e[1] == 'rlk:player/def/par3_go'])
        st['pd'] += len([e for e in ev if e[1] == 'rlk:player/def/pd_go'])
        if inv:
            st['lost_in_beat'] += hp0 - s.sc(P, 'curHealth')
        if not hold:
            if away:
                away -= 1
                if away == 0:
                    pl.pos = list(home)
            b = azsim.body_of(s)
            mb = tuple(sorted((k[0], v) for k, v in s.scores.items() if k[1] == 'mb' and isinstance(k[0], str) and k[0] not in SKIP))
            hz = tuple(sorted((s.sc(('e', h.id), 'mbHzT') or 0, s.sc(('e', h.id), 'mbHzW') or 0, s.sc(('e', h.id), 'mbHzD') or 0,
                               tuple(round(v, 3) for v in h.pos)) for h in s.select('@e[type=minecraft:marker,tag=rlk_mb_hz]', C0)))
            rows[c - c0] = (mb, tuple(round(v, 3) for v in b.pos) if b else None, hz, s.sc(P, 'curHealth'),
                            s.sc(('e', b.id), 'mhpC') if b else None, s.sc(P, 'dashCool'))
    st['lag'] = (s.sc('#btLag', 'cb') or 0) - lag0
    st['K'] = s.sc('#btK', 'cb')
    return rows, st


def first_diff(a, b):
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            if k in a and k in b:
                for i, (x, y) in enumerate(zip(a[k], b[k])):
                    if x != y:
                        if i == 0:
                            dx, dy = dict(x), dict(y)
                            return k, [(n, dx.get(n), dy.get(n)) for n in sorted(set(dx) | set(dy)) if dx.get(n) != dy.get(n)][:6]
                        return k, i, x, y
            return k, 'missing', k in a, k in b
    return None


def main():
    ck('beatloop: mboss/main\'s first command is the hold hook (rlk:tick\'s line calls it as before)', B.code('mboss/main')[0] == 'execute if score #btHold cb matches 1 run return 0' and '#btHold' not in MAINL)
    r0, s0 = fight(0, 'f')
    r1, s1 = fight(1, 'f')
    n = min(len(r0), len(r1))
    common = {k: v for k, v in r0.items() if k in r1}
    d = first_diff(common, {k: r1[k] for k in common})
    ck(f'beatloop: boss n {BOSS}, F before every parryable strike: {s1["par3"]} perfect parries (>= 3) in both runs',
       s1['par3'] >= 3 and s0['par3'] >= s1['par3'], (s0['par3'], s1['par3']))
    ck(f'beatloop: ... beat on = beat off, world tick by world tick ({len(common)} world ticks compared: every #.. mb score, the body, '
       f'every hazard clock, both health pools, the dodge cooldown)', d is None and len(common) >= 400, d)
    ck(f'beatloop: ... the beat-on run held the world {s1["held"]} real ticks = 5 x {s1["par3"]} perfect parries (#btLag +{s1["lag"]}); '
       f'the beat-off run held none', s1['held'] == s1['lag'] and s0['held'] == 0 and s0['lag'] == 0
       and 5 * (s1['par3'] - 1) <= s1['held'] <= 5 * s1['par3'], (s1, s0))
    ck(f'beatloop: ... {len(r1)} world ticks in {s1["real"]} real ticks: every later world tick comes exactly (held so far) real '
       f'ticks later', s1['real'] == len(r1) + s1['held'], (s1['real'], len(r1), s1['held']))
    m0, t0 = fight(0, 'mix')
    m1, t1 = fight(1, 'mix')
    ck(f'beatloop: F and dodges mixed: {t1["par3"]} perfect parries, {t1["pd"]} perfect dodges with the beat on; held '
       f'{t1["held"]} = lag {t1["lag"]} real ticks, between 5 P + 7 D minus the beats cut by the next one and 5 P + 7 D',
       t1['pd'] >= 2 and t1['held'] == t1['lag'] and t1['held'] <= 5 * t1['par3'] + 7 * t1['pd']
       and t1['held'] >= 5 * t1['par3'] + 7 * t1['pd'] - 12 * 3, t1)
    ck('beatloop: ... no health is lost on an untouchable tick', t1['lost_in_beat'] == 0 and s1['lost_in_beat'] == 0, (t1['lost_in_beat'], s1['lost_in_beat']))
    common = {k: v for k, v in m0.items() if k in m1}
    d = first_diff(common, {k: m1[k] for k in common})
    print(f'     (mix: first difference between beat off / on: {d if d is None else str(d)[:300]})')
    print(f'beatloop_cb: {"FAILED " + str(len(FAILS)) if FAILS else "all passed"}')
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())

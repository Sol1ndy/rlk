#!/usr/bin/env python3
"""beatloop_hr.py: the perfect parry beat in 홍련's REAL fight (round V, lane VP; proofs (b) and (d) for her gauntlets).

    python3 beatloop_hr.py <datapack root>

The H1 world of the 홍련 suites (tools/dev/sim/hr/tests/lib/hrsim.py: the real core, the real F path, the real judge) runs
each scenario twice: with the beat's world hold off (#btOn tmp 0) and on (1). With it on, every real tick starts with
rlk:tick's own beat-clock line; on a tick the beat holds, the real game time moves on while her world does not run
(rlk:tick's own mboss/main line is run here as written: mboss/main returns on its first line, the hook; nothing else of
the world is called, as rlk:tick's other gates do). The scripted player presses on world ticks, so both runs get the same inputs on the beat's clock.

  G1 / G2   the two gauntlets (test ids of api.GAUNTLETS), F one tick before every scripted cut: every cut a perfect parry, the
            shield gauge emptied, the same judged strikes on the same world ticks, every `# hr` / `# mb` score, her body and
            the player's health identical world tick by world tick; the beat-on run 5 real ticks longer per perfect parry.
            The closest cuts of the scripts are the back-to-back case.
  P1        900 world ticks of the free phase-1 fight, F one tick before every parryable strike: identical as well
Prints one line per check; exit 1 on any failure.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'hr/tests'))
sys.path.insert(0, str(HERE.parents[1] / 'hr/tests/lib'))
import pat_lib as P  # noqa: E402
from pat_lib import H  # noqa: E402
from mcsim import Ctx, split  # noqa: E402

DP = Path(sys.argv[1]).resolve()
FN = DP / 'data/rlk/function'
C0 = Ctx(None, (0.0, 0.0, 0.0), (0.0, 0.0))
FAILS = []
api, _S = P.load_api(DP)
TEST = {'a8': 21, 'a13': 27}
TICK = [l for l in (FN / 'tick.mcfunction').read_text(encoding='utf-8').split('\n') if l.strip() and not l.startswith('#')]
CLOCK = next(l for l in TICK if 'player/def/beat/clock' in l)
POST = next(l for l in TICK if 'player/def/beat/post' in l)
MAINL = next(l for l in TICK if 'function rlk:mboss/main' in l)
STUB = ('rlk:player/def/guard', 'rlk:items/hook/on_parry_press', 'rlk:items/hook/on_parry', 'rlk:items/hook/on_pdodge',
        'rlk:char/motion/finish', 'rlk:player/def/fx/p1', 'rlk:player/def/fx/p2', 'rlk:player/def/fx/p3_at',
        'rlk:player/def/fx/p3_star', 'rlk:player/def/fx/p3_shatter', 'rlk:player/def/fx/p3_bolt', 'rlk:player/def/fx/ovl',
        'rlk:char/motion/beat/parry', 'rlk:char/motion/beat/off', 'rlk:char/motion/beat/wglow_off', 'rlk:player/def/beat/act',
        'rlk:player/def/beat/rock_on', 'rlk:player/def/beat/rock_off')
SKIP = {'#plG', '#pxG', '#mbPlG'}      # raw game-time caches of the framework (same-tick tests only)


def ck(name, ok, info=''):
    print(('ok   ' if ok else 'FAIL ') + name + ('' if ok or info == '' else f'  -- {info}'), flush=True)
    if not ok:
        FAILS.append(name)


class BeatSim(H.H1Sim):
    """H1Sim whose game time is the world tick + the ticks the beat has held (s.t stays the world tick = the beat's clock)"""
    held = 0
    pre = 0

    def cmd(self, t, ctx):
        if t[:3] == ['time', 'query', 'gametime']:
            return self.t + self.gt_off + self.held + self.pre
        return super().cmd(t, ctx)


def strikes_of(g):
    return [c[2] for _t, _s, _cl, c in api.SCRIPTS[g] if c]


def fight(on, kind):
    s, pl = H.setup_sc(DP, seed=9, lv=15, hp=5834, player_level=15, cls=BeatSim)
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
    s.call('rlk:bal/load', C0)
    for f in STUB:
        s.cache[f] = []
    pid = ('e', pl.id)
    for o in ('dead', 'rnDie', 'pkMode', 'vMap', 'rdCam', 'devMode', 'plActive'):
        s.setsc(pid, o, 0)
    s.call('rlk:player/def/beat/reset', C0)
    s.setsc('#btOn', 'tmp', on)
    assert H.fight_sc(s)
    H.facing_setup(s, 6.0)
    if kind in TEST:
        H.test_id(s, TEST[kind])
        t0 = s.t
        for k in strikes_of(kind):
            s.press(at=t0 + k - 1)
        end = t0 + api.JUDGE_T[kind] + 40
    else:
        t0 = s.t
        end = t0 + 900
    rows, st = {}, {'real': 0, 'held': 0, 'starts': 0}
    j0 = len(s.judged)
    lag0 = s.sc('#btLag', 'cb') or 0
    guard = 0
    while s.t < end and guard < 6000:
        guard += 1
        if kind == 'p1':                                    # F one tick before a parryable strike of the free fight
            for h in s.select('@e[type=minecraft:marker,tag=rlk_mb_hz]', C0):
                g = lambda o, h=h: s.sc(('e', h.id), o) or 0  # noqa: E731
                if g('mbHzD') >= 1 and g('mbHzHit') == 0 and g('mbHzW') - g('mbHzT') == 1 and g('mbHzNP') == 0:
                    s.press(at=s.t + 1)
                    break
        H.heal(s)
        s.pre = 1                                           # the head of the next real tick: rlk:tick's beat clock
        k0 = s.sc('#btK', 'cb') or 0
        s.cmd(split(CLOCK), C0)
        s.pre = 0
        st['real'] += 1
        if (s.sc('#btHold', 'cb') or 0) == 1:
            st['held'] += 1
            s.held += 1
            n0 = s.ncmd
            s.cmd(split(MAINL), C0)                         # rlk:tick's own mboss/main line: main returns on its first line
            st['hook'] = max(st.get('hook', 0), s.ncmd - n0)
        else:
            H.world_h1(s)
            b = H.body_of(s)
            sc = tuple(sorted((k[0], k[1], v) for k, v in s.scores.items() if k[1] in ('mb', 'hr') and isinstance(k[0], str)
                              and k[0] not in SKIP))
            rows[s.t - t0] = (sc, tuple(round(v, 3) for v in b.pos) if b else None, round(b.rot[0], 2) if b else None,
                              s.sc(pid, 'curHealth'), s.sc(('e', b.id), 'mhpC') if b else None)
        s.cmd(split(POST), C0)
    st['judged'] = [(j['t'] - t0, j['dodged'], j['parT'], j['pdg'], j['pat'], j['np']) for j in s.judged[j0:]]
    st['lag'] = (s.sc('#btLag', 'cb') or 0) - lag0
    st['gau'] = s.sc('#gau', 'hr')
    st['K'] = s.sc('#btK', 'cb')
    return rows, st


def first_diff(a, b):
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            if k in a and k in b:
                for i, (x, y) in enumerate(zip(a[k], b[k])):
                    if x != y:
                        if i == 0:
                            dx, dy = {(n, o): v for n, o, v in x}, {(n, o): v for n, o, v in y}
                            return k, [(n, dx.get(n), dy.get(n)) for n in sorted(set(dx) | set(dy)) if dx.get(n) != dy.get(n)][:6]
                        return k, i, x, y
            return k, 'missing', k in a, k in b
    return None


def main():
    for kind in ('a8', 'a13', 'p1'):
        r0, s0 = fight(0, kind)
        r1, s1 = fight(1, kind)
        par = len([j for j in s1['judged'] if j[2] == 3])
        d = first_diff(r0, r1)
        name = {'a8': 'gauntlet G1', 'a13': 'gauntlet G2', 'p1': 'the free P1 fight'}[kind]
        if kind in TEST:
            cuts = strikes_of(kind)
            gaps = sorted(b - a for a, b in zip(cuts, cuts[1:]))
            ck(f'beathr: {name}: F one tick before each of the {len(cuts)} cuts (closest two {gaps[0]} t apart): every cut a perfect '
               f'parry with the beat on, as with it off', par == len(cuts) and s0['judged'] == s1['judged'],
               (par, s1['judged'][:4], s0['judged'][:4]))
        else:
            ck(f'beathr: {name}, F before every parryable strike: {par} perfect parries (>= 3), the judged hits the same on the same '
               f'world ticks', par >= 3 and s0['judged'] == s1['judged'], (par, len(s0['judged']), len(s1['judged'])))
        ck(f'beathr: ... beat on = beat off, world tick by world tick ({len(r1)} world ticks: every `# hr` and `# mb` score, her '
           f'body and yaw, both health pools)', d is None and len(r1) == len(r0) and len(r1) >= 100, d)
        ck(f'beathr: ... held {s1["held"]} real ticks = 5 x {par} perfect parries = #btLag (+{s1["lag"]}); {s1["real"]} real ticks = '
           f'{len(r1)} world ticks + the held ones; on a held tick rlk:tick\'s mboss/main line costs {s1.get("hook", 0)} commands (the call and the hook)',
           s1['held'] == 5 * par == s1['lag'] and s1['real'] == len(r1) + s1['held'] and s0['held'] == 0 and s1.get('hook', 2) <= 2,
           (s1['held'], par, s1['lag'], s1['real'], len(r1), s1.get('hook')))
    print(f'beatloop_hr: {"FAILED " + str(len(FAILS)) if FAILS else "all passed"}')
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())

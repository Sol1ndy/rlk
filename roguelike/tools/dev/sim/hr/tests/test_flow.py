#!/usr/bin/env python3
"""test_flow.py: the whole rebuilt 홍련 fight in one run (lane HI, 11-11): the real rift, the real core, the real sequences with
their lock (hr/h2/camsim.py: the F5 view, FN-cam, spectate), the actor's calls (seqsim's model; test_actor.py runs the real
F:char/cine/**) and the real kit, with a player
who answers her: a perfect parry (F at h - 1) for every parry cue, nothing else (no dodge). Every phase in order:

  CS0 (locked 1440 t) -> P1 (patterns, the gauge, landed hits on her, a groggy) -> the 60 % floor -> CS1 (locked 720 t) ->
  lead60 -> G1 cleared by five perfect parries -> repel {at:60} (locked 140 t, three 15 ‰ steps) -> P2 (+3 balance) ->
  the 5 % floor -> lead5 -> G2 failed (no parry: the instant death) -> Ronova's revive -> the stance -> lead_re -> G2 cleared
  -> repel {at:5} (the kill at the kick) -> the ending (1372 t) -> the coda (120 t) -> the reward

and two branches taken from copies of that run: G1 failed (50 % hit, P2 at T + 240) and the lock's exit paths inside CS1
(player death, Ronova's revive, /reload, a relog, the framework's abort, uninstall): the player is released at the avatar in
their own game mode with nothing left, and the fight goes on (or ends) as the core says. Prints the timeline; fails on any
break of the chain. Run from a copy outside the datapack:   python3 test_flow.py <roguelike>
"""
import copy
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
sys.path.insert(0, str(HERE.parent / 'h2'))
import hrsim as H  # noqa: E402
import camsim as CS  # noqa: E402
import seqsim as Q  # noqa: E402
from mcsim import Ctx  # noqa: E402

DP = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(DP / 'tools'))
from mboss_scarlet import api, s3lib as S3  # noqa: E402

A = H.A
C0 = H.C0
PH, L = api.PH, api.SEQ_LEN
PHN = {v: k for k, v in PH.items()}
SEQN = {i: f'seq {n}' for n, i in S3.SEQ_ID.items()}
R = []


def ck(name, ok, info=''):
    R.append((name, bool(ok)))
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else f'   [{info}]'), flush=True)
    return ok


class FlowSim(Q.SeqSim, H.H1Sim):
    """camsim's world (the view, the lock) + H1Sim's inputs (F with its lock rules, the dodge) and judge log; lane H3's
    actor as seqsim models it (spawn makes the root, stop removes it; its own world is test_actor.py's). No driver: the
    real core starts and ticks the sequences."""

    def __init__(self, root):
        super().__init__(root)
        self.parry_on = True
        self.cues_seen = 0


def world(s):
    """One game tick: the F5 view tick, the inputs + her balance clock + the fight (hrsim.world_h1), FN-cam's lines of
    rlk:tick, the player's own server tick (camsim.world's order)."""
    k0 = len(s.kitl)
    CS.view_tick(s)
    s._cam_done = False
    H.world_h1(s)
    if not s._cam_done:
        s.run_cam_lines()
    pl = s.player()
    if pl is not None:
        s.net_tick(pl)
    if hasattr(s, 'cost'):
        sq = H.hr(s, '#sqn') or 0
        key = SEQN.get(sq) if sq else (PHN.get(H.hr(s, '#ph')) if (H.mb(s, '#mbLive') or 0) == 1 else 'out')
        if (H.mb(s, '#mbArBuild') or 0) >= 1:
            key = f'{key} (arena job)'
        s.cost.append((s.t, s.cmd_hist[-1], key))
    # the parrier: F one tick before every cued hit (the cue is exactly api.CUE_LEAD t before it)
    for t, c, a in s.kitl[k0:]:
        if c == 'snd/' + api.CUE_SND:
            s.cues_seen += 1
            if s.parry_on:
                s.press(at=t + api.CUE_LEAD - 1)


def ph(s):
    return H.hr(s, '#ph')


def hp(s):
    b = H.body_of(s)
    return s.sc(('e', b.id), 'mhpC'), s.sc(('e', b.id), 'mhpM')


LOG = []


def run_until(s, cond, limit, each=None, tag=''):
    held = 0
    for _ in range(limit):
        if cond(s):
            return True, held
        if each:
            each(s)
        world(s)
        held += CS.held(s)
    return cond(s), held


def heal(s):
    if s.player() is not None and not (s.sc(('e', s.player().id), 'rnDie') or 0):
        H.heal(s)


def mark(s, what):
    LOG.append((s.t, what, PHN.get(ph(s)), H.hr(s, '#sqn'), hp(s)[0] if H.body_of(s) else None))
    print(f'  t {s.t:6d}  {what:<44s} #ph {PHN.get(ph(s))}  hp {hp(s)[0] if H.body_of(s) else "-"}', flush=True)


def clean_ok(s, label, gm0='adventure'):
    c = CS.clean(s, gm0=gm0)
    bad = [k for k, v in c.items() if not v]
    actor = any(e.alive and 'rlk_cine_root' in e.tags for e in s.ents)
    return ck(f'{label}: released (at the avatar, on the seat, {gm0}, no stand, no request) and no actor left',
              not bad and not actor, (bad, actor))


def setup():
    s, pl = CS.setup(DP, cls=FlowSim, seed=11, lv=15, hp=5834, player_level=15)
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
    s.call('rlk:bal/load', C0)
    s.storage.setdefault('rlk:pinv', {}).setdefault('order', [])
    s.cost = []
    return s, pl


# ====================================================================================================== the main run
s, pl = setup()
z, a = H.rift_zone(s, 'scarlet')
s.player().pos = list(a.pos)
ok = bool(H.enter(s, a))
s.zone_sc = z
ok, _h = run_until(s, lambda s: H.body_of(s) is not None and s.avatar() is not None and (s.sc('#sq', 'hr') or 0) >= 1, 1200)
ck('the rift: her body, the avatar and CS0 running', ok)
mark(s, 'CS0 starts')
ok, held = run_until(s, lambda s: (H.mb(s, '#mbSt') or 0) == 1, L['intro'] + 40, each=heal)
ck(f'CS0 runs locked to its end ({L["intro"]} t; held {held} t), then the fight', ok and held >= L['intro'] - 10 and ph(s) == PH['p1'], held)
world(s)
clean_ok(s, 'CS0 hand-back')
mark(s, 'P1')
# P1: she fights; the player perfect-parries every cue and lands a hit every 8 t when near her
grog = []
cue0 = s.cues_seen
gau_max = [0]


def p1_each(s):
    heal(s)
    b, p = H.body_of(s), s.player()
    if s.t % 8 == 0 and math.dist(b.pos[::2], p.pos[::2]) <= 4.0 and 'rlk_mb_inv' not in b.tags:
        A.strike(s, b, 30)
    if (s.sc(('e', b.id), 'grgT') or 0) > 0 and (not grog or grog[-1] != s.t - 1):
        grog.append(s.t)
    gau_max[0] = max(gau_max[0], H.hr(s, '#gau') or 0)


t0 = s.t
H.facing_setup(s, 3.0)
run_until(s, lambda s: False, 1500, each=p1_each)
# review H-A, HA-10: every parryable hit is looked at, also one that landed in full (a refused F: parT 0, not np, not dodged)
p1_hits = [j for j in s.judged if j['t'] > t0 and j['pt'] and j['ph'] == PH['p1']]
unparried = [j for j in p1_hits if not (j['parT'] == 3 or j['np'] or j['dodged'])]
ck(f'P1 1500 t: patterns ran, cues came, the perfect parrier perfect-parried every parryable hit ({len(p1_hits)} judged, '
   f'{len(unparried)} parryable not perfect)', s.cues_seen > cue0 and p1_hits and not unparried,
   (s.cues_seen - cue0, unparried[:3]))
ck(f'P1: the balance broke her at least once (groggy ticks seen: {len(grog)}), the gauge filled to {gau_max[0]}', grog and gau_max[0] > 0,
   (grog[:3], gau_max[0]))
mark(s, 'P1 played 1500 t')
H.test_id(s, 80)
run_until(s, lambda s: (H.hr(s, '#pat') or 0) == 0 and (s.sc(('e', H.body_of(s).id), 'grgT') or 0) == 0, 200, each=heal)
A.strike(s, H.body_of(s), 99999)
ck('the hit that reaches 60 % stops there', hp(s)[0] == H.hr(s, '#fl60'), (hp(s), H.hr(s, '#fl60')))
ok, _h = run_until(s, lambda s: ph(s) == PH['cs1'], 300, each=heal)
ck('CS1 at the next decision', ok)
mark(s, 'CS1')
snap_cs1 = copy.deepcopy(s)            # the branch: the lock's exit paths inside CS1
ok, held = run_until(s, lambda s: ph(s) == PH['lead60'], L['cs1'] + 10, each=heal)
ck(f'CS1 runs locked ({held} t of {L["cs1"]}) into lead60', ok and held >= L['cs1'] - 10, held)
world(s)
clean_ok(s, 'CS1 hand-back')
mark(s, 'lead60')
ok, _h = run_until(s, lambda s: ph(s) == PH['a8'], L['lead60'] + 10, each=heal)
ck('lead60 -> G1 with the gauge 5/5', ok and H.hr(s, '#gau') == api.GAUGE['max'], H.hr(s, '#gau'))
mark(s, 'G1')
snap_g1 = copy.deepcopy(s)             # the branch: G1 failed
t1 = s.t
ok, _h = run_until(s, lambda s: ph(s) != PH['a8'], api.JUDGE_T['a8'] + 10, each=heal)
pp = [j for j in s.judged if j['t'] > t1 and j['parT'] == 3]
ck(f'G1 cleared by perfect parries ({len(pp)} perfect of the cuts): the repel {{at:60}} at the judge (T + {api.JUDGE_T["a8"]})',
   ok and ph(s) == PH['cs2'] and s.t - t1 in (api.JUDGE_T['a8'], api.JUDGE_T['a8'] + 1) and len(pp) >= 5, (PHN.get(ph(s)), s.t - t1, len(pp)))
mark(s, 'repel {at:60}')
c0 = hp(s)[0]
s.setsc(('e', H.body_of(s).id), 'bal', 4)     # (so that the + 3 after the repel shows)
b0 = H.bal(s)
ok, held = run_until(s, lambda s: ph(s) == PH['p2'], L['repel'] + 10, each=heal)
c1, m = hp(s)
ck(f'the repel {{at:60}} runs locked ({held} t), three 15 ‰ steps ({c0 - c1} = 3 x {m * 15 // 1000}), then P2', ok and held >= L['repel'] - 5
   and c0 - c1 == 3 * (m * 15 // 1000), (held, c0 - c1, m))
ck(f'... balance + {api.BAL["after_repel"]} after it ({b0} -> {H.bal(s)})', H.bal(s) == min(12, (b0 or 0) + api.BAL['after_repel']), (b0, H.bal(s)))
world(s)
clean_ok(s, 'repel {at:60} hand-back')
mark(s, 'P2')
H.facing_setup(s, 5.0)
seen = set()


def p2_each(s):
    p1_each(s)
    seen.add(H.hr(s, '#pat'))


run_until(s, lambda s: False, 1500, each=p2_each)
ck('P2 1500 t: her P2 kit ran (mx / nb / q among the patterns seen)', {S3.TID[k] for k in ('mx', 'nb', 'q')} & seen,
   sorted(x for x in seen if x))
mark(s, 'P2 played 1500 t')
H.test_id(s, 34)
run_until(s, lambda s: (H.hr(s, '#pat') or 0) == 0 and (s.sc(('e', H.body_of(s).id), 'grgT') or 0) == 0, 200, each=heal)
A.strike(s, H.body_of(s), 99999)
ok, _h = run_until(s, lambda s: ph(s) == PH['lead'], 300, each=heal)
ck('the 5 % floor -> lead5', ok and H.hr(s, '#sqn') == S3.SEQ_ID['lead5'], H.hr(s, '#sqn'))
mark(s, 'lead5')
ok, _h = run_until(s, lambda s: ph(s) == PH['a13'], L['lead5'] + 10, each=heal)
ck('lead5 -> G2 with the gauge 5/5', ok and H.hr(s, '#gau') == api.GAUGE['max'], H.hr(s, '#gau'))
mark(s, 'G2 (no parry: the fail)')
s.parry_on = False
s.revive = 40
t1 = s.t
ok, _h = run_until(s, lambda s: bool([d for d in s.deaths if d > t1]), api.JUDGE_T['a13'] + 10, each=heal)
ck(f'G2 failed: the instant death at the judge (T + {api.JUDGE_T["a13"]})', ok and [d for d in s.deaths if d > t1][0] - t1 == api.JUDGE_T['a13'],
   [d - t1 for d in s.deaths if d > t1])
mark(s, 'the instant death; Ronova revives')
ok, _h = run_until(s, lambda s: H.hr(s, '#sqn') == S3.SEQ_ID['lead_re'], 200 + api.REVIVE['wait'])
ck('... revived: the stance, then lead_re {g:a13}', ok)
s.parry_on = True
s.revive = 0
ok, _h = run_until(s, lambda s: ph(s) == PH['a13'], L['lead_re'] + 10, each=heal)
ck('... G2 again with the gauge 5/5', ok and H.hr(s, '#gau') == api.GAUGE['max'], H.hr(s, '#gau'))
mark(s, 'G2 again (parried)')
t1 = s.t
ok, _h = run_until(s, lambda s: ph(s) != PH['a13'], api.JUDGE_T['a13'] + 10, each=heal)
ck(f'G2 cleared: the repel {{at:5}} at the judge (T + {api.JUDGE_T["a13"]})', ok and ph(s) == PH['cs3'] and s.t - t1 in
   (api.JUDGE_T['a13'], api.JUDGE_T['a13'] + 1), (PHN.get(ph(s)), s.t - t1))
mark(s, 'repel {at:5}')
t1 = s.t
ok, held = run_until(s, lambda s: (H.mb(s, '#mbSt') or 0) == 2, L['repel'] + 10, each=heal)
ck(f'the repel {{at:5}}: the kill at its kick ({api.ev("repel", "kick")}), locked all the way', ok and s.t - t1 in
   (api.ev('repel', 'kick'), api.ev('repel', 'kick') + 1) and held >= s.t - t1 - 2, (s.t - t1, held))
mark(s, 'the kill -> the ending')
t1 = s.t
ok, held = run_until(s, lambda s: (H.mb(s, '#mbLive') or 0) == 0, L['ending'] + L['event'] + 60, each=heal)
ck(f'the ending + the coda run under one lock to the reward ({held} t held of {s.t - t1})', ok and
   L['ending'] + L['event'] - 10 <= held <= L['ending'] + L['event'] + 4, (held, s.t - t1))
run_until(s, lambda s: False, 3)
clean_ok(s, 'after the coda')
mark(s, 'the fight is over')
# the cost (README 0-5: a fight tick's mean <= Apep's ~830): per phase / sequence of this run, the heaviest ticks named
by = {}
for t, n, k in s.cost:
    by.setdefault(k, []).append(n)
print('commands per tick (mean / max / ticks): ' + '; '.join(f'{k} {sum(v) / len(v):.0f} / {max(v)} / {len(v)}' for k, v in sorted(by.items())))
print('the heaviest ticks: ' + ', '.join(f't {t} {n} ({k})' for t, n, k in sorted(s.cost, key=lambda x: -x[1])[:6]))
# (not averaged: 'out' = the room / rift ticks around the fight, the arena's build and look jobs (their slices have their own
# limit, README 홍련 「파일 · 생성 순서」), 'intro' = the one spawn tick before CS0 starts: the rig and the arena helpers summoned)
SKIP_K = ('out', 'intro')
fight = [n for t, n, k in s.cost if k not in SKIP_K and 'arena job' not in k]
ck(f'the cost: every phase and sequence averages <= 830 commands per tick (the whole fight {sum(fight) / len(fight):.0f})',
   all(sum(v) / len(v) <= 830 for k, v in by.items() if 'arena job' not in k and k not in SKIP_K),
   {k: round(sum(v) / len(v)) for k, v in by.items()})

# ====================================================================================================== branch: G1 failed
s = snap_g1
s.parry_on = False
t1 = s.t
pl = s.player()
h0 = s.sc(('e', pl.id), 'curHealth')
ok, _h = run_until(s, lambda s: ph(s) == PH['p2'], api.FAIL60_P2_T + 10)
ck(f'branch G1 failed: no repel, the 50 % hit, P2 at T + {api.FAIL60_P2_T}, the player alive', ok and s.t - t1 in
   (api.FAIL60_P2_T, api.FAIL60_P2_T + 1) and not [d for d in s.deaths if d > t1], (s.t - t1, s.deaths))

# ====================================================================================================== branch: the lock's exits in CS1


def at_cs1(n):
    s = copy.deepcopy(snap_cs1)
    run_until(s, lambda s: False, n, each=heal)
    return s


s = at_cs1(200)
ck('exits: CS1 tick ~200 is held', CS.held(s))
pl = s.player()
s.revive = 30
s.call('rlk:player/die', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
run_until(s, lambda s: False, 2)
ck('exits: the player dies inside CS1 (Ronova\'s revive running) -> released at once', not CS.held(s) and CS.gm(s) == 'adventure', CS.held(s))
ok, held = run_until(s, lambda s: ph(s) == PH['lead60'], 120)
ck(f'exits: ... alive again: CS1 goes to its end state at the resume, lead60, never locked again ({held} t held)', ok and held == 0, (PHN.get(ph(s)), held))
world(s)
clean_ok(s, 'exits: ... after the resume')
ok, _h = run_until(s, lambda s: ph(s) == PH['a8'], 120, each=heal)
ck('exits: ... and the chain goes on into G1', ok, PHN.get(ph(s)))

s = at_cs1(250)
pl = s.player()
s.ents.remove(pl)
run_until(s, lambda s: False, 4)
s.st(pl)['cam'] = s.st(pl)['ccam'] = None
s.ents.append(pl)
s.setsc('#vFresh', 'view', 1)
world(s)
ck('exits: a relog inside CS1 -> released in the first tick back, own game mode', not CS.held(s) and CS.gm(s) == 'adventure', CS.held(s))
ok, _h = run_until(s, lambda s: ph(s) == PH['a8'], 900, each=heal)
ck('exits: ... and the chain goes on into G1', ok, PHN.get(ph(s)))

s = at_cs1(260)
live = s.sc('#mbCamId', 'mb')
for e in s.ents:
    if f'rlk_mb_cam{live}' in e.tags:
        e.alive = False
s.ents = [e for e in s.ents if e.alive]
world(s)
ck('exits: the live camera stand killed inside CS1 -> released in the next tick', not CS.held(s) and CS.gm(s) == 'adventure', CS.held(s))
ok, _h = run_until(s, lambda s: ph(s) == PH['a8'], 900, each=heal)
ck('exits: ... and the chain goes on into G1', ok, PHN.get(ph(s)))

s = at_cs1(300)
for e in s.ents:
    if 'rlk_view' in e.tags:
        e.alive = False
s.ents = [e for e in s.ents if e.alive]
s.setsc('#vFresh', 'view', 1)
s.call('rlk:mboss/init', C0)
ck('exits: /reload inside CS1 -> released inside mboss/init, the stands dead', not CS.held(s) and not s.stands(), (CS.held(s), s.stands()))
run_until(s, lambda s: False, 4, each=heal)
clean_ok(s, 'exits: ... the fight goes on')
ok, _h = run_until(s, lambda s: ph(s) == PH['a8'], 400, each=heal)
ck('exits: ... and the chain goes on into G1', ok, PHN.get(ph(s)))

s = at_cs1(250)
s.call('rlk:boss/test/abort', Ctx(s.player(), tuple(s.player().pos), (0.0, 0.0)))
run_until(s, lambda s: False, 3)
ck('exits: the abort inside CS1 -> the fight ends, released, nothing left', not CS.held(s) and not s.stands() and (H.mb(s, '#mbLive') or 0) == 0
   and not any(e.alive and 'rlk_cine_root' in e.tags for e in s.ents), (CS.held(s), s.stands(), H.mb(s, '#mbLive')))

s = at_cs1(350)
s.call('rlk:mboss/uninstall', C0)
run_until(s, lambda s: False, 2)
ck('exits: the framework\'s uninstall (mboss/uninstall) inside CS1 -> released, no stand', not CS.held(s) and not s.stands(), (CS.held(s), s.stands()))

n_ok = sum(1 for _n, o in R if o)
print(f'test_flow: {n_ok}/{len(R)} passed' + ('' if n_ok == len(R) else f', {len(R) - n_ok} FAILED'))
sys.exit(0 if n_ok == len(R) else 1)

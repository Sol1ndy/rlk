#!/usr/bin/env python3
"""test_bal_hr.py: 홍련's balance adapter on the new combat (hr_design §1.3-1.5, §6.1; lane H1; replaces her rows of
bal/tests/test_bal_boss.py): the groggy = grog_in -> down -> kipup in its last 20 t, 100 t, hittable, damage taken x 1.30;
every bal_ok refusal leaves the break pending and it starts at the first allowed tick; no balance damage in the lead-ins /
gauntlets (#mbBalOff) and the cutscenes; the floor rule (a pending break is dropped, bal 3); + 3 after the repel {at:60};
a floor reached while groggy cuts it to its kip-up; the perfect-parry flinch (PP_FLINCH). Review H-A: HA-02 hits during the
groggy queue no reaction (the counter, the flinch, A6): the first pattern after it starts after the full recovery, as
without hits; HA-04 /reload during the groggy: she lies in the down loop at once, the kip-up at 20 left (from its tick);
HA-05 every pattern's airborne ticks (the body = the rig's root above the floor) are refused by bal_ok, so no break drops
her to the floor (a4's ring hop 28-38 too).
    python3 test_bal_hr.py <roguelike>      (from a copy of tools/dev/sim outside the datapack)
"""
import sys

import pat_lib as P
from pat_lib import ck, H

DP = sys.argv[1]
api, S = P.load_api(DP)
A = H.A
KIP, GIN = api.BAL['kip'], api.BAL['grog_in']


def fresh(seed=6, p2=False):
    s, pl = H.setup_h1(DP, seed=seed)
    assert H.fight_sc(s)
    if p2:
        H.test_id(s, 33)
        H.run_h1(s, 2)
    H.facing_setup(s, 3.0)
    H.hold(s)
    return s


def brk(s):
    b = H.body_of(s)
    s.setsc('#n', 'bal', 12)
    return s.call('rlk:bal/hit', H.Ctx(b, tuple(b.pos), tuple(b.rot)), {'n': 12})


def tags(s):
    return H.body_of(s).tags


# ---- the groggy from idle
s = fresh()
H.run_h1(s, 3)
ck('she starts with 12 pips', (H.bal(s, 'balMax'), H.bal(s)) == (12, 12), (H.bal(s, 'balMax'), H.bal(s)))
n0 = len(s.rigl)
H.test_id(s, 19)
ck('test 19: the groggy starts (100 t), the balance row is empty', (H.bal(s, 'grgT'), H.bal(s)) == (100, 0), (H.bal(s, 'grgT'), H.bal(s)))
clips, inv, pats = {}, [], []
t0 = s.t
hp_before = None
for i in range(1, 104):
    if i == 50:
        b = H.body_of(s)
        hp_before = s.sc(('e', b.id), 'mhpC')
        A.strike(s, b, 100)
        d_grog = hp_before - s.sc(('e', b.id), 'mhpC')
    H.heal(s)
    H.world_h1(s)
    for t, c in s.rigl[n0:]:
        if c.startswith('play/') and t == s.t:
            clips.setdefault(c[5:], H.bal(s, 'grgT'))
    inv.append('rlk_mb_inv' in tags(s))
    pats.append(H.hr(s, '#pat') or 0)
    if (H.bal(s, 'grgT') or 0) == 0 and i > 5:
        break
dur = s.t - t0
ck('the groggy lasts 100 t', dur in (100, 101), dur)
ck('grog_in at the break (from test 19\'s call)', any(c == 'play/grog_in' for t, c in s.rigl[n0:]), [c for t, c in s.rigl[n0:]][:4])
ck(f'down once grog_in ended (grgT {100 - GIN}), kipup in the last {KIP} t', (clips.get('down'), clips.get('kipup')) in
   ((100 - GIN, KIP), (100 - GIN - 1, KIP - 1)), clips)
ck('hittable for the whole groggy (never rlk_mb_inv), nothing runs', not any(inv) and not any(pats))
ck('the gauge is full again at its end', H.bal(s) == 12, H.bal(s))
ck(f'then a {api.GROGGY_RECOVER}-t recovery', H.hr(s, '#rec') in (api.GROGGY_RECOVER, api.GROGGY_RECOVER - 1), H.hr(s, '#rec'))
s2 = fresh()
H.run_h1(s2, 3)
b2 = H.body_of(s2)
h0 = s2.sc(('e', b2.id), 'mhpC')
A.strike(s2, b2, 100)
d_norm = h0 - s2.sc(('e', b2.id), 'mhpC')
ck('damage taken x 1.30 while groggy', d_norm > 0 and abs(d_grog - d_norm * 1.3) <= 1.5, (d_norm, d_grog))

# ---- bal_ok: the windows where the break waits (pending) and starts at the first allowed tick
E = api.ev
WIN = {'a4': (E('a4', 'leap'), E('a4', 'hit'), 9.0, 1), 'a10': (E('a10', 'spring'), E('a10', 'hit'), 6.0, 1),
       'hcut': (E('hcut', 'go'), E('hcut', 'cut'), 14.0, 1), 'a9': (E('a9', 'go'), E('a9', 'cut'), 4.0, 1),
       'kcut': (E('kcut', 'go'), E('kcut', 'cut'), 5.0, 1), 'blue': (E('blue', 'go'), E('blue', 'hit'), 5.0, 1),
       'ult': (E('ult', 'cut1'), E('ult', 'cut2'), 2.4, 1), 'nb': (E('nb', 'leap'), E('nb', 'land'), 9.0, 2),
       'mx': (E('mx', 'go'), E('mx', 'x'), 8.0, 2)}
for key, (a, bb, dist, ph) in WIN.items():
    s = fresh(p2=(ph == 2))
    H.facing_setup(s, dist)
    H.start_pattern(s, S.TID[key])
    H.until_h1(s, lambda s: H.hr(s, '#pat') == S.TID[key] and (H.hr(s, '#pt') or 0) >= a, 200, each=lambda s: H.heal(s))
    brk(s)
    pend = 'rlk_bal_pend' in tags(s)
    g0 = H.bal(s, 'grgT') or 0
    H.until_h1(s, lambda s: (H.bal(s, 'grgT') or 0) > 0, 120, each=lambda s: H.heal(s))
    # the break started by lane B's pending tick right after the first module tick past the window
    ck(f'{key}: a break in its window {a}-{bb} waits (pending) and starts right after it',
       pend and g0 == 0 and (H.hr(s, '#pat') or 0) == 0 and (H.bal(s, 'grgT') or 0) >= 98, (pend, g0, H.hr(s, '#pt'), H.bal(s, 'grgT')))
    b = H.body_of(s)
    ck(f'{key}: she is on the floor when the groggy starts', abs(b.pos[1] - api.CY) < 0.06, b.pos[1])
# q: refused outright while she is the ghost of the lunge (4-20: rlk_mb_inv; fix lane FB's rule in bal/boss/may: an
# untargetable body takes no balance damage), pending from the grab to the pattern's end (bal_ok: q 16 -> end)
s = fresh(p2=True)
H.facing_setup(s, 10.0)
H.start_pattern(s, S.TID['q'])
H.until_h1(s, lambda s: (H.hr(s, '#pt') or 0) >= E('q_grab', 'go') + 2, 60, each=lambda s: H.heal(s))
brk(s)
ck('q: a break during the ghost lunge is refused (no balance taken, nothing pending)', 'rlk_mb_inv' in tags(s)
   and 'rlk_bal_pend' not in tags(s) and H.bal(s) == 12 and (H.bal(s, 'grgT') or 0) == 0, (sorted(tags(s)), H.bal(s)))
H.until_h1(s, lambda s: (H.hr(s, '#pt') or 0) >= api.Q_AIR_T0 + 4, 60, each=lambda s: H.heal(s))
brk(s)
ck('q: a break from the grab on is pending', 'rlk_bal_pend' in tags(s) and (H.bal(s, 'grgT') or 0) == 0, (H.hr(s, '#pt'), sorted(tags(s))))
H.until_h1(s, lambda s: (H.hr(s, '#pat') or 0) == 0, 200, each=lambda s: H.heal(s))
H.run_h1(s, 3)
ck('q: ... and starts when the pattern ended', (H.bal(s, 'grgT') or 0) > 0, H.bal(s, 'grgT'))
# a pattern outside its window: the break cancels it at once
s = fresh()
H.start_pattern(s, S.TID['a3'])
H.run_h1(s, 20, each=lambda s: H.heal(s))
brk(s)
ck('a3 (on the ground): the break starts at once, the pattern and its hazards are gone',
   (H.bal(s, 'grgT'), H.hr(s, '#pat') or 0, len([e for e in s.ents if e.alive and 'rlk_hr_p_a3' in e.tags])) == (100, 0, 0),
   (H.bal(s, 'grgT'), H.hr(s, '#pat')))

# ---- no balance damage in the lead-ins, the gauntlets and the cutscenes
for tid, name in ((20, 'CS1'), (21, 'G1'), (26, 'lead5'), (24, 'the repel')):
    s = fresh(p2=tid != 20)
    H.test_id(s, tid)
    H.run_h1(s, 5)
    r = brk(s)
    ck(f'{name}: balance damage is refused', H.bal(s) == 12 and 'rlk_bal_pend' not in tags(s), (r, H.bal(s)))

# ---- the floor rule and the kip-up cut
s = fresh()
H.start_pattern(s, S.TID['a4'])
H.until_h1(s, lambda s: (H.hr(s, '#pt') or 0) >= 4, 30)
brk(s)
H.hold(s, False)
H.test_id(s, 80)                                   # HP = the 60 % floor + 1
b = H.body_of(s)
A.strike(s, b, 5000)
H.until_h1(s, lambda s: H.hr(s, '#ph') == api.PH['cs1'], 200, each=lambda s: H.heal(s))
ck('the floor reached with a break pending: CS1 starts, the pending break is dropped, bal = 3',
   H.hr(s, '#ph') == api.PH['cs1'] and 'rlk_bal_pend' not in tags(s) and H.bal(s) == api.BAL['floor_min'] and (H.bal(s, 'grgT') or 0) == 0,
   (H.hr(s, '#ph'), H.bal(s), H.bal(s, 'grgT')))
s = fresh()
H.run_h1(s, 3)
H.test_id(s, 19)
H.run_h1(s, 10)
H.hold(s, False)
H.test_id(s, 80)
A.strike(s, H.body_of(s), 5000)
H.run_h1(s, 2)
ck(f'the floor reached while groggy: the groggy is cut to its kip-up ({KIP} t)', (H.bal(s, 'grgT') or 0) <= KIP and H.hr(s, '#fl') == 1,
   (H.bal(s, 'grgT'), H.hr(s, '#fl')))
ok = H.until_h1(s, lambda s: H.hr(s, '#ph') == api.PH['cs1'], KIP + api.GROGGY_RECOVER + 10)
ck('... and the step (CS1) starts when it ended', ok, H.hr(s, '#ph'))

# ---- HA-02 (review H-A, lead ruling): hits during the groggy queue nothing; the first pattern after it waits for the
#      full recovery (the same tick as a run without hits); a skill hit there does not start A6
def skill_strike(s, b, dmg):
    pl = s.player()
    s.call('rlk:combat/clear_atkflags', H.Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    for k, v in (('#dmg', dmg), ('#elem', 0), ('#elU', 0), ('#icd', 0), ('#crit', 0), ('#stunHit', 0), ('#hitLanded', 0),
                 ('#bowHit', 0), ('#lunar', 0), ('#tfm', 0), ('#trueDmg', 0), ('#skillDmg', 1)):
        s.setsc(k, 'tmp', v)
    s.stack.append('rlk:azsim/strike')
    try:
        s.call('rlk:combat/apply', H.Ctx(b, tuple(b.pos), tuple(b.rot)))
    finally:
        s.stack.pop()
    s.setsc('#skillDmg', 'tmp', 0)


def after_groggy(seed, how):
    """the groggy (test 19) after 260 t of the phase (A6's grace over), the player 2.5 b away; how: None / 'basic' (a hit
    every 8 t in its last 60 t) / 'skill' (one skill hit at grgT 30); returns (the first pattern's key, ticks after the
    groggy's last tick, the queued flags at that tick)"""
    s, pl = H.setup_h1(DP, seed=seed)
    assert H.fight_sc(s)
    H.facing_setup(s, 2.5)
    H.hold(s)
    H.run_h1(s, 260, each=H.heal)
    H.test_id(s, 19)
    H.hold(s, False)
    t_end, k = None, 0
    for _ in range(260):
        H.heal(s)
        g = H.bal(s, 'grgT') or 0
        if 0 < g <= 60 and how == 'basic':
            if k % 8 == 0:
                A.strike(s, H.body_of(s), 5)
            k += 1
        if g == 30 and how == 'skill':
            skill_strike(s, H.body_of(s), 5)
        H.world_h1(s)
        if t_end is None and g > 0 and (H.bal(s, 'grgT') or 0) == 0:
            t_end = s.t
            flags = tuple(H.hr(s, x) or 0 for x in ('#ctr', '#flq', '#a6q', '#hits'))
        if t_end is not None and (H.hr(s, '#pat') or 0) > 0:
            return {v: k_ for k_, v in S.TID.items()}.get(H.hr(s, '#pat')), s.t - t_end, flags
    return None, None, None


for seed in (6, 7, 8, 9):
    base = after_groggy(seed, None)
    for how in ('basic', 'skill'):
        got = after_groggy(seed, how)
        ck(f'HA-02 seed {seed}: {how} hits in the groggy\'s last 60 t: nothing queued at its end, the first pattern '
           f'after the full recovery ({base[1]} t, as without hits: no counter, no A6 at its end)',
           got[2] == (0, 0, 0, 0) and got[1] == base[1] and got[1] >= api.GROGGY_RECOVER - 1,
           (base, got))

# ---- HA-04 (review H-A): /reload during the groggy: the rig respawns in its idle pose; she lies in the down loop at
#      once, the kip-up at 20 left as without the reload (the clip's tick follows the groggy's clock)
def rig_after(reload_at):
    s = fresh()
    H.run_h1(s, 3)
    H.test_id(s, 19)
    log = []
    b = H.body_of(s)
    for _ in range(105):
        g = H.bal(s, 'grgT') or 0
        if g == reload_at:
            H.call_sc(s, 'reload')
            log.append(('reload', g, s.sc(('e', b.id), 'hrRigC'), s.sc(('e', b.id), 'hrRigT')))
        H.heal(s)
        H.world_h1(s)
        g2 = H.bal(s, 'grgT') or 0
        log.append((g2, s.sc(('e', b.id), 'hrRigC'), s.sc(('e', b.id), 'hrRigT')))
        if g2 == 0:
            break
    return log


ref = {x[0]: x[1:] for x in rig_after(-1) if len(x) == 3}
for at in (95, 60, 12):
    log = rig_after(at)
    i = next(i for i, x in enumerate(log) if x[0] == 'reload')
    after = [x for x in log[i + 1:] if len(x) == 3]
    want_c = S.clip_id('down') if at > KIP else S.clip_id('kipup')
    kip = [(x[0], x[1:], ref.get(x[0])) for x in after if 0 < x[0] <= min(at - 1, KIP)]
    ck(f'HA-04: /reload at grgT {at}: the next tick shows {"down" if at > KIP else "kipup"} (not idle), and from the '
       f'kip-up on the same clip and tick as without the reload',
       after and after[0][1] == want_c and kip and all(x[1] == x[2] for x in kip), (after[:2], kip[:3]))

# ---- HA-05 (review H-A): every pattern's airborne ticks (her body = the rig's root above the floor) are refused by bal_ok
#      (a break there waits for the landing instead of dropping her to the floor); a4's ring hop 28-38 too
DIST = {'a1': 3.0, 'a2': 3.0, 'a3': 3.0, 'a3s': 3.0, 'a4': 9.0, 'a9': 4.0, 'a10': 6.0, 'd4': 2.6, 'tri': 8.0, 'rings': 2.4,
        'ult': 2.4, 'hcut': 14.0, 'blue': 5.0, 'kcut': 5.0, 'mx': 3.0, 'nb': 9.0, 'q': 10.0}
for key in [k for k in api.P1 + api.P2 if k in DIST]:
    s = fresh(p2=key in api.P2)
    H.facing_setup(s, DIST[key])
    tid = S.TID[key]
    H.start_pattern(s, tid)
    if key == 'ult':
        H.until_h1(s, lambda s: (H.hr(s, '#pat') or 0) == tid, 120, each=lambda s: H.heal(s))
    air, bad = 0, []
    for _ in range(260):
        if (H.hr(s, '#pat') or 0) != tid:
            break
        H.heal(s)
        H.world_h1(s)
        b = H.body_of(s)
        if (H.hr(s, '#pat') or 0) == tid and b.pos[1] > api.CY + 0.05:
            air += 1
            if s.call(H.ROOT_SC + 'bal_ok', H.Ctx(b, tuple(b.pos), tuple(b.rot))):
                bad.append((H.hr(s, '#pt'), round(b.pos[1] - api.CY, 2)))
    ck(f'HA-05 {key}: bal_ok refuses every airborne tick ({air} t in the air)', not bad, bad[:6])
s = fresh()
H.facing_setup(s, 9.0)
H.start_pattern(s, S.TID['a4'])
H.until_h1(s, lambda s: (H.hr(s, '#pt') or 0) >= 31, 60, each=lambda s: H.heal(s))
y0 = H.body_of(s).pos[1]
brk(s)
y1 = H.body_of(s).pos[1]
ck('HA-05 a4: a break on the ring hop (pt 31) waits (pending): she stays up, then lands, then the groggy',
   'rlk_bal_pend' in tags(s) and (H.bal(s, 'grgT') or 0) == 0 and y0 > api.CY + 0.3 and abs(y1 - y0) < 1e-6, (sorted(tags(s)), y0, y1))
H.until_h1(s, lambda s: (H.bal(s, 'grgT') or 0) > 0, 60, each=lambda s: H.heal(s))
ck('HA-05 a4: ... and starts once she has landed', (H.bal(s, 'grgT') or 0) > 0 and abs(H.body_of(s).pos[1] - api.CY) < 0.06,
   (H.bal(s, 'grgT'), H.body_of(s).pos[1]))

# ---- + 3 after the repel {at:60}
s = fresh()
b = H.body_of(s)
s.setsc(('e', b.id), 'bal', 5)
H.test_id(s, 22)                                   # G1 with the gauge at 0 -> the repel -> P2
H.until_h1(s, lambda s: H.hr(s, '#ph') == api.PH['p2'], api.JUDGE_T['a8'] + api.SEQ_LEN['repel'] + 10, each=lambda s: H.heal(s))
ck(f'after the repel {{at:60}}: balance + {api.BAL["after_repel"]}', H.bal(s) == 5 + api.BAL['after_repel'], H.bal(s))
ck(f'... and P2 at once with a {api.P2_RECOVER}-t recovery, balance damage on', (H.hr(s, '#ph'), s.sc('#mbBalOff', 'mb')) == (api.PH['p2'], 0)
   and (H.hr(s, '#rec') or 0) >= api.P2_RECOVER - 1, (H.hr(s, '#ph'), H.hr(s, '#rec')))

# ---- the perfect-parry flinch
for key, dist, ph in (('a1', 3.0, 1), ('a3s', 3.0, 1), ('d4', 2.6, 1), ('mx', 8.0, 2)):
    s = fresh(p2=(ph == 2))
    H.facing_setup(s, dist)
    last = max(E(c, e) for i, (c, e, *_r) in enumerate(api.HITS[key]))
    n0 = len(s.rigl)
    H.start_pattern(s, S.TID[key])
    t0 = s.t
    s.press(at=t0 + last - 1)
    H.until_h1(s, lambda s: (H.hr(s, '#pat') or 0) == 0, 200, each=lambda s: H.heal(s))
    fl = [t - t0 for t, c in s.rigl[n0:] if c == 'play/flinch']
    ck(f'{key}: a perfect parry on its last hit: she flinches the tick after, the pattern ends {api.PP_FLINCH} t later',
       fl == [last + 1] and s.t - t0 == last + 1 + api.PP_FLINCH, (fl, s.t - t0))
    ck(f'{key}: ... and it cost her one balance pip', H.bal(s) == 11, H.bal(s))
s = fresh()
H.start_pattern(s, S.TID['a3'])
t0 = s.t
s.press(at=t0 + E('a3', 'h1') - 1)
H.until_h1(s, lambda s: (H.hr(s, '#pat') or 0) == 0, 200, each=lambda s: H.heal(s))
ck('a3: a perfect parry on its first hit: the chain goes on to its end', s.t - t0 == api.PAT_END['a3'], s.t - t0)
sys.exit(P.summary('test_bal_hr'))

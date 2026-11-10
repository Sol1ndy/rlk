#!/usr/bin/env python3
"""test_scarlet.py: the core of the rebuilt 홍련 fight (hr_design §1.1, §1.5, §3.6, §5.1, §6.1; lane H1): the phase
machine intro -> P1 -> CS1 -> lead60 -> G1 -> repel {at:60} -> P2 -> lead5 -> G2 -> repel {at:5} -> the kill -> the ending
(no down window: #ph 6 never occurs), the floors and the invulnerable windows, the fails (G1 -> P2, G2 -> the instant death
-> the revive stance -> lead_re -> G2), the skips of CS0 and CS1, pause / reload of the locked sequences, the new test ids,
the framework flags (#mbNpOwn for the whole fight; cleanup resets #gau, #mbNpOwn, #mbBalOff), the tick cost.
The sequences are the core stand-ins until lane H2's seq.py lands (the lengths and signals are the contract's either way).
    python3 test_scarlet.py <roguelike>      (from a copy of tools/dev/sim outside the datapack)
"""
import sys

import pat_lib as P
from pat_lib import ck, H

DP = sys.argv[1]
api, S = P.load_api(DP)
A = H.A
PH, L = api.PH, api.SEQ_LEN
ph = lambda s: H.hr(s, '#ph')          # noqa: E731


def fresh(seed=8, intro=False, revive=0):
    s, pl = H.setup_h1(DP, seed=seed)
    assert H.fight_sc(s, intro=intro)
    s.revive = revive
    return s


def hp(s):
    b = H.body_of(s)
    return s.sc(('e', b.id), 'mhpC'), s.sc(('e', b.id), 'mhpM')


def heal(s):
    H.heal(s)


def to(s, cond, limit, each=heal):
    return H.until_h1(s, cond, limit, each=each)


# ---------------------------------------------------------------------------------------------- the whole chain
s = fresh()
ck('spawn: her own flashes for the whole fight (#mbNpOwn 1), balance on (#mbBalOff 0)', (s.sc('#mbNpOwn', 'mb'), s.sc('#mbBalOff', 'mb') or 0) == (1, 0))
ck('P1 after the intro: the 60 % floor, the gauge shown empty', ph(s) == PH['p1'] and H.hr(s, '#gau') == 0 and H.hr(s, '#hud') == 1
   and s.sc('#mbFloor', 'mb') == H.hr(s, '#fl60'), (ph(s), s.sc('#mbFloor', 'mb'), H.hr(s, '#fl60')))
seen = set()
H.facing_setup(s, 3.0)
to(s, lambda s: (H.hr(s, '#pat') or 0) > 0, 60)
H.test_id(s, 80)
A.strike(s, H.body_of(s), 99999)
c, m = hp(s)
ck('the hit that reaches the 60 % floor stops there', c == H.hr(s, '#fl60'), (c, H.hr(s, '#fl60')))
H.world_h1(s)
ck('the floor step is reserved, the running pattern finishes first', H.hr(s, '#fl') == 1 and ph(s) == PH['p1'] and (H.hr(s, '#pat') or 0) > 0,
   (H.hr(s, '#fl'), ph(s), H.hr(s, '#pat')))
ok = to(s, lambda s: ph(s) == PH['cs1'], 200)
ck('CS1 at the next decision: cine, bars off, invulnerable, the floor -> 5 %', ok and (s.sc('#mbCine', 'mb'), s.sc('#mbBarOff', 'mb'), H.hr(s, '#inv'))
   == (1, 1, 1) and s.sc('#mbFloor', 'mb') == H.hr(s, '#fl5'), (s.sc('#mbCine', 'mb'), s.sc('#mbBarOff', 'mb'), H.hr(s, '#inv')))
t_cs1 = s.t
ok = to(s, lambda s: ph(s) == PH['lead60'], L['cs1'] + 5, each=lambda s: (heal(s), seen.add(ph(s))))
ck(f'CS1 lasts {L["cs1"]} t, then lead60: bars on, cine off, no balance damage, still invulnerable',
   ok and s.t - t_cs1 == L['cs1'] and (s.sc('#mbCine', 'mb'), s.sc('#mbBarOff', 'mb'), s.sc('#mbBalOff', 'mb'), H.hr(s, '#inv')) == (0, 0, 1, 1),
   (s.t - t_cs1, s.sc('#mbCine', 'mb'), s.sc('#mbBarOff', 'mb'), s.sc('#mbBalOff', 'mb')))
t1 = s.t
ok = to(s, lambda s: ph(s) == PH['a8'], L['lead60'] + 5)
ck(f'lead60 lasts {L["lead60"]} t, then G1', ok and s.t - t1 == L['lead60'] and H.hr(s, '#pat') == S.TID['a8'], s.t - t1)
t1 = s.t
jt = api.JUDGE_T['a8']
to(s, lambda s: s.t - t1 >= jt - 1, jt + 5, each=lambda s: (heal(s), seen.add(ph(s))))
s.setsc('#gau', 'hr', 0)
c0, m = hp(s)
H.world_h1(s)
ck('G1 judged with the gauge at 0: the repel {at:60} starts in the judge tick, bars on', (ph(s), H.hr(s, '#sqn'), s.sc('#mbBarOff', 'mb')) ==
   (PH['cs2'], S.SEQ_ID['repel'], 0), (ph(s), H.hr(s, '#sqn')))
t1 = s.t
steps = {}
last = c0


def hpstep(s):
    global last
    heal(s)
    seen.add(ph(s))
    c, _m = hp(s)
    if c != last:
        steps[s.t - t1] = last - c
        last = c


ok = to(s, lambda s: ph(s) == PH['p2'], L['repel'] + 5, each=hpstep)
want = {api.ev('repel', e) + 1: m * 15 // 1000 for e in api.COUNTER_EV}
ck('the repel: three true-damage steps of 15 per mille at strike / land / kick', {k: v for k, v in steps.items()} == want or
   sorted(steps.values()) == sorted(want.values()) and len(steps) == 3, (steps, want))
ck(f'the repel lasts {L["repel"]} t, then P2 at once (no down window), a {api.P2_RECOVER}-t recovery, hittable',
   ok and s.t - t1 == L['repel'] and (H.hr(s, '#inv'), s.sc('#mbCine', 'mb'), s.sc('#mbBalOff', 'mb')) == (0, 0, 0)
   and (H.hr(s, '#rec') or 0) >= api.P2_RECOVER - 1, (s.t - t1, H.hr(s, '#inv'), H.hr(s, '#rec')))
H.world_h1(s)
ck('P2: not invulnerable any more', 'rlk_mb_inv' not in H.body_of(s).tags)
H.test_id(s, 34)
A.strike(s, H.body_of(s), 99999)
H.world_h1(s)
ck('the 5 % floor: the step is reserved in P2', H.hr(s, '#fl') == 2 and hp(s)[0] == H.hr(s, '#fl5'), (H.hr(s, '#fl'), hp(s)[0], H.hr(s, '#fl5')))
ok = to(s, lambda s: ph(s) == PH['lead'], 200, each=lambda s: (heal(s), seen.add(ph(s))))
t1 = s.t
ck('lead5 at the next decision: invulnerable, no balance damage', ok and (H.hr(s, '#sqn'), H.hr(s, '#inv'), s.sc('#mbBalOff', 'mb')) ==
   (S.SEQ_ID['lead5'], 1, 1), (H.hr(s, '#sqn'), H.hr(s, '#inv')))
ok = to(s, lambda s: ph(s) == PH['a13'], L['lead5'] + 5)
ck(f'lead5 lasts {L["lead5"]} t, then G2', ok and s.t - t1 == L['lead5'], s.t - t1)
t1 = s.t
jt = api.JUDGE_T['a13']
to(s, lambda s: s.t - t1 >= jt - 1, jt + 5, each=lambda s: (heal(s), seen.add(ph(s))))
s.setsc('#gau', 'hr', 0)
H.world_h1(s)
ck('G2 judged with the gauge at 0: the repel {at:5}', (ph(s), H.hr(s, '#sqn')) == (PH['cs3'], S.SEQ_ID['repel']), (ph(s), H.hr(s, '#sqn')))
t1 = s.t
ok = to(s, lambda s: (H.mb(s, '#mbSt') or 0) == 2, L['repel'] + 5, each=lambda s: (heal(s), seen.add(ph(s))))
ck(f'the repel {{at:5}}: the kill at its kick ({api.ev("repel", "kick")}), the death state, the ending starts',
   ok and s.t - t1 in (api.ev('repel', 'kick'), api.ev('repel', 'kick') + 1) and (ph(s), H.hr(s, '#sqn')) == (PH['death'], S.SEQ_ID['ending']),
   (s.t - t1, ph(s), H.hr(s, '#sqn')))
t1 = s.t
ok = to(s, lambda s: H.hr(s, '#sqn') == S.SEQ_ID['event'], L['ending'] + 5)
ck(f'the ending lasts {L["ending"]} t, then the coda', ok and s.t - t1 in (L['ending'], L['ending'] - 1), s.t - t1)
ck('the down window is gone: #ph 6 never occurred', PH['down'] not in seen, sorted(x for x in seen if x is not None))

# ---------------------------------------------------------------------------------------------- the fails
s = fresh()
H.test_id(s, 23)
ok = to(s, lambda s: ph(s) == PH['p2'], api.FAIL60_P2_T + 5)
ck(f'G1 fail: P2 at T + {api.FAIL60_P2_T} (no repel), the player alive', ok and not s.deaths and (H.hr(s, '#rec') or 0) >= 0)
s = fresh(revive=40)
H.test_id(s, 29)
t1 = s.t
to(s, lambda s: bool(s.deaths), api.JUDGE_T['a13'] + 5)
ck('G2 fail: the instant death at the judge', s.deaths == [t1 + api.JUDGE_T['a13']], s.deaths)
ok = to(s, lambda s: (H.hr(s, '#rvw') or 0) > 0, 120, each=None)
ck('... survived (Ronova): the revive stance', ok and ph(s) == PH['lead'], (ph(s), H.hr(s, '#rvw')))
ok = to(s, lambda s: H.hr(s, '#sqn') == S.SEQ_ID['lead_re'], api.REVIVE['wait'] + 5)
ck(f'... {api.REVIVE["wait"]} t later lead_re {{g:a13}}', ok)
ok = to(s, lambda s: ph(s) == PH['a13'], L['lead_re'] + 5)
ck('... then G2 again with 5/5', ok and H.hr(s, '#gau') == api.GAUGE['max'], H.hr(s, '#gau'))

# ---------------------------------------------------------------------------------------------- the skips
s = fresh()
H.test_id(s, 36)
H.run_h1(s, 101)
ck(f'test 36: CS1 skipped at its tick 100 -> the clock jumps to {api.SKIP["cs1"]["to"]}', H.hr(s, '#sq') in
   (api.SKIP['cs1']['to'], api.SKIP['cs1']['to'] - 1), H.hr(s, '#sq'))
ok = to(s, lambda s: ph(s) == PH['lead60'], L['cs1'] - api.SKIP['cs1']['to'] + 5)
ck('... and CS1 ends into lead60', ok)
s = fresh()
H.test_id(s, 35)
H.run_h1(s, 101)
ck(f'test 35: the intro replay skipped at its tick 100 -> {api.SKIP_T}', H.hr(s, '#sq') in (api.SKIP_T, api.SKIP_T - 1), H.hr(s, '#sq'))
s = fresh(intro=True)
pl = s.player()
H.run_h1(s, 30)
pl.data['sneak'] = 1
H.run_h1(s, api.SKIP_HOLD + 2)
ck('CS0: sneak held 20 t inside the window skips to its last shots', (H.hr(s, '#sq') or 0) >= api.SKIP_T, H.hr(s, '#sq'))
pl.data['sneak'] = 0
ok = H.until_h1(s, lambda s: ph(s) == PH['p1'] and (H.mb(s, '#mbSt') or 0) == 1, L['intro'] - api.SKIP_T + 20)
ck('... and control comes at its end', ok)

# ---------------------------------------------------------------------------------------------- pause / reload (§3.6)
def pause(s, n=4):
    pid = ('e', s.player().id)
    s.setsc(pid, 'pkMode', 1)
    H.run_h1(s, n)
    s.setsc(pid, 'pkMode', 0)
    H.run_h1(s, 2)


s = fresh()
H.test_id(s, 20)
H.run_h1(s, 200)
pause(s)
ck('a pause in CS1: at resume its end state = lead60 from 0 (crimson asked, bars on, gauge 5/5)',
   (ph(s), H.hr(s, '#sqn'), s.sc('#mbBarOff', 'mb'), H.hr(s, '#gau')) == (PH['lead60'], S.SEQ_ID['lead60'], 0, api.GAUGE['max'])
   and (H.hr(s, '#sq') or 0) <= 2, (ph(s), H.hr(s, '#sqn'), H.hr(s, '#sq')))
s = fresh()
H.test_id(s, 24)
c0, m = hp(s)
H.run_h1(s, 60)
pause(s)
c1, _m = hp(s)
ck('a pause in the repel {at:60}: at resume its end state (all three HP steps, P2)', ph(s) == PH['p2'] and c0 - c1 == 3 * (m * 15 // 1000),
   (ph(s), c0 - c1, m))
s = fresh()
H.test_id(s, 26)
H.run_h1(s, 70)
pause(s)
ck('a pause in lead5: it restarts from 0', (H.hr(s, '#sqn'), ) == (S.SEQ_ID['lead5'],) and (H.hr(s, '#sq') or 0) <= 2, (H.hr(s, '#sqn'), H.hr(s, '#sq')))
s = fresh()
H.facing_setup(s, 3.0)
H.start_pattern(s, S.TID['a3'])
H.run_h1(s, 20)
H.call_sc(s, 'reload')
ck('/reload in a P1 pattern: cancelled, the recovery', (H.hr(s, '#pat') or 0) == 0 and ph(s) == PH['p1'] and
   not [e for e in s.ents if e.alive and 'rlk_hr_p_a3' in e.tags])
s = fresh()
H.test_id(s, 20)
H.run_h1(s, 100)
H.call_sc(s, 'reload')
H.run_h1(s, 2)
ck('/reload in CS1: lead60 from 0', (ph(s), H.hr(s, '#sqn')) == (PH['lead60'], S.SEQ_ID['lead60']), (ph(s), H.hr(s, '#sqn')))

# ---------------------------------------------------------------------------------------------- the test ids
s = fresh()
bad = []
for tid in sorted(api.TEST_IDS):
    try:
        H.test_id(s, tid)
        H.run_h1(s, 3, each=heal)
    except Exception as e:      # noqa: BLE001
        bad.append((tid, repr(e)[:80]))
    if tid in (29,):
        s = fresh()
    else:
        H.heal(s)
ck(f'every test id runs ({len(api.TEST_IDS)} ids)', not bad, bad)
ck('the removed ids are gone (25 the down window, 31 the dark look)', not {25, 31} & set(api.TEST_IDS))
s = fresh()
H.test_id(s, 37)
ck('test 37: the gauge is full', H.hr(s, '#gau') == api.GAUGE['max'])
H.test_id(s, 38)
ck('test 38: her balance is 1 pip', H.bal(s) == 1, H.bal(s))
H.test_id(s, 33)
ck('test 33: P2 now', ph(s) == PH['p2'])
for tid, key in ((16, 'mx'), (17, 'nb'), (18, 'q'), (9, 'd4'), (13, 'hcut')):
    H.test_id(s, tid)
    ck(f'test {tid}: {key} starts', H.hr(s, '#pat') == S.TID[key], H.hr(s, '#pat'))
    H.run_h1(s, 2, each=heal)

# ---------------------------------------------------------------------------------------------- cleanup
s = fresh()
H.test_id(s, 21)
H.run_h1(s, 40, each=heal)
ck('in a gauntlet: #mbBalOff 1, the gauge full', (s.sc('#mbBalOff', 'mb'), H.hr(s, '#gau')) == (1, api.GAUGE['max']))
H.call_sc(s, 'cleanup')
left = [e for e in s.ents if e.alive and any(t.startswith('rlk_hr_') for t in e.tags) and e.etype != 'husk']
ck('cleanup: #gau, #mbNpOwn and #mbBalOff are reset, no rlk_hr_* entity is left',
   ((H.hr(s, '#gau') or 0), s.sc('#mbNpOwn', 'mb'), s.sc('#mbBalOff', 'mb'), len(left)) == (0, 0, 0, 0),
   (H.hr(s, '#gau'), s.sc('#mbNpOwn', 'mb'), s.sc('#mbBalOff', 'mb'), len(left)))

# ---------------------------------------------------------------------------------------------- the tick cost
for name, tid in (('P1', None), ('P2', 33)):
    s = fresh(seed=21)
    if tid:
        H.test_id(s, tid)
    H.facing_setup(s, 4.0)
    n0 = len(s.cmd_hist)
    H.run_h1(s, 1200, each=heal)
    avg = sum(s.cmd_hist[n0:]) / max(1, len(s.cmd_hist) - n0)
    ck(f'{name}: {avg:.0f} commands per tick on average over 1200 t (budget 830)', avg <= 830, avg)
sys.exit(P.summary('test_scarlet'))

#!/usr/bin/env python3
"""pat_ghost.py: the gauntlets G1 (a8, 60 %) and G2 (a13, 5 %) of the rebuilt 홍련 fight (hr_design §1.2, §2.4, §6.1; lane
H1): both scripts' made / lock / strike, every cut a parryable disc with the cue at its lock, gaps >= 14 t; a perfect parry
on a cut takes exactly one segment, a perfect dodge / a tier 2 / a tier 1 parry / walking out take none; 5 perfect parries
-> the repel starts in the judge tick, 4 -> the fail of each gauntlet; no balance pip leaves during a gauntlet (#mbBalOff);
a pause / a reload restarts it through lead_re {g} with the gauge 5/5.
    python3 pat_ghost.py <roguelike>      (from a copy of tools/dev/sim outside the datapack)
"""
import sys

import pat_lib as P
from pat_lib import ck, H

DP = sys.argv[1]
api, S = P.load_api(DP)
SEG, MAXG = api.GAUGE['seg'], api.GAUGE['max']
TEST = {'a8': 21, 'a13': 27}
CUTS = {g: [r[3] for r in api.SCRIPTS[g] if r[3]] for g in api.GAUNTLETS}


def start(g, seed=9, revive=0):
    s, pl = H.setup_h1(DP, seed=seed)
    assert H.fight_sc(s)
    s.revive = revive
    H.facing_setup(s, 6.0)
    H.test_id(s, TEST[g])
    return s, s.t


def run(s, t0, until_t, each=None, heal=True):
    def e(s):
        if heal:
            H.heal(s)
        if each:
            each(s)
    while s.t < t0 + until_t:
        e(s)
        H.world_h1(s)


for g in api.GAUNTLETS:
    cuts = CUTS[g]
    jt = api.JUDGE_T[g]
    s, t0 = start(g)
    ck(f'{g}: the gauntlet starts with the gauge 5/5, no balance damage (#mbBalOff 1), invulnerable',
       (H.hr(s, '#gau'), s.sc('#mbBalOff', 'mb'), 'rlk_mb_inv' in H.body_of(s).tags) == (MAXG, 1, True),
       (H.hr(s, '#gau'), s.sc('#mbBalOff', 'mb')))
    n0, k0 = len(s.hzr), len(s.kitl)
    run(s, t0, jt - 1)
    hz = [h for h in s.hzr[n0:]]
    ck(f'{g}: {len(cuts)} cuts made / struck as the script', [(h['pt'], h['pt'] + h['tell']) for h in hz] == [(c[0], c[2]) for c in cuts],
       [(h['pt'], h['pt'] + h['tell']) for h in hz])
    ck(f'{g}: every cut a quiet parryable Electro disc r {api.CUT_R}, tier TC, no knockback',
       all((h['kind'], h['r'], h['np'], h['kb'], h['dmg'], h['quiet'], h['el']) == (1, round(api.CUT_R * 10), 0, 0, api.DMG['TC'], 1, api.ELEC)
           for h in hz), [(h['kind'], h['r'], h['np'], h['kb'], h['dmg']) for h in hz][:3])
    cues = sorted(t - t0 for t, c, a in s.kitl[k0:] if c == 'snd/parry_cue')
    ck(f'{g}: the parry cue at every lock tick (strike - {api.LOCK_LEAD})', cues == [c[1] for c in cuts], cues)
    st = [c[2] for c in cuts]
    ck(f'{g}: strike gaps >= {api.CUT_GAP_MIN} t', min(b - a for a, b in zip(st, st[1:])) >= api.CUT_GAP_MIN, st)
    ck(f'{g}: every cut hit the standing player (no parry: {len(cuts)} landed hits)',
       sorted(j['t'] - t0 for j in s.judged if j['t'] > t0) == st and all(j['dodged'] == 0 for j in s.judged if j['t'] > t0))
    ck(f'{g}: unparried cuts take no segment', H.hr(s, '#gau') == MAXG, H.hr(s, '#gau'))
    ck(f'{g}: no dark look was requested', (H.hr(s, '#hrLook') or 0) in (0, api.LOOK_ID['crimson']), H.hr(s, '#hrLook'))

    # a perfect parry on cut k takes exactly one segment (k = first, middle, last), the cut deals no damage
    for k in (0, len(cuts) // 2, len(cuts) - 1):
        s, t0 = start(g)
        s.press(at=t0 + cuts[k][2] - 1)
        gs = {}
        hp0 = s.sc(('e', s.player().id), 'maxHealth')
        run(s, t0, cuts[k][2] + 3, each=lambda s: gs.__setitem__(s.t - t0, H.hr(s, '#gau')), heal=False)
        j = [x for x in s.judged if x['t'] == t0 + cuts[k][2]]
        ck(f'{g} cut {k + 1}: F at h - 1 = a perfect parry', [(x['dodged'], x['parT']) for x in j] == [(1, 3)], j)
        ck(f'{g} cut {k + 1}: exactly one segment goes (seen the tick after the strike)',
           (gs.get(cuts[k][2]), H.hr(s, '#gau')) == (MAXG, MAXG - SEG), (gs.get(cuts[k][2]), H.hr(s, '#gau')))
        ck(f'{g} cut {k + 1}: no balance pip leaves (#mbBalOff)', H.bal(s) == H.bal(s, 'balMax'), H.bal(s))
    # a perfect dodge, a tier-2 and a tier-1 parry, walking out: no segment
    for name, act in (('perfect dodge', lambda s, t0, h: s.dodge(at=t0 + h - 1)), ('tier-2 parry', lambda s, t0, h: s.press(at=t0 + h - 4)),
                      ('tier-1 parry', lambda s, t0, h: s.press(at=t0 + h - 7))):
        s, t0 = start(g)
        h = cuts[0][2]
        act(s, t0, h)
        run(s, t0, h + 3)
        j = [x for x in s.judged if x['t'] == t0 + h]
        want = {'perfect dodge': (1, 0, 1), 'tier-2 parry': (0, 2, 0), 'tier-1 parry': (0, 1, 0)}[name]
        ck(f'{g}: a {name} of a cut is judged so and takes no segment',
           [(x['dodged'], x['parT'], x['pdg']) for x in j] == [want] and H.hr(s, '#gau') == MAXG, (j, H.hr(s, '#gau')))
    s, t0 = start(g)
    lk, h = cuts[0][1], cuts[0][2]

    def walk(s):
        if s.t - t0 >= lk:
            p = s.player()
            H.place_player(s, p.pos[0] + 0.8, p.pos[2])
    run(s, t0, h + 3, each=walk)
    ck(f'{g}: walking out of the locked disc: no hit, no segment', not [x for x in s.judged if x['t'] >= t0 + h - 1] and H.hr(s, '#gau') == MAXG)

    # 5 perfect parries -> the repel starts in the judge tick; 4 -> the fail
    for n in (5, 4):
        s, t0 = start(g, revive=40 if g == 'a13' else 0)
        for c in cuts[:n]:
            s.press(at=t0 + c[2] - 1)
        hp = s.sc(('e', s.player().id), 'maxHealth')
        run(s, t0, jt - 1)
        ck(f'{g}: {n} perfect parries leave {5 - n} segment(s)', H.hr(s, '#gau') == MAXG - n * SEG, H.hr(s, '#gau'))
        H.heal(s)
        H.world_h1(s)
        if n == 5:
            ck(f'{g}: gauge 0 at the judge: the repel starts in the judge tick (#sqn repel, cine, the gauge 0)',
               (H.hr(s, '#sqn'), H.hr(s, '#ph'), s.sc('#mbCine', 'mb'), H.hr(s, '#pat')) ==
               (S.SEQ_ID['repel'], api.PH['cs2' if g == 'a8' else 'cs3'], 1, 0),
               (H.hr(s, '#sqn'), H.hr(s, '#ph'), s.sc('#mbCine', 'mb'), H.hr(s, '#pat')))
            ck(f'{g}: no g_deflect clip is played', not [c for t, c in s.rigl if c.endswith('g_deflect')])
        elif g == 'a8':
            cur = s.sc(('e', s.player().id), 'curHealth')
            ck('a8: 4 perfect parries: the fail-60 hit (500 per mille, never lethal), she reforms',
               H.hr(s, '#gres') == 2 and 0 < cur <= hp - hp * api.FAIL60_PM // 1000 + 2, (H.hr(s, '#gres'), cur, hp))
            run(s, t0, api.FAIL60_P2_T)
            ck(f'a8 fail: P2 at T + {api.FAIL60_P2_T}, balance damage on again, the gauge 0',
               (H.hr(s, '#ph'), s.sc('#mbBalOff', 'mb'), H.hr(s, '#gau')) == (api.PH['p2'], 0, 0),
               (H.hr(s, '#ph'), s.sc('#mbBalOff', 'mb'), H.hr(s, '#gau')))
        else:
            ck('a13: 4 perfect parries: the instant death at the judge (Ronova\'s revive applies)', s.deaths == [t0 + jt], s.deaths)

    # a pause / a reload inside the gauntlet: cancelled, lead_re {g}, the gauntlet again from T0 with 5/5
    for how in ('pause', 'reload'):
        s, t0 = start(g)
        s.press(at=t0 + cuts[0][2] - 1)
        run(s, t0, 100)
        pid = ('e', s.player().id)
        if how == 'pause':
            s.setsc(pid, 'pkMode', 1)
            H.run_h1(s, 5)
            mid = (H.hr(s, '#pat'), H.hr(s, '#gau'), len([e for e in s.ents if e.alive and 'rlk_hr_cut' in e.tags]))
            s.setsc(pid, 'pkMode', 0)
            H.run_h1(s, 2)
        else:
            H.call_sc(s, 'reload')
            mid = (H.hr(s, '#pat'), 0, len([e for e in s.ents if e.alive and 'rlk_hr_cut' in e.tags]))
            H.run_h1(s, 2)
        ck(f'{g} {how}: the gauntlet is cancelled (no pattern, no cut left)', mid[0] == 0 and mid[2] == 0, mid)
        ck(f'{g} {how}: lead_re runs next', (H.hr(s, '#sqn'), H.hr(s, '#ph')) == (S.SEQ_ID['lead_re'], api.PH['lead']),
           (H.hr(s, '#sqn'), H.hr(s, '#ph')))
        ok = H.until_h1(s, lambda s: H.hr(s, '#pat') == S.TID[g], api.SEQ_LEN['lead_re'] + 5, each=lambda s: H.heal(s))
        ck(f'{g} {how}: the gauntlet again from T0 with the gauge 5/5', ok and H.hr(s, '#gau') == MAXG and (H.hr(s, '#pt') or 0) <= 1,
           (ok, H.hr(s, '#gau'), H.hr(s, '#pt')))
sys.exit(P.summary('pat_ghost'))

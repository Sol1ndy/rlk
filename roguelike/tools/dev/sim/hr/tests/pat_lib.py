#!/usr/bin/env python3
"""pat_lib.py: the pattern checks of the rebuilt 홍련 fight (hr_design §6.1; lane H1), shared by pat_p1.py (the P1 kit in
P1 and in P2) and pat_p2.py (mx / nb / q). Each pattern is started through its test id in the H1 world (lib/hrsim.py) with
the player in front of her, once standing and once strafing, and the run is compared with tools/mboss_scarlet/api.py:
  hit ticks = the clip events; shape / size / tier / knockback of every hazard = api.HITS (kb only where the table has it);
  #hzNoParry of every hazard = the table's P / N; quiet, no framework visual, Electro; the parry cue exactly api.CUE_LEAD
  t before every P hit and at no other tick; the flash sound of every N hit at its api.FLASH_AT tick (purple exactly 12 t
  before its cut, yellow >= 12 t); chain gaps >= 10 t; her aim does not turn in the last 7 t before a hit (lock = h - 7);
  the first visible motion -> the first hit >= 12 t (new clips >= 14 t, big hits >= 20 t); her body stays inside
  api.MOVE_R and never below the floor; airborne spans <= api.AIR_MAX; the pattern ends at its PAT_END.
Scratch tool (never shipped). Run from a copy outside the datapack: python3 pat_p1.py <roguelike>.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import hrsim as H  # noqa: E402

R = []


def ck(name, ok, info=''):
    R.append((name, bool(ok)))
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else f'   [{info}]'), flush=True)
    return ok


def load_api(dp):
    sys.path.insert(0, str(Path(dp).resolve() / 'tools'))
    sys.dont_write_bytecode = True
    from mboss_scarlet import api
    from mboss_scarlet import s3lib
    return api, s3lib


KIND = {'sector': 3, 'disc': 1, 'pdisc': 1, 'line': 4, 'dash_line': 4, 'full': 5}
FLASH_SND = {'yellow': 'snd/yellow_chime', 'purple': 'snd/a9_star', 'blue': 'snd/flash_blue'}
BIG = ('ult', 'a9', 'hcut', 'kcut')                      # the whole arena, T4, the yellow dash cuts: >= 20 t


def run_key(dp, api, S, key, ph=1, dist=3.0, strafe=0.0, seed=7):
    """One run of pattern `key` in fight phase ph with the player dist b in front (strafing strafe b/t sideways). Returns
    dict(s, t0, hz, kit, snaps {pt: (pos, yaw)}, end)."""
    s, pl = H.setup_h1(dp, seed=seed)
    assert H.fight_sc(s)
    if ph == 2:
        H.test_id(s, 33)
        H.run_h1(s, 2)
    H.heal(s)
    H.facing_setup(s, dist)
    tid = S.TID[key]
    n0, k0, j0 = len(s.hzr), len(s.kitl), len(s.judged)
    H.start_pattern(s, tid)
    if key == 'ult':                                      # test 12 = rings with ult to follow
        assert H.until_h1(s, lambda s: (H.hr(s, '#pat') or 0) == tid, 120)
        n0, j0 = len(s.hzr), len(s.judged)
        # ult started inside this world tick (its pt 0, after rings' last tick): its kit calls of the tick count
        k0 = next((i for i, (t, c, a) in enumerate(s.kitl) if t >= s.t and c != 'snd/parry_cue'), len(s.kitl))
    t0 = s.t
    snaps = {}

    def each(s):
        if strafe:
            p = s.player()
            H.place_player(s, p.pos[0] + strafe, p.pos[2])
        H.heal(s)

    def rec(s):
        b = H.body_of(s)
        snaps[H.hr(s, '#pt') or 0] = (tuple(b.pos), b.rot[0] % 360)
    for _ in range(260):
        if (H.hr(s, '#pat') or 0) != tid:
            break
        each(s)
        H.world_h1(s)
        if (H.hr(s, '#pat') or 0) == tid:
            rec(s)
    end = s.t - t0
    hz = [dict(h, h=h['pt'] + h['tell']) for h in s.hzr[n0:] if h['pat'] == tid]
    kit = [(t - t0, c, a) for t, c, a in s.kitl[k0:]]
    return dict(s=s, t0=t0, hz=hz, kit=kit, snaps=snaps, end=end, judged=[dict(j, pt=j['t'] - t0) for j in s.judged[j0:]])


def expect_rows(api, key, ph):
    """The api.HITS rows of the fight phase with their pattern tick."""
    out = []
    for i, row in enumerate(api.HITS[key]):
        only = api.HIT_PH.get(key, {}).get(i)
        if only is not None and only != ph:
            continue
        clip, e = row[0], row[1]
        t = api.ev(clip, e) + (api.Q_AIR_T0 if clip == 'q_air' else 0)
        out.append((i, t, row))
    return out


def check_key(dp, api, S, key, ph=1, dist=3.0, label=None, end=None, new=False):
    lab = label or f'{key} P{ph}'
    rows = expect_rows(api, key, ph)
    r0 = run_key(dp, api, S, key, ph, dist)
    hz = sorted(r0['hz'], key=lambda h: (h['h'], h['kind'], -h['r']))
    exp = sorted(rows, key=lambda x: (x[1], KIND[x[2][2]], -(x[2][3][0] * 10 if x[2][3] else 0)))
    ck(f'{lab}: {len(exp)} hazards, hit ticks = the clip events', [h['h'] for h in hz] == [t for _i, t, _r in exp],
       ([h['h'] for h in hz], [t for _i, t, _r in exp]))
    ok_shape = ok_dmg = ok_kb = ok_np = ok_q = True
    bad = []
    for h, (i, t, row) in zip(hz, exp):
        clip, e, shape, dims, tier, kb, par = row
        if h['kind'] != KIND[shape]:
            ok_shape = False
            bad.append(('kind', i, h['kind']))
        if shape in ('sector', 'disc', 'pdisc') and h['r'] != round(dims[0] * 10):
            ok_shape = False
            bad.append(('r', i, h['r']))
        if shape == 'sector' and h['a'] != dims[1]:
            ok_shape = False
            bad.append(('a', i, h['a']))
        if shape == 'line' and (h['r'] != round(dims[0] * 10) or h['hw'] != round(dims[1] * 10)):
            ok_shape = False
            bad.append(('line', i, h['r'], h['hw']))
        if shape == 'dash_line' and (h['hw'] != round(dims[0] * 10) or not 0 < h['r'] <= round(api.DASH_LEN[key] * 10)):
            ok_shape = False
            bad.append(('dash', i, h['r'], h['hw']))
        ok_dmg &= h['dmg'] == api.DMG[tier]
        ok_kb &= h['kb'] == kb
        ok_np &= h['np'] == (1 if par == 'N' else 0)
        ok_q &= h['quiet'] == 1 and (h['vis'] or 0) == 0 and (h['sfx'] or 0) == 0 and h['el'] == api.ELEC
    ck(f'{lab}: shapes and sizes = api.HITS', ok_shape, bad)
    ck(f'{lab}: damage tiers = api.HITS', ok_dmg, [(h['h'], h['dmg']) for h in hz])
    ck(f'{lab}: knockback only where the table has it (the last hit of a chain)', ok_kb, [(h['h'], h['kb']) for h in hz])
    ck(f'{lab}: #hzNoParry of every hazard = the P / N column', ok_np, [(h['h'], h['np']) for h in hz])
    ck(f'{lab}: every hazard quiet, no framework visual / sound, Electro (no decal, no tele)', ok_q)
    # the parry cue
    cues = sorted(t for t, c, a in r0['kit'] if c == 'snd/parry_cue')
    glints = sorted(t for t, c, a in r0['kit'] if c == 'p/glint' and a.get('c') == api.CUE_KIT[1]['c'])
    p_hits = sorted({t for _i, t, row in exp if row[6] == 'P'})
    n_hits = sorted({t for _i, t, row in exp if row[6] == 'N'})
    ck(f'{lab}: the parry cue exactly {api.CUE_LEAD} t before every P hit, nowhere else', cues == [t - api.CUE_LEAD for t in p_hits],
       (cues, p_hits))
    ck(f'{lab}: the cue is the pink glint + its chime in the same tick', glints == cues, (glints, cues))
    ck(f'{lab}: no cue {api.CUE_LEAD} t before an N-only tick', not [t for t in n_hits if t not in p_hits and t - api.CUE_LEAD in cues])
    # the flashes
    want = []
    for i, t, row in exp:
        if row[6] != 'N':
            continue
        for col, clip, e, off in api.FLASH_AT[key][i]:
            want.append((api.ev(clip, e) + off + (api.Q_AIR_T0 if clip == 'q_air' else 0), col))
    got = sorted((t, col) for t, c, a in r0['kit'] for col, snd in FLASH_SND.items() if c == snd)
    ck(f'{lab}: the flash of every N hit at its tick (api.FLASH_AT)', got == sorted(want), (got, sorted(want)))
    for i, t, row in exp:
        if row[6] == 'N':
            for col, clip, e, off in api.FLASH_AT[key][i]:
                ft = api.ev(clip, e) + off + (api.Q_AIR_T0 if clip == 'q_air' else 0)
                if col == 'purple':
                    ck(f'{lab}: purple exactly {api.PURPLE_LEAD} t before the cut at {t}', t - ft == api.PURPLE_LEAD, ft)
                if col == 'yellow':
                    ck(f'{lab}: yellow >= {api.YELLOW_MIN} t before the hit at {t}', t - ft >= api.YELLOW_MIN, ft)
    ck(f'{lab}: an N hit has a flash, a P pattern none', bool(got) == bool(n_hits), (got, n_hits))
    # chain gaps, the first tell
    ts = sorted({t for _i, t, _r in exp})
    ck(f'{lab}: chain hits >= {api.COMBO_GAP} t apart', all(b - a >= api.COMBO_GAP for a, b in zip(ts, ts[1:])), ts)
    need = api.TELL_BIG if key in BIG else 14 if new else api.TELL_MIN
    ck(f'{lab}: first visible motion -> first hit >= {need} t', ts[0] >= need if ts else True, ts[:1])
    # the end
    want_end = end if end is not None else api.RINGS_END[ph] if key == 'rings' else api.PAT_END.get(key)
    if want_end is not None:
        ck(f'{lab}: ends at tick {want_end}', r0['end'] == want_end, r0['end'])
    # the body: inside MOVE_R, never below the floor, airborne spans
    sn = r0['snaps']
    out = [pt for pt, (pos, _y) in sn.items() if math.hypot(pos[0] - api.CX, pos[2] - api.CZ) > api.MOVE_R + 0.01 or pos[1] < api.CY - 0.01]
    ck(f'{lab}: her body inside MOVE_R and never below the floor', not out, out[:5])
    air, run, best = [pt for pt in sorted(sn) if sn[pt][0][1] > api.CY + 0.05], 0, 0
    prev = None
    for pt in air:
        run = run + 1 if prev is not None and pt == prev + 1 else 1
        best = max(best, run)
        prev = pt
    ck(f'{lab}: airborne spans <= {api.AIR_MAX} t (longest {best})', best <= api.AIR_MAX, best)
    # lock = h - 7: with a strafing player her aim does not turn in the last 7 t before a hit, and a hazard on a locked spot
    # stands where the player was 7 t before
    r1 = run_key(dp, api, S, key, ph, dist, strafe=0.2)
    sn = r1['snaps']
    turned = []
    for t in sorted({t for _i, t, row in exp if row[2] in ('sector', 'line', 'disc') and key not in ('nb', 'q')}):
        ys = {round(sn[p][1], 1) for p in range(t - api.LOCK_LEAD, t) if p in sn}
        if len(ys) > 1:
            turned.append((t, sorted(ys)))
    ck(f'{lab}: the aim is locked {api.LOCK_LEAD} t before every hit (a strafing player)', not turned, turned[:3])
    ck(f'{lab}: the same hit ticks against a strafing player', sorted(h['h'] for h in r1['hz']) == sorted(h['h'] for h in hz),
       sorted(h['h'] for h in r1['hz']))
    return r0


def judged_of(r, t):
    return [j for j in r['judged'] if j['pt'] == t]


def summary(name):
    bad = [n for n, ok in R if not ok]
    print(f'{name}: {len(R) - len(bad)}/{len(R)} checks passed' + (f', FAILED: {len(bad)}' if bad else ''))
    return 1 if bad else 0

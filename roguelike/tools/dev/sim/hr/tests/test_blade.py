#!/usr/bin/env python3
"""test_blade.py: 홍련's drawn blade path and slash effects against the rig's blade track (round V, lane VB; v_brief.md §3 VB 1-3).

    python3 test_blade.py <roguelike dir> [-v]          (run from a copy outside the datapack, tools/dev/sim/README.md §1)

Reads what ships: tools/scarlet_blade_track.json (the rig build's sidecar), the rig's anchor table (rig/an/load) and the pattern
functions p/<key>/** as generated (every sweep card is a literal summon on a pattern tick). It fails when
  track    the sidecar is not the built rig's blade (its tip against the anchor table), a fight clip is missing
  windup   a hit's wind-up pose is reached later than the rule (h - 10 for a single / first hit, h - 6 for a chain follow-up) or
           not held to the swing; a gauntlet cut: the pose shown before it (the approach / the move before) counts
  path     a hit has no drawn path, the path shows for fewer ticks than the rule, a piece of it leaves the tip's way of the
           track (> PATH_TOL), its head does not arrive at the tip's place of the hit tick ON the hit tick
  slash    a slash piece's plane is off the blade (> PLANE_TOL deg between the card and the two blade positions that bound it),
           its rim is off the tip's way (> RIM_TOL), it is born on another tick than its sweep is shown, runs against the
           blade's travel, or outlives the rule (gone ARC_LIFE t after its birth, <= ~6 t after the hit's follow-through)
  size     a path / effect card is thinner than 0.12 b
  lines    a dash / dive hit has no target line shown >= the rule before it whose head arrives on the hit tick; kcut's three
           lines / nb's bands do not run through the locked spot at their yaws
  clock    a sweep command outside the pattern-tick files (the path, the head and the slash are a pure function of #pt hr)
"""
import json
import math
import re
import sys
from pathlib import Path

WT = Path(sys.argv[1]).resolve()
VERBOSE = '-v' in sys.argv[2:]
sys.path.insert(0, str(WT / 'tools'))
sys.dont_write_bytecode = True
from mboss_scarlet import api, blade as B  # noqa: E402

MOD = WT / 'data/rlk/function/boss/scarlet'
FAILS, N = [], [0]
PATH_TOL, RIM_TOL, PLANE_TOL, APEX_TOL = 0.04, 0.12, 4.0, 0.2
MIN_THICK = 0.12


def check(ok, msg, detail=''):
    N[0] += 1
    if not ok:
        FAILS.append(msg)
        print('FAIL', msg, detail)
    elif VERBOSE:
        print('ok  ', msg, detail)


# ----------------------------------------------------------------------------- track
T = json.loads((WT / 'tools/scarlet_blade_track.json').read_text())['clips']
fight = [k for k in api.CLIPS if k not in api.CINE_CLIPS]
check(sorted(T) == sorted(fight), 'track: one row per fight clip', sorted(set(fight) ^ set(T)))
check(all(len(T[k]['t']) == api.CLIPS[k][0] + 1 == len(T[k]['b']) for k in T), 'track: ticks 0 .. len per clip')
MAN = json.loads((WT / 'tools/scarlet_rig_manifest.json').read_text())
AN = {}
for line in (MOD / 'rig/an/load.mcfunction').read_text().splitlines():
    m = re.match(r'data modify storage rlk:hr rig\.an\[(\d+)\]\.(\w+) set value (\[.*\])$', line)
    if m and m.group(2) in ('blade_tip', 'blade_mid'):
        AN[(int(m.group(1)), m.group(2))] = [[float(v.lstrip('^') or 0) for v in s_.split()] for s_ in json.loads(m.group(3))]
worst = 0.0
for k in T:
    cid = MAN['clips'][k]['id']
    for t in range(api.CLIPS[k][0] + 1):
        tip, mid = AN[(cid, 'blade_tip')][t], AN[(cid, 'blade_mid')][t]
        base = [2 * m_ - t_ for m_, t_ in zip(mid, tip)]
        worst = max(worst, math.dist(tip, T[k]['t'][t]), math.dist(base, T[k]['b'][t]) / 3)
check(worst <= 0.012, f'track: the sidecar is the built rig\'s blade (worst {worst:.4f} b against rig/an/load)')


# ----------------------------------------------------------------------------- the shipped sweep commands per pattern tick
def pattern_ticks(key):
    """{pattern tick: [command lines]} of p/<key>: start (0), the tick file's own lines and ranges, the k/<t> files."""
    out = {}
    d = MOD / 'p' / key

    def add(t, ln):
        out.setdefault(t, []).append(ln)
    for ln in (d / 'start.mcfunction').read_text().splitlines():
        add(0, ln)
    for ln in (d / 'tick.mcfunction').read_text().splitlines():
        m = re.match(r'execute if score #pt hr matches (\d+)(?:\.\.(\d+))? (.*)$', ln)
        if not m or '/k/' in m.group(3) or '/b/' in m.group(3):
            continue
        for t in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
            add(t, m.group(3))
    if (d / 'k').is_dir():
        for f in (d / 'k').glob('*.mcfunction'):
            for ln in f.read_text().splitlines():
                add(int(f.stem), ln)
    return out


NB = re.compile(r'summon minecraft:item_display ~ ~ ~ (\{.*\})\s*$')


def qrot(q, v):
    x, y, z, w = q
    u = (x, y, z)
    c1 = B.cross(u, v)
    c2 = B.cross(u, c1)
    return tuple(v[i] + 2 * (w * c1[i] + c2[i]) for i in range(3))


def cards_of(key):
    """Every sweep card the pattern summons: dict(t born, tags, kind, tr, q, s, col, kill, frames {tick: model}), and the head
    moves {uid tag: [(tick, point)]}, the head kills."""
    ticks = pattern_ticks(key)
    cards, heads, hkill, other = [], {}, {}, []
    for t in sorted(ticks):
        for ln in ticks[t]:
            if 'rlk_hr_sw' not in ln and 'core/sw/' not in ln and 'core.sw' not in ln:
                continue
            m = NB.search(ln)
            if m:
                s_ = m.group(1)
                tags = re.search(r'Tags:\[([^\]]*)\]', s_).group(1).replace('"', '').split(',')
                num = lambda k: [float(v.rstrip('f')) for v in re.search(k + r':\[([^\]]*)\]', s_).group(1).split(',')]   # noqa: E731
                cards.append(dict(t=t, tags=tags, kind=re.search(r'hr_kit/(\w+)"', s_).group(1), tr=num('translation'),
                                  q=num('left_rotation'), s=num('scale'), col=int(re.search(r'colors:\[(\d+)\]', s_).group(1)),
                                  kill=None, frames={}, where=ln[:ln.index('summon')], bb=re.search(r'billboard:"(\w+)"', s_).group(1)))
                continue
            m = re.search(r'kill @e\[type=minecraft:item_display,tag=([\w]+)(?:,tag=([\w]+))?', ln)
            if m:
                tg = [x for x in m.groups() if x]
                for c in cards:
                    if all(x in c['tags'] for x in tg) and c['kill'] is None and c['t'] <= t:
                        c['kill'] = t
                if B.TAG_HEAD in tg:
                    hkill[tg[-1]] = t
                continue
            m = re.search(r'tp @e\[type=minecraft:item_display,tag=rlk_hr_swh,tag=(\w+),limit=1\] \^(\S*) \^(\S*) \^(\S*)', ln)
            if m:
                heads.setdefault(m.group(1), []).append((t, tuple(float(v or 0) for v in m.groups()[1:]), ln))
                continue
            m = re.search(r'as @e\[type=minecraft:item_display,tag=(\w+)\] run data modify entity @s item\.components\."minecraft:item_model" set value "rlk:mboss/hr_kit/(\w+)"', ln)
            if m:
                for c in cards:
                    if m.group(1) in c['tags']:
                        c['frames'][t] = m.group(2)
                continue
            other.append((t, ln))
    return cards, heads, hkill, other, ticks


# ----------------------------------------------------------------------------- the hits
def hits_of(key):
    """[(idx, clip, event, pattern tick, clip t0, parry, first?)] of a P1 / P2 pattern (api.HITS; one per clip event)."""
    out, seen, prev = [], set(), None
    for i, row in enumerate(api.HITS[key]):
        clip, ev = row[0], row[1]
        if (clip, ev) in seen:
            continue
        seen.add((clip, ev))
        t0 = api.Q_AIR_T0 if clip == 'q_air' else 0
        h = t0 + api.ev(clip, ev)
        first = prev is None or h - prev > 24 or key == 'ult'
        out.append((i, clip, ev, h, t0, row[6], first))
        prev = h
    return out


LINE_HITS = {('a4', 'hit'), ('a9', 'cut'), ('a10', 'hit'), ('tri', 'h0'), ('hcut', 'cut'), ('blue', 'hit'), ('kcut', 'cut'), ('mx', 'x'),
             ('q_grab', 'grab'), ('q_air', 'beam'), ('q_air', 'hit'), ('q_air', 'pillar')}     # her body carries the blade: a target line
NO_SLASH = {('q_grab', 'grab')}          # the grab is her hand, not the blade


def near_path(sw, p, u0, u1, n=240):
    """(distance, u) of the point of the tip's shown way u0 .. u1 nearest p"""
    best = (9.0, u0)
    for i in range(n + 1):
        u = u0 + (u1 - u0) * i / n
        d = math.dist(sw.blade(u)[1], p)
        if d < best[0]:
            best = (d, u)
    return best


def check_swing(lab, sw, t0, cards, heads, hkill, first, show_rule, path=True, slash=True, uid=None):
    uid = uid or f'{sw.clip}{sw.h}'
    mine = f'rlk_hr_sw_{uid}'
    h = t0 + sw.h
    if path:
        segs = [c for c in cards if mine in c['tags'] and c['kind'] == 'sw_path' and B.TAG_RIDE in c['tags']]
        check(bool(segs), f'{lab}: a drawn path')
        if segs:
            show = min(c['t'] for c in segs)
            check(h - show >= show_rule, f'{lab}: the path shows {h - show} t before the hit (rule {show_rule})')
            worst, ends = 0.0, []
            for c in segs:
                p0 = tuple(c['tr'])
                p1 = B.add(p0, B.mul(qrot(c['q'], (0, 0, 1)), c['s'][2]))
                worst = max(worst, near_path(sw, p0, sw.a, sw.h)[0], near_path(sw, p1, sw.a, sw.h)[0])
                ends.append(p1)
                check(min(c['s'][0], c['s'][1]) * B.PATH_CORE >= MIN_THICK - 1e-6, f'{lab}: a path piece {min(c["s"][:2]) * B.PATH_CORE:.3f} b thick (>= {MIN_THICK})')
            check(worst <= PATH_TOL, f'{lab}: the path lies on the tip\'s way of the track (worst {worst:.3f} b, tol {PATH_TOL})')
            tip_h = sw.blade(sw.h)[1]
            check(min(math.dist(e, tip_h) for e in ends) <= PATH_TOL, f'{lab}: the path ends at the tip\'s place of the hit tick')
            hm = sorted(heads.get(mine, []))
            check(bool(hm) and hm[-1][0] == h - 1 and math.dist(hm[-1][1], tip_h) <= 0.02 and hkill.get(mine) == h,
                  f'{lab}: the head is sent to the hit point at h - 1 (1 t of interpolation: it arrives on the hit tick) and goes at h',
                  str(hm[-1:]))
            check(all(c['kill'] is not None and c['kill'] <= h + B.ARC_LIFE for c in segs), f'{lab}: the path is gone <= {B.ARC_LIFE} t after the hit')
    if slash:
        arcs = [c for c in cards if any(x.startswith(mine + '_') for x in c['tags'])]
        check(bool(arcs), f'{lab}: a slash')
        last_u = -1.0
        for c in sorted(arcs, key=lambda c: c['t']):
            ct = c['t'] - t0
            if c['kind'] == 'sw_path':                      # the blade slid along itself: a band of the tip's way
                p0 = tuple(c['tr'])
                p1 = B.add(p0, B.mul(qrot(c['q'], (0, 0, 1)), c['s'][2]))
                d = max(near_path(sw, p0, ct - 1, ct)[0], near_path(sw, p1, ct - 1, ct)[0])
                check(d <= RIM_TOL, f'{lab}: slash band at {c["t"]} on the tip\'s way ({d:.3f} b)')
                check(min(c['s'][:2]) * B.PATH_CORE >= MIN_THICK - 1e-6, f'{lab}: slash band >= {MIN_THICK} b thick')
                continue
            x, y, z = (qrot(c['q'], a) for a in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
            sx, _sy, sz = c['s']
            beta = math.atan(B.ARC_TAN * sx / sz)
            sa, ca = B.ARC_TAN / math.sqrt(1 + B.ARC_TAN ** 2), 1 / math.sqrt(1 + B.ARC_TAN ** 2)
            R = sz * math.sqrt((sx / sz) ** 2 * sa * sa + ca * ca)
            q = tuple(c['tr'])
            rims = [B.add(q, B.mul(B.add(B.mul(z, math.cos(beta)), B.mul(x, sgn * math.sin(beta))), R)) for sgn in (-1, 1)]
            near = [near_path(sw, r, ct - 1, ct) for r in rims]
            d = max(n[0] for n in near)
            check(d <= RIM_TOL, f'{lab}: slash piece born {c["t"]}: its rim on the tip\'s way of the tick it is born on ({d:.3f} b, tol {RIM_TOL})')
            us = sorted(n[1] for n in near)
            off = 0.0
            for u in us:
                b_, t_ = sw.blade(u)
                dirv = B.unit(B.sub(t_, b_))
                off = max(off, abs(90 - B.angle(dirv, y)))
                # the blade's line passes the piece's apex
                w = B.sub(q, b_)
                apex = B.norm(B.sub(w, B.mul(dirv, B.dot(w, dirv))))
                check(apex <= APEX_TOL, f'{lab}: slash piece born {c["t"]}: the blade\'s line passes its apex ({apex:.3f} b)')
            check(off <= PLANE_TOL, f'{lab}: slash piece born {c["t"]}: its plane holds the blade ({off:.2f} deg off, tol {PLANE_TOL})')
            check(us[0] >= last_u - 0.26, f'{lab}: slash piece born {c["t"]}: follows the blade\'s travel (u {us[0]:.2f} after {last_u:.2f})')
            last_u = max(last_u, us[0])
            check(sw.a <= ct <= sw.b, f'{lab}: slash piece born {c["t"]} inside the swing {t0 + sw.a}-{t0 + sw.b}')
            check(c['kill'] == c['t'] + B.ARC_LIFE, f'{lab}: slash piece born {c["t"]} gone {B.ARC_LIFE} t later ({c["kill"]})')
            check(sorted(c['frames']) == [c['t'] + dt for dt, _f in B.ARC_FRAMES[1:]], f'{lab}: slash piece born {c["t"]} fades through its frames')
            thick = min(2 * R * math.sin(beta), R * (1 - B.ARC_INNER))
            check(thick >= MIN_THICK, f'{lab}: slash piece born {c["t"]} {thick:.2f} b across (>= {MIN_THICK})')
        if arcs:
            check(max(c['kill'] or 999 for c in arcs) <= h + B.SWING_ON + B.ARC_LIFE, f'{lab}: the slash is gone {B.SWING_ON} + {B.ARC_LIFE} t after the hit at the latest')


def check_line(lab, key, h, first, cards, other, lock_by=None):
    lines = [c for c in cards if B.TAG_LINE in c['tags'] and c['t'] <= h and (c['kill'] or 999) >= h]
    check(bool(lines), f'{lab}: a target line')
    if not lines:
        return
    c = max(lines, key=lambda c: c['t'])
    rule = B.LEAD_FIRST if first else B.LEAD_CHAIN
    check(h - c['t'] >= rule, f'{lab}: the target line shows {h - c["t"]} t before the hit (rule {rule})')
    check(min(c['s'][:2]) * B.PATH_CORE >= MIN_THICK - 1e-6, f'{lab}: the target line >= {MIN_THICK} b thick')
    hd = [(t, float(re.search(r'core\.sw\.d double ([\d.]+)', ln).group(1))) for t, ln in other if 'core.sw.d double' in ln and c['t'] <= t < h]
    check(bool(hd) and max(hd)[0] == h - 1 and abs(max(hd)[1] - B.LINE_STEP) < 1e-6 and all(b[1] >= a[1] for a, b in zip(sorted(hd), sorted(hd)[1:])),
          f'{lab}: the line\'s head runs on every tick and is sent to the target at h - 1 (it arrives on the hit tick)', str(sorted(hd)[-2:]))
    aims = sorted(t for t, ln in other if 'core/sw/aim' in ln and c['t'] <= t <= h)
    lock_by = h - api.LOCK_LEAD + 1 if lock_by is None else lock_by
    check(bool(aims) and aims[0] == c['t'] and aims[-1] <= lock_by, f'{lab}: the line is aimed from its first tick to the lock ({aims[:1]}..{aims[-1:]})')
    return c


# ----------------------------------------------------------------------------- P1 / P2
def lead_rule(first):
    return B.LEAD_FIRST if first else B.LEAD_CHAIN


for key in api.P1 + tuple(k for k in api.P2 if k not in api.GAUNTLETS):
    if not api.HITS.get(key):
        continue
    cards, heads, hkill, other, ticks = cards_of(key)
    for c in cards:
        if c['kind'] == 'sw_head':
            check(min(c['s']) >= MIN_THICK, f'{key}: a head card {min(c["s"]):.2f} b (>= {MIN_THICK})')
    prev = None
    for idx, clip, ev, h, t0, par, first in hits_of(key):
        lab = f'{key} {clip}.{ev}@{h}'
        sw = B.swing_of(clip, ev)
        if key != 'a3s' and (clip, ev) != ('q_grab', 'grab'):
            lead = sw.h - sw.w
            check(lead >= lead_rule(first), f'{lab}: the wind-up is reached {lead} t before the hit and held (rule {lead_rule(first)}; swing {sw.a}-{sw.b})')
        line = None
        if (clip, ev) in LINE_HITS:
            line = check_line(lab, key, h, first, cards, other)
            check_swing(lab, sw, t0, cards, heads, hkill, first, lead_rule(first), path=False, slash=(clip, ev) not in NO_SLASH)
        else:
            check_swing(lab, sw, t0, cards, heads, hkill, first, lead_rule(first))
        col = [c['col'] for c in cards if c['t'] <= h and (c is line or f'rlk_hr_sw_{clip}{sw.h}' in c['tags']) and c['kind'] == 'sw_path']
        want = B.colour_of(key, idx)[0]
        check(bool(col) and all(x == want for x in col), f'{lab}: the path\'s colour = {"white-gold (parryable)" if par == "P" else "its flash\'s colour (unparriable)"}', str(set(col)))
    # the statics: kcut's three lines, nb's bands
    if key in ('kcut', 'nb'):
        st = [c for c in cards if c['kind'] == 'sw_path' and c['where'].startswith('execute at ') and 'rlk_hr_lock' in c['where'] and B.TAG_LINE not in c['tags'] and 'rotated ~' in c['where']]
        yaws = sorted(int(re.search(r'rotated ~(-?\d+) 0', c['where']).group(1)) for c in st)
        want = sorted(api.KCUT_YAW if key == 'kcut' else api.NB_YAW)
        ln = api.HITS[key][1][3][0] if key == 'kcut' else api.HITS[key][0][3][0]
        check(yaws == want and all(abs(c['s'][2] - ln) < 1e-6 and f'^-{B.f4(ln / 2)[:-1]}'.rstrip('0').rstrip('.') in c['where'].replace('.0 ', ' ') or f'^-{int(ln / 2)}' in c['where'] for c in st),
              f'{key}: its {len(want)} lines stand in the air through the locked spot at {want} deg, {ln} b long', str((yaws, [c["where"][-60:] for c in st])))
        check(all(min(c['s'][:2]) * B.PATH_CORE >= MIN_THICK - 1e-6 for c in st), f'{key}: the lines >= {MIN_THICK} b thick')

# ----------------------------------------------------------------------------- the gauntlets
for key in api.GAUNTLETS:
    cards, heads, hkill, other, ticks = cards_of(key)
    rows = [r for r in api.SCRIPTS[key] if r[0] >= 0 and r[2]]
    cut_rows = [r for r in rows if r[1].startswith('A8.') and r[1] not in ('A8.T', 'A8.9')]

    def shown(tau):
        """(clip, clip tick) the rig shows at pattern tick tau (the clip started last; held past its end)"""
        r = [x for x in rows if x[0] <= tau]
        if not r:
            return None
        c = r[-1][2]
        return c, min(api.CLIPS[c][0], tau - r[-1][0])
    prev_s = None
    for t, step, clip, _c in cut_rows:
        s = t + api.ev(clip, 'hit')
        lab = f'{key} {step} {clip}@{s}'
        sw = B.swing_of(clip, 'hit')
        # the wind-up: the blade pose at the swing's start, counted back through whatever clip is shown (a clip's first
        # BLEND ticks are the rig's blend from the pose before: they count when both ends are the pose)
        # (a move whose swing starts inside its first 3 ticks is blended in from the pose shown before it: that pose is its
        # wind-up; it must be a pose held away from where the cut lands)
        tau = t + sw.a if sw.a >= 3 else t - 1
        cc = shown(tau)
        ref_b, ref_t = T[cc[0]]['b'][cc[1]], T[cc[0]]['t'][cc[1]]
        check(math.dist(ref_t, sw.T[sw.h]) >= 0.8, f'{lab}: the wind-up holds the blade away from where the cut lands ({math.dist(ref_t, sw.T[sw.h]):.2f} b)')
        while tau - 1 >= 0:
            cc = shown(tau - 1)
            if not cc or not T[cc[0]]['on'][cc[1]]:
                break
            if math.dist(T[cc[0]]['t'][cc[1]], ref_t) > B.WIND_TOL or math.dist(T[cc[0]]['b'][cc[1]], ref_b) > B.WIND_TOL:
                break
            tau -= 1
        lead = s - tau
        check(lead >= B.LEAD_CHAIN, f'{lab}: the wind-up pose is shown {lead} t before the cut and held (rule {B.LEAD_CHAIN}: a gauntlet cut is a chain hit)')
        first = prev_s is None or any(r[1] in ('D1', 'D2', 'D3', 'D4') and (prev_s or 0) < r[0] < s for r in rows)
        check_swing(lab, sw, t, cards, heads, hkill, first, B.LEAD_FIRST if first else B.LEAD_CHAIN, uid=f'c{s}')
        segs = [c for c in cards if f'rlk_hr_sw_c{s}' in c['tags'] and c['kind'] == 'sw_path']
        st = [tt for tt in ticks if any('rlk_hr_gst' in ln and 'tag ' in ln and ' add ' in ln for ln in ticks[tt]) and tt <= s]
        check(bool(st) and bool(segs) and max(st) <= min(c['t'] for c in segs), f'{lab}: its station is fixed before its path is drawn there')
        prev_s = s
    dive = [r for r in rows if r[1] == 'A8.9'][0]
    hj = dive[0] + api.ev('g_dive', 'hit')
    check(hj == api.JUDGE_T[key], f'{key}: the dive ends on the judge tick')
    # (the dive's line follows the player until the dive starts: the judge is no aimed hazard)
    check_line(f'{key} dive@{hj}', key, hj, True, cards, other, lock_by=dive[0] + api.ev('g_dive', 'dive'))
    check(hj - dive[0] >= 12, f'{key}: the dive reappears {hj - dive[0]} t before the judge (>= 12: nothing hits from an empty screen)')

# ----------------------------------------------------------------------------- the clock
bad = []
for p in MOD.rglob('*.mcfunction'):
    rel = p.relative_to(MOD).as_posix()
    if rel.startswith(('fx/', 'rig/')):
        continue
    txt = p.read_text()
    if 'rlk_hr_sw' in txt and not re.match(r'p/\w+/(k/\d+|start|tick|cancel|fail)$|core/sw/|ult/fail60$|g/', rel[:-11]):
        bad.append(rel)
    if 'rlk_hr_sw' in txt and 'schedule ' in txt:
        bad.append(rel + ' (schedule)')
check(not bad, 'clock: every sweep command sits in a pattern-tick file (a pure function of #pt hr; no schedule)', str(bad[:5]))
rt = (MOD / 'core/sw/march.mcfunction').read_text()
check('gametime' not in rt and 'schedule' not in rt, 'clock: the target line\'s run-time part reads no game time')

print(f'test_blade: {N[0] - len(FAILS)}/{N[0]} passed' + (f', {len(FAILS)} FAILED' if FAILS else ''))
sys.exit(1 if FAILS else 0)

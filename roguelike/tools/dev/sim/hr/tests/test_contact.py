#!/usr/bin/env python3
"""test_contact.py [ROGUELIKE] [--actor MANIFEST] [-v] — the cutscene contacts of hr_design.md §4.3, both sides.

Her side comes from tools/dev/sim/hr/cine/her_tracks.json (the rig builder writes it: per cinematic clip tick her sword's grip
and tip, her hands, the left elbow, the soles, the pelvis, the head, the crown top and the brim in the stage frame, on the root
track her clips are choreographed to: tools/scarlet_cine.mjs ROOTS). The actor's side comes from lane H3's
tools/player_motion/cine/manifest.json (per tick shift / hilt / tip / hand_r / hand_l / pommel / foot_r / foot_l / head / shoulder_r);
without it (the lane not merged yet) only her side is judged and the mutual rows are skipped.

  table    the rows this test judges == the §4.3 table of tools/dev/plan/combat/hr_design.md (ids, clips, ticks, points)
  her      at every tick of a row her part is on the stage point: blade rows = the grip-to-tip line within 0.08 b; KW her left
           grip, KH her crown top, KS her left forearm (elbow -> grip), KT her pelvis pivot, KK her pelvis / torso / thigh boxes
           (from the builder's own row in her_tracks.contacts), KG the rim of her hat brim; the others within 0.12 b
  actor    (with --actor) the same rows for the actor's parts as its manifest's `contact` block names them
  meet     (with --actor) the two sides meet each other, not only the point: blade rows = the two blade lines pass within
           0.12 b of each other at the row's ticks and neither blade enters the other's head box (0.25 b half, reported:
           fails below -0.05 b); KW / KH / KK the two parts within 0.20 b
"""
import json, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
args = [a for a in sys.argv[1:] if not a.startswith('-')]
V = '-v' in sys.argv
ACT = None
if '--actor' in sys.argv:
    ACT = Path(sys.argv[sys.argv.index('--actor') + 1]); args = [a for a in args if a != str(ACT)]
DP = Path(args[0]) if args else HERE.parents[4]
TR = json.loads((DP / 'tools/dev/sim/hr/cine/her_tracks.json').read_text())
if ACT is None and (DP / 'tools/player_motion/cine/manifest.json').exists():
    ACT = DP / 'tools/player_motion/cine/manifest.json'
AM = json.loads(ACT.read_text()) if ACT else None
fails, n = [], 0


def ok(c, msg):
    global n
    n += 1
    if not c: fails.append(msg)
    if V or not c: print(('ok   ' if c else 'FAIL ') + msg)


def seg(P, A, B):
    ab = [b - a for a, b in zip(A, B)]; L = sum(x * x for x in ab) or 1e-9
    u = max(0, min(1, sum((p - a) * x for p, a, x in zip(P, A, ab)) / L))
    return math.dist(P, [a + x * u for a, x in zip(A, ab)])


def segseg(p1, q1, p2, q2, m=60):
    best = 9
    for i in range(m + 1):
        P = [a + (b - a) * i / m for a, b in zip(p1, q1)]
        best = min(best, seg(P, p2, q2))
    return best


def segbox(A, B, c, h=.25, m=40):
    best = 9
    for i in range(m + 1):
        q = [abs(a + (b - a) * i / m - cc) - h for a, b, cc in zip(A, B, c)]
        best = min(best, math.hypot(*[max(x, 0) for x in q]) + min(max(q), 0))
    return best


# ---- the table of the design ---------------------------------------------------------------------------------------------------
design = (DP / 'tools/dev/plan/combat/hr_design.md').read_text(encoding='utf-8')
sec = design[design.index('### 4.3 Contacts'):design.index('`test_contact.py` (HI')]
ROWS = []
for m in re.finditer(r'^\| (K\w+) \| `(\w+)` ([\d\- /]+) \| (.+?) \|', sec, re.M):
    kid, clip, ticks, pts = m.group(1), m.group(2), m.group(3).strip(), m.group(4)
    P = [tuple(float(x) for x in re.split(r',\s*', g)) for g in re.findall(r'ST\(([^)]*)\)', pts)]
    spans = [tuple(int(x) for x in t.strip().split('-')) for t in ticks.split('/')]
    for i, sp in enumerate(spans):
        ROWS.append((kid if len(spans) == 1 else f'{kid}.{("over", "land")[i]}', clip, sp[0], sp[-1], P[i if len(P) > 1 else 0]))
KIND = {'K1': 'blade', 'KR': 'blade', 'KW': 'hand_l', 'KH': 'hat_crown', 'KS': 'forearm_l', 'KT.over': 'pelvis', 'KT.land': 'pelvis', 'KK': 'body', 'KG': 'brim',
        'KE2': 'blade', 'KE5': 'blade', 'KA1': 'blade', 'KA2': 'blade', 'KA3': 'blade', 'KA4': 'blade'}
ok(len(ROWS) == 15 and {r[0] for r in ROWS} == set(KIND), f'table: the 15 rows of hr_design §4.3 ({len(ROWS)} parsed)')
built = {c['id']: c for c in TR.get('contacts', [])}
ok(set(built) == set(KIND), f'table: her_tracks.json judges the same rows ({sorted(set(KIND) ^ set(built))})')
for kid, clip, t0, t1, P in ROWS:
    b = built.get(kid)
    ok(b and b['clip'] == clip and b['ticks'] == [t0, t1] and all(abs(x - y) < 1e-9 for x, y in zip(b['point'], P)), f'table: {kid} = {clip} {t0}-{t1} ST{P} (builder {b and (b["clip"], b["ticks"], b["point"])})')

# ---- her side ------------------------------------------------------------------------------------------------------------------
BR = TR['brim_r']
for kid, clip, t0, t1, P in ROWS:
    c, kind, tol = TR['clips'][clip], KIND[kid], (.08 if KIND[kid] == 'blade' else .12)
    worst, at = 0, t0
    for t in range(t0, t1 + 1):
        if kind == 'blade': d = seg(P, c['hilt'][t], c['tip'][t]) if c['hilt'][t] else 9
        elif kind == 'forearm_l': d = seg(P, c['elbow_l'][t], c['hand_l'][t])
        elif kind == 'brim':
            ctr, nn = c['brim'][t]; v = [p - q for p, q in zip(P, ctr)]; h = sum(a * b for a, b in zip(v, nn))
            d = math.hypot(h, math.dist(v, [h * x for x in nn]) - BR)
        elif kind == 'body': d = built[kid]['worst']          # (the boxes are the builder's: its own measure)
        else: d = math.dist(P, c[kind][t])
        if d > worst: worst, at = d, t
    ok(worst <= tol, f'her: {kid} ({clip} {t0}-{t1}, {kind}) worst {worst:.3f} b at t{at} (tol {tol})')
    ok(abs(worst - built[kid]['worst']) < .004, f'her: {kid} the builder gate measured the same ({built[kid]["worst"]})')

# ---- the actor's side and the meeting ---------------------------------------------------------------------------------------------
if AM is None:
    print('skipped: the actor rows and the meeting (no tools/player_motion/cine/manifest.json; --actor <manifest>)')
else:
    AC = AM['contact']
    ACLIP = {'cs1': 'cs1', 'repel': 'repel', 'ending': 'ending'}
    for kid, clip, t0, t1, P in ROWS:
        a = AM['clips'][ACLIP[clip]]['tick']; h = TR['clips'][clip]; kind = KIND[kid]
        base = kid.split('.')[0]
        if base in AC and AC[base]['what'] in ('blade', 'hand_l', 'hilt', 'tip', 'foot_r'):
            what, tol, worst, at = AC[base]['what'], AC[base]['tol'], 0, t0
            for t in range(t0, t1 + 1):
                d = seg(P, a['hilt'][t], a['tip'][t]) if what == 'blade' else min(math.dist(P, a[w][t]) for w in ((what, 'pommel') if what == 'hilt' else (what,)))
                if d > worst: worst, at = d, t
            ok(worst <= tol, f'actor: {kid} ({what}) worst {worst:.3f} b at t{at} (tol {tol})')
        # the meeting
        if kind == 'blade':
            w1 = w2 = 0; hb = ab = 9
            for t in range(t0, t1 + 1):
                w1 = max(w1, segseg(h['hilt'][t], h['tip'][t], a['hilt'][t], a['tip'][t]))
                hb = min(hb, segbox(h['hilt'][t], h['tip'][t], a['head'][t])); ab = min(ab, segbox(a['hilt'][t], a['tip'][t], h['head'][t]))
            ok(w1 <= .12, f'meet: {kid} the two blades pass within {w1:.3f} b of each other (<= 0.12)')
            ok(hb >= -.05, f'meet: {kid} her blade stays out of the actor\'s head box ({hb:+.3f} b)')
            ok(ab >= -.05, f'meet: {kid} the actor\'s blade stays out of her head box ({ab:+.3f} b)')
        elif kid == 'KW':
            w = max(math.dist(h['hand_l'][t], a['hand_l'][t]) for t in range(t0, t1 + 1)); ok(w <= .2, f'meet: KW her left grip and the actor\'s left hand within {w:.3f} b')
        elif kid == 'KH':
            w = min(math.dist(h['hat_crown'][t0], a[x][t0]) for x in ('pommel', 'hilt')); ok(w <= .2, f'meet: KH the actor\'s pommel / hilt {w:.3f} b from her crown top')
        elif kid == 'KK':
            w = math.dist(h['pelvis'][t0], a['foot_r'][t0]); ok(w <= .5, f'meet: KK the actor\'s right foot {w:.3f} b from her pelvis pivot (her hip under it)')
print(f'test_contact: {n - len(fails)} / {n} ok' + ('' if not fails else f', {len(fails)} FAILED'))
sys.exit(1 if fails else 0)

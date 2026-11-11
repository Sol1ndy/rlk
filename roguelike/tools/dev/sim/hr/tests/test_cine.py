#!/usr/bin/env python3
"""test_cine.py [ROGUELIKE] [-v] — lane H2c's suite of 홍련's 8 cinematic clips (hr_design.md §4.1; run from a copy of tools/dev/sim
outside the datapack). It reads what the rig builder shipped: tools/scarlet_rig_manifest.json, the anchor table of
boss/scarlet/rig/an/load.mcfunction, the clips' key files and tools/dev/sim/hr/cine/her_tracks.json.

  contract   the 8 cinematic clips of the manifest == the §4.1 table of tools/dev/plan/combat/hr_design.md: names, lengths, every
             event and its tick ('end' = the length); sq1 / lead_down / lead_stand are gone; a runner, play/ and start/ exist per clip
  handover   the §4.1 hand-over poses on the shipped anchor table (the 8 anchors of the last tick of A against tick 0 of B, b):
             intro 1290 = intro_end 0, intro_end 150 = idle 0, cs1 720 = lead60 0, lead60 / lead5 / lead_re end = g_brim's hold,
             repel 140 = idle2 0, ending 1372 = ev_give 0 (H_POSE) within 0.03 b; repel 129 = ending 0 (the right hand 0.06 b); repel 0 against g_dive's
             last pose: the head and the chest within 0.25 b (the dive's body; the sword is re-gripped on the dive's line: reported)
  states     the hat / sword / scabbard / props states the clips key at the contract's ticks (the key files' stored looks): cs1
             sheathed at 200 and drawn at 642, the bottle 216-500, the hat off 240-258; repel hat off at 84 and on at 139; intro
             bottle 326-424, cup to 712; ending hat on at 20, sheathed at 452, the scabbard in hand from 388
  tracks     her_tracks.json: the 5 staged clips carry every column for len + 1 ticks, the lead-ins are not staged; her root at
             the table's marks = lane H2's sequence moves (cs1 lock f 1.5, repel 88 over the actor, ending 52 half way, the aerial cuts, ...); no root motion in a
             clip on the ground: the pelvis stays within 0.75 b of the root's axis; the feet never under the floor of the stage
  contacts   every §4.3 row of her_tracks.contacts within its tolerance (the builder's gate; test_contact.py judges both sides)
"""
import json, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
args = [a for a in sys.argv[1:] if not a.startswith('-')]
V = '-v' in sys.argv
DP = Path(args[0]) if args else HERE.parents[4]
MAN = json.loads((DP / 'tools/scarlet_rig_manifest.json').read_text())
TR = json.loads((DP / 'tools/dev/sim/hr/cine/her_tracks.json').read_text())
RIG = DP / 'data/rlk/function/boss/scarlet/rig'
fails, n = [], 0


def ok(c, msg):
    global n
    n += 1
    if not c: fails.append(msg)
    if V or not c: print(('ok   ' if c else 'FAIL ') + msg)


# ---- contract: the §4.1 table -----------------------------------------------------------------------------------------------------
design = (DP / 'tools/dev/plan/combat/hr_design.md').read_text(encoding='utf-8')
sec = design[design.index('### 4.1 Her cinematic clips'):design.index('### 4.2 Actor clips')]
TABLE = {}
for m in re.finditer(r'^\| `(\w+)` \| (\d+) \([^)]*\) \| (.+?) \|$', sec, re.M):
    ev = {}
    for name, tick in re.findall(r'(\w+) (\d+)', m.group(3).split('(')[0]): ev[name] = int(tick)
    TABLE[m.group(1)] = (int(m.group(2)), ev)
ok(sorted(TABLE) == sorted(['intro', 'intro_end', 'cs1', 'lead60', 'lead5', 'lead_re', 'repel', 'ending']), f'contract: the design lists 8 cinematic clips ({sorted(TABLE)})')
for name, (ln, ev) in TABLE.items():
    c = MAN['clips'].get(name)
    ok(c is not None and c['len'] == ln, f'contract: {name} is {ln} t (manifest {c and c["len"]})')
    if not c: continue
    ok(ev.get('end', ln) == ln, f'contract: {name} end = its length')
    want = {k: v for k, v in ev.items() if k != 'end'}
    ok(c['events'] == want, f'contract: {name} events == the table ({sorted(set(want.items()) ^ set(c["events"].items()))[:6]})')
    ok(c['authored'] and c['loop'] is None, f'contract: {name} authored, one-shot')
    for f in (f'c/{name}/run', f'play/{name}', f'start/{name}', f'c/{name}/k/0'):
        ok((RIG / f'{f}.mcfunction').exists(), f'contract: rig/{f} exists')
for gone in ('sq1', 'lead_down', 'lead_stand'):
    f = RIG / f'play/{gone}.mcfunction'           # (until api.py lists the new lead-ins the builder leaves a marked alias)
    ok(gone not in MAN['clips'] and (not f.exists() or 'STAND-IN (H2c)' in f.read_text()), f'contract: {gone} is gone')
ok(MAN.get('cine_source') == 'tools/scarlet_cine.mjs', 'contract: the clips come from tools/scarlet_cine.mjs')

# ---- handover: the shipped anchor table -------------------------------------------------------------------------------------------
AN = {}
for line in (RIG / 'an/load.mcfunction').read_text().splitlines():
    m = re.match(r'data modify storage rlk:hr rig.an\[(\d+)\]\.(\w+) set value (\[.*\])', line)
    if m: AN.setdefault(int(m.group(1)), {})[m.group(2)] = [tuple(float(x.lstrip('^') or 0) for x in s.split()) for s in json.loads(m.group(3))]
ID = {k: v['id'] for k, v in MAN['clips'].items()}


def anchors(clip, t):
    return {a: v[t] for a, v in AN[ID[clip]].items()}


def gap(a, ta, b, tb, names=None):
    A, B = anchors(a, ta), anchors(b, tb)
    return max(math.dist(A[k], B[k]) for k in (names or A))


for a, ta, b, tb in [('intro', 1290, 'intro_end', 0), ('intro_end', 150, 'idle', 0), ('cs1', 720, 'lead60', 0), ('lead60', 56, 'g_brim', 14), ('lead5', 116, 'g_brim', 14),
                     ('lead_re', 60, 'g_brim', 14), ('ending', 1372, 'ev_give', 0)]:
    d = gap(a, ta, b, tb)
    ok(d <= .03, f'handover: {a} {ta} = {b} {tb} (the 8 anchors within {d:.3f} b)')
# repel 129 = ending 0 (the lethal kick; lane H2 cuts it under the seam's white, where her place also jumps 3.0 -> 4.2): the
# body within 0.03 b; the right hand is already reaching for the hat in the repel (the pick-up's 4-tick pre-roll from 127), the
# ending starts with it resting on the brim: within 0.06 b (reported)
d = gap('repel', 129, 'ending', 0, [a for a in MAN['anchors'] if a != 'hand_r'])
ok(d <= .03, f'handover: repel 129 = ending 0 (the anchors but the right hand within {d:.3f} b)')
d = gap('repel', 129, 'ending', 0, ['hand_r'])
ok(d <= .06, f'handover: repel 129 = ending 0 the right hand {d:.3f} b (the hat pick-up\'s pre-roll; under the seam\'s white)')
# repel 140 = idle2: hat_on is at 139, so the right hand that set the hat on is still coming down at 140 (the arm turns <= 85
# degrees a tick): every other anchor is on idle2, the hand within its 3-tick blend (reported)
d = gap('repel', 140, 'idle2', 0, [a for a in MAN['anchors'] if a != 'hand_r'])
ok(d <= .03, f'handover: repel 140 = idle2 0 (the anchors but the right hand within {d:.3f} b)')
dr = gap('repel', 140, 'idle2', 0, ('hand_r',))
ok(dr <= .7, f'handover: repel 140 the right hand {dr:.2f} b from idle2\'s (leaving the brim: hat_on is 139)')
GD = 22        # g_dive's last tick (round V, lane VB: the contract's length 10 -> 22, the same last pose)
d = gap('repel', 0, 'g_dive', GD, ('head', 'chest', 'hat_crown'))
ok(d <= .25, f'handover: repel 0 = g_dive\'s last pose (head / chest / crown within {d:.3f} b)')
print(f'  (repel 0 against g_dive {GD}: the sword grip {gap("repel", 0, "g_dive", GD, ("hand_l",)):.2f} b, the tip {gap("repel", 0, "g_dive", GD, ("blade_tip",)):.2f} b apart: the dive\'s two-hand grip is re-gripped '
      'in the left hand on the dive\'s line through KR; the rig blends the first 3 ticks from the shown pose)')

# ---- states: the stored looks the key files set -------------------------------------------------------------------------------------
LOOKS = MAN['looks']; PROPS = MAN['prop_states']
STORE = {'Hat': LOOKS['hat'], 'Sw': LOOKS['sword'], 'Sc': LOOKS['scabbard'], 'Cu': PROPS, 'Bo': PROPS}


def states(clip):
    ln = MAN['clips'][clip]['len']; cur = {}; out = []
    for t in range(ln + 1):
        f = RIG / f'c/{clip}/k/{t}.mcfunction'
        if f.exists():
            for m in re.finditer(r'scoreboard players set @s hrRig(Hat|Sw|Sc|Cu|Bo) (\d+)', f.read_text()):
                cur[m.group(1)] = STORE[m.group(1)][int(m.group(2))]
        out.append(dict(cur))
    return out


def span(st, key, val):
    ts = [t for t, s in enumerate(st) if s.get(key) == val]
    return (ts[0], ts[-1]) if ts else None


S = {c: states(c) for c in TABLE}
ok(span(S['cs1'], 'Sw', 'sheathed') == (200, 641) and S['cs1'][642]['Sw'] == 'hand', f'states: cs1 sheathed 200-641, drawn at 642 ({span(S["cs1"], "Sw", "sheathed")})')
ok(span(S['cs1'], 'Bo', 'hand') == (216, 499), f'states: cs1 the bottle in hand 216-499 ({span(S["cs1"], "Bo", "hand")})')
ok(span(S['cs1'], 'Hat', 'hand') == (240, 257) and S['cs1'][258]['Hat'] == 'worn', f'states: cs1 the hat off 240, on 258 ({span(S["cs1"], "Hat", "hand")})')
ok(all(s['Sc'] == 'hip' for c in ('intro', 'intro_end', 'cs1', 'repel', 'lead60', 'lead5', 'lead_re') for s in S[c]), 'states: the scabbard stays at the hip outside the ending')
ok(span(S['repel'], 'Hat', 'world') == (84, 130) and span(S['repel'], 'Hat', 'hand') == (131, 138) and S['repel'][139]['Hat'] == 'worn', f'states: repel hat off 84, taken up 131, on 139 ({span(S["repel"], "Hat", "world")})')
ok(span(S['intro'], 'Bo', 'hand') == (326, 423) and span(S['intro'], 'Cu', 'hand') == (0, 711), f'states: intro the bottle 326-423, the cup to 711 ({span(S["intro"], "Bo", "hand")}, {span(S["intro"], "Cu", "hand")})')
ok(all(s['Sw'] == 'sheathed' for i, s in enumerate(S['intro']) if not 764 <= i <= 786) and S['intro_end'][66]['Sw'] == 'hand' and S['intro_end'][65]['Sw'] == 'sheathed',
   'states: the sword sheathed through the intro (a hand\'s width out 764-786), drawn at intro_end 66')
ok(S['ending'][0]['Hat'] == 'world' and S['ending'][20]['Hat'] == 'worn' and S['ending'][19]['Hat'] == 'hand', 'states: ending hat on at 20')
ok(S['ending'][452]['Sw'] == 'sheathed' and S['ending'][451]['Sw'] == 'hand' and span(S['ending'], 'Sc', 'hand') == (388, 1372), f'states: ending sheathed at 452, the scabbard in hand from 388 ({span(S["ending"], "Sc", "hand")})')
ok(all(S[c][-1]['Hat'] == 'worn' for c in TABLE), 'states: every clip ends with the hat worn')

# ---- tracks ---------------------------------------------------------------------------------------------------------------------------
STAGED = {'intro': 0, 'intro_end': 1290, 'cs1': 0, 'repel': 0, 'ending': 0}
COLS = ('root', 'hilt', 'tip', 'hand_l', 'hand_r', 'elbow_l', 'foot_l', 'foot_r', 'pelvis', 'head', 'hat_crown', 'brim')
for c, t0 in STAGED.items():
    t = TR['clips'].get(c, {})
    ok(t.get('staged') and t['seq']['t0'] == t0 and all(len(t.get(k, [])) == TABLE[c][0] + 1 for k in COLS), f'tracks: {c} staged, every column for {TABLE[c][0] + 1} ticks')
for c in ('lead60', 'lead5', 'lead_re'):
    ok(TR['clips'].get(c, {}).get('staged') is False, f'tracks: {c} is not staged (the fight is open there)')
R = lambda c, t: TR['clips'][c]['root'][t]
for c, t, want in [('intro', 0, [0, 0, 20.73, 0]), ('intro', 880, [0, 0, 20.73, 180]), ('intro', 1148, [0, 0, 13.5, 180]), ('intro', 1258, [0, 0, 6.5, 180]), ('intro_end', 150, [0, 0, 6.5, 180]),
                   ('cs1', 0, [0, 0, 9, 180]), ('cs1', 10, [0, 0, 1.5, 180]), ('cs1', 30, [0, 0, 1.5, 180]), ('cs1', 50, [0, 0, 9, 180]), ('cs1', 720, [0, 0, 9, 180]),
                   ('repel', 0, [0, 1, 1, 180]), ('repel', 6, [0, 0, 1.3, 180]), ('repel', 36, [0, 0, 1.1, 180]), ('repel', 68, [0, 0, 1.2, 180]), ('repel', 101, [0, 0, 3, 180]),
                   ('repel', 64, [0, 0, 1.2, 180]), ('repel', 129, [0, 0, 3, 180]), ('repel', 140, [0, 0, 9, 180]), ('ending', 0, [0, 0, 4.2, 180]), ('ending', 22, [0, 0, 4.6, 180]),
                   ('ending', 52, [0, 0, 3.75, 180]), ('ending', 54, [0, 0, 2.9, 180]),
                   ('ending', 56, [0, 0, 2.9, 180]), ('ending', 86, [0, 0, 6, 180]), ('ending', 190, [0, 0, 4, 180]), ('ending', 216, [0, 6, 3.6, 180]), ('ending', 228, [0, 6, 3.2, 180]),
                   ('ending', 262, [0, 6.4, 3.4, 180]), ('ending', 286, [0, 6, 3.3, 180]), ('ending', 304, [0, 6, 3.3, 180]),
                   ('ending', 334, [0, 0, 9, 180]), ('ending', 1154, [0, 0, 4.5, 180]), ('ending', 1372, [0, 0, 4.5, 180])]:
    ok(all(abs(a - b) < 1e-6 for a, b in zip(R(c, t)[:3], want[:3])) and abs((R(c, t)[3] - want[3]) % 360) < 1e-6, f'tracks: her root at {c} {t} = ST{tuple(want[:3])} yaw {want[3]} ({R(c, t)})')
# (HF-B, HB-01) the throw's root arcs 0.6 b (seq.py toss; her pelvis rides its own path over the actor's shoulder)
d88 = R('repel', 88); ok(abs(d88[1] - 0.59) < .01 and abs(d88[2] - 1.983) < .01, f'tracks: repel 88 the root on its low arc ({d88})')
for c in STAGED:
    t = TR['clips'][c]; worst = 0; low = 9
    for i in range(TABLE[c][0] + 1):
        r, p = t['root'][i], t['pelvis'][i]
        if r[1] == 0 and (i == 0 or t['root'][i - 1][1] == 0): worst = max(worst, math.hypot(p[0] - r[0], p[2] - r[2]))
        low = min(low, t['foot_l'][i][1] - r[1], t['foot_r'][i][1] - r[1], t['pelvis'][i][1] - r[1])
    ok(worst <= .75, f'tracks: {c} no root motion in the clip (the pelvis within {worst:.2f} b of the root\'s axis on the ground)')
    ok(low >= -.012, f'tracks: {c} soles and pelvis never under the root\'s floor ({low:+.3f} b)')

# ---- contacts --------------------------------------------------------------------------------------------------------------------------
ok(len(TR['contacts']) == 15, f'contacts: 15 rows judged by the builder ({len(TR["contacts"])})')
for c in TR['contacts']:
    ok(c['worst'] <= c['tol'], f'contacts: {c["id"]} ({c["clip"]} {c["ticks"][0]}-{c["ticks"][1]}, {c["kind"]}) {c["worst"]} b <= {c["tol"]}')
print(f'test_cine: {n - len(fails)} / {n} ok' + ('' if not fails else f', {len(fails)} FAILED'))
sys.exit(1 if fails else 0)

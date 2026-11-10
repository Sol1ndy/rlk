#!/usr/bin/env python3
"""test_seq.py: 홍련's sequences on the new combat (tools/mboss_scarlet/seq.py + cam.py, lane H2; hr_design §3 / §6.2): CS0
`intro`, CS1 `cs1`, the lead-ins, the repel counter, the ending and the coda, with their cameras, lock, lines, effects,
signals, skips and hand-backs.

    python3 test_seq.py <datapack root> [section ...] [--frames <dir with frames.json of hr/h2/sheets.py>]

Run it from a copy outside the datapack (tools/dev/sim/README.md §1). World: hr/h2/seqsim.py (the sequences driven as the
core contract says, the core parked; the F5 view and the lock of hr/h2/camsim.py; the kit stubbed and logged).

  static  CONTRACT = 2; one service per api.SEQS; every entry file (start / tick / cancel, skip of api.SEQ_EXTRA, lock /
          unlock / fin / cam of the locked ones); the lock request only in lock; no core / framework-private call, no
          game-mode or spectate command, no chat line, no tip text; vanilla sound ids; every function reference exists;
          no negative literal; the shot tables = the design's cut ticks and cameras, alternating A / B; the lock spans
  run     per sequence at the centre stage: its length; the request on every tick of its lock span, the player held from
          tick 1, released at the span's end, nothing left; the live camera of every tick; at every cut tick the stand
          where the table puts it (stage / her frame) looking at its look point; each line id at its tick (verbatim text,
          span); overlays, signals, music, the title, the look request; her marks and the distances of the design
  stages  cs1 / repel / ending + coda on a stage at the centre and at radius 24 on four bearings (there the stage's
          forward is the arena centre): every lens inside the walk disc, 0.2 b or more over the floor, in an air cell of
          the real arena; her feet and head in free cells inside the arena floor at every tick
  skip    CS0 from five ticks of its window -> 1290, CS1 -> 566: the state after the jump = the uninterrupted run's
  life    every exit path of every locked sequence: the end, cancel at any tick, pause and resume (death, Ronova's revive),
          /reload, relog, the live and the idle stand killed, the framework's cleanup, uninstall: the player released,
          no stand, stage, prop or flag left, the sequence itself never asks again once it was interrupted, its signals
          still come at their ticks; the developer mode (never locked); the real core: the intro from the rift to the
          fight, the kill through the ending and the coda to the reward
  actor   a dry build with the actor lines on (api.actor_ready): spawn as the player at the stage in the first tick, the
          clip of each sequence, #cavT cine = #sq and tick every locked tick, face at the ending's turn to ST2, stop at
          the end / cancel / unlock
  frames  the shot sheets' report (hr/h2/sheets.py: the real arena, stand-in figures): no lens in a block or a plant, no
          shot that never shows its subject; computed here when --frames is not given
"""
import json
import math
import re
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
sys.path.insert(0, str(HERE.parent / 'h2'))
import hrsim as H  # noqa: E402
import camsim as CS  # noqa: E402
import seqsim as Q  # noqa: E402
from mcsim import Ctx, split  # noqa: E402

ARGS = list(sys.argv[1:])
FRAMES = None
if '--frames' in ARGS:
    i = ARGS.index('--frames')
    FRAMES = Path(ARGS[i + 1])
    del ARGS[i:i + 2]
DP = Path(ARGS[0]).resolve()
SECT = ARGS[1:]
F = DP / 'data/rlk/function'
SQ = F / 'boss/scarlet/seq'
sys.path.insert(0, str(DP / 'tools'))
from mboss_scarlet import api, seq as SEQ, cam as CAM  # noqa: E402
import mboss_lib as L  # noqa: E402

LAST_CK = ['']


def ck(name, ok, info=''):
    LAST_CK[0] = name
    return H.ck(name, ok, info)


C0 = H.C0
TR = SEQ.tracks()
LOCKED = ('intro', 'cs1', 'repel', 'ending', 'event')


def want(n):
    return not SECT or n in SECT


# ---- the design's tables (hr_design §3, written out: the test must not read them back from the code under test) -----------
CUTS = {
    'intro': [(0, 1), (60, 2), (110, 1), (170, 2), (250, 1), (320, 2), (410, 1), (460, 2), (536, 1), (666, 2), (750, 1), (790, 2),
              (910, 1), (970, 2), (1040, 1), (1230, 2), (1260, 1), (1290, 2), (1350, 1), (1406, 2)],
    'cs1': [(0, 1), (6, 2), (34, 1), (84, 2), (180, 1), (220, 2), (276, 1), (340, 2), (380, 1), (500, 2), (610, 1), (648, 2)],
    'repel': [(0, 1), (26, 2), (52, 1), (68, 2), (78, 1), (102, 2), (128, 1), (132, 2)],
    'ending': [(0, 1), (50, 2), (94, 1), (118, 2), (150, 1), (190, 2), (204, 1), (240, 2), (276, 1), (314, 2), (338, 1), (378, 2),
               (470, 1), (556, 2), (616, 1), (700, 2), (846, 1), (882, 2), (972, 1), (1072, 2), (1212, 1)],
    'event': [(4, 2)],
}
LEN = {'intro': 1440, 'cs1': 720, 'lead60': 56, 'repel': 140, 'lead5': 116, 'lead_re': 60, 'ending': 1372, 'event': 120}
LOCK = {'intro': (0, 1440), 'cs1': (0, 720), 'repel': (0, 140), 'ending': (0, 1373), 'event': (0, 118)}
LINE_T = {'intro': {1: 258, 2: 340, 3: 462, 4: 540, 5: 690, 6: 838, 7: 906, 8: 980, 9: 1044, 10: 1140, 11: 1294},
          'cs1': {13: 110, 14: 232, 15: 578, 16: 618},
          'ending': {17: 420, 18: 486, 19: 628, 20: 716, 21: 910, 22: 1082, 23: 1230}}
LINE_SPAN = {1: 54, 2: 60, 3: 60, 4: 84, 5: 130, 6: 64, 7: 44, 8: 44, 9: 90, 10: 70, 11: 62, 13: 52, 14: 40, 15: 36, 16: 36,
             17: 58, 18: 66, 19: 42, 20: 118, 21: 128, 22: 128, 23: 88}
GOLD = 'gold' if api.K.ovl('gold', 0, 1, 1) else 'white'       # the stand-in while lane H2c's glyph is missing
OVL = {'intro': [], 'cs1': [(0, 'white', 0, 2, 2), (10, GOLD, 0, 1, 2), (642, 'negative', 0, 3, 0), (645, 'pinkwhite', 0, 3, 4),
                           (650, 'red_tint', 0, 4, 20)],
       'repel': [(0, GOLD, 0, 4, 3)],
       'ending': [(0, 'white', 0, 2, 1), (70, GOLD, 0, 1, 2), (190, GOLD, 0, 6, 6), (286, GOLD, 0, 3, 6)],
       'event': [(110, 'black', 10, 12, 0)], 'lead60': [], 'lead5': [], 'lead_re': []}
SIGS = {'repel': [(49, 1), (101, 2), (129, 3)], 'lead5': [(60, 4)], 'lead_re': [(10, 4)], 'lead60': [], 'intro': [], 'cs1': [],
        'ending': [], 'event': []}
# her mark on the stage axis at a tick (f, tolerance) and the distance her <-> the actor the design names
HER_F = {'intro': [(0, 20.73), (1040, 20.73), (1148, 13.5), (1230, 13.5), (1258, 6.5), (1440, 6.5)],
         'cs1': [(0, 9.0), (10, 1.5), (30, 1.5), (50, 9.0), (720, 9.0)],
         'repel': [(6, 1.3), (36, 1.1), (64, 1.2), (101, 3.0), (135, 8.0), (140, 9.0)],
         'ending': [(0, 4.2), (22, 4.6), (54, 2.9), (86, 6.0), (136, 11.0), (188, 4.0)]}
HER_F2 = {'ending': [(334, 9.0), (1094, 9.0), (1154, 4.5), (1372, 4.5)]}
DIST = {'intro': [(1, 26.7), (100, 20.7), (1148, 13.5), (1440, 6.5)],
        'cs1': [(0, 9.0), (20, 1.5), (58, 10.2), (80, 9.0), (720, 9.0)],
        'repel': [(20, 1.3), (44, 0.6), (72, 0.6), (110, 1.2), (140, 9.0)],
        'ending': [(22, 3.8), (60, 1.6), (90, 6.6), (190, 1.5), (220, 2.1), (334, 9.0), (1372, 4.5)]}


def lerp_keys(keys, t):
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            u = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
            return tuple(a + (b - a) * u for a, b in zip(v0, v1))
    return keys[-1][1]


def actor_shift(name, t):
    import sheets
    return lerp_keys(sheets.ACTOR_SHIFT[name], t)


def fn_lines(p):
    return [l for l in p.read_text(encoding='utf-8').split('\n') if l.strip() and not l.startswith('#')]


def all_seq_files():
    return sorted(SQ.rglob('*.mcfunction'))


def tick_files(name, kind='k'):
    """{tick: lines} of a sequence's leaf files (a shared leaf <a>_<b> counts for each of its ticks)."""
    out = {}
    for p in sorted((SQ / name / kind).glob('*.mcfunction')):
        a, _, b = p.stem.partition('_')
        for t in range(int(a), int(b or a) + 1):
            out[t] = fn_lines(p)
    return out


# ============================================================================================================ static
def static():
    src = (DP / 'tools/mboss_scarlet/seq.py').read_text(encoding='utf-8')
    ck('S1 seq.py declares CONTRACT = 2 (api.SEQ_CONTRACT)', re.search(r'^CONTRACT\s*=\s*2\b', src, re.M) and api.SEQ_CONTRACT == 2)
    ck('S1 one service per api.SEQS', [s.name for s in SEQ.SERVICES] == list(api.SEQS) == list(LEN) and api.SEQ_LEN == LEN)
    miss = []
    for n in api.SEQS:
        for f in ('start', 'tick', 'cancel') + tuple(api.SEQ_EXTRA.get(n, ())) + (('lock', 'unlock', 'fin', 'cam') if n in LOCKED else ()):
            if not (SQ / n / f'{f}.mcfunction').exists():
                miss.append(f'{n}/{f}')
    ck('S1 every entry file exists (start / tick / cancel, skip, lock / unlock / fin / cam)', not miss, str(miss))
    ck('S1 the lock spans of hr_design §3.0', SEQ.LOCK == LOCK, str(SEQ.LOCK))
    # the shot tables
    for n, cuts in CUTS.items():
        got = [(t, c) for t, c, _nm in TR[n].cuts()]
        ck(f'S2 {n}: the cut ticks and cameras of the design ({len(cuts)} shots)', got == cuts, str([x for x in got if x not in cuts]))
        ck(f'S2 {n}: consecutive shots alternate A / B', all(a[1] != b[1] for a, b in zip(got, got[1:])))
    ck('S2 CS0 has 20 shots, I18 (the skip target) at 1290 on camera B',
       len(CUTS['intro']) == 20 and TR['intro'].shot_at(1290).t == 1290 and TR['intro'].shot_at(1290).cam == 2)
    ck('S2 every stage of a dynamic sequence clamps its eyes into the walk disc; CS0 (fixed, checked in `frames`) does not',
       all(s.clamp for n in ('cs1', 'repel', 'ending', 'event') for s in TR[n].shots) and not any(s.clamp for s in TR['intro'].shots))
    # rules over the generated files
    files = all_seq_files()
    snd_ids = set((HERE.parent.parent / 'rd/tests/sound_ids.txt').read_text(encoding='utf-8').split()) \
        if (HERE.parent.parent / 'rd/tests/sound_ids.txt').exists() else None
    bad = {k: [] for k in ('negative literal', 'request outside lock', 'core call', 'gamemode / spectate', 'chat', 'sound',
                           'missing function', 'macro', 'upper case id')}
    for p in files:
        rel = p.relative_to(SQ).as_posix()[:-11]
        for ln in fn_lines(p):
            body = ln[1:] if ln.startswith('$') else ln
            if re.search(r'scoreboard players (add|remove) \S+ \S+ -', body):
                bad['negative literal'].append((rel, ln))
            if '#mbCam mb' in body and not rel.endswith('/lock'):
                bad['request outside lock'].append((rel, ln))
            if re.search(r'function rlk:boss/scarlet/(core|ai|shield|ult|hud|ev|test|p|g)/', body) and 'ev/apply' not in body and 'ev/title' not in body:
                bad['core call'].append((rel, ln))
            if re.search(r'(^| run )(gamemode|spectate) ', body):
                bad['gamemode / spectate'].append((rel, ln))
            if re.search(r'(^| run )(tellraw|say|msg|tell) ', body):
                bad['chat'].append((rel, ln))
            for m in re.finditer(r'playsound (\S+)', body):
                if snd_ids is not None and m.group(1) not in snd_ids:
                    bad['sound'].append((rel, m.group(1)))
            for ref in re.findall(r'function (rlk:[A-Za-z0-9_/.-]+)', body):
                if not (F / (ref.split(':', 1)[1] + '.mcfunction')).exists() and not ref.startswith('rlk:char/cine/'):
                    bad['missing function'].append((rel, ref))
                if ref != ref.lower():
                    bad['upper case id'].append((rel, ref))
            if ln.startswith('$') != ('$(' in ln):
                bad['macro'].append((rel, ln))
    for k, v in bad.items():
        ck(f'S3 seq/**: no {k}' if k not in ('sound', 'macro') else f'S3 seq/**: {"vanilla sound ids only" if k == "sound" else "a macro line has $(...) and only a macro line"}',
           not v, str(v[:4]))
    ck('S3 the sound list of the vanilla jar was there to check against', snd_ids is not None)
    titles = [(p.relative_to(SQ).as_posix(), ln) for p in files for ln in fn_lines(p) if re.search(r'(^| run )title ', ln)]
    ck('S3 the only title commands of seq/**: the blank actionbar at a start', all('actionbar ""' in ln for _r, ln in titles), str(titles[:3]))
    ck('S3 the hudHold of every locked sequence, each tick', all(SEQ.HUD_HOLD in fn_lines(SQ / n / 'tick.mcfunction') for n in LOCKED)
       and not any(SEQ.HUD_HOLD in fn_lines(SQ / n / 'tick.mcfunction') for n in ('lead60', 'lead5', 'lead_re')))
    # lines: verbatim, at their ticks, their spans
    kit = json.loads((DP / 'tools/mboss_hr_fx_manifest.json').read_text(encoding='utf-8'))
    ok = True
    for n, tab in LINE_T.items():
        k = tick_files(n)
        for i, t in tab.items():
            ok &= any(f'fx/hud/line {{id:{i}}}' in ln for ln in k.get(t, []))
        allc = [(t, int(m.group(1))) for t, ls in k.items() for ln in ls for m in [re.search(r'fx/hud/line \{id:(\d+)\}', ln)] if m]
        ok &= sorted(allc) == sorted((t, i) for i, t in tab.items())
    ck('S4 each line id at its tick, once (1-11 intro, 13-16 cs1, 17-23 ending)', ok)
    ck('S4 the lines are api.LINES verbatim in the kit, their spans the design\'s',
       all(api.LINE_AT[i][2] == sp for i, sp in LINE_SPAN.items()) and len(api.LINES) == 25
       and all(kit['lines'][str(i)]['text'] == api.LINES[i] and kit['lines'][str(i)]['on_screen'] == sp for i, sp in LINE_SPAN.items()))
    # music, the title, the look request, the rig looks at their ticks
    def has(n, t, frag):
        return any(frag in ln for ln in tick_files(n).get(t, []))
    ck('S5 music 1 at intro 1420, music 2 at cs1 676, music 3 at ending 420',
       has('intro', 1420, 'music/set {ph:1}') and has('cs1', 676, 'music/set {ph:2}') and has('ending', 420, 'music/set {ph:3}'))
    ck('S5 the title 홍련 / 월하곡 at the draw (intro 1356)', has('intro', 1356, 'mboss/title {title:"홍련",sub:"월하곡"'))
    ck('S5 the crimson look request and the rig\'s P2 accents at cs1 660', has('cs1', 660, '#hrLook hr 2') and has('cs1', 660, 'rig/look/phase/p2'))
    ck('S5 intro_end starts at 1290 (the skip target); the rock and the props go at 1052',
       has('intro', 1290, 'rig/play/intro_end') and has('intro', 1052, 'rig/look/props/none'))


# ============================================================================================================ helpers
def world(name, stage='c'):
    """A parked fight with the avatar and her placed for `name` (sheets.STAGES; the intro: the core's spawn state)."""
    import sheets
    s, pl = Q.setup(DP)
    assert Q.fight(s), 'the fight did not start'
    if name == 'intro':
        b = H.body_of(s)
        b.pos = list(api.SEAT_POS)
        mp = api.MOON_POS
        b.rot = [math.degrees(math.atan2(-(mp[0] - b.pos[0]), mp[2] - b.pos[2])), 0.0]
        st = api.ARENA['start']
        s.avatar().pos = [st['x'], st['y'], st['z']]
    else:
        Q.place(s, *sheets.STAGES[stage])
    return s, pl


ARGS_OF = {'repel60': {'at': 60}, 'repel5': {'at': 5}, 'lead_re': {'g': 'a13'}}


def seq_of(key):
    return {'repel60': 'repel', 'repel5': 'repel'}.get(key, key)


def frames_of(rec):
    """The frames dict of cam.to_world at a recorded tick."""
    fr = {'ENT': {}}
    if rec['stage']:
        fr['ST'] = rec['stage']
    if rec['stage2']:
        fr['ST2'] = rec['stage2']
    if rec['body']:
        fr['HR'] = rec['body']
        fr['ENT'][SEQ.BODY] = (rec['body'][0][0], rec['body'][0][1] + Q.HUSK_EYE, rec['body'][0][2])
    return fr


def near(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def ang(a, b):
    return abs((a - b + 180) % 360 - 180)


def stage_f(rec, frame='stage'):
    """Her (r, f) in the stage frame of a recorded tick."""
    (ox, _oy, oz), yaw = rec[frame]
    (x, _y, z), _ = rec['body']
    f, lf = CAM.basis(yaw)
    dx, dz = x - ox, z - oz
    return -(dx * lf[0] + dz * lf[1]), dx * f[0] + dz * f[1]


# ============================================================================================================ run
def run():
    for key in ('intro', 'cs1', 'lead60', 'repel60', 'repel5', 'lead5', 'lead_re', 'ending'):
        name = seq_of(key)
        s, pl = world(key if key == 'intro' else name)
        if name.startswith('lead'):
            s.setsc('#warn', 'hr', 1)
        then = ('event', None) if key == 'ending' else None
        stop_at = (lambda s: False)
        if key == 'repel5':
            stop_at = (lambda s: (s.sc('#sq', 'hr') or 0) >= 129)      # the core kills her at the kick
        rec = Q.play(s, name, args=ARGS_OF.get(key), then=then, until=stop_at)
        if key == 'repel5':
            Q.stop(s)
            s.call(f'{H.ROOT_SC}seq/repel/cancel', C0)                 # death_start: core/stop_all cancels the running sequence
        parts = {}
        for r in rec:
            parts.setdefault(r['seq'], {})[r['sq']] = r
        for sn, by in parts.items():
            tag = f'{key}{"" if sn == name else " -> " + sn}'
            ln = LEN[sn]
            if key != 'repel5':
                ck(f'R1 {tag}: #sqdone at {ln}', (sn, ln) in s.done and max(by) == ln, f'{s.done} {max(by)}')
            # the lock
            if sn in LOCK:
                t0, t1 = LOCK[sn]
                last = min(t1 - 1, max(by))
                req = [t for t in by if by[t]['req'] != (1 if t <= last and t < t1 else 0)]
                ck(f'R2 {tag}: the request on every tick of {t0}..{t1 - 1} and on no other', not req, str(req[:6]))
                first_held = 1 if sn == name else 0
                held = [t for t in by if first_held <= t <= last and not (by[t]['held'] and by[t]['gm'] == 'spectator')]
                ck(f'R2 {tag}: the player held (spectator) from tick {first_held} on', not held, str(held[:6]))
                live = [t for t in sorted(by) if t <= last and (CUTS[sn][0][0] <= t) and by[t]['live'] != TR[sn].shot_at(t).cam]
                ck(f'R3 {tag}: the live camera of every tick = the table', not live, str(live[:6]))
                bad = []
                for shot in TR[sn].shots:
                    r = by.get(shot.t)
                    if r is None:
                        continue
                    pos, rot = r['cam'][shot.cam]
                    fr = frames_of(r)
                    eye, look = shot.at(shot.t)
                    we, wl = CAM.to_world(eye, fr), CAM.to_world(look, fr)
                    lifted = shot.clamp and eye[0] in ('ST', 'ST2') and eye[2] < CAM.LOW and abs(pos[1] - (201.0 + SEQ.LIFT_TO)) < 1e-6
                    if lifted:
                        we = (we[0], 201.0 + SEQ.LIFT_TO, we[2])
                    y, p = CAM.yaw_pitch(pos, wl)
                    if not near(pos, we, 0.02) or (math.dist(pos, wl) > 0.2 and (ang(rot[0], y) > 0.6 or abs(rot[1] - p) > 0.6)):
                        bad.append((shot.t, shot.name, [round(v, 2) for v in pos], [round(v, 2) for v in we], [round(v, 1) for v in rot], round(y, 1), round(p, 1)))
                ck(f'R3 {tag}: at every cut the stand is at the table\'s eye, looking at its look point', not bad, str(bad[:3]))
            else:
                ck(f'R2 {tag}: never locked', not any(r['req'] or r['held'] for r in by.values()))
            # overlays / signals
            ov = [(t, a['g'], int(a['in']), int(a['hold']), int(a['out'])) for t in sorted(by) for c, a in by[t]['kit'] if c == 'hud/ovl']
            if key != 'repel5':
                ck(f'R4 {tag}: the overlays of the design at their ticks', ov == OVL[sn], str(ov))
            sg = [(t, by[t]['sig']) for t in sorted(by) if by[t]['sig']]
            ck(f'R4 {tag}: the signals {SIGS[sn]}', sg == SIGS[sn], str(sg))
            ls = [(t, int(a['id'])) for t in sorted(by) for c, a in by[t]['kit'] if c == 'hud/line']
            ck(f'R4 {tag}: the lines at their ticks', sorted(ls) == sorted((t, i) for i, t in LINE_T.get(sn, {}).items())
               or sn == 'event', str(ls))
            # her marks and the distances
            miss = [(t, f, round(stage_f(by[t])[1], 2)) for t, f in HER_F.get(sn, []) if t in by and by[t]['stage']
                    and (abs(stage_f(by[t])[1] - f) > 0.06 or abs(stage_f(by[t])[0]) > 0.06)]
            miss += [(t, f, round(stage_f(by[t], 'stage2')[1], 2)) for t, f in HER_F2.get(sn, []) if t in by and by[t]['stage2']
                     and abs(stage_f(by[t], 'stage2')[1] - f) > 0.06]
            ck(f'R5 {tag}: her marks on the stage axis {[f for _t, f in HER_F.get(sn, []) + HER_F2.get(sn, [])]}', not miss, str(miss))
            dd = []
            for t, d in DIST.get(sn, []):
                if t not in by or (key == 'repel5' and t > 129):
                    continue
                r = by[t]
                st = r['stage2'] if (sn == 'ending' and t >= 334 and r['stage2']) else r['stage']
                if st is None:                        # the last tick: the stage is gone, the avatar is its origin
                    st = (r['avatar'], 0.0)
                sh = actor_shift(sn, t) if st is not r['avatar'] else (0, 0, 0)
                fr = {'ST': st}
                ap = CAM.to_world(('ST',) + tuple(sh), fr) if r['stage'] else r['avatar']
                got = math.hypot(r['body'][0][0] - ap[0], r['body'][0][2] - ap[2])
                if abs(got - d) > 0.12:
                    dd.append((t, d, round(got, 2)))
            ck(f'R5 {tag}: the distances her <-> the actor of the design {[d for _t, d in DIST.get(sn, [])]}', not dd, str(dd))
            if sn in LOCK:
                sp = CAM.slow_pans(TR[sn], lambda t: frames_of(by[min(t, max(by))]))
                for _s, nm, t0, t1, dps, _d in sp:
                    print(f'   slow pan (in-game check: rotation is sent in 1.4-degree steps): {tag} {nm} {t0}-{t1}: {dps:.2f} deg / t')
            cm = [r['cmds'] for r in by.values()]
            print(f'   {tag}: {len(by)} ticks, commands per tick avg {sum(cm) / len(cm):.0f} / max {max(cm)} (the sequence\'s own files)')
            ck(f'R6 {tag}: at most 400 commands of its own in a tick', max(cm) <= 400, str(max(cm)))
        Q.go(s, 2)
        if key in ('intro', 'cs1', 'repel60', 'repel5', 'ending'):
            bad = [k for k, v in CS.clean(s).items() if not v]
            ck(f'R7 {key}: after it the player is released and nothing is left', not bad and not Q.leftovers(s), f'{bad} {Q.leftovers(s)}')
        if key == 'intro':
            b, av = H.body_of(s), s.avatar()
            ck('R8 CS0 hand-back: the avatar at P0, she 6.5 b ahead facing it',
               near(av.pos, api.CS0_P0, 0.02) and abs(math.dist(b.pos[::2], av.pos[::2]) - 6.5) < 0.05
               and ang(b.rot[0], math.degrees(math.atan2(-(av.pos[0] - b.pos[0]), av.pos[2] - b.pos[2]))) < 0.5, f'{av.pos} {b.pos} {b.rot}')
        if key in ('cs1', 'repel60'):
            b, av = H.body_of(s), s.avatar()
            ck(f'R8 {key} hand-back: the avatar where it stood, she 9.0 b ahead facing it',
               abs(math.dist(b.pos[::2], av.pos[::2]) - 9.0) < 0.05
               and ang(b.rot[0], math.degrees(math.atan2(-(av.pos[0] - b.pos[0]), av.pos[2] - b.pos[2]))) < 0.5, f'{av.pos} {b.pos} {b.rot}')


# ============================================================================================================ stages
def stages():
    import sheets
    import shots as SH
    arenas = {lk: SH.Arena(DP, lk) for lk in ('moon', 'crimson')}
    for key in ('cs1', 'repel60', 'ending'):
        for st in ('c', 'n', 'e', 's', 'w'):
            s, by = sheets.run(DP, key, st)
            eye_bad, her_bad, fwd = [], [], None
            n = 0
            for sn, recs in by.items():
                for t, r in recs.items():
                    look = 'crimson' if (sn in ('repel', 'ending', 'event') or (sn == 'cs1' and t >= 664)) else 'moon'
                    ar = arenas[look]
                    if r['stage'] and fwd is None:
                        (ox, _y, oz), yaw = r['stage']
                        f, _l = CAM.basis(yaw)
                        to_c = math.degrees(math.atan2(-(880.0 - ox), 8.0 - oz))
                        fwd = 'centre' if ang(yaw, to_c) < 0.5 and math.hypot(ox - 880, oz - 8) > 1 else 'her'
                    if r['req'] and r['live'] in (1, 2) and r['cam'][r['live']]:
                        pos = r['cam'][r['live']][0]
                        n += 1
                        cell, cls = ar.cell(pos)
                        rad = math.hypot(pos[0] - 880.0, pos[2] - 8.0)
                        if cls != SH.AIR or rad > 25.0 or pos[1] < 201.2:
                            eye_bad.append((sn, t, [round(v, 2) for v in pos], cell, round(rad, 2)))
                    (bx, byy, bz), _yaw = r['body']
                    rad = math.hypot(bx - 880.0, bz - 8.0)
                    c1, c2 = ar.cell((bx, byy + 0.01, bz)), ar.cell((bx, byy + 1.5, bz))
                    if rad > 25.0 + 1e-6 or byy < 201.0 - 1e-6 or c1[1] == SH.SOLID or c2[1] == SH.SOLID or 'barrier' in c1[0] + c2[0]:
                        her_bad.append((sn, t, [round(v, 2) for v in (bx, byy, bz)], round(rad, 2), c1[0]))
            want_fwd = 'her' if st == 'c' else 'centre'
            ck(f'G1 {key} stage {st}: the stage faces {"her" if st == "c" else "the arena centre (ST(0, 0, FMAX) fails mv/ok)"}',
               fwd == want_fwd or (st == 'c' and fwd == 'centre'), str(fwd))
            ck(f'G2 {key} stage {st}: every lens in the walk disc, >= 0.2 b over the floor, in an air cell ({n} locked ticks)',
               not eye_bad, str(eye_bad[:4]))
            ck(f'G3 {key} stage {st}: her feet and head in free cells on the arena floor at every tick', not her_bad, str(her_bad[:4]))
            bad = [k for k, v in CS.clean(s).items() if not v]
            Q.go(s, 2)
            bad = [k for k, v in CS.clean(s).items() if not v]
            ck(f'G4 {key} stage {st}: released, nothing left', not bad and not Q.leftovers(s), f'{bad} {Q.leftovers(s)}')


# ============================================================================================================ skip
def state(s):
    """What a skip must reproduce: her place and yaw, the live camera's stand, the props, the lock. (The idle stand stays
    where the skipped shot left it: it is placed again 4 t before the next cut.)"""
    b = H.body_of(s)
    live = s.sc('#mbCamId', 'mb')
    e = s.snap('x', 0, [], 0)['cam'][live]
    return dict(body=[round(v, 2) for v in b.pos], yaw=round(b.rot[0] % 360, 1), live=live,
                cam=None if e is None else ([round(v, 2) for v in e[0]], [round(v, 1) for v in e[1]]),
                props=sorted(sorted(e.tags) for e in s.ents if e.alive and ('rlk_hr_sqp' in e.tags or 'rlk_hr_deco_seat_rock' in e.tags)),
                held=CS.held(s))


def lines_from(rec, name, t0):
    return [(r['sq'], [int(a['id']) for c, a in r['kit'] if c == 'hud/line']) for r in rec
            if r['seq'] == name and r['sq'] >= t0 and any(c == 'hud/line' for c, _a in r['kit'])]


def skip():
    for name in ('intro', 'cs1'):
        to = api.SKIP[name]['to']
        lo, hi = api.SKIP[name]['window']
        ck(f'K0 {name}: the window {lo}..{hi} and the target {to} of hr_design §3',
           (name, lo, hi, to) in (('intro', 20, 1270, 1290), ('cs1', 40, 560, 566)))
        s, pl = world(name)
        k0 = len(s.rec)
        Q.play(s, name, until=lambda s: (s.sc('#sq', 'hr') or 0) >= to + 4)
        ref = state(s)
        while s.drive is not None:                      # the reference run goes on to its end
            CS.world(s)
        ref_end = state(s)
        ref_tail = lines_from(s.rec[k0:], name, to)
        ck(f'K0 {name}: the full run has lines after {to} (the check below is not empty)', len(ref_tail) >= 1, str(ref_tail))
        for at in sorted({lo, lo + 37, (lo + hi) // 2, hi - 51, hi}):
            s, pl = world(name)
            Q.play(s, name, until=lambda s: (s.sc('#sq', 'hr') or 0) >= at)
            b = H.body_of(s)
            n0 = len(s.rec)
            s.call(f'{H.ROOT_SC}seq/{name}/skip', Ctx(b, tuple(b.pos), tuple(b.rot)))      # the core, after the hold
            s.setsc('#sq', 'hr', to - 1)
            ov = [(a['g'], int(a['in']), int(a['hold']), int(a['out'])) for _t, c, a in s.kitl if c == 'hud/ovl'][-1:]
            while s.drive is not None and (s.sc('#sq', 'hr') or 0) < to + 4:
                CS.world(s)
            got = state(s)
            ck(f'K1 {name} skipped at {at}: the black 0 / 20 / 6; the state at {to + 4} = the uninterrupted run\'s (her place and yaw, '
               f'the live camera and its stand, the props, still locked)', ov == [('black', 0, 20, 6)] and got == ref,
               f'{ov} {[(k, got[k], ref[k]) for k in got if got[k] != ref[k]]}')
            while s.drive is not None:
                CS.world(s)
            ck(f'K2 {name} skipped at {at}: it ends as the uninterrupted run (#sqdone at {LEN[name]}, the same end state)',
               (name, LEN[name]) in s.done and state(s) == ref_end, str([(k, state(s)[k], ref_end[k]) for k in ref_end if state(s)[k] != ref_end[k]]))
            tail = lines_from(s.rec[n0:], name, to)
            ck(f'K2 {name} skipped at {at}: the lines from {to} on come as in the full run', tail == ref_tail, f'{tail} {ref_tail}')
            Q.go(s, 2)
            bad = [k for k, v in CS.clean(s).items() if not v]
            ck(f'K3 {name} skipped at {at}: released, nothing left', not bad and not Q.leftovers(s), f'{bad} {Q.leftovers(s)}')
    if api.rig_real():
        ln = fn_lines(SQ / 'cs1/skip.mcfunction')
        ck('K4 the CS1 skip moves her clip to tick 565 (the rig shows 566 next) and sets the discrete looks of 566',
           'scoreboard players set @s hrRigT 565' in ln and all(any(f'rig/look/{x}' in l for l in ln) for x in
                                                                ('sword/sheathed', 'hat/worn', 'scabbard/hip', 'props/none', 'face/calm')))


# ============================================================================================================ life
def clean_now(tag, s, gm0='adventure', seat=True, req=True):
    bad = [k for k, v in CS.clean(s, gm0=gm0, seat=seat, req=req).items() if not v]
    lf = Q.leftovers(s)
    ck(tag, not bad and not lf, f'{bad} {lf}')


def life():
    mids = {'intro': 400, 'cs1': 300, 'repel60': 60, 'ending': 500}
    for key, mid in mids.items():
        name = seq_of(key)
        end = LEN[name]
        chain = ('event', None) if key == 'ending' else None      # the core starts the coda at the ending's #sqdone
        names = (name, 'event') if chain else (name,)

        def start(gm='adventure', upto=mid):
            s, pl = world(key if key == 'intro' else name)
            s.st(pl)['gm'] = gm
            Q.play(s, name, args=ARGS_OF.get(key), then=chain, until=lambda s: (s.sc('#sq', 'hr') or 0) >= upto)
            assert CS.held(s), (key, 'not held at', upto)
            return s, pl

        def cancel(s):
            """What the core does to end a sequence early (core/stop_all, its reload hook): the driver stops, cancel."""
            Q.stop(s)
            for n in names:
                s.call(f'{H.ROOT_SC}seq/{n}/cancel', C0)

        def player_free(s, gm0='adventure'):
            return [k for k, v in CS.clean(s, gm0=gm0, stands=True).items() if not v]

        def finish(s, tag, gm0='adventure'):
            """The sequence goes on (a core that resumes it instead of ending it, hr_design §3.6): it must never ask for the
            lock again, end as usual and leave nothing."""
            k0 = len(s.rec)
            while s.drive is not None:
                CS.world(s)
            rest = [r for r in s.rec[k0:] if r['seq'] in names]
            ck(f'{tag}: the sequence does not ask again for the rest of its run and nobody is held',
               all(r['req'] == 0 and not r['held'] for r in rest[1:]), str([(r['seq'], r['sq'], r['req'], r['held']) for r in rest if r['req'] or r['held']][:4]))
            ck(f'{tag}: it still ends at {end}', (name, end) in s.done and (not chain or ('event', LEN['event']) in s.done), str(s.done))
            if name == 'repel':
                ck(f'{tag}: its HP signals still come at 49 / 101 / 129', [x[1:] for x in s.sigs if x[0] == 'repel'] == SIGS['repel'], str(s.sigs))
            Q.go(s, 2)
            clean_now(f'{tag}: at its end nothing is left', s, gm0=gm0)

        # cancel at a tick (the core's stop_all / a reload's end state)
        s, pl = start(gm='survival')
        cancel(s)
        cancel(s)
        ck(f'L1 {key} cancel at {mid} (twice): the stands, the stage and the props are gone at once', not Q.leftovers(s), str(Q.leftovers(s)))
        CS.world(s)
        clean_now(f'L1 {key} cancel: the player is released in the next tick (the request stopped)', s, gm0='survival')
        # pause by death, then alive again
        s, pl = start()
        s.setsc(('e', pl.id), 'dead', 1)
        CS.world(s)
        ck(f'L2 {key} death at {mid}: released at once (game mode back, not held)', not CS.held(s) and CS.gm(s) == 'adventure')
        s.setsc(('e', pl.id), 'dead', 0)
        CS.world(s)
        finish(s, f'L2 {key} death, alive again')
        # Ronova's revive
        s, pl = start(gm='creative')
        s.setsc(('e', pl.id), 'rnDie', 40)
        CS.world(s)
        ck(f'L3 {key} Ronova\'s revive at {mid}: released at once, back at the avatar on the seat', not player_free(s, 'creative'),
           str(player_free(s, 'creative')))
        s.setsc(('e', pl.id), 'rnDie', 0)
        finish(s, f'L3 {key} revived', gm0='creative')
        # the same pause, the core ending the sequence at the resume (hr_design §3.6: never resumed in the middle)
        s, pl = start()
        s.setsc(('e', pl.id), 'rnDie', 40)
        CS.run(s, 3)
        s.setsc(('e', pl.id), 'rnDie', 0)
        cancel(s)
        CS.world(s)
        clean_now(f'L3 {key} revived, the sequence cancelled at the resume: nothing left', s)
        # /reload: load kills the view entities, mboss/init releases the player and kills the helper entities; her module's
        # reload hook then ends the sequence (core/intro/reload, core/re/cs1, core/re/repel; the death: the framework)
        s, pl = start()
        av0 = list(s.avatar().pos)
        for e in s.ents:
            if 'rlk_view' in e.tags:
                e.alive = False
        s.ents = [e for e in s.ents if e.alive]
        s.setsc('#vFresh', 'view', 1)
        s.setsc('#ph', 'hr', api.PH['death'])           # the hook returns before the core's own states (parked here)
        Q.stop(s)
        s.call('rlk:mboss/init', C0)
        ck(f'L4 {key} /reload at {mid}: released inside mboss/init, the stands dead, the player at the stored point',
           not CS.held(s) and CS.gm(s) == 'adventure' and not s.stands() and abs(pl.pos[0] - av0[0]) < 0.02 and abs(pl.pos[2] - av0[2]) < 0.02)
        cancel(s)
        Q.park_core(s)
        CS.run(s, 3)
        clean_now(f'L4 {key} reloaded, the hook\'s cancel: nothing left, the F5 view rebuilt', s)
        # relog
        s, pl = start()
        s.ents.remove(pl)
        CS.run(s, 4)
        s.st(pl)['cam'] = None
        s.ents.append(pl)
        s.setsc('#vFresh', 'view', 1)
        CS.world(s)
        ck(f'L5 {key} relog at {mid}: released in the first tick back', not CS.held(s) and CS.gm(s) == 'adventure')
        finish(s, f'L5 {key} relogged')
        # the live stand killed / the idle stand killed
        s, pl = start()
        live = s.sc('#mbCamId', 'mb')
        for e in s.ents:
            if f'rlk_mb_cam{live}' in e.tags:
                e.alive = False
        s.ents = [e for e in s.ents if e.alive]
        s.net_tick(pl)
        CS.world(s)
        ck(f'L6 {key} the live stand killed at {mid}: released in the next tick', not CS.held(s) and CS.gm(s) == 'adventure')
        finish(s, f'L6 {key} live stand killed')
        s, pl = start()
        idle = 3 - s.sc('#mbCamId', 'mb')
        for e in s.ents:
            if f'rlk_mb_cam{idle}' in e.tags:
                e.alive = False
        s.ents = [e for e in s.ents if e.alive]
        k0 = len(s.rec)
        while s.drive is not None:
            CS.world(s)
        rest = [r for r in s.rec[k0:] if r['seq'] == name and r['sq'] < LOCK[name][1]]
        ck(f'L7 {key} the idle stand killed at {mid}: it is back for the next cut, the lock holds to the end',
           all(r['held'] for r in rest) and all(r['req'] for r in rest), str([(r['sq'], r['held']) for r in rest if not r['held']][:4]))
        Q.go(s, 2)
        clean_now(f'L7 {key} ... and the end is clean', s)
        # the framework's cleanup (won / cancelled / defeat / map change) and uninstall
        s, pl = start(gm='survival')
        Q.stop(s)
        s.call('rlk:mboss/cleanup', C0)
        clean_now(f'L8 {key} mboss/cleanup at {mid}: released at once, nothing left', s, gm0='survival')
        s, pl = start()
        Q.stop(s)
        s.call('rlk:mboss/uninstall', C0)
        clean_now(f'L9 {key} uninstall at {mid}: released, nothing left', s)
        # sneaking through a stretch (the skip input): held all along
        s, pl = start()
        pl.data['sneak'] = True
        k0 = len(s.rec)
        CS.run(s, 12)
        pl.data['sneak'] = False
        ck(f'L10 {key} Shift held 12 t at {mid}: still locked, the stand taken back every tick', all(r['held'] and r['req'] for r in s.rec[k0 + 1:])
           and CS.held(s))
    # the developer mode: never locked, the sequence runs to its end
    s, pl = Q.setup(DP)
    s.setsc(('e', pl.id), 'devMode', 1)
    z, a = H.rift_zone(s, 'scarlet')
    pl.pos = list(a.pos)
    H.enter(s, a)
    CS.until(s, lambda s: H.body_of(s) is not None and (s.sc('#sq', 'hr') or 0) >= 1, 1200)
    H.call_sc(s, 'core/intro/done')
    Q.park_core(s)
    pl.pos = [880.0, 201.0, 20.0]
    H.place_body(s, 880.0, 8.0)
    rec = Q.play(s, 'cs1')
    ck('L11 developer mode (the player is the body): CS1 runs to its end, the player is never held or switched',
       ('cs1', 720) in s.done and not any(r['held'] for r in rec) and not s.gm_log and all(r['cx'] == 0 for r in rec))
    Q.go(s, 2)
    ck('L11 ... and nothing is left', not Q.leftovers(s), str(Q.leftovers(s)))
    # the real core: the intro from the rift to the fight
    s, pl = Q.setup(DP)
    ok = Q.fight(s, park=False)
    held, t = [], 0
    while (H.mb(s, '#mbSt') or 0) == 0 and t < 1500:
        CS.world(s)
        t += 1
        held.append(CS.held(s))
    sqs = s.sc('#sq', 'hr')
    ck('L12 the real core: the intro runs locked from the rift to the fight (1440 t), the bars off meanwhile',
       ok and (H.mb(s, '#mbSt') or 0) == 1 and sum(held) >= 1430 and (s.sc('#ph', 'hr') or 0) == api.PH['p1'], f'{sum(held)} {t} {sqs}')
    b, av = H.body_of(s), s.avatar()
    d0 = math.dist(b.pos[::2], av.pos[::2])            # at the first fight tick (her AI moves her from the next one)
    CS.world(s)
    clean_now('L12 ... control: the player released, nothing left', s)
    ck('L12 ... she stood 6.5 b before the avatar at the hand-back, the bars are back', abs(d0 - 6.5) < 0.1
       and (H.mb(s, '#mbBarOff') or 0) == 0, f'{d0:.2f} {H.mb(s, "#mbBarOff")}')
    # the real core: /reload inside the intro -> its reload hook ends it (core/intro/reload: cancel + the end state)
    s2, pl2 = Q.setup(DP)
    ok2 = Q.fight(s2, park=False)
    CS.run(s2, 400)
    held0 = CS.held(s2)
    for e in s2.ents:
        if 'rlk_view' in e.tags:
            e.alive = False
    s2.ents = [e for e in s2.ents if e.alive]
    s2.setsc('#vFresh', 'view', 1)
    s2.call('rlk:mboss/init', C0)
    ck('L14 the real core, /reload at tick ~400 of the intro: released inside mboss/init, the stands dead',
       ok2 and held0 and not CS.held(s2) and CS.gm(s2) == 'adventure' and not s2.stands())
    CS.run(s2, 3)
    clean_now('L14 ... its hook ended the intro (the fight runs, phase p1), nothing left, never locked again', s2)
    ck('L14 ... the fight state', (H.mb(s2, '#mbSt') or 0) == 1 and (s2.sc('#ph', 'hr') or 0) == api.PH['p1'] and not CS.held(s2),
       f'{H.mb(s2, "#mbSt")} {s2.sc("#ph", "hr")}')
    # the real core: the kill -> the ending -> the coda -> the reward
    H.hold(s, True)
    H.kill(s, pl)
    held, t = [], 0
    while (H.mb(s, '#mbLive') or 0) == 1 and t < 1700:
        CS.world(s)
        t += 1
        held.append(CS.held(s))
    ck('L13 the real core: the kill -> the ending and the coda run under one lock (1372 + 118 t), then the reward path',
       (H.mb(s, '#mbLive') or 0) == 0 and 1485 <= sum(held) <= 1492 and all(held[:1480]), f'{sum(held)} of {t}')
    Q.go(s, 3)
    clean_now('L13 ... afterwards the player is released and nothing is left', s)


# ============================================================================================================ actor
def actor():
    """The actor wiring (hr_design §5.3; lane H3's functions are stubbed and logged by the sim: its own suite is
    test_actor.py). Without H3's manifest: a dry build with the actor lines on."""
    root, dry = DP, False
    if not api.actor_ready():
        root, dry = H.variant_hr(DP, lambda reg: None, label='h2actor', gens=()), True
        H.dry_build(root, patch='api.actor_ready = lambda: True')
    try:
        _actor(root)
    finally:
        if dry:
            shutil.rmtree(root, ignore_errors=True)


def _actor(root):
    import sheets
    FR = root / 'data/rlk/function'
    man = SEQ.actor_man()
    if man:
        ck('A0 lane H3\'s manifest: the five clips with the sequences\' lengths; every call of the wiring exists as a function',
           {c: man['clips'][c]['len'] for c in man['clips']} == {'cs0': 1440, 'cs1': 720, 'repel': 140, 'ending': 1372, 'coda': 120}
           and all((FR / f'char/cine/{c}.mcfunction').exists() for c in ('spawn', 'play', 'tick', 'face', 'stop')))
        ck('A0 the skip targets and every clip end are sync ticks of the actor (a #cavT jump is exact there)',
           1290 in man['clips']['cs0']['sync'] and 566 in man['clips']['cs1']['sync']
           and all(man['clips'][c]['len'] in man['clips'][c]['sync'] and 0 in man['clips'][c]['sync'] for c in man['clips']))
        st = [t for t, ls in tick_files('intro').items() if any('grass_step' in ln and 'rlk_hr_stage' in ln for ln in ls)]
        ck('A0 CS0: the actor\'s step sounds on the manifest\'s footfalls', sorted(st) == sorted(man['clips']['cs0']['steps']), str(sorted(st)))
    clip_of = {'intro': 'cs0', 'cs1': 'cs1', 'repel': 'repel', 'ending': 'ending'}

    def stage(s, key):
        del s.actor_log[:]                           # (the setup ran the core's own intro start and its end)
        if key == 'intro':
            H.body_of(s).pos = list(api.SEAT_POS)
            st = api.ARENA['start']
            s.avatar().pos = [st['x'], st['y'], st['z']]
        else:
            Q.place(s, *sheets.STAGES['c'])

    for key in ('intro', 'cs1', 'repel60', 'ending'):
        name = seq_of(key)
        s, pl = Q.setup(root)
        assert Q.fight(s)
        stage(s, key)
        t_start = s.t + 1
        rec = Q.play(s, name, args=ARGS_OF.get(key), then=('event', None) if key == 'ending' else None)
        log = s.actor_log
        sp = [x for x in log if x[1] == 'spawn']
        st0 = rec[0]['stage']
        ck(f'A1 {key}: spawn once, in the first tick, as the player, at the stage and rotated as it',
           len(sp) == 1 and sp[0][0] == t_start and sp[0][2] == 'player' and near(sp[0][3], st0[0], 0.01)
           and ang(sp[0][4][0], st0[1]) < 0.01, str(sp[:2]))
        pls = [x[5].get('clip') for x in log if x[1] == 'play']
        ck(f'A2 {key}: play {clip_of[name]}{" then coda (no new spawn: ending 1372 = coda 0)" if key == "ending" else ""}',
           pls == [clip_of[name]] + (['coda'] if key == 'ending' else []), str(pls))
        tk = [x for x in log if x[1] == 'tick']
        span = LOCK[name][1] + (LOCK['event'][1] if key == 'ending' else 0)
        ck(f'A3 {key}: tick as the player on every locked tick ({span}), #cavT cine = #sq',
           len(tk) == span and all(x[2] == 'player' for x in tk) and [x[6] for x in tk][:LOCK[name][1]] == list(range(LOCK[name][1])),
           f'{len(tk)} {[x[6] for x in tk][:5]}')
        stops = [x for x in log if x[1] == 'stop']
        ck(f'A4 {key}: stop at the end; the actor is gone', len(stops) >= 1 and not s.actor_on and stops[0][0] >= t_start + LOCK[name][1] - 1, str(stops[:2]))
        if key == 'ending':
            fc = [x for x in log if x[1] == 'face']
            st2 = next(r['stage2'] for r in rec if r['seq'] == 'ending' and r['sq'] == 338)
            ck('A5 ending: face at 338 with ST2\'s absolute yaw (the turn to her landing mark)',
               len(fc) == 1 and fc[0][0] == t_start + 338 and abs((float(fc[0][5]['yaw']) - st2[1] + 180) % 360 - 180) < 0.02, str(fc))
        # interrupted: the actor is stopped by the unlock (and by the framework's release), never ticked again
        s, pl = Q.setup(root)
        assert Q.fight(s)
        stage(s, key)
        Q.play(s, name, args=ARGS_OF.get(key), then=('event', None) if key == 'ending' else None, until=lambda s: (s.sc('#sq', 'hr') or 0) >= 40)
        s.setsc(('e', pl.id), 'rnDie', 5)
        CS.world(s)
        s.setsc(('e', pl.id), 'rnDie', 0)
        n0 = len(s.actor_log)
        while s.drive is not None:
            CS.world(s)
        ck(f'A6 {key} interrupted at 40: the actor stopped by the release; to the sequence\'s end no spawn, play or tick',
           not s.actor_on and not any(x[1] in ('tick', 'spawn', 'play') for x in s.actor_log[n0:]),
           str([x[:3] for x in s.actor_log[n0:] if x[1] != 'stop'][:4]))
        Q.go(s, 2)
        ck(f'A6 {key} ... nothing left', not Q.leftovers(s), str(Q.leftovers(s)))
    # the lethal repel -> the ending, as the core does it: at the kick (129, signal 3) death_start in the same tick
    # (core/stop_all cancels the repel, core/seq/ending starts the ending). Lane H3: no new spawn, play ending.
    s, pl = Q.setup(root)
    assert Q.fight(s)
    stage(s, 'repel5')
    Q.play(s, 'repel', args={'at': 5}, until=lambda s: (s.sc('#sq', 'hr') or 0) >= 129)
    root_e = s.actor_root()
    ck('A7 repel {at:5} at the kick: locked, the actor stands', CS.held(s) and root_e is not None and s.sigs[-1][1:] == (129, 3), str(s.sigs[-1:]))
    n0 = len(s.actor_log)
    s.setsc('#sqn', 'hr', 4)                         # the core's id of the running repel (core/stop_all cancels by it)
    b = H.body_of(s)
    s.call(f'{H.ROOT_SC}death_start', Ctx(b, tuple(b.pos), tuple(b.rot)))
    new = [(x[1], x[5].get('clip')) for x in s.actor_log[n0:]]
    ck('A7 death_start in that tick: the repel\'s cancel leaves the actor, the ending plays its clip on the same actor (no stop, no spawn)',
       new == [('play', 'ending'), ('tick', None)] and s.actor_root() is root_e and (s.sc('#sq_keep', 'hr') or 0) == 0, str(new))
    s.drive = dict(name='ending', args=None, t=0, then=('event', None))     # the driver takes the ending over from its tick 0
    Q.park_core(s)
    k0 = len(s.rec)
    CS.run(s, 6)
    ck('A7 ... the lock never drops over the hand-over (held every tick, the request on), the actor on the ending\'s clock from 1',
       all(r['held'] and r['req'] for r in s.rec[k0:]) and [x[6] for x in s.actor_log if x[1] == 'tick'][-6:] == [1, 2, 3, 4, 5, 6],
       str([(r['sq'], r['held'], r['req']) for r in s.rec[k0:]]))
    while s.drive is not None:
        CS.world(s)
    Q.go(s, 2)
    ck('A7 ... to the coda\'s end: one spawn in all, released, nothing left',
       len([x for x in s.actor_log if x[1] == 'spawn']) == 1 and not [k for k, v in CS.clean(s).items() if not v] and not Q.leftovers(s),
       f'{[k for k, v in CS.clean(s).items() if not v]} {Q.leftovers(s)}')
    # a repel cancelled at its kick with no ending after it: the framework's release stops the actor in the next tick
    s, pl = Q.setup(root)
    assert Q.fight(s)
    stage(s, 'repel5')
    Q.play(s, 'repel', args={'at': 5}, until=lambda s: (s.sc('#sq', 'hr') or 0) >= 129)
    Q.stop(s)
    s.call(f'{H.ROOT_SC}seq/repel/cancel', C0)
    kept = s.actor_on
    CS.world(s)
    rel = (FR / 'mboss/cam/release.mcfunction').read_text(encoding='utf-8')
    ck('A8 the kept actor without an ending: the framework\'s release (which calls char/cine/stop) removes it in the next tick',
       kept and not s.actor_on and not Q.leftovers(s) and 'function rlk:char/cine/stop' in rel, f'{kept} {Q.leftovers(s)}')
    # the coda by itself (a test, a core that cancelled the ending): its own stage, stands and actor
    s, pl = Q.setup(root)
    assert Q.fight(s)
    stage(s, 'ending')
    rec = Q.play(s, 'event')
    sp = [x for x in s.actor_log if x[1] == 'spawn']
    ck('A9 the coda started alone: locked, its own actor (spawn once, play coda), 118 ticks, then nothing left',
       len(sp) == 1 and [x[5].get('clip') for x in s.actor_log if x[1] == 'play'] == ['coda']
       and len([x for x in s.actor_log if x[1] == 'tick']) == LOCK['event'][1] and all(r['held'] for r in rec if 1 <= r['sq'] < LOCK['event'][1])
       and not Q.leftovers(s), f'{len(sp)} {len([x for x in s.actor_log if x[1] == "tick"])} {Q.leftovers(s)}')


# ============================================================================================================ frames
def frames():
    import sheets
    if FRAMES and (FRAMES / 'frames.json').exists():
        rows = json.loads((FRAMES / 'frames.json').read_text(encoding='utf-8'))
        print(f'   frames: {len(rows)} from {FRAMES / "frames.json"}')
    else:
        import shots as SH
        arenas = {lk: SH.Arena(DP, lk) for lk in ('moon', 'crimson')}
        rows = []
        for name in sheets.PLAN:
            for st in (['c'] if name == 'intro' else ['c', 'n', 'e', 's', 'w']):
                out, _p = sheets.frames_of(DP, name, st, arenas, img=False, w=160)
                rows += out
    eye_bad, never = sheets.verdict(rows)
    seqs = sorted({r['seq'] for r in rows})
    stages_ = sorted({r['stage'] for r in rows})
    ck(f'F0 the report covers intro / cs1 / repel60 / repel5 / ending (+ coda) on the stages c n e s w ({len(rows)} frames)',
       seqs == ['cs1', 'ending', 'intro', 'repel5', 'repel60'] and stages_ == ['c', 'e', 'n', 's', 'w'], f'{seqs} {stages_}')
    ck('F1 no lens in a block or a plant, under 0.2 b over the floor or outside the walk disc', not eye_bad,
       str([(r['seq'], r['stage'], r['sq'], r['shot'], r['cell'], r['height'], r['radius']) for r in eye_bad[:5]]))
    ck('F2 every shot shows each of its subjects (on screen, the head unhidden, half the figure or more) in a frame of it',
       not never, str([(k, [(t, v['sx'], v['sy'], v['hidden'], v['vis']) for t, v in fr][:2]) for k, fr in list(never.items())[:4]]))
    shots_n = len({(r['seq'], r['shot']) for r in rows})
    ck('F3 every shot of every table has a frame', shots_n >= sum(len(TR[n].shots) for n in ('intro', 'cs1', 'ending', 'event')) + 2 * len(TR['repel'].shots) - 1,
       str(shots_n))
    # the look point itself: nothing of the arena between the lens and it (plants included)
    blocked = [r for r in rows if r.get('look_hidden')]
    ck('F4 nothing of the arena between a lens and its look point', not blocked, str([(r['seq'], r['stage'], r['sq'], r['shot'], r['look_hidden']) for r in blocked[:5]]))


SECTIONS = [('static', static), ('run', run), ('stages', stages), ('skip', skip), ('life', life), ('actor', actor), ('frames', frames)]
for name_, f_ in SECTIONS:
    if want(name_):
        print(f'== {name_}')
        try:
            f_()
        except Exception:
            print('CRASH in', name_, '- function path:', Q.TRACE[-8:], '- the last check before it:', LAST_CK[0])
            raise
H.summary('TEST_SEQ')

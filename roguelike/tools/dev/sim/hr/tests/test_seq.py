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
# (HF-B, HB-06) every line on a shot close on her: CS0 I10b (690), I12a (790, the silhouette I12 now 820-838), I13 from 838,
# I14 960-980, I14b (980), I15 tracking; CS1 S4b (110), S11 close on her to 654 (S13 from 654); the ending E9b (420), E14b
# (910), E15 from 1038; the coda E4 / E30 / E52 (the opposite stand of the ending's last shot first)
CUTS = {
    'intro': [(0, 1), (76, 2), (110, 1), (170, 2), (250, 1), (320, 2), (410, 1), (460, 2), (536, 1), (666, 2), (690, 1), (750, 2),
              (790, 1), (820, 2), (838, 1), (960, 2), (980, 1), (1040, 2), (1230, 1), (1260, 2), (1290, 1), (1350, 2), (1406, 1)],
    # (round W) cs1: S2 from 9 (S1 holds the lunge), S5 from above 180 + S5b the waiting actor 198, S9b the drink 446
    'cs1': [(0, 1), (9, 2), (34, 1), (84, 2), (110, 1), (180, 2), (198, 1), (220, 2), (276, 1), (340, 2), (380, 1), (446, 2), (500, 1),
            (608, 2), (654, 1)],
    'repel': [(0, 1), (26, 2), (52, 1), (68, 2), (78, 1), (102, 2), (128, 1), (132, 2)],
    'ending': [(0, 1), (50, 2), (94, 1), (118, 2), (150, 1), (190, 2), (204, 1), (240, 2), (276, 1), (314, 2), (338, 1), (378, 2),
               (420, 1), (470, 2), (556, 1), (616, 2), (700, 1), (846, 2), (882, 1), (910, 2), (1038, 1), (1072, 2), (1212, 1)],
    'event': [(4, 2), (30, 1), (52, 2)],
}
LEN = {'intro': 1440, 'cs1': 720, 'lead60': 56, 'repel': 140, 'lead5': 116, 'lead_re': 60, 'ending': 1372, 'event': 120}
LOCK = {'intro': (0, 1440), 'cs1': (0, 720), 'repel': (0, 140), 'ending': (0, 1373), 'event': (0, 118)}
LINE_T = {'intro': {1: 258, 2: 340, 3: 462, 4: 540, 5: 690, 6: 838, 7: 906, 8: 980, 9: 1044, 10: 1140, 11: 1294},
          'cs1': {13: 110, 14: 232, 15: 578, 16: 618},
          'ending': {17: 420, 18: 486, 19: 628, 20: 716, 21: 910, 22: 1082, 23: 1230}}
LINE_SPAN = {1: 54, 2: 60, 3: 60, 4: 84, 5: 130, 6: 64, 7: 44, 8: 44, 9: 90, 10: 70, 11: 62, 13: 52, 14: 40, 15: 36, 16: 36,
             17: 58, 18: 66, 19: 42, 20: 118, 21: 128, 22: 128, 23: 88}
GOLD = 'gold' if api.K.ovl('gold', 0, 1, 1) else 'white'       # the stand-in while lane H2c's glyph is missing
OVL = {'intro': [(0, 'black', 0, 34, 8)], 'cs1': [(0, 'white', 0, 2, 2), (10, GOLD, 0, 1, 2), (642, 'negative', 0, 3, 0), (645, 'pinkwhite', 0, 3, 4),
                           (650, 'red_tint', 0, 4, 20)],
       'repel': [(0, GOLD, 0, 4, 3)],
       'ending': [(0, 'white', 0, 2, 1), (70, GOLD, 0, 1, 2), (190, GOLD, 0, 6, 6), (286, GOLD, 0, 3, 6)],
       'event': [(110, 'black', 6, 16, 0)], 'lead60': [], 'lead5': [], 'lead_re': []}
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
    ck('S2 CS0 has 23 shots, I18 (the skip target) at 1290 on camera A',
       len(CUTS['intro']) == 23 and TR['intro'].shot_at(1290).t == 1290 and TR['intro'].shot_at(1290).cam == 1)
    # (HF-B, HB-03) every locked start makes its stands at their first shots (mboss/cam/spawn_at, the rotation in the NBT),
    # never with the plain spawn at the stage marker
    sp = {n: fn_lines(SQ / n / 'start.mcfunction') for n in ('intro', 'cs1', 'repel', 'ending')}
    ck('S2 each locked start makes both stands with mboss/cam/spawn_at {id:1} / {id:2} (not cam/spawn)',
       all(sum('mboss/cam/spawn_at {id:1}' in ln for ln in ls) == 1 and sum('mboss/cam/spawn_at {id:2}' in ln for ln in ls) == 1
           and not any(ln.endswith('rlk:mboss/cam/spawn') for ln in ls) for ls in sp.values()), str({n: [ln for ln in ls if 'cam/' in ln] for n, ls in sp.items()}))
    reveal()
    ck('S2 every stage of a dynamic sequence clamps its eyes into the walk disc; CS0 (fixed, checked in `frames`) does not',
       all(s.clamp for n in ('cs1', 'repel', 'ending', 'event') for s in TR[n].shots) and not any(s.clamp for s in TR['intro'].shots))
    # rules over the generated files
    files = all_seq_files()
    snd_ids = set((HERE.parent.parent / 'rd/tests/sound_ids.txt').read_text(encoding='utf-8').split()) \
        if (HERE.parent.parent / 'rd/tests/sound_ids.txt').exists() else None
    bad = {k: [] for k in ('negative literal', 'request outside lock', 'core call', 'gamemode / spectate', 'chat', 'sound',
                           'missing function', 'macro', 'upper case id', 'execute subcommand after run')}
    for p in files:
        rel = p.relative_to(SQ).as_posix()[:-11]
        for ln in fn_lines(p):
            body = ln[1:] if ln.startswith('$') else ln
            if re.search(r'scoreboard players (add|remove) \S+ \S+ -', body):
                bad['negative literal'].append((rel, ln))
            if ('#mbCam mb 1' in body and not rel.endswith('/lock')) or ('#mbCam mb' in body and not rel.endswith(('/lock', '/cancel'))):
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
            # (round V: the real server refused `... run as @a ... run playsound`; the simulators ignore an unknown command)
            if re.search(r' run (as|at|if|unless|positioned|rotated|facing|store|in|anchored|align|on) ', body):
                bad['execute subcommand after run'].append((rel, ln))
    for k, v in bad.items():
        ck((f'S3 seq/**: no {k}' if k != 'request outside lock' else 'S3 seq/**: the lock request is set only in lock files (a cancel takes it back)') if k not in ('sound', 'macro') else f'S3 seq/**: {"vanilla sound ids only" if k == "sound" else "a macro line has $(...) and only a macro line"}',
           not v, str(v[:4]))
    ck('S3 the sound list of the vanilla jar was there to check against', snd_ids is not None)
    titles = [(p.relative_to(SQ).as_posix(), ln) for p in files for ln in fn_lines(p) if re.search(r'(^| run )title ', ln)]
    ck('S3 the only title commands of seq/**: the blank actionbar at a start; the skip prompt\'s action bar only when no camera '
       'holds the player', all('actionbar ""' in ln or ('/skip' in r_ and 'unless entity @a[tag=player,tag=rlk_mb_camh]' in ln)
                               for r_, ln in titles), str([x for x in titles if 'actionbar ""' not in x[1]][:3]))
    ck('S3 the hudHold of every locked sequence, each tick', all(SEQ.HUD_HOLD in fn_lines(SQ / n / 'tick.mcfunction') for n in LOCKED)
       and not any(SEQ.HUD_HOLD in fn_lines(SQ / n / 'tick.mcfunction') for n in ('lead60', 'lead5', 'lead_re')))
    # lines: verbatim, at their ticks, their spans. Round V: in a locked sequence a line is typed on the camera's text
    # (mboss_lib.cam_line); the kit's subtitle line only when no camera holds the player
    kit = json.loads((DP / 'tools/mboss_hr_fx_manifest.json').read_text(encoding='utf-8'))
    ok, why = True, []
    held = 'entity @a[tag=player,tag=rlk_mb_camh]'
    for n, tab in LINE_T.items():
        k = tick_files(n)
        for i, t in tab.items():
            sp = LINE_SPAN[i]
            kl = [ln for ln in k.get(t, []) if f'fx/hud/line {{id:{i}}}' in ln]
            if len(kl) != 1 or f'unless {held}' not in kl[0]:
                why.append((n, i, 'kit line', kl))
            typed = [(tt, m.group(1)) for tt in range(t, t + sp) for ln in k.get(tt, [])
                     for m in [re.search(r'data modify storage rlk:mboss camtx\.line set value \{text:\{text:"([^"]*)",color:"#F2D0E8"\},background:(-?\d+)\}', ln)] if m]
            pages = api.LINE_PAGES.get(i) or (api.LINES[i],)
            full = [x for _tt, x in typed if x in pages]
            if [x for x in full] != list(pages) or typed[0][0] != t or len(typed[0][1].replace(' ', '')) > 2:
                why.append((n, i, 'typed', typed[:2], full))
            if not all(any(pg.startswith(x) for pg in pages) for _tt, x in typed):
                why.append((n, i, 'not a prefix of the line', [x for _tt, x in typed][:3]))
            if not any('data modify storage rlk:mboss camtx.line set value {text:"",background:0}' in ln for ln in k.get(t + sp, [])):
                why.append((n, i, 'not cleared at', t + sp))
        allc = [(t, int(m.group(1))) for t, ls in k.items() for ln in ls for m in [re.search(r'fx/hud/line \{id:(\d+)\}', ln)] if m]
        ok &= sorted(allc) == sorted((t, i) for i, t in tab.items())
    ck('S4 each line id at its tick, once (1-11 intro, 13-16 cs1, 17-23 ending): typed on the camera text from that tick (two '
       'syllables first, every step a prefix, each page of api.LINE_PAGES whole), cleared at the end of its span; the kit\'s '
       'subtitle line only when no camera holds the player', ok and not why, str(why[:4]))
    ck('S4 the lines are api.LINES verbatim, their spans the design\'s',
       all(api.LINE_AT[i][2] == sp for i, sp in LINE_SPAN.items()) and len(api.LINES) == 25
       and all(kit['lines'][str(i)]['text'] == api.LINES[i] and kit['lines'][str(i)]['on_screen'] == sp for i, sp in LINE_SPAN.items())
       and all(' '.join(api.LINE_PAGES.get(i) or (api.LINES[i],)) == api.LINES[i] for i in api.LINES))
    # round V (v_brief VC 1-3, 5, 8): the camera rules in the tables and the generated files
    for n in LOCKED:
        tr = TR[n]
        segs = tr.segments()
        ck(f'S6 {n}: every segment lasts 1..{CAM.SEG_MAX} ticks ({len(segs)} placements after the first keyframes)',
           all(1 <= at - t <= CAM.SEG_MAX and 0 < dur <= CAM.SEG_MAX for _nm, _c, t, at, dur, _k in segs), str([x for x in segs if not 1 <= x[3] - x[2] <= 59][:3]))
        ck(f'S6 {n}: every shot lasts at least {CAM.PRE} ticks (the idle camera settles) and its last move ends before the next cut',
           all(b.t - a.t >= CAM.PRE and a.last_motion() < b.t for a, b in zip(tr.shots, tr.shots[1:])))
        cl = tr.lines()
        dur_err = []
        for sh in tr.shots:
            cur = 0
            if sh.t > 0 and not (any('teleport_duration:0}' in x for x in cl.get(sh.t - 3, [])) and any('mboss/cam/fix' in x for x in cl.get(sh.t - 2, []))):
                dur_err.append((sh.name, 'no preparation'))
            for kf in sh.keys:
                if kf.dur != cur:
                    if not any(f'rlk_mb_cam{sh.cam},limit=1] {{teleport_duration:{kf.dur}}}' in x for x in cl.get(kf.t - 1, [])):
                        dur_err.append((sh.name, kf.t, kf.dur))
                    cur = kf.dur
                if sum('mboss/cam/fix' in x and f'rlk_mb_cam{sh.cam}' in x for x in cl.get(kf.t, [])) < 1:
                    dur_err.append((sh.name, kf.t, 'no placement'))
        ck(f'S6 {n}: each cut prepared (duration 0 three ticks ahead, the placement two ticks ahead), each segment\'s duration set '
           'the tick before its placement', not dur_err, str(dur_err[:4]))
        chase = {t for sh in tr.shots for t0, t1, *_r, kind in sh.moves if kind == 'chase' for t in range(t0, t1)}
        placed = sorted(t for t, ls in cl.items() if any('mboss/cam/fix' in x for x in ls))
        runs = [t for t in placed if t not in chase and t - 1 in placed and t + 1 in placed and (t - 1) not in chase]
        ck(f'S6 {n}: no placement on three ticks running outside a chase ({len(placed)} placement ticks, {len(chase)} of a chase)',
           not runs, str(runs[:6]))
    for n in ('intro', 'cs1'):
        si = fn_lines(SQ / n / 'skipin.mcfunction')
        ck(f'S7 {n}: the skip input is the jump key (never Shift), the core\'s Shift input rests (#skip hr -1), the prompt names Space',
           any('predicate rlk:in_jump' in x for x in si) and not any('in_sneak' in x for x in si) and si[0] == 'scoreboard players set #skip hr -1'
           and any('Space 길게' in x and '건너뛰기' in x for x in si) and not any('Shift' in x for x in si), str(si[:2]))
        tk = fn_lines(SQ / n / 'tick.mcfunction')
        ck(f'S7 {n}: tick calls skipin before its timeline and stops the tick of a skip there',
           f'function rlk:boss/scarlet/seq/{n}/skipin' in tk and tk.index(f'function rlk:boss/scarlet/seq/{n}/skipin') < next(i for i, x in enumerate(tk) if '/k/' in x or '/kb/' in x))
    now = 'execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/rig/follow_now'
    for rel in ('intro/skip', 'cs1/skip', 'cs1/start', 'repel/start', 'ending/start'):
        ls = fn_lines(SQ / f'{rel}.mcfunction')
        tp_i = [i for i, x in enumerate(ls) if re.search(r'(seq/[a-z0-9]+/m/(mark|drop|lie)$)|( run tp @s ~ ~ ~$)', x)]
        ck(f'S8 {rel}: her model follows an instant move of her body in the same tick (rig/follow_now at the body after it and '
           'after her turn)', tp_i and now in ls and ls.index(now) > tp_i[-1]
           and not any('rotate @s' in x for x in ls[ls.index(now):ls.index(now) + 1]), str(tp_i))
    # music, the title, the look request, the rig looks at their ticks
    def has(n, t, frag):
        return any(frag in ln for ln in tick_files(n).get(t, []))
    ck('S5 music 1 at intro 1420, music 2 at cs1 676, music 3 at ending 420',
       has('intro', 1420, 'music/set {ph:1}') and has('cs1', 676, 'music/set {ph:2}') and has('ending', 420, 'music/set {ph:3}'))
    ck('S5 the title 홍련 / 월하곡 at the draw (intro 1356)', has('intro', 1356, 'mboss/title {title:"홍련",sub:"월하곡"'))
    ck('S5 the crimson look request and the rig\'s P2 accents at cs1 660', has('cs1', 660, '#hrLook hr 2') and has('cs1', 660, 'rig/look/phase/p2'))
    ck('S5 intro_end starts at 1290 (the skip target); the rock and the props go at 1052',
       has('intro', 1290, 'rig/play/intro_end') and has('intro', 1052, 'rig/look/props/none'))


def reveal():
    """(HF-B, HB-07) I18 under the brim, from her own points (her_tracks.json: intro_end head, brim) and the built shot: her
    eyes behind the brim from 1290 until the brim lift (intro_end 40-56 = #sq 1330-1346), seen once it has lifted; the mouth
    under the brim edge while she speaks; the lens >= 0.3 b from the brim."""
    T = json.loads((DP / 'tools/dev/sim/hr/cine/her_tracks.json').read_text())
    c, BR = T['clips']['intro_end'], T['brim_r']

    def v(op, a, b):
        return [op(x, y) for x, y in zip(a, b)]

    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))

    def unit(a):
        n = math.sqrt(dot(a, a))
        return [x / n for x in a]
    tr = TR['intro']
    eyes, mouth, near_b = {}, {}, []
    for t in range(api.SKIP_T, 1350):
        ct = t - api.SKIP_T
        root, head, (ctr, n) = c['root'][ct], c['head'][ct], c['brim'][ct]
        eye_pt = tr.shot_at(t).at(t)[0]
        a = math.radians(root[3])
        fw, rt = (math.sin(a), math.cos(a)), (math.cos(a), -math.sin(a))
        L = [root[0] + eye_pt[1] * rt[0] + eye_pt[3] * fw[0], root[1] + eye_pt[2], root[2] + eye_pt[1] * rt[1] + eye_pt[3] * fw[1]]
        up = unit(n)
        F = [fw[0], 0.0, fw[1]]
        fwd = unit(v(lambda x, y: x - y, F, [u * dot(F, up) for u in up]))

        def hidden(P):
            d = v(lambda x, y: x - y, P, L)
            den = dot(d, up)
            if abs(den) < 1e-9:
                return False
            k = dot(v(lambda x, y: x - y, ctr, L), up) / den
            return 0 < k < 1 and math.dist([l + x * k for l, x in zip(L, d)], ctr) < BR
        # the face of the skin (8 x 8 px, 1 px = 1/16 b): the eyes rows 4-5 (the head's centre to 0.125 b under it), the mouth
        # rows 6-7: hidden = the lowest eye row behind the brim; seen = the eyes' middle in sight
        eyes[t] = (hidden([h + 0.25 * f - 0.125 * u for h, f, u in zip(head, fwd, up)]),
                   hidden([h + 0.25 * f - 0.06 * u for h, f, u in zip(head, fwd, up)]))
        mouth[t] = hidden([h + 0.25 * f - 0.19 * u for h, f, u in zip(head, fwd, up)])
        w = v(lambda x, y: x - y, L, ctr)
        hh = dot(w, up)
        near_b.append(math.hypot(hh, max(0.0, math.dist(w, [u * hh for u in up]) - BR)))
    lift0, lift1 = api.SKIP_T + api.ev('intro_end', 'brim'), api.SKIP_T + api.ev('intro_end', 'brim') + 16
    ck(f'F3 I18 (HB-07): her eyes behind her brim from {api.SKIP_T} until the brim lifts ({lift0})',
       all(eyes[t][0] for t in range(api.SKIP_T, lift0)), str([t for t in range(api.SKIP_T, lift0) if not eyes[t][0]][:6]))
    ck(f'F3 ... and seen once it has lifted ({lift1}-1349)', not any(eyes[t][1] for t in range(lift1, 1350)), str([t for t in range(lift1, 1350) if eyes[t][1]]))
    ck('F3 ... her mouth under the brim edge while she speaks before the lift (>= 20 ticks of 1294-1329)',
       sum(not mouth[t] for t in range(1294, lift0)) >= 20, str(sum(not mouth[t] for t in range(1294, lift0))))
    ck('F3 ... the lens >= 0.3 b from the brim over the whole shot', min(near_b) >= 0.3, f'{min(near_b):.3f}')


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
                # the first keyframe of every shot: two ticks before its cut the camera (as the CLIENT has it) looks from the
                # table's eye along the grid rotation nearest its look point, and stands still there until the cut
                bad, unset = [], []
                for shot in TR[sn].shots:
                    if shot.t - 1 > max(by):
                        continue
                    r = by.get(shot.t - 1) if shot.t > 0 else by.get(1)
                    if r is None or not r.get('cam') or r['cam'].get(shot.cam) is None:
                        unset.append(shot.name)
                        continue
                    pos, rot = r['cam'][shot.cam]
                    fr = frames_of(by.get(max(shot.t - 2, 0), r))
                    we, wl = CAM.to_world(shot.eye, fr), CAM.to_world(shot.look, fr)
                    lifted = shot.clamp and shot.eye[0] in ('ST', 'ST2') and shot.eye[2] < CAM.LOW and abs(pos[1] - (201.0 + SEQ.LIFT_TO)) < 0.2
                    if lifted:
                        we = (we[0], 201.0 + SEQ.LIFT_TO, we[2])
                    y, p = CAM.yaw_pitch(we, wl)
                    lead = TR[sn].lead(shot.t - 2, shot.t) if shot.t > 0 else None
                    tol_p, tol_r = (0.35, 8.0) if lead else (0.03, CAM.GRID / 2 + 0.05)
                    if not near(pos, we, tol_p) or not CS.on_grid(rot) or (math.dist(we, wl) > 0.2 and abs(p) < 88
                                                                         and (ang(rot[0], y) > tol_r or abs(rot[1] - p) > tol_r)):
                        bad.append((shot.t, shot.name, [round(v, 2) for v in pos], [round(v, 2) for v in we], [round(v, 2) for v in rot], round(y, 1), round(p, 1)))
                ck(f'R3 {tag}: before every cut the camera\'s viewpoint is the table\'s eye, its rotation the grid step nearest the '
                   'look point', not bad and not unset, f'{bad[:3]} {unset[:3]}')
            else:
                ck(f'R2 {tag}: never locked', not any(r['req'] or r['held'] for r in by.values()))
            # overlays / signals
            ov = [(t, a['g'], int(a['in']), int(a['hold']), int(a['out'])) for t in sorted(by) for c, a in by[t]['kit'] if c == 'hud/ovl']
            if key != 'repel5':
                ck(f'R4 {tag}: the overlays of the design at their ticks', ov == OVL[sn], str(ov))
            sg = [(t, by[t]['sig']) for t in sorted(by) if by[t]['sig']]
            ck(f'R4 {tag}: the signals {SIGS[sn]}', sg == SIGS[sn], str(sg))
            ls = [(t, int(a['id'])) for t in sorted(by) for c, a in by[t]['kit'] if c == 'hud/line']
            if sn in LOCK and key != 'repel5':
                # round V (VC 10): a held run shows every line on the live camera's text, never the kit's subtitle
                tbad = []
                for i, t in LINE_T.get(sn, {}).items():
                    sp = LINE_SPAN[i]
                    pages = api.LINE_PAGES.get(i) or (api.LINES[i],)
                    seen = [by[tt]['text'] for tt in range(t, t + sp) if tt in by]
                    if not seen or not seen[0] or [x for j, x in enumerate(seen) if x in pages and (j == 0 or seen[j - 1] != x)] != list(pages) \
                            or not all(x and any(pg.startswith(x) for pg in pages) for x in seen) or by[t + sp]['text'] not in ('', None) \
                            or (t - 1 in by and by[t - 1]['text'] not in ('', None)):
                        tbad.append((i, t, seen[:2], seen[-1:], by[t + sp]['text']))
                ck(f'R4 {tag}: every line typed on the live camera\'s text for its span (each page whole), gone after it; the kit\'s '
                   'subtitle line never called while held', not tbad and not ls, f'{tbad[:3]} {ls[:3]}')
                other = [t for t in sorted(by) if by[t]['text'] and not any(tt <= t < tt + LINE_SPAN[i] for i, tt in LINE_T.get(sn, {}).items())]
                ck(f'R4 {tag}: no text outside the line spans', not other or sn == 'event', str(other[:5]))
            else:
                ck(f'R4 {tag}: the lines at their ticks', sorted(ls) == sorted((t, i) for i, t in LINE_T.get(sn, {}).items())
                   or sn == 'event' or key == 'repel5', str(ls))
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
                t0, t1 = LOCK[sn]
                last = min(t1 - 1, max(by))
                # round V (VC 3): cuts between settled cameras. The idle camera has stood still at the shot's first keyframe
                # for 2 ticks (the client's interpolated pose = the server's, no step left) when it goes live; the first
                # frame of the new shot is that place (a move that starts at the cut has made at most its first step)
                glide, margins = [], []
                for sh in TR[sn].shots:
                    if sh.t == 0 or sh.t - 1 not in by or sh.t > last:
                        continue
                    a, b, c = by.get(sh.t - 2), by[sh.t - 1], by[sh.t]
                    st = b['cl'][sh.cam]
                    m = 0
                    for k in range(1, 12):
                        q = by.get(sh.t - k)
                        if q is None or q['cl'][sh.cam] is None or q['cl'][sh.cam][2] != 0 or q['cl'][sh.cam][:2] != st[:2]:
                            break
                        m += 1
                    margins.append(m)
                    first = [kf for kf in sh.keys if kf.t == sh.t]
                    step = 1.0 / first[0].dur if first else 0.0
                    moved = math.dist(c['cl'][sh.cam][0], st[0])
                    reach = math.dist(c['ent'][sh.cam][0], st[0]) * step + 1e-6
                    if (st[2] != 0 or m < 2 or st[:2] != (b['ent'][sh.cam][0], b['ent'][sh.cam][1]) or c['con'] != sh.cam or moved > reach
                            or (a is not None and a['con'] == sh.cam)):
                        glide.append((sh.t, sh.name, st[2], m, round(moved, 3), round(reach, 3), c['con']))
                ck(f'R9 {tag} (VC 3): every cut goes to a camera that has stood settled at its first keyframe for 2 ticks or more; '
                   f'the first frame is that place (settle margins {sorted(set(margins))} t)', not glide, str(glide[:4]))
                free = [t for t in sorted(by) if 1 <= t <= last and by[t]['held'] and by[t]['con'] != by[t]['live']]
                ck(f'R11 {tag} (VC 6): the client looks through the live camera on every held tick', not free, str(free[:8]))
                # round V (VC 7): a spectator sees every invisible LIVING entity as a ghost. In a locked tick the only living
                # entities are her body (a husk: its texture is blank in the pack, tools/build_blank_tex.py) and the avatar (a
                # mannequin: its skin is blank while the actor stands in for it, char/cine/blank); never an armour stand
                import importlib
                BT = importlib.import_module('build_blank_tex')
                blank = {'husk': any(f.endswith('zombie/husk.png') for f in BT.FILES),
                         'mannequin': any(f.endswith('skin/blank.png') for f in BT.FILES)
                         and any('profile.texture set value "rlk:skin/blank"' in x for x in fn_lines(F / 'char/cine/blank.mcfunction'))
                         and any('rlk:char/cine/blank' in x for x in fn_lines(F / 'char/cine/hide.mcfunction'))}
                ghosts = sorted({x for t in by if 1 <= t <= last and by[t]['held'] for x in by[t].get('living', []) if not blank.get(x[0])})
                kinds = sorted({x[0] for t in by if 1 <= t <= last and by[t]['held'] for x in by[t].get('living', [])})
                ck(f'R14 {tag} (VC 7): no living entity a spectator could see a ghost of on any held tick (living types present: '
                   f'{kinds}, each with a blank texture)', not ghosts, str(ghosts))
                rg = [t for t in sorted(by) if t <= last and by[t].get('rig') and by[t].get('body1') and math.dist(by[t]['rig'], by[t]['body1'][0]) > 1e-6]
                ck(f'R13 {tag} (VC 8): her model stands where her body stands when every tick is over', not rg, str(rg[:8]))
            if sn == 'event':
                ev_black = [(t, i, h) for t, g, i, h, _o in ov if g == 'black']
                rel = LOCK['event'][1]
                ck(f'R10 {tag} (HB-05): the coda\'s black is opaque at least 2 ticks before the hand-back (E{rel}) and still held there',
                   len(ev_black) == 1 and ev_black[0][0] + ev_black[0][1] <= rel - 2 and ev_black[0][0] + ev_black[0][1] + ev_black[0][2] >= rel + 2,
                   str(ev_black))
            cm = [r['cmds'] for r in by.values()]
            print(f'   {tag}: {len(by)} ticks, commands per tick avg {sum(cm) / len(cm):.0f} / max {max(cm)} (the sequence\'s own files)')
            # (round V: a start that places her instantly also runs the rig's follow, 36 commands, inside the sequence's own
            # call now - before it ran later in the same tick from rig/tick, in the wrong place)
            ck(f'R6 {tag}: at most 440 commands of its own in a tick', max(cm) <= 440, str(max(cm)))
        if key in ('intro', 'cs1', 'repel60', 'ending'):
            # round V (VC 1): what reached the client. Every rotation ever sent for a camera is on the 360 / 256 grid (the
            # byte packet is then exact and agrees with the entity's place); every interpolation it ran lasted <= 59 ticks
            off = [x for x in s.all_sent if not CS.on_grid(x[1])]
            long_ = [x for x in s.all_segs if x[1] > CAM.SEG_MAX]
            n_seg = len(s.all_segs)
            ck(f'R12 {key} (VC 1): every rotation sent for a camera lies on the 1.40625-degree grid; no interpolation longer than '
               f'{CAM.SEG_MAX} t ({len(s.all_sent)} rotations sent, {n_seg} moves interpolated by the client)', not off and not long_ and n_seg > 0 and len(s.all_sent) > 10,
               f'{off[:3]} {long_[:3]}')
        if key in ('intro', 'cs1', 'repel60', 'repel5', 'ending'):
            # (HF-B, HB-04 / HB-06) the framing of every held tick through the built cameras (hr/h2/framing.py: her rig's
            # points from her_tracks.json on her body, the actor's head from lane H3's manifest)
            import framing as FR
            rows = FR.analyse(DP, key, recs=parts)
            emp = FR.spans(FR.empty_ticks(rows))
            ck(f'F1 {key} (HB-04): no tick of a shot with a figure subject shows none of its subjects', not emp, str(emp[:4]))
            far = FR.spans(FR.far_lines(rows))
            ck(f'F2 {key} (HB-06): every tick of every line on a shot close on her (her head in the frame\'s middle, the lens <= '
               f'{FR.CLOSE} b from it)', not far, str(far[:4]))
            over = FR.spans(FR.face_under_text(rows, L))
            ck(f'F4 {key} (VC 10): on no tick of a line does the text box lie over her face', not over, str(over[:6]))
            # (round W, WC 3) a shot of both figures: both heads whole inside the 16 : 9 picture at a field of view of 70, 90
            # and 110 on every tick, never under the line box; a wide one (Shot.full) head to foot
            tf = FR.two_figure_bad(rows, L)
            n2 = sorted({(r['seq'], r['shot']) for r in rows if 'her' in r['sub'] and 'actor' in r['sub']})
            ck(f'F5 {key} (WC 3): both figures inside the picture at 70 / 90 / 110 on every tick of its {len(n2)} two-figure shots',
               not tf and (n2 or key in ('intro',)), str([(r['seq'], r['shot'], r['sq'], fov, w) for r, fov, w in tf[:6]]))
            # (round W, WC 7) the stray line: on every held tick every text display that shows something rides the LIVE camera
            # (the idle one stands somewhere in the world, its billboard text in the live picture); while a line plays the
            # live camera shows it
            stray, shown = [], []
            for sn_, by_ in parts.items():
                lt = {r['sq'] for r in rows if r['seq'] == sn_ and r['line'] and not r['gone']}
                stray += [(sn_, t, by_[t]['live'], by_[t].get('texts')) for t in sorted(by_) if by_[t]['held']
                          and any(c != by_[t]['live'] for c, _tg, _x in by_[t].get('texts', []))]
                if sn_ != 'event':          # (the coda's lines need the core's branch #hrEv, which this run does not set)
                    shown += [(sn_, t) for t in sorted(lt) if t in by_ and by_[t]['held'] and not by_[t].get('text')]
            ck(f'X1 {key} (WC 7): no text on any camera but the live one on any held tick; the line on the live camera on every '
               'line tick', not stray and not shown, f'{stray[:3]} {shown[:5]}')
            if key == 'cs1':
                petal_checks(parts['cs1'], rows, L)
            if key == 'ending':
                n_line = sum(1 for r in rows if r['line'] and not r['gone'])
                ck('F2 ... the ending\'s lines 17-23 and the coda\'s 24 / 25 (while she is there) were measured', n_line >= 600, str(n_line))
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


def petal_checks(by, rows, L):
    """(round W, WC 2; the user: the petal too small, cut hanging in the air) the S11 petal on the live camera's picture at a
    field of view of 90 (the user's): it enters from above and falls with a sway for >= 1.5 s before the cut, is still
    falling at the cut, is >= 60 px tall at 1080p there, her blade passes through it on that tick, its halves fall on apart;
    no petal card over her face on a line tick (any field of view: the projection scales alike)."""
    import framing as FR
    tracks = json.loads((DP / 'tools/dev/sim/hr/cine/her_tracks.json').read_text())['clips']
    tag, ta, tb = SEQ.PETAL[2], SEQ.PETAL[2] + '_a', SEQ.PETAL[2] + '_b'
    cut, fall, art = SEQ.CUT_T, SEQ.PETAL_FALL, SEQ.PETAL_ART
    tv = math.tan(math.radians(45))

    def prop(t, tg):
        return next((p for p in by.get(t, {}).get('props', []) if tg in p['tags']), None)

    def scr(t, p):
        """(sx, sy in -1..1, depth, height px at 1080p) of a prop card on the live camera's picture at FOV 90."""
        eye, rot = by[t]['cam'][by[t]['live']]
        f, r, u = CS_basis(rot)
        d = [p['pos'][i] - eye[i] for i in range(3)]
        z = sum(d[i] * f[i] for i in range(3))
        if z <= 0.05:
            return None
        return (sum(d[i] * r[i] for i in range(3)) / (z * tv * 16 / 9), sum(d[i] * u[i] for i in range(3)) / (z * tv), z,
                art[1] * p['scale'] / (z * tv) * 540)
    ys = [(t, prop(t, tag)) for t in range(cut - fall, cut + 1)]
    ok_all = all(p is not None for _t, p in ys)
    dy = [ys[i + 1][1]['pos'][1] - ys[i][1]['pos'][1] for i in range(len(ys) - 1)] if ok_all else []
    ck(f'P1 the petal falls from {cut - fall} to the cut at {cut}: down every tick ({min(dy, default=0):.3f}..{max(dy, default=0):.3f} b / t), '
       f'still falling at the cut', ok_all and dy and max(dy) < -0.03 and dy[-1] < -0.03, str(dy[:4]))
    vis = [t for t, p in ys if p and scr(t, p) and abs(scr(t, p)[0]) < 1 and abs(scr(t, p)[1]) < 1]
    first = scr(vis[0], prop(vis[0], tag)) if vis else None
    ck(f'P2 ... in the picture (FOV 90) for {len(vis)} t >= 30 (1.5 s) before the cut, entering from above (first seen at sy '
       f'{first[1] if first else None})', len(vis) >= 30 and vis[-1] == cut and first is not None and first[1] > 0.6 and all(vis[i + 1] == vis[i] + 1 for i in range(len(vis) - 1)))
    sx = [scr(t, prop(t, tag))[0] for t in vis]
    ck(f'P2 ... with a visible sway (the picture x of its centre turns {sum(1 for i in range(1, len(sx) - 1) if (sx[i] - sx[i - 1]) * (sx[i + 1] - sx[i]) < 0)} times, '
       f'{(max(sx) - min(sx)) * 960 if sx else 0:.0f} px wide)', sx and (max(sx) - min(sx)) * 960 >= 40
       and sum(1 for i in range(1, len(sx) - 1) if (sx[i] - sx[i - 1]) * (sx[i + 1] - sx[i]) < 0) >= 2)
    pc = prop(cut, tag)
    h = scr(cut, pc)[3] if pc and scr(cut, pc) else 0
    ck(f'P3 ... at the cut it is {h:.0f} px tall at 1080p, FOV 90 (>= 60; {h * math.tan(math.radians(45)) / math.tan(math.radians(55)):.0f} at 110)', h >= 60)
    rc = by[cut]
    hilt, tip = FR.her_point(tracks, 'cs1', rc, 'hilt'), FR.her_point(tracks, 'cs1', rc, 'tip')
    dist = seg_dist(pc['pos'], hilt, tip) if pc and hilt and tip else 9
    ck(f'P4 ... her blade passes through it on the cut tick ({dist:.3f} b from its centre to the blade, <= 0.15)', dist <= 0.15)
    ha = [prop(cut + k, ta) for k in range(1, SEQ.HALF_T)]
    hb = [prop(cut + k, tb) for k in range(1, SEQ.HALF_T)]
    okh = all(ha) and all(hb)
    da = [ha[i + 1]['pos'][1] - ha[i]['pos'][1] for i in range(len(ha) - 1)] if okh else [0]
    db = [hb[i + 1]['pos'][1] - hb[i]['pos'][1] for i in range(len(hb) - 1)] if okh else [0]
    gap = [math.dist(a['pos'], b['pos']) for a, b in zip(ha, hb)] if okh else [0]
    ck(f'P5 the halves fall on (each down every tick until the floor) and apart ({gap[0]:.2f} -> {gap[-1]:.2f} b)',
       okh and all(v < 0 or abs(a['pos'][1] - 201.0 - SEQ.HALF_FLOOR) < 0.02 for v, a in zip(da, ha[1:])) and all(v < 0 or abs(b['pos'][1] - 201.0 - SEQ.HALF_FLOOR) < 0.02 for v, b in zip(db, hb[1:]))
       and gap[-1] > gap[0] + 0.3 and prop(cut + SEQ.HALF_T, ta) is None and prop(cut + 1, tag) is None)
    # no petal card over her face while a line plays
    over = []
    for r in rows:
        if not r['line'] or r['seq'] != 'cs1' or r['her'] is None or r['her'][0] is None:
            continue
        t = r['sq']
        hx, hy, hz = FR.at_fov(r['her'], 90)
        hr = FR.HEAD_R / (hz * tv)
        for p in by[t].get('props', []):
            q = scr(t, p)
            if q is None:
                continue
            pw, ph = art[0] * p['scale'] / (q[2] * tv) / 2, art[1] * p['scale'] / (q[2] * tv) / 2
            if abs(q[0] * 16 / 9 - hx * 16 / 9) < pw + hr and abs(q[1] - hy) < ph + hr and q[2] < hz:
                over.append((t, p['tags']))
    ck('P6 no petal card lies over her face (before it) on any line tick of CS1', not over, str(over[:4]))


def CS_basis(rot):
    y, p = math.radians(rot[0]), math.radians(rot[1])
    f = (-math.sin(y) * math.cos(p), -math.sin(p), math.cos(y) * math.cos(p))
    r = (-math.cos(y), 0.0, -math.sin(y))
    u = (r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0])
    return f, r, u


def seg_dist(p, a, b):
    ab = [b[i] - a[i] for i in range(3)]
    u = max(0.0, min(1.0, sum((p[i] - a[i]) * ab[i] for i in range(3)) / max(1e-9, sum(v * v for v in ab))))
    return math.dist(p, [a[i] + ab[i] * u for i in range(3)])


# ============================================================================================================ stages
def stages():
    import sheets
    import shots as SH
    arenas = {lk: SH.Arena(DP, lk) for lk in ('moon', 'crimson')}
    for key in ('intro', 'cs1', 'repel60', 'ending'):
        for st in (('c',) if key == 'intro' else ('c', 'n', 'e', 's', 'w')):
            s, by = sheets.run(DP, key, st)
            eye_bad, her_bad, f5_bad, fwd = [], [], [], None
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
                        # round V (VC 2): the camera ENTITY (as the client has it this tick) is in air and the client's 4-b
                        # pull-back behind it meets no block - the picture is taken from the viewpoint, not from a wall
                        ep, er = r['cl'][r['live']][:2]
                        hit = SH.f5_clear(ar, ep, er)
                        if hit:
                            f5_bad.append((sn, t, TR[sn].shot_at(t).name, [round(v, 2) for v in ep], hit))
                    (bx, byy, bz), _yaw = r['body']
                    rad = math.hypot(bx - 880.0, bz - 8.0)
                    c1, c2 = ar.cell((bx, byy + 0.01, bz)), ar.cell((bx, byy + 1.5, bz))
                    if rad > 25.0 + 1e-6 or byy < 201.0 - 1e-6 or c1[1] == SH.SOLID or c2[1] == SH.SOLID or 'barrier' in c1[0] + c2[0]:
                        her_bad.append((sn, t, [round(v, 2) for v in (bx, byy, bz)], round(rad, 2), c1[0]))
            want_fwd = 'her' if st == 'c' else 'centre'
            if key == 'intro':
                fwd = want_fwd                         # CS0's stage is fixed (api.CS0_P0, toward her seat)
            shots_bad = sorted({(x[0], x[2]) for x in f5_bad})
            ck(f'G5 {key} stage {st} (VC 2): on every locked tick the camera entity is in air and the 4-block line back to the '
               f'viewpoint is free of blocks', not f5_bad, f'{len(f5_bad)} ticks, shots {shots_bad[:6]}, first {f5_bad[:2]}')
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
    """What a skip must reproduce (v_brief VC 8): her place and yaw, where her MODEL stands (the rig's follow), the live camera
    and the picture the client has through it, the texts, the props and the seat rock, the stage, the actor's clock, the lock.
    (The idle camera is prepared again before the next cut.)"""
    b = H.body_of(s)
    live = s.sc('#mbCamId', 'mb')
    v = CS.client_view(s)
    cam = next((e for e in s.ents if e.alive and f'rlk_mb_cam{live}' in e.tags), None)
    tx = [next((x.data.get('text') for x in s.ents if x.alive and t in x.tags and cam is not None and x.data.get('riding') == cam.id), None)
          for t in (CS.LINE_TAG, CS.HINT_TAG)]
    return dict(body=[round(v_, 2) for v_ in b.pos], yaw=round(b.rot[0] % 360, 1), live=live,
                rig=None if s.rig_pos is None else [round(v_, 2) for v_ in s.rig_pos],
                view=None if v is None else ([round(x, 2) for x in v[0]], [round(x, 2) for x in v[1]]),
                on=CS.client_on(s) is not None and f'rlk_mb_cam{live}' in CS.client_on(s),
                text=tx[0], hint=tx[1], cav=s.sc('#cavT', 'cine'), sq=s.sc('#sq', 'hr'),
                stage=[(sorted(e.tags)[0], [round(x, 2) for x in e.pos], round(e.rot[0], 1)) for e in s.ents
                       if e.alive and e.etype == 'marker' and ('rlk_hr_stage' in e.tags or 'rlk_hr_stage2' in e.tags)],
                props=sorted(sorted(e.tags) for e in s.ents if e.alive and ('rlk_hr_sqp' in e.tags or 'rlk_hr_deco_seat_rock' in e.tags)),
                held=CS.held(s))


def lines_from(rec, name, t0):
    """[(tick, text)] of the camera text from t0 on (each change once)."""
    out, last = [], None
    for r in rec:
        if r['seq'] == name and r['sq'] >= t0 and r.get('text') != last:
            last = r.get('text')
            out.append((r['sq'], last))
    return out


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
        ck(f'K0 {name}: in the full run at {to + 4} her model stands at her body and the client is on the live camera',
           ref['rig'] == ref['body'] and ref['on'] and ref['view'] is not None, str(ref))
        while s.drive is not None:                      # the reference run goes on to its end
            CS.world(s)
        ref_end = state(s)
        ref_tail = lines_from(s.rec[k0:], name, to)
        ck(f'K0 {name}: the full run has lines after {to} (the check below is not empty)', len([x for x in ref_tail if x[1]]) >= 1, str(ref_tail))
        hint0 = [r['hint'] for r in s.rec[k0:] if r['seq'] == name]
        ck(f'K5 {name}: the prompt 「⊙ 건너뛰기 · Space 길게」 on the live camera\'s hint text through the window {lo}..{hi}, nothing before '
           'or after it; never the word Shift',
           all((('건너뛰기' in (h or '') and 'Space 길게' in (h or '')) == (lo <= t <= hi)) and 'Shift' not in (h or '') for t, h in enumerate(hint0)),
           str([(t, h) for t, h in enumerate(hint0) if (('건너뛰기' in (h or '')) != (lo <= t <= hi))][:4]))
        for at in sorted({lo, lo + 37, (lo + hi) // 2, hi - 51, hi - api.SKIP_HOLD}):
            s, pl = world(name)
            Q.play(s, name, until=lambda s: (s.sc('#sq', 'hr') or 0) >= at)
            n0 = len(s.rec)
            if at + 80 < hi:
                # Shift is not the skip any more (it only makes the game drop the camera, which post gives back): nothing happens
                pl.data['sneak'] = True
                Q.go(s, 30)
                pl.data['sneak'] = False
                ck(f'K6 {name} at {at}: Shift held 30 ticks skips nothing; the client stays on the live camera',
                   s.sc('#sq', 'hr') == at + 30 and all(r['con'] == r['live'] for r in s.rec[n0:]) and not any(c == 'hud/ovl' and a.get('g') == 'black' for r in s.rec[n0:] for c, a in r['kit']),
                   f"{s.sc('#sq', 'hr')}")
                pl.data['keys'] = {'jump'}
                Q.go(s, api.SKIP_HOLD - 6)
                pl.data['keys'] = set()
                Q.go(s, 2)
                ck(f'K6 {name} at {at}: the jump key released before {api.SKIP_HOLD} ticks: no skip, the count starts again',
                   s.sc('#sq', 'hr') == at + 30 + api.SKIP_HOLD - 4 and (s.sc('#sq_sk', 'hr') or 0) == 0)
            t_press = s.sc('#sq', 'hr')
            pl.data['keys'] = {'jump'}
            m0 = len(s.rec)
            for _ in range(api.SKIP_HOLD + 3):
                CS.world(s)
                if (s.sc('#sq', 'hr') or 0) == to - 1:
                    break
            pl.data['keys'] = set()
            held_t = len(s.rec) - m0
            ov = [(a['g'], int(a['in']), int(a['hold']), int(a['out'])) for r in s.rec[m0:] for c, a in r['kit'] if c == 'hud/ovl'][-1:]
            ck(f'K1 {name} at {t_press}: the jump key held {api.SKIP_HOLD} ticks skips (#sq = {to - 1}), under the black 0 / 20 / 6',
               s.sc('#sq', 'hr') == to - 1 and held_t == api.SKIP_HOLD and ov == [('black', 0, 20, 6)], f"{s.sc('#sq', 'hr')} {held_t} {ov}")
            sk = state(s)
            ck(f'K1 {name} at {t_press}: in the tick of the skip her model stands at her body (no empty mark), the prompt and the line are gone, '
               'the client is on the new live camera', sk['rig'] == sk['body'] and sk['hint'] in ('', None) and sk['text'] in ('', None) and sk['on'],
               str(sk))
            while s.drive is not None and (s.sc('#sq', 'hr') or 0) < to + 4:
                CS.world(s)
            got = state(s)
            ck(f'K1 {name} skipped at {t_press}: the state at {to + 4} = the uninterrupted run\'s (her place, yaw and model, the live camera '
               f'and the client\'s picture, the texts, the props, the stage, the actor\'s clock, still locked)', got == ref,
               f'{[(k, got[k], ref[k]) for k in got if got[k] != ref[k]]}')
            kit_lines = [(r['sq'], a) for r in s.rec[m0:] for c, a in r['kit'] if c == 'hud/line']
            ck(f'K1 {name} skipped at {t_press}: no subtitle line is ever drawn over the black (the kit\'s title line is not called in a '
               'held run; the camera text is in the world, under the overlay)', not kit_lines, str(kit_lines[:2]))
            while s.drive is not None:
                CS.world(s)
            ck(f'K2 {name} skipped at {t_press}: it ends as the uninterrupted run (#sqdone at {LEN[name]}, the same end state)',
               (name, LEN[name]) in s.done and state(s) == ref_end, str([(k, state(s)[k], ref_end[k]) for k in ref_end if state(s)[k] != ref_end[k]]))
            tail = lines_from(s.rec[m0:], name, to)
            ck(f'K2 {name} skipped at {t_press}: the lines from {to} on come as in the full run', tail == ref_tail, f'{tail[:3]} {ref_tail[:3]}')
            rg = [r['sq'] for r in s.rec[n0:] if r['seq'] == name and r.get('rig') and r.get('body1') and math.dist(r['rig'], r['body1'][0]) > 1e-6]
            ck(f'K2 {name} skipped at {t_press}: her model is at her body on every tick from the skip to the end (no pop)', not rg, str(rg[:6]))
            Q.go(s, 2)
            bad = [k for k, v in CS.clean(s).items() if not v]
            ck(f'K3 {name} skipped at {t_press}: released, nothing left', not bad and not Q.leftovers(s), f'{bad} {Q.leftovers(s)}')
        # the core's test hook (#skp hr = the tick to skip at) is honoured by the sequence's own input
        s, pl = world(name)
        s.setsc('#skp', 'hr', lo + 60)
        Q.play(s, name, until=lambda s: (s.sc('#sq', 'hr') or 0) >= to + 4, limit=lo + 80)
        ck(f'K7 {name}: #skp hr {lo + 60} (the test commands) skips at that tick', s.sc('#sq', 'hr') == to + 4 and len(s.rec) < lo + 80,
           f"{s.sc('#sq', 'hr')} {len(s.rec)}")
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
        s.st(pl)['cam'] = s.st(pl)['ccam'] = None
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

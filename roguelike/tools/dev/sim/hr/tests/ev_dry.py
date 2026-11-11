#!/usr/bin/env python3
"""ev_dry.py [--dp ROGUELIKE] — the offline sequence suite of 홍련 (Scarlet): seq.py's services built with a dummy Writer and
dry-run in mcsim (run from a copy of hr/tests outside the datapack). S2b's suite of 11-06, rebased by lane H2 (11-11) on the
sequence contract 2 (hr_design §3: intro, cs1, lead60, repel, lead5, lead_re, ending, event; tools/mboss_scarlet/seq.py +
cam.py). The locked runs in the framework's world (the lock, the cameras, the hand-backs, every exit path, the shot sheets)
are hr/tests/test_seq.py; this suite needs no world for most of it and pins the generated text.

  build    SERVICES = one api.Service per api.SEQS (clips api.SEQ_CLIPS, args api.SEQ_ARGS); a dummy Writer: every file under
           seq/<its own name>/ (+ the shared seq/lib/), the entry points start / tick / cancel (+ api.SEQ_EXTRA's skips, lock /
           unlock / fin / cam of the locked ones, lead_re/g/<g>), the macro starts take exactly their api.SEQ_ARGS; the kit /
           theme / reward off -> no fx / look / ev line and no empty line; deterministic; CONTRACT = 2 on a line of its own
  refs     every function a sequence calls: its own seq/** files, rig/** (api.RIG_CALLS, play / start of api.CLIPS), the kit
           through api.K (contract names and args), the framework (mboss/**, view/sync), the actor (char/cine/*), ev/apply +
           ev/title - nothing else, never the core; no negative add / remove literals; lowercase resource ids; every summoned
           display rotated after it; the lock only as the framework's request (#mbCam, in lock files): no spectate / gamemode
  ticks    every tick a sequence uses <= its length (api.SEQ_LEN); #sqdone at the length; the dispatch trees (timeline and
           camera) reach exactly their leaves; the lines at api.LINE_AT (each of 1-25 but 12 once), music at api.MUSIC_AT, the
           title at the draw, the crimson look at cs1 recolour, the banner only at the refill beats and only while #warn hr 1,
           #sq_sig only = api.SIG at the repel's api.COUNTER_EV and the refill beats of lead5 / lead_re, the halo's bright looks
  event    (mcsim, both branches x 8 player positions incl. 20 b away): 120 t; the line at E4 cleared at E52 (< E56), the grant
           + title once at E56, the black at E110 (10 / 12 / 0), ev_leave at E34, state/hidden at E40; the thrown sword: rotated
           in its summon tick, one end-over-end turn <= 30 deg / t, never below the floor, at E44 0.9 b before the player's
           chest along their facing, shrinking into the player's hand, gone at E56; the moonlight orb; cancel at every tick
           leaves nothing
  cancel   every sequence cancelled at its cut and signal ticks (twice, no executor) leaves no stage, stand, prop or helper
  seam     the ending's tick 0 opens with the hard cut seq.SEAM_CUT (in 0, hold >= 2), no other effect in its first ticks
  skip     seq/intro/skip: the black, the rock and props gone, her 6.5 b from the avatar facing it; the next tick (#sq 1290)
           plays intro_end, line 11 at 1294. seq/cs1/skip: on her mark 9 b ahead, the clip at 565, the looks of 566
  ending   an unmoving avatar (the framework's real movers): she lands 9 b away toward the moon, faces the moon after the
           turn, the avatar again after the pivot, ends 4.5 b away
"""
import argparse
import importlib
import json
import math
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--dp', default=os.environ.get('HR_DP', ''))
ap.add_argument('-v', action='store_true', help='list the passed checks too')
A = ap.parse_args()
assert A.dp, 'ev_dry.py --dp <datapack root> (or HR_DP)'
DP = Path(A.dp)
FN = DP / 'data/rlk/function'
sys.dont_write_bytecode = True
sys.path.insert(0, str(DP / 'tools'))
sys.path.insert(0, str(HERE / 'lib'))
import mcsim  # noqa: E402
from mboss_scarlet import api  # noqa: E402

FAIL, OK = [], []
LOCKED = ('intro', 'cs1', 'repel', 'ending', 'event')


def check(label, cond, detail=''):
    (OK if cond else FAIL).append(label)
    if not cond:
        print('FAIL ' + label + (('  ' + str(detail)) if detail else ''))


# ================================================================ build (a dummy Writer, the kit / theme / reward forced)
class DW:
    def __init__(self):
        self.files = {}

    def w(self, rel, body):
        assert rel.startswith('seq/'), rel
        if rel in self.files:
            raise AssertionError(f'written twice: {rel}')
        self.files[rel] = list(body)


def build(on=True, patch=None):
    saved = (api.theme_ready, api.reward_ready, api.EVENT['lines'])
    api.K._on = lambda: on
    api.theme_ready = lambda: on
    api.reward_ready = lambda: on
    for k, v in (patch or {}).items():
        if k == 'lines':
            api.EVENT['lines'] = v
        else:
            setattr(api, k, v)
    try:
        from mboss_scarlet import seq
        seq = importlib.reload(seq)
        W, owner = DW(), {}
        for s in seq.SERVICES:
            before = set(W.files)
            s.build(W)
            owner[s.name] = sorted(set(W.files) - before)
        return seq, W.files, owner
    finally:
        try:
            del api.K._on
        except AttributeError:
            pass
        api.theme_ready, api.reward_ready, api.EVENT['lines'] = saved


seq, F, OWNER = build(True)
_, F2, _ = build(True)
seq_off, FOFF, _ = build(False)
src = (DP / 'tools/mboss_scarlet/seq.py').read_text(encoding='utf-8')
check('build: CONTRACT = 2 on a line of its own (the core takes the sequences only then)', re.search(r'^CONTRACT = 2$', src, re.M) is not None
      and seq.CONTRACT == api.SEQ_CONTRACT == 2)
check('build: two builds identical (deterministic)', F == F2)
check(f'build: SERVICES = api.SEQS ({[s.name for s in seq.SERVICES]})', [s.name for s in seq.SERVICES] == list(api.SEQS))
check('build: Service clips = api.SEQ_CLIPS, args = api.SEQ_ARGS',
      all(tuple(s.clip) == tuple(api.SEQ_CLIPS[s.name]) and s.args == dict(api.SEQ_ARGS.get(s.name, {})) for s in seq.SERVICES))
check(f'build: every file under seq/** ({len(F)} files; kit off {len(FOFF)})', all(r.startswith('seq/') for r in list(F) + list(FOFF)))
check('build: each service writes only under seq/<its name>/ (and the shared seq/lib/)',
      all(all(r.startswith((f'seq/{n}/', 'seq/lib/')) for r in rs) for n, rs in OWNER.items()), {n: [r for r in rs if not r.startswith((f'seq/{n}/', 'seq/lib/'))][:2] for n, rs in OWNER.items()})
need = [f'seq/{n}/{p}' for n in api.SEQS for p in ('start', 'tick', 'cancel')] + [f'seq/{n}/{x}' for n, xs in api.SEQ_EXTRA.items() for x in xs] + \
    [f'seq/{n}/{p}' for n in LOCKED for p in ('lock', 'unlock', 'fin', 'cam')] + [f'seq/lead_re/g/{g}' for g in api.SEQ_ARGS['lead_re']['g']]
check('build: entry points start / tick / cancel of the 8, intro/skip + cs1/skip, lock / unlock / fin / cam of the locked five, lead_re/g/<g>',
      all(r in F and r in FOFF for r in need), [r for r in need if r not in F or r not in FOFF])
macro_args = {n: sorted(set(re.findall(r'\$\((\w+)\)', '\n'.join(F[f'seq/{n}/start'])))) for n in api.SEQS}
check('build: the macro starts take exactly api.SEQ_ARGS (repel at, lead_re g; the others none)',
      macro_args == {n: sorted(api.SEQ_ARGS.get(n, {})) for n in api.SEQS}, macro_args)
dollar = [r for r, L in F.items() if any(l.startswith('$') for l in L) and r not in ('seq/repel/start', 'seq/lead_re/start')]
check('build: no other macro file', not dollar, dollar)
empty = [r for r, L in list(F.items()) + list(FOFF.items()) if any(not l.strip() or l.rstrip().endswith(' run') for l in L)]
check('build: no empty or dangling line (kit on and off)', not empty, empty[:4])
off_fx = [r for r, L in FOFF.items() if any('/fx/' in l or 'mboss/arena/' in l or '/ev/' in l or '#hrLook' in l for l in L if not l.startswith('#'))]
check('build: the kit / theme / reward off -> no fx, look or ev line', not off_fx, off_fx[:4])
ALL = '\n'.join(l for L in F.values() for l in L if not l.startswith('#'))
ALL_REF = ALL + '\n' + '\n'.join(l.replace('$(g)', g) for l in ALL.split('\n') if '$(g)' in l for g in api.SEQ_ARGS['lead_re']['g'])

# ================================================================ refs
refs = {r for r in re.findall(r'function (rlk:[a-z0-9_/.\-]+)', ALL_REF) if not r.endswith('/')}
own = {f'{api.NS}{r}' for r in F}
rig_ok = {f'{api.NS}rig/{c}' for c in api.RIG_CALLS} | {f'{api.NS}rig/play/{c}' for c in api.CLIPS} | {f'{api.NS}rig/start/{c}' for c in api.CLIPS}
kit_ok = {f'{api.NS}fx/p/{n}' for n in api.KIT_PRESETS} | {f'{api.NS}fx/prop/{n}' for n in api.KIT_PROPS} | \
    {f'{api.NS}fx/snd/{n}' for n in api.KIT_SOUNDS} | {f'{api.NS}fx/hud/{n}' for n in api.KIT_HUD} | {f'{api.NS}fx/{n}' for n in api.KIT_FIXED}
ev_ok = {f'{api.NS}ev/apply', f'{api.NS}ev/title'}
actor_ok = {f'rlk:char/cine/{c}' for c in api.ACTOR_CALLS}
fw = {r for r in refs if r.startswith('rlk:mboss/') or r == 'rlk:view/sync'}
bad = sorted(r for r in refs - own - rig_ok - kit_ok - ev_ok - fw - actor_ok)
check('refs: only seq/**, rig/** (contract calls), the kit (contract names), ev/apply / ev/title, the actor and the framework', not bad, bad)
fw_missing = sorted(r for r in fw if not (FN / (r.split(':', 1)[1] + '.mcfunction')).exists() and not r.startswith('rlk:mboss/arena/'))
check(f'refs: every framework function exists ({len(fw)})', not fw_missing, fw_missing)
rig_missing = sorted(r for r in refs if r.startswith(f'{api.NS}rig/') and not (FN / (r.split(':', 1)[1] + '.mcfunction')).exists())
check('refs: every rig call exists in rig/**', not rig_missing, rig_missing)
own_missing = sorted(r for r in refs if r.startswith(f'{api.NS}seq/') and r not in own)
check('refs: every seq/** call is a written file', not own_missing, own_missing)
act_used = sorted(r for r in refs if r.startswith('rlk:char/cine/'))
check(f'refs: the actor calls ({act_used}) exist once lane H3\'s manifest does (api.actor_ready); none before',
      (act_used == sorted(actor_ok) and all((FN / (r.split(':', 1)[1] + '.mcfunction')).exists() for r in act_used)) if api.actor_ready() else not act_used)
args_bad = []
for name, a in re.findall(r'function rlk:boss/scarlet/fx/(?:p|prop|hud)/(\w+)(?: (\{[^}]*\}|with storage \S+ \S+))?', ALL):
    if a.startswith('with storage'):
        path = a.split()[3]
        sets = [l for l in ALL.split('\n') if f'data modify storage {a.split()[2]} {path} set value' in l]
        keys = sorted(re.findall(r'(\w+):', sets[0].split('set value', 1)[1])) if sets else []
    else:
        keys = sorted(re.findall(r'(\w+):', a)) if a else []
    want = sorted(api.KIT_PRESETS.get(name, api.KIT_HUD.get(name, list(api.KIT_PROPS.get(name, {})))))
    if keys != want:
        args_bad.append((name, keys, want))
check('refs: every kit call has its contract args', not args_bad, args_bad[:4])
neg = [l for l in ALL.split('\n') if re.search(r'scoreboard players (add|remove) \S+ \S+ -\d', l)]
check('static: no negative add / remove literals', not neg, neg[:3])
upper = [x for x in re.findall(r'"(rlk:[^"]*|minecraft:[^"]*)"', ALL) if x != x.lower()] + \
    [x for x in re.findall(r'function (\S+)', ALL) if x != x.lower()]
check('static: lowercase resource ids', not upper, upper[:3])
unrot = []
for r, L in F.items():
    for i, l in enumerate(L):
        m = re.search(r'summon minecraft:item_display .*Tags:\[[^\]]*"(rlk_hr_(?:sqp_\d|ev_sword))"', l)
        if m and not any(f'tag={m.group(1)}' in x and ' tp @s ' in x for x in L[i + 1:i + 3]):
            unrot.append(r)
check('static: every summoned display is rotated right after its summon (summon ignores the execute rotation)', not unrot, unrot)
BLANK = getattr(seq, 'HUD_BLANK', None)
txt = [l for l in ALL.split('\n') if re.search(r'^(?:execute .* run )?(tellraw|title @|say )', l) and l != BLANK]
check('static: no raw on-screen text (lines, overlays, the banner only through the kit; the empty actionbar aside)', not txt, txt[:2])
blank_bad = {n: len([l for l in F.get(f'seq/{n}/start', []) if l == BLANK]) for n in seq.HUD_OFF}
blank_more = sorted(r for r, L in F.items() if not re.match(r'seq/(%s)/start$' % '|'.join(seq.HUD_OFF), r) and any(l == BLANK for l in L))
check(f'static: the HUD-off sequences {seq.HUD_OFF} blank the actionbar once at their start, nowhere else',
      all(v == 1 for v in blank_bad.values()) and not blank_more, (blank_bad, blank_more[:3]))
korean = sorted({x for l in ALL.split('\n') for x in re.findall(r'"([^"\n]*[가-힣][^"\n]*)"', l)})
check(f'static: the only literal on-screen words are the title / sub ({korean})', set(korean) <= {api.NAME, api.SUB})
cam = [l for l in ALL.split('\n') if re.search(r'(^| run )(spectate|gamemode)\b|inputPermission|attribute .*movement_speed', l)]
check('static: the control lock is only the framework\'s (no spectate, game mode or input command in a sequence)', not cam, cam[:2])
req = sorted(r for r, L in F.items() if any('#mbCam mb 1' in l for l in L if not l.startswith('#')))
req0 = sorted(r for r, L in F.items() if any('#mbCam mb 0' in l for l in L if not l.startswith('#')))
check(f'static: the lock request #mbCam is set only in the lock files of the locked five and taken back only in their cancel',
      req == sorted(f'seq/{n}/lock' for n in LOCKED) and req0 == sorted(f'seq/{n}/cancel' for n in LOCKED), (req, req0))
evtag = [l for l in F['seq/event/k/30'] if 'summon' in l]
check('static: the event entities carry rlk_room rlk_mb_aux rlk_hr_ev', evtag and all('"rlk_room","rlk_mb_aux","rlk_hr_ev"' in l for l in evtag), evtag[:1])
core = [l for l in ALL.split('\n') for f in re.findall(r'function (rlk:boss/scarlet/\S+)', l)
        if not f.startswith(('rlk:boss/scarlet/seq/', 'rlk:boss/scarlet/rig/', 'rlk:boss/scarlet/fx/', 'rlk:boss/scarlet/ev/'))]
check('static: no call into the core (it reads #sq_sig / #sqdone only)', not core, core[:2])


# ================================================================ ticks, the dispatch trees, lines, music, looks, banner, signals
def leaves(name, kind, files=F):
    """{tick: (file, lines)} of a sequence's leaf files k/<t> | k/<a>_<b> (c/ for the camera)."""
    out = {}
    for r, L in files.items():
        m = re.match(rf'seq/{name}/{kind}/(\d+)(?:_(\d+))?$', r)
        if m:
            for t in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
                assert t not in out, (r, t)
                out[t] = (r, L)
    return out


def ticks_of(name, files=F):
    out = {t: L for t, (_r, L) in leaves(name, 'k', files).items()}
    out[0] = files[f'seq/{name}/start']
    return out


DSP = re.compile(r'^execute if score #sq hr matches (\d+)?(\.\.)?(\d+)? run (return run )?function rlk:boss/scarlet/(seq/\w+/(\w+)/\S+)$')


def reach(name, t, kind, files=F):
    """The leaf files the dispatch of `kind` (k from tick, c from cam) runs at #sq = t."""
    hits, todo = [], [f'seq/{name}/' + ('tick' if kind == 'k' else 'cam')]
    while todo:
        for l in files[todo.pop()]:
            m = DSP.match(l)
            if not m or m.group(6) not in (kind, kind + 'b'):
                continue
            lo = int(m.group(1)) if m.group(1) else -10 ** 9
            hi = int(m.group(3)) if m.group(3) else (10 ** 9 if m.group(2) else lo)
            if lo <= t <= hi:
                (todo if m.group(6) == kind + 'b' else hits).append(m.group(5))
                if m.group(4):
                    break
    return hits


T = {n: ticks_of(n) for n in api.SEQS}
over = {n: max(T[n]) for n in api.SEQS if max(T[n]) > api.SEQ_LEN[n]}
check('ticks: every tick a sequence uses <= its length (api.SEQ_LEN)', not over, over)
done = {n: f'execute if score #sq hr matches {api.SEQ_LEN[n]}.. run scoreboard players set #sqdone hr 1' in F[f'seq/{n}/tick'] for n in api.SEQS}
check('ticks: #sqdone at the length in every tick function, #sqdone 0 at start', all(done.values())
      and all('scoreboard players set #sqdone hr 0' in F[f'seq/{n}/start'] for n in api.SEQS), done)
dbad = []
for n in api.SEQS:
    for kind in ('k', 'c') if n in LOCKED else ('k',):
        lv = leaves(n, kind)
        for t in range(1, api.SEQ_LEN[n] + 2):
            got, want = reach(n, t, kind), ([lv[t][0]] if t in lv else [])
            if got != want:
                dbad.append((n, kind, t, got, want))
check('ticks: the dispatch trees (the timeline from tick, the camera from cam) reach exactly their leaf at every #sq', not dbad, dbad[:3])
stage_at = {n: any('rlk_hr_stage' in l and 'summon' in l for l in F[f'seq/{n}/start'] + F.get(f'seq/{n}/m/stage', []) + F.get(f'seq/{n}/m/alone', []))
            for n in LOCKED}
check('ticks: the stage marker (rlk_hr_stage) is made by the start of every locked sequence (the coda: when it starts alone)',
      all(stage_at.values()) and all(f'function {api.NS}seq/{n}/m/stage' in F[f'seq/{n}/start'] for n in ('cs1', 'repel', 'ending')), stage_at)
clk = {'intro': 'intro', 'intro_end': 'intro', 'cs1': 'cs1', 'ending': 'ending', 'event': 'event'}
off = {'intro': 0, 'intro_end': api.SKIP_T, 'cs1': 0, 'ending': 0, 'event': 0}
placed, wrong = {}, []
for n in api.SEQS:
    for t, L in T[n].items():
        for l in L:
            for i in re.findall(r'fx/hud/line \{id:(\d+)\}', l):
                placed.setdefault(int(i), []).append((n, t))
for i, (where, t0, _hold) in api.LINE_AT.items():
    if where == 'a6':
        continue
    want = (clk[where], off[where] + t0)
    if placed.get(i) != [want]:
        wrong.append((i, placed.get(i), want))
check('lines: each of 1-25 (but 12, A6 is the core\'s) exactly once at api.LINE_AT (11 = intro_end 4 = #sq 1294; 24 / 25 the coda at E4)',
      not wrong and 12 not in placed, wrong)
mus = sorted((n, t, int(m)) for n in api.SEQS for t, L in T[n].items() for l in L for m in re.findall(r'mboss/music/set \{ph:(\d)\}', l))
want_mus = sorted((('intro' if c == 'intro_end' else c), (api.SKIP_T if c == 'intro_end' else 0) + api.ev(c, e), ph) for ph, (c, e) in api.MUSIC_AT.items())
check(f'music: api.music(ph) at api.MUSIC_AT ({mus})', mus == want_mus, want_mus)
title = [(n, t) for n in api.SEQS for t, L in T[n].items() for l in L if 'mboss/title' in l]
check('title: mboss_lib.title(*api.TITLE) once at intro_end draw', title == [('intro', api.SKIP_T + api.ev('intro_end', 'draw'))]
      and api.L.title(*api.TITLE) in ALL, title)
looks = sorted((n, t, l.split()[-1]) for n in api.SEQS for t, L in T[n].items() for l in L if '#hrLook' in l)
check(f'looks: the crimson look request at cs1 recolour, no other ({looks})', looks == [('cs1', api.ev('cs1', 'recolour'), str(api.LOOK_ID['crimson']))])
phase = [(n, t) for n in api.SEQS for t, L in T[n].items() for l in L if 'look/phase/' in l]
check('looks: the rig P2 accents at cs1 recolour', phase == [('cs1', api.ev('cs1', 'recolour'))], phase)
HALO_RE = re.compile(re.escape(f'look_{api.AID}:"') + r'(\w+)"\}' + re.escape(f' as @e[type=minecraft:item_display,tag='
                                                                             f'{api.TAGS["deco_moon_halo"]}] run function '
                                                                             f'{api.NS}fx/prop/moon_halo {{look:"') + r'(\w+)"\}')
halo_at = {r: sorted(m.groups() for l in L for m in [HALO_RE.search(l)] if m) for r, L in F.items()}
halo_at = {r: v for r, v in halo_at.items() if v}
BRIGHT, BACK = [('crimson', 'p2b'), ('moon', 'p1b')], [('crimson', 'p2'), ('moon', 'p1')]
H0, H1 = api.ev('intro', 'raise') + 4, 530
G0, G1 = 980, 1060
want_halo = {leaves('intro', 'k')[H0][0]: BRIGHT, leaves('intro', 'k')[H1][0]: BACK, leaves('ending', 'k')[G0][0]: BRIGHT,
             leaves('ending', 'k')[G1][0]: BACK, 'seq/intro/skip': BACK, 'seq/intro/cancel': BACK, 'seq/ending/cancel': BACK}
halo_any = sorted(r for r, L in F.items() if any('fx/prop/moon_halo' in l for l in L))
check(f'halo: p1b / p2b by the arena look at intro {H0} and ending {G0}, p1 / p2 at {H1} and {G1}, the same restore in intro/skip and '
      f'the intro / ending cancel, no other halo line', halo_at == want_halo and halo_any == sorted(want_halo),
      {r: (halo_at.get(r), want_halo.get(r)) for r in set(halo_at) | set(want_halo) if halo_at.get(r) != want_halo.get(r)})
warn_on = sorted((n, t, l) for n in api.SEQS for t, L in T[n].items() for l in L if 'fx/hud/warn {on:1}' in l)
want_warn = [('lead5', api.ev('lead5', 'refill')), ('lead_re', api.ev('lead_re', 'refill'))]
check('banner: on only at the refill beat of lead5 (60) and lead_re (10), and only while #warn hr 1 (the core sets it for a lethal gauntlet)',
      [(n, t) for n, t, _l in warn_on] == want_warn and all(l.startswith('execute if score #warn hr matches 1 run ') for _n, _t, l in warn_on), warn_on)
warn_off = sorted(n for n in api.SEQS if any('fx/hud/warn {on:0}' in l for l in F[f'seq/{n}/start']))
check(f'banner: off at the start of every lead-in ({warn_off}); nothing else touches it (the judge turns it off)',
      warn_off == ['lead5', 'lead60', 'lead_re'] and ALL.count('fx/hud/warn') == len(warn_on) + 3, ALL.count('fx/hud/warn'))
sigs = sorted((n, t, int(v)) for n in api.SEQS for t, L in T[n].items() for l in L for v in re.findall(r'#sq_sig hr (\d+)', l))
want_sig = sorted([('repel', api.ev('repel', e), api.SIG[f'hp{i + 1}']) for i, e in enumerate(api.COUNTER_EV)]
                  + [('lead5', api.ev('lead5', 'refill'), api.SIG['refill']), ('lead_re', api.ev('lead_re', 'refill'), api.SIG['refill'])])
check(f'signal: #sq_sig = api.SIG only at the repel\'s strike / land / kick (49 / 101 / 129) and the refill beat of lead5 / lead_re ({sigs})',
      sigs == want_sig, want_sig)
refx = {n: [l for l in T[n][api.ev(n, 'refill') if n != 'lead60' else 0] if '/fx/' in l and '/hud/warn' not in l] for n in ('lead60', 'lead5', 'lead_re')}
check('refill: every lead-in plays the refill\'s effect and sound itself (lead60 at its tick 0: the core\'s shield/arm is silent)',
      all(any('/fx/p/' in l for l in v) and any('/fx/snd/' in l for l in v) for v in refx.values()), {n: len(v) for n, v in refx.items()})
gold0 = [l for l in T['repel'][0] if '/fx/' in l]
check('repel: its first frame stages the gold deflect (an overlay, the gold burst at the lock point, its sounds; the judge plays nothing)',
      any('fx/hud/ovl' in l for l in gold0) and any('fx/p/clash_gold' in l for l in gold0) and any('playsound' in l or '/fx/snd/' in l for l in T['repel'][0]), gold0[:4])
blk = [l for l in T['event'][api.EV_T['black']] if 'ovl' in l]
check('event: the black at E110 = ovl black in 10 hold 12 out 0', any('{g:"black",in:10,hold:12,out:0}' in l for l in blk), blk)
nl = build(True, {'lines': False})[1]
cut = [l for l in T['ending'][0] if 'fx/hud/ovl' in l]
early = sorted(t for t in T['ending'] if 0 < t <= 3 and any('fx/' in l for l in T['ending'][t]))
check(f'seam: the ending opens with a hard cut at tick 0 ({cut}), no other effect before it ends ({early})',
      len(cut) == 1 and re.search(r'\{g:"(white|black)",in:0,hold:([2-9]|\d\d+),out:[0-3]\}', cut[0]) is not None
      and tuple(seq.SEAM_CUT[1:3]) == (0, int(re.search(r'hold:(\d+)', cut[0]).group(1))) and not early, (cut, early))
check('event: EVENT[lines] off -> no line 24 / 25 (a wordless coda)', not re.search(r'line \{id:2[45]\}', '\n'.join(l for L in nl.values() for l in L)))
# what a cancel releases (lane H1: on a pause / reload the core cancels and goes to the end state itself)
canc = {n: F[f'seq/{n}/cancel'] for n in api.SEQS}
rel_bad = {n: [w for w, ok in (('the stands', 'function rlk:mboss/cam/kill' in L), ('the stage', any('tag=rlk_hr_stage]' in l and l.startswith('kill') for l in L)),
                                 ('the request', 'scoreboard players set #mbCam mb 0' in L), ('the lock flags', any('#sq_cx hr 0' in l for l in L)),
                                 ('the overlay / line', f'function {api.NS}fx/hud/clear' in L), ('hudHold', any('hudHold 0' in l for l in L)),
                                 ('the actor', (not api.actor_ready()) or any('char/cine/stop' in l for l in L))) if not ok] for n, L in canc.items() if n in LOCKED}
check('cancel: a locked sequence\'s cancel takes the request back and removes the stands, the stage, the actor, the kit\'s line / overlay and the HUD hold',
      not any(rel_bad.values()), {n: v for n, v in rel_bad.items() if v})


# ================================================================ the mcsim world
class Sim(mcsim.Sim):
    STUB = ('rlk:boss/scarlet/fx/', 'rlk:boss/scarlet/ev/', 'rlk:mboss/title', 'rlk:mboss/music/', 'rlk:mboss/push/', 'rlk:mboss/pull/',
            'rlk:char/cine/', 'rlk:view/sync')
    RIG_REAL = ('init', 'an/load', 'anchor/', 'play/', 'start/')

    def __init__(self, files):
        super().__init__(FN)
        self.files, self.t, self.log = files, 0, []

    def load(self, fid):
        rel = fid.split(':', 1)[1]
        if rel.startswith('boss/scarlet/seq/'):
            return self.files[rel[len('boss/scarlet/'):]]
        return super().load(fid)

    def call(self, fid, ctx, macro=None):
        self.log.append((self.t, fid, dict(macro or {})))
        if fid.startswith(self.STUB):
            return 1
        if fid.startswith('rlk:boss/scarlet/rig/'):
            rel = fid[len('rlk:boss/scarlet/rig/'):]
            if rel in ('face/player', 'face/track') and ctx.ex:
                pl = self.player()
                if pl:
                    want = math.degrees(math.atan2(-(pl.pos[0] - ctx.ex.pos[0]), pl.pos[2] - ctx.ex.pos[2]))
                    d = (want - ctx.ex.rot[0] + 540) % 360 - 180
                    if rel == 'face/track':
                        d = max(-12, min(12, d))
                    ctx.ex.rot = [ctx.ex.rot[0] + d, 0.0]
                return 1
            if not rel.startswith(self.RIG_REAL):
                return 1
        return super().call(fid, ctx, macro)

    def player(self):
        return next((e for e in self.ents if e.alive and 'rlk_body' in e.tags), None)

    def select(self, sel, ctx):
        if sel.startswith('@p'):
            sel = '@a' + sel[2:]
            return super().select(sel, ctx)[:1]
        return super().select(sel, ctx)

    def execute(self, t, ctx):
        """`facing <x> <y> <z>` (absolute; mcsim knows `facing entity`): rewritten in place to `facing entity` of a fixed marker
        at that point, so the subcommands keep their order."""
        t = list(t)
        i = 0
        while i < len(t) and t[i] != 'run':
            if t[i] == 'facing' and t[i + 1] != 'entity':
                key = '_fc_' + '_'.join(t[i + 1:i + 4]).replace('-', 'm').replace('.', 'p')
                if not any(key in e.tags for e in self.ents if e.alive):
                    self.ents.append(mcsim.Ent('marker', [float(v) for v in t[i + 1:i + 4]], (0.0, 0.0), [key]))
                t[i:i + 4] = ['facing', 'entity', f'@e[tag={key},limit=1]', 'feet']
            i += 1
        return super().execute(t, ctx)

    def cmd(self, t, ctx):
        c = t[0]
        if c == 'summon':
            r = super().cmd(t, ctx)
            e = self.ents[-1]
            if len(t) > 5:
                try:
                    nbt = mcsim.Sim.snbt(re.sub(r'(?<=[:\[,])(-?)\.(\d)', r'\g<1>0.\2', t[5]))
                    e.data.update({k: v for k, v in nbt.items() if k != 'Tags'})
                except Exception:   # noqa: BLE001
                    pass
            e.data['_born'] = self.t
            return r
        if c == 'data' and t[1] == 'merge' and t[2] == 'entity':
            v = mcsim.Sim.snbt(t[4])
            for e in (self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]):
                e.data.update(v)
                e.data['_merged'] = self.t
            return 1
        if c == 'rotate':
            tg = self.select(t[1], ctx) if t[1] != '@s' else [ctx.ex]
            if t[2] == 'facing':           # F2 (HR-02): rotate <target> facing entity <e> [eyes|feet] / facing <x y z>
                if t[3] == 'entity':
                    e2 = (self.select(t[4], ctx) or [None])[0]
                    if e2 is None:
                        return 0
                    tgt = list(e2.pos)
                    if len(t) > 5 and t[5] == 'eyes':
                        tgt[1] += e2.data.get('eye', 0.0)
                else:
                    tgt = list(self.coords(t[3:6], ctx))
                for e in tg:
                    org = list(e.pos)
                    if getattr(ctx, 'anc', False):          # execute anchored eyes: from the target's own eyes
                        org[1] += e.data.get('eye', 0.0)
                    dx, dy, dz = (tgt[j] - org[j] for j in range(3))
                    e.rot = [math.degrees(math.atan2(-dx, dz)), math.degrees(-math.atan2(dy, math.hypot(dx, dz)))]
                    e.data['_rotated'] = self.t
                return 1
            for e in tg:
                e.rot = [ctx.rot[0] + float(t[2][1:] or 0) if t[2].startswith('~') else float(t[2]), 0.0]
            return 1
        if c == 'tp' and len(t) > 5 and t[5] == 'facing':
            pos = self.coords(t[2:5], ctx)
            if t[6] == 'entity':
                e2 = self.select(t[7], ctx)[0]
                tgt = list(e2.pos)
                if len(t) > 8 and t[8] == 'eyes':
                    tgt[1] += e2.data.get('eye', 0.0)
            else:
                tgt = self.coords(t[6:9], ctx)
            for e in (self.select(t[1], ctx) if t[1] != '@s' else [ctx.ex]):
                e.pos = list(pos)
                dx, dy, dz = (tgt[j] - pos[j] for j in range(3))
                e.rot = [math.degrees(math.atan2(-dx, dz)), math.degrees(-math.atan2(dy, math.hypot(dx, dz)))]
            return 1
        if c in ('stopsound', 'particle', 'playsound'):
            return 1
        if c == 'scoreboard' and t[1] == 'objectives':
            return 1
        return super().cmd(t, ctx)


C0 = (api.CX + .5, float(api.CY), api.CZ + .5)


def world(files, body_at, body_yaw, pl_at, pl_yaw, ev_branch=0):
    s = Sim(files)
    arena = mcsim.Ent('marker', list(C0), (0.0, 0.0), ['rlk_mb_arena'])
    body = mcsim.Ent('husk', list(body_at), (body_yaw, 0.0), ['rlk_mb_body', 'rlk_room'])
    pl = mcsim.Ent('player', list(pl_at), (pl_yaw, 0.0), ['player', 'rlk_body'])
    pl.data['eye'] = 1.62
    s.ents += [arena, body, pl]
    for k, v in {'#mbAr': 5, '#c2': 2, '#c4': 4, '#c100': 100, '#c1000': 1000, '#c36000': 36000, '#cm1': -1}.items():
        s.setsc(k, 'mb', v)
    s.setsc('#hrEv', 'hr', ev_branch)
    global AN_STORE
    if AN_STORE is None:
        s.call('rlk:boss/scarlet/rig/init', mcsim.Ctx(body, tuple(body.pos), tuple(body.rot)))
        AN_STORE = json.loads(json.dumps(s.storage.get('rlk:hr', {})))
    s.storage['rlk:hr'] = json.loads(json.dumps(AN_STORE))
    return s, body, pl


AN_STORE = None


def bctx(body):
    return mcsim.Ctx(body, tuple(body.pos), tuple(body.rot))


def run_seq(s, body, name, n, start_args=None, each=None, from_t=0):
    """The core's loop: #sq 0 + start (+ the rig tick); then per tick mv/all, #sq + 1, seq/<name>/tick, the rig tick."""
    s.t = from_t
    s.setsc('#sq', 'hr', 0)
    s.call(f'rlk:boss/scarlet/seq/{name}/start', bctx(body), start_args)
    s.setsc(('e', body.id), 'hrRigT', (s.sc(('e', body.id), 'hrRigT') or 0) + 1)
    if each:
        each(0)
    for k in range(1, n + 1):
        s.t = from_t + k
        if s.sc('#mbMvOn', 'mb') == 1:
            s.call('rlk:mboss/mv/all', mcsim.Ctx(None, C0, (0.0, 0.0)))
        s.setsc('#sq', 'hr', k)
        s.call(f'rlk:boss/scarlet/seq/{name}/tick', bctx(body))
        s.setsc(('e', body.id), 'hrRigT', (s.sc(('e', body.id), 'hrRigT') or 0) + 1)
        if each:
            each(k)


def qangle(a, b):
    return 2 * math.degrees(math.acos(min(1.0, abs(sum(x * y for x, y in zip(a, b))))))


def qrot(q, v):
    x, y, z, w = q
    vx, vy, vz = v
    tx, ty, tz = 2 * (y * vz - z * vy), 2 * (z * vx - x * vz), 2 * (x * vy - y * vx)
    return (vx + w * tx + y * tz - z * ty, vy + w * ty + z * tx - x * tz, vz + w * tz + x * ty - y * tx)


def kitcalls(s, name):
    return [(t, m) for t, f, m in s.log if f == f'{api.NS}fx/{name}']


# ================================================================ the event coda (both branches x 8 player positions)
E = api.EV_T
POS = [(0, 4.5, 0), (40, 4.5, 30), (-60, 6, -20), (90, 3.5, 170), (150, 8, 10), (200, 12, -90), (270, 16, 45), (330, 20, 200)]
ev_res = {'item': [], 'buff': []}
floor_bad, turn_bad, arr_bad, rot_bad, shrink_bad, orb_bad, kit_bad, seq_bad, left = [], [], [], [], [], [], [], [], []
for br, code in (('item', 1), ('buff', 2)):
    for bearing, dist, pl_yaw in POS:
        b = math.radians(bearing)
        bpos = (C0[0] + 3 * math.sin(b) * 0, float(api.CY), C0[2])
        ppos = (bpos[0] - dist * math.sin(b), float(api.CY), bpos[2] + dist * math.cos(b))
        yaw_to_pl = math.degrees(math.atan2(-(ppos[0] - bpos[0]), ppos[2] - bpos[2]))
        s, body, pl = world(F, bpos, yaw_to_pl, ppos, pl_yaw, code)
        s.t = -1
        s.call(f'rlk:boss/scarlet/rig/play/ending', bctx(body))
        s.setsc(('e', body.id), 'hrRigT', api.CLIPS['ending'][0])
        track = []

        def each(k, s=s, track=track):
            sw = [e for e in s.ents if e.alive and 'rlk_hr_ev_sword' in e.tags]
            orb = [e for e in s.ents if e.alive and 'rlk_hr_ev_orb' in e.tags]
            track.append((k, [(list(e.pos), list(e.rot), json.loads(json.dumps(e.data))) for e in sw], [list(e.pos) for e in orb]))
        run_seq(s, body, 'event', api.SEQ_LEN['event'], each=each)
        tag = f'{br} @{bearing}/{dist}b'
        # the sequence's kit / rig timing
        lines = [(t, m.get('id')) for t, m in kitcalls(s, 'hud/line')]
        want_line = [(E['line'], 24 if br == 'item' else 25)]
        clears = [t for t, _ in kitcalls(s, 'hud/clear')]
        grants = [t for t, f, _ in s.log if f in (f'{api.NS}ev/apply', f'{api.NS}ev/title')]
        black = [(t, m) for t, m in kitcalls(s, 'hud/ovl')]
        leave = [t for t, f, _ in s.log if f == f'{api.NS}rig/play/ev_leave']
        hidden = [t for t, f, _ in s.log if f == f'{api.NS}rig/state/hidden']
        clip0 = [f for t, f, _ in s.log if t == 0 and f.startswith(f'{api.NS}rig/play/')]
        ok = (lines == want_line and clears == [E['line_clear']] and E['line_clear'] < E['grant'] and grants == [E['grant'], E['grant']]
              and black == [(E['black'], {'g': 'black', 'in': 10, 'hold': 12, 'out': 0})] and leave == [E['leave']] and hidden == [E['hide']]
              and clip0 == [f'{api.NS}rig/play/' + ('ev_give' if br == 'item' else 'ev_toast')])
        if not ok:
            seq_bad.append((tag, lines, clears, grants, black, leave, hidden, clip0))
        names = {f[len(api.NS) + 3:] for t, f, _ in s.log if f.startswith(f'{api.NS}fx/')}
        badk = [n for n in names if n.split('/', 1)[1] not in {'p': api.KIT_PRESETS, 'snd': api.KIT_SOUNDS, 'hud': api.KIT_HUD,
                                                               'prop': api.KIT_PROPS}[n.split('/', 1)[0]]]
        if badk:
            kit_bad.append((tag, badk))
        want_snd = {'ev_lift', 'ev_chime', 'ev_toss', 'ev_leave', 'ev_beam', 'ev_take_i'} if br == 'item' else \
            {'ev_chime', 'ev_toss', 'ev_leave', 'ev_beam', 'ev_take_b'}
        got_snd = {n.split('/', 1)[1] for n in names if n.startswith('snd/')}
        if got_snd != want_snd:
            kit_bad.append((tag, 'sounds', sorted(got_snd ^ want_snd)))
        if br == 'item':
            fly = [(k, x[0]) for k, x, _ in track if x]
            born = [k for k, x in fly]
            if born[:1] != [E['toss']] or born[-1] != E['grant'] - 1:
                arr_bad.append((tag, 'life', born[:1], born[-1:]))
            prevq = None
            for k, (pos, rot, data) in fly:
                tr = data.get('transformation', {})
                q, sc = tr.get('left_rotation'), (tr.get('scale') or [seq.S0])[0]
                if not q:
                    rot_bad.append((tag, k, 'no transformation'))
                    continue
                tip = qrot(q, (-.7071068, .7071068, 0.0))
                lowest = pos[1] - abs(tip[1]) * seq.SWORD_R * sc - .02
                if lowest < api.CY - 1e-6:
                    floor_bad.append((tag, k, round(lowest - api.CY, 3)))
                if prevq and qangle(prevq, q) > 30.01:
                    turn_bad.append((tag, k, round(qangle(prevq, q), 1)))
                prevq = q
                if k == E['toss'] and (data.get('_merged') is None and abs(rot[0]) < 1e-6):
                    rot_bad.append((tag, k, 'not rotated in its summon tick'))
            a = dict(fly).get(E['beam'])
            if a:
                fy = math.radians(pl.rot[0])
                want = (pl.pos[0] - .9 * math.sin(fy), pl.pos[1] + 1.1, pl.pos[2] + .9 * math.cos(fy))
                d = math.dist(a[0], want)
                if d > .25 and want[1] - 1 > api.CY:
                    arr_bad.append((tag, round(d, 3), [round(v, 2) for v in a[0]], [round(v, 2) for v in want]))
                tipv = qrot(a[2]['transformation']['left_rotation'], (-.7071068, .7071068, 0.0))
                if tipv[1] > -.95:
                    arr_bad.append((tag, 'not upright scabbard down at E44', [round(v, 2) for v in tipv]))
            sc_end = [x[2]['transformation']['scale'][0] for k, x in fly if k == E['grant'] - 1]
            if not sc_end or abs(sc_end[0] - .15) > .02:
                shrink_bad.append((tag, sc_end))
            last = [x[0] for k, x in fly if k == E['grant'] - 1]
            if last:
                hand = (pl.pos[0], pl.pos[1] + 1.0, pl.pos[2])
                if math.dist(last[0], hand) > .6:
                    shrink_bad.append((tag, 'not at the hand', round(math.dist(last[0], hand), 2)))
            ev_res['item'].append(tag)
        else:
            orbs = [(k, o[0]) for k, _, o in track if o]
            ks = [k for k, _ in orbs]
            if ks[:1] != [E['toss']] or ks[-1] != E['arrive'] - 1:
                orb_bad.append((tag, 'life', ks[:1], ks[-1:]))
            chest = (pl.pos[0], pl.pos[1] + 1.1, pl.pos[2])
            a, p0 = dict(orbs).get(E['arrive'] - 1), dict(orbs).get(E['toss'])
            n_orb = E['arrive'] - E['toss']
            if not a or math.dist(a, chest) > math.dist(p0, chest) / n_orb + .35:
                orb_bad.append((tag, 'not 1/12 short of the chest at E41', a and round(math.dist(a, chest), 2)))
            if any(p[1] < api.CY + .9 for _, p in orbs):
                orb_bad.append((tag, 'low'))
            ev_res['buff'].append(tag)
        rest = [e.tags for e in s.ents if e.alive and ({'rlk_hr_ev', 'rlk_hr_sqh'} & set(e.tags))]
        if rest:
            left.append((tag, 'after E120', rest))
check(f'event: both branches ran from 8 player positions incl. 20 b away ({len(ev_res["item"])} + {len(ev_res["buff"])})',
      len(ev_res['item']) == len(ev_res['buff']) == len(POS))
check('event: line 24 / 25 at E4, cleared at E52 (< E56), ev/apply + ev/title once at E56, the black at E110 (10 / 12 / 0), '
      'ev_leave at E34, state/hidden at E40, ev_give / ev_toast at E0', not seq_bad, seq_bad[:2])
check('event: every kit call a contract name; the branch\'s 6 / 5 ev sounds', not kit_bad, kit_bad[:3])
check('event: the thrown sword rotated in its summon tick (summoned, then turned)', not rot_bad, rot_bad[:3])
check('event: the sword never below the floor (every tick, its lowest end at its scale)', not floor_bad, floor_bad[:4])
check('event: one end-over-end turn <= 30 deg / t', not turn_bad, turn_bad[:4])
check('event: the sword lives E30-E55, arrives at E44 0.9 b before the player\'s chest along their facing, upright (scabbard down)',
      not arr_bad, arr_bad[:4])
check(f'event: it sinks into the player\'s hand (scale {seq.S1:g} -> 0.15 at E55, at the hand)', not shrink_bad, shrink_bad[:3])
# S23 (S2d): the toss summon at the right hand's offset the rig builder measured (manifest item_sword.toss_offset, ^left ^up ^forward)
_toss = (api.rig_manifest().get('item_sword') or {}).get('toss_offset')
if _toss:
    _summ = [l for l in F.get(f'seq/event/k/{E["toss"]}', []) if 'summon minecraft:item_display' in l and 'rlk_hr_ev_sword' in l]
    _m = [re.search(r'positioned \^(\S*) \^(\S*) \^(\S*) run summon', l) for l in _summ]
    _got = [[float(v or 0) for v in m.groups()] for m in _m if m]
    check(f'event: the toss summons at the measured hand offset ^{_toss[0]} ^{_toss[1]} ^{_toss[2]} (manifest item_sword.toss_offset ± 0.02)',
          _got and all(all(abs(a - b) <= .02 for a, b in zip(g, _toss)) for g in _got), _got)
else:
    print('skipped event toss offset (manifest without item_sword.toss_offset)')
check('event: the moonlight orb E30-E42 from her left hand onto the player\'s chest (E41 one step short), above the floor', not orb_bad, orb_bad[:3])
check('event: nothing left after E120 (rlk_hr_ev, helpers)', not left, left[:2])


# cancel at every tick of the coda (both branches) and at the cut / signal ticks of every other sequence leaves none of its entities
GONE = {'rlk_hr_sqp', 'rlk_hr_sqh', 'rlk_hr_stage', 'rlk_hr_stage2', 'rlk_hr_ev', 'rlk_mb_cam'}
cancel_bad = []
for br, code in (('item', 1), ('buff', 2)):
    for cut_at in range(0, api.SEQ_LEN['event'] + 1, 1):
        s, body, pl = world(F, (C0[0], api.CY, C0[2] - 4), 0.0, (C0[0], api.CY, C0[2]), 180.0, code)
        s.call(f'rlk:boss/scarlet/rig/play/ending', bctx(body))
        run_seq(s, body, 'event', cut_at)
        s.call(f'{api.NS}seq/event/cancel', mcsim.Ctx(None, C0, (0.0, 0.0)))
        s.call(f'{api.NS}seq/event/cancel', mcsim.Ctx(None, C0, (0.0, 0.0)))
        rest = [sorted(e.tags) for e in s.ents if e.alive and (GONE & set(e.tags))]
        if rest:
            cancel_bad.append((br, cut_at, rest))
check('event: cancel (twice, no executor) at every tick E0-E120 leaves no rlk_hr_ev / stage / stand / helper entity', not cancel_bad, cancel_bad[:3])
TRK = seq.tracks()
for name in ('intro', 'cs1', 'lead60', 'repel', 'lead5', 'lead_re', 'ending'):
    bad_c = []
    pts = {1, api.SEQ_LEN[name] // 2, api.SEQ_LEN[name]} | {t for _n, t, _v in want_sig if _n == name}
    pts |= {t for t, _c, _nm in TRK[name].cuts()} | {t + 2 for t, _c, _nm in TRK[name].cuts()} if name in TRK else set()
    for cut_at in sorted(t for t in pts if 0 <= t <= api.SEQ_LEN[name]):
        s, body, pl = world(F, (C0[0], api.CY, C0[2] - 4), 0.0, (C0[0], api.CY, C0[2] + 4), 180.0)
        args = {'at': 5} if name == 'repel' else {'g': 'a13'} if name == 'lead_re' else None
        run_seq(s, body, name, cut_at, start_args=args)
        s.call(f'{api.NS}seq/{name}/cancel', mcsim.Ctx(None, C0, (0.0, 0.0)))
        s.call(f'{api.NS}seq/{name}/cancel', mcsim.Ctx(None, C0, (0.0, 0.0)))
        rest = [sorted(e.tags) for e in s.ents if e.alive and (GONE & set(e.tags))]
        if rest or (s.sc('#mbCam', 'mb') or 0) != 0 or (s.sc('#mbNoLeash', 'mb') or 0) != 0:
            bad_c.append((cut_at, rest, s.sc('#mbCam', 'mb'), s.sc('#mbNoLeash', 'mb')))
    check(f'cancel: {name} cancelled (twice) at its cut / signal ticks leaves no sequence entity, no request, no leash flag', not bad_c, bad_c[:2])


# ================================================================ the skips
def cs0_world():
    st = api.ARENA_SPEC['start']
    s, body, pl = world(F, api.SEAT_POS, 0.0, (st['x'], api.CY, st['z']), 180.0)
    rock = mcsim.Ent('item_display', list(api.deco()['seat_rock']), (0.0, 0.0), ['rlk_room', 'rlk_mb_aux', api.TAGS['deco'], 'rlk_hr_deco_seat_rock'])
    s.ents.append(rock)
    return s, body, pl, rock


s, body, pl, rock = cs0_world()
run_seq(s, body, 'intro', 100)
d0 = math.dist(body.pos, pl.pos)
s.t = 101
s.call(f'{api.NS}seq/intro/skip', bctx(body))
d1 = math.dist(body.pos, pl.pos)
ovl = [m for t, m in kitcalls(s, 'hud/ovl') if t == 101]
faced = abs(((math.degrees(math.atan2(-(pl.pos[0] - body.pos[0]), pl.pos[2] - body.pos[2])) - body.rot[0]) + 540) % 360 - 180) < 1
props = [f for t, f, _ in s.log if t == 101 and f.endswith('rig/look/props/none')]
check(f'skip: CS0 from {d0:.1f} b: she stands {d1:.2f} b (= {api.CS0_END_F if hasattr(api, "CS0_END_F") else 6.5}) from the avatar, facing it; the black (0 / 20 / 6); the rock and props gone',
      abs(d1 - 6.5) < 0.05 and faced and ovl == [{'g': 'black', 'in': 0, 'hold': 20, 'out': 6}] and not rock.alive and props, (d1, ovl, rock.alive, props))
s.t = 102
s.setsc('#sq', 'hr', api.SKIP['intro']['to'])
s.call(f'{api.NS}seq/intro/tick', bctx(body))
nxt = [f for t, f, m in s.log if t == 102 and f.endswith('play/intro_end')]
for k in range(1, 5):
    s.t = 102 + k
    s.setsc('#sq', 'hr', api.SKIP['intro']['to'] + k)
    s.call(f'{api.NS}seq/intro/tick', bctx(body))
l11 = [(t, m) for t, m in kitcalls(s, 'hud/line')]
check(f'skip: the next tick (#sq {api.SKIP["intro"]["to"]}) plays intro_end; line 11 four ticks later', nxt == [f'{api.NS}rig/play/intro_end']
      and l11[-1:] == [(106, {'id': 11})], (nxt, l11[-2:]))
s, body, pl = world(F, (C0[0], api.CY, C0[2] - 6), 0.0, (C0[0], api.CY, C0[2] + 6), 180.0)
run_seq(s, body, 'cs1', 100)
s.t = 101
s.call(f'{api.NS}seq/cs1/skip', bctx(body))
d1 = math.hypot(body.pos[0] - pl.pos[0], body.pos[2] - pl.pos[2])
faced = abs(((math.degrees(math.atan2(-(pl.pos[0] - body.pos[0]), pl.pos[2] - body.pos[2])) - body.rot[0]) + 540) % 360 - 180) < 1
lk = {f.rsplit('rig/look/', 1)[1] for t, f, _ in s.log if t == 101 and '/rig/look/' in f}
check(f'skip: CS1 at 100: the black (0 / 20 / 6); she stands on her mark {d1:.2f} b (9.0) before the avatar, facing it; her clip at 565; the looks of 566',
      abs(d1 - 9.0) < 0.05 and faced and [m for t, m in kitcalls(s, 'hud/ovl') if t == 101] == [{'g': 'black', 'in': 0, 'hold': 20, 'out': 6}]
      and s.sc(('e', body.id), 'hrRigT') == api.SKIP['cs1']['to'] - 1 and {'sword/sheathed', 'hat/worn', 'scabbard/hip', 'props/none', 'face/calm'} <= lk,
      (d1, s.sc(('e', body.id), 'hrRigT'), sorted(lk)))
check('skip: the skip windows and targets of hr_design §3 (CS0 20-1270 -> 1290, CS1 40-560 -> 566)',
      api.SKIP == {'intro': {'window': (20, 1270), 'to': 1290}, 'cs1': {'window': (40, 560), 'to': 566}})


# ================================================================ the halo's bright looks in a run
def halo_world(record, body_at=api.SEAT_POS, pl_at=(api.ARENA_SPEC['start']['x'], api.CY, api.ARENA_SPEC['start']['z'])):
    """world() + the decor halo (an item_display tagged rlk_hr_deco_moon_halo at api.deco()) + the arena's look record."""
    s, body, pl = world(F, body_at, 0.0, pl_at, 180.0)
    s.ents.append(mcsim.Ent('item_display', list(api.deco()['moon_halo']), (0.0, 0.0),
                            ['rlk_room', 'rlk_mb_aux', api.TAGS['deco'], api.TAGS['deco_moon_halo']]))
    if record:
        s.storage.setdefault('rlk:mboss', {})[f'look_{api.AID}'] = record
    return s, body, pl


def halo_calls(s):
    return [(t, m.get('look')) for t, m in kitcalls(s, 'prop/moon_halo')]


runs = {}
for rec_ in ('moon', 'crimson', 'dark'):
    s, body, pl = halo_world(rec_)
    run_seq(s, body, 'intro', H1 + 10)
    runs[rec_] = halo_calls(s)
want_runs = {'moon': [(H0, 'p1b'), (H1, 'p1')], 'crimson': [(H0, 'p2b'), (H1, 'p2')], 'dark': []}
check(f'halo run: the intro brightens the halo at {H0} and puts it back at {H1} (moon p1b -> p1, crimson p2b -> p2, dark untouched)',
      runs == want_runs, runs)
ends = {}
for how in ('skip', 'cancel'):
    s, body, pl = halo_world('moon')
    run_seq(s, body, 'intro', H0 + 8)
    s.t = H0 + 9
    s.call(f'{api.NS}seq/intro/{how}', bctx(body) if how == 'skip' else mcsim.Ctx(None, C0, (0.0, 0.0)))
    ends[how] = halo_calls(s)
check(f'halo run: the skip and the intro cancel inside the bright window put it back (p1 at {H0 + 9})',
      all(v == [(H0, 'p1b'), (H0 + 9, 'p1')] for v in ends.values()), ends)

# ================================================================ the ending: an unmoving avatar, the landing, the turns, the distances
pl0 = (C0[0] + 2.0, float(api.CY), C0[2] + 6.0)
s, body, pl = halo_world('crimson', (pl0[0], api.CY, pl0[2] - 3.5), pl0)
body.data['eye'] = 1.74
dist, yaw_at, ys = {}, {}, {}


def each_end(k):
    dist[k] = math.hypot(body.pos[0] - pl.pos[0], body.pos[2] - pl.pos[2])
    yaw_at[k] = body.rot[0]
    ys[k] = body.pos[1]


run_seq(s, body, 'ending', api.SEQ_LEN['ending'], each=each_end)
toward = lambda yaw, a, b: abs(((math.degrees(math.atan2(-(a[0] - b[0]), a[2] - b[2])) - yaw) + 540) % 360 - 180)   # noqa: E731
far = [dist[k] for k in range(api.ev('ending', 'land'), api.ev('ending', 'walk') + 1)]
check(f'ending: from the landing ({api.ev("ending", "land")}) to the walk-in ({api.ev("ending", "walk")}) she stands 9.0 b from the unmoving '
      f'avatar ({min(far):.2f}-{max(far):.2f})', abs(min(far) - 9.0) < 0.06 and abs(max(far) - 9.0) < 0.06)
near_ = [dist[k] for k in range(api.ev('ending', 'stop'), api.SEQ_LEN['ending'] + 1)]
check(f'ending: after the walk-in ({api.ev("ending", "stop")}) to the end 4.5 b ({min(near_):.2f}-{max(near_):.2f})',
      abs(min(near_) - 4.5) < 0.06 and abs(max(near_) - 4.5) < 0.06)
land_err = toward(math.degrees(math.atan2(-(body.pos[0] - pl.pos[0]), body.pos[2] - pl.pos[2])), api.MOON_POS, pl.pos)
check(f'ending: she lands on the bearing from the avatar to the moon ({land_err:.1f} deg off; the mark passes mv/ok here)', land_err < 1.0)
moon_err = toward(yaw_at[api.ev('ending', 'turn') + 52], api.MOON_POS, body.pos)
check(f'ending: she faces the moon after the turn {api.ev("ending", "turn")}-{api.ev("ending", "turn") + 50} ({moon_err:.1f} deg off)', moon_err < 2.0)
pl_err = toward(yaw_at[api.ev('ending', 'pivot') + 23], pl.pos, body.pos)
check(f'ending: she faces the avatar again after the pivot {api.ev("ending", "pivot")}-{api.ev("ending", "pivot") + 22} ({pl_err:.1f} deg off)', pl_err < 2.0)
air = [k for k in ys if ys[k] < api.CY - 1e-6]
grounded = [k for k in range(api.ev('ending', 'land') + 1, api.SEQ_LEN['ending'] + 1) if abs(ys[k] - api.CY) > 1e-6]
check('ending: never below the floor; on the floor from the landing on', not air and not grounded, (air[:3], grounded[:3]))
check(f'halo run: the whole ending in the crimson look brightens the halo over the moon gaze ({G0} p2b, {G1} p2), nothing else',
      halo_calls(s) == [(G0, 'p2b'), (G1, 'p2')], halo_calls(s))

# ================================================================ review fixes that still hold (HR-02, HR-46, LF-02, HR-17)
# HR-02 / hr_design §3.1: only CS0's start moves the player (once, to its fixed stage, with view/sync); no other sequence
# teleports the player: the camera is the framework's
tp_pl = sorted(r for r, L in F.items() for l in L if re.search(r'as @a\[tag=player[^\]]*\][^|]* (?:tp|teleport) @s\b', l)
               or re.search(r'\b(?:tp|teleport) @a\[tag=player', l) or 'rlk:view/sync' in l)
check(f'HR-02 static: the player is teleported by CS0\'s start only (its fixed stage, with view/sync) ({sorted(set(tp_pl))})',
      set(tp_pl) == {'seq/intro/start'})
# HR-46: CS0's wind at the player (the listener is the camera the player is held on)
wind = [l for l in F['seq/intro/start'] if 'fx/snd/cs0_wind' in l]
check('HR-46: the CS0 wind plays at the player', wind and all(l.startswith('execute at @a[tag=player') for l in wind), wind)
# LF-02: absolute facings keep x / z exact (the game block-centres a whole x / z)
loose = [l for r, L in F.items() for l in L
         for m in re.finditer(r'facing (-?\d[\d.]*) (-?\d[\d.]*) (-?\d[\d.]*)', l) if '.' not in m.group(1) or '.' not in m.group(3)]
check('LF-02: every absolute facing keeps x / z exact (api.xyz)', not loose and api.xyz(api.MOON_POS, 3) in ALL, loose[:2])
# HR-17: the repel's kick flash is made between fx/keep_on and fx/keep_off (the kick kills her in that tick: death_start's fx/clear)
kick = [(r, L) for r, L in F.items() if r.startswith('seq/repel/') and any('fx/p/kick_flash' in l for l in L)]
check('HR-17: the kick flash is kept (keep_on .. kick_flash .. keep_off in its tick file)', kick and all(
    [i for i, l in enumerate(L) if l.endswith('fx/keep_on')] and
    max(i for i, l in enumerate(L) if l.endswith('fx/keep_on')) < min(i for i, l in enumerate(L) if 'fx/p/kick_flash' in l)
    and any(l.endswith('fx/keep_off') for l in L[min(i for i, l in enumerate(L) if 'fx/p/kick_flash' in l):]) for r, L in kick),
    [r for r, _ in kick])

if A.v:
    print('\n'.join('ok   ' + x for x in OK))
print(f'ev_dry: {len(OK)} passed, {len(FAIL)} failed')
sys.exit(1 if FAIL else 0)

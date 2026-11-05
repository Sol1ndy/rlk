#!/usr/bin/env python3
"""ev_dry.py [--dp ROGUELIKE] — S2b's sequence suite of 홍련 (Scarlet): seq.py's services built with a dummy Writer and dry-run
in mcsim (run from HR/tests, outside the datapack; PLAN §7.6 / §9.3, the S2b brief ⑤).

  build    SERVICES = one api.Service per api.SEQS (clips api.SEQ_CLIPS, args api.SEQ_ARGS); a dummy Writer: every file under
           seq/<its own name>/, the entry points start / tick / cancel (+ intro/skip, lead_stand/g/<g>), the macro starts take
           exactly their api.SEQ_ARGS; the kit / theme / reward off -> no fx / look / ev line and no empty line; deterministic
  refs     every function a sequence calls: its own seq/** files, rig/** (api.RIG_CALLS, play / start of api.CLIPS), the kit
           through api.K (contract names and args), the framework (mboss/**, view/sync), ev/apply + ev/title (api.ev_apply /
           ev_title) — nothing else; no negative add / remove literals; lowercase resource ids; every summon rotated after it
  ticks    every tick a sequence uses <= its length (api.SEQ_LEN; the intro = intro + intro_end); #sqdone at the length; the
           staging marker at tick 0; the lines at api.LINE_AT (each of 1-25 but 12 once), music at api.MUSIC_AT, the title at
           intro_end draw, the looks (crimson at cs1 recolour, dark at the sq1 / lead-in dark events), the warning banner only
           there and only for a lethal gauntlet (both switch values), #sq_sig only = api.SIG at api.COUNTER_EV / refill
  event    (mcsim, both branches x 8 player positions incl. 20 b away): 120 t; the line at E4 cleared at E52 (< E56), the grant
           + title once at E56, the black at E110 (10 / 12 / 0), ev_leave at E34, state/hidden at E40; the thrown sword
           (item_display of api.ITEM_MODEL, rlk_room rlk_mb_aux rlk_hr_ev): rotated in its summon tick, one end-over-end turn
           <= 30 deg / t, never below the floor (centre >= floor + its radius at its scale), at E44 0.9 b before the player's
           chest along their facing, shrinking 1 -> 0.15 into the player's hand, gone at E56; the moonlight orb (marker) from
           her left hand to the player's chest at E42; every kit call a contract name; cancel at every tick leaves nothing
  skip     seq/intro/skip from 30 b: the black, the rock and props gone, her <= 7 b from the player facing them; the next tick
           (#sq 554) plays intro_end with line 11
  cs4      the ending with an unmoving player (the framework's real mv/* movers each tick): her distance over 300-1042 stays
           3.5-6 b; she lands toward the moon; she faces the moon at 526 and the player again at 815
  halo     (I1b verification round 1) S3's decor moon halo in the bright look of the arena's look (moon p1b, crimson p2b; dark
           none) over CS0 E3 (raise + 2 .. l4) and the CS4 gaze (gaze .. gaze + 90), back to p1 / p2 after, restored by
           intro/skip and the intro / ending cancel: the tick files (nowhere else) and runs in the mcsim world
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
S = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
_wt = next((p for p in ('hr/wt_s2b/roguelike', 'hr/wt_s2a/roguelike') if (S / p).exists()), 'hr/wt_s2b/roguelike')
ap = argparse.ArgumentParser()
ap.add_argument('--dp', default=os.environ.get('HR_DP', str(S / _wt)))
ap.add_argument('-v', action='store_true', help='list the passed checks too')
A = ap.parse_args()
DP = Path(A.dp)
FN = DP / 'data/rlk/function'
sys.path.insert(0, str(DP / 'tools'))
sys.path.insert(0, str(HERE / 'lib'))
import mcsim  # noqa: E402
from mboss_scarlet import api  # noqa: E402

FAIL, OK = [], []


def check(label, cond, detail=''):
    (OK if cond else FAIL).append(label)
    if not cond:
        print('FAIL ' + label + (('  ' + str(detail)) if detail else ''))


# ================================================================ build (a dummy Writer, the kit / theme / reward forced)
class DW:
    def __init__(self):
        self.files = {}

    def w(self, rel, body):
        assert rel.startswith(api.OWN['S2b']), rel
        if rel in self.files:
            raise AssertionError(f'written twice: {rel}')
        self.files[rel] = list(body)


def build(on=True, patch=None):
    saved = (api.K._on, api.theme_ready, api.reward_ready, api.ULT60_LETHAL, api.ULT5_LETHAL, api.EVENT['lines'])
    # I1: the off build forces all three off too (on the merged tree reward.py is real; after I1b the kit and theme are)
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
        if 'K' in dir(api):
            try:
                del api.K._on
            except AttributeError:
                pass
        api.theme_ready, api.reward_ready = saved[1], saved[2]
        api.ULT60_LETHAL, api.ULT5_LETHAL, api.EVENT['lines'] = saved[3], saved[4], saved[5]


seq, F, OWNER = build(True)
_, F2, _ = build(True)
seq_off, FOFF, _ = build(False)
check('build: two builds identical (deterministic)', F == F2)
check(f'build: SERVICES = api.SEQS ({[s.name for s in seq.SERVICES]})', [s.name for s in seq.SERVICES] == list(api.SEQS))
check('build: Service clips = api.SEQ_CLIPS, args = api.SEQ_ARGS',
      all(tuple(s.clip) == tuple(api.SEQ_CLIPS[s.name]) and s.args == dict(api.SEQ_ARGS.get(s.name, {})) for s in seq.SERVICES))
check(f'build: every file under seq/** ({len(F)} files; kit off {len(FOFF)})', all(r.startswith('seq/') for r in list(F) + list(FOFF)))
check('build: each service writes only under seq/<its name>/', all(all(r.startswith(f'seq/{n}/') for r in rs) for n, rs in OWNER.items()))
need = [f'seq/{n}/{p}' for n in api.SEQS for p in ('start', 'tick', 'cancel')] + ['seq/intro/skip'] + \
    [f'seq/lead_stand/g/{g}' for g in api.SEQ_ARGS['lead_stand']['g']]
check('build: entry points start / tick / cancel of the 8, intro/skip, lead_stand/g/<g>', all(r in F and r in FOFF for r in need),
      [r for r in need if r not in F])
macro_args = {n: sorted(set(re.findall(r'\$\((\w+)\)', '\n'.join(F[f'seq/{n}/start'])))) for n in api.SEQS}
check('build: the macro starts take exactly api.SEQ_ARGS (repel at, lead_stand g; the others none)',
      macro_args == {n: sorted(api.SEQ_ARGS.get(n, {})) for n in api.SEQS}, macro_args)
dollar = [r for r, L in F.items() if any(l.startswith('$') for l in L) and r not in ('seq/repel/start', 'seq/lead_stand/start')]
check('build: no other macro file', not dollar, dollar)
empty = [r for r, L in list(F.items()) + list(FOFF.items()) if any(not l.strip() or l.rstrip().endswith(' run') for l in L)]
check('build: no empty or dangling line (kit on and off)', not empty, empty[:4])
off_fx = [r for r, L in FOFF.items() if any('/fx/' in l or 'mboss/arena/' in l or '/ev/' in l or '#hrLook' in l for l in L)]
check('build: the kit / theme / reward off -> no fx, look or ev line', not off_fx, off_fx[:4])
ALL = '\n'.join(l for L in F.values() for l in L if not l.startswith('#'))
# a macro line's $(g) / $(at) expanded with its api.SEQ_ARGS values
ALL_REF = ALL + '\n' + '\n'.join(l.replace('$(g)', g) for l in ALL.split('\n') if '$(g)' in l for g in api.SEQ_ARGS['lead_stand']['g'])

# ================================================================ refs
refs = {r for r in re.findall(r'function (rlk:[a-z0-9_/.\-]+)', ALL_REF) if not r.endswith('/')}
own = {f'{api.NS}{r}' for r in F}
manifest = json.loads((DP / 'tools/scarlet_rig_manifest.json').read_text())
rig_ok = {f'{api.NS}rig/{c}' for c in api.RIG_CALLS} | {f'{api.NS}rig/play/{c}' for c in api.CLIPS} | {f'{api.NS}rig/start/{c}' for c in api.CLIPS}
kit_ok = {f'{api.NS}fx/p/{n}' for n in api.KIT_PRESETS} | {f'{api.NS}fx/prop/{n}' for n in api.KIT_PROPS} | \
    {f'{api.NS}fx/snd/{n}' for n in api.KIT_SOUNDS} | {f'{api.NS}fx/hud/{n}' for n in api.KIT_HUD} | {f'{api.NS}fx/{n}' for n in api.KIT_FIXED}
ev_ok = {f'{api.NS}ev/apply', f'{api.NS}ev/title'}
fw = {r for r in refs if r.startswith('rlk:mboss/') or r == 'rlk:view/sync'}
bad = sorted(r for r in refs - own - rig_ok - kit_ok - ev_ok - fw)
check('refs: only seq/**, rig/** (contract calls), the kit (contract names), ev/apply / ev/title and the framework', not bad, bad)
fw_missing = sorted(r for r in fw if not (FN / (r.split(':', 1)[1] + '.mcfunction')).exists() and not r.startswith('rlk:mboss/arena/'))
check(f'refs: every framework function exists ({sorted(fw)})', not fw_missing, fw_missing)
rig_missing = sorted(r for r in refs if r.startswith(f'{api.NS}rig/') and not (FN / (r.split(':', 1)[1] + '.mcfunction')).exists())
check('refs: every rig call exists in rig/**', not rig_missing, rig_missing)
own_missing = sorted(r for r in refs if r.startswith(f'{api.NS}seq/') and r not in own)
check('refs: every seq/** call is a written file', not own_missing, own_missing)
# the kit calls carry their contract args
args_bad = []
for name, a in re.findall(r'function rlk:boss/scarlet/fx/(?:p|prop|hud)/(\w+)(?: (\{[^}]*\}|with storage \S+ \S+))?', ALL):
    if a.startswith('with storage'):
        # F2 (HR-32): the compound the call reads (set in the same tick file) holds exactly the contract args
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
txt = [l for l in ALL.split('\n') if re.search(r'^(?:execute .* run )?(tellraw|title @|say )', l)]
check('static: no raw on-screen text (lines, overlays, the banner only through the kit)', not txt, txt[:2])
korean = sorted({x for l in ALL.split('\n') for x in re.findall(r'"([^"\n]*[가-힣][^"\n]*)"', l)})
check(f'static: the only literal on-screen words are the title / sub ({korean})', set(korean) <= {api.NAME, api.SUB})
cam = [l for l in ALL.split('\n') if re.search(r'\b(spectate|gamemode|inputPermission|attribute .*movement_speed)\b', l)]
check('static: no camera, no input lock', not cam, cam[:2])
evtag = [l for l in F['seq/event/k/30'] if 'summon' in l]
check('static: the event entities carry rlk_room rlk_mb_aux rlk_hr_ev', evtag and all('"rlk_room","rlk_mb_aux","rlk_hr_ev"' in l for l in evtag), evtag[:1])

# ================================================================ ticks, lines, music, looks, banner, signals
SQ = re.compile(r'#sq hr matches (\d+)(\.\.)?(\d+)?')


def ticks_of(name, files=F):
    out = {0: files[f'seq/{name}/start']}
    for r, L in files.items():
        m = re.match(rf'seq/{name}/k/(\d+)$', r)
        if m:
            out[int(m.group(1))] = L
    return out


T = {n: ticks_of(n) for n in api.SEQS}
over = {n: max(T[n]) for n in api.SEQS if max(T[n]) > api.SEQ_LEN[n]}
check('ticks: every tick a sequence uses <= its length (api.SEQ_LEN)', not over, over)
done = {n: f'execute if score #sq hr matches {api.SEQ_LEN[n]}.. run scoreboard players set #sqdone hr 1' in F[f'seq/{n}/tick'] for n in api.SEQS}
check('ticks: #sqdone at the length in every tick function, #sqdone 0 at start', all(done.values())
      and all('scoreboard players set #sqdone hr 0' in F[f'seq/{n}/start'] for n in api.SEQS), done)
disp = {n: sorted({int(m.group(1)) for l in F[f'seq/{n}/tick'] + [x for r, L in F.items() if r.startswith(f'seq/{n}/b/') for x in L]
                   for m in [SQ.search(l)] if m and not m.group(2)}) for n in api.SEQS}
check('ticks: the dispatch reaches exactly the tick files', all(disp[n] == sorted(t for t in T[n] if t) for n in api.SEQS))
check('ticks: the staging marker (rlk_hr_stage) at tick 0 of every sequence', all(any('rlk_hr_stage' in l and 'summon' in l for l in T[n][0]) for n in api.SEQS))
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
check('lines: each of 1-25 (but 12, A6 is the core\'s) exactly once at api.LINE_AT (24 / 25 the event at E4)', not wrong and 12 not in placed, wrong)
mus = sorted((n, t, int(m)) for n in api.SEQS for t, L in T[n].items() for l in L for m in re.findall(r'mboss/music/set \{ph:(\d)\}', l))
want_mus = sorted((('intro' if c == 'intro_end' else c), (api.SKIP_T if c == 'intro_end' else 0) + api.ev(c, e), ph) for ph, (c, e) in api.MUSIC_AT.items())
check(f'music: api.music(ph) at api.MUSIC_AT ({mus})', mus == want_mus, want_mus)
title = [(n, t) for n in api.SEQS for t, L in T[n].items() for l in L if 'mboss/title' in l]
check('title: mboss_lib.title(*api.TITLE) once at intro_end draw', title == [('intro', api.SKIP_T + api.ev('intro_end', 'draw'))]
      and L_ok if (L_ok := api.L.title(*api.TITLE) in ALL) else False, title)
looks = sorted((n, t, l.split()[-1]) for n in api.SEQS for t, L in T[n].items() for l in L if '#hrLook' in l)
want_looks = sorted([('cs1', api.ev('cs1', 'recolour'), str(api.LOOK_ID['crimson'])), ('sq1', api.ev('sq1', 'dark'), str(api.LOOK_ID['dark'])),
                     ('lead_down', api.ev('lead_down', 'dark'), str(api.LOOK_ID['dark'])), ('lead_stand', api.ev('lead_stand', 'dark'), str(api.LOOK_ID['dark']))])
check(f'looks: crimson at cs1 recolour, dark at the sq1 / lead-in dark events ({looks})', looks == want_looks, want_looks)
phase = [(n, t) for n in api.SEQS for t, L in T[n].items() for l in L if 'look/phase/' in l]
check('looks: the rig P2 accents at cs1 recolour', phase == [('cs1', api.ev('cs1', 'recolour'))], phase)
# I1b verification round 1 (m4): the decor halo's bright looks (requests s1k-3 / s2b-4, contract §7), gated on the arena's look
# record (moon -> p1b, crimson -> p2b; dark: no line), back after, restored by the skip and the intro / ending cancel
HALO_RE = re.compile(re.escape(f'look_{api.AID}:"') + r'(\w+)"\}' + re.escape(f' as @e[type=minecraft:item_display,tag='
                                                                             f'{api.TAGS["deco_moon_halo"]}] run function '
                                                                             f'{api.NS}fx/prop/moon_halo {{look:"') + r'(\w+)"\}')
halo_at = {r: sorted(m.groups() for l in L for m in [HALO_RE.search(l)] if m) for r, L in F.items()}
halo_at = {r: v for r, v in halo_at.items() if v}
BRIGHT, BACK = [('crimson', 'p2b'), ('moon', 'p1b')], [('crimson', 'p2'), ('moon', 'p1')]
H0, H1 = api.ev('intro', 'raise') + 2, api.ev('intro', 'l4')
G0, G1 = api.ev('ending', 'gaze'), api.ev('ending', 'gaze') + 90
want_halo = {f'seq/intro/k/{H0}': BRIGHT, f'seq/intro/k/{H1}': BACK, f'seq/ending/k/{G0}': BRIGHT, f'seq/ending/k/{G1}': BACK,
             'seq/intro/skip': BACK, 'seq/intro/cancel': BACK, 'seq/ending/cancel': BACK}
halo_any = sorted(r for r, L in F.items() if any('fx/prop/moon_halo' in l for l in L))
check(f'halo: p1b / p2b by the arena look at intro {H0} and ending {G0}, p1 / p2 at {H1} and {G1}, the same restore in intro/skip and '
      f'the intro / ending cancel, no other halo line ({halo_any})', halo_at == want_halo and halo_any == sorted(want_halo),
      {r: (halo_at.get(r), want_halo.get(r)) for r in set(halo_at) | set(want_halo) if halo_at.get(r) != want_halo.get(r)})


def banners(files):
    out = []
    for n in api.SEQS:
        for t, L in ticks_of(n, files).items():
            for l in L:
                if 'fx/hud/warn {on:1}' in l:
                    g = re.search(r'#sq_g hr matches (\d+)', l)
                    out.append((n, t, int(g.group(1)) if g else None))
    return sorted(out)


B = {}
for a60 in (False, True):
    for a5 in (False, True):
        B[(a60, a5)] = banners(build(True, {'ULT60_LETHAL': a60, 'ULT5_LETHAL': a5})[1])
exp = lambda a60, a5: sorted(([('sq1', api.ev('sq1', 'dark'), None), ('lead_stand', api.ev('lead_stand', 'dark'), 8)] if a60 else [])
                             + ([('lead_down', api.ev('lead_down', 'dark'), None), ('lead_stand', api.ev('lead_stand', 'dark'), 13)] if a5 else []))
check('banner: on only at the dark event of a gauntlet whose fail is lethal (ULT60 / ULT5 both ways; lead_stand per {g})',
      all(B[k] == exp(*k) for k in B), {k: B[k] for k in B if B[k] != exp(*k)})
check('banner: default switches -> A13 only (lead_down, lead_stand {g:a13})', B[(api.ULT60_LETHAL, api.ULT5_LETHAL)] == exp(api.ULT60_LETHAL, api.ULT5_LETHAL))
sigs = sorted((n, t, int(v)) for n in api.SEQS for t, L in T[n].items() for l in L for v in re.findall(r'#sq_sig hr (\d+)', l))
want_sig = sorted([('repel', api.ev('repel', e), api.SIG[f'hp{i + 1}']) for i, e in enumerate(api.COUNTER_EV)]
                  + [('lead_down', api.ev('lead_down', 'refill'), api.SIG['refill']), ('lead_stand', api.ev('lead_stand', 'refill'), api.SIG['refill'])])
check(f'signal: #sq_sig = api.SIG only at repel COUNTER_EV (24 / 75 / 102) and the lead-ins\' refill ({sigs})', sigs == want_sig, want_sig)
core = [l for l in ALL.split('\n') for f in re.findall(r'function (rlk:boss/scarlet/\S+)', l)
        if not f.startswith(('rlk:boss/scarlet/seq/', 'rlk:boss/scarlet/rig/', 'rlk:boss/scarlet/fx/', 'rlk:boss/scarlet/ev/'))]
check('signal: no call into the core (only #sq_sig)', not core, core[:2])
blk = [l for l in F['seq/event/k/' + str(api.EV_T['black'])] if 'ovl' in l]
check('event: the black at E110 = ovl black in 10 hold 12 out 0', any('{g:"black",in:10,hold:12,out:0}' in l for l in blk), blk)
nl = build(True, {'lines': False})[1]
check('event: EVENT[lines] off -> no line 24 / 25 (a wordless coda)', not re.search(r'line \{id:2[45]\}', '\n'.join(l for L in nl.values() for l in L)))


# ================================================================ the mcsim world
class Sim(mcsim.Sim):
    STUB = ('rlk:boss/scarlet/fx/', 'rlk:boss/scarlet/ev/', 'rlk:mboss/title', 'rlk:mboss/music/', 'rlk:mboss/push/', 'rlk:mboss/pull/')
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
                q, sc = tr.get('left_rotation'), (tr.get('scale') or [1.5])[0]
                if not q:
                    rot_bad.append((tag, k, 'no transformation'))
                    continue
                tip = qrot(q, (-.7071068, .7071068, 0.0))
                lowest = pos[1] - abs(tip[1]) * 0.737 * sc - .02
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
check('event: it sinks into the player\'s hand (scale 1 -> 0.15 at E55, at the hand)', not shrink_bad, shrink_bad[:3])
check('event: the moonlight orb E30-E42 from her left hand onto the player\'s chest (E41 one step short), above the floor', not orb_bad, orb_bad[:3])
check('event: nothing left after E120 (rlk_hr_ev, helpers)', not left, left[:2])

# cancel at every tick (both branches, the event and every other sequence) leaves none of its entities
cancel_bad = []
for br, code in (('item', 1), ('buff', 2)):
    for cut_at in range(0, api.SEQ_LEN['event'] + 1, 1):
        s, body, pl = world(F, (C0[0], api.CY, C0[2] - 4), 0.0, (C0[0], api.CY, C0[2]), 180.0, code)
        s.call(f'rlk:boss/scarlet/rig/play/ending', bctx(body))
        run_seq(s, body, 'event', cut_at)
        s.call(f'{api.NS}seq/event/cancel', mcsim.Ctx(None, C0, (0.0, 0.0)))
        s.call(f'{api.NS}seq/event/cancel', mcsim.Ctx(None, C0, (0.0, 0.0)))
        rest = [sorted(e.tags) for e in s.ents if e.alive and ({'rlk_hr_ev', 'rlk_hr_sqh', 'rlk_hr_stage'} & set(e.tags))]
        if rest:
            cancel_bad.append((br, cut_at, rest))
check('event: cancel (twice, no executor) at every tick E0-E120 leaves no rlk_hr_ev / stage / helper entity', not cancel_bad, cancel_bad[:3])
for name in ('intro', 'cs1', 'sq1', 'repel', 'lead_down', 'lead_stand', 'ending'):
    bad_c = []
    for cut_at in sorted(set(list(range(0, api.SEQ_LEN[name] + 1, 7)) + [t for t in T[name] if t] )):
        s, body, pl = world(F, (C0[0], api.CY, C0[2] - 4), 0.0, (C0[0], api.CY, C0[2] + 4), 180.0)
        args = {'at': 5} if name == 'repel' else {'g': 'a13'} if name == 'lead_stand' else None
        run_seq(s, body, name, cut_at, start_args=args)
        s.call(f'{api.NS}seq/{name}/cancel', mcsim.Ctx(None, C0, (0.0, 0.0)))
        rest = [sorted(e.tags) for e in s.ents if e.alive and ({'rlk_hr_sqp', 'rlk_hr_sqh', 'rlk_hr_stage', 'rlk_hr_ev'} & set(e.tags))]
        if rest:
            bad_c.append((cut_at, rest))
    check(f'cancel: {name} cancelled at its event ticks (and every 7 t) leaves no sequence entity', not bad_c, bad_c[:2])

# ================================================================ the intro skip
s, body, pl = world(F, api.SEAT_POS, 0.0, (api.ARENA_SPEC['start']['x'], api.CY, api.ARENA_SPEC['start']['z']), 180.0)
rock = mcsim.Ent('item_display', list(api.deco()['seat_rock']), (0.0, 0.0), ['rlk_room', 'rlk_mb_aux', api.TAGS['deco'], 'rlk_hr_deco_seat_rock'])
s.ents.append(rock)
run_seq(s, body, 'intro', 100)
d0 = math.dist(body.pos, pl.pos)
s.t = 101
s.call(f'{api.NS}seq/intro/skip', bctx(body))
d1 = math.dist(body.pos, pl.pos)
ovl = [m for t, m in kitcalls(s, 'hud/ovl') if t == 101]
faced = abs(((math.degrees(math.atan2(-(pl.pos[0] - body.pos[0]), pl.pos[2] - body.pos[2])) - body.rot[0]) + 540) % 360 - 180) < 1
props = [f for t, f, _ in s.log if t == 101 and f.endswith('rig/look/props/none')]
check(f'skip: from {d0:.1f} b she stands {d1:.2f} b (<= 7) from the player, facing them; the black (0 / 20 / 6); the rock and props gone',
      d1 <= 7.0 + 1e-6 and faced and ovl == [{'g': 'black', 'in': 0, 'hold': 20, 'out': 6}] and not rock.alive and props, (ovl, rock.alive, props))
s.setsc('#sq', 'hr', api.SKIP_T - 1)
s.t = 102
s.setsc('#sq', 'hr', api.SKIP_T)
s.call(f'{api.NS}seq/intro/tick', bctx(body))
nxt = [(f, m) for t, f, m in s.log if t == 102 and (f.endswith('play/intro_end') or f.endswith('hud/line'))]
check('skip: the next tick (#sq 554) plays intro_end with line 11', nxt == [(f'{api.NS}rig/play/intro_end', {}), (f'{api.NS}fx/hud/line', {'id': 11})], nxt)

# ================================================================ the halo's bright looks in a run (I1b verification round 1, m4)
def halo_world(record, body_at=api.SEAT_POS, pl_at=(api.ARENA_SPEC['start']['x'], api.CY, api.ARENA_SPEC['start']['z'])):
    """world() + S3's decor halo (an item_display tagged rlk_hr_deco_moon_halo at api.deco()) + the arena's look record."""
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
PL_E = (C0[0] + 2.0, float(api.CY), C0[2] + 6.0)        # the CS4 run's positions (below)
s, body, pl = halo_world('crimson', (PL_E[0], api.CY, PL_E[2] - 3.5), PL_E)
run_seq(s, body, 'ending', G0 + 10)
s.t = G0 + 11
s.call(f'{api.NS}seq/ending/cancel', mcsim.Ctx(None, C0, (0.0, 0.0)))
check(f'halo run: the ending cancel inside the gaze puts it back (crimson: p2b at {G0}, p2 at {G0 + 11})',
      halo_calls(s) == [(G0, 'p2b'), (G0 + 11, 'p2')], halo_calls(s))

# ================================================================ CS4: the distance to an unmoving player, the landing, the turns
pl0 = (C0[0] + 2.0, float(api.CY), C0[2] + 6.0)
s, body, pl = halo_world('crimson', (pl0[0], api.CY, pl0[2] - 3.5), pl0)      # I1b round 1: + the halo (P2's crimson look)
body.data['eye'] = 1.74
av = mcsim.Ent('armor_stand', list(pl0), (90.0, 0.0), ['rlk_av'])            # F2 (HR-02): an F5 avatar beside the player
pl.rot = [90.0, 20.0]
s.ents.append(av)
dist, yaw_at, start_view, band_at = {}, {}, {}, {}


def each_cs4(k):
    dist[k] = math.hypot(body.pos[0] - pl.pos[0], body.pos[2] - pl.pos[2])
    yaw_at[k] = body.rot[0]
    if k == 0:
        start_view.update(pl=(list(pl.pos), list(pl.rot)), av=(list(av.pos), list(av.rot)), her=list(body.pos))
    if k == api.ev('ending', 'band'):
        band_at.update(sw=(s.storage.get('rlk:hr', {}).get('seq', {}).get('band', {}) or {}).get('sw'),
                       dist=s.sc('#mbDist', 'mb'), d=math.hypot(body.pos[0] - pl.pos[0], body.pos[2] - pl.pos[2]))


run_seq(s, body, 'ending', api.SEQ_LEN['ending'], each=each_cs4)
late = [dist[k] for k in range(300, api.SEQ_LEN['ending'] + 1)]
check(f'cs4: her distance to an unmoving player over 300-1042 stays 3.5-6 b ({min(late):.2f}-{max(late):.2f})', 3.5 <= min(late) and max(late) <= 6.0)
mx, my, mz = api.MOON_POS
land = (dist.get(api.ev('ending', 'land')), )
bear = lambda k: math.degrees(math.atan2(-(mx - body.pos[0]), mz - body.pos[2]))
toward = lambda yaw, a, b: abs(((math.degrees(math.atan2(-(a[0] - b[0]), a[2] - b[2])) - yaw) + 540) % 360 - 180)
check(f'cs4: the landing ~10 b from the player ({dist[api.ev("ending", "land")]:.1f} b)', 8.5 <= dist[api.ev('ending', 'land')] <= 11)
moon_err = toward(yaw_at[api.ev('ending', 'turn') + 20], api.MOON_POS, body.pos)
check(f'cs4: she faces the moon after the turn 506-526 ({moon_err:.1f} deg off)', moon_err < 2.0)
pl_err = toward(yaw_at[api.ev('ending', 'pivot') + 21], pl.pos, body.pos)
check(f'cs4: she faces the player again after the pivot 794-815 ({pl_err:.1f} deg off)', pl_err < 2.0)
check('cs4: on the floor from 268 on (no float after the landing)', all(abs(body.pos[1] - api.CY) < 1e-6 for _ in [0]))
check(f'halo run: the whole ending in the crimson look brightens the halo over the gaze ({G0} p2b, {G1} p2), nothing else',
      halo_calls(s) == [(G0, 'p2b'), (G1, 'p2')], halo_calls(s))

# ================================================================ F2 review fixes (HR-02, HR-17, HR-32, HR-46, LF-02)
# HR-02: the dying facing turns the player (toward her eyes, from their own eyes) and the avatar (toward her feet) with
# `rotate`: nothing teleports the player (a tp would dismount the F5 seat and move the avatar), no view/sync
tp_pl = [(r, l) for r, L in F.items() for l in L if re.search(r'as @a\[tag=player[^\]]*\][^|]* (?:tp|teleport) @s\b', l)
         or re.search(r'\b(?:tp|teleport) @a\[tag=player', l) or 'rlk:view/sync' in l]
check('HR-02 static: no sequence teleports the player or calls view/sync', not tp_pl, tp_pl[:3])
(ppos, prot), (apos, arot), her = start_view['pl'], start_view['av'], start_view['her']
want_y = math.degrees(math.atan2(-(her[0] - ppos[0]), her[2] - ppos[2]))
want_p = math.degrees(-math.atan2(her[1] + 1.74 - (ppos[1] + 1.62), math.hypot(her[0] - ppos[0], her[2] - ppos[2])))
check(f'HR-02: the ending start turns the player toward her eyes in place (yaw {prot[0]:.1f} / {want_y:.1f}, pitch {prot[1]:.1f} / '
      f'{want_p:.1f})', ppos == list(pl0) and abs((prot[0] - want_y + 540) % 360 - 180) < 0.5 and abs(prot[1] - want_p) < 0.5)
check(f'HR-02: and the avatar toward her feet in place (yaw {arot[0]:.1f})', apos == list(pl0)
      and abs((arot[0] - math.degrees(math.atan2(-(her[0] - apos[0]), her[2] - apos[2])) + 540) % 360 - 180) < 0.5 and abs(arot[1]) < 0.5)
# HR-32: CS4 E1b's band sweeps her distance to the player + 1 b (it passes over them), its args through storage seq.band
band_calls = [l for r, L in F.items() if r.startswith('seq/ending/') for l in L if 'fx/p/qi_band' in l]
check('HR-32: the E1b band reads its args from storage rlk:hr seq.band', band_calls and all('with storage rlk:hr seq.band' in l
                                                                                         for l in band_calls), band_calls[:1])
check(f'HR-32: the band sweeps her distance + 1 b ({band_at})', band_at.get('sw') is not None and band_at['dist'] is not None
      and band_at['sw'] == band_at['dist'] + 10 and band_at['sw'] / 10 >= band_at['d'] + 0.9)
# HR-46: CS0's wind at the player (at her seat, 26.7 b away, its minVolume 0 sent it to no one)
wind = [l for l in F['seq/intro/start'] if 'fx/snd/cs0_wind' in l]
check('HR-46: the E0 wind plays at the player', wind and all(l.startswith('execute at @a[tag=player') for l in wind), wind)
# LF-02: the ending's moon target written exactly (x / z with a decimal point: the game block-centres a whole x / z)
loose = [l for r, L in F.items() if r.startswith('seq/ending/') for l in L
         for m in re.finditer(r'facing (-?\d[\d.]*) (-?\d[\d.]*) (-?\d[\d.]*)', l) if '.' not in m.group(1) or '.' not in m.group(3)]
check('LF-02: every absolute facing of the ending keeps x / z exact (api.xyz)', not loose and api.xyz(api.MOON_POS, 3) in ALL,
      loose[:2])
# HR-17: CS3's kick flash is made between fx/keep_on and fx/keep_off (the kick kills her in that tick: death_start's fx/clear)
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

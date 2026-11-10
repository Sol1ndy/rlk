#!/usr/bin/env python3
"""pat_ghost.py: the ghost patterns of 홍련 (Scarlet), stage S4 (scratchpad hr/PLAN.md §4.4-4.5, §5, §9.3; contract §3.5-3.6):
R1 자영 돌격, R2 월륜 일섬, R3 자영 활강 and the gauntlets A8 / A13 (tools/mboss_scarlet/p_ghost.py) with the helpers g/**.

    python3 pat_ghost.py <datapack root> [-v] [section ...]

Run it from HR/tests: the tree is only read; the variant (her registry entry forced enabled, the core regenerated, a real
copy of F:boss/scarlet; the kit / theme sections a dry rebuild inside it with api.K and the theme forced on) lives in
./tmp and is removed at the end. Sections:

  table   p_ghost.TABLE / EVENTS (a dry build): every cut = its script row (made / lock / strike / tier / kb), every strike =
          the contact (row t + clip 'hit') of exactly one move = api.HITS; 9 counting cuts per gauntlet (api.CUT_IDS), R1 / R3
          never count; the discs at DISC_RELEASE; tells >= TELL_MIN 12 (no cut is big: 32 b^2), the yellow tell >= TELL_BIG
          20 before the first disc; hits >= COMBO_GAP 10 apart; lock = strike - LOCK_LEAD 7; kb 0 except the scripts' last
          hits (R1 cut 3, R3 cut 2: kb 3) and R2's last disc (kb 2); every effect / sound / look of PLAN §4.5's move table
          at its clip event (row t + api.ev), the bolts at api.BOLTS
  files   the generated files: start / tick / cancel; the cut builder's macro args = api.CUT_ARGS, every api.cut() line at
          its tick, n 1 only in the gauntlets; quiet (#hzQuiet 1, no #hzVis), no setblock / fill / block or text display (no
          decal); hz only in g/cut/make, pj/launch only in g/disc/throw (summoned, then rotated, then launched); no negative
          literal in scoreboard add / remove; nothing below the floor; every tp through a spot or mv/ok; own fake players
          #g_* / #r2_* only; every referenced function exists
  hits    the sim (standing player, 2 spots): every hazard made at its made tick, tell strike - made, r 3.2, act 2, quiet,
          no sound, Electro, the tier's %, kb; the player hit exactly once per cut, at its strike; the discs after release
  follow  a walking player: every cut on the player's floor spot each tick until its lock, fixed from the lock to the strike
  pips    four dash agents (stand-then-dash; move-then-dash outward / sideways / inward at 0.22 and 0.28 b/t), dashes at
          strike - 2 +- 2: each scores >= 90 % of its dashes (shield/take) and is never hit by a cut; the 2-charge dasher
          (F:player/dash + dash_regen + dash_refill: 2 charges, 20 t each in sequence, 5-t self-cooldown) reaches every
          counting window of both gauntlets
  discs   R2 / A13: one card per disc (item display, rlk_hr_disc), aimed at the player's position at release, 0.9 b over
          the floor, 2.0 b per tick (1.8 asked, 0.25 b sub-steps), no homing, life 16, wall stop; R2 at <= 30 % HP two
          discs (kb 0, 2), above one (kb 2); A13 kb 0
  spots   the reappear / landing spots: bearings and distances for a central player; the player at r 22 facing outward:
          mv/ok within MOVE_R 22.5, the guaranteed fallback on the player -> C line <= FALLBACK_R; stones at the candidates:
          never in blocks; the reappearances of a real A8 run
  ghost   rlk_hr_ghost (hence rlk_mb_inv) from T0 to the dive (A8 / A13) / the solid row (R1 62, R3 46); R2 never; the
          form / hidden rig calls and every clip at its script row
  frame   the judge (deflect: #done at REPEL_T, the blade-lock landing; A8 fail: ult/fail60 at the player, the landing,
          P2 at FAIL60_P2_T; A13 deflect -> CS3; A13 fail: ult/fatal as the player at 258); kit + theme build: the darkness
          ticks (crimson requested at the judge and by the cancel, never dark), the banner off at the judge, the A13 black /
          pink-white / scarlet line staging, every kit effect / sound at its EVENTS tick in the sim
  cancel  a cancel (gauntlets: S3's core/g/pause; R1-R3: core/cancel_pat) at every tick 0..end leaves nothing: no entity of
          the pattern, no cut / spot / disc, the body without the ghost tag, on the floor, no glide, #pat 0, no later hit
  f1      F1 (the 11-05 review fixes, the lead's decisions): HR-19 the counting cuts of A8 / A13 at TC 37 (R1 / R3 keep T2 /
          T3); HR-15 every disc's aim locks 7 t before its release (static) and hits >= 7 t after that lock for a player
          walking in at 0.22 / 0.28 b/t from 5-9 b, for R2 at the rim and for A13's three discs; HR-27 D2 / D4 reappear
          inside the default F5 view near its edge (A8, A13, R3); HR-14 R1 / R3 end <= 12 t after their last hit, R2's kept
          tail moves her (the recovery's move clip) while she turns to the player; F1 round 1: R1 / R3's reform tail moves
          her from the solid row on (static + sim, the recovery keeping the move), the g/spot/d2 / d4 headers and
          api.disc()'s docstring match the code
"""
import copy
import math
import re
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import hrsim as H  # noqa: E402

ARGS = [a for a in sys.argv[1:] if a != '-v']
VERBOSE = '-v' in sys.argv[1:]
DP = Path(ARGS[0]).resolve()
SECTIONS = ARGS[1:] or ['table', 'files', 'hits', 'follow', 'pips', 'discs', 'spots', 'ghost', 'frame', 'cancel', 'f1', 'kept']
sys.path.insert(0, str(DP / 'tools'))
import mboss_scarlet.api as API  # noqa: E402
import mboss_scarlet.p_ghost as PG  # noqa: E402
import mboss_scarlet.s3lib as S3  # noqa: E402
check = H.check if VERBOSE else H.ck
FN = DP / 'data/rlk/function/boss/scarlet'
C = (API.CX, API.CY, API.CZ)
KEYS = list(API.P2)
GAUNT = API.GAUNTLETS
TID = S3.TID
PH = API.PH
# F1 (HR-14): R1 / R3 end 12 t after their last hit (67 / 49); the ends are read from the scripts' 'end' rows
END = {**{k: next(r[0] for r in API.SCRIPTS[k] if r[1] == 'end') for k in ('r1', 'r2', 'r3')},
       'a8': API.FAIL60_P2_T, 'a13': API.REPEL_T['a13']}
CUTS = {k: [r[3] for r in API.SCRIPTS[k] if r[3]] for k in KEYS}            # (made, lock, strike, tier, kb)
STRIKES = {k: [c[2] for c in CUTS[k]] for k in KEYS}
ROWS = {k: [r for r in API.SCRIPTS[k] if r[0] >= 0] for k in KEYS}
RX = API.REAPPEAR


class Dry:
    """A Writer stand-in for a dry build of p_ghost.py (fills TABLE / EVENTS / MOVES, keeps the bodies)."""

    def __init__(self):
        self.files = {}

    def w(self, rel, body):
        self.files[rel] = list(body)


DRY = Dry()
for _k in KEYS:
    PG.BUILD[_k](DRY)


def hr(s, k):
    return H.hr(s, k) or 0


def d2(a, b):
    return math.hypot(a[0] - b[0], a[2] - b[2])


def fdir(yaw):
    """Minecraft's forward vector of a yaw (0 = +z, 90 = -x)."""
    return (-math.sin(math.radians(yaw)), 0.0, math.cos(math.radians(yaw)))


def yaw_of(a, b):
    return math.degrees(math.atan2(-(b[0] - a[0]), b[2] - a[2])) % 360


def angdiff(a, b):
    return abs((a - b + 180) % 360 - 180)


# ================================================================================================= variants / worlds
VARS = {}


def var(name='base'):
    """base: her enabled, the tree's own F:boss/scarlet; kit: a dry rebuild inside the variant with api.K and the theme on."""
    if 'root' not in VARS:
        VARS['root'] = H.variant_hr(DP, H.enable_scarlet, label='pat_ghost')
        VARS['build'] = 'base'
    root = VARS['root']
    if VARS['build'] != name:
        if name == 'base':
            d = root / 'data/rlk/function/boss/scarlet'
            shutil.rmtree(d)
            shutil.copytree(FN, d)
        else:
            patch = {'kit': '', 'kit60': 'api.ULT60_LETHAL = True', 'kit5': 'api.ULT5_LETHAL = False'}[name]
            H.dry_build(root, kit=True, theme=True, patch=patch)
        VARS['build'] = name
    return root


def world(seed=5, name='base'):
    s, pl = H.setup_sc(var(name), seed=seed)
    assert H.fight_sc(s, intro=False), 'the fight did not start'
    H.run_sc(s, 2)
    return s, pl


def rec(s):
    b = H.body_of(s)
    pl = s.player()
    cuts = {s.sc(('e', e.id), 'hr'): tuple(e.pos) for e in s.ents if e.alive and 'rlk_hr_cut' in e.tags}
    discs = [(e.id, tuple(e.pos), e.rot[0], e.etype) for e in s.ents if e.alive and 'rlk_hr_disc' in e.tags]
    php = s.sc(('e', pl.id), 'curHealth')
    pmx = s.sc(('e', pl.id), 'maxHealth')
    return dict(t=s.t, pt=hr(s, '#pt'), pat=hr(s, '#pat'), ph=hr(s, '#ph'), pos=tuple(b.pos) if b else None, lost=(pmx or 0) - (php or 0),
                yaw=(b.rot[0] % 360) if b else None, tags=frozenset(b.tags) if b else frozenset(), pl=tuple(pl.pos),
                cuts=cuts, discs=discs, pips=hr(s, '#pips'), gres=hr(s, '#gres'), look=hr(s, '#hrLook'))


def run_pat(s, key, n=None, each=None, heal=True, stop=True):
    """The test id of key as the player (the core's own start), the AI held; ticks until the pattern is over. Records
    R[i] after the i-th world tick (R[0] = right after the start, pattern tick 0)."""
    H.test_id(s, TID[key])
    H.hold(s, True)
    R = [rec(s)]
    for i in range(n or END[key] + 3):
        if heal:
            H.heal(s)
        if each:
            each(s)
        H.world_sc(s)
        R.append(rec(s))
        if stop and i > 3 and R[-1]['pat'] != TID[key]:
            break
    return R


def pt_of(R):
    """world tick -> pattern tick (while the pattern runs)."""
    return {r['t']: r['pt'] for r in R if r['pat']}


def place(s, x, z, yaw=None):
    pl = H.place_player(s, x, z)
    if yaw is not None:
        pl.rot = [float(yaw), 0.0]
    return pl


# ================================================================================================= table (static)
def contact_rows(key):
    return {r[0] + API.ev(r[2], 'hit'): r for r in ROWS[key] if r[2] and 'hit' in API.CLIPS[r[2]][2]}


# PLAN §4.5 move table: (step, (clip, event) or (clip, offset), kind, name)
REQ = {
    'A8.T': [(('g_tell', 'lilac'), 'snd', 'g_tell'), (('g_tell', 'lilac'), 'look', 'form/ghost'), (('g_tell', 'burst'), 'fx', 'ghost_burst')],
    'D1': [(('g_dash', 'appear'), 'snd', 'g_appear'), (('g_dash', 'go'), 'snd', 'g_dash'), (('g_dash', 'go'), 'fx', 'ghost_trail')],
    'D2': [(('g_glide', 'appear'), 'snd', 'g_appear'), (('g_glide', 'go'), 'snd', 'g_dash'), (('g_glide', 'go'), 'fx', 'ghost_trail')],
    'D3': [(('g_drop', 'flash'), 'snd', 'g_flash'), (('g_drop', 'flash'), 'fx', 'ghost_flash'), (('g_drop', 'gone'), 'fx', 'ghost_burst')],
    'D4': [(('g_run', 'appear'), 'fx', 'ghost_burst'), (('g_run', 'run'), 'fx', 'ghost_trail'), (('g_run', 'run'), 'snd', 'g_step')],
    'A8.1': [(('g_ring', 'hit'), 'fx', 'qi_ring'), (('g_ring', 'hit'), 'snd', 'g_ring')],
    'A8.2': [(('g_rise', 'hit'), 'fx', 'qi_band'), (('g_rise', 'hit'), 'snd', 'g_rise')],
    'A8.3': [(('g_leap', 3), 'snd', 'g_leap'), (('g_leap', 'hit'), 'fx', 'qi_arc'), (('g_leap', 'hit'), 'snd', 'g_leap_cut')],
    'A8.4': [(('g_sweep', 'hit'), 'fx', 'qi_ring'), (('g_sweep', 'hit'), 'snd', 'g_sweep')],
    'A8.5': [(('g_x', 'hit'), 'fx', 'qi_x'), (('g_x', 'hit'), 'snd', 'g_x')],
    'A8.6': [(('g_wrap', 'hit'), 'fx', 'qi_arc'), (('g_wrap', 'hit'), 'snd', 'g_wrap')],
    'A8.7': [(('g_dome', 'hit'), 'fx', 'qi_dome'), (('g_dome', 'hit'), 'snd', 'g_dome')],
    'A8.8': [(('g_vert', 'glow'), 'fx', 'glint'), (('g_vert', 'glow'), 'snd', 'g_glow'), (('g_vert', 'glow'), 'look', 'blade/pink'),
             (('g_vert', 'hit'), 'fx', 'qi_vert'), (('g_vert', 'hit'), 'snd', 'g_vert')],
    'A8.9': [(('g_dive', 'appear'), 'look', 'form/normal'), (('g_dive', 'dive'), 'snd', 'g_dive')],
    'tell': [(('a7_tell', 'yellow'), 'fx', 'yellow_tell'), (('a7_tell', 'yellow'), 'snd', 'yellow_chime')],
    'disc1': [(('a7_throw', 'release'), 'snd', 'disc_release'), (('a7_throw', 'release'), 'snd', 'disc_fly'),
              (('a7_throw', 'spin'), 'look', 'blade/gold')],
    'disc2': [(('a7_throw', 'release'), 'snd', 'disc_release'), (('a7_throw', 'release'), 'snd', 'disc_fly')],
    'disc3': [(('a7_throw', 'release'), 'snd', 'disc_release'), (('a7_throw', 'release'), 'snd', 'disc_fly')],
    'throw': [(('a7_throw', 'release'), 'snd', 'disc_release'), (('a7_throw', 'release'), 'snd', 'disc_fly')],
    'throw2': [(('a7_throw', 'release'), 'snd', 'disc_release'), (('a7_throw', 'release'), 'snd', 'disc_fly')],
    'reform': [(('g_reform', 'solid'), 'look', 'form/normal')],
}


def sec_table():
    for k in KEYS:
        hs = PG.TABLE[k]
        cuts = [h for h in hs if h['kind'] == 'cut']
        got = [(h['t'], h['made'], h['lock'], h['tier'], h['kb']) for h in cuts]
        exp = [(c[2], c[0], c[1], c[3], c[4]) for c in CUTS[k]]
        check(f'T1 {k}: the cuts = the script rows (strike, made, lock, tier, kb)', got == exp, (got, exp))
        con = contact_rows(k)
        api_cuts = [h for h in API.HITS[k] if h[2] == 'pdisc']
        mine = [(con[h['t']][2], 'hit', 'pdisc', tuple(h['dims']), h['tier'], h['kb']) for h in cuts if h['t'] in con]
        check(f'T2 {k}: every strike = the contact (row t + clip hit) of exactly one move, = api.HITS (clip, shape, CUT_R, tier, kb)',
              len(mine) == len(cuts) and mine == [(a, b, c, tuple(d), e, f) for a, b, c, d, e, f in api_cuts], (mine, api_cuts))
        want_n = 1 if k in GAUNT else 0
        check(f'T3 {k}: {"9 counting cuts (api.CUT_IDS)" if k in GAUNT else "no cut counts (R1 / R3: no shield)"}',
              all(h['n'] == want_n for h in cuts) and (k not in GAUNT or len(cuts) == len(API.CUT_IDS[k]) == 9), [h['n'] for h in cuts])
        bad = [(h['t'], h['made']) for h in cuts if h['t'] - h['made'] < API.TELL_MIN]
        big = [h for h in cuts if math.pi * h['dims'][0] ** 2 >= 100 or h['dims'][0] >= 8]
        check(f'T4 {k}: every cut made >= TELL_MIN {API.TELL_MIN} t before its strike (no cut is big: '
              f'{math.pi * API.CUT_R ** 2:.0f} b^2 < 100)', not bad and not big, (bad, big))
        check(f'T5 {k}: every lock = strike - LOCK_LEAD {API.LOCK_LEAD}, made <= lock', all(h['lock'] == h['t'] - API.LOCK_LEAD
                                                                                          and h['made'] <= h['lock'] for h in cuts))
        discs = [h for h in hs if h['kind'] == 'disc']
        if k in API.DISC_RELEASE:
            rel = sorted({h['t'] for h in discs})
            check(f'T6 {k}: the discs at DISC_RELEASE {API.DISC_RELEASE[k]}', tuple(rel) == API.DISC_RELEASE[k], rel)
            yel = [r[0] + API.ev('a7_tell', 'yellow') for r in ROWS[k] if r[2] == 'a7_tell']
            check(f'T7 {k}: the yellow tell >= TELL_BIG {API.TELL_BIG} t before the first disc leaves', yel and rel[0] - yel[0] >= API.TELL_BIG,
                  (yel, rel))
        if k == 'r2':
            kb = sorted((h['t'], h['kb'], h['cond']) for h in discs)
            check('T8 r2: one disc kb 2 (above 30 % HP) / two discs kb 0 then kb 2 (<= 30 %: #r2_two)',
                  kb == [(28, 0, 'if score #r2_two hr matches 1'), (28, 2, 'unless score #r2_two hr matches 1'),
                         (42, 2, 'if score #r2_two hr matches 1')], kb)
        elif k == 'a13':
            check('T8 a13: the three discs kb 0', all(h['kb'] == 0 for h in discs), [h['kb'] for h in discs])
        # gaps between hits (cut strikes, disc releases; R2's two discs only together)
        ts = sorted({h['t'] for h in hs})
        gaps = [b - a for a, b in zip(ts, ts[1:]) if b != a]
        check(f'T9 {k}: successive hits >= COMBO_GAP {API.COMBO_GAP} t apart', all(g >= API.COMBO_GAP for g in gaps), gaps)
        # kb: cuts 0 except the scripts' last hits
        last = {'r1': [55], 'r3': [37]}.get(k, [])
        kbs = [(h['t'], h['kb']) for h in cuts]
        check(f'T10 {k}: cuts kb 0 except the script\'s last hit{"" if last else "s (none here)"} (kb {API.KB_FINAL})',
              all((kb == API.KB_FINAL) == (t in last) for t, kb in kbs), kbs)
        # the move table: every effect / sound / look at its clip event
        evs = {(t, kind, name) for t, kind, name, _src in PG.EVENTS[k]}
        miss = []
        for t, step, clip, c in ROWS[k]:
            if clip:
                if (t, 'clip', clip) not in evs:
                    miss.append((t, 'clip', clip))
            for (cl, e), kind, name in REQ.get(step, []):
                tt = t + (e if isinstance(e, int) else API.ev(cl, e))
                if (tt, kind, name) not in evs:
                    miss.append((tt, kind, name, step))
        if k in GAUNT:
            for bt in API.BOLTS[k]:
                if (bt, 'fx', 'deco_bolt') not in evs or (bt, 'snd', 'deco_bolt') not in evs:
                    miss.append((bt, 'bolt'))
        check(f'T11 {k}: every effect / sound / look of PLAN §4.5\'s move table at its clip event (+ the bolts)', not miss, miss[:6])
        tagged = [(t, n) for t, kind, n, _s in PG.EVENTS[k] if kind == 'tag']
        if k in GAUNT:
            dive = [r[0] for r in ROWS[k] if r[1] == 'A8.9'][0]
            want = [(0, 'ghost+'), (dive, 'ghost-')]
        elif k in ('r1', 'r3'):
            solid = [r[0] for r in ROWS[k] if r[1] == 'solid'][0]
            want = [(0, 'ghost+'), (solid, 'ghost-')]
        else:
            want = []
        check(f'T12 {k}: the ghost tag on at T0, off at {"the dive" if k in GAUNT else "the solid row" if want else "never (R2 is solid)"}',
              tagged == want, tagged)
    hs = PG.TABLE['a8']
    print(f'  table: A8 strikes {[h["t"] for h in hs]}, A13 strikes {[h["t"] for h in PG.TABLE["a13"] if h["kind"] == "cut"]} '
          f'+ discs {list(API.DISC_RELEASE["a13"])}')


# ================================================================================================= files (static)
def my_files():
    out = {}
    for d in [FN / 'g'] + [FN / 'p' / k for k in KEYS]:
        for p in sorted(d.rglob('*.mcfunction')):
            out[str(p.relative_to(FN))[:-len('.mcfunction')]] = p.read_text(encoding='utf-8').split('\n')
    return out


def cmd_lines(lines):
    return [ln for ln in lines if ln.strip() and not ln.lstrip().startswith('#')]


def sec_files():
    F = my_files()
    need = [f'p/{k}/{x}' for k in KEYS for x in ('start', 'tick', 'cancel')] + ['g/cut/make', 'g/cut/aim', 'g/cut/lock',
                                                                                 'g/disc/throw', 'g/ground', 'g/reset']
    need += [f'g/spot/{n}' for n in PG.SPOTS]
    check('F1 every pattern\'s start / tick / cancel and the helpers g/cut, g/disc, g/spot, g/reset exist', all(n in F for n in need),
          [n for n in need if n not in F])
    args = {}
    for rel in ('g/cut/make', 'g/cut/aim', 'g/cut/lock', 'g/disc/throw'):
        args[rel] = sorted(set(re.findall(r'\$\((\w+)\)', '\n'.join(F[rel]))))
    want = {rel: sorted(v) for rel, v in API.CUT_ARGS.items()}
    want['g/disc/throw'] = ['kb']
    check('F2 the macro args: g/cut/make {s,t,dmg,kb,n}, aim {s}, lock {s} (api.CUT_ARGS), g/disc/throw {kb}', args == want, args)
    # every api.cut() line at its tick; nothing else calls g/cut
    bad = [(rel, ln[:60]) for rel, lines in F.items() for ln in cmd_lines(lines) if 'g/cut/' in ln
           and not rel.startswith(('g/cut/', 'p/')) or ('g/cut/' in ln and rel.startswith('p/') and not re.fullmatch(r'p/\w+/k/\d+', rel))]
    for k in KEYS:
        got = set()
        for rel, lines in F.items():
            m = re.fullmatch(rf'p/{k}/k/(\d+)', rel)
            if not m:
                continue
            for ln in cmd_lines(lines):
                if 'g/cut/' in ln:
                    got.add((int(m.group(1)), ln.strip()))
        exp = {(t, ln) for c in CUTS[k] for t, ln in API.cut(*c[:5], count=1 if k in GAUNT else 0)}
        if got != exp:
            bad.append((k, sorted(got ^ exp)[:3]))
    check('F3 every cut through api.cut() at its ticks (make / aim each tick / lock), n 1 only in the gauntlets', not bad, bad[:4])
    text = '\n'.join(ln for lines in F.values() for ln in cmd_lines(lines))
    neg = re.findall(r'scoreboard players (?:add|remove) \S+ \S+ -\d', text)
    check('F4 no negative literal in scoreboard add / remove', not neg, neg[:3])
    deco = [w for w in ('setblock ', 'fill ', 'block_display', 'text_display', '#hzVis') if w in text]
    check('F5 no setblock / fill / block or text display / #hzVis anywhere (no floor decal)', not deco, deco)
    hz = [rel for rel, lines in F.items() if any('rlk:mboss/hz/' in ln and 'hz/aim' not in ln for ln in cmd_lines(lines))]
    pj = [rel for rel, lines in F.items() if any('rlk:mboss/pj/' in ln for ln in cmd_lines(lines))]
    mk = cmd_lines(F['g/cut/make'])
    check('F6 hazards only in g/cut/make (quiet, no sound, Electro, act 2, the disc of CUT_R), pj/launch only in g/disc/throw',
          hz == ['g/cut/make'] and pj == ['g/disc/throw'] and 'scoreboard players set #hzQuiet mb 1' in mk
          and 'scoreboard players set #hzSfx mb 0' in mk and f'scoreboard players set #hzEl mb {API.ELEC}' in mk
          and 'scoreboard players set #hzAct mb 2' in mk and any(f'hz/disc {{r:{round(API.CUT_R * 10)},' in ln for ln in mk), (hz, pj))
    th = cmd_lines(F['g/disc/throw'])
    i_sum = next(i for i, ln in enumerate(th) if 'summon minecraft:item_display' in ln)
    i_rot = next(i for i, ln in enumerate(th) if 'run tp @s ~ ~ ~ ~ ~' in ln)
    i_l = next(i for i, ln in enumerate(th) if 'pj/launch' in ln)
    summons = [ln for ln in th if 'summon ' in ln]
    check('F7 the disc: one card summoned, then rotated (tp facing the player, pitch 0), then launched (README 0-6)',
          i_sum < i_rot < i_l and len(summons) == 1, (i_sum, i_rot, i_l, len(summons)))
    tps = [(rel, ln) for rel, lines in F.items() for ln in cmd_lines(lines) if re.search(r'\btp @s ~ ~ ~$', ln)
           and 'rlk_hr_gsp' not in ln and rel not in ('g/ground', 'g/spot/clamp')]
    check('F8 every body teleport through a spot (mv/ok-checked, g/spot/*) or the floor fallback (g/ground)', not tps, tps[:3])
    names = set(re.findall(r'(#[A-Za-z0-9_]+) hr\b', text))
    # I1b: with S1K's theme merged, api.arena_look() (the gauntlet's crimson request at the judge and in cancel, contract §3.5)
    # writes the core's request score api.LOOK_REQ (#hrLook); it was '' on S4's branch (no theme)
    allowed = {'#pt', '#pat', '#done', '#gres', '#pips', '#c100', API.LOOK_REQ}
    odd = sorted(n for n in names if n not in allowed and not n.startswith(('#g_', '#r2_')))
    check('F9 own fake players #g_* / #r2_* only (+ the core\'s #pt #pat #done #gres #pips #c100 read, the look request '
          '#hrLook through api.arena_look)', not odd, odd)
    below = re.findall(r'positioned ~ ~-[0-9.]+ ~', text) + [y for y in re.findall(r'positioned ~ (\d+(?:\.\d+)?) ~', text) if float(y) < API.CY]
    check('F10 nothing below the floor (no negative y offsets, every absolute y >= the floor)', not below, below[:3])
    refs = set(re.findall(r'function (rlk:[a-z0-9_/]+)', text))
    root = DP / 'data/rlk/function'
    missing = sorted(r for r in refs if not (root / (r.split(':', 1)[1] + '.mcfunction')).exists())
    check('F11 every referenced function exists in the tree (rig stand-in, framework, S3\'s shield / ult)', not missing, missing[:5])
    print(f'  files: {len(F)} S4 functions')


# ================================================================================================= hits (sim)
def hz_of(s, n0):
    return s.hzr[n0:]


def sec_hits():
    for k in KEYS:
        for seed, spot in ((5, (880.5, 14.0)), (6, (874.0, 4.0))):
            s, pl = world(seed)
            place(s, *spot)
            H.place_body(s, C[0], C[2] - 6)
            n0, p0 = len(s.hzr), len(s.phits)
            R = run_pat(s, k)
            P = pt_of(R)
            hz = hz_of(s, n0)
            got = sorted((h['pt'], h['tell'], h['r'], h['dmg'], h['kb'], h['act'], h['quiet'], h['sfx'], h['el'], h['kind']) for h in hz)
            exp = sorted((c[0], c[2] - c[0], round(API.CUT_R * 10), API.DMG[c[3]], c[4], 2, 1, 0, API.ELEC, 1) for c in CUTS[k])
            check(f'H1 {k} @ {spot}: every hazard made at its made tick: tell strike - made, r 3.2, the tier\'s %, kb, act 2, quiet, '
                  f'no sound, Electro, a disc', got == exp, (got, exp))
            onfloor = all(abs(h['pos'][1] - API.CY) < 1e-6 and d2(h['pos'], (spot[0], 0, spot[1])) < 1e-6 for h in hz)
            check(f'H2 {k} @ {spot}: every cut made on the player\'s floor spot', onfloor, [h['pos'] for h in hz][:3])
            hits = [(P.get(t), pct, el) for t, pct, el, pat in s.phits[p0:] if pat == TID[k]]
            cut_hits = sorted(h[0] for h in hits if h[0] in STRIKES[k])
            check(f'H3 {k} @ {spot}: a standing player is hit once per cut, at its strike, with the tier\'s % (Electro)',
                  cut_hits == sorted(STRIKES[k]) and all(el == API.ELEC for _, _, el in hits)
                  and all(pct == API.DMG[c[3]] for c in CUTS[k] for t, pct, _ in hits if t == c[2]), hits)
            rel = sorted({h['t'] for h in PG.TABLE[k] if h['kind'] == 'disc'})
            other = sorted(h[0] for h in hits if h[0] not in STRIKES[k])
            if rel:
                ok = len(other) == (1 if k == 'r2' else 3) and all(any(r < t <= r + API.DISC['life'] for r in rel) for t in other)
                check(f'H4 {k} @ {spot}: the disc hits land after a release, within its life ({other})', ok, (other, rel))
            else:
                check(f'H4 {k} @ {spot}: no hit besides the cuts', not other, other)


# ================================================================================================= follow (sim)
def walker(cx, cz, r, v=0.25):
    def each(s):
        a = s.t * v / r
        pl = s.player()
        pl.pos = [cx + r * math.cos(a), API.CY, cz + r * math.sin(a)]
        H.C.moved(s)
    return each


def sec_follow():
    for k in ('r1', 'a8', 'a13'):
        s, pl = world(9)
        R = run_pat(s, k, each=walker(C[0], C[2], 7.0))
        bad = []
        for made, lock, strike, *_ in CUTS[k]:
            at_lock = None
            for r in R:
                p = r['pt']
                if strike not in r['cuts'] or not r['pat']:
                    continue
                m = r['cuts'][strike]
                if made <= p <= lock:
                    if d2(m, r['pl']) > 1e-6 or abs(m[1] - API.CY) > 1e-6:
                        bad.append((strike, p, 'not on the player', round(d2(m, r['pl']), 3)))
                    if p == lock:
                        at_lock = m
                elif lock < p <= strike + 1 and at_lock is not None and d2(m, at_lock) > 1e-6:
                    bad.append((strike, p, 'moved after the lock'))
            moved = [d2(r['cuts'][strike], r['pl']) for r in R if r['pt'] == strike and strike in r['cuts']]
            if not moved or moved[0] < 1.0:
                bad.append((strike, 'the walker should be ~1.75 b off the lock point at the strike', moved))
        check(f'L1 {k}: every cut on the walking player\'s floor spot each tick until its lock, fixed from the lock to the strike',
              not bad, bad[:4])


# ================================================================================================= pips (sim)
TAKE = 'rlk:boss/scarlet/shield/take'
AGENTS = [('stand', 0.0), ('out', 0.22), ('out', 0.28), ('side', 0.22), ('side', 0.28), ('in', 0.22), ('in', 0.28)]
HOME = {'stand': (C[0] + 0.5, C[2] + 6.0), 'out': (C[0], C[2] + 8.0), 'side': (C[0], C[2] + 10.0), 'in': (C[0], C[2] + 13.0)}


def agent(g, mode, speed, off):
    """Before each world tick: the pattern tick it will run is p = #pt + 1. In [lock, strike + 1] of every cut the agent walks
    along its direction (fixed at the lock: away from C / tangential / toward C; stand: still), dodges at strike + off
    (combat overhaul C: the dodge stamp dgAt that tick, hrsim's s.dash; 1 b per tick along the direction / the look for 3 t),
    and is put back home at strike + 2."""
    st = {'dir': None, 'dash': None}
    hx, hz = HOME[mode]

    def each(s):
        if hr(s, '#pat') != TID[g]:
            return
        p = hr(s, '#pt') + 1
        pl = s.player()
        for made, lock, strike, *_ in CUTS[g]:
            if p == strike + 2:
                pl.pos = [hx, API.CY, hz]
                st['dir'] = None
            if lock <= p <= strike + 1:
                if st['dir'] is None:
                    ox, oz = pl.pos[0] - C[0], pl.pos[2] - C[2]
                    n = math.hypot(ox, oz) or 1.0
                    ox, oz = ox / n, oz / n
                    if mode == 'stand':
                        f = fdir(pl.rot[0])
                        st['dir'] = (f[0], f[2])
                    else:
                        st['dir'] = {'out': (ox, oz), 'in': (-ox, -oz), 'side': (-oz, ox)}[mode]
                dx, dz = st['dir']
                if mode != 'stand':
                    pl.pos = [pl.pos[0] + dx * speed, API.CY, pl.pos[2] + dz * speed]
                if p == strike + off:
                    s.dash(6)
                    st['dash'] = p
        if st['dash'] is not None and 0 <= p - st['dash'] < 3 and st['dir']:
            dx, dz = st['dir']
            pl.pos = [pl.pos[0] + dx, API.CY, pl.pos[2] + dz]
        H.C.moved(s)
    return each


def dash_economy(dash_ticks, cool=12):
    """F:player/dash (combat overhaul C: no charges, the cooldown #dashCoolT 12 t; player/tick removes 1 per tick before the
    input of the next tick): whether every dodge in dash_ticks is off cooldown."""
    cd, out = 0, []
    want = set(dash_ticks)
    for t in range(0, max(dash_ticks) + 1):
        if t in want:
            ok = cd == 0
            out.append((t, ok, cd))
            if ok:
                cd = cool
        if cd >= 1:
            cd -= 1
    return out


def sec_pips():
    res = {}
    for g in GAUNT:
        for mode, speed in AGENTS:
            s, pl = world(31 + len(res))
            n_take, n_dash, hits_on_cut, tried = 0, 0, [], 0
            for off in (-2, -1, 0):
                hx, hz = HOME[mode]
                place(s, hx, hz, yaw=yaw_of((hx, 0, hz), C))
                s.watch[TAKE] = []
                s.dash_t0 = None
                p0 = len(s.phits)
                R = run_pat(s, g, n=API.JUDGE_T[g] + 1, each=agent(g, mode, speed, off), stop=False)
                P = pt_of(R)
                takes = {P.get(t) for t, *_ in s.watch[TAKE]}
                for st in STRIKES[g]:
                    n_dash += 1
                    n_take += bool(takes & {st, st + 1})
                win = {x for st in STRIKES[g] for x in (st, st + 1)}
                hits_on_cut += [(off, r['pt']) for r in R if r['pat'] == TID[g] and r['pt'] in win and r['lost'] > 0]
                tried += sum(1 for t, pct, el, pat in s.phits[p0:] if pat == TID[g] and P.get(t) in win)
            frac = n_take / n_dash
            res[(g, mode, speed)] = frac
            check(f'P1 {g} {mode}{f" {speed} b/t" if speed else ""}: dodges at strike - 1 +- 1 (the perfect window) score {n_take}/{n_dash} = {frac:.0%} '
                  f'(>= 90 %), never hurt by a cut ({tried} cut hits dodged)', frac >= 0.9 and not hits_on_cut, (frac, hits_on_cut[:6]))
    print('  pips: ' + ', '.join(f'{g} {m}{" " + str(v) if v else ""} {f:.0%}' for (g, m, v), f in res.items()))
    for g in GAUNT:
        for off in (-2, -1, 0):
            ec = dash_economy([st + off for st in STRIKES[g]])
            check(f'P2 {g}: a dodger (12-t cooldown) dodging at strike {off:+d} reaches every counting window',
                  all(ok for _, ok, _ in ec), ec)


# ================================================================================================= discs (sim)
def disc_track(R):
    tr = {}
    for r in R:
        for eid, pos, yaw, et in r['discs']:
            tr.setdefault(eid, []).append((r['pt'], pos, yaw, et, r['pl']))
    return tr


def sec_discs():
    # R2 above 30 % HP: one disc; the player 12 b away, then sidestepping after the release (no homing)
    s, pl = world(41)
    H.place_body(s, C[0], C[2] - 4)
    place(s, C[0] + 0.5, C[2] + 10.0)

    def side(s):
        if hr(s, '#pat') == TID['r2'] and hr(s, '#pt') >= 29:
            p = s.player()
            p.pos = [p.pos[0] + 0.3, API.CY, p.pos[2]]
            H.C.moved(s)
    R = run_pat(s, 'r2', each=side)
    tr = disc_track(R)
    check('D1 r2 above 30 % HP: one disc (one item display card, rlk_hr_disc)', len(tr) == 1 and all(v[0][3] == 'item_display' for v in tr.values()),
          {k: len(v) for k, v in tr.items()})
    for eid, pts in tr.items():
        p0, pos0, yaw0, _, pl0 = pts[0]
        rel_r = [r for r in R if r['pt'] == 28][0]
        lk_r = [r for r in R if r['pt'] == 28 - API.LOCK_LEAD][0]      # F1 (HR-15): the aim locks 7 t before the release
        want = yaw_of(rel_r['pos'], lk_r['pl'])
        steps = [d2(a[1], b[1]) for a, b in zip(pts, pts[1:])]
        check('D2 r2: aimed at the player\'s position at its lock (release - 7; yaw), 0.9 b over the floor, never turning (no homing)',
              angdiff(yaw0, want) < 1.0 and all(abs(q[1][1] - (API.CY + 0.9)) < 1e-6 for q in pts)
              and all(angdiff(q[2], yaw0) < 1e-6 for q in pts), (yaw0, want, pts[0][1]))
        fly = math.ceil(API.DISC['speed'] / 0.25 - 1e-9) * 0.25    # I1 (s4-2): the flown speed = whole 0.25 b sub-steps
        check(f'D3 r2: the disc flies {fly:.2f} b per tick ({API.DISC["speed"]} asked, 0.25 b sub-steps rounded up), life <= {API.DISC["life"]} t',
              steps and all(abs(x - fly) < 0.02 for x in steps[:-1]) and len(pts) <= API.DISC['life'] + 1, (steps[:5], len(pts)))
    # kb at launch (the pj's mbPjB): R2 single 2
    def kb_watch(s, out):
        def each(ss):
            for e in ss.ents:
                if e.alive and 'rlk_hr_disc' in e.tags and e.id not in out:
                    out[e.id] = (hr(ss, '#pt'), ss.sc(('e', e.id), 'mbPjB'))
        return each
    for pct, n_want, kb_want in ((31, 1, [2]), (29, 2, [0, 2])):
        s, pl = world(42)
        b = H.body_of(s)
        mx = s.sc(('e', b.id), 'mhpM')
        s.setsc(('e', b.id), 'mhpC', mx * pct // 100)
        H.place_body(s, C[0], C[2] - 4)
        place(s, C[0] + 0.5, C[2] + 10.0)
        seen = {}
        kw = kb_watch(s, seen)
        H.test_id(s, TID['r2'])
        H.hold(s, True)
        for _ in range(END['r2'] + 2):
            H.heal(s)
            H.world_sc(s)
            kw(s)
        kbs = [v[1] for _, v in sorted(seen.items(), key=lambda kv: kv[1][0])]
        check(f'D4 r2 at {pct} % HP: {n_want} disc{"s" if n_want > 1 else ""}, kb {kb_want}', len(seen) == n_want and kbs == kb_want,
              (seen, kbs))
    # wall stop: a stone wall across the flight (2 high): the disc ends at it, no hit
    s, pl = world(43)
    H.place_body(s, C[0], C[2] - 4)
    place(s, C[0] + 0.5, C[2] + 10.0)
    for x in range(int(C[0]) - 6, int(C[0]) + 7):
        for y in (201, 202, 203):
            s.setb(x, y, int(C[2]) + 4, 'minecraft:stone')
    p0 = len(s.phits)
    R = run_pat(s, 'r2')
    tr = disc_track(R)
    far = [max(q[1][2] for q in v) for v in tr.values()]
    hits = [x for x in s.phits[p0:] if x[3] == TID['r2']]
    check('D5 r2: a stone wall across the flight stops the disc there (wall stop), no hit', tr and all(z < C[2] + 4 for z in far) and not hits,
          (far, hits))
    # A13: three discs, kb 0, each aimed at the player's position at its release
    s, pl = world(44)
    place(s, C[0] + 0.5, C[2] + 6.0)
    seen = {}
    kw = kb_watch(s, seen)

    def drift(ss):
        kw(ss)
        if hr(ss, '#pat') == TID['a13'] and 140 <= hr(ss, '#pt') <= 185:
            p = ss.player()
            p.pos = [p.pos[0] + 0.2, API.CY, p.pos[2]]
            H.C.moved(ss)
    R = run_pat(s, 'a13', each=drift)
    tr = disc_track(R)
    ok = []
    for eid, pts in tr.items():
        p0_ = pts[0][0]
        r = [x for x in R if x['pt'] == p0_][0]
        rl = [x for x in R if x['pt'] == p0_ - API.LOCK_LEAD][0]     # F1 (HR-15): the player's spot at the lock
        ok.append(angdiff(pts[0][2], yaw_of(r['pos'], rl['pl'])) < 1.5)
    rels = sorted(v[0] for v in seen.values())
    check('D6 a13: three discs (155 / 167 / 180), one card each, kb 0, each aimed at the player\'s position at its lock (release - 7)',
          len(tr) == 3 and rels == list(API.DISC_RELEASE['a13']) and all(v[1] == 0 for v in seen.values()) and all(ok), (rels, seen, ok))
    one = all(len({x[0] for x in r['discs']}) <= 3 for r in R) and all(x[3] == 'item_display' for r in R for x in r['discs'])
    check('D7 one display card per projectile (the card is the projectile)', one)


# ================================================================================================= spots (sim)
def spot_at(s, name, ppos, pyaw, bpos=None):
    place(s, ppos[0], ppos[1], yaw=pyaw)
    if bpos:
        H.place_body(s, *bpos)
    for e in s.ents:
        if 'rlk_hr_gsp' in e.tags:
            e.alive = False
    H.call_sc(s, f'g/spot/{name}')
    ms = [e for e in s.ents if e.alive and 'rlk_hr_gsp' in e.tags]
    pos = tuple(ms[0].pos) if ms else None
    for e in ms:
        e.alive = False
    s.ents = [e for e in s.ents if e.alive]
    return pos, len(ms)


def mv_ok(s, pos):
    return s.call('rlk:mboss/mv/ok', H.Ctx(None, (pos[0], pos[1], pos[2]), (0.0, 0.0))) == 1


def free(s, pos):
    x, y, z = math.floor(pos[0]), math.floor(pos[1]), math.floor(pos[2])
    return all(s.block_test((x + 0.5, yy + 0.5, z + 0.5), '#rlk:dash_pass') for yy in (y, y + 1))


PRIMARY = {'d1': (RX['D1']['bearing'], RX['D1']['dist']), 'side': (90, RX['D1']['end'][0]), 'd2': (RX['D2']['bearing'], RX['D2']['dist']),
           'd2e': (RX['D2']['end'][1], RX['D2']['end'][0]), 'd3': (RX['D3']['bearing'], RX['D3']['dist']),
           'd4': (RX['D4']['bearing'], RX['D4']['dist']), 'tell': (0, RX['tell']['dist']), 'over': (0, 0.0), 'land': (0, 2.0),
           'lock': (0, 1.2)}


def sec_spots():
    s, pl = world(51)
    H.hold(s, True)
    P = (C[0] + 0.5, C[2] + 6.0)
    for yaw in (180.0, 90.0, 33.0):
        bad = []
        for name, (b, d) in PRIMARY.items():
            pos, n = spot_at(s, name, P, yaw, bpos=(C[0], C[2] - 5))
            f = fdir(yaw + b)
            want = (P[0] + d * f[0], API.CY, P[1] + d * f[2])
            if n != 1 or d2(pos, want) > 0.01 or abs(pos[1] - API.CY) > 1e-6:
                bad.append((name, pos, want))
        check(f'S1 the player at r 6 facing {yaw:.0f}: every spot at its bearing (+ = right) / distance (api.REAPPEAR)', not bad, bad[:3])
    # the her-relative spots: far (12 b toward her), beyond (3 b past the player), land 2, lock 1.2, back (6 b away from the player)
    B = (C[0] - 2.0, C[2] - 2.0)
    bad = []
    for name, d, sign, frm in (('far', 12.0, 1, 'pl'), ('beyond', 3.0, -1, 'pl'), ('back', 6.0, -1, 'body')):
        pos, n = spot_at(s, name, P, 180.0, bpos=B)
        o = (P[0], 0, P[1]) if frm == 'pl' else (B[0], 0, B[1])
        tgt = (B[0], 0, B[1]) if frm == 'pl' else (P[0], 0, P[1])
        u = yaw_of(o, tgt)
        f = fdir(u if sign > 0 else u + 180)
        want = (o[0] + d * f[0], API.CY, o[2] + d * f[2])
        if n != 1 or d2(pos, want) > 0.01:
            bad.append((name, pos, want))
    check('S2 the spots along the player <-> her line: far 12 b (A13 retreat), beyond 3 b (R1 landing), R2\'s back 6 b', not bad, bad)
    # the player at r 22 facing outward: every spot passes mv/ok inside MOVE_R; D1 / D2 / D4: the guaranteed fallback
    bad, fb = [], 0
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        P2 = (C[0] + 22 * math.sin(a), C[2] + 22 * math.cos(a))
        out_yaw = yaw_of(C, (P2[0], 0, P2[1]))
        for name in list(PRIMARY) + ['far', 'beyond', 'back']:
            pos, n = spot_at(s, name, P2, out_yaw, bpos=(C[0] + 15 * math.sin(a), C[2] + 15 * math.cos(a)))
            if n != 1 or not mv_ok(s, pos) or d2(pos, C) > API.MOVE_R + 1e-6 or not free(s, pos):
                bad.append((ang, name, pos))
            if name in ('d1', 'd2', 'd4'):
                # on the player -> C line, <= FALLBACK_R from C
                ux, uz = (C[0] - P2[0]) / 22, (C[2] - P2[1]) / 22
                perp = abs((pos[0] - P2[0]) * uz - (pos[2] - P2[1]) * ux)
                if perp > 0.05 or d2(pos, C) > API.FALLBACK_R + 1e-6:
                    bad.append((ang, name, 'not the guaranteed fallback', pos, round(perp, 3)))
                else:
                    fb += 1
    check(f'S3 the player at r 22 facing outward (12 angles): every spot passes mv/ok within MOVE_R {API.MOVE_R}, never in a block; '
          f'D1 / D2 / D4 fall back to the player -> C line <= {API.FALLBACK_R} b from C ({fb})', not bad, bad[:4])
    # the player on the walk rim (r 24.5, beyond MOVE_R): every spot inside MOVE_R; when no candidate passes, the guaranteed
    # fallback on the player -> C line at most FALLBACK_R from C
    bad, n_tail = [], 0
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        Pr = (C[0] + 24.5 * math.sin(a), C[2] + 24.5 * math.cos(a))
        out_yaw = yaw_of(C, (Pr[0], 0, Pr[1]))
        for name, (cands, tail, _w) in PG.SPOTS.items():
            if tail is None or any(b != 'face' for b, _a, _d in cands):
                continue
            pos, n = spot_at(s, name, Pr, out_yaw, bpos=(C[0] + 15 * math.sin(a), C[2] + 15 * math.cos(a)))
            if n != 1 or not mv_ok(s, pos) or d2(pos, C) > API.MOVE_R + 1e-6 or not free(s, pos):
                bad.append((ang, name, pos))
                continue
            reach = [d2((Pr[0] + d * fdir(out_yaw + b)[0], 0, Pr[1] + d * fdir(out_yaw + b)[2]), C) for _bb, b, d in cands]
            if all(r > API.MOVE_R for r in reach):
                n_tail += 1
                ux, uz = (C[0] - Pr[0]) / 24.5, (C[2] - Pr[1]) / 24.5
                perp = abs((pos[0] - Pr[0]) * uz - (pos[2] - Pr[1]) * ux)
                if perp > 0.05 or d2(pos, C) > API.FALLBACK_R + 1e-6:
                    bad.append((ang, name, 'fallback', pos, round(d2(pos, C), 2), round(perp, 3)))
    check(f'S7 the player on the walk rim (r 24.5, 12 angles): every spot inside MOVE_R (mv/ok, free); the {n_tail} guaranteed fallbacks '
          f'on the player -> C line <= FALLBACK_R {API.FALLBACK_R} b from C', not bad and n_tail > 0, bad[:4])
    # stones at the primary candidates (feet and head): another candidate, never in a block
    bad = []
    for name, (b, d) in PRIMARY.items():
        if d == 0:
            continue
        f = fdir(180.0 + b)
        cx, cz = P[0] + d * f[0], P[1] + d * f[2]
        stones = [(math.floor(cx) + dx, y, math.floor(cz) + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1) for y in (201, 202)]
        for x, y, z in stones:
            s.setb(x, y, z, 'minecraft:stone')
        pos, n = spot_at(s, name, P, 180.0, bpos=(C[0], C[2] - 5))
        if n != 1 or not free(s, pos) or not mv_ok(s, pos):
            bad.append((name, pos))
        for x, y, z in stones:
            s.setb(x, y, z, 'minecraft:air')
    check('S4 a stone block on each primary spot: the next candidate, never in a block', not bad, bad)
    # everything around the player blocked: the guaranteed fallback walked toward C until mv/ok passes
    bad = []
    for name in ('d1', 'side', 'd2', 'd4', 'tell'):
        cands, tail, _w = PG.SPOTS[name]
        pts = []
        for basis, b, d in cands:
            f = fdir(180.0 + b)
            pts.append((P[0] + d * f[0], P[1] + d * f[2]))
        u = yaw_of((P[0], 0, P[1]), C)
        f = fdir(u)
        tp_ = (P[0] + tail * f[0], P[1] + tail * f[2])
        pts.append(tp_)
        stones = {(math.floor(x) + dx, y, math.floor(z) + dz) for x, z in pts for dx in (-1, 0, 1) for dz in (-1, 0, 1) for y in (201, 202)}
        stones -= {(math.floor(P[0]), y, math.floor(P[1])) for y in (201, 202)}
        for x, y, z in stones:
            s.setb(x, y, z, 'minecraft:stone')
        pos, n = spot_at(s, name, P, 180.0, bpos=(C[0], C[2] - 5))
        perp = abs((pos[0] - P[0]) * (C[2] - P[1]) - (pos[2] - P[1]) * (C[0] - P[0])) / d2(C, (P[0], 0, P[1])) if pos else None
        if n != 1 or not free(s, pos) or not mv_ok(s, pos) or perp > 0.05:
            bad.append((name, pos, perp))
        for x, y, z in stones:
            s.setb(x, y, z, 'minecraft:air')
    check('S5 every candidate and the tail point blocked: the guaranteed fallback walked along the player -> C line until free (mv/ok)',
          not bad, bad)
    # a real A8 run: the reappearances (D1 14, D2 70, D1 108, D3 137 up 3, A8.9 188 up 6) for a still player facing north
    s, pl = world(52)
    place(s, P[0], P[1], yaw=180.0)
    R = run_pat(s, 'a8')
    byp = {r['pt']: r for r in R}
    bad = []
    for t, name, up in ((14, 'd1', 0), (70, 'd2', 0), (108, 'd1', 0), (137, 'd3', RX['D3']['up']), (188, 'over', RX['A8.9']['up'])):
        b, d = PRIMARY[name]
        f = fdir(180.0 + b)
        want = (P[0] + d * f[0], API.CY + up, P[1] + d * f[2])
        got = byp[t]['pos']
        if math.dist(got, want) > 0.01:
            bad.append((t, name, got, want))
    check(f'S6 A8\'s reappearances at their ticks and spots (D1 14 b -40, D2 8 b {RX["D2"]["bearing"]:+d}, D3 2.5 b +60 3 up, the dive 6 b up)',
          not bad, bad)


# ================================================================================================= ghost (sim)
def sec_ghost():
    for k in KEYS:
        s, pl = world(61)
        place(s, C[0] + 0.5, C[2] + 6.0)
        n0 = len(s.rigl)
        R = run_pat(s, k)
        P = pt_of(R)
        g = [r['pt'] for r in R if r['pat'] == TID[k] and 'rlk_hr_ghost' in r['tags']]
        inv = [r['pt'] for r in R if r['pat'] == TID[k] and r['pt'] >= 1 and 'rlk_hr_ghost' in r['tags'] and 'rlk_mb_inv' not in r['tags']]
        if k in GAUNT:
            off = [r[0] for r in ROWS[k] if r[1] == 'A8.9'][0]
        elif k == 'r2':
            off = 0
        else:
            off = [r[0] for r in ROWS[k] if r[1] == 'solid'][0]
        check(f'G1 {k}: rlk_hr_ghost from T0 to {off - 1} (then off), rlk_mb_inv on her every tick she carries it',
              g == list(range(0, off)) and not inv, (g[:3], g[-3:], inv[:3]))
        if k in ('r1', 'r3'):
            hit = [r['pt'] for r in R if r['pat'] == TID[k] and r['pt'] >= off and 'rlk_mb_inv' in r['tags']]
            check(f'G2 {k}: hittable again from the solid row {off} (no rlk_mb_inv)', not hit, hit[:5])
        if k == 'r2':
            hit = [r['pt'] for r in R if r['pat'] == TID[k] and 'rlk_mb_inv' in r['tags']]
            check('G2 r2: solid and hittable throughout (no ghost, no rlk_mb_inv)', not hit, hit[:5])
        first = [r[2] for r in ROWS[k] if r[2]][0]
        raw = [(P.get(t), c) for t, c in s.rigl[n0:] if P.get(t) is not None]
        i0 = next(i for i, (p, c) in enumerate(raw) if c == f'play/{first}')
        calls = raw[i0:]
        miss = [(r[0], r[2]) for r in ROWS[k] if r[2] and (r[0], f'play/{r[2]}') not in calls
                and (r[0], f'start/{r[2]}') not in calls]
        if k == 'r2':
            miss = [m for m in miss if not (m[1] == 'a7_throw' and m[0] == 30)]      # the second disc only at <= 30 % HP
        check(f'G3 {k}: every clip of the script played at its row', not miss, miss)
        forms = [(p, c) for p, c in calls if c.startswith('look/form/')]
        if k in GAUNT:
            want = [(0, 'look/form/ghost'), (off, 'look/form/normal')]
        elif k in ('r1', 'r3'):
            rf = [r[0] for r in ROWS[k] if r[1] == 'reform'][0] + API.ev('g_reform', 'solid')
            want = [(0, 'look/form/ghost'), (rf, 'look/form/normal')]
        else:
            want = []
        check(f'G4 {k}: the form looks: ghost at T0, normal at {"the dive" if k in GAUNT else "g_reform solid" if want else "-"}',
              forms == want, forms)


# ================================================================================================= frame (sim, base + kit)
WATCH = ('rlk:boss/scarlet/ult/fail60', 'rlk:boss/scarlet/ult/fatal', 'rlk:boss/scarlet/shield/judge',
         'rlk:mboss/arena/hr_field/look/crimson', 'rlk:mboss/arena/hr_field/look/dark')


def watched(s):
    for f in WATCH:
        s.watch[f] = []


def sec_frame():
    # deflect (0 pips): A8 test 22, A13 test 28
    for g, tid, nxt in (('a8', 22, PH['cs2']), ('a13', 28, PH['cs3'])):
        s, pl = world(71)
        place(s, C[0] + 0.5, C[2] + 6.0)
        H.test_id(s, tid)
        R = [rec(s)]
        for _ in range(API.REPEL_T[g] + 2):
            H.heal(s)
            H.world_sc(s)
            R.append(rec(s))
        jt, rt = API.JUDGE_T[g], API.REPEL_T[g]
        span = [r for r in R if r['ph'] == PH[g]]
        lock = [r for r in R if r['ph'] == PH[g] and r['pt'] == rt - 2]
        check(f'J1 {g} deflect: #gres 1 at the judge {jt}, #done at REPEL_T {rt} -> the counter cinematic (ph {nxt})',
              [r['gres'] for r in R if r['pt'] == jt and r['ph'] == PH[g]] == [1] and len(span) == rt and R[-1]['ph'] == nxt,
              (len(span), R[-1]['ph']))
        b = lock[0] if lock else None
        check(f'J2 {g} deflect: she drops from 1 b above the player to the blade lock (on the floor, ~1.2 b from them) by REPEL_T - 2',
              b and abs(b['pos'][1] - API.CY) < 1e-6 and 0.6 <= d2(b['pos'], b['pl']) <= 1.8, b and (b['pos'], b['pl']))
    # A8 fail (test 23): fail60 at the player's floor spot, the landing, P2 at T + 214
    s, pl = world(72)
    place(s, C[0] + 0.5, C[2] + 6.0)
    watched(s)
    n0 = len(s.rigl)
    H.test_id(s, 23)
    R = [rec(s)]
    for _ in range(API.FAIL60_P2_T + 2):
        H.heal(s)
        H.world_sc(s)
        R.append(rec(s))
    P = pt_of(R)
    f60 = [(P.get(t), pos) for t, et, tg, pos in s.watch['rlk:boss/scarlet/ult/fail60']]
    pr = [r for r in R if r['pt'] == API.JUDGE_T['a8'] - 1 and r['ph'] == PH['a8']]      # where the player stood (the push follows)
    check('J3 a8 fail: ult/fail60 once at the judge, at the player\'s floor spot',
          len(f60) == 1 and f60[0][0] == API.JUDGE_T['a8'] and pr and d2(f60[0][1], pr[0]['pl']) < 1e-6 and abs(f60[0][1][1] - API.CY) < 1e-6,
          (f60, pr[:1]))
    land = [r for r in R if r['ph'] == PH['a8'] and r['pt'] == API.JUDGE_T['a8'] + PG.LAND_T]
    ref = [(P.get(t), c) for t, c in s.rigl[n0:] if c == 'play/g_reform']
    span = [r for r in R if r['ph'] == PH['a8']]
    check(f'J4 a8 fail: g_reform at the judge, she lands on the impact point (the player pushed >= 1.4 b off it), P2 at T + {API.FAIL60_P2_T}',
          land and f60 and abs(land[0]['pos'][1] - API.CY) < 1e-6 and d2(land[0]['pos'], f60[0][1]) < 0.01
          and d2(land[0]['pos'], land[0]['pl']) >= 1.4
          and ref and ref[0][0] == API.JUDGE_T['a8'] and len(span) == API.FAIL60_P2_T and R[-1]['ph'] == PH['p2'],
          (land[:1], ref, len(span), R[-1]['ph']))
    # A13 fail (test 29): ult/fatal as the player at 258; the death pauses; the revive -> the stance
    s, pl = world(73)
    s.revive = 30
    place(s, C[0] + 0.5, C[2] + 6.0)
    watched(s)
    H.test_id(s, 29)
    R = [rec(s)]
    for _ in range(API.JUDGE_T['a13'] + 40):
        H.heal(s) if not s.deaths else None
        H.world_sc(s)
        R.append(rec(s))
    P = pt_of(R)
    fat = [(P.get(t), et) for t, et, tg, pos in s.watch['rlk:boss/scarlet/ult/fatal']]
    # I1: exactly rlk_hr_p / rlk_hr_p_<key> (the real rig's parts carry rlk_hr_part)
    left = [tg for _, tg in H.ents_tagged(s, 'rlk_hr_')
            if any(t == 'rlk_hr_p' or t.startswith(('rlk_hr_p_', 'rlk_hr_cut', 'rlk_hr_gsp')) for t in tg)]
    check('J5 a13 fail: ult/fatal once, as the player, at the judge 258; the death pauses the fight, the gauntlet is cancelled',
          fat == [(API.JUDGE_T['a13'], 'player')] and len(s.deaths) == 1 and not left and 'rlk_hr_ghost' not in H.body_of(s).tags,
          (fat, s.deaths, left))
    # kit + theme build: the darkness ticks, the banner, the A13 staging, every kit event at its tick
    for k in KEYS:
        s, pl = world(74, name='kit')
        place(s, C[0] + 0.5, C[2] + 6.0)
        watched(s)
        n0 = len(s.kitl)
        R = run_pat(s, k)
        P = pt_of(R)
        P[R[0]['t']] = 0
        kl = [(P.get(t), c, a) for t, c, a in s.kitl[n0:] if P.get(t) is not None]
        got = {(p, c) for p, c, _ in kl}
        exp = {(t, ('p/' if kind == 'fx' else 'snd/') + name) for t, kind, name, _s in PG.EVENTS[k] if kind in ('fx', 'snd')
               and not (k == 'r2' and t >= 30 and _s and _s[0] == 'a7_throw')}
        miss = sorted(exp - got)
        check(f'J6 {k} (kit build): every kit effect / sound at its EVENTS tick in the sim', not miss, miss[:6])
        looks = [(P.get(t), f.rsplit('/', 1)[1]) for f in WATCH[3:] for t, *_ in s.watch[f] if (P.get(t) or 0) >= 2]
        reqs = sorted({r['pt'] for r in R if r['look'] and r['pat'] == TID[k] and r['pt'] >= 1})
        if k in GAUNT:
            jt = API.JUDGE_T[k]
            warn = [(p, a.get('on')) for p, c, a in kl if c == 'hud/warn']
            # V2 (HR-51): the test id starts the gauntlet without the darkness and its own crimson job (pattern tick <= 1) stamps
            # the arena crimson, so the judge's crimson request starts no second job (before: a crimson job at jt + 1 rewrote the
            # crimson arena); the job after a dark gauntlet's judge: test_scarlet cost (test 20)
            first = [(P.get(t), f.rsplit('/', 1)[1]) for f in WATCH[3:] for t, *_ in s.watch[f] if (P.get(t) or 0) <= 1]
            check(f'J7 {k}: the darkness ticks: crimson requested at the judge {jt}, never dark (the arena crimson since the test\'s '
                  f'start: no second job, V2 HR-51); the banner off there',
                  reqs == [jt] and ('dark' not in [x for _, x in looks]) and first == [(1, 'crimson')]
                  and not [x for x in looks if x[1] == 'crimson'] and warn == [(jt, 0)], (reqs, first, looks, warn))
        else:
            check(f'J7 {k}: no look request, no banner (no darkness in P2 entries)',
                  not reqs and not looks and not [c for _, c, _ in kl if c == 'hud/warn'], (reqs, looks))
    for tid, fail in ((29, True), (28, False)):
        s, pl = world(75, name='kit')
        place(s, C[0] + 0.5, C[2] + 6.0)
        s.revive = 20
        n0 = len(s.kitl)
        H.test_id(s, tid)
        R = [rec(s)]
        for _ in range(API.JUDGE_T['a13'] + 3):
            H.heal(s) if not s.deaths else None
            H.world_sc(s)
            R.append(rec(s))
        P = pt_of(R)
        kl = [(P.get(t), c, a) for t, c, a in s.kitl[n0:]]
        black = [(p, a) for p, c, a in kl if c == 'hud/ovl' and a.get('g') == 'black']
        pw = [(p, a) for p, c, a in kl if c == 'hud/ovl' and a.get('g') == 'pinkwhite']
        line = [(p, a) for p, c, a in kl if c == 'p/scarlet_line']
        pet = [(p, a) for p, c, a in kl if c == 'p/petal_burst']
        sl = [p for p, c, a in kl if c == 'snd/fatal_slash']
        F5 = API.FAIL5_T
        if fail:
            # I1b (request s1k-1): the scarlet line runs across the player's view (yaw 90, as CS1 C8), not along it (yaw 0)
            check('J8 a13 fail (kit): the black at 255 (pips left), at 258 pink-white, the scarlet line {len:600,yaw:90,roll:13} across '
                  'the player\'s view through them, the petal burst {r:20}, the slash sound',
                  black == [(F5['black'], {'g': 'black', 'in': 0, 'hold': 3, 'out': 0})]
                  and pw == [(F5['slash'], {'g': 'pinkwhite', 'in': 0, 'hold': 3, 'out': 8})]
                  and line == [(F5['slash'], {'len': 600, 'yaw': 90, 'roll': 13})] and pet == [(F5['slash'], {'r': 20})] and sl == [F5['slash']],
                  (black, pw, line, pet, sl))
        else:
            check('J8 a13 deflect (kit): no black, no instant-death staging', not black and not pw and not line and not sl, (black, pw))
    # the switches (PLAN §0.1 question 6): A8 with ULT60_LETHAL true = the instant death; A13 with ULT5_LETHAL false = the 500 per-mille hit
    for name, g, tid in (('kit60', 'a8', 23), ('kit5', 'a13', 29)):
        s, pl = world(76, name=name)
        place(s, C[0] + 0.5, C[2] + 6.0)
        s.revive = 20
        watched(s)
        n0 = len(s.kitl)
        H.test_id(s, tid)
        R = [rec(s)]
        for _ in range(API.JUDGE_T[g] + 120):
            H.heal(s) if not s.deaths else None
            H.world_sc(s)
            R.append(rec(s))
        P = pt_of(R)
        jt = API.JUDGE_T[g]
        fat = [P.get(t) for t, *_ in s.watch['rlk:boss/scarlet/ult/fatal']]
        f60 = [P.get(t) for t, *_ in s.watch['rlk:boss/scarlet/ult/fail60']]
        black = [P.get(t) for t, c, a in s.kitl[n0:] if c == 'hud/ovl' and a.get('g') == 'black']
        if g == 'a8':
            check('J9 kit60 (ULT60_LETHAL true): the A8 fail is the instant death (black at JT - 3, ult/fatal at the judge, no fail60), '
                  'the revive restarts A8 (lead_stand)', fat == [jt] and not f60 and black == [jt - 3] and len(s.deaths) == 1
                  and any(r['ph'] == PH['lead'] for r in R) and R[-1]['ph'] in (PH['lead'], PH['a8']), (fat, f60, black, s.deaths, R[-1]['ph']))
        else:
            stance = [r for r in R if r['ph'] == PH['lead']]
            check('J10 kit5 (ULT5_LETHAL false): the A13 fail is the 500 per-mille dive hit (ult/fail60 at the judge, no death, no black, no '
                  'banner), then the revive stance -> A13 again', f60 == [jt] and not fat and not black and not s.deaths and stance
                  and R[-1]['ph'] in (PH['lead'], PH['a13']), (fat, f60, black, s.deaths, R[-1]['ph']))


# ================================================================================================= cancel (sim, snapshots)
def snapshot(s):
    for k in ('cmd_hist', 'particles', 'rigl', 'kitl', 'bar_draws', 'hz_particles', 'sounds'):
        if hasattr(s, k):
            getattr(s, k).clear()
    return copy.deepcopy(s, {id(s.cache): s.cache})


def sec_cancel():
    for k in KEYS:
        s, pl = world(81)
        place(s, C[0] + 0.5, C[2] + 6.0)
        H.test_id(s, TID[k])
        H.hold(s, True)
        bad = []
        for t in range(0, END[k] + 1):
            if hr(s, '#pat') != TID[k]:
                break
            c = snapshot(s)
            if k in GAUNT:
                H.call_sc(c, 'core/g/pause')
            else:
                H.call_sc(c, 'core/cancel_pat')
            H.call_sc(c, f'p/{k}/cancel')                 # idempotent: a second cancel changes nothing
            # I1: also a finished sequence's staging marker (S2b's rlk_hr_stage, kept until the next sequence / cleanup)
            left = [tg for _, tg in H.ents_tagged(c, 'rlk_hr_') if not any(x in ('rlk_hr_anchor',) or x.startswith('rlk_hr_deco') for x in tg)
                    and 'rlk_hr_part' not in tg and 'rlk_hr_stage' not in tg]
            b = H.body_of(c)
            btags, by, pat = set(b.tags), b.pos[1], hr(c, '#pat')
            hz = [e for e in c.ents if e.alive and 'rlk_mb_hz' in e.tags]
            pre = len(c.phits)
            for _ in range(8):
                H.heal(c)
                H.world_sc(c)
            later = [x for x in c.phits[pre:] if x[3] == TID[k]]
            if left or 'rlk_hr_ghost' in btags or 'rlk_mb_mv' in btags or abs(by - API.CY) > 1e-6 or pat != 0 or later or hz:
                bad.append((t, left[:2], sorted(btags & {'rlk_hr_ghost', 'rlk_mb_mv'}), round(by, 2), pat, later[:1], len(hz)))
            H.heal(s)
            H.world_sc(s)
        check(f'C1 {k}: a cancel at every tick 0..{END[k]} ({"core/g/pause" if k in GAUNT else "core/cancel_pat"} + a second cancel) '
              'leaves no entity of the pattern / cut / spot / disc / hazard, the body solid, visible, on the floor, #pat 0, no later hit',
              not bad, bad[:4])


# ================================================================================================= F1 (11-05 review fixes)
# The lead's decisions (HR/review/findings.md, 11-05): HR-19 the counting cuts of A8 / A13 on a tier of their own, TC 37 (raw
# floor(12 x 37 x 135 / 10000) = 5 = 12 HP on the item-less Lv15 player: 9 cuts 40.3 % <= 45 %); HR-15 every moon disc's aim
# locks 7 t before its release (a floor marker at the player's feet; she faces it; the throw aims at it); HR-27 the D2 / D4
# reappearances inside the default F5 view near its edge (+-55 deg); HR-14 R1 / R3 end 12 t after their last hit, R2's kept
# tail moves her (the recovery's walk / glide / strafe) while she turns to the player. Written to fail on the 4c81817 tree.
TC_WANT = 37
F5_DIST, F5_HALF = 3.5, {'16:9': 51.2, '16:10': 48.2}     # the vanilla F5 camera behind the player; FOV 70 half-widths
BODY_HALF_W = 0.5


def disc_ticks(s, key, R0=None, each=None, n=None):
    """Run `key` (test id, AI held) with `each`; per world tick note the new rlk_hr_lock markers (the aims locked), the new
    disc cards (the releases) and the player hits of the pattern. Returns (locks, releases, hits, R) in world ticks."""
    seen_l, seen_d, locks, rels = set(), set(), [], []

    def ev(ss):
        if each:
            each(ss)
    H.test_id(s, TID[key])
    H.hold(s, True)
    p0 = len(s.phits)
    R = [rec(s)]
    for i in range(n or END[key] + 3):
        H.heal(s)
        ev(s)
        H.world_sc(s)
        for e in s.ents:
            if e.alive and 'rlk_hr_lock' in e.tags and S3.tag_p(key) in e.tags and e.id not in seen_l:
                seen_l.add(e.id)
                locks.append(s.t)
            if e.alive and 'rlk_hr_disc' in e.tags and e.id not in seen_d:
                seen_d.add(e.id)
                rels.append(s.t)
        R.append(rec(s))
        if i > 3 and R[-1]['pat'] != TID[key]:
            break
    hits = [t for t, _p, _e, pat in s.phits[p0:] if pat == TID[key]]
    return locks, rels, hits, R


def lock_to_hit(locks, rels, hits):
    """[(release, its lock (else the release itself: the aim fixed at release), the first hit after the release)]"""
    out = []
    for i, r in enumerate(rels):
        lk = max([t for t in locks if t <= r] or [r])
        nxt = rels[i + 1] if i + 1 < len(rels) else 10 ** 9
        h = [t for t in hits if r <= t < nxt]
        out.append((r, lk, h[0] if h else None))
    return out


def walker_in(cx, cz, v, stop=2.5, t_from=None):
    """A player walking straight toward her body at v b/t (from pattern tick t_from on), stopping `stop` b from her."""
    def each(s):
        if t_from is not None and hr(s, '#pt') < t_from:
            return
        b, p = H.body_of(s), s.player()
        dx, dz = b.pos[0] - p.pos[0], b.pos[2] - p.pos[2]
        d = math.hypot(dx, dz)
        if d > stop:
            p.pos = [p.pos[0] + v * dx / d, API.CY, p.pos[2] + v * dz / d]
            H.C.moved(s)
    return each


def f5_angle(ppos, pyaw, her):
    """Her horizontal angle off the default F5 camera's axis (deg), the camera F5_DIST b behind the player along their
    facing, + her half width seen from there."""
    f = fdir(pyaw)
    cam = (ppos[0] - F5_DIST * f[0], 0.0, ppos[2] - F5_DIST * f[2])
    d = math.hypot(her[0] - cam[0], her[2] - cam[2])
    return angdiff(yaw_of(cam, her), pyaw) + math.degrees(math.atan2(BODY_HALF_W, d))


def done_tick(key):
    t = None
    for rel, lines in my_files().items():
        m = re.fullmatch(rf'p/{key}/k/(\d+)', rel)
        if m and any('scoreboard players set #done hr 1' in ln and not ln.startswith('#') for ln in lines):
            t = max(t or 0, int(m.group(1)))
    return t


def sec_f1():
    F = my_files()
    # HR-19: the counting cuts of A8 / A13 on their own tier TC 37; R1 / R3 keep T2 / T3
    bad = []
    for k in KEYS:
        for c in CUTS[k]:
            made = c[0]
            mk = [ln for ln in F.get(f'p/{k}/k/{made}', []) if 'g/cut/make' in ln and f's:{c[2]},' in ln]
            dm = [int(m) for ln in mk for m in re.findall(r'dmg:(\d+)', ln)]
            want = TC_WANT if k in GAUNT else {'T2': 42, 'T3': 62}[c[3]]      # S5 (11-06): T3 56 -> 62
            if dm != [want]:
                bad.append((k, c[2], dm, want))
    raw = 12 * TC_WANT * 135 // 10000
    check(f'G1 HR-19 every counting cut of A8 / A13 is made at TC {TC_WANT} % (raw {raw} = 12 HP on the Lv15 player: 9 cuts '
          f'<= 45 % max HP); R1 / R3 cuts keep T2 42 / T3 62 (S5)', not bad, bad[:4])
    # HR-15 (static): the lock 7 t before every release; the throw aims at the lock marker
    th = cmd_lines(F.get('g/disc/throw', []))
    aim = [ln for ln in th if 'facing entity' in ln]
    lk = cmd_lines(F.get('g/disc/lock', []))
    miss = []
    for k, rels in API.DISC_RELEASE.items():
        for r in rels:
            body = '\n'.join(F.get(f'p/{k}/k/{r - API.LOCK_LEAD}', []))
            if 'g/disc/lock' not in body:
                miss.append((k, r - API.LOCK_LEAD))
    check(f'G2 HR-15 every disc\'s aim locks {API.LOCK_LEAD} t before its release (g/disc/lock: a marker at the player\'s feet on '
          'the floor, she faces it); g/disc/throw aims at the lock marker, not at the player',
          not miss and lk and any('summon minecraft:marker' in ln and 'rlk_hr_lock' in ln for ln in lk)
          and aim and all('tag=rlk_hr_lock' in ln and 'tag=rlk_body' not in ln for ln in aim), (miss, aim[:2]))
    # HR-15 (sim): R2 against a player walking in at 0.22 / 0.28 b/t from 5 / 7 / 9 b: each disc hits >= 7 t after the lock
    bad, seen = [], []
    for v in (0.22, 0.28):
        for d0 in (5.0, 7.0, 9.0):
            s, pl = world(81)
            H.place_body(s, C[0], C[2] - 4)
            place(s, C[0] + 0.5, C[2] - 4 + d0)
            locks, rels, hits, R = disc_ticks(s, 'r2', each=walker_in(C[0], C[2], v))
            for r, lk_, h in lock_to_hit(locks, rels, hits):
                seen.append((v, d0, r - lk_, h - lk_ if h else None))
                if h is None or h - lk_ < API.LOCK_LEAD:
                    bad.append((v, d0, r, lk_, h))
    check(f'G3 HR-15 R2, a player walking in at 0.22 / 0.28 b/t from 5 / 7 / 9 b: every disc hits >= {API.LOCK_LEAD} t after its '
          'aim locked', not bad and len(seen) == 6, (bad[:3], seen))
    # ... and against the rim (she at r 19, her retreat falls back to 4 b sideways), the player standing 5 / 7 / 9 b in front
    bad, seen = [], []
    for d0 in (5.0, 7.0, 9.0):
        s, pl = world(82)
        H.place_body(s, C[0], C[2] - 19)
        place(s, C[0] + 0.5, C[2] - 19 + d0)
        locks, rels, hits, R = disc_ticks(s, 'r2')
        for r, lk_, h in lock_to_hit(locks, rels, hits):
            seen.append((d0, r - lk_, h - lk_ if h else None))
            if h is None or h - lk_ < API.LOCK_LEAD:
                bad.append((d0, r, lk_, h))
    check(f'G4 HR-15 R2 near the rim (her retreat cut short), a standing player at 5 / 7 / 9 b: the disc hits >= {API.LOCK_LEAD} t after '
          'its aim locked', not bad and len(seen) == 3, (bad, seen))
    # ... A13's three discs against a player walking in at 0.22 b/t from T+141 (stopping 3 b from her)
    s, pl = world(83)
    place(s, C[0] + 0.5, C[2] + 6.0)
    locks, rels, hits, R = disc_ticks(s, 'a13', each=walker_in(C[0], C[2], 0.22, stop=3.0, t_from=141), n=200)
    got = lock_to_hit(locks, rels, hits)
    check(f'G5 HR-15 A13, a player walking in at 0.22 b/t from T+141: each of the 3 discs hits >= {API.LOCK_LEAD} t after its aim '
          'locked', len(got) == 3 and all(h is not None and h - lk_ >= API.LOCK_LEAD for _r, lk_, h in got), got)
    # HR-27: the D2 / D4 reappearances inside the default F5 view (16:9 and 16:10), near its edge (>= 30 deg off the axis)
    rows = []
    for k, step in (('a8', 'D2'), ('a13', 'D2'), ('a13', 'D4'), ('r3', 'D2')):
        for t, st, _cl, _c in ROWS[k]:
            if st == step:
                rows.append((k, step, t))
    bad, seen = [], []
    for k, step, t in rows:
        s, pl = world(84)
        P = (C[0] + 0.5, C[2] + 6.0)
        place(s, P[0], P[1], yaw=180.0)
        H.place_body(s, C[0], C[2] - 4)
        R = run_pat(s, k, n=t + 2)
        r = [x for x in R if x['pt'] == t and x['pat'] == TID[k]]
        if not r:
            bad.append((k, step, t, 'not reached'))
            continue
        a = f5_angle((P[0], 0, P[1]), 180.0, r[0]['pos'])
        seen.append((k, step, t, round(a, 1)))
        if not (30.0 <= a <= F5_HALF['16:10']):
            bad.append((k, step, t, round(a, 1)))
    check(f'G6 HR-27 D2 / D4 reappear inside the default F5 view (FOV 70: 16:9 {F5_HALF["16:9"]} / 16:10 {F5_HALF["16:10"]} deg half-width, '
          'her body included) near its edge (>= 30 deg)', not bad and len(seen) == 4, (bad, seen))
    # HR-14: R1 / R3 end 12 t after their last hit; R2's kept tail moves her (a recovery move) while she turns to the player
    for k in ('r1', 'r3'):
        last = max(c[2] for c in CUTS[k])
        end = done_tick(k)
        check(f'G7 HR-14 {k}: ends at most 12 t after its last hit ({last} -> {end})', end is not None and end - last <= 12, (last, end))
    s, pl = world(85)
    H.place_body(s, C[0], C[2] - 4)
    P = (C[0] + 0.5, C[2] + 4.0)
    place(s, *P)
    n0 = len(s.rigl)
    R = run_pat(s, 'r2', each=lambda ss: place(ss, *P))
    rel = API.DISC_RELEASE['r2'][0]
    t0 = R[0]['t']
    clips = [(t - t0, c) for t, c in s.rigl[n0:] if c.startswith('play/') and t - t0 > rel]
    tail = [r for r in R if r['pat'] == TID['r2'] and r['pt'] > rel + 5]
    moved = tail and d2(tail[0]['pos'], tail[-1]['pos']) >= 1.0
    errs = [angdiff(r['yaw'], yaw_of(r['pos'], (P[0], 0, P[1]))) for r in tail]
    check('G8 HR-14 R2\'s kept tail after its release: the recovery\'s move clip (walk / glide / strafe), she moves >= 1 b and turns '
          'to the player', clips and clips[0][1] in ('play/walk', 'play/glide', 'play/strafe_l', 'play/strafe_r') and moved
          and errs and errs[-1] <= 12.0, (clips[:2], round(d2(tail[0]['pos'], tail[-1]['pos']), 2) if tail else None,
                                          [round(e) for e in errs[::5]]))
    # HR-14 (F1 round 1, VF1R-01: "during any tail kept ... she walks / strafes facing and tracking the player"): R1 / R3's
    # reform tail moves her too - from the solid row (hittable again, the reform over) the recovery's move and clip
    # (ai/tail), one step each later tick to the end (ai/tail_step), no idle2 over it; the recovery keeps the move
    F = my_files()
    for k in ('r1', 'r3'):
        solid = next(r[0] for r in ROWS[k] if r[1] == 'solid')
        end = done_tick(k)

        def calls(t, name):
            return [ln for ln in F.get(f'p/{k}/k/{t}', []) if re.search(rf'function rlk:boss/scarlet/{name}$', ln)]
        miss = ([solid] if not calls(solid, 'ai/tail') else []) + [t for t in range(solid + 1, end or 0) if not calls(t, 'ai/tail_step')]
        idle = [t for t in range(solid, (end or 0) + 1) if any('rig/play/idle2' in ln for ln in F.get(f'p/{k}/k/{t}', []))]
        check(f'G9 HR-14 {k}: from the solid row {solid} the recovery\'s move (ai/tail), a step each tick to the end {end} '
              '(ai/tail_step), no idle2 over it', end is not None and not miss and not idle, (end, miss, idle))
        s, pl = world(86)
        H.place_body(s, C[0], C[2] - 4)
        P = (C[0] + 0.5, C[2] + 4.0)
        place(s, *P)
        n0 = len(s.rigl)
        R = run_pat(s, k, each=lambda ss: place(ss, *P))
        t0 = R[0]['t']
        plays = [(t - t0, c) for t, c in s.rigl[n0:] if c.startswith('play/') and t - t0 >= solid]
        at = {r['pt']: r for r in R if r['pat'] == TID[k]}
        moved = d2(at[solid]['pos'], at[end - 1]['pos']) if end and solid in at and end - 1 in at else 0.0
        ok = (plays[:1] and plays[0] == (solid, plays[0][1]) and plays[0][1] in ('play/walk', 'play/glide', 'play/strafe_l', 'play/strafe_r')
              and len(plays) == 1 and moved >= 0.08 * (end - 1 - solid))
        check(f'G10 HR-14 {k} (sim): a move clip at the solid row {solid}, she moves in the tail (>= 0.08 b / t), no other clip to '
              'the end and at the recovery start (the move kept)', ok, (plays[:3], round(moved, 2)))
    # F1 round 1, VF1-03 / VF1R-03 (HR-27's comments): the g/spot/d2 / d4 headers name the bearings and distances their
    # candidates turn to (5b8ee01 still said +-80 there while the commands turned +-55)
    bad = []
    for n in ('d2', 'd4'):
        lines = F.get(f'g/spot/{n}', [])
        cand = [(int(r), float(d)) for ln in cmd_lines(lines)
                for r, d in re.findall(r'rotated ~(-?\d+) 0 positioned \^ \^ \^([\d.]+) if function', ln)]
        m = re.search(r'reappear: ([\d.]+) b at ([+-]\d+) .*?; else ([+-]\d+) / 0 / \+-(\d+) at ([\d.]+) b', lines[0] if lines else '')
        said = None
        if m:
            d1, b1, b2, b3, d3 = float(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), float(m.group(5))
            sg = 1 if b1 > 0 else -1
            said = [(b1, d1), (b2, d1), (0, d1), (sg * b3, d3), (-sg * b3, d3)]
        if said != cand:
            bad.append((n, said, cand))
    check('G11 HR-27 (VF1-03): the g/spot/d2 / d4 headers name the bearings and distances their candidates use', not bad, bad)
    # F1 round 1, VF1-04 (HR-15's comments): api.disc()'s docstring names its aim, the lock (not the player at the release)
    doc = ' '.join((API.disc.__doc__ or '').split())
    check('G12 HR-15 (VF1-04): api.disc()\'s docstring: the throw is rotated toward its lock (g/disc/lock)',
          'toward its lock' in doc and 'g/disc/lock' in doc and 'position at release' not in doc, doc[:160])


# ================================================================================================= kept (F2: sim, the kit running)
def sec_kept():
    """F2 (HR-17): the A13 instant death's 홍련일섬 line, its petals and the judge tick's bolts carry the kit's keep tag: with the
    kit running for real (H.kit_on), the cards made in the fatal tick are alive >= 12 t after it (death_start's fx/clear and
    the ager's dead / revive clears skip them); the A13 deflect makes none. HR-23: the A13 / R2 yellow tell between
    fx/follow_on and fx/follow_off (its cards travel with her)."""
    keep_t = getattr(API, 'KIT_KEEP_TAG', 'rlk_hr_fx_keep')
    s, pl = world(78, name='kit')
    H.kit_on(s)
    place(s, C[0] + 0.5, C[2] + 6.0)
    s.revive = 20
    watched(s)
    H.test_id(s, 29)
    log = []
    for _ in range(API.JUDGE_T['a13'] + 40):
        H.heal(s) if not s.deaths else None
        H.world_sc(s)
        now = {e.id: e for e in s.ents if e.alive and e.etype == 'item_display' and 'rlk_hr_fx' in e.tags}
        log.append((s.t, set(now), {i for i, e in now.items() if keep_t in e.tags}))
    fat = [t for t, *_ in s.watch['rlk:boss/scarlet/ult/fatal']]
    tf = fat[0] if fat else None
    at = {t: (ids, kp) for t, ids, kp in log}
    before = at.get(tf - 1, (set(), set()))[0] if tf else set()
    made, kept = (at[tf][0] - before, at[tf][1] - before) if tf in at else (set(), set())
    end = {i: s.sc(('e', i), 'hrFxD') for i in kept}
    line = max(kept, key=lambda i: end[i] or 0) if kept else None
    early = [i for i in kept if tf + 2 in at and (end[i] or 0) > tf + 3 and i not in at[tf + 2][0]]
    check('K1 a13 fail (kit running): the cards of the fatal tick (the 홍련일섬 line, its petals, the bolts) carry the keep tag '
          'and outlive the death clears; the line (the longest) is alive 12 t and 20 t after it',
          tf is not None and len(kept) >= 2 and kept == made and line in at.get(tf + 12, (set(),))[0]
          and line in at.get(tf + 20, (set(),))[0] and not early and (end[line] or 0) - tf >= 30,
          (tf, len(made), len(kept), end.get(line), early[:3]))
    check('K2 a13 fail: the kept cards end with their life (gone 40 t after)', tf is not None and tf + 40 in at
          and not (kept & at[tf + 40][0]), len(kept & at.get((tf or 0) + 40, (set(),))[0]))
    for key in ('a13', 'r2'):
        sites = []
        for p in sorted((FN / 'p' / key).rglob('*.mcfunction')):
            L = [x for x in p.read_text(encoding='utf-8').split('\n') if x and not x.startswith('#')]
            for i, x in enumerate(L):
                if 'fx/p/yellow_tell' in x:
                    sites.append((p.name, any(L[j].endswith('fx/follow_on') for j in range(i))
                                  and any(L[j].endswith('fx/follow_off') for j in range(i + 1, len(L)))))
        check(f'K3 {key}: the yellow tell between fx/follow_on and fx/follow_off ({sites})', sites and all(ok for _, ok in sites))


def main():
    try:
        for sec in SECTIONS:
            globals()[f'sec_{sec}']()
    finally:
        if 'root' in VARS:
            H.drop_variant(VARS.pop('root'))
    return H.summary('pat_ghost')


if __name__ == '__main__':
    sys.exit(main())

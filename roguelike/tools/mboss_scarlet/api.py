"""Frozen D0 contract of the 홍련 (Scarlet, special boss) module generator: every stage (S1 framework FN-a/b/c/f, S1K
kit + arena hr_field, S2a rig, S2b cinematic clips + sequences, S3 core / AI / P1 / shield / event logic, S4 ghost
patterns, SR the reward item + buff hand files) imports this file and never edits it. A change goes through a request
(S:hr/requests/<stage>.md) applied by the lead at integration (I1). Prose version: S:hr/contract.md; design:
S:hr/PLAN.md (section numbers below refer to it; §9.0 lists what this file freezes, §9.2 the stage contracts).

Importing has no side effects (no files written); it asserts the contract's own consistency (pure data: clip events
inside their clips, HITS / scripts / LINE_AT against CLIPS, the §9.1 ownership exactly once, the kit sprite budget).
Units: Python helpers take blocks / ticks / degrees; the framework boundary is tenths of a block and % of the base hit
(atk 12 x dmgMul 135: raw = floor(0.162 x pct)).
HR rebuild on the new combat (11-11; design tools/dev/plan/combat/hr_design.md, §5.1 = this file, owner lane H1; §8 wins).
The H1 interface commit landed additively (the 11-06 module kept building):
  final at once   the new names (GAUGE, BAL, PP_FLINCH, CUE_*, FLASH, PURPLE_LEAD, NP_OWN, BAL_OFF, STAGE_FMAX, CS0_*, SKIP,
                  CONTACT, ACTOR_*, actor / actor_ready / cam_req, the kit names of lanes H1c / H2c), the 12 new fight clips
                  (CLIP_OWNER 'H1') and the whole sequence / cinematic contract of lane H2 / H2c: SEQS, SEQ_LEN, SEQ_ARGS,
                  SEQ_CLIPS, SEQ_EXTRA, LINE_AT, MUSIC_AT, SKIP_T / SKIP_WINDOW, END_H, COUNTER_EV, the 8 cinematic rows of
                  CLIPS_PLAN (CLIP_OWNER 'H2'), the registry numbers intro 1450 / death 1494, WARN_TEXT.
  H1's build      the pattern side (HITS with the P / N column, WEIGHTS, COOLDOWN, MID_MAX / MID_MIN, FAR_RULE, PAT_END, the
                  gauntlet scripts G1 / G2, CUT_IDS, BOLTS, JUDGE_T = REPEL_T, FAIL*_T, P1 / P2, TEST_IDS, PIP_RULE) and the
                  removals of §5.1 (the down window, R1-R3, the moon discs, the dark look requests, the dash-timed pips).
Other lanes' parts are picked up when they land, never required before:
  seq.py          its SERVICES are used once the file declares `CONTRACT = 2` (= api.SEQ_CONTRACT) on a line of its own;
                  until then every sequence runs as the core stand-in core/sq/<name> (wait the length, the signals at their
                  events). tools/build_mboss_scarlet.py reads the marker before importing the file.
  scarlet_cine.mjs / scarlet_clips.mjs   a contract clip the files do not author with the contract's length is built as a
                  static placeholder (build_scarlet_rig.mjs prints them; the manifest marks them `placeholder`).
  the kit         KIT_PRESETS / OVERLAYS / KIT_SPRITES hold a new H-lane name once tools/build_mboss_hr_fx.py declares it
                  (kit_declares: `@preset('<name>'`, `api.OVERLAYS['<name>']`, a sprite group `'<name>': [`); the full plan is
                  KIT_PRESETS_PLAN / OVERLAYS_PLAN, and api.K returns '' for a planned name the kit manifest lacks.
  the actor       api.actor() lines are '' until tools/player_motion/cine/manifest.json exists (actor_ready()).
  the camera      api.cam_req() is '' until the framework has FN-cam (tools/build_mboss_core.py writes #mbCam).

    python3 tools/mboss_scarlet/api.py --write-stub   (lead only) regenerates stub_rig_manifest.json from this file
    python3 tools/mboss_scarlet/api.py --check        every self-check + check_manifest on the stub and on the manifest
                                                     in use + the vanilla sound ids (R:tools/dev/sim/rd/tests)
"""
from dataclasses import dataclass, field
from fnmatch import fnmatchcase
from pathlib import Path
import json
import math
import sys

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
import mboss_lib as L  # noqa: E402

# =============================================================================================
# 1. Identity, registry entry, arena (PLAN §0, §6, §8)
ID = 'scarlet'
N = 21
ROOT = L.fn_root_of(ID)                     # 'boss/scarlet'
NS = f'rlk:{ROOT}/'
FDIR = L.FN / ROOT
REG = L.load_registry()
BOSS = dict(next(b for b in REG['boss'] if b['id'] == ID))
assert BOSS['kind'] == 'special' and BOSS['n'] == N and ROOT == 'boss/scarlet', BOSS
assert BOSS['el'] == 3 and BOSS['res'] == {'*': 10} and BOSS['phases'] == [100], 'PLAN §0: Electro, no immunity, one pool'
assert (BOSS['picks'], BOSS['lvup'], BOSS['xp'], BOSS['intro'], BOSS['death']) == (1, 1, 0, 1450, 1494), 'hr_design §3.6'
assert (BOSS['scale'], BOSS['hit']) == (1.0, {'w': 1.2, 'h': 2.4}) and not BOSS.get('px'), 'PLAN §2.1: no hit proxies (S2d: player size)'
NAME, SUB, COLOR = BOSS['name'], BOSS['sub'], BOSS['color']      # 홍련 / 월하곡 / #E8466A
TITLE = (NAME, SUB, COLOR)        # mboss_lib.title(*TITLE) at the draw: clip intro_end 'draw' (CS0 610, PLAN §3.1)
ELEC = 3                          # #elem of every hit (Electro), 1U each
EL_U = 1000
MUSIC_PH = {1: 'P1 (cherry grove pool, from intro_end music)', 2: 'P2 (crimson forest, from cs1 music)',
            3: 'CS4 ending (cherry grove once, from ending music)'}
assert sorted(int(k) for k in BOSS['music']) == sorted(MUSIC_PH)

AID = 'hr_field'
# The arena entry D0 added to arenas{} (PLAN §6.1); stub functions until S1K's theme tools/mboss_arena_hr_field.py exists.
ARENA_SPEC = {'n': 5, 'theme': 'hr_field', 'ver': 1, 'cx': 880, 'cy': 201, 'cz': 8, 'r': 28, 'walk': 25, 'safe': 23,
              'start': {'x': 880.5, 'y': 201.0, 'z': 31.5, 'yaw': 180.0, 'pitch': 0.0},
              'box': {'x0': 832, 'y0': 190, 'z0': -40, 'x1': 928, 'y1': 250, 'z1': 56},
              'looks': ['moon', 'crimson', 'dark'], 'oob': {'y0': 198, 'y1': 236}}
assert AID in REG.get('arenas', {}), f'arenas.{AID} missing (D0 adds it)'
assert all(REG['arenas'][AID].get(k) == v for k, v in ARENA_SPEC.items()), f'arenas.{AID} differs from the D0 contract'
assert BOSS['arena'] == AID
ARENA = dict(ARENA_SPEC, aid=AID)
CX, CY, CZ = ARENA['cx'], ARENA['cy'], ARENA['cz']    # block corner = the axis C (880.0 201 8.0); floor blocks at y 200
WALK, SAFE = float(ARENA['walk']), float(ARENA['safe'])
ARENA_LOOKS = tuple(ARENA['looks'])
LOOK_DEFAULT, LOOK_P2, LOOK_DARK = 'moon', 'crimson', 'dark'    # P1 / P2 (CS1 173-176) / the gauntlets (T0 - 17 -> judge)
LOOK_ID = {'moon': 1, 'crimson': 2, 'dark': 3}                  # values of the request #hrLook hr (0 = none pending)
LOOK_REQ = '#hrLook'                                             # objective OBJ; the core starts the job when #mbArBuild 0
# "north" = -z = bearing 0 (the moon side); bearings clockwise (90 = east, +x). The moon: a block disc r 5 on the north
# dome wall at bearing 12, elevation 22 from C, facing south, in open sky right of the pine crown (PLAN §6.2).
MOON_POS = (889.0, 218.0, -34.0)
MOON_BEARING, MOON_ELEV, MOON_R = 12, 22, 5
# CS0: her seat (kit prop seat_rock) on the start -> moon line (§3.1), 26.7 b from start. I1b (lead decision 1): 5 b nearer
# start than D0's (884.5, 201, 0), so the 0.15 b/t walk (17 legs of 1.2 b) meets a player who stays at start at <= 7 b.
SEAT_POS = (884.0, 201.0, 5.0)
# Decor props the module (S3) spawns at `spawn` (kit fx/prop/*, PLAN §6.7). S1K's theme may override them with a dict
# DECO of the same shape (deco() reads it); these are the D0 defaults: the halo card 1 b in front of the moon, eight lotus
# flowers on the pond (bearing, r) at the water surface, the seat rock.
LOTUS_POLAR = ((304, 30.5), (316, 33.0), (333, 29.0), (346, 32.0), (2, 30.0), (14, 33.5), (44, 30.0), (55, 33.0))
DECO_DEFAULT = {
    'moon_halo': (MOON_POS[0], MOON_POS[1], MOON_POS[2] + 1.0),
    'lotus': tuple((round(CX + r * math.sin(math.radians(b)), 2), CY - 0.1, round(CZ - r * math.cos(math.radians(b)), 2))
                   for b, r in LOTUS_POLAR),
    'seat_rock': SEAT_POS,
}
THEME_FILE = _TOOLS / f'mboss_arena_{AID}.py'                    # S1K


def theme_ready():
    """True once S1K's theme module exists (then mboss/arena/hr_field/look/<look> exists; before it the arena
    generator writes only the stub ensure / build / clear / done / rebuild / sweep)."""
    return THEME_FILE.exists()


def arena_look(look):
    """The look REQUEST line (PLAN §6.6, §9.2): `#hrLook hr` = LOOK_ID[look]; the core (S3) turns it into the look job
    (look_job) at the first tick with #mbArBuild 0, so a pause / reload inside a running job can no longer leave the
    arena dark. '' until theme_ready(): no stage may reference another stage's functions before they exist."""
    assert look in ARENA_LOOKS, look
    return f'scoreboard players set {LOOK_REQ} {OBJ} {LOOK_ID[look]}' if theme_ready() else ''


def look_job(look):
    """The framework look-job call the core issues for a pending request ('' until theme_ready())."""
    assert look in ARENA_LOOKS, look
    return f'function rlk:mboss/arena/{AID}/look/{look}' if theme_ready() else ''


def deco():
    """Decor prop points {moon_halo: (x,y,z), lotus: ((x,y,z) x 8), seat_rock: (x,y,z)}: the theme's DECO when S1K's
    module defines it, else DECO_DEFAULT (S3 spawns from here; S1K keeps every point on its pond / field)."""
    th = L.theme_module(ARENA['theme']) if theme_ready() else None
    d = getattr(th, 'DECO', None) if th else None
    if d:
        assert set(d) == set(DECO_DEFAULT) and len(d['lotus']) == len(DECO_DEFAULT['lotus']), 'theme DECO shape'
        return d
    return DECO_DEFAULT


def xyz(p, nd=4):
    """An absolute point (x, y, z) for summon / tp / execute positioned / facing, written so that the game uses exactly that
    point: x and z keep a decimal point. The game block-centres an absolute x / z written without one (+0.5; never y), while
    mcsim / hrsim read every coordinate as written: L.num(884.0) = `884` put the seat rock and her seated start at (884.5,
    201, 5.5) in game but at SEAT_POS in the suites (I1b verification round 2, m1)."""
    def exact(v):
        s = L.num(v, nd)
        return s if '.' in s else s + '.0'
    return f'{exact(p[0])} {L.num(p[1], nd)} {exact(p[2])}'

# =============================================================================================
# 2. Damage, shapes, hits, telegraph constants (PLAN §4.1-4.5)
DMG = {'T1': 31, 'T2': 42, 'T3': 54, 'T4': 61}         # % of the base hit (mboss/hurt coefficient)
# Round V (11-12): the integration measured T1 (the P1 walker's intake / 타키's) at 1.02 / 1.03 / 0.97 on the merged tree
# (band 1.00-1.15; lane VB's moves shift where the next pick starts from) and raised T2 to 44 (raw 7) to bring seed 33 in.
# The lead took that back: the pooled value (1.007) is in band — the same reading as HB's per-seed caveat — and the user's
# playtest asked for a fight that is easier to read, not one that hits harder. T2 stays 42 (raw 6), as in 11-11b.
# HB (11-11, the balance pass, hr_design §6.4's tier knob +-20 %; mboss/hurt floors 12 x coef x 135 / 10000, so a tier moves in
# whole raw steps): T1 29 -> 31 (raw 4 -> 5, the chain hits; 31 is the smallest coefficient of raw 5): with fewer ultimates
# (GAUGE['hit']) the walker's P1 intake fell under 타키's (T1) and the P hits' share of it under T1b's need; T3 62 -> 54 (raw 10
# -> 8) and T4 71 -> 61 (raw 11 -> 9): the unparriable hits are most of what an average parrier (T1b) still takes.
# S5 (11-06, the balance pass; PLAN §4.8's tier knob +-20 %): T3 56 -> 62 (+10.7 %: mboss/hurt's raw hit 9 -> 10, 23 -> 25 HP
# on the item-less Lv15 player) - the tier of A4's dive, A9, A10, R1's third and R3's second cut; T1 / T2 / T4 as 타키.
# F1 (HR-19, lead decision 11-05): the counting cuts of A8 / A13 on a tier of their own (raw 5 = 12 HP on the item-less
# Lv15 player: 9 cuts 40.3 % <= PLAN §4.8's 45 %, so A8's 50 % fail hit leaves HP without the #mbDotLethal clamp); R1 / R3
# and every other T2 hit keep T2. Coefficients 31-37 all give raw 5 (mboss/hurt floors 12 x coef x 135 / 10000).
DMG['TC'] = 37
# kit colour arg c (PLAN §4.1): 1 lilac sword-qi #C97EDD / rim #FFE6FA, 2 pink-magenta (A1 glint + fan, A4 glint, A9 cut,
# A8.8 glow), 3 yellow tell #FFE14A, 4 crimson (P2 accents, 홍련일섬), 5 white glint
C_LILAC, C_MAGENTA, C_YELLOW, C_CRIMSON, C_WHITE = 1, 2, 3, 4, 5
KB_CHAIN, KB_FINAL, KB_SINGLE, KB_CUT = 0, 3, 2, 0    # chain hits / the last hit of a chain (0.6 b) / single hits / cuts
# HITS[key] = [(clip, event, shape, dims, tier, kb, parry)] (blocks; tier a DMG key; parry 'P' parryable / 'N' unparriable,
# hr_design §2.1-2.2). Shapes (framework mboss/hz/*):
#   sector(r, half_deg) round her; disc(r) round her (rings: at her spot; a4 / a10: at the landing lock); line(len, w) ahead
#   of her (nb / q beam: through the lock, LINE_YAW); dash_line(w) along her dash (length = the dash); pdisc(r) = a disc at
#   the player's locked spot (the cut builder cut(): following the player until strike - LOCK_LEAD); full = the whole arena.
# Every hit Electro 1U, #hzQuiet 1, no floor decal. Every hazard is made with an explicit hz_opts(noparry=0 | 1): a P hit
# is announced by the parry cue CUE_LEAD t before it (CUE_KIT at blade_mid + CUE_SND), an N hit by the module's own flash
# (FLASH: yellow / purple / blue; #mbNpOwn mb 1 keeps the framework glint off). The a8 / a13 entries are derived from the
# scripts of section 3 by _script_hits (section 7): each cut lands on the move whose clip 'hit' meets its strike tick.
# HA-08 (review H-A, lead ruling; README 0-6, 타키's lesson: knockback only on the last hit of a chain): q's grab is the
# first hit of a chain (the beam, the dive, the pillar follow when it lands), so it pushes nothing (kb 0): the throw is her
# pose (q_air 0-2), the player stays where the aimed beam then finds them; only the pillar (the last hit) knocks back.
_RING = ('disc', (2.6,))
HITS = {
    'a1': [('a1', 'hit', 'sector', (4.0, 80), 'T2', KB_SINGLE, 'P')],
    'a2': [('a2', 'hit', 'sector', (3.6, 70), 'T2', KB_SINGLE, 'P')],
    'a3': [('a3', 'h1', 'sector', (4.2, 90), 'T1', KB_CHAIN, 'P'), ('a3', 'h2', 'sector', (4.0, 60), 'T1', KB_CHAIN, 'P'),
           ('a3', 'h3', 'sector', (4.0, 50), 'T1', KB_CHAIN, 'P'), ('a3', 'h4', 'line', (5.0, 1.8), 'T1', KB_CHAIN, 'P'),
           ('a3', 'h5', 'sector', (4.6, 70), 'T2', KB_FINAL, 'P')],
    'a3s': [('a3', 'h1', 'sector', (4.2, 90), 'T1', KB_CHAIN, 'P'), ('a3', 'h2', 'sector', (4.0, 60), 'T2', KB_FINAL, 'P')],
    'd4': [('d4', 'h1', 'disc', (3.0,), 'T1', KB_CHAIN, 'P'), ('d4', 'h2', 'sector', (4.2, 35), 'T1', KB_CHAIN, 'P'),
           ('d4', 'h3', 'line', (5.0, 1.8), 'T1', KB_CHAIN, 'P'), ('d4', 'h4', 'sector', (3.6, 60), 'T2', KB_FINAL, 'P')],
    'tri': [('tri', 'h0', 'line', (6.0, 1.6), 'T1', KB_CHAIN, 'P'), ('tri', 'h1', 'sector', (5.0, 80), 'T1', KB_CHAIN, 'P'),
            ('tri', 'h2', 'sector', (5.0, 80), 'T1', KB_CHAIN, 'P'), ('tri', 'h3', 'sector', (5.0, 80), 'T2', KB_FINAL, 'P')],
    'a4': [('a4', 'hit', 'disc', (2.6,), 'T3', KB_CHAIN, 'P'), ('a4', 'hit2', 'disc', (3.0,), 'T1', KB_SINGLE, 'P')],   # A4 + A5
    # rings: P1 = rows 0-3 (r4 the last: T2 kb 3); P2 = rows 0-2, 4, 5 (r4 a chain hit, r5 the last): HIT_PH
    'rings': [('rings', 'r1') + _RING + ('T1', KB_CHAIN, 'P'), ('rings', 'r2') + _RING + ('T1', KB_CHAIN, 'P'),
              ('rings', 'r3') + _RING + ('T1', KB_CHAIN, 'P'), ('rings', 'r4') + _RING + ('T2', KB_FINAL, 'P'),
              ('rings', 'r4') + _RING + ('T1', KB_CHAIN, 'P'), ('rings', 'r5') + _RING + ('T2', KB_FINAL, 'P')],
    'ult': [('ult', 'cut1', 'full', (), 'T2', KB_CHAIN, 'N'), ('ult', 'cut2', 'full', (), 'T3', KB_FINAL, 'N')],
    'a6': [],                                                                                              # no hit
    'a9': [('a9', 'cut', 'dash_line', (2.4,), 'T3', KB_FINAL, 'N'), ('a9', 'cut', 'pdisc', (4.0,), 'T3', KB_FINAL, 'N')],  # 1 group
    'a10': [('a10', 'hit', 'disc', (3.5,), 'T3', KB_FINAL, 'N')],
    'hcut': [('hcut', 'cut', 'dash_line', (3.0,), 'T3', KB_FINAL, 'N'), ('hcut', 'cut', 'pdisc', (4.5,), 'T3', KB_FINAL, 'N')],
    'blue': [('blue', 'hit', 'dash_line', (1.8,), 'T2', KB_SINGLE, 'N')],
    # kcut: the dash line + three lines crossing the lock at KCUT_YAW (one group = one hit)
    'kcut': [('kcut', 'cut', 'dash_line', (3.0,), 'T4', KB_FINAL, 'N'), ('kcut', 'cut', 'line', (12.0, 1.6), 'T4', KB_FINAL, 'N'),
             ('kcut', 'cut', 'line', (12.0, 1.6), 'T4', KB_FINAL, 'N'), ('kcut', 'cut', 'line', (12.0, 1.6), 'T4', KB_FINAL, 'N')],
    'mx': [('mx', 'x', 'pdisc', (2.8,), 'T3', KB_CHAIN, 'N'), ('mx', 'dome', 'disc', (3.2,), 'T2', KB_FINAL, 'P')],
    'nb': [('nb', 'b1', 'line', (16.0, 3.0), 'T2', KB_CHAIN, 'P'), ('nb', 'b2', 'line', (16.0, 3.0), 'T2', KB_CHAIN, 'P'),
           ('nb', 'b3', 'line', (16.0, 3.0), 'T3', KB_FINAL, 'P')],
    # q (hr_design §8.2: the grab is unparriable): q_grab's grab, then q_air only when the grab landed (clock + Q_AIR_T0)
    'q': [('q_grab', 'grab', 'pdisc', (2.2,), 'T2', KB_CHAIN, 'N'), ('q_air', 'beam', 'line', (14.0, 2.6), 'T2', KB_CHAIN, 'P'),
          ('q_air', 'hit', 'pdisc', (2.6,), 'T3', KB_CHAIN, 'P'), ('q_air', 'pillar', 'pdisc', (2.4,), 'T3', KB_FINAL, 'N')],
}
HIT_PH = {'rings': {3: 1, 4: 2, 5: 2}}            # HITS row -> the only fight phase it is made in (1 P1 / 2 P2)
KCUT_YAW = (0, 55, -55)                           # kcut's three lines through the lock, degrees from the dash direction
NB_YAW = (-30, 30, 0)                             # nb's bands through each lock, degrees from her aim
# The flash of every N hit: HITS row -> ((colour, clip, event, offset), ...): the flash is called at ev(clip, event) + offset.
# Yellow >= YELLOW_MIN t before the hit; purple exactly PURPLE_LEAD t before its cut; blue: the sphere 15 t, then the lunge.
FLASH_AT = {
    'ult': {0: (('yellow', 'ult', 'yellow', 0), ('purple', 'ult', 'star1', 0)), 1: (('purple', 'ult', 'star2', 0),)},
    'a9': {0: (('yellow', 'a9', 'yellow', 0), ('purple', 'a9', 'star', -1)), 1: ()},      # one group: the row 0 flashes
    'a10': {0: (('yellow', 'a10', 'yellow', 0),)},
    'hcut': {0: (('yellow', 'hcut', 'yellow', 0),), 1: ()},
    'blue': {0: (('blue', 'blue', 'yellow', 0),)},      # flash_blue from the clip's yellow ring on (ring 4 t, sphere 4-19)
    'kcut': {0: (('yellow', 'kcut', 'yellow', 0),), 1: (), 2: (), 3: ()},
    'mx': {0: (('purple', 'mx', 'star', 0),)},
    'q': {0: (('purple', 'q_grab', 'star', 0),), 3: (('purple', 'q_air', 'star', 0),)},
}
Q_AIR_T0 = 21             # q: the grab strikes after the module tick of its event (20); the landed branch plays q_air from here
Q_MISS_END = 34           # q: missed / perfect-dodged / left the disc: she reforms, the pattern ends
CUT_R = 3.2               # damage radius of a counting / ghost cut (the visible ring ~2.2; knob 2.8-3.6, PLAN §4.8)
CUT_SHOW_R = 2.2
LOCK_LEAD = 7             # aims lock 7 t before the hit
TELL_MIN, TELL_BIG, COMBO_GAP = 12, 20, 10   # first visible motion -> hit >= 12 t; big / undodgeable / yellow >= 20 t;
#                                              chain hits >= 10 t apart (README 0-6 10-20)
MOVE_R = SAFE - 0.5       # 22.5: every end point (landing, dash end, blink, reappear) via mv/ok + leash inside it
assert MOVE_R == 22.5
FALLBACK_R = 21.0         # the guaranteed last reappear / landing point: on the player -> C line, <= 21 b from C
TRACK = {'deg': 10, 'step': 0.3, 'min': 2.4}   # chains: re-aim <= 10 deg/t + a 0.3 b step before each hit (stop at 2.4 b)
DASH_LEN = {'a9': 12.0, 'a6': 12.0, 'cs1_lunge': 20.0,   # max dash / glide lengths (b): A9 iai dash, A6 back-blink
            'hcut': 16.0, 'blue': 9.0, 'kcut': 10.0, 'tri': 6.0, 'q': 14.0}   # hr_design §2.2
DASH_BEYOND = {'a9': 3.0, 'hcut': 3.0, 'blue': 2.0, 'kcut': 3.0}   # the dash ends this far beyond the locked spot
# round V (v_brief §3 VB 4: she stays in the F5 frame): 6 / 5 / 5 / 5 / 6 b took her out of the top of the screen (review v C4)
LEAP_H = {'a4': 3.4, 'a10': 3.4, 'nb': 3.4, 'q': 3.4, 'q2': 3.6}   # leap heights (b): A4 6 b in 4 t, A10 5 b; nb / q hr_design §2.2
NB_TRAVEL, TRI_GLIDE, MX_RETREAT = 6.0, (6.0, 0.3, 12), (6.0, 9.0, 12)   # nb travels <= 6 b; tri glides in 0.3 b/t beyond 6 b
#                                                          (ticks 0-12); mx: player nearer than 6 b -> a 12-t leap back to ~9 b
MX_REPEAT = {'hp_pct': 30, 'chance': 60}                  # mx may repeat once at once at <= 30 % HP (the video's second X)
RINGS_END = {1: 54, 2: 64}                                # rings ends 10 t after its last ring (P1 r4 44, P2 r5 54)
ULT_AFTER = 6                                             # rings -> ult at a full gauge: ult starts this long after the last ring
AIR_MAX = 44                                              # hr_design §8.5: no pattern holds her out of reach longer (nb 44 t)
A4_TRAVEL, A10_DRIFT = 10.0, 0.4                          # A4 travels <= 10 b toward the player; A10 drifts <= 0.4 b/t
A9_BEYOND = 3.0                                           # A9 dashes through the locked point to 3 b beyond (<= 12 b)
A3_GLIDE = (8.0, 0.3, 14)                                 # A3 from 4.5-8 b: glides in 0.3 b/t during ticks 0-14
# hrfair 2.0, first pass (H1, 11-11; hr_design §6.4's recovery knob + 4): P1 8-16 -> 12-20, P2 10-16 -> 14-20 (the new kit has
# ~20 patterns / min and 1.8 groggies / min for an average parrier with the old values: T10's band is 0.8-1.3).
RECOVER = {1: (12, 20), 2: (14, 20)}                      # idle between patterns (min, max) per fight phase P1 / P2
# F1 (HR-13 / HR-14 / HR-18, the P1 pressure package, lead decision 11-05; PLAN §4.1 wins over §4.3's clip tails): every
# P1-kit pattern ends 8-12 t after its last hit instead of at its clip's end (the clip's follow-through plays on while she
# turns to the player; the AI recovery's walk / strafe takes over: the punish window); RECOVER above = the §4.8 knob
# (P1 16-24 -> 12-20, P2 12-18 -> 10-16); S5 (11-06, the measured balance pass): P1 12-20 -> 8-16 (the knob's -4 t; T1).
# A6 (no hit) keeps A6_TRIGGER['next'].
PAT_END = {'a1': 24, 'a2': 22, 'a3': 79, 'a3s': 40, 'd4': 64, 'tri': 70, 'a4': 46, 'a9': 40, 'a10': 32, 'hcut': 38, 'blue': 32,
           'kcut': 34, 'mx': 40, 'nb': 52, 'ult': 58}     # hr_design §2.2 (rings: RINGS_END; q: Q_MISS_END / Q_AIR_T0 + 90)
# F1 round 1 (HR-14, the decision's "during any tail kept ... she walks / strafes facing and tracking the player"): a kept tail
# lets the clip's follow-through play TAIL_MOVE t after the last hit / release (A4: until it lands; R1 / R3: until the solid
# row), then she moves as in the recovery (ai/tail: the recovery's move and clip, ai/tail_step each later tick) while she
# turns to the player; the recovery after it keeps that move (ai/tail_keep).
TAIL_MOVE = 4
WALK_SPEED, GLIDE_SPEED = 0.12, 0.18                      # recovery walk / strafe (P1) and the P2 glide, b/t

# ---------------------------------------------------------------------------------------------
# 2b. HR rebuild (hr_design §1.2-1.5, §2.1; lane H1): the 5-segment gauge, balance, the parry cue, the unparriable flashes
# hrfair 2.0, first pass (H1, 11-11): hit 5 -> 2. With the design's start value a player who is hit by everything filled it
# every ~16 s (U 3.2 / min, T11's band 0.8-1.5); 2 keeps "full after ~60 s of clean play, ~35 s when hit every 6 s".
# HB (11-11): hit 2 -> 1: the walker still had 2.06 ultimates / min (T11 0.8-1.5); 1 gives 1.33-1.5, the mixed agent's 0.67 stays.
GAUGE = {'max': 50, 'seg': 10, 'pat': 3, 'hit': 1}   # #gau hr in tenths of a segment: +pat at a pattern's end (not A6 / U),
#                                                      +hit per hit of hers that lands (tier 1-2 parries land; PP / PD do not),
#                                                      -seg per perfect-parried gauntlet cut; U is armed at max
GAUGE_FP = '#gau'                                    # objective OBJ; the under bar #buSub = #gau / seg, #buSubMax 5, BU_SHIELD
BAL = {'after_repel': 3, 'floor_min': 3, 'grog_in': 12, 'kip': 20}   # balance pips back after repel {at:60}; bal after a floor
#                                                      step that met a break; the grog_in clip; the kip-up's ticks left
PP_FLINCH = 6             # a perfect parry on a pattern's last / single hit: clip flinch, the pattern ends this many t later
CUE_LEAD = 7              # the parry cue: exactly this many t before every parryable hit (= LOCK_LEAD, the aim-lock tick)
CUE_KIT = ('glint', {'c': 2})          # the white-gold cue sparkle (HA-07; a pink glint inside) at rig anchor blade_mid
CUE_SND = 'parry_cue'                  # KIT_SOUND_RECIPES: block.note_block.iron_xylophone 0.7 pitch 1.8 (HA-06)
# the module's own unparriable flashes on her chest (anchor chest; #mbNpOwn mb 1 for the whole fight): (kit preset, args)
FLASH = {'yellow': ('yellow_tell', {'t': 6}), 'purple': ('star4', {}), 'blue': ('flash_blue', {'t': 15})}
FLASH_SND = {'yellow': 'yellow_chime', 'purple': 'a9_star', 'blue': 'flash_blue'}
PURPLE_LEAD = 12          # the purple star: exactly this many t before its cut
YELLOW_MIN = 12           # the yellow flash: at least this many t before its hit
NP_OWN = ('#mbNpOwn', 'mb')            # set 1 at spawn, cleared by cleanup: the framework's np_glint stays off
BAL_OFF = ('#mbBalOff', 'mb')          # FN-bal: 1 = bal/boss/may refuses balance damage (the lead-ins and the gauntlets)
assert CUE_LEAD == LOCK_LEAD

# =============================================================================================
# 3. Phases, floors, pips, the gauntlet scripts, switches (PLAN §3, §4.4-4.6, §5)
PH = {'intro': 0, 'p1': 1, 'cs1': 2, 'lead60': 3, 'a8': 4, 'cs2': 5, 'down': 6, 'p2': 7, 'lead': 8, 'a13': 9, 'cs3': 10,
      'death': 11}        # #ph hr; 3 = lead60 (was sq1); 6 = the removed down window (reserved; gone with H1's build)
FLOOR_P1 = 600            # per mille of mhpM: the hit reaching it stops there; CS1 at the next decision
FLOOR_ULT = 50            # per mille: the 5 % floor (set at CS1 0); A13 at the next decision (40 t later from the down)
PIPS = 5
PIP_RULE = 'perfect_parry'   # hr_design §1.2: a gauntlet cut whose hit on the player is judged tier 3 (#parT tmp 3, with
# #mbDodgeOk mb 1 from mboss/hurt_dodge) takes one segment (GAUGE['seg']); a perfect dodge, tier 2 / 1, walking out: nothing.
BU_SHIELD = 1             # the under-bar colour (#buSubCol): electro for the 5-segment gauge

# Gauntlet scripts (hr_design §2.4 as tuples). Rows (t, step, clip, cut): t = the clip's start on the pattern clock T+ (T0 =
# the gauntlet's start), or the step's tick when clip is None; cut = (made, lock, strike, tier, kb) of the cut hazard made
# at that step (api.cut), else None. A move's contact = t + ev(clip, 'hit') = the strike of the cut made one step earlier.
_TC = ('TC', KB_CUT)      # F1 (HR-19): the counting cuts of the gauntlets (DMG['TC'])
# HA-03 (review H-A, lead ruling): the strikes are re-timed so that no blind F metronome clears a gauntlet: for every period
# 8-30 t and every start (fresh F state, any tick from 120 t before T0 on) the shipped F rules (player/f_key, press,
# press_re, par_use, the judge) give at most 3 perfect parries in G1 (5 are needed; tests/test_metro.py drives the real
# functions). The old G1 strikes 30 46 64 94 110 138 164 180 196 gave 5 to a 14 / 15 / 16-t beat. Moved: c2 46 -> 48 (A8.2
# 2 t later), c4 94 -> 91 (D2 77, A8.4 88: the glide and the sweep 3 t earlier), c5 110 -> 109 (A8.5 103), c6 138 -> 139
# (D1 125, A8.1 136), c7 164 -> 163 (D3 147, A8.6 160); every gap >= 14, the clips, the judge and the bolts as they were.
# Round W (lane WB; the user's ruling 11-12: the whiff ladder is gone - every accepted F locks 12 t, a parry of any tier 1 t, an
# ignored press blocks F 3 t - and the gauntlets are re-timed instead): the strikes are chosen so that no blind F metronome of any
# period 1-40 t, from any start (fresh F state, any tick from 200 t before T0 on), gets more than 4 perfect parries (5 clear a
# gauntlet) under the shipped rules (tests/test_metro.py drives the real functions; the search tools.dev/sim/hr/review/metro,
# `dfs.c -DNOLADDER`: the nearest strike set to round V's among all such sets that keep the moves' own spacing). The rows are
# written from the strikes (_g1_rows / _g2_rows: every move at its old offset from the strike it delivers), the judge fixed.
G1_STRIKES = (31, 45, 64, 88, 108, 138, 163, 181, 195)
G2_STRIKES = (28, 46, 66, 89, 112, 127, 151, 170, 189, 205, 219)
G1_JUDGE, G2_JUDGE = 220, 242


def _g1_rows(s, j):
    """G1 (60 %): 9 parry cuts. A cut row (made, lock, strike) sits on the step one before the move whose contact delivers it."""
    s1, s2, s3, s4, s5, s6, s7, s8, s9 = s
    c = lambda m, x: (m, x - 7, x) + _TC      # noqa: E731
    return ((0, 'A8.T', 'g_tell', None),
            (s1 - 14, 'D1', 'g_dash', c(s1 - 14, s1)),        # c1
            (s1 - 3, 'A8.1', 'g_ring', c(s1, s2)),            # c2
            (s2 - 9, 'A8.2', 'g_rise', c(s2, s3)),            # c3
            (s3 - 9, 'A8.3', 'g_leap', None),                 # gone s3 + 7
            (s4 - 14, 'D2', 'g_glide', c(s4 - 14, s4)),       # c4 (>= the leap's gone + 2)
            (s4 - 3, 'A8.4', 'g_sweep', c(s4, s5)),           # c5
            (s5 - 6, 'A8.5', 'g_x', None),                    # gone s5 + 8
            (s6 - 14, 'D1', 'g_dash', c(s6 - 14, s6)),        # c6 (>= the X's gone + 2)
            (s6 - 3, 'A8.1', 'g_ring', None),
            (s7 - 16, 'D3', 'g_drop', c(s7 - 16, s7)),        # c7 (>= 8 t after the ring's contact)
            (s7 - 3, 'A8.6', 'g_wrap', c(s7, s8)),            # c8
            (s8 - 3, 'A8.7', 'g_dome', c(s8, s9)),            # c9
            (s9 - 5, 'A8.8', 'g_vert', None),                 # pink glow, rises (the dive's reappearance cuts the rise short)
            # round V (v_brief §3 VB 4: nothing hits from an empty screen): the dive reappears 18 t before the judge, in the F5
            # view, and holds its wind-up 15 t (clip g_dive: appear 0, dive 15, hit 18)
            (j - 18, 'A8.9', 'g_dive', None),
            (j, 'judge', None, None))                         # gauge 0: seq/repel {at:60} in this tick; fail §2.4: g_reform,
    #                                                           the P2 decision at FAIL60_P2_T


def _g2_rows(s, j):
    """G2 (5 %): 11 parry cuts, no discs, no yellow."""
    s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11 = s
    c = lambda m, x: (m, x - 7, x) + _TC      # noqa: E731
    return ((0, 'A8.T', 'g_tell', None),
            (s1 - 14, 'D1', 'g_dash', c(s1 - 14, s1)),        # c1
            (s1 - 3, 'A8.1', 'g_ring', c(s1, s2)),            # c2
            (s2 - 9, 'A8.2', 'g_rise', c(s2, s3)),            # c3
            (s3 - 9, 'A8.3', 'g_leap', None),                 # gone s3 + 7
            (s4 - 14, 'D1', 'g_dash', c(s4 - 14, s4)),        # c4 (>= the leap's gone + 2)
            (s4 - 3, 'A8.1', 'g_ring', None),                 # vanishes (EXTRA_VANISH)
            (s5 - 14, 'D2', 'g_glide', c(s5 - 14, s5)),       # c5 (>= the vanish + 2)
            (s5 - 3, 'A8.4', 'g_sweep', c(s5, s6)),           # c6
            (s6 - 6, 'A8.5', 'g_x', None),                    # gone s6 + 8
            (s7 - 14, 'D4', 'g_run', c(s7 - 14, s7)),         # c7 (>= the X's gone + 2)
            (s7 - 3, 'A8.6', 'g_wrap', c(s7, s8)),            # c8
            (s8 - 3, 'A8.7', 'g_dome', c(s8, s9)),            # c9
            (s9 - 3, 'A8.7', 'g_dome', c(s9, s10)),           # c10
            (s10 - 3, 'A8.7', 'g_dome', c(s10, s11)),         # c11
            (s11 - 5, 'A8.8', 'g_vert', None),                # rises (cut short by the dive's reappearance)
            (j - 18, 'A8.9', 'g_dive', None),                 # reappears 18 t before the judge, dives 3 t before it
            (j, 'judge', None, None))                         # gauge 0: seq/repel {at:5}; fail: the instant death


A8_SCRIPT = _g1_rows(G1_STRIKES, G1_JUDGE)
A13_SCRIPT = _g2_rows(G2_STRIKES, G2_JUDGE)
SCRIPTS = {'a8': A8_SCRIPT, 'a13': A13_SCRIPT}
GAUNTLETS = ('a8', 'a13')
CUT_IDS = {'a8': tuple(str(i) for i in range(1, 10)), 'a13': tuple(str(i) for i in range(1, 12))}
CUT_GAP_MIN = 14          # every strike gap: a missed F (12 t refusal) never blocks the next cut
EXTRA_VANISH = {'a13': (min(G2_STRIKES[3] - 3 + 12, G2_STRIKES[4] - 14 - 2),)}   # g_ring does not end vanished: the vanish
#                                                   before D2's reappearance (its clip's end, at the latest 2 t before D2)
# HA-03: G1's 102 -> 99 and G2's 205 -> 198 (the re-timed cuts would put them on a lock / one tick before a strike)
BOLTS = {'a8': (34, 96, 166, 218), 'a13': (70, 160, 195, 240)}    # deco_bolt 3-6 b from the player (no hit), T+
JUDGE_T = {'a8': 220, 'a13': 242}
REPEL_T = JUDGE_T                                 # the repel starts in the judge tick (its first frames are the gold deflect)
# the 11-06 moon disc: only the kit's prop size reads it now (build_mboss_hr_fx.py DISC_SCALE); the module launches none
DISC = {'hr': 1.4, 'y0': 0.2, 'y1': 2.4, 'speed': 1.75, 'life': 16, 'shape': 1, 'spin': 30, 'tier': 'T2', 'kb': 0,
        'kb_last_r2': 2}
DARK_SLICES = (-17, -14, -11, -8)                 # the `dark` job's four real slices land 3 t apart (PLAN §6.6)
# Reappear geometry (S4's g/**), relative to the player's facing (+ = right), blocks / degrees (PLAN §4.5)
# F1 (HR-27, lead decision 11-05): D2 / D4 at +-55 deg (was +-80): inside the default F5 view near its edge, as the footage
# shows them (camera 3.5 b behind the player, FOV 70: half-width 51.2 deg at 16:9, 48.2 at 16:10; D2 8 b at 39.0 deg off
# the camera axis, D4 12 b at 43.4 deg), so the approach is seen from the reappearance on.
REAPPEAR = {
    # round V (v_brief §3 VB 4: arrivals in front of the avatar): the station of the chain cuts 2.2 b at +35 (the player's front
    # right; was 1.5 b at +90, beside them: her blade swung through the lens)
    'D1': {'dist': 14.0, 'bearing': -40, 'fallback': (40, 0, 90, -90), 'fallback_dist': 10.0, 'end': (2.2, 35)},
    'D2': {'dist': 8.0, 'bearing': 55, 'end': (1.6, 45)},
    'D3': {'dist': 2.5, 'up': 3.0, 'bearing': 60},
    'D4': {'dist': 12.0, 'bearing': -55},
    'A8.9': {'up': 3.0},                             # round V: 3 b over a spot 4.5 b before the player (was 6 b over them: out of view;
    #                                                  at 4 b her head left the top of the frame of a lens aimed 7 b ahead)
}
P2_RECOVER, GROGGY_RECOVER = 20, 12   # P2's first decision after the repel {at:60}; the recovery after the balance groggy
# The counter cinematic's scripted HP steps (true damage, per mille of mhpM via mboss/true_hit, at repel events
# COUNTER_EV): repel {at:60} three steps (-4.5 %), repel {at:5} two steps then the lethal true hit (true_pct 100) at
# 'kick'. PLAN §3.4 / §4.6 / §4.8 give 15, 15 at 5 % (-3 %, the footage 5.2 -> 2.3 %); §9.0's "(10, 10, 'kill')" is
# superseded (contract change log).
COUNTER_PM = {60: (15, 15, 15), 5: (15, 15, 'kill')}
COUNTER_EV = ('strike', 'land', 'kick')           # repel 49 / 101 / 129 (hr_design §3.4)
FAIL60_PM = 500           # A8 fail (ULT60_LETHAL false): pl_dot 500 per mille, #mbDotLethal 0 (cannot kill) + a push
FAIL60_PUSH = (2.5, 3)    # mboss_lib.push_ring(2.5, 3) at the impact point, the same tick
FAIL60_REFORM_T, FAIL60_P2_T = 220, 240           # g_reform 220-230 (she lands 2 b from the player), P2 decision at 240
FAIL5_T = {'reappear': 224, 'black': 239, 'slash': 242}   # the instant-death staging (ovl black 239-242, pinkwhite +
#                                                           scarlet_line + ult/fatal at 242)
REVIVE = {'dist': 8.0, 'wait': 60}                # after a Ronova revive: she stands 8 b away; 60 t later lead_re {g:a13}
# Switches (PLAN §0.1 questions 5-7; each one value here, the default the build proceeds with)
ULT60_LETHAL = False      # A8 fail = the 500 per-mille hit (True: the instant death + the banner)
ULT5_LETHAL = True        # A13 fail = the instant death (ult/fatal; Ronova's revive applies) + the banner
DARK_LIGHT = True         # the `dark` look dims the walk light layer (False: fallback B, dome / moon / lanterns only)
WARN_TEXT = '베기를 완벽하게 패링해 실드를 모두 깎으세요 — 실드가 남으면 즉사합니다'   # hr_design §2.4 (the perfect-parry rule)
WARN_HL = ('즉사', '#FF3A55')   # bossbar rlk:hr_warn: white text, this word crimson; only while a lethal gauntlet runs
END_PROFILE = 'std'       # CS4 profile (question 7); only std is built: short (~600 t) / full (~1500 t) = a request
END_H = {'std': 1372}     # the ending's length H (= clip `ending`, hr_design §3.5); registry death = H + EVENT['len'] + 2
INTRO_SKIP = True         # hold the jump key (round V: Space; Shift ends a spectate) SKIP_HOLD t at any tick in SKIP_WINDOW -> black -> jump to SKIP_T (intro_end)
SKIP_HOLD, SKIP_T, SKIP_WINDOW = 20, 1290, (20, 1270)
# hr_design §3.0 / §3.2: CS0 and CS1 may be skipped (the jump key held SKIP_HOLD t inside the window -> ovl black, the jump to `to`)
SKIP = {'intro': {'window': (20, 1270), 'to': 1290}, 'cs1': {'window': (40, 560), 'to': 566}}
assert SKIP['intro'] == {'window': SKIP_WINDOW, 'to': SKIP_T}
SKIP_TEXT = '⊙ 건너뛰기'      # the original's prompt, verbatim (actionbar, hudHold)
SKIP_HINT = ' · Space 길게'      # the pack's control hint after it (round V: the skip is the jump key, never Shift)
SKIP_COLOR, SKIP_STEPS = '#A8A8B0', 4    # grey; brightens in four 5-t steps while held (fx/hud/skip {s:0..4}, s 5 clears)
P2_KIT = 'footage'        # question 5: the P1 kit with P2 recoveries + R1-R3 (all footage moves)
# triggers (PLAN §4.3 A6, §4.7)
# F1 (HR-38, lead decision 11-05): A6's P2 cooldown 340 -> 400 = PLAN §4.8's hard cap (at most one back-blink per 20 s);
# §4.4's P2 x 0.85 does not apply to this trigger.
A6_TRIGGER = {'chance': 60, 'near': 4.5, 'windup_t': 6, 'phase_grace': 200, 'cd': {1: 400, 2: 400},
              'glide': 12.0, 'glide_t': 3, 'side': (8.0, 10.0), 'inv': (0, 4), 'next': 16, 'line': 12, 'line_t': 12}
COUNTER_TRIGGER = {'hits': 4, 'window': 40, 'chance': 70, 'front_deg': 45, 'flinch_every': 4}   # A1 beside / behind,
#                                                                       A2 in front; only in recovery or idle

# =============================================================================================
# 4. AI (PLAN §4.7; S3 tunes values at review, the keys are frozen)
BANDS = (4.5, 11.0)                              # near <= 4.5 < mid <= 11 < far
MID_MAX = {'a3': 8.0, 'a3s': 8.0, 'a9': 7.0, 'tri': 10.0, 'blue': 7.0, 'kcut': 8.0}   # their mid weight only up to this distance
MID_MIN = {'hcut': 8.0}                          # its mid weight only from this distance
# WEIGHTS[key][fight phase 1 = P1 / 2 = P2] = (near, mid, far); renormalised over the entries off cooldown and allowed.
# hr_design §2.2 *start* values (hrfair 2.0 tunes them, §6.4); a1 / a2 are trigger-only in P2; ult is never weighted.
# HB (11-11, hrfair2 per seed; hb_progress.md), under the lead's rule (11-11, binding; the user: 「패링 불가 공격: 보스의 일부 큰
# 공격만」): in every band of both fight phases the unparriable entries (a9 a10 hcut blue kcut; mx and q count half: one of
# their two kinds of hit is flashed) take at most 35 % of the pick weight, the parried chains keep the majority (the
# design's start values had 40-72 %). Inside that: the parried weight leans on the short chain a3s (2 hits in 40 t) over a3
# (5) / d4 (4), and the free rings (4-5 parried hits) are gone: rings still come before every ult (the full gauge forces
# them). An average parrier (sigma 1.5) then breaks her ~1.33 times / min (the lead's relaxed T10 0.8-1.6; it was 1.67),
# the walker still takes 타키's intake (T1), the sigma-3 parrier <= 0.60 of it (T1b). Shares (near / mid / far / FAR_RULE):
# P1 35.0 / 34.8 / 34.2 / 35.0 %, P2 35.0 / 34.6 / 34.6 / 31.6 %. COOLDOWN (P1): the counter A1 / A2 100 -> 200 (its single
# parried hits) and the near band x ~1.4 (a3 / d4 140 -> 200, rings 160 -> 220, a9 160 -> 220, a10 120 -> 170, blue 180 ->
# 250, kcut 200 -> 280); a3s P1 80 -> 140, P2 70 -> 100 (it is picked most now: without it the walker's ultimates rose
# over T11's 1.5 / min).
WEIGHTS = {
    'a1': {1: (8, 0, 0)},
    'a2': {1: (8, 0, 0)},
    'a3': {1: (20, 10, 0), 2: (12, 10, 0)},
    'a3s': {1: (45, 15, 0), 2: (50, 15, 0)},
    'd4': {1: (12, 0, 0), 2: (8, 0, 0)},
    'tri': {1: (0, 30, 0), 2: (0, 20, 0)},
    'a4': {1: (0, 20, 50), 2: (0, 15, 20)},
    'rings': {1: (0, 0, 0), 2: (0, 0, 0)},
    'a9': {1: (14, 6, 0), 2: (11, 6, 0)},
    'a10': {1: (12, 12, 12), 2: (0, 9, 10)},
    'hcut': {1: (0, 8, 14), 2: (0, 7, 12)},
    'blue': {1: (11, 7, 0), 2: (11, 7, 0)},
    'kcut': {1: (13, 7, 0), 2: (11, 6, 0)},
    'mx': {2: (20, 15, 10)},
    'nb': {2: (0, 20, 35)},
    'q': {2: (0, 16, 20)},
}
COOLDOWN = {'a1': {1: 200, 2: 85}, 'a2': {1: 200, 2: 85}, 'a3': {1: 200, 2: 120}, 'a3s': {1: 140, 2: 100},
            'd4': {1: 200, 2: 120}, 'tri': {1: 140, 2: 120}, 'a4': {1: 160, 2: 140}, 'rings': {1: 220, 2: 140},
            'a6': {1: 400, 2: 400}, 'a9': {1: 220, 2: 140}, 'a10': {1: 170, 2: 100}, 'hcut': {1: 160, 2: 140},
            'blue': {1: 250, 2: 150}, 'kcut': {1: 280, 2: 170}, 'mx': {2: 150}, 'nb': {2: 180}, 'q': {2: 300}}
NP_SHARE = {'a9': 1, 'a10': 1, 'hcut': 1, 'blue': 1, 'kcut': 1, 'mx': 0.5, 'q': 0.5}   # the unparriable part of an entry
NP_SHARE_MAX = 0.35       # the lead (11-11): their share of the pick weight in any band / the far rule (see above)
TRIGGER_ONLY = ('a6', 'ult')                     # never picked by weight: the skill trigger; ult only after rings at a full
#                                                  gauge (A1 / A2: the counter trigger, the rear rule, small P1 near weights)
FAR_RULE = {'dist': 8.0, 'dwell': 30, 1: {'hcut': 20, 'a4': 65, 'a10': 15}, 2: {'nb': 50, 'q': 30, 'hcut': 15},   # HB: <= NP_SHARE_MAX
            'fallback': ('glide', 'a3s')}        # also the decision 16 t after A6
for _fp in (1, 2):                               # the lead's 35 % rule (NP_SHARE above), checked at every build
    for _w in [{k: w[_fp][b] for k, w in WEIGHTS.items() if _fp in w} for b in range(3)] + [FAR_RULE[_fp]]:
        assert sum(v * NP_SHARE.get(k, 0) for k, v in _w.items()) <= NP_SHARE_MAX * sum(_w.values()), (_fp, _w)
ULT_FORCE = {'key': 'rings', 'then': 'ult', 'bands': (0, 1)}   # #gau = max: the next near / mid decision is rings (its cooldown
#                                                                ignored), then ult; from far she closes first (the far rule)
REAR_RULE = {'deg': 60, 'dwell': (20, 30), 'key': 'a1', 'cd_ignore_every': 200}
NO_REPEAT = True                                 # no immediate repeat of an entry

# =============================================================================================
# 5. Keys, sequences, ownership, test ids, lines (PLAN §3.0, §9.0-9.2)
P1 = ('a1', 'a2', 'a3', 'a3s', 'a4', 'a6', 'a9', 'a10', 'd4', 'tri', 'rings', 'ult', 'hcut', 'blue', 'kcut')   # p1.py
P2 = ('mx', 'nb', 'q', 'a8', 'a13')                 # p_ghost.py -> p/<key>/** (P2's three entries + the gauntlets G1 / G2)
SEQS = ('intro', 'cs1', 'lead60', 'repel', 'lead5', 'lead_re', 'ending', 'event')   # H2: seq.py -> seq/<name>/**
SEQ_CONTRACT = 2          # seq.py declares `CONTRACT = 2` once it implements this table (else: the core stand-ins)
SEQ_CLIPS = {'intro': ('intro', 'intro_end'), 'cs1': ('cs1',), 'lead60': ('lead60',), 'repel': ('repel',),
             'lead5': ('lead5',), 'lead_re': ('lead_re',), 'ending': ('ending',),
             'event': ('ev_give', 'ev_toast', 'ev_leave')}
SEQ_ARGS = {'repel': {'at': (60, 5)}, 'lead_re': {'g': ('a8', 'a13')}}   # macro args of seq/<name>/start
SEQ_EXTRA = {'intro': ('skip',), 'cs1': ('skip',)}   # seq/<name>/skip: the core calls it after SKIP_HOLD t of sneak (SKIP)
# A sequence never calls core functions: it signals the core through the score SEQ_SIGNAL (objective OBJ, S2b's #sq_
# prefix) = a SIG value in the tick of the beat; the core reads it right after seq/<name>/tick, applies it (an HP step:
# COUNTER_PM[at][i - 1] via mboss/true_hit, 'kill' = true_pct 100; refill: shield/arm) and resets it to 0.
SEQ_SIGNAL = '#sq_sig'
SIG = {'hp1': 1, 'hp2': 2, 'hp3': 3, 'refill': 4}   # repel: hp1-hp3 at COUNTER_EV; lead60 (tick 0) / lead5 / lead_re: refill
SEQ_LEN = {'intro': 1440, 'cs1': 720, 'lead60': 56, 'repel': 140, 'lead5': 116, 'lead_re': 60, 'ending': 1372,
           'event': 120}
# hr_design §3.0-3.5 (lane H2): the stage, CS0's fixed stage, the contacts (stage frame ST(r, u, f), blocks), the actor
STAGE_FMAX = {'cs1': 10, 'repel': 10, 'ending': 12}    # the stage's forward must pass mv/ok this far, else it faces C
CS0_P0 = (881.28, 201.0, 25.55)                         # CS0 stage origin: start + CS0_WALK_BACK b toward SEAT_POS
CS0_BEARING, CS0_WALK_BACK, CS0_END_DIST = 7.5, 6.0, 6.5
CONTACT = {                                             # id: (sequence, (tick from, tick to), ST(r, u, f), what meets)
    'K1': ('cs1', (10, 30), (0, 1.45, 0.95), 'blade lock (X); she stands at f 2.25 (round W: a swordfighter\'s distance)'),
    'KR': ('repel', (0, 26), (0, 1.55, 0.65), 'her blade pressing down on the actor\'s high guard'),
    'KW': ('repel', (36, 48), (0.15, 1.95, 0.85), 'the actor\'s left hand on her sword wrist (her anchor hand_l)'),
    'KH': ('repel', (49, 49), (0, 2.20, 1.10), 'the actor\'s hilt on her hat crown (her anchor hat_crown)'),
    'KS': ('repel', (70, 78), (0.20, 1.50, 1.60), 'her sword forearm over the actor\'s right shoulder'),
    'KT1': ('repel', (88, 88), (0, 2.95, 1.9), 'her pelvis over the top'),
    'KT2': ('repel', (101, 101), (0, 0.25, 3.0), 'her pelvis on the ground (head toward +f)'),
    'KK': ('repel', (129, 129), (0, 0.35, 2.7), 'the actor\'s right foot on her flank'),
    'KG': ('ending', (52, 52), (0, 2.05, 2.95), 'the actor\'s blade tip on the near edge of her brim'),
    'KE2': ('ending', (56, 80), (0, 1.5, 2.2), 'blade lock (X)'),
    'KE5': ('ending', (190, 204), (0, 1.5, 3.45), 'blade lock (X)'),
    # (round W, lane WC: w_brief §4.6, the aerial duel is gone) the exchange on the ground, her root at f 4.75, the actor's at 2.5
    'KA1': ('ending', (228, 228), (0, 1.45, 3.5), 'her diagonal cut on the actor\'s block'),
    'KA2': ('ending', (262, 262), (0, 1.85, 3.05), 'her overhead cut on the actor\'s horizontal guard (she has stepped in to f 4.35)'),
    'KA3': ('ending', (286, 286), (0, 1.25, 3.55), 'cut on cut (the big flash)'),
    'KA4': ('ending', (298, 304), (0, 1.5, 3.45), 'blade lock (X), then both push off'),
}
CONTACT['KT1'] = ('repel', (88, 88), (0.28, 1.4, 2.0), 'her pelvis over the actor\'s right shoulder')   # HF-B (HB-01): the low throw
CONTACT_TOL = {'blade': 0.08, 'body': 0.12}             # b: blades; hands and feet
ACTOR_CLIPS = {'cs0': 1440, 'cs1': 720, 'repel': 140, 'ending': 1372, 'coda': 120}   # H3: tools/player_motion/cine/<id>.json
ACTOR_LIMIT = {'fwd': 2.5, 'back': 1.5, 'side': 1.5, 'cs0_back': 6.0, 'air': 7.0}   # the actor's displacement from the stage origin
ACTOR_MANIFEST = _TOOLS / 'player_motion/cine/manifest.json'                      # H3 writes it
ACTOR_CALLS = {'spawn': [], 'play': ['clip'], 'tick': [], 'face': ['yaw'], 'stop': []}   # function rlk:char/cine/<call>
ACTOR_CLOCK = ('#cavT', 'cine')                         # the clip tick to show: the module writes #sq hr into it every tick
CAM_REQ, CAM_ID = ('#mbCam', 'mb'), ('#mbCamId', 'mb')  # FN-cam (H2): the lock request (1 every tick) and the live camera 1 / 2
PATTERN_NAMES = {'a1': '회전 반월참', 'a2': '역습 일섬', 'a3': '오연 반월', 'a3s': '쌍월참', 'a4': '월하 낙참 · 공중 원륜',
                 'a6': '후방 섬보', 'a9': '황광 원참', 'a10': '황광 낙참', 'd4': '원월 사연', 'tri': '돌진 삼월참',
                 'rings': '회전 월륜', 'ult': '공간 참', 'hcut': '황광 섬월', 'blue': '청광 돌파', 'kcut': '황광 난참',
                 'mx': '자광 십자참', 'nb': '낙월 사선', 'q': '자영 포박 · 천공 낙월', 'a8': '자영 연참',
                 'a13': '필살 · 자영 연참'}    # test/help only: no pattern name is ever shown in the fight
# boss/test/pattern {id:N} (hr_design §5.1); test/help lists TEST_HELP_NAMES; test/lock {id} for LOCK_IDS. A pattern key
# sits at its #pat id (12 = ult: the test fills the gauge and starts rings, ult follows).
TEST_IDS = {1: 'a1', 2: 'a2', 3: 'a3', 4: 'a4', 5: 'a6', 6: 'a9', 7: 'a10', 8: 'a3s', 9: 'd4', 10: 'tri', 11: 'rings',
            12: 'ult', 13: 'hcut', 14: 'blue', 15: 'kcut', 16: 'mx', 17: 'nb', 18: 'q', 19: 'groggy now',
            20: 'cs1 -> lead60 -> a8', 21: 'a8 now (5/5)', 22: 'a8 with the gauge at 0 (repel -> p2)', 23: 'a8 fail',
            24: 'repel {at:60} only', 26: 'lead5 + a13', 27: 'a13 now',
            28: 'a13 with the gauge at 0 (repel -> kill -> ending -> coda)', 29: 'a13 fail (instant death; test/defeat)',
            30: 'intro replay', 32: 'look crimson', 33: 'p2 now (skip cs1 / a8)', 34: 'HP = 5 % floor + 1',
            35: 'intro skip at tick 100', 36: 'cs1 skip at tick 100', 37: 'gauge = 50', 38: 'balance = 1',
            80: 'HP = next floor + 1', 90: 'next event random', 91: 'next event = item', 92: 'next event = buff', 99: 'hold'}
TEST_HELP_NAMES = {1: '회전 반월참', 2: '역습 일섬', 3: '오연 반월', 4: '월하 낙참 + 공중 원륜', 5: '후방 섬보',
                   6: '황광 원참', 7: '황광 낙참', 8: '쌍월참', 9: '원월 사연', 10: '돌진 삼월참', 11: '회전 월륜',
                   12: '회전 월륜 → 공간 참 (게이지 가득)', 13: '황광 섬월', 14: '청광 돌파', 15: '황광 난참',
                   16: '자광 십자참', 17: '낙월 사선', 18: '자영 포박 · 천공 낙월', 19: '그로기',
                   20: '60% 컷신 → 자영 연참', 21: '자영 연참 (실드 5칸)', 22: '자영 연참 (실드 0칸 → 반격)',
                   23: '자영 연참 실패', 24: '반격 장면', 26: '5% 이어짐 + 필살 · 자영 연참',
                   27: '필살 · 자영 연참', 28: '필살 (실드 0칸 → 엔딩)', 29: '필살 실패 (즉사)', 30: '등장 다시',
                   32: '붉은 들판', 33: '2페이즈로', 34: '체력 = 5% + 1', 35: '등장 건너뛰기 (100틱)',
                   36: '60% 컷신 건너뛰기 (100틱)', 37: '게이지 가득', 38: '균형치 1칸',
                   80: '체력 = 다음 바닥 + 1', 90: '다음 이벤트 무작위',
                   91: '다음 이벤트 = 화무십일홍', 92: '다음 이벤트 = 월하대작', 99: '멈춤'}
LOCK_IDS = tuple(i for i in sorted(TEST_IDS) if 1 <= i <= 18)
# Lines (PLAN §3.0, verbatim from the user's wiki pages w1 / w2 and the footage subtitles; speaker 홍련): kit
# fx/hud/line {id} types two syllables per 2-t step with block.note_block.hat 0.3, holds, clears; a new line replaces a
# running one; while an overlay is up the line keeps the overlay glyph on the title.
LINES = {1: '꽃 속에 술 한 병 놓고,',
         2: '벗 없이 혼자 술잔 드네.',
         3: '잔 들어 밝은 달 맞이하니,',
         4: '달과 나와 그림자 셋이 되었네...',
         5: '그리고 이제 친구가 와 주었으니 월하독작이 아니라, 대작이 되겠구만.',
         6: '낭자, 내 말하지 않았던가?',
         7: '곧 또 보게 될 것 같다고.',
         8: '아름다운 곳이지 않나?',
         9: '신세진 것도 있겠다, 이 달 아래서...',
         10: '한 수 가르침을 청하고 싶네만.',
         11: '낭자 생각은 어떤가?',
         12: '거기가 아닐세.',
         13: '낭자, 대단하구만.',
         14: '진심으로 가겠네.',
         15: '천지만물을 벤다는 건...',
         16: '이런 것일세.',
         17: '낭자, 여기까지 하세.',
         18: '대단하네, 좋은 수련이 되었어.',
         19: '이제 정말 가야겠네.',
         20: '다음 번에 만나면, 그땐 같이 한잔 하면 좋을 텐데...',
         21: '달빛과 바람을 안주 삼아... 말일세.',
         22: '어디 보자, 낭자네에선 이렇게 인사한다고 들었는데...',
         23: '당신의 기억이 이어지기를.',
         24: '조심하게. 칼자루를 쥐었다고 그 검의 주인이 되는 것은 아니니.',
         25: '한잔할 텐가? 안주는 달빛과 바람일세.'}
LINE_COLOR = '#F2D0E8'
# LINE_AT[id] = (where, tick, ticks on screen): where = a clip (its played tick; the sequence / pattern playing it calls
# the line at that tick) or 'event' (the §7 coda, E-tick); the clip event l<id> sits at the same tick.
LINE_AT = {1: ('intro', 258, 54), 2: ('intro', 340, 60), 3: ('intro', 462, 60), 4: ('intro', 540, 84),
           5: ('intro', 690, 130), 6: ('intro', 838, 64), 7: ('intro', 906, 44), 8: ('intro', 980, 44),
           9: ('intro', 1044, 90), 10: ('intro', 1140, 70), 11: ('intro_end', 4, 62), 12: ('a6', 12, 63),
           13: ('cs1', 110, 52), 14: ('cs1', 232, 40), 15: ('cs1', 578, 36), 16: ('cs1', 618, 36),
           17: ('ending', 420, 58), 18: ('ending', 486, 66), 19: ('ending', 628, 42), 20: ('ending', 716, 118),
           21: ('ending', 910, 128), 22: ('ending', 1082, 128), 23: ('ending', 1230, 88),
           24: ('event', 4, 48), 25: ('event', 4, 48)}    # hr_design §3 (24 item branch, 25 buff branch: EVENT['lines'])
# F2 (HR-16): a line wider than LINE_MAX_PX font px (the subtitle is drawn at 2x and never wraps: 192 px fits the Auto GUI
# width of 1920 x 1200, 384 GUI px, and every wider one) is shown as consecutive subtitles split at its natural pause, typed
# one after the other inside its LINE_AT hold (the hold split by the pages' widths); the pages joined with one space are the
# line verbatim (LINES stays whole). As the footage shows its long line as two subtitles (15 / 16).
LINE_MAX_PX = 192
LINE_PAGES = {5: ('그리고 이제 친구가 와 주었으니', '월하독작이 아니라, 대작이 되겠구만.'),
              22: ('어디 보자,', '낭자네에선 이렇게 인사한다고 들었는데...'),
              24: ('조심하게. 칼자루를 쥐었다고', '그 검의 주인이 되는 것은 아니니.')}
MUSIC_AT = {1: ('intro_end', 'music'), 2: ('cs1', 'music'), 3: ('ending', 'music')}   # api.music(ph) at these events

# =============================================================================================
# 6. Scores, tags, storage, resource ids (PLAN §9.0 namespaces). Module state = fake players in objective `hr` (S3's
# init / uninstall); each stage only adds fake players with its own prefix: core CORE_FP, a pattern `#<key>_<x>`, the
# ghost helpers `#g_<x>`, sequences `#sq_<x>`, the event EV_FP. Rig objectives hrRig* (S2a), kit objectives hrFx* (S1K),
# the buff objective hrMoon (SR, per player).
OBJ = 'hr'
CORE_FP = ('#ph', '#pat', '#pt', '#done', '#clk', '#rigc', '#rigt', '#sq', '#sqdone', '#hud', '#fl', '#tst', '#lock',
           '#last', '#last2', '#rear', '#far', '#dec', '#rec', '#hits', '#a6cd', '#gres', '#gk',
           '#skip', '#warn', '#inv', LOOK_REQ)
# I1 (request s3-5): S3's own fake players, folded in from s3lib.FP_EXTRA in the same order (s3lib.FP = CORE_FP; cleanup resets
# exactly these, the build refuses any other '#name hr' of S3's files): temporaries, the constants #c<n> (CORE_CONSTS), the
# floor / sequence / shield / kipup / revive / skip state, the AI's #ai_* and its per-pattern weights / cooldowns.
CORE_CONSTS = (2, 3, 5, 6, 10, 64, 100, 577, 1000, 36000)
CORE_FP += (('#t', '#t2', '#t3', '#t4', '#t5', '#cn1', '#cn1000') + tuple(f'#c{c}' for c in CORE_CONSTS)
            + ('#fl60', '#fl5', '#sqn', '#sqh', '#shb', '#grs', '#rvw', '#a6q', '#ctr', '#flq', '#h1', '#h2',
               '#h3', '#h4', '#pipoff', '#lk', '#skp', '#rp')
            # hr_design §1.2-1.5 (H1's build): #pp a perfect parry seen this tick, #ppf the PP flinch's ticks left, #ultq ult
            # follows the running rings, #hpp the player hits read this tick, #c30 / #c50 constants' helpers
            + ('#pp', '#ppf', '#ultq', '#hpp', '#grc')
            + ('#ai_d2', '#ai_mv', '#ai_pht', '#ai_sum', '#ai_r', '#ai_rc', '#ai_ff', '#ai_nx', '#ai_rcd', '#ai_fl', '#ai_lf',
               '#ai_ls', '#ai_nn', '#ai_bs',        # F1 (HR-13): an empty pick in a row, the backstep's mid pick pending
               '#ai_tmc',                           # F1 round 1 (HR-14): the module clock of a kept tail's last move tick
               GAUGE_FP)                            # hr_design §1.2: the 5-segment gauge (tenths of a segment)
            + tuple(f'#ai_w{k}' for k in P1 + P2) + tuple(f'#cd_{k}' for k in COOLDOWN))
RIG_OBJ_PREFIX, KIT_OBJ_PREFIX = 'hrRig', 'hrFx'
TAGS = {'part': 'rlk_hr_part', 'anchor': 'rlk_hr_anchor', 'fx': 'rlk_hr_fx', 'deco': 'rlk_hr_deco', 'pat': 'rlk_hr_p',
        'cut': 'rlk_hr_cut', 'ghost': 'rlk_hr_ghost', 'down': 'rlk_hr_down', 'stage': 'rlk_hr_stage', 'ev': 'rlk_hr_ev'}
# I1 (request s3-5): the rig's shadow and S3's own tags, folded in (the module cleanup / uninstall kill every value but
# 'ghost', which they remove from the body): the pip windows, the aim lock / dash probe / A9 spot markers, the P2-entry and
# near-spot probes, the decor props by name.
TAGS.update({'shadow': 'rlk_hr_shadow', 'pip': 'rlk_hr_pip', 'lock': 'rlk_hr_lock', 'probe': 'rlk_hr_dp', 'a9s': 'rlk_hr_a9s',
             'pl8': 'rlk_hr_pl8', 'near': 'rlk_hr_near', 'deco_moon_halo': 'rlk_hr_deco_moon_halo',
             'deco_lotus': 'rlk_hr_deco_lotus', 'deco_seat_rock': 'rlk_hr_deco_seat_rock'})
#     pattern markers carry rlk_hr_p + rlk_hr_p_<key>; every part rlk_hr_<part>; everything spawned rlk_room rlk_mb_aux
STORAGE = 'rlk:hr'
STORAGE_KEYS = {'core': 'S3', 'rig': 'S2a', 'seq': 'S2b', 'fx': 'S1K', 'g': 'S4', 'ev': 'S3'}   # rlk:hr <key>.* owner
RIG_UUID = '524c4b4d-4852-4400-8000-0000000000{:02x}'   # part NN 00..28 (= PARTS order), shadow 0x40
SHADOW_NN = 0x40
RP_RIG = 'rlk:mboss/scarlet/'           # S2a (rig models, the ghost model, item_sword)
RP_KIT = 'rlk:mboss/hr_kit/'            # S1K (kit sprites / models, the gate icon)
FONT = 'rlk:mboss_hr'                   # S1K; glyphs U+EC00-ECFF; ends with a minecraft:default reference
FONT_RANGE = (0xEC00, 0xECFF)
WARN_BOSSBAR = 'rlk:hr_warn'            # S1K fx/hud/warn {on}; removed by fx/uninstall
GATE_ICON_MODEL = 'rlk:mboss/hr_kit/gate_icon'   # the registry icon model from I1 (vanilla iron_sword until then)
GHOST_MODEL = 'rlk:mboss/scarlet/ghost'
ITEM_MODEL = 'rlk:mboss/scarlet/item_sword'      # §7: the thrown sword prop and the item icon (S2a's RP tree)
for _rid in (RP_RIG, RP_KIT, FONT, WARN_BOSSBAR, GATE_ICON_MODEL, GHOST_MODEL, ITEM_MODEL, STORAGE):
    assert _rid == _rid.lower(), _rid

# =============================================================================================
# 7. Rig contract (PLAN §2; S2a implements the 39 fight / gauntlet / §7 clips, S2b the 8 cinematic clips; S3 / S4 / S2b
# call). Item displays, billboard fixed, view range 2, culling 8 x 8, brightness 13 (sword_glow 15).
HEIGHT, HAT_TOP, BRIM_D = 2.00, 2.30, 1.32       # head top / hat crown / brim diameter (b), sole 0 (S2d: the player avatar's body)
SWORD_LEN, SCABBARD_LEN, SHADOW_R = 1.94, 1.52, 0.6
ITEM_SWORD_LEN, ITEM_SWORD_SCALE = 2.03, 1.375   # item_sword: length (b) at its display scale; seq.py reads both
PARTS = ('pelvis', 'torso', 'head', 'face', 'hair_tail_1', 'hair_tail_2', 'lock_r', 'lock_l', 'arm_r', 'forearm_r',
         'arm_l', 'forearm_l', 'thigh_r', 'shin_r', 'thigh_l', 'shin_l', 'skirt_fl', 'skirt_fr', 'skirt_bl', 'skirt_br',
         'sash_tails', 'hat', 'hat_strings', 'sword', 'sword_glow', 'scabbard', 'hilt_sheathed', 'cup', 'bottle')
assert len(PARTS) == 29
# default parent (PLAN §2.3); REPARENT: the parent a look state uses (None = the root, keyed by the clip)
PARENTS = {'pelvis': None, 'torso': 'pelvis', 'head': 'torso', 'face': 'head', 'hair_tail_1': 'head',
           'hair_tail_2': 'hair_tail_1', 'lock_r': 'head', 'lock_l': 'head', 'arm_r': 'torso', 'forearm_r': 'arm_r',
           'arm_l': 'torso', 'forearm_l': 'arm_l', 'thigh_r': 'pelvis', 'shin_r': 'thigh_r', 'thigh_l': 'pelvis',
           'shin_l': 'thigh_l', 'skirt_fl': 'pelvis', 'skirt_fr': 'pelvis', 'skirt_bl': 'pelvis', 'skirt_br': 'pelvis',
           'sash_tails': 'pelvis', 'hat': 'head', 'hat_strings': 'hat', 'sword': 'forearm_l', 'sword_glow': 'sword',
           'scabbard': 'pelvis', 'hilt_sheathed': 'scabbard', 'cup': 'forearm_r', 'bottle': 'forearm_l'}
REPARENT = {('hat', 'worn'): 'head', ('hat', 'back'): 'torso', ('hat', 'hand'): 'forearm_r', ('hat', 'world'): None,
            ('scabbard', 'hand'): 'forearm_r', ('scabbard', 'hip'): 'pelvis', ('cup', 'hand'): 'forearm_r',
            ('cup', 'rock'): None, ('bottle', 'hand'): 'forearm_l', ('bottle', 'rock'): None}
# look channels the module / sequences call (rig/look/<channel>/<value>); the module itself calls only form, phase,
# blade and state (clips key hat / sword / scabbard / face / hands / props at their own events)
LOOKS = {'form': ('normal', 'ghost'), 'phase': ('p1', 'p2'), 'hat': ('worn', 'back', 'hand', 'world', 'gone'),
         'sword': ('hand', 'sheathed', 'gone'), 'blade': ('off', 'lilac', 'pink', 'violet', 'gold', 'edge'),
         'scabbard': ('hand', 'hip', 'gone'), 'face': ('calm', 'smile', 'closed'), 'props': ('none',)}
HANDS = ('open', 'grip', 'brim')                 # forearm_r / forearm_l hand models (clip-keyed)
PROP_STATES = ('none', 'hand', 'rock')           # cup / bottle (keyed by the intro clip; props/none hides both)
ANCHORS = ('hand_l', 'hand_r', 'blade_tip', 'blade_mid', 'scabbard_mouth', 'hat_crown', 'head', 'chest')
# rig/<call> functions (all @s = the body = the anchor, at its feet)
RIG_CALLS = ['init', 'spawn', 'spawn_hidden', 'tick', 'kill', 'uninstall', 'flash', 'state/normal', 'state/hidden',
             'face/player', 'face/track'] + [f'look/{ch}/{v}' for ch, vs in LOOKS.items() for v in vs] \
    + [f'anchor/{a}' for a in ANCHORS]
RIG_MACRO_CALLS = {'face/set': ['yaw']}

# CLIPS_PLAN = PLAN §2.5 as written: (len, loop (from, to) or None, {event: tick}); 'end' = the clip length. An event
# name the table writes at two ticks gets numbered (a dict key is unique): walk / strafe_l / strafe_r 'step 0, 12|10' ->
# step1, step2; ending 'rise 28' stays 'rise', its 'rise 268' becomes 'rise2'.
CLIPS_PLAN = {
    'idle': (40, (0, 40), {}),
    'idle2': (40, (0, 40), {}),
    'walk': (24, (0, 24), {'step1': 0, 'step2': 12}),
    'glide': (16, (0, 16), {}),
    'strafe_l': (20, (0, 20), {'step1': 0, 'step2': 10}),
    'strafe_r': (20, (0, 20), {'step1': 0, 'step2': 10}),
    'backstep': (12, None, {'land': 10}),
    'flinch': (6, None, {}),
    'a1': (34, None, {'pivot': 0, 'glint': 6, 'lock': 7, 'fan': 10, 'hit': 14, 'end': 34}),
    'a2': (30, None, {'glint': 0, 'draw': 4, 'lock': 5, 'glow': 6, 'hit': 12, 'end': 30}),
    'a3': (96, None, {'glint': 0, 'lock1': 7, 'h1': 14, 'lock2': 23, 'h2': 30, 'lock3': 38, 'h3': 45, 'lock4': 50,
                      'h4': 57, 'lock5': 62, 'h5': 69, 'end': 96}),
    'a4': (60, None, {'crouch': 0, 'leap': 2, 'apex': 6, 'glint': 7, 'lock': 12, 'flip': 13, 'dive': 16, 'hit': 20,
                      'crouch2': 22, 'slash': 25, 'lock2': 27, 'ring': 28, 'hit2': 34, 'land': 38, 'end': 60}),
    'a6': (20, None, {'bubble': 0, 'gone': 2, 'appear': 4, 'settle': 10, 'end': 20}),
    'a9': (64, None, {'turn': 0, 'spin': 3, 'ring': 4, 'yellow': 8, 'star': 17, 'lock': 22, 'flash': 24, 'go': 26,
                      'cut': 28, 'end': 64}),
    'a10': (56, None, {'crouch': 0, 'spring': 2, 'apex': 8, 'yellow': 10, 'lock': 14, 'dive': 20, 'hit': 22, 'end': 56}),
    # hr_design §2.3 (lane H1; motion: H1c in scarlet_clips.mjs): the 12 new fight clips; q_grab per §8.2 (the grab is
    # unparriable: purple star at 8, no parry cue)
    'grog_in': (12, None, {'hit': 0, 'buckle': 3, 'hat_off': 6, 'land': 10, 'end': 12}),
    'd4': (80, None, {'glint': 0, 'lock1': 7, 'h1': 14, 'lock2': 27, 'h2': 34, 'lock3': 37, 'h3': 44, 'lock4': 47, 'h4': 54,
                      'end': 80}),
    'tri': (84, None, {'glint': 0, 'lock0': 7, 'go': 12, 'h0': 14, 'lock1': 31, 'h1': 38, 'lock2': 41, 'h2': 48, 'lock3': 53,
                       'h3': 60, 'end': 84}),
    'rings': (78, None, {'glint': 0, 'lock1': 7, 'r1': 14, 'lock2': 17, 'r2': 24, 'lock3': 27, 'r3': 34, 'lock4': 37, 'r4': 44,
                         'lock5': 47, 'r5': 54, 'end': 78}),
    'ult': (86, None, {'yellow': 0, 'star1': 12, 'cut1': 24, 'web': 26, 'star2': 34, 'cut2': 46, 'settle': 56, 'end': 86}),
    'hcut': (52, None, {'yellow': 2, 'sparkle': 8, 'lock': 19, 'go': 24, 'cut': 26, 'end': 52}),
    'blue': (46, None, {'yellow': 0, 'blue': 4, 'lock': 15, 'go': 20, 'hit': 22, 'end': 46}),
    'kcut': (50, None, {'crouch': 0, 'yellow': 3, 'sparkle': 9, 'glow': 12, 'lock': 15, 'go': 20, 'cut': 22, 'end': 50}),
    'mx': (60, None, {'crouch': 0, 'star': 4, 'lock': 9, 'go': 14, 'x': 16, 'lock2': 21, 'dome': 28, 'end': 60}),
    'nb': (66, None, {'crouch': 0, 'leap': 2, 'apex': 8, 'lock1': 13, 'b1': 20, 'lock2': 23, 'b2': 30, 'lock3': 33, 'b3': 40,
                      'land': 46, 'end': 66}),
    'q_grab': (40, None, {'glint': 0, 'ghost': 4, 'star': 8, 'lock': 13, 'go': 16, 'grab': 20, 'end': 40}),
    'q_air': (96, None, {'throw': 0, 'rise': 2, 'apex': 10, 'lock1': 15, 'beam': 22, 'lock2': 31, 'dive': 34, 'hit': 38,
                         'land': 40, 'leap': 46, 'apex2': 52, 'star': 62, 'lock3': 67, 'pillar': 74, 'drop': 78, 'land2': 84,
                         'end': 96}),
    'a7_tell': (16, None, {'back': 0, 'yellow': 2, 'retreat': 4, 'settle': 14, 'end': 16}),
    'a7_throw': (16, None, {'crouch': 0, 'up': 4, 'crescent': 6, 'spin': 7, 'release': 12, 'end': 16}),
    'g_brim': (14, (6, 14), {'raise': 0, 'hold': 6, 'end': 14}),
    'g_tell': (12, None, {'lilac': 0, 'burst': 3, 'gone': 4, 'end': 12}),
    'g_reform': (10, None, {'appear': 0, 'solid': 4, 'end': 10}),
    'g_dash': (12, None, {'appear': 0, 'go': 6, 'arrive': 10, 'end': 12}),
    'g_glide': (12, None, {'appear': 0, 'go': 2, 'stop': 9, 'end': 12}),
    'g_drop': (14, None, {'flash': 0, 'gone': 2, 'appear': 7, 'land': 12, 'end': 14}),
    'g_run': (14, None, {'appear': 0, 'run': 2, 'lunge': 10, 'end': 14}),
    'g_ring': (14, None, {'arc': 0, 'hit': 3, 'spin': 4, 'end': 14}),
    'g_rise': (14, None, {'spin': 0, 'arms': 6, 'hit': 9, 'end': 14}),
    'g_leap': (18, None, {'coil': 0, 'raise': 5, 'hit': 9, 'tumble': 10, 'gone': 16, 'end': 18}),
    'g_sweep': (14, None, {'arm': 0, 'hit': 3, 'spring': 4, 'end': 14}),
    'g_x': (16, None, {'drop': 0, 'raise': 2, 'hit': 6, 'gone': 14, 'end': 16}),
    'g_wrap': (12, None, {'land': 0, 'hit': 3, 'end': 12}),
    'g_dome': (12, None, {'swirl': 0, 'hit': 3, 'end': 12}),
    'g_vert': (20, None, {'crouch': 0, 'glow': 1, 'hit': 5, 'rise': 6, 'gone': 18, 'end': 20}),
    'g_dive': (22, None, {'appear': 0, 'dive': 15, 'hit': 18, 'end': 22}),      # round V: the wind-up held 15 t in view (was dive 3, hit 6)
    'g_deflect': (12, None, {'stop': 0, 'fall': 2, 'lock': 10, 'end': 12}),
    'repel': (140, None, {'lock': 0, 'heave': 22, 'wide': 26, 'grab': 36, 'strike': 49, 'cut1': 56, 'cut2': 62, 'hook': 70,
                          'throw': 78, 'hat_off': 84, 'over': 88, 'land': 101, 'lie': 104, 'kick': 129, 'roll': 133,
                          'hat_on': 139, 'end': 140}),
    'down': (40, (0, 40), {}),
    'kipup': (20, None, {'legs': 0, 'up': 8, 'crouch': 10, 'raise': 14, 'end': 20}),
    # hr_design §4.1 (lane H2 / H2c, scarlet_cine.mjs): the three lead-ins (sq1 / lead_down / lead_stand are gone) and the
    # cinematic clips at their new lengths
    'lead60': (56, None, {'rise': 0, 'stand': 20, 'brim': 40, 'end': 56}),
    'lead5': (116, None, {'stagger': 0, 'back': 8, 'refill': 60, 'glow': 84, 'brim': 100, 'end': 116}),
    'lead_re': (60, None, {'refill': 10, 'brim': 44, 'end': 60}),
    'intro': (1290, None, {'l1': 258, 'take_bottle': 326, 'pour': 352, 'l2': 340, 'bottle_down': 414, 'l3': 462, 'raise': 470,
                           'l4': 540, 'drink': 600, 'l5': 690, 'cup_down': 700, 'grip': 756, 'glint': 764, 'stand': 792,
                           'l6': 838, 'turn': 840, 'l7': 906, 'smile': 912, 'l8': 980, 'off_rock': 1040, 'l9': 1044,
                           'walk': 1052, 'l10': 1140, 'stop': 1148, 'tip': 1160, 'crouch': 1230, 'leap': 1234, 'land': 1258,
                           'end': 1290}),
    'intro_end': (150, None, {'l11': 4, 'brim': 40, 'smile': 60, 'draw': 66, 'stance': 90, 'music': 130, 'end': 150}),
    'cs1': (720, None, {'lunge': 6, 'lock': 10, 'push': 30, 'leap': 34, 'land': 50, 'l13': 110, 'sheathe': 200, 'bottle': 216,
                        'l14': 232, 'hat_off': 240, 'hat_on': 258, 'smile': 280, 'raise': 300, 'offer': 404, 'drink': 458,
                        'props_off': 500, 'wipe': 506, 'l15': 578, 'iai': 610, 'l16': 618, 'draw': 642, 'slash': 650,
                        'recolour': 660, 'music': 676, 'end': 720}),
    'ending': (1372, None, {'up': 6, 'hat_on': 20, 'raise': 28, 'lunge': 50, 'graze': 52, 'lock': 56, 'burst': 70, 'shove': 80,
                            'back': 116, 'run': 150, 'clash': 190, 'rise': 204, 'a1': 228, 'a2': 262, 'a3': 286, 'a4': 298,
                            'off': 304, 'fly': 314, 'land': 334, 'scab_up': 388, 'swing': 398, 'l17': 420, 'music': 420,
                            'sheathe': 426, 'sheathed': 452, 'l18': 486, 'l19': 628, 'head_down': 640, 'turn': 650,
                            'l20': 716, 'look_back': 760, 'hand': 800, 'l21': 910, 'gaze': 990, 'pivot': 1072, 'l22': 1082,
                            'walk': 1094, 'stop': 1154, 'gesture': 1160, 'brim': 1216, 'l23': 1230, 'eyes': 1240,
                            'pull': 1290, 'open': 1360, 'end': 1372}),
    'ev_give': (34, None, {'lift': 0, 'present': 12, 'toss': 30, 'end': 34}),
    'ev_toast': (34, None, {'look': 0, 'palm': 14, 'offer': 30, 'end': 34}),
    'ev_leave': (10, None, {'turn': 0, 'gone': 6, 'end': 10}),
}
for _k, (_ln, _lp, _ev) in CLIPS_PLAN.items():
    assert _ev.get('end', _ln) == _ln, f'clip {_k}: end {_ev.get("end")} != len {_ln}'
# CLIPS[name] = (len, loop (from, to) or None, {event: tick}) with every event tick < len: the clip's end is its length
# (ev(clip, 'end') returns it), not a stored event. play/<name> and start/<name> exist for each. Clip ids (manifest
# order) = the index in CLIP_ORDER.
CLIPS = {k: (ln, lp, {e: t for e, t in ev_.items() if e != 'end'}) for k, (ln, lp, ev_) in CLIPS_PLAN.items()}
CLIP_ORDER = tuple(CLIPS)
assert len(CLIPS) == 59                 # hr_design §5.1: 47 - 3 (sq1, lead_down, lead_stand) + 3 lead-ins + 12 fight clips
CINE_CLIPS = ('intro', 'intro_end', 'cs1', 'lead60', 'lead5', 'lead_re', 'repel', 'ending')   # H2 / H2c (scarlet_cine.mjs)
EV_CLIPS = ('ev_give', 'ev_toast', 'ev_leave')                                                    # S2a (§7)
NEW_FIGHT_CLIPS = ('grog_in', 'd4', 'tri', 'rings', 'ult', 'hcut', 'blue', 'kcut', 'mx', 'nb', 'q_grab', 'q_air')   # H1 / H1c
UNUSED_CLIPS = ('a7_tell', 'a7_throw', 'g_deflect')     # kept in the rig, never played from H1's build on (hr_design §2.3)
# the rig generator takes owners 'S2b' / 'H2' from scarlet_cine.mjs and 'S2a' / 'H1' from scarlet_clips.mjs
CLIP_OWNER = {k: ('H2' if k in CINE_CLIPS else 'H1' if k in NEW_FIGHT_CLIPS else 'S2a') for k in CLIPS}
CLIP_SOURCE = {'S2a': 'scarlet_clips.mjs', 'H1': 'scarlet_clips.mjs', 'S2b': 'scarlet_cine.mjs', 'H2': 'scarlet_cine.mjs'}
assert all(k in CLIPS for k in CINE_CLIPS + NEW_FIGHT_CLIPS + UNUSED_CLIPS + EV_CLIPS)

REAL_MANIFEST = _TOOLS / 'scarlet_rig_manifest.json'                          # S2a writes it
STUB_MANIFEST = Path(__file__).resolve().parent / 'stub_rig_manifest.json'   # D0


def stub_manifest():
    """The D0 stub manifest (lead: --write-stub); S2a's real manifest adds transforms, models, budgets and sprites."""
    return {
        'schema': 1, 'id': ID, 'source': 'stub',
        '_doc': ('D0 stub of tools/scarlet_rig_manifest.json (S2a writes the real one with the same parts, clips, events, '
                 'looks, anchors and calls; the real one adds transforms, models, budgets, sprites). Generated from '
                 'tools/mboss_scarlet/api.py --write-stub: do not edit.'),
        'height': HEIGHT, 'hat_top': HAT_TOP, 'brim_d': BRIM_D, 'uuid': RIG_UUID,
        'parts': [{'name': p, 'nn': i, 'parent': PARENTS[p], 'uuid': RIG_UUID.format(i), 'tag': f'rlk_hr_{p}'}
                  for i, p in enumerate(PARTS)],
        'reparent': [{'part': p, 'look': v, 'parent': par} for (p, v), par in REPARENT.items()],
        'shadow': {'nn': SHADOW_NN, 'uuid': RIG_UUID.format(SHADOW_NN), 'radius': SHADOW_R,
                   'tags': ['rlk_room', 'rlk_mb_aux', TAGS['part'], 'rlk_hr_shadow']},
        'clips': {k: {'id': i, 'len': v[0], 'loop': list(v[1]) if v[1] else None, 'events': dict(v[2]),
                      'owner': CLIP_OWNER[k]}
                  for i, (k, v) in enumerate(CLIPS.items())},
        'looks': {k: list(v) for k, v in LOOKS.items()}, 'hands': list(HANDS), 'prop_states': list(PROP_STATES),
        'anchors': list(ANCHORS), 'calls': list(RIG_CALLS), 'macro_calls': {k: list(v) for k, v in RIG_MACRO_CALLS.items()},
    }


def check_manifest(m):
    """A rig manifest (stub or S2a's) carries exactly this contract: schema 1, id, the 29 parts in order, every clip with
    its len / loop / events, the anchors, the look channels, every call."""
    assert m.get('schema') == 1 and m.get('id') == ID, 'scarlet rig manifest: schema 1, id scarlet'
    got = {k: (v['len'], tuple(v['loop']) if v.get('loop') else None, v.get('events', {})) for k, v in m['clips'].items()}
    for k, (ln, lp, ev_) in CLIPS.items():
        assert k in got, f'rig manifest: clip {k} missing'
        assert got[k] == (ln, lp, ev_), f'rig manifest: clip {k} = {got[k]}, contract {(ln, lp, ev_)}'
        assert m['clips'][k]['id'] == CLIP_ORDER.index(k), f'rig manifest: clip {k} id'
    assert [p['name'] for p in m['parts']] == list(PARTS), 'rig manifest: parts / order differ from the contract'
    assert [p['nn'] for p in m['parts']] == list(range(len(PARTS))) and m['shadow']['nn'] == SHADOW_NN
    assert sorted(m.get('anchors', [])) == sorted(ANCHORS), 'rig manifest: anchors differ from the contract'
    assert {k: tuple(v) for k, v in m['looks'].items()} == LOOKS, 'rig manifest: look channels differ from the contract'
    assert set(RIG_CALLS) <= set(m['calls']) and m.get('macro_calls') == RIG_MACRO_CALLS, 'rig manifest: calls'
    return True


def rig_real():
    return REAL_MANIFEST.exists()


def rig_manifest():
    """S2a's manifest when it exists, else the D0 stub; both must carry exactly the contract (check_manifest)."""
    m = json.loads((REAL_MANIFEST if rig_real() else STUB_MANIFEST).read_text(encoding='utf-8'))
    check_manifest(m)
    return m


def rig(call, **macro):
    """The rig call line. While S2a's manifest is missing the core (S3) generates the stand-in rig_stub/** with the same
    call names (every play/<clip> / start/<clip> sets #rigc hr to the clip id for tests; no visuals)."""
    base = 'rig' if rig_real() else 'rig_stub'
    args = ('{' + ','.join(f'{k}:{v}' for k, v in macro.items()) + '}') if macro else ''
    return f'function {NS}{base}/{call}' + (f' {args}' if args else '')


def play(clip):
    """Play clip from its tick 0 at the next rig/tick (event e lands on the e-th rig/tick after the call; play replaces
    the running clip)."""
    assert clip in CLIPS, clip
    return rig(f'play/{clip}')


def start(clip):
    """Start clip now (tick 0 applied in this call)."""
    assert clip in CLIPS, clip
    return rig(f'start/{clip}')


def ev(clip, event):
    """The played tick of a clip event (every hit / effect tick comes from here); 'end' = the clip length."""
    ln, _lp, evs = CLIPS[clip]
    return ln if event == 'end' else evs[event]


def _script_hits(key):
    """HITS rows of a gauntlet: each cut lands as a parryable pdisc(CUT_R) on the contact of the move whose clip 'hit'
    meets the cut's strike."""
    rows, out = SCRIPTS[key], []
    for t, _step, clip, c in rows:
        if c:
            mv = [r for r in rows if r[2] and 'hit' in CLIPS[r[2]][2] and r[0] + ev(r[2], 'hit') == c[2]]
            assert len(mv) == 1, (key, c)
            out.append((mv[0][2], 'hit', 'pdisc', (CUT_R,), c[3], c[4], 'P'))
    return out


HITS.update({k: _script_hits(k) for k in GAUNTLETS})

# =============================================================================================
# 8. Kit contract (S1K implements in tools/build_mboss_hr_fx.py, PLAN §9.2). Values in tenths of a block / degrees /
# ticks; c per §2 (1 lilac, 2 pink-magenta, 3 yellow, 4 crimson, 5 white); look / g are names (quoted macro strings).
KIT_MANIFEST = _TOOLS / 'mboss_hr_fx_manifest.json'
KIT_PRESETS = {                       # fx/p/<name> (position / rotation = the effect)
    # F2 (HR-32): qi_band's sw = the forward sweep (tenths; A8.2 25 = the 2.5 b it always had, CS4 E1b her distance + 1 b)
    'qi_arc': ['r', 'yaw', 'pitch', 'roll', 'c'], 'qi_ring': ['r', 'c'], 'qi_band': ['len', 'yaw', 'pitch', 'roll', 'sw'],
    'qi_x': ['r'], 'qi_dome': ['r'], 'qi_vert': ['h', 'yaw', 'c'], 'qi_fan': ['h', 'c'], 'qi_wedge': ['r', 'roll'],
    'qi_ribbon': [], 'qi_line': ['len'], 'qi_cut': ['len'], 'glint': ['c'], 'star4': [], 'yellow_tell': ['t'],
    'ghost_burst': [], 'ghost_trail': ['len'], 'ghost_flash': [], 'afterimage': ['len'], 'blink_bubble': [],
    'shield_refill': [], 'pip_break': [], 'dive_impact': ['r'], 'light_column': [], 'claw_streaks': ['r'],
    'burst_radial': ['r'], 'dust_ring': ['r'], 'kick_flash': [], 'clash_gold': [], 'clash_spark': [], 'clash_arc': [],
    'deco_bolt': [], 'scarlet_line': ['len', 'yaw', 'roll'], 'petal_burst': ['r'], 'petals_drift': [],
    'petals_wind': [], 'petals_heart': [], 'motes_warm': [], 'leaves_dark': ['n'], 'leaves_swirl': [],
    'ambient_p1': [], 'ambient_p2': [], 'arrive_rift': [],
    # PLAN §7.3.2: the event coda's 8
    'ev_glint': [], 'ev_trail': [], 'ev_petals': ['n'], 'ev_leave': [], 'ev_beam': ['h', 't'], 'ev_wind': ['r'],
    'ev_palm': [], 'ev_take': ['c'],
}
KIT_BASE_PRESETS = len(KIT_PRESETS)   # 50: the 11-06 kit
# hr_design §2.1-2.2 / §5.1 (lane H1c's block of build_mboss_hr_fx.py): the kit holds a name once its generator declares it
# (kit_declares); KIT_PRESETS_PLAN is the whole contract (api.K checks names / args against it and returns '' for a preset
# the kit manifest does not have yet).
KIT_PRESETS_HR = {
    'flash_blue': ['t'],      # the blue unparriable flash on her chest: a yellow ring 4 t that turns into a translucent blue
    #                           sphere (diameter 1.8) round her for t ticks (blue: 15)
    'ult_web': ['t'],         # U cut1: 12 long qi_line cards through the arena + the `web` overlay glyph, t ticks (20)
    'ult_burst': [],          # U cut2: the web's lines fly outward
    'sky_mark': [],           # q: a thin vertical light line from 12 b up to the lock point + a 2-b pink flash line at the feet,
    #                           7 t (a line, never an area on the floor: hr_design §8.6)
    'sky_pillar': ['r'],      # q: the pink-white light column at the lock point (r tenths: 24)
    'qi_beam': ['len'],       # q / nb: the diagonal sword-qi band (the qi_band sprite pitched 35 deg), len tenths (140 / 160)
}


def _kit_src():
    f = _TOOLS / 'build_mboss_hr_fx.py'
    return f.read_text(encoding='utf-8') if f.exists() else ''


_KIT_SRC = _kit_src()


def kit_declares(kind, name):
    """True once tools/build_mboss_hr_fx.py declares the H-lane kit name: kind 'preset' = `@preset('<name>'`, 'ovl' =
    `api.OVERLAYS['<name>']`, 'sprite' = a sprite group `'<name>': [`."""
    pat = {'preset': f"@preset('{name}'", 'ovl': f"api.OVERLAYS['{name}']", 'sprite': f"'{name}': ["}[kind]
    return pat in _KIT_SRC


KIT_PRESETS_PLAN = {**KIT_PRESETS, **KIT_PRESETS_HR}
KIT_PRESETS.update({k: v for k, v in KIT_PRESETS_HR.items() if kit_declares('preset', k)})
SCARLET_LINE_ROLL = 'roll > 0 rises toward the player\'s right (CS1 C8 / the 5 % instant death: +13 deg)'
# fx/prop/<name> {look}: @s = the card / marker the caller summoned (summoned, then rotated); calling it again with
# another look re-looks it
# I1b (requests s1k-3 / s2b-4): moon_halo p1b / p2b = p1 / p2 about 20 % brighter (the same sprite, a brighter tint), for
# CS0 E3 (the cup raised to the moon) and the CS4 moon gaze (seq.py; back to p1 / p2 after).
KIT_PROPS = {'disc': {}, 'petal_big': {'look': ('whole', 'cut', 'split')},
             'moon_halo': {'look': ('p1', 'p2', 'off', 'p1b', 'p2b')},
             'lotus': {'look': ('bud', 'bloom')}, 'seat_rock': {'look': ('bottle', 'bare', 'set')}}
# fx/snd/<name>: one recipe per sound of PLAN §3-§5 and §7 (vanilla events only, mboss_lib.sound min-volume rule). The
# recipe the plan gives: ((event, volume, pitch), ...) layers; S1K may tune volumes by request.
KIT_SOUND_RECIPES = {
    # CS0 intro (§3.1)
    'cs0_wind': (('item.elytra.flying', 0.12, 0.6),),                     # E0 (stopsound at 40)
    'cs0_pour': (('item.bottle.empty', 0.3, 1.4),),                       # 32
    'cs0_sip': (('entity.generic.drink', 0.35, 1.3),),                    # 80
    'cs0_moon': (('block.amethyst_block.chime', 0.3, 1.2),),              # 118
    'cs0_cup': (('block.decorated_pot.insert', 0.3, 1.8),),               # 206
    'cloth': (('item.armor.equip_leather', 0.3, 1.0),),                   # 230, 630; CS4 984
    'grass_step': (('block.grass.step', 0.25, 1.0),),                     # walks (every 12 t); CS4 506-526
    'cs0_petals': (('block.cherry_leaves.fall', 0.3, 1.0),),              # 410
    'scab_raise': (('item.armor.equip_chain', 0.3, 1.4),),                # 510
    'draw_spin': (('item.trident.return', 0.6, 0.9),),                    # 606
    'draw': (('entity.player.attack.sweep', 0.6, 1.4),),                  # 610
    'draw_ring': (('block.amethyst_block.resonate', 0.5, 1.6),),          # 612
    # CS1 (§3.2)
    'lunge': (('entity.phantom.swoop', 0.5, 1.6),),                       # C0 2; CS4 E8 140
    'blade_lock': (('block.anvil.land', 0.35, 1.7), ('item.trident.hit', 0.5, 1.0)),   # C1 10
    'arc_crackle': (('entity.lightning_bolt.impact', 0.15, 2.0),),        # C1 14, 18
    'hat_swing': (('item.armor.equip_leather', 0.5, 1.0),),               # C2 40
    'land_grass': (('block.grass.step', 0.6, 1.0),),                      # C2 52
    'glint_ring': (('block.amethyst_block.resonate', 0.5, 1.8),),         # C3 96
    'black_drop': (('block.beacon.deactivate', 0.5, 0.6),),               # C4 100
    'petal_drift': (('block.cherry_leaves.fall', 0.4, 1.0),),             # C5 114
    'petal_cut': (('block.amethyst_block.chime', 0.6, 2.0),),             # C5 154
    'negative': (('entity.player.attack.sweep', 1.0, 0.5), ('item.trident.riptide_3', 0.6, 1.6)),   # C6 161
    'iai_slash': (('item.trident.thunder', 0.5, 1.4), ('entity.generic.explode', 0.3, 1.8),
                  ('block.glass.break', 0.5, 0.6)),                       # C8 169 (홍련일섬)
    # SQ1 and the lead-ins (§3.3, §3.5)
    'hat_on': (('item.armor.equip_leather', 0.4, 1.0),),                  # SQ1 28, lead_down 48, lead_stand 36
    'dark_fall': (('block.beacon.deactivate', 0.7, 0.6),),                # T0 - 17
    'dark_hum': (('entity.warden.sonic_charge', 0.2, 1.8),),              # T0 - 16
    'brim_ring': (('block.amethyst_block.resonate', 0.4, 1.2),),          # SQ1 48
    'shield_refill': (('block.respawn_anchor.charge', 0.4, 1.6),),        # the lead-ins' refill beat
    # the counter cinematic (§3.4)
    'repel_lock': (('block.anvil.land', 0.3, 1.8),),                      # R0 0
    'blade_tick': (('item.trident.hit', 0.4, 1.0),),                      # R0 4; CS4 64 72 108 116 124
    'grabbed': (('item.armor.equip_chain', 0.4, 0.8),),                   # R1 16
    'hat_clash': (('entity.player.attack.crit', 0.7, 1.0), ('block.anvil.place', 0.3, 1.6)),   # R2 24
    'tip_over': (('entity.player.attack.sweep', 0.6, 0.7),),              # R3 30
    'step_light': (('block.grass.step', 0.4, 1.0),),                      # R4 44; CS4 E6 80
    'thrown': (('entity.player.attack.knockback', 0.6, 1.0),),            # R5 58
    'land_back': (('entity.generic.big_fall', 0.6, 1.0), ('block.grass.break', 0.5, 1.0)),   # R6 75
    'petal_break': (('block.cherry_leaves.break', 0.4, 1.0),),            # R7 80 (at:5 only)
    'kick': (('entity.player.attack.strong', 0.8, 1.0), ('block.anvil.land', 0.4, 1.2)),     # R8 102
    # CS4 (§3.7)
    'band_glint': (('block.amethyst_block.resonate', 0.6, 1.8),),         # E1b 16
    'band_sweep': (('entity.breeze.wind_burst', 0.6, 1.2), ('entity.player.attack.sweep', 0.7, 0.8)),   # E1b 20
    'blade_charge': (('block.respawn_anchor.charge', 0.4, 1.8),),         # E2 48
    'clash': (('block.anvil.land', 0.4, 1.5), ('entity.player.attack.crit', 0.6, 1.0)),      # E2 58
    'clash_big': (('block.anvil.place', 0.3, 1.7), ('entity.player.attack.strong', 0.5, 1.0)),   # E7 96, E9 174 188
    'bolt_crackle': (('entity.lightning_bolt.impact', 0.2, 1.9),),        # E7 100
    'air_slash': (('entity.player.attack.sweep', 0.6, 1.0),),             # S3 204 216 228
    'air_clash': (('block.anvil.land', 0.5, 1.3),),                       # 216
    'air_white': (('item.trident.thunder', 0.3, 1.8),),                   # 232
    'land_far': (('entity.generic.big_fall', 0.4, 1.0),),                 # S4 258
    'scab_swing': (('item.armor.equip_chain', 0.3, 1.6),),                # S5 296
    'sheathe_click': (('block.iron_trapdoor.close', 0.25, 1.8),),         # S5 320
    'moon_gaze': (('block.amethyst_block.chime', 0.2, 0.8),),             # C1 700
    'pivot_cloth': (('item.armor.equip_leather', 0.2, 1.0),),             # C2 805
    # phase 1 (§4.3)
    'a1_fan': (('entity.player.attack.sweep', 0.6, 1.3),),                # A1 10
    'a1_hit': (('entity.breeze.wind_burst', 0.4, 1.5), ('block.amethyst_block.resonate', 0.5, 1.7)),   # A1 14
    'a2_draw': (('item.trident.throw', 0.4, 1.6),),                       # A2 4
    'a2_hit': (('entity.player.attack.sweep', 0.7, 1.5),),                # A2 12
    'a3_h1': (('entity.player.attack.sweep', 0.6, 1.2),),                 # A3 h1 .. h5: pitch 1.2 -> 1.6 rising
    'a3_h2': (('entity.player.attack.sweep', 0.6, 1.3),),
    'a3_h3': (('entity.player.attack.sweep', 0.6, 1.4),),
    'a3_h4': (('entity.player.attack.sweep', 0.6, 1.5),),
    'a3_h5': (('entity.player.attack.sweep', 0.6, 1.6), ('entity.breeze.wind_burst', 0.5, 1.0)),
    'leap': (('entity.breeze.jump', 0.5, 1.0),),                          # A4 2, A10 2
    'a4_glint': (('block.amethyst_block.resonate', 0.6, 1.9),),           # A4 7
    'a4_flip': (('entity.phantom.swoop', 0.5, 1.4),),                     # A4 14
    'a4_impact': (('entity.generic.explode', 0.3, 1.7), ('block.amethyst_block.break', 0.7, 1.0)),   # A4 20
    'a5_spin': (('item.trident.riptide_1', 0.5, 1.5),),                   # A4 30 (A5)
    'a6_blink': (('entity.illusioner.mirror_move', 0.7, 1.3),),           # A6 0
    'a6_arrive': (('entity.enderman.teleport', 0.2, 1.8),),               # A6 3
    'yellow_chime': (('block.bell.use', 0.6, 1.5), ('block.beacon.power_select', 0.5, 1.9)),   # A9 8, A10 10, A7 tell
    'a9_star': (('block.amethyst_block.chime', 0.8, 2.0),),               # A9 17
    'a9_flash': (('entity.illusioner.cast_spell', 0.6, 1.4),),            # A9 24
    'a9_cut': (('item.trident.riptide_3', 0.6, 1.6), ('entity.player.attack.sweep', 1.0, 0.6)),   # A9 28
    'a10_dive': (('entity.phantom.swoop', 0.6, 1.2),),                    # A10 20
    'a10_impact': (('item.mace.smash_ground', 0.6, 1.0), ('block.amethyst_cluster.break', 0.7, 1.0)),   # A10 22
    # the gauntlets / ghost moves (§4.5; "sweep pitch p" = the A8.1 sweep at volume 0.7)
    'g_tell': (('entity.illusioner.prepare_mirror', 0.7, 1.0), ('block.amethyst_block.resonate', 0.7, 1.2)),   # A8.T 0
    'g_appear': (('entity.illusioner.mirror_move', 0.5, 1.6),),           # D1 / D2 0
    'g_dash': (('entity.phantom.swoop', 0.4, 1.8),),                      # D1 / D2 6
    'g_flash': (('entity.illusioner.cast_spell', 0.5, 1.8),),             # D3 0
    'g_step': (('block.grass.step', 0.3, 1.0),),                          # D4 x3
    'g_ring': (('entity.player.attack.sweep', 0.7, 1.3), ('block.amethyst_block.resonate', 0.4, 1.0)),   # A8.1
    'g_rise': (('entity.player.attack.sweep', 0.7, 1.1),),                # A8.2
    'g_leap': (('entity.breeze.jump', 0.4, 1.0),),                        # A8.3 3
    'g_leap_cut': (('entity.player.attack.sweep', 0.7, 1.0),),            # A8.3 hit
    'g_sweep': (('entity.player.attack.sweep', 0.7, 0.8), ('item.trident.riptide_1', 0.4, 1.0)),   # A8.4
    'g_x': (('entity.player.attack.sweep', 0.7, 1.2),),                   # A8.5
    'g_wrap': (('entity.player.attack.sweep', 0.7, 1.0),),                # A8.6
    'g_dome': (('item.trident.riptide_2', 0.5, 1.4),),                    # A8.7
    'g_glow': (('block.amethyst_block.chime', 0.6, 1.9),),                # A8.8 1
    'g_vert': (('entity.player.attack.sweep', 0.7, 1.5),),                # A8.8 5
    'g_dive': (('entity.phantom.swoop', 0.7, 1.0),),                      # A8.9 3
    'deco_bolt': (('entity.lightning_bolt.impact', 0.15, 1.9),),          # BOLTS
    'disc_release': (('item.trident.riptide_2', 0.6, 1.7), ('entity.breeze.shoot', 0.5, 1.0)),   # A7 release
    'disc_fly': (('item.trident.throw', 0.3, 1.0),),                      # A7 flight
    # shield, judge, fails (§5.2, §5.4, §5.5)
    'pip_break': (('block.amethyst_cluster.break', 0.8, 1.4), ('entity.player.attack.crit', 0.5, 1.6)),
    'deflect': (('block.anvil.land', 0.6, 1.4), ('entity.player.attack.crit', 0.8, 1.0)),
    'fail_impact': (('entity.generic.explode', 0.5, 1.4), ('block.amethyst_block.break', 0.8, 1.0)),
    'fatal_slash': (('item.trident.thunder', 0.7, 1.2), ('entity.player.attack.sweep', 1.0, 0.5),
                    ('block.glass.break', 0.6, 0.5)),
    # the event coda (§7.3.2)
    'ev_lift': (('item.armor.equip_chain', 0.6, 1.2),),
    'ev_chime': (('block.amethyst_block.chime', 0.5, 1.4),),
    'ev_toss': (('entity.breeze.wind_burst', 0.4, 1.6),),
    'ev_leave': (('entity.breeze.whirl', 0.6, 1.3), ('block.cherry_leaves.break', 0.5, 1.0)),
    'ev_beam': (('block.amethyst_block.resonate', 0.7, 0.9),),
    'ev_take_i': (('item.armor.equip_netherite', 0.7, 1.1), ('block.note_block.chime', 0.6, 1.5)),
    'ev_take_b': (('entity.generic.drink', 0.5, 1.2), ('block.amethyst_block.resonate', 0.7, 1.4)),
    # hr_design §2.1-2.2 (lane H1 / H1c; the kit generator writes fx/snd/<name> for every recipe of this table)
    # HA-06 (review H-A, lead ruling): the cue ("press F now") is its own sound family, unlike the purple flash's amethyst
    # chime ("F does nothing"): a short, light metal tink no other recipe of hers uses
    'parry_cue': (('block.note_block.iron_xylophone', 0.7, 1.8),),        # CUE_SND: h - 7 of every parryable hit
    'flash_blue': (('block.beacon.activate', 0.5, 1.8),),                 # the blue flash
    'ult_cut1': (('item.trident.thunder', 0.6, 1.6), ('block.glass.break', 0.7, 0.6)),       # U 24
    'ult_cut2': (('entity.generic.explode', 0.4, 1.6), ('block.glass.break', 0.8, 0.5)),     # U 46
    'sky_pillar': (('item.trident.thunder', 0.5, 1.9),),                  # q pillar 74
    'kcut_go': (('item.trident.riptide_3', 0.6, 1.4),),                   # kcut's dash-through 20
}
KIT_SOUNDS = tuple(KIT_SOUND_RECIPES)
# fx/hud/<name>: line {id} (LINES 1-25, letter reveal, overlay-aware), ovl {g,in,hold,out} (a full-screen title glyph;
# vBig = in + hold + out), warn {on} (bossbar WARN_BOSSBAR: WARN_TEXT, WARN_HL), skip {s} (the intro prompt SKIP_TEXT +
# SKIP_HINT at brightness step s 0-4, hudHold 2; s 5 clears it), clear. Font FONT: glyph roots empty and unstyled,
# every component names its font, the font ends with a minecraft:default reference.
KIT_HUD = {'line': ['id'], 'ovl': ['g', 'in', 'hold', 'out'], 'warn': ['on'], 'skip': ['s'], 'clear': []}
OVERLAYS = {'black': 0xEC10, 'negative': 0xEC11, 'pinkwhite': 0xEC12, 'red_tint': 0xEC13, 'magenta': 0xEC14,
            'white': 0xEC15}     # ~144 x 81 glyphs sized as Apep's; `negative` is an approximation (PLAN §3.0)
VIG = 0xEC16                     # §7.4.5: the edge-only vignette glyph (centre clear) SR's hand-written item code titles
OVERLAYS_BASE = tuple(OVERLAYS)
# hr_design §3.0 / §2.2: `gold` (lane H2c: the deflect / clash wash) and `web` (lane H1c: U's shattered glass); in OVERLAYS once
# the kit generator declares them (kit_declares 'ovl'); their opacity steps follow the base six's (U+EC38-EC3F)
OVERLAYS_HR = {'gold': 0xEC17, 'web': 0xEC18}
OVERLAYS_PLAN = {**OVERLAYS, **OVERLAYS_HR}
OVERLAYS.update({k: v for k, v in OVERLAYS_HR.items() if kit_declares('ovl', k)})
OVERLAY_GLYPH = (144, 81)
KIT_FIXED = ('card', 'cardx', 'look', 'clear', 'uninstall')     # fx/<name> (no args)
# F2 (HR-17 / HR-23): two switches around preset calls (fx/<name>, no args). keep_on .. keep_off: the cards made meanwhile
# carry rlk_hr_fx_keep and survive fx/clear and the ager's dead / revive clear (the instant death's line, CS3's kick); the
# module's cleanup and fx/uninstall still remove them. follow_on (@s = the lead: her body) .. follow_off: the cards made
# meanwhile follow the lead every tick (its x / z, their own height over it).
KIT_FIXED += ('keep_on', 'keep_off', 'follow_on', 'follow_off')
KIT_KEEP_TAG = 'rlk_hr_fx_keep'
FX_CARD_CAP, AMBIENT_CARD_CAP = 96, 48                           # the 아를레키노 caps; the ager kills the oldest
AFTERIMAGE_MAX, AFTERIMAGE_FADE = 4, 6                           # one silhouette card per frame, <= 4 alive, fades 6 t
# Kit sprites in the items atlas (the §9.2 table): name -> ((frames, w, h), ...); the kit generator asserts its sprites
# against this and the sum <= KIT_SPRITE_CAP. The overlays and vig are font glyphs (not in the items atlas).
KIT_SPRITES = {
    'qi_arc': ((4, 128, 64),),                       # crescent (also qi_vert, qi_fan, qi_x = two crossed arcs)
    'qi_ring': ((2, 128, 128),),                     # flat ring (also qi_dome's rim)
    'qi_band': ((2, 128, 32),), 'qi_ribbon': ((2, 128, 32),), 'ghost_trail': ((2, 128, 32),),
    'qi_dome': ((1, 128, 64),), 'qi_wedge': ((1, 64, 128),),
    'glint': ((2, 32, 32),),                         # glint + star4
    'shards': ((2, 32, 32),),                        # shield_refill / pip_break
    'lotus': ((2, 32, 32),),                         # bud / bloom
    'yellow_tell': ((1, 64, 64), (1, 128, 16)),      # sphere + flare line
    'ghost_burst': ((3, 64, 64),), 'ghost_flash': ((1, 64, 64),), 'blink_bubble': ((1, 64, 64),),
    'afterimage': ((1, 64, 128),),
    'dive_impact': ((1, 128, 128),),                 # also burst_radial
    'light_column': ((1, 32, 128),), 'claw_streaks': ((1, 32, 128),), 'deco_bolt': ((1, 32, 128),),
    'clash_gold': ((2, 64, 64),),                    # clash_gold / kick_flash
    'clash_spark': ((2, 32, 128),),                  # clash_spark / clash_arc
    'scarlet_line': ((1, 256, 16),),
    'petal_big': ((3, 64, 64),), 'petals_small': ((8, 16, 16),),   # whole / cut / split; small petals and leaves
    'moon_halo': ((2, 96, 96),),                     # p1 / p2
    'disc': ((2, 64, 64),),
    'seat_rock': (),                                 # vanilla block textures
}
KIT_SPRITE_CAP = 260_000
# hr_design §5.4: 22 432 px were left; the one planned new sprite group (lane H1c), counted once the kit generator declares it
KIT_SPRITES_HR = {'flash_blue': ((1, 64, 64),),      # the translucent blue sphere (<= 4 096 px); everything else reuses sprites
                  'cue': ((1, 64, 64),),             # HA-07 (review H-A): the parry cue's white-gold sparkle (4 096 px)
                  # round V (lane VB): the flashes' rimmed star (sw_head); round W (lane WB, w_brief §2 WB): the blade's trail -
                  # the band / ribbon / rim wall (sw_rib), the swept sector (sw_arc) and strip (sw_quad), 3 fading frames each
                  'sw_rib': ((3, 16, 16),), 'sw_head': ((1, 64, 64),), 'sw_arc': ((3, 64, 64),), 'sw_quad': ((3, 16, 16),)}
KIT_SPRITES.update({k: v for k, v in KIT_SPRITES_HR.items() if kit_declares('sprite', k)})
KIT_SPRITE_PX = sum(f * w * h for rows in KIT_SPRITES.values() for f, w, h in rows)
assert KIT_SPRITE_PX == 237_568 + sum(f * w * h for k, rows in KIT_SPRITES_HR.items() if k in KIT_SPRITES for f, w, h in rows) \
    and KIT_SPRITE_PX <= KIT_SPRITE_CAP, KIT_SPRITE_PX
ATLAS_CAP = {'rig': 150_000, 'kit': KIT_SPRITE_CAP, 'gate_icon': 5_000, 'event': 0, 'boss': 430_000}   # PLAN §9.5
GATE_ICON_PX_CAP = ATLAS_CAP['gate_icon']


def _macro(a):
    def v(x):
        return f'"{x}"' if isinstance(x, str) else str(int(x))
    return '{' + ','.join(f'{k}:{v(x)}' for k, x in a.items()) + '}'


class _Kit:
    """Kit call lines. Empty while the kit manifest is missing, so S2b / S3 / S4 build and load without S1K's files (the
    Apep / Tachy / Arlecchino 'api.K stand-in' rule); names / args are checked against the contract either way."""

    _mf = None

    def _on(self):
        return KIT_MANIFEST.exists()

    def has(self, kind, name):
        """True when the kit manifest in use has the name (kind 'presets' / 'sounds' / 'glyphs'): a planned H-lane name
        (KIT_PRESETS_PLAN, OVERLAYS_PLAN) gives '' lines until its lane's kit block has landed and the kit was regenerated."""
        if not self._on():
            return False
        if _Kit._mf is None:
            _Kit._mf = json.loads(KIT_MANIFEST.read_text(encoding='utf-8'))
        return name in _Kit._mf.get(kind, {})

    def _call(self, sub, table, name, a):
        assert name in table, f'kit {sub}{name} is not in the contract'
        assert sorted(a) == sorted(table[name]), f'kit {sub}{name} takes {table[name]}'
        if not self._on():
            return ''
        return f'function {NS}fx/{sub}{name}' + (f' {_macro(a)}' if a else '')

    def p(self, name, **a):
        if name in KIT_PRESETS_HR and not self.has('presets', name):
            assert sorted(a) == sorted(KIT_PRESETS_HR[name]), f'kit p/{name} takes {KIT_PRESETS_HR[name]}'
            return ''
        return self._call('p/', KIT_PRESETS_PLAN, name, a)

    def pw(self, name, path):
        """fx/p/<name> with storage <path> (F2: arguments computed at run time, e.g. A9's probed streak length core.a9,
        CS4 E1b's band sweep); the compound must hold every arg of the preset (extra keys are allowed)."""
        assert name in KIT_PRESETS_PLAN and KIT_PRESETS_PLAN[name], f'kit p/{name}: no macro args'
        if name in KIT_PRESETS_HR and not self.has('presets', name):
            return ''
        return f'function {NS}fx/p/{name} with storage {path}' if self._on() else ''

    def prop(self, name, **a):
        assert name in KIT_PROPS, f'kit prop/{name} is not in the contract'
        spec = KIT_PROPS[name]
        for k, vals in spec.items():
            assert a.get(k) in vals, f'kit prop {name}: {k} must be one of {vals}'
        return self._call('prop/', {n: list(s) for n, s in KIT_PROPS.items()}, name, a)

    def hud(self, name, **a):
        if name == 'line':
            assert a.get('id') in LINES, a
        if name == 'ovl':
            assert a.get('g') in OVERLAYS_PLAN, a
            if a['g'] in OVERLAYS_HR and not self.has('glyphs', a['g']):
                return ''
        if name == 'skip':
            assert 0 <= int(a.get('s', -1)) <= 5, a
        return self._call('hud/', KIT_HUD, name, a)

    def ovl(self, g, t_in, hold, t_out):
        """fx/hud/ovl {g,in,hold,out} (in is a Python keyword)."""
        return self.hud('ovl', **{'g': g, 'in': t_in, 'hold': hold, 'out': t_out})

    def snd(self, name):
        assert name in KIT_SOUNDS, name
        return f'function {NS}fx/snd/{name}' if self.has('sounds', name) else ''

    def fixed(self, name):
        assert name in KIT_FIXED, name
        return f'function {NS}fx/{name}' if self._on() else ''


K = _Kit()


def lines(*cmds):
    """Drop the empty stand-in lines (kit, rig, arena, bars, event)."""
    return [c for c in cmds if c]

# =============================================================================================
# 9. Writer, Pattern, Service, the cut / disc / shield builders, bars, music (PLAN §5.3, §9.2)


class Writer:
    """Writes F:boss/scarlet/<rel> for one owner; rel must start with one of `prefixes` (ownership is enforced)."""

    def __init__(self, owner, prefixes):
        self.owner, self.prefixes = owner, tuple(prefixes)
        self.out = L.Out(owned_dirs=[f'{ROOT}/{p.rstrip("/")}' for p in self.prefixes if p.endswith('/')],
                         owned_files=[f'{ROOT}/{p}' for p in self.prefixes if not p.endswith('/')])

    def w(self, rel, body):
        assert rel.startswith(self.prefixes), f'{self.owner} may not write {rel} (owns {self.prefixes})'
        return self.out.write(f'{ROOT}/{rel}', body)

    def clean(self):
        return self.out.clean()


@dataclass
class Pattern:
    """One AI pattern (P1: S3's p1.py; P2 + gauntlets: S4's p_ghost.py). Runtime contract (all @s = the body, at it;
    clock #pt hr = played ticks since start, set to 0 by the core before `start` and +1 before each `tick`):
      p/<key>/start   begin (play the first clip, lock aims)        p/<key>/tick    one tick (k/<t> busy-tick files)
      p/<key>/cancel  remove every hazard / marker / disc / cut / prop of the pattern (rlk_hr_p_<key>, rlk_hr_cut), stop
                      sounds, lift nothing the core owns; idempotent
      p/<key>/pause, resume (optional: redraw what pause removed)
    The pattern sets `#done hr 1` on its last tick; it never touches another pattern's state, the phase, the floors, the
    invulnerability / cine, the shield bookkeeping (only SHIELD_CALLS), the HUD or the arena look (core-owned; the
    gauntlets request looks through arena_look). Hits only through the framework (mboss/hz/*, pj/launch, grp_new, pl_dot)
    with the HITS tiers, Electro 1U, #hzQuiet 1, never a floor decal; counting / ghost cuts only through cut(), discs only
    through disc(); end points via mv/ok inside MOVE_R."""
    key: str
    tid: int
    clips: tuple
    build: object                      # build(W: Writer) -> None
    pause: bool = False
    notes: str = ''

    @property
    def name(self):
        return PATTERN_NAMES[self.key]

    @property
    def script(self):
        return SCRIPTS.get(self.key)


@dataclass
class Service:
    """A sequence body (S2b's seq.py, written by S3's generator with Writer('S2b', OWN['S2b'])):
    seq/<name>/{start,tick,cancel} on clock #sq hr (0 at start, +1 before tick); sets #sqdone hr 1 at its end; cancel is
    idempotent. start takes SEQ_ARGS[name] as macro args (repel {at:60|5}, lead_re {g:"a8"|"a13"}); intro and cs1 also have
    seq/<name>/skip (SEQ_EXTRA, SKIP). The core owns invulnerability, cine, the phase switch, floors, the death finish, when a
    sequence starts, the HP steps (the sequence marks COUNTER_EV, the core applies them) and the intro skip input; a
    sequence owns its clips, sounds, kit effects / props, lines (K.hud('line')), titles, overlays, push rings, the look
    requests (arena_look), the body moves (mboss/mv/* + mv/ok) and the music line of its music event (music(ph)). The
    event coda calls the event logic only through ev_apply() / ev_title()."""
    name: str
    clip: tuple
    build: object
    events: dict = field(default_factory=dict)
    args: dict = field(default_factory=dict)


# Owned output prefixes under F:boss/scarlet/ per stage (the top generator tools/build_mboss_scarlet.py (S3) creates one
# Writer each). rig/** (S2a, tools/build_scarlet_rig.mjs) and fx/** (S1K, tools/build_mboss_hr_fx.py) are written by
# their own generators (OWN_GEN).
OWN = {
    'S3': tuple(L.HOOKS) + tuple(L.HELP_HOOKS) + ('init', 'reward', 'core/', 'ai/', 'shield/', 'ult/', 'hud/', 'ev/',
                                                 'test/', 'rig_stub/', 'bal_') + tuple(f'p/{k}/' for k in P1),
    'S4': tuple(f'p/{k}/' for k in P2) + ('g/',),
    'S2b': ('seq/',),
}
OWN_GEN = {'S2a': ('rig/',), 'S1K': ('fx/',)}
# Every file / tree PLAN §9.0-9.1 names, per owner (the lead's D0 files included). Patterns: 'T:' = tools/, 'F:' =
# data/rlk/function/ (no .mcfunction), 'R:' = roguelike/, 'RP:' = a resource-pack copy's assets/rlk/, 'HR:' = the
# scratchpad hr/ (tests, scratch, renders, RP copies); '**' = any depth. (pattern, excluded patterns). Each stage owns
# its scratch folder HR:<stage>/** (readme fragments included), its renders HR:renders/<prefix>_* and its RP copy
# HR:rp_<stage>/**. Generated outputs belong to the stage whose generator writes them, also when an unchanged
# generator writes them because of that stage's input (S1K's theme -> the hr_field lines of mboss/arena/{job_tick,abort}).
# Shared by design, outside this table: the RP items atlas assets/minecraft/atlases/items.json (each RP generator adds
# only its own entries, as every precedent) and the hand files' generator hook lines (F:load, F:uninstall: SR adds its
# lines beside them, never edits theirs).
_OWN_FILES = {
    'lead': (('T:mboss_scarlet/__init__.py', ()), ('T:mboss_scarlet/api.py', ()),
             ('T:mboss_scarlet/stub_rig_manifest.json', ()), ('HR:contract.md', ()), ('HR:stage_briefs.md', ()),
             ('HR:tools/**', ()), ('T:dev/regen_all.sh', ()), ('R:README.md', ())),
    'S1': (('T:build_mboss_core.py', ()), ('T:mboss_lib.py', ()), ('T:mboss_registry.json', ()),
           ('T:check_mboss_pack.py', ()), ('HR:tests/test_special_hr.py', ()), ('HR:tests/lib/**', ()),
           ('HR:s1/**', ()),
           ('F:mboss/**', ('F:mboss/arena/**', 'F:mboss/guardian/**', 'F:mboss/butterfly/**', 'F:mboss/fieldgen/**',
                           'F:mboss/proto/**', 'F:mboss/cproto/**', 'F:mboss/spproto/**')),
           ('F:boss/test/**', ())),
    'S1K': (('T:build_mboss_hr_fx.py', ()), ('T:mboss_hr_fx_paint.py', ()), ('T:mboss_hr_fx_manifest.json', ()),
            ('T:mboss_arena_hr_field.py', ()), ('F:boss/scarlet/fx/**', ()), ('F:mboss/arena/hr_field/**', ()),
            ('F:mboss/arena/job_tick', ()), ('F:mboss/arena/abort', ()),
            ('RP:textures/mboss/hr_kit/**', ()), ('RP:models/item/mboss/hr_kit/**', ()), ('RP:items/mboss/hr_kit/**', ()),
            ('RP:font/mboss_hr.json', ()), ('RP:textures/font/mboss_hr/**', ()), ('HR:tests/test_kit.py', ()),
            ('HR:tests/test_arena_hr.py', ()), ('HR:s1k/**', ()), ('HR:renders/s1k_*', ()), ('HR:rp_s1k/**', ())),
    'S2a': (('T:build_scarlet_rig.mjs', ()), ('T:scarlet_pose.mjs', ()), ('T:scarlet_geometry.mjs', ()),
            ('T:scarlet_paint.mjs', ()), ('T:scarlet_clips.mjs', ()), ('T:scarlet_rig_manifest.json', ()),
            ('T:scarlet_rig_api.md', ()), ('F:boss/scarlet/rig/**', ()), ('RP:textures/mboss/scarlet/**', ()),
            ('RP:models/item/mboss/scarlet/**', ()), ('RP:items/mboss/scarlet/**', ()),
            ('HR:tests/test_rig.py', ()), ('HR:s2a/**', ()), ('HR:renders/s2_*', ()), ('HR:rp_s2a/**', ())),
    'S2b': (('T:scarlet_cine.mjs', ()), ('T:mboss_scarlet/seq.py', ()), ('F:boss/scarlet/seq/**', ()),
            ('HR:tests/ev_dry.py', ()), ('HR:s2b/**', ()), ('HR:renders/s2b_*', ()), ('HR:rp_s2b/**', ())),
    'S3': (('T:build_mboss_scarlet.py', ()), ('T:mboss_scarlet/core.py', ()), ('T:mboss_scarlet/ai.py', ()),
           ('T:mboss_scarlet/shield.py', ()), ('T:mboss_scarlet/p1.py', ()), ('T:mboss_scarlet/s3lib.py', ()),
           ('T:mboss_scarlet/reward.py', ()),
           ('F:boss/scarlet/**', ('F:boss/scarlet/rig/**', 'F:boss/scarlet/fx/**', 'F:boss/scarlet/seq/**',
                                  'F:boss/scarlet/g/**', *(f'F:boss/scarlet/p/{k}/**' for k in P2))),
           ('HR:tests/test_scarlet.py', ()), ('HR:tests/pat_p1.py', ()), ('HR:tests/test_reward.py', ()),
           ('HR:s3/**', ()), ('HR:renders/s3_*', ())),
    'S4': (('T:mboss_scarlet/p_ghost.py', ()), ('F:boss/scarlet/g/**', ()),
           *((f'F:boss/scarlet/p/{k}/**', ()) for k in P2), ('HR:tests/pat_ghost.py', ()), ('HR:s4/**', ()),
           ('HR:renders/s4_*', ())),
    'SR': (('F:items/**', ()), ('F:player/take_damage', ()), ('F:player/def/judge', ()), ('F:player/reset_one', ()),
           ('F:player/update_item', ()), ('F:player/update_item_macro', ()), ('F:player/hr_moon/**', ()),
           ('F:codex/labels', ()), *((f'F:snd/f{i}', ()) for i in range(422, 430)), ('F:load', ()), ('F:uninstall', ()),
           ('R:items.md', ()), ('HR:tests/test_hwamu.py', ()), ('HR:tests/test_moon.py', ()), ('HR:sr/**', ()),
           ('HR:renders/sr_*', ())),
}
# + every stage owns its own request file HR:requests/<stage>.md (the lead applies requests at I1)
OWN_FILES = {o: pats + (((f'HR:requests/{o.lower()}.md', ()),) if o != 'lead' else ()) for o, pats in _OWN_FILES.items()}
# Base branch of each stage (PLAN §9.7): S3 from S1's head, S2b from S2a's, S4 from S3's; the rest from D0.
STAGE_BASE = {'S1': 'wip/hr-d0', 'S1K': 'wip/hr-d0', 'S2a': 'wip/hr-d0', 'SR': 'wip/hr-d0', 'S3': 'wip/hr-s1',
              'S2b': 'wip/hr-s2a', 'S4': 'wip/hr-s3'}
# Sequential hand-overs PLAN §9.1 / §9.3 prescribe: OWN_FILES names the creator, who owns the path until its report; the
# taker (a stage that branches from the creator's head) owns it from its own start; never both at once.
HANDOVER = {
    'HR:tests/lib/**': ('S1', 'S3'),               # vendored sims (unchanged, md5s in README.md) + the generic hrsim.py;
    #                                                S3 extends hrsim.py; every other stage reads it (own helpers in HR:<s>/)
    'HR:tests/test_rig.py': ('S2a', 'S2b'),        # S2b adds the cinematic-clip checks (PLAN §9.3)
    'T:scarlet_rig_manifest.json': ('S2a', 'S2b'),  # S2b re-runs S2a's unchanged generator with its scarlet_cine.mjs and
    'F:boss/scarlet/rig/**': ('S2a', 'S2b'),        # commits what that regenerates (never S2a's sources)
    'RP:textures/mboss/scarlet/**': ('S2a', 'S2b'),
    'RP:models/item/mboss/scarlet/**': ('S2a', 'S2b'),
    'RP:items/mboss/scarlet/**': ('S2a', 'S2b'),
}
# The files / trees PLAN §9.0-9.1 name (one concrete representative path per tree): each must be owned exactly once.
FILES_9_1 = (
    'T:mboss_scarlet/__init__.py', 'T:mboss_scarlet/api.py', 'T:mboss_scarlet/stub_rig_manifest.json', 'HR:contract.md',
    'HR:stage_briefs.md', 'HR:tools/regen_d0.sh', 'T:dev/regen_all.sh', 'R:README.md',
    'T:build_mboss_core.py', 'T:mboss_lib.py', 'T:mboss_registry.json', 'T:check_mboss_pack.py',
    'HR:tests/test_special_hr.py', 'HR:tests/lib/hrsim.py', 'HR:tests/lib/cmsim.py', 'HR:s1/readme_special.md',
    'F:mboss/sp/reward', 'F:mboss/death_finish',
    'F:mboss/world', 'F:mboss/fight_vars', 'F:mboss/cleanup_fight', 'F:mboss/test/swon', 'F:mboss/test/swon_msg_w',
    'F:mboss/register', 'F:mboss/ar/hr_field/ok', 'F:mboss/bars_off', 'F:mboss/bars_on', 'F:boss/test/special',
    'T:build_mboss_hr_fx.py', 'T:mboss_hr_fx_paint.py', 'T:mboss_hr_fx_manifest.json', 'T:mboss_arena_hr_field.py',
    'F:boss/scarlet/fx/p/qi_arc', 'F:boss/scarlet/fx/p/ev_beam', 'RP:textures/mboss/hr_kit/qi_arc.png',
    'RP:models/item/mboss/hr_kit/gate_icon.json', 'RP:items/mboss/hr_kit/gate_icon.json', 'RP:font/mboss_hr.json',
    'RP:textures/font/mboss_hr/black.png', 'F:mboss/arena/hr_field/look/dark', 'F:mboss/arena/job_tick',
    'F:mboss/arena/abort', 'HR:s1k/rp_readme_kit.md', 'HR:renders/s1k_sprites.jpg', 'HR:rp_s1k/pack.mcmeta',
    'T:build_scarlet_rig.mjs', 'T:scarlet_pose.mjs', 'T:scarlet_geometry.mjs', 'T:scarlet_paint.mjs',
    'T:scarlet_clips.mjs', 'T:scarlet_rig_manifest.json', 'T:scarlet_rig_api.md', 'F:boss/scarlet/rig/tick',
    'RP:models/item/mboss/scarlet/item_sword.json', 'RP:items/mboss/scarlet/item_sword.json',
    'RP:textures/mboss/scarlet/body.png', 'HR:tests/test_rig.py', 'HR:renders/s2_U1.jpg', 'HR:rp_s2a/pack.mcmeta',
    'T:scarlet_cine.mjs', 'T:mboss_scarlet/seq.py', 'F:boss/scarlet/seq/event/start', 'HR:tests/ev_dry.py',
    'HR:renders/s2b_cs1.jpg', 'HR:rp_s2b/pack.mcmeta',
    'T:build_mboss_scarlet.py', 'T:mboss_scarlet/core.py', 'T:mboss_scarlet/ai.py', 'T:mboss_scarlet/shield.py',
    'T:mboss_scarlet/p1.py', 'T:mboss_scarlet/s3lib.py', 'T:mboss_scarlet/reward.py', 'F:boss/scarlet/spawn',
    'F:boss/scarlet/test/help', 'F:boss/scarlet/init', 'F:boss/scarlet/shield/cut', 'F:boss/scarlet/ult/fatal',
    'F:boss/scarlet/ev/roll', 'F:boss/scarlet/reward', 'F:boss/scarlet/p/a1/start', 'F:boss/scarlet/rig_stub/tick',
    'HR:renders/s3_a1.png',
    'T:mboss_scarlet/p_ghost.py', 'F:boss/scarlet/p/a8/start', 'F:boss/scarlet/p/a13/start', 'F:boss/scarlet/p/mx/start',
    'F:boss/scarlet/p/nb/start', 'F:boss/scarlet/p/q/start', 'F:boss/scarlet/g/cut/make', 'HR:renders/s4_a8.png',
    'F:items/mythic/sword_hwamu/def', 'F:items/proc/hw_hit', 'F:items/register', 'F:player/take_damage',
    'F:player/def/judge', 'F:player/reset_one', 'F:player/update_item', 'F:player/update_item_macro',
    'F:player/hr_moon/apply', 'F:codex/labels', 'F:snd/f422', 'F:snd/f429', 'F:load', 'F:uninstall', 'R:items.md',
    'HR:tests/test_hwamu.py', 'HR:tests/test_moon.py', 'HR:renders/sr_tooltip.txt',
    *(f'HR:requests/{o.lower()}.md' for o in _OWN_FILES if o != 'lead'),
)


def owners_of(path):
    """The owners whose OWN_FILES patterns match path (minus their exclusions)."""
    return [o for o, pats in OWN_FILES.items()
            if any(fnmatchcase(path, p) and not any(fnmatchcase(path, x) for x in ex) for p, ex in pats)]


# Shield = the 5-segment gauge inside a gauntlet (hr_design §1.2; shield.py -> p_ghost.py): call names under
# F:boss/scarlet/ and their macro args
SHIELD_CALLS = {'arm': 'shield/arm', 'judge': 'shield/judge', 'fail60': 'ult/fail60', 'fatal': 'ult/fatal',
                'off': 'shield/off'}
SHIELD_ARGS = {}
GRES = '#gres'          # objective OBJ, after shield/judge: 1 deflect, 2 fail
PIPS_FP = GAUGE_FP      # the segments left = #gau / GAUGE['seg'] (the under bar #buSub)


def shield(call, **a):
    """A shield call line (shield/arm: the gauge 5/5 + the under bar + the refill effect; shield/judge -> #gres hr;
    ult/fail60; ult/fatal (@s = the player); shield/off: the gauge 0). The pip of a cut is the core's: shield/tick after
    every gauntlet tick takes one segment for a perfect parry (PIP_RULE)."""
    assert call in SHIELD_CALLS and sorted(a) == sorted(SHIELD_ARGS.get(call, [])), (call, a)
    return f'function {NS}{SHIELD_CALLS[call]}' + (f' {_macro(a)}' if a else '')


# The cut builder (hr_design §2.4; p_ghost.py implements g/cut/**): a gauntlet cut = a quiet Electro disc hazard of radius
# CUT_R at the player's feet, parryable (hz_opts noparry 0), made at `made` (tell = strike - made), re-aimed onto the player
# every tick until `lock` = strike - LOCK_LEAD, then fixed; the parry cue plays at the lock tick (the pattern's line).
CUT_CALLS = ('g/cut/make', 'g/cut/aim', 'g/cut/lock')
CUT_ARGS = {'g/cut/make': ['s', 't', 'dmg', 'kb', 'n'], 'g/cut/aim': ['s'], 'g/cut/lock': ['s']}


def cut(made, lock, strike, tier='TC', kb=KB_CUT, count=1):
    """[(pattern tick, line)] of one cut: make at `made` (s = strike tick, t = strike - made, dmg = DMG[tier], kb, n =
    1 counting / 0 not), aim every tick made+1 .. lock-1, lock at `lock` (the last aim).
    @s / position: the pattern's executor (the body); g/cut/* find the player and their own marker (rlk_hr_cut, by s)."""
    assert lock == strike - LOCK_LEAD and strike - made >= TELL_MIN and made <= lock, (made, lock, strike)
    assert tier in DMG and int(count) in (0, 1)
    out = [(made, f'function {NS}g/cut/make {_macro({"s": strike, "t": strike - made, "dmg": DMG[tier], "kb": kb, "n": count})}')]
    out += [(t, f'function {NS}g/cut/aim {_macro({"s": strike})}') for t in range(made + 1, lock)]
    out.append((lock, f'function {NS}g/cut/lock {_macro({"s": strike})}'))
    return out


# FN-f (S1): mboss_lib.bars(on) -> one line, BARS_FNS[on]: 'function rlk:mboss/bars_off' (NEW: sets #mbBarOff mb 1,
# then runs the existing mboss/bars_hide) or 'function rlk:mboss/bars_on' (NEW: sets #mbBarOff mb 0, then runs the
# existing mboss/bars_show); mboss/world skips mboss/bars while #mbBarOff is 1; fight_vars and cleanup_fight zero it.
# The existing mboss/bars_hide / bars_show (called by death_start, pause_tick, cleanup_fight, init, main, tick, start_go,
# mboss/bars) stay byte-identical: the flag must never be set by them, or a death pause would leave every boss's bars
# hidden for the rest of its fight (mboss/bars, the only re-show, is skipped while the flag is 1). The module never
# touches the framework-private #mbBar.
BARS_FLAG = ('#mbBarOff', 'mb')
BARS_FNS = ('function rlk:mboss/bars_off', 'function rlk:mboss/bars_on')


def bars(on):
    """The FN-f line (bars off in CS1, back in SQ1); '' until S1's mboss_lib.bars exists."""
    return L.bars(int(on)) if hasattr(L, 'bars') else ''


def actor_ready():
    """True once lane H3's actor exists (tools/player_motion/cine/manifest.json): then the actor lines are real."""
    return ACTOR_MANIFEST.exists()


def actor(call, **macro):
    """An actor line of hr_design §5.3 (`function rlk:char/cine/<call>` + its macro args; spawn / tick run as the player),
    '' until actor_ready(). play takes clip=<an ACTOR_CLIPS id>, face takes yaw=<degrees>."""
    assert call in ACTOR_CALLS and sorted(macro) == sorted(ACTOR_CALLS[call]), (call, macro)
    if call == 'play':
        assert macro['clip'] in ACTOR_CLIPS, macro
    if not actor_ready():
        return ''
    args = ('{' + ','.join(f'{k}:"{v}"' if isinstance(v, str) else f'{k}:{L.num(v)}' for k, v in macro.items()) + '}') if macro else ''
    return f'function rlk:char/cine/{call}' + (f' {args}' if args else '')


def actor_clock():
    """The line that hands the sequence clock to the actor (`#cavT cine` = `#sq hr`); '' until actor_ready()."""
    return f'scoreboard players operation {ACTOR_CLOCK[0]} {ACTOR_CLOCK[1]} = #sq {OBJ}' if actor_ready() else ''


def cam_ready():
    """True once the framework has FN-cam (lane H2: tools/build_mboss_core.py reads #mbCam)."""
    f = _TOOLS / 'build_mboss_core.py'
    return f.exists() and CAM_REQ[0] in f.read_text(encoding='utf-8')


def cam_req(cam=None):
    """The camera-lock request of this tick (`#mbCam mb 1`; with cam 1 / 2 also the live camera `#mbCamId mb`); '' until
    cam_ready()."""
    assert cam in (None, 1, 2), cam
    if not cam_ready():
        return ''
    out = f'scoreboard players set {CAM_REQ[0]} {CAM_REQ[1]} 1'
    return out if cam is None else [out, f'scoreboard players set {CAM_ID[0]} {CAM_ID[1]} {cam}']


def music(ph):
    """The registry music of phase ph (1 P1, 2 P2, 3 the ending; 0 stops): mboss_lib.music."""
    assert int(ph) == 0 or str(int(ph)) in BOSS['music'], ph
    return L.music(int(ph))


# FN-a / FN-b / FN-c (S1, PLAN §7.1.3-7.1.5): the registry fields S1 adds (with their validation) and the literal hook
# line in mboss/sp/reward for an enabled entry with rwHook.
FN_FIELDS = {'winWord': '도전 성공', 'rwHook': True, 'poof': False}
WIN_WORD = FN_FIELDS['winWord']
RW_HOOK_LINE = f'execute if data storage rlk:mboss cur{{id:"{ID}"}} as @a[tag=player,limit=1] run function {NS}reward'

# ---------------------------------------------------------------------------------------------
# 9b. PLAN §7: reward -> event -> item -> buff (frozen names; S3 reward.py writes ev/** + reward, S2b seq/event stages
# the coda, SR hand-writes the item and the buff)
EVENT = {'item_pm': 500,           # per mille for the item branch (written as a literal: regenerate to change)
         'buff_scope': 'run',      # 'run' (reset by player/reset_one) | 'forever' (question 1, PLAN §7.5.3)
         'item_enh': 1,            # the granted star (1 = ★☆☆; 0 = the pack's usual ☆☆☆)
         'lines': True,            # the coda's typed lines 24 / 25 (False = a wordless coda)
         'len': 120}               # the coda E0-E120 after H
EV_T = {'line': 4, 'line_clear': 52, 'present': 12, 'toss': 30, 'leave': 34, 'hide': 40, 'arrive': 42, 'beam': 44,
        'grant': 56, 'black': 110, 'end': 120}      # coda E-ticks (PLAN §7.3.2)
assert BOSS['death'] == END_H[END_PROFILE] + EVENT['len'] + 2
EV_BRANCH = {'none': 0, 'item': 1, 'buff': 2}       # #hrEv hr
EV_FP = ('#hrEv', '#hrEvDone', '#hrEvDrop')         # objective OBJ; not touched by cleanup; cleared by the reward hook,
#                                                     spawn and uninstall
EV_FORCE = 'ev.force'                               # storage rlk:hr: "item" | "buff" (tests 91 / 92; 90 removes it)
EV_TEST_IDS = {90: None, 91: 'item', 92: 'buff'}
EV_CALLS = ('ev/roll', 'ev/apply', 'ev/item', 'ev/buff', 'ev/title', 'ev/record', 'ev/reset')
REWARD_HOOK = 'reward'                              # F:boss/scarlet/reward (FN-b), @s = the player, not positioned
ITEM_ID = 'sword_hwamu'                             # rlk:items registry id (SR); score it_sword_hwamu
ITEM_NAME = '화무십일홍'
ITEM_SCORE = 'it_sword_hwamu'
ITEM_VANILLA = 'minecraft:iron_sword'
BUFF_OBJ = 'hrMoon'                                 # per player: 0 none, 1 on (SR: load / uninstall / reset_one)
BUFF_NAME = '월하대작'
BUFF_FP = ('#hrMoonAtk', '#hrMoonCrit', '#hrMoonSpd')   # objective tmp, set in load's 조절 지점 (SR)
BUFF_VALUES = {'run': (27, 10, 10), 'forever': (8, 4, 4)}   # ampAtk / critChance / moveSpeed for each scope
# S5 (11-06, the measured balance pass; PLAN §7.5.4 / §7.6 G3): the run buff's final ATK 20 -> 27 (B1 within +-5 % of the item
# at ★★ net: x0.976 mid / x1.032 late on the probe's fight rates); crit / move and the forever values unchanged.
ITEM_SND = tuple(f'f{i}' for i in range(422, 430))  # F:snd/f422-f429 with keys #k352-#k359 (SR)
# F3 (HR-33 / HR-35 / HR-11): the texts as rendered with the default constants (run scope, 27 / 10 / 10; item at ★☆☆). The
# coda's 4x item title is the name + the item's own stars (<= 106 font px; the stars are read from rlk:items at run time) with
# 「[ MYTHIC ]」 on the subtitle; the buff's numbers are score components of BUFF_FP: the first two on the subtitle (<= 192 font
# px), the third on the actionbar for the same 54 t; the rift chat record names the full display name / all three numbers with
# the scope words of EVENT['buff_scope'] (BUFF_SCOPE_WORDS; the stat line's word follows load's #hrMoonRun).
EV_TEXT = {'line_item': '조심하게. 칼자루를 쥐었다고 그 검의 주인이 되는 것은 아니니.',
           'line_buff': '한잔할 텐가? 안주는 달빛과 바람일세.',
           'item_title': '화무십일홍 ★☆☆',
           'item_sub': '[ MYTHIC ] 신화 아이템을 얻었습니다',
           'item_name': '[ MYTHIC ] 화무십일홍 ★☆☆',
           'buff_title': '월하대작',
           'buff_stats': '최종 공격력 +27% · 치명타 확률 +10% · 이동 속도 +10%',
           'buff_sub': '최종 공격력 +27% · 치명타 확률 +10%',
           'buff_ab': '이동 속도 +10%',
           'return_title': '홍련 도전 성공',
           'return_sub': '레벨 업 · 아이템 상자 1개',
           'chat_item': '[월하의 선물] 신화 아이템 ',
           'chat_buff': '[월하의 선물] 월하대작 — 이번 런 동안 최종 공격력 +27% · 치명타 확률 +10% · 이동 속도 +10%',
           'chat_full': '[월하의 선물] 보유 칸이 가득 차서 화무십일홍을 발밑에 놓았습니다.',
           'chat_test': '[특수 보스 테스트] 도전 성공! 균열 자리에 아이템 상자가 떨어졌습니다(누르면 아이템 선택). [다시 하기] [로비로]',
           'status': '☾ 월하대작 · 최종 공격력 +27% · 치명타 확률 +10% · 이동 속도 +10% (이번 런)'}
BUFF_SCOPE_WORDS = {'run': ('이번 런 동안', '이번 런'), 'forever': ('영구히', '영구')}   # (the rift chat line, the stat line)
EV_CHAT_BUFF_HEAD = '[월하의 선물] 월하대작 — '
assert EVENT['buff_scope'] in BUFF_SCOPE_WORDS
assert EV_TEXT['chat_buff'] == f"{EV_CHAT_BUFF_HEAD}{BUFF_SCOPE_WORDS['run'][0]} {EV_TEXT['buff_stats']}"
assert EV_TEXT['buff_stats'] == f"{EV_TEXT['buff_sub']} · {EV_TEXT['buff_ab']}"
assert EV_TEXT['status'] == f"☾ {BUFF_NAME} · {EV_TEXT['buff_stats']} ({BUFF_SCOPE_WORDS['run'][1]})"
assert EV_TEXT['item_name'] == f"[ MYTHIC ] {EV_TEXT['item_title']}" and EV_TEXT['item_title'].startswith(ITEM_NAME + ' ')


def reward_ready():
    """True once S3's reward.py has its services (the D0 stub has SERVICES = [])."""
    try:
        from mboss_scarlet import reward as _R
    except ImportError:
        return False
    return bool(getattr(_R, 'SERVICES', None))


def ev_apply():
    """The coda's grant line at E56 (seq/event, S2b): '' until reward_ready()."""
    return f'function {NS}ev/apply' if reward_ready() else ''


def ev_title():
    """The coda's event title line at E56: '' until reward_ready()."""
    return f'function {NS}ev/title' if reward_ready() else ''

# =============================================================================================
# Self-checks (pure data, run at import) and the full check (--check)


def _check_scripts():
    for key, rows in SCRIPTS.items():
        ts = [r[0] for r in rows]
        assert ts == sorted(ts) and ts[0] == 0, f'{key}: rows out of order'
        for t, step, clip, c in rows:
            assert clip is None or clip in CLIPS, (key, step, clip)
            if c:
                made, lock, strike, tier, kb = c
                cut(made, lock, strike, tier, kb)                     # lock = strike - 7, made >= 12 t before
                hits = [r for r in rows if r[2] and 'hit' in CLIPS[r[2]][2] and r[0] + ev(r[2], 'hit') == strike]
                assert len(hits) == 1, f'{key}: cut {c} strikes on no / several move contacts'
    for g, n in (('a8', 9), ('a13', 11)):
        cuts = [r[3] for r in SCRIPTS[g] if r[3]]
        assert len(cuts) == len(CUT_IDS[g]) == n and all(c[3:] == _TC for c in cuts), g    # F1 (HR-19): tier TC, kb 0
        strikes = [c[2] for c in cuts]
        assert all(b - a >= CUT_GAP_MIN for a, b in zip(strikes, strikes[1:])), (g, strikes)
        dive = [r for r in SCRIPTS[g] if r[2] == 'g_dive']
        assert len(dive) == 1 and dive[0][0] + ev('g_dive', 'hit') == JUDGE_T[g] == REPEL_T[g] == SCRIPTS[g][-1][0], g
        assert all(0 < t <= JUDGE_T[g] for t in BOLTS[g]) and len(BOLTS[g]) == 4
    assert FAIL5_T['slash'] == JUDGE_T['a13'] and FAIL60_REFORM_T == JUDGE_T['a8'] < FAIL60_P2_T
    # hr_design §2.1: every pattern ends 8-12 t after its last hit, inside its clip (a4: after its landing)
    for key, end in PAT_END.items():
        hs = [h for i, h in enumerate(HITS[key]) if HIT_PH.get(key, {}).get(i) is None]
        last = max(ev(c, e) for c, e, *_r in hs)
        assert 8 <= end - last <= 12 and last < end < CLIPS[hs[-1][0]][0], (key, end)
    for fp, end in RINGS_END.items():
        assert end == max(ev(c, e) for i, (c, e, *_r) in enumerate(HITS['rings']) if HIT_PH['rings'].get(i, fp) == fp) + 10


def _check_contract():
    """The D0 self-checks (pure data)."""
    for k, (ln, lp, evs) in CLIPS.items():
        assert all(0 <= t < ln for t in evs.values()), f'clip {k}: an event outside 0..len-1'
        assert lp is None or 0 <= lp[0] < lp[1] <= ln, f'clip {k}: loop {lp}'
    for key, hs in HITS.items():
        assert key in P1 + P2, key
        for i, (clip, e, shape, dims, tier, kb, par) in enumerate(hs):
            assert clip in CLIPS and e in CLIPS[clip][2], f'HITS {key}: {clip}.{e}'
            assert tier in DMG and kb in (KB_CHAIN, KB_SINGLE, KB_FINAL) and par in ('P', 'N'), (key, tier, kb, par)
            assert shape in ('sector', 'disc', 'line', 'dash_line', 'pdisc', 'full'), (key, shape)
            # every N hit has its flash row (a group's other rows share it: ()), no P hit has one
            assert (i in FLASH_AT.get(key, {})) == (par == 'N'), f'HITS {key}[{i}]: the flash table and the P / N column differ'
        for i, fl in FLASH_AT.get(key, {}).items():
            h_t = ev(hs[i][0], hs[i][1])
            for col, clip, e, off in fl:
                t = ev(clip, e) + off
                assert col in FLASH and clip == hs[i][0], (key, i, col)
                if col == 'purple':
                    assert h_t - t == PURPLE_LEAD, f'{key}[{i}]: purple {t} -> {h_t}'
                if col == 'yellow':
                    assert h_t - t >= YELLOW_MIN, f'{key}[{i}]: yellow {t} -> {h_t}'
    _check_scripts()
    assert set(HITS) == set(P1 + P2), set(HITS) ^ set(P1 + P2)
    assert all(k in P1 + P2 for k in list(MID_MAX) + list(MID_MIN) + list(PAT_END) + list(DASH_BEYOND))
    for fp in (1, 2):
        assert all(k in WEIGHTS or k in TRIGGER_ONLY for k in FAR_RULE[fp]) and FAR_RULE['fallback'][1] in P1
    assert sorted(LINES) == list(range(1, 26)) and all(LINES.values())
    assert sorted(LINE_AT) == sorted(LINES), 'every line has a place'
    assert all(i in LINES and len(p) >= 2 and ' '.join(p) == LINES[i] for i, p in LINE_PAGES.items()), 'LINE_PAGES verbatim'
    for i, (where, t, hold) in LINE_AT.items():
        assert i in LINES and hold > 0
        if where in CLIPS:
            assert 0 <= t < CLIPS[where][0], (i, where, t)
            if f'l{i}' in CLIPS[where][2]:
                assert ev(where, f'l{i}') == t, (i, where, t)
        else:
            assert where == 'event' and t + hold <= EV_T['grant'], (i, where)
    for ph, (clip, e) in MUSIC_AT.items():
        assert e in CLIPS[clip][2], (ph, clip)
    keys = set(P1 + P2)
    assert {TEST_IDS[i] for i in LOCK_IDS} == keys - set(GAUNTLETS) and len(P1 + P2) == len(keys)
    assert not {11, 25, 31} & {i for i, v in TEST_IDS.items() if v in ('r1', 'down window', 'look dark on / off')}
    assert TEST_IDS[21].startswith('a8') and TEST_IDS[27].startswith('a13')
    assert set(TEST_HELP_NAMES) == set(TEST_IDS) and set(EV_TEST_IDS) <= set(TEST_IDS)
    assert set(WEIGHTS) | set(TRIGGER_ONLY) <= keys and set(COOLDOWN) <= keys and set(WEIGHTS) & set(TRIGGER_ONLY) == set()
    assert set(SEQ_CLIPS) == set(SEQS) == set(SEQ_LEN) and all(c in CLIPS for cs in SEQ_CLIPS.values() for c in cs)
    assert SEQ_LEN['intro'] == CLIPS['intro'][0] + CLIPS['intro_end'][0] <= BOSS['intro'] and SKIP_T == CLIPS['intro'][0]
    assert SEQ_LEN['ending'] == CLIPS['ending'][0] == END_H['std'] and SEQ_LEN['event'] == EVENT['len']
    for s in ('cs1', 'lead60', 'repel', 'lead5', 'lead_re'):
        assert SEQ_LEN[s] == CLIPS[s][0], s
    assert len(CINE_CLIPS) == 8 and len(EV_CLIPS) == 3 and sum(o == 'S2a' for o in CLIP_OWNER.values()) == 39
    assert sum(o == 'H1' for o in CLIP_OWNER.values()) == 12 and sum(o == 'H2' for o in CLIP_OWNER.values()) == 8
    # hr_design §3: the skips, the counter events, the contacts and the actor clips against the sequence table
    for name, sk in SKIP.items():
        assert name in SEQ_EXTRA and 'skip' in SEQ_EXTRA[name] and 0 < sk['window'][0] < sk['window'][1] < sk['to'] < SEQ_LEN[name]
    assert [ev('repel', e) for e in COUNTER_EV] == [49, 101, 129]
    assert SEQ_LEN['intro'] + 10 == BOSS['intro'] and set(STAGE_FMAX) <= set(SEQS)
    for cid, (sq, (t0, t1), pt, _what) in CONTACT.items():
        assert sq in SEQS and 0 <= t0 <= t1 <= SEQ_LEN[sq] and len(pt) == 3, cid
    assert ACTOR_CLIPS == {'cs0': SEQ_LEN['intro'], 'cs1': SEQ_LEN['cs1'], 'repel': SEQ_LEN['repel'],
                           'ending': SEQ_LEN['ending'], 'coda': SEQ_LEN['event']}
    # the new-combat constants (hr_design §1.2, §2.1)
    assert GAUGE['max'] == PIPS * GAUGE['seg'] and FLASH_SND.keys() == FLASH.keys()
    for _name, (_kit, _a) in list(FLASH.items()) + [('cue', CUE_KIT)]:
        assert sorted(_a) == sorted(KIT_PRESETS_PLAN[_kit]), _name
    assert CUE_SND in KIT_SOUND_RECIPES and all(v in KIT_SOUND_RECIPES for v in FLASH_SND.values())
    # ownership: output prefixes disjoint across stages; every §9.0-9.1 file exactly once
    flat = [(o, p) for o, ps in list(OWN.items()) + list(OWN_GEN.items()) for p in ps]
    for o1, p1 in flat:
        for o2, p2 in flat:
            assert o1 == o2 or not (p1.startswith(p2) or p2.startswith(p1)), f'OWN overlap {o1}:{p1} / {o2}:{p2}'
    for f in FILES_9_1:
        assert len(owners_of(f)) == 1, f'{f}: owners {owners_of(f)}'
    assert set(STAGE_BASE) == set(_OWN_FILES) - {'lead'}
    for pat, (first, then) in HANDOVER.items():
        assert any(p == pat for p, _ex in OWN_FILES[first]), f'hand-over {pat}: not listed under its creator {first}'
        assert STAGE_BASE[then] == f'wip/hr-{first.lower()}', f'hand-over {pat}: {then} does not branch from {first}'
    # FN-f: the module's bars lines are new wrappers, never the framework's own bars_hide / bars_show (PLAN FE-6)
    assert all(f.startswith('function rlk:mboss/bars_') and not f.endswith(('/bars_hide', '/bars_show')) for f in BARS_FNS)
    assert set(KIT_SOUND_RECIPES) == set(KIT_SOUNDS) and all(
        ev_.islower() and 0 < (v or 0) <= 1.0 and 0.5 <= p <= 2.0 for r in KIT_SOUND_RECIPES.values() for ev_, v, p in r)
    assert KIT_BASE_PRESETS == 50 and len(KIT_PRESETS_PLAN) == 56 and sum(k.startswith('ev_') for k in KIT_PRESETS) == 8
    assert set(KIT_PRESETS) <= set(KIT_PRESETS_PLAN) and not set(KIT_PRESETS_HR) & set(list(KIT_PRESETS_PLAN)[:KIT_BASE_PRESETS])
    assert sum(k.startswith('ev_') for k in KIT_SOUNDS) == 7
    assert sorted(OVERLAYS[k] for k in OVERLAYS_BASE) == list(range(0xEC10, 0xEC16)) and VIG == 0xEC16
    assert sorted(OVERLAYS_HR.values()) == [0xEC17, 0xEC18] and list(OVERLAYS_PLAN)[-2:] == ['gold', 'web']
    assert all(FONT_RANGE[0] <= c <= FONT_RANGE[1] for c in list(OVERLAYS_PLAN.values()) + [VIG])
    assert all(0 < t <= JUDGE_T[g] for g in GAUNTLETS for t in BOLTS[g])
    assert DARK_SLICES == tuple(DARK_SLICES[0] + 3 * i for i in range(4))    # the theme's dark look (never requested now)
    assert LOOKS['scabbard'][-1] == 'gone' and set(ARENA_LOOKS) == set(LOOK_ID)
    assert xyz((884.0, 201.0, -5.0)) == '884.0 201 -5.0' and xyz((880.5, 200.9, 31.25)) == '880.5 200.9 31.25'
    return True


_check_contract()


def check():
    """--check: the D0 self-checks + check_manifest on the stub and on the manifest in use + the vanilla sound ids."""
    _check_contract()
    check_manifest(json.loads(STUB_MANIFEST.read_text(encoding='utf-8')))
    assert json.loads(STUB_MANIFEST.read_text(encoding='utf-8')) == json.loads(json.dumps(stub_manifest())), \
        'stub_rig_manifest.json is stale: api.py --write-stub'
    rig_manifest()
    ids_file = _TOOLS / 'dev/sim/rd/tests/sound_ids.txt'
    if ids_file.exists():
        ids = set(ids_file.read_text(encoding='utf-8').split())
        bad = sorted({e for r in KIT_SOUND_RECIPES.values() for e, _v, _p in r} - {i.split(':', 1)[1] for i in ids})
        assert not bad, f'not vanilla sound ids: {bad}'
    return True


if __name__ == '__main__':
    if '--write-stub' in sys.argv:
        STUB_MANIFEST.write_text(json.dumps(stub_manifest(), ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print('wrote', STUB_MANIFEST)
    if '--check' in sys.argv:
        check()
        ev_n = sum(len(v[2]) for v in CLIPS.values())
        print(f'scarlet api: {len(PARTS)} parts + shadow, {len(CLIPS)} clips ({ev_n} events), {len(HITS)} hit tables, '
              f'{len(LINES)} lines, {len(KIT_PRESETS)} presets, {len(KIT_SOUNDS)} sounds, {KIT_SPRITE_PX} kit px, '
              f'{len(FILES_9_1)} owned paths: ok')

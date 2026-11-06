"""Frozen D0 contract of the 홍련 (Scarlet, special boss) module generator: every stage (S1 framework FN-a/b/c/f, S1K
kit + arena hr_field, S2a rig, S2b cinematic clips + sequences, S3 core / AI / P1 / shield / event logic, S4 ghost
patterns, SR the reward item + buff hand files) imports this file and never edits it. A change goes through a request
(S:hr/requests/<stage>.md) applied by the lead at integration (I1). Prose version: S:hr/contract.md; design:
S:hr/PLAN.md (section numbers below refer to it; §9.0 lists what this file freezes, §9.2 the stage contracts).

Importing has no side effects (no files written); it asserts the contract's own consistency (pure data: clip events
inside their clips, HITS / scripts / LINE_AT against CLIPS, the §9.1 ownership exactly once, the kit sprite budget).
Units: Python helpers take blocks / ticks / degrees; the framework boundary is tenths of a block and % of the base hit
(atk 12 x dmgMul 135: raw = floor(0.162 x pct)).
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
assert (BOSS['picks'], BOSS['lvup'], BOSS['xp'], BOSS['intro'], BOSS['death']) == (1, 1, 0, 650, 1164), 'PLAN §8'
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
DMG = {'T1': 29, 'T2': 42, 'T3': 62, 'T4': 71}         # % of the base hit (mboss/hurt coefficient); 타키's final tiers
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
# HITS[key] = [(clip, event, shape, dims, tier, kb)] (blocks; tier a DMG key). Shapes (framework mboss/hz/*, pj/launch):
#   sector(r, half_deg) round her; disc(r) round her; line(len, w) ahead of her; dash_line(w) along her dash (length = the
#   dash); pdisc(r) = a disc at the player's spot, locked at the clip's lock event (A9) or, for the cut builder (cut()),
#   following the player until strike - LOCK_LEAD; pj_disc(hr, speed, life) = the moon disc (DISC, disc()).
# Every hit Electro 1U, #hzQuiet 1, no floor decal (PLAN §1.4). The a8 / a13 / r1 / r2 / r3 entries are derived from the
# scripts of section 3 by _script_hits (section 7): each cut lands on the move whose clip 'hit' meets its strike tick.
HITS = {
    'a1': [('a1', 'hit', 'sector', (4.0, 80), 'T2', KB_SINGLE)],
    'a2': [('a2', 'hit', 'sector', (3.6, 70), 'T2', KB_SINGLE)],
    'a3': [('a3', 'h1', 'sector', (4.2, 90), 'T1', KB_CHAIN), ('a3', 'h2', 'sector', (4.0, 60), 'T1', KB_CHAIN),
           ('a3', 'h3', 'sector', (4.0, 50), 'T1', KB_CHAIN), ('a3', 'h4', 'line', (5.0, 1.8), 'T1', KB_CHAIN),
           ('a3', 'h5', 'sector', (4.6, 70), 'T2', KB_FINAL)],
    'a4': [('a4', 'hit', 'disc', (2.6,), 'T3', KB_CHAIN), ('a4', 'hit2', 'disc', (3.0,), 'T1', KB_SINGLE)],   # A4 + A5
    'a6': [],                                                                                              # no hit
    'a9': [('a9', 'cut', 'dash_line', (2.4,), 'T3', KB_FINAL), ('a9', 'cut', 'pdisc', (4.0,), 'T3', KB_FINAL)],  # 1 group
    'a10': [('a10', 'hit', 'disc', (3.5,), 'T3', KB_FINAL)],
}
CUT_R = 3.2               # damage radius of a counting / ghost cut (the visible ring ~2.2; knob 2.8-3.6, PLAN §4.8)
CUT_SHOW_R = 2.2
LOCK_LEAD = 7             # aims lock 7 t before the hit
TELL_MIN, TELL_BIG, COMBO_GAP = 12, 20, 10   # first visible motion -> hit >= 12 t; big / undodgeable / yellow >= 20 t;
#                                              chain hits >= 10 t apart (README 0-6 10-20)
MOVE_R = SAFE - 0.5       # 22.5: every end point (landing, dash end, blink, reappear) via mv/ok + leash inside it
assert MOVE_R == 22.5
FALLBACK_R = 21.0         # the guaranteed last reappear / landing point: on the player -> C line, <= 21 b from C
# the A7 moon disc (R2, A13): pj/launch blade shape (#pjShape 1), half width hr, height y0-y1 over the floor (a jump does
# not clear it), speed b/t, life t, wall stop, aimed at its lock (the player's floor spot LOCK_LEAD t before the release,
# DISC_LOCK; F1 HR-15; no homing), one kit card
# (fx/prop/disc, horizontal, spinning 30 deg/t, facing its flight; summoned, then rotated), tier T2, never counts for pips
# I1 (request s4-2): speed 1.75 = exactly 7 of the framework's 0.25 b sub-steps (mboss_lib.pj_speed_tenths rounds up, so
# the frozen 1.8 flew 8 = 2.0 b/t); PLAN's "≈ 7 t from 12 b" (12 / 1.75 = 6.9 t).
DISC = {'hr': 1.4, 'y0': 0.2, 'y1': 2.4, 'speed': 1.75, 'life': 16, 'shape': 1, 'spin': 30, 'tier': 'T2', 'kb': 0,
        'kb_last_r2': 2}
TRACK = {'deg': 10, 'step': 0.3, 'min': 2.4}   # chains: re-aim <= 10 deg/t + a 0.3 b step before each hit (stop at 2.4 b)
DASH_LEN = {'a9': 12.0, 'a6': 12.0, 'cs1_lunge': 20.0}   # max dash / glide lengths (b): A9 iai dash, A6 back-blink
LEAP_H = {'a4': 6.0, 'a10': 5.0}                         # leap heights (b): A4 rises 6 b in 4 t, A10 springs 5 b
A4_TRAVEL, A10_DRIFT = 10.0, 0.4                          # A4 travels <= 10 b toward the player; A10 drifts <= 0.4 b/t
A9_BEYOND = 3.0                                           # A9 dashes through the locked point to 3 b beyond (<= 12 b)
A3_GLIDE = (8.0, 0.3, 14)                                 # A3 from 4.5-8 b: glides in 0.3 b/t during ticks 0-14
RECOVER = {1: (8, 16), 2: (10, 16)}                       # idle between patterns (min, max) per fight phase P1 / P2
# F1 (HR-13 / HR-14 / HR-18, the P1 pressure package, lead decision 11-05; PLAN §4.1 wins over §4.3's clip tails): every
# P1-kit pattern ends 8-12 t after its last hit instead of at its clip's end (the clip's follow-through plays on while she
# turns to the player; the AI recovery's walk / strafe takes over: the punish window); RECOVER above = the §4.8 knob
# (P1 16-24 -> 12-20, P2 12-18 -> 10-16); S5 (11-06, the measured balance pass): P1 12-20 -> 8-16 (the knob's -4 t; T1).
# A6 (no hit) keeps A6_TRIGGER['next'].
PAT_END = {'a1': 24, 'a2': 22, 'a3': 79, 'a4': 46, 'a9': 40, 'a10': 32}
# F1 round 1 (HR-14, the decision's "during any tail kept ... she walks / strafes facing and tracking the player"): a kept tail
# lets the clip's follow-through play TAIL_MOVE t after the last hit / release (A4: until it lands; R1 / R3: until the solid
# row), then she moves as in the recovery (ai/tail: the recovery's move and clip, ai/tail_step each later tick) while she
# turns to the player; the recovery after it keeps that move (ai/tail_keep).
TAIL_MOVE = 4
WALK_SPEED, GLIDE_SPEED = 0.12, 0.18                      # recovery walk / strafe (P1) and the P2 glide, b/t

# =============================================================================================
# 3. Phases, floors, pips, the gauntlet scripts, switches (PLAN §3, §4.4-4.6, §5)
PH = {'intro': 0, 'p1': 1, 'cs1': 2, 'sq1': 3, 'a8': 4, 'cs2': 5, 'down': 6, 'p2': 7, 'lead': 8, 'a13': 9, 'cs3': 10,
      'death': 11}        # #ph hr (S3 may keep finer state in its own fake players)
FLOOR_P1 = 600            # per mille of mhpM: the hit reaching it stops there; CS1 at the next decision
FLOOR_ULT = 50            # per mille: the 5 % floor (set at CS1 0); A13 at the next decision (40 t later from the down)
PIPS = 5
PIP_RULE = 'timed_dash'   # PLAN §5.1: at the strike tick s a pip goes when dashInvT is 1..6 (at s + 1: 1..5) and the
PIP_DASH = {0: (1, 6), 1: (1, 5)}   # player's feet are within PIP_R of the cut's lock point; one per cut, any direction
PIP_R = CUT_R + 3.0       # 6.2
BU_SHIELD, BU_DOWN = 1, 8  # under-bar colours (#buSubCol): electro for the shield (max 5), gold for the down timer (max 200)

# Gauntlet scripts (PLAN §4.4-4.5 tables as tuples). Rows (t, step, clip, cut): t = the clip's start on the pattern clock
# T+ (T0 = the gauntlet's start), or the step's tick when clip is None; cut = (made, lock, strike, tier, kb) of the cut
# hazard made at that step (api.cut), else None. Rows with t < 0 are played by SQ1 / the lead-ins (S2b), not by the
# pattern. A move's contact = t + ev(clip, 'hit') = the strike of the cut made one step earlier.
_T2, _T3 = ('T2', KB_CUT), ('T3', KB_FINAL)
_TC = ('TC', KB_CUT)      # F1 (HR-19): the counting cuts of A8 / A13 (DMG['TC'])
A8_SCRIPT = (
    (-17, 'dark', None, None),                    # first real slice of the `dark` look job (called at -18)
    (-14, 'brim', 'g_brim', None),                # SQ1 46: the right hand to the brim
    (0, 'A8.T', 'g_tell', None),
    (14, 'D1', 'g_dash', (14, 20, 27) + _TC),     # cut 1
    (24, 'A8.1', 'g_ring', (27, 33, 40) + _TC),   # cut 2
    (31, 'A8.2', 'g_rise', (40, 48, 55) + _TC),   # cut 3
    (46, 'A8.3', 'g_leap', None),                 # vanishes in the air 62
    (70, 'D2', 'g_glide', (70, 75, 82) + _TC),    # cut 4
    (79, 'A8.4', 'g_sweep', (82, 87, 94) + _TC),  # cut 5
    (88, 'A8.5', 'g_x', None),                    # vanishes 103
    (108, 'D1', 'g_dash', (108, 114, 121) + _TC),  # cut 6
    (118, 'A8.1', 'g_ring', None),
    (130, 'D3', 'g_drop', (130, 140, 147) + _TC),  # cut 7
    (144, 'A8.6', 'g_wrap', (147, 152, 159) + _TC),  # cut 8
    (156, 'A8.7', 'g_dome', (159, 167, 174) + _TC),  # cut 9
    (169, 'A8.8', 'g_vert', None),                # pink glow 170-173, rises out of view, hidden 186
    (188, 'A8.9', 'g_dive', None),                # reappears 188 in normal colours, dives; judge at 194
    (194, 'judge', None, None),                   # darkness lifts (crimson, slices 194-197); success g_deflect -> CS2 206;
)                                                 # fail §5.5: g_reform 194-204, P2 decision at 214
A13_SCRIPT = (
    (-17, 'dark', None, None),                    # lead-in: darkness, the hand to the brim, the warning banner (ULT5_LETHAL)
    (0, 'A8.T', 'g_tell', None),
    (14, 'D1', 'g_dash', (14, 20, 27) + _TC),     # U1
    (24, 'A8.1', 'g_ring', (27, 33, 40) + _TC),   # U2
    (31, 'A8.2', 'g_rise', (40, 48, 55) + _TC),   # U3
    (46, 'A8.3', 'g_leap', None),                 # vanishes in the air 62
    (67, 'D1', 'g_dash', (67, 73, 80) + _TC),     # U4
    (77, 'A8.1', 'g_ring', None),                 # vanishes 89
    (96, 'D2', 'g_glide', (96, 101, 108) + _TC),  # U5
    (105, 'A8.4', 'g_sweep', (108, 113, 120) + _TC),  # U6
    (114, 'A8.5', 'g_x', None),                   # vanishes 128
    (127, 'tell', 'a7_tell', None),               # reappears 3 b away inside the yellow tell 129-137, retreats to 12 b
    (143, 'disc1', 'a7_throw', None),             # gold blade line 150-154; release 155 -> at the player ~162
    (155, 'disc2', 'a7_throw', None),             # release 167 -> ~174
    (168, 'disc3', 'a7_throw', None),             # release 180 -> ~187
    (194, 'vanish', None, None),                  # stands far 187-194; vanish 5 (purple glow + white ring)
    (198, 'D4', 'g_run', (198, 204, 211) + _TC),  # U8
    (208, 'A8.6', 'g_wrap', (211, 216, 223) + _TC),  # U9
    (220, 'A8.7', 'g_dome', (223, 231, 238) + _TC),  # U10
    (233, 'A8.8', 'g_vert', None),                # pink glow 234-237; rises, hidden 250
    (252, 'A8.9', 'g_dive', None),                # reappears 252 in normal colours, dives; judge at 258
    (258, 'judge', None, None),                   # success: darkness lifts, g_deflect -> CS3 270; fail: the instant death
)
# P2 entries cut from the gauntlets' moves (PLAN §4.4; no shield, no darkness): same row form, cuts never count. The
# 'solid' row is when the ghost tag (rlk_hr_ghost, hence rlk_mb_inv) goes and she is hittable again (PLAN: R1 "hittable
# at 62", R3 "reforms 37-46"), not the g_reform clip's own visual 'solid' event (its tick 4).
R1 = (
    (0, 'A8.T', 'g_tell', None),                  # lilac switch 0 (form ghost, rlk_mb_inv), burst 3, hidden 4
    (14, 'D1', 'g_dash', (14, 20, 27) + _T2),     # reappears 14 b front-left, dashes 20-24 to 1.5 b at the player's right
    (24, 'A8.1', 'g_ring', (27, 33, 40) + _T2),
    (31, 'A8.2', 'g_rise', (40, 48, 55) + _T3),   # the last hit T3 kb 3 (she leaps over the player)
    (46, 'A8.3', 'g_leap', None),
    (55, 'reform', 'g_reform', None),             # lands 3 b beyond the player and reforms 55-62
    (62, 'solid', None, None),                    # hittable again
    (67, 'end', None, None),                      # F1 (HR-14): 12 t after the last hit (was 76; the reform tail <= 12 t)
)
R2 = (
    (0, 'tell', 'a7_tell', None),                 # a step back 0, yellow tell 2-10, retreats 6 b (4-14), settles 14
    (16, 'throw', 'a7_throw', None),              # release 28: one disc aimed at its lock (F1 HR-15: the player's spot at 21)
    (30, 'throw2', 'a7_throw', None),             # only at <= R2_TWO_PCT HP: release 42 (aimed anew: its lock at 35)
    (60, 'end', None, None),
)
R2_TWO_PCT = 30
R3 = (
    (0, 'A8.T', 'g_tell', None),
    (10, 'D2', 'g_glide', (10, 17, 24) + _T2),    # reappears low 8 b at the player's front-right (+55), glides to 1.6 b +45
    (21, 'A8.4', 'g_sweep', (24, 30, 37) + _T3),  # hit1 24, springs up and hangs turning 24-32; hit2 37 = the X, T3 kb 3
    (31, 'A8.5', 'g_x', None),
    (37, 'reform', 'g_reform', None),             # reforms 37-46
    (46, 'solid', None, None),
    (49, 'end', None, None),                      # F1 (HR-14): 12 t after the last hit (was 60; the reform tail <= 12 t)
)
SCRIPTS = {'a8': A8_SCRIPT, 'a13': A13_SCRIPT, 'r1': R1, 'r2': R2, 'r3': R3}
GAUNTLETS = ('a8', 'a13')
CUT_IDS = {'a8': ('1', '2', '3', '4', '5', '6', '7', '8', '9'),
           'a13': ('U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U8', 'U9', 'U10')}
DISC_RELEASE = {'a13': (155, 167, 180), 'r2': (28, 42)}   # = row t + ev('a7_throw', 'release'); arrival ~ +7
# F1 (HR-15, lead decision 11-05): each disc's aim locks LOCK_LEAD t before its release: a floor marker at the player's feet
# (rlk_hr_lock + the pattern tags, as p1's lock_fn), she turns to it, g/disc/throw aims at it: lock -> hit = 7 t + the flight.
DISC_LOCK = {k: tuple(t - LOCK_LEAD for t in v) for k, v in DISC_RELEASE.items()}
BOLTS = {'a8': (34, 102, 161, 193), 'a13': (70, 225, 245, 258)}   # deco_bolt 3-6 b from the player (no hit), T+
JUDGE_T = {'a8': 194, 'a13': 258}
REPEL_T = {'a8': 206, 'a13': 270}                 # seq/repel {at:60 | 5} after g_deflect
DARK_T, DARK_CALL_T, BRIM_T = -17, -18, -14       # T+ of the dark job's first slice / its call / the hand to the brim
#                                                   in SQ1 (A8: sq1 'brim' 46); the lead-ins raise it at DARK_T (A13)
DARK_SLICES = (-17, -14, -11, -8)                 # the `dark` job's four real slices land 3 t apart (PLAN §6.6)
# Reappear geometry (S4's g/**), relative to the player's facing (+ = right), blocks / degrees (PLAN §4.5)
# F1 (HR-27, lead decision 11-05): D2 / D4 at +-55 deg (was +-80): inside the default F5 view near its edge, as the footage
# shows them (camera 3.5 b behind the player, FOV 70: half-width 51.2 deg at 16:9, 48.2 at 16:10; D2 8 b at 39.0 deg off
# the camera axis, D4 12 b at 43.4 deg), so the approach is seen from the reappearance on.
REAPPEAR = {
    'D1': {'dist': 14.0, 'bearing': -40, 'fallback': (40, 0, 90, -90), 'fallback_dist': 10.0, 'end': (1.5, 90)},
    'D2': {'dist': 8.0, 'bearing': 55, 'end': (1.6, 45)},
    'D3': {'dist': 2.5, 'up': 3.0, 'bearing': 60},
    'D4': {'dist': 12.0, 'bearing': -55},
    'A8.9': {'up': 6.0},
    'tell': {'dist': 3.0, 'retreat': 12.0},
}
DOWN_T = 200              # the down window after CS2 (normal damage, the under bar = ticks left, gold)
DOWN_FLOOR_WAIT = 40      # the hit reaching the 5 % floor in the down window -> lead_down 40 t later
KIPUP_T, KIPUP_RECOVER = 20, 12   # the down's natural end: kipup (invulnerable) -> P2 decisions after 12 t
# The counter cinematic's scripted HP steps (true damage, per mille of mhpM via mboss/true_hit, at repel events
# COUNTER_EV): repel {at:60} three steps (-4.5 %), repel {at:5} two steps then the lethal true hit (true_pct 100) at
# 'kick'. PLAN §3.4 / §4.6 / §4.8 give 15, 15 at 5 % (-3 %, the footage 5.2 -> 2.3 %); §9.0's "(10, 10, 'kill')" is
# superseded (contract change log).
COUNTER_PM = {60: (15, 15, 15), 5: (15, 15, 'kill')}
COUNTER_EV = ('flash', 'land', 'kick')            # repel 24 / 75 / 102
FAIL60_PM = 500           # A8 fail (ULT60_LETHAL false): pl_dot 500 per mille, #mbDotLethal 0 (cannot kill) + a push
FAIL60_PUSH = (2.5, 3)    # mboss_lib.push_ring(2.5, 3) at the impact point, the same tick
FAIL60_REFORM_T, FAIL60_P2_T = 194, 214           # g_reform 194-204 (she lands 2 b from the player), P2 decision at 214
FAIL5_T = {'reappear': 252, 'black': 255, 'slash': 258}   # the instant-death staging (ovl black 255-258, pinkwhite +
#                                                           scarlet_line + ult/fatal at 258)
REVIVE = {'dist': 8.0, 'wait': 60}                # after a Ronova revive: she stands 8 b away; 60 t later lead_stand a13
# Switches (PLAN §0.1 questions 5-7; each one value here, the default the build proceeds with)
ULT60_LETHAL = False      # A8 fail = the 500 per-mille hit (True: the instant death + the banner)
ULT5_LETHAL = True        # A13 fail = the instant death (ult/fatal; Ronova's revive applies) + the banner
DARK_LIGHT = True         # the `dark` look dims the walk light layer (False: fallback B, dome / moon / lanterns only)
WARN_TEXT = '대시로 베기를 아슬아슬하게 피해 실드를 모두 깎으세요 — 실드가 남으면 즉사합니다'
WARN_HL = ('즉사', '#FF3A55')   # bossbar rlk:hr_warn: white text, this word crimson; only while a lethal gauntlet runs
END_PROFILE = 'std'       # CS4 profile (question 7); only std is built: short (~600 t) / full (~1500 t) = a request
END_H = {'std': 1042}     # CS4 length H (= clip `ending`); registry death = H + EVENT['len'] + 2
INTRO_SKIP = True         # hold sneak SKIP_HOLD t at any tick in SKIP_WINDOW -> black -> jump to SKIP_T (intro_end)
SKIP_HOLD, SKIP_T, SKIP_WINDOW = 20, 554, (20, 540)
SKIP_TEXT = '⊙ 건너뛰기'      # the original's prompt, verbatim (actionbar, hudHold)
SKIP_HINT = ' · Shift 길게'      # the pack's control hint after it
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
MID_MAX = {'a3': 8.0, 'a9': 7.0}                 # these use their mid weight only up to this distance
# WEIGHTS[key][fight phase 1 = P1 / 2 = P2] = (near, mid, far); renormalised over the entries off cooldown and allowed
# F1 (HR-13 / HR-18, the P1 pressure package, lead decision 11-05): no empty band - the P1 near band gets A10 (20, the
# yellow plunge on the locked spot) and small A1 / A2 weights (their 100-t cooldowns), so her near decision always has a
# move; a band still empty twice in a row -> the 12-t backstep, then the mid pick (ai/none, ai/backstep).
# S5 (11-06, the measured balance pass, HR-13/14/18 point 5's lever order): P1 near A9 25 -> 40 and A10 20 -> 40 (the two
# player-centred lock discs a walking player cannot side-step; T1).
WEIGHTS = {
    'a1': {1: (10, 0, 0)},
    'a2': {1: (10, 0, 0)},
    'a3': {1: (50, 15, 0), 2: (35, 10, 0)},
    'a4': {1: (0, 35, 40), 2: (0, 20, 20)},
    'a9': {1: (40, 10, 0), 2: (20, 10, 0)},
    'a10': {1: (40, 25, 35), 2: (0, 15, 20)},
    'r1': {2: (0, 20, 35)},
    'r2': {2: (0, 15, 25)},
    'r3': {2: (20, 25, 0)},
}
# F1 (lead decision 11-05): A9 P1 300 -> 160 (one full-screen flash per >= 8 s), A10 P1 260 -> 180, P2 = P1 x 0.85 rounded
# to 10 t as the other entries (A9 140, A10 150); A6 400 in both phases (HR-38). S5 (11-06): A10 P1 180 -> 120, P2 = x0.85
# -> 100 (A9 stays 160 / 140: one full-screen flash per >= 8 s, the lead's floor).
COOLDOWN = {'a1': {1: 100, 2: 85}, 'a2': {1: 100, 2: 85}, 'a3': {1: 120, 2: 100}, 'a4': {1: 160, 2: 140},
            'a6': {1: 400, 2: 400}, 'a9': {1: 160, 2: 140}, 'a10': {1: 120, 2: 100}, 'r1': {2: 220}, 'r2': {2: 260},
            'r3': {2: 200}}
TRIGGER_ONLY = ('a6',)                           # never picked by weight: the skill trigger (A1 / A2: the counter trigger,
#                                                  the rear rule and, F1, small P1 near weights)
FAR_RULE = {'dist': 8.0, 'dwell': 30, 1: {'a4': 60, 'a10': 40}, 2: {'r1': 40, 'a4': 30, 'r2': 30},
            'fallback': ('glide', 'a3')}         # also the decision 16 t after A6
REAR_RULE = {'deg': 60, 'dwell': (20, 30), 'key': 'a1', 'cd_ignore_every': 200}
NO_REPEAT = True                                 # no immediate repeat of an entry

# =============================================================================================
# 5. Keys, sequences, ownership, test ids, lines (PLAN §3.0, §9.0-9.2)
P1 = ('a1', 'a2', 'a3', 'a4', 'a6', 'a9', 'a10')    # S3: tools/mboss_scarlet/p1.py -> p/<key>/** (a4 includes A5)
P2 = ('r1', 'r2', 'r3', 'a8', 'a13')                # S4: tools/mboss_scarlet/p_ghost.py -> p/<key>/**
SEQS = ('intro', 'cs1', 'sq1', 'repel', 'lead_down', 'lead_stand', 'ending', 'event')   # S2b: seq.py -> seq/<name>/**
SEQ_CLIPS = {'intro': ('intro', 'intro_end'), 'cs1': ('cs1',), 'sq1': ('sq1',), 'repel': ('repel',),
             'lead_down': ('lead_down',), 'lead_stand': ('lead_stand',), 'ending': ('ending',),
             'event': ('ev_give', 'ev_toast', 'ev_leave')}
SEQ_ARGS = {'repel': {'at': (60, 5)}, 'lead_stand': {'g': ('a8', 'a13')}}   # macro args of seq/<name>/start
SEQ_EXTRA = {'intro': ('skip',)}                 # seq/intro/skip: the core calls it after SKIP_HOLD t of sneak
# A sequence never calls core functions: it signals the core through the score SEQ_SIGNAL (objective OBJ, S2b's #sq_
# prefix) = a SIG value in the tick of the beat; the core reads it right after seq/<name>/tick, applies it (an HP step:
# COUNTER_PM[at][i - 1] via mboss/true_hit, 'kill' = true_pct 100; refill: shield/arm) and resets it to 0.
SEQ_SIGNAL = '#sq_sig'
SIG = {'hp1': 1, 'hp2': 2, 'hp3': 3, 'refill': 4}   # repel: hp1-hp3 at COUNTER_EV; lead_down / lead_stand: refill
SEQ_LEN = {'intro': 640, 'cs1': 213, 'sq1': 60, 'repel': 104, 'lead_down': 82, 'lead_stand': 70, 'ending': 1042,
           'event': 120}
PATTERN_NAMES = {'a1': '회전 반월참', 'a2': '역습 일섬', 'a3': '오연 반월', 'a4': '월하 낙참 · 공중 원륜',
                 'a6': '후방 섬보', 'a9': '황광 원참', 'a10': '황광 낙참', 'r1': '자영 돌격', 'r2': '월륜 일섬',
                 'r3': '자영 활강', 'a8': '자영 연참', 'a13': '필살 · 자영 연참'}    # test/help only: no pattern
#                                                                                   name is ever shown in the fight
# boss/test/pattern {id:N} (PLAN §9.2); test/help lists TEST_HELP_NAMES; test/lock {id} for LOCK_IDS
TEST_IDS = {1: 'a1', 2: 'a2', 3: 'a3', 4: 'a4', 5: 'a6', 6: 'a9', 7: 'a10', 11: 'r1', 12: 'r2', 13: 'r3',
            20: 'cs1 -> sq1 -> a8', 21: 'a8 now (5/5)', 22: 'a8 with 0 pips (deflect -> cs2 -> down)', 23: 'a8 fail',
            24: 'cs2 only', 25: 'down window', 26: 'lead_stand a13 + a13', 27: 'a13 now',
            28: 'a13 with 0 pips (cs3 -> kill -> cs4 -> coda)', 29: 'a13 fail (instant death; test/defeat)',
            30: 'intro replay', 31: 'look dark on / off', 32: 'look crimson', 33: 'p2 now (skip cs1 / a8)',
            34: 'HP = 5 % floor + 1', 35: 'intro skip at tick 100', 80: 'HP = next floor + 1',
            90: 'next event random', 91: 'next event = item', 92: 'next event = buff', 99: 'hold'}
TEST_HELP_NAMES = {1: '회전 반월참', 2: '역습 일섬', 3: '오연 반월', 4: '월하 낙참 + 공중 원륜', 5: '후방 섬보',
                   6: '황광 원참', 7: '황광 낙참', 11: '자영 돌격', 12: '월륜 일섬', 13: '자영 활강',
                   20: '60% 컷신 → 자영 연참', 21: '자영 연참 (실드 5칸)', 22: '자영 연참 (실드 0칸 → 반격)',
                   23: '자영 연참 실패', 24: '반격 장면', 25: '쓰러짐', 26: '5% 이어짐 + 필살 · 자영 연참',
                   27: '필살 · 자영 연참', 28: '필살 (실드 0칸 → 엔딩)', 29: '필살 실패 (즉사)', 30: '등장 다시',
                   31: '어둠 켜기 / 끄기', 32: '붉은 들판', 33: '2페이즈로', 34: '체력 = 5% + 1',
                   35: '등장 건너뛰기 (100틱)', 80: '체력 = 다음 바닥 + 1', 90: '다음 이벤트 무작위',
                   91: '다음 이벤트 = 화무십일홍', 92: '다음 이벤트 = 월하대작', 99: '멈춤'}
LOCK_IDS = tuple(i for i in sorted(TEST_IDS) if 1 <= i <= 13)
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
LINE_AT = {1: ('intro', 20, 40), 2: ('intro', 62, 40), 3: ('intro', 104, 40), 4: ('intro', 146, 50),
           5: ('intro', 198, 100), 6: ('intro', 300, 50), 7: ('intro', 352, 44), 8: ('intro', 398, 44),
           9: ('intro', 444, 56), 10: ('intro', 502, 50), 11: ('intro_end', 0, 68), 12: ('a6', 12, 63),
           13: ('cs1', 12, 44), 14: ('cs1', 58, 42), 15: ('cs1', 104, 36), 16: ('cs1', 144, 40),
           17: ('ending', 300, 60), 18: ('ending', 368, 68), 19: ('ending', 448, 45), 20: ('ending', 536, 119),
           21: ('ending', 664, 130), 22: ('ending', 800, 130), 23: ('ending', 936, 90),
           24: ('event', 4, 48), 25: ('event', 4, 48)}    # 24 item branch, 25 buff branch (EVENT['lines'])
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
           '#last', '#last2', '#rear', '#far', '#dec', '#rec', '#hits', '#a6cd', '#pips', '#gres', '#gk', '#down',
           '#skip', '#warn', '#inv', LOOK_REQ)
# I1 (request s3-5): S3's own fake players, folded in from s3lib.FP_EXTRA in the same order (s3lib.FP = CORE_FP; cleanup resets
# exactly these, the build refuses any other '#name hr' of S3's files): temporaries, the constants #c<n> (CORE_CONSTS), the
# floor / sequence / shield / kipup / revive / skip state, the AI's #ai_* and its per-pattern weights / cooldowns.
CORE_CONSTS = (2, 3, 5, 10, 64, 100, 577, 1000, 36000)
CORE_FP += (('#t', '#t2', '#t3', '#t4', '#t5', '#cn1', '#cn1000') + tuple(f'#c{c}' for c in CORE_CONSTS)
            + ('#fl60', '#fl5', '#flw', '#sqn', '#sqh', '#shb', '#kip', '#grs', '#rvw', '#a6q', '#ctr', '#flq', '#h1', '#h2',
               '#h3', '#h4', '#pipoff', '#lk', '#skp', '#rp')
            + ('#ai_d2', '#ai_mv', '#ai_pht', '#ai_sum', '#ai_r', '#ai_rc', '#ai_ff', '#ai_nx', '#ai_rcd', '#ai_fl', '#ai_lf',
               '#ai_ls', '#ai_nn', '#ai_bs',        # F1 (HR-13): an empty pick in a row, the backstep's mid pick pending
               '#ai_tmc')                           # F1 round 1 (HR-14): the module clock of a kept tail's last move tick
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
         'sword': ('hand', 'sheathed', 'gone'), 'blade': ('off', 'lilac', 'pink', 'violet', 'gold'),
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
    'g_dive': (10, None, {'appear': 0, 'dive': 3, 'hit': 6, 'end': 10}),
    'g_deflect': (12, None, {'stop': 0, 'fall': 2, 'lock': 10, 'end': 12}),
    'repel': (104, None, {'lock': 0, 'grab': 8, 'hat_back': 8, 'flash': 24, 'throw': 28, 'b2b': 44, 'toss': 58,
                          'hat_off': 60, 'land': 75, 'lie': 78, 'petals': 80, 'kick': 102, 'end': 104}),
    'down': (40, (0, 40), {}),
    'kipup': (20, None, {'legs': 0, 'up': 8, 'crouch': 10, 'raise': 14, 'end': 20}),
    'lead_down': (82, None, {'legs': 0, 'up': 7, 'sword_up': 10, 'hat_hand': 12, 'walk': 12, 'refill': 29,
                             'hat_over': 42, 'hat_on': 48, 'glow': 56, 'dark': 64, 'brim': 65, 'end': 82}),
    'lead_stand': (70, None, {'stagger': 0, 'hat_hand': 8, 'walk': 10, 'refill': 18, 'hat_over': 30, 'hat_on': 36,
                              'glow': 44, 'dark': 52, 'brim': 53, 'end': 70}),
    'sq1': (60, None, {'crouch': 0, 'rise': 6, 'rehat': 10, 'hat_hand': 12, 'hat_on': 28, 'standoff': 30, 'dark': 42,
                       'brim': 46, 'end': 60}),
    'intro': (554, None, {'l1': 20, 'pour': 30, 'l2': 62, 'sip': 80, 'l3': 104, 'raise': 110, 'l4': 146, 'l5': 198,
                          'cup_down': 206, 'stand': 214, 'turn': 248, 'l6': 300, 'scab_hand': 300, 'l7': 352,
                          'l8': 398, 'gesture': 402, 'l9': 444, 'l10': 502, 'scab_up': 510, 'end': 554}),
    'intro_end': (86, None, {'l11': 0, 'smile': 2, 'head_down': 36, 'turn_away': 44, 'spin': 50, 'draw': 56,
                             'stance': 60, 'brim': 62, 'tuck': 76, 'music': 76, 'push': 82, 'end': 86}),
    'cs1': (213, None, {'lunge': 0, 'lock': 10, 'l13': 12, 'push': 32, 'leap': 36, 'hat_back': 40, 'land': 52,
                        'l14': 58, 'glint': 96, 'black': 100, 'sheathe': 104, 'hat_on': 104, 'l15': 104, 'petal': 114,
                        'petal2': 128, 'l16': 144, 'cut': 154, 'neg': 161, 'pink': 165, 'slash': 169, 'recolour': 173,
                        'hat_back2': 176, 'music': 179, 'swirl': 183, 'end': 213}),
    'ending': (1042, None, {'glint': 16, 'band': 20, 'rise': 28, 'hat_on': 44, 'raise': 48, 'clash1': 58, 'lock': 62,
                            'back': 80, 'lunge': 92, 'clash2': 96, 'x1': 108, 'x2': 116, 'x3': 124, 'pass': 140,
                            'strike': 143, 'return': 170, 'clash3': 174, 'flash2': 188, 'leap': 190, 'a1': 204,
                            'a2': 216, 'a3': 228, 'white': 232, 'fly': 238, 'land': 258, 'rise2': 268, 'walk': 272,
                            'scab_up': 284, 'swing': 296, 'l17': 300, 'music': 300, 'seated': 320, 'l18': 368,
                            'l19': 448, 'head_down': 494, 'turn': 506, 'l20': 536, 'profile': 600, 'hand': 612,
                            'l21': 664, 'gaze': 690, 'dip': 786, 'pivot': 794, 'l22': 800, 'gesture': 860,
                            'smile': 920, 'l23': 936, 'brim': 936, 'pull': 980, 'eyes': 1030, 'end': 1042}),
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
assert len(CLIPS) == 47
CINE_CLIPS = ('intro', 'intro_end', 'cs1', 'sq1', 'repel', 'lead_down', 'lead_stand', 'ending')   # S2b (scarlet_cine.mjs)
EV_CLIPS = ('ev_give', 'ev_toast', 'ev_leave')                                                    # S2a (§7)
CLIP_OWNER = {k: ('S2b' if k in CINE_CLIPS else 'S2a') for k in CLIPS}

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
    """HITS rows of a scripted pattern: each cut lands as a pdisc(CUT_R) on the contact of the move whose clip 'hit'
    meets the cut's strike; each a7_throw row releases one moon disc."""
    rows, out = SCRIPTS[key], []
    for t, _step, clip, c in rows:
        if c:
            mv = [r for r in rows if r[2] and 'hit' in CLIPS[r[2]][2] and r[0] + ev(r[2], 'hit') == c[2]]
            assert len(mv) == 1, (key, c)
            out.append((mv[0][2], 'hit', 'pdisc', (CUT_R,), c[3], c[4]))
        if clip == 'a7_throw':
            out.append(('a7_throw', 'release', 'pj_disc', (DISC['hr'], DISC['speed'], DISC['life']), DISC['tier'],
                        DISC['kb']))
    return out


HITS.update({k: _script_hits(k) for k in ('a8', 'a13', 'r1', 'r3')})
# R2: one disc (kb 2 as a single hit); at <= R2_TWO_PCT HP a second disc follows, then the first is kb 0, the last kb 2
HITS['r2'] = [('a7_throw', 'release', 'pj_disc', (DISC['hr'], DISC['speed'], DISC['life']), DISC['tier'],
               DISC['kb_last_r2'])]

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
KIT_SPRITE_PX = sum(f * w * h for rows in KIT_SPRITES.values() for f, w, h in rows)
assert KIT_SPRITE_PX == 237_568 and KIT_SPRITE_PX <= KIT_SPRITE_CAP, KIT_SPRITE_PX
ATLAS_CAP = {'rig': 150_000, 'kit': KIT_SPRITE_CAP, 'gate_icon': 5_000, 'event': 0, 'boss': 430_000}   # PLAN §9.5
GATE_ICON_PX_CAP = ATLAS_CAP['gate_icon']


def _macro(a):
    def v(x):
        return f'"{x}"' if isinstance(x, str) else str(int(x))
    return '{' + ','.join(f'{k}:{v(x)}' for k, x in a.items()) + '}'


class _Kit:
    """Kit call lines. Empty while the kit manifest is missing, so S2b / S3 / S4 build and load without S1K's files (the
    Apep / Tachy / Arlecchino 'api.K stand-in' rule); names / args are checked against the contract either way."""

    def _on(self):
        return KIT_MANIFEST.exists()

    def _call(self, sub, table, name, a):
        assert name in table, f'kit {sub}{name} is not in the contract'
        assert sorted(a) == sorted(table[name]), f'kit {sub}{name} takes {table[name]}'
        if not self._on():
            return ''
        return f'function {NS}fx/{sub}{name}' + (f' {_macro(a)}' if a else '')

    def p(self, name, **a):
        return self._call('p/', KIT_PRESETS, name, a)

    def pw(self, name, path):
        """fx/p/<name> with storage <path> (F2: arguments computed at run time, e.g. A9's probed streak length core.a9,
        CS4 E1b's band sweep); the compound must hold every arg of the preset (extra keys are allowed)."""
        assert name in KIT_PRESETS and KIT_PRESETS[name], f'kit p/{name}: no macro args'
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
            assert a.get('g') in OVERLAYS, a
        if name == 'skip':
            assert 0 <= int(a.get('s', -1)) <= 5, a
        return self._call('hud/', KIT_HUD, name, a)

    def ovl(self, g, t_in, hold, t_out):
        """fx/hud/ovl {g,in,hold,out} (in is a Python keyword)."""
        return self.hud('ovl', **{'g': g, 'in': t_in, 'hold': hold, 'out': t_out})

    def snd(self, name):
        assert name in KIT_SOUNDS, name
        return f'function {NS}fx/snd/{name}' if self._on() else ''

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
    idempotent. start takes SEQ_ARGS[name] as macro args (repel {at:60|5}, lead_stand {g:"a8"|"a13"}); intro also has
    seq/intro/skip (SEQ_EXTRA). The core owns invulnerability, cine, the phase switch, floors, the death finish, when a
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
                                                 'test/', 'rig_stub/') + tuple(f'p/{k}/' for k in P1),
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
    'SR': (('F:items/**', ()), ('F:player/take_damage', ()), ('F:player/dash_iframe', ()), ('F:player/reset_one', ()),
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
    'T:mboss_scarlet/p_ghost.py', 'F:boss/scarlet/p/a8/start', 'F:boss/scarlet/p/a13/start', 'F:boss/scarlet/p/r1/start',
    'F:boss/scarlet/p/r2/start', 'F:boss/scarlet/p/r3/start', 'F:boss/scarlet/g/cut/make', 'HR:renders/s4_a8.png',
    'F:items/mythic/sword_hwamu/def', 'F:items/proc/hw_hit', 'F:items/register', 'F:player/take_damage',
    'F:player/dash_iframe', 'F:player/reset_one', 'F:player/update_item', 'F:player/update_item_macro',
    'F:player/hr_moon/apply', 'F:codex/labels', 'F:snd/f422', 'F:snd/f429', 'F:load', 'F:uninstall', 'R:items.md',
    'HR:tests/test_hwamu.py', 'HR:tests/test_moon.py', 'HR:renders/sr_tooltip.txt',
    *(f'HR:requests/{o.lower()}.md' for o in _OWN_FILES if o != 'lead'),
)


def owners_of(path):
    """The owners whose OWN_FILES patterns match path (minus their exclusions)."""
    return [o for o, pats in OWN_FILES.items()
            if any(fnmatchcase(path, p) and not any(fnmatchcase(path, x) for x in ex) for p, ex in pats)]


# Shield (S3 -> S4; PLAN §5): call names under F:boss/scarlet/ and their macro args
SHIELD_CALLS = {'arm': 'shield/arm', 'cut': 'shield/cut', 'judge': 'shield/judge', 'fail60': 'ult/fail60',
                'fatal': 'ult/fatal', 'off': 'shield/off'}
SHIELD_ARGS = {'cut': ['s']}
GRES = '#gres'          # objective OBJ, after shield/judge: 1 deflect, 2 fail
PIPS_FP = '#pips'       # pips left (the under bar #buSub)


def shield(call, **a):
    """A shield call line (shield/arm: 5/5 + the under bar; shield/cut {s}: register a counting cut's strike tick s and
    store its lock point (@s / position = the cut marker at the lock); shield/judge -> #gres hr; ult/fail60; ult/fatal
    (@s = the player); shield/off)."""
    assert call in SHIELD_CALLS and sorted(a) == sorted(SHIELD_ARGS.get(call, [])), (call, a)
    return f'function {NS}{SHIELD_CALLS[call]}' + (f' {_macro(a)}' if a else '')


# The cut builder (PLAN §5.3; S4 implements g/cut/**): a ghost cut = a quiet Electro disc hazard of radius CUT_R at the
# player's feet, made at `made` (tell = strike - made), re-aimed onto the player every tick until `lock` = strike -
# LOCK_LEAD, then fixed; a counting cut (gauntlets) registers with shield/cut {s} at the lock.
CUT_CALLS = ('g/cut/make', 'g/cut/aim', 'g/cut/lock')
CUT_ARGS = {'g/cut/make': ['s', 't', 'dmg', 'kb', 'n'], 'g/cut/aim': ['s'], 'g/cut/lock': ['s']}


def cut(made, lock, strike, tier='T2', kb=KB_CUT, count=1):
    """[(pattern tick, line)] of one cut: make at `made` (s = strike tick, t = strike - made, dmg = DMG[tier], kb, n =
    1 counting / 0 not), aim every tick made+1 .. lock-1, lock at `lock` (which also calls shield/cut {s} when n = 1).
    @s / position: the pattern's executor (the body); g/cut/* find the player and their own marker (rlk_hr_cut, by s)."""
    assert lock == strike - LOCK_LEAD and strike - made >= TELL_MIN and made <= lock, (made, lock, strike)
    assert tier in DMG and int(count) in (0, 1)
    out = [(made, f'function {NS}g/cut/make {_macro({"s": strike, "t": strike - made, "dmg": DMG[tier], "kb": kb, "n": count})}')]
    out += [(t, f'function {NS}g/cut/aim {_macro({"s": strike})}') for t in range(made + 1, lock)]
    out.append((lock, f'function {NS}g/cut/lock {_macro({"s": strike})}'))
    return out


def disc(kb=0):
    """The one A7 moon-disc launch line (S4's g/disc/throw): @s = the body, rotated toward its lock (F1 HR-15: g/disc/lock,
    the player's floor spot at DISC_LOCK = release - LOCK_LEAD; a throw without a lock locks at once); one pj/launch (DISC)
    + one kit card (fx/prop/disc); kb 0, or 2 for R2's last disc."""
    assert int(kb) in (0, DISC['kb_last_r2'])
    return f'function {NS}g/disc/throw {_macro({"kb": kb})}'


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
        assert ts == sorted(ts), f'{key}: rows out of order'
        for t, step, clip, c in rows:
            assert clip is None or clip in CLIPS, (key, step, clip)
            if c:
                made, lock, strike, tier, kb = c
                cut(made, lock, strike, tier, kb)                     # lock = strike - 7, made >= 12 t before
                hits = [r for r in rows if r[2] and 'hit' in CLIPS[r[2]][2] and r[0] + ev(r[2], 'hit') == strike]
                assert len(hits) == 1, f'{key}: cut {c} strikes on no / several move contacts'
    for g in GAUNTLETS:
        cuts = [r[3] for r in SCRIPTS[g] if r[3]]
        assert len(cuts) == len(CUT_IDS[g]) == 9 and all(c[3:] == _TC for c in cuts), g    # F1 (HR-19): tier TC
        dive = [r for r in SCRIPTS[g] if r[2] == 'g_dive']
        assert len(dive) == 1 and dive[0][0] + ev('g_dive', 'hit') == JUDGE_T[g], g
        assert REPEL_T[g] == JUDGE_T[g] + CLIPS['g_deflect'][0], g
    for key, rels in DISC_RELEASE.items():
        rows = [r for r in SCRIPTS[key] if r[2] == 'a7_throw']
        assert tuple(r[0] + ev('a7_throw', 'release') for r in rows) == rels, key
        assert all(r[0] <= lk < rel for r, lk, rel in zip(rows, DISC_LOCK[key], rels)), key   # F1 (HR-15): inside its throw
    # F1 (HR-14): every P1-kit pattern ends 8-12 t after its last hit, inside its clip
    for key, end in PAT_END.items():
        last = max(ev(c, e) for c, e, *_r in HITS[key]) if key != 'a4' else ev('a4', 'land')
        assert 8 <= end - max(ev(c, e) for c, e, *_r in HITS[key]) <= 12 and last < end < CLIPS[key][0], (key, end)


def _check_contract():
    """The D0 self-checks (pure data)."""
    for k, (ln, lp, evs) in CLIPS.items():
        assert all(0 <= t < ln for t in evs.values()), f'clip {k}: an event outside 0..len-1'
        assert lp is None or 0 <= lp[0] < lp[1] <= ln, f'clip {k}: loop {lp}'
    for key, hs in HITS.items():
        assert key in P1 + P2, key
        for clip, e, shape, dims, tier, kb in hs:
            assert clip in CLIPS and e in CLIPS[clip][2], f'HITS {key}: {clip}.{e}'
            assert tier in DMG and kb in (KB_CHAIN, KB_SINGLE, KB_FINAL), (key, tier, kb)
    _check_scripts()
    for key in ('a8', 'a13', 'r1', 'r2', 'r3'):
        assert key in HITS, key
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
    assert TEST_IDS[21].startswith('a8') and TEST_IDS[27].startswith('a13')
    assert set(TEST_HELP_NAMES) == set(TEST_IDS) and set(EV_TEST_IDS) <= set(TEST_IDS)
    assert set(WEIGHTS) | set(TRIGGER_ONLY) <= keys and set(COOLDOWN) <= keys and set(WEIGHTS) & set(TRIGGER_ONLY) == set()
    assert set(SEQ_CLIPS) == set(SEQS) == set(SEQ_LEN) and all(c in CLIPS for cs in SEQ_CLIPS.values() for c in cs)
    assert SEQ_LEN['intro'] == CLIPS['intro'][0] + CLIPS['intro_end'][0] <= BOSS['intro'] and SKIP_T == CLIPS['intro'][0]
    assert SEQ_LEN['ending'] == CLIPS['ending'][0] == END_H['std'] and SEQ_LEN['event'] == EVENT['len']
    for s in ('cs1', 'sq1', 'repel', 'lead_down', 'lead_stand'):
        assert SEQ_LEN[s] == CLIPS[s][0], s
    assert len(CINE_CLIPS) == 8 and len(EV_CLIPS) == 3 and sum(o == 'S2a' for o in CLIP_OWNER.values()) == 39
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
    assert len(KIT_PRESETS) == 50 and sum(k.startswith('ev_') for k in KIT_PRESETS) == 8
    assert sum(k.startswith('ev_') for k in KIT_SOUNDS) == 7
    assert sorted(OVERLAYS.values()) == list(range(0xEC10, 0xEC16)) and VIG == 0xEC16
    assert all(FONT_RANGE[0] <= c <= FONT_RANGE[1] for c in list(OVERLAYS.values()) + [VIG])
    assert all(0 < t <= JUDGE_T[g] for g in GAUNTLETS for t in BOLTS[g])
    assert DARK_SLICES[0] == DARK_T == DARK_CALL_T + 1 and DARK_SLICES == tuple(DARK_T + 3 * i for i in range(4))
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

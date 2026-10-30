"""Frozen D0 contract of the 타키 (Tachy) module generator: every stage (S1 framework + rift, S1K kit + arena, S2 rig +
sequences, S3 core / AI / gimmicks / melee, S4 aerial / mantle) imports this file and never edits it. A change goes
through a request (S:tk/requests/<stage>.md) applied by the lead at integration. Prose version: S:tk/contract.md;
design: S:tk/PLAN.md (section numbers below refer to it).

Importing has no side effects (no files written). Units: Python helpers take blocks / ticks / degrees; the framework
boundary is tenths of a block and % of the base hit (atk 12 x dmgMul 135: raw = floor(0.162 x pct)).
"""
from dataclasses import dataclass, field
from pathlib import Path
import json
import sys

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
import mboss_lib as L  # noqa: E402

# =============================================================================================
# 1. Identity, registry entry, arena (PLAN §6, §8)
ID = 'tachy'
N = 20
ROOT = L.fn_root_of(ID)                     # 'boss/tachy'
NS = f'rlk:{ROOT}/'
FDIR = L.FN / ROOT
REG = L.load_registry()
BOSS = dict(next(b for b in REG['boss'] if b['id'] == ID))
assert BOSS['kind'] == 'special' and BOSS['n'] == N and ROOT == 'boss/tachy', BOSS
NAME, SUB, COLOR = BOSS['name'], BOSS['sub'], BOSS['color']   # 타키 / 잠식된 제7공수대원 / #F2C230

AID = 'tk_lift'
# The arena entry S1 adds to arenas{} (frozen here so S1K / S3 / S4 can work before it lands).
ARENA_SPEC = {'n': 3, 'theme': 'tk_lift', 'ver': 1, 'cx': 640, 'cy': 201, 'cz': 8, 'r': 27, 'walk': 24, 'safe': 22,
              'start': {'x': 640.5, 'y': 201.0, 'z': 30.5, 'yaw': 180.0, 'pitch': 0.0},
              'box': {'x0': 600, 'y0': 190, 'z0': -32, 'x1': 680, 'y1': 250, 'z1': 48},
              'looks': ['dust', 'abyss'], 'oob': {'y0': 198, 'y1': 235}}
if AID in REG.get('arenas', {}):
    _a = REG['arenas'][AID]
    assert all(_a.get(k) == v for k, v in ARENA_SPEC.items()), f'arenas.{AID} differs from the D0 contract'
ARENA = dict(ARENA_SPEC, aid=AID)
CX, CY, CZ = ARENA['cx'], ARENA['cy'], ARENA['cz']    # block corner = the arena axis (centre point 640.0 201 8.0)
WALK, SAFE = float(ARENA['walk']), float(ARENA['safe'])
MOVE_R = WALK - 1.5                                    # blink / landing / dash end points stay inside (PLAN §4.1)
HOVER_Y = CY + 6                                       # W2 hover (feet)
HIGH_Y = CY + 13                                       # L high hover (feet, <= 214)
LOOK_DEFAULT, LOOK_ABYSS = 'dust', 'abyss'


def arena_ready():
    """True once S1 has added arenas.tk_lift (the framework then generates F:mboss/ar/tk_lift/** and the arena generator
    F:mboss/arena/tk_lift/**, a stub until S1K's theme module exists)."""
    return AID in REG.get('arenas', {})


def arena_look(look):
    """The look-job call (T2 'dark' event: abyss; the framework's ensure restores dust at the next fight). Empty until
    arena_ready(): no stage may reference another stage's functions before they exist (a missing function fails load)."""
    assert look in ARENA['looks'], look
    return f'function rlk:mboss/arena/{AID}/look/{look}' if arena_ready() else ''

# =============================================================================================
# 2. Damage, elements, hits (PLAN §4.1-4.2)
# % of the base hit (mboss/hurt coefficient). R2: x 0.83 (35 / 50 / 68 / 85 before): the chains now land on a player who
# stands or walks in (no knockback between hits, tracking, the gap closer), so the same tiers cost about 20 % more
DMG = {'T1': 29, 'T2': 42, 'T3': 56, 'T4': 71}
NOVA_PM = 250                                          # pl_dot per mille, non-lethal
FEATHER_TIER = 'T1'
PYRO, ELECTRO = 1, 3                                   # #elem numbering
EL_NAME = {PYRO: '불', ELECTRO: '번개'}
EL_HEX = {PYRO: '#FF8A3D', ELECTRO: '#E8C84A'}
EL_U = 1000                                            # 1U per hit
# el: 'cur' = the current blade element (G1), or a fixed element
# HITS[pattern] = [(clip, event, shape, dims, tier, el)]; shapes: sector(r, half_deg), disc(r), line(len, w),
# pj_blade(hr, speed, life), pj_ball(hr, speed, life), dash_line(w) (length = the dash), full()
# R2 (10-30, the user: "보스가 너무 작음 · 앙상해 보임"): the figure is SIZE x the D0 design (2.25 b -> 2.81 b) and her
# blade reach grows with it (REACH x every melee radius / width; the W1 / W2 crescents, the L shock and the mantle keep
# theirs). The numbers in HITS are the scaled ones.
SIZE = 1.25
REACH = 1.2
_R = lambda v: round(v * REACH, 1)   # noqa: E731
HITS = {
    'a1': [('a1_dash', 'go', 'dash_line', (_R(1.6),), 'T2', 'cur'), ('a1_dash', 'hit', 'sector', (_R(3.4), 60), 'T2', 'cur')],
    'b1': [('b1_wrap2', 'hit1', 'sector', (_R(3.8), 75), 'T2', 'cur'), ('b1_wrap2', 'hit2', 'sector', (_R(3.4), 60), 'T3', 'cur'),
           ('b1_wrap2', 'hit2', 'disc', (_R(1.6),), 'T3', 'cur')],
    'b2': [('b2_side4', 'hit1', 'sector', (_R(3.6), 60), 'T2', 'cur'), ('b2_side4', 'hit2', 'line', (_R(5.0), _R(1.8)), 'T3', 'cur'),
           ('b2_side4', 'hit3', 'sector', (_R(3.2), 90), 'T1', 'cur'), ('b2_side4', 'hit4', 'sector', (_R(3.2), 90), 'T1', 'cur')],
    # R2: the three bangs T2 (were T3): all six now land on a standing player (P3 standing loss <= 1.8 x the Guardian's)
    'b3': [('b3_six', 'hit1', 'sector', (_R(5.0), 85), 'T2', 'cur'), ('b3_six', 'hit2', 'sector', (_R(3.6), 70), 'T1', 'cur'),
           ('b3_six', 'hit3', 'sector', (_R(3.6), 70), 'T1', 'cur'),
           ('b3_six', 'bang1', 'sector', (_R(3.2), 45), 'T2', PYRO), ('b3_six', 'bang1', 'disc', (_R(1.4),), 'T2', PYRO),
           ('b3_six', 'bang2', 'sector', (_R(3.2), 45), 'T2', PYRO), ('b3_six', 'bang2', 'disc', (_R(1.4),), 'T2', PYRO),
           ('b3_six', 'bang3', 'sector', (_R(3.2), 45), 'T2', PYRO), ('b3_six', 'bang3', 'disc', (_R(1.4),), 'T2', PYRO)],
    'c1': [('c1_combo', 'h1', 'sector', (_R(3.6), 70), 'T1', 'cur'), ('c1_combo', 'h2', 'disc', (_R(4.2),), 'T2', 'cur'),
           ('c1_combo', 'h3', 'sector', (_R(3.4), 70), 'T1', 'cur'), ('c1_combo', 'h4', 'sector', (_R(4.0), 80), 'T2', 'cur'),
           ('c1_combo', 'thrust', 'dash_line', (_R(1.8),), 'T3', 'cur')],
    'c2': [('c2_combo', 'h1', 'sector', (_R(3.4), 70), 'T1', 'cur'), ('c2_combo', 'h2', 'sector', (_R(3.4), 70), 'T1', 'cur'),
           ('c2_combo', 'h3', 'sector', (_R(3.6), 70), 'T2', 'cur'), ('c2_combo', 'thrust', 'dash_line', (_R(1.8),), 'T3', 'cur')],
    'c3': [('c3_combo', 'h1', 'sector', (_R(3.4), 70), 'T1', 'cur'), ('c3_combo', 'h2', 'sector', (_R(3.4), 70), 'T1', 'cur'),
           ('c3_combo', 'h3', 'sector', (_R(3.4), 70), 'T1', 'cur'), ('c3_combo', 'h4', 'sector', (_R(3.8), 75), 'T2', 'cur'),
           ('c3_combo', 'h5', 'sector', (_R(3.8), 75), 'T2', 'cur'), ('c3_combo', 'thrust', 'dash_line', (_R(1.8),), 'T3', 'cur')],
    'k': [('k_glint', 'thrust', 'dash_line', (_R(1.8),), 'T3', 'cur'), ('k_plunge', 'hit', 'disc', (_R(3.5),), 'T4', ELECTRO)],
    'w1': [('w1_wave', e, 'pj_blade', (3.5, 1.25, 32), 'T2', 'cur') for e in ('wave1', 'wave2', 'wave3')],
    'w2': [('w2_air', e, 'pj_ball', (1.3, 1.1, 30), 'T2', 'cur') for e in ('c1', 'c2', 'c3')]
          + [('w2_dive', 'slash', 'sector', (_R(4.5), 80), 'T4', 'cur')],
    'l': [('dive', 'impact', 'disc', (_R(1.4),), 'T2', ELECTRO), ('l_shock', 'shock', 'disc', (5.5,), 'T4', ELECTRO)],
    'mantle': [('mantle_hold', None, 'pj_ball', (1.8, 0.5, 16), 'T1', ELECTRO),
               ('mantle_nova', 'hit', 'full', (), 'NOVA', ELECTRO)],
}
# R2: only the last hit of a melee chain knocks back (#hzKB); the earlier ones stay put so the chain is not broken by its
# own knockback (the user: "넉백때문에 공격범위에서 벗어나 마지막 2~3 번째 공격은 안 맞음")
KB_CHAIN, KB_FINAL = 0, 3
DASH_LEN = {'a1': 12.0, 'c1': 8.0, 'c2': 8.0, 'c3': 8.0, 'k': 7.0, 'w2': 14.0}   # max dash lengths (b)
TELL_MIN, TELL_BIG, COMBO_GAP = 12, 20, 10       # PLAN §4.1 (first visible motion -> hit; follow-ups apart)
NO_DECALS = True                                 # every Tachy hazard is #hzQuiet 1, no ground telegraph (PLAN §1.2)

# =============================================================================================
# 3. Phases, floors, gimmicks (PLAN §4.3, §5)
PH = {'intro': 0, 'p1': 1, 'm1': 2, 't1': 3, 'p2': 4, 'm2': 5, 't2': 6, 'p3': 7, 'death': 8}
FLOORS = (70, 35)                               # % of max HP: reaching one schedules M -> T at the next decision
RECOVER = {1: (18, 26), 2: (18, 26), 3: (12, 18)}   # idle after a pattern (min, max) per fight phase 1..3
# G1 twin-pole blade
G1_START = PYRO
G1_REFRESH_T, G1_REFRESH_BELOW, G1_AURA = 20, 400, 1000
G1_FORCE_SWAP = {1: 600, 2: 600, 3: 400}         # ticks without a swap -> forced swap
G1_SWAP_AFTER_C = 50                             # % chance after a C combo; always after K
# G2 overload mantle
G2_GAUGE = 100
G2_RX, G2_DOT, G2_HIT, G2_HIT_ICD = 12, 4, 1, 5  # gauge loss: reaction / reaction tick / other hit (once per ICD t)
G2_TIME = {'m1': 360, 'm2': 300}
G2_TAKEN_PCT = 20                                # body damage taken while mantled (not immune)
G2_ALT_T = 60                                    # self-aura alternation while mantled
G2_STUN_T, G2_STUN_TAKEN_PCT, G2_ENERGY = 120, 150, 15
G2_FEATHER_EVERY = 36
# G3 unstable core: windows on the pattern clock (the core tags the body rlk_tk_core inside them)
G3_WINDOWS = {'a1': (0, 14), 'b3': (0, 30), 'w1': (6, 40), 'c3': (0, 22)}
G3_TRUE_PCT, G3_STAGGER_T, G3_STAGGER_TAKEN_PCT = 3, 50, 130

# =============================================================================================
# 4. AI (PLAN §4.3; S3 tunes values at review, the keys are frozen)
BANDS = (5.0, 12.0)                              # near <= 5 < mid <= 12 < far
REAR_DEG, REAR_DWELL = 60, (20, 30)              # rear zone half-angle; 20 of 30 t -> B2 70 % / K 30 %
FAR_B, FAR_DWELL = 14.0, 40
# WEIGHTS[key][fight phase 1..3] = (near, mid, far); 0 = not used
WEIGHTS = {
    # R2: the far column also holds the melee chains (they open with the gap-closer blink, core.CLOSE_KEYS); A1 / W1 less
    'a1': {1: (0, 30, 35), 2: (0, 20, 25), 3: (0, 15, 20)},
    'b1': {1: (0, 0, 0), 2: (25, 10, 0), 3: (15, 5, 0)},
    'b2': {1: (35, 15, 10), 2: (15, 10, 10), 3: (10, 5, 5)},
    'b3': {1: (0, 0, 0), 2: (0, 0, 0), 3: (20, 20, 10)},
    'c1': {1: (35, 20, 20), 2: (10, 5, 0), 3: (0, 0, 0)},
    'c2': {1: (0, 0, 0), 2: (20, 15, 15), 3: (15, 10, 0)},
    'c3': {1: (0, 0, 0), 2: (0, 0, 0), 3: (25, 15, 15)},
    'k': {1: (15, 20, 20), 2: (10, 20, 15), 3: (15, 20, 15)},
    'w1': {1: (15, 15, 25), 2: (0, 15, 20), 3: (0, 0, 15)},
    'w2': {1: (0, 0, 0), 2: (10, 20, 25), 3: (0, 15, 20)},
    'l': {1: (0, 0, 0), 2: (5, 10, 20), 3: (0, 15, 20)},
}
# R2: out of reach (farther than OOR_B b) for OOR_DWELL t -> a chain with the gap closer OOR_PCT % of the decisions
OOR_B, OOR_DWELL, OOR_PCT = 5.5, 20, 60
COOLDOWN = {'a1': 120, 'b1': 160, 'b2': 140, 'b3': 300, 'c1': 200, 'c2': 200, 'c3': 200, 'k': 260, 'w1': 360,
            'w2': 420, 'l': 700}
P3_COOLDOWN_PCT = 80
L_P3_COOLDOWN, L_FIRST_P2 = 560, 200
K_RULES = {'gap': 2, 'not_after': ('c1', 'c2', 'c3')}

# =============================================================================================
# 5. Pattern / service keys, ownership, test ids (contract §1)
MELEE = ('a1', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3')     # S3: tools/mboss_tachy/p_melee.py -> p/<key>/**
AIR = ('k', 'w1', 'w2', 'l')                           # S4: tools/mboss_tachy/p_air.py -> p/<key>/**
MANTLE = ('mantle',)                                   # S4: tools/mboss_tachy/p_mantle.py -> p/mantle/** (hazards only)
SEQS = ('intro', 'death', 't1', 't2')                  # S2: tools/mboss_tachy/seq.py -> seq/<name>/**
PATTERN_NAMES = {'a1': '돌진 베기', 'b1': '날개 가리기 2연격', 'b2': '옆걸음 4연격', 'b3': '충전 6연격',
                 'c1': '연속기 · 블링크', 'c2': '연속기 · 블링크 Ⅱ', 'c3': '붉은 핵 연속기', 'k': '블링크',
                 'w1': '지상 장풍', 'w2': '공중 장풍', 'l': '착지 공격', 'mantle': '과부하 외피'}
TEST_IDS = {1: 'a1', 2: 'b1', 3: 'b2', 4: 'b3', 5: 'c1', 6: 'c2', 7: 'c3', 8: 'k', 9: 'w1', 10: 'w2', 11: 'l',
            20: 'mantle (break demo: gauge to 1)', 21: 'mantle (fail: nova)', 22: 't1 날개 전개', 23: 't2 심연',
            24: 'G1 swap', 25: 'G3 backfire demo', 26: 'intro replay', 27: 'death', 30: 'phase 2', 31: 'phase 3',
            40: 'element Pyro', 41: 'element Electro', 80: 'HP = next floor + 1', 99: 'freeze'}
TEST_HELP_NAMES = {1: '돌진 베기', 2: '날개 가리기 2연격', 3: '옆걸음 4연격', 4: '충전 6연격', 5: '연속기 · 블링크',
                   6: '연속기 · 블링크 Ⅱ', 7: '붉은 핵 연속기', 8: '블링크', 9: '지상 장풍', 10: '공중 장풍',
                   11: '착지 공격', 20: '과부하 외피 (파괴)', 21: '과부하 외피 (폭발)', 22: '날개 전개', 23: '심연',
                   24: '원소 전환', 25: '불안정한 핵', 26: '등장 다시', 27: '쓰러짐', 30: '2단계로', 31: '3단계로',
                   40: '불 칼날', 41: '번개 칼날', 80: '체력 = 다음 바닥 + 1', 99: '멈춤'}

# =============================================================================================
# 6. Scores, tags, storage (contract §2). Module state = fake players in objective `tk` (owned by S3's init /
# uninstall); each stage may only add fake players with its own prefix: core `#<name>` from CORE_FP, a pattern
# `#<key>_<x>`, seq `#sq_<x>`. Rig objectives tkRig* (S2), kit objectives tkFx* (S1K).
OBJ = 'tk'
CORE_FP = ('#ph', '#pat', '#pt', '#done', '#el', '#swt', '#aut', '#sh', '#sht', '#shicd', '#core', '#stun', '#stag',
           '#last', '#last2', '#kgap', '#rear', '#far', '#dec', '#rec', '#sq', '#sqdone', '#fl', '#flnext', '#tst',
           '#lock', '#taken')
TAGS = {'part': 'rlk_tk_part', 'prop': 'rlk_tk_prop', 'fx': 'rlk_tk_fx', 'core': 'rlk_tk_core',
        'mantle': 'rlk_tk_mantle', 'air': 'rlk_tk_air', 'pat': 'rlk_tk_p'}   # pattern markers: rlk_tk_p + rlk_tk_p_<key>
STORAGE = 'rlk:tk'                     # keys: core.* (S3), rig.* (S2), fx.* (S1K), air.* (S4), seq.* (S2)
RIG_UUID = '524c4b4d-544b-4900-8000-0000000000{:02x}'   # part NN 00..27, shadow 40

# =============================================================================================
# 7. Rig contract (PLAN §2; S2 implements, S3/S4 call)
PARTS = ('pelvis', 'abdomen', 'chest', 'chest_glow', 'neck', 'head', 'hair_top', 'hair_1', 'hair_2', 'hair_3',
         'helmet', 'visor_glow', 'collar', 'shoulder_l', 'upper_arm_l', 'forearm_l', 'hand_l', 'shoulder_r',
         'upper_arm_r', 'forearm_r', 'hand_r', 'spine_pack', 'tassets', 'thigh_l', 'shin_l', 'foot_l', 'thigh_r',
         'shin_r', 'foot_r', 'wing_l1', 'wing_l2', 'wing_l3', 'wing_r1', 'wing_r2', 'wing_r3', 'sword', 'sword_edge',
         'scabbard', 'tendril_l', 'tendril_r')
assert len(PARTS) == 40
HEIGHT, HIP_Y = round(2.25 * SIZE, 3), round(1.10 * SIZE, 3)
LOOKS = {'form': ('cape', 'winged', 'abyss'), 'visor': ('up_off', 'down_pyro', 'down_electro', 'down_abyss', 'down_off'),
         'edge': ('off', 'yellow', 'pyro', 'electro', 'glint'), 'chest': ('off', 'amber', 'red', 'gold'),
         'hands': ('open', 'grip', 'fist')}
RIG_PROPS = ('cables',)
# rig/<call> functions (all @s = the body = the anchor, at its feet)
RIG_CALLS = ['init', 'spawn', 'tick', 'kill', 'uninstall', 'flash', 'state/normal', 'state/hidden', 'face/player',
             'face/track', 'prop/clear'] + [f'look/{ch}/{v}' for ch, vs in LOOKS.items() for v in vs] \
    + [f'prop/{p}' for p in RIG_PROPS]
RIG_MACRO_CALLS = {'face/set': ['yaw']}

# CLIPS[name] = (len, loop (from, to) or None, {event: tick}); play/<name> and start/<name> exist for each.
CLIPS = {
    'idle': (40, (0, 40), {}),
    'walk': (24, (0, 24), {'step1': 0, 'step2': 12}),
    'strafe_l': (20, (0, 20), {}), 'strafe_r': (20, (0, 20), {}),
    'backstep': (12, None, {'land': 10}),
    'flinch': (6, None, {}),
    'stagger': (50, (10, 50), {}),
    'stun': (120, (20, 100), {'rise': 100}),
    'swap_pyro': (24, None, {'drag': 6, 'ignite': 14}),
    'swap_electro': (24, None, {'drag': 6, 'spark': 14}),
    'blink_out': (8, None, {'gone': 6}),
    'blink_in': (10, None, {'appear': 0, 'settle': 8}),
    'leap_up': (16, None, {'lift': 6, 'top': 16}),
    'hover': (40, (0, 40), {}),
    'dive': (12, None, {'impact': 10}),
    'land': (16, None, {'settle': 14}),
    'leap_high': (16, None, {'gone_high': 16}),
    'hover_high': (40, (0, 40), {}),
    'a1_dash': (34, None, {'flare': 0, 'go': 14, 'hit': 20, 'end': 34}),
    'b1_wrap2': (50, None, {'wrap': 0, 'open': 22, 'hit1': 24, 'hit2': 40, 'end': 50}),
    'b2_side4': (78, None, {'hop': 0, 'land': 14, 'hit1': 22, 'raise': 30, 'hit2': 44, 'hit3': 54, 'hit4': 64, 'end': 78}),
    'b3_six': (112, None, {'glow': 0, 'dash': 30, 'hit1': 40, 'hit2': 50, 'hit3': 60, 'raise': 64, 'bang1': 76,
                           'bang2': 88, 'bang3': 100, 'end': 112}),
    'c1_combo': (92, None, {'h1': 14, 'h2': 32, 'h3': 46, 'h4': 58, 'glint': 68, 'thrust': 86, 'end': 92}),
    'c2_combo': (74, None, {'h1': 12, 'h2': 24, 'h3': 38, 'glint': 50, 'thrust': 68, 'end': 74}),
    'c3_combo': (104, None, {'flare': 0, 'h1': 22, 'h2': 32, 'h3': 44, 'h4': 60, 'h5': 70, 'glint': 80, 'thrust': 98,
                             'end': 104}),
    'k_hold': (20, (0, 20), {}),
    'k_glint': (18, None, {'glint': 0, 'thrust': 16}),
    'k_leap': (14, None, {'up': 8}),
    'k_plunge': (20, None, {'arcs': 0, 'hit': 16}),
    'w1_wave': (88, None, {'plant': 0, 'glow': 6, 'wave1': 46, 'wave2': 58, 'wave3': 70, 'end': 88}),
    'w2_air': (66, None, {'c1': 14, 'c2': 28, 'c3': 42, 'pull': 46, 'go': 66}),
    'w2_dive': (16, None, {'slash': 10, 'end': 16}),
    'l_shock': (20, None, {'shock': 10, 'end': 20}),
    'mantle_in': (24, None, {'wrap': 12, 'lift': 20}),
    'mantle_hold': (40, (0, 40), {}),
    'mantle_break': (40, None, {'crack': 0, 'fall': 20}),
    'mantle_nova': (44, None, {'swell': 0, 'flash': 40, 'hit': 44}),
    'intro': (184, None, {'hang': 0, 'snap1': 30, 'snap2': 33, 'snap3': 36, 'land': 42, 'pulse1': 48, 'pulse2': 56,
                          'push': 60, 'rise': 84, 'flare': 108, 'hair': 116, 'visor': 126, 'skull': 136, 'draw': 142,
                          'ignite': 156, 'stance': 170, 'music': 176, 'ring': 178, 'end': 184}),
    't1_wings': (80, None, {'kneel': 0, 'split': 10, 'spread': 30, 'flare': 50, 'stand': 70}),
    't2_abyss': (110, None, {'stagger': 0, 'flare': 20, 'tendrils': 36, 'dark': 50, 'swap': 60, 'rise': 90}),
    'death': (130, None, {'knee': 20, 'sword_plant': 36, 'visor_off': 50, 'wings_fall': 70, 'collapse': 100, 'ash': 116}),
}
# Clip ids (manifest order): the index in this tuple.
CLIP_ORDER = tuple(CLIPS)
# the form a clip is authored for (None = any form: the rig plays it in the stored form)
CLIP_FORM = {'intro': 'cape', 't1_wings': 'cape', 'b1_wrap2': 'winged', 'w2_air': 'winged', 'w2_dive': 'winged',
             't2_abyss': 'winged', 'b3_six': 'abyss', 'c3_combo': 'abyss'}

REAL_MANIFEST = _TOOLS / 'tachy_rig_manifest.json'          # S2 writes it
STUB_MANIFEST = Path(__file__).resolve().parent / 'stub_rig_manifest.json'   # D0


def rig_manifest():
    """S2's manifest when it exists, else the D0 stub; both must carry exactly the CLIPS table."""
    m = json.loads((REAL_MANIFEST if REAL_MANIFEST.exists() else STUB_MANIFEST).read_text(encoding='utf-8'))
    check_manifest(m)
    return m


def check_manifest(m):
    assert m.get('schema') == 1 and m.get('id') == ID, 'tachy rig manifest: schema 1, id tachy'
    got = {k: (v['len'], tuple(v['loop']) if v.get('loop') else None, v.get('events', {})) for k, v in m['clips'].items()}
    for k, (ln, lp, ev) in CLIPS.items():
        assert k in got, f'rig manifest: clip {k} missing'
        assert got[k] == (ln, lp, ev), f'rig manifest: clip {k} = {got[k]}, contract {(ln, lp, ev)}'
    assert [p['name'] for p in m['parts']] == list(PARTS), 'rig manifest: parts / order differ from the contract'
    return True


def rig_real():
    return REAL_MANIFEST.exists()


def rig(call, **macro):
    """The rig call line. While S2's manifest is missing the core (S3) generates the stand-in AP-style rig_stub/** with
    the same call names (every call sets #rigc tk to the clip id for tests; no visuals)."""
    base = 'rig' if rig_real() else 'rig_stub'
    args = ('{' + ','.join(f'{k}:{v}' for k, v in macro.items()) + '}') if macro else ''
    return f'function {NS}{base}/{call}' + (f' {args}' if args else '')


def play(clip):
    assert clip in CLIPS, clip
    return rig(f'play/{clip}')


def ev(clip, event):
    """The played tick of a clip event (patterns take every hit tick from here)."""
    return CLIPS[clip][2][event]

# =============================================================================================
# 8. Kit contract (S1K implements in tools/build_mboss_tk_fx.py; PLAN §9.2). Presets with args are macros (values in
# tenths for lengths, degrees for angles, el = 1 / 3, c = 1 amber 2 red 3 gold, pct 0-100, t ticks).
KIT_MANIFEST = _TOOLS / 'mboss_tk_fx_manifest.json'
KIT_PRESETS = {
    'slash_arc': ['r', 'yaw', 'pitch', 'roll', 'el'], 'spin_ring': ['r', 'el'], 'thrust_trail': ['len', 'el'],
    'dash_trail': ['len', 'el'], 'glint': [], 'core_flare': ['c'], 'core_burst': [], 'sky_arcs': ['r', 't'], 'bolt': [],
    'shock_ring': ['r'], 'ember_burst': [], 'blink_out': [], 'blink_in': [], 'wing_flare': [], 'cocoon': ['pct'],
    'cocoon_crack': [], 'nova_swell': ['t'], 'nova_flash': [], 'ignite_blade': [], 'dust_ring': ['r'], 'swap_fx': ['el'],
    'arrive_rift': [], 'ambient_dust': [], 'impact': ['el'], 'high_glint': [],
}
KIT_PROPS = ('crescent_h_1', 'crescent_h_3', 'crescent_v_1', 'crescent_v_3', 'feather')   # pj looks (@s = the display)
KIT_SOUNDS = (
    # intro / sequences (PLAN §3)
    'hang_amb', 'chain_step', 'cable_snap', 'body_land', 'heartbeat', 'servo', 'armor', 'bulb', 'cape_gust', 'hair',
    'visor_close', 'skull_ignite', 'sword_draw', 'blade_ignite', 'stance', 't1_split', 't1_flare', 't2_flare', 't2_dark',
    'death_knee', 'death_ash', 'arrive_rift',
    # fight (PLAN §4-5)
    'flare_tell', 'dash', 'slash_light', 'slash_heavy', 'spin', 'chop', 'glint', 'thrust', 'blink_out', 'blink_in',
    'leap', 'sky_arcs', 'plunge', 'charge_core', 'wave_release', 'wave_hit', 'air_swoop', 'dive', 'shock', 'high_glint',
    'swap_pyro', 'swap_electro', 'mantle_wrap', 'mantle_break', 'nova_swell', 'nova_blast', 'feather_fall',
    'core_backfire', 'stagger', 'step',
    # I1: S1K K1 / S4 R3 (the W1 charge)
    'wave_charge')
KIT_HUD = {'badge': ['el'], 'gauge': ['pct'], 'clear': []}    # badge el: 1 ◈불, 3 ◈번개, 9 ◈외피 (0 = none)
KIT_FIXED = ('card', 'cardx', 'look', 'clear', 'uninstall')     # fx/<name> (no args)
GATE_ICON_MODEL = 'rlk:mboss/tk_kit/gate_icon'


class _Kit:
    """Kit call lines. No-op ([]-like empty string) while the kit manifest is missing, so S3/S4 build and load without
    S1K's files (the Apep 'api.K stand-in' rule); names / args are checked against the contract either way."""

    def _on(self):
        return KIT_MANIFEST.exists()

    def p(self, name, **a):
        assert name in KIT_PRESETS, name
        assert sorted(a) == sorted(KIT_PRESETS[name]), f'kit preset {name} takes {KIT_PRESETS[name]}'
        if not self._on():
            return ''
        if not a:
            return f'function {NS}fx/p/{name}'
        return f'function {NS}fx/p/{name} {{' + ','.join(f'{k}:{int(v)}' for k, v in a.items()) + '}'

    def snd(self, name):
        assert name in KIT_SOUNDS, name
        return f'function {NS}fx/snd/{name}' if self._on() else ''

    def prop(self, name):
        assert name in KIT_PROPS, name
        return f'function {NS}fx/prop/{name}' if self._on() else ''

    def hud(self, name, **a):
        assert name in KIT_HUD and sorted(a) == sorted(KIT_HUD[name]), name
        if not self._on():
            return ''
        return f'function {NS}fx/hud/{name}' + ((' {' + ','.join(f'{k}:{int(v)}' for k, v in a.items()) + '}') if a else '')

    def fixed(self, name):
        assert name in KIT_FIXED, name
        return f'function {NS}fx/{name}' if self._on() else ''


K = _Kit()


def lines(*cmds):
    """Drop the empty kit stand-in lines."""
    return [c for c in cmds if c]

# =============================================================================================
# 9. Writer + pattern / service interface (contract §3)


class Writer:
    """Writes F:boss/tachy/<rel> for one owner; rel must start with one of `prefixes` (ownership is enforced)."""

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
    """One AI pattern. Runtime contract (all @s = the body, at it; clock #pt tk = played ticks since start, set to 0 by
    the core before `start` and +1 before each `tick`):
      p/<key>/start   begin (play the first clip, lock aims)        p/<key>/tick    one tick (k/<t> busy-tick files)
      p/<key>/cancel  remove every hazard / marker / prop of the pattern (rlk_tk_p_<key>), stop sounds; idempotent
      p/<key>/pause, resume (optional: redraw what pause removed)
    The pattern sets `#done tk 1` on its last tick; it never touches another pattern's state, the phase, the floors,
    the aura or the HUD (core-owned). Hits only through the framework (mboss/hz/*, pj/launch, grp_new) with the
    HITS tiers and elements; #hzQuiet 1 always."""
    key: str
    tid: int
    clips: tuple
    build: object                      # build(W: Writer) -> None
    pause: bool = False
    extra_objectives: tuple = ()       # none: patterns use fake players '#<key>_<x>' in objective tk
    notes: str = ''

    @property
    def name(self):
        return PATTERN_NAMES[self.key]

    @property
    def weights(self):
        return WEIGHTS.get(self.key, {})

    @property
    def core_window(self):
        return G3_WINDOWS.get(self.key)


@dataclass
class Service:
    """A sequence body (S2's seq.py): seq/<name>/{start,tick,cancel} on clock #sq tk (0 at start, +1 before tick); sets
    #sqdone tk 1 at its end. intro: the boss is rlk_mb_inv throughout (core); death: the core finishes the fight after
    #sqdone; t1 / t2: invulnerable, the core switches the phase after #sqdone; t2 starts the arena look job `abyss` at
    its 'dark' event through the framework (function rlk:mboss/arena/tk_lift/look/abyss)."""
    name: str
    clip: str
    build: object
    events: dict = field(default_factory=dict)


# owned output prefixes per stage (the top generator, tools/build_mboss_tachy.py (S3), creates one Writer each)
OWN = {
    'S3': ('spawn', 'intro_tick', 'tick', 'on_hit', 'aux_hit', 'incoming', 'pause', 'resume', 'death_start',
           'death_tick', 'cleanup', 'reload', 'bars', 'hz_vis', 'pj_end', 'test', 'uninstall', 'init', 'core/', 'ai/',
           'el/', 'mantle/', 'hud/', 'test/', 'rig_stub/') + tuple(f'p/{k}/' for k in MELEE),
    'S4': tuple(f'p/{k}/' for k in AIR + MANTLE),
    'S2seq': ('seq/',),
}
# rig/** (S2, build_tachy_rig.mjs) and fx/** kit paths (S1K, build_mboss_tk_fx.py) are written by their own generators.

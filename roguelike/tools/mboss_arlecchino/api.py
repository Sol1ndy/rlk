"""Frozen D0 contract of the 아를레키노 (Arlecchino, chapter-4 boss) module generator: every stage (S1 framework + arena +
routing, S1K kit, S2 rig + sequences, S3 core / AI / bond / phase 1, S4 phase 2) imports this file and never edits it. A
change goes through a request (S:ar/requests/<stage>.md) applied by the lead at integration. Prose version:
S:ar/contract.md; design: S:ar/PLAN.md (section numbers below refer to it).

Importing has no side effects (no files written). Units: Python helpers take blocks / ticks / degrees; the framework
boundary is tenths of a block and % of the base hit (atk 12 x dmgMul 150: raw = floor(0.18 x pct)).
`python3 tools/mboss_arlecchino/api.py --write-stub` (lead only) regenerates stub_rig_manifest.json from this file.
"""
from dataclasses import dataclass, field
from pathlib import Path
import inspect
import json
import sys

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
import mboss_lib as L  # noqa: E402

# =============================================================================================
# 1. Identity, registry entry, arena (PLAN §0, §8, §9)
ID = 'arlecchino'
N = 12
ROOT = L.fn_root_of(ID)                     # 'boss/arlecchino'
NS = f'rlk:{ROOT}/'
FDIR = L.FN / ROOT
REG = L.load_registry()
BOSS = dict(next(b for b in REG['boss'] if b['id'] == ID))
assert BOSS['kind'] == 'chapter' and BOSS['n'] == N and ROOT == 'boss/arlecchino' and BOSS['ch'] == [4], BOSS
assert not BOSS.get('px') and BOSS.get('shield') and BOSS['res'] == {'*': 10}, 'PLAN §0: no proxies, no Pyro resistance'
NAME, SUB, COLOR = BOSS['name'], BOSS['sub'], BOSS['color']      # 아를레키노 / 우인단 집행관 서열 4위 / #E0303A
# boss-bar titles per phase (mboss_lib.title); the footage's boss bar (ref/hud_bars_banner.jpg)
TITLE_P1 = ('「아를레키노」', '우인단 집행관 서열 4위')
TITLE_P2 = ('두 세계 불의 잔재', '페르엘')
TITLE_COLOR = {1: '#E0303A', 2: '#C8102E'}
GATE_LINES = ('추억: 빛과 그림자의 결별', '「아를레키노」', '영락한 폐허')   # cprep.arlecchino.gate (prep, S3)

AID = 'fl_ruins'
# The arena entry S1 adds to arenas{} (frozen here so S1K / S2 / S3 / S4 can work before it lands).
ARENA_SPEC = {'n': 4, 'theme': 'fl_ruins', 'ver': 1, 'cx': 760, 'cy': 201, 'cz': 8, 'r': 30, 'walk': 26, 'safe': 24,
              'start': {'x': 760.5, 'y': 201.0, 'z': 30.5, 'yaw': 180.0, 'pitch': 0.0},
              'box': {'x0': 712, 'y0': 190, 'z0': -40, 'x1': 808, 'y1': 250, 'z1': 56},
              'looks': ['day', 'crimson'], 'oob': {'y0': 198, 'y1': 230}}
if AID in REG.get('arenas', {}):
    _a = REG['arenas'][AID]
    assert all(_a.get(k) == v for k, v in ARENA_SPEC.items()), f'arenas.{AID} differs from the D0 contract'
ARENA = dict(ARENA_SPEC, aid=AID)
CX, CY, CZ = ARENA['cx'], ARENA['cy'], ARENA['cz']    # block corner = the arena axis (centre point 760.0 201 8.0)
WALK, SAFE = float(ARENA['walk']), float(ARENA['safe'])
MOVE_R = WALK - 1.5                                    # every end point (landing, dash, perch, hover) stays inside
AIR_MAX = 12.0                                         # highest feet height over the floor (Q6 hover); dome is higher
LOOK_DEFAULT, LOOK_P2 = 'day', 'crimson'
WISP_POSTS = ((0, 28.0), (150, 28.0), (210, 28.0))    # (compass bearing: 0 north (-z), 90 east; radius) of the 3 wisps


def arena_ready():
    """True once S1 has added arenas.fl_ruins (the framework then generates F:mboss/ar/fl_ruins/** and the arena generator
    F:mboss/arena/fl_ruins/**)."""
    return AID in REG.get('arenas', {})


def arena_look(look):
    """The look-job call (T 'dark' event: crimson; the framework's ensure restores day at the next fight). Empty until
    arena_ready(): no stage may reference another stage's functions before they exist (a missing function fails load)."""
    assert look in ARENA['looks'], look
    return f'function rlk:mboss/arena/{AID}/look/{look}' if arena_ready() else ''

# =============================================================================================
# 2. Damage, Bond of Life hazards (FN-1), hits (PLAN §4, §5.1)
# % of the base hit (mboss/hurt coefficient). P2 hits x P2_MUL (the wiki's P2 attack is x 1.4 of P1; tempered).
DMG = {'T1': 32, 'T2': 45, 'T3': 62, 'T4': 80}
P2_MUL = 120
PYRO = 1
EL_U = 1000                                            # 1U Pyro on every hit
C_PYRO, C_BOL = 1, 2                                   # kit colour arg c: orange-gold Pyro / crimson Bond-of-Life look


def dmg(tier, phase=1):
    """The mboss/hurt coefficient (%) of a tier in a fight phase (1 = P1, 2 = P2)."""
    v = DMG[tier]
    return v * P2_MUL // 100 if phase == 2 else v

# FN-1 (S1 implements in tools/build_mboss_core.py + mboss_lib; contract §3.1). Frozen names:
FN1_OPT = 'bol'                     # keyword of mboss_lib.hz_opts(...) and pj_opts(...): 1..100 (% of max HP bonded)
FN1_HZ_SCORE = ('#hzBol', 'mb')     # one-shot option score before mboss/hz/<shape> (reset after the hazard is made)
FN1_PJ_SCORE = ('#pjBol', 'mb')     # one-shot option score before mboss/pj/launch
FN1_IN = ('#mbBolIn', 'mb')         # copied by hz/hurt, pj/hit, hz/hurt_pm into mboss/hurt / pl_dot for one hit
FN1_RE = ('#mbBolRe', 'mb')         # module-owned multiplier % applied to a bol hit's raw damage (default 100)
FN1_EVENT = ('#mbHitBol', 'mb')     # after a landed bol hit = the option value; read and cleared by the module


def fn1_ready():
    """True once S1's mboss_lib accepts the bol option (until then S3 / S4 fall back as contract §3.1 says)."""
    return FN1_OPT in inspect.signature(L.hz_opts).parameters and FN1_OPT in inspect.signature(L.pj_opts).parameters

# HITS[pattern] = [(clip, event, shape, dims, tier, bol)]; bol = 1: a Bond-of-Life hit (FN-1 option bol=BOL_HIT);
# shapes (framework mboss/hz/* unless noted): sector(r, half_deg), disc(r), ring(r0, r), line(len, w), dash_line(w)
# (length = the dash), full() (whole arena, dash-dodgeable), pj_wheel(hr, speed, range) (returning vertical wheel),
# pj_cres(hr, speed, range) (returning crescent), pj_bolt(r) (falling feather, disc r at landing),
# pj_burst(hr, speed, r) (wheel exploding at the locked point), pm_disc(r, per_mille) (a disc whose hit is the FN-1-aware
# #hzPm pl_dot path, non-lethal: Q5B_FINAL_LETHAL), orb_discs(r, count, rim_r) (count discs on the rim, Q6),
# disc_ahead(r, dist) (a disc centred dist blocks ahead of her).
HITS = {
    'a2': [('a2', 'h1', 'sector', (4.2, 75), 'T2', 0), ('a2', 'h2', 'sector', (4.2, 75), 'T2', 0)],
    'a4': [('a4', 'h1', 'sector', (4.2, 75), 'T1', 0), ('a4', 'h2', 'sector', (4.2, 75), 'T1', 0),
           ('a4', 'h3', 'disc', (4.6,), 'T2', 0), ('a4', 'h4', 'sector', (3.6, 40), 'T3', 0),
           ('a4', 'h4', 'disc_ahead', (2.2, 2.6), 'T3', 0)],
    'a5': [('a5', 'h1', 'sector', (4.2, 75), 'T1', 0), ('a5', 'h2', 'sector', (4.2, 75), 'T1', 0),
           ('a5', 'h3', 'disc', (4.6,), 'T2', 0), ('a5', 'h4', 'sector', (3.6, 40), 'T3', 0),
           ('a5', 'h4', 'disc_ahead', (2.2, 2.6), 'T3', 0), ('a5', 'h5', 'disc', (4.8,), 'T2', 0)],
    'b1': [('b1', 'release', 'pj_wheel', (1.1, 1.4, 16.0), 'T2', 0)],
    'b2': [('b2', 'rel1', 'pj_wheel', (1.1, 1.4, 16.0), 'T2', 0), ('b2', 'rel2', 'pj_wheel', (1.1, 1.4, 16.0), 'T2', 0),
           ('b2', 'grab', 'disc', (2.2,), 'T2', 1)],
    'c1': [('c1', 'impact', 'disc', (3.6,), 'T3', 0), ('c1', 'impact', 'line', (6.0, 2.0), 'T3', 0)],
    'c2': [('c2', 'impact', 'disc', (3.6,), 'T3', 0), ('c2', 'impact', 'line', (6.0, 2.0), 'T3', 0),
           ('c2', 'wing', 'sector', (5.6, 70), 'T2', 1)],
    'd1': [('d1', 'go', 'dash_line', (2.0,), 'T2', 0), ('d1', 'hit', 'sector', (4.2, 70), 'T2', 0)],
    'd2': [('d2', 'go', 'dash_line', (2.0,), 'T2', 0), ('d2', 'hit', 'sector', (4.2, 70), 'T2', 0),
           ('d2', 'fhit', 'disc', (3.2,), 'T2', 0), ('d2', 'fhit', 'sector', (4.0, 60), 'T2', 0)],
    'e1': [('e1', 'sweep', 'sector', (5.2, 90), 'T2', 0), ('e1', 'spin', 'disc', (4.2,), 'T2', 0)],
    'f1': [('f1', 'hit1', 'full', (), 'T3', 1), ('f1', 'hit2', 'full', (), 'T3', 1)],
    'g1': [('g1', 'cross1', 'line', (28.0, 3.0), 'T2', 1), ('g1', 'cross2', 'line', (28.0, 3.0), 'T2', 1),
           ('g1', 'field', 'full', (), 'T2', 1)],
    'h1': [('h1', 'strike', 'line', (10.0, 2.0), 'T2', 1), ('h1', 'wing', 'sector', (6.0, 80), 'T2', 1),
           ('h1', 'sweep', 'sector', (5.0, 90), 'T2', 0)],
    'e70': [],
    'q0': [('q0_dive', 'impact', 'disc', (3.0,), 'T2', 1), ('q0_dive', 'blades', 'ring', (3.0, 7.0), 'T2', 1)],
    'q1': [('q1', 'h1', 'disc', (4.2,), 'T1', 0), ('q1', 'h2', 'sector', (4.5, 70), 'T2', 0),
           ('q1', 'h3', 'pj_cres', (1.0, 1.2, 12.0), 'T1', 0), ('q1', 'h4', 'sector', (4.4, 80), 'T1', 0),
           ('q1', 'h5', 'sector', (4.4, 80), 'T2', 0), ('q1', 'h6', 'pj_cres', (1.0, 1.2, 12.0), 'T1', 0)],
    'q2': [('q2', 'release', 'pj_burst', (1.1, 1.5, 2.2), 'T2', 0), ('q2', 'slash', 'sector', (4.5, 80), 'T2', 0)],
    'q3': [('q3', 'spin', 'disc', (4.6,), 'T2', 0)],
    'q4': [('q4_shot', 'fire', 'line', (30.0, 2.2), 'T3', 1)],
    'q5a': [('q5a', 'hit1', 'disc', (6.0,), 'T3', 1), ('q5a', 'hit2', 'ring', (6.0, 15.0), 'T3', 1),
            ('q5a', 'hit3', 'disc', (11.0,), 'T4', 1)],
    'q5b': [('q5b', f's{i}', 'disc', (5.5,), 'T1', 0) for i in range(1, 10)] + [('q5b', 'final', 'pm_disc', (7.5, 450), 'PM', 1)],
    'q6': [('q6', f'v{i}', 'pj_bolt', (1.6,), 'T1', 0) for i in range(1, 7)]
          + [('q6', 'impact', 'disc', (4.0,), 'T3', 1), ('q6', 'impact', 'orb_discs', (5.0, 8, 22.0), 'T3', 1)],
}
Q5B_FINAL_LETHAL = False                         # 450 per mille, leaves 1 HP (PLAN §6)
Q5B_SLASH_GROUP = 2                              # one hazard group per 2 rapid slashes (<= 5 landings)
DASH_LEN = {'d1': 14.0, 'd2': 14.0, 'e1': 14.0, 'q2': 14.0}         # max dash lengths (b)
LEAP_H = {'c1': 9.0, 'c2': 9.0, 'e1': 2.5, 'h1': 7.0, 'q0': 10.0, 'q4': 4.0, 'q6': 12.0}
TELL_MIN, TELL_BIG, COMBO_GAP = 12, 20, 10       # PLAN §5.1 (first visible motion -> hit; follow-ups apart)
# Floor decals: only these pattern keys may draw them (PLAN §1.5), each flashing DECAL_FLASH ticks before its hit tick.
DECALS = {'f1': ('flood', 'cracks'), 'g1': ('strip', 'rim_tint'), 'e70': ('pool',), 'q5a': ('ring_o', 'donut_o')}
DECAL_FLASH = 6
KB_CHAIN, KB_FINAL = 0, 3                        # knockback steps: chain hits / the last hit of a string

# =============================================================================================
# 3. Phases, floors, Bond of Life, 선혈의 충격 (PLAN §4, §7.1)
PH = {'intro': 0, 'p1a': 1, 'e70': 2, 'p1b': 3, 't': 4, 'p2': 5, 'death': 6}
PHASES = (64, 36)                                # registry phases: P1 pool / P2 pool (% of #mbTot)
FLOOR_E70_PCT = 70                               # % of the P1 pool: the hit reaching it schedules E70
FLOOR_T = 1                                      # HP floor of P1 after E70 (T at the next decision); P2 floor 0
RECOVER = {1: (16, 24), 2: (12, 18)}             # idle after a pattern (min, max) per fight phase (1 = P1, 2 = P2)
BOL_HIT = 6                                      # % max HP bonded by a bol hit
BOL_FORCE = 18                                   # % max HP of a forced bond (E70, f1, q5a / q5b)
BOL_REHIT_PCT = 250                              # #mbBolRe while her bond is on the player
BOL_DOT_PM, BOL_DOT_T = 10, 50                   # pl_dot per mille every T ticks while her bond is on (non-lethal)
BOL_HEAL_PM = 10                                 # her heal per landed bol hit, per mille of mhpM
BREAK_PM = {1: 150, 2: 125}                      # break true damage, per mille of mhpM (clamped above the floor)
STUN_T = 140
SHOCK_BONUS_PCT = 2                              # 선혈의 충격 outside a break window: true % of mhpM (clamped)
ORBS, ORB_R, ORB_MAX = 3, (6.0, 14.0), 3         # heal orbs per forced bond (existing 회복구슬, 10 % each)
# Break windows on the pattern clock #pt (the core tags the body rlk_kn_win inside them)
BREAK_WINDOWS = {'f1': (22, 159), 'q5a': (22, 121), 'q5b': (22, 96)}
FORCE_TICK = {'e70': 70, 'f1': 22, 'q5a': 22, 'q5b': 22}          # clip tick of the forced bond (the brand event)
# the normal-attack predicate (an execute prefix, read in on_hit before apply_mods; PLAN §4.3, Raiden's guard_hit rule)
NORMAL_HIT_IF = ('if score #icd tmp matches 1 unless score #skillDmg tmp matches 1 unless score #tfm tmp matches 1 '
                 'unless score #sub itv matches 1 unless score #trueDmg tmp matches 1')
BOND_CALLS = {'force': f'function {NS}bond/force', 'orbs': f'function {NS}bond/orbs'}   # S3 writes them; any executor
BANNER = '생명의 계약을 제거하고 일반 공격으로 「붉은 피의 연회」를 중단시키세요'   # the real game's line, adapted (PLAN §4.6)
BADGE = '◆선혈의 충격'

# =============================================================================================
# 4. AI (PLAN §7.2; S3 tunes values at review, the keys are frozen)
BANDS = (4.5, 11.0)                              # near <= 4.5 < mid <= 11 < far
REAR_DEG, REAR_DWELL = 60, (20, 30)              # rear = +-60 deg behind her; 20 of 30 ticks
FAR_DWELL = (14.0, 40)                           # > 14 b for 40 t -> gap closer (D / Q2 60 %, else C / Q4)
WALK_SPEED = 0.12
# groups the AI picks; the variant depends on the phase (P1a > 70 %, P1b <= 70 %); weights (near, mid, far)
GROUPS = {
    'A': {'p1a': ('a2',), 'p1b': ('a4', 'a5')}, 'B': {'p1a': ('b1',), 'p1b': ('b2',)},
    'C': {'p1a': ('c1',), 'p1b': ('c2',)}, 'D': {'p1a': ('d1',), 'p1b': ('d2',)}, 'E': {'p1b': ('e1',)},
    'G': {'p1b': ('g1',)}, 'H': {'p1b': ('h1',)}, 'F': {'p1b': ('f1',)},
    'Q1': {'p2': ('q1',)}, 'Q2': {'p2': ('q2',)}, 'Q3': {'p2': ('q3',)}, 'Q4': {'p2': ('q4',)},
    'Q5': {'p2': ('q5a', 'q5b')}, 'Q6': {'p2': ('q6',)}, 'Q0': {'p2': ('q0',)},
}
WEIGHTS = {
    'A': {'p1a': (60, 10, 0), 'p1b': (45, 10, 0)},
    'B': {'p1a': (10, 35, 35), 'p1b': (10, 30, 30)},
    'C': {'p1a': (10, 30, 30), 'p1b': (10, 25, 25)},
    'D': {'p1a': (0, 25, 40), 'p1b': (0, 20, 30)},
    'E': {'p1b': (0, 20, 25)}, 'G': {'p1b': (15, 20, 15)}, 'H': {'p1b': (10, 15, 20)},
    'Q1': {'p2': (60, 15, 0)}, 'Q2': {'p2': (10, 35, 40)}, 'Q4': {'p2': (0, 25, 40)}, 'Q6': {'p2': (10, 20, 25)},
}
COOLDOWN = {'A': 60, 'B': 160, 'C': 200, 'D': 140, 'E': 260, 'G': 420, 'H': 380,
            'Q1': 60, 'Q2': 160, 'Q3': 120, 'Q4': 300, 'Q6': 600}
SCHEDULE = {'F': {'first_after': ('e70', 240), 'every': 900, 'min_others': 3},
            'Q5': {'first_after': ('q0', 300), 'every': 900, 'min_others': 3}}
Q6_FIRST = 400                                   # ticks into P2 before the first Q6
Q3_CHANCE = 80                                   # % when the rear rule fires
A_FIVE_PCT = 50                                  # a5 instead of a4
Q4_SHOTS = {'base': 1, 'missed': 2, 'low_pct': (50, 3)}      # 2 if the first missed; 3 at <= 50 % of the P2 pool
Q0_TRIGGER = (1.5, 80)                           # player moved >= 1.5 b since T's end, or 80 t

# =============================================================================================
# 5. Pattern / service keys, ownership, test ids (contract §1)
P1 = ('a2', 'a4', 'a5', 'b1', 'b2', 'c1', 'c2', 'd1', 'd2', 'e1', 'f1', 'g1', 'h1', 'e70')   # S3: p1.py -> p/<key>/**
P2 = ('q0', 'q1', 'q2', 'q3', 'q4', 'q5a', 'q5b', 'q6')                                         # S4: p2.py -> p/<key>/**
SEQS = ('intro', 't_p2', 'death')                                                               # S2: seq.py -> seq/<name>/**
PATTERN_NAMES = {'a2': '사형장으로의 초대', 'a4': '사형장으로의 초대', 'a5': '사형장으로의 초대',
                 'b1': '붉은 달의 낫', 'b2': '붉은 달의 낫', 'c1': '불꽃 도약', 'c2': '불꽃 도약',
                 'd1': '블러드 돌진', 'd2': '블러드 돌진', 'e1': '와리가리 베기', 'f1': '붉은 피의 연회',
                 'g1': '죽음의 칼날', 'h1': '연옥 그림자 분신', 'e70': '재가 된 만상', 'q0': '낙하 공격',
                 'q1': '사형장으로의 초대', 'q2': '불꽃이 타오르는 낫', 'q3': '붉은 죽음의 무도회',
                 'q4': '떠오르는 재액의 달', 'q5a': '붉은 피의 연회 · 형벌의 핏값', 'q5b': '붉은 피의 연회 · 붉은 피의 사형',
                 'q6': '핏빛 연회'}
TEST_IDS = {1: 'a2', 2: 'a5', 13: 'a4', 3: 'b1', 4: 'b2', 5: 'c1', 6: 'c2', 7: 'd1', 8: 'd2', 9: 'e1', 10: 'f1',
            11: 'g1', 12: 'h1', 20: 'e70', 21: 'forced bond', 22: 'heal 30 %', 23: 'arm shock', 24: 'break now',
            25: 'intro replay', 26: 'transition', 27: 'death', 28: 'heal orbs', 29: 'stun', 30: 'phase 1b',
            31: 'phase 2 (skip T)', 41: 'q0', 42: 'q1', 43: 'q2', 44: 'q3', 45: 'q4 (3 shots)', 46: 'q5a', 47: 'q5b',
            48: 'q6', 80: 'HP = next floor + 1', 99: 'hold'}
TEST_HELP_NAMES = {1: '사형장으로의 초대 (2타)', 2: '사형장으로의 초대 (5타)', 13: '사형장으로의 초대 (4타)',
                   3: '붉은 달의 낫', 4: '붉은 달의 낫 (손아귀)', 5: '불꽃 도약', 6: '불꽃 도약 (날개)',
                   7: '블러드 돌진', 8: '블러드 돌진 (추가타)', 9: '와리가리 베기', 10: '붉은 피의 연회',
                   11: '죽음의 칼날', 12: '연옥 그림자 분신', 20: '재가 된 만상', 21: '생명의 계약 강제 부여',
                   22: '체력 30% 회복', 23: '선혈의 충격 얻기', 24: '연회 파훼', 25: '등장 다시', 26: '2페이즈 전환',
                   27: '쓰러짐', 28: '회복구슬', 29: '그로기', 30: '체력 70% 이하로', 31: '2페이즈로', 41: '낙하 공격',
                   42: '사형장으로의 초대 (쌍낫)', 43: '불꽃이 타오르는 낫', 44: '붉은 죽음의 무도회',
                   45: '떠오르는 재액의 달', 46: '형벌의 핏값', 47: '붉은 피의 사형', 48: '핏빛 연회',
                   80: '체력 = 다음 바닥 + 1', 99: '멈춤'}
LOCK_IDS = tuple(range(1, 14)) + tuple(range(41, 49))
# Dialog subtitles (the wiki's pattern lines; kit fx/hud/line {id}); LINE_OF: lines a cast picks from (random)
LINES = {
    1: '두려운가? 아니면 두려워할 용기조차 없는 건가?', 2: '피어오르는 불꽃으로.', 3: '도망칠 수 없다.',
    4: '뭘 망설이는 거지?', 5: '힘 뺄 거 없어. 도망칠 수 없을 테니.', 6: '어둠이 내려앉는 순간 멸망이 도래한다.',
    7: '카운트 다운이 시작됐군.', 8: '네가 몸을 기댈 거미줄이 있을까.', 9: '도망치기 바쁜 꼴이 가엾게 떠는 짐승 같구나.',
    10: '연옥의 그림자를 보아라.', 11: '보아라, 모든 선의를 불태울 칼날을!', 12: '이제 네 본심을 볼 수 있겠군.',
    13: '형벌을 시작하지.', 14: '일몰은 그저, 모든 것의 시작일 뿐.', 15: '해와 달은 결국 지고 파멸은 계속해서 찾아오지!',
    16: '부질없는 저항이군!', 17: '희망은 사라진지 오래다!',
}
LINE_OF = {'intro': (1,), 'c1': (2,), 'c2': (2,), 'd1': (3,), 'd2': (3,), 'a2': (4,), 'a4': (4,), 'a5': (4,),
           'e70': (5,), 'f1': (6, 7, 8), 'g1': (9,), 'h1': (10,), 't_p2': (11,), 'q5a': (12, 13, 14),
           'q5b': (12, 13, 14), 'q6': (15, 16, 17)}

# =============================================================================================
# 6. Scores, tags, storage (contract §2). Module state = fake players in objective `kn` (owned by S3's init /
# uninstall); each stage may only add fake players with its own prefix: core `#<name>` from CORE_FP, a pattern
# `#<key>_<x>`, seq `#sq_<x>`. Rig objectives knRig* (S2), kit objectives knFx* (S1K).
OBJ = 'kn'
CORE_FP = ('#ph', '#pat', '#pt', '#done', '#clk', '#rigc', '#rigt', '#sq', '#sqdone', '#bonded', '#given', '#shock',
           '#shk_hit', '#brk', '#stun', '#stun_t', '#e70', '#win', '#sch_f', '#sch_q5', '#lines', '#last', '#last2',
           '#rear', '#far', '#dec', '#rec', '#fl', '#tst', '#lock', '#dot_t', '#orbs', '#q0_ok')
TAGS = {'part': 'rlk_kn_part', 'prop': 'rlk_kn_prop', 'anchor': 'rlk_kn_anchor', 'fx': 'rlk_kn_fx',
        'orb': 'rlk_kn_orb', 'pat': 'rlk_kn_p', 'win': 'rlk_kn_win', 'stun': 'rlk_kn_stun'}   # pattern markers: + rlk_kn_p_<key>
STORAGE = 'rlk:kn'                     # keys: core.* (S3), rig.* (S2), fx.* (S1K), p2.* (S4), seq.* (S2)
RIG_UUID = '524c4b4d-4b4e-4100-8000-0000000000{:02x}'   # part NN 00..25, shadow 40

# =============================================================================================
# 7. Rig contract (PLAN §2; S2 implements, S3/S4 call)
SIZE = 1.4                                       # x the player avatar (PLAN §0.1 Q3, accepted)
HEIGHT, HIP_Y = 2.8, 1.05
BODY = ('head', 'body', 'right_arm', 'right_forearm', 'left_arm', 'left_forearm', 'right_leg', 'right_shin',
        'left_leg', 'left_shin')
LEGS = tuple(f'leg_{i}{s}' for i in range(1, 7) for s in 'ab')
PARTS = BODY + ('scythe_r', 'scythe_l') + LEGS + ('cup', 'saucer')
assert len(PARTS) == 26
PARENTS = {'head': 'body', 'body': None, 'right_arm': 'body', 'right_forearm': 'right_arm', 'left_arm': 'body',
           'left_forearm': 'left_arm', 'right_leg': 'body', 'right_shin': 'right_leg', 'left_leg': 'body',
           'left_shin': 'left_leg', 'scythe_r': 'right_forearm', 'scythe_l': 'left_forearm', 'cup': 'right_forearm',
           'saucer': 'left_forearm', **{f'leg_{i}a': 'body' for i in range(1, 7)},
           **{f'leg_{i}b': f'leg_{i}a' for i in range(1, 7)}}
# models: P1 body parts are the player avatar's existing item models (never copied); P2 the S2-built skin_33 parts
AVATAR_MODEL = {p: f'rlk:player_motion/arle/{p}' for p in BODY}
P2_MODEL = {p: f'rlk:mboss/arlecchino/p2/{p}' for p in BODY}
SCYTHE_MODEL = 'rlk:player_motion/weapons/scythe'
ARM_LAYOUT = {'p1': 'slim', 'p2': 'classic'}     # skin_33 has 4-px arms (PLAN §2.1)
LOOKS = {'form': ('p1', 'p2'), 'wings': ('off', 'open'), 'weapon_r': ('hand', 'gone', 'world'),
         'weapon_l': ('hand', 'gone', 'world'), 'glow': ('normal', 'crimson'), 'props': ('none', 'tea')}
ANCHORS = ('hand_r', 'hand_l', 'blade_r', 'blade_l', 'palm_r', 'chest', 'spine')
# rig/<call> functions (all @s = the body = the anchor, at its feet)
RIG_CALLS = ['init', 'spawn', 'spawn_hidden', 'tick', 'kill', 'uninstall', 'flash', 'state/normal', 'state/hidden',
             'face/player', 'face/track'] + [f'look/{ch}/{v}' for ch, vs in LOOKS.items() for v in vs] \
    + [f'anchor/{a}' for a in ANCHORS]
RIG_MACRO_CALLS = {'face/set': ['yaw']}

# CLIPS[name] = (len, loop (from, to) or None, {event: tick}); play/<name> and start/<name> exist for each.
CLIPS = {
    'idle': (40, (0, 40), {}),
    'walk': (24, (0, 24), {'step1': 0, 'step2': 12}),
    'strafe_l': (20, (0, 20), {}), 'strafe_r': (20, (0, 20), {}),
    'idle2': (40, (0, 40), {}),
    'walk2': (24, (0, 24), {'step1': 0, 'step2': 12}),
    'strafe2_l': (20, (0, 20), {}), 'strafe2_r': (20, (0, 20), {}),
    'backstep': (12, None, {'land': 10}),
    'flinch': (6, None, {}),
    'brk': (20, None, {'hit': 0}),
    'stun': (140, (20, 120), {'kneel': 10, 'rise': 120}),
    'stun2': (140, (20, 120), {'kneel': 10, 'rise': 120}),
    'intro': (150, None, {'sip': 14, 'lower': 22, 'embers': 34, 'flee': 35, 'reach': 44, 'vortex': 52, 'form': 60,
                          'blade': 70, 'hold': 72, 'title': 80, 'twirl': 92, 'ring': 98, 'twirl_end': 104, 'flip': 110,
                          'stance': 116, 'set': 120, 'beat': 126, 'music': 136, 'push': 140, 'end': 150}),
    'a2': (46, None, {'raise': 0, 'h1': 14, 'h2': 24, 'end': 46}),
    'a4': (100, None, {'h1': 14, 'h2': 24, 'h3': 44, 'h4': 64, 'end': 100}),
    'a5': (124, None, {'h1': 14, 'h2': 24, 'h3': 44, 'h4': 64, 'h5': 84, 'end': 124}),
    'b1': (60, None, {'raise': 0, 'spin': 10, 'release': 28, 'catch': 52, 'end': 60}),
    'b2': (130, None, {'spin': 10, 'rel1': 28, 'spin2': 40, 'rel2': 58, 'reach': 76, 'lock': 80, 'grab': 96, 'end': 130}),
    'c1': (80, None, {'crouch': 0, 'jump': 8, 'apex': 18, 'lock': 44, 'dive': 48, 'impact': 54, 'end': 80}),
    'c2': (140, None, {'crouch': 0, 'jump': 8, 'apex': 18, 'lock': 44, 'dive': 48, 'impact': 54, 'wing_open': 84,
                       'wing': 90, 'end': 140}),
    'd1': (56, None, {'flare': 0, 'go': 26, 'hit': 30, 'end': 56}),
    'd2': (76, None, {'flare': 0, 'go': 26, 'hit': 30, 'fhit': 46, 'end': 76}),
    'e1': (112, None, {'rise': 0, 'zig1': 16, 'zig2': 26, 'zig3': 36, 'zig4': 46, 'zig5': 56, 'lock': 64, 'go': 70,
                       'sweep': 76, 'spin': 92, 'end': 112}),
    'f1': (232, None, {'raise': 0, 'brand': 22, 'centre': 40, 'arms': 100, 'flood': 110, 'hit1': 160, 'wings': 166,
                       'hit2': 196, 'end': 232}),
    'g1': (140, None, {'plant': 0, 'blades': 6, 'cross1': 34, 'relock': 40, 'cross2': 62, 'rim': 70, 'field': 104,
                       'end': 140}),
    'h1': (124, None, {'leap': 0, 'perch': 10, 'clones': 20, 'strike': 34, 'drop': 64, 'wing': 72, 'sweep': 84,
                       'end': 124}),
    'e70': (110, None, {'glow': 0, 'rise': 20, 'pool': 40, 'brand': 70, 'wings': 74, 'land': 96, 'end': 110}),
    't_p2': (180, None, {'kneel': 0, 'pillar': 24, 'dark': 50, 'rise': 70, 'swap': 90, 'legs1': 110, 'legs2': 116,
                         'legs3': 122, 'scythes': 130, 'title': 140, 'launch': 150, 'end': 180}),
    'q0_hover': (40, (0, 40), {}),
    'q0_dive': (40, None, {'go': 0, 'impact': 20, 'blades': 28, 'end': 40}),
    'q1': (124, None, {'h1': 14, 'h2': 30, 'h3': 46, 'h4': 66, 'h5': 82, 'h6': 100, 'end': 124}),
    'q2': (70, None, {'windup': 0, 'release': 20, 'go': 34, 'slash': 42, 'end': 70}),
    'q3': (36, None, {'whip': 0, 'spin': 14, 'end': 36}),
    'q4_up': (20, None, {'top': 20}),
    'q4_shot': (50, None, {'aim': 0, 'lock': 20, 'fire': 26, 'end': 50}),
    'q4_land': (16, None, {'land': 12}),
    'q5a': (180, None, {'raise': 0, 'brand': 22, 'ring1': 60, 'hit1': 95, 'donut': 100, 'hit2': 121, 'ring3': 130,
                        'hit3': 158, 'end': 180}),
    'q5b': (136, None, {'raise': 0, 'brand': 22, 'x': 26, 'mark': 50, **{f's{i}': 53 + 3 * i for i in range(1, 10)},
                        'final': 96, 'end': 136}),
    'q6': (200, None, {'fly': 0, 'gone': 20, 'moon': 30, **{f'v{i}': 40 + 10 * i for i in range(1, 7)}, 'orbs': 110,
                       'toss': 125, 'lock': 140, 'dive': 160, 'impact': 168, 'end': 200}),
    'death': (110, None, {'stop': 0, 'lower': 10, 'fade': 30, 'stand': 50, 'flames': 70, 'gone': 96, 'wisps': 100,
                          'end': 110}),
}
CLIP_ORDER = tuple(CLIPS)                        # clip ids (manifest order) = the index here
# the form a clip is authored for (None = any form: the rig plays it in the stored form)
CLIP_FORM = {k: 'p1' for k in ('idle', 'walk', 'strafe_l', 'strafe_r', 'stun', 'intro', 'a2', 'a4', 'a5', 'b1', 'b2',
                               'c1', 'c2', 'd1', 'd2', 'e1', 'f1', 'g1', 'h1', 'e70', 't_p2')}
CLIP_FORM.update({k: 'p2' for k in ('idle2', 'walk2', 'strafe2_l', 'strafe2_r', 'stun2', 'q0_hover', 'q0_dive', 'q1',
                                    'q2', 'q3', 'q4_up', 'q4_shot', 'q4_land', 'q5a', 'q5b', 'q6', 'death')})
CLIP_FORM.update({'backstep': None, 'flinch': None, 'brk': None})

REAL_MANIFEST = _TOOLS / 'arlecchino_rig_manifest.json'                       # S2 writes it
STUB_MANIFEST = Path(__file__).resolve().parent / 'stub_rig_manifest.json'   # D0


def stub_manifest():
    """The D0 stub manifest (the lead writes it with --write-stub; S2's real manifest adds transforms, budgets, sprites)."""
    return {
        'schema': 1, 'id': ID, 'source': 'stub',
        '_doc': ('D0 stub of tools/arlecchino_rig_manifest.json (S2 writes the real one with the same parts, clips, '
                 'events, looks, anchors, calls; the real one adds transforms, budgets, sprites). Generated from '
                 'tools/mboss_arlecchino/api.py.'),
        'height': HEIGHT, 'hip_y': HIP_Y, 'size': SIZE, 'uuid': RIG_UUID,
        'parts': [{'name': p, 'nn': i, 'parent': PARENTS[p],
                   'model': {'p1': AVATAR_MODEL.get(p, SCYTHE_MODEL if p.startswith('scythe') else None),
                             'p2': P2_MODEL.get(p, SCYTHE_MODEL if p.startswith('scythe') else None)}}
                  for i, p in enumerate(PARTS)],
        'clips': {k: {'id': i, 'len': v[0], 'loop': list(v[1]) if v[1] else None, 'events': v[2], 'form': CLIP_FORM[k]}
                  for i, (k, v) in enumerate(CLIPS.items())},
        'looks': {k: list(v) for k, v in LOOKS.items()}, 'arm_layout': ARM_LAYOUT, 'anchors': list(ANCHORS),
        'calls': RIG_CALLS, 'macro_calls': RIG_MACRO_CALLS,
    }


def rig_manifest():
    """S2's manifest when it exists, else the D0 stub; both must carry exactly the CLIPS table."""
    m = json.loads((REAL_MANIFEST if REAL_MANIFEST.exists() else STUB_MANIFEST).read_text(encoding='utf-8'))
    check_manifest(m)
    return m


def check_manifest(m):
    assert m.get('schema') == 1 and m.get('id') == ID, 'arlecchino rig manifest: schema 1, id arlecchino'
    got = {k: (v['len'], tuple(v['loop']) if v.get('loop') else None, v.get('events', {}), v.get('form'))
           for k, v in m['clips'].items()}
    for k, (ln, lp, ev_, *_r) in CLIPS.items():
        assert k in got, f'rig manifest: clip {k} missing'
        assert got[k] == (ln, lp, ev_, CLIP_FORM[k]), f'rig manifest: clip {k} = {got[k]}, contract {(ln, lp, ev_, CLIP_FORM[k])}'
    assert [p['name'] for p in m['parts']] == list(PARTS), 'rig manifest: parts / order differ from the contract'
    assert sorted(m.get('anchors', [])) == sorted(ANCHORS), 'rig manifest: anchors differ from the contract'
    return True


def rig_real():
    return REAL_MANIFEST.exists()


def rig(call, **macro):
    """The rig call line. While S2's manifest is missing the core (S3) generates the stand-in rig_stub/** with the same
    call names (every play/<clip> sets #rigc kn to the clip id for tests; no visuals)."""
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
# 8. Kit contract (S1K implements in tools/build_mboss_kn_fx.py; contract §3.3). Presets with args are macros (values in
# tenths for lengths, degrees for angles, c = 1 Pyro orange-gold / 2 crimson BoL, t ticks, on 0/1, id = LINES key).
KIT_MANIFEST = _TOOLS / 'mboss_kn_fx_manifest.json'
KIT_PRESETS = {
    'slash_arc': ['r', 'yaw', 'pitch', 'roll', 'c'], 'spin_ring': ['r', 'c'], 'twirl_ring': [], 'scythe_form': [],
    'embers_puff': [], 'wheel_trail': ['len'], 'dash_trail': ['len', 'c'], 'leap_flare': [], 'dive_streak': ['len'],
    'impact_burst': ['r', 'c'], 'claw': ['r'], 'wing_burst': [], 'zig_streak': ['len'], 'brand_ring': [], 'brand_x': [],
    'threads': ['r'], 'thorns': ['r'], 'blast': ['r'], 'web': [], 'clone_trail': [], 'blade_rise': [], 'blade_burst': [],
    'shock_gain': [], 'shock_aura': [], 'shock_hit': [], 'break_burst': [], 'stun_motes': [], 'pillar': ['r'],
    'legs_burst': [], 'moon_flare': [], 'aim_line': ['len'], 'reticle': [], 'beam': ['len'], 'x_mark': [],
    'rapid_slash': [], 'final_burst': ['r'], 'feather_hit': [], 'orb_gather': [], 'orb_burst': ['r'],
    'death_flames': [], 'wisp_turn': ['c'], 'gate_flames': [], 'ambient_petals': [],
}
KIT_PROPS = {'wheel': [], 'crescent': [], 'feather': [], 'orb': [], 'blade': [], 'clone': [], 'wisp': ['c'],
             'moon_halo': []}                                            # @s = the projectile display / marker
KIT_DECALS = {'flood': ['r', 't'], 'cracks': ['r'], 'strip': ['len', 'w', 'yaw', 't'], 'rim_tint': ['r0', 'r', 't'],
              'pool': ['r', 't'], 'ring_o': ['r', 't'], 'donut_o': ['r0', 'r', 't']}
assert set(KIT_DECALS) == {d for ds in DECALS.values() for d in ds}
KIT_SOUNDS = (
    # intro / transition / death (PLAN §3)
    'tea_sip', 'wisp_chime', 'cup_embers', 'wisps_flee', 'ember_reach', 'scythe_vortex', 'scythe_form', 'blade_ignite',
    'intro_title', 'twirl', 'twirl_ring', 'flip', 'stance', 'heartbeat', 't_stagger', 't_pillar', 't_dark', 't_swap',
    't_legs', 't_scythes', 't_title', 't_launch', 'death_lower', 'death_flames', 'death_gone',
    # fight (PLAN §4-6)
    'step', 'swing_light', 'swing_heavy', 'spin', 'slam', 'wheel_spin', 'wheel_throw', 'wheel_catch', 'claw_reach',
    'claw_grab', 'leap', 'apex', 'dive', 'impact', 'wing_burst', 'wing_hit', 'dash_tell', 'dash', 'follow', 'zig',
    'sweep', 'brand', 'bond_gain', 'bond_tick', 'orb_spawn', 'flood', 'threads', 'blast', 'cracks', 'blade_rise',
    'cross_hit', 'rim', 'clone_launch', 'clone_hit', 'perch', 'shock_gain', 'shock_hit', 'break', 'stun', 'beam_aim',
    'beam_fire', 'x_carve', 'rapid', 'final', 'feather', 'orbs_gather', 'orbs_toss', 'orb_burst', 'fall_dive',
    'fall_impact', 'rear_whip', 'crescent_throw', 'moon')
KIT_HUD = {'badge': ['on'], 'banner': ['on'], 'line': ['id'], 'clear': []}
KIT_FIXED = ('card', 'cardx', 'look', 'clear', 'uninstall')     # fx/<name> (no args)
GATE_ICON_MODEL = 'rlk:mboss/kn_kit/gate_icon'


class _Kit:
    """Kit call lines. Empty while the kit manifest is missing, so S2 / S3 / S4 build and load without S1K's files (the
    Apep / Tachy 'api.K stand-in' rule); names / args are checked against the contract either way."""

    def _on(self):
        return KIT_MANIFEST.exists()

    def _call(self, sub, table, name, a):
        assert name in table, name
        assert sorted(a) == sorted(table[name]), f'kit {sub}{name} takes {table[name]}'
        if not self._on():
            return ''
        if not a:
            return f'function {NS}fx/{sub}{name}'
        return f'function {NS}fx/{sub}{name} {{' + ','.join(f'{k}:{int(v)}' for k, v in a.items()) + '}'

    def p(self, name, **a):
        return self._call('p/', KIT_PRESETS, name, a)

    def prop(self, name, **a):
        return self._call('prop/', KIT_PROPS, name, a)

    def decal(self, name, **a):
        return self._call('decal/', KIT_DECALS, name, a)

    def hud(self, name, **a):
        return self._call('hud/', KIT_HUD, name, a)

    def snd(self, name):
        assert name in KIT_SOUNDS, name
        return f'function {NS}fx/snd/{name}' if self._on() else ''

    def fixed(self, name):
        assert name in KIT_FIXED, name
        return f'function {NS}fx/{name}' if self._on() else ''


K = _Kit()


def lines(*cmds):
    """Drop the empty kit stand-in lines."""
    return [c for c in cmds if c]

# =============================================================================================
# 9. Writer + pattern / service interface (contract §3.4)


class Writer:
    """Writes F:boss/arlecchino/<rel> for one owner; rel must start with one of `prefixes` (ownership is enforced)."""

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
    """One AI pattern. Runtime contract (all @s = the body, at it; clock #pt kn = played ticks since start, set to 0 by
    the core before `start` and +1 before each `tick`):
      p/<key>/start   begin (play the first clip, lock aims)        p/<key>/tick    one tick (k/<t> busy-tick files)
      p/<key>/cancel  remove every hazard / marker / prop / decal of the pattern (rlk_kn_p_<key>), stop sounds; idempotent
      p/<key>/pause, resume (optional: redraw what pause removed)
    The pattern sets `#done kn 1` on its last tick; it never touches another pattern's state, the phase, the floors, the
    bond bookkeeping (only BOND_CALLS) or the HUD (core-owned). Hits only through the framework (mboss/hz/*, pj/launch,
    grp_new, pl_dot) with the HITS tiers (dmg(tier, phase)) and the FN-1 bol option; #hzQuiet 1 except DECALS keys."""
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
    def window(self):
        return BREAK_WINDOWS.get(self.key)


@dataclass
class Service:
    """A sequence body (S2's seq.py): seq/<name>/{start,tick,cancel} on clock #sq kn (0 at start, +1 before tick); sets
    #sqdone kn 1 at its end. intro: the boss is rlk_mb_inv throughout (core), title at 'title', push ring at 'push';
    t_p2: invulnerable + cine, the arena look job `crimson` at its 'dark' event (arena_look), the title at 'title'; the
    core does repool / music / the phase switch after #sqdone; death: the core finishes the fight after #sqdone."""
    name: str
    clip: str
    build: object
    events: dict = field(default_factory=dict)


# owned output prefixes per stage (the top generator, tools/build_mboss_arlecchino.py (S3), creates one Writer each)
OWN = {
    'S3': ('spawn', 'intro_tick', 'tick', 'on_hit', 'aux_hit', 'incoming', 'pause', 'resume', 'death_start',
           'death_tick', 'cleanup', 'reload', 'bars', 'hz_vis', 'pj_end', 'test', 'uninstall', 'prep', 'init',
           'core/', 'ai/', 'bond/', 'hud/', 'test/', 'rig_stub/', 'gate/') + tuple(f'p/{k}/' for k in P1),
    'S4': tuple(f'p/{k}/' for k in P2),
    'S2seq': ('seq/',),
}
# rig/** (S2, build_arlecchino_rig.mjs) and fx/** kit paths (S1K, build_mboss_kn_fx.py) are written by their own generators.

if __name__ == '__main__' and '--write-stub' in sys.argv:
    STUB_MANIFEST.write_text(json.dumps(stub_manifest(), ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('wrote', STUB_MANIFEST)

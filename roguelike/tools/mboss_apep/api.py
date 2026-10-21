"""Shared, stable API of the 아펩의 오아시스 파수꾼 (Apep) module generator (core <-> pattern / revival / org modules).

The binding contract is S:ap/ap_contract.md (section 0 = the day-0 interfaces; section 1 = this file, written by
AP-CORE); the framework names are S:az/contract/cm.md (AZ-CM + AP-FW, change note 22); the kit names
S:ap/ap_fx_api.md section 0. Module authors (p1 seq p3 aftermath revival org) import this module and never edit it:
new helpers, constants or table keys go through a request (S:ap/requests/<stage>.md, ap_contract 0.11). Frozen at AP-I1.

Units: Python helpers take blocks / ticks / degrees; the framework boundary is tenths of a block and % of the base hit
(atk 12 x dmgMul 150 / 10000: raw = floor(0.18 x pct), plan 9.2). Elements in #elem numbering (7 = Dendro).

Three parts may still be missing while the stages run in parallel; each has a marked stand-in that switches off by
itself when the real part lands (the build prints every one in use):
- the rig (wip/ap-rig, AP-I1 / AP-I2): the manifest is the real one ("schema": 1, "source": "rig") merged per clip with
  the stub of stub_rig.py (FALLBACKS = the clips taken from the stub, ids >= 1000; AP-I2 asserts none); the rig API is
  the real rig's where F:mboss/apep/rig/<fn> exists, else the stand-in AP:rig_stub/** (rig_fn, play_fn);
- the org manifest (wip/ap-org, AP-I1): T:mboss_apep_org_manifest.json when present, else stub_org.py's;
- the kit (wip/ap-fx, AP-I1): K = the kit's Python API (`import build_mboss_ap_fx`) when present, else KitStub with the
  ap_fx_api.md 0.10 signatures, whose every call is an empty module-owned function AP:kstub/<kit path>;
- the arena theme (wip/ap-arena, AP-I1): mboss_arena_ap_oasis when present, else _THEME_FALLBACK (ap_contract 0.6.3
  points; no props but the lush water tiles; the framework builds a stub arena, cm.md 6.3).
"""
from pathlib import Path
import json
import math
import re
import sys

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
import mboss_lib as L  # noqa: E402
from . import stub_rig as SR  # noqa: E402
from . import stub_org as SO  # noqa: E402

ID = 'apep'
NS = f'rlk:mboss/{ID}/'
N = 11
FDIR = L.FN / 'mboss' / ID

# =============================================================================================
# Registry entry and arena (plan 3.7; ap_contract 0.3.6; cm.md 2)
REG = L.load_registry()
BOSS = dict(next(b for b in REG['boss'] if b['id'] == ID))
assert BOSS.get('kind') == 'chapter' and BOSS['n'] == N, BOSS
ARENA = dict(L.arena_of(BOSS, REG))
AID = ARENA['aid']
assert AID == 'ap_oasis' and ARENA['n'] == 2, ARENA
CX, CY, CZ = ARENA['cx'], ARENA['cy'], ARENA['cz']          # 440 201 8: a block corner = the arena axis
WALK, SAFE = float(ARENA['walk']), float(ARENA['safe'])    # 26, 24
WALK_R = WALK - 0.7                                        # 25.3: locked ground targets (plan 7.3)
IDLE_R = 14.0                                              # the anchor at idle, both forms (plan 7.3 clamps)
BURST_R = {1: 18.0, 3: 16.0}                               # burst / emergence points per form
GLIDE_R = 16.0                                             # glides end inside this
LEASH_SPD = 0.13                                           # the module leash back to IDLE_R (b/t)
PARK_Y = 30.0                                              # the body parked 30 b above the centre in phase 2 (R10)
SINK_Y = -6.0                                              # the root under the floor while burrowed (R9)
HUSK_SCALE = float(BOSS.get('scale', 2.0))                 # the registry scale (the torso click shield)
HIDE_SCALE = 0.1                                           # the husk while hidden / parked (FN-13)
TOT_HP_REF = 7235                                          # plan 7.2 (L18, hp 290); the build prints the exact value
GOLD_HEX = BOSS['color']                                   # #C9C452: the speaker / name colour
P3_HEX = '#7FD68A'                                         # phase-3 name colour (lush)
HEART_HEX = '#EDCF63'                                      # the Heart gold (#buHpCol 10)
DIM_HEX = '#707070'
WARN_HEX = '#C36E5A'

# =============================================================================================
# The arena theme (ap_contract 0.6): POINTS / props / entrance from T:mboss_arena_ap_oasis.py when it exists, else
# this fallback (0.6.3 values; the lush water tiles only; no crystals, no pond props, no gate crystals).


def _bearing_point(r, b, y=201.0):
    return (round(440.0 + r * math.sin(math.radians(b)), 2), y, round(8.0 - r * math.cos(math.radians(b)), 2))


def _theme_fallback():
    org = [_bearing_point(12.0, 22.5 + 45 * k) for k in range(8)]
    nurt = [_bearing_point(7.0, 22.5 + 45 * k) for k in range(8)]
    water = [(float(x), 201.005, float(z)) for z in (-13, 1, 15, 29) for x in (419, 433, 447, 461)]
    points = {'spawn': (440.0, 201.0, 8.0, 0.0), 'centre': (440.0, 201.0, 8.0), 'heart': (440.0, 201.0, 8.0),
              'arrival': (440.5, 201.0, 24.5, 180.0), 'org_spawn': org, 'nurt_spawn': nurt,
              'ember_twig': (432.6, 203.5, -19.6), 'water_tiles': water, 'pond_props': [], 'bank_crystals': [],
              'trees': [], 'motes': []}
    lush = [{'name': f'water_{i % 4}_{i // 4}', 'kind': 'water_sheet', 'group': 'water', 'pos': p, 'yaw': 0.0,
             'pitch': 0.0, 'scale': 14.0, 'el': 7, 'uuid': i} for i, p in enumerate(water)]
    return {'POINTS': points, 'PROPS': {'withered': [], 'lush': lush}, 'GLYPHS': {}, 'GLOW': None}


_THEME_FALLBACK = _theme_fallback()


def _load_theme():
    mod = L.theme_module(ARENA.get('theme', AID))
    if mod is None:
        fb = _THEME_FALLBACK
        return dict(fb['POINTS']), {k: list(v) for k, v in fb['PROPS'].items()}, dict(fb['GLYPHS']), fb['GLOW'], True
    ent = mod.entrance_layout()
    props = {lk: list(mod.props(lk)) for lk in ARENA['looks']}
    return dict(mod.POINTS), props, dict(ent.get('glyphs') or {}), ent.get('stele_glow'), False


POINTS, PROPS, ENTRANCE_GLYPHS, ENTRANCE_GLOW, THEME_STUBBED = _load_theme()
LOOKS = list(ARENA['looks'])                               # ['withered', 'lush']
PROP_INTS = [1380731725, 1095778560, -2147483648]          # arena-prop UUID block 524c4b4d-4150-4100-8000-…
PROP_BLOCK = '524c4b4d-4150-4100-8000-0000000000'
CENTRE = tuple(float(v) for v in POINTS['centre'][:3])
ORG_SPAWN = [tuple(p) for p in POINTS['org_spawn']]
NURT_SPAWN = [tuple(p) for p in POINTS['nurt_spawn']]
EMBER_TWIG = tuple(POINTS['ember_twig'])

# =============================================================================================
# The rig manifest (ap_contract 0.4): the real one (schema 1, source rig) merged per clip with the stub (ids >= 1000)
MANIFEST = _TOOLS / 'mboss_apep_rig_manifest.json'
STUB_MANIFEST = Path(__file__).resolve().parent / 'stub_rig_manifest.json'
_REAL_RAW = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else None
REAL_MAN = isinstance(_REAL_RAW, dict) and _REAL_RAW.get('schema') == 1 and _REAL_RAW.get('source') == 'rig'
STUB = SR.build_rig()


def merge(real, stub):
    """ap_contract 0.4.1 / cm.md 9.2: every clip of the real rig manifest, stub clips (ids >= 1000) only for the names
    it lacks; the globals (proxies uuids states capsules runtime + every Apep extra) from the real file when present."""
    import copy
    if real is None:
        m = copy.deepcopy(stub)
        return m, [c['name'] for c in stub['clips']]
    m = copy.deepcopy(real)
    have = {c['name'] for c in real.get('clips', [])}
    fb = [c for c in stub['clips'] if c['name'] not in have]
    m['clips'] = list(m.get('clips', [])) + copy.deepcopy(fb)
    m['fallbacks'] = [c['name'] for c in fb]
    for k in ('stances', 'hands', 'park', 'states', 'capsules', 'proxies', 'flash_groups', 'looks', 'rest_anchors'):
        m.setdefault(k, copy.deepcopy(stub[k]))
    return m, [c['name'] for c in fb]


MAN, FALLBACKS = merge(_REAL_RAW if REAL_MAN else None, STUB)
CLIPS = {c['name']: c for c in MAN['clips'] if not c['name'].startswith('dbg_')}
CLIP_NAMES = [c['name'] for c in STUB['clips']]
assert set(CLIP_NAMES) <= set(CLIPS), sorted(set(CLIP_NAMES) - set(CLIPS))
ids = [c['id'] for c in MAN['clips']]
assert len(set(ids)) == len(ids), 'two clips of the merged manifest share an id (cm.md 9.2)'
REAL_CLIPS = {c['name'] for c in (_REAL_RAW or {}).get('clips', [])} if REAL_MAN else set()
EV_FALLBACKS = []

RIG_DIR = FDIR / 'rig'
REAL_RIG = (RIG_DIR / 'spawn.mcfunction').exists()
RIG_STUBBED = set()


def rig_fn(name):
    """Full id of a rig API function (ap_contract 0.4.9): the real rig's when it exists, else the stand-in's."""
    if (RIG_DIR / (name + '.mcfunction')).exists():
        return f'{NS}rig/{name}'
    if REAL_RIG:
        RIG_STUBBED.add(name)
    return f'{NS}rig_stub/{name}'


def play_fn(clip):
    assert clip in CLIPS, clip
    if clip in REAL_CLIPS and (RIG_DIR / 'play' / (clip + '.mcfunction')).exists():
        return f'{NS}rig/play/{clip}'
    return f'{NS}rig_stub/play/{clip}'


def rig_tick_lines():
    """The rig tick (last in the module tick): the real rig's tick (+ the stand-in chain while a clip falls back), or the
    stand-in's."""
    if REAL_RIG:
        return [f'function {NS}rig/tick'] + ([f'function {NS}rig_stub/chain'] if FALLBACKS else [])
    return [f'function {NS}rig_stub/tick']


def stub_rig_needed():
    return (not REAL_RIG) or bool(FALLBACKS) or bool(RIG_STUBBED)


def fallback_list():
    return {'clips': sorted(FALLBACKS), 'events': sorted(set(EV_FALLBACKS)), 'rig_functions': sorted(RIG_STUBBED)}


def ev(clip, event):
    """Played tick of a clip event (= the pattern clock tick when the clip starts at clock 0)."""
    return CLIPS[clip]['events'][event]


def ev_or(clip, event, default):
    e = CLIPS.get(clip, {}).get('events', {})
    if event in e:
        return e[event]
    EV_FALLBACKS.append((clip, event, default))
    return default


def clip_len(clip):
    return CLIPS[clip]['len']


def clip_id(clip):
    return CLIPS[clip]['id']


def anchor(clip, event, point):
    """A named local point (x = s left, y up, z = f forward; blocks from the anchor) at a clip event (0.4.5)."""
    return tuple(float(v) for v in CLIPS[clip]['anchors'][event][point])


def track(clip, name):
    """Per-tick local points (tail_root / tail_tip), one per played tick, before the yaw schedule."""
    return [tuple(float(v) for v in p) for p in CLIPS[clip]['tracks'][name]]


def yaw_at(clip, t):
    y = CLIPS[clip].get('yaw')
    if not y:
        return 0.0
    return float(y[max(0, min(len(y) - 1, int(t)))])


def px_sets(clip):
    """[[t, set]] of a clip (the framework px set from that tick; the core applies them, decision 0.11.2)."""
    return [list(x) for x in CLIPS[clip].get('px_sets') or []]


def stance_of(clip):
    st = CLIPS[clip].get('stance') or {'start': 'CROUCH', 'end': 'CROUCH'}
    return st['start'], st['end']


def hidden_spans(clip):
    return [tuple(h[:2]) for h in CLIPS[clip].get('hidden') or []]


def px_at(clip, t, proxy):
    """[x, z, top] of a proxy at played tick t (lerp between the manifest keys)."""
    keys = sorted((int(k), v) for k, v in CLIPS[clip]['px']['keys'].items())
    if t <= keys[0][0]:
        return tuple(keys[0][1][proxy])
    for (t0, a), (t1, b) in zip(keys, keys[1:]):
        if t <= t1:
            u = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
            return tuple(x + (y - x) * u for x, y in zip(a[proxy], b[proxy]))
    return tuple(keys[-1][1][proxy])


def rt(clip, t_authored):
    """The played tick of an authored tick (the clip's RETIME knots; identity without knots)."""
    k = CLIPS[clip].get('retime') or []
    if not k:
        return int(round(t_authored))
    for (a0, p0), (a1, p1) in zip(k, k[1:]):
        if t_authored <= a1:
            return int(round(p0 + (p1 - p0) * (t_authored - a0) / (a1 - a0)))
    return int(k[-1][1])


# Proxies, px sets, stances, capsules (ap_contract 0.4.6-0.4.7; data, never typed by hand in pattern code)
PX_LAYOUT = list(MAN['proxies']['layout'])
PX_NAMES = [p['name'] for p in PX_LAYOUT]
PX_FLASH = {k + 1: p['flash'] for k, p in enumerate(PX_LAYOUT)}            # mbPart -> flash group
FLASH_GROUPS = tuple(MAN['flash_groups'])
STATES = tuple(MAN['states'])                                              # the 8 px sets
PX_ID = {name: i for i, name in enumerate(STATES)}
HIDDEN_SETS = ('burrowed', 'parked')                                       # husk 0.1 + rlk_mb_noshield (FN-13, R10)
PUSH_SETS = ('p1', 'p3u', 'p3c')                                           # the body push only in these (0.4.6)
STANCE = {'CROUCH': 0, 'UPRIGHT': 1}
STANCE_SET = MAN['stances']['px_set']                                      # {p1: {CROUCH: p1}, p3: {CROUCH: p3c, UPRIGHT: p3u}}
REST = {s: {k: tuple(float(v) for v in p) for k, p in d.items()} for s, d in MAN['stances']['rest_anchors'].items()}
TORSO_HW = MAN['stances']['torso_hw']
HAND_SETS = tuple(MAN['hands']['ids'])
YAW_CLIPS = tuple(c for c in CLIP_NAMES if CLIPS[c].get('yaw'))

# =============================================================================================
# The org manifest (ap_contract 0.5): real (source "org") when present, else the stub
ORG_MANIFEST = _TOOLS / 'mboss_apep_org_manifest.json'
ORG_STUB_FILE = Path(__file__).resolve().parent / 'stub_org_manifest.json'
_ORG_RAW = json.loads(ORG_MANIFEST.read_text(encoding='utf-8')) if ORG_MANIFEST.exists() else None
ORG_STUBBED = not (isinstance(_ORG_RAW, dict) and _ORG_RAW.get('source') == 'org')
ORG = SO.build_org() if ORG_STUBBED else _ORG_RAW
KINDS = {k: v for k, v in ORG['kinds'].items()}                            # basic nurt guard nest destr pred
KIND_ID = {k: v['id'] for k, v in KINDS.items()}                           # apK 1..6
KIND_KEY = {v: k for k, v in KIND_ID.items()}
KIND_KO = {k: v['name'] for k, v in KINDS.items()}
ORG_CLIPS = {}
for _owner, _rec in list(ORG['kinds'].items()) + list(ORG['objects'].items()):
    for _c in _rec.get('clips', []):
        ORG_CLIPS[_c['name'] if _c['name'] not in ORG_CLIPS else f'{_owner}:{_c["name"]}'] = dict(_c, owner=_owner)
FOOTPRINT = ORG['objects']['heart']['footprint']
OBJ_INTS = list(ORG['uuids']['ints'])
OBJ_BLOCK = ORG['uuids']['block']


def org_clip(owner, name):
    """An org clip record of an owner (kind key or object key)."""
    for c in (ORG['kinds'].get(owner) or ORG['objects'].get(owner) or {}).get('clips', []):
        if c['name'] == name:
            return c
    raise KeyError((owner, name))


# =============================================================================================
# Balance tables (plan 9.3 / 7.6.2 / 9.4 / 9.5). % of the base hit (coefficient x 100); only the balance fixer (AP-FIX)
# changes values. raw = floor(0.18 x pct) against the reference player (plan 9.2). Phase-3 rows include the x1.25 bump.
DMG = {
    'p1_burst': 120, 'p1_sweep': 140,
    'p2_plunge': 80, 'p2_strip': 100,
    'p3_slam1': 110, 'p3_slam2': 110, 'p3_slam3': 130, 'p3_carpet': 30, 'p3_wheel': 15,
    'p4': 130,
    'p5_1': 130, 'p5_2': 140,
    'p6_1': 100, 'p6_2': 120, 'p6_3': 90, 'p6_4': 140,
    'q1_burst': 140, 'q1_slam': 150,
    'q3_1': 150, 'q3_23': 130,
    'q3s_splash': 80, 'q3s_shell': 130,
    'q4_1': 150, 'q4_2': 160,
    'q5_volley': 120, 'q5_blade': 60,
    'o1': 25, 'o1_buffed': 30, 'o2': 34, 'o2_buffed': 42,
    'o6_burst': 35, 'o6_chain1': 67, 'o6_chain2': 34, 'o6_chain3': 20, 'o6_chain4': 13, 'o6_single': 34,
    'o7': 67,
}
DMG_PM = {                                                  # per mille of the player's max HP (FN-15 / FN-16)
    'q2_tick': 30, 'q2_blast': 800, 'fail1': 250,
}
O6_UNEMPOWERED_PCT = 70                                     # un-empowered 포식성 bites x0.7
KB = {'default': 3, 'light': 2, 'heavy': 4, 'none': 0}
ORG_PM = {'basic': 17, 'guard': 34, 'destr': 21, 'pred': 26, 'nest': 26, 'nurt': 34}   # HP in per mille of #apTot
ORG_RES = {'dendro': 20, 'other': 10}                       # U2: organisms Dendro 20 %, the rest 10 %
BOSS_RES = {'dendro': 30, 'other': 10}                      # U2: the body (registry res)
REV = {                                                     # plan 7.6.2 / 9.5 (the solo economy); AP-REV owns the use
    'start': 2700, 'win': 10000, 'basic_kill': 325, 'kill': 1400,
    'basic_hit': 60, 'buffed_hit': 120, 'destr_blast': 1400,
    'slots': 3, 'cap': 6, 'wave_clock': 600, 'wave_left': 1,
    'timeout': 2000, 'timeout_every': 600, 'timeout_alive': 1, 'warn_lead': 0,
    'fail_strikes': 2, 'fail_restart': 2700, 'fail_hint_t': 400,
    'basic_spd': 0.12, 'melee_every': 40, 'ranged_every': 50,
    'nurt_links': 3, 'nurt_loss_pct': 40, 'nurt_relink': 80, 'shield_mult': 5, 'pyro_vs_shield_pct': 150,
    'destr_spd': 0.10, 'destr_fuse': 56, 'destr_blast_at': 61,
    'guard_recast': 240, 'nest_every': 160, 'nest_first': 60,
}
# 양육 (U2, the user's "buffed organisms can't be damaged"): which organisms carry the immunity tag rlk_mb_ap_imm.
# 'A' (plan Q1 default, the wiki table row "양육의 증식 생명체 버프 중 RES 9910 %"): the 양육 itself while it holds >= 1
# link; 'B': the buffed basics. The core's aux_hit makes any tagged organism take nothing ("면역"); AP-REV sets the tag.
NURTURE_MODE = 'A'
WAVES = [                                                   # plan 7.6.3 (6+: 4 basics + a shuffle-bag special; 7+: two)
    {'basic': 4, 'melee': 2},
    {'basic': 4, 'special': ['guard']},
    {'basic': 4, 'special': ['nest']},
    {'basic': 4, 'special': ['nurt']},
    {'basic': 4, 'special': ['pred']},
]
SPECIAL_BAG = ('guard', 'nest', 'nurt', 'pred')

# Phases (#apPh, ap_contract 0.3.3): 0 entrance, 1, 15 = T1, 2, 25 = CS, 3, 9 = death
PH = {'E': 0, 'P1': 1, 'T1': 15, 'P2': 2, 'CS': 25, 'P3': 3, 'D': 9}
POOL = {1: int(BOSS['phases'][0]), 3: int(BOSS['phases'][1])}             # 53 / 47 % of #mbTot
FLOOR_PCT_P1 = 1                                                           # 1 % of the P1 pool (plan 7.2)
T1_LEN, CS_LEN, FAIL_LEN = 136, 192, 60                                    # plan 7.5, 7.7, 3.4
E_LEN = clip_len('entrance_p1')                                            # 110 = registry intro
D_LEN = clip_len('death')                                                  # 120 <= registry death 140
assert E_LEN <= int(BOSS['intro']) and D_LEN <= int(BOSS['death']), (E_LEN, D_LEN)

# =============================================================================================
# Zones, bands, AI constants (plan 7.3 / 7.4; ai.py implements them; values only here)
ZONES = ('front', 'side', 'under', 'back')
ZONE_ID = {z: i + 1 for i, z in enumerate(ZONES)}
BANDS = ('near', 'mid', 'far')
BAND_ID = {b: i + 1 for i, b in enumerate(BANDS)}
FRONT_F = 3.0                                              # FRONT: f >= 3 and |s| <= 4 + 0.6 (f - 3)
FRONT_CONE = (4.0, 0.6)
SIDE_S = 3.0                                               # SIDE |s| > 3, UNDER |s| <= 3, both -3 <= f < 3
BACK_F = -3.0                                              # BACK: f < -3
BAND_P1 = (7.5, 14.0)                                      # near <= 7.5, mid <= 14, far beyond
BAND_P3 = (6.0, 14.0)
COLS_P1 = ('front_near', 'front_mid', 'front_far', 'side_under', 'back')   # the plan 7.4 weight columns
COLS_P3 = ('near', 'mid', 'far')
BACK_DWELL = (10, 3, 2)                                    # sample every 10 t, 3 samples, >= 2 in BACK (20 of 30 t)
BACK_RULE_PCT = 75
RIM_R = 12.0                                               # the rim rule: anchor beyond r 12 with the player BACK
ANTI_STALL = 3
CHAIN_GAP = 20                                             # a chain starts >= 20 t after the last hit (plan 7.4)
Q2_FIRST_AFTER = 1                                         # first use after the first P3 pattern
Q2_EVERY, Q2_OTHERS = 900, 3                               # then >= 900 t since the last and >= 3 other patterns
Q2_CANCEL_CD = 300                                         # a cancelled Q2 (pause / reload) waits 300 t
TURN_IDLE = {1: 3, 3: 3}                                   # idle tracking deg/t per form
TURN_MAX = {1: 3, 3: 6}                                    # turns within patterns (P3 <= 6 deg/t)
STEP_TURN = 60                                             # |dyaw| > 60 at idle -> a crab-turn step (P1)
CRAWL = {'spd': 0.25, 'max': 40}                           # P1 crab crawl when far / after a far landing
WALK = {'spd': 0.12, 'max': 40}                            # P1 side walk when mid
P3_WALK = {'spd': 0.2, 'max': 30}                          # P3 reposition (the Q4 opener) in the crawl stance
P3_CENTRE_WALK = {'spd': 0.4, 'max': 50}                   # P3 walk to the centre before Q2
R_FAR = 9.0                                                # P4's opener R when the player is > 9 b away
Q4_FAR = 8.0                                               # Q4's walk opener when the player is > 8 b away

# =============================================================================================
# Korean texts (U9). The core types the phase lines; patterns / revival own theirs (in their files or here by request)
TXT = {
    'title_p1': BOSS['name'], 'sub_p1': BOSS['sub'], 'sub_p1_line': '긴 「종말」을 걸쳐 진화한 생명',
    'title_heart': '「오아시스의 심장」', 'title_p3': '기원 오아시스 파수꾼', 'sub_p3': '「불씨」를 받아 소생한 생명',
    't1_sink': '종막 오아시스 파수꾼이 땅속으로 숨어듭니다…',
    'p2_goal': '마물을 처치해서 소생 진행도를 올리세요',
    'p2_progress': '소생 진행도',
    'fail_title': '「소생 실패」', 'fail_line': '다시 한 번 실패하면 쓰러집니다',
    'fail_hint': '수호 → 강화된 기본 → 파괴 순서로 처치하세요',
    'warn_title': '!', 'warn_sub': '오아시스의 심장이 위험합니다', 'warn_line': '파괴의 증식 생명체가 나타납니다',
    'cs_done': '오아시스의 심장이 소생했습니다', 'cs_heal': '오아시스의 심장이 생명을 나눕니다',
    'floor_pop': '…', 'immune': '면역',
    'back_hint': '꼬리 뒤는 위험합니다 — 정면에 서세요',
    'gate_l2': '내성: 풀 30% · 그 외 10%', 'gate_l3': '챕터 3 보스',
    'q2_lethal': '다음 종말의 여파는 치명적입니다 — 보호막 안에 머무르세요',
}
WAVE_FMT = '  {n}웨이브'


def tell_rt(t):
    """The wind-up rule of plan U4: max(10, round(0.75 t)) played ticks for a footage tell of t ticks."""
    return max(10, int(round(0.75 * t)))


# =============================================================================================
# The kit (AP-FX, ap_fx_api.md 0.10): its Python API when present, else KitStub (same signatures; each call = an
# empty module-owned function AP:kstub/<kit path>, written by the core for the paths used; AP-I1 switches by merging)
class KitStub:
    """No-op stand-in of `import build_mboss_ap_fx as K` until AP-I1 (ap_fx_api.md 0.10). Every builder returns ONE
    function line (valid after `execute ... run`)."""
    STUB = True
    FN = f'{NS}fx/'
    FONT = 'rlk:mboss_ap'
    STO = 'rlk:apkit'
    CAP, TCAP, SOFT, DCAP, FLCAP = 64, 40, 40, 16, 48
    OWNED_DIRS = ('e', 'p', 'tele', 'dress', 'snd', 'hud', 'prop', 'test')
    OWNED_FILES = ('card', 'cardx', 'look', 'clear', 'uninstall')
    KINDS, PRESETS, SOUNDS, PROPS, GLYPHS, AMBIENT, TELE_COL = {}, {}, {}, {}, {}, set(), {}
    WHITE = 16777215
    BADGE_COL = {'guard': '#F2D45C', 'nest': '#C9E07A', 'nurt': '#D4E784', 'pred': '#E07A5A', 'destr': '#F0A040',
                 'fail': WARN_HEX}
    BADGE_KO = {'guard': '수호', 'nest': '둥지', 'nurt': '양육', 'pred': '포식성', 'destr': '파괴', 'fail': '⚠'}

    def __init__(self):
        self.used = {}

    def _c(self, path, **a):
        path = path.strip('/')
        self.used.setdefault(path, {k: v for k, v in a.items() if v is not None})
        return f'function {NS}kstub/{path}'

    def card(self, kind, pos='~ ~ ~', rot='~ ~', bb='fixed', roll=0, spin=0, s0=0.0, s1=1.0, move=(0, 0, 0), life=8,
             fade=0, col=16777215, dly=0, dur=0, hit=-1, col2=-1, off=None):
        return self._c('card', kind=kind)

    def look(self, kind, col=16777215):
        return self._c('look', kind=kind)

    def clear(self):
        return self._c('clear')

    def uninstall(self):
        return self._c('uninstall')

    def tele_disc(self, r, tell, el=7, nd=0, hold=3):
        return self._c('tele/disc', r=r, tell=tell, el=el)

    def tele_sector(self, r, a, tell, el=7, nd=0, hold=3):
        return self._c('tele/sector', r=r, a=a, tell=tell, el=el)

    def tele_wedge(self, r0, r1, a0, a1, tell, el=7, nd=0, hold=3):
        return self._c('tele/wedge', r0=r0, r1=r1, a0=a0, a1=a1, tell=tell, el=el)

    def tele_line(self, length, w, tell, el=7, nd=0, hold=3, back=0.0):
        return self._c('tele/line', len=length, w=w, tell=tell, el=el)

    def tele_crack(self, length, w, tell, nd=0, hold=3, back=0.0):
        return self._c('tele/crack', len=length, w=w, tell=tell)

    def tele_wave(self, wid, r0, r1, w, tell, dur, el=7, nd=0, hold=2):
        return self._c('tele/wave', id=wid, r0=r0, r1=r1, w=w, tell=tell, dur=dur, el=el)

    def tele_wave_end(self, wid):
        return self._c('tele/wave_end', id=wid)

    def tele_mask_wash(self, r, tell, hold):
        return self._c('tele/mask_wash', r=r, tell=tell, hold=hold)

    def tele_safe_rim(self, sid, r, tell, hold):
        return self._c('tele/safe_rim', id=sid, r=r, tell=tell, hold=hold)

    def tele_safe_end(self, sid):
        return self._c('tele/safe_end', id=sid)

    def tele_mring(self, mid, r, el=22):
        return self._c('tele/mring', id=mid, r=r, el=el)

    def tele_mring_move(self, mid, t=2):
        return self._c('tele/mring_move', id=mid, t=t)

    def tele_mring_end(self, mid):
        return self._c('tele/mring_end', id=mid)

    def tele_wall_spot(self, tell, hold):
        return self._c('tele/wall_spot', tell=tell, hold=hold)

    def tele_clear(self):
        return self._c('tele/clear')

    def dress(self, name, **a):
        return self._c(f'dress/{name}', **a)

    def fx(self, name, **a):
        return self._c(f'p/{name}', **a)

    def snd(self, name):
        return self._c(f'snd/{name}')

    def prop(self, name):
        return self._c(f'prop/{name}')

    def hud(self, name, **a):
        return self._c(f'hud/{name}', **a)

    def glyph(self, name):
        return ''

    def badge(self, kind, on):
        """◆ + the kind's Korean name (dim #707070 off, the kind colour on), as a text component (plain text here)."""
        col = self.BADGE_COL.get(kind, '#FFFFFF') if on else DIM_HEX
        nm = self.BADGE_KO.get(kind, kind)
        return f'{{text:"  ◆{nm}",color:"{col}",bold:false}}'

    def heart_bar(self, v, vmax=10000):
        n = max(0, min(20, int(v * 20 // max(1, vmax))))
        return '{text:"' + '■' * n + '□' * (20 - n) + f'",color:"{HEART_HEX}"}}'


try:
    import build_mboss_ap_fx as K  # noqa: E402  (AP-FX's kit; no files written on import)
    KIT = True
except ImportError:
    K = KitStub()
    KIT = False

# =============================================================================================
BODY = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
PLAYER = '@e[tag=rlk_body,limit=1]'
ARENA_M = '@e[type=minecraft:marker,tag=rlk_mb_arena,limit=1]'
LOCK = '@e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1]'
HEART_M = '@e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1]'
ORGS = '@e[type=minecraft:husk,tag=rlk_mb_ap_org]'
KINDS_PAT = ('normal', 'scheduled', 'chain', 'opener', 'service', 'seq')
PAT_HOOKS = ('pause', 'resume', 'reload', 'vis', 'pj_end')
GATES = ('side_rear', 'centre_free')
# the files every pattern kind writes (the build asserts them)
REQ_HOOKS = {'normal': ('start', 'tick', 'cancel'), 'scheduled': ('start', 'tick', 'cancel'),
             'chain': ('start', 'tick', 'cancel'), 'opener': ('start', 'tick', 'cancel'),
             'service': ('start', 'tick', 'cancel'), 'seq': ()}
# the files the service modules must write (the core calls them; ap_contract 1.6)
REQ_FILES = {
    'seq': ('seq/entrance/setup', 'seq/entrance/tick', 'seq/entrance/done', 'seq/death/start', 'seq/death/tick'),
    'revival': ('rev/start', 'rev/tick', 'rev/ready', 'rev/reload', 'rev/pause', 'rev/resume', 'rev/clear', 'rev/bars',
                'rev/hud', 'heart/add', 'heart/sub', 'heart/p1_hang', 'heart/p1_up', 'heart/p1_respawn', 'heart/clear'),
    'org': ('org/aux_hit', 'org/clear', 'org/freeze', 'wall/clear'),
    'aftermath': ('dome/clear',),
}


class Pattern:
    """One pattern or service a module provides (ap_contract 1.3).

    id / key / label: the 0.8 table (test ids = pattern ids); kind: normal (AI-picked), scheduled (Q2: forced when due),
    chain (Q3s: only as a chain), opener (R: only before its host), service (main-slot services: T1 fail CS move stance),
    seq (E / D: run by the intro / death hooks, no main slot). phase: 1 or 3 (services: None). weight: the plan 7.4
    columns (phase 1: front_near front_mid front_far side_under back; phase 3: near mid far), 0..9. cooldown (t, from the
    pattern's end), first_after (n other patterns of the fight before the first pick), lead (pre-turn ticks <= 10 before
    clock 0), recover (idle ticks after the end), max_len (a hard stop), length (the expected end clock, the HUD and the
    fairness sim), last_hit (clock of the last damaging tick: the chain gap counts from it), chain ({id: pct}: after this
    pattern, pct % that chain id, CHAIN_GAP after last_hit), opener ((id, dist b): when the player is farther, the opener
    runs first and hands over to this pattern), gates, hooks (pause resume reload vis pj_end files it writes)."""

    def __init__(self, id, key, label, kind, clip=None, phase=None, weight=None, cooldown=0, first_after=0, lead=0,  # noqa: A002
                 recover=20, max_len=200, length=None, last_hit=None, chain=None, opener=None, gates=(), hooks=()):
        assert kind in KINDS_PAT, (key, kind)
        assert 0 <= lead <= 10, (key, lead)
        assert all(g in GATES for g in gates), (key, gates)
        assert all(h in PAT_HOOKS for h in hooks), (key, hooks)
        clips = [clip] if isinstance(clip, str) else list(clip or [])
        assert all(c in CLIPS for c in clips), (key, clips)
        cols = COLS_P1 if phase == 1 else COLS_P3
        for k, v in (weight or {}).items():
            assert k in cols and 0 <= v <= 9, (key, k, v)
        self.id, self.key, self.label, self.kind = id, key, label, kind
        self.clip = clips[0] if clips else None
        self.clips = clips
        self.phase = phase
        self.weight = dict(weight or {})
        self.cooldown, self.first_after, self.lead, self.recover = int(cooldown), int(first_after), int(lead), int(recover)
        self.max_len = int(max_len)
        self.length = int(length) if length is not None else self.max_len - 4
        assert 0 < self.length <= self.max_len, (key, self.length, self.max_len)
        self.last_hit = self.length if last_hit is None else int(last_hit)
        self.chain = dict(chain or {})
        self.opener = opener
        self.gates, self.hooks = tuple(gates), tuple(hooks)
        self.module = None

    def w(self, col):
        return int(self.weight.get(col, 0))


# =============================================================================================
OWN = {   # who writes where (paths relative to AP:); the core writes everywhere else it owns
    'p1': {'p': {'burrow', 'hands', 'glow', 'wither', 'tail', 'combo', 'reloc'}, 'dirs': (), 'files': ('p/move/fx',)},
    'seq': {'p': set(), 'dirs': ('seq',), 'files': ()},
    'p3': {'p': {'mstrike', 'shells', 'tail3', 'spiral', 'surface'}, 'dirs': (), 'files': ()},
    'aftermath': {'p': {'aftermath'}, 'dirs': ('dome',), 'files': ()},
    'revival': {'p': {'t1', 'fail', 'cs'}, 'dirs': ('rev', 'heart'), 'files': ()},
    'org': {'p': set(), 'dirs': ('org', 'wall'), 'files': ()},
    'core': None,
}


def _flat(lines):
    if isinstance(lines, str):
        lines = lines.strip('\n').split('\n')
    flat = []
    for ln in lines:
        if isinstance(ln, (list, tuple)):
            flat.extend(_flat(ln))
        elif ln is not None and ln != '':
            flat.extend(ln.split('\n'))
    return flat


COMMANDS = {'execute', 'function', 'scoreboard', 'data', 'tag', 'kill', 'summon', 'tp', 'teleport', 'tellraw', 'title',
            'particle', 'playsound', 'stopsound', 'schedule', 'return', 'effect', 'attribute', 'ride', 'damage', 'bossbar',
            'forceload', 'setblock', 'fill', 'item', 'rotate', 'team', 'clear', 'give', 'random', 'time'}


class Gen:
    """Writer handed to every emit(gen) (ap_contract 1.4). Paths are relative to F:mboss/apep/."""

    def __init__(self, out):
        self.out = out
        self.files = set()
        self.owner = 'core'

    # -- files and ownership
    def _may(self, rel):
        own = OWN.get(self.owner)
        if own is None:
            return True
        if rel in own['files']:
            return True
        if rel.startswith('p/') and rel.split('/')[1] in own['p']:
            return True
        return any(rel == d or rel.startswith(d + '/') for d in own['dirs'])

    def w(self, rel, lines):
        flat = _flat(lines)
        assert re.fullmatch(r'[a-z0-9_/.-]+', rel), f'invalid function path {rel!r}'
        assert self._may(rel), f'{self.owner} may not write {rel} (ap_contract 1.4 ownership)'
        for ln in flat:
            cmd = ln.lstrip('$').split(' ', 1)[0]
            assert ln.startswith('#') or cmd in COMMANDS, f'{rel}: not a command line: {ln!r}'
            assert not re.search(r'scoreboard players (set|add|remove|operation) [#@][^ ]+ -?\d+( |$)', ln), \
                f'{rel}: scoreboard line without an objective: {ln!r}'
        self.out.write(f'mboss/{ID}/{rel}', flat)
        self.files.add(rel)

    def pw(self, key, name, lines):
        self.w(f'p/{key}/{name}', lines)

    def has(self, rel):
        return rel in self.files

    @staticmethod
    def fn(rel):
        return f'function {NS}{rel}'

    # -- the rig (ap_contract 0.4.9) through the core's wrappers (px sets and yaw schedules armed by play)
    @staticmethod
    def play(clip):
        """Play a clip from its tick 0 (the core wrapper AP:play/<clip>: the rig, the clip's px-set driver and its
        yaw schedule; mirror the yaw with #apYawS -1 set before the call)."""
        assert clip in CLIPS, clip
        return f'function {NS}play/{clip}'

    @staticmethod
    def flash(group):
        assert group in FLASH_GROUPS, group
        return f'function {rig_fn("flash/" + group)}'

    @staticmethod
    def face(kind):
        assert kind in ('player', 'track'), kind
        return f'function {rig_fn("face/" + kind)}'

    @staticmethod
    def hands(hset):
        assert hset in HAND_SETS, hset
        return f'function {rig_fn("hands/" + hset)}'

    @staticmethod
    def rig_look(channel, look):
        return f'function {rig_fn(f"look/{channel}/{look}")}'

    @staticmethod
    def bright(v):
        assert v in (13, 15)
        return f'function {rig_fn(f"bright/{v}")}'

    # -- the main slot (ap_contract 1.2)
    @staticmethod
    def end():
        return f'function {NS}p/end'

    @staticmethod
    def release():
        """The dangerous part is over: a queued transition (#apTr 1) ends the pattern here (its cancel runs)."""
        return f'function {NS}p/release'

    @staticmethod
    def set_len(t):
        return f'scoreboard players set #apPLen mb {int(t)}'

    @staticmethod
    def at(t, cmd, clock='#apPT'):
        if isinstance(t, tuple):
            return f'execute if score {clock} mb matches {t[0]}..{t[1]} run {cmd}'
        return f'execute if score {clock} mb matches {t} run {cmd}'

    MODULI = (2, 3, 4, 5, 6, 7, 8, 10, 20, 40)

    @staticmethod
    def every(n, cmd, start=0, clock='#apPT'):
        assert n in Gen.MODULI, n
        return [f'scoreboard players operation #apM mb = {clock} mb', f'scoreboard players operation #apM mb %= #apK{n} mb',
                f'execute if score #apM mb matches {start} run {cmd}']

    # -- services of the core (ap_contract 1.5)
    @staticmethod
    def svc(name):
        assert name in SERVICES, name
        return f'function {NS}svc/{name}'

    @staticmethod
    def px(name):
        """The framework px set (cm.md 9.4) through the core: burrowed / parked also set husk 0.1 + rlk_mb_noshield."""
        assert name in STATES, name
        return f'function {NS}px/{name}'

    @staticmethod
    def stance(target):
        """The stance change clip (crouch_p3 / stand_p3) inside a pattern: the px sets and #apStance follow the clip."""
        assert target in ('crouch', 'stand')
        return f'function {NS}play/{"crouch_p3" if target == "crouch" else "stand_p3"}'

    # -- positions (markers rlk_mb_ap_lock on the floor y 201)
    @staticmethod
    def lockp():
        """The lock under the player's body now, pulled inside the walk disc (r 25.3)."""
        return f'function {NS}u/lockp'

    @staticmethod
    def lockb(d=2.0):
        """The lock d b in front of the player on the boss -> player line (R's re-emerge point), clamped to IDLE_R."""
        return f'function {NS}u/lockb {{d:{L.num(float(d))}}}'

    @staticmethod
    def lockv(lead):
        """The framework predictive lock (cm.md 13.1 mv/lockv, dash samples skipped, sprint cap) re-tagged
        rlk_mb_ap_lock (the framework's rlk_mb_lock removed so the next lockv call keeps it)."""
        return ['kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]', L.lockv(lead),
                'tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_ap_lock',
                'tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] remove rlk_mb_lock']

    @staticmethod
    def keep(new_tag, src='rlk_mb_ap_lock'):
        """Keep the current lock under a pattern tag (rlk_mb_ap_p<id>…); the core kills rlk_mb_ap_kept at the end."""
        assert new_tag.startswith('rlk_mb_ap_p'), new_tag
        return [f'kill @e[type=minecraft:marker,tag={new_tag}]',
                f'tag @e[type=minecraft:marker,tag={src}] add rlk_mb_ap_kept',
                f'tag @e[type=minecraft:marker,tag={src}] add {new_tag}',
                f'tag @e[type=minecraft:marker,tag={new_tag}] remove {src}',
                f'tag @e[type=minecraft:marker,tag={new_tag}] remove rlk_mb_lock']

    @staticmethod
    def clamp(kind):
        """@s = a marker pulled toward the arena axis: 'walk' r 25.3, 'idle' r 14, 'burst1' r 18, 'burst3' r 16, 'glide' r 16."""
        assert kind in CLAMPS, kind
        return f'function {NS}u/clamp_{kind}'

    @staticmethod
    def move_to(sel, spd):
        """@s = body: one glide step of spd b/t toward the entity sel (yaw kept), clamped to the glide disc."""
        return f'execute facing entity {sel} feet rotated ~ 0 positioned ^ ^ ^{L.num(float(spd))} run function {NS}u/step_here'

    @staticmethod
    def tp_to(sel):
        """@s = the body (hidden while burrowed): to the floor point (y 201) of the marker sel, yaw kept. The anchor never
        enters blocks (plan 7.2): the rig's clip sinks the visible body (R9), the anchor stays on the floor."""
        return f'execute at {sel} run tp @s ~ {CY} ~'

    @staticmethod
    def tag_last_hz(tag):
        return f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add {tag}'

    # -- hazards / projectiles with the module defaults: Dendro (el 7), QUIET (the 10-20 telegraph rule: no framework
    # outline; a kit decal only for the *keep* rows through Gen.decal), no framework sound; player-side reactions kept
    # (plan Q13) unless norx=1
    @staticmethod
    def hz_opts(**kw):
        kw.setdefault('quiet', 1)
        kw.setdefault('sfx', 0)
        kw.setdefault('el', 7)
        return L.hz_opts(**kw)

    @staticmethod
    def pj_opts(**kw):
        kw.setdefault('el', 7)
        return L.pj_opts(**kw)

    hz_disc = staticmethod(L.hz_disc)
    hz_ring = staticmethod(L.hz_ring)
    hz_sector = staticmethod(L.hz_sector)
    hz_line = staticmethod(L.hz_line)
    hz_full = staticmethod(L.hz_full)
    hz_aim = staticmethod(L.hz_aim)
    hz_resize = staticmethod(L.hz_resize)
    hz_mask = staticmethod(L.hz_mask)
    hz_extend = staticmethod(L.hz_extend)
    hz_safe_new = staticmethod(L.hz_safe_new)
    pj_launch = staticmethod(L.pj_launch)
    pj_steer = staticmethod(L.pj_steer)
    pl_dot = staticmethod(L.pl_dot)
    GRP_NEW = L.GRP_NEW

    @staticmethod
    def decal(tele, *lines):
        """A pre-hit ground telegraph (kit decal) is allowed ONLY for a *keep* row of the 10-20 telegraph rule (plan 14,
        ap_contract 0.13): decal('keep', K.tele_disc(...)). Every other hazard shows its motion tell and its impact fx."""
        assert tele == 'keep', 'the 10-20 telegraph rule: a ground decal only for a keep row'
        return _flat(list(lines))

    kit = K

    @staticmethod
    def sound(event, vol=1.0, pitch=1.0):
        return L.sound(event, vol, pitch)

    @staticmethod
    def particle(name, pos='~ ~ ~', delta=(0, 0, 0), speed=0, n=1):
        d = ' '.join(L.num(float(v), 3) for v in delta)
        return f'particle minecraft:{name} {pos} {d} {L.num(float(speed), 3)} {int(n)} force @a[tag=player]'

    @staticmethod
    def line(text, colour=GOLD_HEX, hold=50):
        """A typed line on the sub-line (rlk:mboss/line/say, the framework's typer)."""
        return L.say(text, colour, 2, hold, 2)


CLAMPS = {'walk': WALK_R, 'idle': IDLE_R, 'burst1': BURST_R[1], 'burst3': BURST_R[3], 'glide': GLIDE_R}
SERVICES = ('park', 'unpark', 'cine_on', 'cine_off', 'music_1', 'music_2', 'music_3', 'music_stop', 'title_p1',
            'title_heart', 'title_p3', 'px_rest', 'phase_1', 'phase_t1', 'phase_2', 'phase_cs', 'phase_3', 'repool_p3',
            'floor_p1', 'floor_0', 'look_p1', 'look_p3', 'arena_lush', 'arena_withered', 'heal_cs', 'push_ring_cs',
            'req_cs', 'req_fail', 'lose', 'centre_hidden', 'targetable', 'untargetable', 'lib_clear', 'hud_now')


def rot_local(s, f, delta):
    """The local point (s, f) of the anchor turned by delta degrees (Minecraft sense), in the start frame."""
    d = math.radians(delta)
    return (s * math.cos(d) - f * math.sin(d), s * math.sin(d) + f * math.cos(d))


def dir_yaw(s, f):
    """Yaw of the direction (s, f) relative to the facing: 0 forward, -90 the boss's left, +90 its right, 180 back."""
    return math.degrees(math.atan2(-s, f))


def loc(x, z, y=0.0, nd=3):
    n = L.num
    return f'^{n(float(x), nd)} ^{n(float(y), nd)} ^{n(float(z), nd)}'


def wedges(clip, t0, t1, reach):
    """The per-tick swept wedges of a tail swing (plan 7.11 rule 3; ap_contract 0.4.5): for every played tick k of
    t0..t1, dict(t=k, root=(s, f) of the tail root in the START frame, a0 < a1 = the tail-line yaws (relative to the
    start facing, Minecraft sense) of ticks k-1 and k about that root, r1 = reach). From the manifest's tail_root /
    tail_tip tracks composed with the clip's yaw schedule. Each wedge is one hz/sector of half-angle (a1 - a0) / 2 on
    the bisector, all in one volley group. No kit decal (the 10-20 telegraph rule: the P5 / Q4 lanes are *none*)."""
    root, tip = track(clip, 'tail_root'), track(clip, 'tail_tip')

    def line_yaw(t):
        t = max(0, min(len(root) - 1, t))
        d = yaw_at(clip, t)
        rs, rf = rot_local(root[t][0], root[t][2], d)
        ts, tf = rot_local(tip[t][0], tip[t][2], d)
        return dir_yaw(ts - rs, tf - rf), (rs, rf)
    out = []
    for k in range(t0, t1 + 1):
        a_prev, _ = line_yaw(k - 1)
        a_now, r = line_yaw(k)
        while a_now - a_prev > 180:
            a_now -= 360
        while a_now - a_prev < -180:
            a_now += 360
        a0, a1 = sorted((a_prev, a_now))
        out.append(dict(t=k, root=r, a0=a0, a1=a1, r1=reach))
    return out


class TL:
    """Per-tick timeline of one pattern: lines grouped into p/<key>/<sub>/<t> and reached through a binary dispatch tree
    on the clock (#apPT by default).

        tl = TL(g, 'burrow'); tl.at(8, cmd); tl.span(10, 14, cmd); tl.write(start_head, tick_head)"""

    def __init__(self, g, key, clock='#apPT', sub='k'):
        self.g, self.key, self.ev, self.clock, self.sub = g, key, {}, clock, sub

    def at(self, t, *lines):
        for line in lines:
            for one in _flat([line]):
                self.ev.setdefault(int(t), []).append(one)

    def span(self, t0, t1, *lines):
        for t in range(t0, t1 + 1):
            self.at(t, *lines)

    def fn(self, rel):
        return f'function {NS}p/{self.key}/{rel}'

    def tname(self, t):
        return f'{self.sub}/{t}' if t >= 0 else f'{self.sub}/m{-t}'

    def _node(self, ts):
        if len(ts) <= 6:
            return [f'execute if score {self.clock} mb matches {t} run return run {self.fn(self.tname(t))}' for t in ts]
        mid = len(ts) // 2
        out = []
        for part in (ts[:mid], ts[mid:]):
            name = f'{self.sub}d/{part[0]}_{part[-1]}'.replace('-', 'm')
            self.g.pw(self.key, name, [f'# dispatch {self.clock} {part[0]}..{part[-1]}'] + self._node(part))
            out.append(f'execute if score {self.clock} mb matches {part[0]}..{part[-1]} run return run {self.fn(name)}')
        return out

    def write(self, start_head, tick_head, t0=0, extra_tick=(), start='start', tick='tick'):
        for t, lines in sorted(self.ev.items()):
            if t > t0:
                self.g.pw(self.key, self.tname(t), [f'# {self.key} {self.clock} {t}'] + lines)
        self.g.pw(self.key, start, list(_flat(start_head)) + self.ev.get(t0, []))
        ts = sorted(t for t in self.ev if t > t0)
        self.g.pw(self.key, tick, list(_flat(tick_head)) + list(_flat(extra_tick)) + self._node(ts))

    def ticks(self):
        return sorted(self.ev)


def stub_pattern(g, p, tick=(), end=None, head_note=''):
    """AP-CORE's working frame stub of a pattern (no hazards): start / tick / cancel (+ declared hooks) that play the
    pattern's clips at their real clocks and end at its real length, so the AI, the slot, the px sets, the yaw
    schedules and the phase flow run with the pattern's true timing. tick: extra (clock, line) pairs."""
    head = f'# STUB (AP-CORE, ap_contract 1.3): {p.label} ({p.key}, id {p.id}); the pattern stage replaces this file. {head_note}'.rstrip()
    end = p.length if end is None else end
    lines = [head, '# keeps time only (the clip of each step at its clock; no hazards)']
    for t, ln in tick:
        lines.append(Gen.at(t, ln))
    lines.append(f'execute if score #apPT mb matches {end}.. run {Gen.end()}')
    g.pw(p.key, 'start', [head])
    g.pw(p.key, 'tick', lines)
    g.pw(p.key, 'cancel', [head, '# nothing of its own lingers (selectors only, idempotent)', 'kill @e[tag=rlk_mb_ap_p' + str(p.id) + ']'])
    for h in p.hooks:
        if not g.has(f'p/{p.key}/{h}'):
            g.pw(p.key, h, [head])

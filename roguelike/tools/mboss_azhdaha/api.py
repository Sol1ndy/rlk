"""Shared, stable API of the 야타용왕 (Azhdaha) module generator (core <-> pattern modules).

The binding contract is the scratchpad file az/contract/s2.md (this file implements its sections 2-10); the rig
manifest schema is az/contract/manifest.md; the framework names are az/contract/cm.md; the kit names az/contract/fx.md.
Pattern authors (geo_a geo_b leg tail trans seq) import this module and never edit it (except the re-export line of
their own h_<stage>.py at the end); new helpers, constants or DMG keys go through a request (s2.md section 13).

Units: Python helpers take blocks / ticks / degrees; the framework boundary is tenths of a block and % of the base hit
(atk 12 x dmgMul 140: 100 = 1.0 = 23 HP on an item-less Lv5 player).

Three things may be missing while the stages run in parallel; each has a clearly marked local fallback that switches
off by itself when the real thing lands (the build prints every fallback in use):
- the framework (AZ-CM, wip/az-cm, cm.md): fw(rel) returns the real function line when F:mboss/<rel> exists in the
  tree (the core generator runs before this module), else a LOCAL STUB F:mboss/azhdaha/cmstub/<rel> written by the core
  (CMSTUBS); the registry entry (REG_STUB = plan.md 1.6 while tools/mboss_registry.json lacks "azhdaha") and the
  arena (ARENA_STUB = cm.md 2.3 while mboss_lib has no arena_of / the registry no arenas);
- the rig (wip/az-rig, R3a): the manifest is the real v1 rig manifest merged with the stub manifest of stub_rig.py
  (FALLBACKS = the clips taken from the stub; the I2b build asserts it is empty), the rig API functions are the real
  rig's where F:mboss/azhdaha/rig/<fn> exists, else the stub rig's (rig_stub/**);
- the kit (wip/az-fx, S1-FX, fx.md): K is the kit's Python API when tools/build_mboss_az_fx.py exists, else KitStub with
  the same signatures, whose every call is a module-owned empty function F:mboss/azhdaha/kstub/<kit path> (I1-WIRE
  switches to the kit by merging it; nothing here changes).
"""
from pathlib import Path
import inspect
import json
import re
import math
import sys

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
import mboss_lib as L  # noqa: E402
from . import stub_rig as SR  # noqa: E402

ID = 'azhdaha'
NS = f'rlk:mboss/{ID}/'
N = 10
FDIR = L.FN / 'mboss' / ID

# =============================================================================================
# Registry entry and arena (cm.md 2; plan.md 1.6). LOCAL STUBS while AZ-CM has not landed.
REG = L.load_registry()
REG_STUB = {
    'id': 'azhdaha', 'n': 10, 'kind': 'chapter', 'ch': [1], 'route': False, 'enabled': True, 'w': 0,
    'minCh': 1, 'maxCh': 1, 'name': '야타용왕', 'sub': '봉인된 바위 용의 왕', 'color': '#F2B53A', 'el': 5,
    'hp': 260, 'xp': 40, 'atk': 12, 'lvAdd': 0, 'dmgMul': 140, 'goldMul': 1, 'sap': 0, 'picks': 0,
    'scale': 0.1, 'px': True, 'pxBase': 65, 'intro': 160, 'death': 140, 'deathSnd': False,
    'arena': 'az_cavern', 'theme': 'az_cavern', 'res': {'0': 30, '5': 30, '*': 10}, 'phases': [100],
    'music': {'1': {'ev': 'minecraft:music.end', 'len': 0}, '2': {'ev': 'minecraft:music.dragon', 'len': 0}},
    'icon': {'item': 'minecraft:raw_gold_block', 'model': 'rlk:mboss/az_kit/gate_icon'},
    'hit': {'w': 1.0, 'h': 1.0},
}
_B = next((b for b in REG.get('boss', []) if b.get('id') == ID), None)
BOSS_STUBBED = _B is None
BOSS = dict(REG_STUB) if _B is None else dict(_B)
BOSS.setdefault('hit', {'w': 1.0, 'h': 1.0})
ARENA_STUB = {'aid': 'az_cavern', 'n': 1, 'theme': 'az_cavern', 'ver': 1, 'cx': 320, 'cy': 201, 'cz': 8, 'r': 33, 'walk': 28,
              'safe': 26, 'start': {'x': 320.5, 'y': 201.0, 'z': 34.5, 'yaw': 180.0, 'pitch': 0.0},
              'box': {'x0': 280, 'y0': 190, 'z0': -32, 'x1': 360, 'y1': 240, 'z1': 48}, 'looks': ['default'],
              'oob': {'y0': 198, 'y1': 237}}
ARENA_STUBBED = True
ARENA = dict(ARENA_STUB)
if hasattr(L, 'arena_of') and BOSS.get('arena', 'plaza') in REG.get('arenas', {}):
    try:
        ARENA = dict(L.arena_of(BOSS, REG))
        ARENA_STUBBED = False
    except TypeError:
        ARENA = dict(L.arena_of(BOSS))
        ARENA_STUBBED = False
CX, CY, CZ = ARENA['cx'], ARENA['cy'], ARENA['cz']
WALK, SAFE = float(ARENA['walk']), float(ARENA['safe'])
WALK_R = WALK - 0.7                  # 27.3: ground targets (lockp / lockv clamp)
SAFE_R = SAFE                        # 26
BODY_R = 8.0                         # the anchor at idle and for jump / burrow destinations
CHARGE_R = 12.0                      # the anchor during a charge
CLEAR_PAD = 1.5                      # pattern fields keep r + 1.5 off the two clear melee points
MAX_HP_CAP = 2 ** 31 - 1


# The arena theme (theme.md 1, 4; S1-ARENA's T:mboss_arena_az_cavern.py): api.POINTS = the theme's POINTS, api.PROPS =
# props('default'), api.ENTRANCE_GLYPHS / ENTRANCE_GLOW = entrance_layout()['glyphs'] / ['stele_glow'] (s2.md 5.1).
# While L.theme_module('az_cavern') is None (wip/az-mod before it merges wip/az-arena) the module uses _THEME_FALLBACK,
# its own copy of theme.md 6.3 / 6.4: the spawn (320, 201, 8) yaw 0, the 16 water tiles, the seal steles r 8 at the
# compass bearings 30 + 60 k (0 = north -z, 90 = east +x; a centre-facing prop at bearing b has yaw b), the prism and
# the crater at the centre; no crystals, no glyphs; ENTRANCE_GLYPHS empty (prep summons no glyph props). The build
# prints a WARN; the I1 build asserts the real theme was used.
def _theme_fallback():
    import math as _m
    water = [(float(x), 201.005, float(z)) for z in (-13, 1, 15, 29) for x in (299, 313, 327, 341)]
    steles = []
    for k in range(6):
        b = 30 + 60 * k
        steles.append((round(320 + 8 * _m.sin(_m.radians(b)), 3), 201.0, round(8 - 8 * _m.cos(_m.radians(b)), 3), float(b)))
    points = {'spawn': (320.0, 201.0, 8.0, 0.0), 'seal_steles': steles, 'seal_prism': (320.0, 201.0, 8.0),
              'crater': (320.0, 201.0, 8.0), 'motes': []}
    props = [{'name': f'water_{i % 4}_{i // 4}', 'kind': 'water_sheet', 'group': 'water', 'pos': p, 'yaw': 0.0, 'pitch': 0.0,
              'scale': 14.0, 'el': 'fight', 'uuid': None} for i, p in enumerate(water)]
    return {'POINTS': points, 'PROPS': props, 'GLYPHS': {}, 'GLOW': None}


_THEME_FALLBACK = _theme_fallback()


def _load_theme():
    import importlib
    mod = None
    name = ARENA.get('theme', 'az_cavern')
    if hasattr(L, 'theme_module'):
        mod = L.theme_module(name)
    elif (_TOOLS / f'mboss_arena_{name}.py').exists():
        mod = importlib.import_module('mboss_arena_' + name)
    if mod is None:
        fb = _THEME_FALLBACK
        return dict(fb['POINTS']), list(fb['PROPS']), dict(fb['GLYPHS']), fb['GLOW'], True
    ent = mod.entrance_layout()
    return (dict(mod.POINTS), list(mod.props('default')), dict(ent.get('glyphs') or {}), ent.get('stele_glow'), False)


POINTS, PROPS, ENTRANCE_GLYPHS, ENTRANCE_GLOW, THEME_STUBBED = _load_theme()
# the module's view of the theme (seq.py, core.py)
THEME = {'spawn': tuple(POINTS['spawn']), 'seal_steles': [tuple(v) for v in POINTS['seal_steles']],
         'seal_prism': tuple(POINTS['seal_prism']), 'crater': tuple(POINTS['crater']),
         'motes': [tuple(v) for v in POINTS.get('motes', [])], 'props': PROPS, 'glyphs': ENTRANCE_GLYPHS,
         'stele_glow': ENTRANCE_GLOW, 'centre': (ARENA['cx'], ARENA['cz'])}
THEME_CENTRE = THEME['centre']


# =============================================================================================
# Framework functions (cm.md) and their LOCAL STUBS (written by the core under cmstub/ while missing)
CMSTUBS = {}                         # rel -> the cm.md section it stands in for


# Framework dispatchers that exist before they serve this boss (AZ-CM commit 1: px/state has no per-boss lines until
# the core compiles the px runtime from the manifests, cm.md 9.3): usable only with a line for #mbId N.
FW_PER_BOSS = {'px/state': f'#mbId mb matches {N} if data storage rlk:mboss {{pxq:'}


def fw_has(rel):
    p = L.FN / 'mboss' / (rel + '.mcfunction')
    if not p.exists():
        return False
    need = FW_PER_BOSS.get(rel)
    return need is None or need in p.read_text(encoding='utf-8')


CM_SEC = {'cb/body': '5.5', 'px/state': '9.3', 'px/spawn': '9.3', 'mv/lockv': '13.1', 'mv/local': '13.2',
          'pl_dot': '13.4', 'push/ring': '13.5', 'cine/start': '13.7', 'cine/end': '13.7', 'music/set': '10',
          'music/stop': '10', 'hz/extend': '13.8', 'hz/mask': '13.6', 'floor': '7.2', 'res_pre': '8'}


def fw(rel, args=None):
    """The line `function rlk:mboss/<rel> [args]` of a framework function (cm.md), or of its local stub
    F:mboss/azhdaha/cmstub/<rel with / -> _> when the tree has no such function yet (CMSTUBS)."""
    a = f' {args}' if args else ''
    if fw_has(rel):
        return f'function rlk:mboss/{rel}{a}'
    CMSTUBS[rel] = CM_SEC.get(rel, '?')
    return f'function {NS}cmstub/{rel.replace("/", "_")}{a}'


# =============================================================================================
# The rig manifest (manifest.md): the real v1 rig manifest merged with the stub manifest per clip
MANIFEST = _TOOLS / 'mboss_azhdaha_rig_manifest.json'
STUB_MANIFEST = Path(__file__).resolve().parent / 'stub_rig_manifest.json'
_REAL_RAW = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else None
REAL_KIND = None if _REAL_RAW is None else ('v1' if SR.is_v1_rig(_REAL_RAW) else ('r1' if 'schema' not in _REAL_RAW else 'other'))
STUB = SR.stub_manifest()
MAN, FALLBACKS = SR.merge(_REAL_RAW if REAL_KIND == 'v1' else None, STUB)
CLIPS = {c['name']: c for c in MAN['clips'] if not c['name'].startswith('dbg_')}
REAL_CLIPS = {c['name'] for c in (_REAL_RAW or {}).get('clips', [])} if REAL_KIND == 'v1' else set()
EV_FALLBACKS = []                    # (clip, event, default) used because the manifest lacks the event
assert set(SR.CLIP_NAMES) <= set(CLIPS), sorted(set(SR.CLIP_NAMES) - set(CLIPS))

RIG_DIR = FDIR / 'rig'
REAL_RIG = (RIG_DIR / 'spawn.mcfunction').exists()
RIG_STUBBED = set()                  # rig API functions taken from the stub rig although a real rig exists


def rig_fn(name):
    """Full id of a rig API function (manifest.md 7): the real rig's when it exists, else the stub rig's."""
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
    """The rig tick of the module tick (last): the real rig's tick (+ the stub chain while some clip still comes from
    the stub manifest, FALLBACKS), or the stub's."""
    if REAL_RIG:
        return [f'function {NS}rig/tick'] + ([f'function {NS}rig_stub/chain'] if FALLBACKS else [])
    return [f'function {NS}rig_stub/tick']


def stub_rig_needed():
    """I1-WIRE: the stand-in rig AZ:rig_stub/** is written only while something still needs it (no real rig, a clip
    from the stub manifest, or a rig API function the real rig lacks). Valid after the emit (RIG_STUBBED fills there)."""
    return (not REAL_RIG) or bool(FALLBACKS) or bool(RIG_STUBBED)


def fallback_list():
    """What the real rig manifest v1 / rig still lacks (plan 7.3 I1-WIRE; the I2b build asserts it is empty)."""
    return {'clips': sorted(FALLBACKS), 'events': sorted(set(EV_FALLBACKS)), 'rig_functions': sorted(RIG_STUBBED)}


def ev(clip, event):
    """Played tick of a clip event (= the pattern clock: #azPT 0 is the tick the core plays the clip)."""
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
    """A named local point (x = s left, y up, z = f forward; blocks from the anchor) at a clip event."""
    return tuple(float(v) for v in CLIPS[clip]['anchors'][event][point])


def track(clip, name):
    """Per-tick local points (tail_root / tail_tip), one per played tick, before the yaw schedule."""
    return [tuple(float(v) for v in p) for p in CLIPS[clip]['tracks'][name]]


def yaw_at(clip, t):
    y = CLIPS[clip].get('yaw')
    if not y:
        return 0.0
    return float(y[max(0, min(len(y) - 1, int(t)))])


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


# Rest anchors and the 4.12 zone thresholds, computed from the manifest (never typed by hand: s2.md 4.3)
REST = {k: tuple(float(v) for v in p) for k, p in MAN['rest_anchors'].items()}
P_NOSE = REST['nose']
P_HEAD_COL = REST['head_col']
P_HEAD_FRONT = (P_HEAD_COL[0], 0.0, P_HEAD_COL[2] + 2.5)
_t2 = MAN['proxies']['rest']['tail2']
P_TAIL_LANE = (float(_t2[0]), 0.0, float(_t2[1]))
P_TAIL_ROOT = REST['tail_root']
P_PAW = {1: REST['paw_fl'], 2: REST['paw_fr'], 3: REST['foot_hl'], 4: REST['foot_hr']}
PAW_NAMES = {1: 'fl', 2: 'fr', 3: 'hl', 4: 'hr'}
TORSO_HW = float(MAN.get('torso_hw', 3.0))
HEAD_F = round(P_HEAD_COL[2] - 0.7, 3)            # 3.6: HEAD f >= 3.6
HEAD_CONE = (4.0, 0.6)                            # HEAD |s| <= 4 + 0.6 (f - 3.6)
FLANK_S0, FLANK_S1 = TORSO_HW, 9.0                # FLANK-near 3.0 <= |s| <= 9.0
TAIL_F = round(P_TAIL_ROOT[2] - 0.05, 3)          # -4.8: TAIL f < -4.8
TAIL_S = TORSO_HW + 0.5                           # 3.5: TAIL-lane |s| <= 3.5
PAW_R = 2.8                                       # PAW: horizontal distance to a paw / foot <= 2.8
BAND_NEAR, BAND_MID = 9.0, 15.0                   # anchor distance near <= 9, mid 9-15, far > 15
ZONES = ('head_near', 'head_mid', 'head_far', 'flank_near', 'flank_far', 'tail_lane', 'tail_off', 'paw')
ZONE_ID = {z: i + 1 for i, z in enumerate(ZONES)}
WHIP_REACH = 12.0                                 # P7 sweep from the tail root
WHIP_TIP_R = round(-P_TAIL_ROOT[2] + WHIP_REACH, 3)   # 16.75 from the anchor
WHIP_EXIT_R = 7.2                                 # P7 exit test: 3 + (23 - 8) x 0.281
WHIP_HEAD_LANE = 65.0                             # the hazard ends 65 degrees from the front axis


# =============================================================================================
# Balance tables (plan.md 6.3 / s2.md 5.1). % of the base hit; only the balance fixer changes values.
DMG = {
    'p1': 140, 'p2_land': 110, 'p2_wave2': 110, 'p3': 180, 'p4_land': 90, 'p4_blast': 90, 'p5': 90, 'p5b': 90,
    'p6_strip': 120, 'p6_end': 60, 'p7_sweep': 150, 'p7_erupt': 80, 'p8': 140,
    'p9_ring': 90, 'p9_rock': 60, 'p9_rush': 110, 'p9_burst': 150, 'p9_run': 130,
    't1_wave': 80, 't1_wave6': 100, 'b3_emerge': 140,
    'o31': 35, 'o32_big': 140, 'o32_small': 80, 'fire': 20, 'hail': 15,
    'o41': 90, 'o42': 120, 'o42_sky': 50, 'o43': 70, 'o44': 60, 'o45': 100, 'o46': 70,
    'x_geyser': 80, 'x_blade': 50, 'x_lump': 60, 'x_cring': 60, 'x_bolt': 60, 'x_wall': 80, 'x_hail': 15,
    'x_wline': 60, 'x_estrip': 20, 'x_strip': 15,
    'brand_pm': 30, 'shard_pm': 120,
}
KB = {'default': 3, 'light': 2, 'heavy': 4, 'none': 0, 'p6_out': 4, 'p7_tan': 4, 'p8_side': 3, 'o32_big': 3, 'o42_sky': 2}
ADDON_LEAD = 12
FIELD_CAPS = {'fire': 4, 'hail': 2, 'strip': 1}
FIELD_FAM = {'fire': 1, 'hail': 2, 'strip': 3}
FIELD_AREA_MAX = 220                 # b2 of all lingering fields
FIELD_GATE = 150                     # b2: the picker skips field-making patterns from here
FIELD_SLOTS = 8
FIELD_REARM = 10
# element numbering (#elem) and names
EL = {'phys': 0, 'pyro': 1, 'hydro': 2, 'electro': 3, 'cryo': 4, 'geo': 5, 'anemo': 6, 'dendro': 7, 'void': 8}
EL_NAME = {1: '불', 2: '물', 3: '번개', 4: '얼음', 5: '바위'}
EL_KEY = {1: 'pyro', 2: 'hydro', 3: 'electro', 4: 'cryo', 5: 'geo'}
EL_COL = {1: '#FF8A3D', 2: '#4FB8FF', 3: '#C58BFF', 4: '#9FE8F5', 5: '#F0A93A'}
EL_GLYPH_COL = {1: '#FF8A3D', 2: '#8CCCDE', 3: '#A291D0', 4: '#9FE8F5'}   # entrance stele glyphs (plan 2.3)
LEG_ELS, TAIL_ELS = (1, 2), (3, 4)
PAIRS = {0: (1, 3), 1: (2, 4), 2: (1, 4), 3: (2, 3)}   # pair roll 0..3 -> (leg, tail): 불/번개, 물/얼음, 불/얼음, 물/번개
GOLD_HEX = BOSS['color']              # #F2B53A: speaker colour, the name
DIM_HEX = '#707070'


def tell_rt(t, nododge=False):
    """Telegraph rule of plan.md 0: max(F, round(0.75 t)), F = 12 (20 for #hzNoDodge hits)."""
    return max(20 if nododge else 12, int(round(0.75 * t)))


# =============================================================================================
# The B3 frame (s2.md 7.1; ticks of #azB3T)
B3_LEN = 433
B3_INV = 8
B3_GLIDE = (40, 56)
B3_TAILUP = 58
B3_PILLAR = 66
B3_TAILSINK = 335
B3_GONE = 353
B3_MOUND = (353, 380)
B3_EMERGE_HZ = 360         # the emergence burst hazard is made here (internal tell 28); NO decal (Change note 1:
                           # B3_EMERGE_DECAL is retired, the dust mound of B3_MOUND is the readable tell)
B3_EMERGE = 380
B3_BURST = 388
B3_OUT = 418
B3_END = 433
B3_LAST = B3_BURST - 31
B3_HIT_MAX = B3_BURST - 20
B3_WINDOW = (58, 335)
assert B3_LAST == 357 and B3_HIT_MAX == 368
assert ev('p3_sink', 'pillar') == B3_TAILUP and clip_len('p3_sink') == B3_PILLAR
assert B3_GONE == B3_TAILSINK + ev('tail_pillar_sink', 'gone') and B3_EMERGE + ev('burrow_emerge', 'burst') == B3_BURST
assert B3_EMERGE + ev('burrow_emerge', 'out') == B3_OUT and B3_EMERGE + clip_len('burrow_emerge') == B3_END


# =============================================================================================
# Addon points (s2.md 10; plan.md 4.6). point -> host pattern id, clip, event, the element bodies the table names.
ADDON_POINTS = {
    'chin/impact': dict(host=1, clip='chin_slam', event='impact', bodies=('hydro', 'pyro', 'cryo', 'electro'),
                        ctx='the impact point; yaw of the crack line (anchor -> impact); #azCtxGrp'),
    'jump/land': dict(host=2, clip='jump_slam', event='land', bodies=('hydro', 'cryo'),
                      ctx='the landing point; yaw to the player; #azCtxGrp = the landing group'),
    'jump/wave2': dict(host=2, clip='jump_slam', event='wave2', bodies=('pyro', 'electro'),
                       ctx='the landing point (the anchor); yaw to the player; #azCtxGrp = the wave-2 group'),
    'stomp/w1': dict(host=5, clip='stomp_fl', event='w1', bodies=('hydro', 'cryo'),
                     ctx="the paw point; yaw to the player; #azCtxPaw, #azCtxGrp = w1's group"),
    'stomp/w3': dict(host=5, clip='stomp_fl', event='w3', bodies=('pyro', 'electro'),
                     ctx="the paw point; yaw to the player; #azCtxPaw, #azCtxGrp = w3's group"),
    'stomp3/s1': dict(host=10, clip='stomp3_fl', event='s1', bodies=('hydro', 'cryo'),
                      ctx="paw A; yaw to the player; #azCtxGrp = s1's group"),
    'stomp3/s3': dict(host=10, clip='stomp3_fl', event='s3', bodies=('pyro', 'electro'),
                      ctx="paw A; yaw to the player; #azCtxGrp = s3's group"),
    'whip/sweep': dict(host=7, clip='tail_whip_l', event='sweep', bodies=('cryo',),
                       ctx="the tail root at E; the anchor's start yaw; #azCtxSide, #azCtxA0, #azCtxA1"),
    'whip/end': dict(host=7, clip='tail_whip_l', event='erupt', bodies=('electro',),
                     ctx='the end-line point (the tail root at sweep_end); the end-line yaw'),
    'tailslam/impact': dict(host=8, clip='tail_slam', event='impact', bodies=('cryo', 'electro'),
                            ctx='the tail root; the line yaw (straight back)'),
}
for _p, _d in ADDON_POINTS.items():
    _d['E'] = ev(_d['clip'], _d['event'])
    _d['call'] = _d['E'] - ADDON_LEAD
    _d['key'] = _p.replace('/', '_')
assert {p: d['call'] for p, d in ADDON_POINTS.items()} == {
    'chin/impact': 23, 'jump/land': 9, 'jump/wave2': 20, 'stomp/w1': 5, 'stomp/w3': 35, 'stomp3/s1': 5, 'stomp3/s3': 51,
    'whip/sweep': 11, 'whip/end': 21, 'tailslam/impact': 27}
LEG_BODY = {'hydro': 2, 'pyro': 1}
TAIL_BODY = {'cryo': 4, 'electro': 3}


def addon_test_ctx(point, pos, yaw, scores=None):
    """Lines that set up a synthetic addon context (pat_leg.py / pat_tail.py): the context marker at pos (x, y, z)
    rotated yaw, the context scores (default 0 / the host event tick), then the point's dispatcher as the body."""
    d = ADDON_POINTS[point]
    sc = dict({'#azCtxGrp': 0, '#azCtxYaw': int(yaw), '#azCtxSide': 1, '#azCtxPaw': 1, '#azCtxA0': 0, '#azCtxA1': 0,
               '#azCtxT': d['E']}, **(scores or {}))
    x, y, z = pos
    return ([f'scoreboard players set {k} mb {int(v)}' for k, v in sc.items()]
            + [f'execute positioned {L.num(float(x))} {L.num(float(y))} {L.num(float(z))} rotated {L.num(float(yaw))} 0 run '
               f'function {NS}x/ctx',
               f'execute as {BODY} at @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] rotated as '
               f'@e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] run function {NS}x/{d["key"]}'])


# =============================================================================================
# The kit (S1-FX, fx.md): its Python API when present, else KitStub (same signatures; every call = an empty
# module-owned function F:mboss/azhdaha/kstub/<kit path>, written by the core for the paths used)
class KitStub:
    """No-op stand-in of `import build_mboss_az_fx as K` (fx.md section 9) until I1. Every builder returns ONE
    function line (valid after `execute ... run`); the core writes the empty kstub/<path> functions used."""
    STUB = True
    FN = f'{NS}fx/'
    FONT = 'rlk:mboss_az'
    STO = 'rlk:azkit'
    CAP, TCAP, SOFT, FCAP = 64, 40, 40, 16
    OWNED_DIRS = ('e', 'p', 'tele', 'snd', 'hud', 'prop', 'test')
    OWNED_FILES = ('card', 'cardx', 'look', 'clear', 'uninstall')
    KINDS, PRESETS, EPRESETS, SOUNDS, PROPS, GLYPHS, AMBIENT, TELE_COL = {}, {}, {}, {}, {}, {}, set(), {}
    WHITE = 16777215

    def __init__(self):
        self.used = {}                     # kit path -> args of the first call (docs in the stub file)

    def _c(self, path, **a):
        path = path.strip('/')
        self.used.setdefault(path, {k: v for k, v in a.items() if v is not None})
        return f'function {NS}kstub/{path}'

    # card engine
    def card(self, kind, pos='~ ~ ~', rot='~ ~', **kw):
        return self._c('card', kind=kind)

    def look(self, kind, col=16777215):
        return self._c('look', kind=kind)

    def clear(self):
        return self._c('clear')

    def uninstall(self):
        return self._c('uninstall')

    # telegraphs (blocks in; the kit converts to tenths)
    def tele_disc(self, r, tell, el=5, nd=0, hold=3, fill=1):
        return self._c('tele/disc' if fill else 'tele/disc_o', r=r, tell=tell, el=el, nd=nd)

    def tele_ring(self, r0, r, tell, el=5, nd=0, hold=3):
        return self._c('tele/ring', r0=r0, r=r, tell=tell, el=el, nd=nd)

    def tele_sector(self, r, a, tell, el=5, nd=0, hold=3):
        return self._c('tele/sector', r=r, a=a, tell=tell, el=el, nd=nd)

    def tele_wedge(self, r0, r1, a0, a1, tell, el=5, nd=0, hold=3):
        return self._c('tele/wedge', r0=r0, r1=r1, a0=a0, a1=a1, tell=tell, el=el, nd=nd)

    def tele_line(self, len, w, tell, el=5, nd=0, hold=3, back=0):   # noqa: A002 (fx.md name)
        return self._c('tele/line', len=len, w=w, tell=tell, el=el, nd=nd)

    def tele_lane_side(self, len, w, tell, el=5, hold=3, back=0):   # noqa: A002
        return self._c('tele/lane_side', len=len, w=w, tell=tell, el=el)

    def tele_wave(self, id, r0, r1, w, tell, dur, el=5, nd=0, hold=3):   # noqa: A002
        return self._c('tele/wave', id=id, r0=r0, r1=r1, w=w, tell=tell, dur=dur, el=el, nd=nd)

    def tele_wave_to(self, id, r, dur):   # noqa: A002
        return self._c('tele/wave_to', id=id, r=r, dur=dur)

    def tele_wave_end(self, id):   # noqa: A002
        return self._c('tele/wave_end', id=id)

    def tele_mline(self, id, len, w, tell, el=5, nd=0, hold=3, back=0):   # noqa: A002
        return self._c('tele/mline', id=id, len=len, w=w, tell=tell, el=el, nd=nd)

    def tele_mline_aim(self, id):   # noqa: A002
        return self._c('tele/mline_aim', id=id)

    def tele_mline_turn(self, id, d):   # noqa: A002
        return self._c('tele/mline_turn', id=id, d=d)

    def tele_mline_end(self, id):   # noqa: A002
        return self._c('tele/mline_end', id=id)

    def tele_heptagram(self, r, tell, el=4, hold=3, fill=1):
        return self._c('tele/heptagram' if fill else 'tele/heptagram_o', r=r, tell=tell, el=el)

    def tele_hexagram(self, r, tell, el=3, hold=3, fill=1):
        return self._c('tele/hexagram' if fill else 'tele/hexagram_o', r=r, tell=tell, el=el)

    def tele_starseal(self, r, tell, el=4, hold=3, fill=1):
        return self._c('tele/starseal' if fill else 'tele/starseal_o', r=r, tell=tell, el=el)

    def tele_seal8(self, r, tell, el=1, hold=3, fill=1):
        return self._c('tele/seal8' if fill else 'tele/seal8_o', r=r, tell=tell, el=el)

    def tele_mask_wash(self, r, tell, hold=3):
        return self._c('tele/mask_wash', r=r, tell=tell)

    def tele_safe_rim(self, id, r, tell, hold=3):   # noqa: A002
        return self._c('tele/safe_rim', id=id, r=r, tell=tell)

    def tele_safe_beam(self, id):   # noqa: A002
        return self._c('tele/safe_beam', id=id)

    def tele_safe_end(self, id):   # noqa: A002
        return self._c('tele/safe_end', id=id)

    def tele_crater(self, r, tell, hold=3):
        return self._c('tele/crater', r=r, tell=tell)

    def tele_halo(self, r, h, tell, el=1, hold=3):
        return self._c('tele/halo', r=r, h=h, tell=tell, el=el)

    def tele_glyph_circle(self, r, tell, hold=3):
        return self._c('tele/glyph_circle', r=r, tell=tell)

    def tele_field(self, id, r, el, life):   # noqa: A002
        return self._c('tele/field', id=id, r=r, el=el, life=life)

    def tele_strip(self, id, len, w, yaw, el, life):   # noqa: A002
        return self._c('tele/strip', id=id, len=len, w=w, yaw=yaw, el=el, life=life)

    def tele_field_end(self, id):   # noqa: A002
        return self._c('tele/field_end', id=id)

    # presets, sounds, props, HUD
    def fx(self, name, **a):
        return self._c(f'p/{name}', **a)

    def fxe(self, name, el, **a):
        return self._c(f'p/{name}/{int(el)}', **a)

    def snd(self, name):
        return self._c(f'snd/{name}')

    def snde(self, name, el):
        return self._c(f'snd/{name}/{int(el)}')

    def prop(self, name):
        return self._c(f'prop/{name}')

    def prope(self, name, el):
        return self._c(f'prop/{name}/{int(el)}')

    def hud(self, name):
        return self._c(f'hud/{name}')

    def hude(self, name, el):
        return self._c(f'hud/{name}/{int(el)}')

    def glyph(self, name):
        return ''

    def badge(self, el, lit):
        """Name-line badge ◈<element> (fx.md 7): dim #707070 until lit, then the element colour (plain text here)."""
        nm = {1: '불', 2: '물', 3: '번개', 4: '얼음', 5: '바위'}.get(int(el), '?')
        col = ({1: '#FF8A3D', 2: '#4FB8FF', 3: '#C58BFF', 4: '#9FE8F5', 5: '#F0A93A'}.get(int(el), '#FFFFFF')
               if lit else '#707070')
        return f'{{text:"  ◈{nm}",color:"{col}",bold:false}}'

    def brand_badge(self, el):
        """The third badge ◈낙인 while branded, in the brand element's colour (az_fx_api.md K.brand_badge)."""
        col = {1: '#FF8A3D', 2: '#4FB8FF', 3: '#C58BFF', 4: '#9FE8F5', 5: '#F0A93A'}.get(int(el), '#FFFFFF')
        return f'{{text:"  ◈낙인",color:"{col}",bold:false}}'


try:
    import build_mboss_az_fx as K  # noqa: E402  (S1-FX's kit; no files written on import)
    KIT = True
except ImportError:
    K = KitStub()
    KIT = False


# =============================================================================================
BODY = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
PLAYER = '@e[tag=rlk_body,limit=1]'
ARENA_M = '@e[type=minecraft:marker,tag=rlk_mb_arena,limit=1]'
LOCK = '@e[type=minecraft:marker,tag=rlk_mb_az_lock,limit=1]'
KINDS = ('normal', 'cast', 'bg', 'special', 'service')
HOOKS = ('vis', 'pj_end', 'pause', 'resume', 'reload', 'cast', 'ctick', 'refresh', 'bgtick', 'cancel_bg', 'b3tick', 'stop')
GATES = ('anchor8', 'front35', 'exit', 'field_area', 'no_bg', 'no_live')
# s2.md 2: the files every pattern of a kind writes (services 20-23 also `reload`; 31 declares refresh / bgtick /
# cancel_bg / reload in its hooks); the build asserts them.
REQ_HOOKS = {'normal': ('start', 'tick', 'cancel'), 'bg': ('start', 'tick', 'cancel', 'bgtick', 'cancel_bg', 'reload'),
             'cast': ('cast', 'ctick', 'cancel'), 'special': ('start', 'b3tick', 'stop', 'cancel', 'reload'),
             'service': ('start', 'tick', 'cancel')}


class Pattern:
    """One pattern a module provides (s2.md section 2)."""

    def __init__(self, id, key, label, kind, clip, phases=(1, 2, 3), elem=None, weight=None, phase_weight=None,  # noqa: A002
                 cooldown=0, lead=0, recover=18, max_len=120, length=None, gates=(), replaces=None, hooks=()):
        assert kind in KINDS, (key, kind)
        assert 0 <= lead <= 10, (key, lead)
        assert all(g in GATES for g in gates), (key, gates)
        assert all(h in HOOKS for h in hooks), (key, hooks)
        assert elem is None or (elem[0] in ('leg', 'tail') and elem[1] in (LEG_ELS if elem[0] == 'leg' else TAIL_ELS)), elem
        if isinstance(clip, dict):
            assert clip['by'] in ('paw', 'side') and all(c in CLIPS for c in clip['map'].values()), clip
        elif clip is not None:
            assert clip in CLIPS, (key, clip)
        for zw in [weight or {}] + list((phase_weight or {}).values()):
            assert set(zw) <= set(ZONES), (key, zw)
            assert all(0 <= v <= 9 for v in zw.values()), (key, zw)
        self.id, self.key, self.label, self.kind, self.clip = id, key, label, kind, clip
        self.phases, self.elem = tuple(phases), elem
        self.weight = dict(weight or {})
        self.phase_weight = {int(k): dict(v) for k, v in (phase_weight or {}).items()}
        self.cooldown, self.lead, self.recover, self.max_len = int(cooldown), int(lead), int(recover), int(max_len)
        self.length = int(length) if length is not None else self.max_len - 4
        assert 0 < self.length <= self.max_len, (key, self.length, self.max_len)
        self.gates, self.replaces, self.hooks = tuple(gates), replaces, tuple(hooks)
        self.module = None

    def w_in(self, ph, zone):
        """Weight of this pattern in phase ph and zone (0 = never); ai.WEIGHT_OVERRIDE applies on top."""
        if ph not in self.phases:
            return 0
        if ph in self.phase_weight:
            return self.phase_weight[ph].get(zone, 0)
        return self.weight.get(zone, 0)

    def clips(self):
        if isinstance(self.clip, dict):
            return list(self.clip['map'].values())
        return [self.clip] if self.clip else []


# =============================================================================================
OWN_KEYS = {
    'geo_a': {'chin', 'jump', 'charge', 'spikes'},
    'geo_b': {'stomp', 'stomp3', 'feint', 'whip', 'tailslam', 'burrow'},
    'leg': {'orbs', 'meteor', 'firefield'},
    'tail': {'frost', 'bolt', 'icicle', 'shell', 'icespike', 'elspike'},
    'trans': {'slide', 'absorb1', 'absorb2', 'burrow3'},
    'seq': set(),
    'core': None,                      # the core writes anywhere it owns
}
OWN_X = {'leg': 'xl', 'tail': 'xt'}
AFTER = {}                             # rel -> after-dispatch id (N13)


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


def _hz_opts_kw():
    try:
        return set(inspect.signature(L.hz_opts).parameters)
    except (TypeError, ValueError):
        return set()


_HZK, _PJK = _hz_opts_kw(), set(inspect.signature(L.pj_opts).parameters)


COMMANDS = {'execute', 'function', 'scoreboard', 'data', 'tag', 'kill', 'summon', 'tp', 'teleport', 'tellraw', 'title',
            'particle', 'playsound', 'stopsound', 'schedule', 'return', 'effect', 'attribute', 'ride', 'damage', 'bossbar',
            'forceload', 'setblock', 'fill', 'item', 'rotate', 'team', 'clear', 'give', 'spreadplayers', 'random', 'gamerule',
            'stopwatch', 'time'}


class Gen:
    """Writer handed to every emit(gen) (s2.md 5.2). Paths are relative to F:mboss/azhdaha/."""

    def __init__(self, out):
        self.out = out
        self.files = set()
        self.owner = 'core'

    # -- files and ownership (s2.md 1)
    def w(self, rel, lines):
        flat = _flat(lines)
        assert re.fullmatch(r'[a-z0-9_/.-]+', rel), f'invalid function path {rel!r} (resource locations are lower case)'
        for ln in flat:
            cmd = ln.lstrip('$').split(' ', 1)[0]
            assert ln.startswith('#') or cmd in COMMANDS, f'{rel}: not a command line: {ln!r}'
            assert not re.search(r'scoreboard players (set|add|remove|operation) [#@][^ ]+ -?\d+( |$)', ln), \
                f'{rel}: scoreboard line without an objective: {ln!r}'
        self.out.write(f'mboss/{ID}/{rel}', flat)
        self.files.add(rel)

    def pw(self, key, name, lines):
        own = OWN_KEYS.get(self.owner)
        assert own is None or key in own, f'{self.owner} may not write p/{key}/ (s2.md 1)'
        self.w(f'p/{key}/{name}', lines)

    def xw(self, rel, lines):
        """Addon bodies: AZ:xl/<rel> (leg.py) or AZ:xt/<rel> (tail.py) only."""
        d = OWN_X.get(self.owner)
        assert d, f'{self.owner} may not write addon bodies (xl/ is leg.py\'s, xt/ is tail.py\'s)'
        self.w(f'{d}/{rel}', lines)

    def sw(self, rel, lines):
        assert self.owner in ('seq', 'core'), f'{self.owner} may not write seq/'
        self.w(f'seq/{rel}', lines)

    def has(self, rel):
        return rel in self.files

    @staticmethod
    def fn(rel):
        return f'function {NS}{rel}'

    # -- rig calls (manifest.md 7)
    @staticmethod
    def play(clip):
        return f'function {play_fn(clip)}'

    @staticmethod
    def look_legs():
        """The rolled leg element's legs look (runtime, #azLeg)."""
        return f'function {NS}look/legs'

    @staticmethod
    def look_tail():
        return f'function {NS}look/tail'

    @staticmethod
    def glow(on):
        return f'function {rig_fn("glow/gold_on" if on else "glow/gold_off")}'

    @staticmethod
    def flash(group):
        assert group in SR.FLASH_GROUPS, group
        return f'function {rig_fn("flash/" + group)}'

    @staticmethod
    def face(kind):
        assert kind in ('player', 'track'), kind
        return f'function {rig_fn("face/" + kind)}'

    # -- the slot (s2.md 3)
    @staticmethod
    def end():
        return f'function {NS}p/end'

    @staticmethod
    def release():
        return f'function {NS}p/release'

    @staticmethod
    def set_len(t):
        return f'scoreboard players set #azPLen mb {int(t)}'

    # -- positions
    @staticmethod
    def lockp():
        """Marker rlk_mb_az_lock on the floor under the player, pulled inside the walk disc (any executor)."""
        return f'function {NS}u/lockp'

    @staticmethod
    def lockb(r=BODY_R):
        """The lock pulled into the body disc r (a point the body moves to)."""
        if abs(r - BODY_R) < 1e-9:
            return f'function {NS}u/lockb'
        return f'function {NS}u/lockb_r {{r:{L.num(float(r))}}}'

    @staticmethod
    def lockv(lead):
        """The framework predictive lock (cm.md 13.1) at pos + v x lead, re-tagged rlk_mb_az_lock."""
        return [f'kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]', fw('mv/lockv', f'{{lead:{int(lead)}}}'),
                'tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_lock',
                'tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] remove rlk_mb_lock']

    @staticmethod
    def keep(new_tag, src='rlk_mb_az_lock'):
        return [f'kill @e[type=minecraft:marker,tag={new_tag}]',
                f'tag @e[type=minecraft:marker,tag={src}] add rlk_mb_az_kept',
                f'tag @e[type=minecraft:marker,tag={src}] add {new_tag}',
                f'tag @e[type=minecraft:marker,tag={new_tag}] remove {src}',
                f'tag @e[type=minecraft:marker,tag={new_tag}] remove rlk_mb_lock']

    @staticmethod
    def clamp_walk():
        return f'function {NS}u/clamp_w'

    @staticmethod
    def clamp_body(r=BODY_R):
        if abs(r - BODY_R) < 1e-9:
            return f'function {NS}u/clamp_b'
        return f'function {NS}u/clamp_r {{r:{L.num(float(r))}}}'

    @staticmethod
    def clamp_safe():
        return f'function {NS}u/clamp_s'

    @staticmethod
    def bstep(kind, d):
        assert kind in ('toward', 'away', 'fwd'), kind
        return f'function {NS}u/{kind} {{d:{L.num(float(d))}}}'

    @staticmethod
    def tag_last_hz(tag):
        return f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add {tag}'

    @staticmethod
    def at(t, cmd, clock='#azPT'):
        if isinstance(t, tuple):
            return f'execute if score {clock} mb matches {t[0]}..{t[1]} run {cmd}'
        return f'execute if score {clock} mb matches {t} run {cmd}'

    MODULI = (2, 3, 4, 5, 6, 8, 10, 20, 34)

    @staticmethod
    def every(n, cmd, start=0, clock='#azPT'):
        assert n in Gen.MODULI, n
        return [f'scoreboard players operation #azM mb = {clock} mb', f'scoreboard players operation #azM mb %= #azK{n} mb',
                f'execute if score #azM mb matches {start} run {cmd}']

    # -- hazard / projectile options with the module defaults (quiet, no framework sound, NoRx)
    @staticmethod
    def hz_opts(**kw):
        kw.setdefault('quiet', 1)
        kw.setdefault('sfx', 0)
        norx = kw.pop('norx', 1)
        safe_g = kw.pop('safe_g', None)
        out = []
        if 'norx' in _HZK:
            kw['norx'] = norx
        elif norx and fw_has('pl_dot'):
            out.append('scoreboard players set #hzNR mb 1')
        if safe_g is not None:
            if 'safe_g' in _HZK:
                kw['safe_g'] = safe_g
            else:
                out.append(f'scoreboard players set #hzSafeG mb {int(safe_g)}')
        return L.hz_opts(**kw) + out

    @staticmethod
    def pj_opts(**kw):
        norx = kw.pop('norx', 1)
        nododge = kw.pop('nododge', None)
        out = []
        if 'norx' in _PJK:
            kw['norx'] = norx
        elif norx and fw_has('pl_dot'):
            out.append('scoreboard players set #pjNR mb 1')
        if nododge is not None:
            if 'nododge' in _PJK:
                kw['nododge'] = nododge
            else:
                out.append(f'scoreboard players set #pjNoDodge mb {int(nododge)}')
        return L.pj_opts(**kw) + out

    @staticmethod
    def el_ground():
        """#hzEl / #pjEl = the ground element now (#azE: Geo in phase 1, the leg element from phase 2)."""
        return ['scoreboard players operation #hzEl mb = #azE mb', 'scoreboard players operation #pjEl mb = #azE mb']

    @staticmethod
    def el_tail():
        return ['scoreboard players operation #hzEl mb = #azET mb', 'scoreboard players operation #pjEl mb = #azET mb']

    @staticmethod
    def el(n):
        return [f'scoreboard players set #hzEl mb {int(n)}', f'scoreboard players set #pjEl mb {int(n)}']

    hz_disc = staticmethod(L.hz_disc)
    hz_ring = staticmethod(L.hz_ring)
    hz_sector = staticmethod(L.hz_sector)
    hz_line = staticmethod(L.hz_line)
    hz_full = staticmethod(L.hz_full)
    hz_aim = staticmethod(L.hz_aim)
    hz_resize = staticmethod(L.hz_resize)
    pj_launch = staticmethod(L.pj_launch)
    pj_steer = staticmethod(L.pj_steer)
    GRP_NEW = L.GRP_NEW

    @staticmethod
    def hz_mask(r0, tell, dmg):
        """N4 (cm.md 13.6): the mask hazard over everything outside the rlk_mb_hzsafe markers of its group."""
        if hasattr(L, 'hz_mask'):
            return L.hz_mask(r0, tell, dmg)
        return [f'scoreboard players set #hzR0 mb {int(round(r0 * 10))}', fw('hz/mask', f'{{tell:{int(tell)},dmg:{int(dmg)}}}')]

    @staticmethod
    def hz_extend(n):
        return fw('hz/extend', f'{{n:{int(n)}}}')

    # -- the kit (fx.md; api.K)
    kit = K

    @staticmethod
    def _el_store(el, path='az.tl.el'):
        if el == 'ground':
            return [f'execute store result storage rlk:mboss {path} int 1 run scoreboard players get #azE mb']
        if el == 'tail':
            return [f'execute store result storage rlk:mboss {path} int 1 run scoreboard players get #azET mb']
        return [f'data modify storage rlk:mboss {path} set value {int(el)}']

    def ktele(self, shape, el='ground', **args):
        """A kit telegraph with a runtime element: storage rlk:mboss az.tl, then fx/tele/<shape> with storage (sizes in
        blocks here, tenths in storage; ticks as given)."""
        tenths = {'r', 'r0', 'r1', 'len', 'w', 'back', 'h'}
        vals = ','.join(f'{k}:{int(round(v * 10)) if k in tenths else int(v)}' for k, v in args.items())
        lines = [f'data modify storage rlk:mboss az.tl set value {{{vals}}}'] + self._el_store(el)
        if KIT:
            lines.append(f'function {K.FN}tele/{shape} with storage rlk:mboss az.tl')
        else:
            lines.append(K._c(f'tele/{shape}', **args))
        return lines

    @staticmethod
    def fx(name, **a):
        return K.fx(name, **a)

    def fxe(self, name, el, **a):
        """A per-element preset; el int, or 'ground' / 'tail' (runtime: a 5-line dispatch on #azE / #azET)."""
        if el in ('ground', 'tail'):
            sc = '#azE' if el == 'ground' else '#azET'
            return [f'execute if score {sc} mb matches {e} run {K.fxe(name, e, **a)}' for e in (1, 2, 3, 4, 5)]
        return K.fxe(name, el, **a)

    @staticmethod
    def snd(name):
        return K.snd(name)

    def snde(self, name, el):
        if el in ('ground', 'tail'):
            sc = '#azE' if el == 'ground' else '#azET'
            return [f'execute if score {sc} mb matches {e} run {K.snde(name, e)}' for e in (1, 2, 3, 4)]
        return K.snde(name, el)

    @staticmethod
    def kprop(name):
        return K.prop(name)

    def kprope(self, name, el):
        if el in ('ground', 'tail'):
            sc = '#azE' if el == 'ground' else '#azET'
            return [f'execute if score {sc} mb matches {e} run {K.prope(name, e)}' for e in (1, 2, 3, 4, 5)]
        return K.prope(name, el)

    @staticmethod
    def khud(name):
        return K.hud(name)

    # -- vanilla single layers
    @staticmethod
    def sound(event, vol=1.0, pitch=1.0):
        return L.sound(event, vol, pitch)

    @staticmethod
    def dust(rgb, scale=1.0, pos='~ ~ ~', delta=(0, 0, 0), n=1, speed=0):
        c = L.colour_list(rgb)
        d = ' '.join(L.num(float(v), 3) for v in delta)
        return f'particle minecraft:dust{{color:{c},scale:{L.num(float(scale), 2)}}} {pos} {d} {L.num(float(speed), 3)} {int(n)} force @a[tag=player]'

    @staticmethod
    def particle(name, pos='~ ~ ~', delta=(0, 0, 0), speed=0, n=1):
        d = ' '.join(L.num(float(v), 3) for v in delta)
        return f'particle minecraft:{name} {pos} {d} {L.num(float(speed), 3)} {int(n)} force @a[tag=player]'

    @staticmethod
    def line(text, hold=50):
        """Typed line, speaker 야타용왕 in gold (plan.md 4.13 texts verbatim; no voice)."""
        return L.say(text, GOLD_HEX, 2, hold, 2)

    # -- N10 fronts
    def wave(self, tl, strike, r0, r1, spd, band, tell, dmg, nd=0, el='ground', grp='new', low=0.7, ease=None, wid=0,
             tag=None, kb=None, tele='none'):
        """N10 on the TL `tl`: at strike - tell a hz/ring {r0:0, r:r0} (the slam disc, quiet: no framework outline);
        from the strike the front grows each tick (r = r0 + spd k, or the ease knots [(dt, r), ...] linearly) with the
        hazard's inner edge band behind it (hz/resize every tick), the kit front preset 1 t before the strike. Asserts
        band >= the per-tick advance (plan rule 5). grp 'new' (its own volley group), 'ctx' (#azCtxGrp: addon bodies),
        'cur' (the current #mbGrp) or None. Returns the last front tick.
        tele (plan Change note 1, the 10-20 telegraph rule): 'none' (default; every N10 front of plan 5 is a *none* row:
        P2, P5, P5b, T1, the Cryo rings) draws no pre-strike decal: the kit tele/wave {id:wid} ring is called 1 t before
        the strike with tell 1 and nd 0, so only the travelling front (the hazard's own visual) shows; 'keep' = the old pairing
        (the tele/wave fill from strike - tell). `tell` stays the hazard's internal tell (N7 #mbDodgeOk, the brand's
        perfect dodge); the readable tell of a *none* row is its clip pose / sound (TABLE tell_src)."""
        assert tell >= 12, tell
        assert tele in ('none', 'keep'), tele
        radii = []
        if ease:
            pts = [(0, r0)] + [(int(dt), float(r)) for dt, r in ease]
            for (t0, a), (t1, b) in zip(pts, pts[1:]):
                for k in range(t0 + 1, t1 + 1):
                    radii.append(a + (b - a) * (k - t0) / (t1 - t0))
        else:
            r = r0
            while r < r1 - 1e-9:
                r = min(r1, r + spd)
                radii.append(r)
        prev = r0
        for r in radii:
            assert band + 1e-9 >= r - prev, ('front band < per-tick advance (plan rule 5)', band, r - prev)
            prev = r
        n = len(radii)
        tag = tag or f'rlk_mb_az_wv{wid}'
        made = strike - tell
        opts = dict(act=n + 1, y1=low if low else None, nododge=1 if nd else None)
        if kb is not None:
            opts['kb'] = kb
        lines = []
        if grp == 'new':
            lines.append(self.GRP_NEW)
        lines += [f'kill @e[type=minecraft:marker,tag={tag}]']
        lines += self.hz_opts(grp=grp in ('new', 'cur'), **{k: v for k, v in opts.items() if v is not None})
        if grp == 'ctx':
            lines.append('scoreboard players operation #hzGrp mb = #azCtxGrp mb')
        lines += (self.el_ground() if el == 'ground' else self.el_tail() if el == 'tail' else self.el(el))
        lines += [L.hz_ring(0, r0, tell, dmg), self.tag_last_hz(tag)]
        # 'none': the plain ring (nd 0: the shared undodgeable look lost its users, Change note 1 on plan rule 6)
        ring = self.ktele('wave', el, id=wid, r0=r0, r1=r1, w=band, tell=(tell if tele == 'keep' else 1), dur=n,
                          nd=((2 if nd and low else nd) if tele == 'keep' else 0), hold=3)
        if tele == 'keep':
            lines += ring
        tl.at(made, *lines)
        if strike - 1 >= made:
            # REQ ps-1 / pa-1 (one fix): K.fxe takes blocks and converts to tenths itself (tenths gave a 10x front)
            tl.at(strike - 1, *(([] if tele == 'keep' else ring)
                                + _flat([self.fxe('front', el, r0=r0, r1=r1, w=band, dur=n)])))
        for k, r in enumerate(radii, 1):
            tl.at(strike + k, f'execute as @e[type=minecraft:marker,tag={tag}] run '
                              f'{L.hz_resize(r, max(0.0, r - band))}')
        tl.at(strike + n + 1, f'tag @e[type=minecraft:marker,tag={tag}] remove {tag}')
        return strike + n

    # -- N6 lingering fields
    def field(self, fam, r, life, dmg, el='ground', shape='disc', len=None, w=None, yaw=None, rule=False):   # noqa: A002
        """N6 (s2.md 9): a lingering field positioned here (disc centre / line start; line yaw = yaw or the context
        rotation). rule=True: a fire-rule field (exempt from the clear melee points). Returns lines."""
        assert fam in FIELD_CAPS, fam
        assert shape in ('disc', 'line')
        sh = 1 if shape == 'line' else 0
        if sh:
            assert len and w, 'a line field needs len and w'
            area = int(round(len * w))
        else:
            area = int(round(math.pi * r * r))
        vals = (f'fam:{FIELD_FAM[fam]},r:{int(round((r or 0) * 10))},len:{int(round((len or 0) * 10))},'
                f'w:{int(round((w or 0) * 10))},life:{int(life)},dmg:{int(dmg)},sh:{sh},area:{area},rule:{1 if rule else 0},'
                f'yaw:{-999 if yaw is None else int(yaw)}')
        return [f'data modify storage rlk:mboss az.nf set value {{{vals}}}'] + self._el_store(el, 'az.nf.el') + [
            f'function {NS}fld/new']

    @staticmethod
    def field_refresh(sel, n):
        """N6 refresh: extend the field hazard(s) `sel` by n ticks, at most 2x its base life; the kit redraws it."""
        return f'execute as {sel} run function {NS}fld/refresh {{n:{int(n)}}}'

    # -- N5 orbit mover
    @staticmethod
    def orbit_spawn(tag, ring, k, r, omega, a0, hr, band, dmg, grp=True):
        """N5: one orb (prop + hz/disc r hr, #hzRearm 10) at angle a0 + 90 k of ring `ring` (radius r, omega deg/t,
        + = clockwise from above) about the orbit centre rlk_mb_az_orbc; band (y0, y1) blocks; grp True = the
        current #mbGrp (all orbs one volley group). As the body, positioned at the orbit centre."""
        y0, y1 = band
        return [f'data modify storage rlk:mboss az.orb set value {{tag:"{tag}",ring:{int(ring)},a:{int(round((a0 + 90 * k) * 100))},'
                f'r:{int(round(r * 1000))},w:{int(round(omega * 100))},hr:{int(round(hr * 10))},y0:{int(round(y0 * 10))},'
                f'y1:{int(round(y1 * 10))},dmg:{int(dmg)},grp:{1 if grp else 0}}}',
                f'function {NS}orb/spawn with storage rlk:mboss az.orb']

    @staticmethod
    def orbit_tick(tag):
        """N5: every orb `tag` one step (angle += omega, plain tp of the prop and its hazard, the band rules)."""
        return f'execute as @e[type=minecraft:marker,tag={tag}] run function {NS}orb/step'

    @staticmethod
    def orbit_end(tag):
        return [f'kill @e[tag={tag}]', f'execute unless entity @e[tag=rlk_mb_az_orb] run kill @e[tag=rlk_mb_az_orbc]']

    # -- N13 addon points and timers
    @staticmethod
    def addon(point):
        """Call the addon point here (positioned / rotated as the context, the context scores set): the context
        marker moves here, then the core dispatcher AZ:x/<point_key> runs as the body at it (s2.md 10.1)."""
        d = ADDON_POINTS[point]
        return [f'function {NS}x/ctx',
                f'execute as {BODY} at @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] rotated as '
                f'@e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] run function {NS}x/{d["key"]}']

    def after(self, delay, rel):
        """N13: run F:mboss/azhdaha/<rel> `delay` module ticks later, as the body at this position / rotation."""
        assert 1 <= delay <= 2000, delay
        own = OWN_KEYS.get(self.owner)
        if own is not None:
            ok = any(rel.startswith(f'p/{k}/') for k in own) or (self.owner in OWN_X and rel.startswith(OWN_X[self.owner] + '/')) \
                or (self.owner == 'seq' and rel.startswith('seq/'))
            assert ok, f'{self.owner}: after() target {rel} is not in its own paths'
        if rel not in AFTER:
            AFTER[rel] = len(AFTER) + 1
        return [f'scoreboard players set #azAftF mb {AFTER[rel]}', f'scoreboard players set #azAftD mb {int(delay)}',
                f'function {NS}aft/new']

    # -- core services (S2-S: transitions and sequences)
    @staticmethod
    def cast_leg():
        return f'function {NS}cast/leg'

    @staticmethod
    def cast_end():
        return f'function {NS}cast/end'

    @staticmethod
    def bg_start(slot):
        assert slot in ('L', 'T')
        return f'function {NS}bg/start_{slot.lower()}'

    @staticmethod
    def bg_end(slot):
        assert slot in ('L', 'T')
        return f'function {NS}bg/end_{slot.lower()}'

    @staticmethod
    def b3_special(op):
        """The B3 special dispatchers (s2.md 7.2): start / tick / stop / reload / cancel of p/<frost|bolt>/ by #azTail."""
        assert op in ('start', 'tick', 'stop', 'reload', 'cancel')
        return f'function {NS}b3/special_{op}'

    @staticmethod
    def music(ph):
        return f'function {NS}svc/music_{int(ph)}'

    @staticmethod
    def cine(on):
        return f'function {NS}svc/cine_{"on" if on else "off"}'

    @staticmethod
    def px(name):
        assert name in SR.STATES, name
        return f'function {NS}px/{name}'

    @staticmethod
    def arena_look(el):
        """N17: the arena props to the element look (int, 'leg', 'tail', 'geo'), as a recolour wave."""
        k = {'leg': 'leg', 'tail': 'tail', 'geo': 'geo', 5: 'geo'}.get(el, el)
        return f'function {NS}arena/look_{k}'

    @staticmethod
    def phase(n):
        assert n in (1, 2, 3)
        return f'function {NS}svc/phase_{n}'

    @staticmethod
    def floor(expr):
        """#mbFloor: 'f1' (2/3 of the pool), 'f2' (1/3), 1 or 0."""
        return f'function {NS}svc/floor_{expr}'

    @staticmethod
    def banner(kind):
        """Kit banners of the transitions (fx.md 7): 'tr' (leg / tail element by the step), 'ab', 'ab2', 'brand'."""
        assert kind in ('tr', 'ab', 'ab2', 'brand', 'end')
        return f'function {NS}svc/banner_{kind}'


class TL:
    """Per-tick timeline of one pattern (fieldgen TL): lines grouped into p/<key>/<sub>/<t> and reached through a
    binary dispatch tree on the clock (#azPT by default; cast slot #azCT with sub 'ck', bg slots #azBgLT / #azBgTT
    with 'bk', the B3 clock #azB3T with 'b3k').

        tl = TL(g, 'chin'); tl.at(8, cmd); tl.span(10, 14, cmd); tl.write(start_head, tick_head, t0=-lead)"""

    def __init__(self, g, key, clock='#azPT', sub='k'):
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


# =============================================================================================
# Per-author helpers, re-exported (s2.md 1). Each stage adds only its own line.
from .h_core import *  # noqa: E402,F401,F403
from .h_ps import *  # noqa: E402,F401,F403  (REQ ps-2)

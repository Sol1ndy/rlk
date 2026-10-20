"""야타용왕 (Azhdaha) stub rig: the per-clip fallbacks of the rig manifest (schema v1) and the stand-in rig runtime.

Contract: scratchpad az/contract/manifest.md (schema v1: sections 2-8; the stub rules of section 8; the R1 -> v1
migration of section 10). Owner S1-MOD. Two jobs:

1. DATA (pure, importable without side effects; api.py imports it): `stub_manifest()` returns the full v1 manifest
   ("source": "stub") with every clip of manifest.md section 5 (41 entries: 35 authored + 6 mirrors) built from the
   binding clip table below (lengths, authored lengths, RETIME knots, played events) and a parametric body: anchors
   from the rest anchors (R1 rest numbers), dense tail tracks from a parametric tail (root at rest, tip 12 b behind
   it; raised for tail_slam / tail_cast, vertical for the pillar clips), proxy keys at 0 and len-1 (+ the span
   boundaries of hidden spans and tail-only states), the yaw schedules of section 4.5, the hidden spans / root_z /
   state switches of sections 4.6-4.7, and the R1 globals (proxies, states, capsules, flash groups, looks, parts with
   the fixed UUID name table, culling, budgets). `migrate_r1(r1)` is the section-10 migration of the R1 rig manifest
   (wip/az-rig 7c3e9fe: no "schema"): px per event in the rig frame {x, z, base, top, w, hidden} -> per-tick keys
   [x, -z, top] in the local frame (R1 rig +z = back, the local frame z = forward: the z flip the D0 report flagged),
   base dropped, hidden -> top 0; the R1 debug poses become dbg_<name>; the globals are kept / added.
   `merge(real, stub)` is the per-clip merge of manifest.md section 1 (real clips first; stub clips only for names the
   real manifest lacks, with ids >= 1000; the globals from the real file when it is v1 from the rig).

2. RUNTIME (emit(g), called by core.build): writes T:mboss_azhdaha/stub_rig_manifest.json (the framework compiles the
   hit proxies, capsules and state sets from it while no v1 rig manifest exists, cm.md 9.2) and the stand-in rig
   F:mboss/azhdaha/rig_stub/** with the rig API of manifest.md section 7 (init, spawn, tick, kill, uninstall,
   look_apply, play/<clip>, face/{player,track,set}, state/<normal|burrowed|tail_only>, look/legs/<geo|hydro|pyro>,
   look/tail/<geo|cryo|electro>, look/petrify, glow/gold_on|off, flash/<head|front|rear|tail>) + chain (loop / next of
   stub clips while a real rig ticks). Clips keep time only (azRigC / azRigT exactly as the R1 rig, so the
   framework's px/tick reads the right clip tick); the figure is a crude vanilla stand-in (a tuff torso, a blackstone
   head, a log tail) that follows the anchor, hides in the burrow states and stands the tail up in the tail-only
   state, so a test fight in game is readable.

The module calls the real rig (F:mboss/azhdaha/rig/**) for every API function the real rig provides and this stub for
the rest (api.rig_fn); play/<clip> goes to the real rig only for clips the real v1 manifest has (api.play_fn). The I2b
build asserts that no clip falls back (api.FALLBACKS empty).
"""
import copy
import json
import math

SCHEMA = 1
BOSS = 'azhdaha'
NS_RIG = 'rlk:mboss/azhdaha/rig/'
NS_STUB = 'rlk:mboss/azhdaha/rig_stub/'
STUB_ID0 = 1000                       # stub clip ids (never a rig id, cm.md 9.2)
UUID_BLOCK = '524c4b4d-415a-4400-8000-0000000000'
UUID_INTS = [1380731725, 1096434688, -2147483648]
PX_BASE = 0x41

OBJECTIVES = {'azRigC': 'current clip id (anchor)', 'azRigT': 'tick within the clip (anchor; -1 = queued by play)',
              'azRigF': 'hit flash countdown', 'azRigY': 'face/track scratch',
              'azRigLegs': 'legs look: 0 geo, 1 hydro, 2 pyro', 'azRigTail': 'tail look: 0 geo, 1 cryo, 2 electro',
              'azRigState': 'body state: 0 normal, 1 burrowed, 2 tail-only'}
RUNTIME = {'clip_obj': 'azRigC', 'tick_obj': 'azRigT', 'state_obj': 'azRigState', 'legs_obj': 'azRigLegs',
           'tail_obj': 'azRigTail'}

# ---------------------------------------------------------------------------------------------
# The binding clip table (manifest.md section 5 = plan.md 3.2): name, played len, authored len, loop, next, RETIME
# knots (authored -> played), played events. Mirrors are listed by MIRRORS (name -> source).
CLIP_TABLE = [
    ('idle', 80, 80, True, None, [], {'snarl': 30}),
    ('walk', 40, 40, True, None, [], {'lh': 0, 'lf': 10, 'rh': 20, 'rf': 30}),
    ('walk_stop', 16, 16, False, 'idle', [], {'plant': 4}),
    ('turn45_l', 24, 24, False, 'idle', [], {'plant_1': 10, 'plant_2': 17, 'yaw0': 4, 'yaw1': 18}),
    ('turn45_r', 24, 24, False, 'idle', [], {'plant_1': 10, 'plant_2': 17, 'yaw0': 4, 'yaw1': 18}),
    ('turn90_l', 36, 36, False, 'idle', [], {'plant_1': 12, 'plant_2': 18, 'plant_3': 24, 'plant_4': 30, 'yaw0': 6, 'yaw1': 30}),
    ('turn90_r', 36, 36, False, 'idle', [], {'plant_1': 12, 'plant_2': 18, 'plant_3': 24, 'plant_4': 30, 'yaw0': 6, 'yaw1': 30}),
    ('turn180', 60, 60, False, 'idle', [], dict({f'plant_{k + 1}': 12 + 6 * k for k in range(8)}, yaw0=6, yaw1=54)),
    ('intro', 150, 150, False, 'idle', [], {'eyes': 25, 'rise': 30, 'crack1': 50, 'crack2': 70, 'seal': 112, 'land': 116,
                                           'roar': 120, 'blast': 130}),
    ('pose_ref', 20, 20, True, None, [], {}),
    ('roar_low', 40, 50, False, 'idle', [[0, 0], [10, 8], [50, 40]], {'roar': 8, 'blast': 10}),
    ('roar_rear', 82, 100, False, 'idle', [[0, 0], [20, 20], [76, 62], [100, 82]], {'rise': 8, 'roar': 20, 'drop': 62, 'land': 74}),
    ('chin_slam', 65, 84, False, 'idle', [[0, 0], [47, 35], [84, 65]], {'lift': 2, 'rear': 14, 'top': 23, 'drop': 32, 'impact': 35}),
    ('jump_slam', 53, 60, False, 'idle', [[0, 0], [28, 21], [60, 53]], {'crouch': 0, 'takeoff': 6, 'apex': 13, 'land': 21, 'wave2': 32}),
    ('charge_coil', 26, 34, False, 'charge_run', [[0, 0], [32, 24], [34, 26]], {'coil': 6, 'launch': 24}),
    ('charge_run', 12, 12, True, None, [], {'plant': 6}),
    ('charge_stop', 21, 24, False, 'idle', [[0, 0], [8, 8], [24, 21]], {'skid': 0, 'stop': 8}),
    ('spikes', 40, 48, False, 'idle', [[0, 0], [18, 14], [24, 20], [48, 40]],
     {'brace': 0, 'launch': 14, 'launch_last': 20, 'gold_on': 0, 'gold_off': 22}),
    ('stomp_fl', 63, 72, False, 'idle', [[0, 0], [22, 17], [52, 47], [72, 63]], {'lift': 5, 'slam': 13, 'w1': 17, 'w2': 32, 'w3': 47}),
    ('stomp_fr', 63, 72, False, 'idle', [[0, 0], [22, 17], [52, 47], [72, 63]], {'lift': 5, 'slam': 13, 'w1': 17, 'w2': 32, 'w3': 47}),
    ('stomp_hl', 63, 72, False, 'idle', [[0, 0], [22, 17], [52, 47], [72, 63]], {'lift': 5, 'slam': 13, 'w1': 17, 'w2': 32, 'w3': 47}),
    ('stomp_hr', 63, 72, False, 'idle', [[0, 0], [22, 17], [52, 47], [72, 63]], {'lift': 5, 'slam': 13, 'w1': 17, 'w2': 32, 'w3': 47}),
    ('stomp3_fl', 85, 90, False, 'idle', [[0, 0], [22, 17], [90, 85]], {'lift': 3, 's1': 17, 's2': 40, 's3': 63}),
    ('stomp3_fr', 85, 90, False, 'idle', [[0, 0], [22, 17], [90, 85]], {'lift': 3, 's1': 17, 's2': 40, 's3': 63}),
    ('feint', 50, 56, False, 'idle', [[0, 0], [22, 22], [56, 50]], {'sway': 0, 'swayback': 12, 'drop': 18, 'burst': 22}),
    ('tail_whip_l', 64, 64, False, 'idle', [], {'raise': 0, 'cock': 12, 'pivot': 20, 'sweep': 23, 'sweep_end': 31, 'erupt': 33,
                                               'settle': 42}),
    ('tail_whip_r', 64, 64, False, 'idle', [], {'raise': 0, 'cock': 12, 'pivot': 20, 'sweep': 23, 'sweep_end': 31, 'erupt': 33,
                                               'settle': 42}),
    ('tail_slam', 70, 90, False, 'idle', [[0, 0], [52, 39], [58, 45], [90, 70]],
     {'raise': 0, 'hold': 9, 'slam': 36, 'impact': 39, 'spikes': 41}),
    ('burrow_dive', 40, 44, False, 'burrow_travel', [[0, 0], [18, 14], [44, 40]], {'snarl': 3, 'dive': 14, 'under': 40}),
    ('burrow_travel', 20, 20, True, None, [], {}),
    ('burrow_breach', 36, 36, False, 'burrow_travel', [], {'ring': 0, 'burst': 8, 'hit': 10, 'under': 30}),
    ('burrow_emerge', 53, 56, False, 'idle', [[0, 0], [40, 40], [56, 53]], {'rumble': 0, 'burst': 8, 'fore': 24, 'out': 38, 'shake': 40}),
    ('landslide', 203, 270, False, 'idle',
     [[0, 0], [76, 57], [104, 77], [132, 98], [156, 118], [186, 139], [212, 159], [240, 179], [270, 203]],
     {'tell': 0, 'w1': 57, 'w2': 77, 'w3': 98, 'w4': 118, 'w5': 139, 'rear': 159, 'w6': 179, 'end': 203}),
    ('absorb', 94, 108, False, 'idle', [[0, 0], [12, 12], [60, 46], [108, 94]],
     {'press': 0, 'rise': 46, 'burst': 47, 'stamp1': 62, 'stamp2': 86, 'gold_on': 0, 'gold_off': 60}),
    ('absorb_p3', 52, 70, False, 'idle', [[0, 0], [60, 42], [70, 52]], {'orb': 0, 'burst': 42, 'gather': 42, 'gold_on': 0,
                                                                         'gold_off': 50}),
    ('p3_sink', 66, 80, False, 'tail_pillar', [[0, 0], [8, 8], [50, 40], [80, 66]], {'sink': 8, 'under': 40, 'tail': 40,
                                                                                     'pillar': 58}),
    ('tail_pillar', 80, 80, True, None, [], {'pulse': 0, 'pulse2': 40}),
    ('tail_pillar_strike', 24, 24, False, 'tail_pillar', [], {'strike': 10}),
    ('tail_pillar_sink', 20, 20, False, None, [], {'gone': 18}),
    ('tail_cast', 34, 40, False, 'idle', [[0, 0], [24, 18], [40, 34]], {'raise': 0, 'charge': 12, 'fire': 18, 'lower': 26}),
    ('death', 120, 120, False, None, [], {'stagger': 0, 'chin': 34, 'tail': 66, 'last': 80, 'head': 92, 'still': 96}),
]
MIRRORS = {'turn45_r': 'turn45_l', 'turn90_r': 'turn90_l', 'stomp_fr': 'stomp_fl', 'stomp_hr': 'stomp_hl',
           'stomp3_fr': 'stomp3_fl', 'tail_whip_r': 'tail_whip_l'}
CLIP_NAMES = [c[0] for c in CLIP_TABLE]
assert len(CLIP_NAMES) == 41 and len(set(CLIP_NAMES)) == 41 and len(MIRRORS) == 6
TRACK_CLIPS = ('tail_whip_l', 'tail_whip_r', 'tail_slam', 'tail_cast', 'tail_pillar', 'tail_pillar_strike',
               'tail_pillar_sink', 'p3_sink')
YAW_CLIPS = ('turn45_l', 'turn45_r', 'turn90_l', 'turn90_r', 'turn180', 'tail_whip_l', 'tail_whip_r')

# ---------------------------------------------------------------------------------------------
# R1 rest numbers (wip/az-rig 7c3e9fe, manifest.md 4.1 / 6.1), local frame: x = s (+ the boss's left), y up,
# z = f (+ forward). R1 rig frame z is BACK: local = (rig.x, rig.y, -rig.z).
REST_ANCHORS = {
    'nose': (0.0, 0.85, 5.5), 'head_col': (0.0, 0.0, 4.3), 'head_front': (0.0, 0.0, 6.8), 'chest': (0.0, 0.0, 2.1),
    'hips': (0.0, 0.0, -3.4), 'tail_root': (0.0, 2.85, -4.75), 'paw_fl': (3.15, 0.0, 2.95), 'paw_fr': (-3.15, 0.0, 2.95),
    'foot_hl': (2.5, 0.0, -2.55), 'foot_hr': (-2.5, 0.0, -2.55), 'back': (0.0, 4.0, -0.2),
}
TORSO_HW = 3.0
# proxies.layout (manifest.md 6.1): name, R1 part, bone-local point (rig frame; the R3a rig's points since I1), w, top
# margin, flash, tail_only, rest [x, z, top] (local; the pinned contract columns = proxies.rest of the real rig)
PROXY_LAYOUT = [
    ('head', 'head', [0, -0.6, -0.6], 2.8, 1.6, 'head', False, [0.0, 4.3, 3.05]),
    ('chest', 'chest', [0, 0, -0.4], 4.6, 1.5, 'front', False, [0.0, 2.1, 4.85]),
    ('belly', 'belly', [0, 0, 0.2], 4.6, 1.5, 'rear', False, [0.0, -0.5, 4.85]),
    ('hips', 'pelvis', [0, 0, 1], 4.4, 1.2, 'rear', False, [0.0, -3.4, 4.2]),
    ('tail1', 't1', [0, 0, 1.2], 2.6, 1.2, 'tail', True, [0.0, -6.35, 3.94]),
    ('tail2', 't3', [0, 0, 1], 2.2, 1.0, 'tail', True, [0.0, -10.12, 3.9]),
    ('tail3', 't5', [0, 0, 0.9], 1.8, 0.9, 'tail', True, [0.0, -12.86, 5.81]),
    ('tail4', 't7', [0, 0, 1.5], 1.4, 0.8, 'tail', True, [0.0, -11.9, 8.51]),
    ('paw_l', 'paw_l', [0, -0.3, -0.55], 1.8, 2.6, 'front', False, [3.15, 2.95, 2.8]),
    ('paw_r', 'paw_r', [0, -0.3, -0.55], 1.8, 2.6, 'front', False, [-3.15, 2.95, 2.8]),
    ('foot_l', 'foot_l', [0, -1.18, -0.35], 1.8, 2.6, 'rear', False, [2.5, -2.55, 2.92]),
    ('foot_r', 'foot_r', [0, -1.18, -0.35], 1.8, 2.6, 'rear', False, [-2.5, -2.55, 2.92]),
]
PROXIES = [p[0] for p in PROXY_LAYOUT]
# proxies.rest_pose (manifest.md 6.1, I1): the R3a idle columns [x, z, top] (the tail is curled up over the back in idle;
# the body columns equal `rest`). The stub keeps `rest` for its own px keys; the real rig's per-clip px rule the runtime.
REST_POSE = {'head': [0.0, 4.3, 3.05], 'chest': [0.0, 2.1, 4.85], 'belly': [0.0, -0.5, 4.85], 'hips': [0.0, -3.4, 4.2],
             'tail1': [0.0, -5.863, 4.5], 'tail2': [0.0, -8.59, 7.209], 'tail3': [0.0, -7.898, 10.434],
             'tail4': [0.0, -4.458, 11.736], 'paw_l': [3.15, 2.95, 2.8], 'paw_r': [-3.15, 2.95, 2.8],
             'foot_l': [2.5, -2.55, 2.92], 'foot_r': [-2.5, -2.55, 2.92]}
TAIL_PX = ('tail1', 'tail2', 'tail3', 'tail4')
BODY_PX = tuple(p for p in PROXIES if p not in TAIL_PX)
PILLAR_TOPS = {'tail1': 2.8, 'tail2': 4.8, 'tail3': 6.8, 'tail4': 8.8}    # tail-only: stacked at the anchor
# The fixed, append-only part name -> UUID index table (Rig decision change 3; R1's order is the initial table)
PART_TABLE = [
    ('head', 'head'), ('jaw', 'head'), ('eyes', 'head'), ('horn_l', 'head'), ('horn_r', 'head'), ('beard1', 'head'),
    ('beard2', 'head'), ('chest', 'body'), ('belly', 'body'), ('pelvis', 'body'), ('neck1', 'body'), ('neck2', 'body'),
    ('apron', 'body'), ('glow_apron', 'body'), ('plates_neck', 'body'), ('plates_sh', 'body'), ('plates_mid', 'body'),
    ('plates_hip', 'body'), ('crys_sh', 'body'), ('crys_mid', 'body'), ('crys_hip', 'body'), ('uarm_l', 'legs'),
    ('bracer_l', 'legs'), ('paw_l', 'legs'), ('uarm_r', 'legs'), ('bracer_r', 'legs'), ('paw_r', 'legs'), ('thigh_l', 'legs'),
    ('gaiter_l', 'legs'), ('foot_l', 'legs'), ('thigh_r', 'legs'), ('gaiter_r', 'legs'), ('foot_r', 'legs'),
    ('glow_bracer_l', 'legs'), ('glow_bracer_r', 'legs'), ('glow_gaiter_l', 'legs'), ('glow_gaiter_r', 'legs'),
    ('t1', 'tail'), ('t2', 'tail'), ('t3', 'tail'), ('t4', 'tail'), ('t5', 'tail'), ('t6', 'tail'), ('t7', 'tail'),
    ('t8', 'tail'), ('tip', 'tail'),
]
FLASH_GROUPS = {'head': ['head', 'jaw', 'horn_l', 'horn_r'],
                'front': ['chest', 'neck1', 'neck2', 'apron', 'uarm_l', 'uarm_r', 'bracer_l', 'bracer_r', 'paw_l', 'paw_r'],
                'rear': ['belly', 'pelvis', 'thigh_l', 'thigh_r', 'gaiter_l', 'gaiter_r', 'foot_l', 'foot_r'],
                'tail': ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 'tip']}
STATES = {
    'normal': {'px': list(PROXIES), 'vis': 'normal', 'inv': False, 'capsules': ['torso', 'head']},
    'jump': {'px': [], 'vis': None, 'inv': False, 'capsules': []},
    'inv': {'px': [], 'vis': None, 'inv': True, 'capsules': []},
    'tail_only': {'px': list(TAIL_PX), 'vis': 'tail_only', 'inv': False, 'capsules': []},
    'dead': {'px': [], 'vis': None, 'inv': True, 'capsules': []},
}
CAPSULES = {'torso': {'f0': -3.8, 'f1': 2.6, 'hw': 2.8},
            'head': {'f0': 2.6, 'f1': 5.4, 'hw': 1.6, 'px': 'head', 'top_max': 3.5}}
LOOKS_LEGS = ('geo', 'hydro', 'pyro')
LOOKS_TAIL = ('geo', 'cryo', 'electro')
VIS_STATES = ('normal', 'burrowed', 'tail_only')
CULLING = {'width': 30, 'height': 12, 'view_range': 3}
REST_EXTENTS = [[-4.09, 4.09], [-0.35, 8.27], [-5.3, 13.53]]      # R1 bookkeeping (rig frame)
SKELETON = {'joints': {'pelvis': [0, 3, 2.4], 'spine1': [0, 3.35, 0.3], 'chest': [0, 3.35, -1.7], 'neck1': [0, 3.05, -2.55],
                       'neck2': [0, 2.6, -3.05], 'head': [0, 2.05, -3.3], 'jaw': [0, 1.3, -3.6], 't1': [0, 2.85, 4.75],
                       'shoulder': [2.3, 3.25, -2.15], 'wrist': [3.15, 0.5, -2.45], 'hip': [2, 3, 2.45], 'hock': [2.5, 0.72, 3.05]},
            'scale_H': 7, 'frame': 'rig (+x left, +y up, +z back)'}
BUDGETS = {'parts': 46, 'part_budget': '44-48 (cap 56)', 'atlas_px': 947200, 'atlas_budget': 1200000,
           'regions': {'head': {'parts': 8, 'px': 300000}, 'body': {'parts': 14, 'px': 300000},
                       'legs': {'parts': 16, 'px': 320000}, 'tail': {'parts': 10, 'px': 280000}}}

# parametric tail (local frame): rest root, tip 12 b behind it
TAIL_ROOT = REST_ANCHORS['tail_root']
TAIL_TIP = (0.0, 1.0, TAIL_ROOT[2] - 12.0)           # (0, 1, -16.75)
PILLAR_ROOT, PILLAR_TIP = (0.0, 0.0, 0.0), (0.0, 8.8, 0.0)
ROOT_Z_PILLAR = -TAIL_ROOT[2]                        # +4.75: puts the tail root (the pillar base) on the anchor


# ---------------------------------------------------------------------------------------------
def _r(v, nd=3):
    return round(float(v) + 0.0, nd)


def _pt(p):
    return [_r(p[0]), _r(p[1]), _r(p[2])]


def _lerp(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _seg(t, keys):
    """Piecewise smoothstep through keys [(t, (x, y, z)), ...] (held before / after)."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, p0), (t1, p1) in zip(keys, keys[1:]):
        if t <= t1:
            return _lerp(p0, p1, smooth((t - t0) / (t1 - t0)) if t1 > t0 else 1.0)
    return keys[-1][1]


def yaw_schedule(name, n):
    """Dense cumulative anchor-yaw delta per played tick (manifest.md 4.5), Minecraft units."""
    ev = dict(next(c for c in CLIP_TABLE if c[0] == name)[6])
    if name.startswith('turn'):
        tot = {'turn45_l': -45, 'turn45_r': 45, 'turn90_l': -90, 'turn90_r': 90, 'turn180': -180}[name]
        y0, y1 = ev['yaw0'], ev['yaw1']
        return [_r(tot * smooth((t - y0) / (y1 - y0)), 2) for t in range(n)]
    if name.startswith('tail_whip'):
        sgn = 1 if name.endswith('_l') else -1
        out = []
        for t in range(n):
            if t <= 20:
                v = 0.0
            elif t <= 31:
                v = 115 * smooth((t - 20) / 11)
            elif t <= 35:
                v = 115 + 7 * smooth((t - 31) / 4)
            elif t <= 42:
                v = 122 - 7 * smooth((t - 35) / 7)
            else:
                v = 115.0
            out.append(_r(sgn * v, 2))
        return out
    return None


def _tracks(name, n):
    if name.startswith('tail_whip'):
        return [list(_pt(TAIL_ROOT)) for _ in range(n)], [list(_pt(TAIL_TIP)) for _ in range(n)]
    if name == 'tail_slam':
        up = (0.0, TAIL_ROOT[1] + 10.0, TAIL_ROOT[2] - 2.0)
        down = (0.0, 0.0, TAIL_ROOT[2] - 13.0)
        tip = [_seg(t, [(0, TAIL_TIP), (9, up), (36, up), (39, down), (60, down), (69, TAIL_TIP)]) for t in range(n)]
        return [list(_pt(TAIL_ROOT)) for _ in range(n)], [list(_pt(p)) for p in tip]
    if name == 'tail_cast':
        up = (0.0, 9.0, -3.0)
        tip = [_seg(t, [(0, TAIL_TIP), (12, up), (26, up), (33, TAIL_TIP)]) for t in range(n)]
        return [list(_pt(TAIL_ROOT)) for _ in range(n)], [list(_pt(p)) for p in tip]
    if name == 'tail_pillar':
        return [list(_pt(PILLAR_ROOT)) for _ in range(n)], [list(_pt(PILLAR_TIP)) for _ in range(n)]
    if name == 'tail_pillar_strike':
        lean = (0.0, 8.5, 1.0)
        tip = [_seg(t, [(0, PILLAR_TIP), (10, lean), (23, PILLAR_TIP)]) for t in range(n)]
        return [list(_pt(PILLAR_ROOT)) for _ in range(n)], [list(_pt(p)) for p in tip]
    if name == 'tail_pillar_sink':
        tip = [_seg(t, [(0, PILLAR_TIP), (18, (0.0, 0.0, 0.0))]) for t in range(n)]
        return [list(_pt(PILLAR_ROOT)) for _ in range(n)], [list(_pt(p)) for p in tip]
    if name == 'p3_sink':
        sunk_root = (0.0, -1.0, TAIL_ROOT[2])
        root, tip = [], []
        for t in range(n):
            if t < 40:
                root.append(_seg(t, [(0, TAIL_ROOT), (40, sunk_root)]))
                tip.append(_seg(t, [(0, TAIL_TIP), (40, (0.0, 0.0, TAIL_TIP[2]))]))
            else:
                root.append(PILLAR_ROOT)
                tip.append(_seg(t, [(40, (0.0, 0.5, 0.0)), (58, PILLAR_TIP)]))
        return [list(_pt(p)) for p in root], [list(_pt(p)) for p in tip]
    raise KeyError(name)


def _paw_of(name):
    """The slamming paw of a stomp clip (rest-anchor name) and its proxy."""
    return {'stomp_fl': 'paw_fl', 'stomp_fr': 'paw_fr', 'stomp_hl': 'foot_hl', 'stomp_hr': 'foot_hr'}[name]


def _floor(p):
    return [_r(p[0]), 0.0, _r(p[2])]


def _anchors(name, ev, tracks):
    A = REST_ANCHORS
    nose = _pt(A['nose'])
    out = {}
    if name == 'chin_slam':
        out['impact'] = {'impact': [0.0, 0.0, _r(A['nose'][2] + 1.0)], 'nose': nose}
    elif name == 'jump_slam':
        out['land'] = {'nose': nose}
        out['wave2'] = {'nose': nose}
    elif name == 'spikes':
        b = A['back']
        pts = {f'launch_{k + 1}': _pt((b[0] + dx, b[1] + 0.4, b[2] + dz)) for k, (dx, dz) in
               enumerate(((0.9, 1.4), (-0.9, 0.5), (0.9, -0.5), (-0.9, -1.4)))}
        out['launch'] = pts
        out['launch_last'] = {'launch_4': pts['launch_4']}
    elif name.startswith('stomp_'):
        paw = _floor(A[_paw_of(name)])
        for e in ('slam', 'w1', 'w2', 'w3'):
            out[e] = {'paw': list(paw)}
    elif name.startswith('stomp3_'):
        a, b = ('paw_fl', 'paw_fr') if name.endswith('_fl') else ('paw_fr', 'paw_fl')
        out['s1'] = {'paw': _floor(A[a])}
        out['s2'] = {'paw': _floor(A[b])}
        out['s3'] = {'paw': _floor(A[a])}
    elif name == 'feint':
        out['burst'] = {'nose': nose, 'tail_root': _pt(A['tail_root'])}
    elif name in ('tail_whip_l', 'tail_whip_r', 'tail_slam', 'tail_cast', 'p3_sink', 'tail_pillar_strike'):
        evs = {'tail_whip_l': ('sweep', 'sweep_end', 'erupt'), 'tail_whip_r': ('sweep', 'sweep_end', 'erupt'),
               'tail_slam': ('slam', 'impact', 'spikes'), 'tail_cast': ('charge', 'fire'), 'p3_sink': ('pillar',),
               'tail_pillar_strike': ('strike',)}[name]
        root, tip = tracks
        for e in evs:
            t = min(ev[e], len(root) - 1)
            pts = {'tail_root': list(root[t]), 'tail_tip': list(tip[t])}
            if name in ('tail_cast', 'tail_pillar_strike'):
                pts = {'tail_tip': list(tip[t])}
            out[e] = pts
    elif name in ('roar_low', 'roar_rear'):
        out['roar'] = {'nose': nose}
    elif name in ('absorb', 'absorb_p3'):
        out['burst'] = {'back': _pt(A['back'])}
    elif name in ('walk', 'walk_stop') or name.startswith('turn'):
        cyc = ['paw_fl', 'paw_fr', 'foot_hl', 'foot_hr']
        walk = {'lh': 'foot_hl', 'lf': 'paw_fl', 'rh': 'foot_hr', 'rf': 'paw_fr', 'plant': 'paw_fl'}
        k = 0
        for e in sorted(ev, key=lambda x: (ev[x], x)):
            if e.startswith('yaw'):
                continue
            pa = walk.get(e) or cyc[k % 4]
            if name.endswith('_r'):
                pa = {'paw_fl': 'paw_fr', 'paw_fr': 'paw_fl', 'foot_hl': 'foot_hr', 'foot_hr': 'foot_hl'}[pa]
            out[e] = {'paw': _floor(A[pa])}
            k += 1
    return out


def _rest_key():
    return {p[0]: list(p[7]) for p in PROXY_LAYOUT}


def _key(kind):
    """A proxy key: 'rest', 'hidden' (all tops 0), 'tail_only' (body hidden, tail1-4 stacked at the anchor)."""
    k = _rest_key()
    if kind == 'hidden':
        return {n: [v[0], v[1], 0.0] for n, v in k.items()}
    if kind == 'tail_only':
        out = {n: [v[0], v[1], 0.0] for n, v in k.items() if n in BODY_PX}
        out.update({n: [0.0, 0.0, PILLAR_TOPS[n]] for n in TAIL_PX})
        return out
    return k


def _px(name, n, hidden, state):
    """Proxy keys: rest at 0 and n-1, the boundaries of hidden spans and of the tail-only states."""
    kinds = {}
    tail_only = any(s == 'tail_only' for _, s in state) or name.startswith('tail_pillar')

    def kind_at(t):
        if name.startswith('tail_pillar') or (name == 'p3_sink' and t >= 40):
            if name == 'tail_pillar_sink' and t >= 18:
                return 'hidden'
            return 'tail_only'
        for t0, t1, what in hidden:
            if t0 <= t <= t1:
                return 'hidden' if what in ('all', 'body') else 'rest'
        return 'rest'
    ts = {0, n - 1}
    for t0, t1, _ in hidden:
        ts |= {max(0, t0 - 1), min(n - 1, t0), min(n - 1, t1), min(n - 1, t1 + 1)}
    if tail_only and name == 'p3_sink':
        ts |= {39, 40}
    if name == 'tail_pillar_sink':
        ts |= {17, 18}
    for t in sorted(ts):
        if 0 <= t < n:
            kinds[str(t)] = _key(kind_at(t))
    return {'lerp': True, 'keys': kinds}


def _vis(name, n):
    """hidden spans, root_z spans, state switches: the binding table of manifest.md 4.6 (a state entry at t = len
    applies at the hand-over to next; burrowed <=> "all", tail_only <=> "body", normal <=> no span)."""
    hid, rz, st = [], [], []
    if name == 'burrow_dive':
        hid, st = [], [[n, 'burrowed']]
    elif name == 'burrow_travel':
        hid, st = [[0, n - 1, 'all']], []
    elif name == 'burrow_breach':
        hid, st = [[0, 7, 'all'], [30, n - 1, 'all']], [[8, 'normal'], [30, 'burrowed']]
    elif name == 'burrow_emerge':
        hid, st = [[0, 23, 'all']], [[24, 'normal']]
    elif name == 'p3_sink':
        hid, rz, st = [[40, n - 1, 'body']], [[40, n - 1, ROOT_Z_PILLAR]], [[40, 'tail_only']]
    elif name in ('tail_pillar', 'tail_pillar_strike'):
        hid, rz, st = [[0, n - 1, 'body']], [[0, n - 1, ROOT_Z_PILLAR]], []
    elif name == 'tail_pillar_sink':
        hid, rz, st = [[0, 17, 'body'], [18, n - 1, 'all']], [[0, n - 1, ROOT_Z_PILLAR]], [[18, 'burrowed']]
    return hid, rz, st


def _clip(idx, name, n, authored, loop, nxt, knots, events):
    tracks = _tracks(name, n) if name in TRACK_CLIPS else None
    hid, rz, st = _vis(name, n)
    c = {'id': STUB_ID0 + idx, 'name': name, 'len': n, 'authored': authored, 'loop': loop, 'next': nxt,
         'mirror_of': MIRRORS.get(name), 'retime': [list(k) for k in knots], 'events': dict(events),
         'anchors': _anchors(name, events, tracks),
         'tracks': {'tail_root': tracks[0], 'tail_tip': tracks[1]} if tracks else {},
         'px': _px(name, n, hid, st), 'yaw': yaw_schedule(name, n) if name in YAW_CLIPS else None,
         'hidden': hid, 'root_z': rz, 'state': st}
    return c


def _functions(ns):
    return {
        'init': ns + 'init', 'spawn': ns + 'spawn', 'tick': ns + 'tick', 'kill': ns + 'kill', 'uninstall': ns + 'uninstall',
        'look_apply': ns + 'look_apply',
        'play': {n: f'{ns}play/{n}' for n in CLIP_NAMES},
        'face': {'player': ns + 'face/player', 'track': ns + 'face/track', 'set': ns + 'face/set'},
        'state': {v: f'{ns}state/{v}' for v in VIS_STATES},
        'look_legs': {lk: f'{ns}look/legs/{lk}' for lk in LOOKS_LEGS},
        'look_tail': {lk: f'{ns}look/tail/{lk}' for lk in LOOKS_TAIL},
        'petrify': ns + 'look/petrify', 'glow_on': ns + 'glow/gold_on', 'glow_off': ns + 'glow/gold_off',
        'flash': {g: f'{ns}flash/{g}' for g in FLASH_GROUPS},
    }


def _globals(ns):
    layout = []
    for k, (name, part, point, w, mar, fl, to, rest) in enumerate(PROXY_LAYOUT):
        idx = PX_BASE + k
        layout.append({'name': name, 'part': part, 'point': list(point), 'w': w, 'top_margin': mar, 'tail_only': to,
                       'idx': idx, 'uuid': f'{UUID_BLOCK}{idx:02x}', 'flash': fl})
    parts = [{'name': n, 'region': r, 'idx': i + 1, 'uuid': f'{UUID_BLOCK}{i + 1:02x}', 'tag': f'rlk_mb_az_{n}'}
             for i, (n, r) in enumerate(PART_TABLE)]
    return {
        'schema': SCHEMA, 'boss': BOSS,
        'runtime': dict(RUNTIME, ns=ns),
        'functions': _functions(ns),
        'parts': parts,
        'uuids': {'block': UUID_BLOCK, 'ints': list(UUID_INTS), 'parts': {p['name']: p['idx'] for p in parts}, 'shadow': 64,
                  'proxies': {p['name']: p['idx'] for p in layout}, 'props': {'seal_prism': 128, 'crater': 129}},
        'skeleton': copy.deepcopy(SKELETON),
        'rest_anchors': {k: _pt(v) for k, v in REST_ANCHORS.items()},
        'torso_hw': TORSO_HW,
        'proxies': {'layout': layout, 'rest': _rest_key(), 'rest_pose': copy.deepcopy(REST_POSE)},
        'states': copy.deepcopy(STATES),
        'capsules': copy.deepcopy(CAPSULES),
        'flash_groups': copy.deepcopy(FLASH_GROUPS),
        'looks': {'legs': {'objective': 'azRigLegs', 'ids': {lk: i for i, lk in enumerate(LOOKS_LEGS)}},
                  'tail': {'objective': 'azRigTail', 'ids': {lk: i for i, lk in enumerate(LOOKS_TAIL)}},
                  'functions': {'legs': {lk: f'{ns}look/legs/{lk}' for lk in LOOKS_LEGS},
                                'tail': {lk: f'{ns}look/tail/{lk}' for lk in LOOKS_TAIL},
                                'petrify': ns + 'look/petrify', 'glow_on': ns + 'glow/gold_on', 'glow_off': ns + 'glow/gold_off'}},
        'culling': dict(CULLING),
        'rest_extents': copy.deepcopy(REST_EXTENTS),
        'budgets': copy.deepcopy(BUDGETS),
        'objectives': dict(OBJECTIVES),
    }


def stub_manifest():
    """The full v1 stub manifest (manifest.md section 8): every clip of section 5, the R1 globals."""
    m = _globals(NS_STUB)
    m['source'] = 'stub'
    m['clips'] = [_clip(i, *c) for i, c in enumerate(CLIP_TABLE)]
    m['fallbacks'] = list(CLIP_NAMES)
    return m


# ---------------------------------------------------------------------------------------------
def is_v1_rig(m):
    return isinstance(m, dict) and m.get('schema') == SCHEMA and m.get('source') == 'rig'


def migrate_r1(r1):
    """manifest.md section 10: the R1 rig manifest (no "schema") -> a v1 manifest ("source": "rig", clips = the R1
    debug poses renamed dbg_<name>, never §5 clips). The proxy columns go from the rig frame (+z back) to the local
    frame (z forward): [x, -z, top], hidden -> top 0, base dropped."""
    assert 'schema' not in r1, 'not an R1 manifest'
    m = _globals(NS_RIG)
    m['source'] = 'rig'
    m['migrated_from'] = 'R1'
    order = {name: i for i, name in enumerate(PROXIES)}
    lay = r1.get('proxies', {}).get('layout', [])
    if lay:
        assert [p['name'] for p in lay] == PROXIES, [p['name'] for p in lay]
        for k, (dst, src) in enumerate(zip(m['proxies']['layout'], lay)):
            dst.update({'part': src['part'], 'point': list(src['point']), 'w': src['w'], 'top_margin': src['top_margin'],
                        'tail_only': bool(src.get('tail_only'))})
    rest = r1.get('proxies', {}).get('rest', {})
    if rest:
        m['proxies']['rest'] = {n: [_r(v['x']), _r(-v['z']), 0.0 if v.get('hidden') else _r(v['top'])]
                                for n, v in sorted(rest.items(), key=lambda kv: order.get(kv[0], 99))}
    if r1.get('parts'):
        m['parts'] = [{'name': p['name'], 'region': p.get('region'), 'idx': int(p['uuid'][-2:], 16), 'uuid': p['uuid'],
                       'tag': p.get('tag'), 'model': p.get('model'), 'brightness': p.get('brightness'),
                       'scale': p.get('scale'), 'elements': p.get('elements')} for p in r1['parts']]
        m['uuids']['parts'] = {p['name']: p['idx'] for p in m['parts']}
    for k in ('flash_groups', 'culling', 'rest_extents', 'budgets', 'objectives'):
        if k in r1:
            m[k] = copy.deepcopy(r1[k])
    if 'skeleton' in r1:
        m['skeleton'] = dict(copy.deepcopy(r1['skeleton']), frame='rig (+x left, +y up, +z back)')
    if 'looks' in r1:
        lk = copy.deepcopy(r1['looks'])
        lk['functions'] = {'legs': lk.get('legs', {}).get('functions', {}), 'tail': lk.get('tail', {}).get('functions', {}),
                           'petrify': NS_RIG + 'look/petrify', 'glow_on': NS_RIG + 'glow/gold_on',
                           'glow_off': NS_RIG + 'glow/gold_off'}
        m['looks'] = lk
    if 'states' in r1 and isinstance(r1['states'].get('functions'), dict):
        m['functions']['state'] = dict(r1['states']['functions'])
    clips = []
    for c in r1.get('clips', []):
        px = {}
        for t, cols in (c.get('px') or {}).items():
            px[str(t)] = {n: [_r(v['x']), _r(-v['z']), 0.0 if v.get('hidden') else _r(v['top'])] for n, v in cols.items()}
        clips.append({'id': c['id'], 'name': 'dbg_' + c['name'], 'len': c['len'], 'authored': c['len'], 'loop': bool(c.get('loop')),
                      'next': None, 'mirror_of': None, 'retime': [], 'events': dict(c.get('events', {})), 'anchors': {},
                      'tracks': {}, 'px': {'lerp': True, 'keys': px}, 'yaw': None, 'hidden': [], 'root_z': [],
                      'state': [[0, c['state']]] if c.get('state') else [], 'extents': c.get('extents')})
    m['clips'] = clips
    return m


def merge(real, stub):
    """manifest.md section 1 / cm.md 9.2: every clip of the real v1 rig manifest, stub clips only for names it lacks
    (ids >= 1000); globals from the real file when it is v1 from the rig, else the stub's. Returns (merged, fallbacks)."""
    if not is_v1_rig(real):
        m = copy.deepcopy(stub)
        return m, [c['name'] for c in stub['clips']]
    m = copy.deepcopy(real)
    have = {c['name'] for c in real.get('clips', [])}
    fb = [c for c in stub['clips'] if c['name'] not in have]
    m['clips'] = list(m.get('clips', [])) + copy.deepcopy(fb)
    m['fallbacks'] = [c['name'] for c in fb]
    return m, [c['name'] for c in fb]


def dumps(m):
    """Deterministic JSON (stable bytes for the committed stub manifest)."""
    return json.dumps(m, ensure_ascii=False, indent=1, sort_keys=False) + '\n'


# =============================================================================================
# The stand-in runtime F:mboss/azhdaha/rig_stub/**
TAG = 'rlk_mb_azs'
FIG = {   # stand-in part -> (item, scale (x, y, z), local offset (s, y, f) from the anchor, flash group)
    'sbody': ('minecraft:tuff', (5.4, 3.2, 8.6), (0.0, 2.9, -0.3), 'front'),
    'shead': ('minecraft:polished_blackstone', (2.2, 2.0, 2.6), (0.0, 1.6, 4.6), 'head'),
    'stail': ('minecraft:stripped_jungle_log', (1.5, 1.5, 11.0), (0.0, 1.6, -10.3), 'tail'),
    'seyes': ('minecraft:redstone_block', (1.4, 0.25, 0.3), (0.0, 2.15, 5.95), 'head'),
}
LEG_ITEM = {'geo': 'minecraft:tuff', 'hydro': 'minecraft:dark_prismarine', 'pyro': 'minecraft:magma_block'}
TAIL_ITEM = {'geo': 'minecraft:stripped_jungle_log', 'cryo': 'minecraft:packed_ice', 'electro': 'minecraft:purpur_pillar'}
PILLAR_ROT = '[-0.7071f,0f,0f,0.7071f]'         # the log stood up (90 degrees about x)
ID_ROT = '[0f,0f,0f,1f]'


def _tf(scale, rot=ID_ROT):
    sx, sy, sz = scale
    return (f'{{translation:[0f,0f,0f],left_rotation:{rot},right_rotation:[0f,0f,0f,1f],'
            f'scale:[{_n(sx)}f,{_n(sy)}f,{_n(sz)}f]}}')


def _n(v):
    s = f'{float(v):.4f}'.rstrip('0').rstrip('.')
    return s if s not in ('-0', '') else '0'


def _sel(name):
    return f'@e[type=minecraft:item_display,tag=rlk_mb_az_{name},tag={TAG},limit=1]'


def emit(g, merged=None, functions=True):
    """Write the stub manifest JSON and F:mboss/azhdaha/rig_stub/**. g = api.Gen; merged = api.MAN (for the clip ids
    of the stub clips the module uses: their ids are the merged table's). functions=False (I1-WIRE: the real rig serves
    every clip and function, api.stub_rig_needed()): only the JSON, no rig_stub/** (the module's clean removes it)."""
    from . import api as A
    sm = stub_manifest()
    A.STUB_MANIFEST.write_text(dumps(sm), encoding='utf-8')
    if not functions:
        return
    man = merged or A.MAN
    ids = {c['name']: c['id'] for c in man['clips']}
    stub_clips = [c for c in man['clips'] if c['id'] >= STUB_ID0]
    w = lambda rel, lines: g.w(f'rig_stub/{rel}', lines)       # noqa: E731
    head = '# STUB rig (tools/mboss_azhdaha/stub_rig.py, manifest.md 8): the real rig (wip/az-rig) replaces it per function.'
    NSR = NS_STUB
    w('init', [head, '# Rig objectives (the R1 names; shared with the real rig); safe on every load.']
      + [f'scoreboard objectives add {o} dummy' for o in OBJECTIVES])
    spawn = [head, '# @s = anchor (the body husk on the floor), at it, rotated as it: kills old parts, summons the stand-in,',
             '# queues idle, re-applies the stored looks and the visibility state.',
             f'function {NSR}init', f'function {NSR}kill']
    for name, (item, sc, (x, y, z), _) in FIG.items():
        tags = f'["rlk_room","rlk_mb_aux","rlk_mb_azhdaha_part","{TAG}","rlk_mb_az_{name}"]'
        spawn.append(f'summon minecraft:item_display ^{_n(x)} ^{_n(y)} ^{_n(z)} {{Tags:{tags},billboard:"fixed",'
                     f'item_display:"none",teleport_duration:1,interpolation_duration:2,brightness:{{block:13,sky:15}},'
                     f'view_range:3f,width:30f,height:12f,transformation:{_tf(sc)},item:{{id:"{item}",count:1}}}}')
    spawn += ['execute unless score @s azRigLegs matches 0..2 run scoreboard players set @s azRigLegs 0',
              'execute unless score @s azRigTail matches 0..2 run scoreboard players set @s azRigTail 0',
              'execute unless score @s azRigState matches 0..2 run scoreboard players set @s azRigState 0',
              f'scoreboard players set @s azRigC {ids["idle"]}', 'scoreboard players set @s azRigT -1',
              'scoreboard players set @s azRigF 0', f'function {NSR}look_apply']
    w('spawn', spawn)
    follow = [head, '# @s = anchor, at it, rotated ~ 0 as it: the parts to their offsets (tail-only: the tail stands on the anchor).']
    for name, (_, _, (x, y, z), _) in FIG.items():
        if name == 'stail':
            follow.append(f'execute if score @s azRigState matches 2 run tp {_sel(name)} ~ ~4.4 ~ ~ 0')
            follow.append(f'execute unless score @s azRigState matches 2 positioned ^{_n(x)} ^{_n(y)} ^{_n(z)} run tp {_sel(name)} ~ ~ ~ ~ 0')
        else:
            follow.append(f'execute positioned ^{_n(x)} ^{_n(y)} ^{_n(z)} run tp {_sel(name)} ~ ~ ~ ~ 0')
    w('follow', follow)
    w('tick', [head, '# @s = anchor, at it; once per game tick after the module (the pose of this tick). Missing parts respawn.',
               f'execute unless entity {_sel("sbody")} run function {NSR}spawn',
               f'execute rotated as @s rotated ~ 0 run function {NSR}follow',
               'scoreboard players add @s azRigT 1',
               f'function {NSR}chain',
               f'execute if score @s azRigF matches 1.. run function {NSR}flash_tick'])
    chain = [head, '# Loop / next / hold of the stub clips (ids >= 1000); also called after a real rig tick (api.rig_tick).',
             f'execute unless score @s azRigC matches {STUB_ID0}.. run return 0']
    for c in stub_clips:
        for t, st in c.get('state') or []:          # the recorded visibility state switches (t = len: at the hand-over)
            chain.append(f'execute if score @s azRigC matches {c["id"]} if score @s azRigT matches {t} run function {NSR}state/{st}')
    for c in stub_clips:
        if c['loop']:
            chain.append(f'execute if score @s azRigC matches {c["id"]} if score @s azRigT matches {c["len"]}.. run scoreboard players set @s azRigT 0')
        elif c['next']:
            nid = ids[c['next']]
            chain.append(f'execute if score @s azRigC matches {c["id"]} if score @s azRigT matches {c["len"]}.. run return run '
                         f'function {NSR}chain_to {{c:{nid}}}')
        else:
            chain.append(f'execute if score @s azRigC matches {c["id"]} if score @s azRigT matches {c["len"]}.. run scoreboard players '
                         f'set @s azRigT {c["len"] - 1}')
    w('chain', chain)
    w('chain_to', ['# The next clip starts at its tick 0 this same tick (R1 start/<clip> semantics).',
                   '$scoreboard players set @s azRigC $(c)', 'scoreboard players set @s azRigT 0'])
    for c in stub_clips:
        w(f'play/{c["name"]}', [head, f'# Play {c["name"]} ({c["len"]} t, stub id {c["id"]}) from its tick 0 at the next rig tick.',
                                f'scoreboard players set @s azRigC {c["id"]}', 'scoreboard players set @s azRigT -1'])
    # visibility states
    vis = {'normal': {'sbody', 'shead', 'stail', 'seyes'}, 'burrowed': set(), 'tail_only': {'stail'}}
    for i, st in enumerate(VIS_STATES):
        lines = [head, f'# Visibility state {st} (azRigState {i}).', f'scoreboard players set @s azRigState {i}']
        for name, (_, sc, _, _) in FIG.items():
            shown = name in vis[st]
            rot = PILLAR_ROT if (st == 'tail_only' and name == 'stail') else ID_ROT
            s2 = (sc[0], sc[1], 9.0) if (st == 'tail_only' and name == 'stail') else sc
            lines.append(f'data merge entity {_sel(name)} {{start_interpolation:0,interpolation_duration:3,'
                         f'transformation:{_tf(s2 if shown else (0, 0, 0), rot)}}}')
        w(f'state/{st}', lines)
    for i, lk in enumerate(LOOKS_LEGS):
        w(f'look/legs/{lk}', [head, f'# Legs channel {lk} (azRigLegs {i}).', f'scoreboard players set @s azRigLegs {i}',
                              f'data modify entity {_sel("sbody")} item set value {{id:"{LEG_ITEM[lk]}",count:1}}'])
    for i, lk in enumerate(LOOKS_TAIL):
        w(f'look/tail/{lk}', [head, f'# Tail channel {lk} (azRigTail {i}).', f'scoreboard players set @s azRigTail {i}',
                              f'data modify entity {_sel("stail")} item set value {{id:"{TAIL_ITEM[lk]}",count:1}}',
                              f'data merge entity {_sel("stail")} {{brightness:{{block:{15 if lk != "geo" else 13},sky:15}}}}'])
    w('look/petrify', [head, '# Death seal: every part turns to stone, darker (base looks at brightness -3).']
      + [f'data modify entity {_sel(n)} item set value {{id:"minecraft:stone",count:1}}' for n in FIG]
      + [f'data merge entity {_sel(n)} {{brightness:{{block:10,sky:12}}}}' for n in FIG])
    w('look_apply', [head, '# The stored looks and state again (spawn, reload).']
      + [f'execute if score @s azRigLegs matches {i} run function {NSR}look/legs/{lk}' for i, lk in enumerate(LOOKS_LEGS)]
      + [f'execute if score @s azRigTail matches {i} run function {NSR}look/tail/{lk}' for i, lk in enumerate(LOOKS_TAIL)]
      + [f'execute if score @s azRigState matches {i} run function {NSR}state/{st}' for i, st in enumerate(VIS_STATES)])
    w('glow/gold_on', [head, '# Gold parts 13 -> 15 (the 천동만상 tell, the absorbs): a gold outline on the stand-in.',
                       f'data merge entity {_sel("sbody")} {{Glowing:1b,glow_color_override:15905594}}'])
    w('glow/gold_off', [head, '# Gold back to matte 13.', f'data merge entity {_sel("sbody")} {{Glowing:0b}}'])
    for grp in FLASH_GROUPS:
        parts = [n for n, v in FIG.items() if v[3] == grp] or ['sbody']
        w(f'flash/{grp}', [head, f'# Hit flash of the {grp} group: a white outline for 3 t.', 'scoreboard players set @s azRigF 3']
          + [f'data merge entity {_sel(n)} {{Glowing:1b,glow_color_override:16777215}}' for n in parts])
    w('flash_tick', ['scoreboard players remove @s azRigF 1',
                     f'execute if score @s azRigF matches ..0 as @e[type=minecraft:item_display,tag={TAG}] run data merge entity @s {{Glowing:0b}}'])
    w('face/player', [head, '# Instant yaw toward the player\'s body.',
                      'execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0'])
    w('face/track', [head, '# At most 2 degrees per call toward the player\'s body.', 'function rlk:mboss/mv/turn {max:2}'])
    w('face/set', [head, '# Macro {yaw}: absolute yaw.', '$tp @s ~ ~ ~ $(yaw) 0'])
    w('kill', [head, f'kill @e[type=minecraft:item_display,tag={TAG}]'])
    w('uninstall', [head, f'function {NSR}kill'] + [f'scoreboard objectives remove {o}' for o in OBJECTIVES])

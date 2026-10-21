"""아펩의 오아시스 파수꾼 (Apep) stub rig: the day-0 stub rig manifest and the stand-in rig runtime (AP-CORE).

Contract: scratchpad ap/ap_contract.md 0.4 (the rig manifest schema = Azhdaha manifest v1 + the Apep extras) and 0.9.
Two jobs:

1. DATA (pure, importable without side effects; api.py imports it): `build_rig()` returns the full stub manifest
   ("source": "stub") of S:ap/spec/make_stubs.py (AP-SPEC, D0), carried over verbatim (clip table, parts, proxies,
   states, capsules, stances, hands, looks, park, sprite ledger) with ONE change: the clip ids are 1000 + k (cm.md change
   note 22.6: a stub clip that falls back beside a real rig manifest must never reuse a rig id; the framework's px
   dispatch is keyed by clip id). Names, lengths, authored lengths, loop / next, events, hidden spans, yaw knots and
   anchors stay the frozen D0 values (validate.py --against S:ap/spec/stub_rig_manifest.json passes; it does not
   compare ids). `merge(real, stub)` is the per-clip merge of ap_contract 0.4.1 / cm.md 9.2.

2. RUNTIME (emit(g), called by core.build): writes T:mboss_apep/stub_rig_manifest.json (the framework compiles the hit
   proxies, the px state sets and the capsules from it while no real rig manifest exists, cm.md 9.2) and the stand-in
   rig F:boss/apep/rig_stub/** with the rig API of ap_contract 0.4.9 (init spawn tick kill uninstall look_apply,
   play/<clip>, face/{player,track,set}, state/{normal,burrowed}, flash/<group>, park / unpark, stance/{crouch,upright},
   hands/<set>, look/<channel>/<look>, bright/{13,15}). Clips keep time exactly as a real rig (apRigC / apRigT; loop,
   next, hold) and apply their stance / look / hand events and visibility switches as scores, so the framework's
   px/tick and the core read the same state the real rig will write. The figure is a crude vanilla stand-in (a moss
   torso, a dark hood, a log tail) that follows the anchor, hides while burrowed / parked and stands taller upright.

The real rig (wip/ap-rig, merged at AP-I1) replaces every function it provides (api.rig_fn); play/<clip> goes to the
real rig for the clips its manifest has (api.play_fn). AP-I2 asserts that no clip falls back (api.FALLBACKS empty).
"""
import json
from pathlib import Path
import mboss_lib as L

HERE = Path(__file__).resolve().parent
STUB_ID0 = 1000          # stub clip ids (never a rig id: cm.md 9.2 / change note 22.6)

# ------------------------------------------------------------------------------------------------ rig
BLOCK = '524c4b4d-4150-4400-8000-0000000000'
RIG_INTS = [1380731725, 1095779328, -2147483648]
NS = f'rlk:{L.fn_root_of("apep")}/rig/'           # the module root from the registry (boss/apep)

# (name, region, parent, scale, brightness p1, brightness p3); order = the append-only idx table (0x00 ..), plan R4.
PARTS = [
    ('abdomen', 'body', 'pelvis', 1.6, 13, 13), ('hem_a', 'body', 'abdomen', 1.4, 13, 13),
    ('hem_b', 'body', 'hem_a', 1.1, 13, 13), ('chest', 'body', 'pelvis', 1.5, 13, 13),
    ('shoulders', 'body', 'chest', 2.0, 13, 13), ('core', 'body', 'chest', 0.9, 15, 15),
    ('crys_low', 'body', 'chest', 1.1, 14, 15), ('crys_back', 'body', 'shoulders', 1.5, 14, 15),
    ('neck', 'head', 'shoulders', 0.8, 13, 13), ('head', 'head', 'neck', 1.1, 13, 13),
    ('face', 'head', 'head', 1.5, 15, 15), ('hood', 'head', 'hood_hinge', 2.1, 13, 13),
    ('crown', 'head', 'hood', 1.3, 15, 15),
    ('hair_l_1', 'head', 'head', 1.2, 13, 13), ('hair_r_1', 'head', 'head', 1.2, 13, 13),
    ('hair_l_2', 'head', 'hair_l_1', 1.2, 13, 13), ('hair_r_2', 'head', 'hair_r_1', 1.2, 13, 13),
    ('mantle_l_a', 'body', 'shoulders', 1.7, 13, 13), ('mantle_r_a', 'body', 'shoulders', 1.7, 13, 13),
    ('mantle_l_b', 'body', 'mantle_l_a', 1.5, 13, 13), ('mantle_r_b', 'body', 'mantle_r_a', 1.5, 13, 13),
    ('a_up_l', 'limbs', 'clav_a_l', 2.0, 13, 13), ('a_up_r', 'limbs', 'clav_a_r', 2.0, 13, 13),
    ('a_lo_l', 'limbs', 'a_up_l', 2.1, 13, 13), ('a_lo_r', 'limbs', 'a_up_r', 2.1, 13, 13),
    ('a_hand_l', 'hands', 'a_lo_l', 1.0, 13, 13), ('a_hand_r', 'hands', 'a_lo_r', 1.0, 13, 13),
    ('b_up_l', 'limbs', 'shoulders', 1.5, 13, 13), ('b_up_r', 'limbs', 'shoulders', 1.5, 13, 13),
    ('b_lo_l', 'limbs', 'b_up_l', 1.5, 13, 13), ('b_lo_r', 'limbs', 'b_up_r', 1.5, 13, 13),
    ('b_hand_l', 'hands', 'b_lo_l', 1.8, 13, 13), ('b_hand_r', 'hands', 'b_lo_r', 1.8, 13, 13),
    ('c_up_l', 'limbs', 'pelvis', 1.4, 13, 13), ('c_up_r', 'limbs', 'pelvis', 1.4, 13, 13),
    ('c_lo_l', 'limbs', 'c_up_l', 1.6, 13, 13), ('c_lo_r', 'limbs', 'c_up_r', 1.6, 13, 13),
    ('c_hand_l', 'hands', 'c_lo_l', 1.2, 13, 13), ('c_hand_r', 'hands', 'c_lo_r', 1.2, 13, 13),
] + [(f'tail_{k}', 'tail', 'pelvis' if k == 1 else f'tail_{k - 1}', 1.1, 13, 13) for k in range(1, 8)] + [
    ('tail_tip', 'tail', 'tail_7', 1.0, 13, 13),
    ('beads_l', 'limbs', 'b_up_l', 1.6, 14, 14), ('beads_r', 'limbs', 'b_up_r', 1.6, 14, 14),
]
POSE_ONLY = {'root': None, 'pelvis': 'root', 'clav_a_l': 'shoulders', 'clav_a_r': 'shoulders', 'hood_hinge': 'head'}
HAND_PARTS = ['a_hand_l', 'a_hand_r', 'b_hand_l', 'b_hand_r', 'c_hand_l', 'c_hand_r']
OWN_CHANNEL = {'face', 'core'}
HAND_VARIANTS = {'a': ['p1_planted', 'p1_raised', 'p3_fork'],
                 'b': ['p1_open', 'p1_curl', 'p3_curl', 'p3_open'],
                 'c': ['p1_open', 'p1_curl', 'p3_curl']}
HAND_SETS = {'p1_rest': {'a': 'p1_planted', 'b': 'p1_open', 'c': 'p1_open'},
             'p1_lift': {'a': 'p1_raised', 'b': 'p1_curl', 'c': 'p1_curl'},
             'p3_open': {'a': 'p3_fork', 'b': 'p3_open', 'c': 'p3_curl'},
             'p3_curl': {'a': 'p3_fork', 'b': 'p3_curl', 'c': 'p3_curl'}}
FLASH_GROUPS = {
    'head': ['neck', 'head', 'face', 'hood', 'crown', 'hair_l_1', 'hair_r_1', 'hair_l_2', 'hair_r_2'],
    'body': ['chest', 'shoulders', 'core', 'crys_low', 'crys_back', 'mantle_l_a', 'mantle_r_a', 'mantle_l_b',
             'mantle_r_b'],
    'front': ['b_up_l', 'b_up_r', 'b_lo_l', 'b_lo_r', 'b_hand_l', 'b_hand_r'],
    'rear': ['abdomen', 'hem_a', 'hem_b', 'c_up_l', 'c_up_r', 'c_lo_l', 'c_lo_r', 'c_hand_l', 'c_hand_r'],
    'tail': [f'tail_{k}' for k in range(1, 8)] + ['tail_tip'],
    'arms': ['a_up_l', 'a_up_r', 'a_lo_l', 'a_lo_r', 'a_hand_l', 'a_hand_r', 'beads_l', 'beads_r'],
}
# proxies (plan R7; names without the plan's px_ prefix, as Azhdaha's). Plan values are rig frame (x left, z back):
# name, part (bone it rides), flash group, CROUCH (x, z, w, h), UPRIGHT (x, z, w, h).
PROXIES = [
    ('head', 'head', 'head', (0, -3.4, 2.4, 4.5), (0, -0.7, 2.8, 8.5)),
    ('chest', 'chest', 'body', (0, 0.0, 3.0, 5.0), (0, 0.5, 2.6, 6.5)),
    ('abd', 'abdomen', 'rear', (0, 2.0, 2.6, 4.0), (0, 1.3, 2.0, 2.5)),
    ('tail_a', 'tail_3', 'tail', (0.2, 6.0, 1.8, 2.0), (1.6, 4.1, 1.8, 1.5)),
    ('tail_b', 'tail_6', 'tail', (1.3, 9.3, 1.8, 2.0), (3.8, 2.4, 1.8, 1.5)),
    ('a_l', 'a_hand_l', 'arms', (5.3, -2.6, 1.8, 2.5), (2.8, -0.9, 1.6, 6.0)),
    ('a_r', 'a_hand_r', 'arms', (-5.3, -2.6, 1.8, 2.5), (-2.8, -0.9, 1.6, 6.0)),
    ('b_l', 'b_hand_l', 'front', (2.5, -3.6, 1.8, 3.0), (4.6, -1.0, 2.2, 6.8)),
    ('b_r', 'b_hand_r', 'front', (-2.5, -3.6, 1.8, 3.0), (-4.6, -1.0, 2.2, 6.8)),
    ('c_l', 'c_hand_l', 'rear', (3.0, 3.0, 1.6, 3.0), (3.7, -0.8, 1.8, 2.5)),
    ('c_r', 'c_hand_r', 'rear', (-3.0, 3.0, 1.6, 3.0), (-3.7, -0.8, 1.8, 2.5)),
]
ALL_PX = [p[0] for p in PROXIES]


def loc(p):
    """rig frame (+z back) -> local frame (z = f forward)."""
    return [p[0], p[1], round(-p[2], 3) + 0.0]


def _mirror(d):
    out = {}
    for k, v in d.items():
        out[k] = v
        if k.endswith('_l'):
            out[k[:-2] + '_r'] = [-v[0], v[1], v[2]]
    return out


RIG_ANCHORS = {   # rig frame, model_p3 §6.2
    'CROUCH': _mirror({
        'pelvis': [0, 2.8, 1.0], 'thorax': [0, 3.1, 0.0], 'shoulder': [0, 3.4, -1.2], 'head': [0, 3.4, -1.9],
        'hood_front': [0, 3.0, -4.0], 'hood_top': [0, 4.4, -2.7], 'crown': [0, 5.0, -2.7], 'face': [0, 2.9, -3.3],
        'core': [0, 1.7, -1.0], 'tail_root': [0, 2.4, 2.9], 'tail_tip': [1.6, 0.2, 10.9],
        'hand_a_l': [5.3, 0.15, -2.6], 'hand_b_l': [2.5, 0.15, -3.6], 'hand_c_l': [3.0, 0.15, 3.0]}),
    'UPRIGHT': _mirror({
        'pelvis': [0, 3.1, 0.2], 'thorax': [0, 4.2, 0.0], 'shoulder': [0, 5.3, -0.1], 'head': [0, 6.0, -0.3],
        'hood_front': [0, 7.7, -0.9], 'hood_top': [0, 8.5, -0.1], 'crown': [0, 7.9, -0.4], 'face': [0, 6.9, -0.9],
        'core': [0, 4.4, -0.7], 'tail_root': [0, 1.2, 0.5], 'tail_tip': [3.9, 0.2, 1.4],
        'hand_a_l': [3.8, 10.4, -0.2], 'hand_b_l': [5.2, 6.2, -1.0], 'hand_c_l': [3.9, 0.15, -0.8]}),
}
ANCHORS = {s: {k: loc(v) for k, v in d.items()} for s, d in RIG_ANCHORS.items()}   # local frame
JOINTS = {   # rig frame (AZ manifest: skeleton stays in the rig frame)
    'CROUCH': {'root': [0, 0, 0], 'pelvis': [0, 2.8, 1.0], 'chest': [0, 3.1, 0.0], 'shoulders': [0, 3.4, -1.2],
               'neck': [0, 3.4, -1.6], 'head': [0, 3.4, -1.9], 'hood_hinge': [0, 3.7, -2.1],
               'clav_a_l': [0.9, 3.6, -1.0], 'clav_a_r': [-0.9, 3.6, -1.0], 'tail_1': [0, 2.4, 2.9]},
    'UPRIGHT': {'root': [0, 0, 0], 'pelvis': [0, 3.1, 0.2], 'chest': [0, 4.2, 0.0], 'shoulders': [0, 5.3, -0.1],
                'neck': [0, 5.6, -0.2], 'head': [0, 6.0, -0.3], 'hood_hinge': [0, 6.6, 0.1],
                'clav_a_l': [0.8, 5.5, 0.1], 'clav_a_r': [-0.8, 5.5, 0.1], 'tail_1': [0, 1.2, 0.5]},
}
# Push capsules in the Azhdaha box form (manifest.md §6.3: f0 <= f <= f1, |s| < hw, local frame, blocks). Plan R11's
# vertical columns (centre f, radius r) become f0 = f - r, f1 = f + r, hw = r; `col` keeps the plan's numbers.
CAPSULES = {'sac': {'f0': 0.0, 'f1': 2.0, 'hw': 1.0, 'col': {'f': 1.0, 'r': 1.0}},
            'hips': {'f0': -2.2, 'f1': 0.2, 'hw': 1.2, 'col': {'f': -1.0, 'r': 1.2}},
            'stem': {'f0': -1.4, 'f1': 1.4, 'hw': 1.4, 'col': {'f': 0.0, 'r': 1.4}}}
STANCE_CAPSULES = {'CROUCH': ['sac', 'hips'], 'UPRIGHT': ['stem']}
SETS = ['p1', 'p3u', 'p3c', 'burrowed', 'aloft', 'inv', 'parked', 'dead']
SET_STANCE = {'p1': 'CROUCH', 'p3u': 'UPRIGHT', 'p3c': 'CROUCH', 'aloft': 'UPRIGHT'}


def px_table(stance, hidden=False, tops=None):
    i = 3 if stance == 'CROUCH' else 4
    out = {}
    for p in PROXIES:
        x, z, _w, h = p[i]
        top = 0 if hidden else (tops or {}).get(p[0], h)
        out[p[0]] = [x, round(-z, 3) + 0.0, top]
    return out


# §6.3 clip table in the plan's terms. Keys: name, form, played len, events (lists = repeated names), next, loop,
# authored, retime, hidden (half-open plan spans), stance (start, end), moves (t0, t1, stance: the stance change slides
# the proxy columns from t0 to t1), looks, hands, yaw (knots, ease),
# pxs (proxy set at t0), pxs_changes, anchors (rig frame), tail (track stances), aloft (px tops), extra keys.
C = []


def clip(name, form, played, events, **kw):
    C.append(dict(name=name, form=form, played=played, events=events, **kw))


clip('entrance_p1', 'p1', 110, dict(pool=0, hood=16, reach=31, touch=47, flash=60, embers=63, heart_up=70,
                                    crouch=91, roar=100, end=110),
     next='idle_p1', hidden=[[0, 4]], looks=[[0, 'tint', 'p1_dark'], [30, 'tint', 'none']],
     hands=[[31, 'a_hand_r', 'p1_raised'], [91, 'a_hand_r', 'p1_planted']],
     pxs='inv', pxs_changes=[[110, 'p1']], anchors={'touch': {'hand_a_r': [-1.4, 8.6, -1.2]}})
clip('idle_p1', 'p1', 60, {}, loop=True)
clip('turn_p1', 'p1', 20, dict(step=[0, 5, 10, 15]), loop=True)
clip('turn_p1_step', 'p1', 10, dict(step=[0, 5]), next='idle_p1', yaw=([[0, 0], [9, -90]], 'smooth'))
clip('crawl_p1', 'p1', 16, dict(stepA=0, stepB=8), loop=True,
     hands=[[0, 'b_hand_l', 'p1_curl'], [0, 'c_hand_r', 'p1_curl'], [0, 'b_hand_r', 'p1_open'],
            [0, 'c_hand_l', 'p1_open'], [8, 'b_hand_l', 'p1_open'], [8, 'c_hand_r', 'p1_open'],
            [8, 'b_hand_r', 'p1_curl'], [8, 'c_hand_l', 'p1_curl']])
clip('crawl_stop_p1', 'p1', 32, dict(plant=8, open=16, end=32), next='idle_p1', hands=[[8, 'p1_rest']])
clip('walk_p1', 'p1', 36, dict(step=[0, 9, 18, 27]), loop=True)
clip('burrow_strike', 'p1', 82, dict(tell=0, dive=4, inv=6, sink=8, hide=22, travel=23, lock=32, burst=44, rise=49,
                                     loom=52, yawlock=52, sweep=64, sweep_end=71, land=77, end=82),
     authored=94, retime=[[0, 0], [28, 22], [50, 44], [76, 64], [94, 82]], next='idle_p1', hidden=[[22, 44]],
     looks=[[6, 'tint', 'p1_dark'], [44, 'tint', 'none']], pxs_changes=[[6, 'burrowed'], [44, 'p1']],
     anchors={'burst': {'impact': [0, 0, 0]}})
clip('sink_p1', 'p1', 17, dict(tell=0, sink=4, chunks=8, hide=14), authored=18, retime=[[0, 0], [5, 4], [18, 17]],
     hidden=[[14, -1]], looks=[[4, 'tint', 'p1_brown']], pxs_changes=[[4, 'burrowed']])
clip('emerge_on_p1', 'p1', 24, dict(show=1, solid=4, settle=12, end=24), next='rotation', hidden=[[0, 1]],
     looks=[[1, 'tint', 'none']], pxs='burrowed', pxs_changes=[[4, 'p1']], scale_in=[1, 4, 0.85])
clip('burrow_in_p1', 'p1', 23, dict(tell=0, inv=5, dive=5, sink=6, hide=21), authored=30, retime=[[0, 0], [30, 23]],
     hidden=[[21, -1]], looks=[[6, 'tint', 'p1_dark']], pxs_changes=[[5, 'burrowed']])
clip('emerge_crown_p1', 'p1', 40, dict(glow=0, crown=5, hood=10, targetable=11, out=21, end=40), next='idle_p1',
     hidden=[[0, 5]], looks=[[5, 'tint', 'p1_dark'], [20, 'tint', 'none']], pxs='burrowed', pxs_changes=[[11, 'p1']])
clip('hands', 'p1', 140, dict(spread=0, swirl=5, raise_=27, plunge=30, lock=33, legs=36, lines=40, slam1=62,
                              slam2=69, slam3=75, slam4=82, sink=83, stand=100, pull=108, flower=118, fold=128,
                              end=140),
     authored=160, retime=[[0, 0], [40, 30], [82, 62], [102, 82], [160, 140]], next='idle_p1',
     yaw=([[5, 0], [27, 360]], 'smooth'), anchors={'plunge': {'impact': [0, 0, 0]}})
clip('glow_slams', 'p1', 131, dict(wind=0, coil=23, column=36, slam1=47, rear2=65, slam2=70, leap=77, apex=83,
                                   dive=90, slam3=101, settle=121, end=131),
     authored=160, retime=[[0, 0], [48, 36], [59, 47], [89, 70], [130, 101], [160, 131]], next='idle_p1',
     looks=[[0, 'core_glow', 'lit'], [47, 'core_glow', 'idle']],
     anchors={'slam1': {'impact': [0, 0, 0]}, 'slam2': {'impact': [0, 0, 0]}, 'slam3': {'impact': [0, 0, 0]}})
clip('rotation', 'p1', 130, dict(arms=0, rear=10, disc=16, full=39, crash=40, spin=47, flash=57, spin_end=71,
                                 rise=85, stand=100, end=130),
     authored=135, retime=[[0, 0], [21, 16], [135, 130]], next='idle_p1', yaw=([[47, 0], [71, 360]], 'smooth'),
     anchors={'crash': {'impact': [0, 0, 0]}})
clip('tail_p1x2', 'p1', 127, dict(turn=0, raise_=8, cock=23, swing1=28, end1=37, cock2=48, swing2=52, end2=59,
                                  rise=86, end=127),
     authored=141, retime=[[0, 0], [37, 28], [46, 37], [66, 52], [73, 59], [141, 127]], next='idle_p1',
     yaw=([[27, 0], [35, 200], [51, 200], [59, 0]], 'linear'), tail=('CROUCH', 'CROUCH'),
     anchors={'cock': {'tail_tip': RIG_ANCHORS['CROUCH']['tail_tip']},
              'swing1': {'tail_root': RIG_ANCHORS['CROUCH']['tail_root']},
              'swing2': {'tail_root': RIG_ANCHORS['CROUCH']['tail_root']}})
clip('combo_a', 'p1', 29, dict(tell=0, swing=10, hit=14), anchors={'hit': {'impact': [0, 0, 0]}})
clip('combo_b', 'p1', 44, dict(rear=0, high=12, slam=17), authored=48, retime=[[0, 0], [18, 14], [48, 44]],
     anchors={'slam': {'impact': [0, 0, -4.8]}})
clip('combo_c', 'p1', 20, dict(twist=0, spin=5, hit=10), yaw=([[5, 0], [15, 360]], 'smooth'),
     anchors={'hit': {'impact': [0, 0, 0]}})
clip('combo_d', 'p1', 77, dict(rear=0, tall=20, lunge=22, slam=27, recover=43), authored=84,
     retime=[[0, 0], [29, 22], [84, 77]], anchors={'slam': {'impact': [0, 0, -7.2]}})
clip('combo_end', 'p1', 20, {}, next='idle_p1')
clip('sink_revive', 'p1', 60, dict(stagger=0, flicker=4, sink=20, chunks=30, hide=45, park=46, end=60),
     hidden=[[45, -1]], looks=[[20, 'tint', 'p1_brown']], pxs_changes=[[6, 'burrowed'], [46, 'parked']])
clip('revival', 'p3', 160, dict(burst=60, splash=60, reach=88, flash2=96, reveal=100, end=160), next='idle_p3',
     blend_out=6, hidden=[[0, 60]],
     looks=[[0, 'form', 'p3'], [0, 'face', 'p3_idle'], [0, 'core', 'p3_sternum'], [0, 'tint', 'none']],
     hands=[[104, 'p3_open']], stance=('UPRIGHT', 'UPRIGHT'), pxs='inv', pxs_changes=[[118, 'p3u']])
clip('idle_p3', 'p3', 60, {}, loop=True, stance=('UPRIGHT', 'UPRIGHT'))
clip('turn_p3', 'p3', 20, dict(step=[0, 5, 10, 15]), loop=True, stance=('UPRIGHT', 'UPRIGHT'),
     yaw=([[0, 0], [19, 114]], 'linear'))   # a loop: the schedule is a rate (6 deg / t, plan §7.3), ap_contract §0.4.5
clip('walk_p3', 'p3', 32, dict(step=[0, 8, 16, 24]), loop=True, stance=('CROUCH', 'CROUCH'))
clip('crouch_p3', 'p3', 8, dict(closed=6, end=8), stance=('UPRIGHT', 'CROUCH'), moves=[(0, 7, 'CROUCH')],
     hands=[[2, 'p3_curl']], looks=[[6, 'face', 'hidden']], pxs_changes=[[6, 'p3c']])
clip('stand_p3', 'p3', 14, dict(open=10, end=14), next='idle_p3', stance=('CROUCH', 'UPRIGHT'),
     moves=[(0, 13, 'UPRIGHT')], looks=[[4, 'face', 'p3_idle']],
     hands=[[5, 'b_hand_l', 'p3_open'], [8, 'b_hand_r', 'p3_open'], [8, 'p3_open']],
     pxs_changes=[[10, 'p3u']])
clip('move_strike_p3', 'p3', 92, dict(fold=0, mound=8, inv=8, hide=16, trail=16, lock=32, show=42, burst=44,
                                      hoop=44, roll=49, slam=61, tail=65, sweep=69, rise=71, stand=85, end=92),
     authored=100, retime=[[0, 0], [22, 16], [52, 44], [100, 92]], next='idle_p3', hidden=[[16, 42]],
     stance=('UPRIGHT', 'UPRIGHT'), moves=[(0, 7, 'CROUCH'), (71, 91, 'UPRIGHT')],
     hands=[[2, 'p3_curl'], [90, 'p3_open']], looks=[[6, 'face', 'hidden'], [89, 'face', 'p3_idle']],
     yaw=([[66, 0], [72, 360]], 'linear'), keyed_pitch=[49, 61], tail=('UPRIGHT', 'UPRIGHT'),
     pxs='p3u', pxs_changes=[[8, 'burrowed'], [44, 'p3c'], [85, 'p3u']],
     anchors={'burst': {'impact': [0, 0, 0]}, 'slam': {'impact': [0, 0, 0]},
              'sweep': {'tail_root': RIG_ANCHORS['CROUCH']['tail_root']}})
clip('aftermath', 'p3', 224, dict(charge=0, whirl=18, land=40, field=40, pillar1=44, pillar2=48, pillar3=52,
                                  dome1=54, dome2=58, dome3=62, rise=76, ticks=80, aloft=84, rain=134, blast=156,
                                  descend=162, window_end=176, pop=189, burst=190, end=224),
     authored=240, retime=[[0, 0], [52, 40], [84, 68], [172, 156], [240, 224]], next='idle_p3',
     stance=('CROUCH', 'UPRIGHT'), moves=[(76, 84, 'UPRIGHT')],
     looks=[[0, 'bright', '15'], [18, 'face', 'p3_charge'], [189, 'face', 'p3_idle'], [189, 'bright', '13']],
     hands=[[76, 'p3_open']], yaw=([[18, 0], [36, 360]], 'smooth'), aloft=(84, 161),
     pxs='p3c', pxs_changes=[[84, 'aloft'], [176, 'p3u']],
     anchors={'charge': {'core': RIG_ANCHORS['CROUCH']['core']}, 'blast': {'core': [0, 13.0, -0.7]}})
clip('shells', 'p3', 113, dict(hunch=0, ring=10, lit=14, lock1=33, launch=35, ball=36, hit1=45, cool=48, lock2=79,
                               lock3=82, hit2=93, hit3=96, end=113),
     authored=140, retime=[[0, 0], [46, 35], [56, 45], [120, 93], [123, 96], [140, 113]], next='idle_p3',
     stance=('UPRIGHT', 'UPRIGHT'), looks=[[14, 'bright', '15'], [48, 'bright', '13']],
     anchors={'launch': {'ball': [0, 9.4, -0.4]}, 'ball': {'ball': [0, 9.4, -0.4]}})
clip('sink_p3', 'p3', 20, dict(fold=0, inv=8, sink=8, hide=12, end=20), hidden=[[12, -1]],
     stance=('UPRIGHT', 'CROUCH'), moves=[(0, 7, 'CROUCH')], hands=[[2, 'p3_curl']],
     looks=[[6, 'face', 'hidden']], pxs='p3u', pxs_changes=[[8, 'burrowed']])
clip('surface_p3', 'p3', 40, dict(show=0, splash=0, charge=0, launch=10, hit=12, recover=12, end=40),
     next='stand_p3', hidden=[[0, 0]], stance=('CROUCH', 'CROUCH'), looks=[[0, 'bright', '15'], [10, 'bright', '13']],
     pxs='burrowed', pxs_changes=[[0, 'p3c']], anchors={'launch': {'muzzle': [0, 2.9, -3.6]}})
clip('tail_p3', 'p3', 87, dict(crouch=0, cock=3, swing1=14, rise=24, coil=36, lunge=36, swing2=46, rise2=57, end=87),
     authored=100, retime=[[0, 0], [14, 11], [18, 15], [58, 45], [62, 49], [100, 87]], next='idle_p3',
     stance=('CROUCH', 'UPRIGHT'), moves=[(57, 86, 'UPRIGHT')], looks=[[61, 'face', 'p3_idle']],
     hands=[[62, 'p3_open']], yaw=([[13, 0], [21, 200], [45, 200], [53, 0]], 'linear'), tail=('CROUCH', 'UPRIGHT'),
     pxs='p3c', pxs_changes=[[57, 'p3u']],
     anchors={'cock': {'tail_tip': RIG_ANCHORS['CROUCH']['tail_tip']},
              'swing1': {'tail_root': RIG_ANCHORS['CROUCH']['tail_root']},
              'swing2': {'tail_root': RIG_ANCHORS['CROUCH']['tail_root']}})
clip('spikes', 'p3', 72, dict(curl=4, rise=10, column=14, summon=19, lockA=37, fireA=42, lockB=43, fireB=48, hitA=49,
                              blades=52, hitB=55, skim=64, recover=65, end=72),
     authored=84, retime=[[0, 0], [49, 37], [54, 42], [84, 72]], next='idle_p3', stance=('UPRIGHT', 'UPRIGHT'),
     looks=[[10, 'bright', '15'], [48, 'bright', '13']],
     anchors={'column': {'crown': RIG_ANCHORS['UPRIGHT']['crown']}, 'summon': {'crown': RIG_ANCHORS['UPRIGHT']['crown']}})
clip('death', 'p3', 120, dict(hit=0, flicker=8, droop=30, kneel=55, fall=70, land=82, wither=85, sink=100, gone=118,
                              end=120),
     blend_in=6, hidden=[[118, -1]], stance=('UPRIGHT', 'UPRIGHT'),
     looks=[[30, 'face', 'p3_dim'], [85, 'tint', 'withered']], hands=[[55, 'p3_curl']], pxs='dead')


def smooth(u):
    return u * u * (3 - 2 * u)


def dense_yaw(knots, ease, n):
    out = []
    for t in range(n):
        if t <= knots[0][0]:
            v = knots[0][1]
        elif t >= knots[-1][0]:
            v = knots[-1][1]
        else:
            for (t0, v0), (t1, v1) in zip(knots, knots[1:]):
                if t0 <= t <= t1:
                    u = (t - t0) / (t1 - t0)
                    v = v0 + (v1 - v0) * (smooth(u) if ease == 'smooth' else u)
                    break
        out.append(round(v, 2) + 0.0)
    return out


def flat_events(ev):
    out = {}
    for k, v in ev.items():
        k = 'raise' if k == 'raise_' else k
        if isinstance(v, list):
            for i, t in enumerate(v, 1):
                out[f'{k}_{i}'] = t
        else:
            out[k] = v
    return out


def build_clip(cid, c):
    L = c['played']
    stance = c.get('stance') or ('CROUCH', 'CROUCH')
    hidden = []
    for a, b in c.get('hidden', []):
        b = L if b == -1 else b
        if b > a:
            hidden.append([a, b - 1, 'all'])
    vis = []
    for a, b, _ in hidden:
        vis.append([a, 'burrowed'])
        if b + 1 <= L - 1:
            vis.append([b + 1, 'normal'])
    if c['name'] == 'surface_p3':
        vis = [[0, 'normal']]

    moves = c.get('moves', [])

    def stance_at(t):
        s = stance[0]
        for _t0, t1, se in moves:
            if t1 <= t:
                s = se
        return s

    def is_hidden(t):
        return any(a <= t <= b for a, b, _ in hidden)

    ticks = {0, L - 1}
    for t0, t1, _ in moves:
        ticks.update({t0, t1})
    for a, b, _ in hidden:
        ticks.update({a, b} | ({a - 1} if a >= 1 else set()) | ({b + 1} if b + 1 <= L - 1 else set()))
    al = c.get('aloft')
    if al:
        ticks.update({al[0], al[1], al[1] + 1})
    keys = {}
    for t in sorted(x for x in ticks if 0 <= x <= L - 1):
        tops = {'head': 10.0, 'chest': 10.0} if al and al[0] <= t <= al[1] else None
        keys[str(t)] = px_table(stance_at(t), hidden=is_hidden(t), tops=tops)

    pxs = c.get('pxs') or ('p1' if c['form'] == 'p1' else ('p3u' if stance[0] == 'UPRIGHT' else 'p3c'))
    o = {'id': cid, 'name': c['name'], 'len': L, 'authored': c.get('authored', L), 'loop': bool(c.get('loop')),
         'next': c.get('next'), 'mirror_of': None, 'retime': c.get('retime', []),
         'events': flat_events(c['events']),
         'anchors': {ev: {k: loc(v) for k, v in pts.items()} for ev, pts in c.get('anchors', {}).items()},
         'tracks': {},
         'px': {'lerp': True, 'keys': keys},
         'yaw': dense_yaw(c['yaw'][0], c['yaw'][1], L) if c.get('yaw') else None,
         'hidden': hidden, 'root_z': [], 'state': vis,
         'form': c['form'], 'stance': {'start': stance[0], 'end': stance[1]},
         'stance_events': [[t1, se] for _t0, t1, se in moves],
         'px_sets': [[0, pxs]] + c.get('pxs_changes', []),
         'look_events': c.get('looks', []), 'hand_events': c.get('hands', [])}
    if c.get('tail'):
        s0, s1 = c['tail']
        r0, r1 = ANCHORS[s0]['tail_root'], ANCHORS[s1]['tail_root']
        p0, p1 = ANCHORS[s0]['tail_tip'], ANCHORS[s1]['tail_tip']
        lerp = lambda a, b, u: [round(a[i] + (b[i] - a[i]) * u, 3) + 0.0 for i in range(3)]
        o['tracks'] = {'tail_root': [lerp(r0, r1, t / max(L - 1, 1)) for t in range(L)],
                       'tail_tip': [lerp(p0, p1, t / max(L - 1, 1)) for t in range(L)]}
    for k in ('blend_in', 'blend_out', 'keyed_pitch', 'scale_in'):
        if c.get(k) is not None:
            o[k] = c[k]
    return o


def build_rig():
    parts, idx = [], {}
    for i, (name, region, parent, scale, b1, b3) in enumerate(PARTS):
        model = (f'{name}_p1_planted' if name in ('a_hand_l', 'a_hand_r') else
                 f'{name}_p1_open' if name in HAND_PARTS else
                 'face_p1_bud' if name == 'face' else 'core_p1_bulb' if name == 'core' else f'{name}_p1')
        p = {'name': name, 'region': region, 'uuid': f'{BLOCK}{i:02x}', 'idx': i, 'tag': f'rlk_mb_ap_{name}',
             'model': model, 'brightness': b1, 'scale': scale, 'elements': 0, 'parent': parent,
             'tol_tp': 0.012 if (name in ('hood', 'face', 'crown') or name in HAND_PARTS) else 0.03}
        if b3 != b1:
            p['brightness_p3'] = b3
        parts.append(p)
        idx[name] = i
    assert len(parts) == 49

    form_parts = {n: {'p1': f'{n}_p1', 'p3': f'{n}_p3'} for n, *_ in PARTS if n not in HAND_PARTS and n not in OWN_CHANNEL}
    fn = lambda path: NS + path
    looks = {
        'form': {'objective': 'apRigForm', 'ids': {'p1': 0, 'p3': 1}, 'parts': form_parts,
                 'also': {'p1': {'face': 'p1_bud', 'core': 'p1_bulb', 'hands': 'p1_rest', 'tint': 'none'},
                          'p3': {'face': 'p3_idle', 'core': 'p3_sternum', 'hands': 'p3_open', 'tint': 'none'}},
                 'brightness': {'p3': {p['name']: p['brightness_p3'] for p in parts if 'brightness_p3' in p}},
                 'functions': {f: fn(f'look/form/{f}') for f in ('p1', 'p3')}},
        'face': {'objective': 'apRigFace', 'ids': {'p1_bud': 0, 'p3_idle': 1, 'p3_charge': 2, 'p3_dim': 3, 'hidden': 4},
                 'parts': {'face': {'p1_bud': 'face_p1_bud', 'p3_idle': 'face_p3_idle', 'p3_charge': 'face_p3_charge',
                                    'p3_dim': 'face_p3_dim', 'hidden': None}},
                 'functions': {f: fn(f'look/face/{f}') for f in ('p1_bud', 'p3_idle', 'p3_charge', 'p3_dim', 'hidden')}},
        'core': {'objective': 'apRigCore', 'ids': {'p1_bulb': 0, 'p3_sternum': 1},
                 'parts': {'core': {'p1_bulb': 'core_p1_bulb', 'p3_sternum': 'core_p3_sternum'}},
                 'functions': {f: fn(f'look/core/{f}') for f in ('p1_bulb', 'p3_sternum')}},
        'core_glow': {'objective': 'apRigGlow', 'ids': {'idle': 0, 'lit': 1},
                      'brightness': {'idle': {'core': 12}, 'lit': {'core': 15}},
                      'functions': {f: fn(f'look/core_glow/{f}') for f in ('idle', 'lit')}},
        'tint': {'objective': 'apRigTint', 'ids': {'none': 0, 'p1_dark': 1, 'p1_brown': 2, 'withered': 3, 'p3_dim': 4},
                 'colors': {'p1_dark': '#2D2A04', 'p1_brown': '#605D37', 'withered': '#8C8458', 'p3_dim': '#6F8A73'},
                 'forms': {'p1_dark': ['p1'], 'p1_brown': ['p1'], 'withered': ['p3'], 'p3_dim': ['p3']},
                 'item_pattern': '{model}_t{id}',
                 'functions': {f: fn(f'look/tint/{f}') for f in ('none', 'p1_dark', 'p1_brown', 'withered', 'p3_dim')}},
        'bright': {'objective': 'apRigBright', 'ids': {'13': 0, '15': 1},
                   'brightness': {'15': {n: 15 for n, *_ in PARTS}},
                   'functions': {'13': fn('bright/13'), '15': fn('bright/15')}},
    }
    variants = {hp: {v: f'{hp}_{v}' for v in HAND_VARIANTS[hp[0]]} for hp in HAND_PARTS}
    hands = {'objective': 'apRigHands', 'parts': HAND_PARTS, 'variants': variants,
             'sets': {s: {hp: m[hp[0]] for hp in HAND_PARTS} for s, m in HAND_SETS.items()},
             'ids': {s: i for i, s in enumerate(HAND_SETS)},
             'functions': {'set': fn('hands/<set>'), 'part': fn('hand/<part>/<variant>')},
             'pulse': {'from': 0.9, 'to': 1.0, 'ticks': 2}}
    w_fixed = {p[0]: max(p[3][2], p[4][2]) for p in PROXIES}
    layout = []
    for k, (name, part, group, _, _) in enumerate(PROXIES):
        layout.append({'name': name, 'part': part, 'point': [0.0, 0.0, 0.0], 'w': w_fixed[name], 'top_margin': 0.0,
                       'tail_only': False, 'idx': 0x41 + k, 'uuid': f'{BLOCK}{0x41 + k:02x}', 'flash': group,
                       'plan': f'px_{name}'})
    proxies = {'layout': layout, 'rest': px_table('CROUCH'),
               'rest_by_stance': {'CROUCH': px_table('CROUCH'), 'UPRIGHT': px_table('UPRIGHT')},
               'coverage': {'within': 3.0, 'target': 1.0, 'poses': ['CROUCH', 'UPRIGHT', 'HOOP', 'CROUCH_OVER']}}
    states = {
        'p1': {'px': ALL_PX, 'vis': 'normal', 'inv': False, 'capsules': STANCE_CAPSULES['CROUCH']},
        'p3u': {'px': ALL_PX, 'vis': 'normal', 'inv': False, 'capsules': STANCE_CAPSULES['UPRIGHT']},
        'p3c': {'px': ALL_PX, 'vis': 'normal', 'inv': False, 'capsules': STANCE_CAPSULES['CROUCH']},
        'burrowed': {'px': [], 'vis': None, 'inv': True, 'capsules': []},
        'aloft': {'px': ['head', 'chest'], 'vis': 'normal', 'inv': False, 'capsules': []},
        'inv': {'px': [], 'vis': None, 'inv': True, 'capsules': []},
        'parked': {'px': [], 'vis': None, 'inv': True, 'capsules': []},
        'dead': {'px': [], 'vis': None, 'inv': True, 'capsules': []},
    }
    clips = [build_clip(STUB_ID0 + i, c) for i, c in enumerate(C)]
    functions = {
        'init': fn('init'), 'spawn': fn('spawn'), 'tick': fn('tick'), 'kill': fn('kill'), 'uninstall': fn('uninstall'),
        'look_apply': fn('look_apply'),
        'play': {c['name']: fn(f'play/{c["name"]}') for c in clips},
        'face': {'player': fn('face/player'), 'track': fn('face/track'), 'set': fn('face/set')},
        'state': {'normal': fn('state/normal'), 'burrowed': fn('state/burrowed')},
        'flash': {g: fn(f'flash/{g}') for g in FLASH_GROUPS},
        'park': fn('park'), 'unpark': fn('unpark'),
        'stance': {'CROUCH': fn('stance/crouch'), 'UPRIGHT': fn('stance/upright')},
        'hands': {s: fn(f'hands/{s}') for s in HAND_SETS},
        'hand': {hp: {v: fn(f'hand/{hp}/{v}') for v in vs} for hp, vs in variants.items()},
        'look': {ch: c['functions'] for ch, c in looks.items() if ch != 'bright'},
        'bright': looks['bright']['functions'],
    }
    ledger = [
        ('hood_shell', 'head', 192, 128, 48, 'tinted', 'both'), ('hood_face_p1', 'head', 128, 128, 48, 'unique', 'p1'),
        ('face_p1_bud', 'head', 128, 128, 64, 'unique', 'p1'), ('face_p3_mask', 'head', 128, 112, 64, 'unique', 'p3'),
        ('face_p3_charge', 'head', 128, 112, 64, 'unique', 'p3'), ('crown_p1', 'head', 128, 64, 64, 'unique', 'p1'),
        ('crown_p3_fan', 'head', 192, 128, 64, 'unique', 'p3'), ('hair_ribbon', 'head', 64, 128, 32, 'tinted', 'both'),
        ('neck_collar', 'head', 128, 64, 32, 'tinted', 'both'), ('scarf_p3', 'head', 64, 64, 32, 'unique', 'p3'),
        ('thorax_plates', 'body', 128, 128, 32, 'tinted', 'both'), ('ribs_bark', 'body', 128, 64, 32, 'tinted', 'both'),
        ('hump_dorsal', 'body', 128, 128, 32, 'tinted', 'both'), ('mantle', 'body', 128, 128, 32, 'tinted', 'both'),
        ('core_p1_sac', 'body', 64, 64, 48, 'unique', 'p1'), ('sternum_p3', 'body', 64, 128, 48, 'unique', 'p3'),
        ('robe_p3', 'body', 128, 128, 32, 'unique', 'p3'), ('hem_p3', 'body', 128, 64, 32, 'unique', 'p3'),
        ('belly_ribbon_p1', 'body', 64, 128, 32, 'unique', 'p1'), ('crystal_gold_p1', 'body', 32, 64, 48, 'unique', 'p1'),
        ('emerald_p3', 'body', 32, 64, 48, 'unique', 'p3'), ('cones', 'body', 32, 64, 48, 'tinted', 'both'),
        ('gem_p1', 'body', 32, 32, 48, 'unique', 'p1'),
        ('limb_shell', 'limbs', 64, 128, 32, 'tinted', 'both'), ('arm_shell', 'limbs', 64, 128, 32, 'tinted', 'both'),
        ('leaf_cladding_p3', 'limbs', 128, 128, 32, 'unique', 'p3'), ('beads_p3', 'limbs', 64, 64, 32, 'unique', 'p3'),
        ('petal_p1', 'hands', 128, 128, 64, 'unique', 'p1'), ('claw_p1', 'hands', 64, 64, 48, 'unique', 'p1'),
        ('leafhand_b_p3_open', 'hands', 144, 144, 64, 'unique', 'p3'),
        ('leafhand_b_p3_curl', 'hands', 128, 128, 64, 'unique', 'p3'),
        ('leafhand_c_p3', 'hands', 128, 64, 48, 'unique', 'p3'), ('glyph_c_p3', 'hands', 32, 32, 48, 'unique', 'p3'),
        ('fork_a_p3', 'hands', 64, 64, 48, 'unique', 'p3'),
        ('tail_band', 'tail', 64, 128, 32, 'tinted', 'both'), ('tail_hook_p1', 'tail', 64, 64, 32, 'unique', 'p1'),
        ('tail_whip_p3', 'tail', 64, 64, 32, 'unique', 'p3'),
    ]
    entries = [{'name': n, 'region': r, 'w': w, 'h': h, 'px': w * h, 'px_per_b': d, 'use': u, 'forms': f}
               for n, r, w, h, d, u, f in ledger]
    regions = {}
    for e in entries:
        regions[e['region']] = regions.get(e['region'], 0) + e['px']
    total = sum(regions.values())
    region_parts = {}
    for p in parts:
        region_parts[p['region']] = region_parts.get(p['region'], 0) + 1

    return {
        'schema': 1, 'boss': 'apep', 'source': 'stub', 'apep': 1,
        'runtime': {'ns': NS, 'clip_obj': 'apRigC', 'tick_obj': 'apRigT', 'state_obj': 'apRigState',
                    'form_obj': 'apRigForm', 'stance_obj': 'apRigStance', 'face_obj': 'apRigFace',
                    'core_obj': 'apRigCore', 'glow_obj': 'apRigGlow', 'tint_obj': 'apRigTint',
                    'bright_obj': 'apRigBright', 'hands_obj': 'apRigHands', 'park_obj': 'apRigPark'},
        'functions': functions,
        'parts': parts,
        'shadow': {'uuid': f'{BLOCK}40', 'idx': 0x40, 'tag': 'rlk_mb_ap_shadow', 'shadow_radius': 4.5,
                   'shadow_strength': 0.8},
        'uuids': {'block': BLOCK, 'ints': RIG_INTS, 'parts': idx, 'shadow': 0x40,
                  'proxies': {x['name']: x['idx'] for x in layout}, 'props': {}},
        'skeleton': {'joints': JOINTS['CROUCH'], 'scale_H': 4.4,
                     'joints_by_stance': JOINTS,
                     'bones': {**{n: {'parent': p, 'pose_only': True} for n, p in POSE_ONLY.items()},
                               **{n: {'parent': par, 'pose_only': False} for n, _, par, *_ in PARTS}}},
        'rest_anchors': ANCHORS['CROUCH'],
        'torso_hw': 1.5,
        'proxies': proxies,
        'states': states,
        'capsules': CAPSULES,
        'flash_groups': FLASH_GROUPS,
        'looks': looks,
        'tinted_items': {},
        'clips': clips,
        'culling': {'width': 30, 'height': 16, 'view_range': 3},
        'budgets': {'parts': 49, 'part_cap': 56, 'models': 0, 'hand_models': sum(len(v) for v in variants.values()),
                    'atlas_px': total, 'atlas_budget': 900000,
                    'elements_shown_rest': {'p1': 0, 'p3': 0}, 'elements_budget': {'p1': 7000, 'p3': 8000},
                    'regions': {r: {'parts': region_parts[r], 'px': regions.get(r, 0)} for r in region_parts}},
        'objectives': {
            'apRigC': 'current clip id (anchor)', 'apRigT': 'tick of the pose shown this tick (-1 = queued)',
            'apRigF': 'hit flash countdown', 'apRigY': 'face/track scratch', 'apRigState': 'visibility: 0 normal, 1 burrowed',
            'apRigForm': 'form look: 0 p1, 1 p3', 'apRigStance': 'stance: 0 CROUCH, 1 UPRIGHT', 'apRigFace': 'face look id',
            'apRigCore': 'core look id', 'apRigGlow': 'core glow: 0 idle, 1 lit', 'apRigTint': 'tint id (0 none)',
            'apRigBright': 'body brightness: 0 = own levels, 1 = 15', 'apRigHands': 'hand set id',
            'apRigPark': '1 while parked'},
        'textures': len(entries),
        'fallbacks': [c['name'] for c in clips],
        # ---- Apep extras (rig_manifest.schema.json; ap_contract.md §0.4)
        'stances': {'objective': 'apRigStance', 'ids': {'CROUCH': 0, 'UPRIGHT': 1},
                    'default': {'p1': 'CROUCH', 'p3': 'UPRIGHT'},
                    'rest_anchors': ANCHORS, 'torso_hw': {'CROUCH': 1.5, 'UPRIGHT': 1.3},
                    'heights': {'CROUCH': {'hood_top': 4.4, 'crown_tip': 5.0, 'length': 15.0},
                                'UPRIGHT': {'hood_top': 8.5, 'face_low': 6.0, 'face_high': 7.85}},
                    'transitions': {'stand_p3': {'from': 'CROUCH', 'to': 'UPRIGHT'},
                                    'crouch_p3': {'from': 'UPRIGHT', 'to': 'CROUCH'}},
                    'px_set': {'p1': {'CROUCH': 'p1'}, 'p3': {'CROUCH': 'p3c', 'UPRIGHT': 'p3u'}}},
        'hands': hands,
        'park': {'objective': 'apRigPark', 'px_set': 'parked', 'shadow': False, 'tick': 'skip',
                 'respawn': 'keeps scale 0 while the flag is set',
                 'reapply': ['form', 'stance', 'looks', 'hands', 'follow']},
        'sprites': {'budget': 900000, 'total': total, 'regions': regions, 'ledger': entries, 'planned': True,
                    'densities': {'face': 64, 'crown': 64, 'b_hand': 64, 'hood': 48, 'default': 32}},
        'elements': {'budget': {'p1': 7000, 'p3': 8000}, 'visible_rest': {'p1': 0, 'p3': 0},
                     'per_region': {r: {'p1': 0, 'p3': 0} for r in ('head', 'body', 'limbs', 'hands', 'tail')},
                     'densest': ['face', 'crown', 'b_hand_l', 'b_hand_r', 'hood', 'shoulders']},
    }

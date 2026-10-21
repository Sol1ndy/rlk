"""아펩의 오아시스 파수꾼 (Apep) stub org manifest (AP-CORE): the day-0 organisms / Heart / domes / walls / stalks /
seed manifest of S:ap/spec/make_stubs.py (AP-SPEC, D0), carried over verbatim (ap_contract.md 0.5). api.py reads the
real T:mboss_apep_org_manifest.json (AP-ORG, merged at AP-I1) when it exists, else this stub (T:mboss_apep/
stub_org_manifest.json, written by emit()). Dropped at AP-I1 (plan 10 AP-I1 "stub org dropped").
"""
import json
from pathlib import Path
import mboss_lib as L

from .stub_rig import flat_events

HERE = Path(__file__).resolve().parent
# ------------------------------------------------------------------------------------------------ org
OBLOCK = '524c4b4d-4150-4800-8000-0000000000'
ORG_INTS = [1380731725, 1095780352, -2147483648]
RIDE_Y = 2.0
_cid = [0]


def oclip(name, length, events=None, loop=False, nxt=None, note=None):
    c = {'id': _cid[0], 'name': name, 'len': length, 'loop': loop, 'next': nxt, 'events': flat_events(events or {})}
    if note:
        c['note'] = note
    _cid[0] += 1
    return c


def disp(kind, name, looks, default, br=14, scale=1.0, pivot='feet', pivot_y=0.0, overlay=False, note=None):
    d = {'name': name, 'tag': f'rlk_ap_om_{name}', 'model': f'{kind}_{name}_{default}',
         'looks': {k: f'{kind}_{name}_{k}' for k in looks}, 'default_look': default, 'brightness': br,
         'scale': scale, 'pivot': pivot, 'offset': [0.0, round(-RIDE_Y + pivot_y, 3), 0.0], 'overlay': overlay}
    if note:
        d['note'] = note
    return d


def fixed(name, idx, looks, default, br=14, scale=1.0, pivot='feet', note=None):
    d = {'name': name, 'idx': idx, 'uuid': f'{OBLOCK}{idx:02x}', 'tag': f'rlk_mb_ap_{name}', 'model': f'{name}_{default}',
         'looks': {k: f'{name}_{k}' for k in looks}, 'default_look': default, 'brightness': br, 'scale': scale,
         'pivot': pivot}
    if note:
        d['note'] = note
    return d


def setd(name, idxs, br=14, scale=1.0, note=None):
    d = {'name': name, 'idxs': idxs, 'tag': f'rlk_mb_ap_{name}', 'model': name, 'looks': {'idle': name},
         'default_look': 'idle', 'brightness': br, 'scale': scale, 'pivot': 'feet'}
    if note:
        d['note'] = note
    return d


def build_org():
    _cid[0] = 0
    kinds = {}

    def kind(key, kid, kor, size, hp_bar_y, shield, displays, clips, elements, px, hover_y=0.0, note=None):
        k = {'id': kid, 'name': kor, 'tag': f'rlk_mb_ap_{key}', 'size': size, 'hover_y': hover_y,
             'hp_bar_y': hp_bar_y, 'shield': {'w': shield[0], 'h': shield[1]}, 'displays': displays, 'clips': clips,
             'budget': {'elements': elements, 'px': px}, 'elements': 0, 'px': 0}
        if note:
            k['note'] = note
        kinds[key] = k

    kind('basic', 1, '기본', {'h': 1.15, 'h_stem': 1.35, 'd': 0.9, 'bag': [1.43, 1.31]}, 1.6, (1.2, 1.6),
         [disp('basic', 'bulb', ['bell', 'bag', 'buffed', 'bag_buffed', 'dying'], 'bell'),
          disp('basic', 'crown', ['closed', 'open'], 'closed', note='the crown glow (15) is painted emissive'),
          disp('basic', 'shield', ['on'], 'on', overlay=True,
               note='2-4 cutout leaf panes 1.3 x 0.55 + a low-alpha bubble rim + a yellow 3-leaf crown; only while '
                    'shielded')],
         [oclip('org_spawn', 20, nxt='basic_bob'), oclip('basic_bob', 24, loop=True),
          oclip('basic_melee', 14, {'hit': 10}, nxt='basic_bob'),
          oclip('basic_lie', 10, {'bag': 10}, note='bell -> bag'),
          oclip('basic_ranged', 20, {'open': 0, 'fire': 12}, note='crown open 0-12'),
          oclip('org_die', 10, {'gone': 10})], 350, 12000,
         note='bag_buffed added by AP-SPEC: a buffed ranged basic lies as a bag')
    kind('nurt', 2, '양육', {'h': 2.4}, 2.8, (1.4, 2.6),
         [disp('nurt', 'stalk', ['idle'], 'idle', note='S-curved dark-teal ribbon'),
          disp('nurt', 'cap', ['idle', 'tilt'], 'idle', note='cream hood-leaf'),
          disp('nurt', 'orb', ['on'], 'on', br=15, note='pulse'),
          disp('nurt', 'ring', ['on'], 'on', overlay=True, note='translucent cylinder r 1.3, h 0.5, only while immune')],
         [oclip('nurt_idle', 40, loop=True), oclip('nurt_buff', 20, {'tilt': 0, 'tethers': 8}, nxt='nurt_idle'),
          oclip('nurt_die', 17, {'gone': 17})], 450, 16000)
    kind('guard', 3, '수호', {'h': 4.4, 'bud': 2.0, 'orb_d': 0.4}, 3.0, (1.4, 3.0),
         [disp('guard', 'spire', ['spire', 'bud', 'wisp'], 'spire', pivot='mid', pivot_y=2.2),
          disp('guard', 'orb', ['on'], 'on', br=15, pivot='mid', pivot_y=5.0, note='bob 0.6-0.8 above the tip')],
         [oclip('guard_idle', 60, loop=True),
          oclip('guard_cast', 30, {'collapse': 0, 'bud': 7, 'regrow': 16, 'regrow_end': 24, 'shields': 30},
                nxt='guard_idle'),
          oclip('guard_die', 17, {'gone': 17})], 450, 16000,
         note='HP bar beside the base (+3.0); the orb at about 5 b is out of reach')
    kind('nest', 4, '둥지', {'w': 2.2, 'h': 1.3}, 2.2, (1.6, 2.2),
         [disp('nest', 'cap', ['idle'], 'idle', note='cap + the orb eye (painted emissive)'),
          disp('nest', 'wing_l', ['idle'], 'idle'), disp('nest', 'wing_r', ['idle'], 'idle')],
         [oclip('nest_fly', 14, loop=True), oclip('nest_cast', 12, {'walls': 12}, nxt='nest_fly'),
          oclip('nest_blink', 6, {'out': 0, 'in': 3}, nxt='nest_fly'), oclip('org_die', 12, {'gone': 12})], 400, 12000, hover_y=1.0)
    kind('destr', 5, '파괴', {'d': 1.2, 'spikes': 0.2, 'beak': 0.4}, 1.6, (1.3, 1.3),
         [disp('destr', 'shell', ['normal', 'husk'], 'normal'),
          disp('destr', 'face', ['on'], 'on', br=15, note='pulse scale')],
         [oclip('destr_roll', 32, loop=True), oclip('destr_fuse', 56, {'pulse': [0, 9, 18, 27, 36], 'fast': 36},
                                                    nxt='destr_suck'),
          oclip('destr_suck', 5, nxt='destr_blast'), oclip('destr_blast', 1, {'blast': 1}), oclip('org_die', 10, {'gone': 10})],
         300, 8000)
    kind('pred', 6, '포식성', {'fish': [2.5, 1.3], 'bud': [2.1, 1.6], 'pod': [3.5, 1.8]}, 2.2, (1.6, 1.6),
         [disp('pred', 'body', ['fish', 'fish_flare', 'bud', 'pod', 'face'], 'fish'),
          disp('pred', 'jaw', ['idle'], 'idle'), disp('pred', 'fin', ['idle'], 'idle'),
          disp('pred', 'core', ['on'], 'on', br=15)],
         [oclip('pred_swim', 16, loop=True, note='fin yaw +-25, body +-8 with 3 t lag'),
          oclip('pred_swallow', 24, {'eat': 12, 'bud': 14}, nxt='pred_bud'), oclip('pred_bud', 20, loop=True),
          oclip('pred_inflate', 10, nxt='pred_burst'), oclip('pred_burst', 10, {'hit': 0, 'fish': 2}, nxt='pred_swim'),
          oclip('pred_bite', 6, {'open': 0, 'hit': 4}, nxt='pred_swim'),
          oclip('pred_bite_chain', 38, {'hit': [4, 10, 16, 22]}, nxt='pred_swim'),
          oclip('org_die', 12, {'gone': 12})], 500, 20000, hover_y=1.2)

    heart = {
        'kind': 'single', 'tag': 'rlk_mb_ap_heart',
        'marker': {'tags': ['rlk_mb_ap_heart', 'rlk_room', 'rlk_mb_aux'], 'not': ['rlk_mob', 'rlk_zmob']},
        'displays': [
            fixed('heart_bulb', 0x00, ['idle', 'egg_gold', 'egg_green', 'withered', 'blaze'], 'idle', br=15,
                  note='translucent lemon seed 3.2 x 2.6 x 2.3, alpha ~0.85; the arrival egg = this model at scale 0.7, '
                       'pitch 0 (upright)'),
            fixed('heart_cradle', 0x01, ['pedestal', 'full'], 'pedestal', scale=2.2, pivot='mid'),
            fixed('heart_arms', 0x02, ['idle'], 'idle', scale=2.2, pivot='mid', note='root arms to 4.0-4.3 b'),
            fixed('heart_tips', 0x03, ['idle'], 'idle', br=15, note='leaf-flame sprouts, swaying'),
            fixed('vine_hand', 0x04, ['idle', 'wrap'], 'idle'),
        ] + [fixed(f'vine_stem_{k}', 0x05 + k, ['idle'], 'idle') for k in range(4)],
        'egg': {'scale': 0.7, 'pitch': 0, 'land_ticks': 6},
        'clips': [oclip('heart_hang', 80, loop=True), oclip('heart_up', 30, nxt='heart_hang'), oclip('heart_lower', 50),
                  oclip('heart_drop', 30, {'land': 6, 'beam': 6, 'beam_end': 16}, nxt='heart_idle'),
                  oclip('heart_idle', 40, loop=True),
                  oclip('heart_hit', 6, nxt='heart_idle'), oclip('heart_gain', 8, nxt='heart_idle'), oclip('heart_wither', 30), oclip('heart_blaze', 24),
                  oclip('heart_lift', 46), oclip('cradle_rise', 20), oclip('cradle_sink', 10)],
        'footprint': {
            'centre': 'the arena centre (cx, cz) = theme POINTS["heart"]',
            'note': 'bearings are compass degrees around the centre: 0 = north (-z), 90 = east (+x), 180 = south (+z)',
            'bulb_box': {'l': 3.2, 'w': 2.6, 'h': 2.3, 'centre_y': 1.6, 'yaw': 0},
            'root_radius': 2.5,
            'sockets': [{'id': 0, 'bearing': 0, 'r': 3.4}, {'id': 1, 'bearing': 120, 'r': 3.4},
                        {'id': 2, 'bearing': 240, 'r': 3.4}],
            'wait_ring': 4.5, 'destr_stop': {'r': 2.6, 'bearings': [60, 180, 300]}, 'wall_exclusion': 4.6,
            'bolt_end': {'r': 1.5, 'from': 'bulb_box'}, 'swirl_r': 3.5,
            'hang': {'entrance_y': 9.0, 'canopy_y': 20.0, 'lowered_y': 3.0}},
        'budget': {'elements': 800, 'px': 40000}, 'elements': 0, 'px': 0}
    domes = {'kind': 'fixed_set', 'count': 3, 'tag': 'rlk_mb_ap_dome', 'radius': 4.5,
             'displays': [setd('dome_shell', [0x10, 0x12, 0x14], scale=3.3,
                               note='two-sided shell, inward lathe, alpha <= 0.35'),
                          setd('dome_decor', [0x11, 0x13, 0x15], scale=3.3,
                               note='cutout vine / leaf-sprig pattern, bright base rim, light seam, sprout on top')],
             'clips': [oclip('dome_rise', 10, nxt='dome_idle'), oclip('dome_idle', 40, loop=True), oclip('dome_pop', 6)],
             'budget': {'elements': 300, 'px': 24000}, 'elements': 0, 'px': 0}
    walls = {'kind': 'multi', 'max': 15, 'tag': 'rlk_mb_ap_wall',
             'displays': [{'name': 'wall_blade', 'tag': 'rlk_mb_ap_wall_blade', 'model': 'wall_blade',
                           'looks': {'idle': 'wall_blade'}, 'default_look': 'idle', 'brightness': 14, 'scale': 2.0,
                           'pivot': 'feet',
                           'note': 'translucent yellow-green blade 2.5-3 b, darker midrib, two cutout windows'}],
             'clips': [oclip('wall_rise', 5), oclip('wall_fade', 8)],
             'blocks': {'block': 'minecraft:barrier', 'y': [201, 202], 'place': 'replace air'},
             'budget': {'elements': 60, 'px': 8000}, 'elements': 0, 'px': 0}
    stalks = {'kind': 'fixed_set', 'count': 4, 'tag': 'rlk_mb_ap_stalk', 'height': [5.5, 6.0],
              'displays': [setd('stalk_low', [0x20, 0x23, 0x26, 0x29], br=13, scale=2.2),
                           setd('stalk_high', [0x21, 0x24, 0x27, 0x2A], br=13, scale=2.2),
                           setd('stalk_tip', [0x22, 0x25, 0x28, 0x2B], note='hooked tip + small gold cone')],
              'clips': [oclip('leg_rise', 10), oclip('leg_slam', 6, {'hit': 4}), oclip('leg_sink', 10)],
              'budget': {'elements': 240, 'px': 16000}, 'elements': 0, 'px': 0}
    seed = {'kind': 'single', 'tag': 'rlk_mb_ap_seed',
            'displays': [fixed('seed', 0x30, ['idle'], 'idle', br=15, note='glowing golden seed at the death spot')],
            'clips': [], 'budget': {'elements': 40, 'px': 2000}, 'elements': 0, 'px': 0}
    return {
        'schema': 1, 'boss': 'apep', 'source': 'stub', 'manifest': 'org',
        'runtime': {'ns': f'rlk:{L.fn_root_of("apep")}/om/', 'kind_obj': 'apK', 'clip_obj': 'apOI', 'tick_obj': 'apOC'},
        'uuids': {'block': OBLOCK, 'ints': ORG_INTS},
        'objectives': {'apK': 'organism kind id (kinds.<k>.id)', 'apS': 'organism state', 'apT': 'state clock',
                       'apL': 'link id (buffed basic -> its 양육)', 'apShd': 'shield pool', 'apOC': 'org clip clock',
                       'apOI': 'org clip id (clips[].id)', 'apSock': 'Heart socket (0-2, -1 none)',
                       'apTok': 'attack token'},
        'passenger': {'ride_y': RIDE_Y, 'tag_prefix': 'rlk_ap_om_', 'tags': ['rlk_room', 'rlk_mb_aux'],
                      'face': 'rotate',
                      'key': 'execute on passengers if entity @s[tag=rlk_ap_om_<display>] run data merge entity @s {..}'},
        'spawn': {'marker_ticks': 20, 'scale_in': {'ticks': 4, 'from': 0.85}, 'untargetable_until': 'solid'},
        'kinds': kinds,
        'objects': {'heart': heart, 'dome': domes, 'wall': walls, 'stalk': stalks, 'seed': seed},
        'budgets': {'px_total': 200000, 'organism_elements': 500, 'heart_elements': 800, 'px': 0},
    }

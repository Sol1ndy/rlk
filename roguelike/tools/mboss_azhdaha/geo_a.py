"""S2-A: P1 chin slam, P2 jump slam, P3 charge, P4 back spikes (plan.md 5 rows P1-P4 + Change note 1; s2.md 2.1, 10, 17,
18). Writes AZ:p/{chin,jump,charge,spikes}/** only.

Telegraph rule (plan Change note 1, the 10-20 user rule): only the P4 spike landings keep a ground decal (the zig-zag
crack ring tele/disc r 1.6, 14 t before each landing); every other hazard here is quiet and drawn by nothing before its
hit: the readable tell is the clip pose + its sound (P1 rear-up and roar, P2 take-off, P3 coil and growl) or the visible
prop (P4 the planted spikes glowing from t64). Every hit has its impact visual on the hit tick.

Clocks: the main-slot pattern clock #azPT = the clip tick (s2.md 3); lead patterns (P1 8 t, P3 10 t) start at -lead and
the core pre-turns <= 4 deg/t meanwhile. Ticks below are played clip ticks read from the manifest where the clip names
them (impact, takeoff, land, wave2, launch).

Host side of the addon points (s2.md 10, api.ADDON_POINTS): chin/impact at 23 (P1), jump/land at 9 and jump/wave2 at 20
(P2), each called at event - 12 at the context point / rotation with the context scores set.
"""
from . import api as A
from . import h_pa as H

L = A.L
NS = A.NS
BODY = A.BODY
PLAYER = A.PLAYER
CY = L.num(float(A.CY))
KB_HEAVY = A.KB['heavy']

# ------------------------------------------------------------------------------------------------ P1 chin slam
P1 = dict(lead=8, roar=8, track=(0, 10), lock=10, impact=A.ev('chin_slam', 'impact'), disc_r=5.0, sect_r=5.6, sect_a=30,
          f_min=5.5, f_max=7.5, cone=30, release=36, end=A.clip_len('chin_slam'))
P1['tell'] = P1['impact'] - P1['lock']                                     # 25
assert P1['impact'] == 35 and P1['end'] == 65 and P1['tell'] == 25
assert A.ev('chin_slam', 'rear') == 14

# ------------------------------------------------------------------------------------------------ P2 jump slam
P2 = dict(lock=1, takeoff=A.ev('jump_slam', 'takeoff'), land=A.ev('jump_slam', 'land'), wave2=A.ev('jump_slam', 'wave2'),
          disc_r=4.5, r0=3.0, r1=10.5, spd=1.5, band=2.5, low=0.7, apex=3.0, short=3.0, tmin=4.0, tmax=14.0,
          w2_made=12, release=33, end=A.clip_len('jump_slam'), turn=6)
P2['tell'] = P2['land'] - P2['lock']                                       # 20
P2['w2_tell'] = P2['wave2'] - P2['w2_made']                                # 20
P2['air'] = P2['land'] - P2['takeoff']                                     # 15 (mv/leap t6 -> 21)
assert (P2['takeoff'], P2['land'], P2['wave2'], P2['end']) == (6, 21, 32, 53)

# ------------------------------------------------------------------------------------------------ P3 charge
P3 = dict(lead=10, track=(0, 14), made=12, launch=A.ev('charge_coil', 'launch'), run_max=24, spd=1.0, disc_r=4.0,
          disc_f=2.5, stop_len=A.clip_len('charge_stop'), skid=(0.5, 0.4, 0.3, 0.2, 0.1), skid_turn=3, skid_turn_n=9)
P3['tell'] = P3['launch'] - P3['made']                                     # 12
P3['act'] = P3['run_max'] + 2
assert P3['launch'] == 24 and P3['stop_len'] == 21 and A.ev('charge_stop', 'stop') == 8
assert P3['skid_turn'] * P3['skid_turn_n'] <= 30                           # skid yaw <= 30 degrees (plan 3.2)

# ------------------------------------------------------------------------------------------------ P4 back spikes
P4 = dict(launch=A.ev('spikes', 'launch'), gold_off=A.ev('spikes', 'gold_off'), pts=18, land=(46, 51, 54, 59), mark=14,
          fall=4, glow=64, blast=(76, 79, 82, 85), end=90, r_land=1.6, r_blast=2.5, lead_v=28, step=(4.0, 8.0),
          v_min=80, clamp=27.0, head_step=3.0, fall_h=8.0, up=(15, 22), up_dy=2.0, release=86)
assert P4['launch'] == 14 and P4['gold_off'] == 22
LAUNCH_PTS = [A.anchor('spikes', 'launch', f'launch_{k}') for k in (1, 2, 3, 4)]
PT_TAGS = ('rlk_mb_az_p4a', 'rlk_mb_az_p4b', 'rlk_mb_az_p4c', 'rlk_mb_az_p4d')   # boss outward: head + 3, the lock, +4, +8
# the planted spike: point first, tilted 15 degrees off vertical (the model stands on its base, tip up: turned 165
# degrees about x and lifted, so the tip sinks 0.2 b into the floor), 2.5 b
SPIKE_TR = ('{translation:[0f,2.2f,0f],left_rotation:[0.9914f,0f,0f,0.1305f],scale:[2.5f,2.5f,2.5f],'
            'right_rotation:[0f,0f,0f,1f]}')

P4_W = {'head_near': 2, 'head_mid': 3, 'head_far': 3, 'flank_near': 2, 'flank_far': 2, 'tail_lane': 2, 'tail_off': 2, 'paw': 1}
PATTERNS = [
    A.Pattern(1, 'chin', '갈라지는 봉인의 땅', 'normal', 'chin_slam', lead=P1['lead'], recover=18, max_len=80, length=P1['end'],
              weight={'head_near': 4, 'head_mid': 2, 'paw': 2}, gates=('field_area',)),
    A.Pattern(2, 'jump', '바위 분쇄 충돌', 'normal', 'jump_slam', recover=16, max_len=70, length=P2['end'],
              weight={'head_near': 1, 'head_mid': 3, 'head_far': 3, 'flank_near': 1, 'flank_far': 2, 'tail_lane': 1,
                      'tail_off': 2, 'paw': 1}, gates=('field_area',)),
    A.Pattern(3, 'charge', '바위 용왕의 돌진', 'normal', 'charge_coil', lead=P3['lead'], recover=30, max_len=90, length=71,
              weight={'head_mid': 1, 'head_far': 5}, gates=('front35',)),
    A.Pattern(4, 'spikes', '천동만상', 'normal', 'spikes', phases=(1, 2), recover=20, max_len=100, length=P4['end'], weight=P4_W,
              hooks=('resume',)),
]


def _ctx(g, point, grp, t_event, yaw_from_ctx=True):
    """The addon call (s2.md 10.1): the context scores, the context marker here (x/ctx), the int world yaw read back
    from it, then the core dispatcher. Runs positioned / rotated as the context."""
    lines = g.addon(point)
    return ([f'scoreboard players operation #azCtxGrp mb = {grp} mb', 'scoreboard players set #azCtxSide mb 1',
             'scoreboard players set #azCtxPaw mb 1', 'scoreboard players set #azCtxA0 mb 0',
             'scoreboard players set #azCtxA1 mb 0', f'scoreboard players set #azCtxT mb {int(t_event)}', lines[0],
             'execute store result score #azCtxYaw mb run data get entity '
             '@e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] Rotation[0]'] + lines[1:])


def _fxg(g, name, **a):
    """A kit element-family preset in the ground element (runtime #azE)."""
    return g.fxe(name, 'ground', **a)


# ================================================================================================ P1
def emit_chin(g):
    key, tag, ti = 'chin', 'rlk_mb_az_p1', 'rlk_mb_az_p1i'
    tl = A.TL(g, key)
    for t in range(P1['track'][0], P1['track'][1] + 1):
        tl.at(t, 'function rlk:mboss/mv/turn {max:4}')
    tl.at(P1['roar'], g.snd('chin_rear'))
    tl.at(P1['lock'], g.fn(f'p/{key}/lock'), f'{H.at_m(ti)} run {g.fn(f"p/{key}/hz")}')
    tl.at(P1['impact'] - A.ADDON_LEAD, f'{H.at_m(ti)} run {g.fn(f"p/{key}/ax")}')
    tl.at(P1['impact'], f'{H.at_m(ti)} run {g.fn(f"p/{key}/fx")}')
    tl.at(P1['impact'] + 1, f'{H.at_m(ti)} run {g.fn(f"p/{key}/fx2")}')
    tl.at(P1['release'], g.release())
    tl.at(P1['end'], f'kill @e[tag={tag}]', g.end())
    # the impact point: on the line to the player when the player is inside the head's +-30 degree cone (the body has
    # tracked it through t10), else on the facing axis; the distance from the anchor clamped to 5.5-7.5 b
    step = []
    for mb in (1024, 512, 256, 128, 64, 32, 16, 8):              # greedy: within 8 mb of the clamped distance
        step += [f'execute if score #aq1D mb matches {mb}.. as {H.sel_m(ti)} at @s rotated as @s run tp @s ^ ^ ^{mb / 1000:g}',
                 f'execute if score #aq1D mb matches {mb}.. run scoreboard players remove #aq1D mb {mb}']
    g.pw(key, 'lock', [
        '# @s = body (t10): lock the impact point (plan 5 P1): marker rlk_mb_az_p1i, rotated along the crack line',
        '# (anchor -> impact). mv/local gives the player in the anchor frame (mb).',
        f'kill @e[type=minecraft:marker,tag={ti}]',
        H.marker((tag, ti)),
        A.fw('mv/local'),
        'scoreboard players set #aq1C mb 0',
        'scoreboard players operation #aq1S mb = #mbLs mb',
        'scoreboard players set #aq1K mb -1',
        'execute if score #aq1S mb matches ..-1 run scoreboard players operation #aq1S mb *= #aq1K mb',
        'scoreboard players set #aq1K mb 1000', 'scoreboard players operation #aq1S mb *= #aq1K mb',
        'scoreboard players operation #aq1T mb = #mbLf mb',
        f'scoreboard players set #aq1K mb {int(round(1000 * 0.57735))}', 'scoreboard players operation #aq1T mb *= #aq1K mb',
        '# inside the cone: f >= 1 b and |s| <= f tan 30',
        'execute if score #mbLf mb matches 1000.. if score #aq1S mb <= #aq1T mb run scoreboard players set #aq1C mb 1',
        '# the distance: d ~ f + s^2 / 2f in the cone (1 % at 30 degrees), f on the axis; clamped 5.5 .. 7.5 b',
        'scoreboard players operation #aq1D mb = #mbLf mb',
        f'execute if score #aq1C mb matches 1 run {g.fn(f"p/{key}/dist")}',
        f'execute if score #aq1D mb matches ..{int(P1["f_min"] * 1000)} run scoreboard players set #aq1D mb {int(P1["f_min"] * 1000)}',
        f'execute if score #aq1D mb matches {int(P1["f_max"] * 1000)}.. run scoreboard players set #aq1D mb {int(P1["f_max"] * 1000)}',
        f'scoreboard players remove #aq1D mb {int(P1["f_min"] * 1000)}',
        f'execute if score #aq1C mb matches 1 as {H.sel_m(ti)} at @s facing entity {PLAYER} feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0',
        f'execute if score #aq1C mb matches 0 as {H.sel_m(ti)} at @s rotated as {BODY} rotated ~ 0 run tp @s ~ ~ ~ ~ 0',
        f'execute as {H.sel_m(ti)} at @s rotated as @s run tp @s ^ ^ ^{L.num(P1["f_min"])}'] + step)
    g.pw(key, 'dist', ['# d = f + s^2 / (2 f) (mb; f >= 1000 here)',
                       'scoreboard players operation #aq1T mb = #mbLs mb', 'scoreboard players operation #aq1T mb *= #mbLs mb',
                       'scoreboard players operation #aq1U mb = #mbLf mb', 'scoreboard players operation #aq1U mb += #mbLf mb',
                       'scoreboard players operation #aq1T mb /= #aq1U mb', 'scoreboard players operation #aq1D mb += #aq1T mb'])
    hz = g.hz_opts(grp=True, kb=KB_HEAVY, kbdir=0)
    g.pw(key, 'hz', [
        f'# At the impact point, rotated along the crack line (t{P1["lock"]}): disc r {P1["disc_r"]} + sector r {P1["sect_r"]} /',
        f'# +-{P1["sect_a"]} deg forward (the cracks), one volley group, {A.DMG["p1"]} %, heavy KB away, ground element; quiet: no',
        f'# decal (Change note 1: the rear-up + roar is the tell); hit t{P1["impact"]} (internal tell {P1["tell"]}).',
        g.GRP_NEW, 'scoreboard players operation #aq1G mb = #mbGrp mb']
        + hz + g.el_ground() + [L.hz_disc(P1['disc_r'], P1['tell'], A.DMG['p1']), g.tag_last_hz('rlk_mb_az_p1h')]
        + hz + g.el_ground() + [L.hz_sector(P1['sect_r'], P1['sect_a'], P1['tell'], A.DMG['p1']), g.tag_last_hz('rlk_mb_az_p1h')])
    g.pw(key, 'ax', ['# At the impact point, rotated along the crack line: the chin/impact addon point (E 35, call 23).']
         + _ctx(g, 'chin/impact', '#aq1G', P1['impact']))
    g.pw(key, 'fx', ['# The impact visual (t35) at the impact point: blade crown, crack fan, sound, flash (the dust ring follows',
                     '# 1 t later: one tick of four card presets passed the 3000-command perf budget).']
         + _fxg(g, 'crown') + _fxg(g, 'cracks', r=P1['sect_r']) + [g.snd('chin_impact'), g.khud('flash_amber')])
    g.pw(key, 'fx2', ['# t36 at the impact point: the dust ring of the impact.'] + _fxg(g, 'dust_ring', r=P1['disc_r']))
    tl.write([f'# P1 chin slam (plan 5 P1): pre-turn {P1["lead"]} t (the core), tracking to t10, lock + hazards t10, addon t23,',
              f'# impact t{P1["impact"]}, end {P1["end"]}. Starts at #azPT -{P1["lead"]}.', f'kill @e[tag={tag}]',
              'scoreboard players set #aq1G mb 0'],
             ['# P1 tick (#azPT = the chin_slam clip tick)'], t0=-P1['lead'])
    g.pw(key, 'cancel', ['# P1 cut (any executor): its markers go; its hazards are the framework\'s.', f'kill @e[tag={tag}]'])


# ================================================================================================ P2
def emit_jump(g):
    key, tag, tl_ = 'jump', 'rlk_mb_az_p2', 'rlk_mb_az_p2l'
    tl = A.TL(g, key)
    sub = H.Sub(g, key, 'l')
    # t1: the landing point and the landing hazards (disc + front, one group)
    tl.at(P2['lock'], g.fn(f'p/{key}/lock'))
    sub.at(P2['lock'], g.GRP_NEW, 'scoreboard players operation #aq2G1 mb = #mbGrp mb',
           *g.hz_opts(grp=True, y1=P2['low']), *g.el_ground(),
           L.hz_disc(P2['disc_r'], P2['tell'], A.DMG['p2_land']), g.tag_last_hz('rlk_mb_az_p2h'))
    g.wave(sub, P2['land'], P2['r0'], P2['r1'], P2['spd'], P2['band'], P2['tell'], A.DMG['p2_land'], el='ground',
           grp='cur', low=P2['low'], wid=0, tag='rlk_mb_az_p2w0')
    # t12: wave 2 (its own group), from the landing point
    g.wave(sub, P2['wave2'], P2['r0'], P2['r1'], P2['spd'], P2['band'], P2['w2_tell'], A.DMG['p2_wave2'], el='ground',
           grp='new', low=P2['low'], wid=1, tag='rlk_mb_az_p2w1')
    sub.at(P2['w2_made'], 'scoreboard players operation #aq2G2 mb = #mbGrp mb')
    # impact visuals (the fronts' kit ring + front preset come from g.wave 1 t before each strike)
    sub.at(P2['land'], *_fxg(g, 'impact'), *_fxg(g, 'dust_ring', r=P2['disc_r']), g.snd('jump_land'))
    sub.at(P2['wave2'], g.snd('jump_wave2'), g.fx('dust'))
    sub.flush(tl, tl_)
    # take-off, the leap, the landing
    tl.at(P2['takeoff'], g.snd('jump_takeoff'), g.px('jump'), 'scoreboard players set #azLeap mb 1',
          f'execute at {H.sel_m(tl_)} run function rlk:mboss/mv/leap {{t:{P2["air"]},h:{int(round(P2["apex"] * 10))}}}')
    tl.span(P2['takeoff'], P2['land'], 'scoreboard players set #azNoPush mb 1')
    tl.span(P2['takeoff'] + 1, P2['land'] - 1, f'function rlk:mboss/mv/turn {{max:{P2["turn"]}}}')
    tl.at(P2['land'] - A.ADDON_LEAD, f'execute at {H.sel_m(tl_)} facing entity {PLAYER} feet rotated ~ 0 run {g.fn(f"p/{key}/ax_land")}')
    tl.at(P2['wave2'] - A.ADDON_LEAD, f'execute at {H.sel_m(tl_)} facing entity {PLAYER} feet rotated ~ 0 run {g.fn(f"p/{key}/ax_wave2")}')
    tl.at(P2['land'], 'scoreboard players set #azLeap mb 0', g.px('normal'))
    tl.at(P2['release'], g.release())
    tl.at(P2['end'], f'kill @e[tag={tag}]', g.end())
    g.pw(key, 'lock', [
        f'# @s = body (t{P2["lock"]}): the landing point (plan 5 P2): from the anchor toward the player\'s feet, travel',
        f'# clamp(dist - {P2["short"]:g}, {P2["tmin"]:g}, {P2["tmax"]:g}) b (0.5-b steps), then pulled into the body disc r {A.BODY_R:g}.',
        f'kill @e[type=minecraft:marker,tag={tl_}]', H.marker((tag, tl_)),
        f'execute as {H.sel_m(tl_)} at @s facing entity {PLAYER} feet rotated ~ 0 run tp @s ^ ^ ^{P2["tmin"]:g} ~ 0',
        'scoreboard players set #aq2N mb 0',
        f'execute as {H.sel_m(tl_)} at @s run {g.fn(f"p/{key}/lstep")}',
        f'execute as {H.sel_m(tl_)} run {g.clamp_body()}'])
    nmax = int(round((P2['tmax'] - P2['tmin']) / 0.5))
    g.pw(key, 'lstep', [
        f'# @s = the landing marker: one 0.5-b step along its yaw while the player is > {P2["short"]:g} b ahead (<= {nmax} steps).',
        f'execute if entity @e[tag=rlk_body,distance=..{P2["short"]:g}] run return 0',
        'scoreboard players add #aq2N mb 1', f'execute if score #aq2N mb matches {nmax + 1}.. run return 0',
        'execute rotated as @s positioned ^ ^ ^0.5 run tp @s ~ ~ ~',
        f'execute at @s run {g.fn(f"p/{key}/lstep")}'])
    g.pw(key, 'ax_land', ['# At the landing point, rotated toward the player: the jump/land addon point (E 21, call 9).']
         + _ctx(g, 'jump/land', '#aq2G1', P2['land']))
    g.pw(key, 'ax_wave2', ['# At the landing point (the anchor), rotated toward the player: jump/wave2 (E 32, call 20).']
         + _ctx(g, 'jump/wave2', '#aq2G2', P2['wave2']))
    tl.write(['# P2 jump slam (plan 5 P2): lock t1, take-off t6, land t21 (+ front), wave 2 t32, end 53.', f'kill @e[tag={tag}]',
              'scoreboard players set #aq2G1 mb 0', 'scoreboard players set #aq2G2 mb 0'],
             ['# P2 tick (#azPT = the jump_slam clip tick)'], t0=0)
    g.pw(key, 'cancel', [
        '# P2 cut (any executor; selectors): markers, a leap in the air (the body back on the floor), the jump proxy state',
        '# (not while dying: the framework set the proxies dead). A kit front ring already drawn runs out by itself (<= 9 t,',
        '# like the front preset; pause / death / test cut clear the kit telegraphs; wire F5 allows no tele/wave_end).',
        f'kill @e[tag={tag}]',
        f'execute if score #azLeap mb matches 1 as {BODY} run function rlk:mboss/mv/stop',
        f'execute if score #azLeap mb matches 1 as {BODY} at @s run tp @s ~ {CY} ~',
        f'execute if score #azPx mb matches 1 unless score #mbSt mb matches 2 run {g.px("normal")}',
        'scoreboard players set #azLeap mb 0'])


# ================================================================================================ P3
def emit_charge(g):
    key, th = 'charge', 'rlk_mb_az_p3h'
    tl = A.TL(g, key)
    tl.at(0, g.snd('charge_growl'))
    for t in range(P3['track'][0], P3['track'][1] + 1):
        tl.at(t, 'function rlk:mboss/mv/turn {max:4}')
    tl.at(P3['made'], g.fn(f'p/{key}/hz'))
    for t in range(P3['made'] + 1, P3['track'][1] + 1):          # the disc follows the last tracking turns the same tick
        tl.at(t, g.fn(f'p/{key}/follow'))
    tl.at(P3['launch'], 'scoreboard players set #aq3R mb 1', 'scoreboard players set #aq3N mb 0', g.fn(f'p/{key}/run'),
          g.fn(f'p/{key}/follow'))
    front = f'at @s rotated as @s rotated ~ 0 positioned ^ ^ ^{L.num(P3["disc_f"])}'   # at @s: the body moved this tick
    g.pw(key, 'hz', [
        f'# @s = body (t{P3["made"]}): the charge hit, a disc r {P3["disc_r"]:g} on the body front (f {P3["disc_f"]:g}), moved onto the',
        f'# body every tick (plain tp); strike at the launch t{P3["launch"]} (internal tell {P3["tell"]}), active for the run;',
        f'# one hit; {A.DMG["p3"]} %, Geo in every phase, heavy KB away; quiet: no lane decal (Change note 1: coil + growl).',
        f'kill @e[type=minecraft:marker,tag={th}]']
        + g.hz_opts(act=P3['act'], kb=KB_HEAVY, kbdir=0) + g.el(5)
        + [f'execute {front} run {L.hz_disc(P3["disc_r"], P3["tell"], A.DMG["p3"])}', g.tag_last_hz(th),
           'scoreboard players set #aq3H mb 1', 'scoreboard players set #aq3X mb 0'])
    g.pw(key, 'follow', [
        '# @s = body: the hit disc onto the body front; its first touch (hit or dash) shows the contact impact once.',
        f'execute {front} as @e[type=minecraft:marker,tag={th}] run tp @s ~ ~ ~ ~ 0',
        f'execute unless score #aq3X mb matches 1 as @e[type=minecraft:marker,tag={th}] if score @s mbHzHit matches 1 '
        f'at {PLAYER} positioned ~ {CY} ~ run {g.fn(f"p/{key}/contact")}'])
    g.pw(key, 'contact', ['# At the player\'s floor point: the body contact impact (once).', 'scoreboard players set #aq3X mb 1']
         + [A.K.fxe('impact', 5), L.sound('entity.ravager.attack', 1.0, 0.6), L.sound('entity.generic.explode', 0.6, 0.9)])
    g.pw(key, 'run', [
        f'# @s = body: one run tick: 1 b forward along the locked line while the next anchor stays inside r {A.CHARGE_R:g}',
        f'# of the arena centre, at most {P3["run_max"]} ticks; dust + gallop every 4 t; no body push.',
        'scoreboard players set #azNoPush mb 1', 'scoreboard players add #aq3N mb 1', 'scoreboard players set #aq3M mb 0',
        f'execute store success score #aq3M mb at @s rotated as @s rotated ~ 0 positioned ^ ^ ^{L.num(P3["spd"])} positioned ~ {CY} ~ '
        f'if entity {A.ARENA_M.replace("limit=1", f"distance=..{L.num(A.CHARGE_R)},limit=1")} run tp @s ~ ~ ~',
        f'execute if score #aq3M mb matches 0 run return run {g.fn(f"p/{key}/stop")}',
        'scoreboard players operation #azM mb = #aq3N mb', 'scoreboard players operation #azM mb %= #azK4 mb',
        f'execute if score #azM mb matches 1 at @s run {g.snd("charge_gallop")}',
        f'execute if score #azM mb matches 1 at @s run {g.fx("dust_trail")}',
        f'execute if score #aq3N mb matches {P3["run_max"]}.. run return run {g.fn(f"p/{key}/stop")}'])
    g.pw(key, 'stop', [
        f'# @s = body: the run ends (lane end / r {A.CHARGE_R:g} / {P3["run_max"]} t): the hit goes, charge_stop ({P3["stop_len"]} t), the',
        '# skid (decelerating slide, turn <= 30 deg), the end tick; the dangerous part is over (release).',
        'scoreboard players set #aq3R mb 0', 'scoreboard players set #aq3K mb 1', 'scoreboard players set #aq3H mb 0',
        f'execute as @e[type=minecraft:marker,tag={th}] at @s rotated as @s run function rlk:mboss/hz/expire',
        'scoreboard players operation #aq3E mb = #azPT mb', f'scoreboard players add #aq3E mb {P3["stop_len"]}',
        'scoreboard players operation #azPLen mb = #aq3E mb',
        g.play('charge_stop'), f'execute at @s run {g.fx("skid")}', f'execute at @s run {g.snd("charge_skid")}', g.release()])
    skid = ['# @s = body: the skid after the stop (charge_stop 0..8): a decelerating slide inside the charge disc and a',
            f'# turn of <= {P3["skid_turn"]} deg/t toward the player for {P3["skid_turn_n"]} t; no body push.',
            'scoreboard players add #aq3K mb 1']
    for k, d in enumerate(P3['skid'], 2):
        skid.append(f'execute if score #aq3K mb matches {k} at @s rotated as @s rotated ~ 0 positioned ^ ^ ^{L.num(d)} positioned ~ {CY} ~ '
                    f'if entity {A.ARENA_M.replace("limit=1", f"distance=..{L.num(A.CHARGE_R)},limit=1")} run tp @s ~ ~ ~')
    skid += [f'execute if score #aq3K mb matches 2..{1 + P3["skid_turn_n"]} run function rlk:mboss/mv/turn {{max:{P3["skid_turn"]}}}',
             f'execute if score #aq3K mb matches ..{1 + A.ev("charge_stop", "stop")} run scoreboard players set #azNoPush mb 1',
             f'execute if score #aq3K mb matches {2 + P3["skid_turn_n"]}.. run scoreboard players set #aq3K mb 0']
    g.pw(key, 'skid', skid)
    extra = [f'execute if score #aq3R mb matches 1 run {g.fn(f"p/{key}/run")}',
             f'execute if score #aq3K mb matches 1.. run {g.fn(f"p/{key}/skid")}',
             f'execute if score #aq3H mb matches 1 run {g.fn(f"p/{key}/follow")}',
             f'execute if score #aq3E mb matches 1.. if score #azPT mb >= #aq3E mb run {g.end()}']
    tl.write([f'# P3 charge (plan 5 P3): pre-turn {P3["lead"]} t (the core), growl + coil, tracking to t14 (the lane locks), the hit',
              f'# made t{P3["made"]}, launch t{P3["launch"]}, run <= {P3["run_max"]} t at 1 b/t, charge_stop {P3["stop_len"]} t. Starts at #azPT -{P3["lead"]}.',
              f'kill @e[type=minecraft:marker,tag={th}]'] + [f'scoreboard players set #aq3{x} mb 0' for x in 'RNHKEX'],
             ['# P3 tick (#azPT = the charge_coil clip tick; the coil chains into charge_run by itself)'],
             t0=-P3['lead'], extra_tick=extra)
    g.pw(key, 'cancel', ['# P3 cut (any executor): the hit disc and the run / skid / end state.',
                         f'kill @e[type=minecraft:marker,tag={th}]'] + [f'scoreboard players set #aq3{x} mb 0' for x in 'RNHKEX'])


# ================================================================================================ P4
def _redraw_tell(g, el, shape, **args):
    """ktele with the tell taken at runtime from #aq4R (the resume redraw: the remaining ticks)."""
    lines = g.ktele(shape, el, **args)
    return lines[:-1] + ['execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq4R mb', lines[-1]]


def emit_spikes(g):
    key, tag = 'spikes', 'rlk_mb_az_p4'
    tl = A.TL(g, key)
    back = A.REST['back']
    at_back = f'execute rotated as @s rotated ~ 0 positioned ^{L.num(back[0])} ^{L.num(back[1])} ^{L.num(back[2])} run '
    # t0: bristle (the clip glows the gold parts 0..22 by itself), t14: launch
    tl.at(0, at_back + g.fx('gold_plume'), g.snd('spikes_bristle'))
    up = []
    for k, (x, y, z) in enumerate(LAUNCH_PTS, 1):
        up += [f'execute rotated as @s rotated ~ 0 positioned ^{L.num(x)} ^{L.num(y)} ^{L.num(z)} run summon minecraft:item_display ~ ~ ~ '
               f'{{Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","{tag}","rlk_mb_az_p4up","rlk_mb_az_p4n"],teleport_duration:1}}']
    up += [f'execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p4n] run {A.K.prope("spike", 5)}',
           'tag @e[type=minecraft:item_display,tag=rlk_mb_az_p4n] remove rlk_mb_az_p4n']
    tl.at(P4['launch'], *up, at_back + g.fx('gold_plume'), g.snd('spikes_launch'))
    tl.span(P4['up'][0], P4['up'][1], f'execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p4up] at @s run tp @s ~ ~{L.num(P4["up_dy"])} ~')
    tl.at(P4['up'][1] + 1, 'kill @e[type=minecraft:item_display,tag=rlk_mb_az_p4up]')
    tl.at(P4['pts'], g.fn(f'p/{key}/pts'))
    # the landings: the kept crack-ring decal + the hazard 14 t before, the falling shard 4 t before, the planted spike
    for k, (tp, tl_k) in enumerate(zip(PT_TAGS, P4['land'])):
        made = tl_k - P4['mark']
        grp = [g.GRP_NEW, 'scoreboard players operation #aq4G mb = #mbGrp mb'] if k == 0 else []
        g.pw(key, f'land{k}', [f'# At point {k + 1} (t{made}): the landing ring (kept decal, Change note 1) + its hazard, one group.'] + grp
             + g.hz_opts() + ['scoreboard players operation #hzGrp mb = #aq4G mb'] + g.el_ground()
             + [L.hz_disc(P4['r_land'], P4['mark'], A.DMG['p4_land']), g.tag_last_hz('rlk_mb_az_p4h')]
             + g.ktele('disc', 'ground', r=P4['r_land'], tell=P4['mark'], nd=0, hold=3))
        tl.at(made, f'{H.at_m(tp)} run {g.fn(f"p/{key}/land{k}")}')
        tl.at(tl_k - P4['fall'], f'{H.at_m(tp)} run {g.fx("shard_fall", h=P4["fall_h"])}')
        g.pw(key, f'plant{k}', [f'# At point {k + 1} (t{tl_k}): the landing burst and the planted spike.']
             + _fxg(g, 'impact') + [g.snd('spikes_land'),
                                    f'summon minecraft:item_display ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","{tag}",'
                                    f'"rlk_mb_az_p4s","rlk_mb_az_p4s{k}","rlk_mb_az_p4n"]}}',
                                    f'execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p4n] run {A.K.prope("spike", 5)}',
                                    f'execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p4n] at @s rotated ~{37 * k + 20} 0 run tp @s ~ ~ ~ ~ 0',
                                    f'data merge entity @e[type=minecraft:item_display,tag=rlk_mb_az_p4n,limit=1] {{transformation:{SPIKE_TR}}}',
                                    'tag @e[type=minecraft:item_display,tag=rlk_mb_az_p4n] remove rlk_mb_az_p4n'])
        tl.at(tl_k, f'{H.at_m(tp)} run {g.fn(f"p/{key}/plant{k}")}')
    # t64: the planted spikes glow (the tell of the bursts) and the burst hazards (one group) are made
    blast = [g.GRP_NEW]
    for tp, tb in zip(PT_TAGS, P4['blast']):
        blast += g.hz_opts(grp=True) + g.el_ground() + [
            f'{H.at_m(tp)} run {L.hz_disc(P4["r_blast"], tb - P4["glow"], A.DMG["p4_blast"])}', g.tag_last_hz('rlk_mb_az_p4x')]
    g.pw(key, 'blast', [f'# @s = body (t{P4["glow"]}): the four burst hazards r {P4["r_blast"]:g} (one group, {A.DMG["p4_blast"]} %), quiet: no decal',
                        '# (Change note 1: the planted spikes\' veins glow from here, boss outward).'] + blast)
    tl.at(P4['glow'], g.fn(f'p/{key}/blast'),
          'execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p4s] run ' + L.sound('block.respawn_anchor.charge', 0.8, 1.3),
          'execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p4s] run ' + L.sound('block.amethyst_block.resonate', 1.0, 0.7))
    glow = ['execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p4s] run '
            + g.dust((255, 196, 64), 1.6, '~ ~1.1 ~', (0.25, 0.7, 0.25), 4),
            'execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p4s] run ' + g.particle('wax_on', '~ ~1.2 ~', (0.3, 0.6, 0.3), 0, 2)]
    for t in range(P4['glow'], P4['blast'][-1], 2):
        tl.at(t, *glow)
    for k, (tp, tb) in enumerate(zip(PT_TAGS, P4['blast'])):
        g.pw(key, f'burst{k}', [f'# At point {k + 1} (t{tb}): the planted spike bursts (crystal-blade crown in the ground element).']
             + _fxg(g, 'crown') + [g.snd('spikes_explode'), g.particle('block{block_state:"minecraft:raw_gold_block"}', '~ ~1 ~', (0.6, 0.8, 0.6), 0.1, 18),
                                   f'kill @e[type=minecraft:item_display,tag=rlk_mb_az_p4s{k}]'])
        tl.at(tb, f'{H.at_m(tp)} run {g.fn(f"p/{key}/burst{k}")}')
    tl.at(P4['release'], g.release())
    tl.at(P4['end'], f'kill @e[tag={tag}]', g.end())
    # t18: the four points
    c = g.clamp_body(P4['clamp'])
    g.pw(key, 'pts', [
        f'# @s = body (t{P4["pts"]}): the four spike points (plan 5 P4), clamped inside r {P4["clamp"]:g}: B = lockv (lead {P4["lead_v"]}),',
        f'# A = the head column + {P4["head_step"]:g} b toward B, C / D = B + {P4["step"][0]:g} / {P4["step"][1]:g} b along the player\'s velocity',
        f'# (|v| > {P4["v_min"]} mb/t) else along head -> B.',
        *g.lockv(P4['lead_v']), *g.keep(PT_TAGS[1]),
        f'tag @e[type=minecraft:marker,tag={PT_TAGS[1]}] add {tag}', f'tag @e[type=minecraft:marker,tag={PT_TAGS[1]}] add rlk_mb_az_pat',
        f'execute as {H.sel_m(PT_TAGS[1])} run {c}',
        f'kill @e[type=minecraft:marker,tag=rlk_mb_az_p4t]',
        f'execute rotated as @s rotated ~ 0 positioned ^ ^ ^{L.num(A.P_HEAD_COL[2])} run ' + H.marker((tag, 'rlk_mb_az_p4t', 'rlk_mb_az_p4hd')),
        f'execute at {H.sel_m("rlk_mb_az_p4hd")} facing entity {H.sel_m(PT_TAGS[1])} feet rotated ~ 0 positioned ^ ^ ^{L.num(P4["head_step"])} run '
        + H.marker((tag, PT_TAGS[0])),
        f'execute at {H.sel_m(PT_TAGS[1])} run ' + H.marker((tag, 'rlk_mb_az_p4t', 'rlk_mb_az_p4dir'), '~ ~ ~'),
        f'execute if score #mbV mb matches {P4["v_min"] + 1}.. run {g.fn(f"p/{key}/vdir")}',
        f'execute unless score #mbV mb matches {P4["v_min"] + 1}.. as {H.sel_m("rlk_mb_az_p4dir")} at @s facing entity '
        f'{H.sel_m("rlk_mb_az_p4hd")} feet rotated ~180 0 run tp @s ~ ~ ~ ~ 0',
        f'execute at {H.sel_m("rlk_mb_az_p4dir")} rotated as {H.sel_m("rlk_mb_az_p4dir")} positioned ^ ^ ^{L.num(P4["step"][0])} run '
        + H.marker((tag, PT_TAGS[2])),
        f'execute at {H.sel_m("rlk_mb_az_p4dir")} rotated as {H.sel_m("rlk_mb_az_p4dir")} positioned ^ ^ ^{L.num(P4["step"][1])} run '
        + H.marker((tag, PT_TAGS[3])),
        *[f'execute as {H.sel_m(t)} run {c}' for t in (PT_TAGS[0], PT_TAGS[2], PT_TAGS[3])],
        'kill @e[type=minecraft:marker,tag=rlk_mb_az_p4t]'])
    g.pw(key, 'vdir', [
        '# The direction marker along the player\'s velocity (#mbVx #mbVz mb/t from mv/lockv): it faces B + 20 v.',
        f'execute at {H.sel_m(PT_TAGS[1])} run ' + H.marker((tag, 'rlk_mb_az_p4t', 'rlk_mb_az_p4v'), '~ ~ ~'),
        f'execute store result score #aq4X mb run data get entity {H.sel_m(PT_TAGS[1])} Pos[0] 1000',
        f'execute store result score #aq4Z mb run data get entity {H.sel_m(PT_TAGS[1])} Pos[2] 1000',
        'scoreboard players set #aq4K mb 20',
        'scoreboard players operation #aq4T mb = #mbVx mb', 'scoreboard players operation #aq4T mb *= #aq4K mb',
        'scoreboard players operation #aq4X mb += #aq4T mb',
        'scoreboard players operation #aq4T mb = #mbVz mb', 'scoreboard players operation #aq4T mb *= #aq4K mb',
        'scoreboard players operation #aq4Z mb += #aq4T mb',
        f'execute store result entity {H.sel_m("rlk_mb_az_p4v")} Pos[0] double 0.001 run scoreboard players get #aq4X mb',
        f'execute store result entity {H.sel_m("rlk_mb_az_p4v")} Pos[2] double 0.001 run scoreboard players get #aq4Z mb',
        f'execute as {H.sel_m("rlk_mb_az_p4dir")} at @s facing entity {H.sel_m("rlk_mb_az_p4v")} feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0'])
    rs = ['# Hook resume (@s = body): the kit cleared every attack decal at the pause; the landing rings still ahead are',
          '# redrawn with the ticks they have left (the clock and the hazards were frozen with the fight).']
    for k, (tp, tl_k) in enumerate(zip(PT_TAGS, P4['land'])):
        g.pw(key, f'redraw{k}', [f'scoreboard players set #aq4R mb {tl_k}', 'scoreboard players operation #aq4R mb -= #azPT mb']
             + _redraw_tell(g, 'ground', 'disc', r=P4['r_land'], tell=P4['mark'], nd=0, hold=3))
        rs.append(f'execute if score #azPT mb matches {tl_k - P4["mark"]}..{tl_k - 1} {H.at_m(tp)[len("execute "):]} run '
                  f'{g.fn(f"p/{key}/redraw{k}")}')
    g.pw(key, 'resume', rs)
    tl.write([f'# P4 back spikes (plan 5 P4): bristle t0 (gold 0..22 by the clip), launch t14, points t18, landings '
              f'{"/".join(map(str, P4["land"]))}, glow t{P4["glow"]}, bursts {"/".join(map(str, P4["blast"]))}, end {P4["end"]}.',
              f'kill @e[tag={tag}]', 'scoreboard players set #aq4G mb 0'],
             ['# P4 tick (#azPT = the spikes clip tick)'], t0=0)
    g.pw(key, 'cancel', ['# P4 cut (any executor): markers, launched and planted spikes; the gold glow off.', f'kill @e[tag={tag}]',
                         g.glow(False)])


def emit(g):
    emit_chin(g)
    emit_jump(g)
    emit_charge(g)
    emit_spikes(g)

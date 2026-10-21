"""Q2 종말의 여파 (AP-P3; plan 8.3 Q2, 7.4, 7.8, 9.3, Q3 / Q25; cm.md 13.6 / 13.11; ap_contract 0.8 id 32, kind
scheduled: forced by the core's Q2 schedule) and the 소생의 찬가 domes (AP:dome/**). Writes AP:p/aftermath/** and
AP:dome/** only (api.OWN['aftermath']).

B0 (the pattern start, before anything moves): the real game's banner (kit hud/banner_aftermath, "소생의 찬가 보호막 안으로
들어가서 종말의 여파를 막아내세요" with the red phrase: footage v5 18.2 s, w1) and the three dome footprints (pale rims,
dim until their dome forms) placed around the arena centre from the player's distance d and bearing (plan 7.8): A on the
bearing at 7 b, B on it at max(16, d - 5) (<= 21) when d >= 13 else 120 degrees round at 14 b, C 120 degrees the other
way at 14 b. Then crouch_p3 and, unless the boss is within 2 b of the centre, the crawl to it (walk_p3, 0.4 b/t, <= 50 t);
the aftermath clip from its tick 0 (#apq32 = the clip tick, negative during the approach).

Mechanic (a *mechanic* row of the 10-20 telegraph rule: the field, the domes and their footprints stay): t40 the field
release (kit mask wash filled at t80 + the field ring); pillars t44 / 48 / 52, domes formed t54 / 58 / 62 (marker
rlk_mb_ap_dome + rlk_mb_hzsafe in the cast's safe group, the org models om/dome/*); two mask hazards (FN-14 / FN-15,
Dendro, #hzNoDodge, no reaction): the field ticks 3 % max HP (never lethal) re-arming every 15 t over t80-154 (<= 5),
and the blast 80 % max HP over t156-175 (one hit; the first cast of a fight is never lethal, #apAft1 0, and is followed
by the instant-kill warning TXT['q2_lethal']). Inside a formed dome: no hit, +1 % max HP every 20 t (t54-174). The domes
pop at t189. No cine (the player must act). No-tips rule (user 10-21): the plan's sub-line "보호막이 사라질 때까지
기다리세요" (blast -> pop) is advice the footage does not show: dropped.
"""
from .api import Pattern, Gen, TL, PLAYER, BODY, ARENA_M, K, L
from . import api as A
from .p3 import mdist_lines, marker, m1, mall

NS = A.NS
CY = A.CY
num = L.num
AFT = 'aftermath'
ev = A.ev
WALK = A.P3_CENTRE_WALK
QA = dict(crouch=A.clip_len('crouch_p3'), field=ev(AFT, 'field'), pillars=(ev(AFT, 'pillar1'), ev(AFT, 'pillar2'), ev(AFT, 'pillar3')),
          domes=(ev(AFT, 'dome1'), ev(AFT, 'dome2'), ev(AFT, 'dome3')), ticks=ev(AFT, 'ticks'), rain=ev(AFT, 'rain'),
          blast=ev(AFT, 'blast'), window_end=ev(AFT, 'window_end'), pop=ev(AFT, 'pop'), burst=ev(AFT, 'burst'),
          end=A.clip_len(AFT), whirl=ev(AFT, 'whirl'), dome_r=4.5, field_r=26.0, tick_every=15, heal_every=20,
          near=2.0, turn=12, pop_clip=6)
QA['tick_act'] = QA['blast'] - 1 - QA['ticks']               # 75: t80-154, <= 5 re-armed ticks
QA['blast_act'] = QA['window_end'] - QA['blast']             # 20: t156-175
assert (QA['field'], QA['pillars'], QA['domes'], QA['ticks'], QA['blast'], QA['window_end'], QA['pop'], QA['end']) == \
    (40, (44, 48, 52), (54, 58, 62), 80, 156, 176, 189, 224), QA
assert QA['blast'] - QA['domes'][-1] >= 85                    # every dome stands >= 85 t before the blast (U4)
assert (QA['tick_act'] - 1) // QA['tick_every'] + 1 <= 5     # re-armed hits at t80, 95, 110, 125, 140
PLACE = dict(a=7.0, far=13.0, b_min=16.0, b_back=5.0, b_max=21.0, side=14.0)
HEAL_TICKS = list(range(QA['domes'][0], QA['pop'], QA['heal_every']))   # 54 .. 174
LEN = QA['crouch'] + WALK['max'] + QA['end']
PATTERNS = [
    Pattern(32, 'aftermath', '종말의 여파', 'scheduled', None, phase=3, length=LEN, recover=16, max_len=LEN + 30,
            last_hit=QA['crouch'] + WALK['max'] + QA['window_end']),
]
T_ = 'rlk_mb_ap_p32'
FP = [f'{T_}f{k}' for k in range(3)]                          # the footprints (planned dome centres)
HZ = f'{T_}h'                                                 # the two mask hazards
DOME = 'rlk_mb_ap_dome'
CX, CZ = num(A.CENTRE[0]), num(A.CENTRE[2])
CENTRE = f'positioned {CX} {CY} {CZ}'
HEAD = '# 종말의 여파 (aftermath, id 32; plan 8.3 Q2 / 7.8).'


def mask(pm, tell, act, lethal, rearm=None):
    """A mask hazard here (the cast's safe group #apq32G): pm per mille of max HP, tell, active window."""
    opts = dict(nododge=1, norx=1, pm=pm, act=act)
    if not lethal:
        opts['pm_lethal'] = 0
    if rearm:
        opts['rearm'] = rearm
    return [*Gen.hz_opts(**opts), 'scoreboard players operation #hzSafeG mb = #apq32G mb',
            *L.hz_mask(QA['dome_r'], tell, 1), Gen.tag_last_hz(HZ)]


def emit(g):
    p = PATTERNS[0]
    key = p.key
    F = g.fn
    tl = TL(g, key, clock='#apq32')
    d0 = QA['domes']
    # ---------------------------------------------------------------- B0 + approach
    start = [HEAD, '# B0: the banner, the footprints, the safe group; the approach length n (0 within 2 b of the centre, else',
             f'# ceil(d / 0.4 b) <= {WALK["max"]}); the clip starts at #apPT = 8 + n (#apq32S); the footprint rims dim until each forms.',
             f'kill @e[tag={T_}]', F('dome/clear'),
             L.hz_safe_new(), 'scoreboard players operation #apq32G mb = #mbSafeG mb',
             f'execute at @s run {K.hud("banner_aftermath")}', f'execute at @s run {K.snd("q2_banner")}',
             F(f'p/{key}/place'),
             f'execute at @s run {F(f"p/{key}/dist")}',
             'scoreboard players set #apq32N mb 0',
             f'execute if score #apq32D mb matches {int(QA["near"] * 10) + 1}.. run scoreboard players operation #apq32N mb = #apq32D mb',
             f'execute if score #apq32D mb matches {int(QA["near"] * 10) + 1}.. run scoreboard players add #apq32N mb 3',
             f'execute if score #apq32D mb matches {int(QA["near"] * 10) + 1}.. run scoreboard players operation #apq32N mb /= #apK4 mb',
             f'execute if score #apq32N mb matches {WALK["max"] + 1}.. run scoreboard players set #apq32N mb {WALK["max"]}',
             'scoreboard players operation #apq32S mb = #apq32N mb', f'scoreboard players add #apq32S mb {QA["crouch"]}',
             'scoreboard players operation #apPLen mb = #apq32S mb', f'scoreboard players add #apPLen mb {QA["end"]}',
             'scoreboard players operation #apq32 mb = #apPT mb', 'scoreboard players operation #apq32 mb -= #apq32S mb',
             'scoreboard players operation #apq32H mb = #mbHitEv mb',
             Gen.play('crouch_p3')]
    for k in range(3):
        start += [f'data modify storage rlk:mboss ap.p32.r{k} set value {{id:{k},r:{int(QA["dome_r"] * 10)},tell:1,'
                  f'hold:{QA["pop"] - d0[k]}}}',
                  'scoreboard players operation #apq32X mb = #apq32S mb', f'scoreboard players add #apq32X mb {d0[k]}',
                  f'execute store result storage rlk:mboss ap.p32.r{k}.tell int 1 run scoreboard players get #apq32X mb',
                  f'execute at {m1(FP[k])} run function {K.FN}tele/safe_rim with storage rlk:mboss ap.p32.r{k}']
    g.pw(key, 'dist', ['# @s = body: #apq32D = the horizontal distance to the arena centre in tenths.']
         + mdist_lines(ARENA_M, '#apq32D', '#apq32'))
    g.pw(key, 'place', [
        '# @s = body (B0): the three footprints from the player\'s bearing about the centre (plan 7.8), on the floor.',
        f'kill @e[tag={T_}f]', f'execute {CENTRE} facing entity {PLAYER} feet rotated ~ 0 run {F(f"p/{key}/place_t")}'])
    far = PLAYER.replace('limit=1', f'distance={num(PLACE["far"])}..,limit=1')
    pl21 = PLAYER.replace('limit=1', f'distance={num(PLACE["b_min"] + PLACE["b_back"])}..,limit=1')
    pl26 = PLAYER.replace('limit=1', f'distance={num(PLACE["b_max"] + PLACE["b_back"])}..,limit=1')
    g.pw(key, 'place_t', [
        '# At the centre, rotated = the bearing of the player: A at 7 b; B (far: d >= 13) on the bearing at max(16, d - 5) <= 21,',
        '# (near) 120 degrees clockwise at 14 b; C 120 degrees the other way at 14 b. Centres >= 9 b apart, r <= 21.',
        f'execute positioned ^ ^ ^{num(PLACE["a"])} run {marker(32, f"{T_}f", FP[0])}',
        f'execute if entity {far} unless entity {pl21} positioned ^ ^ ^{num(PLACE["b_min"])} run {marker(32, f"{T_}f", FP[1])}',
        f'execute if entity {pl21} unless entity {pl26} at {PLAYER} facing entity {ARENA_M} feet rotated ~ 0 positioned '
        f'^ ^ ^{num(PLACE["b_back"])} positioned ~ {CY} ~ run {marker(32, f"{T_}f", FP[1])}',
        f'execute if entity {pl26} positioned ^ ^ ^{num(PLACE["b_max"])} run {marker(32, f"{T_}f", FP[1])}',
        f'execute unless entity {far} rotated ~120 0 positioned ^ ^ ^{num(PLACE["side"])} run {marker(32, f"{T_}f", FP[1])}',
        f'execute rotated ~-120 0 positioned ^ ^ ^{num(PLACE["side"])} run {marker(32, f"{T_}f", FP[2])}'])
    # ---------------------------------------------------------------- the clip timeline (#apq32 = the aftermath tick)
    tl.at(0, F(f'p/{key}/go'))
    tl.at(0, f'execute at @s run {K.fx("crouch_splash")}', f'execute at @s run {K.snd("q2_charge")}')
    tl.at(QA['whirl'], f'execute at @s run {K.snd("q2_whirl")}')
    for t in range(QA['whirl'], QA['whirl'] + 19, 3):
        tl.at(t, f'execute at @s run {K.fx("whirl_leaves")}')
    tl.at(QA['field'], F(f'p/{key}/field'))
    for t in range(QA['field'], QA['blast'], 20):
        tl.at(t, f'execute {CENTRE} run {K.snd("q2_field_loop")}')
    for k in range(3):
        tl.at(QA['pillars'][k], f'execute at {m1(FP[k])} run {K.fx("light_pillar")}')
        tl.at(d0[k], f'execute at {m1(FP[k])} run {F(f"p/{key}/form")} {{i:{k}}}')
    for t in HEAL_TICKS:
        tl.at(t, F(f'p/{key}/heal'))
    for t in range(QA['ticks'], QA['ticks'] + QA['tick_act']):
        tl.at(t, f'execute if score #mbHitEv mb > #apq32H mb at {PLAYER} run {K.snd("q2_tick")}',
              'scoreboard players operation #apq32H mb = #mbHitEv mb')
    for t in range(QA['ticks'], QA['blast'], 10):
        tl.at(t, f'execute {CENTRE} run {K.fx("floor_glitter")}')
    tl.at(QA['rain'], f'execute {CENTRE} run {K.snd("q2_rain")}')
    for t in range(QA['rain'], QA['blast'] + 1, 4):
        tl.at(t, f'execute {CENTRE} run {K.fx("beam_rain")}')
    tl.at(QA['blast'], K.hud('flash_white'), f'execute {CENTRE} run {K.fx("flood", life=24)}', f'execute {CENTRE} run {K.snd("q2_blast")}',
          K.hud('banner_end'))
    tl.at(QA['window_end'], Gen.release(),
          f'execute if score #apAft1 mb matches 0 run {Gen.line(A.TXT["q2_lethal"], A.WARN_HEX, 60)}')
    tl.at(QA['pop'], F(f'p/{key}/pop'))
    for k in range(3):
        tl.at(QA['pop'] + k, f'execute at {m1(FP[k])} run {K.fx("dome_pop")}')
    tl.at(QA['burst'], f'execute at @s run {K.fx("green_burst")}')
    tl.at(QA['pop'] + QA['pop_clip'] + 1, f'function {NS}om/dome/kill_all')
    extra = ['scoreboard players operation #apq32 mb = #apPT mb', 'scoreboard players operation #apq32 mb -= #apq32S mb',
             f'execute if score #apq32 mb matches ..-1 if score #apPT mb matches {QA["crouch"]} run {Gen.play("walk_p3")}',
             f'execute if score #apq32 mb matches ..-1 if score #apPT mb matches {QA["crouch"]}.. run {F(f"p/{key}/walk")}',
             f'execute if score #apq32 mb matches {d0[0]}..{QA["pop"] + QA["pop_clip"]} run function {NS}om/dome/tick',
             f'execute if score #apq32 mb matches {QA["end"]}.. run return run {F(f"p/{key}/done")}']
    tl.write(start, [HEAD, '# tick: the approach (#apq32 < 0), the dome models\' clips (om/dome/tick), then the clip timeline.'],
             t0=-1000, extra_tick=extra)
    g.pw(key, 'walk', ['# @s = body (the approach): one 0.4 b step toward the centre and a turn toward it (<= 12 deg/t).',
                       f'execute at @s unless entity {ARENA_M.replace("limit=1", "distance=..0.25,limit=1")} run '
                       f'{Gen.move_to(ARENA_M, WALK["spd"])}',
                       F(f'p/{key}/turn_c')])
    g.pw(key, 'turn_c', [
        '# @s = body: turn toward the arena centre by <= 12 degrees (mboss/mv/turn with the centre as the target).',
        'execute store result score #apq32Y0 mb run data get entity @s Rotation[0] 100',
        f'execute at @s run summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","{T_}","{T_}y"]}}',
        f'execute at @s facing entity {ARENA_M} feet run tp {m1(T_ + "y")} ~ ~ ~ ~ 0',
        f'execute store result score #apq32Y1 mb run data get entity {m1(T_ + "y")} Rotation[0] 100',
        f'kill {mall(T_ + "y")}',
        'scoreboard players operation #apq32Y1 mb -= #apq32Y0 mb', 'scoreboard players add #apq32Y1 mb 90000',
        'scoreboard players operation #apq32Y1 mb %= #c36000 mb', 'scoreboard players remove #apq32Y1 mb 18000',
        f'execute if score #apq32Y1 mb matches {QA["turn"] * 100 + 1}.. run scoreboard players set #apq32Y1 mb {QA["turn"] * 100}',
        f'execute if score #apq32Y1 mb matches ..{-QA["turn"] * 100 - 1} run scoreboard players set #apq32Y1 mb {-QA["turn"] * 100}',
        'scoreboard players operation #apq32Y0 mb += #apq32Y1 mb',
        'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #apq32Y0 mb'])
    g.pw(key, 'go', [f'# @s = body (#apq32 0): at the centre on the floor (yaw kept), the aftermath clip ({QA["end"]} t) from its tick 0.',
                     f'execute at {ARENA_M} run tp @s ~ {CY} ~', Gen.play(AFT)])
    g.pw(key, 'field', [
        f'# At t{QA["field"]}: the field release (the kit wash fills to t{QA["ticks"]} and holds to t{QA["window_end"]}; the field ring',
        f'# r 3 -> {QA["field_r"]}) and the two mask hazards of the cast\'s safe group at the centre: the field ticks',
        f'# ({A.DMG_PM["q2_tick"]} per mille, never lethal, re-armed every {QA["tick_every"]} t, t{QA["ticks"]}-{QA["ticks"] + QA["tick_act"] - 1}) and the blast',
        f'# ({A.DMG_PM["q2_blast"]} per mille, t{QA["blast"]}-{QA["window_end"] - 1}, lethal unless this is the first cast: #apAft1 0).',
        f'execute {CENTRE} run {K.tele_mask_wash(QA["field_r"], QA["ticks"] - QA["field"], QA["window_end"] - QA["ticks"])}',
        f'execute {CENTRE} run {K.fx("field_ring", r0=3.0, r1=QA["field_r"], dur=18)}',
        f'execute {CENTRE} run {K.snd("q2_release")}',
        f'execute {CENTRE} run {F(f"p/{key}/hz_ticks")}',
        f'execute if score #apAft1 mb matches 0 {CENTRE} run {F(f"p/{key}/hz_blast0")}',
        f'execute unless score #apAft1 mb matches 0 {CENTRE} run {F(f"p/{key}/hz_blast1")}'])
    g.pw(key, 'hz_ticks', mask(A.DMG_PM['q2_tick'], QA['ticks'] - QA['field'], QA['tick_act'], False, rearm=QA['tick_every']))
    g.pw(key, 'hz_blast0', ['# the first cast of the fight: the blast never kills (plan Q3).']
         + mask(A.DMG_PM['q2_blast'], QA['blast'] - QA['field'], QA['blast_act'], False))
    g.pw(key, 'hz_blast1', ['# a later cast: the blast is lethal.']
         + mask(A.DMG_PM['q2_blast'], QA['blast'] - QA['field'], QA['blast_act'], True))
    g.pw(key, 'form', [
        '# Macro {i}, at footprint i: the dome forms: the safe marker (rlk_mb_ap_dome + rlk_mb_hzsafe, mbHzSG = the cast\'s group;',
        '# at the floor point, RFX-3 / RORG-2), the dome models (org om/dome, rising), the rise sparkle and its sound.',
        f'summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","{T_}","{DOME}","rlk_mb_hzsafe","{T_}n"]}}',
        f'scoreboard players operation @e[type=minecraft:marker,tag={T_}n] mbHzSG = #apq32G mb',
        f'$scoreboard players set @e[type=minecraft:marker,tag={T_}n] apL $(i)',
        f'tag @e[type=minecraft:marker,tag={T_}n] remove {T_}n',
        f'$execute rotated 0 0 run function {NS}om/dome/spawn {{i:$(i)}}',
        f'$function {NS}om/dome/play {{i:$(i),clip:"dome_rise"}}',
        K.fx('dome_rise'), K.snd('q2_dome')])
    g.pw(key, 'heal', [
        f'# Every {QA["heal_every"]} t while the domes stand: a player inside a formed dome (feet within its radius) heals 1 % max HP',
        '# (plan Q25 "소생의 찬가"; player/heal, so the item heal hooks see it).',
        f'execute at {PLAYER} positioned ~ {CY} ~ if entity @e[type=minecraft:marker,tag={DOME},distance=..{num(QA["dome_r"] + 0.3)}] '
        f'as @a[tag=player,scores={{dead=0}}] run {F(f"p/{key}/heal1")}'])
    g.pw(key, 'heal1', ['scoreboard players operation #heal tmp = @s maxHealth', 'scoreboard players operation #heal tmp /= #c100 mb',
                        'execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1', 'function rlk:player/heal',
                        f'execute at {PLAYER} run {K.fx("spark")}'])
    g.pw(key, 'pop', [f'# t{QA["pop"]}: every dome pops (the models\' pop clip, the rims end, the pop sound); the safe markers go. The kit\'s',
                      '# flash + shards per dome at t189 / 190 / 191 (one dome a tick: the per-tick command budget).']
         + [f'function {NS}om/dome/play {{i:{k},clip:"dome_pop"}}' for k in range(3)]
         + [f'execute as @e[type=minecraft:marker,tag={DOME},limit=1] at @s run {K.snd("q2_pop")}']
         + [K.tele_safe_end(k) for k in range(3)] + [f'kill @e[type=minecraft:marker,tag={DOME}]'])
    g.pw(key, 'done', [HEAD, '# The clip is over: the domes (popped at t189) and the pattern\'s markers go, then p/end.', F('dome/clear'),
                       f'kill @e[tag={T_}]', Gen.end()])
    g.pw(key, 'cancel', [HEAD, '# Cut / cancelled (pause -> resume, reload, death, tests; any executor): the domes, the masks, the',
                         '# footprints and the banner go.', F('dome/clear'), f'kill @e[tag={T_}]', K.hud('banner_end')])
    g.w('dome/clear', ['# Every dome (safe markers + org models), the Q2 mask hazards and the footprint rims (idempotent, any executor;',
                       '# the core calls it from cleanup, the phase jumps, death and a cancelled Q2).',
                       f'execute as @e[type=minecraft:marker,tag={HZ}] at @s run function rlk:mboss/hz/expire',
                       f'kill @e[type=minecraft:marker,tag={DOME}]', f'function {NS}om/dome/kill_all',
                       'kill @e[tag=rlk_mb_ap_domed]', 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_aft]']
        + [K.tele_safe_end(k) for k in range(3)])

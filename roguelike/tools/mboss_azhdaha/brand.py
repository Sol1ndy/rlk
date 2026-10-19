"""The brand (낙인), plan.md 4.10 (our fair rule), and the 응결 결정 shards. Called by core.emit (AZ:brand/**).

Per player (objectives created by ai/consts, removed by uninstall): azBrT = DoT ticks left (0 = not branded),
azBrE = the brand element (#elem), azBrS = Cryo stacks 1..3, azBrC = ticks to the next DoT tick. The harness
(S:az/harness/azfair.py CONTRACT) reads azBrT / azBrE.

1. Apply: a landed STRIKE hit (#mbHitEv with #mbHitRA 0) of an absorbed element brands (the leg element from phase 2,
   both absorbed elements in phase 3); a lingering / re-arming hazard hit (#mbHitRA 1: fields, strips, hail, orbs)
   brands too but at most once per 20 t and never adds Cryo stacks; Geo and physical never brand. A new element
   replaces the brand (5 ticks, first tick 20 t later); the same element refreshes it to max(remaining, 3).
2. DoT: every 20 t, mboss/pl_dot (cm.md 13.4) with #mbDotPct = DMG brand_pm (30 = 3 % max HP) x 1 / 1.5 / 2 for 1 / 2 / 3
   Cryo stacks, non-lethal; each Cryo strike +1 stack (max 3); a DoT tick without a new Cryo strike since the
   previous tick drops one stack (3 -> 2 -> 1).
3. Cleanse: healing (#mbHealAmt, the framework's cumulative heal amount, read and cleared here) reaching 6 % max HP
   while branded; a perfect dodge (#mbDodgeEv with #mbDodgeOk 1: a one-shot strike >= 12 t, not nododge, or a pj) at
   most once per 40 t; shields absorb the ticks (pl_dot).
4. Shards: a strike brand on a player with no shield (#mbHitSh 0) sheds one 응결 결정 (cooldown 300 t, at most 1, life
   200 t of the module clock: frozen by pause), placed 4-6 b from the player away from the anchor when the player is
   within 10 b of it, off live hazards and the body; picked up within 1.4 b: a shield of DMG shard_pm (12 %) max HP for
   15 s with the brand element (element/shield_gain; the element only when the new amount >= the current shield).
5. Show: the kit rune over the player every 4 t, the HUD brand part (storage az.hud.br: "낙인(물) N초", the core's
   sub-line appends it) and the ◈낙인 badge (core hud/extra); the first brand types the hint (plan 4.13).
6. Rule 33: a Pyro brand applied or refreshed by a strike outside the landslide calls p/firefield/on_brand (S2-L) as
   the body at the player's floor point (#azBrNew 1 new / 0 refresh), only when that file exists.
"""
from . import api as A

HINT = '낙인 — 보호막이 막아 줍니다 · 공격을 대시로 피하거나 6% 회복하면 지워집니다 · 결정을 주우면 보호막'
SHARD_LINE = '응결 결정 — 주우면 보호막'
DOT_T, DOT_N = 20, 5
REFRESH_MIN = 3
LINGER_GAP = 20
DODGE_GAP = 40
HEAL_PCT = 6
SHARD_CD, SHARD_LIFE, SHARD_PICK = 300, 200, 1.4
OBJ = ('azBrT', 'azBrE', 'azBrS', 'azBrC')
PLAYER1 = '@a[tag=player,limit=1]'
BRANDED = '@a[tag=player,scores={azBrT=1..},limit=1]'


def emit(core):
    g, F, NS = core.g, core.F, A.NS
    w = core.w
    on_brand = g.has('p/firefield/on_brand')
    w('brand/tick', [
        '# @s = body, at it, every module tick (after the clocks): the hit / dodge events of the framework (cm.md 13.3), the',
        '# heal meter, the DoT clock, the rune, the shards. The events are read and cleared here.',
        f'execute if score #mbHitEv mb matches 1.. run {F("brand/hit")}',
        'scoreboard players set #mbHitEv mb 0',
        f'execute if score #mbDodgeEv mb matches 1.. run {F("brand/dodge")}',
        'scoreboard players set #mbDodgeEv mb 0', 'scoreboard players set #mbDodgeOk mb 0',
        f'execute as {BRANDED} run {F("brand/heal")}',
        f'execute unless entity {BRANDED} run scoreboard players set #mbHealAmt mb 0',
        f'execute as {BRANDED} run {F("brand/clock")}',
        f'execute as {BRANDED} run {F("brand/rune_t")}',
        f'execute if entity @e[type=minecraft:item_display,tag=rlk_az_shard,limit=1] run {F("brand/shard_tick")}',
        'scoreboard players set #azBrCs mb 0'])
    w('brand/rune_t', ['# Every 4 t (module clock): the rune over the branded player.',
                       'scoreboard players operation #azM mb = #azClk mb', 'scoreboard players operation #azM mb %= #azK4 mb',
                       'execute unless score #azM mb matches 0 run return 0']
      + [f'execute if score @s azBrE matches {e} at @s positioned ~ ~1.2 ~ run {A.K.fxe("brand_rune", e)}' for e in (1, 2, 3, 4)])
    w('brand/hit', [
        '# @s = body. A landed hit this tick (#mbHitEl element, #mbHitRA 1 lingering, #mbHitSh 1 shielded before it): brand',
        '# only for an absorbed element (phase >= 2: the leg element; phase 3: the tail element too).',
        'scoreboard players set #azX mb 0',
        'execute if score #azPh mb matches 2..3 if score #mbHitEl mb = #azLeg mb run scoreboard players set #azX mb 1',
        'execute if score #azPh mb matches 3 if score #mbHitEl mb = #azTail mb run scoreboard players set #azX mb 1',
        'execute if score #azX mb matches 0 run return 0',
        'scoreboard players operation #azBrIn mb = #mbHitEl mb',
        f'execute if score #mbHitRA mb matches 1.. run return run {F("brand/linger")}',
        'scoreboard players set #azBrStrike mb 1',
        f'execute as {PLAYER1} run {F("brand/apply")}',
        f'execute unless score #mbHitSh mb matches 1.. as {PLAYER1} run {F("brand/shard_try")}'])
    w('brand/linger', [f'# A lingering / re-arming hit: at most one brand per {LINGER_GAP} t, never a Cryo stack.',
                       'scoreboard players operation #azX mb = #azClk mb', 'scoreboard players operation #azX mb -= #azBrRf mb',
                       f'execute if score #azX mb matches ..{LINGER_GAP - 1} run return 0',
                       'scoreboard players operation #azBrRf mb = #azClk mb',
                       'scoreboard players set #azBrStrike mb 0',
                       f'execute as {PLAYER1} run {F("brand/apply")}'])
    apply = ['# @s = player; #azBrIn = the element, #azBrStrike 1 strike / 0 lingering.',
             'scoreboard players set #azBrNew mb 0',
             f'execute if score @s azBrT matches 1.. if score @s azBrE = #azBrIn mb run {F("brand/refresh")}',
             f'execute unless score @s azBrT matches 1.. run {F("brand/new")}',
             f'execute if score @s azBrT matches 1.. unless score @s azBrE = #azBrIn mb run {F("brand/new")}',
             'scoreboard players set #azHudQ mb 1']
    if on_brand:
        apply.append('# rule 33 (S2-L): a Pyro brand by a strike outside the landslide -> p/firefield/on_brand at the floor point')
        apply.append(f'execute if score #azBrStrike mb matches 1 if score #azBrIn mb matches 1 unless score #azPat mb matches 20 '
                     f'at @s positioned ~ {A.CY} ~ as {A.BODY} run function {NS}p/firefield/on_brand')
    w('brand/apply', apply)
    w('brand/new', [f'# A new brand ({DOT_N} DoT ticks, the first {DOT_T} t later); a Cryo strike starts at 1 stack.',
                    'scoreboard players operation @s azBrE = #azBrIn mb', f'scoreboard players set @s azBrT {DOT_N}',
                    f'scoreboard players set @s azBrC {DOT_T}', 'scoreboard players set @s azBrS 0',
                    'execute if score #azBrIn mb matches 4 run scoreboard players set @s azBrS 1',
                    'execute if score #azBrIn mb matches 4 if score #azBrStrike mb matches 1 run scoreboard players set #azBrCs mb 1',
                    'scoreboard players set #azBrNew mb 1', 'scoreboard players set #azHeal mb 0',
                    A.K.snd('brand_apply'),
                    f'execute unless score #azBrHint mb matches 1 run {F("brand/hint")}'])
    w('brand/hint', ['# The first brand of the fight: the typed hint (plan 4.13).', 'scoreboard players set #azBrHint mb 1',
                     A.L.say(HINT, '#FFD27A', 1, 80, 1)])
    w('brand/refresh', [f'# The same element: remaining ticks = max(remaining, {REFRESH_MIN}); a Cryo strike +1 stack (max 3).',
                        f'execute if score @s azBrT matches ..{REFRESH_MIN - 1} run scoreboard players set @s azBrT {REFRESH_MIN}',
                        'execute if score #azBrIn mb matches 4 if score #azBrStrike mb matches 1 run scoreboard players add @s azBrS 1',
                        'execute if score #azBrIn mb matches 4 if score #azBrStrike mb matches 1 run scoreboard players set #azBrCs mb 1',
                        'execute if score @s azBrS matches 4.. run scoreboard players set @s azBrS 3'])
    w('brand/clock', ['# @s = the branded player: the DoT clock.', 'scoreboard players remove @s azBrC 1',
                      f'execute if score @s azBrC matches ..0 run {F("brand/dot")}'])
    w('brand/dot', [
        '# @s = player: one DoT tick through mboss/pl_dot (non-lethal, shields absorb, no defence, i-frames ignored).',
        f'scoreboard players set @s azBrC {DOT_T}',
        f'scoreboard players set #mbDotPct mb {A.DMG["brand_pm"]}',
        f'execute if score @s azBrE matches 4 if score @s azBrS matches 2 run scoreboard players set #mbDotPct mb {A.DMG["brand_pm"] * 3 // 2}',
        f'execute if score @s azBrE matches 4 if score @s azBrS matches 3.. run scoreboard players set #mbDotPct mb {A.DMG["brand_pm"] * 2}',
        'scoreboard players operation #mbDotEl mb = @s azBrE', 'scoreboard players set #mbDotLethal mb 0',
        A.fw('pl_dot'),
        A.K.snd('brand_tick'),
        'scoreboard players remove @s azBrT 1',
        '# Cryo: a tick without a new Cryo strike since the previous tick drops one stack (3 -> 2 -> 1)',
        'execute if score @s azBrE matches 4 unless score #azBrCs mb matches 1 if score @s azBrS matches 2.. run scoreboard players remove @s azBrS 1',
        'scoreboard players set #azBrCs mb 0',
        'scoreboard players set #azHudQ mb 1',
        f'execute if score @s azBrT matches ..0 run {F("brand/clear")}'])
    w('brand/heal', [
        f'# @s = the branded player: the cure meter (cumulative healing while branded) reaching {HEAL_PCT} % max HP cleanses.',
        'scoreboard players operation #azHeal mb += #mbHealAmt mb', 'scoreboard players set #mbHealAmt mb 0',
        'scoreboard players operation #azX mb = @s maxHealth', f'scoreboard players set #azY mb {HEAL_PCT}',
        'scoreboard players operation #azX mb *= #azY mb',
        'scoreboard players operation #azY mb = #azHeal mb', 'scoreboard players operation #azY mb *= #c100 mb',
        f'execute if score #azY mb >= #azX mb run {F("brand/cleanse")}'])
    w('brand/dodge', [
        f'# @s = body: a perfect dodge (#mbDodgeOk 1: one-shot strike >= 12 t, not nododge, or a pj) cleanses, once per {DODGE_GAP} t.',
        'execute unless score #mbDodgeOk mb matches 1 run return 0',
        f'execute unless entity {BRANDED} run return 0',
        'scoreboard players operation #azX mb = #azClk mb', 'scoreboard players operation #azX mb -= #azDgClk mb',
        f'execute if score #azX mb matches ..{DODGE_GAP - 1} run return 0',
        'scoreboard players operation #azDgClk mb = #azClk mb',
        f'execute as {BRANDED} run {F("brand/cleanse")}'])
    w('brand/cleanse', ['# @s = player: the brand and its stacks end (the butterfly-style cure fx and a chime).',
                        f'execute at @s run {A.K.fx("cure")}', A.K.snd('cleanse'),
                        f'execute at @s run {A.L.sound("block.amethyst_block.chime", 1.0, 1.4, target="@s")}',
                        F('brand/clear')])
    w('brand/clear', ['# @s = player: not branded.', 'scoreboard players set @s azBrT 0', 'scoreboard players set @s azBrE 0',
                      'scoreboard players set @s azBrS 0', 'scoreboard players set @s azBrC 0', 'scoreboard players set #azHeal mb 0',
                      'scoreboard players set #azHudQ mb 1'])
    w('brand/clear_all', ['# Every brand and shard (death, abort, cleanup, uninstall, fight end; any executor).',
                          f'execute as @a[tag=player] run {F("brand/clear")}', 'kill @e[type=minecraft:item_display,tag=rlk_az_shard]',
                          'data remove storage rlk:mboss az.hud.br'])
    # shards
    hz_near = '@e[type=minecraft:marker,tag=rlk_mb_hz,distance=..4,limit=1]'
    w('brand/shard_try', [
        f'# @s = the player just branded without a shield: one 응결 결정 (cooldown {SHARD_CD} t, at most 1 alive, life {SHARD_LIFE} t).',
        'execute if score #azClk mb < #azShCd mb run return 0',
        'execute if entity @e[type=minecraft:item_display,tag=rlk_az_shard,limit=1] run return 0',
        'kill @e[type=minecraft:marker,tag=rlk_mb_az_shp]',
        '# away from the anchor when it is within 10 b, else a random bearing; 5 b out',
        f'execute at @s if entity {A.BODY.replace("limit=1", "distance=..10,limit=1")} facing entity {A.BODY} feet rotated ~180 0 '
        f'positioned ^ ^ ^5 run summon minecraft:marker ~ {A.CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_shp"]}}',
        'execute store result storage rlk:mboss az.sh.a int 1 run random value 0..359',
        f'execute at @s unless entity @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] run function {NS}brand/shard_rnd with storage rlk:mboss az.sh',
        f'execute as @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] run {g.clamp_walk()}',
        '# off a live hazard and the body: one swing of 60 degrees about the player, else give up',
        f'execute as @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] at @s if entity {hz_near} at {PLAYER1} facing entity @s feet '
        f'rotated ~60 0 positioned ^ ^ ^5 run tp @s ~ {A.CY} ~',
        f'execute as @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] at @s if entity {A.BODY.replace("limit=1", "distance=..5,limit=1")} '
        f'at {PLAYER1} facing entity @s feet rotated ~-120 0 positioned ^ ^ ^5 run tp @s ~ {A.CY} ~',
        f'execute as @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] at @s if entity {hz_near} run kill @s',
        f'execute at @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] run {F("brand/shard_make")}',
        'kill @e[type=minecraft:marker,tag=rlk_mb_az_shp]'])
    w('brand/shard_rnd', ['$execute rotated $(a) 0 positioned ^ ^ ^5 run summon minecraft:marker ~ ' + str(A.CY) +
                          ' ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_shp"]}'])
    w('brand/shard_make', [
        '# At the shard spot (floor): the gold-amber shard with the brand element inside, hovering 1 b up.',
        'summon minecraft:item_display ~ ~1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_az_shard","rlk_az_shnew"],billboard:"vertical",'
        'brightness:{block:15,sky:15},teleport_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],'
        'right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]},item:{id:"minecraft:amethyst_shard",count:1}}',
        f'scoreboard players set @e[type=minecraft:item_display,tag=rlk_az_shnew] azT {SHARD_LIFE}',
        f'execute as @e[type=minecraft:item_display,tag=rlk_az_shnew] run scoreboard players operation @s azS = {PLAYER1} azBrE']
      + [f'execute as @e[type=minecraft:item_display,tag=rlk_az_shnew,scores={{azS={e}}}] run {A.K.prope("shard", e)}' for e in (1, 2, 3, 4)]
      + ['tag @e[type=minecraft:item_display,tag=rlk_az_shnew] remove rlk_az_shnew',
         'scoreboard players operation #azShCd mb = #azClk mb', f'scoreboard players add #azShCd mb {SHARD_CD}',
         A.K.snd('shard_spawn'),
         f'execute unless score #azShHint mb matches 1 run {F("brand/shard_hint")}'])
    w('brand/shard_hint', ['scoreboard players set #azShHint mb 1', f'scoreboard players set #azHint mb 3',
                           'scoreboard players operation #azHintT mb = #azClk mb', 'scoreboard players add #azHintT mb 100',
                           'scoreboard players set #azHudQ mb 1'])
    w('brand/shard_tick', [f'execute as @e[type=minecraft:item_display,tag=rlk_az_shard] at @s run {F("brand/shard1")}'])
    w('brand/shard1', [
        '# @s = a shard (module clock: frozen while paused): ages, sparkles, is picked up within 1.4 b.',
        'scoreboard players remove @s azT 1',
        'execute if score @s azT matches ..0 run return run kill @s',
        'scoreboard players operation #azM mb = @s azT', 'scoreboard players operation #azM mb %= #azK4 mb',
        'execute if score #azM mb matches 0 run particle minecraft:wax_on ~ ~0.3 ~ 0.15 0.15 0.15 0 1 force @a[tag=player]',
        f'execute if entity @a[tag=player,distance=..{SHARD_PICK},limit=1] run {F("brand/shard_pick")}'])
    w('brand/shard_pick', [
        f'# @s = the shard: a shield of {A.DMG["shard_pm"] / 10:g} % max HP for 15 s with the brand element (own copy of the',
        '# crystallize pickup, not counted against the crystal cap); the element only when the new amount >= the shield.',
        f'execute store result score #amt tmp run scoreboard players get {PLAYER1} maxHealth',
        f'scoreboard players set #azX mb {A.DMG["shard_pm"]}', 'scoreboard players operation #amt tmp *= #azX mb',
        'scoreboard players operation #amt tmp /= #c1000 mb',
        'execute if score #amt tmp matches ..0 run scoreboard players set #amt tmp 1',
        'scoreboard players operation #shEl tmp = @s azS',
        f'execute as {PLAYER1} unless score @s shieldHP > #amt tmp run function rlk:element/shield_gain',
        'scoreboard players set #shEl tmp 0',
        A.K.snd('shard_pick'), A.L.sound('block.amethyst_block.chime', 1.0, 1.2),
        'kill @s'])
    # the HUD brand part (core hud/sub appends storage az.hud.br)
    w('brand/hud', ['# The sub-line part "낙인(<element>) N초" of the branded player (rebuilt with the lines).',
                    'data remove storage rlk:mboss az.hud.br',
                    f'execute unless entity {BRANDED} run return 0',
                    f'execute store result storage rlk:mboss az.hb.n int 1 run scoreboard players get {BRANDED} azBrT']
      + [f'execute if entity @a[tag=player,scores={{azBrT=1..,azBrE={e}}}] run data modify storage rlk:mboss az.hb.e set value '
         f'"{A.EL_NAME[e]}"' for e in (1, 2, 3, 4)]
      + [f'execute if entity @a[tag=player,scores={{azBrT=1..,azBrE={e}}}] run data modify storage rlk:mboss az.hb.c set value '
         f'"{A.EL_COL[e]}"' for e in (1, 2, 3, 4)]
      + [f'function {NS}brand/hud_set with storage rlk:mboss az.hb'])
    w('brand/hud_set', ['$data modify storage rlk:mboss az.hud.br set value [{text:"   낙인(",color:"#E8D0B0"},'
                        '{text:"$(e)",color:"$(c)"},{text:") $(n)초",color:"#E8D0B0"}]'])

# G3 backfire (@s = body; on_hit flagged #core 2: the first reaction on her inside a core window): the pattern is
# cancelled, a burst at her chest, true damage 3 % of her max HP, stagger 50 t taking 130 %. Once per pattern.
scoreboard players set #core tk 1
execute unless score #pat tk matches 1..11 run return 0
function rlk:boss/tachy/core/cancel_pat
execute at @s run particle minecraft:explosion_emitter ~ ~1.4 ~ 0 0 0 0 1 force @a[tag=player]
execute at @s run particle minecraft:flame ~ ~1.4 ~ 0.3 0.3 0.3 0.2 40 force @a[tag=player]
execute at @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.9 0.9 0.3
execute at @s run playsound minecraft:entity.blaze.hurt hostile @a[tag=player] ~ ~ ~ 0.7 0.6 0.23
scoreboard players operation #mbTrueEl mb = #el tk
function rlk:mboss/true_pct {pct:3}
execute unless score #mbSt mb matches 1 run return 0
# true damage skips the HP floor: a backfire below it still reserves the phase step
execute if score #mbFloor mb matches 1.. if score @s mhpC <= #mbFloor mb run scoreboard players set #mbFloorHit mb 1
scoreboard players set #stag tk 50
scoreboard players set #taken tk 130
function rlk:boss/tachy/rig_stub/play/stagger
execute at @s run playsound minecraft:entity.iron_golem.damage hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.2

# G3 backfire (@s = body; on_hit flagged #core 2: the first reaction on her inside a core window): the pattern is
# cancelled, a burst at her chest, true damage 3 % of her max HP, stagger 50 t taking 130 %. Once per pattern.
scoreboard players set #core tk 1
execute unless score #pat tk matches 1..11 run return 0
function rlk:boss/tachy/core/cancel_pat
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run function rlk:boss/tachy/fx/p/core_burst
execute at @s run function rlk:boss/tachy/fx/snd/core_backfire
scoreboard players operation #mbTrueEl mb = #el tk
function rlk:mboss/true_pct {pct:3}
execute unless score #mbSt mb matches 1 run return 0
# true damage skips the HP floor: a backfire below it still reserves the phase step
execute if score #mbFloor mb matches 1.. if score @s mhpC <= #mbFloor mb run scoreboard players set #mbFloorHit mb 1
scoreboard players set #stag tk 50
scoreboard players set #taken tk 130
function rlk:boss/tachy/rig/play/stagger
execute at @s run function rlk:boss/tachy/fx/snd/stagger

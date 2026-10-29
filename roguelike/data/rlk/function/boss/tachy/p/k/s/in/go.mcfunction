# K stage in: tick 0 (@s = body).
scoreboard players set #k_s tk 2
scoreboard players set #k_c tk 0
function rlk:boss/tachy/p/k/spot
tag @s remove rlk_mb_inv
function rlk:boss/tachy/rig/state/normal
function rlk:boss/tachy/rig/play/blink_in
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/tachy/fx/p/blink_in
execute at @s run function rlk:boss/tachy/fx/snd/blink_in
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run function rlk:boss/tachy/fx/p/wing_flare
execute store result score #k_h tk run random value 20..60
execute if score #ph tk matches 7 store result score #k_h tk run random value 10..40
scoreboard players add #k_h tk 10

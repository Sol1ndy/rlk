# A13 pattern tick 97.
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.95 ~ run function rlk:boss/scarlet/fx/p/ghost_burst
function rlk:boss/scarlet/rig/state/hidden
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b80]
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_89]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_91] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_93] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_95] remove rlk_hr_trr

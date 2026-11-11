# A8 pattern tick 200.
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.95 ~ run function rlk:boss/scarlet/fx/p/ghost_burst
function rlk:boss/scarlet/rig/state/hidden
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c196]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c196_196] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c196_198] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"

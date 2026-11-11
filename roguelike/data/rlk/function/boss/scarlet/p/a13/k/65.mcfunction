# A13 pattern tick 65.
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.95 ~ run function rlk:boss/scarlet/fx/p/ghost_burst
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c58_59]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c58_61] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"

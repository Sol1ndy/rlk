# A13 pattern tick 65.
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.95 ~ run function rlk:boss/scarlet/fx/p/ghost_burst
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b16]
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_57]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_59] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_61] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_63] remove rlk_hr_trr
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13r1r58]

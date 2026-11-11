# RINGS pattern tick 38
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings34]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings34_32]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings34_34] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings34_36] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_rings44,limit=1] ^-1.118 ^1.026 ^1.656

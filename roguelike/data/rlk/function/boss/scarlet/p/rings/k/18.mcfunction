# RINGS pattern tick 18
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings14]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings14_12]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings14_14] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings14_16] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_rings24,limit=1] ^-1.118 ^1.026 ^1.656

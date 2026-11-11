# RINGS pattern tick 39
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings34_33]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings34_35] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings34_37] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_rings44,limit=1] ^-1.893 ^1.019 ^0.237

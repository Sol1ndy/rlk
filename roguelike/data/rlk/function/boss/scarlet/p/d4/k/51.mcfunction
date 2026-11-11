# D4 pattern tick 51
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_d444_45]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d444_47] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_d454,limit=1] ^0.952 ^0.778 ^1.842

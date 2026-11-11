# D4 pattern tick 48
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_d444]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_d444_42]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d444_44] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d444_46] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_d454,limit=1] ^1.919 ^0.75 ^0.598

# D4 pattern tick 38
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_d434]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_d434_32]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d434_34] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_d444] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_d444,limit=1] ^0.092 ^2.948 ^1.128

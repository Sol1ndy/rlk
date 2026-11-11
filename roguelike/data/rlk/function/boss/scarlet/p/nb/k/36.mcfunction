# NB pattern tick 36
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_30]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_32] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_nb40] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_nb40,limit=1] ^0.423 ^2.22 ^2.181

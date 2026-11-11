# NB pattern tick 37
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_31]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_33] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_nb40,limit=1] ^0.281 ^1.884 ^2.291

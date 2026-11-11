# NB pattern tick 26
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_nb20_20]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb20_22] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_nb30,limit=1] ^0.684 ^2.894 ^1.754

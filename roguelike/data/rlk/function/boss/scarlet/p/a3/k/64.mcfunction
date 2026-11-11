# A3 pattern tick 64
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a357_58]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a357_60] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_a369] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_a369,limit=1] ^1.861 ^0.108 ^0.667

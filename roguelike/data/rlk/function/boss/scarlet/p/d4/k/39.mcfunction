# D4 pattern tick 39
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_d434_33]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d434_35] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_d444,limit=1] ^0.114 ^2.681 ^1.477

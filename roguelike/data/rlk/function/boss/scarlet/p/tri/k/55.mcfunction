# TRI pattern tick 55
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_tri48_49]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_tri48_51] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_tri60] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_tri60,limit=1] ^-0.659 ^2.205 ^1.436

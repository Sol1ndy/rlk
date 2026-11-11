# A4 pattern tick 36
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_a434] ~ ~ ~ ~ 0
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a434_30]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a434_32] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"

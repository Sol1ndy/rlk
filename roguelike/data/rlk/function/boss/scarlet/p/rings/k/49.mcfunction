# RINGS pattern tick 49
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44_43]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44_45] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44_47] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute if score #ph hr matches 7 at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54] ~ ~ ~ ~ 0
execute if score #ph hr matches 7 at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_rings54,limit=1] ^1.794 ^1.046 ^-0.075

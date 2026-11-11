# RINGS pattern tick 59
execute if score #ph hr matches 7 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54_53]
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54_55] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54_57] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"

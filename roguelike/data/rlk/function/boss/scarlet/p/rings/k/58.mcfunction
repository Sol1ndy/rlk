# RINGS pattern tick 58
execute if score #ph hr matches 7 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54]
execute if score #ph hr matches 7 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54_52]
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54_54] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54_56] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute if score #ph hr matches 7 unless score #ultq hr matches 1 run function rlk:boss/scarlet/ai/tail

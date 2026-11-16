# RINGS pattern tick 58
execute if score #ph hr matches 7 unless score #ultq hr matches 1 run function rlk:boss/scarlet/ai/tail
execute if score #ph hr matches 7 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1b48]
execute if score #ph hr matches 7 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_50]
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_52] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_54] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute if score #ph hr matches 7 run tag @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_56] remove rlk_hr_trr

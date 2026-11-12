# RINGS pattern tick 60
execute if score #ph hr matches 7 if score #ultq hr matches 1 run scoreboard players set #done hr 1
execute if score #ph hr matches 7 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_52]
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_54] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_56] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"

# RINGS pattern tick 61
execute if score #ph hr matches 7 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_53]
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_55] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"

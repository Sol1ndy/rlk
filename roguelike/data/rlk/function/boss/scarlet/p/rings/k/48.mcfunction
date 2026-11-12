# RINGS pattern tick 48
execute if score #ph hr matches 1 unless score #ultq hr matches 1 run function rlk:boss/scarlet/ai/tail
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0b1]
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_40]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_42] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_44] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_46] remove rlk_hr_trr
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1b48] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.3155f,1.1596f,0.0843f],left_rotation:[-0.5997f,-0.6243f,0.3747f,0.332f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}

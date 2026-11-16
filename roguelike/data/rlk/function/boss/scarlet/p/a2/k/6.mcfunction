# A2 pattern tick 6
function rlk:boss/scarlet/rig/look/blade/lilac
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a2b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3959f,1.4842f,0.1279f],left_rotation:[-0.8913f,-0.3692f,0.1007f,0.2431f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a2_2] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_quad_1"

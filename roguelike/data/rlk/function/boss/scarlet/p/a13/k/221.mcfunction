# A13 pattern tick 221.
execute at @s positioned ~ ~0.67 ~ run function rlk:mboss/mv/glide {t:1}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_219] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_220,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3915f,1.2021f,0.2919f],left_rotation:[0.0184f,0.0538f,-0.3625f,0.9302f],scale:[0.8185f,0.3f,1.8394f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_220,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3858f,1.3021f,0.0842f],left_rotation:[0.0968f,0.2536f,-0.3439f,0.8989f],scale:[0.8662f,0.3f,1.9476f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_220,tag=rlk_hr_tr_i2] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3943f,1.3865f,0.0331f],left_rotation:[0.1707f,0.4414f,-0.3089f,0.825f],scale:[0.8819f,0.3f,1.9835f],right_rotation:[0f,0f,0f,1f]}}

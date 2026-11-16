# A2 pattern tick 4
execute at @s run function rlk:boss/scarlet/fx/snd/a2_draw
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a2b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4064f,1.4956f,0.1226f],left_rotation:[-0.8853f,-0.3667f,0.1095f,0.2643f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a2_2] remove rlk_hr_trr

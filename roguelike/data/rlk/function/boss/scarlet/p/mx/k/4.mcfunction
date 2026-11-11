# MX pattern tick 4
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/head
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/star4
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/a9_star
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mxb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5632f,0.9028f,-0.4087f],left_rotation:[0.3574f,-0.8626f,0.3307f,-0.1374f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_2] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_3,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3429f,1.0946f,-0.0596f],left_rotation:[0.0801f,0.9093f,-0.232f,0.3362f],scale:[0.5178f,0.18f,2.0154f],right_rotation:[0f,0f,0f,1f]}}

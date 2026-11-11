# KCUT pattern tick 3
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/head
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/yellow_tell {t:110}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/yellow_chime
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2742f,0.8059f,-0.126f],left_rotation:[-0.954f,0.0204f,0.0667f,0.2917f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_1] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_2,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2896f,0.8235f,-0.1034f],left_rotation:[-0.8744f,-0.2687f,0.2992f,0.2715f],scale:[0.6654f,0.22f,1.5422f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_2,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2699f,0.8317f,-0.1451f],left_rotation:[-0.9418f,-0.1078f,0.1373f,0.2871f],scale:[0.6578f,0.22f,1.5243f],right_rotation:[0f,0f,0f,1f]}}

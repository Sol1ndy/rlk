# ULT pattern tick 34
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/head
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/star4
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/a9_star
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.7096f,1.1326f,-0.0992f],left_rotation:[-0.63f,0.5337f,-0.321f,0.4639f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}

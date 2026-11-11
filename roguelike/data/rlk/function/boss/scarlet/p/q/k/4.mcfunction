# Q pattern tick 4
function rlk:boss/scarlet/rig/look/form/ghost
tag @s add rlk_hr_ghost
execute at @s run function rlk:boss/scarlet/fx/snd/g_tell
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.95 ~ run function rlk:boss/scarlet/fx/p/ghost_burst
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3827f,0.726f,0.0421f],left_rotation:[-0.5173f,0.6601f,-0.4821f,0.2536f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q0_2] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0_3,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0964f,0.8338f,0.1828f],left_rotation:[0.0992f,0.7945f,-0.1633f,0.5763f],scale:[0.5145f,0.22f,1.9005f],right_rotation:[0f,0f,0f,1f]}}

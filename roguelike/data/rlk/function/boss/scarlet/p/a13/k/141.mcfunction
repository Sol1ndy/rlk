# A13 pattern tick 141.
execute at @s run function rlk:boss/scarlet/fx/snd/g_step
function rlk:boss/scarlet/g/cut/aim {s:151}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b139] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5855f,1.4163f,-0.2238f],left_rotation:[-0.7697f,0.539f,-0.1962f,0.2802f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_139] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_140,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3466f,1.3359f,0.0797f],left_rotation:[-0.9642f,0f,-0.0622f,0.2579f],scale:[0.7664f,0.22f,1.8978f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_140,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3555f,1.3193f,0.058f],left_rotation:[-0.8949f,0.3213f,-0.168f,0.2601f],scale:[0.7686f,0.22f,1.9096f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.685 ^1.453 ^-0.35 run function rlk:boss/scarlet/core/sw/rib

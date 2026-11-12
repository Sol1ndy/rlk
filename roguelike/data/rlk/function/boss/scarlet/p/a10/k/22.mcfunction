# A10 pattern tick 22
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 201.1 ~ run function rlk:boss/scarlet/fx/p/burst_radial {r:35}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:boss/scarlet/fx/snd/a10_impact
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.1195f,0.6665f,0.6635f],left_rotation:[0.1592f,0.0001f,0.0006f,0.9872f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_20] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_21,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0752f,1.0892f,-0.4982f],left_rotation:[0.011f,0.011f,-0.7067f,0.7073f],scale:[0.5652f,0.3f,2.7894f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_21,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0671f,1.0883f,-0.4917f],left_rotation:[0.0822f,0.0823f,-0.7018f,0.7028f],scale:[0.5646f,0.3f,2.7862f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.12 ^0.615 ^0.82 run function rlk:boss/scarlet/core/sw/rib

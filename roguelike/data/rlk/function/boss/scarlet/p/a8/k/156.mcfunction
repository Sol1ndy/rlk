# A8 pattern tick 156.
function rlk:boss/scarlet/g/cut/lock {s:163}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^0.16 ^2.98 ^0.272 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b154] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5797f,1.526f,-0.247f],left_rotation:[-0.7697f,0.539f,-0.1962f,0.2802f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_155,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.6519f,1.4296f,-0.4894f],left_rotation:[0.7237f,0.5994f,0.3221f,0.1149f],scale:[0.2822f,0.22f,1.435f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.679 ^1.562 ^-0.373 run function rlk:boss/scarlet/core/sw/rib

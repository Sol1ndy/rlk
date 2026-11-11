# A13 pattern tick 144.
execute at @s run function rlk:boss/scarlet/fx/snd/g_step
function rlk:boss/scarlet/g/cut/lock {s:151}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^0.16 ^2.98 ^0.272 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b139] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5855f,1.4446f,-0.2238f],left_rotation:[-0.7697f,0.539f,-0.1962f,0.2802f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_140] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute at @s rotated as @s rotated ~ 0 positioned ^0.685 ^1.481 ^-0.35 run function rlk:boss/scarlet/core/sw/rib

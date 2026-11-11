# A8 pattern tick 57.
function rlk:boss/scarlet/g/cut/lock {s:64}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^0.826 ^1.941 ^-1.031 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b19] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3884f,1.3595f,-0.4084f],left_rotation:[-0.8719f,0.3611f,-0.1266f,0.3057f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_49]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_51] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_55] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_56,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2273f,1.4276f,-0.1853f],left_rotation:[-0.2727f,0.83f,0.068f,0.4819f],scale:[0.608f,0.22f,1.9114f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a8_57","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.396f,1.4132f,-0.3673f],left_rotation:[0.1736f,0.8885f,0.2509f,0.3445f],scale:[0f,0.22f,1.6365f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16771496]}}}}

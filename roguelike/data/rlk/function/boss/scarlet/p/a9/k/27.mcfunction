# A9 pattern tick 27
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 1
execute at @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line with storage rlk:hr core.dash
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/a9
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 1
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:40,tell:1,dmg:54}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/a9
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3273f,0.7708f,0.5868f],left_rotation:[-0.1591f,-0.0862f,-0.689f,-0.7018f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_25] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_26,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0636f,0.7467f,0.447f],left_rotation:[0.0299f,-0.7875f,0.0631f,0.6124f],scale:[0.6483f,0.26f,1.7061f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_26,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0637f,0.7553f,0.4547f],left_rotation:[0.036f,-0.6585f,0.0532f,0.7498f],scale:[0.6722f,0.26f,1.7693f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_26,tag=rlk_hr_tr_i2] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1314f,0.7592f,0.4324f],left_rotation:[0.0408f,-0.506f,0.0415f,0.8606f],scale:[0.6856f,0.26f,1.8045f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a9","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a9_27","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.1737f,0.7659f,0.397f],left_rotation:[0.0523f,-0.4215f,0.0124f,0.9052f],scale:[0f,0.26f,1.8445f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[15584255]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a9","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a9_27","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.2208f,0.7836f,0.3034f],left_rotation:[0.0532f,-0.4205f,-0.0092f,0.9057f],scale:[0f,0.26f,1.8972f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[15584255]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a9","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a9_27","rlk_hr_tr_i2"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.2214f,0.7962f,0.2953f],left_rotation:[0.0536f,-0.0285f,-0.0093f,0.9981f],scale:[0f,0.26f,1.9013f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[15584255]}}}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.383 ^0.754 ^0.741 run function rlk:boss/scarlet/core/sw/rib

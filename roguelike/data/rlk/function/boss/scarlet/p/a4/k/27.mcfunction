# A4 pattern tick 27
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ^-0.239 ^2.967 ^0.332 run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2007f,1.4278f,0.3212f],left_rotation:[-0.4258f,-0.4053f,0.5651f,0.5789f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_19]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_23] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_25] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_26,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0154f,1.1155f,0.5435f],left_rotation:[-0.7932f,0.0138f,0.6087f,0.0107f],scale:[0.1828f,0.22f,1.7391f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a4","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a4_27","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.3988f,1.2045f,0.4081f],left_rotation:[0.0122f,-0.8079f,-0.0104f,0.5879f],scale:[0f,0.3f,1.247f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a4","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a4_27","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.0668f,1.356f,0.4076f],left_rotation:[0.0049f,-0.7066f,-0.0102f,0.707f],scale:[0f,0.3f,1.4115f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a4r0r16]

# A8 pattern tick 22.
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.95 ~ run function rlk:boss/scarlet/fx/p/ghost_trail {len:125}
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run function rlk:mboss/mv/glide {t:4}
execute at @s run function rlk:boss/scarlet/fx/snd/g_dash
function rlk:boss/scarlet/g/cut/aim {s:30}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b19] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4514f,1.5828f,-0.2766f],left_rotation:[-0.933f,0.25f,-0.067f,0.25f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:marker,tag=rlk_hr_trt]
execute at @s rotated as @s rotated ~ 0 positioned ^0.493 ^1.658 ^-0.497 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_hr_tr","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_trt"]}
tag @e[type=minecraft:item_display,tag=rlk_hr_trg] remove rlk_hr_trg
execute at @s rotated as @s rotated ~ 0 positioned ^0.493 ^1.658 ^-0.497 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_tri","rlk_hr_trg","rlk_hr_tr_a8r0r22"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.3f,0.3f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_rib_0","minecraft:custom_model_data":{colors:[16771496]}}}}

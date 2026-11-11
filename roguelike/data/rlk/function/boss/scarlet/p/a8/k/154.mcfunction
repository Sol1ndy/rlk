# A8 pattern tick 154.
function rlk:boss/scarlet/g/spot/d3
function rlk:mboss/mv/stop
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] positioned ~ ~3 ~ run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/rig/follow_now
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run function rlk:mboss/mv/glide {t:5}
function rlk:boss/scarlet/g/cut/aim {s:163}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b154] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5287f,1.2557f,-0.3927f],left_rotation:[-0.7697f,0.539f,-0.1962f,0.2802f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:marker,tag=rlk_hr_trt]
execute at @s rotated as @s rotated ~ 0 positioned ^0.628 ^1.292 ^-0.519 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_hr_tr","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_trt"]}
tag @e[type=minecraft:item_display,tag=rlk_hr_trg] remove rlk_hr_trg
execute at @s rotated as @s rotated ~ 0 positioned ^0.628 ^1.292 ^-0.519 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_tri","rlk_hr_trg","rlk_hr_tr_a8r4r154"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.3f,0.3f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_rib_0","minecraft:custom_model_data":{colors:[16771496]}}}}

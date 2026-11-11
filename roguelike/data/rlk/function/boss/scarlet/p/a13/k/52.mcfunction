# A13 pattern tick 52.
execute at @s run function rlk:boss/scarlet/fx/snd/g_leap
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run function rlk:mboss/mv/leap {t:6,h:30}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b16] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3862f,1.358f,-0.4123f],left_rotation:[-0.8727f,0.3615f,-0.1256f,0.3032f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_44]
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_50] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_51,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.396f,1.4132f,-0.3673f],left_rotation:[0.1537f,0.9159f,0.2532f,0.271f],scale:[0.5279f,0.22f,1.6151f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:marker,tag=rlk_hr_trt]
execute at @s rotated as @s rotated ~ 0 positioned ^0.461 ^1.432 ^-0.537 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_hr_tr","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a13","rlk_hr_trt"]}
tag @e[type=minecraft:item_display,tag=rlk_hr_trg] remove rlk_hr_trg
execute at @s rotated as @s rotated ~ 0 positioned ^0.461 ^1.432 ^-0.537 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a13","rlk_hr_tri","rlk_hr_trg","rlk_hr_tr_a13r1r52"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.3f,0.3f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_rib_0","minecraft:custom_model_data":{colors:[16771496]}}}}

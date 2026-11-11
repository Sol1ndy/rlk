# HCUT pattern tick 2
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/head
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/yellow_tell {t:6}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/yellow_chime
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2802f,0.7025f,0.369f],left_rotation:[0.2084f,-0.441f,0.6767f,-0.5514f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_1,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.17f,0.8981f,0.3594f],left_rotation:[0.2281f,0.0313f,0.1083f,0.9671f],scale:[0.4879f,0.22f,1.666f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_1,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1741f,0.8732f,0.363f],left_rotation:[0.1946f,0.2243f,-0.1166f,0.9477f],scale:[0.4911f,0.22f,1.6794f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_hcut","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_hcut_2","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.1368f,0.8323f,0.2933f],left_rotation:[0.2233f,0.2698f,-0.0029f,0.9365f],scale:[0f,0.22f,1.7829f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16769354]}}}}

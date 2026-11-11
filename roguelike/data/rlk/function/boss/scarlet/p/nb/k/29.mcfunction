# NB pattern tick 29
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 0
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s rotated ~30 0 positioned ^ ^ ^-8 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:160,w:30,tell:1,dmg:42}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/nb
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nbb2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4376f,1.787f,0.6819f],left_rotation:[-0.0228f,-0.2011f,-0.3575f,0.9117f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_21]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_23] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_28,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2842f,1.6876f,0.0352f],left_rotation:[-0.4952f,-0.377f,-0.759f,0.191f],scale:[0.8481f,0.26f,2.0313f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_28,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3998f,1.7436f,0.1168f],left_rotation:[-0.3302f,-0.3303f,-0.8439f,0.2638f],scale:[0.8209f,0.26f,1.9657f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_nb_29","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.479f,1.7627f,0.2217f],left_rotation:[-0.2382f,-0.306f,-0.872f,0.2966f],scale:[0f,0.26f,1.9641f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_nb_29","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.5324f,1.7498f,0.3393f],left_rotation:[-0.055f,-0.2393f,-0.903f,0.3519f],scale:[0f,0.26f,1.9168f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}

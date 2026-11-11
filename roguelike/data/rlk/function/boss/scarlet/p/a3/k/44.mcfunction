# A3 pattern tick 44
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 0
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:40,a:50,tell:1,dmg:31}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/a3
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3408f,1.6352f,0.4094f],left_rotation:[0f,-0.342f,-0.9397f,0f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_42] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_43,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3116f,1.2951f,0.1501f],left_rotation:[0.0043f,-0.1981f,0.547f,0.8134f],scale:[0.7047f,0.26f,2.047f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a3","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a3_44","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.3388f,1.3016f,0.0499f],left_rotation:[-0.0492f,-0.1249f,0.591f,0.7953f],scale:[0f,0.26f,2.1077f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a3","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a3_44","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.3414f,1.2848f,-0.0079f],left_rotation:[-0.0453f,-0.1196f,0.6074f,0.784f],scale:[0f,0.26f,2.138f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}

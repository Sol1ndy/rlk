# RINGS pattern tick 37
function rlk:mboss/mv/turn {max:10}
execute at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #ph hr matches 1 run function rlk:boss/scarlet/fx/follow_on
execute if score #ph hr matches 1 at @s rotated as @s rotated ~ 0 positioned ^0.117 ^3.104 ^0.212 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute if score #ph hr matches 1 run function rlk:boss/scarlet/fx/follow_off
execute if score #ph hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute if score #ph hr matches 7 run function rlk:boss/scarlet/fx/follow_on
execute if score #ph hr matches 7 at @s rotated as @s rotated ~ 0 positioned ^0.117 ^3.104 ^0.212 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute if score #ph hr matches 7 run function rlk:boss/scarlet/fx/follow_off
execute if score #ph hr matches 7 at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5549f,1.1003f,-0.0583f],left_rotation:[-0.5997f,0.6243f,-0.3747f,0.332f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_29]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_31] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_33] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_35] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_36,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0514f,1.1798f,0.1482f],left_rotation:[-0.0155f,0.4731f,-0.1722f,0.8639f],scale:[0.8018f,0.3f,1.9285f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_36,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1232f,1.1621f,0.1647f],left_rotation:[0.1531f,0.617f,0.0803f,0.7677f],scale:[0.786f,0.3f,1.8896f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_rings","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_rings0_37","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.1526f,1.1525f,0.1521f],left_rotation:[-0.0886f,0.7005f,-0.1399f,0.6936f],scale:[0f,0.22f,1.9578f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16771496]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_rings","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_rings0_37","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.2661f,1.136f,0.1132f],left_rotation:[0.1618f,0.7753f,0.0298f,0.6097f],scale:[0f,0.22f,1.8999f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16771496]}}}}

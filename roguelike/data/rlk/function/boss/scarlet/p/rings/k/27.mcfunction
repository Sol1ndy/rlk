# RINGS pattern tick 27
function rlk:mboss/mv/turn {max:10}
execute at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ^-0.117 ^3.105 ^0.212 run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.3126f,1.1442f,0.0939f],left_rotation:[-0.5997f,-0.6243f,0.3747f,0.332f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_19]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_21] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_23] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_25] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_26,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0185f,1.1774f,0.2626f],left_rotation:[0.4731f,-0.0156f,-0.8639f,0.1722f],scale:[0.761f,0.26f,1.8308f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_26,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0383f,1.1743f,0.2607f],left_rotation:[-0.617f,-0.1531f,0.7677f,0.0803f],scale:[0.7574f,0.26f,1.8224f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_rings","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_rings0_27","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.0448f,1.172f,0.2508f],left_rotation:[0.7007f,-0.0914f,-0.6933f,0.1427f],scale:[0f,0.18f,1.8755f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16771496]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_rings","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_rings0_27","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.0708f,1.1724f,0.2368f],left_rotation:[-0.7749f,-0.1646f,0.6098f,0.0313f],scale:[0f,0.18f,1.8671f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16771496]}}}}

# MX 자광 십자참 (p_ghost.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.
scoreboard players set #done hr 0
function rlk:mboss/mv/face
scoreboard players set #mx_pre hr 0
execute at @s if entity @e[tag=rlk_body,limit=1,distance=..6] run return run function rlk:boss/scarlet/p/mx/retreat
function rlk:boss/scarlet/rig/play/mx
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_mx","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_mxb1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.2687f,0.8994f,0.279f],left_rotation:[-0.1328f,0.2385f,-0.5906f,-0.7594f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[14060543]}}}}

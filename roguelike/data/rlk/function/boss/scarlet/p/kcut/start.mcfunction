# KCUT 황광 난참 (p1.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.
scoreboard players set #done hr 0
function rlk:mboss/mv/face
function rlk:boss/scarlet/rig/play/kcut
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_kcut","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_kcutb1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.3616f,0.8574f,0.2569f],left_rotation:[-0.3851f,-0.5171f,0.593f,0.4822f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[16769354]}}}}

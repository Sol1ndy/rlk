# A1 회전 반월참 (p1.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.
scoreboard players set #done hr 0
function rlk:boss/scarlet/rig/play/a1
function rlk:mboss/mv/turn {max:60}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a1","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_a1b1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.1154f,1.0267f,0.4041f],left_rotation:[-0.0747f,-0.4969f,0.3931f,0.7701f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[16771496]}}}}

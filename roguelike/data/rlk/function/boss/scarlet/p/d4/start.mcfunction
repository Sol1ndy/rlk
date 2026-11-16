# D4 원월 사연 (p1.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.
scoreboard players set #done hr 0
function rlk:mboss/mv/face
function rlk:boss/scarlet/rig/play/d4
function rlk:boss/scarlet/rig/anchor/chest
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:1}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_d4","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_d4b1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.0463f,1.077f,0.4013f],left_rotation:[-0.0281f,-0.4723f,0.4086f,0.7805f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[16771496]}}}}

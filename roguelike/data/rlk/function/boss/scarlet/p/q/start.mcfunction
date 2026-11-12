# Q 자영 포박 · 천공 낙월 (p_ghost.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.
scoreboard players set #done hr 0
function rlk:mboss/mv/face
scoreboard players set #q_hit hr 0
function rlk:boss/scarlet/rig/play/q_grab
function rlk:boss/scarlet/rig/anchor/blade_mid
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:1}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_q","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_q0b1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.2686f,0.8502f,0.3486f],left_rotation:[-0.2144f,-0.0795f,0.3711f,-0.9f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[14060543]}}}}

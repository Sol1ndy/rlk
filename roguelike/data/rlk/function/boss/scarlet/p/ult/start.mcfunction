# ULT 공간 참 (p1.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.
scoreboard players set #done hr 0
scoreboard players set #ultq hr 0
function rlk:boss/scarlet/rig/play/ult
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/head
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/yellow_tell {t:6}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/yellow_chime
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_ult","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_ultb1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.0664f,0.9331f,0.2965f],left_rotation:[-0.018f,-0.6412f,0.4053f,0.6513f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[14060543]}}}}

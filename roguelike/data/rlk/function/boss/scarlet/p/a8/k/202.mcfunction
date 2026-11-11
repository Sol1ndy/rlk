# A8 pattern tick 202.
function rlk:boss/scarlet/rig/play/g_dive
function rlk:boss/scarlet/rig/look/form/normal
tag @s remove rlk_hr_ghost
function rlk:boss/scarlet/g/spot/dv
function rlk:mboss/mv/stop
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] positioned ~ ~3 ~ run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/rig/follow_now
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.1 ~ run function rlk:boss/scarlet/fx/p/ghost_burst
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_a8b203"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.0607f,2.1518f,0.4012f],left_rotation:[-0.7786f,0.0008f,-0.0014f,0.6276f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[14060543]}}}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_194]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_196] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_198] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"

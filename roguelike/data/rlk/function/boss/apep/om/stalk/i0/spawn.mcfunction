# stalk 0 at the execution point (its yaw from the execution rotation), hidden at leg_rise tick 0; play leg_rise next.
function rlk:boss/apep/om/stalk/i0/kill
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,32],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_stalk_low"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:2f,width:14f,height:7f,shadow_radius:0f,brightness:{block:13,sky:15},transformation:{translation:[0f,-6.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.3f,2.3f,2.3f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/stalk_low_idle"}}}
rotate 524c4b4d-4150-4800-8000-000000000020 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000020 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000020 apOC 0
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,33],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_stalk_high"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:2f,width:14f,height:7f,shadow_radius:0f,brightness:{block:13,sky:15},transformation:{translation:[0f,-3.78f,0f],left_rotation:[-0.08716f,0f,0f,0.99619f],scale:[1.8f,1.8f,1.8f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/stalk_high_idle"}}}
rotate 524c4b4d-4150-4800-8000-000000000021 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000021 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000021 apOC 0
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,34],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_stalk_tip"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:2f,width:14f,height:7f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,-1.79069f,-0.35077f],left_rotation:[-0.30071f,0f,0f,0.95372f],scale:[1.25f,1.25f,1.25f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/stalk_tip_idle"}}}
rotate 524c4b4d-4150-4800-8000-000000000022 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000022 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000022 apOC 0

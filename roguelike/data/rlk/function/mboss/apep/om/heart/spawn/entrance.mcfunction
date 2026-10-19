# The Heart of the Oasis in its entrance state at the arena centre (the floor point), rotated as wanted: E: the egg held by the vine hand at the entrance height, the cradle under the floor.
function rlk:mboss/apep/om/heart/kill
summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_ap_heart","rlk_room","rlk_mb_aux"]}
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,0],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_heart_bulb"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:3f,width:9f,height:30f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,10.12f,0f],left_rotation:[-0.70711f,0f,0f,0.70711f],scale:[0.84f,0.84f,0.84f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/heart_bulb_idle"}}}
rotate 524c4b4d-4150-4800-8000-000000000000 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000000 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000000 apOC 0
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,1],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_heart_cradle"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:3f,width:9f,height:30f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,-3.7f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/heart_cradle_pedestal"}}}
rotate 524c4b4d-4150-4800-8000-000000000001 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000001 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000001 apOC 0
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,2],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_heart_arms"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:3f,width:9f,height:30f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,-2.7f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/heart_arms_idle"}}}
rotate 524c4b4d-4150-4800-8000-000000000002 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000002 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000002 apOC 0
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,3],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_heart_tips"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:3f,width:9f,height:30f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,-2.7f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/heart_tips_idle"}}}
rotate 524c4b4d-4150-4800-8000-000000000003 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000003 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000003 apOC 0
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,4],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_vine_hand"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:3f,width:9f,height:30f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,11.36f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/vine_hand_idle"}}}
rotate 524c4b4d-4150-4800-8000-000000000004 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000004 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000004 apOC 0
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,5],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_vine_stem_0"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:3f,width:9f,height:30f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[4.6f,27.5f,2.2f],left_rotation:[0.07397f,-0.00831f,-0.11127f,0.991f],scale:[4.4f,2.6292f,4.4f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/heart_vine_stem"}}}
rotate 524c4b4d-4150-4800-8000-000000000005 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000005 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000005 apOC 0
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,6],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_vine_stem_1"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:3f,width:9f,height:30f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[3.7875f,23.9275f,1.65f],left_rotation:[0.06753f,-0.00889f,-0.13021f,0.98914f],scale:[4.4f,2.8718f,4.4f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/heart_vine_stem"}}}
rotate 524c4b4d-4150-4800-8000-000000000006 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000006 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000006 apOC 0
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,7],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_vine_stem_2"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:3f,width:9f,height:30f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[2.75f,20.055f,1.1f],left_rotation:[0.06204f,-0.00918f,-0.14609f,0.98728f],scale:[4.4f,3.11824f,4.4f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/heart_vine_stem"}}}
rotate 524c4b4d-4150-4800-8000-000000000007 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000007 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000007 apOC 0
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,8],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_vine_stem_3"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:3f,width:9f,height:30f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[1.4875f,15.8825f,0.55f],left_rotation:[0.0573f,-0.00928f,-0.15958f,0.98548f],scale:[4.4f,3.36767f,4.4f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/heart_vine_stem"}}}
rotate 524c4b4d-4150-4800-8000-000000000008 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000008 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000008 apOC 0

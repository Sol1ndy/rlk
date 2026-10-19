# dome 0 at the execution point (its yaw from the execution rotation), hidden at dome_rise tick 0; play dome_rise next.
function rlk:mboss/apep/om/dome/i0/kill
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,16],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_dome_shell"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:2f,width:10f,height:5f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.155f,0.066f,1.155f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/dome_shell_idle"}}}
rotate 524c4b4d-4150-4800-8000-000000000010 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000010 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000010 apOC 0
summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1095780352,-2147483648,17],Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_dome_decor"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:2f,width:10f,height:5f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.155f,0.066f,1.155f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/dome_decor_idle"}}}
rotate 524c4b4d-4150-4800-8000-000000000011 ~ 0
scoreboard players set 524c4b4d-4150-4800-8000-000000000011 apOI -1
scoreboard players set 524c4b4d-4150-4800-8000-000000000011 apOC 0

# One wall blade at the execution point, facing the execution yaw; it plays wall_rise now. Tag it into its group with rlk_ap_om_new right after.
tag @e[type=minecraft:item_display,tag=rlk_ap_om_new] remove rlk_ap_om_new
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_obj","rlk_mb_ap_wall_blade","rlk_ap_om_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:2f,width:2f,height:3.2f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.2f,0.1f,1.2f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/wall_blade_idle"}}}
execute as @e[type=minecraft:item_display,tag=rlk_ap_om_new,limit=1] run rotate @s ~ 0
scoreboard players set @e[type=minecraft:item_display,tag=rlk_ap_om_new,limit=1] apOI 44
scoreboard players set @e[type=minecraft:item_display,tag=rlk_ap_om_new,limit=1] apOC 0

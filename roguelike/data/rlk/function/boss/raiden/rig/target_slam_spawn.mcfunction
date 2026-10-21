# TEMPORARY (release P13): a pale palm falls onto the fixed ground point (no damage here). Positioned at the point.
tag @e[tag=rlk_rd_slam_new] remove rlk_rd_slam_new
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_slam_hand","rlk_rd_slam_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:0,view_range:2.5f,width:16f,height:20f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,7.000000f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[0.010000f,0.010000f,0.010000f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/prop/slam_palm"}}}
scoreboard players set @e[tag=rlk_rd_slam_new,limit=1] rdRigT -1
tag @e[tag=rlk_rd_slam_new] remove rlk_rd_slam_new

# Called positioned at the fixed target ground point. This helper does no damage.
tag @e[tag=rlk_rd_slam_new] remove rlk_rd_slam_new
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_slam_hand","rlk_rd_slam_new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:0,view_range:2.5f,width:16f,height:20f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,7f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/puppet_hand_open"}}}
scoreboard players set @e[tag=rlk_rd_slam_new,limit=1] rdRigT -1
tag @e[tag=rlk_rd_slam_new] remove rlk_rd_slam_new

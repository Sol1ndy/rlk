# Summons the prop vortex: switch vortex disc r 2.8 b on the floor. At the execution position, facing the execution yaw.
tag @e[tag=rlk_rd_prop_new] remove rlk_rd_prop_new
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_prop","rlk_rd_prop_vortex","rlk_rd_prop_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:3f,width:8f,height:8f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/prop/vortex"}}}
execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_rd_prop_new] ~ ~ ~ ~ 0

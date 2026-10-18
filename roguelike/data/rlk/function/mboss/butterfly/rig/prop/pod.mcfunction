# Summons the wrapped wing pod (코코볼 ball, 달빛 해제 wrap; 3.4 b tall, r 1.4 b) centred on the execution point, at the execution position and yaw.
# Tags rlk_room, rlk_mb_aux, rlk_mb_bf_prop, rlk_mb_bf_prop_pod and, for this call only, rlk_mb_bf_prop_new. Scale = the model scale.
tag @e[tag=rlk_mb_bf_prop_new] remove rlk_mb_bf_prop_new
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_prop","rlk_mb_bf_prop_pod","rlk_mb_bf_prop_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:3f,width:16f,height:16f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.5f,2.5f,2.5f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/butterfly/pod"}}}
execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_mb_bf_prop_new] ~ ~ ~ ~ 0

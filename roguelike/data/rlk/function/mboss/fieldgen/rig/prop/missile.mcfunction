# Summons a gold drill missile, 1.4 b, point down (-Y in its frame): turn it with its transformation or summon it rotated, at the execution position and yaw.
# Tags rlk_room, rlk_mb_aux, rlk_mb_fg_prop, rlk_mb_fg_prop_missile and, for this call only, rlk_mb_fg_prop_new.
tag @e[tag=rlk_mb_fg_prop_new] remove rlk_mb_fg_prop_new
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_prop","rlk_mb_fg_prop_missile","rlk_mb_fg_prop_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:3f,width:4f,height:4f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/fieldgen/missile"}}}
execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_mb_fg_prop_new] ~ ~ ~ ~ 0

# Summons the prop musou_orb: Musou crystal orb, centred. At the execution position, facing the execution yaw.
tag @e[tag=rlk_rd_prop_new] remove rlk_rd_prop_new
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_prop","rlk_rd_prop_musou_orb","rlk_rd_prop_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:3f,width:8f,height:8f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.4f,1.4f,1.4f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/prop/musou_orb"}}}
execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_rd_prop_new] ~ ~ ~ ~ 0

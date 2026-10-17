# Summons a free spear prop at the execution position/rotation, tagged rlk_mb_gd_prop + rlk_mb_gd_prop_new.
# The pattern code moves/poses it (model frame: grip at the origin, tip along +Y). Scale 2.2 = her spear.
tag @e[tag=rlk_mb_gd_prop_new] remove rlk_mb_gd_prop_new
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_prop","rlk_mb_gd_prop_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:3f,width:16f,height:16f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/guardian/prop_spear"}}}
execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_mb_gd_prop_new,limit=1] ~ ~ ~ ~ 0

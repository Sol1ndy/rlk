# pull tick 79 (@s = body, at the body).
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4cr","rlk_mb_gd_p4cb10","rlk_mb_gd_p4new"],billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,1.5f,0f],left_rotation:[0.0939f,-0.1985f,-0.0191f,0.9754f],scale:[11.0309f,11.0309f,11.0309f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:navia_fx/crescent"}}}
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run tp @e[tag=rlk_mb_gd_p4new] ~ ~ ~ ~ 0
tag @e[tag=rlk_mb_gd_p4new] remove rlk_mb_gd_p4new
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4cr","rlk_mb_gd_p4cb11","rlk_mb_gd_p4new"],billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,1.5f,0f],left_rotation:[0.0939f,-0.1985f,-0.0191f,0.9754f],scale:[8.6041f,8.6041f,8.6041f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:navia_fx/crescent"}}}
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run tp @e[tag=rlk_mb_gd_p4new] ~ ~ ~ ~ 0
tag @e[tag=rlk_mb_gd_p4new] remove rlk_mb_gd_p4new
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.3

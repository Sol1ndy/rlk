# hz_vis of the slam disc (@s = hazard marker on the floor, rotated = aim; #hzEv 0 create / 1 strike / 2 end):
# a thin gold ring decal (Navia ring card, ring at r 6 when full) that appears at 0.4 of its size,
# widens to the rim in 5 t and turns until the strike (the slam's only ground telegraph, rule 10-20).
execute if score #hzEv mb matches 0 run summon minecraft:item_display ~ ~0.04 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p3","rlk_mb_hzfx","rlk_mb_gd_p3ring"],billboard:"fixed",brightness:{sky:15,block:15},view_range:3f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,0f,0f],left_rotation:[-0.7071f,0f,0f,0.7071f],scale:[5.5814f,5.5814f,5.5814f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:navia_fx/ring"}}}
execute if score #hzEv mb matches 1.. run kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p3ring]

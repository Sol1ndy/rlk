# @s = body (on the route), rotated as the predictor: one bomb display at the port, falling next tick.
summon minecraft:item_display ^ ^4.2 ^ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p1","rlk_mb_fg_p1b","rlk_mb_fg_pnew"],teleport_duration:5,billboard:"center",brightness:{block:15,sky:15},item:{id:"minecraft:fire_charge",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbT 0
tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew
particle minecraft:flame ~ ~4 ~ 0.15 0.1 0.15 0.01 2 force @a[tag=player]

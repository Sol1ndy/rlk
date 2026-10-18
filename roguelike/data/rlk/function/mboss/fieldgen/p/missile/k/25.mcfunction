# missile clock 25
execute at @s rotated as @s positioned ^1.2 ^4.6 ^ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p4","rlk_mb_fg_p4m","rlk_mb_fg_pnew"],Rotation:[108.0f,0.0f],teleport_duration:7,billboard:"fixed",brightness:{block:15,sky:15},item:{id:"minecraft:pointed_dripstone",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[1f,0f,0f,0f],right_rotation:[0f,0f,0f,1f],scale:[1.2f,1.6f,1.2f]}}
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbT 0
scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbS = #mbGrp mb
tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew
playsound minecraft:entity.breeze.shoot hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23

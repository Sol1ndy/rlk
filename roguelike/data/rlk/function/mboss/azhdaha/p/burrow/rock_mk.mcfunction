# The rock hazard (the current group) and the rock prop 14 b up (falls 1 b/t)
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzEl mb 5
scoreboard players set #pjEl mb 5
function rlk:mboss/hz/disc {r:14,tell:14,dmg:29}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p9
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p9h
summon minecraft:item_display ~ ~14 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p9","rlk_mb_az_p9m","rlk_mb_az_p9rp","rlk_mb_az_p9rpn"],billboard:"center",teleport_duration:1,view_range:3f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.8f,1.8f,1.8f]}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p9rpn] run function rlk:mboss/azhdaha/fx/look {kind:"boulder",col:16777215}
tag @e[type=minecraft:item_display,tag=rlk_mb_az_p9rpn] remove rlk_mb_az_p9rpn

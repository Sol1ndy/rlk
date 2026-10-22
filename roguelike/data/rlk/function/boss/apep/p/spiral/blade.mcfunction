# At a lane start, rotated = the lane: its frame marker, the standing blade (kit look), the lane hazard.
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p35","rlk_mb_ap_p35x","rlk_mb_ap_p35n"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p35n] run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p35n] remove rlk_mb_ap_p35n
execute positioned ~ ~0.15 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p35","rlk_mb_ap_p35w","rlk_mb_ap_p35n"],teleport_duration:1,item:{id:"minecraft:paper",count:1}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p35n] run data merge entity @s {billboard:"vertical",view_range:2f,transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.1f,1.8f,1.1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p35n] run function rlk:boss/apep/fx/look {kind:"leaf_blade",col:15986854}
tag @e[type=minecraft:item_display,tag=rlk_mb_ap_p35n] remove rlk_mb_ap_p35n
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 7
function rlk:mboss/hz/line {len:140,w:22,tell:12,dmg:24}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p35h

setblock ~ ~ ~ minecraft:barrier
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_wallb","rlk_mb_ap_new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_ap_new] apL = #apWid mb
tag @e[type=minecraft:marker,tag=rlk_mb_ap_new] remove rlk_mb_ap_new

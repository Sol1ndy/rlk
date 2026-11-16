# icespike #azPT 67
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p45f0,limit=1] run function rlk:boss/azhdaha/fx/snd/ice_land
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p45f0,limit=1] run function rlk:boss/azhdaha/fx/p/dust_ring/4 {r:15}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p45f1,limit=1] run summon minecraft:item_display ~ ~14 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p45","rlk_mb_az_p45d1"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p45d1] run function rlk:boss/azhdaha/fx/prop/spike/4
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p45d1] run data merge entity @s {transformation:{left_rotation:[1f,0f,0f,0f]}}

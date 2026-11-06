# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# The 8 spawn points on r 12 as candidate markers (rlk_mb_ap_cand), minus those within 4 b of the player.
kill @e[type=minecraft:marker,tag=rlk_mb_ap_cand]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_cused]
summon minecraft:marker 444.59 201 -3.09 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_cand"]}
summon minecraft:marker 451.09 201 3.41 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_cand"]}
summon minecraft:marker 451.09 201 12.59 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_cand"]}
summon minecraft:marker 444.59 201 19.09 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_cand"]}
summon minecraft:marker 435.41 201 19.09 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_cand"]}
summon minecraft:marker 428.91 201 12.59 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_cand"]}
summon minecraft:marker 428.91 201 3.41 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_cand"]}
summon minecraft:marker 435.41 201 -3.09 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_cand"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_cand] at @s if entity @e[tag=rlk_body,distance=..4] run kill @s

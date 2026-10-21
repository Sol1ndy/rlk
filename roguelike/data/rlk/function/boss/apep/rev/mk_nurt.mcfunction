# The 양육: on the r 7 point (of the 8 bearings) nearest one of this wave's basics, never within 4 b of the player.
kill @e[type=minecraft:marker,tag=rlk_mb_ap_ncand]
summon minecraft:marker 442.68 201 1.53 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_ncand"]}
summon minecraft:marker 446.47 201 5.32 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_ncand"]}
summon minecraft:marker 446.47 201 10.68 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_ncand"]}
summon minecraft:marker 442.68 201 14.47 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_ncand"]}
summon minecraft:marker 437.32 201 14.47 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_ncand"]}
summon minecraft:marker 433.53 201 10.68 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_ncand"]}
summon minecraft:marker 433.53 201 5.32 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_ncand"]}
summon minecraft:marker 437.32 201 1.53 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_ncand"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_ncand] at @s if entity @e[tag=rlk_body,distance=..4] run kill @s
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn,scores={apK=1},sort=random,limit=1] at @s as @e[type=minecraft:marker,tag=rlk_mb_ap_ncand,sort=nearest,limit=1] at @s run function rlk:boss/apep/org/mark {k:2,a:-1}
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn,scores={apK=2}] as @e[type=minecraft:marker,tag=rlk_mb_ap_ncand,sort=random,limit=1] at @s run function rlk:boss/apep/org/mark {k:2,a:-1}
kill @e[type=minecraft:marker,tag=rlk_mb_ap_ncand]

# The bolt: a seed-bolt prop (kit) flying 0.75 b/t straight at the Heart 1.6 b up (pj sphere hr 0.7, life 20).
# A player in its path takes it (pj_end 4: the Heart is spared); the stage ends it near the Heart (org/bolts).
execute at @s rotated as @s rotated ~ 0 positioned ^ ^1.6 ^0.8 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_opj","rlk_mb_ap_bolt","rlk_mb_ap_new"],teleport_duration:1,billboard:"center",item:{id:"minecraft:paper",count:1}}
execute if entity @s[tag=rlk_mb_ap_buff] run tag @e[type=minecraft:item_display,tag=rlk_mb_ap_new] add rlk_mb_ap_bbuf
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_new,limit=1] run function rlk:boss/apep/fx/prop/seed_bolt
execute if entity @s[tag=rlk_mb_ap_buff] as @e[type=minecraft:item_display,tag=rlk_mb_ap_new,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet rotated ~ 0 run function rlk:boss/apep/org/basic/pj_b
execute unless entity @s[tag=rlk_mb_ap_buff] as @e[type=minecraft:item_display,tag=rlk_mb_ap_new,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet rotated ~ 0 run function rlk:boss/apep/org/basic/pj
tag @e[type=minecraft:item_display,tag=rlk_mb_ap_new] remove rlk_mb_ap_new
execute at @s run function rlk:boss/apep/fx/snd/o2_shoot

# The 파괴: on the point whose distance from the player is nearest 10 b (8-12, else 6-14, else any).
# the free points first (no basic of this wave there), else the used ones
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_ap_cand] run tag @e[type=minecraft:marker,tag=rlk_mb_ap_cused] add rlk_mb_ap_cand
tag @e[type=minecraft:marker] remove rlk_mb_ap_cpk
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_cand] at @s if entity @e[tag=rlk_body,distance=8..12] run tag @s add rlk_mb_ap_cpk
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_ap_cpk] as @e[type=minecraft:marker,tag=rlk_mb_ap_cand] at @s if entity @e[tag=rlk_body,distance=6..14] run tag @s add rlk_mb_ap_cpk
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_ap_cpk] run tag @e[type=minecraft:marker,tag=rlk_mb_ap_cand] add rlk_mb_ap_cpk
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_cpk,sort=random,limit=1] at @s run function rlk:boss/apep/rev/put_destr
tag @e[type=minecraft:marker] remove rlk_mb_ap_cpk

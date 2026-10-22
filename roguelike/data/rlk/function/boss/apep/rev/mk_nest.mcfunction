# The 둥지: on the free point nearest the player.
# the free points first (no basic of this wave there), else the used ones
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_ap_cand] run tag @e[type=minecraft:marker,tag=rlk_mb_ap_cused] add rlk_mb_ap_cand
execute at @e[tag=rlk_body,limit=1] as @e[type=minecraft:marker,tag=rlk_mb_ap_cand,sort=nearest,limit=1] at @s run function rlk:boss/apep/rev/put_nest

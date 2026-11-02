# C2 pattern tick 54
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:boss/arlecchino/fx/p/impact_burst {r:36,c:1}
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ~ ~1.4 ~ run function rlk:boss/arlecchino/fx/p/slash_arc {r:40,yaw:0,pitch:-40,roll:90,c:1}
execute at @s run function rlk:boss/arlecchino/fx/snd/impact

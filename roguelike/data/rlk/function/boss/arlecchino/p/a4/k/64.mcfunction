# A4 pattern tick 64
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ~ ~2 ~ run function rlk:boss/arlecchino/fx/p/slash_arc {r:36,yaw:0,pitch:-50,roll:90,c:1}
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2.6 run function rlk:boss/arlecchino/fx/p/impact_burst {r:22,c:1}
execute at @s run function rlk:boss/arlecchino/fx/snd/slam

# A8 pattern tick 55.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=55},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~1.2 ~ positioned ^0 ^ ^2 run function rlk:boss/scarlet/fx/p/qi_arc {r:45,yaw:0,pitch:0,roll:-40,c:1}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=55},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_leap_cut

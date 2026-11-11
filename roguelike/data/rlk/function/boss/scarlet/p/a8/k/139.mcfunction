# A8 pattern tick 139.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=139},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.8 ~ run function rlk:boss/scarlet/fx/p/qi_ring {r:22,c:1}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=139},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_ring

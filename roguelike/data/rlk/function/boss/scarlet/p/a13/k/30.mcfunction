# A13 pattern tick 30.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=30},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.8 ~ run function rlk:boss/scarlet/fx/p/qi_ring {r:22,c:1}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=30},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_ring
function rlk:boss/scarlet/g/cut/make {s:44,t:14,dmg:37,kb:0,n:1}

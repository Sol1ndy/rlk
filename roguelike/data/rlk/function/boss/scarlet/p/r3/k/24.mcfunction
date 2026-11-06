# R3 pattern tick 24.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=24},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.1 ~ run function rlk:boss/scarlet/fx/p/qi_ring {r:30,c:1}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=24},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_sweep
function rlk:boss/scarlet/g/cut/make {s:37,t:13,dmg:62,kb:3,n:0}

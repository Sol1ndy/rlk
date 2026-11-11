# A8 pattern tick 91.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=91},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.1 ~ run function rlk:boss/scarlet/fx/p/qi_ring {r:30,c:1}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=91},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_sweep
function rlk:boss/scarlet/g/cut/make {s:109,t:18,dmg:37,kb:0,n:1}

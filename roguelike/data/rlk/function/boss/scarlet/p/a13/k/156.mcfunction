# A13 pattern tick 156.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=156},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.8 ~ run function rlk:boss/scarlet/fx/p/qi_arc {r:40,yaw:0,pitch:0,roll:15,c:1}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=156},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_wrap
function rlk:boss/scarlet/g/cut/make {s:172,t:16,dmg:37,kb:0,n:1}

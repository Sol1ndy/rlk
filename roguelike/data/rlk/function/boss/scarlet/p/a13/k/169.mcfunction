# A13 pattern tick 169.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=169},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/p/qi_dome {r:35}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=169},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_dome
function rlk:boss/scarlet/g/cut/make {s:190,t:21,dmg:37,kb:0,n:1}

# A13 pattern tick 190.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=190},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/p/qi_dome {r:35}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=190},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_dome
function rlk:boss/scarlet/g/cut/make {s:206,t:16,dmg:37,kb:0,n:1}

# A13 pattern tick 40.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=40},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.3 ~ run function rlk:boss/scarlet/fx/p/qi_band {len:70,yaw:0,pitch:35,roll:0,sw:25}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=40},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_rise
function rlk:boss/scarlet/g/cut/make {s:55,t:15,dmg:42,kb:0,n:1}

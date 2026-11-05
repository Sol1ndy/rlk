# A8 pattern tick 159.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=159},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1.93 0.05 1.93 0 31 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=159},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run particle minecraft:sweep_attack ~ ~ ~ 1.4 0.05 1.4 0 3 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=159},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run particle minecraft:dust{color:[1.0,0.95,0.98],scale:1.0} ~ ~ ~ 1.6 1.4 1.6 0 24 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=159},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run playsound minecraft:item.trident.riptide_2 hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
function rlk:boss/scarlet/g/cut/make {s:174,t:15,dmg:42,kb:0,n:1}

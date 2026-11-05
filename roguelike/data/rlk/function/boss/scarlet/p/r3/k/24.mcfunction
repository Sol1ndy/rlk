# R3 pattern tick 24.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=24},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.1 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1.65 0.05 1.65 0 28 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=24},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.1 ~ run particle minecraft:sweep_attack ~ ~ ~ 1.2 0.05 1.2 0 3 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=24},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.23
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=24},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.4 1 0.13
function rlk:boss/scarlet/g/cut/make {s:37,t:13,dmg:56,kb:3,n:0}

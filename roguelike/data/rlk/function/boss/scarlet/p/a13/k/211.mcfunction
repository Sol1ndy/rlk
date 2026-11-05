# A13 pattern tick 211.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=211},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.4 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1.5 0.3 1.5 0 28 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=211},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23
function rlk:boss/scarlet/g/cut/make {s:223,t:12,dmg:42,kb:0,n:1}

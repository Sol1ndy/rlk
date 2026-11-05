# R1 pattern tick 40.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=40},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.3 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.9 1.2 0.9 0 26 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=40},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 1.1 0.23
function rlk:boss/scarlet/g/cut/make {s:55,t:15,dmg:56,kb:3,n:0}

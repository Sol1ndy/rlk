# R1 pattern tick 55.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=55},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~1.2 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1.6 0.6 1.6 0 30 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=55},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~1.2 ~ run particle minecraft:dust{color:[1.0,0.95,0.98],scale:1.0} ~ ~ ~ 1.2 0.4 1.2 0 10 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=55},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23
function rlk:boss/scarlet/rig_stub/play/g_reform

# A8 pattern tick 121.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=121},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.8 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1.21 0.05 1.21 0 23 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=121},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.8 ~ run particle minecraft:sweep_attack ~ ~ ~ 0.88 0.05 0.88 0 3 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=121},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 1.3 0.23
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=121},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.4 1 0.13

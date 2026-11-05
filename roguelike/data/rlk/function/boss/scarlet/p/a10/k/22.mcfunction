# A10 pattern tick 22
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1.4 0.2 1.4 0 36 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 201.1 ~ run particle minecraft:end_rod ~ ~ ~ 0.2 1.5 0.2 0.05 10 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run playsound minecraft:item.mace.smash_ground hostile @a[tag=player] ~ ~ ~ 0.6 1 0.2
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23

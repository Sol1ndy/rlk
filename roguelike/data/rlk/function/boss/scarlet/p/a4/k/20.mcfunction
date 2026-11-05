# A4 pattern tick 20
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1 0.1 1 0 30 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.3 1.7 0.1
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run playsound minecraft:block.amethyst_block.break hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23

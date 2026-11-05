# A9 pattern tick 28
execute at @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] positioned ~ ~1.0 ~ run particle minecraft:dust{color:[0.88,0.25,0.62],scale:1.2} ~ ~ ~ 2 0.2 0.2 0 30 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ ~1.0 ~ run particle minecraft:dust{color:[0.88,0.25,0.62],scale:1.2} ~ ~ ~ 1.6 0.05 1.6 0 24 force @a[tag=player]
execute at @s run playsound minecraft:item.trident.riptide_3 hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.2
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33

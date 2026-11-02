# Q4 stage land tick 12
execute at @s run playsound minecraft:entity.player.attack.nodamage hostile @a[tag=player] ~ ~ ~ 0.4 0.6 0.13
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.6 0.2 0.6 0 12 force @a[tag=player]

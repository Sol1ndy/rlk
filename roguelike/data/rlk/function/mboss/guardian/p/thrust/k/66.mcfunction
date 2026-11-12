# thrust clip tick 66
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.3 1.4 0.1
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.45 0.7 0.15
execute at @s rotated as @s rotated ~ 0 positioned ^1.324 ^1.203 ^1 run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:0.6} ~ ~ ~ 0.03 0.03 0.03 0 1 force @a[tag=player]

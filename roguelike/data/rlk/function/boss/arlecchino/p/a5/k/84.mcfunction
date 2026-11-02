# A5 pattern tick 84
execute at @s positioned ~ ~1 ~ run particle minecraft:flame ~ ~ ~ 2.16 0.1 2.16 0.03 30 force @a[tag=player]
execute at @s positioned ~ ~1 ~ run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 2.4 0.1 2.4 0 20 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
execute at @s run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.6 1.3 0.2

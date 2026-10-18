# missile clock 8
execute at @s run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.5} ~ ~6 ~ 0.3 1.5 0.3 0 6 force @a[tag=player]
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.8 1.2 0.27
playsound minecraft:block.vault.activate hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23

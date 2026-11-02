# E70 pattern tick 40
execute at @s run playsound minecraft:block.respawn_anchor.deplete hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
execute at @s positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.72 0.02 0.72 0 40 force @a[tag=player]

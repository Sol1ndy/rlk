# rock clock 12
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.8 0.9 0.27
execute at @s run particle minecraft:flame ~ ~5 ~ 0.6 0.3 0.6 0.02 10 force @a[tag=player]

# C5 지면 충격 (clip coreup; @s = body): disc r 12 made at 3, blast at 48.
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.8 1.4 0.27
execute at @s run particle minecraft:electric_spark ~ ~4.6 ~ 0.3 0.2 0.3 0.1 8 force @a[tag=player]

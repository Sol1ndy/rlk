# @s = body: the charge sphere at the hanging core (about 3.8 b up), pulsing.
execute at @s run particle minecraft:dust{color:[0.992f,0.984f,0.82f],scale:1.4} ~ ~3.8 ~ 0.45 0.45 0.45 0 6 force @a[tag=player]
execute at @s run particle minecraft:end_rod ~ ~3.8 ~ 0.3 0.3 0.3 0.02 1 force @a[tag=player]

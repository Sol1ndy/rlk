# Core fx crack (vanilla particles / sounds; @s = body unless noted).
execute at @s run playsound minecraft:block.amethyst_cluster.hit hostile @a[tag=player] ~ ~ ~ 1 0.9 0.33
execute at @s run particle minecraft:wax_off ~ ~3.8 ~ 0.6 0.6 0.6 0 6 force @a[tag=player]

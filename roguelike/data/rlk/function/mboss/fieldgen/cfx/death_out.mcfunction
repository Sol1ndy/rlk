# Core fx death_out (vanilla particles / sounds; @s = body unless noted).
execute at @s run playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
execute at @s run playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
execute at @s run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~1.5 ~ 2 1.2 2 0 30 force @a[tag=player]
execute at @s run particle minecraft:dust{color:[0.612f,0.525f,0.91f],scale:1.2} ~ ~1.5 ~ 2 1.2 2 0 12 force @a[tag=player]

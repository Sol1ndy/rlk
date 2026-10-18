# Core fx death_start (vanilla particles / sounds; @s = body unless noted).
execute at @s run playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
execute at @s run playsound minecraft:block.respawn_anchor.deplete hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
execute at @s run particle minecraft:electric_spark ~ ~4 ~ 1.5 0.6 1.5 0.1 12 force @a[tag=player]

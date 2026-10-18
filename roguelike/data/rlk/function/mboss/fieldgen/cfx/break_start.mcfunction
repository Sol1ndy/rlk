# Core fx break_start (vanilla particles / sounds; @s = body unless noted).
execute at @s run playsound minecraft:block.respawn_anchor.deplete hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
execute at @s run particle minecraft:end_rod ~ ~3.8 ~ 0.9 0.9 0.9 0.02 12 force @a[tag=player]

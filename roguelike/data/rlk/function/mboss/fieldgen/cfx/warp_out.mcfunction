# Core fx warp_out (vanilla particles / sounds; @s = body unless noted).
# @s = body at the old spot: the white-cyan pillar and the warp sounds.
execute at @s run particle minecraft:end_rod ~ ~1 ~ 0.2 0.4 0.2 0.02 3 force @a[tag=player]
execute at @s run particle minecraft:end_rod ~ ~3 ~ 0.2 0.4 0.2 0.02 3 force @a[tag=player]
execute at @s run particle minecraft:end_rod ~ ~5 ~ 0.2 0.4 0.2 0.02 3 force @a[tag=player]
execute at @s run particle minecraft:end_rod ~ ~7 ~ 0.2 0.4 0.2 0.02 3 force @a[tag=player]
execute at @s run playsound minecraft:block.respawn_anchor.deplete hostile @a[tag=player] ~ ~ ~ 1 1.2 0.33
execute at @s run playsound minecraft:entity.enderman.teleport hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27

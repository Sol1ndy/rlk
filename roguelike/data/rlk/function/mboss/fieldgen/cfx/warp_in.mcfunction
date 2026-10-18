# Core fx warp_in (vanilla particles / sounds; @s = body unless noted).
# @s = body at the centre: the warp-in flash.
execute at @s run particle minecraft:flash{color:[0.92,0.86,1.0,1.0]} ~ ~5 ~ 0 0 0 0 1 force @a[tag=player]
execute at @s run particle minecraft:end_rod ~ ~5 ~ 1.2 1.2 1.2 0.08 20 force @a[tag=player]
execute at @s run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute at @s run playsound minecraft:entity.enderman.teleport hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27

# Pack-up (core service 22; clip field_end; @s = body at the centre): lift-off flash, rise, lances at 22,
# the roll / pack at 50, compact at 78; the meter and low gravity ended at 0 (p/svc).
execute at @s run particle minecraft:flash{color:[1.0,0.95,0.8,1.0]} ~ ~0.5 ~ 0 0 0 0 1 force @a[tag=player]
execute at @s run particle minecraft:end_rod ~ ~0.4 ~ 1.5 0.2 1.5 0.05 16 force @a[tag=player]
playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.9 0.8 0.3
playsound minecraft:entity.breeze.wind_burst hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.27

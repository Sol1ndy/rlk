# Nova cancel (any executor; idempotent): its hazard, the swell sounds.
kill @e[type=minecraft:marker,tag=rlk_tk_nova]
stopsound @a[tag=player] hostile minecraft:block.respawn_anchor.charge
stopsound @a[tag=player] hostile minecraft:block.beacon.ambient
stopsound @a[tag=player] hostile minecraft:entity.warden.sonic_charge
stopsound @a[tag=player] hostile minecraft:block.beacon.power_select

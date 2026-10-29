# L cancel (any executor; idempotent): its hazards, markers and props, the body
# back on the floor (inside mv/ok), visible and vulnerable, the looks and the long sounds.
kill @e[tag=rlk_tk_p_l]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/tachy/p/l/u/settle
scoreboard players set #l_s tk 0
stopsound @a[tag=player] hostile minecraft:block.respawn_anchor.charge
stopsound @a[tag=player] hostile minecraft:block.beacon.ambient
stopsound @a[tag=player] hostile minecraft:entity.warden.sonic_charge
stopsound @a[tag=player] hostile minecraft:block.beacon.power_select

# The gate of cproto was pressed (@s = the object marker, at it; the zone tagged rlk_cbz): forceload again (a cancelled
# cb/won released it; the chunks load during the 30-t delay), the object goes, the zone fight starts, the gate texts.
# A press (by hand or by test/cwait) ends the test's auto press, so a gate that comes back is never pressed again for you.
scoreboard players set #cbWait mb 0
scoreboard players set #cbAuto mb 0
execute in minecraft:overworld run function rlk:mboss/ar/cp_test/fl_on
function rlk:room/obj/kill_group
execute as @e[tag=rlk_zone,tag=rlk_cbz,limit=1] at @s run function rlk:room/combat_start
tag @e[tag=rlk_cbz] remove rlk_cbz
scoreboard players set #spawnT room 30
title @a[tag=player] times 6 46 14
title @a[tag=player] subtitle {nbt:"cprep.cproto.sub",storage:"rlk:mboss",interpret:true}
title @a[tag=player] title {nbt:"cprep.cproto.title",storage:"rlk:mboss",interpret:true}
scoreboard players set @a[tag=player] vBig 66
scoreboard players set @a[tag=player] ttlT 66
execute as @a[tag=player] at @s run playsound minecraft:block.bell.resonate hostile @s ~ ~ ~ 0.7 0.6
execute as @a[tag=player] at @s run playsound minecraft:entity.warden.heartbeat hostile @s ~ ~ ~ 1 0.7

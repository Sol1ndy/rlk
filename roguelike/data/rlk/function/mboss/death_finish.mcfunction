# @s = body. Removing the last rlk_zmob lets room/combat_tick clear the zone -> mboss/won.
execute at @s run particle minecraft:poof ~ ~1 ~ 0.6 1 0.6 0.02 30 force @a[tag=player]
kill @s

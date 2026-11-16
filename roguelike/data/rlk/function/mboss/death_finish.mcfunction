# @s = body. Removing the last rlk_zmob lets room/combat_tick clear the zone -> mboss/won.
# hr FN-c: no poof for an entry with "poof": false (its record carries poof:0b; the boss left on its own, not killed)
execute unless data storage rlk:mboss cur{poof:0b} at @s run particle minecraft:poof ~ ~1 ~ 0.6 1 0.6 0.02 30 force @a[tag=player]
kill @s

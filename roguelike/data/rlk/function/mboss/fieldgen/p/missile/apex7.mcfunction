# Missile 8 (@s, at it), clock 8: to its apex (half way to the player, 16 b up, 3 b off to the
# side away from its vent) in 6 t, nose along the flight.
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/mv/dist
execute store result storage rlk:mboss fg.m4.z double 0.05 run scoreboard players get #mbDist mb
data modify storage rlk:mboss fg.m4.x set value 3
function rlk:mboss/fieldgen/p/missile/apex_at with storage rlk:mboss fg.m4
data merge entity @s {teleport_duration:6}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p4a,limit=1] feet positioned as @e[type=minecraft:marker,tag=rlk_mb_fg_p4a,limit=1] run tp @s ~ ~ ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p4a]

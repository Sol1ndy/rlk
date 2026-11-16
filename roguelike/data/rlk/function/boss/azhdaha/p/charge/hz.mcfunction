# @s = body (t12): the charge hit, a disc r 4 on the body front (f 2.5), moved onto the
# body every tick (plain tp); strike at the launch t24 (internal tell 12), active for the run;
# one hit; 158 %, Geo in every phase, heavy KB away; quiet: no lane decal (Change note 1: coil + growl).
kill @e[type=minecraft:marker,tag=rlk_mb_az_p3h]
scoreboard players set #hzAct mb 26
scoreboard players set #hzKB mb 4
scoreboard players set #hzKBDir mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzEl mb 5
scoreboard players set #pjEl mb 5
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^2.5 run function rlk:mboss/hz/disc {r:40,tell:12,dmg:158}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p3h
scoreboard players set #aq3H mb 1
scoreboard players set #aq3X mb 0

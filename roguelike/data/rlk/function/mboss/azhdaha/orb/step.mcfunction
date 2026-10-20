# @s = an orb marker: angle += omega; at the centre + r (sin, cos) of the angle (plain tp of the marker and its
# hazard); the band rides high while #azOrbHigh 1 (transitions, absorbs) or in the head-lane eye (S2-L refines).
scoreboard players operation @s azS += @s azPT
execute store result storage rlk:mboss az.ob.a float 0.01 run scoreboard players get @s azS
execute store result storage rlk:mboss az.ob.r double 0.001 run scoreboard players get @s azT
execute at @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] run function rlk:mboss/azhdaha/orb/place with storage rlk:mboss az.ob
scoreboard players operation #azX mb = @s azF
execute at @s as @e[type=minecraft:marker,tag=rlk_mb_az_orbhz] if score @s mbHzI = #azX mb run tp @s ~ ~ ~
execute if score #azOrbHigh mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_orbhz] if score @s mbHzI = #azX mb run scoreboard players set @s mbHzY0 2600

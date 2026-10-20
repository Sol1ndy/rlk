# @s = an orb marker near the anchor: the yaw anchor -> orb against the facing (#aq31Y), x 100, mod 360.
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] facing entity @s feet as @e[type=minecraft:marker,tag=rlk_mb_az_p31y,limit=1] run tp @s ~ ~ ~ ~ 0
execute store result score #aq31Q mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_az_p31y,limit=1] Rotation[0] 100
scoreboard players operation #aq31Q mb -= #aq31Y mb
scoreboard players operation #aq31Q mb %= #aq31K mb
execute if score #aq31Q mb matches ..3000 run scoreboard players set #aq31H mb 1
execute if score #aq31Q mb matches 33000.. run scoreboard players set #aq31H mb 1

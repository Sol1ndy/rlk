# Homing (@s = a live prop, at @s; from the module tick, which runs before pj/all moves the props): turn the
# flight direction toward the player's chest (body feet + 0.9 b, so the hit point 0.9 b below the prop meets the
# feet) by at most $(max) degrees in yaw and in pitch this tick; the pitch stays within +-60 degrees.
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute store result score #y0 mb run data get entity @s Rotation[0] 100
execute store result score #p0 mb run data get entity @s Rotation[1] 100
kill @e[type=minecraft:marker,tag=rlk_mb_help]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~0.9 ~ {Tags:["rlk_mb_help"]}
execute facing entity @e[type=minecraft:marker,tag=rlk_mb_help,limit=1] feet run tp @e[type=minecraft:marker,tag=rlk_mb_help,limit=1] ~ ~ ~ ~ ~
execute store result score #y1 mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_help,limit=1] Rotation[0] 100
execute store result score #p1 mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_help,limit=1] Rotation[1] 100
kill @e[type=minecraft:marker,tag=rlk_mb_help]
scoreboard players operation #y1 mb -= #y0 mb
scoreboard players add #y1 mb 90000
scoreboard players operation #y1 mb %= #c36000 mb
scoreboard players remove #y1 mb 18000
scoreboard players operation #p1 mb -= #p0 mb
$scoreboard players set #m mb $(max)
scoreboard players operation #m mb *= #c100 mb
scoreboard players operation #y1 mb < #m mb
scoreboard players operation #p1 mb < #m mb
scoreboard players operation #m mb *= #cm1 mb
scoreboard players operation #y1 mb > #m mb
scoreboard players operation #p1 mb > #m mb
scoreboard players operation #y0 mb += #y1 mb
scoreboard players operation #p0 mb += #p1 mb
scoreboard players set #m mb 6000
scoreboard players operation #p0 mb < #m mb
scoreboard players set #m mb -6000
scoreboard players operation #p0 mb > #m mb
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #y0 mb
execute store result entity @s Rotation[1] float 0.01 run scoreboard players get #p0 mb

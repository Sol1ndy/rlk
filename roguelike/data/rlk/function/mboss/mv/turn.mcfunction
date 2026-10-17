# @s turns toward the player's body by at most {max} degrees this tick (smooth tracking).
execute store result score #y0 mb run data get entity @s Rotation[0] 100
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_help"]}
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @e[tag=rlk_mb_help,limit=1] ~ ~ ~ ~ 0
execute store result score #y1 mb run data get entity @e[tag=rlk_mb_help,limit=1] Rotation[0] 100
kill @e[tag=rlk_mb_help]
scoreboard players operation #y1 mb -= #y0 mb
scoreboard players add #y1 mb 90000
scoreboard players operation #y1 mb %= #c36000 mb
scoreboard players remove #y1 mb 18000
$scoreboard players set #m mb $(max)
scoreboard players operation #m mb *= #c100 mb
execute if score #y1 mb > #m mb run scoreboard players operation #y1 mb = #m mb
scoreboard players operation #m mb *= #cm1 mb
execute if score #y1 mb < #m mb run scoreboard players operation #y1 mb = #m mb
scoreboard players operation #y0 mb += #y1 mb
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #y0 mb
data modify entity @s Rotation[1] set value 0.0f

# #aq20Y = |yaw to the player - the facing| x 100 (0 .. 18000), as rlk:mboss/mv/turn measures it.
execute store result score #aq20Y mb run data get entity @s Rotation[0] 100
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_help"]}
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @e[tag=rlk_mb_help,limit=1] ~ ~ ~ ~ 0
execute store result score #t mb run data get entity @e[tag=rlk_mb_help,limit=1] Rotation[0] 100
kill @e[type=minecraft:marker,tag=rlk_mb_help]
scoreboard players operation #t mb -= #aq20Y mb
scoreboard players add #t mb 90000
scoreboard players operation #t mb %= #c36000 mb
scoreboard players remove #t mb 18000
execute if score #t mb matches ..-1 run scoreboard players operation #t mb *= #cm1 mb
scoreboard players operation #aq20Y mb = #t mb

scoreboard players set #mbMvOn mb 1
tag @s add rlk_mb_mv
scoreboard players set @s mbMvK 1
scoreboard players set @s mbMvT 0
execute store result score @s mbMvX0 run data get entity @s Pos[0] 1000
execute store result score @s mbMvY0 run data get entity @s Pos[1] 1000
execute store result score @s mbMvZ0 run data get entity @s Pos[2] 1000
summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_help"]}
execute store result score @s mbMvX1 run data get entity @e[tag=rlk_mb_help,limit=1] Pos[0] 1000
execute store result score @s mbMvY1 run data get entity @e[tag=rlk_mb_help,limit=1] Pos[1] 1000
execute store result score @s mbMvZ1 run data get entity @e[tag=rlk_mb_help,limit=1] Pos[2] 1000
kill @e[tag=rlk_mb_help]

execute store result score #cxN tmp run data get storage rlk:codex list
scoreboard players add #cxN tmp 23
scoreboard players operation #cxN tmp /= #c24 tmp
execute if score #cxN tmp matches ..0 run scoreboard players set #cxN tmp 1
scoreboard players operation @s cxPage = #cxN tmp
scoreboard players remove @s cxPage 1

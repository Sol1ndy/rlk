# @s = moving entity (world tick, before the body tick so the module sees the new position).
scoreboard players set #mbMvOn mb 1
execute unless score @s mbMvN matches 1.. run return run function rlk:mboss/mv/stop
scoreboard players add @s mbMvT 1
scoreboard players operation #x mb = @s mbMvX1
scoreboard players operation #x mb -= @s mbMvX0
scoreboard players operation #x mb *= @s mbMvT
scoreboard players operation #x mb /= @s mbMvN
scoreboard players operation #x mb += @s mbMvX0
scoreboard players operation #y mb = @s mbMvY1
scoreboard players operation #y mb -= @s mbMvY0
scoreboard players operation #y mb *= @s mbMvT
scoreboard players operation #y mb /= @s mbMvN
scoreboard players operation #y mb += @s mbMvY0
scoreboard players operation #z mb = @s mbMvZ1
scoreboard players operation #z mb -= @s mbMvZ0
scoreboard players operation #z mb *= @s mbMvT
scoreboard players operation #z mb /= @s mbMvN
scoreboard players operation #z mb += @s mbMvZ0
execute if score @s mbMvH matches 1.. run function rlk:mboss/mv/arc
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_help"]}
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[0] double 0.001 run scoreboard players get #x mb
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[1] double 0.001 run scoreboard players get #y mb
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[2] double 0.001 run scoreboard players get #z mb
execute at @e[tag=rlk_mb_help,limit=1] run tp @s ~ ~ ~
kill @e[tag=rlk_mb_help]
execute if score @s mbMvT >= @s mbMvN run function rlk:mboss/mv/stop

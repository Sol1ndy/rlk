scoreboard players operation #pose tmp = @s cmAF
scoreboard players operation #pose tmp /= #c2c12 tmp
execute unless entity @s[tag=rlk_cmhold] run function rlk:cm/c2/walk8
execute if score @s c2T matches 1..3 if entity @e[tag=rlk_body,distance=..7] run function rlk:cm/c2/walk8
execute if score @s cmS matches 1 run function rlk:cm/cw/rig/chan
execute if score @s c3I matches 45.. run scoreboard players set #pose tmp 70
execute if score @s cmAH matches 4.. run scoreboard players set #pose tmp 40
execute if score @s cmAH matches 1..3 run scoreboard players set #pose tmp 41

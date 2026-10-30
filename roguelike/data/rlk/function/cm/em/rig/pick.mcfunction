scoreboard players operation #pose tmp = @s cmAF
scoreboard players operation #pose tmp /= #c2c12 tmp
execute unless entity @e[tag=rlk_body,distance=..2.3] if score @s c2Age matches 1.. if data entity @s {OnGround:1b} unless entity @s[tag=rlk_cmhold] run function rlk:cm/c2/walk8
execute if entity @s[tag=rlk_cmhold] if score @s c2T matches 1..3 unless entity @e[tag=rlk_body,distance=..3] run function rlk:cm/c2/walk8
execute if score @s cmAR matches 12.. run scoreboard players set #pose tmp 30
execute if score @s cmAR matches 1..11 run scoreboard players set #pose tmp 31
execute if score @s cmS matches 1 if score @s cmT matches 8.. run scoreboard players set #pose tmp 20
execute if score @s cmS matches 1 if score @s cmT matches ..7 run scoreboard players set #pose tmp 21
execute if score @s cmS matches 2 if score @s cmT matches 3.. run scoreboard players set #pose tmp 24
execute if score @s cmS matches 2 if score @s cmT matches ..2 run scoreboard players set #pose tmp 25
execute if score @s cmAH matches 4.. run scoreboard players set #pose tmp 40
execute if score @s cmAH matches 1..3 run scoreboard players set #pose tmp 41

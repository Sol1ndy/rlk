scoreboard players set #pose tmp 90
execute if score @s c3B matches 1 run scoreboard players operation #pose tmp = @s c2T
execute if score @s c3B matches 1 run scoreboard players operation #pose tmp %= #c3c4 tmp
execute if score @s c3B matches 1 if score #pose tmp matches 0..1 run scoreboard players set #pose tmp 80
execute if score @s c3B matches 1 if score #pose tmp matches 2..3 run scoreboard players set #pose tmp 81
execute if score @s c3B matches 2 run function rlk:cm/sb/rig/pick_up
execute if score @s c3B matches 3 run scoreboard players set #pose tmp 85

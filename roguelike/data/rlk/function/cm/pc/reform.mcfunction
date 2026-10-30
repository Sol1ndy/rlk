# 10 t: the cubes stream in and glow at the spot; then the attack tell
scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
particle minecraft:dust{color:[1.0,0.86,0.45],scale:1.3} ~ ~1.2 ~ 0.45 0.7 0.45 0 5
particle minecraft:end_rod ~ ~0.15 ~ 0.6 0.02 0.6 0.01 2
execute if score @s cmT matches 8 run execute rotated 0 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 8 run execute rotated 36 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 8 run execute rotated 72 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 8 run execute rotated 108 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 8 run execute rotated 144 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 8 run execute rotated 180 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 8 run execute rotated 216 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 8 run execute rotated 252 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 8 run execute rotated 288 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 8 run execute rotated 324 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 4 run execute rotated 0 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 4 run execute rotated 36 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 4 run execute rotated 72 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 4 run execute rotated 108 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 4 run execute rotated 144 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 4 run execute rotated 180 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 4 run execute rotated 216 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 4 run execute rotated 252 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 4 run execute rotated 288 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 4 run execute rotated 324 0 positioned ^ ^0.1 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches ..0 run function rlk:cm/pc/pick

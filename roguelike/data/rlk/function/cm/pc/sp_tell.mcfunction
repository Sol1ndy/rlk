scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute store result score #c2t tmp run scoreboard players get @s cmT
scoreboard players operation #c2t tmp %= #2 tmp
execute if score #c2t tmp matches 0 run execute rotated 0 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 22 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 45 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 67 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 90 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 112 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 135 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 157 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 180 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 202 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 225 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 247 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 270 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 292 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 315 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 337 0 positioned ^ ^0.1 ^3.0 run particle minecraft:dust{color:[0.55,0.95,0.9],scale:1.3} ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches ..0 run function rlk:cm/pc/sp_hit

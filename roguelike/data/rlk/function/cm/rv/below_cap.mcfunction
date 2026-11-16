execute store result score #y tmp run data get entity @s Pos[1] 100
scoreboard players add #y tmp 30
execute if score #y tmp > @s cmVy run return 0
return 1

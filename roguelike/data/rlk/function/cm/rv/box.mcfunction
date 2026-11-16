# @s = new brain at its spawn spot. Fallback (no fight zone around it, e.g. a test spawn): +-14 b, spawn + 7 b
execute store result score #px tmp run data get entity @s Pos[0] 100
execute store result score #py tmp run data get entity @s Pos[1] 100
execute store result score #pz tmp run data get entity @s Pos[2] 100
scoreboard players operation @s cmAX = #px tmp
scoreboard players remove @s cmAX 1400
scoreboard players operation @s cmVx = #px tmp
scoreboard players add @s cmVx 1400
scoreboard players operation @s cmAZ = #pz tmp
scoreboard players remove @s cmAZ 1400
scoreboard players operation @s cmVz = #pz tmp
scoreboard players add @s cmVz 1400
scoreboard players operation @s cmVy = #py tmp
scoreboard players add @s cmVy 700
scoreboard players set #bOk tmp 0
execute if score #active room matches 1 as @e[tag=rlk_zone] if score @s zid = #combat room run function rlk:cm/rv/box_zone
execute if score #bOk tmp matches 1 run function rlk:cm/rv/box_set

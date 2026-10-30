scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.25 ~ 0.6 0.15 0.6 0 8
execute store result score #c2t tmp run scoreboard players get @s cmT
scoreboard players operation #c2t tmp %= #2 tmp
execute if score #c2t tmp matches 0 run execute rotated 0 0 positioned ^ ^0.1 ^1.8 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 36 0 positioned ^ ^0.1 ^1.8 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 72 0 positioned ^ ^0.1 ^1.8 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 108 0 positioned ^ ^0.1 ^1.8 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 144 0 positioned ^ ^0.1 ^1.8 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 180 0 positioned ^ ^0.1 ^1.8 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 216 0 positioned ^ ^0.1 ^1.8 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 252 0 positioned ^ ^0.1 ^1.8 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 288 0 positioned ^ ^0.1 ^1.8 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~ ~ 0.02 0 0.02 0 1
execute if score #c2t tmp matches 0 run execute rotated 324 0 positioned ^ ^0.1 ^1.8 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~ ~ 0.02 0 0.02 0 1
execute if score @s cmT matches 4 run playsound minecraft:block.sand.break master @a ~ ~ ~ 1 0.5
execute if score @s cmT matches ..0 run function rlk:cm/cs/erupt

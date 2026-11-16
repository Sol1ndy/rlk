scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute store result score #c2t tmp run scoreboard players get @s cmT
scoreboard players operation #c2t tmp %= #3 tmp
execute if score #c2t tmp matches 0 run particle minecraft:cloud ~ ~2 ~ 0.25 0.2 0.25 0.03 2
execute if score #c2t tmp matches 0 run particle minecraft:flame ~ ~1.45 ~ 0.25 0.25 0.25 0.01 2
execute if score @s cmT matches 15 run playsound minecraft:block.lava.extinguish master @a ~ ~ ~ 0.6 1.2
execute if score @s cmT matches ..0 run function rlk:cm/pc/oh_end

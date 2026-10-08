scoreboard players set @s nfDewT 0
execute if score @s nfDew matches 3.. run return 0
scoreboard players add @s nfDew 1
playsound minecraft:block.amethyst_block.resonate master @s ~ ~ ~ 0.7 1.8
playsound minecraft:block.bubble_column.upwards_ambient master @s ~ ~ ~ 0.4 1.6

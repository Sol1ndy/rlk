scoreboard players set @s c3B 3
scoreboard players set @s c2T 6
scoreboard players set @s c2T2 -1
particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.2 ~ 0.3 0.1 0.3 0.1 12 normal
execute unless score #c3sbsink snd matches 1 run function rlk:cm/c3/snd/sbsink

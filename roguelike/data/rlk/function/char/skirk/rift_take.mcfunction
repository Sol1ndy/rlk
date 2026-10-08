scoreboard players add #skAbs tmp 1
scoreboard players operation @a[tag=player,limit=1] energy += #skRiftGain tmp
particle minecraft:witch ~ ~ ~ 0.2 0.2 0.2 0.1 12
kill @s

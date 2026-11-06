# exhausted: 30 t standing, staggerable (the punish window)
scoreboard players set @s cmS 4
scoreboard players set @s cmT 30
scoreboard players set @s cmN 0
tag @s remove rlk_cmch
particle minecraft:cloud ^ ^1.4 ^0.4 0.05 0.05 0.05 0.01 3
playsound minecraft:entity.player.breath master @a ~ ~ ~ 1 0.9

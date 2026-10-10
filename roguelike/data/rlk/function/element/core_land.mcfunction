scoreboard players set @s cF 0
execute at @s run particle minecraft:composter ~ ~0.15 ~ 0.2 0.05 0.2 0 8
execute at @s unless score #k35 snd matches 1 run function rlk:snd/f37

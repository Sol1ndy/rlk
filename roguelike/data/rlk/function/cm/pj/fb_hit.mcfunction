function rlk:cm/hit_pj
particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.06 14
particle minecraft:lava ~ ~ ~ 0.2 0.2 0.2 0 3
execute unless score #k81 snd matches 1 run function rlk:snd/f87
kill @s

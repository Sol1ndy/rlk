# at the body: keep the hazard on its own floor height
execute store result score #rdOY rd run data get entity @s Pos[1] 1000
tp @s ~ ~ ~
execute store result entity @s Pos[1] double 0.001 run scoreboard players get #rdOY rd

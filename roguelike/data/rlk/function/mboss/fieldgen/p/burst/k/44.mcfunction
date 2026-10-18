# burst clock 44
execute at @s positioned ~ 201 ~ rotated ~ 0 run function rlk:mboss/fieldgen/fx/p/floor_hit
execute at @s positioned ~ 201 ~ rotated ~ 0 run playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 0.7 0.9 0.23
execute at @s positioned ~ 201 ~ rotated ~ 0 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.4 1.3 0.13

# @s = a wall piece on its strike (at the tail root, rotated to the piece's mid angle): ice walls.
execute positioned ^ ^ ^6.5 run function rlk:mboss/azhdaha/fx/p/ice_wall
execute positioned ^ ^ ^10 run function rlk:mboss/azhdaha/fx/p/ice_wall
playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.27
playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27

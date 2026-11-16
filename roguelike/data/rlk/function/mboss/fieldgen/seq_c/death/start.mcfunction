# S4 death clip tick 0 (@s = body; the core cancelled the pattern, cleared the decals and the HUD flags): the
# first flicker of the dying seam, the power-down.
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/p/death_flicker
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/snd/death

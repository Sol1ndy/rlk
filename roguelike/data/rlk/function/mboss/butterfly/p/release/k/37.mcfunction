# release clock 37
# the cyan X glint through her chest
execute rotated as @s rotated ~ 0 positioned ^0 ^5.022 ^0.3 run function rlk:mboss/butterfly/fx/p/rel_xglint
execute rotated as @s rotated ~ 0 positioned ^0 ^5.022 ^0.3 run particle minecraft:end_rod ~ ~ ~ 0.6 0.6 0.6 0.05 6 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/release_charge
playsound minecraft:block.amethyst_cluster.hit hostile @a[tag=player] ~ ~ ~ 0.8 1.9 0.27

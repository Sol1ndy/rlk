# A13 pattern tick 194.
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.35 0.7 0.35 0.02 16 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run particle minecraft:end_rod ~ ~ ~ 0.25 0.6 0.25 0.04 4 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run particle minecraft:dust{color:[1.0,0.95,0.98],scale:1.0} ~ ~ ~ 0.77 0.05 0.77 0 18 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run particle minecraft:sweep_attack ~ ~ ~ 0.56 0.05 0.56 0 3 force @a[tag=player]
function rlk:boss/scarlet/rig/state/hidden

# [c_rocks] @s = a waiting slab, at it: its clock mbT (-10 at the decal, 0 at the burst); it rises at 2, then
# drips tuff dust every 4 t while it hovers.
scoreboard players add @s mbT 1
execute if score @s mbT matches 2 run return run function rlk:mboss/fieldgen/p/rock/rk_rise
scoreboard players operation #fgM mb = @s mbT
scoreboard players operation #fgM mb %= #fgK4 mb
execute if score @s mbT matches 3.. if score #fgM mb matches 0 run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~-0.3 ~ 0.5 0.1 0.5 0 1 force @a[tag=player]

# The edge changes (swap event): the new element, its burst.
function rlk:boss/tachy/el/flip
execute if score #el tk matches 1 at @s run particle minecraft:flame ~ ~1.2 ~ 0.4 0.6 0.4 0.05 24 force @a[tag=player]
execute if score #el tk matches 3 at @s run particle minecraft:electric_spark ~ ~1.2 ~ 0.4 0.6 0.4 0.05 24 force @a[tag=player]

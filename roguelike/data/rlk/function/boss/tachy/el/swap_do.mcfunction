# The edge changes (swap event): the new element, its burst.
function rlk:boss/tachy/el/flip
execute if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/swap_fx {el:1}
execute if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/swap_fx {el:3}

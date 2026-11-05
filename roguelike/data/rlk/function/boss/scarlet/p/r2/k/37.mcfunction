# R2 pattern tick 37.
execute if score #r2_two hr matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run function rlk:boss/scarlet/fx/p/qi_ring {r:12,c:1}
execute unless score #r2_two hr matches 1 run function rlk:mboss/mv/turn {max:10}

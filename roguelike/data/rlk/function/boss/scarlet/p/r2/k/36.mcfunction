# R2 pattern tick 36.
execute if score #r2_two hr matches 1 at @s rotated as @s rotated ~ 0 positioned ^0.6 ^0.15 ^0.4 run function rlk:boss/scarlet/fx/p/qi_vert {h:19,yaw:0,c:1}
execute unless score #r2_two hr matches 1 run function rlk:mboss/mv/turn {max:10}

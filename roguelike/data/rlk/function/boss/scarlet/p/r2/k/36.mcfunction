# R2 pattern tick 36.
execute if score #r2_two hr matches 1 at @s rotated as @s rotated ~ 0 positioned ^0.6 ^0.2 ^0.4 run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.2 1 0.2 0 16 force @a[tag=player]
execute unless score #r2_two hr matches 1 run function rlk:mboss/mv/turn {max:10}

# R2 pattern tick 37.
execute if score #r2_two hr matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.66 0.05 0.66 0 17 force @a[tag=player]
execute if score #r2_two hr matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run particle minecraft:sweep_attack ~ ~ ~ 0.48 0.05 0.48 0 3 force @a[tag=player]
execute unless score #r2_two hr matches 1 run function rlk:mboss/mv/turn {max:10}

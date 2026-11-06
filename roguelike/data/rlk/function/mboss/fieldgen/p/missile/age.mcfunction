# @s = a missile, at it: its clock mbT; up 7 b (1), the apex (8), the lock (14), the dive (15), the impact (28); the
# smoke trail every 3 t.
scoreboard players add @s mbT 1
execute if score @s mbT matches 1 run tp @s ~ ~7 ~
execute if score @s mbT matches 8 run function rlk:mboss/fieldgen/p/missile/apex_d
execute if score @s mbT matches 14 run function rlk:mboss/fieldgen/p/missile/lock_d
execute if score @s mbT matches 15 run function rlk:mboss/fieldgen/p/missile/dive_d
execute if score @s mbT matches 28.. run return run function rlk:mboss/fieldgen/p/missile/hit_d
scoreboard players operation #fgM mb = @s mbT
scoreboard players operation #fgM mb %= #fgK3 mb
execute if score #fgM mb matches 0 run function rlk:mboss/fieldgen/fx/p/missile_trail

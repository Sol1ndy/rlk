# @s = a marker on the floor: 0.5 b toward the arena centre until mv/ok passes there (at most 60 steps).
execute if function rlk:mboss/mv/ok run return 0
scoreboard players add #t4 kn 1
execute if score #t4 kn matches 60.. run return 0
execute facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~
execute at @s run function rlk:boss/arlecchino/core/clamp

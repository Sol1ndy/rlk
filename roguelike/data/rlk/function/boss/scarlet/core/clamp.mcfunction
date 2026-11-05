# @s = a marker on the floor: 0.5 b toward the arena axis until mv/ok passes there (at most 60 steps; the
# guaranteed fallback is the axis itself).
execute if function rlk:mboss/mv/ok run return 1
scoreboard players add #t4 hr 1
execute if score #t4 hr matches 60.. run return 0
execute facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~
execute at @s run function rlk:boss/scarlet/core/clamp

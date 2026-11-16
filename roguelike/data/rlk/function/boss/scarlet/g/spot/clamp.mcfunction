# @s = the spot marker on the floor: 0.5 b toward the arena axis until mv/ok passes (at most 60 steps, then the axis
# C itself): the guaranteed fallback never stands in a block or outside MOVE_R.
execute if function rlk:mboss/mv/ok run return 1
scoreboard players add #g_c hr 1
execute if score #g_c hr matches 60.. at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run return run tp @s ~ ~ ~
execute facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~
execute at @s run function rlk:boss/scarlet/g/spot/clamp

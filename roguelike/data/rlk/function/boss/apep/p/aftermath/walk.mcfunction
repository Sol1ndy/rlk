# @s = body (the approach): one 0.4 b step toward the centre and a turn toward it (<= 12 deg/t).
execute at @s unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..0.25,limit=1] run execute facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.4 run function rlk:boss/apep/u/step_here
function rlk:boss/apep/p/aftermath/turn_c

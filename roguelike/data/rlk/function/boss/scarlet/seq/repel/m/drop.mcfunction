# R0 her place at tick 0: 1 b above ST(0, 0, 1.0), the dive's end (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^0 ^1 if function rlk:boss/scarlet/seq/lib/ok run return run tp @s ~ ~1 ~

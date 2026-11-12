# @s = the body: back on the floor at once if airborne (a cancelled leap / hang): the spot below when mv/ok, else C.
execute if entity @s[tag=rlk_mb_mv] run function rlk:mboss/mv/stop
execute store result score #g_y hr run data get entity @s Pos[1] 100
execute if score #g_y hr matches ..20104 run return 0
execute at @s positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/core/ground_to
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:boss/scarlet/core/ground_to

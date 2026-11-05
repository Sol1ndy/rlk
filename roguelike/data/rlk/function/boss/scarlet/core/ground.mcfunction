# Back on the floor at once if airborne (a cancelled leap; @s = body): the spot below when mv/ok, else C.
function rlk:boss/scarlet/core/stop_move
execute store result score #t hr run data get entity @s Pos[1] 100
execute if score #t hr matches ..20104 run return 0
execute at @s positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run tp @s ~ ~ ~

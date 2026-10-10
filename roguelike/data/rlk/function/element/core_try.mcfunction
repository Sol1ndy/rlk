execute if score #cpOk tmp matches 1 run return 0
execute store result storage rlk:cf d double 0.1 run random value 16..24
execute at @e[tag=rlk_cpo,limit=1] rotated as @e[tag=rlk_cpo,limit=1] run function rlk:element/core_try_at with storage rlk:cf
execute as @e[tag=rlk_cpo] at @s run tp @s ~ ~ ~ ~90 ~

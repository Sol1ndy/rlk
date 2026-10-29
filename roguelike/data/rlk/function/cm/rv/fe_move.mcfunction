execute at @s positioned ^ ^ ^0.35 unless block ~ ~ ~ #rlk:dash_pass run return run function rlk:cm/rv/fe_wall
execute at @s run tp @s ^ ^ ^0.35
execute at @s if entity @e[tag=rlk_cmaim,distance=..0.8] run return run function rlk:cm/rv/fe_hit
scoreboard players remove #c2s tmp 1
execute if score #c2s tmp matches 1.. run function rlk:cm/rv/fe_move

# 벽에 맞았거나 수명이 다함 (@s = 투사체)
scoreboard players set #jend tmp 1
execute if score @s aKind matches 8 run return run function rlk:char/ronova/echo_boom
execute at @s run particle minecraft:crit ~ ~ ~ 0.1 0.1 0.1 0.1 4
execute at @s unless block ~ ~ ~ #rlk:dash_pass unless score #k229 snd matches 1 run function rlk:snd/f256
kill @s

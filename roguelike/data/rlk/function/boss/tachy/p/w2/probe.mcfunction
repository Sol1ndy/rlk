# The dive probe (@s = marker on the floor, rotated toward the lock): 0.5 b steps while the next spot passes mv/ok,
# at most 28 (14.0 b), stopping 1.5 b short of the locked point.
execute if score #w2_n tk matches 28.. run return 0
execute if entity @e[type=minecraft:marker,tag=rlk_tk_w2lock,distance=..1.5] run return 0
execute positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0
execute positioned ^ ^ ^0.5 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
scoreboard players add #w2_n tk 1
execute at @s run function rlk:boss/tachy/p/w2/probe

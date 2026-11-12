# @s = the landing marker: one 0.5-b step along its yaw while the player is > 3 b ahead (<= 20 steps).
execute if entity @e[tag=rlk_body,distance=..3] run return 0
scoreboard players add #aq2N mb 1
execute if score #aq2N mb matches 21.. run return 0
execute rotated as @s positioned ^ ^ ^0.5 run tp @s ~ ~ ~
execute at @s run function rlk:boss/azhdaha/p/jump/lstep

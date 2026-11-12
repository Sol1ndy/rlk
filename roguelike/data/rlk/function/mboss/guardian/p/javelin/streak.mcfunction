# @s = body, at A rotated along the lane: the hot streak, a step every 0.5 b up to #gp2Len.
particle minecraft:dust{color:[0.992f,0.957f,0.584f],scale:1.8} ~ ~ ~ 0.06 0.06 0.12 0 2 force @a[tag=player]
scoreboard players operation #gp2M mb = #gp2S mb
scoreboard players operation #gp2M mb %= #c10 mb
execute if score #gp2M mb matches 0 run particle minecraft:end_rod ~ ~ ~ 0.05 0.05 0.1 0.01 1 force @a[tag=player]
scoreboard players add #gp2S mb 5
execute if score #gp2S mb < #gp2Len mb positioned ^ ^ ^0.5 run function rlk:mboss/guardian/p/javelin/streak

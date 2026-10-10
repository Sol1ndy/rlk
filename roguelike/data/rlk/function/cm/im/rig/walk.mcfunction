scoreboard players operation #imFrame tmp = @s cmAF
scoreboard players set #imDiv tmp 24
scoreboard players operation #imFrame tmp %= #imDiv tmp
scoreboard players set #imDiv tmp 3
scoreboard players operation #imFrame tmp /= #imDiv tmp
scoreboard players operation #imPose tmp = #imFrame tmp
scoreboard players add #imPose tmp 10

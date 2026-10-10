scoreboard players operation #swFrame tmp = @s cmAF
scoreboard players set #swDiv tmp 24
scoreboard players operation #swFrame tmp %= #swDiv tmp
scoreboard players set #swDiv tmp 3
scoreboard players operation #swFrame tmp /= #swDiv tmp
scoreboard players operation #swPose tmp = #swFrame tmp
scoreboard players add #swPose tmp 10

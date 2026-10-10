scoreboard players operation #shFrame tmp = @s cmAF
scoreboard players set #shDiv tmp 24
scoreboard players operation #shFrame tmp %= #shDiv tmp
scoreboard players set #shDiv tmp 3
scoreboard players operation #shFrame tmp /= #shDiv tmp
scoreboard players operation #shPose tmp = #shFrame tmp
scoreboard players add #shPose tmp 10

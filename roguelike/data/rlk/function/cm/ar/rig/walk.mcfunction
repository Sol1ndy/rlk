scoreboard players operation #arFrame tmp = @s cmAF
scoreboard players set #arDiv tmp 24
scoreboard players operation #arFrame tmp %= #arDiv tmp
scoreboard players set #arDiv tmp 3
scoreboard players operation #arFrame tmp /= #arDiv tmp
scoreboard players operation #arPose tmp = #arFrame tmp
scoreboard players add #arPose tmp 10

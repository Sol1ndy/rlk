scoreboard players operation #fmFrame tmp = @s cmAF
scoreboard players set #fmDiv tmp 24
scoreboard players operation #fmFrame tmp %= #fmDiv tmp
scoreboard players set #fmDiv tmp 3
scoreboard players operation #fmFrame tmp /= #fmDiv tmp
scoreboard players operation #fmPose tmp = #fmFrame tmp
scoreboard players add #fmPose tmp 10

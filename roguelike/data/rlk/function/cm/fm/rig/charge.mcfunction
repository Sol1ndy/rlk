# Raised arms, then an original eight-keyframe overhead staff circle.
scoreboard players operation #fmElapsed tmp = #cmW_fm tmp
scoreboard players operation #fmElapsed tmp -= @s cmT
scoreboard players operation #fmPhase tmp = #fmElapsed tmp
scoreboard players set #fmDiv tmp 100
scoreboard players operation #fmPhase tmp *= #fmDiv tmp
scoreboard players operation #fmDiv tmp = #cmW_fm tmp
execute if score #fmDiv tmp matches ..0 run scoreboard players set #fmDiv tmp 1
scoreboard players operation #fmPhase tmp /= #fmDiv tmp
scoreboard players operation #fmFrame tmp = #fmElapsed tmp
scoreboard players set #fmDiv tmp 16
scoreboard players operation #fmFrame tmp %= #fmDiv tmp
scoreboard players set #fmDiv tmp 2
scoreboard players operation #fmFrame tmp /= #fmDiv tmp
scoreboard players operation #fmPose tmp = #fmFrame tmp
scoreboard players add #fmPose tmp 23
execute if score #fmPhase tmp matches ..12 run scoreboard players set #fmPose tmp 20
execute if score #fmPhase tmp matches 13..27 run scoreboard players set #fmPose tmp 21
execute if score #fmPhase tmp matches 28..38 run scoreboard players set #fmPose tmp 22

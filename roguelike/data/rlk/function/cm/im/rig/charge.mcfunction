# Raised arms, then an original eight-keyframe overhead staff circle.
scoreboard players operation #imElapsed tmp = #cmW_im tmp
scoreboard players operation #imElapsed tmp -= @s cmT
scoreboard players operation #imPhase tmp = #imElapsed tmp
scoreboard players set #imDiv tmp 100
scoreboard players operation #imPhase tmp *= #imDiv tmp
scoreboard players operation #imDiv tmp = #cmW_im tmp
execute if score #imDiv tmp matches ..0 run scoreboard players set #imDiv tmp 1
scoreboard players operation #imPhase tmp /= #imDiv tmp
scoreboard players operation #imFrame tmp = #imElapsed tmp
scoreboard players set #imDiv tmp 16
scoreboard players operation #imFrame tmp %= #imDiv tmp
scoreboard players set #imDiv tmp 2
scoreboard players operation #imFrame tmp /= #imDiv tmp
scoreboard players operation #imPose tmp = #imFrame tmp
scoreboard players add #imPose tmp 23
execute if score #imPhase tmp matches ..12 run scoreboard players set #imPose tmp 20
execute if score #imPhase tmp matches 13..27 run scoreboard players set #imPose tmp 21
execute if score #imPhase tmp matches 28..38 run scoreboard players set #imPose tmp 22
execute if score @s cmT matches 3..5 run scoreboard players set #imPose tmp 31
execute if score @s cmT matches 1..2 run scoreboard players set #imPose tmp 32

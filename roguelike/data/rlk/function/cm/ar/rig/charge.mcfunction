# Normalize draw progression to the configured attack windup.
scoreboard players operation #arElapsed tmp = #cmW_ar tmp
scoreboard players operation #arElapsed tmp -= @s cmT
scoreboard players set #arDiv tmp 100
scoreboard players operation #arElapsed tmp *= #arDiv tmp
scoreboard players operation #arDiv tmp = #cmW_ar tmp
execute if score #arDiv tmp matches ..0 run scoreboard players set #arDiv tmp 1
scoreboard players operation #arElapsed tmp /= #arDiv tmp
scoreboard players set #arPose tmp 23
execute if score #arElapsed tmp matches ..19 run scoreboard players set #arPose tmp 20
execute if score #arElapsed tmp matches 20..39 run scoreboard players set #arPose tmp 21
execute if score #arElapsed tmp matches 40..64 run scoreboard players set #arPose tmp 22
execute if score @s cmT <= #cmW_arL tmp run scoreboard players set #arPose tmp 24

# Normalize the five anticipation stages to configured fuse duration.
scoreboard players operation #cnWind tmp = @s cmT
scoreboard players set #cnDiv tmp 5
scoreboard players operation #cnWind tmp *= #cnDiv tmp
scoreboard players operation #cnDiv tmp = #cmW_cn tmp
execute if score #cnDiv tmp matches ..0 run scoreboard players set #cnDiv tmp 1
scoreboard players operation #cnWind tmp /= #cnDiv tmp
scoreboard players set #cnPose tmp 14
execute if score #cnWind tmp matches 4.. run scoreboard players set #cnPose tmp 10
execute if score #cnWind tmp matches 3 run scoreboard players set #cnPose tmp 11
execute if score #cnWind tmp matches 2 run scoreboard players set #cnPose tmp 12
execute if score #cnWind tmp matches 1 run scoreboard players set #cnPose tmp 13

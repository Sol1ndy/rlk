scoreboard players operation #shPhase tmp = @s cmT
scoreboard players set #shDiv tmp 3
scoreboard players operation #shPhase tmp *= #shDiv tmp
scoreboard players operation #shPhase tmp /= #cmW_sh tmp
scoreboard players set #shPose tmp 21
execute if score #shPhase tmp matches 2.. run scoreboard players set #shPose tmp 20
execute if score @s cmT matches 3..5 run scoreboard players set #shPose tmp 22
execute if score @s cmT matches 1..2 run scoreboard players set #shPose tmp 23

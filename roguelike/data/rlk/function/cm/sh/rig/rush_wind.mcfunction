scoreboard players operation #shPhase tmp = @s cmT
scoreboard players set #shDiv tmp 3
scoreboard players operation #shPhase tmp *= #shDiv tmp
scoreboard players operation #shPhase tmp /= #cmW_shR tmp
scoreboard players set #shPose tmp 31
execute if score #shPhase tmp matches 2.. run scoreboard players set #shPose tmp 30
execute if score @s cmT matches 1..5 run scoreboard players set #shPose tmp 32

# Normalize anticipation to the configured windup; last two ticks always approach contact.
scoreboard players operation #swWind tmp = @s cmT
scoreboard players remove #swWind tmp 4
scoreboard players set #swThree tmp 3
scoreboard players operation #swWind tmp *= #swThree tmp
scoreboard players operation #swDiv tmp = #cmW_sw tmp
scoreboard players remove #swDiv tmp 3
execute if score #swDiv tmp matches ..0 run scoreboard players set #swDiv tmp 1
scoreboard players operation #swWind tmp /= #swDiv tmp
scoreboard players set #swPose tmp 22
execute if score #swWind tmp matches 2.. run scoreboard players set #swPose tmp 20
execute if score #swWind tmp matches 1 run scoreboard players set #swPose tmp 21
execute if score @s cmT matches 3 run scoreboard players set #swPose tmp 23
execute if score @s cmT matches 1..2 run scoreboard players set #swPose tmp 24

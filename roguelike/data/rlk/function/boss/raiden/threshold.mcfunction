scoreboard players operation #dmg tmp = @s mhpC
scoreboard players operation #dmg tmp -= #rdFloor rd
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 0
scoreboard players set @s rdRage 900

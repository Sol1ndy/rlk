# Restart the put-away countdown (#pmShDelay ticks, or the character sheath.delay).
scoreboard players operation @s pmShT = #pmShDelay tmp
execute if score #charN tmp matches 5 run scoreboard players set @s pmShT 100
execute if score #charN tmp matches 3 run scoreboard players set @s pmShT 100
execute if score #charN tmp matches 6 run scoreboard players set @s pmShT 100

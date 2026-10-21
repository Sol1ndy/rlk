scoreboard players operation #rdSx rd = @s rdHB
scoreboard players operation #rdSx rd += @s rdHB
scoreboard players operation #rdSz rd = @s rdHA
execute if score @s rdHK matches 3..4 store result storage rlk:rd v.tz float 0.001 run scoreboard players get @s rdHC

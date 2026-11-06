# macro: k = 능력치 키
$execute store result score #sv tmp run data get storage rlk:io src.stats.$(k)
scoreboard players operation #sv tmp *= #fA tmp
scoreboard players operation #sv tmp += #500 tmp
scoreboard players operation #sv tmp /= #1000 tmp
$execute store result storage rlk:io src.stats.$(k) int 1 run scoreboard players get #sv tmp

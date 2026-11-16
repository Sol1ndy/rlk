# items/scan_add_prep 에서 (정의에 elemMastery 가 있을 때): eqElemMastery += (값 × #cntF + 500) / 1000
execute store result score #v tmp run data get storage rlk:scan def.stats.elemMastery
scoreboard players operation #v tmp *= #cntF tmp
scoreboard players operation #v tmp += #500 tmp
scoreboard players operation #v tmp /= #1000 tmp
scoreboard players operation @s eqElemMastery += #v tmp

# items/scan_add_prep 에서 (정의에 hpFlat 가 있을 때): eqHpFlat += (값 × #cntF + 500) / 1000
execute store result score #v tmp run data get storage rlk:scan def.stats.hpFlat
scoreboard players operation #v tmp *= #cntF tmp
scoreboard players operation #v tmp += #500 tmp
scoreboard players operation #v tmp /= #1000 tmp
scoreboard players operation @s eqHpFlat += #v tmp

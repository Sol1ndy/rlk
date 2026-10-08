# 달 감전 1초 피해 (@s = 몹): 하늘에서 은빛 번개
particle minecraft:end_rod ~ ~2.5 ~ 0.05 0.8 0.05 0.02 8
scoreboard players operation #lnB tmp = @s ecDmg
scoreboard players set #lnEl tmp 3
scoreboard players set #lnT tmp 1
function rlk:element/lunar/hit

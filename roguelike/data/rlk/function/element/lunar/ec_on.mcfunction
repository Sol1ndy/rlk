# 달 감전으로 (@s = 몹): 1초 피해 = 반응 기준 × #lnEC%
scoreboard players set #lunRx tmp 24
scoreboard players operation @s ecDmg = #rBase tmp
scoreboard players operation @s ecDmg *= #lnEC tmp
scoreboard players operation @s ecDmg /= #100 tmp
scoreboard players set @s lnEC 1
scoreboard players set #lnT tmp 1
function rlk:element/lunar/count

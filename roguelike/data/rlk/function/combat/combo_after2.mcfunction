# 2타 후: 다음 1타. atkCD = #comboD21 / atkSpeed(기본100)
scoreboard players operation #cd tmp = #comboD21 tmp
# 나비아(양손검): 마지막 타 뒤 간격 ×130%
execute if score #charN tmp matches 6 run scoreboard players operation #cd tmp *= #c130 tmp
execute if score #charN tmp matches 6 run scoreboard players operation #cd tmp /= #100 tmp
scoreboard players set #as tmp 100
execute if score @s atkSpeed matches 1.. run scoreboard players operation #as tmp = @s atkSpeed
scoreboard players operation #cd tmp /= #as tmp
execute if score #cd tmp matches ..1 run scoreboard players set #cd tmp 2
scoreboard players operation @s atkCD = #cd tmp
scoreboard players set @s comboStep 0
scoreboard players set @s cboIdle 0

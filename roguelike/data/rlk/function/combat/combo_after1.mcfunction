# 1타 후: 다음 2타. atkCD = #comboD12 / atkSpeed(기본100)
scoreboard players operation #cd tmp = #comboD12 tmp
scoreboard players operation #cd tmp *= #naD tmp
scoreboard players operation #cd tmp /= #100 tmp
scoreboard players set #as tmp 100
execute if score @s atkSpeed matches 1.. run scoreboard players operation #as tmp = @s atkSpeed
scoreboard players operation #cd tmp /= #as tmp
execute if score #cd tmp matches ..1 run scoreboard players set #cd tmp 2
execute unless score #pmResolving tmp matches 1 run scoreboard players operation @s atkCD = #cd tmp
scoreboard players set @s comboStep 1
scoreboard players set @s cboIdle 0

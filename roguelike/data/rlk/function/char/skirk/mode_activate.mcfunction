scoreboard players operation @s energy += #skGain tmp
execute if score @s energy > #burstCost100 tmp run scoreboard players operation @s energy = #burstCost100 tmp
# 일곱빛 섬광 시작
scoreboard players operation @s skM = #skModeDur tmp
scoreboard players set #skMode tmp 1
scoreboard players set @s buShown -1
attribute @s minecraft:knockback_resistance modifier add rlk:skirk 1 add_value

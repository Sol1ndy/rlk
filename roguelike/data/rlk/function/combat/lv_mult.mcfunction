# @s = 맞는 몹. #dmg 에 레벨 보정
execute unless score #dmg tmp matches 1.. run return 0
scoreboard players operation #lvA tmp = @a[tag=player,limit=1] level
execute unless score #lvA tmp matches 1.. run scoreboard players set #lvA tmp 1
scoreboard players add #lvA tmp 100
scoreboard players operation #lvB tmp = @s mlv
execute unless score #lvB tmp matches 1.. run scoreboard players set #lvB tmp 1
# 몹 쪽 항 = 100 + 몹 레벨 × #mobLvDef/100 (레벨이 높은 몹일수록 단단함)
scoreboard players operation #lvB tmp *= #mobLvDef tmp
scoreboard players operation #lvB tmp /= #100 tmp
scoreboard players add #lvB tmp 100
scoreboard players operation #lvB tmp += #lvA tmp
scoreboard players operation #dmg tmp *= #lvA tmp
scoreboard players operation #dmg tmp /= #lvB tmp
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1

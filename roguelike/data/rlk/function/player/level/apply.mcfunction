# 레벨 → 기초 스탯 / 다음 레벨까지 필요한 경험치 (@s = 플레이어). 수치는 load 의 조절 지점
execute unless score @s level matches 1.. run scoreboard players set @s level 1
scoreboard players operation #lvN tmp = @s level
scoreboard players remove #lvN tmp 1
scoreboard players operation @s base_maxHealth = #lvN tmp
scoreboard players operation @s base_maxHealth *= #lvHpUp tmp
scoreboard players operation @s base_maxHealth += #lvHp0 tmp
scoreboard players operation @s base_atk = #lvN tmp
scoreboard players operation @s base_atk *= #lvAtkUp tmp
scoreboard players operation @s base_atk += #lvAtk0 tmp
scoreboard players operation @s base_def = #lvN tmp
scoreboard players operation @s base_def *= #lvDefUp tmp
scoreboard players operation @s base_def += #lvDef0 tmp
scoreboard players operation @s xpNeed = #lvN tmp
scoreboard players operation @s xpNeed *= #xpNeedUp tmp
scoreboard players operation @s xpNeed += #xpNeed0 tmp
execute if score @s xpNeed matches ..0 run scoreboard players set @s xpNeed 1

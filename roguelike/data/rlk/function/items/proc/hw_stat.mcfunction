# 화무십일홍 스탯 (@s = 플레이어, items/hook/stat_buffs 에서 2틱마다)
# 육참골단: 공격력 % += 중첩 × #hwStkAtk (#hwAtk: 중첩이 바뀔 때 hw_stack · hw_stk_end 가 계산)
scoreboard players operation @s atkPct += #hwAtk itv
# 검신합일: 체력이 최대 체력의 #hwLowHp % 이하이면 치명타 피해 + (#hwB = 최대 체력 × #hwLowHp ÷ 100 버림: 체력이 정수라 '이하'가 정확함)
scoreboard players operation #hwB itv = @s maxHealth
scoreboard players operation #hwB itv *= #hwLowHp tmp
scoreboard players operation #hwB itv /= #100 tmp
execute if score @s curHealth <= #hwB itv run function rlk:items/proc/hw_low
# 홍련일섬: 체력 #hwSlHp % 이하에서 썼으면 #hwSlCritDur 틱 동안 치명타 확률 +
execute if score #hwCritT itv matches 1.. run scoreboard players operation @s critChance += #hwSlCrit tmp

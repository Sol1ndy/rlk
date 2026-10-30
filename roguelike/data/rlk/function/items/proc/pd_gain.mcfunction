# 고통&절망: 액션 시 #pdDur 틱(기본 2초) 공속/이속 버프 스택 (최대 #pdMax, 기본 20. 둘 다 강화 단계로 조정)
scoreboard players add @s pdStack 1
execute if score @s pdStack > #pdMax tmp run scoreboard players operation @s pdStack = #pdMax tmp
scoreboard players operation @s pdT = #pdDur tmp

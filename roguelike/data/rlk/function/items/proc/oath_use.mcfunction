# 원소폭발을 쓴 직후: 전의를 모두 소모 (그 폭발의 남은 타격은 #oathUse 로 계속 증가, 기본 공격 증가량 #oathB = 전의 × #oathBasic / 10)
scoreboard players operation #oathUse itv = #oath itv
scoreboard players operation #oathB itv = #oath itv
scoreboard players operation #oathB itv *= #oathBasic tmp
scoreboard players operation #oathB itv /= #st10 tmp
scoreboard players operation #oathT itv = #oathDur tmp
scoreboard players set #oath itv 0

# 일반 공격 4타: 197% / 184% / 72% ×3 / 282% (@s = 플레이어, comboStep 0~3)
# D12: 평타 클립을 재생 속도 130%로 빠르게 한 만큼(공격 속도 +30%, 연타 한 바퀴 75 → 59게임틱) D11 계수(256/239/94×3/366%)를
# 1.3으로 나눴다. 평타 초당 피해는 D11과 거의 같다(한 바퀴가 틱 단위로 올림되어 약 2% 낮음). D11 계수는 사용자 영상의 빌드
# (ed3f05b: 150/140/55×3/215%, 한 바퀴 44틱)와 초당 피해가 같도록 ×75/44 한 값이었다.
# #naD(다음 타까지 간격 %)는 나비아에게 쓰이지 않는다: 리그 캐릭터는 클립의 chain_tick과 재생 속도가 다음 입력 간격을 정하고
# (char/motion/combat/request), combat/combo_after1·2는 #pmResolving 중에는 atkCD를 바꾸지 않는다. 값은 예전 그대로 둔다.
scoreboard players set #naSteps tmp 4
scoreboard players set #coef tmp 197
execute if score @s comboStep matches 1 run scoreboard players set #coef tmp 184
execute if score @s comboStep matches 2 run scoreboard players set #coef tmp 72
execute if score @s comboStep matches 2 run scoreboard players set #naX2 tmp 2
execute if score @s comboStep matches 3.. run scoreboard players set #coef tmp 282
scoreboard players set #naD tmp 155
execute if score @s comboStep matches 2 run scoreboard players set #naD tmp 190

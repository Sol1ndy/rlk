# 고유 특성 비밀 유통 경로 (@s = 플레이어, 피해 계산 직후): 결정 축포 뒤 #nvPDur 틱 동안 일반 공격 = 다른 원소 부여로 바뀌지 않는 바위 원소 + 피해 #nvPBonus% 증가
scoreboard players set #elem tmp 5
scoreboard players operation #t1 tmp = #nvPBonus tmp
scoreboard players add #t1 tmp 100
scoreboard players operation #dmg tmp *= #t1 tmp
scoreboard players operation #dmg tmp /= #100 tmp

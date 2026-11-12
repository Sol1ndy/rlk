# 강화 단계 #enh tmp (0~3) → 배율(‰): #fA 효과량 · #fD 지속 시간 · #fC 재사용 대기. 0단계 = 너프된 기본, 3단계 = 너프 전 값
# 효과량 500 + 500×단계/3, 지속 700 + 100×단계, 대기 1300 − 100×단계 (값은 rlk:tune fac)
execute unless score #enh tmp matches 0..3 run scoreboard players set #enh tmp 0
execute store result storage rlk:tune a.l int 1 run scoreboard players get #enh tmp
function rlk:items/tune/fac2 with storage rlk:tune a

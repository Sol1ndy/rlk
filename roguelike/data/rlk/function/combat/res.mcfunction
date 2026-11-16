# 몹 저항 (@s = 몹, #dmg tmp > 0): 저항 R = mres(%). 원신 공식
#   R < 0  : 피해 × (100 - R/2) / 100
#   0~75   : 피해 × (100 - R) / 100
#   R > 75 : 피해 × 100 / (100 + 4R)   (예: R 80 → × 0.238)
# 결과는 최소 1. 사용처: 중간보스 몸체 · 보조 오브젝트(원소별 등). 기본값 0(없음)
execute unless score @s mres matches -1000..-1 unless score @s mres matches 1.. run return 0
scoreboard players operation #resR tmp = @s mres
execute if score #resR tmp matches ..-1 run function rlk:combat/res_neg
execute if score #resR tmp matches 1..75 run function rlk:combat/res_low
execute if score #resR tmp matches 76.. run function rlk:combat/res_high
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1

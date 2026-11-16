# 원소폭발 피해 × (1000 + 원소 에너지 × #eyeRate × 개수 ÷ 10)‰. #eyeRate 는 0.01% 단위 (30 = 1pt당 0.3%, 강화 단계로 조정)
scoreboard players operation #eb tmp = #burstCost tmp
scoreboard players operation #eb tmp *= #eyeRate tmp
scoreboard players operation #eb tmp *= @s it_stormy_eye
scoreboard players operation #eb tmp /= #10 tmp
scoreboard players add #eb tmp 1000
scoreboard players operation #dmg tmp *= #eb tmp
scoreboard players operation #dmg tmp /= #1000 tmp

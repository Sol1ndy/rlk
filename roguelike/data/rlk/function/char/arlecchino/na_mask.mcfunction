# 붉은 죽음의 가면 중의 일반 공격 (@s = 플레이어, 피해 계산 직후): 다른 원소 부여로 바뀌지 않는 불 원소 + 공격력 × #arMaskCoef% × (생명의 계약 %)/100 추가
scoreboard players set #elem tmp 1
function rlk:player/bol/pct
scoreboard players operation #pb tmp = @s atk
scoreboard players operation #pb tmp *= #arMaskCoef tmp
scoreboard players operation #pb tmp /= #100 tmp
scoreboard players operation #pb tmp *= #bolNow tmp
scoreboard players operation #pb tmp /= #100 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #pb tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #pb tmp /= #100 tmp
scoreboard players operation #dmg tmp += #pb tmp
scoreboard players set #arUsed tmp 1

# @s = 플레이어 (#fanT > 0 인 동안 매 틱). 체력 변동량을 모아 열기로: 열기 = 변동량 합 × #fanGain / 최대 체력 (최대 #fanMax)
scoreboard players operation #t1 itv = @s curHealth
scoreboard players operation #t1 itv -= #fanPrev itv
execute if score #t1 itv matches ..-1 run scoreboard players operation #t1 itv *= #neg1 tmp
scoreboard players operation #fanPrev itv = @s curHealth
scoreboard players operation #t1 itv *= #fanGain tmp
scoreboard players operation #fanRaw itv += #t1 itv
scoreboard players operation #fan itv = #fanRaw itv
scoreboard players operation #fan itv /= @s maxHealth
execute if score #fan itv > #fanMax tmp run scoreboard players operation #fan itv = #fanMax tmp

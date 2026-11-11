# @s = 플레이어 (#parT tmp = 이번 패링의 단계). 패링이 된 F: 그 F 는 이 틱의 공격들만 막고(parHit = 지금), 다음 F 는 #parChain 틱
# 뒤부터(연속 공격을 이어 막게). #parWsClr 단계 이상이면 헛누름 연속을 지운다(1단계는 받지 않는 시간만 줄이고 연속은 그대로)
scoreboard players operation @s parHit = #now cb
scoreboard players operation @s parLk = #now cb
scoreboard players operation @s parLk += #parChain tmp
execute if score #parT tmp >= #parWsClr tmp run scoreboard players set #parWs cb 0

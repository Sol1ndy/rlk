# @s = 플레이어 (#parT tmp = 이번 패링의 단계). 패링이 된 F: 그 F 는 이 틱의 공격들만 막고(parHit = 지금), 다음 F 는 #parChain 틱
# 뒤부터(연속 공격을 이어 막게: 1 · 2 · 3단계 모두, 박자의 멈춤 · 느린 화면 중에도 — 전투 시계로 센다)
scoreboard players operation @s parHit = #now cb
scoreboard players operation @s parLk = #now cb
scoreboard players operation @s parLk += #parChain tmp

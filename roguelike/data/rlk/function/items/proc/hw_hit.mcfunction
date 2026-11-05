# 화무십일홍 「육참골단」 (@s = 플레이어, items/hook/on_hit: 기본 공격이 적중한 타마다)
# #hwEvery 번째 적중마다 중첩 +1(hw_stack) · 체력 소모(hw_cost)
scoreboard players set #hwOn itv 1
scoreboard players add #hwHits itv 1
execute if score #hwHits itv < #hwEvery tmp run return 0
scoreboard players set #hwHits itv 0
function rlk:items/proc/hw_stack
function rlk:items/proc/hw_cost

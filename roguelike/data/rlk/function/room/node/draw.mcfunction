# 가중치로 노드 하나 뽑기 → #nk tmp (없으면 0). 뺄 노드 = rlk:room excl (구역 종류 목록) + 조건이 안 맞는 노드
data modify storage rlk:room cand set value []
scoreboard players set #wsum tmp 0
data modify storage rlk:room wq set from storage rlk:room nw
function rlk:room/node/cand_loop
scoreboard players set #nk tmp 0
execute if score #wsum tmp matches ..0 run return 0
execute store result score #wr tmp run random value 0..9999
scoreboard players operation #wr tmp %= #wsum tmp
function rlk:room/node/pick_loop

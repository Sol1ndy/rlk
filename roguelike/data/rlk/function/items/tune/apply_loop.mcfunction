execute unless data storage rlk:tune q[0] run return 0
execute store result score #tv tmp run data get storage rlk:tune q[0].b
scoreboard players operation #tf tmp = #fA tmp
# 목록 칸([0]) 뒤에는 {..} 조건을 붙일 수 없어서, 맨 앞 항목을 qh 로 복사해 검사한다
data modify storage rlk:tune qh set from storage rlk:tune q[0]
execute if data storage rlk:tune qh{m:"d"} run scoreboard players operation #tf tmp = #fD tmp
execute if data storage rlk:tune qh{m:"c"} run scoreboard players operation #tf tmp = #fC tmp
scoreboard players operation #tv tmp *= #tf tmp
scoreboard players operation #tv tmp += #500 tmp
scoreboard players operation #tv tmp /= #1000 tmp
# 0 이 되면 효과가 사라지므로 기준값이 1 이상이면 최소 1
execute if score #tv tmp matches ..0 if data storage rlk:tune q[0].b run function rlk:items/tune/apply_min
function rlk:items/tune/apply_set with storage rlk:tune q[0]
data remove storage rlk:tune q[0]
function rlk:items/tune/apply_loop

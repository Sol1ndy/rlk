execute unless data storage rlk:tune q[0] run return 0
execute store result score #tv tmp run data get storage rlk:tune q[0].b
scoreboard players operation #tf tmp = #fA tmp
execute if data storage rlk:tune q[0]{m:"d"} run scoreboard players operation #tf tmp = #fD tmp
execute if data storage rlk:tune q[0]{m:"c"} run scoreboard players operation #tf tmp = #fC tmp
scoreboard players operation #tv tmp *= #tf tmp
scoreboard players operation #tv tmp += #500 tmp
scoreboard players operation #tv tmp /= #1000 tmp
# 0 이 되면 효과가 사라지므로 기준값이 1 이상이면 최소 1
execute if score #tv tmp matches ..0 if data storage rlk:tune q[0].b run function rlk:items/tune/apply_min
function rlk:items/tune/apply_set with storage rlk:tune q[0]
data remove storage rlk:tune q[0]
function rlk:items/tune/apply_loop

# 다음 챕터의 첫 맵으로
scoreboard players add #chapter room 1
# 새 챕터: 들어간 맵 종류 기록 지우기
scoreboard players reset #seen1 room
scoreboard players reset #seen2 room
scoreboard players reset #seen3 room
scoreboard players reset #seen4 room
scoreboard players reset #seen5 room
scoreboard players reset #seen6 room
scoreboard players reset #seen7 room
scoreboard players set #mapIdx room 0
# 새 챕터: 고른 노드 기록 지우기
data modify storage rlk:room seen set value []
scoreboard players set #mapType room 0
execute in minecraft:overworld run function rlk:room/gen


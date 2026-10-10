# 다음 맵으로 (입력: #mapType room = 고른 맵 종류)
# 이번 챕터에 들어간 맵 종류 기록(재련 제외)
execute if score #mapType room matches 1 run scoreboard players set #seen1 room 1
execute if score #mapType room matches 2 run scoreboard players set #seen2 room 1
execute if score #mapType room matches 3 run scoreboard players set #seen3 room 1
execute if score #mapType room matches 4 run scoreboard players set #seen4 room 1
execute if score #mapType room matches 5 run scoreboard players set #seen5 room 1
execute if score #mapType room matches 7 run scoreboard players set #seen7 room 1
function rlk:run/field_next
scoreboard players add #mapIdx room 1
execute in minecraft:overworld run function rlk:room/gen


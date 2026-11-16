# 다음 맵으로 (입력: #mapType room = 1 노드 맵(노드 = rlk:room next) / 8 보스전)
function rlk:run/field_next
scoreboard players add #mapIdx room 1
execute in minecraft:overworld run function rlk:room/gen


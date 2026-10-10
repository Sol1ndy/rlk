# 던전 구역 전체 초기화: 방 엔티티 제거 + 구덩이 높이(y 186~198) 비우기 + 바닥판(검은 유리: 지도에서 '아직 안 가 본 곳'으로 보이고 몹이 자연 스폰되지 않음) + 그 위(y 200~210) 비우기
function rlk:boss/raiden/cleanup
kill @e[tag=rlk_room]
scoreboard players set #combat room 0
fill -64 186 -64 -1 192 -1 minecraft:air strict
fill -64 186 0 -1 192 63 minecraft:air strict
fill 0 186 -64 63 192 -1 minecraft:air strict
fill 0 186 0 63 192 63 minecraft:air strict
fill -64 193 -64 -1 198 -1 minecraft:air strict
fill -64 193 0 -1 198 63 minecraft:air strict
fill 0 193 -64 63 198 -1 minecraft:air strict
fill 0 193 0 63 198 63 minecraft:air strict
fill -64 199 -64 63 199 63 minecraft:black_stained_glass
fill -64 200 -64 -1 205 -1 minecraft:air strict
fill -64 200 0 -1 205 63 minecraft:air strict
fill 0 200 -64 63 205 -1 minecraft:air strict
fill 0 200 0 63 205 63 minecraft:air strict
fill -64 206 -64 -1 210 -1 minecraft:air strict
fill -64 206 0 -1 210 63 minecraft:air strict
fill 0 206 -64 63 210 -1 minecraft:air strict
fill 0 206 0 63 210 63 minecraft:air strict

fill -64 211 -64 -1 230 -1 minecraft:air strict
fill -64 211 0 -1 230 63 minecraft:air strict
fill 0 211 -64 63 230 -1 minecraft:air strict
fill 0 211 0 63 230 63 minecraft:air strict
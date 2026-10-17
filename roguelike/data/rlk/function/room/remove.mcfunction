# 던전 구역 완전 제거(블록 비우기 + 청크 고정 해제). 사용: /function rlk:room/remove
execute if score #active room matches 1 as @a[tag=player,limit=1] run function rlk:run/stop
execute in minecraft:overworld run function rlk:room/wipe
execute in minecraft:overworld run fill -64 199 -64 63 199 63 minecraft:air
execute in minecraft:overworld run forceload remove -64 -64 63 63
data modify storage rlk:room ready set value 0b
# 아이템 선택 공간도 제거
execute in minecraft:overworld run fill 96 188 0 111 202 10 minecraft:air
# 중간보스 원형 경기장도 제거(청크 고정은 room/setup · /reload · 전투 시작 때 다시 걸리고, 다음 전투에서 다시 지어짐)
execute in minecraft:overworld run function rlk:mboss/arena/clear
execute in minecraft:overworld run forceload remove 176 -16 223 31
tellraw @a [{"text":"[방] ","color":"gold","bold":true},{"text":"던전 구역을 제거했습니다.","color":"gray","bold":false}]

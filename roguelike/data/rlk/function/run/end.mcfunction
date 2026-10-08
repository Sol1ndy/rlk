# 런 종료 공통 처리: 방 치우기 + 지도 회수
scoreboard players set #active room 0
execute in minecraft:overworld run function rlk:room/clear
clear @a minecraft:filled_map[minecraft:custom_data~{rlk_map:1b}]
# 필드에 남은 것 정리: 사파이어 조각은 줍고, 떨어진 아이템·골드와 나머지는 지운다
execute as @e[tag=rlk_gold,tag=rlk_sap] run function rlk:combat/sap_absorb
kill @e[tag=rlk_gold]
kill @e[tag=rlk_ditem]
kill @e[tag=rlk_dinfo]
kill @e[tag=rlk_dbtn]
kill @e[tag=rlk_dlbl]
data modify storage rlk:ditems records set value {}
function rlk:run/field_clear

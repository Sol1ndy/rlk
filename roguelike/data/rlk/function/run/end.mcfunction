# 런 종료 공통 처리: 방 치우기 + 지도 회수
execute as @a[tag=player,scores={vMap=1}] run function rlk:view/map_close
scoreboard players set #active room 0
# 보스 테스트 상태도 함께 끝낸다(패턴 지정·고정도 다음 런으로 넘어가지 않게)
scoreboard players set #rdTest rd 0
scoreboard players set #rdForce rd 0
scoreboard players set #rdLock rd 0
execute in minecraft:overworld run function rlk:room/clear
clear @a minecraft:filled_map[minecraft:custom_data~{rlk_map:1b}]
clear @a *[minecraft:custom_data~{rlk_ui:{role:"map"}}]
# 필드에 남은 것 정리: 사파이어 조각은 줍고, 떨어진 아이템·골드와 나머지는 지운다
execute as @e[tag=rlk_gold,tag=rlk_sap] run function rlk:combat/sap_absorb
kill @e[tag=rlk_gold]
kill @e[tag=rlk_ditem]
kill @e[tag=rlk_dinfo]
kill @e[tag=rlk_dbtn]
kill @e[tag=rlk_dlbl]
data modify storage rlk:ditems records set value {}
function rlk:run/field_clear

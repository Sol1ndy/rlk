# 게임 리셋 (사용: /function rlk:reset) — 스탯/골드/아이템/스택 초기화
# 진행 중인 런이 있으면 중단(시작 자리로 복귀)
execute if score #active room matches 1 as @a[tag=player,limit=1] run function rlk:run/stop
execute as @a[tag=player] run function rlk:player/reset_one
# 월드 잔여 UI 엔티티 정리 (드롭/소환물)
kill @e[tag=rlk_ditem]
kill @e[tag=rlk_dbtn]
kill @e[tag=rlk_dlbl]
kill @e[tag=rlk_dinfo]
kill @e[tag=rlk_healorb]
function rlk:items/hook/reset_world
data modify storage rlk:ditems records set value {}
tellraw @a [{"text":"[리셋] ","color":"red","bold":true},{"text":"게임이 초기화되었습니다.","color":"gray"}]

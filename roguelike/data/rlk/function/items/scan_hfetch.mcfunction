# macro: cur. 이번 빠른 스캔에서 처음 보는 id 면 정의를 가져오고 #scN 1 (같은 아이템 여러 개는 scan_count 가 한 번에 셈).
# 전체 순회가 훑는 목록(rlk:items ids)에 없는 id(레지스트리의 캐릭터 항목 char_* 등)는 전체 순회처럼 세지 않는다
$execute if data storage rlk:scan seen.$(cur) run return 0
$data modify storage rlk:scan seen.$(cur) set value 1b
$execute unless data storage rlk:items {ids:["$(cur)"]} run return 0
$data modify storage rlk:scan def set from storage rlk:items registry.$(cur)
scoreboard players set #scN tmp 1

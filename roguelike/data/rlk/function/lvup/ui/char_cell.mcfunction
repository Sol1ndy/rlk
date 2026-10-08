# 현재 캐릭터 칸 (요소 종류 9: 조준하면 설명만, 눌러도 아무 일 없음)
data modify storage rlk:io id set from storage rlk:chars cur.itemId
scoreboard players set #pkIdx tmp 0
scoreboard players set #pkKind tmp 9
function rlk:lvup/ui/item_load with storage rlk:io
function rlk:lvup/ui/item_el with storage rlk:io

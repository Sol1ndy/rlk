# 현재 캐릭터 칸 (요소 종류 9: 조준하면 설명만, 눌러도 아무 일 없음. 위치 = 칸의 가운데)
summon minecraft:block_display ~ ~ ~0.05 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.42f,-0.42f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.84f,0.84f,0.02f]}}
data modify storage rlk:io id set from storage rlk:chars cur.itemId
scoreboard players set #pkIdx tmp 0
scoreboard players set #pkKind tmp 9
function rlk:lvup/ui/item_load with storage rlk:io
function rlk:lvup/ui/item_el with storage rlk:io

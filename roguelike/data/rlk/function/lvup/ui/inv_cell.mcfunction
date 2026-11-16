# 인벤 칸 하나 (macro: i = 보유 목록의 순번, 위치 = 칸의 가운데). 잠긴 칸(invCap 밖)은 어둡게 + 방벽, 비어 있으면 판만
$scoreboard players set #pkIdx tmp $(i)
execute if score #pkIdx tmp >= @s invCap run return run function rlk:invd/cell_locked
summon minecraft:block_display ~ ~ ~0.05 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.42f,-0.42f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.84f,0.84f,0.02f]}}
$execute unless data storage rlk:pinv order[$(i)] run return 0
$data modify storage rlk:io id set from storage rlk:pinv order[$(i)]
scoreboard players set #pkKind tmp 2
function rlk:lvup/ui/item_load with storage rlk:io
function rlk:lvup/ui/item_el with storage rlk:io

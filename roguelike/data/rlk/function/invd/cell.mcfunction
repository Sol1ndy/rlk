# 칸 하나 (macro: i = 보유 목록의 순번, n = 표시 번호, 위치 = 칸의 가운데). 고른 칸은 노란 판, 잠긴 칸(invCap 밖)은 어둡게 + 방벽
$scoreboard players set #pkIdx tmp $(i)
execute if score #pkIdx tmp >= @s invCap run return run function rlk:invd/cell_locked
$summon minecraft:text_display ~-0.31 ~-0.41 ~-0.01 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"$(n)",color:"gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.4f,0.4f,0.4f]}}
execute unless score #pkIdx tmp = @s pkSel run summon minecraft:block_display ~ ~ ~0.05 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.42f,-0.42f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.84f,0.84f,0.02f]}}
execute if score #pkIdx tmp = @s pkSel run summon minecraft:block_display ~ ~ ~0.05 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:yellow_concrete"},transformation:{translation:[-0.42f,-0.42f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.84f,0.84f,0.02f]}}
$execute unless data storage rlk:pinv order[$(i)] run return 0
$data modify storage rlk:io id set from storage rlk:pinv order[$(i)]
scoreboard players set #pkKind tmp 2
function rlk:lvup/ui/item_load with storage rlk:io
function rlk:lvup/ui/item_el with storage rlk:io

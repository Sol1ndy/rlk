# 인챈트 화면의 칸 하나 (macro: i = 보유 목록의 순번, 위치 = 칸의 가운데). 아래에 별. 잠긴 칸은 어둡게 + 방벽
$scoreboard players set #pkIdx tmp $(i)
execute if score #pkIdx tmp >= @s invCap run return run function rlk:invd/cell_locked
summon minecraft:block_display ~ ~ ~0.05 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.42f,-0.42f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.84f,0.84f,0.02f]}}
$execute unless data storage rlk:pinv order[$(i)] run return 0
$data modify storage rlk:io id set from storage rlk:pinv order[$(i)]
scoreboard players set #pkKind tmp 2
function rlk:lvup/ui/item_load with storage rlk:io
function rlk:lvup/ui/item_el with storage rlk:io
# 별 (item_load → build_display 가 io.sx = 이름 뒤 별을 채움)
summon minecraft:text_display ~ ~-0.72 ~ {Tags:["rlk_pk","rlk_ench_st"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.5f,0.5f,0.5f]}}
data modify entity @e[tag=rlk_ench_st,limit=1] text set from storage rlk:io sx
tag @e[tag=rlk_ench_st] remove rlk_ench_st

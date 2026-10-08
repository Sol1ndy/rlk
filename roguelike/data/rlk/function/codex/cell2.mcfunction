$execute unless data storage rlk:codex list[$(k)] run return 0
summon minecraft:block_display ~ ~ ~0.05 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.42f,-0.42f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.84f,0.84f,0.02f]}}
$data modify storage rlk:io id set from storage rlk:codex list[$(k)]
scoreboard players set #pkKind tmp 13
function rlk:lvup/ui/item_load with storage rlk:io
function rlk:lvup/ui/item_el with storage rlk:io
# 이름표: 미리 만들어 둔 것이 없으면 이름 그대로 한 줄
data modify storage rlk:io lab set value {t:"",dy:"-0.632"}
data modify storage rlk:io lab.t set from storage rlk:io nm
function rlk:codex/lab_get with storage rlk:io
data modify storage rlk:io lab.color set from storage rlk:io color
function rlk:codex/label with storage rlk:io lab

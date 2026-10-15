# 각인 카드 하나 (macro: i = rootc 의 순번, 위치 = 카드 가운데): 판 + 각인 아이콘 + "◆ 이름 / 보유 n개"
$execute unless data storage rlk:room rootc[$(i)] run return 0
summon minecraft:block_display ~ ~ ~0.05 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.8f,-0.9f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.6f,2.1f,0.02f]}}
$data modify storage rlk:lvpick b.e set from storage rlk:room rootc[$(i)]
function rlk:root/card2 with storage rlk:lvpick b
$scoreboard players set #pkIdx tmp $(i)
scoreboard players set #pkKind tmp 14
summon minecraft:marker ~ ~0.3 ~ {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players operation @e[tag=rlk_pk_new] pkKind = #pkKind tmp
scoreboard players operation @e[tag=rlk_pk_new] pkIdx = #pkIdx tmp
tag @e[tag=rlk_pk_new] remove rlk_pk_new

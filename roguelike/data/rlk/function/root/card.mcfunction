# 각인 카드 하나 (macro: i = rootc 의 순번, 위치 = 카드 가운데)
# 위: 각인 아이콘 + "◆ 이름 / 보유 n개", 아래: 함께 얻는 아이템(아이콘 + 이름). 카드 어디를 조준해도 고를 수 있게 표식 둘(종류 14)
$execute unless data storage rlk:room rootc[$(i)] run return 0
summon minecraft:block_display ~ ~ ~0.05 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.85f,-1.3f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.7f,2.35f,0.02f]}}
$scoreboard players set #pkIdx tmp $(i)
scoreboard players set #pkKind tmp 14
$data modify storage rlk:lvpick b.e set from storage rlk:room rootc[$(i)]
function rlk:root/card2 with storage rlk:lvpick b
data remove storage rlk:lvpick c
$execute if data storage rlk:room rooti[$(i)] run data modify storage rlk:lvpick c.id set from storage rlk:room rooti[$(i)]
execute if data storage rlk:lvpick c.id unless data storage rlk:lvpick {c:{id:""}} positioned ~ ~-0.55 ~ run function rlk:root/card4 with storage rlk:lvpick c
summon minecraft:marker ~ ~0.45 ~ {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
summon minecraft:marker ~ ~-0.6 ~ {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players operation @e[tag=rlk_pk_new] pkKind = #pkKind tmp
scoreboard players operation @e[tag=rlk_pk_new] pkIdx = #pkIdx tmp
tag @e[tag=rlk_pk_new] remove rlk_pk_new

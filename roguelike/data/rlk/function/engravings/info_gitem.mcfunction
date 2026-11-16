# 묶음 gq[0] = {n, ids} 하나의 아이템: 묶음 안의 각인마다 이름 + 단계 설명(켜짐/꺼짐)을 이어 붙인다
execute store result score #n tmp run data get storage rlk:eng gq[0].n
data modify storage rlk:eng gid set from storage rlk:eng gq[0].ids
data modify storage rlk:eng lore set value []
scoreboard players set #gk eng 0
function rlk:engravings/info_gitem_lines
# 아이콘 · 이름 · 색은 첫 각인
data modify storage rlk:eng e set from storage rlk:eng gq[0].ids[0]
function rlk:engravings/info_gitem_head with storage rlk:eng
scoreboard players operation #c eng = #n tmp
execute if score #c eng matches 100.. run scoreboard players set #c eng 99
execute store result storage rlk:eng cur.cnt int 1 run scoreboard players get #c eng
execute store result storage rlk:eng cur.slot int 1 run scoreboard players get #slot eng
execute store result storage rlk:eng cur.n int 1 run scoreboard players get #n tmp
data modify storage rlk:eng cur.lore set from storage rlk:eng lore
scoreboard players remove #gk eng 1
execute store result storage rlk:eng cur.more int 1 run scoreboard players get #gk eng
execute if score #gk eng matches 0 run function rlk:engravings/info_item_put with storage rlk:eng cur
execute if score #gk eng matches 1.. run function rlk:engravings/info_gitem_put with storage rlk:eng cur

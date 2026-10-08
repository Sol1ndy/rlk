# macro: id, n. 각인 하나의 아이템: 설명 줄(단계마다 켜짐/꺼짐)을 모아 #slot 칸에 놓는다
$scoreboard players set #n tmp $(n)
$data modify storage rlk:eng cur set from storage rlk:engravings registry.$(id)
$data modify storage rlk:eng cur.n set value $(n)
scoreboard players operation #c eng = #n tmp
execute if score #c eng matches 100.. run scoreboard players set #c eng 99
execute store result storage rlk:eng cur.cnt int 1 run scoreboard players get #c eng
execute store result storage rlk:eng cur.slot int 1 run scoreboard players get #slot eng
data modify storage rlk:eng lore set value []
data modify storage rlk:eng tq set from storage rlk:eng cur.tiers
function rlk:engravings/info_tiers
data modify storage rlk:eng cur.lore set from storage rlk:eng lore
function rlk:engravings/info_item_put with storage rlk:eng cur

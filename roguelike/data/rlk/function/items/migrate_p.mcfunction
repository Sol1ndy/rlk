# @s = 예전 id(favonius_bow) 아이템을 가진 플레이어: 그 아이템을 지우고 보유 목록에서 빼고, 페보니우스 비전을 준다
clear @s *[minecraft:custom_data~{rlk:{id:"favonius_bow"}}]
data modify storage rlk:mig q set from storage rlk:pinv order
data modify storage rlk:mig out set value []
function rlk:items/migrate_loop
data modify storage rlk:pinv order set from storage rlk:mig out
data remove storage rlk:pinv pcnt
function rlk:items/give {id:"favonius_codex"}

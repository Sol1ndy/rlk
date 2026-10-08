# ids 를 등급순(common→rare→epic→legendary→mythic)으로 재정렬
data modify storage rlk:sort src set from storage rlk:items ids
data modify storage rlk:items ids set value []
data modify storage rlk:sort rarities set value ["common","rare","epic","legendary","mythic"]
function rlk:items/sort_rar_loop

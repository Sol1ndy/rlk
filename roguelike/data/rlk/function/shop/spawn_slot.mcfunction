# at = 블록 코너. 안산암/유리 설치 + 아이템 롤 배치
setblock ~ ~ ~ minecraft:polished_andesite
setblock ~ ~1 ~ minecraft:glass
data modify storage rlk:pick picked set value []
function rlk:shop/roll_pick
execute if data storage rlk:pick pid run function rlk:shop/place_item

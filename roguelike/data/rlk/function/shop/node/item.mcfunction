# 진열대 하나 (위치 = 블록 코너): 안산암 + 유리, 아이템 하나
setblock ~ ~ ~ minecraft:polished_andesite
setblock ~ ~1 ~ minecraft:glass
function rlk:shop/node/roll
execute unless data storage rlk:pick pid run return 0
function rlk:shop/place_item

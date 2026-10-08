data remove storage rlk:io clickdrop
# 표시 데이터 구성 + 접힘/펼침 텍스트 + 스폰
function rlk:items/build_display
# 판매가 조회
data modify storage rlk:io rr set from storage rlk:io rarity
function rlk:items/drop_price with storage rlk:io
data modify storage rlk:io dfull set value []
data modify storage rlk:io dfull append from storage rlk:io name
data modify storage rlk:io lj set from storage rlk:io lore
function rlk:items/drop_lj_loop
function rlk:items/drop_spawn with storage rlk:io

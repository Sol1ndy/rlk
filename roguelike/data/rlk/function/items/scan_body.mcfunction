# 한 id (@s = 플레이어, rlk:scan cur = id, def = 그 정의): items/scan_one(전체 순회) · items/scan_hloop(빠른 스캔)
data modify storage rlk:scan item set from storage rlk:scan def.item
data modify storage rlk:scan id set from storage rlk:scan cur

# 보유 개수 (#cnt) + 보유 플래그 스코어(it_<id>)
function rlk:items/scan_count with storage rlk:scan

# 스탯 합산
execute if score #cnt tmp matches 1.. run function rlk:items/scan_add_prep

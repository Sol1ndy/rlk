# 리스트 맨 앞 아이템 처리 (@s = 플레이어)
data modify storage rlk:scan cur set from storage rlk:scan ids[0]
function rlk:items/scan_fetch with storage rlk:scan
data modify storage rlk:scan item set from storage rlk:scan def.item
data modify storage rlk:scan id set from storage rlk:scan cur

# 보유 개수 (#cnt) + 보유 플래그 스코어(it_<id>)
function rlk:items/scan_count with storage rlk:scan

# 스탯 합산
execute if score #cnt tmp matches 1.. run function rlk:items/scan_add_prep

data remove storage rlk:scan ids[0]
function rlk:items/scan_loop

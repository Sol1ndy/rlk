# 리스트 맨 앞 아이템 처리 (@s = 플레이어)
data modify storage rlk:scan cur set from storage rlk:scan ids[0]
function rlk:items/scan_fetch with storage rlk:scan
function rlk:items/scan_body

data remove storage rlk:scan ids[0]
function rlk:items/scan_loop

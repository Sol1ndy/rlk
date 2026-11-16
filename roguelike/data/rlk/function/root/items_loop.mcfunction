# rootc 의 각인마다 함께 줄 아이템을 미리 정해 rooti 에 (없으면 "")
execute unless data storage rlk:room iq[0] run return 0
data modify storage rlk:room ie.e set from storage rlk:room iq[0]
function rlk:root/pick_item with storage rlk:room ie
execute unless data storage rlk:room gid run data modify storage rlk:room gid set value ""
data modify storage rlk:room rooti append from storage rlk:room gid
data remove storage rlk:room iq[0]
function rlk:root/items_loop

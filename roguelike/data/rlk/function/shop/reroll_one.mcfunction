data modify storage rlk:shop rc set from storage rlk:shop scan[0]
data modify storage rlk:shop rcx set from storage rlk:shop rc.x
data modify storage rlk:shop rcy set from storage rlk:shop rc.y
data modify storage rlk:shop rcz set from storage rlk:shop rc.z
function rlk:shop/reroll_at with storage rlk:shop
data remove storage rlk:shop scan[0]
function rlk:shop/reroll_loop

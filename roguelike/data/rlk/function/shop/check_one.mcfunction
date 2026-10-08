data modify storage rlk:shop ccur set from storage rlk:shop cscan[0]
data modify storage rlk:shop ccx set from storage rlk:shop ccur.x
data modify storage rlk:shop ccy set from storage rlk:shop ccur.y
data modify storage rlk:shop ccz set from storage rlk:shop ccur.z
function rlk:shop/check_at with storage rlk:shop
data remove storage rlk:shop cscan[0]
function rlk:shop/check_loop

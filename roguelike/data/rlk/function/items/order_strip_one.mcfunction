data modify storage rlk:pinv scur set from storage rlk:pinv sscan[0]
function rlk:items/order_strip_decide with storage rlk:pinv
data remove storage rlk:pinv sscan[0]
function rlk:items/order_strip_loop

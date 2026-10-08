data modify storage rlk:shop fcur set from storage rlk:shop fscan[0]
data modify storage rlk:shop fcx set from storage rlk:shop fcur.x
data modify storage rlk:shop fcy set from storage rlk:shop fcur.y
data modify storage rlk:shop fcz set from storage rlk:shop fcur.z
function rlk:shop/filter_decide with storage rlk:shop
data remove storage rlk:shop fscan[0]
function rlk:shop/filter_loop

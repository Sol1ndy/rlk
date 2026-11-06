execute unless data storage rlk:tune xq[0] run return 0
data modify storage rlk:tune xc set from storage rlk:tune xq[0]
execute if data storage rlk:tune xc.tk run function rlk:items/tune/disp_tk
data modify storage rlk:tune xo append from storage rlk:tune xc
data remove storage rlk:tune xq[0]
function rlk:items/tune/disp_x_loop

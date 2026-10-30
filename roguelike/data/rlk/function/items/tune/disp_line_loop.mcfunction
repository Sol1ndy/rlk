execute unless data storage rlk:tune dl[0] run return 0
data modify storage rlk:tune dline set from storage rlk:tune dl[0]
data modify storage rlk:tune xq set value []
execute if data storage rlk:tune dline.extra[0] run data modify storage rlk:tune xq set from storage rlk:tune dline.extra
data modify storage rlk:tune xo set value []
function rlk:items/tune/disp_x_loop
execute if data storage rlk:tune dline.extra[0] run data modify storage rlk:tune dline.extra set from storage rlk:tune xo
data modify storage rlk:tune dout append from storage rlk:tune dline
data remove storage rlk:tune dl[0]
function rlk:items/tune/disp_line_loop

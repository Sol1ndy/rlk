execute unless data storage rlk:cm zs[0] run return 0
data modify storage rlk:cm cs set from storage rlk:cm zs[0].cells
function rlk:cm/brk_c
data remove storage rlk:cm zs[0]
function rlk:cm/brk_z

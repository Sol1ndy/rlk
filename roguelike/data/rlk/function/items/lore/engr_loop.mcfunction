execute unless data storage rlk:io engq[0] run return 0
execute if data storage rlk:io engx[0] run data modify storage rlk:io engx append value {text:" · ",color:"gray"}
data modify storage rlk:io enge set from storage rlk:io engq[0]
function rlk:items/lore/engr_one with storage rlk:io
data remove storage rlk:io engq[0]
function rlk:items/lore/engr_loop

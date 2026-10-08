data modify storage rlk:io dfull append value {text:"\n",italic:false,bold:false}
data modify storage rlk:io dfull append from storage rlk:io lj[0]
data remove storage rlk:io lj[0]
function rlk:items/drop_lj_loop

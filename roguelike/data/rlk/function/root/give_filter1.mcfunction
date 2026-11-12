$execute if data storage rlk:pinv {order:["$(x)"]} run return 0
$execute if data storage rlk:room {rooti:["$(x)"]} run return 0
$data modify storage rlk:room gq2 append value "$(x)"

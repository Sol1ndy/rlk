data modify storage rlk:pinv ccur set from storage rlk:pinv cscan[0]
function rlk:player/inv/collect_check with storage rlk:pinv
data remove storage rlk:pinv cscan[0]
function rlk:player/inv/collect_loop

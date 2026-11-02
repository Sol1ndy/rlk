scoreboard players add #sq kn 1
function rlk:boss/arlecchino/seq/intro/tick
execute if score #sqdone kn matches 1 run return run function rlk:boss/arlecchino/core/replay/end
execute if score #sq kn matches 152.. run function rlk:boss/arlecchino/core/replay/end

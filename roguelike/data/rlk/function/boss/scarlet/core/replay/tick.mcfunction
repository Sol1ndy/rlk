scoreboard players add #sq hr 1
function rlk:boss/scarlet/seq/intro/tick
scoreboard players set #sq_sig hr 0
function rlk:boss/scarlet/core/skip
execute if score #sqdone hr matches 1 run return run function rlk:boss/scarlet/core/replay/end
execute if score #sq hr matches 1442.. run function rlk:boss/scarlet/core/replay/end

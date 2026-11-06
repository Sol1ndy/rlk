# A fight-state sequence ended (@s = body): the next step of the chain.
scoreboard players set #sqdone hr 0
execute if score #sqn hr matches 2 run return run function rlk:boss/scarlet/core/sq1/start
execute if score #sqn hr matches 3 run return run function rlk:boss/scarlet/core/g/start/a8
execute if score #sqn hr matches 4 run return run function rlk:boss/scarlet/core/repel/end
execute if score #gk hr matches 1 run return run function rlk:boss/scarlet/core/g/start/a8
function rlk:boss/scarlet/core/g/start/a13

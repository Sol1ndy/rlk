# The state of the phase (@s = body).
execute if score #rp hr matches 1 run return run function rlk:boss/scarlet/core/replay/tick
execute if score #ph hr matches 1 run return run function rlk:boss/scarlet/core/fp
execute if score #ph hr matches 7 run return run function rlk:boss/scarlet/core/fp
execute if score #ph hr matches 4 run return run function rlk:boss/scarlet/core/g/tick
execute if score #ph hr matches 9 run return run function rlk:boss/scarlet/core/g/tick
execute if score #ph hr matches 6 run return run function rlk:boss/scarlet/core/down/tick
execute if score #rvw hr matches 1.. run return run function rlk:boss/scarlet/core/revive/tick
execute if score #sqn hr matches 1.. run return run function rlk:boss/scarlet/core/seq/tick

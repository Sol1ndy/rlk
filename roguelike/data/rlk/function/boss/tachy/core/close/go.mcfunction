# The queued chain begins (@s = body); unknown id: the recovery.
scoreboard players set #pat tk 0
execute if score #cl_q tk matches 2 run return run function rlk:boss/tachy/core/begin/b1
execute if score #cl_q tk matches 3 run return run function rlk:boss/tachy/core/begin/b2
execute if score #cl_q tk matches 5 run return run function rlk:boss/tachy/core/begin/c1
execute if score #cl_q tk matches 6 run return run function rlk:boss/tachy/core/begin/c2
execute if score #cl_q tk matches 7 run return run function rlk:boss/tachy/core/begin/c3
function rlk:boss/tachy/ai/rec_start

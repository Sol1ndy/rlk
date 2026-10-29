# The running pattern (@s = body): #pt + 1, the core wrapper core/run/<key> (G3 window tags + p/<key>/tick).
scoreboard players add #pt tk 1
execute if score #pat tk matches 1 run function rlk:boss/tachy/core/run/a1
execute if score #pat tk matches 2 run function rlk:boss/tachy/core/run/b1
execute if score #pat tk matches 3 run function rlk:boss/tachy/core/run/b2
execute if score #pat tk matches 4 run function rlk:boss/tachy/core/run/b3
execute if score #pat tk matches 5 run function rlk:boss/tachy/core/run/c1
execute if score #pat tk matches 6 run function rlk:boss/tachy/core/run/c2
execute if score #pat tk matches 7 run function rlk:boss/tachy/core/run/c3
execute if score #done tk matches 1 run function rlk:boss/tachy/core/pat_end

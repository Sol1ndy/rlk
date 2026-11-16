# Q4 떠오르는 재액의 달: one tick (the stage machine: #q4_s kn = stage, #q4_c kn = its clock = the clip tick).
scoreboard players add #q4_c kn 1
execute if score #q4_s kn matches 1 run return run function rlk:boss/arlecchino/p/q4/s/up/tick
execute if score #q4_s kn matches 2 run return run function rlk:boss/arlecchino/p/q4/s/shot/tick
execute if score #q4_s kn matches 3 run return run function rlk:boss/arlecchino/p/q4/s/land/tick

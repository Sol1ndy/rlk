# Q6 핏빛 연회: one tick (the stage machine: #q6_s kn = stage, #q6_c kn = its clock = the clip tick).
scoreboard players add #q6_c kn 1
execute if score #q6_s kn matches 1 run return run function rlk:boss/arlecchino/p/q6/s/main/tick

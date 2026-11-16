# Q1 사형장으로의 초대: one tick (the stage machine: #q1_s kn = stage, #q1_c kn = its clock = the clip tick).
scoreboard players add #q1_c kn 1
execute if score #q1_s kn matches 1 run return run function rlk:boss/arlecchino/p/q1/s/main/tick
execute if score #q1_s kn matches 2 run return run function rlk:boss/arlecchino/p/q1/s/hold/tick

# Q2 불꽃이 타오르는 낫: one tick (the stage machine: #q2_s kn = stage, #q2_c kn = its clock = the clip tick).
scoreboard players add #q2_c kn 1
execute if score #q2_s kn matches 1 run return run function rlk:boss/arlecchino/p/q2/s/main/tick

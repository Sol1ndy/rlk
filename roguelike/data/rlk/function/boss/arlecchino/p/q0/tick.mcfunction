# Q0 낙하 공격: one tick (the stage machine: #q0_s kn = stage, #q0_c kn = its clock = the clip tick).
scoreboard players add #q0_c kn 1
execute if score #q0_s kn matches 1 run return run function rlk:boss/arlecchino/p/q0/s/hover/tick
execute if score #q0_s kn matches 2 run return run function rlk:boss/arlecchino/p/q0/s/dive/tick

# Q5A 붉은 피의 연회 · 형벌의 핏값: one tick (the stage machine: #q5a_s kn = stage, #q5a_c kn = its clock = the clip tick).
scoreboard players add #q5a_c kn 1
execute if score #q5a_s kn matches 1 run return run function rlk:boss/arlecchino/p/q5a/s/main/tick

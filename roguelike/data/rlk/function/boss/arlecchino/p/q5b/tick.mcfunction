# Q5B 붉은 피의 연회 · 붉은 피의 사형: one tick (the stage machine: #q5b_s kn = stage, #q5b_c kn = its clock = the clip tick).
scoreboard players add #q5b_c kn 1
execute if score #q5b_s kn matches 1 run return run function rlk:boss/arlecchino/p/q5b/s/main/tick

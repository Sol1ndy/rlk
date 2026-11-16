# Q3 붉은 죽음의 무도회: one tick (the stage machine: #q3_s kn = stage, #q3_c kn = its clock = the clip tick).
scoreboard players add #q3_c kn 1
execute if score #q3_s kn matches 1 run return run function rlk:boss/arlecchino/p/q3/s/whip/tick
execute if score #q3_s kn matches 2 run return run function rlk:boss/arlecchino/p/q3/s/cut/tick
execute if score #q3_s kn matches 3 run return run function rlk:boss/arlecchino/p/q3/s/hold/tick

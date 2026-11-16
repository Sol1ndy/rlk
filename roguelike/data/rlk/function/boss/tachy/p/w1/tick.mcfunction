# W1 지상 장풍: one tick; the stage machine (#w1_s = stage, #w1_c = stage clock).
scoreboard players add #w1_c tk 1
execute if score #w1_s tk matches 1 run return run function rlk:boss/tachy/p/w1/s/bl/tick
execute if score #w1_s tk matches 2 run return run function rlk:boss/tachy/p/w1/s/ch/tick

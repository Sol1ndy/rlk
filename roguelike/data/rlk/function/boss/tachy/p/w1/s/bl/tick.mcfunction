# W1 stage bl: one tick (#w1_c 1..).
scoreboard players set #pt tk 0
execute if score #w1_c tk matches 12 run function rlk:boss/tachy/p/w1/s/bl/k/12
execute if score #w1_c tk matches 18 run function rlk:boss/tachy/p/w1/s/bl/k/18
execute if score #w1_c tk matches 24 run function rlk:boss/tachy/p/w1/s/bl/k/24
execute if score #w1_c tk matches 34 run return run function rlk:boss/tachy/p/w1/s/bl/k/34

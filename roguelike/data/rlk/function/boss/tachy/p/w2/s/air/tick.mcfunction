# W2 stage air: one tick (#w2_c 1..).
execute if score #w2_c tk matches 1..60 run function rlk:mboss/mv/turn {max:8}
execute if score #w2_c tk matches 14 run function rlk:boss/tachy/p/w2/s/air/k/14
execute if score #w2_c tk matches 28 run function rlk:boss/tachy/p/w2/s/air/k/28
execute if score #w2_c tk matches 42 run function rlk:boss/tachy/p/w2/s/air/k/42
execute if score #w2_c tk matches 46 run function rlk:boss/tachy/p/w2/s/air/k/46
execute if score #w2_c tk matches 60 run function rlk:boss/tachy/p/w2/s/air/k/60
execute if score #w2_c tk matches 66 run return run function rlk:boss/tachy/p/w2/s/air/k/66

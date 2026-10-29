# W1 stage ch: one tick (#w1_c 1..).
execute if score #w1_c tk matches 1..69 run function rlk:mboss/mv/turn {max:6}
execute if score #w1_c tk matches 6 run function rlk:boss/tachy/p/w1/s/ch/k/6
execute if score #w1_c tk matches 40 run function rlk:boss/tachy/rig/look/chest/off
execute if score #w1_c tk matches 46 run function rlk:boss/tachy/p/w1/s/ch/k/46
execute if score #w1_c tk matches 58 run function rlk:boss/tachy/p/w1/s/ch/k/58
execute if score #w1_c tk matches 70 run function rlk:boss/tachy/p/w1/s/ch/k/70
execute if score #w1_c tk matches 88 run scoreboard players set #done tk 1

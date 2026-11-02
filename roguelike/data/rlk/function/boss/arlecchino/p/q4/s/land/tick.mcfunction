# Q4 stage land: one tick (#q4_c 1..).
execute if score #q4_c kn matches 1..12 run function rlk:mboss/mv/turn {max:10}
execute if score #q4_c kn matches 12 run function rlk:boss/arlecchino/p/q4/s/land/k/12
execute if score #q4_c kn matches 16 run return run function rlk:boss/arlecchino/p/q4/s/land/k/16

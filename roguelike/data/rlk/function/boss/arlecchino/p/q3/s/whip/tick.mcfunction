# Q3 stage whip: one tick (#q3_c 1..).
execute if score #q3_c kn matches 1..10 run function rlk:mboss/mv/turn {max:30}
execute if score #q3_c kn matches 15..20 run function rlk:mboss/mv/turn {max:20}
execute if score #q3_c kn matches 13 run function rlk:boss/arlecchino/p/q3/s/whip/k/13
execute if score #q3_c kn matches 14 run function rlk:boss/arlecchino/p/q3/s/whip/k/14
execute if score #q3_c kn matches 20 run function rlk:boss/arlecchino/p/q3/s/whip/k/20
execute if score #q3_c kn matches 26 if score #q3_k kn matches 2 run function rlk:boss/arlecchino/p/q3/f/far
execute if score #q3_c kn matches 36 run return run function rlk:boss/arlecchino/p/q3/s/whip/k/36

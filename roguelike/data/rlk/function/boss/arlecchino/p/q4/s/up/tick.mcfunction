# Q4 stage up: one tick (#q4_c 1..).
execute if score #q4_c kn matches 1..20 run function rlk:mboss/mv/turn {max:12}
execute if score #q4_c kn matches 20 run return run function rlk:boss/arlecchino/p/q4/s/up/k/20

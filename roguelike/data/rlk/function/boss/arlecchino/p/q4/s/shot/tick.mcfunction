# Q4 stage shot: one tick (#q4_c 1..).
execute if score #q4_c kn matches 1..19 run function rlk:mboss/mv/turn {max:12}
execute if score #q4_c kn matches 2 run function rlk:boss/arlecchino/p/q4/f/aim
execute if score #q4_c kn matches 4 run function rlk:boss/arlecchino/p/q4/f/aim
execute if score #q4_c kn matches 6 run function rlk:boss/arlecchino/p/q4/f/aim
execute if score #q4_c kn matches 8 run function rlk:boss/arlecchino/p/q4/f/aim
execute if score #q4_c kn matches 10 run function rlk:boss/arlecchino/p/q4/f/aim
execute if score #q4_c kn matches 12 run function rlk:boss/arlecchino/p/q4/f/aim
execute if score #q4_c kn matches 14 run function rlk:boss/arlecchino/p/q4/f/aim
execute if score #q4_c kn matches 16 run function rlk:boss/arlecchino/p/q4/f/aim
execute if score #q4_c kn matches 18 run function rlk:boss/arlecchino/p/q4/f/aim
execute if score #q4_c kn matches 20 run function rlk:boss/arlecchino/p/q4/s/shot/k/20
execute if score #q4_c kn matches 25 run function rlk:boss/arlecchino/p/q4/s/shot/k/25
execute if score #q4_c kn matches 26 run function rlk:boss/arlecchino/p/q4/s/shot/k/26
execute if score #q4_c kn matches 27 if score #q4_k kn matches 1 if score #q4_n kn matches ..1 unless score #hitev kn matches 1.. run scoreboard players set #q4_n kn 2
execute if score #q4_c kn matches 50 run return run function rlk:boss/arlecchino/p/q4/s/shot/k/50

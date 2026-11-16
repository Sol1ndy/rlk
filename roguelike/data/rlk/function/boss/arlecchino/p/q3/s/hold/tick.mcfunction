# Q3 stage hold: one tick (#q3_c 1..).
execute if score #q3_c kn matches 1..30 run function rlk:mboss/mv/turn {max:10}
execute if score #q3_c kn matches 1..30 unless entity @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] run return run function rlk:boss/arlecchino/p/q3/fin
execute if score #q3_c kn matches 30 run return run function rlk:boss/arlecchino/p/q3/s/hold/k/30

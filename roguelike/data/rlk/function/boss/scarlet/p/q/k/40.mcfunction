# Q pattern tick 40
execute if score #q_hit hr matches 1 store result storage rlk:hr core.sw.d double 0.4167 run scoreboard players get #sw_n hr
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw

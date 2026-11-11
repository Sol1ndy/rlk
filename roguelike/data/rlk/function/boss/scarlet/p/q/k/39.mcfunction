# Q pattern tick 39
execute if score #q_hit hr matches 1 store result storage rlk:hr core.sw.d double 0.375 run scoreboard players get #sw_n hr
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw

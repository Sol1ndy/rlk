# Q pattern tick 55
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/core/near {d:1.4,t:4}
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/g_dive
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:30}
execute if score #q_hit hr matches 1 store result storage rlk:hr core.sw.d double 0.3125 run scoreboard players get #sw_n hr
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw

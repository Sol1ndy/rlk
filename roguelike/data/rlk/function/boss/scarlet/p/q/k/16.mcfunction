# Q pattern tick 16
function rlk:boss/scarlet/p/q/lunge
execute at @s run function rlk:boss/scarlet/fx/snd/g_dash
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.95 ~ run function rlk:boss/scarlet/fx/p/ghost_trail {len:140}
execute store result storage rlk:hr core.sw.d double 0.375 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw

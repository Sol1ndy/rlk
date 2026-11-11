# Q pattern tick 87
execute if score #q_hit hr matches 1 run tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
execute if score #q_hit hr matches 1 run tag @e[tag=rlk_body,limit=1] add rlk_hr_swt
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ^0.4 ^3.856 ^-0.125 facing entity @e[tag=rlk_body,limit=1] feet run function rlk:boss/scarlet/core/sw/aim {dy:"0"}
execute if score #q_hit hr matches 1 run tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
execute if score #q_hit hr matches 1 store result storage rlk:hr core.sw.d double 0.2083 run scoreboard players get #sw_n hr
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw

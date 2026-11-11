# Q pattern tick 36
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/p/q/lockp
execute if score #q_hit hr matches 1 at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/fx/follow_on
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/rig/anchor/blade_mid
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/fx/follow_off
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute if score #q_hit hr matches 1 run tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] add rlk_hr_swt
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ^-0.635 ^3.195 ^0.094 facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run function rlk:boss/scarlet/core/sw/aim {dy:"0"}
execute if score #q_hit hr matches 1 run tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
execute if score #q_hit hr matches 1 store result storage rlk:hr core.sw.d double 0.25 run scoreboard players get #sw_n hr
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw

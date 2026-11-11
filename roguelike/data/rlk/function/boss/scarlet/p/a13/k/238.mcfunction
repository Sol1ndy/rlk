# A13 pattern tick 238.
tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
tag @e[tag=rlk_body,limit=1] add rlk_hr_swt
execute at @s rotated as @s rotated ~ 0 positioned ^0.089 ^3.703 ^0.907 facing entity @e[tag=rlk_body,limit=1] feet run function rlk:boss/scarlet/core/sw/aim {dy:"0"}
tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
execute store result storage rlk:hr core.sw.d double 0.4167 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw

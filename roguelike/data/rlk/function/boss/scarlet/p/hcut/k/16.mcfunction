# HCUT pattern tick 16
function rlk:boss/scarlet/rig/anchor/blade_tip
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:5}
tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
tag @e[tag=rlk_body,limit=1] add rlk_hr_swt
execute at @s facing entity @e[tag=rlk_body,limit=1] feet positioned ~ ~1.0 ~ run function rlk:boss/scarlet/core/sw/aim {dy:"-1.0"}
tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
execute store result storage rlk:hr core.sw.d double 0.125 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw

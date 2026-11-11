# TRI pattern tick 9
execute store result storage rlk:hr core.sw.d double 0.3333 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
execute at @e[tag=rlk_body,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_m14,limit=1] ~ ~3.321 ~

# A13 pattern tick 227.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c220_221]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c220_223] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
tag @e[tag=rlk_body,limit=1] add rlk_hr_swt
execute at @s rotated as @s rotated ~ 0 positioned ^0.089 ^3.703 ^0.907 facing entity @e[tag=rlk_body,limit=1] feet run function rlk:boss/scarlet/core/sw/aim {dy:"0"}
tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
execute store result storage rlk:hr core.sw.d double 0.1111 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw

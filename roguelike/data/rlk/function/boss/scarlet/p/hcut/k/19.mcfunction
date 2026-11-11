# HCUT pattern tick 19
function rlk:boss/scarlet/p/hcut/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..13] rotated as @s rotated ~ 0 positioned ^ ^ ^13 run tp @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] ~ ~ ~
tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
tag @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] add rlk_hr_swt
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet positioned ~ ~1.0 ~ run function rlk:boss/scarlet/core/sw/aim {dy:"-1.0"}
tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
execute store result storage rlk:hr core.sw.d double 0.25 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw

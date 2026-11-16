# @s = the boss: the palms slam together over the zone (3 t).
execute as @e[tag=rlk_rd_clap,type=item_display] run data merge entity @s {teleport_duration:3}
execute at @e[tag=rlk_rd_tm_clapc,limit=1] facing entity @s feet rotated ~180 0 positioned ^0.9 ^1.6 ^ run tp @e[tag=rlk_rd_tm_hl,limit=1] ~ ~ ~ ~ 0
execute at @e[tag=rlk_rd_tm_clapc,limit=1] facing entity @s feet rotated ~180 0 positioned ^-0.9 ^1.6 ^ run tp @e[tag=rlk_rd_tm_hr,limit=1] ~ ~ ~ ~ 0

# @s = the boss: the pair centre walks after the player at 0.3 b/t; the hands keep their sides.
execute as @e[tag=rlk_rd_tm_clapc,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.3 unless entity @e[tag=rlk_body,distance=..0.35] run tp @s ~ 201 ~
execute at @e[tag=rlk_rd_tm_clapc,limit=1] facing entity @s feet rotated ~180 0 positioned ^2.8 ^1.6 ^ run tp @e[tag=rlk_rd_tm_hl,limit=1] ~ ~ ~ ~ 0
execute at @e[tag=rlk_rd_tm_clapc,limit=1] facing entity @s feet rotated ~180 0 positioned ^-2.8 ^1.6 ^ run tp @e[tag=rlk_rd_tm_hr,limit=1] ~ ~ ~ ~ 0

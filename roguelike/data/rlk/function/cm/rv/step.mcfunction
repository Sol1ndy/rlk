# one 0.32 b move toward rlk_cmrot; blocked -> slide level, then up (under the ceiling) or down (>= 1.2 b over ground)
execute if entity @e[tag=rlk_cmrot,distance=..0.35] run return 0
execute facing entity @e[tag=rlk_cmrot,limit=1] feet positioned ^ ^ ^0.32 if function rlk:cm/rv/free run return run tp @s ~ ~ ~
execute facing entity @e[tag=rlk_cmrot,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.3 if function rlk:cm/rv/free run return run tp @s ~ ~ ~
execute if function rlk:cm/rv/below_cap positioned ~ ~0.3 ~ if function rlk:cm/rv/free run return run tp @s ~ ~ ~
execute positioned ~ ~-0.3 ~ if block ~ ~-1.2 ~ #rlk:cm_pass if function rlk:cm/rv/free run tp @s ~ ~ ~

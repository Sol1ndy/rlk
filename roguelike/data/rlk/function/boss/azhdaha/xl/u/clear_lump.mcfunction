# @s = a target marker of a pattern field r 4: pushed radially to >= 5.5 b from the head-front point and
# the tail-lane point (plan 4.7 clear melee points), then pulled inside the walk disc.
tag @s add rlk_mb_az_xcp
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^ ^6.8 run function rlk:boss/azhdaha/xl/u/cp_lump
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^ ^-10.12 run function rlk:boss/azhdaha/xl/u/cp_lump
tag @s remove rlk_mb_az_xcp
function rlk:boss/azhdaha/u/clamp_w

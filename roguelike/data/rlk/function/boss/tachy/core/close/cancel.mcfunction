# The gap closer stops (any executor; idempotent): the body visible and vulnerable.
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/tachy/rig/state/normal
tag @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] remove rlk_mb_inv

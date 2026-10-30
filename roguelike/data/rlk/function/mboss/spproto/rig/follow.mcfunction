execute unless entity @e[type=minecraft:block_display,tag=rlk_mb_spproto_part,limit=1] run return run function rlk:mboss/spproto/rig/spawn
execute rotated as @s rotated ~ 0 run tp @e[type=minecraft:block_display,tag=rlk_mb_spproto_part] ~ ~ ~ ~ 0

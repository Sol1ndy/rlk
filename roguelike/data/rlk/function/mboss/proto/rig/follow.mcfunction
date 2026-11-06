# @s = body, at @s: parts follow the body position and yaw (teleport_duration 1 smooths it).
execute unless entity @e[type=minecraft:block_display,tag=rlk_mbp_torso,limit=1] run function rlk:mboss/proto/rig/spawn
execute rotated as @s rotated ~ 0 run tp @e[type=minecraft:block_display,tag=rlk_mb_proto_part] ~ ~ ~ ~ 0

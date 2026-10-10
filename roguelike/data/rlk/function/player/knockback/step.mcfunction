# Refresh the body position for every substep; only the marker supplies yaw.
scoreboard players set #pkbBlocked tmp 0
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^ ^0.1 run function rlk:player/knockback/check
execute if score #pkbBlocked tmp matches 1 run return run kill @s
# Position-only teleport preserves the body's own yaw and pitch and current Y.
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^ ^0.1 run tp @e[tag=rlk_body,limit=1] ~ ~ ~
scoreboard players remove #pkbSteps tmp 1
execute if score #pkbSteps tmp matches 1.. run function rlk:player/knockback/step

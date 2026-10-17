# @s = rig anchor, at its feet. Once per game tick.
execute unless entity 524c4b4d-4247-4400-8000-000000000007 run function rlk:mboss/guardian/rig/spawn
execute rotated as @s rotated ~ 0 run function rlk:mboss/guardian/rig/follow
scoreboard players add @s gdRigT 1
function rlk:mboss/guardian/rig/run
execute if score @s gdRigF matches 1.. run function rlk:mboss/guardian/rig/flash_tick

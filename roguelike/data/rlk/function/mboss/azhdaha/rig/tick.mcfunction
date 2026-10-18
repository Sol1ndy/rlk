# @s = rig anchor, at its feet. Once per game tick. Missing parts respawn in the rest pose (stored looks and state kept).
execute unless entity 524c4b4d-415a-4400-8000-000000000008 run function rlk:mboss/azhdaha/rig/spawn
execute rotated as @s rotated ~ 0 run function rlk:mboss/azhdaha/rig/follow
scoreboard players add @s azRigT 1
function rlk:mboss/azhdaha/rig/run
execute if score @s azRigF matches 1.. run function rlk:mboss/azhdaha/rig/flash_tick

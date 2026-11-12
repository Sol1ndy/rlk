# @s = rig anchor, at its feet. Once per game tick. Missing parts respawn in the rest pose of the stored form
# (the clip restarts as that form's idle).
execute unless entity 524c4b4d-4246-4c00-8000-000000000002 run function rlk:mboss/butterfly/rig/spawn
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/rig/follow
scoreboard players add @s bfRigT 1
function rlk:mboss/butterfly/rig/run
execute if score @s bfRigF matches 1.. run function rlk:mboss/butterfly/rig/flash_tick

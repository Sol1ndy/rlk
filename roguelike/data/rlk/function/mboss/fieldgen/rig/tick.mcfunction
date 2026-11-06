# @s = rig anchor, at its feet. Once per game tick. Missing parts respawn in the rest pose of the stored form
# (the clip restarts as that form's hold).
execute unless entity 524c4b4d-4647-4400-8000-000000000001 run function rlk:mboss/fieldgen/rig/spawn
execute rotated as @s rotated ~ 0 run function rlk:mboss/fieldgen/rig/follow
scoreboard players add @s fgRigT 1
function rlk:mboss/fieldgen/rig/run
execute if score @s fgRigF matches 1.. run function rlk:mboss/fieldgen/rig/flash_tick

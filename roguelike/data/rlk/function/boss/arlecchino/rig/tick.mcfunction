# @s = the boss (the anchor), at its feet, once per game tick (the core calls it). Missing parts respawn; hidden: only the
# follow runs until a clip is queued (its tick 0 shows the rig again).
execute unless entity 524c4b4d-4b4e-4100-8000-000000000001 run function rlk:boss/arlecchino/rig/spawn
execute rotated as @s rotated ~ 0 run function rlk:boss/arlecchino/rig/follow
execute if score @s knRigF matches 1.. run function rlk:boss/arlecchino/rig/flash_tick
execute if score @s knRigS matches 1 unless score @s knRigT matches -1 run return 0
scoreboard players add @s knRigT 1
function rlk:boss/arlecchino/rig/run

# @s = the boss (the anchor), at its feet, once per game tick (the core calls it). Missing parts respawn; hidden: only the
# follow runs until a clip is queued (its tick 0 shows the rig again).
execute unless entity 524c4b4d-544b-4900-8000-000000000000 run function rlk:boss/tachy/rig/spawn
execute rotated as @s rotated ~ 0 run function rlk:boss/tachy/rig/follow
execute if score @s tkRigF matches 1.. run function rlk:boss/tachy/rig/flash_tick
execute if score @s tkRigS matches 1 unless score @s tkRigT matches -1 run return 0
scoreboard players add @s tkRigT 1
function rlk:boss/tachy/rig/run

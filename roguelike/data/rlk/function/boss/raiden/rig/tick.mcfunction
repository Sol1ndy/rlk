# @s = the boss (the anchor), at its feet, once per game tick. Missing parts respawn.
execute unless entity 524c4b4d-5244-4900-8000-000000000002 run function rlk:boss/raiden/rig/spawn
function rlk:boss/raiden/rig/legacy_anim
execute rotated as @s rotated ~ 0 run function rlk:boss/raiden/rig/follow
execute if score @s rdRigF matches 1.. run scoreboard players remove @s rdRigF 1
execute if score @s rdRigF matches 0 run function rlk:boss/raiden/rig/flash_off
# hidden: nothing runs until a clip is queued (its tick 0 shows the rig again)
execute if score @s rdRigS matches 2 unless score @s rdRigT matches -1 run return 0
scoreboard players add @s rdRigT 1
function rlk:boss/raiden/rig/run

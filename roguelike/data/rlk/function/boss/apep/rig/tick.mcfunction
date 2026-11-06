# @s = rig anchor, at its feet. Once per game tick. Parked (R10): nothing runs. Missing parts respawn in the rest
# pose of the stored form and stance with every stored look.
execute if score @s apRigPark matches 1.. run return 0
execute unless entity 524c4b4d-4150-4400-8000-000000000003 run function rlk:boss/apep/rig/spawn
execute rotated as @s rotated ~ 0 run function rlk:boss/apep/rig/follow
scoreboard players add @s apRigT 1
function rlk:boss/apep/rig/run
execute if score @s apRigF matches 1.. run function rlk:boss/apep/rig/flash_tick

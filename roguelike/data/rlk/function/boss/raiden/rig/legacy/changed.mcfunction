# TEMPORARY: a new rdAnim or rdPhase. The form follows rdPhase (2 Tenma; 0 / 3 Shogun; 1 keeps the transform clip's).
execute unless score @s rdPhase = @s rdRigP if score @s rdPhase matches 2 unless score @s rdAnim matches 9 run function rlk:boss/raiden/rig/state/tenma
execute unless score @s rdPhase = @s rdRigP if score @s rdPhase matches 0 run function rlk:boss/raiden/rig/state/shogun
scoreboard players operation @s rdRigP = @s rdPhase
execute if score @s rdAnim = @s rdRigL run return 0
scoreboard players operation @s rdRigL = @s rdAnim
execute if score @s rdPhase matches 2 run return run function rlk:boss/raiden/rig/legacy/tenma
function rlk:boss/raiden/rig/legacy/shogun

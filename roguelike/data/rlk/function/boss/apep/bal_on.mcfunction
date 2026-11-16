# @s = body: the slot and the library effects cut, the groggy pose of the phase.
function rlk:boss/apep/svc/lib_clear
function rlk:boss/apep/p/cancel
scoreboard players set #apChP mb 0
scoreboard players set #apYawC mb 0
execute if score #apPh mb matches 1 run function rlk:boss/apep/play/idle_p1
execute if score #apPh mb matches 1 run function rlk:boss/apep/rig/tick
execute if score #apPh mb matches 3 run function rlk:boss/apep/rig/stance/upright
execute if score #apPh mb matches 3 run function rlk:boss/apep/play/crouch_p3
function rlk:boss/apep/px/restate
scoreboard players set #apHudQ mb 1

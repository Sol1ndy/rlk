# @s = body, instead of the hook tick while groggy: the clock, the flash, the HUD; the phase-3 bow plays
# out, then the pose holds; stand_p3 in the last ticks.
scoreboard players add #apFc mb 1
execute if score #apFlash mb matches 0.. run function rlk:boss/apep/u/flash
scoreboard players set #apFlash mb -1
function rlk:boss/apep/hud/tick
execute if score #apPh mb matches 3 if score @s grgT matches 14 run function rlk:boss/apep/play/stand_p3
execute if score #apPh mb matches 3 if score @s grgT matches 92.. run function rlk:boss/apep/rig/tick
execute if score #apPh mb matches 3 if score @s grgT matches ..14 run function rlk:boss/apep/rig/tick
execute if score #apPh mb matches 3 if score @s grgT matches 92.. run function rlk:boss/apep/pxs/tick
execute if score #apPh mb matches 3 if score @s grgT matches ..14 run function rlk:boss/apep/pxs/tick

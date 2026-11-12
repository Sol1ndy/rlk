# @s = body, instead of the hook tick while groggy (grgT = ticks left): the rig and the hit flash only.
scoreboard players add #gdT mb 1
execute if score @s grgT matches 34 run function rlk:mboss/guardian/rig/play/groggy_b
execute if score #gdFlash mb matches 1 unless score @s gdRigF matches 1.. run function rlk:mboss/guardian/rig/flash
scoreboard players set #gdFlash mb 0
function rlk:mboss/guardian/rig/tick

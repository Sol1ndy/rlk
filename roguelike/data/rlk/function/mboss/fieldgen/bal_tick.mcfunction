# @s = body, instead of the hook tick while groggy: clock, flash, the rig.
scoreboard players add #fgClk mb 1
execute if score #fgFlash mb matches 1 run function rlk:mboss/fieldgen/rig/flash
scoreboard players set #fgFlash mb 0
function rlk:mboss/fieldgen/rig/tick

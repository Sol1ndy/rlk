# @s = body, instead of the hook tick while groggy: the clock, the hit flash, the HUD (the pose holds).
scoreboard players add #azClk mb 1
execute if score #azFlash mb matches 1.. run function rlk:boss/azhdaha/u/flash
scoreboard players set #azFlash mb 0
function rlk:boss/azhdaha/hud/tick

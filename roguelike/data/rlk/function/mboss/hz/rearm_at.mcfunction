# @s = a #hzRearm hazard that is disarmed now: armed again when the re-arm clock #mbHzClk reaches mbHzRT.
scoreboard players operation @s mbHzRT = #mbHzClk mb
scoreboard players operation @s mbHzRT += @s mbHzRA

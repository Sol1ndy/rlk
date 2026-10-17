# @s = prop, at/rotated as @s. Moves in 0.25-block sub-steps (speed rounded up to 0.25 b/t).
scoreboard players add @s mbPjT 1
execute if score @s mbPjRet matches 2 run return run function rlk:mboss/pj/back
execute if score @s mbPjT > @s mbPjL run return run function rlk:mboss/pj/stop {ev:2}
scoreboard players operation #pjN mb = @s mbPjV
scoreboard players operation #pjN mb *= #c4 mb
scoreboard players add #pjN mb 9
scoreboard players operation #pjN mb /= #c10 mb
execute if score #pjN mb matches ..0 run scoreboard players set #pjN mb 1
scoreboard players set #pjStop mb 0
execute store result storage rlk:mboss pjp.hr int 1 run scoreboard players get @s mbPjR
function rlk:mboss/pj/step
execute if score #pjStop mb matches 1 run function rlk:mboss/pj/stop {ev:1}

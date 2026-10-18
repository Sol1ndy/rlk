# Human rotation again: 4 patterns before the next transformation (no time limit), starting with
# pattern 2 (the video goes straight into 달빛 점프).
scoreboard players set #bfHumN mb 0
scoreboard players set #bfHumLim mb 4
scoreboard players set #bfHumT mb 0
scoreboard players set #bfHumTL mb 0
execute if score #mbLock mb matches 0 run scoreboard players set #bfReq mb 2
scoreboard players set #bfCool mb 4
function rlk:mboss/butterfly/ai/enter

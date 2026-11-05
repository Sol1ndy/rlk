# Every 4th hit taken in recovery: the flinch clip (6 t, no step).
scoreboard players set #flq hr 0
execute unless score #pat hr matches 0 run return 0
scoreboard players set #ai_fl hr 6
function rlk:boss/scarlet/rig/play/flinch

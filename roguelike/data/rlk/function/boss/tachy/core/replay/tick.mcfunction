scoreboard players add #sq tk 1
function rlk:boss/tachy/core/sq/intro/tick
execute if score #sqdone tk matches 1 run return run function rlk:boss/tachy/core/replay/end
execute if score #sq tk matches 186.. run function rlk:boss/tachy/core/replay/end

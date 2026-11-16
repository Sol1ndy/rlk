# From p/finish: the state that owns the slot continues (unless it already moved on at the pattern's release).
execute if score #gdPRel mb matches 1 run return 0
execute if score #gdSt mb matches 3 run return run function rlk:mboss/guardian/guard/after
execute if score #gdSt mb matches 4 run return run scoreboard players set #gdFailDone mb 1
function rlk:mboss/guardian/ai/recover

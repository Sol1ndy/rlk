# @s = body. One AI state per tick (the pattern slot runs after it, see p/run).
execute if score #gdSt mb matches 0 run return run function rlk:mboss/guardian/ai/idle
execute if score #gdSt mb matches 2 run return run function rlk:mboss/guardian/ai/close
execute if score #gdSt mb matches 3 run return run function rlk:mboss/guardian/guard/tick
execute if score #gdSt mb matches 4 run return run function rlk:mboss/guardian/chaos/tick
execute if score #gdSt mb matches 5 run return run function rlk:mboss/guardian/groggy/tick
execute if score #gdSt mb matches 6 run return run function rlk:mboss/guardian/ai/approach
execute if score #gdSt mb matches 8 run return run function rlk:mboss/guardian/ai/back

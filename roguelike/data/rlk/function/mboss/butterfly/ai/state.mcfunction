# @s = body. One AI state per tick (the pattern slot runs after it, see p/run).
execute if score #bp4B mb matches 1.. run function rlk:mboss/butterfly/p/vacuum/blades
execute if score #bfSt mb matches 0 run return run function rlk:mboss/butterfly/ai/idle
execute if score #bfSt mb matches 2 run return run function rlk:mboss/butterfly/ai/close
execute if score #bfSt mb matches 3 run return run function rlk:mboss/butterfly/groggy/tick
execute if score #bfSt mb matches 4 run return run function rlk:mboss/butterfly/recover/tick
execute if score #bfSt mb matches 5 run return run function rlk:mboss/butterfly/ai/prep

# A slot pattern finished (#bfPDone = its id): recovery before the next decision.
scoreboard players set #bfCool mb 20
execute if score #bfPDone mb matches 1 run scoreboard players set #bfCool mb 16
execute if score #bfPDone mb matches 2 run scoreboard players set #bfCool mb 16
execute if score #bfPDone mb matches 3 run scoreboard players set #bfCool mb 16
execute if score #bfPDone mb matches 4 run scoreboard players set #bfCool mb 18
execute if score #bfPDone mb matches 11 run scoreboard players set #bfCool mb 18
execute if score #bfPDone mb matches 12 run scoreboard players set #bfCool mb 20
execute if score #bfPDone mb matches 13 run scoreboard players set #bfCool mb 18
execute if score #bfPDone mb matches 14 run scoreboard players set #bfCool mb 20
execute if score #bfPDone mb matches 15 run scoreboard players set #bfCool mb 0
execute if score #bfPDone mb matches 20 run scoreboard players set #bfCool mb 0
function rlk:mboss/butterfly/ai/enter

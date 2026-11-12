# A slot pattern finished (#gdPDone = its id): recovery before the next decision.
scoreboard players set #gdCool mb 20
execute if score #gdPDone mb matches 1 run scoreboard players set #gdCool mb 18
execute if score #gdPDone mb matches 2 run scoreboard players set #gdCool mb 20
execute if score #gdPDone mb matches 3 run scoreboard players set #gdCool mb 20
execute if score #gdPDone mb matches 4 run scoreboard players set #gdCool mb 22
execute if score #gdPDone mb matches 5 run scoreboard players set #gdCool mb 22
execute if score #gdPDone mb matches 11 run scoreboard players set #gdCool mb 20
execute if score #gdPDone mb matches 12 run scoreboard players set #gdCool mb 20
execute if score #gdPDone mb matches 13 run scoreboard players set #gdCool mb 20
function rlk:mboss/guardian/ai/enter

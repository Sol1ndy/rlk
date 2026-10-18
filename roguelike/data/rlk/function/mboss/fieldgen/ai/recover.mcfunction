# A slot pattern finished (#fgPDone = its id): recovery before the next decision.
scoreboard players set #fgCool mb 20
execute if score #fgPDone mb matches 1 run scoreboard players set #fgCool mb 20
execute if score #fgPDone mb matches 2 run scoreboard players set #fgCool mb 20
execute if score #fgPDone mb matches 3 run scoreboard players set #fgCool mb 20
execute if score #fgPDone mb matches 4 run scoreboard players set #fgCool mb 20
execute if score #fgPDone mb matches 5 run scoreboard players set #fgCool mb 20
execute if score #fgPDone mb matches 6 run scoreboard players set #fgCool mb 20
execute if score #fgPDone mb matches 11 run scoreboard players set #fgCool mb 14
execute if score #fgPDone mb matches 12 run scoreboard players set #fgCool mb 14
execute if score #fgPDone mb matches 21 run scoreboard players set #fgCool mb 0
execute if score #fgPDone mb matches 20 run scoreboard players set #fgCool mb 0
execute if score #fgPDone mb matches 22 run scoreboard players set #fgCool mb 20
function rlk:mboss/fieldgen/ai/enter

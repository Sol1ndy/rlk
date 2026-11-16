# @s = body. A main-slot pattern finished (#azPDone): a transition step advances; else the recovery, the
# cooldown, the FLANK skip-once, P8 + turn180 when the player is still behind.
execute if score #azPDone mb matches 20..23 if score #azTr mb matches 2.. run return run function rlk:boss/azhdaha/tr/next
execute if score #azPDone mb matches 30 if score #azTr mb matches 2 run return run function rlk:boss/azhdaha/tr/next
scoreboard players set #azCool mb 20
scoreboard players set #azCastFirst mb 0
execute if score #azPDone mb matches 1 run scoreboard players set #azCool mb 18
execute if score #azPDone mb matches 2 run scoreboard players set #azCool mb 16
execute if score #azPDone mb matches 3 run scoreboard players set #azCool mb 30
execute if score #azPDone mb matches 4 run scoreboard players set #azCool mb 20
execute if score #azPDone mb matches 5 run scoreboard players set #azCool mb 18
execute if score #azPDone mb matches 10 run scoreboard players set #azCool mb 20
execute if score #azPDone mb matches 6 run scoreboard players set #azCool mb 14
execute if score #azPDone mb matches 7 run scoreboard players set #azCool mb 18
execute if score #azPDone mb matches 8 run scoreboard players set #azCool mb 18
execute if score #azPDone mb matches 9 run scoreboard players set #azCool mb 24
execute if score #azPDone mb matches 31 run scoreboard players set #azCool mb 30
execute if score #azPDone mb matches 32 run scoreboard players set #azCool mb 30
execute if score #azPDone mb matches 41 run scoreboard players set #azCool mb 18
execute if score #azPDone mb matches 42 run scoreboard players set #azCool mb 18
execute if score #azPDone mb matches 43 run scoreboard players set #azCool mb 18
execute if score #azPDone mb matches 44 run scoreboard players set #azCool mb 20
execute if score #azPDone mb matches 45 run scoreboard players set #azCool mb 20
execute if score #azPDone mb matches 46 run scoreboard players set #azCool mb 20
execute if score #azPDone mb matches 20 run scoreboard players set #azCool mb 20
execute if score #azPDone mb matches 21 run scoreboard players set #azCool mb 10
execute if score #azPDone mb matches 22 run scoreboard players set #azCool mb 0
execute if score #azPDone mb matches 23 run scoreboard players set #azCool mb 16
execute if score #azPDone mb matches 27 run scoreboard players set #azCool mb 4
execute if score #azPDone mb matches 28 run scoreboard players set #azCool mb 0
execute if score #azPDone mb matches 30 run scoreboard players set #azCool mb 30
execute if score #azPDone mb matches 9 run scoreboard players operation #azCdE9 mb = #azClk mb
execute if score #azPDone mb matches 9 run scoreboard players add #azCdE9 mb 600
execute if score #azPDone mb matches 44 run scoreboard players operation #azCdE44 mb = #azClk mb
execute if score #azPDone mb matches 44 run scoreboard players add #azCdE44 mb 400
execute if score #azPDone mb matches 2 run scoreboard players set #azSkipF mb 1
execute if score #azPDone mb matches 7 run scoreboard players set #azSkipF mb 1
execute if score #azPDone mb matches 8 run scoreboard players set #azSkipF mb 1
execute if score #azPDone mb matches 9 run scoreboard players set #azSkipF mb 1
execute if score #azPDone mb matches 20 run scoreboard players set #azSkipF mb 1
execute if score #azPDone mb matches 21 run scoreboard players set #azSkipF mb 1
execute if score #azPDone mb matches 22 run scoreboard players set #azSkipF mb 1
execute if score #azPDone mb matches 23 run scoreboard players set #azSkipF mb 1
execute if score #azPDone mb matches 8 run function rlk:boss/azhdaha/ai/p8_turn

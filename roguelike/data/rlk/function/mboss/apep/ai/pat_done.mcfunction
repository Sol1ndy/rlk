# @s = body. A main-slot pattern finished (#apPDone): the opener hand-over, the recover, the cooldown, the counts
# (patterns of the fight, phase-3 patterns, Q2 bookkeeping), the chain roll (never after a chain), the rest set.
execute if score #apNext mb matches 1.. run return run function rlk:mboss/apep/ai/next_go
scoreboard players set #apCool mb 20
execute if score #apPDone mb matches 1 run scoreboard players set #apCool mb 40
execute if score #apPDone mb matches 4 run scoreboard players set #apCool mb 10
execute if score #apPDone mb matches 5 run scoreboard players set #apCool mb 15
execute if score #apPDone mb matches 7 run scoreboard players set #apCool mb 0
execute if score #apPDone mb matches 34 run scoreboard players set #apCool mb 18
execute if score #apPDone mb matches 32 run scoreboard players set #apCool mb 16
execute if score #apPDone mb matches 20 run scoreboard players set #apCool mb 1
execute if score #apPDone mb matches 40 run scoreboard players set #apCool mb 1
execute if score #apPDone mb matches 10 run scoreboard players set #apCool mb 6
execute if score #apPDone mb matches 61 run scoreboard players set #apCool mb 6
execute if score #apPDone mb matches 1 run scoreboard players operation #apCdE1 mb = #apFc mb
execute if score #apPDone mb matches 1 run scoreboard players add #apCdE1 mb 400
execute if score #apPDone mb matches 3 run scoreboard players operation #apCdE3 mb = #apFc mb
execute if score #apPDone mb matches 3 run scoreboard players add #apCdE3 mb 700
execute if score #apPDone mb matches 5 run scoreboard players operation #apCdE5 mb = #apFc mb
execute if score #apPDone mb matches 5 run scoreboard players add #apCdE5 mb 200
execute if score #apPDone mb matches 1 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 2 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 3 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 4 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 5 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 6 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 31 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 33 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 34 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 35 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 36 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 32 run scoreboard players add #apPatN mb 1
execute if score #apPDone mb matches 31 run scoreboard players add #apP3N mb 1
execute if score #apPDone mb matches 33 run scoreboard players add #apP3N mb 1
execute if score #apPDone mb matches 34 run scoreboard players add #apP3N mb 1
execute if score #apPDone mb matches 35 run scoreboard players add #apP3N mb 1
execute if score #apPDone mb matches 32 run scoreboard players add #apP3N mb 1
# Q2 (plan 7.4): the first-cast flag, the clock, the count of other patterns since
execute if score #apPDone mb matches 31 run scoreboard players add #apAftN mb 1
execute if score #apPDone mb matches 33 run scoreboard players add #apAftN mb 1
execute if score #apPDone mb matches 34 run scoreboard players add #apAftN mb 1
execute if score #apPDone mb matches 35 run scoreboard players add #apAftN mb 1
execute if score #apPDone mb matches 32 run scoreboard players set #apAft1 mb 1
execute if score #apPDone mb matches 32 run scoreboard players set #apAftN mb 0
execute if score #apPDone mb matches 32 run scoreboard players operation #apAftCd mb = #apFc mb
execute if score #apPDone mb matches 32 run scoreboard players add #apAftCd mb 900
# chains: rolled after a pattern that names some, unless it ran as a chain itself (never two in a row)
execute if score #apPDone mb matches 33 unless score #apChainRun mb matches 1 run function rlk:mboss/apep/ai/chain_33
execute if score #apPDone mb matches 35 unless score #apChainRun mb matches 1 run function rlk:mboss/apep/ai/chain_35
scoreboard players set #apChainRun mb 0
execute if score #apPh mb matches 1 run function rlk:mboss/apep/svc/px_rest
execute if score #apPh mb matches 3 run function rlk:mboss/apep/svc/px_rest

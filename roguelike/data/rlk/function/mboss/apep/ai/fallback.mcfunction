# Nothing allowed here: phase 1 a crab-turn step (not after a move), else idle 10 t.
execute if score #apPh mb matches 1 unless score #apLastMv mb matches 1 run return run function rlk:mboss/apep/ai/step_go
scoreboard players set #apCool mb 10

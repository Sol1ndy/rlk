# A hit reached the floor (#mbFloorHit, framework) or her HP sits on it (@s = body): the step is reserved for the next
# decision (#fl 1 CS1 in P1, 2 lead5 in P2); a running pattern finishes first, a groggy is cut to its kip-up (bal_tick).
scoreboard players set #mbFloorHit mb 0
execute unless score #fl hr matches 0 run return 0
execute if score #ph hr matches 1 run return run scoreboard players set #fl hr 1
execute if score #ph hr matches 7 run scoreboard players set #fl hr 2

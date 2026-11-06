# A hit reached the floor (#mbFloorHit, framework) or her HP sits on it (@s = body): the step is reserved for the next
# decision (#fl 1 CS1 in P1, 2 the A13 lead-in in P2); in the down window lead_down follows 40 t later (#flw).
scoreboard players set #mbFloorHit mb 0
execute unless score #fl hr matches 0 run return 0
execute if score #ph hr matches 1 run return run scoreboard players set #fl hr 1
execute if score #ph hr matches 6 if score #kip hr matches 0 run scoreboard players set #flw hr 40
execute if score #ph hr matches 6 run return run scoreboard players set #fl hr 2
execute if score #ph hr matches 7 run scoreboard players set #fl hr 2

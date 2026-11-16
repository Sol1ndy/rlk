# A hit reached the floor (#mbFloorHit, framework) or her HP sits on it (DoTs, reactions; @s = body): the phase step
# is reserved for the next decision (#fl 1 = E70 in P1a, 2 = T in P1b). Nothing else changes now.
scoreboard players set #mbFloorHit mb 0
execute unless score #fl kn matches 0 run return 0
execute if score #ph kn matches 1 if score #e70 kn matches 0 run return run scoreboard players set #fl kn 1
execute if score #ph kn matches 3 run scoreboard players set #fl kn 2

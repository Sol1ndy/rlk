# The framework clamped a hit at #mbFloor (#mbFloorHit 1): the phase step is reserved for the next decision
# (#flnext 1 = M1 -> T1 -> P2 at 70 %, 2 = M2 -> T2 -> P3 at 35 %). The floor stays until the mantle moves it.
# R (TK-01): while M1 is only reserved (#fl 1, still P1) the floor is the 70 % one: more hits on it change nothing
# (they used to reserve the 35 % step as well, so M1 / T1 / P2 were skipped); the 35 % step counts from M1 on.
scoreboard players set #mbFloorHit mb 0
execute if score #fl tk matches 1 if score #ph tk matches 2.. run return run function rlk:boss/tachy/core/floor_2
execute if score #fl tk matches 1.. run return 0
execute if score #fl tk matches 0 run scoreboard players set #flnext tk 1
execute if score #fl tk matches 0 run scoreboard players set #fl tk 1

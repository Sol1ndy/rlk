# The framework clamped a hit at #mbFloor (#mbFloorHit 1): the phase step is reserved for the next decision
# (#flnext 1 = M1 -> T1 -> P2 at 70 %, 2 = M2 -> T2 -> P3 at 35 %). The floor stays until the mantle moves it.
scoreboard players set #mbFloorHit mb 0
execute if score #fl tk matches 1 run return run function rlk:boss/tachy/core/floor_2
execute if score #fl tk matches 0 run scoreboard players set #flnext tk 1
execute if score #fl tk matches 0 run scoreboard players set #fl tk 1

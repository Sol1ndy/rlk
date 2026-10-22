# B3 special start (s2.md 7.2; from the B3 frame at B3_TAILUP): 41 frost (Cryo tail) / 42 bolt (Electro tail).
execute if score #azTail mb matches 4 run scoreboard players set #azB3Sp mb 41
execute if score #azTail mb matches 3 run scoreboard players set #azB3Sp mb 42
execute if score #azB3Sp mb matches 41 run return run function rlk:boss/azhdaha/p/frost/start
execute if score #azB3Sp mb matches 42 run return run function rlk:boss/azhdaha/p/bolt/start

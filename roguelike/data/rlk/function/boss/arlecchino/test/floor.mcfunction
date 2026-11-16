# Test 80: HP = the next floor + 1 (P1a: the 70 % floor, P1b: 1, P2: 0).
execute if score #mbSt mb matches 0 run function rlk:boss/arlecchino/core/intro/done
execute if score #ph kn matches 1 run scoreboard players operation @s mhpC = #fl70 kn
execute if score #ph kn matches 3 run scoreboard players set @s mhpC 1
execute if score #ph kn matches 5 run scoreboard players set @s mhpC 0
scoreboard players add @s mhpC 1

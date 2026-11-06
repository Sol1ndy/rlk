# Test 80: HP = the next floor + 1 (P1: 60 %, later 5 %).
execute if score #mbSt mb matches 0 run function rlk:boss/scarlet/core/intro/done
execute if score #ph hr matches 1 run scoreboard players operation @s mhpC = #fl60 hr
execute unless score #ph hr matches 1 run scoreboard players operation @s mhpC = #fl5 hr
scoreboard players add @s mhpC 1

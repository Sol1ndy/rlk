# Test 34: HP = the 5 % floor + 1.
execute if score #mbSt mb matches 0 run function rlk:boss/scarlet/core/intro/done
scoreboard players operation @s mhpC = #fl5 hr
scoreboard players add @s mhpC 1

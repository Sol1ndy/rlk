# Test 80: HP = the next floor + 1.
execute if score #mbSt mb matches 0 run function rlk:boss/tachy/core/intro/done
execute if score #fl tk matches 0 run scoreboard players operation @s mhpC = #fl70 tk
execute if score #fl tk matches 1 run scoreboard players operation @s mhpC = #fl35 tk
execute if score #fl tk matches ..1 run scoreboard players add @s mhpC 1

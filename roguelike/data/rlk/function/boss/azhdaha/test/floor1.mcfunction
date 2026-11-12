# 80: HP to the current floor + 1 (the next hit queues the transition).
scoreboard players operation @s mhpC = #mbFloor mb
scoreboard players add @s mhpC 1

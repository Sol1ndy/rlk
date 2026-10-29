# The HP floors (absolute HP) of the 70 % and 35 % phase steps from the max HP (@s = body; one pool, phases [100]).
scoreboard players operation #fl70 tk = @s mhpM
scoreboard players operation #fl70 tk /= #c100 tk
scoreboard players set #t tk 70
scoreboard players operation #fl70 tk *= #t tk
execute if score #fl70 tk matches ..0 run scoreboard players set #fl70 tk 1
scoreboard players operation #fl35 tk = @s mhpM
scoreboard players operation #fl35 tk /= #c100 tk
scoreboard players set #t tk 35
scoreboard players operation #fl35 tk *= #t tk
execute if score #fl35 tk matches ..0 run scoreboard players set #fl35 tk 1

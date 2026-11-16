# The 70 % floor (absolute HP) of the P1 pool (@s = body; the pool is phases[0] of the total).
scoreboard players operation #fl70 kn = @s mhpM
scoreboard players operation #fl70 kn /= #c100 kn
scoreboard players set #t kn 70
scoreboard players operation #fl70 kn *= #t kn
execute if score #fl70 kn matches ..1 run scoreboard players set #fl70 kn 2

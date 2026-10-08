scoreboard players operation #t2 tmp = @s elemMastery
scoreboard players remove #t2 tmp 300
execute if score #t2 tmp matches ..0 run return 0
scoreboard players operation #t2 tmp /= #c10 tmp
execute if score #t2 tmp matches 51.. run scoreboard players set #t2 tmp 50
scoreboard players operation #t1 tmp += #t2 tmp

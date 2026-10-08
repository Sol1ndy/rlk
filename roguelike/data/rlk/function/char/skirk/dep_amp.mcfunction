scoreboard players operation #t1 tmp = @s skDepB
scoreboard players add #t1 tmp 100
scoreboard players operation #dmg tmp *= #t1 tmp
scoreboard players operation #dmg tmp /= #100 tmp
scoreboard players set #skDepUsed tmp 1
